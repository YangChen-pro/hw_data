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
        return str(resolved)


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

    repo_root = Path(__file__).resolve().parents[2]
    workflow_path = resolve_input_path(repo_root, args.workflow)
    steps_dir = resolve_input_path(repo_root, args.steps_dir)
    workflow_display_path = to_repo_relative(workflow_path)
    steps_display_path = to_repo_relative(steps_dir)
    if args.output_dir:
        output_dir = Path(args.output_dir).resolve()
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = repo_root / "reports" / "yaml_evaluation" / workflow_namespace(workflow_path, repo_root) / timestamp

    issues, stats = evaluate_workflow(workflow_path, steps_dir)
    report = build_report_payload(workflow_display_path, steps_display_path, issues, stats)
    write_outputs(output_dir, report, issues)

    print(f"报告已生成: {output_dir}")
    print(
        f"问题总数: {report['issue_count']} "
        f"(critical={report['critical_count']}, warning={report['warning_count']}, info={report['info_count']})"
    )
    return 0
