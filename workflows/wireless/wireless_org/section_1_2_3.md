# 1.2.3 HTTP协议外置Portal认证失败常见问题

Portal页面输入账号密码后，没有跳转到设备登录URL或跳转到错误的设备登录URL

Portal页面输入账号密码后跳转到设备登录URL，但显示超时

跳转到设备登录URL，提示安全告警

跳转到设备登录URL，但认证失败

## 1.2.3.1 Portal页面输入账号密码后，没有跳转到设备登录URL或跳转到错误的设备登录URL

### 问题现象

分别以Cisco ISE服务器和Aruba Clearpass服务器为例。

- Cisco ISE服务器：在Portal认证页面输入账号密码后点击登录，之后再点击继续，直接跳转到成功页面，没有看到跳转到设备登录URL，此时在设备上查看用户状态，仍然处于Pre-authen状态

- Aruba Clearpass服务器：在Portal认证页面输入账号密码后点击登录，但跳转的URL不是正确的设备登录URL。

### 问题原因

- 如果没有跳转到设备登录URL，其原因是Portal服务器不知道设备登录URL，没有配置设备登录URL。

- 如果跳转到错误的设备登录URL，原因是配置的设备登录URL错误。

### 解决方案

设备登录URL的配置依赖于Portal服务器，不同的Portal服务器配置方式不同，一般有两种方式：一种是直接在Portal服务器上配置设备登录URL；另一种是在设备上配置URL参数，在URL参数中携带设备登录URL。

- 方式一：在Portal服务器上配置设备登录URL。

Aruba Clearpass服务器是在服务器上直接配置设备登录URL，以该服务器为例，其他服务器需要服务器侧提供支持：

  1. 登录Aruba ClearPass服务器。

    a. 在浏览器中输入Aruba ClearPass的访问地址，地址格式为https://Aruba ClearPass IP，其中Aruba ClearPass IP是Aruba ClearPass服务器的IP地址。

    b. 选择“ClearPass Guest访客管理”。

    c. 在登录页面中，输入用户名和密码进行登录。

  2. 配置认证界面。

依次选择“配置 > Pages > 网页登录”，选择已经创建的网络登录页面，点击“编辑”进入编辑页面，在“提交URL”中设置设备登录URL。

- 方式二：在设备上通过URL参数配置设备登录URL。

Cisco ISE服务器是在设备上通过URL参数配置设备登录URL。

在设备URL模板下配置login-url参数：

```text
[HUAWEI] url-template name url_test
[HUAWEI-url-template-url_test] url-parameter login-url switch_url https://1.1.1.1:8443/login
```

设备登录URL格式为http(s)://ip:port/login，其中协议类型和端口号通过命令portal web-authen-server决定，IP地址为AC设备本机任一地址，后续需要通过免认证free-rule放通该地址，且要确保终端与该地址路由可达。

开启HTTP/HTTPS协议的Portal对接功能命令：

```text
[HUAWEI] portal web-authen-server https ssl-policy default_policy port 8443  //协议为https，端口号为8443
[HUAWEI] portal web-authen-server http port 8000  //协议为http，端口号为8000
```

## 1.2.3.2 Portal页面输入账号密码后跳转到设备登录URL，但显示超时

在Portal认证页面输入账号密码后，能够跳转到设备登录URL，但显示“无法访问此网站”，提示“ERR_CONNECTION_TIMED_OUT”。

该问题原因是终端与设备登录URL地址不通，按照如下步骤排查：

1. 排查设备是否通过free-rule放通设备登录URL对应的IP地址。

终端在访问设备登录URL时，终端还没有认证成功，所以需要在free-rule下放通设备登录URL对应的IP地址。

2. 排查终端与设备登录URL地址路由是否可达。

可在终端网关设备上使用网关地址作为源ping设备登录URL对应的IP地址，确认路由是否可达。如果路由不可达，需要排查路由配置。

## 1.2.3.3 跳转到设备登录URL，提示安全告警

在Portal认证页面输入账号密码登录后，能够跳转到设备登录URL，但提示安全告警，显示“您的连接不是私密连接”。

该问题原因是设备配置HTTPS协议的Portal对接，使用的证书是设备预置证书，不是合法机构颁发的证书，浏览器校验设备证书不合法。有如下两个方案：

- 使用HTTP协议的Portal对接。

- 购买合法证书，并导入到设备，设备登录URL不能直接使用IP地址，需要使用域名方式配置，同时需要DNS服务器配合能够解析该设备登录URL域名。

本地证书里面字段必须要包含有“使用者可选名称”，值为“DNS Name=客户用的域名”，否则还会提示安全证书有问题。

## 1.2.3.4 跳转到设备登录URL，但认证失败

### 终端使用get方式提交，但设备不支持

终端提交的用户名密码请求中未携带用户名或密码，或用户名密码的识别关键字不匹配

RADIUS服务器认证拒绝

RADIUS服务器不响应

RADIUS服务器授权数据失败

终端与设备之间存在NAT

### 1.2.3.4.1 终端使用get方式提交，但设备不支持

通过debugging web all，可以看到收到终端get请求，显示“Not permit http GET method.(method=0)”。

```text
Sep 16 2023 10:11:06.632 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]HttpAgt send mesh msg len=140
Sep 16 2023 10:11:06.633 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]HttpAgtProcQueueMeshMsg sendMsg len=140
Sep 16 2023 10:11:06.633 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]Recive http request mesh msg. (http_ctxid=0, http_cbid=4, need_lb=0, method=3, client=0XC401018E:16328, server=0XC2010101:6550, fd=195)
Sep 16 2023 10:11:06.633 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]Get user access ifindex 1627389953 by ip 0XC401018E & vrf 0.
Sep 16 2023 10:11:06.634 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_EVENT(d):CID=0x5c;
[Web-Evt][slot: 0, process: nac_svc1]web get active svrIndex is 0, userIfIndex is 1627389953.
Sep 16 2023 10:11:06.634 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_ERROR(d):CID=0x5c;
[Web-Err][slot: 0, process: nac_svc1][HTTPAGT][Http Pkt] Not permit http GET method.(method=0)
Sep 16 2023 10:11:06.634 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_ERROR(d):CID=0x5c;
[Web-Err][slot: 0, process: nac_svc1][HTTPAGT][Http Pkt] Check user permit login  fail.(ret=6)
```

该问题原因是终端使用GET方式向设备提交用户名密码信息，但设备默认只开启了HTTP POST的方式，未开启HTTP GET方式（HTTP GET方式存在密码泄露风险，推荐使用POST方式）。

在设备Portal服务器模板下开启允许用户使用GET方式向设备提交用户名和密码等信息：

```text
[HUAWEI] web-auth-server portal_test
[HUAWEI-web-auth-server-portal_test] http get-method enable
```

### 1.2.3.4.2 终端提交的用户名密码请求中未携带用户名或密码，或用户名密码的识别关键字不匹配

通过debugging web all，可以看到收到终端get请求，显示“[Http Req] Get username attr by key username fail.”或者“[Http Req] Get password attr by key password fail.”。

```text
Sep 16 2023 10:14:48.235 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]HttpAgt send mesh msg len=140
Sep 16 2023 10:14:48.236 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]HttpAgtProcQueueMeshMsg sendMsg len=140
Sep 16 2023 10:14:48.236 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]Recive http request mesh msg. (http_ctxid=0, http_cbid=6, need_lb=0, method=3, client=0XC401018E:17352, server=0XC2010101:6550, fd=195)
Sep 16 2023 10:14:48.236 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]Get user access ifindex 1627389953 by ip 0XC401018E & vrf 0.
Sep 16 2023 10:14:48.237 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_EVENT(d):CID=0x5c;
[Web-Evt][slot: 0, process: nac_svc1]web get active svrIndex is 0, userIfIndex is 1627389953.
Sep 16 2023 10:14:48.237 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_ERROR(d):CID=0x5c;
[Web-Err][slot: 0, process: nac_svc1][HTTPAGT][Http Req] Get username attr by key username fail.
Sep 16 2023 10:14:48.237 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_ERROR(d):CID=0x5c;
[Web-Err][slot: 0, process: nac_svc1][HTTPAGT][Http Pkt] Decode username & password fail.(ret=10)
Sep 16 2023 10:16:41.145 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]HttpAgt send mesh msg len=140
Sep 16 2023 10:16:41.145 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]HttpAgtProcQueueMeshMsg sendMsg len=140
Sep 16 2023 10:16:41.146 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]Recive http request mesh msg. (http_ctxid=0, http_cbid=7, need_lb=0, method=3, client=0XC401018E:17864, server=0XC2010101:6550, fd=195)
Sep 16 2023 10:16:41.146 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_MESSAGE(d):CID=0x5c;
[Web-Msg][slot: 0, process: nac_svc1][HTTPAGT]Get user access ifindex 1627389953 by ip 0XC401018E & vrf 0.
Sep 16 2023 10:16:41.147 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_EVENT(d):CID=0x5c;
[Web-Evt][slot: 0, process: nac_svc1]web get active svrIndex is 0, userIfIndex is 1627389953.
Sep 16 2023 10:16:41.147 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_ERROR(d):CID=0x5c;
[Web-Err][slot: 0, process: nac_svc1][HTTPAGT][Http Req] Get password attr by key password fail.
Sep 16 2023 10:16:41.147 9700s-2.196 %%01ESAP_WEB/6/WEB_DEBUG_ERROR(d):CID=0x5c;
[Web-Err][slot: 0, process: nac_svc1][HTTPAGT][Http Pkt] Decode username & password fail.(ret=11)
```

终端使用post或者get方式提交用户名密码信息给设备时，需要同时携带用户名和密码，且用户名的识别关键字和密码的识别关键字需要和设备配置的识别关键字一致。

1. 当终端使用get方式提交用户名密码信息给设备时，可以在URL中看到用户名密码信息

如果设备登录URL使用HTTP协议，可以在终端上抓取报文，确认提交给设备的用户名密码信息。

1. 当终端使用post方式提交用户名密码信息给设备时，如果设备登录URL使用HTTP协议，可以在终端上抓取报文，确认提交给设备的用户名密码信息。

上述示例报文中用户名的识别关键字为username，密码的识别关键字为password。如果没有用户名密码信息，需要Portal服务器确认根因；如果用户名密码的识别关键字与设备不一致，可以在Portal服务器侧修改，也可在设备上修改。方法如下：

  - 在Portal服务器上修改用户名密码识别关键字。

以Aruba Clearpass服务器为例，其他服务器需要服务器侧提供支持。

    a. 登录Aruba ClearPass服务器。

      i. 在浏览器中输入Aruba ClearPass的访问地址，地址格式为https://Aruba ClearPass IP，其中Aruba ClearPass IP是Aruba ClearPass服务器的IP地址。

      ii. 选择“ClearPass Guest访客管理”。

      iii. 在登录页面中，输入用户名和密码进行登录。

    b. 配置认证界面。

依次选择“配置 > Pages > 网页登录”，选择已经创建的网络登录页面，点击“编辑”进入编辑页面，在“用户名字段”和“密码字段”中设置用户名识别关键字和密码识别关键字。

  - 在设备上修改用户名密码识别关键字。

在Portal服务器模板下配置HTTP/HTTPS协议的POST/GET请求报文的参数。

用户名的识别关键字默认为username，密码的识别关键字默认为password。

```text
[HUAWEI] web-auth-server portal_test
[HUAWEI-web-auth-server-portal_test] http-method post username-key username password-key password
```

### 1.2.3.4.3 RADIUS服务器认证拒绝

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

服务器回应认证拒绝有多种原因，最常见的有用户名密码错误、授权策略无法匹配等，这些问题需要在通过排查服务器日志找到根因后，调整服务器、终端或设备配置解决。

### 1.2.3.4.4 RADIUS服务器不响应

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

  a. 从设备指定源IP ping服务器测试，确认路由是否可达；

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

设备支持在全局下配置指定RADIUS服务器的共享密钥及在RADIUS服务器模板下配置共享密钥，其中全局下的配置优先级高于模板下的配置。

建议在RADIUS服务器模板下配置共享密钥。如果全局下和模板下都配置了共享密钥，建议删除全局下的配置，仅保留模板下的配置。

RADIUS服务器模板下配置共享密钥：

```text
[HUAWEI] radius-server template radius_test
[HUAWEI-radius-radius_test] radius-server shared-key cipher HUAWEI@123
```

全局下配置RADIUS服务器共享密钥：

```text
[HUAWEI] radius-server ip-address 10.10.10.1 shared-key cipher HUAWEI@123
```

### 1.2.3.4.5 RADIUS服务器授权数据失败

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

### 1.2.3.4.6 终端与设备之间存在NAT

通过debugging web all，可以看到收到终端http请求报文，但源IP地址不是用户实际IP地址，出现报错“[Web-Evt] WEBAdp FindOut AccessIf By IpVrf. Can't Find Sta Mac By Ip(0xc0c0c4b) From AC Snooping Table!”。

```text
<HUAWEI>
Dec 01 2020 17:33:14.947.1+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] Web receive http msg.
<HUAWEI>
Dec 01 2020 17:33:14.947.2+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] Web http msg accept.
<HUAWEI>
Dec 01 2020 17:33:14.947.3+08:00 HUAWEI WEB/7/DEBUG:
[Web-Evt]  Src:User Event:Accept HTTP connect(IP:12.12.12.75 , PORT:10253 , RequestId:669978704.)
<HUAWEI>
Dec 01 2020 17:33:14.947.4+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] [WEB RecvHttp] Userip = 12.12.12.75,UserVrf = 0.
<HUAWEI>
Dec 01 2020 17:33:14.947.5+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg]  Method:GET
<HUAWEI>
Dec 01 2020 17:33:14.947.6+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg]  HTTP Version:HTTP/1.1
<HUAWEI>
Dec 01 2020 17:33:14.947.7+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg]  Http Version:HTTP/1.1
<HUAWEI>
Dec 01 2020 17:33:14.947.8+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] WEB Get Header Value, RequestId:669978704, Field:Content-Length, ret:1
<HUAWEI>
Dec 01 2020 17:33:14.947.9+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] WEB Get Header Value, RequestId:669978704, Field:If-Modified-Since, ret:1
<HUAWEI>
Dec 01 2020 17:33:14.947.10+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] WEB Get Header Value, RequestId:669978704, Field:Cookie, ret:1
<HUAWEI>
Dec 01 2020 17:33:14.947.11+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] WEB Get Header Value, RequestId:669978704, Field:Referer, ret:1
<HUAWEI>
Dec 01 2020 17:33:14.947.12+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] WEB Get Header Value, RequestId:669978704, Field:Host, ret:1
<HUAWEI>
Dec 01 2020 17:33:14.947.13+08:00 HUAWEI WEB/7/DEBUG:
[Web-Evt] WEBAdp FindOut AccessIf By IpVrf. Can't Find Sta Mac By Ip(0xc0c0c4b) From AC Snooping Table!
<HUAWEI>
Dec 01 2020 17:33:14.947.14+08:00 HUAWEI WEB/7/DEBUG:
[Web-Evt] WEBAdp FindOut AccessIf By IpVrf. Get IP information.(ulGwIpaddr=12.12.12.76,ulDstIpaddr=12.12.12.0, ulDstIpMask=255.255.255.0)
<HUAWEI>
Dec 01 2020 17:33:14.947.15+08:00 HUAWEI WEB/7/DEBUG:
[Web-Evt] Get ulNextHop.(ulNextHop=0xc0c0c4c)
<HUAWEI>
Dec 01 2020 17:33:14.947.16+08:00 HUAWEI WEB/7/DEBUG:
[Web-Err] WEBAdp FindOut AccessIf By IpVrf. Get Sta Info By Mac Failed!
<HUAWEI>
Dec 01 2020 17:33:14.947.17+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] Get user access ifinex by ip fail[1]: ip[12.12.12.75]
<HUAWEI>
Dec 01 2020 17:33:14.947.18+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] Get receive ifindex by CIB fail!.
<HUAWEI>
Dec 01 2020 17:33:14.947.19+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] Get user ifindex[4], L3IfIndex[4294967295], VID[12].
<HUAWEI>
Dec 01 2020 17:33:14.947.20+08:00 HUAWEI WEB/7/DEBUG:
[Web-Msg] Portal disable on ifindex[4], L3IfIndex[4294967295].
<HUAWEI>
Dec 01 2020 17:33:14.947.1+08:00 HUAWEI WEB/7/DEBUG:
[Web-Err] Get web server config fail[1].
[HUAWEI] display access-user
-----------------------------------------------------------------
UserID  Username        IP address     MAC                Status
-----------------------------------------------------------------
16654   5cd998bc034c    200.1.1.64     5cd9-98bc-034c     Pre-authen
-----------------------------------------------------------------
Total: 1, printed: 1
```

该问题原因为终端用户与设备之间存在NAT，设备收到终端http请求报文的源IP地址为NAT转后之后的IP地址，设备根据该IP地址无法查找到用户信息，导致认证失败。

该问题可通过增加配置使用HTTP/HTTPS协议进行Portal认证时CAPWAP隧道转发的IP地址来解决，该CAPWAP隧道转发的IP地址为设备本机地址，与设备登录URL对应的IP地址相同。

```text
[HUAWEI] portal tunnel-forward ip 12.12.12.76
```
