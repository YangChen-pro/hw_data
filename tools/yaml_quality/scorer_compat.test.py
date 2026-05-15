"""Compatibility smoke test for YAML quality scoring."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.yaml_quality.scorer import score_workflow


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        steps = root / "steps"
        steps.mkdir()
        (root / "workflow.yaml").write_text(
            """
workflow_id: wf_quality_smoke
name: 质量评分烟测
input_schema:
  - name: facts
    type: object
    required: false
    description: 外部事实
    properties: []
  - name: current_hop
    type: object
    required: true
    description: 当前排查对象
    properties:
      - name: hop_index
        type: integer
        required: true
        description: 当前跳索引
      - name: current_device
        type: string
        required: true
        description: 当前设备
      - name: path_state
        type: string
        required: true
        description: 路径状态
start_node:
  - step_id: step_1_check_entry
    description: 入口
steps:
  - step_1_check_entry
conclusions:
  CONCLUSION_OK:
    level: info
    message: 正常
    suggestion: 结束
  CONCLUSION_MANUAL_CHECK:
    level: error
    message: 人工介入
    suggestion: 人工确认
""".lstrip(),
            encoding="utf-8",
        )
        (steps / "step_1_check_entry.yaml").write_text(
            """
step_id: step_1_check_entry
name: 入口检查
content: 检查入口状态
type: diagnosis
skills:
  - skill_id: skill_display_interface
    inputs: {}
    selector: 按接口定位状态行
    extraction_schema:
      - name: current_state
        type: string
        description: 接口状态
transitions:
  rules:
    - description: 状态正常
      condition: extracted.current_state == 'UP'
      next_node: CONCLUSION_OK
  on_error:
    handler_execution_failed: CONCLUSION_MANUAL_CHECK
    cli_command_execution_failed: CONCLUSION_MANUAL_CHECK
    parse_failure: CONCLUSION_MANUAL_CHECK
""".lstrip(),
            encoding="utf-8",
        )
        user_skills = root / "user_skills"
        user_skills.mkdir()
        (user_skills / "skill_display_interface.yaml").write_text(
            """
skill_id: skill_display_interface
description: 执行 display interface 命令
action:
  type: cli_command
  commands: display interface
parser:
  method: llm
  data_type: command
default_schema:
  type: object
  properties:
    current_state:
      type: string
      description: 接口状态
""".lstrip(),
            encoding="utf-8",
        )
        result = score_workflow(root / "workflow.yaml", steps)

    assert result.workflow == Path(tmp).name
    assert result.overall_score > 80, result.to_dict()
    print("yaml_quality_scorer_compat: ok")


if __name__ == "__main__":
    main()
