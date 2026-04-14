### 6.1.2 AP 异常掉线

### 步骤1 检查AP下线原因记录

在WAC上执行命令`display ap offline-record all`，查看AP下线原因。

```bash
<WAC> display ap offline-record all
Total APs: 3 Total records: 3
------------------------------------------------------------------------------
MAC             Last offline time         Reason
------------------------------------------------------------------------------
00e0-fc24-0080  2015-01-31/16:21:50       Reboot by ap-reset command
00e0-fc76-e360  2015-01-31/14:02:35       Reboot by ap update reset command
00e0-fcb1-56a0  2015-01-31/13:52:35       Reboot by ap update reset command
------------------------------------------------------------------------------
```

常见AP下线的原因及处理建议如下：

**配置变更类（无需处理）：**
- **The AC country code is modified**：修改国家码。无需处理，正常配置变更触发。
- **The AP is replaced**：此AP被替换。无需处理，正常配置变更触发。
- **Reboot by ap update reset command**：下发升级复位命令。无需处理，AP升级后需要重启刷新版本。
- **A command is delivered to reboot an AP**：下发复位命令。无需处理，AC下发复位命令。
- **An AP is deleted**：删除AP。无需处理，AC删除AP。
- **The DTLS configuration of the CAPWAP tunnel changes**：CAPWAP链路DTLS配置变更。无需处理，正常配置变更触发。
- **The AP's factory settings are restored**：AP恢复出厂配置。无需处理，正常配置变更触发。
- **The dual-link networking configuration is modified**：修改双链路组网配置。无需处理，配置导致AP自动重启。
- **The AP name is modified**：更改AP名称。无需处理，正常配置变更触发。
- **The AP group name is modified**：更改AP组配置。无需处理，正常配置变更触发。
- **The management VLAN is modified**：修改管理VLAN。无需处理，正常配置变更触发。
- **AP provisioning parameters are set**：配置AP上线参数。无需处理，正常配置变更触发。
- **The CAPWAP source IP address is deleted**：删除CAPWAP源地址。无需处理，正常配置变更触发。
- **The central AP proactively reboots RUs**：中心AP主动重启RU。无需处理，正常配置变更触发。
- **The CAPWAP sensitive-info PSK is modified**：CAPWAP链路敏感信息PSK变更。无需处理，配置导致AP自动重启。
- **The CAPWAP integrity-check PSK is modified**：CAPWAP链路报文完整性校验PSK变更。无需处理，配置导致AP自动重启。
- **The wideband status change**：wideband使能状态变更。无需处理，正常配置变更触发。
- **Reboot for AP Channel-load-mode change**：信道集模式变更。无需处理，正常配置变更触发。
- **Reset for the data link DTLS configuration change**：数据链路DTLS配置更改，导致AP重启。无需处理，配置导致AP自动重启。
- **Reset for the AC list configuration change**：更改AC list配置导致AP重启。无需处理，配置导致AP自动重启。
- **Reset for the change of the IP address obtaining mode**：更改AP获取IP地址的模式导致AP重启。无需处理，配置导致AP自动重启。
- **Reset for the IP address configuration change**：更改IP地址配置导致AP重启。无需处理，配置导致AP自动重启。
- **Reboot for the branch group of AP change**：修改AP分支组配置，导致AP重启。无需处理，正常配置变更触发。
- **The CAPWAP DTLS authentication configuration of the AP is changed**：AP CAPWAP DTLS认证配置变更。无需处理，配置变更触发。
- **Inner gateway mode change**：AC切换网关模式踢AP下线。无需处理。
- **Reset for the radio mode change**：射频模式切换重启。无需处理。
- **Reset for RTU license activation**：激活RTU license。无需处理。
- **DTLS data link status change**：data link链路状态切换致AP重启。无需处理。
- **The AP type is modified**：修改ap type导致的AP重启。无需处理。
- **Reconnect by command**：AC下发AP重建链命令。无需处理。

**License相关：**
- **The license expires**：License过期导致AC管理AP的资源不足。处理建议：请重新申请License。华为的License发放系统ESDP提供Internet网络访问地址（https://app.huawei.com/isdp）。
- **Insufficient license resources**：License资源不足。处理建议：根据实际组网情况确定处理方法：如果组网采用License集中控制，请查看License Client和License Server是否有断链，如果有，请先恢复链路连接；如果组网采用N+1或双链路，请查看主备链路是否断开，如果有，请先恢复链路连接；如果组网中实际AP数超过了License资源总数，请申请新的License。
- **The AC license expires**：AC license过期，导致AP重启。处理建议：请重新激活License。
- **The WAC license expires**：iMaster NCE-Campus的License已超期。处理建议：购买新的License并加载到iMaster NCE-Campus。
- **Insufficient RTU license**：RTU License资源不足。处理建议：1. 请进行RTU License扩容。2. 华为的License发放系统ESDP提供Internet网络访问地址（https://app.huawei.com/isdp）。
- **Insufficient RTU license and normal license**：RTU License资源不足。处理建议：1. 请进行RTU License和普通License扩容。2. 华为的License发放系统ESDP提供Internet网络访问地址（https://app.huawei.com/isdp）。
- **Reset for an overdue demo license**：AP的RTU Demo License到期，AP重启。处理建议：无需处理。
- **Cloud licenses expire, and local license resources are insufficient**：云管理License过期，且本地License不足。处理建议：请扩容License（远端接入单元并不耗费License）。

**网络/链路异常类：**
- **A CAPWAP tunnel is faulty (due to inconsistent link IDs)**：内部LINK ID不匹配导致的CAPWAP链路异常。处理建议：无需处理，AP会自动尝试修复链路。
- **Heartbeat packet transmission for the CAPWAP data tunnel between the AC and AP times out**：AC与AP间的CAPWAP数据链路心跳超时。处理建议：请检查AP和AC中间网络。
- **Heartbeat packet transmission for the CAPWAP control tunnel between the AC and AP times out**：AC与AP间的CAPWAP控制报文心跳超时。处理建议：请检查AP和AC中间网络。
- **The central AP goes offline**：中心AP掉线导致RU掉线。处理建议：请检查中心AP掉线原因。
- **A CAPWAP tunnel is faulty (due to a CAPWAP link entry verification failure)**：因CAPWAP LINK表项校验失败导致CAPWAP链路异常。处理建议：无需处理，AP会自动尝试修复链路。
- **CAPWAP sensitive-info PSK mismatch**：敏感信息密钥在主备不一致。处理建议：请检查主备AC是否异常。
- **Reboot for AP config fail**：配置下发失败导致AP重启。处理建议：请检查AC与AP间链路是否异常。
- **CAPWAP link down**：capwap链路异常。处理建议：请联系技术支持人员。

**黑名单/安全类：**
- **The AP is added to the blacklist**：AP被添加到黑名单。处理建议：请确认是否需要将此AP加入黑名单。

**配置不匹配类：**
- **The radio type is inconsistent between the AC and AP**：AC和AP间射频类型不匹配。处理建议：请执行命令`display ap config-info`检查AP射频配置是否正确。
- **The country code is inconsistent on the AC and AP**：国家码不匹配。处理建议：请确认AC上的国家码配置与AP所支持的国家码是否一致。
- **Incompatible DTLS version or encryption algorithm**：DTLS版本或加密算法不兼容。处理建议：请升级AP版本，或使用命令`capwap dtls version1.0 enable`和`capwap dtls cbc enable`开启兼容DTLS老版本。

**设备/硬件异常类：**
- **The AP is powered off and restarts**：AP断电重启。处理建议：请确认AP供电是否异常。
- **The reset button is pressed to reset the AP**：手动按复位键重启。处理建议：请确认是否人为复位。
- **The AP restarts due to AP interference**：AP靠太近，干扰导致AP复位重启。处理建议：请联系技术支持人员。
- **Reset for insufficient power supply**：AP供电不足导致设备重启。处理建议：请联系技术支持人员。
- **An internal error (exceed the extreme temperature) occurs**：AP超过极限高温导致重启。处理建议：对环境进行降温处理，如调低空调温度、疏导通风设备等。

**设备内部异常类（需联系技术支持）：**
- **An internal error (KP) occurs**：设备内部异常（内存KP异常）。处理建议：请联系技术支持人员。
- **An internal error (VOS signal error) occurs**：设备内部异常（VOS信号异常）。处理建议：请联系技术支持人员。
- **An internal error (forwarding error monitored by MFPI) occurs**：设备内部异常（MFPI监控到转发异常）。处理建议：请联系技术支持人员。
- **An internal error (PKO error monitored by MSC) occurs**：设备内部异常（MSC监控到PKO异常）。处理建议：请联系技术支持人员。
- **An internal error (reset due to timer expiration) occurs**：设备内部异常（定时器超时复位）。处理建议：请联系技术支持人员。
- **An internal error (reset of the write CPLD register) occurs**：设备内部异常（写CPLD寄存器复位）。处理建议：请联系技术支持人员。
- **The AP restarts due to a CANBUS reset**：CANBUS复位重启。处理建议：请联系技术支持人员。
- **An internal error (MSC error monitored by MFPI) occurs**：设备内部异常（MFPI监控到MSC异常）。处理建议：请联系技术支持人员。
- **An internal error (MSU error monitored by MFPI) occurs**：设备内部异常（MFPI监控到MSU异常）。处理建议：请联系技术支持人员。
- **An internal error (KAP error monitored by MFPI) occurs**：设备内部异常（MFPI监控到KAP异常）。处理建议：请联系技术支持人员。
- **An internal error (TX DMA stop) occurs**：设备内部异常（TX DMA停止）。处理建议：请联系技术支持人员。
- **An internal error (other reason) occurs**：设备内部异常（其他原因）。处理建议：请联系技术支持人员。
- **An internal error (Reset for firmware abnormal) occurs**：WIFI芯片固件异常导致AP重启。处理建议：请联系技术支持人员。
- **An internal error (Reset for abnormal network port self-healing) occurs**：网口异常自愈导致AP重启。处理建议：请联系技术支持人员。
- **An internal error (Reset for the forcible AP disconnection in specific scenarios) occurs**：特定场景下强制AP断开。处理建议：请联系技术支持人员。
- **An internal error (Reset for slow task switching) occurs**：系统运行慢导致AP重启。处理建议：请联系技术支持人员。
- **An internal error (Reset for MFPI detect CAP PBUF use out) occurs**：MFPI监控到转发PBUF耗尽导致AP重启。处理建议：请联系技术支持人员。
- **An internal error (Reset for ap abnormal self-healing) occurs**：AP异常状态自愈。处理建议：无需处理。
- **An internal error (Reset for exception(redis-server exit)) occurs**：redis-server进程异常退出导致AP重启。处理建议：请联系技术支持人员。
- **An internal error (Reset for exception(confd exit)) occurs**：confd进程异常退出导致AP重启。处理建议：请联系技术支持人员。
- **An internal error (Reset for exception(callhome exit)) occurs**：callhome进程异常退出导致AP重启。处理建议：请联系技术支持人员。
- **An internal error (Reset for an abnormal process) occurs**：进程异常导致AP重启。处理建议：请联系技术支持人员。
- **An internal error (memory use out) occurs**：AP的内存耗尽导致重启。处理建议：请联系技术支持人员。
- **An internal error (dophi-server exit) occurs**：Dophi-server进程异常退出。处理建议：联系技术支持人员。
- **An internal error (Wi-Fi SDK self-healing failure) occurs**：Wi-Fi SDK自愈失败。处理建议：联系技术支持人员。
- **Other reasons**：其他原因，一般为设备内部原因。处理建议：请联系技术支持人员。

**其他类：**
- **The AP is forcibly disconnected**：特定场景下（比如CAPWAP隧道满）强制AP断开。处理建议：无需处理。
- **CAPWAP link down for DTLS smooth**：HA或VRRP主备倒换时DTLS平滑导致AP掉线。处理建议：无需处理。
- **Batch delete**：主备AC场景下，主AC切换备AC时，主AC上的AP下线，在备AC上线。处理建议：检查主AC和网络是否异常，主AC恢复后AP切回主AC上线。
- **Reset for the AC mode switching**：AC模式切换。处理建议：无需处理。
- **The device has been disconnected from the iMaster NCE-Campus for more than 90 days**：AC与iMaster NCE-Campus持续断链超过90天。处理建议：执行命令`display controller connect-status`，查看AC上配置的iMaster NCE-Campus地址是否正确，并检查网络连通性。
- **The device is deleted from the iMaster NCE-Campus**：iMaster NCE-Campus删除AC设备。处理建议：无需处理。

> 说明：不同的版本之间的原因字段可能有差异，请以对应版本的原因字段为准。