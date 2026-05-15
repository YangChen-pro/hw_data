## 1.1.1 关键配置检查

- VAP模板配置检查

- 认证模式配置检查

### 1.1.1.1 VAP模板配置检查

根据SSID找到对应VAP模板，检查VAP模板下配置，主要检查安全模板和认证模板配置。

1. 通过命令display vap-profile all查看所有的VAP模板，根据SSID找到对应的VAP模板。

```text
[HUAWEI] display vap-profile all
FMode   : Forward mode
STA U/D : Rate limit client up/down
VAP U/D : Rate limit VAP up/down
BR2G/5G : Beacon 2.4G/5G rate
---------------------------------------------------------------------------------------------------------------------
Name     FMode     Type     VLAN      AuthType      STA U/D(Kbps)  VAP U/D(Kbps)  BR2G/5G(Mbps)  Reference  SSID
---------------------------------------------------------------------------------------------------------------------
default  direct   service  VLAN 1    Open         -/-              -/-              1/6               0            HUAWEI-WLAN
vap_dot1x tunnel service  VLAN 200  WPA2+802.1X  -/-              -/-              1/6               3            dot1x_test
---------------------------------------------------------------------------------------------------------------------
Total: 2
```

不建议多个VAP模板下绑定相同SSID，因为SSID相同的多个VAP模板绑定到同一AP时，会引起接入失败等异常现象。

2. 查看VAP模板下的配置，检查VAP模板下绑定的安全模板和认证模板。

```text
[HUAWEI] wlan
[HUAWEI-wlan-view] vap-profile name vap_dot1x
[HUAWEI-wlan-vap-prof-vap_dot1x] display this
#
forward-mode tunnel
service-vlan vlan-id 200
ssid-profile dot1x
security-profile security_dot1x
authentication-profile authen_dot1x
#
```

3. 查看安全模板下的配置，安全策略需要配置为WPA/WPA2的802.1X认证和加密。

```text
[HUAWEI] wlan
[HUAWEI-wlan-view] security-profile name security_dot1x
[HUAWEI--wlan-sec-prof-security_dot1x] display this
#
security wpa2 dot1x aes
#
```

4. 查看认证模板下的配置，需要绑定802.1X接入模板。

```text
[HUAWEI] authentication-profile name authen_dot1x
[HUAWEI-authentication-profile-authen_dot1x] display this
#
authentication-profile name authen_dot1x
dot1x-access-profile access_dot1x
access-domain domain_test
#
```

5. 查看802.1X接入模板下的配置，dot1x认证方式需要配置为EAP中继方式，默认为EAP中继方式。

```text
[HUAWEI] dot1x-access-profile name access_dot1x
[HUAWEI--dot1x-access-profile-access_dot1x] display this
#
dot1x-access-profile name access_dot1x
#
```

### 1.1.1.2 认证模式配置检查

802.1X认证场景认证模式需要配置为RADIUS认证模式。

802.1X认证支持本地认证和RADIUS认证两种认证模式。本地认证模式需要创建本地用户并配置内置EAP服务器，本文仅考虑RADIUS认证模式。

认证模式在认证方案下指定，认证方案的引用有两种方式：第一种方式是在认证模板下直接引用认证方案，第二种方式是在域下引用认证方案，然后在认证模板下引用域，第一种方式优先级更高。两种方式不可混用，若两种方式同时配置，第一种方式生效，第二种方式在认证模板下配置的默认域或强制域不生效。实际项目应用中，推荐采用第二种方式。

- 方式一：在认证模板下引用认证方案。

在认证模板下引用认证方案时，需要同时引用RADIUS服务器模板，如果需要计费，还需要同时引用计费方案。

```text
[HUAWEI] authentication-profile name authen_dot1x
[HUAWEI-authentication-profile-authen_dot1x] display this
#
authentication-profile name authen_dot1x
dot1x-access-profile access_dot1x
authentication-scheme radius
accounting-scheme radius
radius-server radius_test
#
```

- 方式二：在域下引用认证方案。

在域下引用认证方案时，需要同时在域下引用RADIUS服务器模板，如果需要计费，还需要同时在域下引用计费方案。

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
[HUAWEI] authentication-profile name authen_dot1x
[HUAWEI-authentication-profile-authen_dot1x] display this
#
authentication-profile name authendot1x
dot1x-access-profile accessdot1x
access-domain domain_test
#
```

认证域之间存在优先级，终端在优先级高的认证域中进行认证：指定接入类型的强制域 > 非指定接入类型的强制域 > 用户名中携带的合法域 > 指定接入类型的默认域 > 非指定接入类型的默认域 > 全局默认域。各种域的配置示例如下：

  - 指定接入类型的强制域：

```text
[HUAWEI-authentication-profile-authen_dot1x] display this
#
authentication-profile name authendot1x
dot1x-access-profile accessdot1x
access-domain domain_test dot1x force
```

  - 非指定接入类型的强制域：

```text
[HUAWEI-authentication-profile-authen_dot1x] display this
#
authentication-profile name authendot1x
dot1x-access-profile accessdot1x
access-domain domain_test force
```

  - 用户名中携带的合法域：指用户认证时使用的用户名中使用@携带了域名，并且该域在设备上已创建。

  - 指定接入类型的默认域：

```text
[HUAWEI-authentication-profile-authen_dot1x] display this
#
authentication-profile name authendot1x
dot1x-access-profile accessdot1x
access-domain domain_test dot1x
```

  - 非指定接入类型的默认域：

```text
[HUAWEI-authentication-profile-authen_dot1x] display this
#
authentication-profile name authendot1x
dot1x-access-profile accessdot1x
access-domain domain_test
```

  - 全局默认域：指在系统视图上通过domain xxx指定的全局默认域。
