# 1.5.6 故障案例：AC上配置的Portal服务器IP地址与Portal服务器实际IP地址不一致导致STA认证失败

### 现象描述

AC与第三方Portal服务器对接，STA Portal认证失败。

### 相关告警与日志

无。

### 原因分析

AC上配置的Portal服务器IP地址与Portal服务器实际IP地址不一致。

### 操作步骤

1. 通过trace功能查看终端用户认证过程。

```text
[AC] trace object mac-address sta-mac
[AC] trace object ip-address y.y.y.y
[AC] trace enable
[AC] terminal debugging
[AC] terminal monitor
```

存在Portal服务器发包源地址与AC侧配置的server-ip地址未配置的提示。

```text
[BTRACE][WEB][y.y.y.y]:Received packet from socket (length = 61 Vrf = 0):
Version         : 2
Type            : authentication request
Method          : pap
[BTRACE][WEB][y.y.y.y]:WEB receive packet from portal server successfully.
[BTRACE][WEB][y.y.y.y]:[WEB Proc PS Msg] Server IP = z.z.z.z, Server Vrf = 0
[BTRACE][WEB][y.y.y.y]:
Failed to process packet for portal server,because server IP does not config.(serverIP=z.z.z.z)
```

2. 在AC上修改Portal服务器IP地址与Portal服务器发包源地址一致后，问题解决。

```text
<AC> system-view
[AC] web-auth-server test
[AC-web-auth-server-test] server-ip z.z.z.z
```
