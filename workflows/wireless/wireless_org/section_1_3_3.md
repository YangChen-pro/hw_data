# 1.3.3 Portal协议外置Portal认证失败常见问题

Portal认证页面提示认证失败

页面显示认证成功，但访问网络又弹出Portal认证页面

页面在认证成功页面和推送页面之间反复跳转

PC无线终端认证成功后关闭认证页面，一段时间后访问网页又弹出Portal认证页面

## 1.3.3.1 Portal认证页面提示认证失败

设备未收到Portal服务器认证请求报文

设备Portal服务器模板下配置的共享密钥和服务器不一致

设备支持的Portal版本与服务器不兼容

设备Portal服务器模板下配置的server-ip与设备收到Portal报文源IP地址不一致

终端与Portal服务器之间存在NAT

RADIUS服务器认证拒绝

RADIUS服务器不响应

RADIUS服务器授权数据失败

### 1.3.3.1.1 设备未收到Portal服务器认证请求报文

通过业务诊断功能，追踪终端用户上线认证过程，看到没有收到任何挑战或认证请求的输出：

```text
[HUAWEI] trace object ip-address 196.1.1.65
[HUAWEI] trace enable
```

通采集debugging信息，也有同样的现象：

```text
<HUAWEI> debugging web all
<HUAWEI> terminal debugging
<HUAWEI> terminal monitor
<HUAWEI> debugging timeout 0
```

当设备收到Portal挑战请求或者认证请求时，会有如下trace信息：

```text
[BTRACE][2023-09-14 21:33:05][0][WEB][196.1.1.65]:Web receive challenge-req from portal server. (ip:196.1.1.65, vrf:0, sn:1134, reqId:0)
[BTRACE][2023-09-14 21:33:05][0][WEB][196.1.1.65]:Web receive challenge-req request packet from portal server. (ReqID:0)
```

如果设备没收到Portal挑战请求和认证请求，请按照如下步骤排查确认：

1. 确认设备的监听端口是否进行了变更，默认的端口号是2000。

```text
[HUAWEI] display web-auth-server configuration
 Listening port           : 2000
 Portal                   : version 1, version 2, version 3
 Include reply message    : enabled
 Server-Source            : all-interface
```

2. 根据测试终端MAC地址查询终端接入的Process，再查询该Process下Portal报文计数，看Portal挑战请求或者认证请求或错误报文计数是否增加。

  a. 根据测试终端MAC地址查询终端接入的Process。

```text
[HUAWEI] diagnose
[HUAWEI-diagnose] display access-user mac-address 04f9-f8da-bc5e
 Total: 1
 process  4:
 ------------------------------------------------------------------------------
Basic:
  User ID                         : 16513
  User name                       : portal
  Domain-name                     : -
  User MAC                        : 04f9-f8da-bc5e
  User IP address                 : 196.1.1.65
  User vlan event                 : Pre-authen
  QinQVlan/UserVlan               : 0/92
  User vlan source                : user request
  User access time                : 2023/09/14 21:33:06
  User access type                : None
  AP name                         : 9700s-23.188-ap
  Radio ID                        : 0
  AP MAC                          : acdc-cae4-4550
  WLAN ID                         : 1
  SSID                            : portal-yunshan-2.196
  Online time                     : 1651(s)
  Service Scheme Priority         : 0
AAA:
  User authentication type        : None
  Current authentication method   : None
  Current authorization method    : Local
  Current accounting method       : None
 ------------------------------------------------------------------------------
Total: 1, printed: 1
```

  b. 查询该Process下Portal报文计数。

```text
[HUAWEI-diagnose] display web statistics packet process 4
process  4:
  Packet error Total       : 0
  Challenge req error      : 0
  Auth req error           : 0
  Logout req error         : 0
  Info req error           : 0
  Auth ntf error           : 0
  Discover req error       : 0
  IPChange ack error       : 0
  Cut ack  error           : 0
  Recv auth req            : 0
  Recv Auth ntf            : 0
  Recv Logout req          : 0
  Recv Challenge req       : 0
```

如果挑战请求报文、认证请求报文、错误报文计数均为0，则表明没有收到Portal服务器发送的报文。

3. 上述根据报文计数就可以确认是否收到Portal服务器报文，如果需要进一步确认是否收到报文，还可以通过在设备连接Portal服务器的出接口抓包进行确认。

设备收不到Portal服务器报文问题有如下几种可能原因：

- Portal服务器无法找到设备。终端访问Portal服务器页面，输入账号密码后，Portal服务器根据终端IP地址信息无法识别该终端从哪台设备接入。

Portal服务器无法找到设备有如下可能原因：

  - Portal服务器上没有添加设备IP。

需要Portal服务器侧确认是否添加设备IP。

  - Portal服务器需要在终端访问Portal服务器认证页面时携带终端用户IP地址或者设备地址信息。

此时需要在URL模板下配置URL参数，配置命令如下：

```text
[HUAWEI] url-template name url_test
[HUAWEI-url-template-url_test] url-parameter device-ip ac-ip user-ipaddress userip
```

其中device-ip后面配置的ac-ip或者user-ipaddress的具体名字需要根据Portal服务器要求配置，比如有的Portal服务器需要将device-ip配置为wlanacip，将user-ipaddress配置为wlanuserip。

设备携带的device-ip参数默认为capwap source的IP地址，如果Portal服务器上添加的设备IP地址不是capwap source的IP地址，需要通过命令修改device-ip的参数值（该参数值必须是设备可用的IP）：

```text
[HUAWEI] url-template name url_test
[HUAWEI-url-template-url_test] url-parameter set device-ip x.x.x.x
```

- 中间网络存在问题，如路由配置错误等。

- Portal服务器发送的目的端口号设置错误，默认Portal报文目的端口是2000，Portal服务器上修改了该目的端口。

### 1.3.3.1.2 设备Portal服务器模板下配置的共享密钥和服务器不一致

通过业务诊断功能，追踪终端用户上线认证过程，看到提示“Web 2.0 shared-key mismatch.”，可以确认设备Portal服务器模板下配置的共享密钥和服务器上配置不一致。

```text
[HUAWEI] trace object ip-address 196.1.1.142
[HUAWEI] trace enable
[BTRACE][2023-09-14 22:36:05][0][WEB][196.1.1.142]:Web 2.0 shared-key mismatch.
```

需要在Portal服务器模板和Portal服务器上重新配置共享密钥，使两者配置的共享密钥相同。

### 1.3.3.1.3 设备支持的Portal版本与服务器不兼容

通过业务诊断功能，追踪终端用户上线认证过程，看到提示“Web current version 2 does not support.”或“Web current version 1 does not support.”，可以确认设备配置的Portal协议版本不支持Portal服务器发送的Portal报文使用的Portal协议版本。

```text
<HUAWEI> debugging web all
<HUAWEI> terminal debugging
<HUAWEI> terminal monitor
<HUAWEI> debugging timeout 0
<HUAWEI> system
[HUAWEI] trace object ip-address 196.1.1.142
[HUAWEI] trace enable
[BTRACE][2023-09-14 23:01:40][0][WEB][196.1.1.142]:Web current version 2 does not support.
```

需要在设备上配置Portal协议版本支持Portal服务器发送的Portal报文使用的Portal协议版本，或者恢复设备支持的Portal协议版本为缺省配置（缺省情况下，设备同时支持v3、v2与v1版本），执行如下两条命令均可：

配置设备支持的Portal协议版本为v3、v2和v1：

```text
[HUAWEI] web-auth-server version v3 v2 v1
```

恢复设备支持的Portal协议版本为缺省配置

```text
[HUAWEI] undo web-auth-server version
```

### 1.3.3.1.4 设备Portal服务器模板下配置的server-ip与设备收到Portal报文源IP地址不一致

通过业务诊断功能，追踪终端用户上线认证过程，看到“Get web item by ip failed. (server-ip:x.x.x.x)”，可以确认设备收到的Portal报文的源IP地址不在设备配置的server-ip列表里：

```text
<HUAWEI> debugging web all
<HUAWEI> terminal debugging
<HUAWEI> terminal monitor
<HUAWEI> debugging timeout 0
Sep 16 2023 18:54:02.472 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x96;
[Web-Msg][slot: 0, process: nac_main]Web hrp receive portal protocol packet ok. (rcvLen:32).
Sep 16 2023 18:54:02.472 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x96;
[Web-Msg][slot: 0, process: nac_main]Web normal socket msg. (msg type:1).
Sep 16 2023 18:54:02.472 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x96;
[Web-Msg][slot: 0, process: nac_main]Get web item by ip failed. (server-ip:172.94.2.96)
Sep 16 2023 18:54:02.472 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_ERROR(d):CID=0x96;
[Web-Err][slot: 0, process: nac_main]WEB GetClearPswbyServerIpVrf, Get server index error. (server ip:172.94.2.96, vrf:0)
```

确认Portal服务器实际地址与收到报文的源IP地址是否一致：

- 如果一致，则表明是设备上配置的server-ip错误，需要修改设备Portal服务器模板下server-ip配置。

- 如果Portal服务器实际地址与收到报文的源IP地址不一致，则可能是Portal服务器与设备之间存在NAT，将Portal报文源IP地址做了修改。如果设备与Portal服务器之间的NAT可以删除，则建议删除NAT，如果不能删除，需要修改设备Portal服务器模板下server-ip配置。

### 1.3.3.1.5 终端与Portal服务器之间存在NAT

通过业务诊断功能（根据用户IP地址），追踪终端用户上线认证过程，但无任何打印。通过debugging web all或服务器抓包，可以看到收到Portal服务器请求报文中的IP地址不是终端实际IP地址。

[Web-Msg][slot: 0, process: nac_svc1]Web hrp receive portal protocol packet ok. (rcvLen:38).

[Web-Msg][slot: 0, process: nac_svc1]Web normal socket msg. (msg type:5).

[Web-Msg][slot: 0, process: nac_svc1]Web check authenticator. (version:2, cmpResult:0)

[Web-Msg][slot: 0, process: nac_svc1]Web check packet, finish.

[Web-Msg][slot: 0, process: nac_svc1]Web get user mac from arp db. (user-ip:2891842145, user-mac=286e-d489-20cf)

[Web-Evt][slot: 0, process: nac_svc1]WEB Failed to get IP from if interface, user is in direct network. (IfIndex:4294967295)

[Web-Msg][slot: 0, process: nac_svc2]Web packet dispatch get user info. (ipv4:172.94.2.97, type:5)

[Web-Msg][slot: 0, process: nac_svc2]Web packet dispatch get user info by ipv4. (pevlan:0, cevlan:0, l2if:0, mac:286e-d489-20cf)

```text
[HUAWEI] display access-user
 Total: 1
 ------------------------------------------------------------------------------------------------------
 UserID  Username               IP address                               MAC            Status
 ------------------------------------------------------------------------------------------------------
 16516   portal                 196.1.1.142                              04f9-f8da-bc5e Pre-authen
 ------------------------------------------------------------------------------------------------------
```

可以确认终端与Portal服务器之间NAT，终端访问Portal服务器时源IP地址已经被NAT转换，因此Portal服务器仅能感知到终端被NAT转换后的IP地址，无法感知到终端实际IP地址。此种情况下需要在URL模板下携带终端IP地址参数。

```text
[HUAWEI] url-templat name url_portal
[HUAWEI-url-template-url_portal] url-parameter user-ipaddress userip
```

### 1.3.3.1.6 RADIUS服务器认证拒绝

通过命令display aaa online-fail-record mac-address H-H-H查看终端上线失败记录，用户上线失败原因（User online fail reason）显示Radius authentication reject。

```text
[HUAWEI] display aaa online-fail-record mac-address 04f9-f8da-bc5e
  ------------------------------------------------------------------------------
  User name               : portal
  Domain name             : 2.96
  User MAC                : 04f9-f8da-bc5e
  User access type        : Web
  Qinq vlan/User vlan     : 0/92
  User IP address         : 196.1.1.142
  User IPV6 address       : -
  User ID                 : 16516
  User login time         : 2023/09/15 15:05:38
  User online fail reason : Radius authentication reject
  Authen reply message    : Rejected
  User name to server     : portal
  AP ID                   : 0
  Radio ID                : 0
  WLAN ID                 : 1
  AP MAC                  : acdc-cae4-4550
  SSID                    : portal-yunshan-2.196
  ------------------------------------------------------------------------------
```

通过业务诊断功能，追踪终端用户上线认证过程，看到RADIUS服务器回应了拒绝报文：

```text
[HUAWEI] trace object mac-address 04f9-f8da-bc5e
[HUAWEI] trace enable
[BTRACE][2023-09-15 15:05:38][0][AAA][04f9-f8da-bc5e]:
 AAA receive AAA_RD_MSG_AUTHENREJECT message(51) from RADIUS module(6).
[BTRACE][2023-09-15 15:05:38][0][AAA][04f9-f8da-bc5e]:
    CID:23  TemplateNo:20  SerialNo:4294967295
    SrcMsg:AAA_RD_MSG_AUTHENREQ
    PriyServer::: Vrf:0
    SendServer::: Vrf:0
    SessionTimeout:0 IdleTimeout:0
    AcctInterimInterval:0 RemanentVolume:0
    InputPeakRate:0 InputAverageRate:0
    OutputPeakRate:0 OutputAverageRate:0
    InputBasicRate:0 OutputBasicRate:0
    InputPBS:0 OutputPBS:0
    Priority:[0,0] DNS:[0.0.0.0, 0.0.0.0]
    ServiceType:0 LoginService:0 AdminLevel:0 FramedProtocol:0
    LoginIpHost:0 NextHop:0
    EapLength:0 ReplyMessage:Rejected
    TunnelType:0 MediumType:0 PrivateGroupID:
    WlanReasonCode:0
[BTRACE][2023-09-15 15:05:38][0][AAA][04f9-f8da-bc5e]:Radius authentication is rejected.
[BTRACE][2023-09-15 15:05:38][0][AAA][04f9-f8da-bc5e]:
 [AAA ERROR]authen finish,the authen fail code is:6,reason is:Radius authentication is rejected.
```

服务器回应认证拒绝有多种原因，最常见的有用户名密码错误、授权策略无法匹配等，这些问题需要首先通过排查服务器日志找到根因后，再调整服务器、终端或设备配置解决。

### 1.3.3.1.7 RADIUS服务器不响应

通过命令display aaa online-fail-record mac-address H-H-H查看终端上线失败记录，用户上线失败原因（User online fail reason）显示The radius server is up but has no reply或者The radius server is not reachable。

```text
[HUAWEI] display aaa online-fail-record mac-address 04f9-f8da-bc5e
  ------------------------------------------------------------------------------
  User name               : portal
  Domain name             : 2.96
  User MAC                : 04f9-f8da-bc5e
  User access type        : Web
  Qinq vlan/User vlan     : 0/92
  User IP address         : 196.1.1.142
  User IPV6 address       : -
  User ID                 : 16516
  User login time         : 2023/09/15 15:19:01
  User online fail reason : The radius server is up but has no reply
  Authen reply message    : Authentication fail
  User name to server     : portal
  AP ID                   : 0
  Radio ID                : 0
  WLAN ID                 : 1
  AP MAC                  : acdc-cae4-4550
  SSID                    : portal-yunshan-2.196
  ------------------------------------------------------------------------------
[HUAWEI] display aaa online-fail-record mac-address 04f9-f8da-bc5e
  ------------------------------------------------------------------------------
  User name               : portal
  Domain name             : 2.96
  User MAC                : 04f9-f8da-bc5e
  User access type        : Web
  Qinq vlan/User vlan     : 0/92
  User IP address         : 196.1.1.142
  User IPV6 address       : -
  User ID                 : 16516
  User login time         : 2023/09/15 14:53:46
  User online fail reason : The radius server is not reachable
  Authen reply message    : Authentication fail
  User name to server     : portal
  AP ID                   : 0
  Radio ID                : 0
  WLAN ID                 : 1
  AP MAC                  : acdc-cae4-4550
  SSID                    : portal-yunshan-2.196
  ------------------------------------------------------------------------------
```

通过业务诊断功能，追踪终端用户上线认证过程，看到RADIUS服务器无响应：

```text
[HUAWEI] trace object mac-address 04f9-f8da-bc5e
[HUAWEI] trace enable
[BTRACE][2023-09-15 15:19:01][0][AAA][04f9-f8da-bc5e]:
 AAA receive AAA_RD_MSG_SERVERNOREPLY message(61) from RADIUS module(6).
[BTRACE][2023-09-15 15:19:01][0][AAA][04f9-f8da-bc5e]:
    CID:25  TemplateNo:6  SerialNo:4294967295
    SrcMsg:AAA_RD_MSG_AUTHENREQ
    PriyServer::: Vrf:0
    SendServer::: Vrf:0
[BTRACE][2023-09-15 15:19:01][0][AAA][04f9-f8da-bc5e]:Radius server is up but no response.
[BTRACE][2023-09-15 15:19:01][0][AAA][04f9-f8da-bc5e]:
 [AAA ERROR]authen finish,the authen fail code is:8,reason is:Radius server is up but no response.
[BTRACE][2023-09-15 14:53:46][0][AAA][04f9-f8da-bc5e]:
 AAA receive AAA_RD_MSG_SERVERNOREPLY message(61) from RADIUS module(6).
[BTRACE][2023-09-15 14:53:46][0][AAA][04f9-f8da-bc5e]:
    CID:22  TemplateNo:15  SerialNo:4294967295
    SrcMsg:AAA_RD_MSG_AUTHENREQ
    PriyServer::: Vrf:0
    SendServer::: Vrf:0
[BTRACE][2023-09-15 14:53:46][0][AAA][04f9-f8da-bc5e]:Radius authentication has no response.
[BTRACE][2023-09-15 14:53:46][0][AAA][04f9-f8da-bc5e]:
 [AAA ERROR]authen finish,the authen fail code is:7,reason is:Radius authentication has no response.
```

RADIUS服务器不响应问题排查步骤如下：

1. 确认RADIUS服务器是否正确添加设备IP。

RADIUS服务器如果没有添加设备IP地址则需要添加正确的设备IP。

2. 如果RADIUS服务器已经添加设备IP地址，需要确认添加的设备IP与设备发送RADIUS认证请求报文的源IP是否相同。

设备发送RADIUS认证请求报文的源IP可通过命令配置，如果没有通过命令配置，则使用路由出接口IP地址。如果RADIUS服务器上添加的设备IP地址与路由出接口IP地址一致，则不需要在设备上配置与RADIUS服务器通信的源IP地址，否则需要通过命令配置源IP地址。

  a. 先根据RADIUS服务器IP地址查找路由表获取出接口，然后再根据出接口确认IP地址，如果RADIUS服务器添加的设备IP地址与路由出接口地址一致，则不需要再通过命令配置与RADIUS服务器通信的源IP地址。

```text
[HUAWEI] display ip routing-table 196.1.1.1
Proto: Protocol        Pre: Preference
Route Flags: R - relay, D - download to fib, T - to vpn-instance, B - black hole route
------------------------------------------------------------------------------
Routing Table : _public_
Summary Count : 1
Destination/Mask    Proto   Pre  Cost        Flags NextHop                                  Interface
      196.1.1.1/32  Direct  0    0             D   127.0.0.1                                Vlanif92
[HUAWEI] interface Vlanif 92
[HUAWEI-Vlanif92] display this
#
interface Vlanif92
 ip address 196.1.1.1 255.255.255.0
#
```

  b. 如果RADIUS服务器添加的设备IP地址与路由出接口地址不同，则需要在RADIUS服务器模板下配置与RADIUS服务器通信的源IP地址。

查看RADIUS服务器模板是否配置与RADIUS服务器通信的源IP地址：

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

在RADIUS模板下配置与RADIUS服务器通信源IP地址：

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
 ------------------------------------------------------------------------------
  STState    = STState-up
  STChgTime  = -
  ServerId   = 1
  Type       = auth-server
  State      = state-up
  AlarmFlag  = false
  STUseNum   = 1
  IPAddress  = 10.10.10.76
  AlarmTimer = 0xffffffff
  Head       = 4129
  Tail       = 4383
  ProbeID    = 255
  SourceIp   = ::
  LoopBack   = -
  Vlanif     = -
  Vrf        = -
  ServerId   = 0
  Type       = acct-server
  State      = state-up
  AlarmFlag  = false
  STUseNum   = 1
  IPAddress  = 10.10.10.76
  AlarmTimer = 0xffffffff
  Head       = 4129
  Tail       = 4383
  ProbeID    = 255
  SourceIp   = ::
  LoopBack   = -
  Vlanif     = -
  Vrf        = -
 ------------------------------------------------------------------------------
```

5. 确认设备与RADIUS服务器配置的共享密钥（shared-key）是否一致。可以通过test-aaa命令测试，同时开启radius debug打印，debug信息中如出现“Authenticator error·”则表示设备与RADIUS服务器配置的共享密钥不一致，需要同时修改设备与RADIUS服务器上共享密钥，使其相同。

```text
[HUAWEI] test-aaa test test radius-template radius_test
[RDS(Err):] Receive a illegal packet(Authenticator error), please check share key config.(ip:10.10.10.76 port:1812)
```

设备支持在全局下配置指定RADIUS服务器的共享密钥及在RADIUS服务器模板下配置共享密钥，其中全局下的配置优先级高于模板下的配置.

建议在RADIUS服务器模板下配置共享密钥，如果两个都配置的条件下，建议删除全局下的配置，仅保留模板下的配置。

RADIUS服务器模板下配置共享密钥：

```text
[HUAWEI] radius-server template radius_test
[HUAWEI-radius-radius_test] radius-server shared-key cipher HUAWEI@123
```

全局下配置RADIUS服务器共享密钥：

```text
[HUAWEI] radius-server ip-address 10.10.10.1 shared-key cipher HUAWEI@123
```

### 1.3.3.1.8 RADIUS服务器授权数据失败

通过命令display aaa online-fail-record mac-address H-H-H查看终端上线失败记录，用户上线失败原因（User online fail reason）显示Authorization data error。

```text
[HUAWEI] display aaa online-fail-record mac-address 04f9-f8da-bc5e
  ------------------------------------------------------------------------------
  User name               : portal
  Domain name             : 2.96
  User MAC                : 04f9-f8da-bc5e
  User access type        : Web
  Qinq vlan/User vlan     : 0/92
  User IP address         : 196.1.1.142
  User IPV6 address       : -
  User ID                 : 16520
  User login time         : 2023/09/15 19:06:23
  User online fail reason : Authorization data error
  Authen reply message    : Authentication fail
  User name to server     : portal
  AP ID                   : 0
  Radio ID                : 0
  WLAN ID                 : 1
  AP MAC                  : acdc-cae4-4550
  SSID                    : portal-yunshan-2.196
  ------------------------------------------------------------------------------
```

原因为RADIUS服务器授权了相关权限（如ACL），但设备上无对应的授权内容配置（如未创建授权ACL）。或者RADIUS服务器授权了VLAN，Portal认证不支持授权VLAN。

通过业务诊断功能，追踪终端用户上线认证过程，看到RADIUS服务器下发的授权内容：

```text
[HUAWEI] trace object mac-address 04f9-f8da-bc5e
[HUAWEI] trace enable
```

- 授权ACL检查失败

```text
[BTRACE][2023-09-15 19:06:23][0][RADIUS][04f9-f8da-bc5e]:
 Received a authentication accept packet from radius server(server ip = 172.94.2.96).
[BTRACE][2023-09-15 19:06:23][0][RADIUS][04f9-f8da-bc5e]:
  Template name: 2.96
  Server Template: 6
  Server IP   : 172.94.2.96
  Server Port : 1812
  Protocol: Standard
  Code    : 2
  Len     : 26
  ID      : 13
  [Filter-Id                          ] [6 ] [3027]
[BTRACE][2023-09-15 19:06:23][0][RADIUS][04f9-f8da-bc5e]:Send authentication reply message to AAA.
[BTRACE][2023-09-15 19:06:23][0][AAA][04f9-f8da-bc5e]:
 AAA receive AAA_RD_MSG_AUTHENACCEPT message(50) from RADIUS module(6).
[BTRACE][2023-09-15 19:06:23][0][AAA][04f9-f8da-bc5e]:
    CID:36  TemplateNo:6  SerialNo:4294967295
    SrcMsg:AAA_RD_MSG_AUTHENREQ
    PriyServer::: Vrf:0
    SendServer:172.94.2.96 Vrf:0
    SessionTimeout:0 IdleTimeout:0
    AcctInterimInterval:0 RemanentVolume:0
    InputPeakRate:0 InputAverageRate:0
    OutputPeakRate:0 OutputAverageRate:0
    InputBasicRate:0 OutputBasicRate:0
    InputPBS:0 OutputPBS:0
    Priority:[0,0] DNS:[0.0.0.0, 0.0.0.0]
    ServiceType:0 LoginService:0 AdminLevel:0 FramedProtocol:0
    LoginIpHost:0 NextHop:0
    EapLength:0 ReplyMessage:
    TunnelType:0 MediumType:0 PrivateGroupID:
    WlanReasonCode:0
[BTRACE][2023-09-15 19:06:23][0][AAA][04f9-f8da-bc5e]:Radius authorization data error.
[BTRACE][2023-09-15 19:06:23][0][AAA][04f9-f8da-bc5e]:
 [AAA ERROR]authen finish,the authen fail code is:16,reason is:Radius authorization data error.
```

授权ACL须知：无线场景下，授权ACL ID取值范围为3000-3031，ACL中rule id最大为64。

RADIUS服务器授权数据失败排查步骤如下：

1. 确认是否需要对应的授权。

  - 如果需要，则需要在设备上创建对应的授权内容，如授权VLAN需要在设备上创建对应VLAN；如授权ACL需要创建对应ACL，并且在ACL中配置相应规则。

  - 如果不需要，可以修改RADIUS服务器上的授权策略，将对应授权内容删除，也可以在设备通过配置忽略对应的授权内容，配置命令如下：

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

## 1.3.3.2 页面显示认证成功，但访问网络又弹出Portal认证页面

与Agile Controller服务器对接，终端用户在Portal认证页面输入用户名密码后显示认证成功，但访问其他网页时又弹出Portal认证页面，在设备上查看用户状态，仍然为Pre-authen状态。

该问题原因为Agile Controller服务器上没有配置接入终端IP地址列表，或者配置的接入终端IP地址列表与终端实际IP地址不一致

## 1.3.3.3 页面在认证成功页面和推送页面之间反复跳转

与Agile Controller服务器对接，终端用户在Portal认证页面输入用户名密码后显示认证成功，并自动跳转到认证成功后的推送页面，然后又转到认证成功页面，如此反复。在设备上查看用户状态，仍然为Pre-authen状态。

该问题原因同样是由于Agile Controller服务器上没有配置接入终端IP地址列表，或者配置的接入终端IP地址列表与终端实际IP地址不一致。导致现象不一致的原因是Agile Controller服务器上配置了认证成功后推送到指定页面。

## 1.3.3.4 PC无线终端认证成功后关闭认证页面，一段时间后访问网页又弹出Portal认证页面

PC无线终端Portal认证成功后，关闭认证页面，使用一段时间后，访问网页又重新弹出Portal认证页面，在设备上通过命令display aaa offline-record mac-address H-H-H查看终端上下线记录，下线原因为Web user request。

```text
[HUAWEI] display aaa offline-record mac-address 5cd9-98bc-034c
----------------------------------------------------------------
User name             : test
Domain name           : radius
User MAC              : 5cd9-98bc-034c
User access type      : Web
User access interface : Wlan-Dbss17498
Qinq vlan/User vlan   : 0/200
User IP address       : 200.1.1.64
User IPV6 address     : -
User ID               : 16614
User login time       : 2023/09/15 10:17:57
User offline time     : 2023/09/15 10:28:47
User offline reason   : Web user request
User name to server   : test
AP ID                 : 0
Radio ID              : 0
AP MAC                : 18de-d777-c120
SSID                  : portal_test
----------------------------------------------------------------
```

出现这种情况大概率是对接Agile Controller服务器时，无线接入终端Web认证会话超时时间没有启用兼容PC无线终端。解决方法就是在无线接入终端Web认证会话超时时间选项中启用兼容PC无线终端配置
