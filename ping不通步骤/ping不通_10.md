

### 15.2.10 收集信息并寻求技术支持

### 1. 收集信息

a. 收集上述各个操作步骤的执行结果。
b. 采集logbuffer信息、trapbuffer信息。
<HUAWEI> display logbuffer
<HUAWEI> display trapbuffer
c. 采集一键式诊断信息。
<HUAWEI> display diagnostic-information
须知
•若输出诊断信息过长,可以按Ctrl+C停止。
•此命令主要用于问题定位,搜集系统诊断信息,搜集时可能会影响系统的
性能(例如CPU占用率升高等)。因此,在系统正常运行时不建议执行此
命令。
•严禁在连接到设备的多个终端上同时执行display diagnostic-
information命令,否则可能造成设备的CPU占用率明显增高,导致设备
性能下降。
d. 保存交换机的日志、诊断日志。

```bash
<HUAWEI> save logfile
<HUAWEI> system-view
[HUAWEI] diagnose
[HUAWEI-diagnose] save diag-logfile
```

将框式交换机CF卡中保存的日志、诊断日志文件导出到相关文件路径。

```bash
<HUAWEI> cd cfcard:/logfile
```

将盒式交换机Flash中保存的日志、诊断日志文件导出到相文件路径。

```bash
<HUAWEI> cd logfile/
```

### 2. 寻求技术支持

请联系华为技术支持人员获取技术支持。
