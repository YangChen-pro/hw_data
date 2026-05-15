# 1.5.5 故障案例：AC与Portal服务器上配置的Portal协议版本不一致导致STA认证失败

### 现象描述

AC与第三方Portal服务器对接，STA Portal认证失败。

### 相关告警与日志

无。

### 原因分析

AC与Portal服务器上配置的Portal协议版本不一致（第三方服务器仅支持Portal协议V1.0、V2.0，AC上手动配置成了Portal协议V3.0）。

### 操作步骤

1. 通过trace功能查看终端用户认证过程。

```text
[AC] trace object mac-address sta-mac
[AC] trace object ip-address sta-ip
[AC] trace enable
[AC] terminal debugging
[AC] terminal monitor
```

存在提示“Web current version 2 does not support.”或“Web current version 1 does not support.”，可以确认设备配置的Portal协议版本不支持Portal服务器发送的Portal报文使用的Portal协议版本。

```text
[BTRACE][2023-09-14 23:01:40][0][WEB][196.1.1.142]:Web current version 2 does not support.
```

2. 检查AC侧Portal认证配置。

```text
<AC> display web-auth-server configuration
  Listening port           : 2000
  Portal                   : version 3
  Include reply message    : enabled
  Server-Source            : all-interface
```

对比trace信息发现，AC与第三方服务器上使用的Portal协议版本不一致，Portal服务器侧请求使用Portal协议V2.0，而AC侧配置了仅支持Portal协议V3.0。

3. 由于Portal服务器侧无法修改Portal协议版本，在修改AC侧Portal协议版本为同时支持Portal协议V2.0和Portal协议V3.0版本后，问题解决。

```text
[AC] web-auth-server version v3 v2
```

或恢复为默认同时支持Portal协议V1.0、V2.0和V3.0版本。

```text
[AC] undo web-auth-server version
```

### 建议与总结

当前通用的Portal协议版本是Portal协议V2.0。但是为了保证通信正常，建议采用设备的缺省配置，即Portal协议V1.0和Portal协议V2.0、V3.0三个版本都支持。
