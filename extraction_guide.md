# 网络故障排查 Markdown → YAML 抽取操作手册

> **使用方式**：本手册分为 **两个输出阶段**，必须严格按顺序执行。
>
> **第一次输出（骨架）**：执行 Phase 1 + Phase 2，输出 input_schema + step 列表 + start_node + conclusions + transitions 拓扑。输出后执行骨架自检清单。
>
> **第二次输出（细节）**：执行 Phase 3 + Phase 4，为每个 step 填充 skills/preconditions/transitions 表达式 + 创建 skill 文件。输出后执行细节自检清单。
>
> **⚠️ 严禁在第一次输出中填写 skills/extraction_schema 等细节。先把骨架做对，再填细节。**

---

## Phase 1：input_schema 设计

> 目标：输出 `facts` 和 `current_hop` 的完整 properties 列表。

### 1.1 必填基线（直接写入，不需要从 markdown 推导）

```yaml
current_hop:  # required: true
  hop_index:    { type: integer, required: true,  description: 当前跳索引 }
  current_device: { type: string,  required: true,  description: 当前设备管理IP }
  path_state:   { type: string,  required: true,  description: 路径状态(resolved|partial|failed) }
```

### 1.2 模型选择（从 markdown 判断）

阅读 markdown，判断场景模型：
- **双设备模型**（如 SwitchA ↔ SwitchB，两端设备对比排查）→ 加入：
  - `peer_device` (str, **required: true**)
  - `current_interface` (str, opt)
  - `peer_interface` (str, opt)
- **单设备上下行口模型**（如 VLAN 场景，在一台设备上排查接入侧+互联侧）→ 加入：
  - `current_interface` (str, opt) — 接入侧/下行口
  - `interconnect_interface` (str, opt) — 互联侧/上行口

### 1.3 扩展字段推导（逐条追溯法）

**依次执行以下 5 步，每发现一个依赖就加一个字段。Step A~E 推导出的字段都是必要字段，必须全部加入 input_schema，不可跳过。**

**Step A — display 命令入参扫描**：
逐条检查 markdown 中每个 `display xxx <参数>` 命令。如果参数**不来自前序 step 的提取结果**，就需要一个 input_schema 字段。
> 例：`display eth-trunk trunk-id` → 需要 `eth_trunk_id`
> 例：`display ip routing-table ip-address` → 需要 `next_hop_ip`
> 例：`display vlan vlan-id` → 需要 `vlan_id`
> 例：`display acl <number>` → number 来自前序 step → 不需要新字段

**Step B — selector 定位字段扫描**：
对于输出为表格的命令，需要按某个字段定位目标行。这个定位字段如果来自 input 而非 extracted，就需要一个字段。
> 例：`display port vlan` 按接口名定位 → 复用 `current_interface`
> 例：`display ip interface brief` 按 VLANIF 名定位 → 需要 `vlanif_interface`
> 例：`display mac-address` 按终端 MAC 定位 → 终端 MAC **无法通过 display 命令从设备获取** → 放入 `facts.terminal_mac`

**Step C — 跨 step 比对字段扫描**：
PDF 中"对比两端"或"与输入值比较"的场景，检查比对用的锚点是否都有字段。
> 例：ACL source_ip 与 peer_device 比对 → `peer_device` 已有

**Step D — 无法自动获取的外部信息 → 放入 `facts`**：
PDF 中提到的信息，如果**无法通过在被管设备上执行 display 命令获取**，必须放入 `facts`。这包括两类：
1. **终端侧属性**：需要从终端设备或外部系统获取的信息
   > 例：终端 MAC 地址 → `facts.terminal_mac`
   > 例：终端静态 ARP 状态（correct/incorrect/unknown）→ `facts.terminal_static_arp_status`
2. **配置意图**：step 执行配置命令时需要知道的目标状态，但无法从当前 display 输出推断
   > 例：Hybrid 接口 tagged/untagged 模式 → `facts.hybrid_vlan_mode`

**Step E — 外部提供的判断依据扫描**：
PDF 中有些排查步骤的判断逻辑**不依赖 display 命令输出**，而是**直接消费一个外部提供的状态值**。这类状态值也必须作为 input 字段。
> 例：PDF 说"检查终端设备上是否配置了错误的静态 ARP"→ 这无法在被管设备上 display 获取，需要外部告知结果 → `facts.terminal_static_arp_status`
> 判断方法：如果某个 step 的 transitions 条件中需要引用一个**不来自任何 skill 提取结果**的字段，那个字段就是外部判断依据，必须放入 input_schema。

### 1.4 字段归属判断：current_hop vs facts

- **current_hop**：描述**当前排查对象（设备/接口/链路）的属性**——设备名、接口名、VLAN ID、IP 地址等
- **facts**：描述**终端设备/外部系统的状态**或**配置意图**——终端 MAC、终端 ARP 状态、Hybrid 模式等

> 简单判断：如果这个信息是"被管设备的属性"→ current_hop；如果是"终端/外部的信息"→ facts

### 1.5 ⚠️ input_schema 边界规则

**先做加法，再做减法**：
1. ✅ **必须加入**：Step A~E 推导出的每一个字段都是必要的，不可因为"看起来像推测"而跳过。如果 Step A~E 能给出明确来源依据（哪条命令/哪个 selector/哪个判断需要它），就必须加入。
2. ❌ **禁止加入**：只有以下情况才不加：
   - markdown 中完全**未提及**的辅助字段（如 `scenario`、`forwarding_mode` 等推测性字段）
   - start_node 分发逻辑字段（多入口直接用 `start_node` 数组实现，不需要 `scenario` 字段）
   - workflow 可从 display 输出自动推断的信息（如 `link_type` 可从 display port vlan 提取，不需要作为 input）

### 1.6 Phase 1 自检

- [ ] current_hop 包含 3 个必填基线字段
- [ ] 模型选择字段已加入（双设备 or 单设备上下行口）
- [ ] 每个 `display xxx <参数>` 命令的参数都有来源（input_schema 字段或前序 step 输出）
- [ ] 每个 selector 定位用的字段都有来源
- [ ] 所有无法通过 display 自动获取的信息都放入了 facts
- [ ] **判断逻辑中需要消费但不来自任何 skill 提取结果的字段**，已作为 input（通常放 facts）
- [ ] **每个字段都标注了来源依据**（哪条命令/哪个 selector/哪个判断需要它）
- [ ] 没有添加 markdown 未提及且无来源依据的推测性字段
- [ ] facts 对象已创建（即使当前场景无 facts 字段，也应写为 `facts: { properties: [] }`）
- [ ] current_hop vs facts 归属正确（设备属性→current_hop，终端/外部状态→facts）

---

## Phase 2：骨架设计（step 列表 + start_node + transitions 拓扑 + conclusions）

> 目标：确定有多少个 step、如何串联、每个异常分支对应什么结论。**不填 skills 细节。**

### 2.1 识别 start_node

**规则**：PDF 中每个**顶级排查章节**（如 15.2.2、15.2.3）对应一个 `start_node` 入口链路。

- 章节内部的子步骤链（如"先查路由再查策略路由"）属于同一入口链路的多个 step，**不**各自成为 start_node。
- start_node 按 PDF 排查顺序排列。
- **执行语义**：顺序执行，命中故障结论后停止后续入口。
- 不纳入自动化的章节（纯人工/抓包/信息收集）**不**生成 start_node。

### 2.2 拆分 step（逐章节执行）

对 markdown 的每个排查章节，按以下规则拆分：

| 场景 | 拆法 |
|------|------|
| 1 条命令 + 1 个判断 | 1 个 step |
| 多条命令，**共同服务同一判断**（如 STP + RRPP + Smart Link 判断"是否被阻塞"） | 1 个 step，多个 skill |
| 多条命令，各自做**独立判断** | 多个 step，transitions 串联 |
| **链式数据传递**（a 的输出是 b 的入参） | **每个子步骤必须独立 step**，禁止合并 |
| 同一命令在**本端和对端**各执行一次，**同一 step 内对比** | 1 个 step + 2 个 skill（result_key 区分） |
| 同一命令在**本端和对端**各执行一次，需要**跨 step 比对**（如先本端统计再对端统计，两个 step 的判断逻辑不同） | 拆为 **2 个独立 step** |
| 对**同一设备的同一接口类型**的多个接口（如 current_interface + interconnect_interface）执行同一命令 | 1 个 step + 2 个 skill（result_key 区分，不要拆成 2 个 step） |

**关键提醒**：
- 对"同一设备的多个接口各查一次"的场景，优先合并为 **1 个 step 多 skill**（用 result_key 区分），而不是拆成多个 step。拆为多 step 的前提是**判断逻辑不同**。
- step_id 格式：`step_{序号}_{动词}_{对象}`，序号全局递增，允许跳号和子编号（如 10a/10b/10c）。

### 2.3 确定每个 step 的 type

- `diagnosis`：仅执行 display 查询命令。**绝大多数 step 都是 diagnosis。**
- `configuration`：step 本身执行**在当前被管设备上的配置修改命令**（如 `vlan`、`port default vlan`）。

**⚠️ 何时不创建 configuration step（逐条检查）：**
1. 修改操作需在**终端设备**上执行（如修正终端静态 ARP）→ **只出结论**
2. 修改操作需**人工现场**操作（如更换网线、调整指示灯）→ **只出结论**
3. PDF 说"请取消/请修改"但属于**建议性修改**（如端口隔离：检测到后出结论，repair_action 给出 undo 命令）→ **只出结论**
4. PDF 是**配置检测类**章节（如 LNP/OPS，只判断配置对不对 → 不对就出结论）→ **只出结论**

**简单判断公式**：修复主体是当前被管设备 + 可用 system-view 配置命令完成 + PDF 描述是"必须修复才能继续排查"的强制修复 → config step。其余 → 结论。

### 2.4 诊断→修复→复核 模式（模式 G）

- **configuration step 完成后**，用 `condition: True` 直接跳到排查流程中的**下一个 diagnosis step**（不创建独立 verify step）。
- 后续 diagnosis step **自然承担**"验证修复结果"的职责。
- 仅在整条入口链路**末尾**、所有修复分支**汇聚**后，才设 1 个专门的复核 step。

### 2.5 按接口类型分支修复（模式 H）

当需要按 link_type（Access/Trunk/Hybrid）执行不同的配置命令时：
- 1 个 diagnosis step 检查并提取 link_type → 按 link_type 分流
- 3 个 configuration step（Access/Trunk/Hybrid），每个用 `condition: True` 汇聚到同一后续 step

### 2.6 确定 conclusions

**对每个 step 的每个异常判断分支，创建一个独立的 conclusion。**

规则：
- 如果一个 step 提取了多个字段，对**不同字段的异常**分别判断 → 每种异常一个独立 conclusion
  > 例：display port vlan 提取 link_type 和 vlan_list → "link_type 不一致"和"vlan_list 不一致"是两个独立 conclusion
- **固定系统三条**（必须逐字复制，一字不差）：
  ```
  CONCLUSION_HANDLER_EXECUTION_FAILED
  CONCLUSION_CLI_COMMAND_EXECUTION_FAILED
  CONCLUSION_PARSE_FAILURE
  ```
- **防御性 conclusion**（warning）：当提取字段可能为空导致无法完成判断时
- **兜底 conclusion**（warning）：检查正常但故障仍存在、需进一步抓包等
- **通用结论模板**（每个 workflow 都应考虑是否需要以下通用结论）：
  - `CONCLUSION_MANUAL_CHECK`（error）：无法自动判断、需人工介入时的通用兜底
  - `CONCLUSION_ESCALATE_WITH_DEVICE_INFO`（error）：所有排查步骤完成仍无法定位、需升级技术支持时
  - `CONCLUSION_CHECK_PACKET_TX_RX`（warning）：需进一步做报文收发统计/抓包确认时
- 命名规则：`CONCLUSION_` + 全大写下划线语义
- level：故障=error，兜底/防御性=warning，系统兜底=warning
- **禁止**定义"无故障结论"（如 `CONCLUSION_NO_ISSUE`）

### 2.7 不纳入自动化的内容

以下 PDF 内容**不**转成 step：
1. **纯人工操作**：查看指示灯、更换光模块/网线
2. **抓包/镜像操作**：端口镜像、流镜像、capture 命令
3. **信息收集与升级**：收集诊断信息联系技术支持 → 可在 conclusion 的 suggestion 中体现
4. **命令格式检查**：如"是否使用了 -f 参数"
5. **纯人工修改**：如"检查终端 IP 是否同一网段，不是请修改"——修改操作在终端设备上，不涉及 display 命令自动判断

### 2.8 Phase 2 自检（⚠️ 必须逐条执行！）

- [ ] start_node 数量 = markdown 中**可自动化**的顶级排查章节数（跳过纯人工/抓包/信息收集章节）
- [ ] 链式数据传递的子步骤（命令 b 的入参来自命令 a 的输出）都拆为**独立 step**
- [ ] 本端+对端需要**跨 step 比对**的场景拆为 2 个独立 step
- [ ] 同一设备的多个接口执行同一命令 → 合并为 1 step 多 skill，而非拆成多个 step
- [ ] 没有为端口隔离/静态ARP/LNP 等"检测→出结论"场景创建 configuration step
- [ ] configuration step 后没有创建独立的 verify step
- [ ] 仅在入口链路末尾汇聚处设了复核 step（如果有的话）
- [ ] 每个异常判断分支都有对应的独立 conclusion
- [ ] 固定系统三条结论名称已**逐字复制**（CONCLUSION_HANDLER_EXECUTION_FAILED / CONCLUSION_CLI_COMMAND_EXECUTION_FAILED / CONCLUSION_PARSE_FAILURE）
- [ ] 已评估是否需要通用结论（CONCLUSION_MANUAL_CHECK / CONCLUSION_ESCALATE_WITH_DEVICE_INFO / CONCLUSION_CHECK_PACKET_TX_RX）
- [ ] 不纳入自动化的 PDF 内容没有被转成 step
- [ ] **没有添加 markdown 中未提及的额外 step 或字段**（如 scenario 分发 step）
- [ ] step 总数与 markdown 中可自动化的检查判断点数量**匹配**
- [ ] **回顾 Phase 1 的 input_schema**：确认骨架中每个 step 依赖的输入字段都已在 Phase 1 中定义（如果发现遗漏，回到 Phase 1 补充）

---

## Phase 3：step 细节填充

> 目标：为 Phase 2 骨架中的每个 step 填充 skills、preconditions、extraction_schema、transitions 表达式。

### 3.1 preconditions

当 step 使用了 `required: false` 的 input 字段或前序 step 输出时，**必须**加 preconditions 做非空判断。
- on_fail.action: skip
- on_fail.next_node: 若同链路还有后续 step 则指向它；否则省略

### 3.2 skills 填充

每个 skill 条目：
- `skill_id`：`skill_` + 命令语义小写下划线
- `target_device`："在 SwitchA/本端执行" → `current_device`；"在 SwitchB/对端执行" → `peer_device`
- `result_key`：同 step 内多个 skill 有同名提取字段时**必须**配置；双端对比模式推荐始终配置（如 `local_xxx`/`peer_xxx`）
- `inputs`：命令有参数→映射（source_type: workflow_input / step_output / constant）；无参数→`{}`
- `selector`：表格输出→必须写定位描述；单一对象/全局统计→`null`
- `extraction_schema`：只提取判断所需字段；configuration step 通常为空 `[]`

### 3.3 transitions 填充

- rules 有序数组，首条命中即跳转
- condition **必填**，禁止为空；无条件匹配写 `True`
- 入口链路**末尾正常路径**→不写 rule（隐式结束）
- 每个 step 必须有 on_error 三条固定兜底
- **禁止**跳转到同一 workflow 的其他 start_node
- **禁止**定义 `default` 字段

### 3.4 condition 语法参考

```
引用：input.xxx / state.results.step_xxx.yyy / extracted.xxx / extracted.result_key.xxx
运算：== != <= >= < > in not_in and or not ()
函数：check_same_subnet(ip_with_mask_a, ip_with_mask_b)
```

### 3.5 Phase 3 自检

- [ ] 引用 `required: false` 输入的 step 都有 preconditions
- [ ] 所有 condition 非空
- [ ] 每条 rule 只有 next_node 或 next_workflow 之一
- [ ] 所有 next_node 引用的 step/conclusion 已在 Phase 2 中定义
- [ ] 每个 step 有 on_error 三条
- [ ] 同 step 多 skill 有同名字段时配置了 result_key
- [ ] configuration step 的 extraction_schema 为空 `[]`
- [ ] configuration step 的 transitions 使用 `condition: True` 无条件跳转

---

## Phase 4：Skill 层 + 整体一致性校验

### 4.1 创建 user_skills

从所有 step 中收集 skill_id，为每个新 skill 创建 YAML：
```yaml
skill_id: skill_display_xxx
description: 执行 display xxx 命令
action:
  type: cli_command
  commands: "display xxx"
parser:
  method: llm
  data_type: command
default_schema:
  # 标量：type + description
  # 表格：type: array, items.type: object, items.properties
```

### 4.2 整体一致性校验

- [ ] 所有 `source_type: workflow_input` 的 `source_key` 在 Phase 1 的 input_schema 中有定义
- [ ] 所有 `source_type: step_output` 的 `source_key` 对应 step 和字段存在
- [ ] 从每个 start_node 出发，所有 step 和 conclusion 均可达
- [ ] step 中 `skill_id` 在 user_skills 中存在
- [ ] extraction_schema 字段名来自对应 skill 的 default_schema
- [ ] PDF 中描述的每个排查分支都有对应的 step 或标记为"不自动化"

---

## 附录 A：常见转换模式速查

### 模式 A：双端对比
在本端和对端分别执行同一命令 → 1 个 step + 2 个 skill + result_key 区分

### 模式 B：链式深入排查
子步骤间有数据传递依赖 → **每个子步骤必须独立 step**

例：策略路由 4 步链
```
step_7: display traffic-policy applied-record → 提取 behavior_name
step_8: display traffic behavior <behavior_name> → 提取 classifier_name (输入来自 step_7)
step_9: display traffic classifier <classifier_name> → 提取 acl_number (输入来自 step_8)
step_10: display acl <acl_number> → 提取 rule_source_ip (输入来自 step_9)
```

例：黑名单 3 步链
```
step_13: display cpu-defend policy → 提取 policy_name
step_14: display cpu-defend policy <policy_name> → 提取 blacklist_acl_number (输入来自 step_13)
step_15: display acl <acl_number> → 提取 rule_source_ip (输入来自 step_14)
```

### 模式 C：前后对比采样
基线→操作→二次采样 → 1 个 step + 3 个 skill（result_key: before/probe/after）

### 模式 D：条件前置跳过
preconditions 判断可选字段非空

### 模式 E：跨 step 数据比对
本端统计 → 对端统计（**2 个独立 step**），对端 step 的 condition 引用 `state.results.本端step.字段`

### 模式 F：提取值 vs 输入值比较
condition 中用 `extracted.xxx == input.current_hop.yyy` 比对

### 模式 G：诊断→修复→复核
config step 后直接跳下一个 diagnosis → 仅末尾汇聚处设 1 个复核 step

### 模式 H：按接口类型分支修复
diagnosis step 按 link_type 分流 → 3 个 config step → 各用 `condition: True` 汇聚到同一后续 step

---

## 附录 B：命名规范

| 对象 | 格式 | 示例 |
|------|------|------|
| workflow_id | `wf_{场景}` | `wf_check_ping_command` |
| step_id | `step_{序号}_{动词}_{对象}` | `step_1_check_port_vlan` |
| skill_id | `skill_{命令语义}` | `skill_display_port_vlan` |
| conclusion | `CONCLUSION_{全大写语义}` | `CONCLUSION_PORT_LINK_TYPE_MISMATCH` |
| result_key | `{位置}_{对象}` | `local_port_vlan` |

---

## 附录 C：不纳入自动化的内容

1. **纯人工操作**：查看指示灯、更换光模块/网线
2. **抓包/镜像操作**：端口镜像、流镜像、capture 命令
3. **信息收集与升级**：收集诊断信息联系技术支持 → 可在 conclusion 的 suggestion 中体现
4. **命令格式检查**：如"是否使用了 -f 参数"
5. **终端侧人工修改**：如"检查终端 IP 是否同一网段，不是请修改"
