#!/usr/bin/env bash
# Deprecated: unattended `pi update --all` was intentionally removed.
set -euo pipefail
cat <<'EOF'
Unattended upstream updates are disabled for reproducibility and supply-chain safety.

Use:
  ./update.sh            # read-only drift/health check
  ./update.sh --apply    # reconcile to repository-pinned versions

Upgrade pins through a reviewed pi-config commit, then run the checks again.
EOF
