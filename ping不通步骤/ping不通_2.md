

### 15.2.2 检查配置是否正确

- · 若PC直连交换机,确保PC与所属VLAN配置的VLANIF IP地址为同一网段。
若交换机与其他网络设备直连,确保两端设备接口类型、VLAN配置一致,两端
VLANIF IP地址为同一网段。
以SwitchA为例,查看方法如下:

- 执行命令display port vlan查看GE1/0/1接口的接口类型和VLAN配置。其中 Link Type代表的是接口链路类型,Trunk VLAN List代表的是接口动态加入和静态配置允许通过的VLAN ID。

```bash
<SwitchA> display port vlan
Port     Link Type  PVID Trunk VLAN List
----------------------------------------------------------------------
GigabitEthernet1/0/1  trunk     1   10
GigabitEthernet1/0/2  access     1   1-11 13-30
GigabitEthernet1/0/3  hybrid    50  -
```

- 执行命令display ip interface brief查看VLANIF10接口下的IP地址配置。其中IP Address/Mask代表的是接口的IP地址和掩码。

<SwitchA> display ip interface brief ...... Interface IP Address/Mask

Vlanif10 192.168.1.10/24 ......

Physical Protocol up up

