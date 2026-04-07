"""workflow HTML 查看器命令行入口。"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from .parser import WorkflowViewerError, build_viewer_data
from .renderer import write_html


def resolve_input_path(repo_root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    return path.resolve() if path.is_absolute() else (repo_root / path).resolve()


def workflow_namespace(workflow_path: Path, repo_root: Path) -> str:
    resolved = workflow_path.resolve()
    try:
        relative = resolved.relative_to(repo_root)
    except ValueError:
        if resolved.stem == "workflow" and resolved.parent.name:
            return resolved.parent.name
        return resolved.stem
    parts = relative.parts
    if len(parts) >= 2 and parts[0] == "workflows":
        return parts[1]
    if relative.stem == "workflow" and len(parts) >= 2:
        return parts[-2]
    return relative.stem


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="生成 workflow 单页 HTML 可视化页面。")
    parser.add_argument(
        "--workflow",
        default="workflows/ping_unreachable/workflow.yaml",
        help="workflow.yaml 路径",
    )
    parser.add_argument(
        "--steps-dir",
        default="workflows/ping_unreachable/steps",
        help="steps 目录",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="输出目录，默认生成时间戳目录",
    )
    parser.add_argument(
        "--issues-report",
        default="",
        help="可选：评估报告 report.json 路径。为空时自动读取最近一次报告。",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[2]
    workflow_path = resolve_input_path(repo_root, args.workflow)
    steps_dir = resolve_input_path(repo_root, args.steps_dir)
    namespace = workflow_namespace(workflow_path, repo_root)
    report_root = repo_root / "reports" / "yaml_evaluation" / namespace
    issues_report = resolve_input_path(repo_root, args.issues_report) if args.issues_report else None
    if args.output_dir:
        output_dir = Path(args.output_dir).resolve()
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = repo_root / "reports" / "workflow_viewer" / namespace / timestamp

    try:
        viewer_data = build_viewer_data(
            workflow_path,
            steps_dir,
            report_root=report_root if not issues_report else None,
            issues_report_path=issues_report,
        )
    except WorkflowViewerError as error:
        print(f"HTML 生成失败: {error}")
        return 1

    template_path = Path(__file__).with_name("graph_template.html")
    write_html(output_dir / "index.html", template_path, viewer_data)

    print(f"HTML 已生成: {output_dir / 'index.html'}")
    print(
        f"节点数: {viewer_data['meta']['step_count']} | "
        f"结论数: {viewer_data['meta']['conclusion_count']} | "
        f"边数: {viewer_data['edge_count']}"
    )
    return 0
