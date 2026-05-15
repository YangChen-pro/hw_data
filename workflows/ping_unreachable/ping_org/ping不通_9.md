

### 15.2.9 检查报文格式是否正确

有时虽然交换机收到了报文,但是可能报文的格式不对,导致无法得到正确处理。例如目的MAC错误,VLAN的CFI被置为1等,此时则需要通过获取报文信息来确认。

- • 在端口获取报文可以更加直接的看到设备上报文的收发情况,可以使用端口镜像
或者流镜像获取端口下的所有报文,然后分析ICMP报文格式是否正确。
• 在镜像获取报文无法实施时,使用capture命令确认报文接收情况,然后分析
ICMP报文格式是否正确。
### 配置镜像查看报文收发情况

- • 如果端口上流量不大,可以配置端口镜像,确认报文的收发情况(以SwitchA为
例)。
a. 配置观察口。

```bash
<SwitchA> system-view
[SwitchA] observe-port 1 interface gigabitethernet 1/0/1
```

b. 配置镜像口,获取双向报文。

```bash
[SwitchA] interface gigabitethernet 1/0/2
[SwitchA-GigabitEthernet1/0/1] port-mirroring to observe-port 1 both
[SwitchA-GigabitEthernet1/0/1] return
```

• 如果端口上流量比较大,可以配置流镜像(以SwitchA为例)。

a. 配置观察口。

```bash
<SwitchA> system-view
[SwitchA] observe-port 1 interface gigabitethernet 1/0/1
```

b. 配置ACL规则。

```bash
[SwitchA] acl number 3033
[SwitchA-acl-adv-3033] rule permit icmp source 192.168.1.11 0 destination 192.168.1.10 0
[SwitchA-acl-adv-3033] rule permit icmp source 192.168.1.10 0 destination 192.168.1.11 0
[SwitchA-acl-adv-3033] quit
```

c. 配置流分类。

```bash
[SwitchA] traffic classifier 3033
[SwitchA-classifier-3033] if-match acl 3033
[SwitchA-classifier-3033] quit
```

d. 配置流行为。

```bash
[SwitchA] traffic behavior 3033
[SwitchA-behavior-3033] mirroring to observe-port 1
[SwitchA-behavior-3033] quit
```

e. 配置流策略。

```bash
[SwitchA] traffic policy 3033
[SwitchA-trafficpolicy-3033] classifier 3033 behavior 3033
[SwitchA-trafficpolicy-3033] quit
```

f. 在接口上应用流策略。

```bash
[SwitchA] interface gigabitethernet 1/0/1
[SwitchA-GigabitEthernet1/0/1] traffic-policy 3033 inbound
[SwitchA-GigabitEthernet1/0/1] traffic-policy 3033 outbound
[SwitchA-GigabitEthernet1/0/1] return
```


通过对镜像报文进行分析,不仅可以确认报文的收发情况,同时可以对报文进行校验,包括:报文的VLAN是否正确、报文的目的MAC地址是否是设备系统MAC地址、 报文IP头的checksum是否正确、ICMP的checksum是否正确。

### 使用 capture 命令确认报文接收情况

在镜像获取报文无法实施时,也可以使用Capture命令来确认端口收到的报文情况,可以将报文打印到登录终端进行显示,也可以存入.cap文件中保存到设备上,然后对获取到的报文进行分析。

capture命令如下:

```bash
[HUAWEI] capture-packet interface GigabitEthernet 1/0/1 destination terminal packet-num 100
Info: Captured packets will be shown on terminal.
[HUAWEI]
Packet: 1
----------------------------------------------------------------------
00 00 0a 88 15 d0 00 00 0a 88 15 d5 81 00 00 c8
08 00 45 00 00 54 17 9e 00 00 ff 01 05 eb 07 08
c8 0d 07 08 c8 02 08 00 40 69 ab e4 00 01 Df 84
d1 ea 00 00 00 00 00 01 02 03 04 05 06 07 08 09
0a 0b 0c 0d 0e 0f 10 11 12 13 14 15 16 17 18 19
1a 1b 1c 1d 1e 1f 20 21 22 23 24 25 26 27 28 29
2a 2b 2c 2d 2e 2f
----------------------------------------------------------------------
Packet: 2
----------------------------------------------------------------------
00 00 0a 88 15 d0 00 00 0a 88 15 d5 81 00 00 c8
08 00 45 00 00 54 17 9e 00 00 ff 01 05 eb 07 08
c8 0d 07 08 c8 02 08 00 40 69 ab e4 00 01 Df 84
d1 ea 00 00 00 00 00 01 02 03 04 05 06 07 08 09
0a 0b 0c 0d 0e 0f 10 11 12 13 14 15 16 17 18 19
1a 1b 1c 1d 1e 1f 20 21 22 23 24 25 26 27 28 29
2a 2b 2c 2d 2e 2f
```


说明

该命令只有在V100R006及之后的版本支持。
