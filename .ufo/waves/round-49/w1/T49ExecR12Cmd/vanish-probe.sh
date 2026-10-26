#!/bin/sh
# T49ExecR12Cmd M1 probe (round 49): self-deleting counter command.
# run 1 -> A, run 2 -> B, run 3 -> C then remove itself, run 4 -> cannot exec.
# Driven as: python3 tools/repeat-control.py --runs 4 --out $S/r12-mixed -- $S/probe/vanish.sh
# The script deletes itself on run 3, so this copy is the preserved source of the
# receipt I.txt / r12-mixed/run-{1..4}.* (it is not re-executed from this path).
n=0
[ -f "$0.count" ] && n=$(cat "$0.count")
n=$((n+1))
printf '%s\n' "$n" > "$0.count"
case "$n" in
  1) printf 'A\n' ;;
  2) printf 'B\n' ;;
  3) printf 'C\n'; rm -f "$0" ;;
  *) printf 'D\n' ;;
esac
exit 0
