"""workflow HTML 查看器命令行入口。"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from .parser import build_viewer_data
from .renderer import write_html


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
    workflow_path = (repo_root / args.workflow).resolve()
    steps_dir = (repo_root / args.steps_dir).resolve()
    report_root = repo_root / "reports" / "yaml_evaluation" / "ping_unreachable"
    issues_report = Path(args.issues_report).resolve() if args.issues_report else None
    if args.output_dir:
        output_dir = Path(args.output_dir).resolve()
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = repo_root / "reports" / "workflow_viewer" / "ping_unreachable" / timestamp

    viewer_data = build_viewer_data(
        workflow_path,
        steps_dir,
        report_root=report_root if not issues_report else None,
        issues_report_path=issues_report,
    )

    template_path = Path(__file__).with_name("graph_template.html")
    write_html(output_dir / "index.html", template_path, viewer_data)

    print(f"HTML 已生成: {output_dir / 'index.html'}")
    print(
        f"节点数: {viewer_data['meta']['step_count']} | "
        f"结论数: {viewer_data['meta']['conclusion_count']} | "
        f"边数: {viewer_data['edge_count']}"
    )
    return 0
