#!/bin/bash
# usage: run_counter.sh <branch> <rev>
set -u
S="$(cd "$(dirname "$0")" && pwd)"
branch="$1"; rev="$2"
W="$S/runs/$branch"; O="$S/out/$branch"
rm -rf -- "$W" "$O"; mkdir -p "$W" "$O"
t0=$(date +%s)
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/c2/measure.py \
  --lane "$S/mut" --rev "$rev" --work "$W" --explain \
  > "$O/verdict.out" 2> "$O/verdict.err"
rc=$?
t1=$(date +%s)
{ echo "branch=$branch rev=$rev rc=$rc elapsed_s=$((t1-t0))";
  grep '^C2_R55:' "$O/verdict.out";
  echo "--- bad map:";
  python3 -c "import json;d=json.load(open('$W/c2-receipts.json'));print(json.dumps(d['bad'],indent=1,sort_keys=True))" 2>&1;
  echo "--- stderr:"; cat "$O/verdict.err"; } > "$O/summary.txt" 2>&1
cat "$O/summary.txt"
