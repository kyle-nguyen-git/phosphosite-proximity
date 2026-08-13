#!/usr/bin/env bash
# Rebuild every panel and both figures from scratch. Clearing out/ first is what stops a
# partial rebuild from composing a figure out of mixed-vintage panels with no trace.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf out && mkdir -p out
# Inherit the pipeline's interpreter and font cache when run from phase0_5/run_all.sh;
# fall back to a standalone default when run by hand.
PYTHON_BIN="${PYTHON_BIN:-python3}"
: "${MPLCONFIGDIR:=$(mktemp -d)}"
export MPLCONFIGDIR
for f in src/p1a_cohort_flow.py src/p1b_roc.py src/p2a_ecdf.py \
         src/p2b_pae_scatter.py src/p2c_confidence_forest.py \
         src/p2d_sensitivity_forest.py; do
  PYTHONPATH=src "$PYTHON_BIN" "$f"
done
"$PYTHON_BIN" compose.py
