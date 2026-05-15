

### 15.2.6 检查是否配置黑名单

配置cpu-defend黑名单后,设备将直接丢弃黑名单用户上送的报文。

通过display cpu-defend policy查看调用在全局或特定槽位的策略名,然后通过 display cpu-defend policy policy-name查看策略中是否配置黑名单( Blacklist ), 再通过display acl acl-number查看黑名单调用的ACL具体内容。

```bash
<SwitchA> display cpu-defend policy
----------------------------------------------------
Name : default
Related slot : <>
----------------------------------------------------
Name : test1
Related slot : <1>  //名称为test1的policy调用在1号错位
----------------------------------------------------
<SwitchA> display cpu-defend policy test1
Related slot : <1>
Configuration :
Blacklist 1 ACL number : 3300  //该策略test1下配置了黑名单, 关联的ACL编号为3300
Car packet-type icmp : CIR(5000) CBS(20000)
Car packet-type tcp : CIR(2000) CBS(376000)
<SwitchA> display acl 3300
Advanced ACL 3300, 1 rule
Acl's step is 5
rule 5 permit ip source 10.1.1.1 0 (match-counter 0)  //ACL匹配源IP地址为10.1.1.1的IP报文
```

黑名单中应用的ACL,无论其rule配置为permit还是deny,命中该ACL的报文均会被丢弃。


• 如果策略中配置了黑名单,且黑名单中包含对端IP,请尝试删除黑名单或修改黑名单关联的ACL,保证报文可以被正常处理。

例如:取消防攻击策略test1下的黑名单配置。

```bash
<SwitchA> system-view
[SwitchA] cpu-defend policy test1
[SwitchA-defend-policy-test] display this
#
cpu-defend policy test1
blacklist 1 acl 3300
car packet-type icmp cir 5000 cbs 20000
car packet-type tcp cir 2000 cbs 376000
......
[SwitchA-defend-policy-test1] undo blacklist 1
[SwitchA-defend-policy-test1] quit
```

• 如果策略中没有配置黑名单,或者黑名单中不包含对端IP,进行下一步排查。


说明

如果对端可以Ping通交换机,而从交换机无法Ping通对端,需要确认对方是否禁Ping(如PC上的软件防火墙限制或网络设备上调用了相关策略拒绝访问)。

