
### 15.2.4 检查路由是否正常

1. 检查是否有直连路由

- 如果和交换机连接的是终端设备,检查终端设备上是否配置了正确的网关地址。

- 如果和交换机连接的是交换机或路由设备,检查设备上是否有正确的回程路由。

在源端执行命令display ip routing-table ip-address检查有无到对端的路由。

如有路由则显示如下信息,回显字段中Proto为Direct表示为直连路由。由于遵循最长匹配原则,同一路由前缀,当非直连路由掩码长度大于直连路由时,将导致报文无法从直连接口转发。若检查目的IP匹配的路由为非直连路由,需排查路由故障。


```bash
<SwitchA> display ip routing-table 192.168.1.11
Route Flags: R - relay, D - download to fib
-------------------------------------------------------------------------------
Routing Table : Public
Summary Count : 1
Destination/Mask  Proto  Pre Cost  Flags NextHop  Interface
 192.168.1.0/24  Direct 0  0     D 192.168.1.10  Vlanif10
```

如果没有路由,则输入上述命令后无任何信息显示,需要检查路由协议配置是否正确。

2. 检查是否配置了策略路由

例如:SwitchB在GE1/0/2接口调用策略路由,将SwitchA上送的源IP地址为 192.168.1.10的报文重定向到下一跳192.168.2.11。

可以通过下述步骤查看策略路由配置并做相应配置的修改。

a. 执行display traffic-policy applied-record命令,查看流策略的应用记录。

```bash
<SwitchB> display traffic-policy applied-record
#
----------------------------------------------------------------------
 Policy Name:  p1
 Policy Index: 0
 Classifier.c1   Behavior:b1 //流策略p1中关联了流分类c1和流行为b1
----------------------------------------------------------------------
 *interface GigabitEthernet1/0/2
  traffic-policy p1 inbound //流策略p1应用在接口GE1/0/2的入方向
    slot 1  : success
----------------------------------------------------------------------
 Policy total applied times: 1.
#
```

b.执行display traffic behavior user-defined behavior-name命令,查看已配置的流行为信息。

```bash
<SwitchB> display traffic behavior user-defined b1
 User Defined Behavior Information:
 Behavior: bb
 Permit
 Redirect: no forced
 Redirect ip-nexthop
  192.168.2.11  //流行为b1的动作为重定向,下一跳IP为192.168.2.11
```

c.执行display traffic classifier user-defined classifier-name命令,查看策略中流分类关联的ACL编号。

```bash
<SwitchB> display traffic classifier user-defined c1
User Defined Classifier Information:
Classifier: c1
 Precedence: 15
Operator: AND
Rule(s) : if-match acl 3000 //流分类c1关联的ACL为acl 3000
```

d. 执行display acl acl-number命令,查看ACL具体内容。

```bash
<SwitchB> display acl 3000
Advanced ACL 3000, 1 rule
Acl's step is 5
 rule 5 permit ip source 192.168.1.10 0  //acl 3000中匹配了源地址为192.168.1.10的所有IP报文
```

3. 修改流策略,保证SwitchA与SwitchB之间的流量正常转发。

配置思路:新建ACL,匹配SwitchA到SwitchB的流量,这部分流量不做重定向。

配置顺序:配置流分类时,先创建不做重定向的流分类,再配置用于重定向的流分类。配置流策略时,先绑定不做重定向的流分类和流行为,再绑定用于重定向的流分类和流行为。

```bash
<SwitchB> system-view
[SwitchB] acl 3001    //新建ACL
[SwitchB-acl-adv-3001] rule permit ip source 192.168.1.10 0 destination 192.168.1.11 0.0.0.255 //
匹配SwitchA到SwitchB的IP报文(不做重定向的流量)
[SwitchB-acl-adv-3001] quit
```


```bash
[SwitchB] traffic behavior b2 //新建流行为
[SwitchB-behavior-b2] permit //动作为允许(正常转发,不做重定向动作)
[SwitchB-behavior-b2] quit
//由于之前的策略已经调用在接口,所以需要先在接口下取消策略调用,再到流策略中解除绑定的流分类,
在全局删除流分类后再按顺序配置。
[SwitchB] interface GigabitEthernet1/0/1
[SwitchB-GigabitEthernet1/0/1] undo traffic-policy inbound //进入接口下取消策略调用
[SwitchB-GigabitEthernet1/0/1] quit
[SwitchB] traffic policy p1
[SwitchB-trafficpolicy-p1] undo classifier c1 //解除策略下绑定的流分类
[SwitchB-trafficpolicy-p1] quit
[SwitchB] undo traffic classifier c1 //全局下取消之前创建的流分类
[SwitchB] traffic classifier c2  //先创建不做重定向的流分类c2
[SwitchB-classifier-c2] if-match acl 3001  //在c2中匹配acl 3001
[SwitchB-classifier-c2] quit
[SwitchB] traffic classifier c1  //再创建用于重定向的流分类c1
[SwitchB-classifier-c1] if-match acl 3000 //在c1中匹配acl 3000
[SwitchB-classifier-c1] quit
[SwitchB] traffic policy p1 //进入流策略,先绑定不做重定向的流分类和流行为,再绑定需要重定向的流
分类和流行为
[SwitchB-trafficpolicy-p1] classifier c2 behavior b2
[SwitchB-trafficpolicy-p1] classifier c1 behavior b1
[SwitchB-trafficpolicy-p1] quit
[SwitchB] interface GigabitEthernet1/0/1 //进入接口下调用流策略
[SwitchB-GigabitEthernet1/0/1] traffic-policy p1 inbound
[SwitchB-GigabitEthernet1/0/1] quit
```
