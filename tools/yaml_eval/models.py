"""评估器共用的数据模型和基础工具。"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


STATE_REF_RE = re.compile(r"\bstate(?:\.results)?\.(step_[A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\b")
EXTRACTED_REF_RE = re.compile(r"\bextracted\.([A-Za-z0-9_]+)\b")
INPUT_FACTS_RE = re.compile(r"\binput\.facts\.([A-Za-z0-9_]+)\b")
LEGACY_STATE_REF_RE = re.compile(r"\bstate\.step_[A-Za-z0-9_]+\.[A-Za-z0-9_]+\b")
PLACEHOLDER_HINT_RE = re.compile(
    r"[\u4e00-\u9fff]|来自|接口|地址|名称|参数|视图|序号|上一步|当前|对端|系统MAC|未填|待填|待办"
)


@dataclass(frozen=True)
class Issue:
    """单条评估问题。"""

    file: str
    step_id: str
    severity: str
    category: str
    path: str
    message: str
    recommendation: str
    line: int | None = None


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def natural_step_key(path: Path) -> tuple[int, str]:
    match = re.search(r"step_(\d+)_", path.name)
    return (int(match.group(1)) if match else 10**9, path.name)


def normalize_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def is_placeholder_text(text: str) -> bool:
    stripped = text.strip()
    return bool(stripped) and bool(PLACEHOLDER_HINT_RE.search(stripped))


def collect_references(condition: str) -> tuple[set[str], set[str], set[str]]:
    state_steps = {step_id for step_id, _ in STATE_REF_RE.findall(condition)}
    extracted_fields = set(EXTRACTED_REF_RE.findall(condition))
    input_fields = set(INPUT_FACTS_RE.findall(condition))
    return state_steps, extracted_fields, input_fields

