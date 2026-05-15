# 1.5.11 故障案例：笔记本电脑升级Windows 11操作系统后，802.1X认证失败

### 现象描述

笔记本电脑升级到Windows 11操作系统后，802.1X认证失败，通过trace object mac-address mac-address命令查看业务诊断信息，发现终端不回应Request Identity报文。

### 相关告警与日志

无

### 原因分析

Windows 11加强了安全性，对于自颁布证书默认拒绝。

### 操作步骤

1. 在系统使用自带客户端进行802.1X证书认证（包括TLS和PEAP-MSchapv2），报错为E63505证书认证错误。

2. 对Windows 11 EAP-PEAP认证抓包，发现在EAP的认证流程初期服务器请求身份，客户端回应，交换校验方式流程正常，但在服务器发送Server Hello交换秘钥后，Windows 11系统返回了拒绝认证报文，因此判断问题出在Windows 11正式版本的EAP认证校验阶段。

3. 根据微软提供的日志收集工具分别收集了Windows 10、Windows 11正式版本和Windows 11预览版的客户端认证日志，根据日志分析尝试以下配置（该配置不影响用户业务）。

```text
<AC> system-view
[AC] dot1x timer tx-period 3  //缩短发送认证请求的时间间隔
[AC] dot1x-access-profile name Test  //进入业务对应的802.1X接入模板视图
[AC-dot1x-access-profile-Test] dot1x retry 10    //增加向802.1X用户发送认证请求报文的重传次数
```
