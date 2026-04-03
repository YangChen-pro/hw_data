### 15.2 Ping 不通故障定位指导

### 15.2.1 检查 Ping 命令是否合理

在SwitchA上检查是否执行了ping -f 192.168.1.11命令,如果执行了此操作,则ICMP 报文发送的过程中不支持分片,此时需要检查链路上出接口的MTU值。

```bash
<SwitchA> system-view
[SwitchA] interface GigabitEthernet 1/0/1
[SwitchA-GigabitEthernet1/0/1] display this
[SwitchA-GigabitEthernet1/0/1] undo portswitch
[SwitchA-GigabitEthernet1/0/1] mtu 1600 //接口的MTU值为1600字节,如果此字段不显示,代表接口的MTU
为缺音值1500字节。
```

如果MTU值小于ICMP报文长度,由于ICMP报文的发送过程中不支持分片,如果ICMP 报文的大小超过链路的MTU值,ICMP报文将会被丢弃,所以会导致Ping不通,此时可以通过不使用-f参数或者增大链路MTU值的方式使ICMP报文不被丢弃。

如果您需要了解Ping命令的格式, 请参见Ping命令格式。

