# 1.4.3 如何实现终端上自动弹出Portal认证页面

自动弹出Portal认证页面实现原理：终端关联到SSID后，主动发出HTTP的探测请求报文，检测目的地址是否可达，以及回应的内容是否符合预期，以此来判断接入的网络是否需要进行Portal认证。目的地址一般是固定的网址，各终端或APP应用存在差异。如果目的地址不可达或回应内容不符合预期，那么终端会调用浏览器再次发出HTTP请求，设备拦截到此请求进行重定向，实现自动弹出Portal认证页面的功能。

某些终端无法自动弹出页面的原因：

- 终端不会主动发出探测请求报文。

- 终端可以发出一次探测请求报文，但是由于某些安装的APP影响导致终端无法调用浏览器再次发出请求，无法自动弹出页面。

- 大部分安卓手机，自动弹出Portal功能，依赖用户手动点击SSID界面进行触发。

### 苹果终端

苹果终端通过自身的CNA（Captive Network Assistant）工具固定对http://captive.apple.com进行探测，如果网络畅通，那么终端会收到内容为Success的回应；反之，则会调用浏览器再次进行探测，实现自动弹出页面的功能。

但是，苹果的自动探测机制对重定向页面有要求，如果是HTTPS的页面，并且证书不是终端信任的第三方机构颁发，那么自动弹出的机制就会失效；同时，苹果终端上安装的APP（如Wi-Fi助手）对其自身的探测机制影响很大，也会导致自动探测功能失效，还有可能导致苹果终端的WIFI信号无法点亮。因此，需要配置以下解决方法：

- 在设备系统视图下执行命令portal captive-adaptive enable，该配置的作用是在“微信”或其它APP认证时，对第一次CNA探测重定向，第二次回应Success，使得APP可以正常唤醒。

### 其它终端

由于安卓系统的开放性，所以每个厂家的生产的安卓终端的探测地址不一样，甚至没有自动探测的功能，需要借助某些APP才能实现该功能。

Windows系统也具有自动探测功能，Windows 7的探测地址是http://www.msftncsi.com/ncsi.txt，Windows 10的探测地址是http://www.msftconnecttest.com/connecttest.txt。小米手机的探测地址是http://connect.rom.miui.com/generate_204。自动探测功能可以通过注册表进行开启或关闭，探测地址也可以进行修改。Windows 7系统注册表是HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\NlaSvc\Parameters\Internet。
