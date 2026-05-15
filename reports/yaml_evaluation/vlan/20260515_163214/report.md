# YAML 评估报告

## 总览

- 工作流文件: `workflows/vlan/workflow.yaml`
- 步骤目录: `workflows/vlan/steps`
- 步骤文件数: 19
- workflow.steps 声明数: 19
- 问题总数: 23
- 严重问题: 23
- 警告: 0
- 提示: 0

## 共性问题

- 空 `condition`: 0 处
- 使用旧式 `state.step_...` 引用: 0 处
- 看起来像占位符的 `inputs`: 0 处
- `condition` 使用了 `True` 兜底: 0 处
- 空 `selector`: 13 处
- 空 `selector` 示例: step_4_create_vlan.yaml#skills[0], step_7_config_access_port_vlan.yaml#skills[0], step_7_config_access_port_vlan.yaml#skills[1], step_8_config_trunk_port_vlan.yaml#skills[0], step_8_config_trunk_port_vlan.yaml#skills[1], step_9_config_hybrid_port_vlan.yaml#skills[0], step_9_config_hybrid_port_vlan.yaml#skills[1], step_10a_config_interconnect_access_vlan.yaml#skills[0]

## 按文件汇总

| 文件 | 问题数 | 严重 | 警告 | 提示 |
|---|---:|---:|---:|---:|
| step_0_check_interface_status.yaml | 5 | 5 | 0 | 0 |
| step_10_check_interconnect_vlan_pass.yaml | 1 | 1 | 0 | 0 |
| step_10a_config_interconnect_access_vlan.yaml | 1 | 1 | 0 | 0 |
| step_10b_config_interconnect_trunk_vlan.yaml | 1 | 1 | 0 | 0 |
| step_10c_config_interconnect_hybrid_vlan.yaml | 1 | 1 | 0 | 0 |
| step_11_recheck_mac_address_table.yaml | 1 | 1 | 0 | 0 |
| step_12_check_port_isolation.yaml | 1 | 1 | 0 | 0 |
| step_13_check_static_arp.yaml | 1 | 1 | 0 | 0 |
| step_15_check_lnp_interface_status.yaml | 1 | 1 | 0 | 0 |
| step_16_check_lnp_link_type.yaml | 1 | 1 | 0 | 0 |
| step_17_check_lnp_configuration.yaml | 1 | 1 | 0 | 0 |
| step_18_check_ops_status.yaml | 1 | 1 | 0 | 0 |
| step_2_check_mac_address_table.yaml | 1 | 1 | 0 | 0 |
| step_3_check_vlan_created.yaml | 1 | 1 | 0 | 0 |
| step_4_create_vlan.yaml | 1 | 1 | 0 | 0 |
| step_5_check_interface_vlan_membership.yaml | 1 | 1 | 0 | 0 |
| step_7_config_access_port_vlan.yaml | 1 | 1 | 0 | 0 |
| step_8_config_trunk_port_vlan.yaml | 1 | 1 | 0 | 0 |
| step_9_config_hybrid_port_vlan.yaml | 1 | 1 | 0 | 0 |

## 详细问题

### step_0_check_interface_status.yaml

- [critical] extraction_schema `transitions.rules[0].condition`: condition 使用了未声明的 extracted 字段: access_port
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[1].condition`: condition 使用了未声明的 extracted 字段: interconnect_port
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[2].condition`: condition 使用了未声明的 extracted 字段: access_port
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[2].condition`: condition 使用了未声明的 extracted 字段: interconnect_port
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_10_check_interconnect_vlan_pass.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_10a_config_interconnect_access_vlan.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_10b_config_interconnect_trunk_vlan.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_10c_config_interconnect_hybrid_vlan.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_11_recheck_mac_address_table.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_12_check_port_isolation.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_13_check_static_arp.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_15_check_lnp_interface_status.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_16_check_lnp_link_type.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_17_check_lnp_configuration.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_18_check_ops_status.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_2_check_mac_address_table.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_3_check_vlan_created.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_4_create_vlan.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_5_check_interface_vlan_membership.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_7_config_access_port_vlan.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_8_config_trunk_port_vlan.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_9_config_hybrid_port_vlan.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

## 问题分类统计

- extraction_schema: 4
- next_node: 19
