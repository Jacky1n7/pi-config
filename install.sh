#!/usr/bin/env bash
# Transactional, pinned Pi workflow installer. Dry-run unless --apply is passed.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/scripts/pi_config.py" apply-global "$@"
