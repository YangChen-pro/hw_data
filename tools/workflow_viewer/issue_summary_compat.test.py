"""回归测试：workflow viewer 的报告总数与问题明细展示兼容性。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    parser_path = repo_root / "tools" / "workflow_viewer" / "parser.py"
    spec = importlib.util.spec_from_file_location("workflow_viewer_parser", parser_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 parser: {parser_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    build_viewer_data = module.build_viewer_data

    workflow_path = repo_root / "workflows" / "ping_unreachable" / "workflow.yaml"
    steps_dir = repo_root / "workflows" / "ping_unreachable" / "steps"
    report_path = repo_root / "reports" / "yaml_evaluation" / "ping_unreachable" / "20260405_221402" / "report.json"

    data = build_viewer_data(workflow_path, steps_dir, report_root=repo_root / "reports" / "yaml_evaluation" / "ping_unreachable", issues_report_path=report_path)

    summary = data["issue_summary"]
    assert summary["total"] == 62, summary
    assert summary["global"] == {"critical": 2, "warning": 60, "info": 0}, summary

    node = data["step_node_map"]["step_21_check_blacklist_acl"]
    messages = [item["message"] for item in node.get("issue_items", [])]
    assert any("condition 为空" in message for message in messages), messages

    node_20 = data["step_node_map"]["step_20_check_cpu_defend_blacklist"]
    messages_20 = [item["message"] for item in node_20.get("issue_items", [])]
    assert any("__NEED_FILL__" in message for message in messages_20), messages_20

    print("issue_summary_compat: ok")


if __name__ == "__main__":
    main()
