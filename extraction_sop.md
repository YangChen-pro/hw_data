# Workflow 提取 SOP（多文档切片 → 完整 Workflow）

版本：v1.1 | 日期：2026-03-29
来源：基于 ping不通 诊断项目的真实提取经验总结

---

## 0. 概述与参考资料

### 0.1 任务目标
将一组故障诊断切片源文档，逐个提取为 GenericAgent 可执行的 Workflow 格式。
**核心原则：逐文档提取，每完成一个切片必须暂停等待用户确认，不得一次性提取所有文档。**

### 0.2 输出目录结构

    <项目名>_extract/
    ├── workflow.yaml
    └── steps/
        ├── step_0_xxx.yaml
        ├── step_1_xxx.yaml
        └── ...

### 0.3 参考格式文档路径（可直接查阅）

- 参考 workflow：`./ping/ping_extract/workflow.yaml`
- 参考 step 文件：`./ping/ping_extract/steps/`（可 ls 查看所有示例）
- 源切片文档示例：`./ping/ping不通步骤/`

---

## 1. 启动阶段：询问路径与初始化

### 1.1 向用户询问路径

执行提取任务前，必须先向用户询问以下信息：

    问题1：切片文档所在文件夹路径？
           （例：./ping/ping不通步骤/）
    
    问题2：输出文件夹路径？
           （例：./ping/ping_extract/，如不存在将自动创建）

### 1.2 扫描切片文档列表

用 `ls` 或 `os.listdir` 列出切片文件夹中的所有文档，**禁止猜测文件名**。

    import os
    files = sorted(os.listdir("<切片文件夹路径>"))
    # 过滤出 .md 或 .txt 文件
    slice_docs = [f for f in files if f.endswith('.md') or f.endswith('.txt')]
    for i, f in enumerate(slice_docs):
        print(f"{i+1}. {f}")

向用户展示文档列表，并说明拟处理顺序（通常按文件名排序）。

### 1.3 初始化输出目录与 workflow 骨架

创建输出文件夹和 steps/ 子目录，并写入 **workflow.yaml 空骨架**（后续逐步填充）：

```yaml
workflow_id: <项目名_workflow>
name: "<中文名称>"
version: "1.0"
description: "<待完善>"
input_schema: {}

start_node: []

steps: []

conclusions:
  CONCLUSION_MANUAL_CHECK:
    level: error
    message: "无法自动判断，需人工介入"
    suggestion: "请联系网络管理员"
```

> 注意：start_node、steps、conclusions（除默认的 MANUAL_CHECK 外）都是空的，将在后续提取每个切片时逐步追加。

---

## 2. 核心循环：逐切片文档提取

**对每一个切片文档，严格按照以下子步骤执行，最后必须暂停等待用户确认。**

---

### 2.1 读取并分析切片文档

    file_read(<切片文档路径>)

判断文档类型：
- **文本型**：以自然语言描述步骤为主，夹杂 CLI 代码块
- **表格型**：核心内容为 Markdown 表格（如告警对照表、字段说明表）
- **混合型**：两者兼有

### 2.2 规划本文档产生的 step 列表

根据文档的子章节自然划分，记录：
- 本文档将产生哪些 step（N个步骤）
- 各 step 的 step_id（延续全局编号，不重置）
- 本文档的第一个 step 是否为新的 start_node（通常是）
- 本文档是否引入新的 conclusions

**step 编号规则**：全局连续，不按文档重新编号。
例：前一个文档最后是 step_4，本文档从 step_5 开始。

**step_id 命名规则**：`step_N_动词_名词` 格式，全小写英文下划线。

### 2.3 提取各 step 文件

对本文档的每个子章节，创建对应的 step yaml 文件。

**step 文件完整结构**：

```yaml
step_id: step_N_verb_noun
name: "中文步骤名称"
content: "详细说明：本步骤检查xxx，通过xxx命令获取xxx，判断xxx"
type: diagnosis

skills:
  - skill_id: "display stp brief"
    inputs: {}
    selector:
    extraction_schema:
      - name: stp_state
        description: "[custom] STP端口是否处于Discarding状态"
        type: string
      - name: learned_from
        description: "Learned-From"
        type: string

transitions:
  rules:
    - description: "条件描述"
      condition: "extracted.stp_state == 'DISCARDING'"
      next_node: step_X_xxx
    - description: "其他情况"
      condition: ""
      next_node: step_Y_xxx
  on_error:
    handler_execution_failed: CONCLUSION_MANUAL_CHECK
    cli_command_execution_failed: CONCLUSION_MANUAL_CHECK
    parse_failure: CONCLUSION_MANUAL_CHECK
  default: CONCLUSION_MANUAL_CHECK
```

#### 字段填写规则详解

**step_id / 文件名**
- 文件路径：`steps/step_N_verb_noun.yaml`
- step_id 与文件名（去掉 .yaml）完全一致

**type 字段**
- `diagnosis`：只读命令（display/show 类）
- `configuration`：写入命令（undo/interface/ip address 类）

**skill_id 格式（踩坑重灾区）**

    正确：  "display stp brief"
    正确：  "display logbuffer"
    正确：  "display ip routing-table"
    正确：  "display acl 3000"
    错误！  "display_stp_brief"          ← 禁止用下划线替代空格
    错误！  "display_logbuffer"           ← 此坑在 ping 项目中大量出现
    错误！  "displayStpBrief"             ← 禁止驼峰命名

**inputs 字段**

无参数时写 `inputs: {}`，有动态参数时：

```yaml
inputs:
  acl_number: "acl编号，示例3000"
  interface_name: "接口名称，示例GE0/0/1"
```

**selector 字段**
当前版本留空（后续确认用途后填写）：

```yaml
selector:
```

**extraction_schema 与 [custom] 前缀规则**

| 情况 | 是否加 [custom] | 说明 |
|------|----------------|------|
| CLI 输出中真实存在的列名 | 不加 | 直接从 CLI 表格中复制列名 |
| 需要从输出中推理/聚合/语义判断的字段 | 加 [custom] | AI 需理解后归纳 |

判断步骤：
1. 打开 CLI 命令的输出格式，找该字段名的原始列 → 找到 = 无 [custom]
2. 需要从多行/多列推断或语义理解 → 加 [custom] 前缀

示例对比：

```yaml
# 原生列名，不加[custom]
- name: learned_from
  description: "Learned-From"
  type: string

# 推理/聚合字段，加[custom]
- name: stp_blocking_detected
  description: "[custom] 是否发现STP端口处于Discarding状态"
  type: string
```

**transitions.rules 的 condition 字段**

- **非空表达式**：可引用以下变量
  - `extracted.<field_name>`：当前 step 提取的字段
    - 示例：`extracted.interface_status == 'Down'`
    - 示例：`extracted.packet_loss_rate > 0`
  - `state.<step_id_完整名称>.<field_name>`：其他 step 已提取的字段
    - 示例：`state.step_22_check_icmp_statistics_switcha.bad_checksum_in > 0`
    - 示例：`state.step_3_check_vlan.vlan_id == '100'`

- **空字符串 `""`**：该条件无法表达为 Python 表达式，执行引擎根据 description 语义判断
  - 通常作为 rules 列表的最后一条（"否则"分支）

**on_error 标准模板（每个 step 必须包含）**

```yaml
on_error:
  handler_execution_failed: CONCLUSION_MANUAL_CHECK
  cli_command_execution_failed: CONCLUSION_MANUAL_CHECK
  parse_failure: CONCLUSION_MANUAL_CHECK
```

**next_node 引用规则**
- 所有 next_node 的值必须在 workflow.yaml 的 steps 列表或 conclusions 字典中存在
- 如果目标 step 尚未提取（来自后续切片文档），可先写占位符 `__NEED_FILL__`，但最终验证前必须填写完整

### 2.4 更新 workflow.yaml

每提取完一个切片文档的所有 step 后，立即更新 workflow.yaml：

**a. 追加 start_node**（本文档的第一个 step）

```yaml
start_node:
  - step_0_check_physical_link    # 已有
  - step_5_check_vlan_config      # 新增
```

**b. 追加 steps 列表**

```yaml
steps:
  - step_id: step_0_check_physical_link
  - step_id: step_1_check_interface_status
  - step_id: step_5_check_vlan_config      # 新增
  - step_id: step_6_check_vlan_membership  # 新增
```

**c. 追加新 conclusions**（如本文档引入了新的结论）

```yaml
conclusions:
  CONCLUSION_MANUAL_CHECK:
    level: error
    message: "无法自动判断，需人工介入"
    suggestion: "请联系网络管理员"
  CONCLUSION_VLAN_CONFIG_ERROR:            # 新增
    level: error
    message: "VLAN配置错误"
    suggestion: "检查接口VLAN归属及trunk放行配置"
```

### 2.5 【强制】暂停等待用户确认

完成当前切片文档的所有 step 提取并更新 workflow.yaml 后，**必须**调用 ask_user，展示以下信息后等待确认：

    展示内容：
    1. 本次切片文档名：xxx.md
    2. 本次新增 step 列表（step_id + name）
    3. 本次新增 conclusions（如有）
    4. 本次更新的 start_node（如有）
    5. 提问：是否需要修改？确认后才继续下一个文档

**禁止在用户确认前开始下一个切片文档的提取。**

---

## 3. 特殊场景处理

### 3.1 无 CLI 命令的纯文本判断步骤

当某个 step 纯粹描述人工判断逻辑（无命令），skills 为空列表：

```yaml
skills: []
```

transitions 的 condition 通常全部为 `""` （依赖人工语义判断）。

### 3.2 多 skill 步骤（同一步骤执行多条命令）

一个 step 可以包含多个 skill：

```yaml
skills:
  - skill_id: "display interface brief"
    inputs: {}
    selector:
    extraction_schema:
      - name: interface_status
        description: "PHY"
        type: string
  - skill_id: "display ip interface brief"
    inputs: {}
    selector:
    extraction_schema:
      - name: ip_status
        description: "[custom] IP接口是否UP"
        type: string
```

### 3.3 配置类步骤（type: configuration）

步骤目的是修改设备配置时，type 设为 configuration：

```yaml
type: configuration
skills:
  - skill_id: "interface GigabitEthernet0/0/1"
    inputs:
      interface_name: "需要恢复的接口名称"
    selector:
    extraction_schema:
      - name: config_result
        description: "[custom] 配置是否执行成功"
        type: string
```

### 3.4 一个子章节内容过多时的自然切分

如果一个子章节描述了多个独立动作（如：先检查A，再检查B，再配置C），可按动作边界拆分为多个 step：
- 切分依据：每个 step 对应一个独立的 CLI 命令集合或一个独立的判断维度
- step_id 编号连续递增
- 切分后每个 step 的 content 字段清晰描述该 step 的单一职责

### 3.5 跨步骤状态引用

当 transitions.condition 需要引用前面 step 的提取结果时：

```yaml
condition: "state.step_22_check_icmp_statistics_switcha.bad_checksum_in > 0"
```

- step_id 使用**完整名称**（含序号，如 `step_22_check_icmp_statistics_switcha`）
- field_name 对应该 step 的 extraction_schema 中的 name 字段

---

## 4. 最终验证阶段

所有切片文档提取完毕且用户全部确认后，执行最终验证。

### 4.1 验证脚本

在输出目录下运行以下 Python 脚本：

    import yaml, os

    output_dir = "<输出文件夹路径>"

    with open(os.path.join(output_dir, 'workflow.yaml')) as f:
        workflow = yaml.safe_load(f)

    valid_nodes = set()
    for step in workflow.get('steps', []):
        valid_nodes.add(step['step_id'])
    for cid in workflow.get('conclusions', {}).keys():
        valid_nodes.add(cid)

    errors = []
    warnings = []

    for step_entry in workflow.get('steps', []):
        step_id = step_entry['step_id']
        step_file = os.path.join(output_dir, 'steps', f"{step_id}.yaml")
        if not os.path.exists(step_file):
            errors.append(f"[文件缺失] {step_file}")
            continue
        with open(step_file) as f:
            step_data = yaml.safe_load(f)

        # 检查 next_node 引用
        for rule in step_data.get('transitions', {}).get('rules', []):
            nn = rule.get('next_node', '')
            if nn and nn != '__NEED_FILL__' and nn not in valid_nodes:
                errors.append(f"[无效引用] {step_id}.rules.next_node: '{nn}'")
            if nn == '__NEED_FILL__':
                warnings.append(f"[待回填] {step_id} next_node 存在 __NEED_FILL__，最终交付前需替换为真实 step_id")

        default = step_data.get('transitions', {}).get('default', '')
        if default and default not in valid_nodes:
            errors.append(f"[无效引用] {step_id}.default: '{default}'")

        on_error = step_data.get('transitions', {}).get('on_error', {})
        for handler, target in on_error.items():
            if target and target not in valid_nodes:
                errors.append(f"[无效引用] {step_id}.on_error.{handler}: '{target}'")

        # 检查 skill_id 格式
        for skill in step_data.get('skills', []):
            sid = skill.get('skill_id', '')
            if '_' in sid:
                warnings.append(f"[疑似错误] {step_id} skill_id '{sid}' 含下划线，请确认是否应为空格")

    # 检查 start_node 是否在 steps 中
    for sn in workflow.get('start_node', []):
        if sn not in valid_nodes:
            errors.append(f"[无效入口] start_node '{sn}' 不在 steps 列表中")

    if errors:
        print("=== ERRORS ===")
        for e in errors:
            print(f"  {e}")
    if warnings:
        print("=== WARNINGS ===")
        for w in warnings:
            print(f"  {w}")
    if not errors and not warnings:
        print("验证通过！所有引用有效，无格式问题。")

### 4.2 人工复核清单

验证脚本通过后，人工确认以下项：

    [ ] 所有 start_node 覆盖了所有诊断入口（每个切片文档至少一个）
    [ ] 所有 step 的 content 描述清晰，不含占位符
    [ ] [custom] 前缀使用正确（推理字段有，原生列名无）
    [ ] 所有 skill_id 为原始 CLI 命令格式（含空格/连字符）
    [ ] 所有 transitions.rules 顺序合理（特殊条件在前，兜底在后）
    [ ] on_error 三项在每个 step 中均已填写
    [ ] default 每个 step 均已填写
    [ ] conclusions 中的 level / message / suggestion 均已完善
    [ ] 所有 next_node 中的 __NEED_FILL__ 已全部回填为真实 step_id（验证脚本 WARNING 为零）
    [ ] __NEED_FILL__ 未出现在 next_node 以外的任何字段

---

## 5. 常见错误与避坑记录

来源：ping不通项目真实踩坑

### 5.1 skill_id 下划线错误（高频）

**现象**：skill_id 写成 `"display_logbuffer"`、`"display_stp_brief"` 等，把命令中的空格替换成了下划线。
**原因**：Python 变量名习惯被代入 YAML 字段值。
**解法**：skill_id 是原始命令字符串，保留空格。一旦发现 `_` 出现在常见 CLI 命令中，立即核查。

### 5.2 [custom] 前缀漏加

**现象**：字段名是自行定义的语义字段（如 `stp_state`、`log_has_error`），但 description 里没有 [custom] 前缀。
**原因**：提取时未仔细判断该字段是否为 CLI 原生列名。
**解法**：每个 extraction_schema 字段，先找 CLI 输出里有没有这一列；没有则必须加 [custom]。

### 5.3 __NEED_FILL__ 占位符（合法前向引用）

**规则**：`__NEED_FILL__` **仅允许出现在 `next_node` 字段**，其他字段（如 content、description）中禁止使用。

**合法场景**：某切片文档的最后一步存在两个分支：
- 一个分支结论已知 → 直接写 `CONCLUSION_XXX`
- 另一个分支需要继续诊断 → 目标 step 在后续切片文档中，此时写 `__NEED_FILL__` 占位

**处理时机**：不要在提取中间阶段急于替换——等所有切片文档全部提取完成后，在最终验证阶段统一回填所有 `__NEED_FILL__`。

**错误用法**：在 `content`、`description`、`skill_id` 等字段中写 `__NEED_FILL__` 是错误的，必须在提取时填写完整。

**常见失误**：提取完所有切片后忘记回填 `__NEED_FILL__`，导致 workflow 出现悬空引用。验证脚本会以 WARNING 形式报出所有残留的 `__NEED_FILL__`，最终交付前必须全部消除。

### 5.4 文件名与 step_id 不一致

**现象**：step 文件名为 `step_6_check_loop.yaml`，但文件内 step_id 字段写的是 `step_6_check_loop_isolation`。
**原因**：命名时手误或前后不一致。
**解法**：写文件时保持文件名（去掉 .yaml）与内部 step_id 完全一致；写完立即核对。

### 5.5 next_node 引用了不存在的节点

**现象**：transitions 中 next_node 指向了一个笔误的 step_id（如多了或少了一个单词）。
**原因**：step_id 较长时手动输入容易出错。
**解法**：transitions 里引用其他 step 时，直接从 workflow.yaml 的 steps 列表复制粘贴 step_id，不手打。

### 5.6 实际文件名与预期不符

**现象**：以为文件是 `ping不通_1.md`，实际是 `ping_1.md` 或文件名有额外空格。
**原因**：根据语境猜文件名。
**解法**：执行 `ls` 之后看实际文件名再引用，禁止一切形式的路径猜测。

---

## 附录：YAML 字段速查

### skill 字段结构

    skill_id: "原始CLI命令 含空格保留"   # 必填
    inputs:                               # 无参数写 {}
      param_name: "参数说明，示例值"
    selector:                             # 暂留空
    extraction_schema:                    # 提取字段列表
      - name: field_name
        description: "[custom] 说明"     # 推理字段加[custom]，原生列名不加
        type: string | integer | list | boolean

### extraction_schema type 取值

- `string`：字符串（状态、名称、地址、版本号）
- `integer`：整数（计数器、包数、长度）
- `list`：多条记录的列表
- `boolean`：true/false 判断结果

### transitions 完整结构

    transitions:
      rules:
        - description: "条件语义说明"
          condition: "extracted.xxx == 'yyy'"   # 或留空 ""
          next_node: step_N_xxx                  # 或 CONCLUSION_XXX
        - description: "其余情况（兜底）"
          condition: ""
          next_node: step_M_xxx
      on_error:
        handler_execution_failed: CONCLUSION_MANUAL_CHECK
        cli_command_execution_failed: CONCLUSION_MANUAL_CHECK
        parse_failure: CONCLUSION_MANUAL_CHECK
      default: CONCLUSION_MANUAL_CHECK

### condition 可引用变量

- `extracted.<field_name>`：当前 step 的提取字段
- `state.<step_id_完整名>.<field_name>`：其他 step 的提取字段
  - 示例：`state.step_22_check_icmp_statistics_switcha.bad_checksum_in > 0`