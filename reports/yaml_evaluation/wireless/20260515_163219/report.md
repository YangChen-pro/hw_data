# YAML 评估报告

## 总览

- 工作流文件: `workflows/wireless/workflow.yaml`
- 步骤目录: `workflows/wireless/steps`
- 步骤文件数: 15
- workflow.steps 声明数: 15
- 问题总数: 15
- 严重问题: 15
- 警告: 0
- 提示: 0

## 共性问题

- 空 `condition`: 0 处
- 使用旧式 `state.step_...` 引用: 0 处
- 看起来像占位符的 `inputs`: 0 处
- `condition` 使用了 `True` 兜底: 0 处
- 空 `selector`: 11 处
- 空 `selector` 示例: step_1_check_vap_config.yaml#skills[0], step_2_check_auth_profile.yaml#skills[0], step_3_check_security_profile.yaml#skills[0], step_4_check_domain_config.yaml#skills[0], step_8_check_radius_global_config.yaml#skills[0], step_9_check_radius_template.yaml#skills[0], step_10_check_radius_server_item.yaml#skills[0], step_11_check_web_auth_server_config.yaml#skills[0]

## 按文件汇总

| 文件 | 问题数 | 严重 | 警告 | 提示 |
|---|---:|---:|---:|---:|
| step_0_check_vap_profile.yaml | 1 | 1 | 0 | 0 |
| step_10_check_radius_server_item.yaml | 1 | 1 | 0 | 0 |
| step_11_check_web_auth_server_config.yaml | 1 | 1 | 0 | 0 |
| step_12_check_portal_server_template.yaml | 1 | 1 | 0 | 0 |
| step_13_check_free_rule.yaml | 1 | 1 | 0 | 0 |
| step_14_check_account_blocked.yaml | 1 | 1 | 0 | 0 |
| step_15_check_dot1x_quiet.yaml | 1 | 1 | 0 | 0 |
| step_16_check_vlan_created.yaml | 1 | 1 | 0 | 0 |
| step_1_check_vap_config.yaml | 1 | 1 | 0 | 0 |
| step_2_check_auth_profile.yaml | 1 | 1 | 0 | 0 |
| step_3_check_security_profile.yaml | 1 | 1 | 0 | 0 |
| step_4_check_domain_config.yaml | 1 | 1 | 0 | 0 |
| step_5_check_aaa_fail_record.yaml | 1 | 1 | 0 | 0 |
| step_8_check_radius_global_config.yaml | 1 | 1 | 0 | 0 |
| step_9_check_radius_template.yaml | 1 | 1 | 0 | 0 |

## 详细问题

### step_0_check_vap_profile.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_10_check_radius_server_item.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_11_check_web_auth_server_config.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_12_check_portal_server_template.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_13_check_free_rule.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_14_check_account_blocked.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_15_check_dot1x_quiet.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_16_check_vlan_created.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_1_check_vap_config.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_2_check_auth_profile.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_3_check_security_profile.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_4_check_domain_config.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_5_check_aaa_fail_record.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_8_check_radius_global_config.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_9_check_radius_template.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

## 问题分类统计

- next_node: 15
