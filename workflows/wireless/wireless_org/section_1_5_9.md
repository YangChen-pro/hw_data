# 1.5.9 故障案例：域下错误配置了force-push功能，导致STA Portal认证成功后无法访问特定网站

### 现象描述

业务数据直接转发模式下，终端可以正常短信认证成功，但是在访问特定网站是出现异常。

### 相关告警与日志

无。

### 原因分析

域下错误配置了force-push功能，导致HTTP报文被封装进CAPWAP隧道转发。

### 操作步骤

1. 根据业务数据直接转发的特点，在直连AP的交换机上配置镜像报文捕获功能，确认报文转发情况。

镜像配置：

[SW] observe-port Z interface gigabitethernet x/x/x    //观察口一般保持端口默认配置，接入报文捕获PC

[SW] interface gigabitethernet y/y/y   //真实数据流量通过的接口

[SW-GigabitEthernety/y/y] port-mirroring to observe-port Z both  //一般配置双向镜像

通过访问异常网站来进行问题复现，发现流量被封装进了AP与AC之间的CAPWAP隧道。

2. 在AP上打印转发报文分析报文处理过程。

```text
[AP-diagnose] debug cap print condition clear
[AP-diagnose] debug cap print condition src-ip sta-ip-address  //STA的IP地址
[AP-diagnose] debug cap print condition dst-ip dst-website-ip //目标网站的IP地址
[AP-diagnose] debug cap print print-length 64
[AP-diagnose] debug cap print on print-num 2
<AP> terminal debugging
<AP> terminal monitor
```

分析报文转发过程发现，由于force-push的配置导致数据报文进入CAPWAP隧道进行转发，转发异常。

3. 删除对应认证domain域下force-push配置，问题解决。
