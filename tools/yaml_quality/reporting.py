"""Report writers for YAML workflow quality scores."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import WorkflowQuality


METRIC_EXPLANATIONS = [
    ("输入 Schema 完整性", "对应 extraction_guided.md Phase 1：facts/current_hop、必填基线字段、字段 type/required/description。"),
    ("骨架拓扑一致性", "对应 Phase 2：start_node、steps、step 文件、conclusions 和重复声明。"),
    ("Step 内容完整性", "对应 Phase 2/3：step_id、文件名、name、content、type、preconditions 与 result_key。"),
    ("Skill 与抽取字段", "对应 Phase 3/4：skill_id、user_skills、inputs、selector、extraction_schema 与 [custom] 约定。"),
    ("条件表达式质量", "对应 Phase 3：condition、next_node、extracted/input/state 引用合法性。"),
    ("错误兜底与可执行性", "对应 Phase 4：on_error、系统 conclusion、conclusion level/message/suggestion、禁止 default。"),
]


def write_reports(scores: list[WorkflowQuality], output_dir: Path, chart_paths: dict[str, str]) -> dict[str, str]:
    """Write JSON, CSV and Markdown reports."""
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": output_dir / "scores.json",
        "csv": output_dir / "scores.csv",
        "markdown": output_dir / "report.md",
    }
    payload = build_payload(scores, chart_paths)
    paths["json"].write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(paths["csv"], scores)
    paths["markdown"].write_text(render_markdown(payload), encoding="utf-8")
    return {key: str(path) for key, path in paths.items()}


def build_payload(scores: list[WorkflowQuality], chart_paths: dict[str, str]) -> dict[str, Any]:
    """Build a JSON-ready report payload."""
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "metric_explanations": [
            {"name": name, "basis": basis}
            for name, basis in METRIC_EXPLANATIONS
        ],
        "charts": chart_paths,
        "workflows": [score.to_dict() for score in scores],
    }


def write_csv(path: Path, scores: list[WorkflowQuality]) -> None:
    """Write a flat score table."""
    dimension_names = [dimension.name for dimension in scores[0].dimensions] if scores else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["workflow", "overall_score", *dimension_names])
        for score in scores:
            writer.writerow(
                [
                    score.workflow,
                    f"{score.overall_score:.2f}",
                    *[f"{dimension.score:.2f}" for dimension in score.dimensions],
                ]
            )


def render_markdown(payload: dict[str, Any]) -> str:
    """Render the score report as Markdown."""
    lines: list[str] = [
        "# YAML Workflow 质量评分报告",
        "",
        f"- 生成时间: {payload['generated_at']}",
        f"- Matplotlib 中文字体: {payload['charts'].get('font', '未知')}",
        "",
        "## 评分指标",
        "",
    ]
    for item in payload["metric_explanations"]:
        lines.append(f"- **{item['name']}**: {item['basis']}")

    lines.extend(["", "## 总分表", ""])
    workflows = payload["workflows"]
    dimension_names = [item["name"] for item in workflows[0]["dimensions"]] if workflows else []
    lines.append("| Workflow | 总分 | " + " | ".join(dimension_names) + " |")
    lines.append("|---|---:|" + "|".join(["---:"] * len(dimension_names)) + "|")
    for item in workflows:
        dim_scores = " | ".join(f"{dim['score']:.1f}" for dim in item["dimensions"])
        lines.append(f"| {item['workflow']} | {item['overall_score']:.1f} | {dim_scores} |")

    lines.extend(["", "## 图表", ""])
    for key, value in payload["charts"].items():
        if key == "font":
            continue
        lines.append(f"- `{Path(value).name}`")

    lines.extend(["", "## 主要扣分项", ""])
    for workflow in workflows:
        lines.append(f"### {workflow['workflow']}")
        for dimension in workflow["dimensions"]:
            if dimension["findings"]:
                findings = "；".join(dimension["findings"][:4])
                lines.append(f"- **{dimension['name']}** ({dimension['score']:.1f}): {findings}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
