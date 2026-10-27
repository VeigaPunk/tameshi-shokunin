#!/usr/bin/env bash
set -euo pipefail
printf 'alpha\nbeta\n' > "$PWD/f.txt"
actual=$(grep -nE -m1 -- '^zzz$' "$PWD/f.txt" | cut -d: -f1)
printf 'AFTER-ASSIGN actual=[%s]\n' "$actual"
printf 'REACHED-END\n'
