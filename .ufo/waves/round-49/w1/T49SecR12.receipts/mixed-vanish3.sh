#!/bin/sh
n=$(cat ctr 2>/dev/null || echo 0)
n=$((n+1))
printf '%s' "$n" > ctr
echo "run$n"
if [ "$n" = 2 ]; then chmod -x "$0"; fi
