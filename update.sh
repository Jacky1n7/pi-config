#!/usr/bin/env bash
# Reconcile to repository locks; never resolves upstream latest versions.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "${1:-}" == "--apply" ]]; then
  shift
  exec python3 "$SCRIPT_DIR/scripts/pi_config.py" apply-global --apply "$@"
fi
exec python3 "$SCRIPT_DIR/scripts/pi_config.py" check --installed "$@"
