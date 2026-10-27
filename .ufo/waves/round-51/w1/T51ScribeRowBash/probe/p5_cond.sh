#!/usr/bin/env bash
set -euo pipefail
verify() {
  local actual p="$PWD/f.txt" ere='^zzz$'
  actual=$(grep -nE -m1 -- "$ere" "$p" | cut -d: -f1)
  printf 'MOVED   %s:1->%s (continues: -e ignored in this context)\n' "$p" "$actual"
  return 1
}
rc=0; verify || rc=$?
printf 'REACHED-END rc=%s\n' "$rc"
