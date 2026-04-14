### 步骤3 如果AP的下线原因是静态IP地址相关配置导致的AP重启

且重启后AP无法重新上线，说明IP信息配置错误，可以在AP上通过以下两种方法重新配置。

**方法一：配置AP上线方式为DHCP动态获取方式**

```bash
[root@HUAWEI]
MDCLI> diagnose ap-address address-mode
[(x)root@HUAWEI]/diagnose/ap-address/address-mode
MDCLI> mode dhcp
[*(x)root@HUAWEI]/diagnose/ap-address/address-mode
MDCLI> emit
[root@HUAWEI]/diagnose/ap-address
MDCLI> reboot  //重启AP生效
```

**方法二：重新配置正确的静态IP地址**

```bash
[root@HUAWEI]
MDCLI> diagnose ap-address ap-ipv4-address
[(x)root@HUAWEI]/diagnose/ap-address/ap-ipv4-address
MDCLI> ipv4-address 10.23.100.100 gateway 10.23.100.1 subnet-mask 24
[*(x)root@HUAWEI]/diagnose/ap-address/ap-ipv4-address
MDCLI> emit
[root@HUAWEI]/diagnose/ap-address
MDCLI> reboot  //重启AP生效
```