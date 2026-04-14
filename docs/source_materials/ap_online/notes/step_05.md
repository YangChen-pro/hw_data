### 步骤5 如果AP的下线原因是AP断电重启

请检查AP供电是否正常。

1. 检查网线等物理连接设备，是否出现老化。

在WAC上执行命令`virtual-cable-test`，检测网线是否正常工作。

> 注意：执行virtual-cable-test命令会导致设备对应接口的业务中断。

```bash
[HUAWEI] interface 10ge 0/0/2
[HUAWEI-10GE0/0/2] virtual-cable-test
Warning: This operation will take several minutes. Continue? [Y/N]:Y
State Note
OK : Check succeeded.
Open/Short : There may be an open circuit. Please connect cables correctly.
Crosstalk : Check is affected by crosstalk. Please remove the interference source.
notSupport/not: Check is not supported. Please check whether the interface supports the check.
Unknown : Check did not complete successfully, possibly due to user configuration. Please check configuration on local and remote interfaces.
--------------------------------------------------------------------------------
Pair A length(meters): 10
Pair B length(meters): 10
Pair C length(meters): 10
Pair D length(meters): 10
Pair A state: OK
Pair B state: OK
Pair C state: OK
Pair D state: OK
```

**判断标准**：最后四个状态均为OK表示网线是正常的，否则建议更换网线。