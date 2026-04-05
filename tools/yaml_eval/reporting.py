"""评估结果的报告生成。"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import Issue


def build_report_payload(
    workflow_path: Path,
    steps_dir: Path,
    issues: list[Issue],
    stats: dict[str, Any],
) -> dict[str, Any]:
    empty_condition_count = sum(
        1 for issue in issues if issue.category == "condition" and issue.message == "condition 为空"
    )
    legacy_state_ref_count = sum(
        1 for issue in issues if issue.category == "condition" and "state.step_" in issue.message
    )
    placeholder_input_count = sum(
        1 for issue in issues if issue.category == "inputs" and "占位符" in issue.message
    )
    true_condition_count = sum(
        1 for issue in issues if issue.category == "condition" and '仅为 "True"' in issue.message
    )
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "workflow_path": str(workflow_path),
        "steps_dir": str(steps_dir),
        "step_file_count": stats["step_file_count"],
        "workflow_step_count": stats["workflow_step_count"],
        "issue_count": len(issues),
        "critical_count": sum(1 for issue in issues if issue.severity == "critical"),
        "warning_count": sum(1 for issue in issues if issue.severity == "warning"),
        "info_count": sum(1 for issue in issues if issue.severity == "info"),
        "empty_condition_count": empty_condition_count,
        "legacy_state_ref_count": legacy_state_ref_count,
        "placeholder_input_count": placeholder_input_count,
        "true_condition_count": true_condition_count,
        "blank_selector_count": stats["blank_selector_count"],
        "blank_selector_examples": stats["blank_selector_examples"],
        "files_with_issues": stats["files_with_issues"],
        "issue_counter": stats["issue_counter"],
        "issues": [asdict(issue) for issue in issues],
    }


def render_markdown(report: dict[str, Any], issues: list[Issue]) -> str:
    by_file: dict[str, list[Issue]] = defaultdict(list)
    by_category: Counter[str] = Counter()
    by_severity: Counter[str] = Counter()
    for issue in issues:
        by_file[issue.file].append(issue)
        by_category[issue.category] += 1
        by_severity[issue.severity] += 1

    lines: list[str] = []
    lines.append("# YAML 评估报告")
    lines.append("")
    lines.append("## 总览")
    lines.append("")
    lines.append(f"- 工作流文件: `{report['workflow_path']}`")
    lines.append(f"- 步骤目录: `{report['steps_dir']}`")
    lines.append(f"- 步骤文件数: {report['step_file_count']}")
    lines.append(f"- workflow.steps 声明数: {report['workflow_step_count']}")
    lines.append(f"- 问题总数: {len(issues)}")
    lines.append(f"- 严重问题: {by_severity.get('critical', 0)}")
    lines.append(f"- 警告: {by_severity.get('warning', 0)}")
    lines.append(f"- 提示: {by_severity.get('info', 0)}")
    lines.append("")
    lines.append("## 共性问题")
    lines.append("")
    lines.append(f"- 空 `condition`: {report['empty_condition_count']} 处")
    lines.append(f"- 使用旧式 `state.step_...` 引用: {report['legacy_state_ref_count']} 处")
    lines.append(f"- 看起来像占位符的 `inputs`: {report['placeholder_input_count']} 处")
    lines.append(f"- `condition` 使用了 `True` 兜底: {report['true_condition_count']} 处")
    lines.append(f"- 空 `selector`: {report['blank_selector_count']} 处")
    if report["blank_selector_examples"]:
        lines.append(f"- 空 `selector` 示例: {', '.join(report['blank_selector_examples'])}")
    lines.append("")
    lines.append("## 按文件汇总")
    lines.append("")
    lines.append("| 文件 | 问题数 | 严重 | 警告 | 提示 |")
    lines.append("|---|---:|---:|---:|---:|")
    for file_name in sorted(by_file):
        file_issues = by_file[file_name]
        critical = sum(1 for issue in file_issues if issue.severity == "critical")
        warning = sum(1 for issue in file_issues if issue.severity == "warning")
        info = sum(1 for issue in file_issues if issue.severity == "info")
        lines.append(f"| {file_name} | {len(file_issues)} | {critical} | {warning} | {info} |")
    lines.append("")
    lines.append("## 详细问题")
    lines.append("")
    for file_name in sorted(by_file):
        lines.append(f"### {file_name}")
        lines.append("")
        for issue in by_file[file_name]:
            location = f" `{issue.path}`" if issue.path else ""
            line = f" (line {issue.line})" if issue.line else ""
            lines.append(f"- [{issue.severity}] {issue.category}{location}{line}: {issue.message}")
            lines.append(f"  - 建议: {issue.recommendation}")
        lines.append("")

    lines.append("## 问题分类统计")
    lines.append("")
    for category, count in sorted(by_category.items()):
        lines.append(f"- {category}: {count}")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_csv(path: Path, issues: list[Issue]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["file", "step_id", "severity", "category", "path", "line", "message", "recommendation"])
        for issue in issues:
            writer.writerow(
                [
                    issue.file,
                    issue.step_id,
                    issue.severity,
                    issue.category,
                    issue.path,
                    "" if issue.line is None else issue.line,
                    issue.message,
                    issue.recommendation,
                ]
            )


def write_outputs(output_dir: Path, report: dict[str, Any], issues: list[Issue]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "report.md").write_text(render_markdown(report, issues), encoding="utf-8")
    (output_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_csv(output_dir / "issues.csv", issues)
    manifest = {
        "generated_at": report["generated_at"],
        "workflow": report["workflow_path"],
        "steps_dir": report["steps_dir"],
        "files": ["report.md", "report.json", "issues.csv"],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

