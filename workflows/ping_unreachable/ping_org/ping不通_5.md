

### 15.2.5 检查 ARP 学习是否正确

执行display arp all命令,检查直连地址的ARP是否学习正常。

下述回显信息中,如果MAC ADDRESS显示的是MAC地址,则代表ARP学习正确;如果显示的是Incomplete,表示当前表项为临时ARP表项,尚未学习到ARP,出现MAC 地址后,代表ARP学习完成。

```bash
<SwitchA> display arp all
IP ADDRESS   MAC ADDRESS   EXPIRE(M) TYPE INTERFACE   VPN-INSTANCE
-------------------------------------------------------------------------------
192.168.1.10  4c1f-cc17-1ca5      I - Vlanif10
192.168.1.11  4c1f-cc2f-3634 19      D-0 GE1/0/1
-------------------------------------------------------------------------------
Total:2  Dynamic:1  Static:0  Interface:1
```

• 如果ARP学习正确,通过display mac-address interface-type interface-number 命令查看MAC表项,确认MAC地址的出接口和ARP的物理出接口是否一致。若不一致,排查是否存在环路或MAC冲突。

```bash
<SwitchA> display mac-address 4c1f-cc2f-3634
-------------------------------------------------------------------------------
MAC Address    VLAN/VSI           Learned-From      Type
-------------------------------------------------------------------------------
4c1f-cc2f-3634   10/-                  GE1/0/1       dynamic
Total items displayed = 2
```

• 如果ARP学习失败,有以下几种可能性,请参照表15-3进行排查ARP学习失败的原因(SwitchA向SwitchB发送ARP请求报文)。



表 15-3 ARP 学习失败可能的原因

<table><tr><td>可能情况</td><td>可能原因</td></tr><tr><td>ARP请求报文没有发出去</td><td>SwitchA短期内大量ARP Miss消息 触发太多ARP请求, 来不及发送出去、终结子接口上没有使能arp broadcast enable。终结子接口不 能转发ARP广播报文, 在收到ARP 广播报文后它们直接把该报文丢弃</td></tr><tr><td>ARP请求报文没有到达对端SwitchB, 在网络上被丢弃了</td><td>传输链路问题</td></tr><tr><td>ARP请求报文到达了对端SwitchB, 但是被SwitchB丢弃了</td><td>SwitchB受到攻击, 收到大量ARP报 文, 报文被CPCAR机制丢掉</td></tr><tr><td>SwitchB的响应报文没有到达SwitchA</td><td>传输链路问题</td></tr><tr><td>SwitchB的响应报文到达SwitchA但是 没有上送CPU</td><td>SwitchA的CPCAR机制丢掉或ARP限速 丢弃</td></tr><tr><td>SwitchB的响应报文到达SwitchA的 CPU, 但是被丢弃了</td><td>SwitchA的ARP处理模块出错</td></tr></table>

