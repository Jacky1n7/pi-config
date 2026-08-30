#!/usr/bin/env bash
# Deprecated: unattended `pi update --all` was intentionally removed.
set -euo pipefail
cat <<'EOF'
Unattended all-package updates are disabled for reproducibility and supply-chain safety.
Pi core is intentionally unpinned and should track the latest stable release.

Use:
  ./update.sh --self     # update Pi core only
  ./update.sh            # read-only extension/config drift check
  ./update.sh --apply    # reconcile extensions/config to repository-pinned versions

Upgrade extension pins through a reviewed pi-config commit, then run the checks again.
EOF
