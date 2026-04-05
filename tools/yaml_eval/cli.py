"""命令行入口。"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from .checks import evaluate_workflow
from .reporting import build_report_payload, write_outputs


def to_repo_relative(path: Path) -> str:
    repo_root = Path(__file__).resolve().parents[2]
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(repo_root))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="评估 ping_unreachable 工作流 YAML 并导出报告。")
    parser.add_argument(
        "--workflow",
        default="workflows/ping_unreachable/workflow.yaml",
        help="workflow.yaml 的路径",
    )
    parser.add_argument(
        "--steps-dir",
        default="workflows/ping_unreachable/steps",
        help="step YAML 目录",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="报告输出目录；为空时自动创建时间戳目录",
    )
    args = parser.parse_args(argv)

    workflow_path = Path(args.workflow).resolve()
    steps_dir = Path(args.steps_dir).resolve()
    workflow_display_path = to_repo_relative(Path(args.workflow))
    steps_display_path = to_repo_relative(Path(args.steps_dir))
    if args.output_dir:
        output_dir = Path(args.output_dir).resolve()
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("reports/yaml_evaluation/ping_unreachable") / timestamp
        output_dir = output_dir.resolve()

    issues, stats = evaluate_workflow(workflow_path, steps_dir)
    report = build_report_payload(workflow_display_path, steps_display_path, issues, stats)
    write_outputs(output_dir, report, issues)

    print(f"报告已生成: {output_dir}")
    print(
        f"问题总数: {report['issue_count']} "
        f"(critical={report['critical_count']}, warning={report['warning_count']}, info={report['info_count']})"
    )
    return 0
