# 1.5.4 故障案例：AC与Portal服务器配置的共享密钥不一致导致STA认证失败

### 现象描述

AC对接第三方Portal服务器，STA Portal认证失败。

### 相关告警与日志

无。

### 原因分析

Portal服务器与AC侧配置的共享密钥不一致。

### 操作步骤

1. 通过trace功能查看终端用户认证过程。

```text
[AC] trace object mac-address sta-mac
[AC] trace object ip-address sta-ip
[AC] trace enable
[AC] terminal debugging
[AC] terminal monitor
```

存在Portal服务器与AC侧配置的shared-key需要一致的提示。

```text
[BTRACE][2023-09-14 22:36:05][0][WEB][196.1.1.142]:Web 2.0 shared-key mismatch.
```

2. 在AC上将AC与Portal服务器两端共享密钥配置一致之后，问题解决。

```text
<AC> system-view
[AC] web-auth-server test
[AC-web-auth-server-test] shared-key cipher test@123
```
