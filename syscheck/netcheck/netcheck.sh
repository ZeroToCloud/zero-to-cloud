#!/usr/bin/env bash
set -euo pipefail

OUTDIR="$HOME/zero_to_cloud/syscheck/netcheck"
DATESTAMP="$(date +%F_%H-%M-%S)"
OUTFILE="$OUTDIR/netcheck_${DATESTAMP}.txt"

mkdir -p "$OUTDIR"

{
echo "=================================================="
echo "   ____                  ______    ________          __ "
echo "  /_  /  ___  _________ /_  __/___/_  __/ /___  ____/ / "
echo "   / /  / _ \/ ___/ __ \ / / / __ \/ / / / __ \/ __  /  "
echo "  / /__/  __/ /  / /_/ // / / /_/ / / / / /_/ / /_/ /   "
echo " /____/\___/_/   \____//_/  \____/_/ /_/\____/\__,_/    "
echo "                 Z E R O   T O   C L O U D              "
echo "=================================================="
echo ""

date
echo ""


  echo "=============================="
  echo "ZERO2CLOUD NETCHECK"
  echo "Date: $(date)"
  echo "Host: $(hostname)"
  echo "User: $(whoami)"
  echo "=============================="
  echo

  echo "### IP / ROUTES"
  ip a || true
  echo
  ip route || true
  echo

  echo "### DNS (resolv.conf)"
  cat /etc/resolv.conf || true
  echo

  echo "### QUICK CONNECTIVITY"
  echo "- Gateway ping (if available):"
  GATEWAY="$(ip route | awk '/default/ {print $3; exit}')"
  if [ -n "${GATEWAY:-}" ]; then
    echo "Gateway: $GATEWAY"
    ping -c 2 "$GATEWAY" || true
  else
    echo "No gateway found."
  fi
  echo

  echo "- Public IP ping test (basic):"
  ping -c 2 1.1.1.1 || true
  echo

  echo "- DNS test (cloudflare.com):"
  getent hosts cloudflare.com || true
  echo

  echo "### RECENT LAN DEVICES (ARP table)"
  ip neigh || true
  echo
  echo "### WINDOWS NETWORK (via PowerShell)"
  if command -v powershell.exe >/dev/null 2>&1; then
    echo "- Windows default gateway:"
    powershell.exe -NoProfile -Command "Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Sort-Object RouteMetric | Select-Object -First 1 -ExpandProperty NextHop" 2>/dev/null || true
    echo

    echo "- Windows IP config (summary):"
    powershell.exe -NoProfile -Command "ipconfig | Select-String 'Adapter|IPv4 Address|Default Gateway|DNS Servers'" 2>/dev/null || true

    echo ""

    echo ""
    echo "===== WINDOWS NET IP CONFIG (FULL) ====="
    powershell.exe -NoProfile -Command "Get-NetIPConfiguration | Format-List" 2>/dev/null || true

    echo ""
    echo "===== WINDOWS IPCONFIG /ALL (FULL) ====="
    ipconfig.exe /all 2>/dev/null || true


    echo
    echo "=============================="
    echo "LISTENING PORTS (ss -tulpen)"
    echo "=============================="
    ss -tulpen || true


    echo

    echo "- Windows ARP table (LAN neighbors Windows has seen):"
    powershell.exe -NoProfile -Command "arp -a" 2>/dev/null || true
    echo
  else
    echo "powershell.exe not found (are you in WSL2 on Windows?)."
    echo
  fi


} > "$OUTFILE"

echo "✅ NetCheck saved to: $OUTFILE"
