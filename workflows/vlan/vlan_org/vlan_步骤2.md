### 1.1.2 LNP 协商结果错误

### 现象描述

LNP 协商失败。

### 可能原因

- • 链路故障。
• 接口状态Down 。
• link-type 配置有误。
• LNP 配置有误。
• OPS 机制未 ready。
### 操作步骤

图1故障诊断流程

---

![Figure](figures/vlan_page_005_figure_000.png)

1. 检查当前设备与其他设备连接的接口状态是否是Up 。

在任意视图下执行 display interface interface-type interface-number 命令查看需要互通的接口的运行状态。

- • 如果接口的状态为 Down, 请先根据 故障处理: 以太网接口物理 DOWN 排除接口 Down 的故障。
• 如果成员口的状态是 Up, 请执行步骤 2。
2. 检查接口下的link-type配置是否正确。

在任意视图下执行 display current–configuration interface interface–type interface–number命令查

看接口下的配置。

- ·若 port link-type 不是 negotiation-desirable 或者 negotiation-auto,需要修改为其中的一种。
若 port link-type 为 negotiation-desirable 或者 negotiation-auto,请执行步骤 3。
3. 检查Inp的配置是否正确。

在设备上执行 display Inp summary 命令检查全局和接口下配置是否正确。

- · 设备全局需要配置 Inp enable 命令, 接口下需要配置 undo port negotiation disable 命令。
· 若 LNP 配置无问题, 请执行步骤 4。
4. 检查OPS机制是否正常。

在任意视图下执行display ops assistant verbose default 查看 OPS 脚本的状态是否正确。

- · 若无名为_lnp_port_linktype_change.py 的脚本,或脚本的 State 状态不为 ready,请执行步骤 6。
---

- · 若名为_lnp_port_linktype_change.py 的脚本存在且 State 状态为 ready, 请执行步骤 6。
. 请收集如下信息,并联系技术支持人员。
. 上述步骤的执行结果。
. 设备的配置文件、日志信息、告警信息。
