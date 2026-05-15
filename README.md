# YAML 工作流评估工作区

## 仓库用途

这个仓库用于存放从网络故障处理资料中抽取出来的结构化工作流。

当前已经包含四类结构化 workflow，以及一组尚未完全结构化的原始资料：

- `ping_unreachable`
  - 已由 `HWDA.zip` 中的 `ping` 内容替换，是评估工具默认输入
- `ap_offline`
  - 已有完整结构化 YAML，可直接通过 CLI 参数传给评估器和 HTML viewer
- `vlan`
  - 来自 `HWDA.zip`，包含 VLAN 故障诊断 workflow、步骤 YAML 与原始切片资料
- `wireless`
  - 来自 `HWDA.zip`，包含无线认证故障诊断 workflow、步骤 YAML 与原始切片资料
- `ap_online`
  - 当前只有 `docs/source_materials/ap_online/` 下的 PDF 和分步笔记，尚未补齐 `workflows/ap_online/`

当前工作的重点是持续整理故障处理知识、基于 `extraction_guided.md` 抽象可量化质量指标，评估已有 YAML workflow 质量，并逐步把原始资料补全为结构化产物。

## 目录结构

```text
.
├── README.md
├── todo.md
├── design.md
├── extraction_guided.md
├── docs/
│   ├── yaml_evaluation_guide.md
│   └── source_materials/
│       ├── ap_online/
│       │   ├── ap_online_steps.pdf
│       │   └── notes/
│       └── ping_unreachable/
│           ├── ping_unreachable_steps.pdf
│           └── notes/
├── workflows/
│   ├── ap_offline/
│   │   ├── workflow.yaml
│   │   └── steps/
│   ├── vlan/
│   │   ├── workflow.yaml
│   │   ├── steps/
│   │   └── vlan_org/
│   ├── wireless/
│   │   ├── workflow.yaml
│   │   ├── steps/
│   │   └── wireless_org/
│   └── ping_unreachable/
│       ├── workflow.yaml
│       ├── steps/
│       ├── ping_org/
│       └── ping_unreachable_steps.pdf
├── reports/
│   ├── yaml_evaluation/
│   └── workflow_viewer/
├── tools/
└── .helloagents/
```

## 关键文件

- `workflows/ping_unreachable/workflow.yaml`
  - Ping 不通故障定位的主 workflow，当前评估器和 viewer 的默认输入，已替换为 `HWDA.zip` 中的 `ping`
- `workflows/ping_unreachable/steps/*.yaml`
  - Ping 不通 workflow 的步骤定义
- `workflows/vlan/workflow.yaml`、`workflows/vlan/steps/*.yaml`
  - VLAN 故障诊断 workflow 与步骤定义
- `workflows/wireless/workflow.yaml`、`workflows/wireless/steps/*.yaml`
  - 无线认证故障诊断 workflow 与步骤定义
- `extraction_guided.md`
  - Markdown → YAML 抽取操作手册，后续质量评分指标应以该手册的自检项和转换规则为主要依据
- `workflows/ap_offline/workflow.yaml`
  - AP 下线故障诊断的主 workflow，覆盖黑名单、静态 IP、License、心跳超时和设备内部异常等路径
- `workflows/ap_offline/steps/*.yaml`
  - AP 下线 workflow 的步骤定义
- `docs/source_materials/ap_online/`
  - AP 上线问题的原始资料，目前包含 PDF 和 6 份分步笔记，尚未映射到结构化 workflow
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
2. 看 `workflows/` 和 `docs/source_materials/` 下当前有哪些主题已经结构化、哪些还只是原始资料
3. 阅读 `docs/yaml_evaluation_guide.md`
4. 如果要跑现成工具样例，先打开 `workflows/ping_unreachable/workflow.yaml`
5. 按 `todo.md` 中的说明完成当前任务

## 评估工具

当前已经提供一个可直接运行的 YAML 评估脚本：

- `tools/yaml_workflow_evaluator.py`
- 运行方式：`conda run -n claw python tools/yaml_workflow_evaluator.py`
- 默认输出：`reports/yaml_evaluation/ping_unreachable/<时间戳>/`
- 默认输入：`workflows/ping_unreachable/workflow.yaml` 和 `workflows/ping_unreachable/steps/`
- 自定义输入：可通过 `--workflow` 和 `--steps-dir` 切换到其他主题，例如 `ap_offline`
- 新手说明：[`tools/README.md`](/Users/yangchen/Desktop/hw_data/tools/README.md)
- 报告说明：[`reports/README.md`](/Users/yangchen/Desktop/hw_data/reports/README.md)

另外还有一个 workflow HTML 查看器：

- `tools/workflow_html_viewer.py`
- 运行方式：`bash tools/run_viewer_example.sh`
- 默认输出：`reports/workflow_viewer/ping_unreachable/<时间戳>/index.html`
- 默认输入：`workflows/ping_unreachable/workflow.yaml` 和 `workflows/ping_unreachable/steps/`
- 自定义输入：同样支持 `--workflow`、`--steps-dir`，输出目录会自动按 workflow 名称分 namespace
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

如果要按 `extraction_guided.md` 的抽取规则生成质量评分和中文图表：

- `tools/yaml_quality_score.py`
- 运行方式：`bash tools/run_quality_score_example.sh`
- 默认输出：`reports/yaml_quality_scores/<时间戳>/`
- 默认输入：扫描 `workflows/*/workflow.yaml`
- 输出内容：
  - `scores.csv`：各 workflow 总分和分维度得分
  - `scores.json`：结构化评分详情和扣分项
  - `report.md`：人工阅读版评分报告
  - `overall_score_bar.png`：质量总分柱状图
  - `dimension_score_heatmap.png`：分维度热力图
  - `dimension_radar.png`：分维度雷达图

如果你先看 workflow 结构，再看评估结果，建议顺序是：

1. 先打开 workflow HTML 查看器，理解流程跳转和分组范围
2. 再运行评估器生成 `report.md`
3. 最后按 `todo.md` 的检查项修正 YAML
4. 如果主题还没有结构化 workflow（如当前的 `ap_online`），先整理 `docs/source_materials/<topic>/` 再新增 `workflows/<topic>/`

## 工作约定

- 文件名和目录名统一使用英文
- 保持 `step_id` 与工作流节点引用一致
- 如果要重命名 step 文件或节点 id，必须同步更新所有相关引用
- `.helloagents/` 视为项目元数据，不是主要工作区
