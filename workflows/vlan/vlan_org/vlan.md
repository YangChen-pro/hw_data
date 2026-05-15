### 1.1.1 VLAN 内不能互通

### 现象描述

VLAN 内用户之间不能互通。

### 可能原因

- · 链路故障。
· 接口被人为 Shutdown 或物理接口损坏。
· 设备 MAC 地址学习错误。
· 设备上配置了二层端口隔离。
· 主机配置了错误的静态 ARP。
· 设备上配置了错误的接口和 MAC 地址绑定。
### 操作步骤

图1故障诊断流程

---

![Figure](figures/vlan_page_002_figure_000.png)

1. 检查 VLAN 内需要互通的接口是否 Up。

在任意视图下执行 display interface interface-type interface-number 命令查看需要互通的接口的运行状态。

- · 如果成员口的状态是Up,请执行步骤2。
2. 检查需要互通的终端 IP 地址是否在同一网段,如果不是请修改为同一网段,如果故障仍然存在请执行步骤 3。

3. 检查设备上 MAC 地址表项是否正确。

在设备上执行display mac-address命令检查设备学习到的MAC地址、MAC地址对应接口、所属 VLAN是否正确,如果不正确请在接口上执行undo mac-address mac-address vlan vlan-id命令使设备重新学习指定的MAC地址。执行完上述操作后,再检查设备学习到的MAC地址、MAC地址对应接口、 所属VLAN是否正确:

- • 如果不正确请执行步骤 4。
• 如果正确但用户仍无法互相访问请执行步骤 5。
4. 检查 VLAN 相关配置是否正确。

请执行如下操作检查 VLAN 相关配置是否正确。

---

<table><tr><td>检查项</td><td>检查方法及处理建议</td></tr><tr><td>需要互通的接口所在的 VLAN 是否已经创建</td><td>在任意视图下,执行 display vlan vlan-id 查看需要互通的接口所在的 VLAN 是否已经创建,如果未创建请在系统视图下执行 vlan 命令创建 VLAN。</td></tr><tr><td>检查需要互通的接口是 否加入 VLAN</td><td>执行 display vlan vlan-id 检查需要互通的接口是否已经加入指定 VLAN,如果未加入请将 接口加入指定 VLAN。</td></tr><tr><td></td><td>说明:</td></tr><tr><td></td><td>如果需要互通的接口不在同一个设备上,还需要考虑设备互联的接口允许指定的 VLAN 通过。</td></tr><tr><td></td><td>Access 类型接口加入 VLAN。根据需要可以选择如下方式将 Access 类型接口加入 VLAN。</td></tr><tr><td></td><td>说明:</td></tr><tr><td></td><td>块省情况下,设备的接口类型为 Access。在选择以 Access 方式将接口加入 VLAN时,如果接 口类型不是 Access,需要先使用 port link-type access 命令将接口类型修改为 Access 类 型。</td></tr><tr><td></td><td>在接口视图下执行命令 port default vlan 将 Access 类型的接口加入 VLAN。</td></tr><tr><td></td><td>在 VLAN 视图下执行命令 port 将 Access 类型的接口加入 VLAN。</td></tr><tr><td></td><td>Trunk 类型接口加入 VLAN。</td></tr><tr><td></td><td>说明:</td></tr><tr><td></td><td>执省情况下,设备的接口类型为 Access。在选择以 Trunk 方式将接口加入 VLAN时,如果接</td></tr><tr><td></td><td>负责型不是 Trunk,需要先使用 port link-type trunk 命令将接口类型修改为 Trunk 类型。</td></tr><tr><td></td><td>在接口视图下执行命令 port trunk allow-pass vlan 将 Trunk 类型的接口加入 VLAN。</td></tr><tr><td></td><td>Hybrid 类型接口加入 VLAN。根据需要可以选择如下方式将 Hybrid 类型接口加入 VLAN。</td></tr><tr><td></td><td>说明:</td></tr><tr><td></td><td>执省情况下,设备的接口类型为 Access。在选择以 Hybrid 方式将接口加入 VLAN时,如果接</td></tr><tr><td></td><td>口类型不是 Hybrid,需要先使用 port link-type hybrid 命令将接口类型修改为 Hybrid 类型。</td></tr><tr><td></td><td>在接口视图下执行命令 port hybrid tagged vlan 将 Hybrid 接口以 Tagged 方式加入 VLAN。</td></tr><tr><td></td><td>在接口视图下执行命令 port hybrid untagged vlan 将 Hybrid 接口以 Untagged 方式加入 VLAN。</td></tr><tr><td></td><td>接口和终端是否按照规 划的对应关系将终端与设备接口进行连接。</td></tr></table>


执行完上述操作后:

- • MAC 地址表项正确,但故障仍然存在,请执行步骤 5。
• MAC 地址表项不正确,请执行步骤 7。
---

5. 检查设备上是否配置了二层端口隔离。

在系统视图下执行Interface interface-type interface-number 进入故障接口视图,然后执行display this命令查看接口是否配置了二层端口隔离:

- • 如果未配置二层端口隔离请执行步骤 6。
• 如果配置了二层端口隔离,请使用 undo port–isolate enable 命令取消接口上二层端口隔离配置。
取消二层端口隔离后如果故障依然存在请执行步骤 6。
6. 检查终端设备上是否配置了错误的静态 ARP 表项,如果终端设备上配置了错误的静态 ARP 表项请修正, 完成后如果故障仍然存在请执行步骤 7。

7. 请收集如下信息,并联系技术支持人员。

- • 上述步骤的执行结果。
• 设备的配置文件、日志信息、告警信息。
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
