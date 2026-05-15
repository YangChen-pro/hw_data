# 1.5.1 故障案例：AC免认证规则模板中未配置放行终端DNS报文导致Portal页面无法正常弹出

### 现象描述

Portal认证场景下，STA连入无线后没有弹出Portal认证页面，STA无法使用无线网络。

### 相关告警与日志

无。

### 原因分析

DNS未放通导致Portal页面重定向失败，Portal页面无法正常弹出。

### 操作步骤

1. 在终端的浏览器中直接输入Portal页面的IP地址，发现Portal认证页面可以正常弹出。

2. 在AC上执行命令display current-configuration，确认Portal认证相关的基本配置正确。

3. 在AP上查看AP推送的Portal url地址是否正确。

```text
<AP> debug portal all
<AP> terminal debugging
<AP> terminal monitor
```

输出内容中未发现有http或https报文触发Portal重定向。

4. 在AP诊断视图下执行命令display wsrv portal free-rule，检查AP上Portal认证用户的免认证规则，发现没有放行DNS报文。

5. 在AC上查看是否配置了Portal认证用户的免认证规则，发现未配置。

```text
[AC] display free-rule-template configuration name test
free-rule-template name test
Total 0 free-rule(s)
```

6. 在AC的免认证规则模板里放行终端DNS报文后，问题解决。

```text
[AC] free-rule-template name test
[AC-free-rule-f1] free-rule 10 destination ip x.x.x.x mask 255.255.255.255
```
