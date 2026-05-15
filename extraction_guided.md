# 网络故障排查 Markdown → YAML 抽取统一指南

版本：v2.0 | 合并来源：`extraction_sop.md` + `extraction_guide.md`

本指南是网络故障排查资料抽取为 GenericAgent Workflow YAML 的唯一依据。它合并了旧版 SOP 的逐切片执行纪律、路径初始化、验证经验，以及新版 guide 的 Phase 1~4 结构化设计规则。

## 0. 使用方式与合并决策

### 0.1 两阶段输出

抽取必须分两次输出，先骨架、后细节：

- 第一次输出：执行 Phase 1 + Phase 2，只输出 `input_schema`、`start_node`、`steps`、`conclusions`、transitions 拓扑，不填 `skills` / `extraction_schema` 细节。
- 第二次输出：执行 Phase 3 + Phase 4，补齐每个 step 的 `preconditions`、`skills`、`transitions.condition`、`user_skills` 和整体一致性校验。

### 0.2 逐切片纪律

当源资料被拆成多个 Markdown/TXT 切片时，必须逐切片处理：

- 先扫描真实文件列表，禁止猜文件名。
- 每次只处理一个切片。
- 每完成一个切片，展示本次新增 step、conclusion、start_node 和待确认问题。
- 用户确认后才进入下一个切片。

### 0.3 冲突决策

旧 SOP 与新版 guide 存在几处格式差异，本统一版以当前项目 YAML 结构为准：

- `skill_id` 使用 `skill_{命令语义}`，原始 CLI 命令写入 `user_skills/<skill_id>.yaml` 的 `action.commands`。
- `workflow.steps` 使用 step_id 字符串列表；`start_node` 推荐使用 `{step_id, description}` 字典列表。
- `condition` 必须非空；无条件跳转写 `True`。
- `transitions` 禁止定义 `default` 字段；兜底错误统一放入 `on_error`，正常入口链路末尾可隐式结束或跳转到兜底 conclusion。
- 跨 step 引用使用 `state.results.<step_id>.<field>`；旧式 `state.<step_id>.<field>` 只作为历史兼容，不作为新抽取目标。
- `[custom]` 只写在 `description` 中，不写进 `name`。

## 1. 项目输入与输出结构

### 1.1 启动前确认

开始抽取前确认两个路径：

- 源切片目录：包含 `.md` 或 `.txt` 切片文件。
- 输出目录：通常为 `workflows/<topic>/`。

扫描文件示例：

```python
import os
files = sorted(os.listdir(source_dir))
slice_docs = [name for name in files if name.endswith((".md", ".txt"))]
for index, name in enumerate(slice_docs, 1):
    print(f"{index}. {name}")
```

### 1.2 推荐输出目录

```text
workflows/<topic>/
├── workflow.yaml
├── steps/
│   ├── step_1_xxx.yaml
│   └── step_2_xxx.yaml
├── user_skills/
│   ├── skill_display_xxx.yaml
│   └── skill_configure_xxx.yaml
└── <topic>_org/              # 可选，保存源切片
```

### 1.3 workflow.yaml 骨架

```yaml
workflow_id: wf_<topic>
name: <中文名称>
version: "1.0"
description: <场景说明>
input_schema:
  - name: facts
    type: object
    required: false
    description: 外部事实与配置意图
    properties: []
  - name: current_hop
    type: object
    required: true
    description: 当前排查对象
    properties: []
start_node: []
steps: []
conclusions:
  CONCLUSION_HANDLER_EXECUTION_FAILED:
    level: warning
    message: 工作流处理器执行失败
    suggestion: 请检查 workflow 引擎运行状态、step 编排配置和执行上下文，然后重试
  CONCLUSION_CLI_COMMAND_EXECUTION_FAILED:
    level: warning
    message: 设备命令执行失败
    suggestion: 请检查设备连通性、认证权限、命令可用性与执行超时情况，然后重试
  CONCLUSION_PARSE_FAILURE:
    level: warning
    message: 命令回显解析失败
    suggestion: 请检查命令回显格式是否变化、解析 schema/selector 是否匹配，并修正后重试
  CONCLUSION_MANUAL_CHECK:
    level: error
    message: 无法自动判断，需人工介入
    suggestion: 请补充现场信息或联系网络管理员进一步确认
```

## 2. Phase 1：input_schema 设计

目标：输出 `facts` 和 `current_hop` 的完整 properties 列表，并给每个字段标注可追溯来源。

### 2.1 必填基线

`current_hop` 必须包含：

```yaml
- name: hop_index
  type: integer
  required: true
  description: 当前跳索引
- name: current_device
  type: string
  required: true
  description: 当前设备管理 IP 或设备标识
- name: path_state
  type: string
  required: true
  description: 路径状态，建议取值 resolved、partial、failed
```

### 2.2 场景模型字段

阅读 Markdown/PDF 后判断模型：

- 双设备模型，如 SwitchA ↔ SwitchB：加入 `peer_device`、`current_interface`、`peer_interface`。
- 单设备上下行口模型，如 VLAN：加入 `current_interface`、`interconnect_interface`。
- 终端或外部系统属性：放入 `facts`，不放入 `current_hop`。

### 2.3 扩展字段五步追溯

逐条执行以下扫描，发现依赖即加入 input_schema：

- Step A：`display xxx <参数>` 的参数若不来自前序 step 输出，则加入 input 字段。
- Step B：selector 定位字段若来自 input 而非 extracted，则加入 input 字段。
- Step C：跨 step 比对或与输入值比较的锚点字段必须有来源。
- Step D：无法通过被管设备 `display` 获取的终端侧属性或配置意图，放入 `facts`。
- Step E：判断逻辑直接消费的外部状态值，放入 `facts` 或 `current_hop`。

### 2.4 字段归属

- `current_hop`：当前排查对象的设备、接口、链路、VLAN、IP、下一跳等属性。
- `facts`：终端设备、外部系统状态、配置意图、人工提供的判断依据。

### 2.5 边界规则

- 必须加入 Step A~E 推导出的字段。
- 禁止加入 Markdown/PDF 未提及、无来源依据的推测字段。
- 多入口分发用 `start_node` 数组表达，不新增 `scenario` 之类分发字段。
- 可由 display 输出推断的值不放入 input。

### 2.6 Phase 1 自检

- [ ] `facts` 对象已创建，即使 properties 为空。
- [ ] `current_hop` 包含 `hop_index`、`current_device`、`path_state`。
- [ ] 模型字段已加入，双设备和单设备上下行口没有混用。
- [ ] 每个 display 命令参数都有来源。
- [ ] 每个 selector 定位字段都有来源。
- [ ] 判断逻辑中不来自 skill 输出的字段已定义为 input。
- [ ] 每个字段都有 type、required、description 和来源依据。
- [ ] 没有加入无来源的推测性字段。

## 3. Phase 2：骨架设计

目标：确定 step 列表、start_node、transitions 拓扑和 conclusions。此阶段不填写 `skills` / `extraction_schema`。

### 3.1 识别 start_node

- Markdown/PDF 中每个可自动化的顶级排查章节对应一个 `start_node`。
- 顶级章节内部的子步骤链不单独成为 start_node。
- start_node 按源文档排查顺序排列。
- 纯人工、抓包、镜像、信息收集章节不生成 start_node。
- 推荐格式：

```yaml
start_node:
  - step_id: step_1_check_port_vlan
    description: 二层接口 VLAN 配置一致性检查
```

### 3.2 step 拆分规则

| 场景 | 拆法 |
|---|---|
| 1 条命令 + 1 个判断 | 1 个 step |
| 多条命令共同服务同一判断 | 1 个 step，多个 skill |
| 多条命令各自独立判断 | 多个 step，transitions 串联 |
| 链式数据传递，后续命令入参来自前序输出 | 每个子步骤独立 step |
| 本端和对端执行同一命令并在同一判断中对比 | 1 个 step + 2 个 skill，使用 result_key |
| 本端和对端统计逻辑不同，需要跨 step 比对 | 2 个独立 step |
| 同一设备多个同类接口执行同一命令 | 1 个 step + 多个 skill，使用 result_key |

step_id 格式：`step_{序号}_{动词}_{对象}`，全小写英文下划线，允许 `10a`、`10b` 这类子编号。

### 3.3 type 判定

- `diagnosis`：只读命令，如 `display` / `show`。
- `configuration`：在当前被管设备上执行配置修改命令。

以下情况不创建 configuration step，只输出 conclusion 或 suggestion：

- 修复动作在终端设备上执行。
- 修复动作需要现场人工操作。
- PDF 中只是建议性修改，不是 workflow 必须执行的强制修复。
- 章节本质是配置检测，不要求自动修复。

### 3.4 诊断→修复→复核

- configuration step 完成后用 `condition: True` 跳到后续 diagnosis step。
- 不创建紧挨着配置 step 的独立 verify step。
- 只有入口链路末尾、多条修复分支汇聚时，才设置专门复核 step。

### 3.5 conclusions 设计

对每个异常判断分支创建独立 conclusion：

- 不同字段异常分别建 conclusion。
- 固定系统三条结论必须存在：
  - `CONCLUSION_HANDLER_EXECUTION_FAILED`
  - `CONCLUSION_CLI_COMMAND_EXECUTION_FAILED`
  - `CONCLUSION_PARSE_FAILURE`
- 常用通用结论按需添加：
  - `CONCLUSION_MANUAL_CHECK`
  - `CONCLUSION_ESCALATE_WITH_DEVICE_INFO`
  - `CONCLUSION_CHECK_PACKET_TX_RX`
- 命名格式：`CONCLUSION_` + 全大写下划线语义。
- level：故障用 `error`；防御性、系统兜底、进一步确认用 `warning`；正常结束可用 `info`，但禁止用“无故障”掩盖未定位场景。

### 3.6 不纳入自动化

以下内容不转成 step：

- 查看指示灯、更换光模块/网线等纯人工操作。
- 抓包、端口镜像、流镜像等动作。
- 收集诊断信息联系技术支持。
- 命令格式提醒，如是否使用 `-f` 参数。
- 终端侧人工修改。

这些内容可写入 conclusion 的 `suggestion` / `repair_action`。

### 3.7 Phase 2 自检

- [ ] start_node 数量等于可自动化顶级排查章节数。
- [ ] 链式数据传递步骤已拆分。
- [ ] 本端+对端跨 step 比对场景拆为 2 个 step。
- [ ] 同一设备多个同类接口合并为 1 step 多 skill。
- [ ] 没有为纯检测类场景创建 configuration step。
- [ ] 每个异常分支都有独立 conclusion。
- [ ] 固定系统三条 conclusion 已逐字定义。
- [ ] 不自动化内容没有被转成 step。
- [ ] step 总数与可自动化检查判断点匹配。
- [ ] 每个 step 依赖的 input 字段都已在 Phase 1 定义。

## 4. Phase 3：step 细节填充

目标：为每个 step 填充 `preconditions`、`skills`、`extraction_schema`、`transitions.condition`。

### 4.1 step 文件结构

```yaml
step_id: step_1_check_port_vlan
name: 检查双端接口类型与 VLAN 配置
content: 在本端和对端执行 display port vlan，确认接口类型和 VLAN 配置一致。
type: diagnosis
preconditions:
  rules:
    - description: 需要本端和对端接口锚点。
      condition: input.current_hop.current_interface != '' and input.current_hop.peer_interface != ''
      on_fail:
        action: skip
        next_node: step_2_check_ip_interface
skills:
  - skill_id: skill_display_port_vlan
    target_device: current_device
    result_key: local_port_vlan
    inputs: {}
    selector: 按 {{ input.current_hop.current_interface }} 定位接口行。
    extraction_schema:
      - name: link_type
        type: string
        description: 接口链路类型，如 Access、Trunk 或 Hybrid
transitions:
  rules:
    - description: 接口类型一致，继续下一步。
      condition: extracted.local_port_vlan.link_type == extracted.peer_port_vlan.link_type
      next_node: step_2_check_ip_interface
  on_error:
    handler_execution_failed: CONCLUSION_HANDLER_EXECUTION_FAILED
    cli_command_execution_failed: CONCLUSION_CLI_COMMAND_EXECUTION_FAILED
    parse_failure: CONCLUSION_PARSE_FAILURE
```

### 4.2 preconditions

当 step 使用 `required: false` 的 input 字段或依赖前序 step 输出时，必须添加 preconditions：

- `on_fail.action: skip`
- `on_fail.next_node` 指向同链路下一个适用 step；如果没有后续 step 可省略。

### 4.3 skills

每个 skill 条目必须符合：

- `skill_id`：`skill_` + 命令语义，小写下划线。
- `target_device`：本端用 `current_device`，对端用 `peer_device`。
- `result_key`：同 step 多 skill、双端对比或同名字段时必须配置。
- `inputs`：命令有参数时用结构化来源；无参数写 `{}`。
- `selector`：表格输出必须写定位描述；全局统计或不可定位时可写 `null` 并说明原因。
- `extraction_schema`：只提取判断所需字段；configuration step 通常为空 `[]`。

inputs 推荐结构：

```yaml
inputs:
  interface_name:
    name: interface_name
    source_type: workflow_input
    source_key: input.current_hop.current_interface
    description: 当前设备待检查的接口名
```

### 4.4 extraction_schema 与 [custom]

| 情况 | 写法 |
|---|---|
| CLI 原生列名或字段 | `name` 写稳定字段名，`description` 写原始列含义 |
| 需要推理、聚合、语义判断 | `description` 以 `[custom]` 开头 |

要求：

- `[custom]` 不写进 `name`。
- `name` 使用稳定英文 snake_case。
- 每个字段都有 `type` 和 `description`。

### 4.5 transitions

- `rules` 是有序数组，首条命中即跳转。
- `condition` 必填，禁止空字符串。
- 无条件跳转写 `True`。
- 每条 rule 只能有 `next_node` 或 `next_workflow` 之一。
- 禁止跳转到同一 workflow 的其他 start_node。
- 每个 step 必须有 on_error 三条固定兜底。
- 禁止定义 `default` 字段。
- 入口链路末尾正常路径可不写 rule，让执行自然结束；若仍需人工确认，跳转到 warning/error conclusion。

condition 可引用：

```text
input.facts.xxx
input.current_hop.xxx
extracted.xxx
extracted.<result_key>.xxx
state.results.<step_id>.xxx
```

可用运算：`== != <= >= < > in not_in and or not ()`。

### 4.6 Phase 3 自检

- [ ] 引用 optional input 的 step 都有 preconditions。
- [ ] 所有 condition 非空。
- [ ] configuration step 使用 `condition: True` 无条件跳转。
- [ ] next_node 指向 Phase 2 已定义的 step 或 conclusion。
- [ ] 每个 step 有 on_error 三条。
- [ ] 同 step 多 skill 同名字段已配置 result_key。
- [ ] configuration step 的 extraction_schema 为空 `[]`。
- [ ] 没有定义 `default` 字段。

## 5. Phase 4：user_skills 与整体验证

### 5.1 user_skills

从所有 step 收集 skill_id，为每个新 skill 创建文件：

```yaml
skill_id: skill_display_port_vlan
description: 执行 display port vlan 命令并解析接口 VLAN 信息
action:
  type: cli_command
  commands: display port vlan
parser:
  method: llm
  data_type: command
default_schema:
  type: array
  items:
    type: object
    properties:
      interface:
        type: string
        description: Interface
      link_type:
        type: string
        description: Link Type
```

### 5.2 自动验证

最终交付前至少检查：

- workflow.yaml 能被 YAML 解析。
- steps/ 下每个 step 文件能被 YAML 解析。
- workflow.steps 与 steps 文件一一对应。
- start_node 指向已声明 step。
- 所有 next_node / on_error 目标都存在。
- 所有 `source_type: workflow_input` 的 `source_key` 在 input_schema 中定义。
- 所有 `source_type: step_output` 的 step 和字段存在。
- 所有 `skill_id` 在 user_skills 中存在。
- extraction_schema 字段来自对应 skill 的 default_schema，或在 description 中明确 `[custom]`。
- 不存在 `__NEED_FILL__`。
- 不存在 `transitions.default`。

### 5.3 人工复核清单

- [ ] 所有 start_node 覆盖可自动化诊断入口。
- [ ] 所有 step 的 content 清晰、单一职责、不含占位符。
- [ ] `[custom]` 使用正确。
- [ ] `skill_id` 使用 `skill_*`，原始 CLI 命令位于 user_skills。
- [ ] rules 顺序合理，特殊条件在前，兜底条件在后。
- [ ] on_error 三项完整。
- [ ] conclusions 的 level、message、suggestion 完整。
- [ ] 所有不自动化内容已进入 suggestion 或明确跳过。

## 6. 逐切片执行 SOP

对每个切片按以下流程执行：

1. 读取切片，判断文本型、表格型或混合型。
2. 规划本切片产生的 step 列表、首个 step 是否成为 start_node、是否新增 conclusions。
3. 按 Phase 1/2 更新骨架。
4. 第二阶段按 Phase 3/4 填充细节。
5. 展示本切片新增内容并暂停确认：
   - 本次切片文档名。
   - 新增 step 列表。
   - 新增 conclusions。
   - 新增或更新的 start_node。
   - 待回填或需人工确认的问题。
6. 用户确认后再处理下一个切片。

禁止在用户确认前开始下一个切片。

## 7. 常见模式

### 模式 A：双端对比

本端和对端分别执行同一命令 → 1 个 step + 2 个 skill + `result_key` 区分。

### 模式 B：链式深入排查

后续命令入参来自前序输出 → 每个子步骤独立 step。

示例：

```text
step_7: display traffic-policy applied-record → behavior_name
step_8: display traffic behavior <behavior_name> → classifier_name
step_9: display traffic classifier <classifier_name> → acl_number
step_10: display acl <acl_number> → rule_source_ip
```

### 模式 C：前后对比采样

基线 → 操作 → 二次采样 → 1 个 step + 3 个 skill，`result_key` 使用 `before`、`probe`、`after`。

### 模式 D：条件前置跳过

optional input 或可选链路信息缺失时，用 preconditions 跳过当前 step。

### 模式 E：跨 step 数据比对

先采本端统计，再采对端统计；对端 step 的 condition 引用 `state.results.<本端step>.<字段>`。

### 模式 F：提取值 vs 输入值比较

使用 `extracted.xxx == input.current_hop.yyy`。

### 模式 G：诊断→修复→复核

config step 后跳到后续 diagnosis；只在末尾汇聚时设置复核 step。

### 模式 H：按接口类型分支修复

diagnosis step 提取 link_type → Access/Trunk/Hybrid 三个 configuration step → 汇聚到后续 diagnosis。

## 8. 常见错误与避坑

### 8.1 路径和文件名猜测

必须先扫描真实文件名，禁止凭记忆写路径。

### 8.2 skill_id 格式混用

统一使用 `skill_*`。不要把原始 CLI 命令直接写在 step 的 `skill_id` 中；原始命令属于 user_skills 的 `action.commands`。

### 8.3 [custom] 位置错误

`[custom]` 只放在 description 开头，不放进 name。

### 8.4 `__NEED_FILL__` 残留

`__NEED_FILL__` 只允许中间阶段临时出现在 `next_node`，最终交付必须全部消除；禁止出现在 content、description、skill_id 等字段。

### 8.5 step_id 与文件名不一致

step 文件名必须等于内部 step_id 加 `.yaml`。

### 8.6 next_node 悬空引用

next_node 必须从 workflow.steps 或 conclusions 中复制，避免手打。

### 8.7 default 字段遗留

新抽取目标禁止 `transitions.default`。旧 YAML 中若存在 default，应迁移为显式 rule 或 conclusion。

## 9. 质量评分指标映射

质量评分工具应以本指南为准，至少覆盖以下维度：

| 维度 | 对应指南章节 | 主要检查 |
|---|---|---|
| 输入 Schema 完整性 | Phase 1 | facts/current_hop、必填基线、字段 type/required/description |
| 骨架拓扑一致性 | Phase 2 | start_node、steps、step 文件、conclusions、重复声明 |
| Step 内容完整性 | Phase 2/3 | step_id、文件名、name、content、type、preconditions、result_key |
| Skill 与抽取字段 | Phase 3/4 | skill_id、user_skills、inputs、selector、extraction_schema、[custom] |
| 条件表达式质量 | Phase 3 | condition 非空、next_node、extracted/input/state 引用合法性 |
| 错误兜底与可执行性 | Phase 4 | on_error、系统 conclusion、conclusion level/message/suggestion、禁止 default |

评分结果只能作为结构质量和规则符合度参考，不能替代人工核对源文档语义。
