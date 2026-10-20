#!/bin/sh
# Designed counterexample only; not executed by this seat.
# Pass one persistent state-file path. With an absent state file, runs 1-3
# have the exact same control tuple; run 4 differs despite unchanged script.
state=$1
n=0
if [ -f "$state" ]; then
  IFS= read -r n < "$state"
fi
n=$((n + 1))
printf '%s\n' "$n" > "$state"
if [ "$n" -le 3 ]; then
  printf 'CONTROL: GREEN\n'
  exit 0
fi
printf 'CONTROL: FLAKE\n'
exit 1
