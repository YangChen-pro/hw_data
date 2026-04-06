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
- [ ] 下一步：根据最新评估结果继续修正 YAML 内容

## 目标

评估 `workflows/ping_unreachable/` 下现有 YAML 工作流的结构质量，在继续抽取或清理之前先识别出明显问题。

## 评估文件

- `workflows/ping_unreachable/workflow.yaml`
- `workflows/ping_unreachable/steps/*.yaml`

## 检查项

1. 每个 `next_node` 都指向合法的 step 或 conclusion。
2. 每个 `condition` 使用的字段和逻辑都合法。
3. 每个 `inputs` 和 `selector` 都能被解析。
4. 每个 `extraction_schema` 都与预期 skill 输出匹配。

## 交付结果

- 一份按文件整理的问题清单
- 一份重复性规则问题的简短总结
- 一份需要产品或工程确认的边界问题列表

## 完成标准

- 所有 step YAML 都已检查
- 所有无效引用都已列出
- “明确缺陷”和“规则未定”已分开记录
