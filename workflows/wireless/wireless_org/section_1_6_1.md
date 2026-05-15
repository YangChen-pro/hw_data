# 1.6.1 Portal用户认证问题

Portal用户无法认证成功

外置Portal服务器弹出页面是空白的

Portal服务器不自动推送认证页面

iOS终端不自动弹认证页面

用户配置基于域名放通功能不生效

AC与Portal服务器用户信息同步失败导致用户异常掉线

Portal认证终端显示认证成功，但终端仍会重定向到Portal认证页面

## 1.6.1.1 Portal用户无法认证成功

故障现象

Portal用户无法认证成功。

### 操作步骤

1. 检查AC上是否配置了共享密钥。

易错配置：AC上的shared-key配置需要和服务器保持一致。

```text
[AC-web-auth-server-controller] display this
#
web-auth-server controller
 server-ip 10.10.10.1
 port 50100
 shared-key cipher %^%#E=77UW>`&A-6}x,G*-}X~5pb5\HVe'sU6+Q1S3x%%^%#
 url http://10.10.10.1:8080/portal
#
```

处理建议：建议重新配置一遍后再进行Portal用户认证测试。

2. 检查是否关闭了STA地址学习功能。

易错配置：AC处理Portal服务器认证请求时，需要根据用户IP地址查找用户MAC，若AP不上报终端用户的IP地址，则AC不会记录用户IP地址信息，在根据IP地址查找MAC时会失败，导致AC无法处理Portal服务器认证请求。

```text
[AC] display current-configuration | include learn-client-address disable
```

处理建议：开启STA地址学习功能。

## 1.6.1.2 外置Portal服务器弹出页面是空白的

故障现象

外置portal服务器在升级前能正常使用，升级后能弹出页面，但是整个浏览器是空白的。

### 操作步骤

检查AC上是否配置了第三方Portal服务器要求的URL参数。

易错配置：与第三方Portal服务器对接时，Portal服务器要求在URL中携带acip参数，在AC上未配置该URL参数。

```text
[AC-url-template-test] display this
#
url-template name test
 url http://10.10.10.1:8080/portal
 url-parameter ac-ip wlanacip
#
```

处理建议：根据第三方portal服务器需要，配置相应的URL参数。

## 1.6.1.3 Portal服务器不自动推送认证页面

故障现象

Portal服务器不自动推送认证页面。

### 操作步骤

检查web-auth-server模板下是否开启了探测功能。

易错配置：AC上开启了探测功能，Portal服务器未开启，导致设备上Portal服务器的状态为Abnormal。

```text
[AC-web-auth-server-controller] display this
#
web-auth-server controller
 server-ip 10.10.10.1
 port 50100
 shared-key cipher %^%#E=77UW>`&A-6}x,G*-}X~5pb5\HVe'sU6+Q1S3x%%^%#
 url http://10.10.10.1:8080/portal
 server-detect
#
```

处理建议：建议在需要配置Portal逃生功能时才开启探测。若Portal服务器不支持或未开启心跳探测功能，AC上需要关闭探测功能。

## 1.6.1.4 iOS终端不自动弹认证页面

故障现象

iOS终端不自动弹认证页面。

### 操作步骤

1. 确认Portal服务器是否使用HTTPS协议推送页面。

易错配置：若Portal服务器使用HTTPS协议推送页面，且Portal服务器未安装证书机构颁发的合法证书，则iOS终端不会自动弹出Portal认证页面。

如果Portal认证页面为HTTPS类型，只有当HTTPS网址为域名网址，并且域名证书合法时，终端才能自动弹出Portal认证页面。

处理建议：在Portal服务器上将HTTPS协议推送修改为HTTP协议推送，或者安装合法证书。

## 1.6.1.5 用户配置基于域名放通功能不生效

故障现象

用户配置基于域名放通功能不生效。

### 操作步骤

检查Portal认证时是否放通了DNS服务器。

易错配置：在放通相应的域名时，未放通DNS服务器地址。

```text
#
authentication-profile name p1
 portal-access-profile portal1
 free-rule-template default_free_rule
 authentication-scheme radius_huawei
 radius-server radius_huawei
#
free-rule-template name default_free_rule
 free-rule 1 destination ip 10.23.200.2 mask 255.255.255.0
#
```

处理建议：Portal认证时，放通DNS服务器。

## 1.6.1.6 AC与Portal服务器用户信息同步失败导致用户异常掉线

故障现象

Portal认证场景下，AC与Portal服务器用户信息同步失败导致用户异常掉线。

### 操作步骤

检查web-auth-server模板下是否开启了用户同步功能。

易错配置：AC上在web-auth-server模板下开启了同步功能，但对应Portal服务器上未开启同步，导致AC上用户因为同步失败而下线。

在AC上可以查看用户异常下线记录，下线原因为“WEB user synchronize fail”。

```text
[AC-web-auth-server-controller] display this
#
web-auth-server controller
 server-ip 10.10.10.1
 port 50100
 shared-key cipher %^%#E=77UW>`&A-6}x,G*-}X~5pb5\HVe'sU6+Q1S3x%%^%#
 url http://10.10.10.1:8080/portal
 user-sync
#
```

处理建议：如果Portal服务器不支持或未开启用户同步，AC上需要关闭用户同步功能。

## 1.6.1.7 Portal认证终端显示认证成功，但终端仍会重定向到Portal认证页面

故障现象

Portal认证场景下，终端显示认证成功，但仍会重定向到Portal认证页面。这种现象也被称为“假认证”。

### 操作步骤

检查终端与认证服务器之间是否存在NAT。

易错配置：AC与Controller服务器对接，终端报文经过NAT转换到达Controller服务器，终端发送的报文源IP地址会转换为公网地址，Controller无法识别终端IP段，出现假认证。

```text
#
url-template name url
 url-parameter user-ipaddress userip
#
```

处理建议：如果终端与Controller服务器之间存在NAT，则需要在url参数中携带user-ipaddress参数。
