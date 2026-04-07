"""HTML 渲染。"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def _escape_json_for_script(data: str) -> str:
    return data.replace("</", "<\\/")


def _escape_html_text(value: Any) -> str:
    return html.escape(str(value), quote=True)


def render_html(template_path: Path, viewer_data: dict[str, Any]) -> str:
    template = template_path.read_text(encoding="utf-8")
    data_json = _escape_json_for_script(json.dumps(viewer_data, ensure_ascii=False))
    page_title = _escape_html_text(viewer_data["meta"]["name"])
    page_subtitle = _escape_html_text(viewer_data["meta"]["workflow_path"])
    return (
        template.replace("__WORKFLOW_VIEWER_DATA__", data_json)
        .replace("__PAGE_TITLE__", page_title)
        .replace("__PAGE_SUBTITLE__", page_subtitle)
    )


def write_html(output_path: Path, template_path: Path, viewer_data: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(template_path, viewer_data), encoding="utf-8")
