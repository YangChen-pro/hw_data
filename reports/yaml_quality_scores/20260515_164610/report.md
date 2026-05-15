# YAML Workflow 质量评分报告

- 生成时间: 2026-05-15T16:46:11
- Matplotlib 中文字体: STHeiti

## 评分指标

- **输入 Schema 完整性**: 对应 extraction_guide Phase 1：facts/current_hop、必填基线字段、字段 type/required/description。
- **骨架拓扑一致性**: 对应 Phase 2：start_node、steps、step 文件、conclusions 和重复声明。
- **Step 内容完整性**: 对应 Phase 2/3：step_id、文件名、name、content、type、preconditions 与 result_key。
- **Skill 与抽取字段**: 对应 Phase 3/4：skill_id、user_skills、inputs、selector、extraction_schema 与 [custom] 约定。
- **条件表达式质量**: 对应 Phase 3：condition、next_node、extracted/input/state 引用合法性。
- **错误兜底与可执行性**: 对应 Phase 4：on_error、default、conclusion level/message/suggestion。

## 总分表

| Workflow | 总分 | 输入 Schema 完整性 | 骨架拓扑一致性 | Step 内容完整性 | Skill 与抽取字段 | 条件表达式质量 | 错误兜底与可执行性 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ap_offline | 80.1 | 0.0 | 100.0 | 97.8 | 86.1 | 96.7 | 100.0 |
| ping_unreachable | 95.6 | 100.0 | 100.0 | 100.0 | 91.2 | 99.4 | 83.0 |
| vlan | 93.3 | 100.0 | 100.0 | 100.0 | 83.3 | 96.1 | 80.3 |
| wireless | 95.2 | 100.0 | 100.0 | 100.0 | 88.3 | 97.3 | 85.4 |

## 图表

- `overall_score_bar.png`
- `dimension_score_heatmap.png`
- `dimension_radar.png`

## 主要扣分项

### ap_offline
- **输入 Schema 完整性** (0.0): 缺少 facts input_schema 对象；缺少 current_hop input_schema 对象；current_hop 缺少必填基线字段 hop_index；current_hop 缺少必填基线字段 current_device
- **Step 内容完整性** (97.8): step_02_remove_blacklist type 无效；step_03_fix_static_ip type 无效
- **Skill 与抽取字段** (86.1): step_01_check_offline_reason display ap offline-record all selector 为空或占位；step_01_check_offline_reason [custom]reason_category 不应把 [custom] 放在 name；step_02_remove_blacklist display ap blacklist selector 为空或占位；step_02_remove_blacklist undo ap blacklist mac ap-mac selector 为空或占位
- **条件表达式质量** (96.7): step_01_check_offline_reason rule[57] condition 为空；step_02_remove_blacklist rule[2] condition 为空；step_03_fix_static_ip rule[2] condition 为空；step_04_check_license rule[0] condition 为空

### ping_unreachable
- **Skill 与抽取字段** (91.2): step_10_check_redirect_acl_detail 引用的 skill_display_acl 缺少 user_skills 定义；step_11_check_arp_learning 引用的 skill_display_arp 缺少 user_skills 定义；step_12_check_mac_outbound 引用的 skill_display_mac_address 缺少 user_skills 定义；step_13_check_cpu_defend_policy 引用的 skill_display_cpu_defend_policy 缺少 user_skills 定义
- **条件表达式质量** (99.4): step_18_check_icmp_cpcar_statistics rule[1] condition 为空
- **错误兜底与可执行性** (83.0): step_10_check_redirect_acl_detail transitions.default 缺失或无效；step_11_check_arp_learning transitions.default 缺失或无效；step_12_check_mac_outbound transitions.default 缺失或无效；step_13_check_cpu_defend_policy transitions.default 缺失或无效

### vlan
- **Skill 与抽取字段** (83.3): step_0_check_interface_status 引用的 skill_display_interface 缺少 user_skills 定义；step_10_check_interconnect_vlan_pass 引用的 skill_display_port_vlan 缺少 user_skills 定义；step_10a_config_interconnect_access_vlan 引用的 skill_port_link_type_access 缺少 user_skills 定义；step_10a_config_interconnect_access_vlan skill_port_link_type_access selector 为空或占位
- **条件表达式质量** (96.1): step_10a_config_interconnect_access_vlan rule[0] condition 为空；step_10b_config_interconnect_trunk_vlan rule[0] condition 为空；step_10c_config_interconnect_hybrid_vlan rule[0] condition 为空；step_4_create_vlan rule[0] condition 为空
- **错误兜底与可执行性** (80.3): step_0_check_interface_status transitions.default 缺失或无效；step_10_check_interconnect_vlan_pass transitions.default 缺失或无效；step_10a_config_interconnect_access_vlan transitions.default 缺失或无效；step_10b_config_interconnect_trunk_vlan transitions.default 缺失或无效

### wireless
- **Skill 与抽取字段** (88.3): step_0_check_vap_profile 引用的 skill_display_vap_profile_all 缺少 user_skills 定义；step_10_check_radius_server_item 引用的 skill_display_radius_server_item 缺少 user_skills 定义；step_10_check_radius_server_item skill_display_radius_server_item selector 为空或占位；step_11_check_web_auth_server_config 引用的 skill_display_web_auth_server_configuration 缺少 user_skills 定义
- **条件表达式质量** (97.3): step_11_check_web_auth_server_config rule[2] condition 为空；step_2_check_auth_profile rule[3] condition 为空；step_8_check_radius_global_config rule[0] condition 为空；step_9_check_radius_template rule[1] condition 为空
- **错误兜底与可执行性** (85.4): step_0_check_vap_profile transitions.default 缺失或无效；step_10_check_radius_server_item transitions.default 缺失或无效；step_11_check_web_auth_server_config transitions.default 缺失或无效；step_12_check_portal_server_template transitions.default 缺失或无效
