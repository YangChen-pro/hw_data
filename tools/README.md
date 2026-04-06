# 工具说明

这个目录放的是 YAML 评估器和它的运行入口。

## 怎么运行

最简单的方式是直接执行示例脚本：

```bash
bash tools/run_example.sh
```

如果你想把结果输出到自定义目录，也可以继续传参数：

```bash
bash tools/run_example.sh \
  --output-dir reports/yaml_evaluation/ping_unreachable/manual_run
```

如果你想生成 workflow 的单页 HTML 流程图页面：

```bash
bash tools/run_viewer_example.sh
```

脚本默认会使用 `conda` 环境 `claw`，然后评估：

- `workflows/ping_unreachable/workflow.yaml`
- `workflows/ping_unreachable/steps/*.yaml`

## 输出是什么

运行后会生成一个新的报告目录，默认形如：

```text
reports/yaml_evaluation/ping_unreachable/<时间戳>/
```

目录里有 4 个文件：

- `report.md`：给人看的总结报告
- `report.json`：给程序处理的结构化结果
- `issues.csv`：按行展开的问题清单，方便筛选
- `manifest.json`：本次生成了哪些文件

报告中的 `workflow_path` 和 `steps_dir` 默认使用仓库相对路径，例如：

- `workflows/ping_unreachable/workflow.yaml`
- `workflows/ping_unreachable/steps`

HTML 查看器默认输出到：

```text
reports/workflow_viewer/ping_unreachable/<时间戳>/index.html
```

它会把 workflow 里的跳转关系渲染成一张可点击、可聚焦的单页流程图。节点和边都可以点开看详情，若仓库里已有最近一次评估报告，还会自动给节点附加问题徽标。

当前 viewer 只保留最少必要的交互：

- 默认优先聚焦当前节点及其直接相关上下游
- 提供 `全图 / 回到当前` 两个按钮，避免复杂工作台感
- 鼠标滚轮默认平移画布，`Ctrl/Cmd + 滚轮` 才缩放
- 拖拽空白区域可以平移画布，双击不会触发缩放
- 节点在图中只保留标题、阶段和少量状态徽标，详细说明放到右侧
- 节点问题状态和边的跳转语义分开表达
- 选中节点或边后，右侧直接显示对应详情
- 边标签优先显示在当前相关路径上，非重点边会降噪，避免局部重叠
- 图谱是主视觉，右侧详情只负责解释当前焦点

如果你需要验证“跳转目标字段兼容性”，可以直接运行：

```bash
node tools/workflow_viewer/route_target_compat.test.mjs
```

如果你需要验证“报告总数 / 问题明细兼容性”，可以直接运行：

```bash
conda run -n claw python -X utf8 tools/workflow_viewer/issue_summary_compat.test.py
```

## 报告怎么看

先看 `report.md`，通常按这个顺序读：

1. `总览`
   - 先看问题总数、严重问题数
2. `共性问题`
   - 看是不是大面积存在空 `condition`、占位输入、旧式引用
3. `按文件汇总`
   - 先定位问题最多的文件
4. `详细问题`
   - 按文件逐条修复

如果你要批量处理，优先看 `issues.csv` 或 `report.json`。

## 适合新手的最短路径

1. 执行 `bash tools/run_example.sh`
2. 打开最新生成的 `report.md`
3. 先修 `critical`，再修 `warning`
4. 修完后重新运行脚本验证结果是否减少

## HTML 查看器的最短路径

1. 执行 `bash tools/run_viewer_example.sh`
2. 打开 `reports/workflow_viewer/ping_unreachable/<时间戳>/index.html`
3. 在图上点击节点或边
4. 用顶部按钮切换视图、缩放或回到当前节点
5. 在右侧详情面板看节点内容、技能、转移规则、跳转条件、分组摘要和问题徽标
