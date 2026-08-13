#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" -c 'import sys; expected=(3, 12, 4); raise SystemExit(0 if sys.version_info[:3] == expected else f"CPython {expected[0]}.{expected[1]}.{expected[2]} is required; found {sys.version.split()[0]}")'
command -v pdftoppm >/dev/null || {
    echo "pdftoppm (Poppler) is required to render and verify the manuscript PDF" >&2
    exit 1
}
export PYTHON_BIN
exec "$ROOT_DIR/robustness/run_all.sh"
