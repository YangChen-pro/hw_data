#!/usr/bin/env python3
"""工作流 YAML 评估入口。"""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.yaml_eval import main


if __name__ == "__main__":
    raise SystemExit(main())
