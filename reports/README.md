# 报告目录说明

这里存放 YAML 评估器的输出结果。

## 目录结构

通常会生成这样的目录：

```text
reports/yaml_evaluation/ping_unreachable/<时间戳>/
```

每次运行都会生成一份新的结果，不会覆盖历史结果。

## 文件说明

- `report.md`
  - 给人看的主报告，先看这个
- `report.json`
  - 机器可读的结构化结果，适合后续自动处理
- `issues.csv`
  - 扁平化问题列表，适合用表格工具过滤和统计
- `manifest.json`
  - 本次输出文件清单，便于确认结果是否完整

另一个常见输出目录是：

```text
reports/workflow_viewer/ping_unreachable/<时间戳>/index.html
```

这是一份单页 HTML 流程图页面，用来缩放浏览 workflow、点击节点/边查看详情和转移规则。

当前 HTML 查看器支持：

- 默认聚焦当前节点的局部子图
- `当前子图 / 全图 / 异常路径 / 分组聚焦`
- 右下角固定 minimap
- 点击节点、边或分组查看对应详情或摘要

## 阅读顺序

1. 先看 `report.md` 的 `总览`
2. 再看 `共性问题`
3. 然后看 `按文件汇总`
4. 最后处理 `详细问题`

## 修复顺序建议

- 先修 `critical`
- 再修 `warning`
- 如果你只是想快速判断质量，先看 `问题总数` 和 `共性问题`
