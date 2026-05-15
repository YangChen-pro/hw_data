# 1.4.2 关键配置检查

AC上模板配置检查

## 1.4.2.1 AC上模板配置检查

根据SSID找到对应VAP模板，检查VAP模板下配置，主要检查认证模板配置。

1. 通过命令display vap-profile all查看所有的VAP模板，根据SSID找到对应的VAP模板。

```text
[HUAWEI] display vap-profile all
FMode   : Forward mode
STA U/D : Rate limit client up/down
VAP U/D : Rate limit VAP up/down
BR2G/5G : Beacon 2.4G/5G rate
---------------------------------------------------------------
Name         FMode    Type     VLAN       AuthType     STA U/D(Kbps)  VAP U/D(Kbps)  BR2G/5G(Mbps)  Reference  SSID
---------------------------------------------------------------
default      direct   service  VLAN 1    Open         -/-            -/-               1/6              0           HUAWEI-WLAN
vap_portal  tunnel    service  VLAN 200 Open+Portal -/-            -/-               1/6              3           portal_test
---------------------------------------------------------------
Total: 2
```

不建议多个VAP模板下绑定相同SSID，因为SSID相同的多个VAP模板绑定到同一AP时，会引起接入失败等异常现象。

1. 查看VAP模板下的配置，检查VAP模板下绑定的认证模板。

```text
[HUAWEI] wlan
[HUAWEI-wlan-view] vap-profile name vap_portal
[HUAWEI-wlan-vap-prof-vap_portal]display this
#
 forward-mode tunnel
 service-vlan vlan-id 200
 ssid-profile localportal
 authentication-profile authen_portal
#
```

1. 查看认证模板下的配置，需要绑定Portal接入模板。

```text
[HUAWEI] authentication-profile name authen_portal
[HUAWEI-authentication-profile-authen_portal] display this
#
authentication-profile name authen_portal
 portal-access-profile access_portal
 access-domain domain_test
#
```

2. 查看Portal接入模板下的配置，需要绑定Portal服务器模板。如果是外置Portal，需要配置Server IP和URL。

URL有两种配置方式，一是直接在Portal服务器下配置URL；二是在Portal服务器下引用URL模板，在URL模板下配置URL，同时URL模板下可以配置所需的URL参数，如果Portal服务器需要特定的URL参数，则只能通过URL模板方式配置。

  - 方式一：Portal服务器下直接配置url。

```text
[HUAWEI] web-auth-server portal_test
[HUAWEI-web-auth-server-portal_test] display this
#
web-auth-server server_portal
 server-ip 12.12.12.1
 port 50100
 url http://12.12.12.1:8080/portal
 protocol http
#
```

  - 方式二：Portal服务器下配置url模板。

```text
[HUAWEI] web-auth-server portal_test
[HUAWEI-web-auth-server-portal_test] display this
#
web-auth-server server_portal
 server-ip 12.12.12.1
 port 50100
 url-template url_test
 protocol http
#
```

查看URL模板下配置，需要配置URL及所需要的参数。

```text
[HUAWEI]url-template name url_test
[HUAWEI-url-template-url_test] display this
#
url-template name url_test
 url http://12.12.12.1:8080/portal
 url-parameter device-ip ac-ip user-ipaddress userip ssid ssid
#
```

3. 外置Portal认证，需要在Portal接入模板下绑定Portal服务器模板：

```text
[HUAWEI] portal-access-profile name access_portal
[HUAWEI-portal-access-profile-access_portal] display this
#
portal-access-profile name access_portal
 web-auth-server portal_test direct
#
```

4. 检查DNS放通配置。

查看系统视图，有没有配置portal pass dns enable，如果没有配置，需要通过free rule的方式将dns服务器地址放通，如下示例，将dns服务器地址8.8.8.8通过free rule放通。

```text
[HUAWEI] free-rule-template name default
[HUAWEI-free-rule-default] display this
#
free-rule-template name default_free_rule
 free-rule 1 destination ip 8.8.8.8 mask 255.255.255.0 source ip any
#
[HUAWEI] authentication-profile name authen_portal
[HUAWEI-authentication-profile-authen_portal] display this
#
authentication-profile name authen_portal
 portal-access-profile access_portal
 access-domain domain_test
 free-rule-template default_free_rule
#
```
