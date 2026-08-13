#!/usr/bin/env bash
set -euo pipefail

PHASE0_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$PHASE0_DIR/phase0_5/run_all.sh"
