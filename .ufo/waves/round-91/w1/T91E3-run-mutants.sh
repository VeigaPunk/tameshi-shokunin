#!/bin/bash
set -u
S=/fast/scratch/hyaku/tameshi-r91/T91E3
ARMED="$S/armed.sh"
LOG="$S/work/T91E3.log"
mkdir -p "$S/work/runs"
run_mutant() { # id, old, new  (old/new passed via env file to avoid quoting pain)
  local id=$1 old=$2 new=$3
  local d="$S/work/runs/$id"
  mkdir -p "$d/scripts/fixtures"
  cp -r "$S/g/scripts/fixtures/sources-census" "$d/scripts/fixtures/"
  python3 -I - "$ARMED" "$d/scripts/sources-census.sh" "$old" "$new" <<'PY'
import sys
src, dst, old, new = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
t = open(src).read()
assert t.count(old) == 1, f"old-string count {t.count(old)} for {old!r}"
open(dst, "w").write(t.replace(old, new))
PY
  chmod 755 "$d/scripts/sources-census.sh"
  bash -n "$d/scripts/sources-census.sh" || { echo "$id SYNTAX-FAIL"; return; }
  bash "$d/scripts/sources-census.sh" selftest > "$d/out.txt" 2>&1
  local rc=$?
  local surv arm survlines
  surv=$(grep -c '^killed' "$d/out.txt")
  arm=$(grep '^SURVIVED' "$d/out.txt" || true)
  echo "=== $id exit=$rc killed=$surv ===" >> "$LOG"
  grep -E '^SURVIVED|selftest (ok|FAILED)' "$d/out.txt" >> "$LOG" || true
  echo "--- $id exit=$rc survived-arm-lines:" >> "$LOG"
  printf '%s\n' "$arm" >> "$LOG"
}
run_mutant C01 'if (tier=="A" && kind=="community")' 'if (tier=="A" && kind=="communityX")'
run_mutant C02 'length(teaches)<8' 'length(teaches)<7'
run_mutant C03 'teaches !~ /supersedes S[0-9]{3}/' 'teaches !~ /supersedes S[0-9]{4}/'
run_mutant C04 'if (due!=INVALID_EPOCH && due<=today_s)' 'if (due!=INVALID_EPOCH && due<today_s)'
run_mutant C05 'opened_epoch>today_s)' 'opened_epoch>=today_s)'
run_mutant C06 'if (c !~ /^:?-+:?$/) return 0' 'if (c !~ /^-+$/) return 0'
run_mutant C07 'if (line !~ /^ {0,3}\|/) next' 'if (line !~ /^ {0,2}\|/) next'
run_mutant C08 'if [ ! -e "$dir/$path" ]; then' 'if [ ! -f "$dir/$path" ]; then'
run_mutant C09 'sub(/#[^ ]*$/,"",u)' 'sub(/#[^ ]*$/,"&",u)'
run_mutant C10 'function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ }' 'function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9_-]*$/ }'
run_mutant C11 '[ "$missing_error" = 1 ] && exit 2' '[ "$missing_error" = 1 ] && exit 1'
run_mutant C12 '      path=$(trim_cell "$path")' '      path=$path'
