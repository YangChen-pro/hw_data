"""通用校验工具。"""

from __future__ import annotations

import re
from typing import Any

from .models import Issue


def find_line(text: str, pattern: str) -> int | None:
    regex = re.compile(pattern)
    for index, line in enumerate(text.splitlines(), start=1):
        if regex.search(line):
            return index
    return None


def validate_target(
    target: Any,
    workflow_step_ids: set[str],
    conclusion_ids: set[str],
    file_name: str,
    step_id: str,
    path: str,
) -> list[Issue]:
    if target is None or (isinstance(target, str) and not target.strip()):
        return [
            Issue(
                file=file_name,
                step_id=step_id,
                severity="critical",
                category="next_node",
                path=path,
                message="目标节点为空",
                recommendation="补充合法的 step_id 或 conclusion_id",
            )
        ]

    if not isinstance(target, str):
        return [
            Issue(
                file=file_name,
                step_id=step_id,
                severity="critical",
                category="next_node",
                path=path,
                message=f"目标节点类型非法: {type(target).__name__}",
                recommendation="改为字符串类型的 step_id 或 conclusion_id",
            )
        ]

    if target == "__NEED_FILL__":
        return [
            Issue(
                file=file_name,
                step_id=step_id,
                severity="critical",
                category="next_node",
                path=path,
                message="使用了占位值 __NEED_FILL__",
                recommendation="替换为合法的 step_id 或 conclusion_id",
            )
        ]

    issues: list[Issue] = []
    if target.startswith("step_") and target not in workflow_step_ids:
        issues.append(
            Issue(
                file=file_name,
                step_id=step_id,
                severity="critical",
                category="next_node",
                path=path,
                message=f"指向不存在的 step: {target}",
                recommendation="改为 workflow.yaml 中已声明的 step_id",
            )
        )
    elif target.startswith("CONCLUSION_") and target not in conclusion_ids:
        issues.append(
            Issue(
                file=file_name,
                step_id=step_id,
                severity="critical",
                category="next_node",
                path=path,
                message=f"指向不存在的 conclusion: {target}",
                recommendation="改为 workflow.yaml 中已声明的 conclusion_id",
            )
        )
    elif not target.startswith("step_") and not target.startswith("CONCLUSION_"):
        issues.append(
            Issue(
                file=file_name,
                step_id=step_id,
                severity="warning",
                category="next_node",
                path=path,
                message=f"目标节点命名不符合当前约定: {target}",
                recommendation="优先使用 step_... 或 CONCLUSION_... 命名",
            )
        )
    return issues

