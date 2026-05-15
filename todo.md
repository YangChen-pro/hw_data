# TODO：评估已有 YAML

## 当前实现状态

- [x] 已实现可直接运行的 YAML 评估器
- [x] 已实现 workflow 单页 HTML 查看器
- [x] HTML 查看器已重构为简单的单页 workflow 图查看器
- [x] 图中只保留 `全图 / 回到当前` 两个最小必要操作
- [x] 图谱交互已调整为滚轮平移、`Ctrl/Cmd + 滚轮` 缩放、拖拽空白平移
- [x] 图中节点已简化为标题、阶段和少量状态徽标
- [x] 节点问题态与边的跳转语义分开表达
- [x] 顶部起点列表已折叠为数量概览
- [x] 评估报告已经输出为 `report.md / report.json / issues.csv`
- [x] 已基于 `extraction_guided.md` 抽象可量化 YAML 质量指标，并用图表展示各 workflow 得分
- [ ] 下一步：按质量报告中的扣分项补齐 `user_skills`、空 `condition`，并清理旧 YAML 中残留的 `transitions.default`

## 目标

评估 `workflows/` 下现有 YAML 工作流的结构质量，在继续抽取或清理之前先识别出明显问题，并逐步把 `extraction_guided.md` 中的抽取规则转化为可量化评分。

## 评估文件

- `workflows/ping_unreachable/workflow.yaml`
- `workflows/ping_unreachable/steps/*.yaml`
- `workflows/vlan/workflow.yaml`
- `workflows/vlan/steps/*.yaml`
- `workflows/wireless/workflow.yaml`
- `workflows/wireless/steps/*.yaml`

## 检查项

1. 每个 `next_node` 都指向合法的 step 或 conclusion。
2. 每个 `condition` 使用的字段和逻辑都合法。
3. 每个 `inputs` 和 `selector` 都能被解析。
4. 每个 `extraction_schema` 都与预期 skill 输出匹配。
5. `input_schema`、`start_node`、`step` 拆分、`conclusions`、`skills` 与 `transitions` 符合 `extraction_guided.md` 的 Phase 1~4 自检规则。
6. 后续图表需要使用 Matplotlib/plt，并配置中文字体；专业术语可保留英文。

## 交付结果

- 一份按文件整理的问题清单
- 一份重复性规则问题的简短总结
- 一份需要产品或工程确认的边界问题列表
- 一份按可量化指标输出的 workflow 质量得分表
- 一张或多张中文图表，展示各 workflow 在结构完整性、字段来源、拓扑一致性、技能定义和表达式合法性上的得分

## 完成标准

- 所有 step YAML 都已检查
- 所有无效引用都已列出
- “明确缺陷”和“规则未定”已分开记录
