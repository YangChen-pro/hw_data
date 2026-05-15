# 1.5.2 故障案例：STA与Portal服务器之间网络不可达导致STA接入AP后无法弹出Portal认证页面

### 现象描述

AC对接控制器配置Portal+RADIUS认证，STA接入AP后，无法弹出Portal认证页面。

### 相关告警与日志

无。

### 原因分析

STA网关设备上配置了ACL规则限制了访问Portal服务器，导致STA与Portal服务器之间网络不可达。

### 操作步骤

1. 在AP上通过debug手段查看Portal认证页面推送过程。

```text
<AP> debug portal all
<AP> terminal debugging
<AP> terminal monitor
Mar 01 2021 14:18:21.280.36+00:00 AP16 PORTAL/7/PORTAL DEBUG:
PORTAL->(CB:0)HTTP Push Payload:
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 352
<TITLE> Web Authentication Redirect</TITLE>
<META http-equiv="Cache-control" content="no-cache">
<META http-equiv="Pragma" content="no-cache">
<META http-equiv="Expires" content="-1">
<META http-equiv=“refresh” content=“1; URL=http://portal-server-ip:8080/portal?ssid=Talent……">
```

确认AP已按Portal服务器需求将Portal认证页面推送给了STA。

2. 在STA上通过Telnet测试TCP 8080端口可达性。

pc-client> telnet portal-server-ip 8080

发现STA到Portal服务器端口不可达。

3. 在STA网关设备上，带源测试到Portal服务器的可达性。

```text
<STA-Gateway> telnet –s source-ip portal-server-ip
```

发现STA网关到Portal服务器网络可达。

4. 检查STA网关设备配置，发现STA业务VLAN内配置ACL规则限制了访问Portal服务器。删除规则限制后，问题解决。
