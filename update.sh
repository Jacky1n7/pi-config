#!/usr/bin/env bash
# Keep Pi core current while reconciling extensions and configuration to repository locks.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "${1:-}" == "--self" ]]; then
  shift
  pi update --self "$@"
  PI_ZH_APPLY="${PI_ZH_APPLY:-$HOME/pi-zh-pi-coding-agent/pi-zh-apply.py}"
  if [[ -f "$PI_ZH_APPLY" ]]; then
    python3 "$PI_ZH_APPLY"
  else
    echo "Pi 中文补丁未找到，跳过: $PI_ZH_APPLY"
  fi
  exit 0
fi
if [[ "${1:-}" == "--apply" ]]; then
  shift
  exec python3 "$SCRIPT_DIR/scripts/pi_config.py" apply-global --apply "$@"
fi
exec python3 "$SCRIPT_DIR/scripts/pi_config.py" check --installed "$@"
