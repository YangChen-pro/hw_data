

### 15.2.8 检查CPCAR统计是否有过多ICMP报文被丢弃

查看CPCAR的统计情况,检查ICMP报文是否由于CPCAR超出限制被丢弃,相关命令行如下(不同形态、不同版本的命令行有所不同):

• 对于框式交换机V100R002版本、盒式交换机V100R005版本,执行display cpudefend icmp statistics all命令查看Drop计数是否在增加。

```bash
<HUAWEI> display cpu-defend icmp statistics all
CPCAR on mainboard
--------------------------------------------------------------------------
Packet Type     Pass(Bytes) Drop(Bytes)  Pass(Packets)  Drop(Packets)
icmp     0     0     0     0
--------------------------------------------------------------------------
CPCAR on slot 4
--------------------------------------------------------------------------
Packet Type     Pass(Bytes) Drop(Bytes)  Pass(Packets)  Drop(Packets)
icmp     0     0     0     0
--------------------------------------------------------------------------
```

• 对于框式交换机V100R003及之后版本、盒式交换机V100R005及之后版本,执行 display cpu-defend statistics packet-type icmp all命令查看Drop计数是否在增加。

```bash
<HUAWEI> display cpu-defend statistics packet-type icmp all
Statistics on mainboard:
----------------------------------------------------------------------
Packet Type     Pass(Bytes) Drop(Bytes)  Pass(Packets)  Drop(Packets)
----------------------------------------------------------------------
icmp     4488     0     44      0
----------------------------------------------------------------------
Statistics on slot 3:
----------------------------------------------------------------------
Packet Type     Pass(Bytes) Drop(Bytes)  Pass(Packets)  Drop(Packets)
----------------------------------------------------------------------
icmp     0     0     0     0
----------------------------------------------------------------------
```

如果Drop计数在增加,说明存在CAR丢包,可以适当增加CAR值再进行Ping测试,看问题是否解决,最后建议恢复CAR值。

须知

调整CPCAR不当将会影响网络业务,如果需要调整CPCAR,建议联系技术支持人员处理。

修改CAR的命令如下:

1.配置cpu-defend policy,执行命令car packet-type icmp cir cir-value指定新的 CAR值。

```bash
<HUAWEI> system-view
[HUAWEI] cpu-defend policy 1
[HUAWEI-cpu-defend-policy-1] car packet-type icmp cir 256
[HUAWEI-cpu-defend-policy-1] display this
#
cpu-defend policy 1
car packet-type icmp cir 256 cbs 48128
#
```

2. 将该Policy策略在全局或者指定的接口板应用。

- - 全局应用:
[HUAWEI] cpu-defend-policy 1 global
- 在指定的接口板应用:


```bash
[HUAWEI] slot 1
[HUAWEI-slot-1] cpu-defend-policy 1
[HUAWEI-slot-1] display this
#
slot 1
cpu-defend-policy 1
#
```
