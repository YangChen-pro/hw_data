

### 15.2.3 检查物理链路状态是否正常

### 1. 检查物理链路连接

- - 查看设备接口指示灯状态,如果是常灭,说明无连接。此时需要更换接口或
者网线再进行尝试。
- 查看光纤或网线连接的接口和网络要求的部署是否一致。如果不一致,需要
重新对接口进行部署。
- 光纤所带的光模块波长参数需要一致,光模块建议使用华为认证光模块。
- 如果是通过Eth-Trunk接口连接,执行命令display eth-trunk trunk-id检查两
端设备上Eth-Trunk中加入的物理成员接口数量是否一致,如果不一致,需要
进行Eth-Trunk的重新配置。
如果是手工模式Eth-Trunk,回显如下,其中PortName代表的是加入EthTrunk的接口。

<SwitchA> display eth-trunk 11 Eth-Trunk11's state information is: WorkingMode: NORMAL Hash arithmetic: According to SIP-XOR-DIP Least Active-linknumber: 1 Max Bandwidth-affected-linknumber: 8 Operate status: up Number Of Up Port In Trunk: 1 ---------------------------------------------------PortName Status Weight GigabitEthernet1/0/1 Up 1

如果是LACP模式Eth-Trunk,回显如下,其中ActorPortName代表的是加入 Eth-Trunk的接口。

```bash
<SwitchA> display eth-trunk 10
Eth-Trunk10's state information is:
Local:
LAG ID: 10       WorkingMode: LACP
Preempt Delay Time: 10    Hash arithmetic: According to SIP-XOR-DIP
System Priority: 120       System ID: 0018-82d4-04c3
Least Active-linknumber: 1 Max Active-linknumber: 2
Operate status: up      Number Of Up Port In Trunk: 2
-------------------------------------------------------------------------------
ActorPortName              Status  PortType  PortPri PortNo PortKey PortState Weight
GigabitEthernet1/0/1              Selected 1GE             10  262  2609  10111100 1
GigabitEthernet1/0/2              Selected 1GE             10  263  2609  10111100 1
GigabitEthernet1/0/3              Unselect 1GE             32768  264  2609  10100000 1
Partner:
ActorPortName              SysPri  SystemID PortPri PortNo PortKey  PortState
GigabitEthernet1/0/1             32768 00e0-fc6e-bb11 32768 262  2609  10111100
GigabitEthernet1/0/2             32768 00e0-fc6e-bb11 32768 263  2609  10111100
GigabitEthernet1/0/3             32768 00e0-fc6e-bb11 32768 264  2609  10110000
```

### 2. 检查对应的VLANIF接口是否Up

VLANIF接口UP是能Ping通的前提。执行命令display ip interface brief查看 VLANIF接口的状态,如果VLANIF接口Down,说明该VLAN下没有成员接口Up。

```bash
<SwitchA> display ip interface brief
......
Interface       IP Address/Mask    Physical  Protocol
Vlanif10      10.1.1.1/24    down   down
Vlanif30       unassigned     *down   down
```


执行命令display interface brief查看接口状态,保证接口Up。如果接口为Down 状态,请首先排除接口Down的故障。

```bash
<SwitchA> display interface brief
......
Interface       PHY  Protocol InUti OutUti  inErrors outErrors
GigabitEthernet1/0/1   down down  0%  0%    0     0
GigabitEthernet1/0/2   down down  0%  0%    0     0
```

3.如果VLANIF和物理接口均为UP状态,检查设备上是否运行了STP、RRPP或Smart Link等二层协议,确认Ping业务经过的物理接口是否被阻塞。如果接口被阻塞, 需要修改相关的配置。

- 执行命令display stp brief命令,查看STP状态,回显信息中STP State为 FORWARDING表示转发状态,为DISCARDING表示阻塞状态。

```bash
<SwitchA> display stp brief
MSTID Port      Role STP State   Protection
  0  GigabitEthernet1/0/1  DESI DISCARDING  LOOPBACK
```

- 执行命令display rrpp verbose [ domain domain-id [ ring ring-id ] ], 查看RRPP配置的详细信息,回显信息中Port status为UP表示转发状态,为 BLOCKED表示阻塞状态。

```bash
<SwitchA> display rrpp verbose domain 1 ring 1
Domain Index  : 1
Control VLAN  : major 400  sub 401
Protected VLAN : Reference Instance 30
Hello Timer  : 1 sec(default is 1 sec)  Fail Timer : 6 sec(default is 6 sec)
RRPP Ring   : 1
Ring Level  : 0
Node Mode   : Master
Ring State  : Complete
Is Enabled   : Enable             Is Active : Yes
Primary port  : GigabitEthernet1/0/1      Port status: BLOCKED
Secondary port : GigabitEthernet1/0/2      Port status: UP
```

- 执行命令display smart-link group all,查看Smart Link组的状态信息,回显信息中State为Active表示转发状态,为Inactive表示阻塞状态。

```bash
<SwitchA> display smart-link group all
Smart Link group 1 information :
  Smart Link group was enabled
  Link status: Lock
  Wtr-time is: 60 sec.
  Load-Balance Instance: 10
  Protected-vlan reference-instance: 1
  DeviceID: 0025-9e80-2494  Control-vlan ID: 505
  Member     Role  State  Flush Count Last-Flush-Time
----------------------------------------------------------------------
GigabitEthernet1/0/1  Master Inactive 1     2010/09/29 09:30:09 UTC+08:00
  GigabitEthernet1/0/2  Slave Active  0     0000/00/00 00:00:00 UTC+00:00
```

