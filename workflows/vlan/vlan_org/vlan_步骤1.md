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

<table><tr><td>检查项</td><td>检查方法及处理建议</td></tr><tr><td>需要互通的接口所在的 VLAN 是否已经创建</td><td>在任意视图下,执行 display vlan vlan-id 查看需要互通的接口所在的 VLAN 是否已经创建,如果未创建请在系统视图下执行 vlan 命令创建 VLAN。</td></tr><tr><td>检查需要互通的接口是 否加入 VLAN</td><td>执行 display vlan vlan-id 检查需要互通的接口是否已经加入指定 VLAN,如果未加入请将 接口加入指定 VLAN。说明:如果需要互通的接口不在同一个设备上,还需要考虑设备互联的接口允许指定的 VLAN 通过。Access 类型接口加入 VLAN。根据需要可以选择如下方式将 Access 类型接口加入 VLAN。说明:缺省情况下,设备的接口类型为 Access。在选择以 Access 方式将接口加入 VLAN时,如果接 口类型不是 Access,需要先使用 port link-type access 命令将接口类型修改为 Access 类 型。在接口视图下执行命令 port default vlan 将 Access 类型的接口加入 VLAN。在 VLAN 视图下执行命令 port 将 Access 类型的接口加入 VLAN。Trunk 类型接口加入 VLAN。说明:缺省情况下,设备的接口类型为 Access。在选择以 Trunk 方式将接口加入 VLAN时,如果接负责型不是 Trunk,需要先使用 port link-type trunk 命令将接口类型修改为 Trunk 类型。在接口视图下执行命令 port trunk allow-pass vlan 将 Trunk 类型的接口加入 VLAN。Hybrid 类型接口加入 VLAN。根据需要可以选择如下方式将 Hybrid 类型接口加入 VLAN。说明:缺省情况下，设备的接口类型为 Access。在选择以 Hybrid 方式将接口加入 VLAN时,如果接口类型不是 Hybrid,需要先使用 port link-type hybrid 命令将接口类型修改为 Hybrid 类型。在接口视图下执行命令 port hybrid tagged vlan 将 Hybrid 接口以 Tagged 方式加入 VLAN。在接口视图下执行命令 port hybrid untagged vlan 将 Hybrid 接口以 Untagged 方式加入 VLAN。</td></tr><tr><td></td><td>接口和终端是否按照规 划的对应关系将终端与设备接口进行连接。</td><td>按照正确的对应关系将终端与设备接口进行连接。</td></tr></table>


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
