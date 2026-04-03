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

## 工作约定

- 文件名和目录名统一使用英文
- 保持 `step_id` 与工作流节点引用一致
- 如果要重命名 step 文件或节点 id，必须同步更新所有相关引用
- `.helloagents/` 视为项目元数据，不是主要工作区
