

### 15.2.7 检查报文收发是否正常

如果通过以上步骤排查配置、链路、ARP表项和路由表项均正常,但是仍然Ping不通,接下来检查ICMP报文收发是否正常。

### ICMP 统计查询

进行Ping操作时,通过命令display icmp statistics查看ICMP报文的收发情况,ICMP Echo Request和ICMP Echo Reply报文收发是否一致,是否存在checksum错误统计计数。

SwitchA Ping SwitchB,以SwitchA的回显为例,Output方向的echo字段代表的是请求报文数目,Input方向的echo reply代表的是应答报文数目,bad checksum代表的是校验错误的报文数目。

```bash
<SwitchA> display icmp statistics
 Input: bad formats      0       bad checksum      0
    echo      0      0       destination unreachable 0
    source quench      0      0       redirects      0
    echo reply      25       parameter problem      0
    timestamp request  0       information request  0
    mask requests      0      0       mask replies      0
    time exceeded      0      0       timestamp reply      0
    Mping request      0      0       Mping reply      0
 Output:echo      25      0       destination unreachable 0
    source quench      0      0       redirects      0
    echo reply      0      0       parameter problem      0
    timestamp request  0      0       information reply      0
    mask requests      0      0       mask replies      0
    time exceeded      0      0       timestamp reply      0
    Mping request      0       Mping reply      0
```

在SwitchA上执行Ping操作的前后查看bad checksum计数是否一直增长,如果一直增长,需要检查对端设备SwitchB的协议栈软件回应ICMP报文的格式是否正确。

如果echo和echo reply数目一致,但是仍然Ping不通,接下来需要进行ICMP报文流量统计进而判断报文的收发情况。

如果echo和echo reply数目不一致:


- • 如果SwitchA发出的echo报文数目少于Ping发送的报文数目,说明报文在SwitchA
上被丢弃。
• 如果SwitchA发出的echo报文数目多于SwitchB接收到的echo报文的数目,说明报
文在传输链路上被丢弃。
• 如果SwitchA发出的echo报文数目等于SwitchB接收到的echo报文的数目,但是离
开SwitchB的echo reply报文数目少于进入SwitchB的echo报文的数目,说明报文
在SwitchB上被丢弃。
如果报文在链路上被丢弃,请更换链路再进行Ping测试;如果报文在终端或其他厂商设备被丢弃,请排查终端或者其他厂商设备;如果报文在华为交换机被丢弃,可进入下一步排查或者联系技术支持人员处理。

## ICMP报文流量统计

以SwitchA为例,介绍如何对ICMP报文做流量统计。

#配置进入SwitchA报文的流量统计。

1. 配置ACL规则。


这里的ACL一定要是高级ACL,编号范围为3000~3999。

```bash
<SwitchA> system-view
[SwitchA] acl number 3000
[SwitchA-acl-adv-3000] rule permit icmp source 192.168.1.11 0 destination 192.168.1.10 0
[SwitchA-acl-adv-3000] quit
```

2.配置流分类。

```bash
[SwitchA] traffic classifier 3000
[SwitchA-classifier-3000] if-match acl 3000
[SwitchA-classifier-3000] quit
```

3. 配置流行为。

```bash
[SwitchA] traffic behavior 3000
[SwitchA-behavior-3000] statistic enable
[SwitchA-behavior-3000] quit
```

4. 配置流策略。

```bash
[SwitchA] traffic policy 3000
[SwitchA-trafficpolicy-3000] classifier 3000 behavior 3000
[SwitchA-trafficpolicy-3000] quit
```

5. 在接口上应用流策略

```bash
[SwitchA] interface gigabitethernet 1/0/1
[SwitchA-GigabitEthernet1/0/1] traffic-policy 3000 inbound
[SwitchA-GigabitEthernet1/0/1] return
```

#配置离开SwitchA报文的流量统计。

1. 配置ACL规则。


这里的ACL一定要是高级ACL,编号范围为3000~3999。

```bash
<SwitchA> system-view
[SwitchA] acl number 3001
[SwitchA-acl-adv-3001] rule permit icmp source 192.168.1.10 0 destination 192.168.1.11 0
[SwitchA-acl-adv-3001] quit
```

2. 配置流分类。

```bash
[SwitchA] traffic classifier 3001
[SwitchA-classifier-3001] if-match acl 3001
[SwitchA-classifier-3001] quit
```


3. 配置流行为。

```bash
[SwitchA] traffic behavior 3001
[SwitchA-behavior-3001] statistic enable
[SwitchA-behavior-3001] quit
```

4. 配置流策略。

```bash
[SwitchA] traffic policy 3001
[SwitchA-trafficpolicy-3001] classifier 3001 behavior 3001
[SwitchA-trafficpolicy-3001] quit
```

5. 在接口上应用流策略

```bash
[SwitchA] interface gigabitethernet 1/0/1
[SwitchA-GigabitEthernet1/0/1] traffic-policy 3001 outbound
[SwitchA-GigabitEthernet1/0/1] return
```

如果是交换机直连PC,在连接PC的接口出、入方向调用流统策略;如果是交换机与其他网络设备直连,建议在两台设备两个接口的出、入方向都使用流量统计。

配置完成后,先执行reset命令清空计数信息,以保证接口流统计数归零,相关命令如下:

reset traffic policy statistics interface GigabitEthernet 1/0/1 inbound

reset traffic policy statistics interface GigabitEthernet 1/0/1 outbound

在SwitchA上持续Ping SwitchB, 通过display traffic policy statistics interface interface-type interface-number{ inbound | outbound } verbose rule-base命令查看接口流量统计信息。

以SwitchA出方向为例,介绍上述display命令的回显,其中Packets和Bytes分别代表报文包个数和报文字节数。

```bash
<SwitchA> display traffic policy statistics interface gigabitethernet 1/0/1 outbound verbose rule-base
Interface: GigabitEthernet1/0/1
Traffic policy outbound: 3001
Rule number: 1
Current status: OK!
Statistics interval: 300
----------------------------------------------------------------------
Classifier: 3001 operator or
Behavior: 3001
Board : 1
rule 5 permit icmp source 10.1.1.1 0 destination 10.1.1.2 0 (match-counter
0)
----------------------------------------------------------------------
Passed     |  Packets:         100
        |  Bytes:         10,200
        |  Rate(pps):         0
        |  Rate(bps):         0
----------------------------------------------------------------------
Dropped     |  Packets:         0
        |  Bytes:         0
        |  Rate(pps):         0
        |  Rate(bps):         0
```

- • 如果离开SwitchA的报文数目少于Ping发送的报文数目,说明报文在SwitchA上被
丢弃。
• 如果离开SwitchA的报文数目多余进入SwitchB的报文数目,说明报文在传输链路
上被丢弃。
• 如果离开SwitchA的报文数目等于进入SwitchB的报文数目,但是离开SwitchB的
报文数目少于进入SwitchB的报文数目,说明报文在SwitchB上被丢弃。
如果报文在链路上被丢弃,请更换链路再进行Ping测试;如果报文在终端或其他厂商设备被丢弃,请排查终端或者其他厂商设备;如果报文在华为交换机被丢弃,可进入下一步排查或者联系技术支持人员处理。
