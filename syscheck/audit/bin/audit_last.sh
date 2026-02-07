#!/usr/bin/env bash
set -euo pipefail
DIR="$HOME/zero_to_cloud/syscheck/audit/reports"
latest="$(ls -1t "$DIR"/audit_*.txt 2>/dev/null | head -n 1 || true)"
if [ -z "${latest:-}" ]; then
  echo "No audit reports found in $DIR"
  exit 1
fi
echo "Latest: $latest"
echo
tail -n 80 "$latest"
