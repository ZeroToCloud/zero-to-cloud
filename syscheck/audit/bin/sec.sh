#!/usr/bin/env bash
set -euo pipefail

echo "=============================="
echo "Z2C SECURITY QUICK CHECK"
echo "Date: $(date)"
echo "Host: $(hostname)"
echo "=============================="
echo

echo "== Listening ports =="
ss -tuln
echo

echo "== Sudo group =="
getent group sudo || true
echo

echo "== Recent sudo/auth failures (last 20) =="
if [ -f /var/log/auth.log ]; then
  grep -Ei 'sudo: pam_unix\(sudo:auth\): authentication failure|Failed password|Invalid user' /var/log/auth.log | tail -n 20 || true
else
  echo "(no /var/log/auth.log found)"
fi
echo

echo "== Recent system warnings/errors (last 30) =="

tail -n 400 /var/log/syslog 2>/dev/null \
  | grep --color=always -Ei "warn|error|fail|denied" \
  | grep -Ev "wsl-pro-service|dxgk|CDI directory does not exist|nftables|PackageKit|cups\.cupsd" \
  | tail -n 30 || echo "(no matches after filtering common noise)"

echo
