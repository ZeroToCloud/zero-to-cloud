#!/usr/bin/env bash

echo "=============================="
echo "        Z2C NETWATCH"
echo "=============================="

echo
echo "🧑 Logged-in users:"
who

echo
echo "🌐 Interfaces:"
ip -brief addr

echo
echo "🚪 Default route:"
ip route | grep default

echo
echo "🧭 DNS servers:"
grep nameserver /etc/resolv.conf

echo
echo "📡 Listening ports:"
ss -tulpen | grep LISTEN

echo
echo "🌍 Internet test:"
ping -c 1 1.1.1.1 >/dev/null 2>&1 && echo "Internet reachable" || echo "Internet DOWN"

echo
echo "=============================="

