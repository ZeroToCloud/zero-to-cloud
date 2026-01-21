#!/usr/bin/env bash
set -e

echo " ________________"
echo "|   ZERO2CLOUD   |"
echo "|  SYS CHECK ✅  |"
echo "|________________|"
echo
echo "Time: $(date)"
echo

echo "[User / Host]"
echo "User: $(whoami)"
echo "Host: $(hostname)"
echo

echo "[OS]"
uname -a
echo

echo "[Docker]"
docker --version 2>/dev/null || echo "docker: not installed in container"
echo

echo "[CPU]"
lscpu | grep -E 'Model name|CPU\(s\)|Thread|Core|Socket' || true
echo

echo "[Memory]"
free -h || true
echo

echo "[Disk]"
echo "Linux / :"
df -h / || true
echo
if [ -d /mnt/c ]; then
  echo "Windows C: (/mnt/c):"
  df -h /mnt/c || true
  echo
fi


echo "[IP]"
IP_ADDR="$(hostname -I 2>/dev/null | awk '{print $1}')"
if [ -n "$IP_ADDR" ]; then
  echo "$IP_ADDR"
else
  echo "No IP found ⚠️"
fi
echo

echo "[Online?]"
if command -v curl >/dev/null 2>&1; then
  curl -4 -s --max-time 3 https://example.com >/dev/null && echo "Online ✅" || echo "Offline ⚠️"
else
  echo "curl not installed ⚠️"
fi
echo




echo "=============================="
echo "      Z2C READY 🚀"
echo "=============================="
