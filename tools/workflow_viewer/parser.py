"""将 workflow YAML 转换为简洁的 HTML 查看器数据。"""

from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


LAYOUT_PADDING_X = 96
LAYOUT_PADDING_Y = 88
LAYOUT_LAYER_GAP = 96
LAYOUT_NODE_GAP = 20
LAYOUT_TITLE_CHARS_PER_LINE = 16
LAYOUT_META_CHARS_PER_LINE = 24
NODE_MIN_WIDTH = 170
NODE_MAX_WIDTH = 230
CONCLUSION_MIN_WIDTH = 170
CONCLUSION_MAX_WIDTH = 240

GROUP_RULES = [
    (0, 6, "基础连通性", "Ping 命令、MTU、二层连通性、物理链路"),
    (7, 10, "路由与策略路由", "直连路由、流策略、重定向、ACL 关联"),
    (11, 18, "ARP / MAC / 二层阻断", "ARP 学习、MAC 出接口、二层阻塞"),
    (19, 21, "cpu-defend 黑名单", "防攻击策略、黑名单、ACL 命中"),
    (22, 30, "ICMP 统计与 CPCAR", "收发统计、流量统计、限速调整"),
    (31, 34, "抓包分析", "端口镜像、流镜像、capture 抓包"),
    (35, 36, "日志收尾", "日志收集、文件保存"),
]


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _safe_relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _estimate_lines(text: Any, chars_per_line: int) -> int:
    normalized = _normalize_text(text)
    if not normalized:
        return 0
    return max(1, math.ceil(len(normalized) / max(chars_per_line, 1)))


def _step_number(step_id: str) -> int:
    if not step_id.startswith("step_"):
        return 10_000
    parts = step_id.split("_", 2)
    try:
        return int(parts[1])
    except (IndexError, ValueError):
        return 10_000


def _group_for_step(step_id: str) -> dict[str, str]:
    number = _step_number(step_id)
    for start, end, title, description in GROUP_RULES:
        if start <= number <= end:
            return {
                "id": f"group_{start:02d}_{end:02d}",
                "title": title,
                "description": description,
                "range": f"step_{start} ~ step_{end}",
            }
    return {
        "id": "group_misc",
        "title": "其他",
        "description": "未归类节点",
        "range": "misc",
    }


def _load_latest_issue_report(report_root: Path) -> dict[str, Any] | None:
    if not report_root.exists():
        return None
    candidates = sorted(report_root.glob("*/report.json"))
    if not candidates:
        return None
    latest = candidates[-1]
    try:
        return json.loads(latest.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _build_issue_summary(issue_report: dict[str, Any] | None) -> tuple[dict[str, dict[str, int]], dict[str, int]]:
    by_node: dict[str, dict[str, int]] = defaultdict(lambda: {"critical": 0, "warning": 0, "info": 0})
    global_counts = {"critical": 0, "warning": 0, "info": 0}
    if not issue_report:
        return {}, global_counts
    for item in issue_report.get("issues", []):
        severity = item.get("severity", "warning")
        step_id = item.get("step_id") or "workflow"
        if step_id == "workflow":
            global_counts[severity] = global_counts.get(severity, 0) + 1
            continue
        by_node[step_id][severity] = by_node[step_id].get(severity, 0) + 1
    return dict(by_node), global_counts


def _summarize_transitions(transitions: dict[str, Any]) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for rule in transitions.get("rules", []) or []:
        summary.append(
            {
                "route_type": "rule",
                "description": rule.get("description", ""),
                "condition": rule.get("condition", ""),
                "next_node": rule.get("next_node", ""),
            }
        )
    on_error = transitions.get("on_error") or {}
    for key, target in on_error.items():
        summary.append(
            {
                "route_type": "on_error",
                "description": key,
                "condition": "",
                "next_node": target or "",
            }
        )
    if transitions.get("default"):
        summary.append(
            {
                "route_type": "default",
                "description": "default",
                "condition": "",
                "next_node": transitions.get("default"),
            }
        )
    return summary


def _estimate_step_box(node: dict[str, Any]) -> tuple[int, int]:
    title = _normalize_text(node.get("title") or node.get("id"))
    type_label = _normalize_text(node.get("type_label"))
    issue_total = int(node.get("issue_total") or 0)
    badge_count = 1  # 状态
    if issue_total:
        badge_count += 1
    if node.get("group_title"):
        badge_count += 1
    badge_rows = max(1, math.ceil(badge_count / 2))

    title_lines = min(2, _estimate_lines(title, LAYOUT_TITLE_CHARS_PER_LINE)) or 1
    meta_lines = 1 if type_label else 0

    width = 160 + max(len(title) - 10, 0) * 3.0
    width = int(min(max(width, NODE_MIN_WIDTH), NODE_MAX_WIDTH))
    height = 20 + title_lines * 18 + meta_lines * 12 + badge_rows * 16
    return width, max(height, 80)


def _estimate_conclusion_box(node: dict[str, Any]) -> tuple[int, int]:
    title = _normalize_text(node.get("title") or node.get("id"))
    level = _normalize_text(node.get("level"))
    issue_total = int(node.get("issue_total") or 0)
    badge_count = 1
    if issue_total:
        badge_count += 1
    if node.get("repair_action"):
        badge_count += 1
    if level:
        badge_count += 1
    badge_rows = max(1, math.ceil(badge_count / 2))

    title_lines = min(2, _estimate_lines(title, 16)) or 1

    width = 160 + max(len(title) - 10, 0) * 3.0
    width = int(min(max(width, CONCLUSION_MIN_WIDTH), CONCLUSION_MAX_WIDTH))
    height = 20 + title_lines * 18 + badge_rows * 16
    return width, max(height, 78)


def _assign_layers(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], start_nodes: list[str]) -> dict[str, int]:
    node_ids = {node["id"] for node in nodes}
    incoming: dict[str, list[str]] = defaultdict(list)
    valid_edges: list[tuple[str, str]] = []
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        if source in node_ids and target in node_ids:
            incoming[target].append(source)
            valid_edges.append((source, target))

    layer_map: dict[str, int] = {}
    for start in start_nodes:
        if start in node_ids:
            layer_map[start] = 0

    if not layer_map:
        for node in nodes:
            if not incoming.get(node["id"]):
                layer_map[node["id"]] = 0

    for _ in range(max(len(nodes), 1) * 2):
        changed = False
        for source, target in valid_edges:
            if source not in layer_map:
                continue
            candidate = layer_map[source] + 1
            if candidate > layer_map.get(target, -1):
                layer_map[target] = candidate
                changed = True
        if not changed:
            break

    fallback_base = max(layer_map.values(), default=0)
    for node in sorted(nodes, key=lambda item: (0 if item["kind"] == "step" else 1, item.get("order", 99999), item["id"])):
        node_id = node["id"]
        if node_id in layer_map:
            continue
        predecessors = [layer_map[src] for src in incoming.get(node_id, []) if src in layer_map]
        if predecessors:
            layer_map[node_id] = max(predecessors) + 1
        else:
            layer_map[node_id] = fallback_base + 1

    compact = {raw: index for index, raw in enumerate(sorted(set(layer_map.values())))}
    return {node_id: compact[layer] for node_id, layer in layer_map.items()}


def _layout_graph(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], start_nodes: list[str]) -> dict[str, Any]:
    node_by_id = {node["id"]: node for node in nodes}
    for node in nodes:
        if node["kind"] == "step":
            width, height = _estimate_step_box(node)
        else:
            width, height = _estimate_conclusion_box(node)
        node["graph_size"] = {"width": width, "height": height}

    layer_map = _assign_layers(nodes, edges, start_nodes)
    layered_nodes: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        layer = layer_map.get(node["id"], 0)
        node["graph_layer"] = layer
        layered_nodes[layer].append(node)

    def sort_key(node: dict[str, Any]) -> tuple[int, int, int, str]:
        return (
            0 if node["kind"] == "step" else 1,
            int(node.get("issue_total") or 0) * -1,
            int(node.get("order") or 99999),
            node["id"],
        )

    layer_widths: dict[int, int] = {}
    layer_heights: dict[int, int] = {}
    ordered_layers = sorted(layered_nodes)
    for layer in ordered_layers:
        layer_nodes = sorted(layered_nodes[layer], key=sort_key)
        layered_nodes[layer] = layer_nodes
        width = max((node["graph_size"]["width"] for node in layer_nodes), default=NODE_MIN_WIDTH)
        height = sum(node["graph_size"]["height"] for node in layer_nodes)
        if layer_nodes:
            height += LAYOUT_NODE_GAP * (len(layer_nodes) - 1)
        layer_widths[layer] = width
        layer_heights[layer] = max(height, 1)

    max_height = max(layer_heights.values(), default=0)
    x_cursor = LAYOUT_PADDING_X
    layout_nodes = []
    for layer in ordered_layers:
        column_width = layer_widths[layer]
        column_height = layer_heights[layer]
        column_top = LAYOUT_PADDING_Y + (max_height - column_height) / 2
        y_cursor = column_top
        for node in layered_nodes[layer]:
            width = node["graph_size"]["width"]
            height = node["graph_size"]["height"]
            node["graph_layout"] = {
                "x": round(x_cursor + (column_width - width) / 2, 1),
                "y": round(y_cursor, 1),
                "width": width,
                "height": height,
                "center_x": round(x_cursor + column_width / 2, 1),
                "center_y": round(y_cursor + height / 2, 1),
                "layer": layer,
            }
            y_cursor += height + LAYOUT_NODE_GAP
            layout_nodes.append(node)
        x_cursor += column_width + LAYOUT_LAYER_GAP

    graph_width = int(x_cursor - LAYOUT_LAYER_GAP + LAYOUT_PADDING_X)
    graph_height = int(max_height + LAYOUT_PADDING_Y * 2)

    outgoing_count: dict[str, int] = defaultdict(int)
    outgoing_entries_by_source: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    outgoing_pairs_by_source: dict[str, dict[str, list[tuple[int, dict[str, Any]]]]] = defaultdict(lambda: defaultdict(list))
    for edge in edges:
        if edge["source"] in node_by_id and edge["target"] in node_by_id:
            outgoing_count[edge["source"]] += 1
    for edge_index, edge in enumerate(edges):
        if edge["source"] in node_by_id and edge["target"] in node_by_id:
            outgoing_entries_by_source[edge["source"]].append((edge_index, edge))
            outgoing_pairs_by_source[edge["source"]][edge["target"]].append((edge_index, edge))

    edge_lane_lookup: dict[int, tuple[int, int]] = {}
    edge_pair_lookup: dict[int, tuple[int, int, int, int]] = {}
    for source, entries in outgoing_entries_by_source.items():
        entries.sort(
            key=lambda item: (
                item[1]["target"],
                item[1].get("route_type", ""),
                item[1].get("description", ""),
                item[0],
            )
        )
        total = len(entries)
        for lane_index, (edge_index, _) in enumerate(entries):
            edge_lane_lookup[edge_index] = (lane_index, total)
        pair_targets = sorted(outgoing_pairs_by_source[source])
        pair_total = len(pair_targets)
        for pair_index, target in enumerate(pair_targets):
            pair_entries = outgoing_pairs_by_source[source][target]
            pair_entries.sort(
                key=lambda item: (
                    item[1].get("route_type", ""),
                    item[1].get("description", ""),
                    item[0],
                )
            )
            pair_lane_total = len(pair_entries)
            for pair_lane_index, (edge_index, _) in enumerate(pair_entries):
                edge_pair_lookup[edge_index] = (pair_index, pair_total, pair_lane_index, pair_lane_total)

    graph_edges: list[dict[str, Any]] = []
    for edge_index, edge in enumerate(edges):
        source = node_by_id.get(edge["source"])
        target = node_by_id.get(edge["target"])
        source_exists = bool(source)
        target_exists = bool(target)
        if not source_exists:
            continue

        edge_record = {
            **edge,
            "id": f"edge_{edge_index:03d}",
            "source_exists": source_exists,
            "target_exists": target_exists,
            "route_type": edge.get("route_type", "rule"),
            "route_label": edge.get("route_label", ""),
            "path": "",
            "label_x": 0,
            "label_y": 0,
        }

        if source_exists and target_exists:
            source_layout = source["graph_layout"]
            target_layout = target["graph_layout"]
            slot, total = edge_lane_lookup.get(edge_index, (0, outgoing_count.get(edge["source"], 1)))
            pair_index, pair_total, pair_lane_index, pair_lane_total = edge_pair_lookup.get(edge_index, (slot, total, 0, 1))
            pair_unit = max(26.0, min(source_layout["height"], target_layout["height"]) * 0.24)
            inner_unit = max(16.0, min(source_layout["height"], target_layout["height"]) * 0.14)
            branch_offset = (pair_index - (pair_total - 1) / 2) * pair_unit
            branch_offset += (pair_lane_index - (pair_lane_total - 1) / 2) * inner_unit

            source_x = source_layout["x"] + source_layout["width"]
            source_y = source_layout["center_y"] + branch_offset
            target_x = target_layout["x"]
            target_y = target_layout["center_y"] + branch_offset * 0.52
            delta_x = target_x - source_x
            bend = max(72.0, abs(delta_x) * 0.52)
            direction = 1 if delta_x >= 0 else -1
            c1_x = source_x + direction * bend
            c2_x = target_x - direction * bend
            edge_record["path"] = (
                f"M {source_x:.1f} {source_y:.1f} "
                f"C {c1_x:.1f} {source_y:.1f}, {c2_x:.1f} {target_y:.1f}, {target_x:.1f} {target_y:.1f}"
            )
            pair_bias_x = (pair_index - (pair_total - 1) / 2) * 18
            pair_bias_y = (pair_index - (pair_total - 1) / 2) * 10
            local_bias_x = (pair_lane_index - (pair_lane_total - 1) / 2) * 14
            local_bias_y = (pair_lane_index - (pair_lane_total - 1) / 2) * 16
            edge_record["label_x"] = round((source_x + target_x) / 2 + pair_bias_x + local_bias_x, 1)
            edge_record["label_y"] = round((source_y + target_y) / 2 - 12 + pair_bias_y + local_bias_y, 1)
            edge_record["lane_index"] = slot
            edge_record["lane_total"] = total
            edge_record["pair_index"] = pair_index
            edge_record["pair_total"] = pair_total
            edge_record["pair_lane_index"] = pair_lane_index
            edge_record["pair_lane_total"] = pair_lane_total
            edge_record["route_span"] = max(1, total)

        graph_edges.append(edge_record)

    for node in layout_nodes:
        incoming_edges = [edge for edge in graph_edges if edge["target"] == node["id"] and edge["source_exists"] and edge["target_exists"]]
        outgoing_edges = [edge for edge in graph_edges if edge["source"] == node["id"] and edge["source_exists"] and edge["target_exists"]]
        node["incoming_ids"] = [edge["source"] for edge in incoming_edges]
        node["outgoing_ids"] = [edge["target"] for edge in outgoing_edges]
        node["incoming_routes"] = [edge["route_label"] for edge in incoming_edges if edge.get("route_label")]
        node["outgoing_routes"] = [edge["route_label"] for edge in outgoing_edges if edge.get("route_label")]

    return {
        "width": graph_width,
        "height": graph_height,
        "layers": [
            {
                "index": layer,
                "node_ids": [node["id"] for node in layered_nodes[layer]],
                "width": layer_widths[layer],
                "height": layer_heights[layer],
            }
            for layer in ordered_layers
        ],
        "edges": graph_edges,
    }


def _build_group_summaries(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    group_map: dict[str, dict[str, Any]] = {}
    for start, end, title, description in GROUP_RULES:
        group_map[f"group_{start:02d}_{end:02d}"] = {
            "id": f"group_{start:02d}_{end:02d}",
            "title": title,
            "description": description,
            "range": f"step_{start} ~ step_{end}",
            "step_ids": [],
            "issue_counts": {"critical": 0, "warning": 0, "info": 0},
        }
    group_map["group_conclusions"] = {
        "id": "group_conclusions",
        "title": "结论节点",
        "description": "流程收敛的最终结果",
        "range": "conclusions",
        "step_ids": [],
        "issue_counts": {"critical": 0, "warning": 0, "info": 0},
    }

    for node in nodes:
        group_id = node.get("group_id") or "group_conclusions"
        group = group_map.setdefault(
            group_id,
            {
                "id": group_id,
                "title": "其他",
                "description": "未归类节点",
                "range": "misc",
                "step_ids": [],
                "issue_counts": {"critical": 0, "warning": 0, "info": 0},
            },
        )
        if node["kind"] == "step":
            group["step_ids"].append(node["id"])
        counts = node.get("issue_counts") or {}
        for key in group["issue_counts"]:
            group["issue_counts"][key] += int(counts.get(key, 0) or 0)

    ordered_groups = []
    for start, end, _, _ in GROUP_RULES:
        group_id = f"group_{start:02d}_{end:02d}"
        ordered_groups.append(group_map[group_id])
    ordered_groups.append(group_map["group_conclusions"])
    return ordered_groups


def build_viewer_data(
    workflow_path: Path,
    steps_dir: Path,
    report_root: Path | None = None,
    issues_report_path: Path | None = None,
) -> dict[str, Any]:
    workflow = _load_yaml(workflow_path)
    steps = workflow.get("steps") or []
    conclusions = workflow.get("conclusions") or {}

    if issues_report_path and issues_report_path.exists():
        try:
            issue_report = json.loads(issues_report_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            issue_report = None
    else:
        issue_report = _load_latest_issue_report(report_root) if report_root else None

    issues_by_node, global_issue_counts = _build_issue_summary(issue_report)
    repo_root = workflow_path.parents[2]

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    step_node_map: dict[str, dict[str, Any]] = {}

    for step_id in steps:
        step_file = steps_dir / f"{step_id}.yaml"
        if not step_file.exists():
            continue
        doc = _load_yaml(step_file)
        group = _group_for_step(step_id)
        node = {
            "id": step_id,
            "kind": "step",
            "order": _step_number(step_id),
            "title": doc.get("name", step_id),
            "content": doc.get("content", ""),
            "file_path": _safe_relative(step_file, repo_root),
            "group_id": group["id"],
            "group_title": group["title"],
            "group_description": group["description"],
            "group_range": group["range"],
            "type_label": doc.get("type", "step"),
            "skills": doc.get("skills") or [],
            "transitions": _summarize_transitions(doc.get("transitions") or {}),
            "issue_counts": issues_by_node.get(step_id, {"critical": 0, "warning": 0, "info": 0}),
        }
        node["issue_total"] = sum(int(v or 0) for v in node["issue_counts"].values())
        if node["issue_counts"].get("critical", 0):
            node["issue_level"] = "critical"
        elif node["issue_counts"].get("warning", 0):
            node["issue_level"] = "warning"
        elif node["issue_counts"].get("info", 0):
            node["issue_level"] = "info"
        else:
            node["issue_level"] = "neutral"
        nodes.append(node)
        step_node_map[step_id] = node

        for rule in doc.get("transitions", {}).get("rules", []) or []:
            target = rule.get("next_node", "")
            edges.append(
                {
                    "source": step_id,
                    "target": target,
                    "kind": "rule",
                    "route_type": "rule",
                    "description": rule.get("description", ""),
                    "condition": rule.get("condition", ""),
                    "route_label": rule.get("description", "") or rule.get("condition", "") or "rule",
                }
            )
        for key, target in (doc.get("transitions", {}).get("on_error") or {}).items():
            edges.append(
                {
                    "source": step_id,
                    "target": target or "",
                    "kind": f"error:{key}",
                    "route_type": "on_error",
                    "description": key,
                    "condition": "",
                    "route_label": key,
                }
            )
        if doc.get("transitions", {}).get("default"):
            edges.append(
                {
                    "source": step_id,
                    "target": doc.get("transitions", {}).get("default"),
                    "kind": "default",
                    "route_type": "default",
                    "description": "default",
                    "condition": "",
                    "route_label": "default",
                }
            )

    conclusion_nodes: list[dict[str, Any]] = []
    for conclusion_id, doc in conclusions.items():
        node = {
            "id": conclusion_id,
            "kind": "conclusion",
            "order": 10000,
            "title": doc.get("message", conclusion_id),
            "content": doc.get("suggestion", ""),
            "level": doc.get("level", "info"),
            "repair_action": doc.get("repair_action", ""),
            "issue_counts": issues_by_node.get(conclusion_id, {"critical": 0, "warning": 0, "info": 0}),
        }
        node["issue_total"] = sum(int(v or 0) for v in node["issue_counts"].values())
        if node["issue_counts"].get("critical", 0):
            node["issue_level"] = "critical"
        elif node["issue_counts"].get("warning", 0):
            node["issue_level"] = "warning"
        elif node["issue_counts"].get("info", 0):
            node["issue_level"] = "info"
        else:
            node["issue_level"] = "neutral"
        conclusion_nodes.append(node)
        nodes.append(node)
        step_node_map[conclusion_id] = node

    graph = _layout_graph(nodes, edges, workflow.get("start_node") or [])
    groups = _build_group_summaries(nodes)

    incoming_by_node: dict[str, list[str]] = defaultdict(list)
    outgoing_by_node: dict[str, list[str]] = defaultdict(list)
    outgoing_routes_by_node: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in graph["edges"]:
        if edge["source_exists"] and edge["target_exists"]:
            incoming_by_node[edge["target"]].append(edge["source"])
            outgoing_by_node[edge["source"]].append(edge["target"])
            outgoing_routes_by_node[edge["source"]].append(edge)

    for node in nodes:
        node["incoming_ids"] = incoming_by_node.get(node["id"], [])
        node["outgoing_ids"] = outgoing_by_node.get(node["id"], [])
        node["outgoing_routes"] = [
            {
                "target": edge["target"],
                "next_node": edge["target"],
                "route_type": edge["route_type"],
                "description": edge.get("description", ""),
                "condition": edge.get("condition", ""),
                "route_label": edge.get("route_label", ""),
            }
            for edge in outgoing_routes_by_node.get(node["id"], [])
        ]
        node["incoming_routes"] = [
            {
                "source": edge["source"],
                "next_node": edge["target"],
                "route_type": edge["route_type"],
                "description": edge.get("description", ""),
                "condition": edge.get("condition", ""),
                "route_label": edge.get("route_label", ""),
            }
            for edge in graph["edges"]
            if edge["target"] == node["id"] and edge["source_exists"] and edge["target_exists"]
        ]

    meta = {
        "workflow_id": workflow.get("workflow_id", ""),
        "name": workflow.get("name", workflow_path.stem),
        "version": workflow.get("version", ""),
        "workflow_path": _safe_relative(workflow_path, repo_root),
        "steps_dir": _safe_relative(steps_dir, repo_root),
        "step_count": len([node for node in nodes if node["kind"] == "step"]),
        "conclusion_count": len(conclusion_nodes),
        "edge_count": len(edges),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "start_nodes": workflow.get("start_node") or [],
        "default_node_id": (workflow.get("start_node") or [None])[0] or (nodes[0]["id"] if nodes else ""),
    }

    return {
        "meta": meta,
        "groups": groups,
        "nodes": nodes,
        "conclusion_nodes": conclusion_nodes,
        "edges": graph["edges"],
        "graph": graph,
        "edge_count": len(edges),
        "issue_report": issue_report,
        "issue_summary": {
            "by_node": issues_by_node,
            "global": global_issue_counts,
            "total": sum(global_issue_counts.values()) + sum(sum(v.values()) for v in issues_by_node.values()),
        },
        "step_node_map": step_node_map,
    }
