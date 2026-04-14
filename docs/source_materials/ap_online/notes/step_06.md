### 步骤6 如果AP下线原因为心跳超时

请按如下步骤进行排查：

**1. 检查WAC长ping AP时是否存在丢包。**

- 如果不能ping通或丢包严重，请检查网络是否正常、网线等连接线是否老化。
- 如果能够ping通，请登录AP获取日志文件，查看AP掉线时间点记录的网络ping结果。如果ping包结果超时，则AP下线为网络异常导致，请联系技术支持人员进行定位。

**2. 检查中间网络是否存在某类型报文过量的情况。**

大量报文（如ND报文等）上送设备，会导致设备CPU使用率过高，很可能导致AP掉线。在AC上执行命令`display cpu-defend statistics`，查看上送CPU的报文统计。如果存在某些报文数量过多，则需要排查网络，找到该类报文的来源，具体请联系技术支持人员寻求技术支持。

```bash
<WAC> display cpu-defend statistics all
Statistics(packets) on slot 0 :
----------------------------------------------------------------------------------------------
PacketType                 Total Passed   Total Dropped  Last Dropping Time
                           Last 5 Min Passed Last 5 Min Dropped
----------------------------------------------------------------------------------------------
8021x                      0              0               -
                           0              0
...
```

**3. 检查CPU使用率是否过高。**

如果设备的CPU利用率一直很高（超过80%），会导致各种业务异常，出现丢包、网络延迟大等现象。在AC上执行命令`display cpu-usage`，查看设备CPU使用率历史信息。造成设备CPU使用率高的原因有很多，当设备的CPU使用率一直很高时，请参考故障案例：CPU占用率高的定位思路进行处理。

```bash
<WAC> display cpu-usage
Slot: 0 CPU:0
CPU utilization statistics at 2022-09-28 10:49:55 616 ms
System CPU Using Percentage : 10%
Dataplane CPU Using Percentage : 0%
CPU utilization for five seconds: 10%, one minute: 9%, five minutes: 9%.
Max CPU Usage : 48%
Max CPU Usage Stat. Time : 2022-09-27 19:12:14 867 ms
State: Unoverload
Overload threshold: 90%, Overload clear threshold: 75%, Duration: 60s
```

**4. 排查接入层交换机的配置，检查是否存在风暴告警或存在大量广播报文。**

在交换机上执行命令`display interface`，查看接口上的组播和广播报文的统计信息，并观察组播、广播报文增长速率。

```bash
<Switch> display interface 10ge 1/0/1
10GE 1/0/1 current state : UP
Line protocol current state : UP
...
Input: 7650 packets, 1327062 bytes
Unicast: 0, Multicast: 7650
Broadcast: 0, Jumbo: 0
...
```

如果该接口接收到的广播、组播报文过多，则需要继续检查是否配置了风暴控制。

在交换机上执行命令`display storm control`，查看对应接口上配置的风暴控制信息。

```bash
<HUAWEI> display storm control interface 10ge 1/0/1
--------------------------------------------------------------------------------
NOTE:
BC = Broadcast; MC = Unknown Multicast; UUC = Unknown Unicast
Int = Interval value (unit: seconds)
--------------------------------------------------------------------------------
PortName Type MaxRate Mode Action Punish- Trap Log Int Last
Status Punish-Time
--------------------------------------------------------------------------------
10GE1/0/1 BC 2000 Pps Block Normal Off On 90 --
10GE1/0/1 MC 2000 Pps Block Normal Off On 90 --
10GE1/0/1 UUC 2000 Pps Block Normal Off On 90 --
```

如果"Action"显示为"Error-Down"，则建议先排除引起接口Error-Down的原因。有以下两种方式可以恢复接口状态：

- **手动恢复（Error-Down发生后）**：当处于Error-Down状态的接口数量较少时，可在该接口视图下依次执行命令`shutdown`和`undo shutdown`，或者执行命令`restart`，重启接口。
- **自动恢复（Error-Down发生前）**：如果处于Error-Down状态的接口数量较多，逐一手动恢复接口状态将产生大量重复工作，且可能出现部分接口配置遗漏。为避免这一问题，用户可在系统视图下执行命令`error-down auto-recovery cause storm-control interval interval-value`使能接口状态自动恢复为Up的功能，并设置接口自动恢复为Up的延时时间。可以通过执行命令`display error-down recovery`查看接口状态自动恢复信息。

**5. 检查AC、中间交换机上是否存在IP冲突或者ARP miss。**

可通过命令行`display trapbuffer`查看设备Trap缓冲区信息，看是否存在大量"ARP detects IP conflict"或"arp-miss"相关告警。排查网络中是否存在与AP网关冲突的IP地址。

**6. 如果使用交换机作为AP网关，需要排查交换机上是否存在大量TC报文，导致AP的ARP表项频繁刷新，引发AP掉线。**

正常情况下，当STP检测到网络的拓扑发生变化，会发送TC报文通知ARP模块对ARP表项进行老化或者删除，此时设备需要重新进行ARP学习，以获得最新的ARP表项信息。但是如果网络的拓扑变化频繁，或者网络中设备的ARP表项很多，ARP的重新学习会导致网络中的ARP报文过多，极大地占用系统资源，影响其他业务的正常运行。

为了尽量避免这种情况的发生，可以让ARP表不响应TC报文，这样即使网络的拓扑发生了变化，网络中设备的ARP表项也不会被老化或者删除。同时，开启MAC刷新ARP功能，避免ARP表项没有得到及时刷新，可能导致用户业务中断。

```bash
<Switch> display stp topology-change    //查看拓扑变化
<Switch> display stp tc-bpdu statistics  //查看端口TC报文收发计数
```

如果交换机上存在大量TC报文，可以执行如下命令解决：

```bash
<Switch> system-view
[Switch] mac-address update arp enable  //开启MAC刷新ARP功能，即MAC地址的出接口变化时，通知更新ARP表项的出接口
[Switch] arp topology-change disable    //关闭设备响应TC报文的功能，即当设备收到TC报文时，不对ARP表项进行老化或删除
```

**7. 检查CAPWAP配置是否正确。**

a. **心跳检测间隔时间的配置是否合理。**

CAPWAP心跳检测间隔时间如果配置得过短，在网络状况不佳时，可能会导致AP掉线。

缺省情况下，CAPWAP心跳检测的间隔时间为25秒，心跳检测报文次数为6。如果开启了双链路备份功能，则缺省情况下，CAPWAP心跳检测的间隔时间为25秒，心跳检测报文次数为3。如果"Echo interval(seconds)"小于缺省值，建议适当调高该值。

```bash
<WAC> display capwap configuration
---------------------------------------------------------------
Source interface IPv4 : vlanif 120
Source interface IPv6 : -
Source IPv4 address : -
Source IPv6 address : -
Echo interval(seconds) : 25
Echo times : 6
...
```

b. **检查CAPWAP配置的源接口是否被误shutdown，如果被shutdown，需要undo shutdown。**

```bash
<WAC> system-view
[WAC] interface vlanif 120
[WAC-Vlanif120] undo shutdown
```

c. **检查capwap source是否配置了VLANIF 1，如果是，需要修改为其他VLANIF接口。**

```bash
<WAC> system-view
[WAC] undo capwap source interface vlanif 1
[WAC] capwap source interface vlanif 120
```

**8. 如果有获取报文头的条件，可同时获取AP、AC侧CAPWAP报文，查看中间链路是否存在丢包。**

----结束