"""将 workflow YAML 转换成 HTML 视图所需的数据。"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


GROUP_RULES = [
    (0, 6, "基础连通性", "Ping 命令、MTU、二层连通性、物理链路"),
    (7, 10, "路由与策略路由", "直连路由、流策略、重定向、ACL 关联"),
    (11, 18, "ARP / MAC / 二层阻断", "ARP 学习、MAC 出接口、二层阻塞"),
    (19, 21, "cpu-defend 黑名单", "防攻击策略、黑名单、ACL 命中"),
    (22, 30, "ICMP 统计与 CPCAR", "收发统计、流量统计、限速调整"),
    (31, 34, "抓包分析", "端口镜像、流镜像、capture 抓包"),
    (35, 36, "日志收尾", "日志收集、文件保存"),
]

GRAPH_NODE_WIDTH = 250
GRAPH_CONCLUSION_WIDTH = 220
GRAPH_NODE_HEIGHT = 104
GRAPH_CONCLUSION_HEIGHT = 88
GRAPH_LAYER_STEP = 168
GRAPH_NODE_GAP = 40
GRAPH_PADDING_X = 72
GRAPH_PADDING_Y = 72
GRAPH_LAYER_GAP = 96
GRAPH_ROW_GAP = 28
GRAPH_MAX_STEP_PER_ROW = 4
GRAPH_MAX_CONCLUSION_PER_ROW = 5
GROUP_ORDER = {
    "group_00_06": 0,
    "group_07_10": 1,
    "group_11_18": 2,
    "group_19_21": 3,
    "group_22_30": 4,
    "group_31_34": 5,
    "group_35_36": 6,
    "group_conclusions": 7,
    "group_misc": 8,
}


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _step_number(step_id: str) -> int:
    if not step_id.startswith("step_"):
        return 10_000
    parts = step_id.split("_", 2)
    try:
        return int(parts[1])
    except (IndexError, ValueError):
        return 10_000


def _group_for_step(step_id: str) -> dict[str, Any]:
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


def _find_step_file(steps_dir: Path, step_id: str) -> Path | None:
    candidate = steps_dir / f"{step_id}.yaml"
    if candidate.exists():
        return candidate
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
                "kind": "rule",
                "description": rule.get("description", ""),
                "condition": rule.get("condition", ""),
                "next_node": rule.get("next_node", ""),
            }
        )
    on_error = transitions.get("on_error") or {}
    for key, target in on_error.items():
        summary.append(
            {
                "kind": "on_error",
                "description": key,
                "condition": "",
                "next_node": target or "",
            }
        )
    if transitions.get("default"):
        summary.append(
            {
                "kind": "default",
                "description": "default",
                "condition": "",
                "next_node": transitions.get("default"),
            }
        )
    return summary


def _build_graph_layout(
    nodes: list[dict[str, Any]],
    conclusion_nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    start_nodes: list[str],
) -> dict[str, Any]:
    all_nodes = nodes + conclusion_nodes
    node_by_id = {node["id"]: node for node in all_nodes}
    node_order = {node["id"]: index for index, node in enumerate(nodes)}

    incoming_map: dict[str, list[dict[str, Any]]] = defaultdict(list)
    outgoing_map: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        if source not in node_by_id or target not in node_by_id:
            continue
        incoming_map[target].append(edge)
        outgoing_map[source].append(edge)

    layer_map: dict[str, int] = {}
    for start in start_nodes:
        if start in node_by_id:
            layer_map[start] = 0

    for _ in range(len(all_nodes)):
        changed = False
        for edge in edges:
            source = edge["source"]
            target = edge["target"]
            if source not in layer_map or target not in node_by_id:
                continue
            candidate = layer_map[source] + 1
            if candidate > layer_map.get(target, -1):
                layer_map[target] = candidate
                changed = True
        if not changed:
            break

    fallback_layer = max(layer_map.values(), default=0) + 1
    for node in all_nodes:
        node_id = node["id"]
        if node_id in layer_map:
            continue
        incoming_layers = [layer_map[edge["source"]] for edge in incoming_map.get(node_id, []) if edge["source"] in layer_map]
        if incoming_layers:
            layer_map[node_id] = max(incoming_layers) + 1
        elif node["type"] == "step":
            layer_map[node_id] = node_order.get(node_id, fallback_layer)
        else:
            layer_map[node_id] = fallback_layer

    compressed_layers = {layer: index for index, layer in enumerate(sorted(set(layer_map.values())))}

    layered_nodes: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for node in all_nodes:
        layer = compressed_layers[layer_map[node["id"]]]
        node["graph_layer"] = layer
        layered_nodes[layer].append(node)

    def sort_key(node: dict[str, Any]) -> tuple[int, int, int, str]:
        return (
            GROUP_ORDER.get(node.get("group_id"), 999),
            0 if node["type"] == "step" else 1,
            node.get("order", 99999),
            node["id"],
        )

    def row_capacity(node: dict[str, Any]) -> int:
        return GRAPH_MAX_CONCLUSION_PER_ROW if node["type"] == "conclusion" else GRAPH_MAX_STEP_PER_ROW

    layer_rows: dict[int, list[list[dict[str, Any]]]] = {}
    layer_widths: dict[int, int] = {}
    layer_heights: dict[int, int] = {}

    for layer, layer_nodes in layered_nodes.items():
        ordered = sorted(layer_nodes, key=sort_key)
        if not ordered:
            layer_rows[layer] = []
            layer_widths[layer] = GRAPH_NODE_WIDTH
            layer_heights[layer] = GRAPH_NODE_HEIGHT
            continue

        rows: list[list[dict[str, Any]]] = []
        current_row: list[dict[str, Any]] = []
        current_capacity = row_capacity(ordered[0])
        for node in ordered:
            capacity = row_capacity(node)
            if current_row and (len(current_row) >= current_capacity or current_capacity != capacity):
                rows.append(current_row)
                current_row = []
                current_capacity = capacity
            current_row.append(node)
            current_capacity = min(current_capacity, capacity)
            if len(current_row) >= current_capacity:
                rows.append(current_row)
                current_row = []
                current_capacity = capacity
        if current_row:
            rows.append(current_row)

        layer_rows[layer] = rows

        max_width = 0
        total_height = 0
        for row_index, row in enumerate(rows):
            row_width = 0
            row_height = 0
            for index, node in enumerate(row):
                width = GRAPH_CONCLUSION_WIDTH if node["type"] == "conclusion" else GRAPH_NODE_WIDTH
                height = GRAPH_CONCLUSION_HEIGHT if node["type"] == "conclusion" else GRAPH_NODE_HEIGHT
                row_width += width
                if index < len(row) - 1:
                    row_width += GRAPH_NODE_GAP
                row_height = max(row_height, height)
            max_width = max(max_width, row_width)
            total_height += row_height
            if row_index < len(rows) - 1:
                total_height += GRAPH_ROW_GAP

        layer_widths[layer] = max_width
        layer_heights[layer] = total_height

    max_layer_width = max(layer_widths.values(), default=GRAPH_NODE_WIDTH)

    layer_y_offsets: dict[int, int] = {}
    y_cursor = GRAPH_PADDING_Y
    for layer in sorted(layer_rows):
        layer_y_offsets[layer] = y_cursor
        y_cursor += layer_heights[layer] + GRAPH_LAYER_GAP

    for layer, rows in layer_rows.items():
        layer_width = layer_widths[layer]
        row_cursor_y = layer_y_offsets[layer]
        for row in rows:
            row_height = max((GRAPH_CONCLUSION_HEIGHT if node["type"] == "conclusion" else GRAPH_NODE_HEIGHT) for node in row)
            row_width = 0
            for index, node in enumerate(row):
                width = GRAPH_CONCLUSION_WIDTH if node["type"] == "conclusion" else GRAPH_NODE_WIDTH
                row_width += width
                if index < len(row) - 1:
                    row_width += GRAPH_NODE_GAP
            start_x = GRAPH_PADDING_X + (max_layer_width - row_width) / 2
            cursor_x = start_x
            for node in row:
                width = GRAPH_CONCLUSION_WIDTH if node["type"] == "conclusion" else GRAPH_NODE_WIDTH
                height = GRAPH_CONCLUSION_HEIGHT if node["type"] == "conclusion" else GRAPH_NODE_HEIGHT
                node["graph_layout"] = {
                    "x": round(row_cursor_y, 1),
                    "y": round(cursor_x, 1),
                    "width": width,
                    "height": height,
                    "center_x": round(row_cursor_y + width / 2, 1),
                    "center_y": round(cursor_x + height / 2, 1),
                    "layer": layer,
                }
                cursor_x += width + GRAPH_NODE_GAP
            row_cursor_y += row_height + GRAPH_ROW_GAP

    graph_width = int(
        max((node["graph_layout"]["x"] + node["graph_layout"]["width"] for node in all_nodes), default=GRAPH_NODE_WIDTH)
        + GRAPH_PADDING_X
    )
    graph_height = int(
        max((node["graph_layout"]["y"] + node["graph_layout"]["height"] for node in all_nodes), default=GRAPH_NODE_HEIGHT)
        + GRAPH_PADDING_Y
    )

    outgoing_index: dict[str, int] = defaultdict(int)
    outgoing_count: dict[str, int] = defaultdict(int)
    for edge in edges:
        if edge["source"] in node_by_id and edge["target"] in node_by_id:
            outgoing_count[edge["source"]] += 1

    graph_edges: list[dict[str, Any]] = []
    for edge_index, edge in enumerate(edges):
        source = node_by_id.get(edge["source"])
        target = node_by_id.get(edge["target"])
        if not source or not target:
            continue
        source_layout = source.get("graph_layout") or {}
        target_layout = target.get("graph_layout") or {}
        if not source_layout or not target_layout:
            continue

        slot = outgoing_index[edge["source"]]
        outgoing_index[edge["source"]] += 1
        total = outgoing_count.get(edge["source"], 1)
        branch_offset = (slot - (total - 1) / 2) * 18

        source_x = source_layout["x"] + source_layout["width"]
        source_y = source_layout["center_y"] + branch_offset
        target_x = target_layout["x"]
        target_y = target_layout["center_y"] + branch_offset * 0.3
        delta_x = target_x - source_x
        bend = max(48.0, abs(delta_x) * 0.55)
        direction = 1 if delta_x >= 0 else -1
        c1_x = source_x + direction * bend
        c2_x = target_x - direction * bend
        path = (
            f"M {source_x:.1f} {source_y:.1f} "
            f"C {c1_x:.1f} {source_y:.1f}, {c2_x:.1f} {target_y:.1f}, {target_x:.1f} {target_y:.1f}"
        )
        label_lines = []
        if edge.get("description"):
            label_lines.append(edge["description"])
        if edge.get("condition"):
            label_lines.append(edge["condition"])
        if not label_lines:
            label_lines.append(edge.get("kind", "edge"))
        graph_edges.append(
            {
                **edge,
                "id": f"edge_{edge_index:03d}",
                "layout": {
                    "path": path,
                    "label_x": round((source_x + target_x) / 2 - 10, 1),
                    "label_y": round((source_y + target_y) / 2, 1),
                    "hit_width": 12,
                },
                "display_lines": label_lines[:2],
            }
        )

    return {
        "width": graph_width,
        "height": graph_height,
        "node_width": GRAPH_NODE_WIDTH,
        "node_height": GRAPH_NODE_HEIGHT,
        "conclusion_width": GRAPH_CONCLUSION_WIDTH,
        "conclusion_height": GRAPH_CONCLUSION_HEIGHT,
        "layer_step": GRAPH_LAYER_STEP,
        "node_gap": GRAPH_NODE_GAP,
        "padding_x": GRAPH_PADDING_X,
        "padding_y": GRAPH_PADDING_Y,
        "layer_count": len(layered_nodes),
        "layers": [
            {
                "index": layer,
                "node_ids": [node["id"] for node in layer_nodes],
                "width": layer_widths[layer],
            }
            for layer, layer_nodes in sorted(layered_nodes.items())
        ],
        "edges": graph_edges,
    }


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
    groups: dict[str, dict[str, Any]] = {}
    step_node_map: dict[str, dict[str, Any]] = {}

    for step_id in steps:
        step_file = _find_step_file(steps_dir, step_id)
        if not step_file:
            continue
        doc = _load_yaml(step_file)
        group = _group_for_step(step_id)
        group_entry = groups.setdefault(
            group["id"],
            {
                "id": group["id"],
                "title": group["title"],
                "description": group["description"],
                "range": group["range"],
                "step_ids": [],
            },
        )
        node = {
            "id": step_id,
            "type": "step",
            "order": _step_number(step_id),
            "name": doc.get("name", step_id),
            "content": doc.get("content", ""),
            "step_file": str(step_file.relative_to(repo_root)),
            "group_id": group["id"],
            "group_title": group["title"],
            "type_label": doc.get("type", "step"),
            "skills": doc.get("skills") or [],
            "transitions": _summarize_transitions(doc.get("transitions") or {}),
            "issue_counts": issues_by_node.get(step_id, {"critical": 0, "warning": 0, "info": 0}),
        }
        step_node_map[step_id] = node
        nodes.append(node)
        group_entry["step_ids"].append(step_id)

        for rule in doc.get("transitions", {}).get("rules", []) or []:
            edges.append(
                {
                    "source": step_id,
                    "target": rule.get("next_node", ""),
                    "kind": "rule",
                    "description": rule.get("description", ""),
                    "condition": rule.get("condition", ""),
                }
            )
        for key, target in (doc.get("transitions", {}).get("on_error") or {}).items():
            edges.append(
                {
                    "source": step_id,
                    "target": target or "",
                    "kind": f"error:{key}",
                    "description": key,
                    "condition": "",
                }
            )
        if doc.get("transitions", {}).get("default"):
            edges.append(
                {
                    "source": step_id,
                    "target": doc.get("transitions", {}).get("default"),
                    "kind": "default",
                    "description": "default",
                    "condition": "",
                }
            )

    conclusion_nodes: list[dict[str, Any]] = []
    conclusion_group = {
        "id": "group_conclusions",
        "title": "结论节点",
        "description": "流程收敛的最终结果",
        "range": "conclusions",
        "step_ids": [],
    }
    for conclusion_id, doc in conclusions.items():
        conclusion_nodes.append(
            {
                "id": conclusion_id,
                "type": "conclusion",
                "order": 10000,
                "name": doc.get("message", conclusion_id),
                "content": doc.get("suggestion", ""),
                "level": doc.get("level", "info"),
                "repair_action": doc.get("repair_action", ""),
                "issue_counts": issues_by_node.get(conclusion_id, {"critical": 0, "warning": 0, "info": 0}),
            }
        )

    groups_list = sorted(groups.values(), key=lambda item: item["step_ids"][0] if item["step_ids"] else item["id"])
    groups_list.append(conclusion_group)

    for group in groups_list:
        group["issue_counts"] = {"critical": 0, "warning": 0, "info": 0}
        for step_id in group.get("step_ids", []):
            counts = issues_by_node.get(step_id, {"critical": 0, "warning": 0, "info": 0})
            for key in group["issue_counts"]:
                group["issue_counts"][key] += counts.get(key, 0)

    for node in nodes + conclusion_nodes:
        node["issue_total"] = sum(node.get("issue_counts", {}).values())
        node["summary_badge"] = f"{node['issue_total']} 问题" if node["issue_total"] else "无问题"

    graph = _build_graph_layout(nodes, conclusion_nodes, edges, workflow.get("start_node") or [])

    meta = {
        "workflow_id": workflow.get("workflow_id", ""),
        "name": workflow.get("name", workflow_path.stem),
        "version": workflow.get("version", ""),
        "workflow_path": str(workflow_path.relative_to(repo_root)),
        "steps_dir": str(steps_dir.relative_to(repo_root)),
        "step_count": len(nodes),
        "conclusion_count": len(conclusion_nodes),
        "start_nodes": workflow.get("start_node") or [],
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    edge_count = len(edges)
    return {
        "meta": meta,
        "groups": groups_list,
        "nodes": nodes,
        "conclusion_nodes": conclusion_nodes,
        "edges": edges,
        "graph": graph,
        "edge_count": edge_count,
        "issue_report": issue_report,
        "issue_summary": {
            "by_node": issues_by_node,
            "global": global_issue_counts,
            "total": sum(global_issue_counts.values()) + sum(sum(v.values()) for v in issues_by_node.values()),
        },
        "group_order": [group["id"] for group in groups_list],
        "step_node_map": step_node_map,
    }
