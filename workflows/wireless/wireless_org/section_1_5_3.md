# 1.5.3 故障案例：Portal服务器不识别AP推送的URL地址导致未正确弹出Portal认证页面

### 现象描述

FIT AP配置外置Portal认证（第三方认证服务器），STA未正确弹出Portal认证页面。

### 相关告警与日志

无。

### 原因分析

Portal服务器不识别带有转义字符的URL地址。

转义字符：为了Web应用安全，将重定向url中的一些特殊字符转换成安全的形式，从而避免跨站脚本攻击与各种类型的注入攻击。

### 操作步骤

1. 在STA上测试STA到Portal服务器IP地址的网络可达性，确认网络可达。

```text
<STA> ping portal-server-ip
```

2. 在AP上检查Portal认证相关配置，确认Portal认证配置正确。

```text
<AP> display current-configuration
web-auth-server 123
server-ip portal-server-ip port 50100
shared-key cipher %^%#3`la2Q\{……..
url https://xxxxxx
#
portal-access-profile name test
web-auth-server 123 direct
```

3. 在AP上查看AP推送的url地址是否正确。

```text
<AP> debug portal all
<AP> terminal debugging
<AP> terminal monitor
```

检查发现，实际AP推给STA的url格式为http%253A%252F%252，该url中包含了转义字符，Portal服务器无法识别该url格式。Portal服务器能识别的url格式为：http%3A%2F%2，即不带转义字符的格式。

4. 综上确认，AP重定向url推给STA时，将URL进行了安全编解码，关闭该功能后问题解决。

```text
[AP] portal url-encode disable    // URL编解码功能默认开启
```
