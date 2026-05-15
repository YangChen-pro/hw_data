# 1.4.1 Portal重定向

Portal重定向原理

Portal重定向流程

终端自动弹出Portal认证页面原理

## 1.4.1.1 Portal重定向原理

Portal重定向可以实现终端访问HTTP或者HTTPS网站时，如果认证还未通过则自动弹出认证页面控制接入的功能。它的原理是设备拦截HTTP（默认80端口）或者HTTPS（默认443端口）TCP固定端口的流量，伪装成终端要访问的目的地址和终端建立TCP连接，将认证页面重定向给终端。通常重定向是Portal认证的第一阶段，但是也有客户端可以省略重定向过程直接向Portal服务器提交用户名和密码。

无线场景下，Portal重定向是由AP完成的。

Portal重定向可以通过以下两种方式进行：

- 方式一：HTTP 200 OK的方式。

如下所示，其中42.1.1.19是终端IP地址，1.1.1.1是终端访问的目的IP地址：

终端在浏览器中输入http://1.1.1.1后，设备进行拦截，伪装成1.1.1.1并和终端建立TCP连接，即图1中第1到第3个报文。TCP建立完成后，终端发出HTTP GET报文，设备回应HTTP 200 OK报文，即图1中第4和第5个报文。其中HTTP 200 OK报文携带了重定向认证页面的地址，即图2中红框圈出的内容，终端收到此报文后就会访问重定向认证页面。

- 方式二：HTTP 302 Moved Temporarily的方式。

如下所示，其中42.1.1.76是终端IP地址，1.1.1.1是终端访问的目的IP地址：

这种方式和HTTP 200 OK方式的区别就在于设备回应的是HTTP 302 Moved Temporarily报文，重定向的认证页面地址在该报文中携带。

WLAN 默认使用HTTP 200 OK的方式重定向，如果需要使用HTTP 302 Moved Temporarily的方式（如部分定制终端不支持HTTP 200 OK），可使用portal redirect-302 enable命令行进行配置。

## 1.4.1.2 Portal重定向流程

## 1.4.1.3 终端自动弹出Portal认证页面原理

无线终端连接无线网络后，均会先使用内部工具向指定服务器发送HTTP嗅探请求，用来探测无线网络是否有网络访问权限，对于Portal认证网络，设备会拦截终端内部工具发送的HTTP嗅探请求，并发送重定向页面给终端，终端内部工具判断该回应不是期望的回应，认为此无线网络是受控网络，后续会调用系统默认浏览器重新发送HTTP嗅探请求，设备继续拦截并发送重定向页面给终端，浏览器会被重定向到Portal认证页面，此即终端连接无线网络后自动弹出Portal认证页面原理。

以苹果终端为例，苹果终端自动弹出Portal认证页面过程如下：

1. 终端发送一个HTTP 1.0请求到http://captive.apple.com，报文中的User-Agent是CaptiveNetworkSupport。

2. 如果收到的不是期望的success页面，即http://www.apple.com/library/test/success.html，那么终端认为连接网络失败，就会调用浏览器再次发出HTTP 1.1请求到http://captive.apple.com，报文中的User-Agent是Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G34（不同苹果终端或版本之间稍有差异）。

3. 此时，终端自动弹出了Portal的认证页面，用户输入账号密码后即可连接无线网络。

上述即为苹果的CNA(Captive Network Assistant)原理，能够自动推出Portal认证页面的关键在于2中通过浏览器来再次发出HTTP请求，如果不调用或是间隔较长时间调用浏览器，那么认证页面就会无法推出或是推出时间较长。
