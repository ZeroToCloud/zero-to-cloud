#!/usr/bin/env bash
set -euo pipefail
DIR="$HOME/zero_to_cloud/syscheck/audit/reports"
latest="$(ls -1t "$DIR"/audit_*.txt 2>/dev/null | head -n 1 || true)"
prev="$(ls -1t "$DIR"/audit_*.txt 2>/dev/null | head -n 2 | tail -n 1 || true)"

if [ -z "${latest:-}" ] || [ -z "${prev:-}" ] || [ "$latest" = "$prev" ]; then
  echo "Need at least two audit reports to diff."
  exit 1
fi

echo "=============================="
echo "Z2C AUDIT DIFF"
echo "OLD: $prev"
echo "NEW: $latest"
echo "=============================="
echo
diff -u "$prev" "$latest" | less
