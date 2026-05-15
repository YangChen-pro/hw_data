#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export MPLCONFIGDIR="${MPLCONFIGDIR:-/private/tmp/hw_data_matplotlib}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/private/tmp/hw_data_matplotlib}"

conda run -n claw python -X utf8 "${ROOT_DIR}/tools/yaml_quality_score.py" "$@"
