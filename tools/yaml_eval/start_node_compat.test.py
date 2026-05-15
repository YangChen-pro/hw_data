"""回归测试：start_node 支持带 description 的字典写法。"""

from __future__ import annotations

import tempfile
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.yaml_eval.checks import evaluate_workflow


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        workflow_path = root / "workflow.yaml"
        steps_dir = root / "steps"
        steps_dir.mkdir()

        workflow_path.write_text(
            """
workflow_id: wf_start_node_mapping
name: start_node 兼容性测试
start_node:
  - step_id: step_1_check_entry
    description: 入口步骤说明
steps:
  - step_1_check_entry
conclusions:
  CONCLUSION_MANUAL_CHECK:
    level: error
    message: 需要人工介入
    suggestion: 人工确认
""".lstrip(),
            encoding="utf-8",
        )
        (steps_dir / "step_1_check_entry.yaml").write_text(
            """
step_id: step_1_check_entry
name: 入口检查
type: diagnosis
skills: []
transitions:
  rules: []
  default: CONCLUSION_MANUAL_CHECK
""".lstrip(),
            encoding="utf-8",
        )

        issues, stats = evaluate_workflow(workflow_path, steps_dir)

    messages = [issue.message for issue in issues if issue.path.startswith("start_node")]
    assert not messages, messages
    assert stats["start_node_count"] == 1, stats
    print("start_node_compat: ok")


if __name__ == "__main__":
    main()
