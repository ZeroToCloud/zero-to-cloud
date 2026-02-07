#!/usr/bin/env bash
# Zero2Cloud terminal MOTD banner

# Only show for interactive shells
[[ $- != *i* ]] && return 0

TIPS_FILE="$HOME/zero_to_cloud/motd/z2c_tips.txt"

clear

cat <<'ASCII'
==================================================
        Z E R O   T O   C L O U D
==================================================
ASCII

echo "Host: $(hostname)   User: $USER   Time: $(date '+%Y-%m-%d %H:%M:%S')"

CACHE="$HOME/.cache/z2c_weather.txt"
mkdir -p "$HOME/.cache"

# refresh cache if missing or older than 30 minutes
if [[ ! -f "$CACHE" || $(find "$CACHE" -mmin +30 2>/dev/null | wc -l) -gt 0 ]]; then
  curl -4 -sS -L --max-time 2 -A "Mozilla/5.0" "https://wttr.in/Tofino?format=3" > "$CACHE" 2>/dev/null || true
fi

WEATHER=$(tr -d '\r\n' < "$CACHE" 2>/dev/null)
echo "Weather: ${WEATHER:-Unavailable}"

echo


echo

if [[ -f "$TIPS_FILE" ]]; then
  tip=$(grep -vE '^\s*(#|$)' "$TIPS_FILE" | shuf -n 1)
  echo "Today's rep:"
  echo "  $tip"
else
  echo "Tip file not found: $TIPS_FILE"
fi

echo
echo "Wisdom of the session:"
fortune


echo "--------------------------------------------------"
