"""CLI entrypoint for YAML workflow quality scoring."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from .plotting import write_charts
from .reporting import write_reports
from .scorer import score_workflow, score_workflows


def resolve_path(repo_root: Path, raw_path: str) -> Path:
    """Resolve a CLI path relative to the repository root."""
    path = Path(raw_path)
    return path.resolve() if path.is_absolute() else (repo_root / path).resolve()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="基于 extraction_guided.md 生成 YAML workflow 质量评分和图表。")
    parser.add_argument("--workflows-root", default="workflows", help="包含多个 workflow 目录的根目录")
    parser.add_argument("--workflow", default="", help="单个 workflow.yaml 路径；为空时扫描 workflows-root")
    parser.add_argument("--steps-dir", default="", help="单个 workflow 的 steps 目录，配合 --workflow 使用")
    parser.add_argument("--output-dir", default="", help="输出目录；为空时写入 reports/yaml_quality_scores/<时间戳>")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[2]
    output_dir = (
        resolve_path(repo_root, args.output_dir)
        if args.output_dir
        else repo_root / "reports" / "yaml_quality_scores" / datetime.now().strftime("%Y%m%d_%H%M%S")
    )

    if args.workflow:
        workflow_path = resolve_path(repo_root, args.workflow)
        steps_dir = resolve_path(repo_root, args.steps_dir) if args.steps_dir else workflow_path.parent / "steps"
        scores = [score_workflow(workflow_path, steps_dir)]
    else:
        scores = score_workflows(resolve_path(repo_root, args.workflows_root))

    if not scores:
        raise SystemExit("未找到可评分的 workflow.yaml")

    chart_paths = write_charts(scores, output_dir)
    report_paths = write_reports(scores, output_dir, chart_paths)

    print(f"质量评分报告已生成: {output_dir}")
    print(f"图表: {chart_paths['overall_bar']}, {chart_paths['dimension_heatmap']}, {chart_paths['radar']}")
    print(f"数据: {report_paths['json']}, {report_paths['csv']}, {report_paths['markdown']}")
    for score in sorted(scores, key=lambda item: item.workflow):
        print(f"- {score.workflow}: {score.overall_score:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
