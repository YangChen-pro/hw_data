#!/usr/bin/env python3
"""workflow HTML 查看器入口。"""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.workflow_viewer.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
