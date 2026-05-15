"""Shared constants for YAML quality scoring."""

from __future__ import annotations

import re


GUIDE_DIMENSIONS = [
    ("schema", "输入 Schema 完整性"),
    ("topology", "骨架拓扑一致性"),
    ("step", "Step 内容完整性"),
    ("skill", "Skill 与抽取字段"),
    ("condition", "条件表达式质量"),
    ("fallback", "错误兜底与可执行性"),
]

EXTRACTED_REF_RE = re.compile(r"\bextracted\.([A-Za-z0-9_]+)(?:\.([A-Za-z0-9_]+))?\b")
INPUT_REF_RE = re.compile(r"\binput\.(facts|current_hop)\.([A-Za-z0-9_]+)\b")
STATE_REF_RE = re.compile(r"\bstate(?:\.results)?\.(step_[A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\b")
STEP_ID_RE = re.compile(r"^step_[0-9]+[a-z]?_[a-z0-9_]+$")
GENERIC_TEXT_RE = re.compile(r"待填|待完善|TODO|__NEED_FILL__|未填")
