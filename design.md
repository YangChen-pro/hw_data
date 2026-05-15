# 三层架构设计

## 第一层：Workflow 层
位置：`xxx/workflow.yaml`

字段说明：

1. `workflow_id`
   workflow 唯一标识，要求全局唯一且稳定（建议前缀 `wf_`）。

2. `name`
   workflow 故障名称。

3. `input_schema`
   workflow 输入定义。每个字段为对象，包含 `name`、`type`、`required`、`description`、`properties`。

   规则：
   - `required: true` 缺失时，不启动 workflow。
   - `required: false` 缺失时，统一注入空串 `''`。
   - step 使用可选字段前，必须做非空判断（建议放 `preconditions`）。

   建议输入：
   - `facts`：通用事实输入。
   - `current_hop`：排障锚点。

   `current_hop` 基线必填字段：
   - `hop_index`、`current_device`、`path_state`（建议值：`resolved|partial|failed`）

   `current_hop` 两种模型：
   - 双设备模型：`current_interface`、`peer_device`、`peer_interface`
   - 单设备上下行口模型：`current_interface`（下行口）、`interconnect_interface`（上行/互联口）

   其他字段按场景扩展（如 `next_hop_ip`、`vlan_id`、`eth_trunk_id`、`vlanif_interface`、`peer_vlanif_interface`、`forwarding_mode`）。

4. `start_node`
   入口节点列表，可配置多个。每个入口包含：
   - `step_id`：入口 step ID。
   - `description`：入口链路说明。

   执行模式（顺序）：
   - 按 `start_node` 列表顺序执行。
   - 前一条入口链路命中故障结论后，停止后续入口。
   - 前一条入口链路未命中故障结论时，继续下一个入口。

   step 不适用（skip）规则：
   - 关键依赖为空串 `''` 时，skip 当前 step，不执行 skill。
   - skip 优先走当前链路正常 `next_node`。
   - 不在 step 内显式跳转“下一个 `start_node`”；由编排器在当前入口链路结束后进入下一个入口。

   当前入口链路结束规则：
   - `transitions.rules` 全部未命中时，默认视为当前入口链路结束。
   - 该结束语义为执行器隐式行为，不写入 YAML，不展示为页面节点或边。
   - 当前入口链路结束且未命中故障结论时，由编排器按 `start_node` 顺序进入下一个入口。

5. `steps`
   workflow 涉及的 step ID 列表，仅用于声明。应覆盖 workflow 中会被引用的所有 step。

6. `conclusions`
   workflow 结论集合。每个结论包含：
   - `level`：`warning|error`
   - `message`：根因描述
   - `suggestion`：修复建议
   - `repair_action`：可自动化执行的修复动作（无则留空）

   页面展示约定：
   - `on_error` 专用的系统结论可以保留在 YAML 中供运行时兜底使用。
   - 系统结论不要求在页面中展示为可编辑 conclusion 节点。

## 第二层：Workflow Step 层
位置：`xxx/steps/step_xxx.yaml`

字段说明：

1. `step_id`
   step 的唯一标识。

2. `name`
   步骤名称，简短明确。

3. `content`
   步骤说明。

4. `skills`
   当前 step 调用的 skill 列表，可配置多个，按顺序串行执行。

   每个 skill 包含：
   - `skill_id`：skill 唯一标识。
   - `target_device`：目标设备标识（应来自 `current_hop` 或可解析上下文）。
   - `result_key`：可选，结果命名空间；配置后按 `extracted.result_key.xxx` 访问。
   - `inputs`：入参映射，字段包含 `name`、`source_type`、`source_key`、`description`。
     `source_type` 取值：`step_output`、`workflow_input`、`user_input`、`constant`。
   - `selector`：可选，定位目标内容的规则描述。
   - `extraction_schema`：当前 step 要提取的字段。

   约定：
   - 同一步内多个 skill 输出字段同名时，必须配置 `result_key`。
   - `extraction_schema` 字段必须来自对应 `skill.default_schema`，不允许为场景重命名字段。
   - 多对象比对统一通过 `extracted.result_key.xxx` 引用。

5. `transitions`
   当前 step 流转逻辑，包含 `rules`、`on_error`。

   `rules` 约定：
   - `rules` 为有序数组，按顺序匹配，首条命中即跳转。
   - 每条 rule 包含：
     - `description`：规则说明
     - `condition`：必填表达式（禁止空 `condition`；无条件匹配请写 `True`）
     - `next_node` 或 `next_workflow`：二选一
   - 若 `rules` 为空，或全部 `rules` 均未命中，则隐式结束当前入口链路。
   - `condition` 可引用：
     - `input.xxx`
     - `state.results.step_xxx.yyy`
     - `extracted.xxx` 或 `extracted.result_key.xxx`
   - 支持运算符：`==`、`!=`、`<=`、`>=`、`<`、`>`、`in`、`not in`、`and`、`or`、`not`、`()`
   - 支持函数（可扩展）：`check_same_subnet(ip_with_mask_a, ip_with_mask_b)`

   `rules` 设计约束（强约束）：
   - 不允许配置 `default`。
   - 仅在需要显式跳转时写 `rules`；链路结束不通过 rule 表达。
   - 允许的去向：异常结论、链内其他 step、`next_workflow`。
   - 不允许输出“无故障结论”（包括 `CONCLUSION_CURRENT_BRANCH_NO_ISSUE` 一类结论）。
   - 不允许显式跳转到同一 workflow 的其他 `start_node`；切换入口只能由编排器完成。
   - `rules` 可以按顺序组织互斥分支（如 `A==true` / `A==false`）；若未覆盖完整决策面，则剩余路径隐式结束当前入口链路。

   `on_error`：
   - 定义执行失败兜底（如 handler 失败、命令失败、解析失败）的结论去向。

6. `preconditions`（可选）
   前置适用性检查，在 `skills` 前执行。

   结构：
   - `rules`：
     - `description`
     - `condition`（语法与 `transitions.condition` 一致）
     - `on_fail`：
       - `action`：建议固定 `skip`
       - `next_node`：可选，未配置则按当前链路默认收敛

   约定：
   - `preconditions` 不通过时，不执行任何 skill。
   - `preconditions` 只负责“step 是否适用”。
   - `transitions` 只负责“skills 执行后的结果判断”。

## 第三层：Skill 层
位置：`skills/skill_xxx.yaml`

skill 是可复用的“命令执行 + 回显解析”定义。

字段说明：

1. `skill_id`
   skill 唯一标识，建议命名：`skill_` + 命令固定语义（小写，下划线分隔）。

2. `description`
   skill 功能描述，说明“执行什么、产出什么”。

3. `action`
   执行定义，包含：
   - `type`：支持 `cli_command`、`function_call`。
   - `commands`：当 `type=cli_command` 时必填，表示执行命令内容。
   - `function_name`：当 `type=function_call` 时必填，表示调用的函数名。
   - `arguments`：当 `type=function_call` 时可选，表示函数入参定义。

4. `parser`
   解析定义，包含：
   - `method`：当前统一为 `llm`。
   - `data_type`：当 `action.type=cli_command` 时为 `command`；当 `action.type=function_call` 时为 `function_call`。
   - `default_schema`：该 skill 可解析的完整字段并集。

5. `default_schema` 约定
   - 标量字段：定义 `type`、`description`（可选 `enum`）。
   - 表格字段：`type: array`，`items.type: object`，行字段放在 `items.properties`。
   - 表格字段建议以 `_table` 结尾（如 `interface_table`）。
   - 同一命令在不同回显分支出现字段差异时，按并集建模。
   - 不存在的标量字段返回 `null`，不存在的表格返回 `[]`。

6. 与 Step 层协同约束
   - step 的 `extraction_schema` 只能引用 skill 的 `default_schema` 字段。
   - 若 step 需要按行提取表格字段，必须先通过 `selector` 定位目标行。
   - skill 层不承载业务判断逻辑；业务判断放在 step 的 `transitions.rules`。

## 页面映射

页面用于将三层结构映射为可视化 workflow 图，三层 YAML 仍然是唯一数据源。

1. 图节点
   - `step` 与 `conclusion` 都展示为节点。
   - `start_node` 对应节点增加 `Start` 标记。
   - `conclusion` 节点仅允许 `warning|error`。
   - `on_error` 专用的系统结论可不展示为图节点。

2. 图边
   - 仅根据 `transitions.rules` 生成边。
   - `next_node` 生成普通边；`next_workflow` 生成跨 workflow 特殊边。
   - 隐式结束当前入口链路不生成图边。

3. 右侧面板
   - 点击节点后编辑详情。
   - `skills` 以可排序子卡片展示。
   - `conclusion` 支持直接编辑 `level/message/suggestion/repair_action`。

4. skill 编辑
   - 页面按 `skill_id` 选择或新建 skill。
   - `action.type` 支持 `cli_command`、`function_call`。
   - 当 `type=cli_command` 时编辑 `commands`。
   - 当 `type=function_call` 时编辑 `function_name`、`arguments`。
   - 基于 skill 的 `default_schema` 辅助编辑 step 的 `selector` 与 `extraction_schema`。

5. transitions 编辑
   - 在节点详情中统一编辑 `rules`（有序列表）。
   - 每条 rule 必须填写 `description`、`condition`、跳转目标（`next_node` 或 `next_workflow`）。
   - 禁止空 `condition`；无条件规则必须显式写 `True`。
   - 页面需阻止“同一 rule 同时填写 `next_node` 与 `next_workflow`”。
   - 页面需阻止“rule 跳转到无故障结论”。
   - 页面不展示“当前入口链路结束”的隐式语义。

6. 保存方式
   - 页面保存整个图模型。
   - 保存时回写三层 YAML，保持字段与顺序规则一致。

## 自动化检查

建议提供独立检查脚本，对单个或多个 workflow 做结构和引用校验。

第一版检查项：

1. YAML 解析检查
   - `workflow.yaml`、`steps/*.yaml`、`skills/*.yaml` 均可解析。

2. Workflow 结构检查
   - `workflow.steps` 中声明的 step 文件必须存在。
   - `start_node.step_id` 必须引用已定义 step。
   - `conclusions` 的 `level` 只能是 `warning|error`。
   - 禁止定义或引用无故障结论（如 `*_NO_ISSUE`）。

3. Step 与 transitions 检查
   - `transitions.rules` 必须为数组，可为空数组。
   - 每条 rule 的 `condition` 必填且非空。
   - 每条 rule 必须且仅能设置 `next_node` 或 `next_workflow` 之一。
   - 不允许配置 `transitions.default`。
   - `next_node` 必须引用已定义 step 或 conclusion。
   - `next_workflow.workflow_id` 必须存在；若填写 `start_node`，必须是目标 workflow 合法入口。
   - 不允许 rule 直接跳转到同一 workflow 的其他 `start_node`。

4. Skill 定义与引用检查
   - step 中 `skill_id` 必须存在于 `skills/*.yaml`。
   - `action.type` 只能是 `cli_command` 或 `function_call`。
   - `type=cli_command` 时必须有 `commands`。
   - `type=function_call` 时必须有 `function_name`，`arguments` 可选。
   - `parser.data_type` 必须与 `action.type` 匹配（`command`/`function_call`）。
   - step 的 `extraction_schema` 只能引用对应 skill 的 `default_schema`。

5. 输入参数与引用检查
   - `source_type` 只能是 `step_output`、`workflow_input`、`user_input`、`constant`。
   - `workflow_input` 必须引用 `input.xxx` 且在 `input_schema` 中定义。
   - `step_output` 必须引用 `state.results.step_xxx.yyy` 且对应 step/字段存在。
   - `user_input` 的 `source_key` 不能为空。

6. 可达性与收敛性检查
   - 从 `start_node` 出发不可达的 step 或 conclusion 给出告警。
   - 不要求每个 step 用 `rules` 覆盖完整决策面；未命中路径默认隐式结束当前入口链路。
