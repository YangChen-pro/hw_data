## 1.1.2 802.1X认证失败常见问题

- RADIUS服务器认证拒绝

- RADIUS服务器不响应

- RADIUS服务器授权数据失败

- 认证账号被锁定

- 终端MAC地址静默

- 终端不响应EAP报文

- 四步握手失败

- 认证成功后定时做重认证

### 1.1.2.1 RADIUS服务器认证拒绝

通过命令display aaa online-fail-record mac-address H-H-H查看终端上线失败记录，用户上线失败原因（User online fail reason）显示Radius authentication reject。

```text
[HUAWEI] display aaa online-fail-record mac-address 64e5-99f3-18f6
----------------------------------------------------------------
User name               : test
Domain name             : domain_test
User MAC                : 64e5-99f3-18f6
User access type        : 802.1x
User access interface   : Wlan-Dbss17496
Qinq vlan/User vlan     : 0/200
User IP address         : -
User IPV6 address       : -
User ID                 : 32846
User login time         : 2020/10/19 14:53:22
User online fail reason : Radius authentication reject
Authen reply message    : ErrorReason is Incorrect user na...
User name to server     : test
AP ID                   : 0
Radio ID                : 0
AP MAC                  : 18de-d777-c120
SSID                    : dot1x_test
----------------------------------------------------------------
```

通过业务诊断功能，追踪终端用户上线认证过程，看到RADIUS服务器回应了拒绝报文：

```text
[HUAWEI] trace object mac-address 64e5-99f3-18f6
[HUAWEI] trace enable
[BTRACE][2020/10/19 14:53:23][6144][RADIUS][64e5-99f3-18f6]:
Received a authentication reject packet from radius server(server ip = 10.10.10.1).
[BTRACE][2020/10/19 14:53:23][6144][RADIUS][64e5-99f3-18f6]:
Server Template: 4
Server IP   : 10.10.10.1
Server Port : 1812
Protocol: Standard
Code    : 3
Len     : 176
ID      : 80
[EAP-Message                        ] [6 ] [04 22 00 04 ]
[State                              ] [16] [\001u?\237\372O]
[Reply-Message                      ] [116] [ErrorReason is Incorrect user name or password or Incorrect dataSource or Incorrect access device key.ErrCode:4101]
[Message-Authenticator              ] [18] [00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ]
[BTRACE][2020/10/19 14:53:23][6144][RADIUS][64e5-99f3-18f6]:Send authentication reject message to AAA.
[BTRACE][2020/10/19 14:53:23][6144][AAA][64e5-99f3-18f6]:
AAA receive AAA_RD_MSG_AUTHENREJECT message(51) from RADIUS module(235).
```

服务器回应认证拒绝有多种原因，最常见的有用户名密码错误、授权策略无法匹配等，这些问题需要首先通过排查服务器日志找到根因后，再调整服务器、终端或设备配置解决。

### 1.1.2.2 RADIUS服务器不响应

通过命令display aaa online-fail-record mac-address H-H-H查看终端上线失败记录，用户上线失败原因（User online fail reason）显示The radius server is up but has no reply或者The radius server is not reachable。

```text
[HUAWEI] display aaa online-fail-record mac-address 00e0-fc2d-0c70
------------------------------------------------------------------------------
User name               : huawei-dot1x
Domain name             : dot1x-radius
User MAC                : 00e0-fc2d-0c70
User access type        : 802.1x
Qinq vlan/User vlan     : 0/11
User IP address         : -
User IPV6 address       : -
User ID                 : 65697
User login time         : 2023/12/29 16:46:39
User online fail reason : The radius server is up but has no reply
Authen reply message    : -
User name to server     : huawei-dot1x
AP ID                   : 2
Radio ID                : 0
WLAN ID                 : 3
AP MAC                  : 00e0-fc71-1020
SSID                    : dot1x-23.160
------------------------------------------------------------------------------
[HUAWEI] display aaa online-fail-record mac-address 00e0-fc2d-0c70
------------------------------------------------------------------------------
User name               : huawei-dot1x
Domain name             : dot1x-radius
User MAC                : 00e0-fc2d-0c70
User access type        : 802.1x
Qinq vlan/User vlan     : 0/11
User IP address         : -
User IPV6 address       : -
User ID                 : 65697
User login time         : 2023/12/29 16:51:11
User online fail reason : The radius server is up but has no reply
Authen reply message    : -
User name to server     : huawei-dot1x
AP ID                   : 2
Radio ID                : 0
WLAN ID                 : 3
AP MAC                  : 00e0-fc71-1020
SSID                    : dot1x-23.160
------------------------------------------------------------------------------
```

通过业务诊断功能，追踪终端用户上线认证过程，看到RADIUS服务器无响应：

```text
[HUAWEI] trace object mac-address 00e0-fc2d-0c70
[HUAWEI] trace enable
[HUAWEI] quit
<HUAWEI> terminal monitor
<HUAWEI> terminal debugging
<HUAWEI> debugging timeout 0 // 关闭debugging超时结束的功能
[BTRACE][2023-12-29 16:46:28-08:08][0][AAA][00e0-fc2d-0c70:
AAA receive AAA_RD_MSG_SERVERNOREPLY message(61) from RADIUS module(6).
[BTRACE][2023-12-29 16:46:28-08:08][0][AAA][00e0-fc2d-0c70:
CID:269  TemplateNo:29  SerialNo:43
SrcMsg:AAA_RD_MSG_AUTHENREQ
PriyServer::: Vrf:0
SendServer::: Vrf:0
[BTRACE][2023-12-29 16:46:28-08:08][0][AAA][00e0-fc2d-0c70:Radius server is up but no response.
[BTRACE][2023-12-29 16:46:28-08:08][0][AAA][00e0-fc2d-0c70:
[AAA ERROR]authen finish,the authen fail code is:8,reason is:Radius server is up but no response.
```

RADIUS服务器不响应问题排查步骤如下：

1. 确认RADIUS服务器是否正确添加设备IP。

RADIUS服务器如果没有添加设备IP地址则需要添加正确的设备IP。

2. 如果RADIUS服务器已经添加设备IP地址，需要确认添加的设备IP与设备发送RADIUS认证请求报文的源IP是否相同。

设备发送RADIUS认证请求报文的源IP可通过命令配置，如果没有通过命令配置，则使用路由出接口IP地址。如果RADIUS服务器上添加的设备IP地址与路由出接口IP地址一致，则不需要在设备上配置与RADIUS服务器通信的源IP地址，否则需要通过命令配置源IP地址。

  a. 先根据RADIUS服务器IP地址查找路由表获取出接口，然后再根据出接口确认IP地址，如果RADIUS服务器添加的设备IP地址与路由出接口地址一致，则不需要再通过命令配置与RADIUS服务器通信的源IP地址。

```text
[HUAWEI] display ip routing-table 172.94.2.96
Proto: Protocol        Pre: Preference
Route Flags: R - relay, D - download to fib, T - to vpn-instance, B - black hole route
------------------------------------------------------------------------------
Routing Table : _public_
Summary Count : 1
Destination/Mask    Proto   Pre  Cost        Flags NextHop                                  Interface
172.94.2.0/24  Direct  0    0             D   172.94.2.160                             Vlanif172
[HUAWEI] interface Vlanif 172
[HUAWEI] display this
#
interface Vlanif172
ip address 172.94.2.160 255.255.255.0
#
```

  b. 如果RADIUS服务器添加的设备IP地址与路由出接口地址不同，则需要在设备上配置与RADIUS服务器通信的源IP地址。源IP地址可在全局下配置，也可在RADIUS服务器模板下配置，RADIUS服务器模板下配置的源IP地址优先级高于全局下的配置。

在VRRP双机热备场景开启了无线配置同步条件下，只能在全局下配置与RADIUS服务器通信的源IP地址，如果是单机场景下，建议在RADIUS服务器模板下配置源IP地址。

查询设备上配置的与RADIUS服务器通信的源IP地址。

    i. 查看全局是否配置与RADIUS服务器通信的源IP地址。

```text
[HUAWEI] display radius-server configuration
------------------------------------------------------
Global:
Radius Server Source IP Address           : -
Radius Server Source IPv6 Address         : ::
Radius Attribute Nas IP Address           : -
Radius Attribute Nas IPv6 Address         : ::
------------------------------------------------------
[HUAWEI] display radius-server configuration
------------------------------------------------------
Global:
Radius Server Source IP Address           : 100.1.1.1
Radius Server Source IPv6 Address         : ::
Radius Attribute Nas IP Address           : -
Radius Attribute Nas IPv6 Address         : ::
------------------------------------------------------
```

如果“Radius Server Source IP Address”为“-”，则表明全局下没有配置源IP地址，如果“Radius Server Source IP Address”为具体IP地址，则表明配置了源IP地址。

    ii. 查看RADIUS服务器模板是否配置与RADIUS服务器通信的源IP地址。

```text
[HUAWEI] radius-server template radius_test
[HUAWEI-radius-radius_test] display this
#
radius-server template radius_test
radius-server shared-key cipher %^%#x\[y<Fe^2Dee<5/L>B5Wd"!3GqH6,@[kW(Xi6PYA%^%#
radius-server authentication 10.10.10.1 1812 source ip-address 100.1.1.1 weight 80
radius-server accounting 10.10.10.1 1813 source ip-address 100.1.1.1 weight 80
#
[HUAWEI] radius-server template radius_test
[HUAWEI-radius-radius_test] display this
#
radius-server template radius_test
radius-server shared-key cipher %^%#x\[y<Fe^2Dee<5/L>B5Wd"!3GqH6,@[kW(Xi6PYA%^%#
radius-server authentication 10.10.10.1 1812 source Vlanif 100 weight 80
radius-server accounting 10.10.10.1 1813 source Vlanif 100 weight 80
```

如果RADIUS服务器模板下再认证服务器或计费服务器后面写的“source ip-address”或者“source vlanif”，则表明RADIUS服务器模板下配置了源IP地址。

配置设备与RADIUS服务器通信的源IP地址。

    i. 在RADIUS模板下配置与RADIUS服务器通信源IP地址。

```text
[HUAWEI] radius-server template radius_test
[HUAWEI-radius-radius_test] radius-server authentication 10.10.10.1 1812 source ip-address 100.1.1.1
```

3. 确认设备与RADIUS服务器之间中间链路是否正常。

  a. 从设备指定源IP ping服务器测试，确认路由是否可达。

```text
[HUAWEI] ping -a 10.10.10.76 10.10.10.1
```

  b. 在设备和服务器同时抓包确认认证报文收发是否正常，常见问题有中间网络存在防火墙，防火墙未放通RADIUS（默认认证端口：1812）报文。

4. 查看RADIUS服务器状态是否正常，STState字段如果不是STState-up状态，则为异常。

```text
[HUAWEI] display radius-server item template radius_test
---------------------------------------------------------------
STState    = STState-up
STChgTime  = -
ServerId   = 25
Type       = auth-server
State      = state-up
AlarmFlag  = false
STUseNum   = 1
IPAddress  = 100.100.1.1
AlarmTimer = 0xffffffff
Head       = 4129
Tail       = 4383
ProbeID    = 255
SourceIp   = ::
LoopBack   = -
Vlanif     = -
Vrf        = -
--------------------------------------------------------------
```

5. 确认设备与RADIUS服务器配置的共享密钥（shared-key）是否一致。可以通过test-aaa命令测试，同时开启radius debug打印，debug信息中如出现“Authenticator error·”则表示设备与RADIUS服务器配置的共享密钥不一致，需要同时修改设备与RADIUS服务器上共享密钥，使其相同。

```text
[HUAWEI] test-aaa test test radius-template radius_test
[HUAWEI]
Oct 24 2020 15:57:49.591.1+08:00 AC6605_129_76 RDS/7/DEBUG:
RADIUS packet: IN (TotalLen=20)
Len 1 ~ 20:
02 08 00 14 F6 DA 06 57 40 25 32 2A A9 70 6E FD
46 F6 B1 25
[HUAWEI]
Oct 24 2020 15:57:49.591.2+08:00 AC6605_129_76 RDS/7/DEBUG:
[RDS(Err):] Receive a illegal packet(Authenticator error), please check share key config.(ip:10.10.10.1 port:1812)
```

设备支持在全局下配置指定RADIUS服务器的共享密钥及在RADIUS服务器模板下配置共享密钥，其中全局下的配置优先级高于模板下的配置。

建议在RADIUS服务器模板下配置共享密钥，如果两个都配置的条件下，建议删除全局下的配置，仅保留模板下的配置。

RADIUS服务器模板下配置共享密钥：

```text
[HUAWEI] radius-server template radius_test
[HUAWEI-radius-radius_test] radius-server shared-key cipher HUAWEI@123
```

### 1.1.2.3 RADIUS服务器授权数据失败

通过命令display aaa online-fail-record mac-address H-H-H查看终端上线失败记录，用户上线失败原因（User online fail reason）显示Authorization data error。

```text
[HUAWEI] display aaa online-fail-record mac-address 64e5-99f3-18f6
----------------------------------------------------------------
User name               : test
Domain name             : domaintest
User MAC                : 64e5-99f3-18f6
User access type        : 802.1x
User access interface   : Wlan-Dbss17496
Qinq vlan/User vlan     : 0/200
User IP address         : -
User IPV6 address       : -
User ID                 : 32873
User login time         : 2020/10/24 16:32:34
User online fail reason : Authorization data error
Authen reply message    : -
User name to server     : test
AP ID                   : 0
Radio ID                : 0
AP MAC                  : 18de-d777-c120
SSID                    : dot1x_test
----------------------------------------------------------------
```

原因为RADIUS服务器授权了相关权限（如VLAN或者ACL等），但设备上无对应的授权内容配置（如未创建授权VLAN或者未创建授权ACL）。

通过业务诊断功能，追踪终端用户上线认证过程，看到RADIUS服务器下发的授权内容：

```text
[HUAWEI] trace object mac-address 64e5-99f3-18f6
[HUAWEI] trace enable
```

- 授权VLAN检查失败

```text
[BTRACE][2020/10/24 16:48:14][6144][RADIUS][64e5-99f3-18f6]:
Received a authentication accept packet from radius server(server ip = 12.12.12.1).
[BTRACE][2020/10/24 16:48:14][6144][RADIUS][64e5-99f3-18f6]:
Server Template: 4
Server IP   : 12.12.12.1
Server Port : 1812
Protocol: Standard
Code    : 2
Len     : 194
ID      : 194
[Tunnel-Type                        ] [6 ] [13]
[Tunnel-Medium-Type                 ] [6 ] [6]
[Tunnel-Private-Group-ID            ] [6 ] [201]
[EAP-Message                        ] [6 ] [03 4a 00 04 ]
[State                              ] [16] [\001uY\311\025N]
[MS-MPPE-Send-Key                   ] [52] [fb a1 e9 55 16 62 a3 e5 da 35 fc ce 3e 8f ae 7d ac 0a d6 0b 20 59 ad 82 a8 66 88 06 6a 81 10 82 61 95 2e cf 44 50 c0 79 e5 3f a4 32 43 45 a5 9e 2b c4 ]
[MS-MPPE-Recv-Key                   ] [52] [fb a1 e9 65 b1 18 6d 60 8f 0a ed af 53 1e 26 8a e6 18 9d 26 8c 21 c8 4f c2 8a 6a d5 a8 85 8a 9d ba d8 be 8d 97 b8 b8 d3 24 04 21 23 90 71 33 35 f4 6b ]
[Message-Authenticator              ] [18] [00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ]
[BTRACE][2020/10/24 16:48:14][6144][RADIUS][64e5-99f3-18f6]:Send authentication reply message to AAA.
[BTRACE][2020/10/24 16:48:14][6144][AAA][64e5-99f3-18f6]:
AAA receive AAA_RD_MSG_AUTHENACCEPT message(50) from RADIUS module(235).
[BTRACE][2020/10/24 16:48:14][6144][AAA][64e5-99f3-18f6]:
CID:57  TemplateNo:4  SerialNo:73
SrcMsg:AAA_RD_MSG_AUTHENREQ
PriyServer::: Vrf:0
SendServer:12.12.12.1 Vrf:0
SessionTimeout:0 IdleTimeout:0
AcctInterimInterval:0 RemanentVolume:0
InputPeakRate:0 InputAverageRate:0
OutputPeakRate:0 OutputAverageRate:0
InputBasicRate:0 OutputBasicRate:0
InputPBS:0 OutputPBS:0
Priority:[0,0] DNS:[0.0.0.0, 0.0.0.0]
ServiceType:0 LoginService:0 AdminLevel:0 FramedProtocol:0
LoginIpHost:0 NextHop:0
EapLength:4 ReplyMessage:
TunnelType:13 MediumType:6 PrivateGroupID:201
WlanReasonCode:0
[BTRACE][2020/10/24 16:48:14][6144][AAA][64e5-99f3-18f6]:
[AAA ERROR]AAA check authen ack, check VLANID error!
[BTRACE][2020/10/24 16:48:14][6144][AAA][64e5-99f3-18f6]:Radius authorization data error.
[BTRACE][2020/10/24 16:48:14][6144][AAA][64e5-99f3-18f6]:
[AAA ERROR]authen finish,the authen fail code is:16,reason is:Radius authorization data error.
```

授权VLAN需要同时下发RADIUS 64号属性Tunnel-Type，值固定为13，表示VLAN协议，RADIUS 65号属性Tunnel-Medium-Type，值固定为6，表示以太类型，RADIUS 81号属性Tunnel-Private-Group-ID，支持通过VLAN编号、VLAN描述信息、VLAN名称和VLAN Pool授权，并且授权生效顺序为：VLAN编号 > VLAN描述信息 > VLAN名称 > VLAN Pool。

- 授权ACL检查失败

```text
Received a authentication accept packet from radius server(server ip = 12.12.12.1).
[BTRACE][2020/10/24 16:52:19][6144][RADIUS][64e5-99f3-18f6]:
Server Template: 4
Server IP   : 12.12.12.1
Server Port : 1812
Protocol: Standard
Code    : 2
Len     : 182
ID      : 205
[Filter-Id                          ] [6 ] [3000]
[EAP-Message                        ] [6 ] [03 4c 00 04 ]
[State                              ] [16] [\001uY\314\321\003]
[MS-MPPE-Send-Key                   ] [52] [bd ce 7f 1d bf 78 33 d4 6c 45 d8 d0 1b f7 ee d2 02 16 7a ac fd 62 25 88 f7 84 7a 22 44 d8 01 8a 99 a3 33 66 7d 47 e9 a7 ed 88 d5 01 f8 62 4f 9d cd 56 ]
[MS-MPPE-Recv-Key                   ] [52] [bd ce 7f 54 6f 27 35 d1 01 5c f1 5e aa e8 27 91 c7 8b 89 2f 06 8f ac 46 13 5c 92 78 ec cf 39 aa dc bb f8 ff b1 b8 5c 42 6b f8 ca 80 76 b1 e8 35 c9 ed ]
[Message-Authenticator              ] [18] [00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ]
[BTRACE][2020/10/24 16:52:19][6144][RADIUS][64e5-99f3-18f6]:Send authentication reply message to AAA.
[BTRACE][2020/10/24 16:52:19][6144][AAA][64e5-99f3-18f6]:
AAA receive AAA_RD_MSG_AUTHENACCEPT message(50) from RADIUS module(235).
[BTRACE][2020/10/24 16:52:19][6144][AAA][64e5-99f3-18f6]:
CID:58  TemplateNo:4  SerialNo:75
SrcMsg:AAA_RD_MSG_AUTHENREQ
PriyServer::: Vrf:0
SendServer:12.12.12.1 Vrf:0
SessionTimeout:0 IdleTimeout:0
AcctInterimInterval:0 RemanentVolume:0
InputPeakRate:0 InputAverageRate:0
OutputPeakRate:0 OutputAverageRate:0
InputBasicRate:0 OutputBasicRate:0
InputPBS:0 OutputPBS:0
Priority:[0,0] DNS:[0.0.0.0, 0.0.0.0]
ServiceType:0 LoginService:0 AdminLevel:0 FramedProtocol:0
LoginIpHost:0 NextHop:0
EapLength:4 ReplyMessage:
TunnelType:0 MediumType:0 PrivateGroupID:
ACLID:3000
WlanReasonCode:0
[BTRACE][2020/10/24 16:52:19][6144][AAA][64e5-99f3-18f6]:
[AAA ERROR]AAA check radius authen ack, check acl error!
[BTRACE][2020/10/24 16:52:19][6144][AAA][64e5-99f3-18f6]:Radius authorization data error.
[BTRACE][2020/10/24 16:52:19][6144][AAA][64e5-99f3-18f6]:
[AAA ERROR]authen finish,the authen fail code is:16,reason is:Radius authorization data error.
```

无线场景下，授权ACL ID取值范围为3000-3031，ACL中rule id最大为64。

RADIUS服务器授权数据失败排查步骤如下：

1. 确认是否需要对应的授权。

  - 如果需要，则需要在设备上创建对应的授权内容，如授权VLAN需要在设备上创建对应VLAN；如授权ACL需要创建对应ACL，并且在ACL中配置相应规则。

  - 如果不需要，可以修改RADIUS服务器上的授权策略，将对应授权内容删除，也可以在设备通过配置忽略对应的授权内容，配置命令如下。

忽略授权VLAN：

```text
[HUAWEI] radius-server template radius_test
[HUAWEI-radius-radius_test] radius-server attribute translate
[HUAWEI-radius-radius_test] radius-attribute disable Tunnel-Private-Group-ID receive
```

忽略授权ACL：

```text
[HUAWEI] radius-server template radius_test
[HUAWEI-radius-radius_test] radius-server attribute translate
[HUAWEI-radius-radius_test] radius-attribute disable Filter-Id receive
```

### 1.1.2.4 认证账号被锁定

通过命令display aaa online-fail-record mac-address H-H-H查看终端上线失败记录，用户上线失败原因（User online fail reason）显示Remote user is blocked。

```text
[HUAWEI] display aaa online-fail-record mac-address 64e5-99f3-18f6
----------------------------------------------------------------
User name               : test
Domain name             : domaintest
User MAC                : 64e5-99f3-18f6
User access type        : 802.1x
User access interface   : Wlan-Dbss17496
Qinq vlan/User vlan     : 0/200
User IP address         : -
User IPV6 address       : -
User ID                 : 16450
User login time         : 2020/11/03 19:15:15
User online fail reason : Remote user is blocked
Authen reply message    : -
User name to server     : test
AP ID                   : 0
Radio ID                : 0
AP MAC                  : 18de-d777-c120
SSID                    : dot1x_test
----------------------------------------------------------------
```

认证账号被锁定原因为该账号在一段时间内连续认证失败次数过多，需要确认认证账号被锁定之前多次认证失败原因，该失败原因需要在RADIUS服务器侧排查。

有一种场景需要特别注意，即所有终端使用相同账号认证接入，如果有一个终端使用了错误的密码，导致该账号被锁定，会导致所有终端均无法接入，该场景下需要关闭远端账号锁定功能。

接入用户远端认证失败后账号锁定功能默认关闭。

查看远端账号是否被锁定命令：

```text
[HUAWEI] display remote-user authen-fail blocked
Interval: Retry Interval(Mins)
TimeLeft: Retry Time Left
BlockDuration: Block Duration(Mins)
----------------------------------------------------------------
Username  Interval  TimeLeft  BlockDuration  BlockTime
----------------------------------------------------------------
test       0         0         5              2020-11-03 19:11:14+08:00
----------------------------------------------------------------
Total 1, 1 printed
```

解锁特定远端账号命令：

```text
[HUAWEI] aaa
[HUAWEI-aaa] remote-user authen-fail unblock username test
```

关闭接入用户远端认证失败后账号锁定功能：

```text
[HUAWEI] aaa
[HUAWEI-aaa] undo access-user remote authen-fail
```

### 1.1.2.5 终端MAC地址静默

在系统视图下执行命令trace object mac-address mac-address可以看到提示User is still in quiet status，说明终端处于静默状态。

```text
[BTRACE][2020/11/21 15:25:01][7177][EAPoL][000c-291a-4b03]:User is still in quiet status.(MAC:000c-291a-4b03)    //终端处于静默状态，报文被丢弃
[BTRACE][2020/11/21 15:25:01][7177][EAPoL][000c-291a-4b03]:Quiet table check failure,drop the packet.
```

可以执行命令display dot1x quiet-user all，查看用户MAC处于静默状态的剩余静默时间。

```text
[HUAWEI] display dot1x quiet-user all
---------------------------------------------------------------
MacAddress                      Quiet Remain Time(Sec)
---------------------------------------------------------------
000c-291a-4b03                  49
---------------------------------------------------------------
1 silent mac address(es) found, 1 printed.
```

该终端用户在60s内连续802.1X认证失败达到一定次数，需要确认认证账号前多次认证失败原因，等到用户MAC退出静默状态后再重新尝试。也可以在系统视图下执行命令dot1x timer quiet-period quiet-period-times调小802.1X用户被静默的时间。

```text
[HUAWEI] dot1x timer quiet-period 60
```

### 1.1.2.6 终端不响应EAP报文

- 终端不响应Request Identity

- 终端不响应Request Challenge

#### 1.1.2.6.1 终端不响应Request Identity

通过业务诊断功能，追踪终端用户上线认证过程，看到设备发出Request Identity报文后没有收到回应，超时后设备进行了重传：

```text
[HUAWEI] trace object mac-address 64e5-99f3-18f6
[HUAWEI] trace enable
[BTRACE][2020/11/02 14:22:45][6144][EAPoL][64e5-99f3-18f6]:Send a EAPoL request identity packet to user.
[BTRACE][2020/11/02 14:22:45][6144][EAPoL][64e5-99f3-18f6]:Add a Eap Packet Node to EAPOL Ucib, MAC is 64e5-99f3-18f6.
[BTRACE][2020/11/02 14:22:45][6144][EAPoL][64e5-99f3-18f6]:
EAPOL packet: OUT
64 e5 99 f3 18 f6 84 5b 12 69 22 e8 81 00 00 c8
88 8e 01 00 00 05 01 60 00 05 01
[BTRACE][2020/11/02 14:22:45][6144][EAPoL][64e5-99f3-18f6]:
802.1x packet:
Version:802.1X-2001(1); Type:Eap(0); Length:5
EAPOL packet:
Code:Request(1); Id:96; Length:5; Type:Identity(1)
[BTRACE][2020/11/02 14:22:45][6144][EAPoL][64e5-99f3-18f6]:Send EAP_request packet to user successfully.(Index=120)
[BTRACE][2020/11/02 14:22:45][6144][WLAN_AC][64e5-99f3-18f6]:[Process:6][WSTA] Process eapol start message up sucessfully.
[BTRACE][2020/11/02 14:22:45][6144][WLAN_AC][64e5-99f3-18f6]:[Process:6][WADP] Receive EAP authentication ack message from EAPOL(Value:0, Code:0, Current SN:159, Response SN:159).
[BTRACE][2020/11/02 14:22:45][6144][WLAN_AC][64e5-99f3-18f6]:[Process:6][WSTA] Sta table aging.
[BTRACE][2020/11/02 14:22:47][6144][EAPoL][64e5-99f3-18f6]:No response of request identity from user.
[BTRACE][2020/11/02 14:22:47][6144][EAPoL][64e5-99f3-18f6]:Resend a EAPoL request identity packet to user.
[BTRACE][2020/11/02 14:22:47][6144][EAPoL][64e5-99f3-18f6]:Add a Eap Packet Node to EAPOL Ucib, MAC is 64e5-99f3-18f6.
[BTRACE][2020/11/02 14:22:47][6144][EAPoL][64e5-99f3-18f6]:
EAPOL packet: OUT
64 e5 99 f3 18 f6 84 5b 12 69 22 e8 81 00 00 c8
88 8e 01 00 00 05 01 60 00 05 01
[BTRACE][2020/11/02 14:22:47][6144][EAPoL][64e5-99f3-18f6]:
802.1x packet:
Version:802.1X-2001(1); Type:Eap(0); Length:5
EAPOL packet:
Code:Request(1); Id:96; Length:5; Type:Identity(1)
[BTRACE][2020/11/02 14:22:47][6144][EAPoL][64e5-99f3-18f6]:Send EAP_request packet to user successfully.(Index=120)
```

如果是所有终端均存在该问题，则大概率可能是没有创建业务VLAN，需要创建业务VLAN（即使AC仅作为二层网络，不作为用户网关，也需要创建对应业务VLAN）。首选查看业务VLAN是否创建，如果没有创建，创建对应的业务VLAN。

查看业务VLAN是否创建（以业务VLAN 200为例）：

```text
[HUAWEI] display vlan summary
static vlan:
Total 12 static vlan exist(s).
1 10 12 100 111 to 112 999 1110 to 1114
dynamic vlan:
Total 0 dynamic vlan exist(s).
```

创建业务VLAN（以业务VLAN 200为例）：

```text
[HUAWEI] vlan 200
```

#### 1.1.2.6.2 终端不响应Request Challenge

通过业务诊断功能，追踪终端用户上线认证过程，看到设备发出Request Challeng报文没有收到回应，超时后设备进行了重传，超过重传次数后设备发送了Failure报文。

```text
[HUAWEI] trace object mac-address 64e5-99f3-18f6
[HUAWEI] trace enable
[BTRACE][2020/11/03 14:41:00][6144][EAPoL][64e5-99f3-18f6]:Eapol send authentication request challenge packet to user.
[BTRACE][2020/11/03 14:41:00][6144][EAPoL][64e5-99f3-18f6]:Add a Eap Packet Node to EAPOL Ucib, MAC is 64e5-99f3-18f6.
[BTRACE][2020/11/03 14:41:00][6144][EAPoL][64e5-99f3-18f6]:
EAPOL packet: OUT
64 e5 99 f3 18 f6 84 5b 12 69 22 e8 81 00 00 c8
88 8e 01 00 00 41 01 6c 00 41 19 00 14 03 01 00
01 01 16 03 01 00 30 85 17 ee 90 6c 84 62 9f 66
28 bb d7 29 2c e4 3f 44 dd 79 aa 10 54 3b 6d 54
ac 8e c8 6b a8 3f f7 cd 68 47 4f cc 9a a3 4e ba
0f b5 88 00 22 3e 0a
[BTRACE][2020/11/03 14:41:00][6144][EAPoL][64e5-99f3-18f6]:
802.1x packet:
Version:802.1X-2001(1); Type:Eap(0); Length:65
EAPOL packet:
Code:Request(1); Id:108; Length:65; Type:PEAP(25)
[BTRACE][2020/11/03 14:41:00][6144][EAPoL][64e5-99f3-18f6]:Send EAP_request packet to user successfully.(Index=122)
[BTRACE][2020/11/03 14:41:00][6144][EAPoL][64e5-99f3-18f6]:Eapol send request/challenge packet to user successfully.enter request status.(local index:122)
[BTRACE][2020/11/03 14:41:02][6144][EAPoL][64e5-99f3-18f6]:No response of request challenge from user.
[BTRACE][2020/11/03 14:41:02][6144][EAPoL][64e5-99f3-18f6]:Resend a EAPoL request challenge packet to user.
[BTRACE][2020/11/03 14:41:02][6144][EAPoL][64e5-99f3-18f6]:Add a Eap Packet Node to EAPOL Ucib, MAC is 64e5-99f3-18f6.
[BTRACE][2020/11/03 14:41:02][6144][EAPoL][64e5-99f3-18f6]:
EAPOL packet: OUT
64 e5 99 f3 18 f6 84 5b 12 69 22 e8 81 00 00 c8
88 8e 01 00 00 41 01 6c 00 41 19 00 14 03 01 00
01 01 16 03 01 00 30 85 17 ee 90 6c 84 62 9f 66
28 bb d7 29 2c e4 3f 44 dd 79 aa 10 54 3b 6d 54
ac 8e c8 6b a8 3f f7 cd 68 47 4f cc 9a a3 4e ba
0f b5 88 00 22 3e 0a
[BTRACE][2020/11/03 14:41:02][6144][EAPoL][64e5-99f3-18f6]:
802.1x packet:
Version:802.1X-2001(1); Type:Eap(0); Length:65
EAPOL packet:
Code:Request(1); Id:108; Length:65; Type:PEAP(25)
[BTRACE][2020/11/03 14:41:02][6144][EAPoL][64e5-99f3-18f6]:Send EAP_request packet to user successfully.(Index=122)
[BTRACE][2020/11/03 14:41:03][6144][WLAN_AC][64e5-99f3-18f6]:[Process:6][WSTA] Sta table aging.
[BTRACE][2020/11/03 14:41:03][2048][WLAN_AC][64e5-99f3-18f6]:[Process:2][WSTA] Flow fork MultiSta MsgType3101 Vcpu6
[BTRACE][2020/11/03 14:41:03][2048][WLAN_AC][64e5-99f3-18f6]:[Process:2][WSTA] Flow fork MultiSta MsgType3121 Vcpu6
[BTRACE][2020/11/03 14:41:04][6144][EAPoL][64e5-99f3-18f6]:No response of request challenge from user.
[BTRACE][2020/11/03 14:41:04][6144][EAPoL][64e5-99f3-18f6]:Resend a EAPoL request challenge packet to user.
[BTRACE][2020/11/03 14:41:04][6144][EAPoL][64e5-99f3-18f6]:Add a Eap Packet Node to EAPOL Ucib, MAC is 64e5-99f3-18f6.
[BTRACE][2020/11/03 14:41:04][6144][EAPoL][64e5-99f3-18f6]:
EAPOL packet: OUT
64 e5 99 f3 18 f6 84 5b 12 69 22 e8 81 00 00 c8
88 8e 01 00 00 41 01 6c 00 41 19 00 14 03 01 00
01 01 16 03 01 00 30 85 17 ee 90 6c 84 62 9f 66
28 bb d7 29 2c e4 3f 44 dd 79 aa 10 54 3b 6d 54
ac 8e c8 6b a8 3f f7 cd 68 47 4f cc 9a a3 4e ba
0f b5 88 00 22 3e 0a
[BTRACE][2020/11/03 14:41:04][6144][EAPoL][64e5-99f3-18f6]:
802.1x packet:
Version:802.1X-2001(1); Type:Eap(0); Length:65
EAPOL packet:
Code:Request(1); Id:108; Length:65; Type:PEAP(25)
[BTRACE][2020/11/03 14:41:04][6144][EAPoL][64e5-99f3-18f6]:Send EAP_request packet to user successfully.(Index=122)
[BTRACE][2020/11/03 14:41:06][6144][EAPoL][64e5-99f3-18f6]:No response of request challenge from user.
[BTRACE][2020/11/03 14:41:06][6144][EAPoL][64e5-99f3-18f6]:Resend EAP_request/identity times exceed max times.(Index=122)
[BTRACE][2020/11/03 14:41:06][6144][EAPoL][64e5-99f3-18f6]:Send EAP-Failure packet to user.
[BTRACE][2020/11/03 14:41:06][6144][EAPoL][64e5-99f3-18f6]:Add a Eap Packet Node to EAPOL Ucib, MAC is 64e5-99f3-18f6.
[BTRACE][2020/11/03 14:41:06][6144][EAPoL][64e5-99f3-18f6]:
EAPOL packet: OUT
64 e5 99 f3 18 f6 84 5b 12 69 22 e8 81 00 00 c8
88 8e 01 00 00 04 04 6c 00 04
[BTRACE][2020/11/03 14:41:06][6144][EAPoL][64e5-99f3-18f6]:
802.1x packet:
Version:802.1X-2001(1); Type:Eap(0); Length:4
EAPOL packet:
Code:Failure(4); Id:108; Length:4; Type:Unknown(0)
```

终端不响应Request Challenge排查步骤如下：

1. 首先在AC上采集station-trace信息（station-trace信息记录的是AP收发EAP报文情况）。

```text
[HUAWEI-diagnose] station-trace sta-mac 64e5-99f3-18f6
```

2. 按顺序确认以下四个信息：

<7>Nov 03 2020 14:40:58.20.1 AP-10 WSRV/7/BTRACE:(BTRACE)(WLAN_AP)(64e5-99f3-18f6):receive eap pkt to sta from CAPWAP(9),[type(0)=EAP pkt, src mac=84:5b:12:69:22:e8, len=1122]

<7>Nov 03 2020 14:40:58.20.2 AP-10 WIFI/7/BTRACE:[BTRACE][WLAN_WIFI][64E5-99F3-18F6]:SeqNo[28] [EAPOL] EAPOL packet payload[1100] Recved from software switch  //AP收到AC发送的EAP Request challenge报文

<7>Nov 03 2020 14:40:58.20.3 AP-10 WIFI/7/BTRACE:[BTRACE][WLAN_WIFI][64E5-99F3-18F6]:SeqNo[28] [EAPOL] EAPOL packet payload[1100] elapsed[0 ms] Sending pkt to target(Single)

<7>Nov 03 2020 14:40:58.70.1 AP-10 WIFI/7/BTRACE:[BTRACE][WLAN_WIFI][64E5-99F3-18F6]:SeqNo[28] [EAPOL] EAPOL packet payload[1100] elapsed[30 ms] Success to send pkt to air  //AP向终端发送EAP Request challenge报文

<7>Nov 03 2020 14:40:58.70.2 AP-10 WIFI/7/BTRACE:[BTRACE][WLAN_WIFI][64E5-99F3-18F6]:SeqNo[29] [EAPOL] EAPOL packet payload[6] Recved from target  //AP收到终端发送的EAP Response challenge报文

```text
<7>Nov 03 2020 14:40:58.70.3 AP-10 WIFI7/BTRACE:[BTRACE][WLAN_WIFI][64E5-99F3-18F6]:SeqNo[29] [EAPOL] EAPOL packet payload[6] elapsed[0 ms] Entering rx reorder
```

<7>Nov 03 2020 14:40:58.70.4 AP-10 WIFI/7/BTRACE:[BTRACE][WLAN_WIFI][64E5-99F3-18F6]:SeqNo[29] [EAPOL] EAPOL packet payload[6] elapsed[0 ms] Exiting rx reorder for release

<7>Nov 03 2020 14:40:58.70.5 AP-10 WIFI/7/BTRACE:[BTRACE][WLAN_WIFI][64E5-99F3-18F6]:SeqNo[29] [EAPOL] EAPOL packet payload[6] elapsed[0 ms] Success to send pkt to software switch  //AP向AC发送EAP Response challenge报文

<7>Nov 03 2020 14:40:58.70.6 AP-10 WSRV/7/BTRACE:(BTRACE)(WLAN_AP)(64e5-99f3-18f6):receive eap pkt from sta by BSS(26),[type(0)=EAP pkt, dest mac=18:de:d7:77:c1:20, len=28]

  a. AP是否收到AC发送的EAP Request challenge报文。

根据station-trace，确认AP是否收到AC发送的EAP Request challenge请求报文（Recved from software switch）。如果AP没有收到AC发送的EAP Request challenge请求报文，可首先在AP上开启转发debug，看AP转发有没有收到，如果AP转发没有收到，再在AC上开启转发debug，看AC转发有没有发送，如果确认AP转发接收和AC转发发送都没有问题，则需要在中间链路抓包，可能被中间链路丢弃。

  b. AP收到后是否将EAP Request challenge报文发送给终端。

根据station-trace，确认AP是否成功将EAP Request challenge报文发送给终端（Success to send pkt to air）。

  c. AP是否收到终端EAP Response challenge报文。

根据station-trace，确认AP是否收到终端发送的EAP Response challenge报文（Recved from target）。

  d. AP是否将EAP Response challenge报文发送给AC。

根据station-trace，确认AP是否成功将EAP Response challenge报文发送给AC（Success to send pkt to software switch）。如果station-trace显示发送成功，但AC没有收到，可首先在AC上开启转发debug，看AC转发有没有收到，如果AC转发没有收到，再在AP上开启转发debug，看AP转发有没有发送，如果确认AC转发接收和AP转发发送都没有问题，则需要在中间链路抓包，可能被中间链路丢弃。

3. 还有一个可能原因，RADIUS服务器发送的Access-challenge报文中EAP内容比较大（长度都超过1200），导致终端接收大的EAP Request challenge报文失败，可在station-trace中确认。

```text
[G12-AP-09-3-diagnose]
May 13 2019 17:28:10.230.6+00:00 G12-AP-09-3 WSRV/7/BTRACE:[BTRACE][WLAN_AP][3C2E-FF90-662F]:receive eap pkt to sta from CAPWAP(23),[type(0)=EAP pkt, src mac=10:c1:72:90:85:e6, len=1518]
[G12-AP-09-3-diagnose]
May 13 2019 17:28:10.230.7+00:00 G12-AP-09-3 WIFI/7/BTRACE:[BTRACE][WLAN_WIFI][3C2E-FF90-662F]:SeqNo[3259] [EAPOL] EAPOL packet payload[1496] Recved from software switch
[G12-AP-09-3-diagnose]
May 13 2019 17:28:10.230.8+00:00 G12-AP-09-3 WIFI/7/BTRACE:[BTRACE][WLAN_WIFI][3C2E-FF90-662F]:SeqNo[3259] [EAPOL] EAPOL packet payload[1496] elapsed[0 ms] Sending pkt to target(Single)
[G12-AP-09-3-diagnose]
May 13 2019 17:28:10.240.1+00:00 G12-AP-09-3 WIFI/7/BTRACE:[BTRACE][WLAN_WIFI][3C2E-FF90-662F]:SeqNo[3259] [EAPOL] EAPOL packet payload[1496] elapsed[0 ms] Fail to send pkt to air with status[2]
```

如上所示，EAP Request challenge报文长度为1496，AP发送给终端失败，该问题有两种解决方式

  - 在RADIUS服务器上调整Frame-Mtu大小为1000以下。

  - 可尝试在radius-server模板下降低设备发送给RADIUS服务器认证请求报文中Frame-Mtu属性值，Frame-Mtu属性值默认为1500，可将其调整为1000。

部分第三方RADIUS服务器不支持该属性，只能采用第一种方式去调整。

```text
[HUAWEI] radius-server template radius_test
[HUAWEI-radius-radius_test] radius-server attribute translate
[HUAWEI-radius-radius_test] radius-attribute set Framed-Mtu 1000
```

### 1.1.2.7 四步握手失败

在系统视图下执行命令trace object mac-address mac-address可以看到提示4-way-handshake failed，说明四步握手失败。

```text
[BTRACE] [2020/11/30 11:56:42][3072][WLAN_AC][0433-c2ad-9008]:[Process:3][WSTA] Receive elb table process(Ap:22, radio:1, wlan:1, vlan:1199, access mode:0, L3:0, version:0, IP:00000000, code:0, type:2)
[BTRACE][2020/11/30 11:56:42][6144][WLAN_AC][0433-c2ad-9008]:[Process:6][WSEC] 4-way-handshake failed (Code:00000003).
```

四步握手失败一般是由于空口环境干扰大/终端信号弱引起的，此时建议排查WLAN空口环境，可以联系技术支持人员查看。

### 1.1.2.8 认证成功后定时做重认证

出现上述情况，可能原因如下：

#### 设备本地配置了重认证

检查接入模板下有没有配置dot1x reauthenticate命令。如果有，请删除该配置。

```text
[HUAWEI] dot1x-access-profile name access_dot1x
[HUAWEI--dot1x-access-profile-access_dot1x] display this
#
dot1x-access-profile name access_dot1x
dot1x reauthenticate
#
```

#### RADIUS服务器错误下发Session-Timeout和Termination-Action属性

通过业务诊断功能，追踪终端用户上线认证过程，查看RADIUS服务器下发的授权内容。

如下所示trace中，显示RADIUS服务器在认证成功报文中下发了Session-Timeout和Termination-Action属性。

```text
[HUAWEI] trace object mac-address 64e5-99f3-18f6
[HUAWEI] trace enable
[BTRACE][2020/10/24 16:48:14][6144][RADIUS][64e5-99f3-18f6]:
Received a authentication accept packet from radius server(server ip = 12.12.12.1).
[BTRACE][2020/10/24 16:48:14][6144][RADIUS][64e5-99f3-18f6]:
Server Template: 4
Server IP   : 12.12.12.1
Server Port : 1812
Protocol: Standard
Code    : 2
Len     : 194
ID      : 194
[Session-Timeout                ] [6 ] [3600]
[Termination-Action             ] [6 ] [1]
[EAP-Message                        ] [6 ] [03 4a 00 04 ]
[State                              ] [16] [\001uY\311\025N]
[MS-MPPE-Send-Key                   ] [52] [fb a1 e9 55 16 62 a3 e5 da 35 fc ce 3e 8f ae 7d ac 0a d6 0b 20 59 ad 82 a8 66 88 06 6a 81 10 82 61 95 2e cf 44 50 c0 79 e5 3f a4 32 43 45 a5 9e 2b c4 ]
[MS-MPPE-Recv-Key                   ] [52] [fb a1 e9 65 b1 18 6d 60 8f 0a ed af 53 1e 26 8a e6 18 9d 26 8c 21 c8 4f c2 8a 6a d5 a8 85 8a 9d ba d8 be 8d 97 b8 b8 d3 24 04 21 23 90 71 33 35 f4 6b ]
[Message-Authenticator              ] [18] [00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ]
```

可以修改RADIUS服务器上的授权策略，将对应授权内容删除。

也可以在设备通过配置忽略对应的授权内容，配置命令如下：

```text
[HUAWEI] radius-server template radius_test
[HUAWEI-radius-radius_test] radius-server attribute translate
[HUAWEI-radius-radius_test] radius-attribute disable Termination-Action receive
[HUAWEI-radius-radius_test] radius-attribute disable Session-Timeout receive
```