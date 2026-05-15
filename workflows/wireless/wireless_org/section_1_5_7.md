# 1.5.7 故障案例：Portal服务器与STA之间的心跳时间过短导致STA上频繁弹Portal认证页面

### 现象描述

AC配置Portal认证，终端认证通过之后，过几分钟就会自动断开无线网络，需要重新认证。

### 相关告警与日志

无。

### 原因分析

Portal服务器与STA之间的心跳时间过短，且STA上关闭了Portal认证成功页面，导致STA被强制离线。

### 操作步骤

1. Portal认证提交账号时，执行如下命令查看终端上线失败和异常下线原因。

  a. 执行命令display aaa online-fail-record mac-address mac-address，发现终端上线失败原因为终端用户认证被radius server reject。

  b. 执行命令display aaa abnormal-offline-record mac-address mac-address，发现终端异常下线原因为终端请求离线（Web user request）。

  c. 执行命令display access-user mac-address mac-address，发现在弹出Portal认证页面但不输入账号密码时，终端处于认证前域状态（pre-authen）。

2. 通过trace功能查看终端用户认证过程。

```text
[AC] trace object mac-address sta-mac
[AC] trace object ip-address sta-ip
[AC] trace enable
[AC] terminal debugging
[AC] terminal monitor
```

结合回显信息分析可知，是Portal服务器向AC发起logout request引起的STA下线。

```text
[BTRACE][2023-09-16 18:25:42][0][WEB][10.1.1.1]:Received packet from socket (length = 1025 Vrf = 0):
Version         : 2
Type            : logout request
Method          : chap
SerialNo        : 12034
RequestID       : 0
UserIP          : 10.1.1.1
ErrorCode       : 0
AttributeNumber : 1
```

3. 在Portal服务器上调大Portal服务器与STA的心跳时间为4小时或更长。与此同时，建议使用MAC地址优先的Portal认证。
