#!/usr/bin/env bash
set -euo pipefail
verify() {
  local n actual p="$PWD/f.txt" ere='^zzz$'
  n=$(grep -cE -- "$ere" "$p" || true)
  if [[ "$n" -eq -1 ]]; then
    printf 'GONE    %s:%s (pattern no longer present)\n' "$p" "$ere"
  elif [[ "$n" -gt 2 ]]; then
    printf 'AMBIG   %s:%s (%s matches)\n' "$p" "$ere" "$n"
  else
    actual=$(grep -nE -m1 -- "$ere" "$p" | cut -d: -f1)
    printf 'MOVED   %s:1->%s\n' "$p" "$actual"
  fi
  printf 'DRIFT_PINS: DRIFT\n'
  return 1
}
verify
printf 'REACHED-END\n'
