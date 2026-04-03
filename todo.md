# TODO：评估已有 YAML

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
