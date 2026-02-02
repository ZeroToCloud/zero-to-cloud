#!/bin/bash
set -euo pipefail

DIR="$HOME/zero_to_cloud/syscheck/netcheck"

# Pick newest + previous netcheck logs
newest="$(ls -1t "$DIR"/netcheck_*.txt 2>/dev/null | sed -n '1p' || true)"
older="$(ls -1t "$DIR"/netcheck_*.txt 2>/dev/null | sed -n '2p' || true)"

if [ -z "${newest:-}" ]; then
  echo "❌ No netcheck logs found in: $DIR"
  exit 1
fi
if [ -z "${older:-}" ]; then
  echo "❌ Only one netcheck log exists. Run NetCheck again to compare two."
  echo "Found: $(basename "$newest")"
  exit 1
fi

tmp_old_ports="$(mktemp)"
tmp_new_ports="$(mktemp)"
tmp_old_ifaces="$(mktemp)"
tmp_new_ifaces="$(mktemp)"

cleanup() {
  rm -f "$tmp_old_ports" "$tmp_new_ports" "$tmp_old_ifaces" "$tmp_new_ifaces"
}
trap cleanup EXIT

# Extract ports from ss output embedded in the logs
extract_ports() {
  # Keep lines likely from `ss -tulpen`, then grab the "Local Address:Port" column (usually $5)
  # Includes TCP LISTEN and UDP UNCONN (so DNS etc still shows)
  grep -E '^(tcp|udp)\s' "$1" \
    | grep -E 'LISTEN|UNCONN' \
    | awk '{print $5}' \
    | sort -u
}

# Extract interfaces from ip output embedded in the logs
extract_ifaces() {
  # Looks for lines like: "1: lo:" or "2: eth0:"
  grep -E '^[0-9]+:\s+[a-zA-Z0-9_.:-]+:' "$1" \
    | sed -E 's/^[0-9]+:\s+([^:]+):.*/\1/' \
    | sort -u
}

extract_ports "$older"  > "$tmp_old_ports" || true
extract_ports "$newest" > "$tmp_new_ports" || true
extract_ifaces "$older"  > "$tmp_old_ifaces" || true
extract_ifaces "$newest" > "$tmp_new_ifaces" || true

echo "=== ZERO2CLOUD NETCHECK SUMMARY ==="
echo "Old: $(basename "$older")"
echo "New: $(basename "$newest")"
echo ""

echo "Ports ADDED:"
comm -13 "$tmp_old_ports" "$tmp_new_ports" | sed 's/^/ - /' | sed '/^- $/d'
echo ""

echo "Ports REMOVED:"
comm -23 "$tmp_old_ports" "$tmp_new_ports" | sed 's/^/ - /' | sed '/^- $/d'
echo ""

echo "Interfaces ADDED:"
comm -13 "$tmp_old_ifaces" "$tmp_new_ifaces" | sed 's/^/ - /' | sed '/^- $/d'
echo ""

echo "Interfaces REMOVED:"
comm -23 "$tmp_old_ifaces" "$tmp_new_ifaces" | sed 's/^/ - /' | sed '/^- $/d'
echo ""

echo "Summary:"
echo " Old ports:   $(wc -l < "$tmp_old_ports" | tr -d ' ')  ->  New ports:   $(wc -l < "$tmp_new_ports" | tr -d ' ')"
echo " Old ifaces:  $(wc -l < "$tmp_old_ifaces" | tr -d ' ')  ->  New ifaces:  $(wc -l < "$tmp_new_ifaces" | tr -d ' ')"
