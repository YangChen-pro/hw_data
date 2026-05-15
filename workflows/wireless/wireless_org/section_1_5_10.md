# 1.5.10 故障案例：终端成功连接SSID并打开浏览器后，无法弹出Portal认证页面

### 现象描述

终端成功连接SSID并打开浏览器后，无法弹出Portal认证页面。

### 相关告警与日志

无。

### 原因分析

在终端浏览器中手动输入Portal页面的IP地址，发现Portal认证页面可以弹出。这说明可能是免认证规则未放通DNS服务器导致，在认证成功之前用户可以访问一些加入到免认证规则的网络资源，但需要放通DNS服务器来解析域名，否则输入域名后无法解析。放通DNS服务器后问题解决。

### 操作步骤

1. 将DNS服务器加入到免认证资源中，配置如下：

```text
<AC> system-view
[AC] free-rule-template name default_free_rule
[AC] free-rule 1 destination ip 8.8.8.8 mask 255.255.255.255
```

### 建议与总结

配置Portal认证时，需通过free-rule放通DNS服务器，否则输入的域名无法被解析。
