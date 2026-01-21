#!/usr/bin/env bash
set -euo pipefail

DIR="$HOME/zero_to_cloud/syscheck/netcheck"

FILES=($(ls -1 "$DIR"/netcheck_*.txt 2>/dev/null | sort))
COUNT="${#FILES[@]}"

if [ "$COUNT" -lt 2 ]; then
  echo "❌ Need at least 2 netcheck reports to compare."
  echo "Found: $COUNT"
  echo "Tip: run 'netcheck' again (now that filenames include time) and then run 'diffcheck'."
  exit 1
fi

OLD="${FILES[$COUNT-2]}"
NEW="${FILES[$COUNT-1]}"

echo "=============================="
echo "ZERO2CLOUD DIFFCHECK"
echo "OLD: $OLD"
echo "NEW: $NEW"
echo "=============================="
echo

diff -u "$OLD" "$NEW" || true
