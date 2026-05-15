# 1.5.8 故障案例：AC上配置的侦听Portal协议报文的端口号错误导致STA Portal认证失败

### 现象描述

AC配置外置Portal认证，终端可正常弹出Portal认证页面，但是提交账号和密码后显示认证失败。

### 相关告警与日志

无。

### 原因分析

AC上配置的侦听Portal协议报文的端口号与服务器侧配置不一致。

### 操作步骤

1. 复现故障，通过trace和debug功能查看认证报文交互过程。

```text
[AC] trace object mac-address sta-mac
[AC] trace enable
[AC] terminal debugging
[AC] terminal monitor
[AC] quit
<AC> debug web all
<AC> debug portal all
```

查看回显信息发现没有Portal报文交互过程。

2. 查看AC侧Portal认证相关配置和服务器侧发包情况。

  a. 查看AC侧Portal认证相关配置。

```text
<AC> display web-auth-server configuration
  Listening port           : 3000
  Portal                   : version 1, version 2, version 3
  Include reply message    : enabled
  Server-Source            : all-interface
......
```

  b. 通过报文捕获工具对AC连向Portal服务器方向的端口进行镜像报文捕获。

  c. 对比发现，AC侧配置的Portal协议报文的侦听端口（3000）与Portal服务器侧的端口（2000）不一致，导致Portal报文交互失败。

3. 在AC的系统视图下执行命令undo web-auth-server listening-port，恢复AC Portal协议报文的端口号为缺省值2000，问题解决。

### 建议与总结

执行命令web-auth-server listening-port可配置设备侦听Portal协议报文的端口号。该端口号需要和Portal服务器发送Portal报文的目的端口号相同，且全局唯一。
