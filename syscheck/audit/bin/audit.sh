#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%F_%H-%M-%S)"
BASE="$HOME/zero_to_cloud/syscheck/audit"
OUTDIR="$BASE/reports"
OUT="$OUTDIR/audit_$TS.txt"

mkdir -p "$OUTDIR"

run() {
  echo "\$ $*"
  "$@" 2>&1 || echo "(command failed: $*)"
  echo
}

{
  echo "=================================================="
  echo "        Z E R O 2 C L O U D   A U D I T"
  echo "=================================================="
  echo "Date: $(date)"
  echo "Host: $(hostname)"
  echo "User: $(whoami)"
  echo

  echo "== SYSTEM =="
  run uname -a
  run uptime
  run bash -lc "command -v lsb_release >/dev/null 2>&1 && lsb_release -a || echo '(lsb_release not available)'"
  echo

  echo "== CPU / MEMORY =="
  run free -h
  run bash -lc "command -v vmstat >/dev/null 2>&1 && vmstat 1 2 | tail -n 1 || echo '(vmstat not installed)'"
  echo

  echo "== DISK =="
  run df -hT
  run bash -lc "du -sh \$HOME 2>/dev/null | sed 's#^#HOME usage: #' || true"
  echo

  echo "== TOP PROCESSES (CPU/MEM) =="
  run bash -lc "ps aux --sort=-%cpu | head -n 8"
  run bash -lc "ps aux --sort=-%mem | head -n 8"
  echo

  echo "== NETWORK =="
  run ip -br addr
  run ip route
  echo

  echo "== LISTENING PORTS =="
  run ss -tuln
  echo

  echo "== LOGGED IN USERS =="
  run who
  echo

  echo "== AUTH / SECURITY QUICK LOOK =="
  if [ -f /var/log/auth.log ]; then
    echo "Recent sudo/auth failures (last 20):"
    run bash -lc "grep -Ei 'sudo: pam_unix\\(sudo:auth\\): authentication failure|Failed password|Invalid user' /var/log/auth.log | tail -n 20"
    echo "Service timeouts/errors (last 10):"
    run bash -lc "grep -Ei 'timed out|timeout|failed to activate service' /var/log/auth.log | tail -n 10"
  else
    echo "(no /var/log/auth.log found)"
    echo
  fi

  echo "Sudo group:"
  run getent group sudo
  echo

  echo "== SERVICES (systemd) =="
  run systemctl --no-pager --failed
  echo

  echo "== DOCKER (if installed) =="
  if command -v docker >/dev/null 2>&1; then
    run docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
  else
    echo "(docker not installed)"
    echo
  fi

  echo "== YOUR Z2C NETCHECK =="
  if [ -x "$HOME/zero_to_cloud/syscheck/netcheck/netcheck.sh" ]; then
    echo "(Running netcheck...)"
    run "$HOME/zero_to_cloud/syscheck/netcheck/netcheck.sh"
  else
    echo "(netcheck script not found/executable at ~/zero_to_cloud/syscheck/netcheck/netcheck.sh)"
    echo
  fi

  echo "=================================================="
  echo "Saved: $OUT"
  echo "=================================================="
} | tee "$OUT" 
