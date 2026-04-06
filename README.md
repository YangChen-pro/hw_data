# YAML 工作流评估工作区

## 仓库用途

这个仓库用于存放从网络故障处理资料中抽取出来的结构化工作流。

当前样例是 `ping_unreachable` 工作流：

- 原始资料放在 `docs/source_materials/`
- 结构化 YAML 产物放在 `workflows/`

当前工作的重点是评估和改进 YAML 工作流的质量，而不是从头重写故障处理知识。

## 目录结构

```text
.
├── README.md
├── todo.md
├── docs/
│   ├── yaml_evaluation_guide.md
│   └── source_materials/
│       └── ping_unreachable/
│           ├── ping_unreachable_steps.pdf
│           └── notes/
├── workflows/
│   └── ping_unreachable/
│       ├── workflow.yaml
│       └── steps/
└── .helloagents/
```

## 关键文件

- `workflows/ping_unreachable/workflow.yaml`
  - 工作流入口、步骤列表和结论定义
- `workflows/ping_unreachable/steps/*.yaml`
  - 每个步骤的 skill、抽取字段和流转规则
- `docs/yaml_evaluation_guide.md`
  - 评估已有 YAML 的规则说明
- `todo.md`
  - 你当前要完成的任务说明

## 核心概念

- `workflow.yaml`
  - 定义完整的故障排查流程图
- `step`
  - 定义一个检查、配置或诊断动作
- `conclusion`
  - 定义某条分支收敛后的最终结论
- `transition`
  - 定义步骤如何流转到下一个步骤或结论

## 新人接手顺序

1. 先阅读 `README.md`
2. 打开 `workflows/ping_unreachable/workflow.yaml`
3. 阅读 `docs/yaml_evaluation_guide.md`
4. 按 `todo.md` 中的说明完成当前任务

## 评估工具

当前已经提供一个可直接运行的 YAML 评估脚本：

- `tools/yaml_workflow_evaluator.py`
- 运行方式：`conda run -n claw python tools/yaml_workflow_evaluator.py`
- 默认输出：`reports/yaml_evaluation/ping_unreachable/<时间戳>/`
- 新手说明：[`tools/README.md`](/Users/yangchen/Desktop/hw_data/tools/README.md)
- 报告说明：[`reports/README.md`](/Users/yangchen/Desktop/hw_data/reports/README.md)

另外还有一个 workflow HTML 查看器：

- `tools/workflow_html_viewer.py`
- 运行方式：`bash tools/run_viewer_example.sh`
- 默认输出：`reports/workflow_viewer/ping_unreachable/<时间戳>/index.html`
- 页面形态：单页、图为中心的 workflow 查看器
- 交互重点：点击节点或边查看详情；默认自动聚焦当前内容
- 画布操作：鼠标滚轮默认平移，`Ctrl/Cmd + 滚轮` 缩放，拖拽空白区域平移
- 展示重点：图中的节点只保留标题、阶段和少量状态徽标，详细说明放在右侧
- 边标签会优先在当前相关路径上显示，非重点边降噪，避免局部重叠
- 语义重点：节点问题状态和边的跳转语义分开表达，避免把 `严重 / 警告 / 正常` 与 `rule / default / on_error` 混在一起
- 顶部摘要：起点列表默认折叠，只显示起点数量

输出目录内包含：

- `report.md`：人工阅读版结果
- `report.json`：结构化结果
- `issues.csv`：扁平问题清单
- `manifest.json`：本次生成的文件清单

如果你先看 workflow 结构，再看评估结果，建议顺序是：

1. 先打开 workflow HTML 查看器，理解流程跳转和分组范围
2. 再运行评估器生成 `report.md`
3. 最后按 `todo.md` 的检查项修正 YAML

## 工作约定

- 文件名和目录名统一使用英文
- 保持 `step_id` 与工作流节点引用一致
- 如果要重命名 step 文件或节点 id，必须同步更新所有相关引用
- `.helloagents/` 视为项目元数据，不是主要工作区
