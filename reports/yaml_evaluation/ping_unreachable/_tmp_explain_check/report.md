# YAML 评估报告

## 总览

- 工作流文件: `workflows/ping_unreachable/workflow.yaml`
- 步骤目录: `workflows/ping_unreachable/steps`
- 步骤文件数: 37
- workflow.steps 声明数: 37
- 问题总数: 62
- 严重问题: 2
- 警告: 60
- 提示: 0

## 共性问题

- 空 `condition`: 38 处
- 使用旧式 `state.step_...` 引用: 3 处
- 看起来像占位符的 `inputs`: 16 处
- `condition` 使用了 `True` 兜底: 3 处
- 空 `selector`: 61 处
- 空 `selector` 示例: step_1_check_mtu.yaml#skills[0], step_2_check_port_vlan.yaml#skills[0], step_3_check_ip_interface.yaml#skills[0], step_4_check_physical_link.yaml#skills[0], step_5_check_vlanif_status.yaml#skills[0], step_5_check_vlanif_status.yaml#skills[1], step_6_check_layer2_blocking.yaml#skills[0], step_6_check_layer2_blocking.yaml#skills[1]

## 按文件汇总

| 文件 | 问题数 | 严重 | 警告 | 提示 |
|---|---:|---:|---:|---:|
| step_0_check_ping_command.yaml | 2 | 0 | 2 | 0 |
| step_10_check_classifier_acl.yaml | 2 | 0 | 2 | 0 |
| step_12_check_mac_outbound.yaml | 2 | 0 | 2 | 0 |
| step_13_check_arp_miss_overload.yaml | 2 | 0 | 2 | 0 |
| step_14_check_arp_request_link_drop.yaml | 2 | 0 | 2 | 0 |
| step_15_check_switchb_cpcar_drop.yaml | 2 | 0 | 2 | 0 |
| step_16_check_arp_response_link_drop.yaml | 2 | 0 | 2 | 0 |
| step_17_check_switcha_cpcar_drop.yaml | 2 | 0 | 2 | 0 |
| step_18_check_switcha_arp_module_error.yaml | 2 | 0 | 2 | 0 |
| step_19_check_cpu_defend_policy.yaml | 1 | 0 | 1 | 0 |
| step_1_check_mtu.yaml | 2 | 0 | 2 | 0 |
| step_20_check_cpu_defend_blacklist.yaml | 2 | 1 | 1 | 0 |
| step_21_check_blacklist_acl.yaml | 4 | 1 | 3 | 0 |
| step_23_check_icmp_statistics_switchb.yaml | 3 | 0 | 3 | 0 |
| step_24_configure_inbound_traffic_statistics.yaml | 4 | 0 | 4 | 0 |
| step_25_configure_outbound_traffic_statistics.yaml | 4 | 0 | 4 | 0 |
| step_26_reset_traffic_statistics.yaml | 3 | 0 | 3 | 0 |
| step_27_check_switcha_outbound_statistics.yaml | 1 | 0 | 1 | 0 |
| step_28_check_switchb_inbound_statistics.yaml | 3 | 0 | 3 | 0 |
| step_2_check_port_vlan.yaml | 2 | 0 | 2 | 0 |
| step_30_configure_icmp_cpcar_value.yaml | 1 | 0 | 1 | 0 |
| step_31_check_packet_format.yaml | 3 | 0 | 3 | 0 |
| step_32_configure_port_mirroring.yaml | 1 | 0 | 1 | 0 |
| step_33_configure_flow_mirroring.yaml | 1 | 0 | 1 | 0 |
| step_34_capture_packet_format.yaml | 1 | 0 | 1 | 0 |
| step_35_collect_log_info.yaml | 1 | 0 | 1 | 0 |
| step_36_save_log_files.yaml | 1 | 0 | 1 | 0 |
| step_3_check_ip_interface.yaml | 2 | 0 | 2 | 0 |
| step_4_check_physical_link.yaml | 2 | 0 | 2 | 0 |
| step_7_check_direct_route.yaml | 1 | 0 | 1 | 0 |
| step_9_check_traffic_behavior_redirect.yaml | 1 | 0 | 1 | 0 |

## 详细问题

### step_0_check_ping_command.yaml

- [warning] condition `transitions.rules[0].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_10_check_classifier_acl.yaml

- [warning] inputs `skills[1].inputs.acl_number`: 输入值看起来像占位符: 与流分类关联的ACL编号
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] condition `transitions.rules[0].condition` (line 24): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_12_check_mac_outbound.yaml

- [warning] inputs `skills[0].inputs.mac_address`: 输入值看起来像占位符: 来自step_11提取的MAC_ADDRESS字段值
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] condition `transitions.rules[0].condition` (line 17): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_13_check_arp_miss_overload.yaml

- [warning] condition `transitions.rules[0].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_14_check_arp_request_link_drop.yaml

- [warning] condition `transitions.rules[0].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_15_check_switchb_cpcar_drop.yaml

- [warning] condition `transitions.rules[0].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_16_check_arp_response_link_drop.yaml

- [warning] condition `transitions.rules[0].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_17_check_switcha_cpcar_drop.yaml

- [warning] condition `transitions.rules[0].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_18_check_switcha_arp_module_error.yaml

- [warning] condition `transitions.rules[0].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_19_check_cpu_defend_policy.yaml

- [warning] condition `transitions.rules[0].condition` (line 19): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_1_check_mtu.yaml

- [warning] condition `transitions.rules[0].condition` (line 16): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 16): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_20_check_cpu_defend_blacklist.yaml

- [warning] inputs `skills[0].inputs.policy_name`: 输入值看起来像占位符: 策略名称（来自上一步获取的Name字段）
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [critical] next_node `transitions.rules[1].next_node` (line 21): 使用了占位值 __NEED_FILL__
  - 建议: 替换为合法的 step_id 或 conclusion_id

### step_21_check_blacklist_acl.yaml

- [warning] inputs `skills[0].inputs.acl_number`: 输入值看起来像占位符: ACL编号（来自Blacklist字段中的ACL number）
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] condition `transitions.rules[0].condition` (line 17): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 17): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [critical] next_node `transitions.rules[1].next_node` (line 21): 使用了占位值 __NEED_FILL__
  - 建议: 替换为合法的 step_id 或 conclusion_id

### step_23_check_icmp_statistics_switchb.yaml

- [warning] condition `transitions.rules[0].condition`: condition 使用了 state.step_... 的旧式引用
  - 建议: 如需和文档保持一致，可统一为 state.results.step_...；否则在文档中说明兼容旧格式
- [warning] condition `transitions.rules[1].condition`: condition 使用了 state.step_... 的旧式引用
  - 建议: 如需和文档保持一致，可统一为 state.results.step_...；否则在文档中说明兼容旧格式
- [warning] condition `transitions.rules[2].condition` (line 25): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_24_configure_inbound_traffic_statistics.yaml

- [warning] inputs `skills[0].inputs.src_ip`: 输入值看起来像占位符: 源IP地址
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] inputs `skills[0].inputs.dst_ip`: 输入值看起来像占位符: 目的IP地址
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] inputs `skills[4].inputs.interface`: 输入值看起来像占位符: 接口名称
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] condition `transitions.rules[0].condition` (line 41): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_25_configure_outbound_traffic_statistics.yaml

- [warning] inputs `skills[0].inputs.src_ip`: 输入值看起来像占位符: 源IP地址
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] inputs `skills[0].inputs.dst_ip`: 输入值看起来像占位符: 目的IP地址
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] inputs `skills[4].inputs.interface`: 输入值看起来像占位符: 接口名称
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] condition `transitions.rules[0].condition` (line 41): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_26_reset_traffic_statistics.yaml

- [warning] inputs `skills[0].inputs.interface`: 输入值看起来像占位符: 接口名称
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] inputs `skills[1].inputs.interface`: 输入值看起来像占位符: 接口名称
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] condition `transitions.rules[0].condition` (line 21): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_27_check_switcha_outbound_statistics.yaml

- [warning] inputs `skills[0].inputs.interface`: 输入值看起来像占位符: 接口名称
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值

### step_28_check_switchb_inbound_statistics.yaml

- [warning] inputs `skills[0].inputs.interface`: 输入值看起来像占位符: 接口名称
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值
- [warning] condition `transitions.rules[0].condition`: condition 使用了 state.step_... 的旧式引用
  - 建议: 如需和文档保持一致，可统一为 state.results.step_...；否则在文档中说明兼容旧格式
- [warning] condition `transitions.rules[2].condition` (line 27): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_2_check_port_vlan.yaml

- [warning] condition `transitions.rules[0].condition` (line 22): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 22): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_30_configure_icmp_cpcar_value.yaml

- [warning] condition `transitions.rules[0].condition` (line 22): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_31_check_packet_format.yaml

- [warning] condition `transitions.rules[0].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[2].condition` (line 9): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_32_configure_port_mirroring.yaml

- [warning] condition `transitions.rules[0].condition` (line 18): condition 仅为 "True"
  - 建议: 改为明确的判断条件，或注明这是人工兜底分支

### step_33_configure_flow_mirroring.yaml

- [warning] condition `transitions.rules[0].condition` (line 65): condition 仅为 "True"
  - 建议: 改为明确的判断条件，或注明这是人工兜底分支

### step_34_capture_packet_format.yaml

- [warning] condition `transitions.rules[0].condition` (line 15): condition 仅为 "True"
  - 建议: 改为明确的判断条件，或注明这是人工兜底分支

### step_35_collect_log_info.yaml

- [warning] condition `transitions.rules[0].condition` (line 21): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_36_save_log_files.yaml

- [warning] condition `transitions.rules[0].condition` (line 25): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_3_check_ip_interface.yaml

- [warning] condition `transitions.rules[0].condition` (line 22): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 22): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_4_check_physical_link.yaml

- [warning] condition `transitions.rules[0].condition` (line 14): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式
- [warning] condition `transitions.rules[1].condition` (line 14): condition 为空
  - 建议: 若分支依赖人工判断可保留；否则补充可规则化表达式

### step_7_check_direct_route.yaml

- [warning] inputs `skills[0].inputs.ip_address`: 输入值看起来像占位符: 目标IP地址
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值

### step_9_check_traffic_behavior_redirect.yaml

- [warning] inputs `skills[0].inputs.behavior_name`: 输入值看起来像占位符: 流行为名称（从step_8的Policy_Name关联获取）
  - 建议: 替换为可由用户输入、前序结果或固定常量解析的真实值

## 问题分类统计

- condition: 44
- inputs: 16
- next_node: 2
