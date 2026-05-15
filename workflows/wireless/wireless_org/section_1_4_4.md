# 1.4.4 Portal重定向失败常见问题

能重定向到Portal页面URL，但无法打开Portal页面

访问任意IP地址可以重定向， 访问网页域名无法定向

访问HTTPS网页报安全告警（正常现象）

访问HTTPS网页无法重定向（HSTS协议）

终端配置了HTTP代理，无法重定向到Portal页面

重定向的Portal页面URL包含%XX，部分Portal服务器无法识别

苹果终端关联信号后无法自动弹出Portal认证页面

终端输入任意IP地址和域名后均无法重定向

## 1.4.4.1 能重定向到Portal页面URL，但无法打开Portal页面

### 问题现象

浏览器访问任意网页可以看到浏览器地址栏上已经跳转到Portal页面URL，但无法打开Portal页面。

### 问题原因

1. 终端与Portal服务器网络不通。

2. 与第三方Portal服务器对接，Portal服务器可能存在负载分担，此时会出现Portal服务器地址与Portal页面URL对应的地址不是同一个，导致AP和AC未放通Portal页面URL对应的地址。

可检查web-auth-server模板下配置的Server IP与URL（两者地址不一致）：

```text
[HUAWEI-web-auth-server-server_portal] display this
#
web-auth-server server_portal
 server-ip 12.12.12.1 12.12.12.2
 port 50100
 shared-key cipher %^%#&=*FNh9cq9Z!8CJee+u(JX1jNUQvz#b+iM#Msz3P%^%#
 url http://12.12.12.3:8080/portal
#
```

### 解决方案

1. 排查终端与Portal服务器之间网络，可以在终端网关上使用网关地址作为源IP地址ping Portal服务器地址，确认路由是否正确，如果无法ping通，需要检查路由配置。

2. 与第三方Portal服务器对接，Portal服务器可能存在负载分担，此时会出现Portal服务器地址与Portal页面URL对应的地址不是同一个，该场景可以在free-rule模板下放通Portal页面URL对应的地址；

在free-rule模板下放通Portal URL对应的地址，再将free-rule模板绑定到认证模板：

```text
[HUAWEI]free-rule-template name default_free_rule
[HUAWEI-free-rule-default_free_rule] free-rule 0 destination ip 12.12.12.3 mask 255.255.255.255
[HUAWEI] authentication-profile name  authen_portal
[HUAWEI-authentication-profile-authen_portal] free-rule-template default_free_rule
```

## 1.4.4.2 访问任意IP地址可以重定向， 访问网页域名无法定向

### 问题现象

在浏览器输入任意IP地址可以重定向到Portal页面并正常访问，但输入任意域名时无法重定向到Portal页面。

### 问题原因

终端在Portal认证成功之前无法访问DNS服务器，有如下三个可能原因：

- 网络中没有DNS服务器（一般是测试阶段，还没有部署DNS服务器）。

- AC和AP没有通过free-rule放通DNS服务器IP地址。

- 终端与DNS服务器网络不通。

### 解决方案

1. 检查网络中是否有DNS服务器，DHCP Server是否给终端分配了DNS服务器；如果网络中没有DNS服务器，则访问域名无法触发重定向。

2. 检查free-rule是否放通DNS服务器IP地址，如果没有放通，在free-rule模板下放通DNS服务器IP地址，再将free-rule模板绑定到认证模板。

```text
[HUAWEI]free-rule-template name default_free_rule
[HUAWEI-free-rule-default_free_rule] free-rule 1 destination ip 114.114.114.114 mask 255.255.255.255
[HUAWEI] authentication-profile name  authen_portal
[HUAWEI-authentication-profile-authen_portal] free-rule-template default_free_rule
```

3. 在终端网关上以网关地址作为源IP地址ping DNS服务器，看路由是否可达，如果路由不可达，需要排查中间网络。

4. 在终端上通过nslookup命令测试DNS服务器是否能正确解析访问的域名，如果不能解析，请排查DNS服务器。

## 1.4.4.3 访问HTTPS网页报安全告警（正常现象）

从Portal重定向原理可知，终端访问HTTPS网页时，设备拦截HTTPS（默认443端口）TCP固定端口的流量，仿冒成终端要访问的目的地址和终端建立TCP连接，TCP建链完成后进行SSL握手，SSL握手使用的是设备内置的自签名证书，设备内置自签名证书并不是合法机构颁发的证书，因此能否重定向成功取决于终端浏览器的安全策略，部分终端浏览器校验服务器证书时会产生告警，点击信任继续后，可以正常重定向到Portal页面。也有部分浏览器没有该提示页面，直接中断访问。

## 1.4.4.4 访问HTTPS网页无法重定向（HSTS协议）

### 问题现象

访问HTTPS网页无法重定向。

### 问题原因

网站要求浏览器必须使用HTTPS访问，而且证书必须要合法，即HSTS。HTTPS重定向时，设备会使用自签名证书（设备不可能拥有目标网站的证书，只能使用自签名证书）伪装成目标网站和浏览器建立SSL连接，如果网站开启了该功能，那么浏览器一旦检测到证书不受信任，将导致重定向失败，如下图中Google Chrome浏览器所示。

## 1.4.4.5 终端配置了HTTP代理，无法重定向到Portal页面

### 问题现象

终端配置了HTTP代理，无法重定向到Portal页面。

### 问题原因

客户在网络中使用了HTTP代理或其它非80或443端口。

### 解决方案

1. 在终端上进行抓包确认，或者在终端上查看浏览器的配置。以Windows终端的IE浏览器为例（Internet选项->连接->局域网(LAN)设置）

2. 在设备上开启HTTP代理功能。

```text
[HUAWEI] portal http-proxy-redirect enable
```

## 1.4.4.6 重定向的Portal页面URL包含%XX，部分Portal服务器无法识别

### 问题现象

对接第三方Portal服务器，浏览器可以重定向到Portal页面URL，但无法打开Portal页面，查看Portal页面URL中包含%XX，如URL为http://12.12.12.1:8080/portal?ac%2Dip=100%2E1%2E1%2E1&userip=200%2E1%2E1%2E172&ssid=portal%5Ftest。

### 问题原因

设备默认开启Portal URL编解码功能。

URL编码对特殊的字符（就是那些不是简单的七位ASCII，如汉字）将以百分符%用十六进制编码，当然也包括如“=”、“&”和“%”这些特殊的字符。其实URL编码就是一个字符ASCII码的十六进制。不过稍微有些变动，需要在前面加上“%”。比如“\”，它的ASCII码是92，92的十六进制是5c，所以“\”的URL编码就是%5c。URL编码表可以在网上查到。某些Portal服务器不支持这样的编码，当设备使能了URL编码功能后就会导致重定向失败。

### 解决方案

关闭设备Portal URL编码功能：

```text
[HUAWEI] portal url-encode disable
```

## 1.4.4.7 苹果终端关联信号后无法自动弹出Portal认证页面

### 问题现象

苹果终端连接无线网络后，不会自动弹出Portal认证页面。

### 问题原因

- 如果是所有苹果终端均存在该问题，有如下可能原因：

  - 设备通过free-rule放行了苹果终端探测的服务器域名（captive.apple.com）的IP地址。

  - Portal服务器页面使用HTTPS协议，且Portal服务器页面网站没有合法证书。

- 如果是个别苹果终端存在该问题，大概率为终端自身问题，可能原因是终端连上无线网络后，使用内部探测工具向苹果服务器发送了探测请求，但后续没有再调用浏览器发送探测，导致无法自动弹出。

### 解决方案

- 如果是所有苹果终端均存在该问题，则按照如下步骤进行处理：

  1. 检查free-rule是否放行苹果终端探测的服务器域名或者对应该域名的地址，如果放通了，需要在free-rule下删除。

    a. 查看free-rule模板下配置。

```text
[HUAWEI] free-rule-template name default_free_rule
[HUAWEI-free-rule-default_free_rule] display this
#
free-rule-template name default_free_rule
 free-rule acl 6000
#
```

    b. 查看ACL下配置。

```text
[HUAWEI] acl 6000
[HUAWEI-acl-ucl-6000] display this
#
acl number 6000
 rule 5 permit ip destination 114.114.114.114 0
 rule 10 permit ip destination 10.10.10.1 24
#
```

    c. 删除放通的苹果探测服务器域名ip地址。

```text
[HUAWEI] acl 6000
[HUAWEI-acl-ucl-6000] undo rule 10
```

  2. 确认Portal服务器页面使用的协议，可以使用浏览器访问任意网址跳转到Portal页面，查看浏览器地址栏URL，如果是https://打头，则表明Portal服务器页面使用HTTPS协议，建议修改成HTTP协议或者购买合法证书。

- 如果是个别苹果终端存在该问题，建议抓取终端侧无线报文，分析报文。

## 1.4.4.8 终端输入任意IP地址和域名后均无法重定向

### 问题现象

终端输入任意IP地址和域名后均无法重定向。

### 问题原因

可能原因为web-auth-server模板下误配置了使能Portal服务器探测功能。

```text
[HUAWEI] web-auth-server test
[HUAWEI-web-auth-server-test] display this
#
web-auth-server test
 server-ip 12.12.12.6
 port 50100
 shared-key cipher %^%#N|):V]!Q-,Og!^95TW9I:(wsM_VyjF~"n*L@.ay2%^%#
 url http://12.12.12.6
 server-detect
#
```

server-detect命令的实现机制为依赖Portal服务器主动向设备发送心跳报文，设备每60s检查一次有没有收到心跳报文，如果连续三次检测都没收到心跳报文，则会将Portal服务器状态置为down，此时不会再进行重定向。

### 解决方案

- 如果Portal服务器是Agile Controller，需要在设备管理的认证参数中勾选“启动接入设备与Portal服务器的心跳”。

- 第三方Portal服务器一般不支持此功能，建议删除server-detect配置。
