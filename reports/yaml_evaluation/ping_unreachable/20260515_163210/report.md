# YAML 评估报告

## 总览

- 工作流文件: `workflows/ping_unreachable/workflow.yaml`
- 步骤目录: `workflows/ping_unreachable/steps`
- 步骤文件数: 18
- workflow.steps 声明数: 18
- 问题总数: 36
- 严重问题: 36
- 警告: 0
- 提示: 0

## 共性问题

- 空 `condition`: 0 处
- 使用旧式 `state.step_...` 引用: 0 处
- 看起来像占位符的 `inputs`: 0 处
- `condition` 使用了 `True` 兜底: 0 处
- 空 `selector`: 6 处
- 空 `selector` 示例: step_6_check_direct_route.yaml#skills[0], step_16_check_icmp_statistics_local.yaml#skills[0], step_17_check_icmp_statistics_peer.yaml#skills[0], step_18_check_icmp_cpcar_statistics.yaml#skills[0], step_18_check_icmp_cpcar_statistics.yaml#skills[1], step_18_check_icmp_cpcar_statistics.yaml#skills[2]

## 按文件汇总

| 文件 | 问题数 | 严重 | 警告 | 提示 |
|---|---:|---:|---:|---:|
| step_10_check_redirect_acl_detail.yaml | 1 | 1 | 0 | 0 |
| step_11_check_arp_learning.yaml | 1 | 1 | 0 | 0 |
| step_12_check_mac_outbound.yaml | 1 | 1 | 0 | 0 |
| step_13_check_cpu_defend_policy.yaml | 1 | 1 | 0 | 0 |
| step_14_check_cpu_defend_blacklist.yaml | 1 | 1 | 0 | 0 |
| step_15_check_blacklist_acl.yaml | 1 | 1 | 0 | 0 |
| step_16_check_icmp_statistics_local.yaml | 1 | 1 | 0 | 0 |
| step_17_check_icmp_statistics_peer.yaml | 1 | 1 | 0 | 0 |
| step_18_check_icmp_cpcar_statistics.yaml | 3 | 3 | 0 | 0 |
| step_1_check_port_vlan.yaml | 7 | 7 | 0 | 0 |
| step_2_check_ip_interface.yaml | 3 | 3 | 0 | 0 |
| step_3_check_physical_link.yaml | 5 | 5 | 0 | 0 |
| step_4_check_vlanif_status.yaml | 5 | 5 | 0 | 0 |
| step_5_check_layer2_blocking.yaml | 1 | 1 | 0 | 0 |
| step_6_check_direct_route.yaml | 1 | 1 | 0 | 0 |
| step_7_check_policy_routing_applied.yaml | 1 | 1 | 0 | 0 |
| step_8_check_traffic_behavior_redirect.yaml | 1 | 1 | 0 | 0 |
| step_9_check_classifier_acl.yaml | 1 | 1 | 0 | 0 |

## 详细问题

### step_10_check_redirect_acl_detail.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_11_check_arp_learning.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_12_check_mac_outbound.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_13_check_cpu_defend_policy.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_14_check_cpu_defend_blacklist.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_15_check_blacklist_acl.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_16_check_icmp_statistics_local.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_17_check_icmp_statistics_peer.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_18_check_icmp_cpcar_statistics.yaml

- [critical] extraction_schema `transitions.rules[0].condition` (line 52): condition 使用了未声明的 extracted 字段: cpcar_after
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[0].condition` (line 52): condition 使用了未声明的 extracted 字段: cpcar_before
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_1_check_port_vlan.yaml

- [critical] extraction_schema `transitions.rules[0].condition`: condition 使用了未声明的 extracted 字段: local_port_vlan
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[0].condition`: condition 使用了未声明的 extracted 字段: peer_port_vlan
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[1].condition`: condition 使用了未声明的 extracted 字段: local_port_vlan
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[1].condition`: condition 使用了未声明的 extracted 字段: peer_port_vlan
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[2].condition`: condition 使用了未声明的 extracted 字段: local_port_vlan
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[2].condition`: condition 使用了未声明的 extracted 字段: peer_port_vlan
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_2_check_ip_interface.yaml

- [critical] extraction_schema `transitions.rules[0].condition`: condition 使用了未声明的 extracted 字段: local_ip_interface_brief
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[0].condition`: condition 使用了未声明的 extracted 字段: peer_ip_interface_brief
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_3_check_physical_link.yaml

- [critical] extraction_schema `transitions.rules[0].condition`: condition 使用了未声明的 extracted 字段: local_eth_trunk
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[0].condition`: condition 使用了未声明的 extracted 字段: peer_eth_trunk
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[1].condition`: condition 使用了未声明的 extracted 字段: local_eth_trunk
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[1].condition`: condition 使用了未声明的 extracted 字段: peer_eth_trunk
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_4_check_vlanif_status.yaml

- [critical] extraction_schema `transitions.rules[0].condition`: condition 使用了未声明的 extracted 字段: current_port_interface_brief
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[0].condition`: condition 使用了未声明的 extracted 字段: vlanif_interface_brief
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[1].condition`: condition 使用了未声明的 extracted 字段: current_port_interface_brief
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] extraction_schema `transitions.rules[1].condition`: condition 使用了未声明的 extracted 字段: vlanif_interface_brief
  - 建议: 把该字段补入 extraction_schema，或修改 condition
- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_5_check_layer2_blocking.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_6_check_direct_route.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_7_check_policy_routing_applied.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_8_check_traffic_behavior_redirect.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

### step_9_check_classifier_acl.yaml

- [critical] next_node `transitions.default`: 目标节点为空
  - 建议: 补充合法的 step_id 或 conclusion_id

## 问题分类统计

- extraction_schema: 18
- next_node: 18
