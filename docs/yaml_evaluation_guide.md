# YAML 评估说明

## 评估范围

本次评估只看以下结构化产物：

- `workflows/ping_unreachable/workflow.yaml`
- `workflows/ping_unreachable/steps/*.yaml`

重点关注结构正确性和规则一致性。

## 评估清单

### 1. `next_node` 合法性

检查每条 `transitions.rules[*].next_node`。

- 如果指向 step：
  - 对应 step 文件必须存在
  - 对应 step id 必须出现在 `workflow.yaml` 中
- 如果指向 conclusion：
  - 对应 conclusion 必须在 `workflow.yaml` 中声明
- 像 `__NEED_FILL__` 这样的占位值属于无效值

### 2. `condition` 合法性

检查每条 condition 是否写得清楚、可解释。

- 允许的来源：
  - `input.facts.xxx`
  - `state.results.step_xxx.yyy`
  - `extracted.xxx`
- 被引用字段必须真实存在
- 运算符应限制在常见比较和布尔逻辑范围内
- 只有当分支本身依赖人工判断或尚无法规则化时，才允许空 condition

### 3. `inputs` 和 `selector` 是否可解析

检查每个 skill 调用是否能被解析。

- 引用型输入必须来自用户输入或前序步骤结果
- 常量值允许直接写在 YAML 中
- `selector` 使用的字段必须能映射到 skill 输出字段，或有明确说明
- 无法解析来源的动态输入需要单独记录

### 4. `extraction_schema` 是否匹配

检查声明的抽取字段是否合理。

- 抽取字段应存在于 skill 输出中，或能通过明确规则稳定推导
- 推导字段应在 `description` 中写明依据
- 对纯配置或纯操作步骤，`extraction_schema: []` 是可接受的

## 建议输出格式

建议用紧凑表格或清单输出：

```text
file | issue | severity | recommendation
```

示例：

```text
step_20_check_cpu_defend_blacklist.yaml | next_node 使用 __NEED_FILL__ | high | 替换为合法的 step 或 conclusion
```

## 当前已知问题

- `workflows/ping_unreachable/steps/step_20_check_cpu_defend_blacklist.yaml`
  - 含有 `next_node: __NEED_FILL__`
- `workflows/ping_unreachable/steps/step_21_check_blacklist_acl.yaml`
  - 含有 `next_node: __NEED_FILL__`

这两个文件可以直接作为当前评估中的已知失败样例。
