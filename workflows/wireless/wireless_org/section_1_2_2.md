# 1.2.2 关键配置检查

VAP模板配置检查

认证模式配置检查

## 1.2.2.1 VAP模板配置检查

根据SSID找到对应VAP模板，检查VAP模板下配置，主要检查认证模板配置。

1. 通过命令display vap-profile all查看所有的VAP模板，根据SSID找到对应的VAP模板。

```text
[HUAWEI] display vap-profile all
FMode   : Forward mode
STA U/D : Rate limit client up/down
VAP U/D : Rate limit VAP up/down
BR2G/5G/6G : Beacon 2.4G/5G/6G rate
Total: 3
-----------------------------------------------------------------------------------------------------------------------------
Name       FMode    Type     VLAN     AuthType     STA U/D(Kbps)  VAP U/D(Kbps)  BR2G/5G/6G(Mbps)  Reference  SSID
-----------------------------------------------------------------------------------------------------------------------------
default    direct   service  VLAN 1   -            -/-            -/-            5.5/6/6           0          HUAWEI-WLAN
vap_portal tunnel   service  VLAN 200 Open+Portal  -/-            -/-            5.5/6/6           1          portal_test
-----------------------------------------------------------------------------------------------------------------------------
```

不建议多个VAP模板下绑定相同SSID，因为SSID相同的多个VAP模板绑定到同一AP时，会引起接入失败等异常现象。

2. 查看VAP模板下的配置，检查VAP模板下绑定的认证模板。

```text
[HUAWEI] wlan
[HUAWEI-wlan-view] vap-profile name vap_portal
[HUAWEI-wlan-vap-prof-vap_portal] display this
#
 forward-mode tunnel
 service-vlan vlan-id 200
 ssid-profile localportal
 security-profile sec_portal
 authentication-profile authen_portal
#
```

3. 查看认证模板下的配置，需要绑定Portal接入模板。

```text
[HUAWEI] authentication-profile name authen_portal
[HUAWEI-authentication-profile-authen_portal] display this
#
authentication-profile name authen_portal
 portal-access-profile access_portal
 access-domain domain_test
#
```

4. 查看Portal接入模板下的配置，需要绑定Portal服务器模板。

```text
[HUAWEI] portal-access-profile name access_portal
[HUAWEI-portal-access-profile-access_portal] display this
#
portal-access-profile name access_portal
 web-auth-server portal_test
#
```

5. 查看Portal服务器模板配置，需要配置server-ip和URL。

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
 http get-method enable
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
 http get-method enable
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

6. 需要开启HTTP/HTTPS协议的Portal对接功能。

开启HTTP协议的Portal对接：

```text
[HUAWEI] portal web-authen-server http port 8000
```

开启HTTPS协议的Portal对接：

```text
[HUAWEI] portal web-authen-server https ssl-policy default_policy port 8443
```

## 1.2.2.2 认证模式配置检查

外置Portal认证支持本地认证、RADIUS认证、LDAP认证和AD认证，但大部分场景都是使用RADIUS认证，本文仅考虑RADIUS认证模式。

认证模式在认证方案下指定，认证方案的引用方式是在域下引用认证方案，然后在认证模板下引用域。在域下引用认证方案时，需要同时在域下引用RADIUS服务器模板，如果需要计费，还需要同时在域下引用计费方案。

```text
[HUAWEI] aaa
[HUAWEI-aaa] domain domain_test
[HUAWEI-aaa-domain-domain_test] display this
#
 domain domain_test
  authentication-scheme radius
  accounting-scheme radius
  radius-server radius_test
#
```

后续需要在认证模板下配置默认域或者强制域。建议在认证模板下配置不指定接入类型的默认域：

```text
[HUAWEI] authentication-profile name authen_portal
[HUAWEI-authentication-profile-authen_portal] display this
#
authentication-profile name authen_portal
 portal-access-profile access_portal
 access-domain domain_test
#
```

认证域之间存在优先级，终端在优先级高的认证域中进行认证：指定接入类型的强制域 > 非指定接入类型的强制域 > 用户名中携带的合法域 > 指定接入类型的默认域 > 非指定接入类型的默认域 > 全局默认域。各种域的配置示例如下：

- 指定接入类型的强制域：

```text
[HUAWEI-authentication-profile-authen_portal] display this
#
authentication-profile name authen_portal
 portal-access-profile access_portal
 access-domain domain_test portal force
```

- 非指定接入类型的强制域：

```text
[HUAWEI-authentication-profile-authen_portal] display this
#
authentication-profile name authen_portal
 portal-access-profile access_portal
 access-domain domain_test force
```

- 用户名中携带的合法域：指用户认证时使用的用户名中使用@携带了域名，并且该域在设备上已创建

- 指定接入类型的默认域：

```text
[HUAWEI-authentication-profile-authen_portal] display this
#
authentication-profile name authen_portal
 portal-access-profile access_portal
 access-domain domain_test portal
```

- 非指定接入类型的默认域：

```text
[HUAWEI-authentication-profile-authen_portal] display this
#
authentication-profile name authen_portal
 portal-access-profile access_portal
 access-domain domain_test
```

- 全局默认域：指在系统视图上通过domain xxx指定的全局默认域
