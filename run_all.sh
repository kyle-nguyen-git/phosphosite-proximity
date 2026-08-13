#!/usr/bin/env bash
set -euo pipefail

PHASE0_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$PHASE0_DIR/robustness/run_all.sh"
