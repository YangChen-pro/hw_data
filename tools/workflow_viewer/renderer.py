"""HTML 渲染。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _escape_json_for_script(data: str) -> str:
    return data.replace("</", "<\\/")


def render_html(template_path: Path, viewer_data: dict[str, Any]) -> str:
    template = template_path.read_text(encoding="utf-8")
    data_json = _escape_json_for_script(json.dumps(viewer_data, ensure_ascii=False))
    return (
        template.replace("__WORKFLOW_VIEWER_DATA__", data_json)
        .replace("__PAGE_TITLE__", viewer_data["meta"]["name"])
        .replace("__PAGE_SUBTITLE__", viewer_data["meta"]["workflow_path"])
    )


def write_html(output_path: Path, template_path: Path, viewer_data: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(template_path, viewer_data), encoding="utf-8")

