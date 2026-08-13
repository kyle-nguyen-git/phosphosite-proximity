#!/usr/bin/env bash
set -euo pipefail

PHASE05_DIR="$(cd "$(dirname "$0")" && pwd)"
PHASE0_DIR="$(cd "$PHASE05_DIR/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
export MPLCONFIGDIR="${TMPDIR:-/tmp}/robustness_matplotlib"
mkdir -p "$MPLCONFIGDIR"

if [[ -n "${SOURCE_ARCHIVE:-}" ]]; then
    "$PYTHON_BIN" "$PHASE0_DIR/tools/fetch_sources.py" --archive "$SOURCE_ARCHIVE"
else
    "$PYTHON_BIN" "$PHASE0_DIR/tools/fetch_sources.py"
fi
"$PYTHON_BIN" "$PHASE0_DIR/tools/verify_third_party_cache.py"
"$PYTHON_BIN" "$PHASE0_DIR/src/01_build_sites.py"
"$PYTHON_BIN" "$PHASE0_DIR/src/02_structures.py"
"$PYTHON_BIN" "$PHASE0_DIR/src/03_analysis.py"
"$PYTHON_BIN" "$PHASE0_DIR/src/04_figure.py"
"$PYTHON_BIN" "$PHASE05_DIR/src/01_build_robustness_dataset.py"
"$PYTHON_BIN" "$PHASE05_DIR/src/02_robustness_analysis.py"
"$PYTHON_BIN" "$PHASE05_DIR/src/03_robustness_figure.py"
"$PYTHON_BIN" "$PHASE05_DIR/src/04_build_release_artifacts.py"
# Panel-composed figures for the editable manuscript. Must precede the two
# verifiers below, which hash the release tree including these outputs.
"$PHASE0_DIR/manuscript/panels/build_all.sh"
"$PYTHON_BIN" "$PHASE0_DIR/manuscript/src/build_figure1.py"
"$PYTHON_BIN" "$PHASE0_DIR/manuscript/src/build_preprint_pdf.py"
"$PYTHON_BIN" "$PHASE0_DIR/manuscript/src/render_preprint.py"
"$PYTHON_BIN" "$PHASE05_DIR/src/04_verify_release.py"
"$PYTHON_BIN" "$PHASE0_DIR/tools/verify_release_package.py"
