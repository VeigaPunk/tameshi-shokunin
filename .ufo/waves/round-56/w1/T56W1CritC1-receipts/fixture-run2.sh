#!/bin/bash
set -u
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r56/T56W1CritC1
L=$S/lane
C=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c1/measure.py
run() { local name=$1 rev=$2 w=$S/work-$1; rm -rf "$w"; mkdir -p "$w"
  python3 "$C" --lane "$L" --rev "$rev" --work "$w" --explain > "$S/out/$name.txt" 2>"$S/out/$name.err"; local rc=$?
  echo "=== $name exit=$rc rev=$rev"; grep '^EXPLAIN' "$S/out/$name.txt" || true; tail -1 "$S/out/$name.txt"; }
for st in repin fabricate unstable tamper; do
  rev=$(python3 "$S/build.py" "$st") || { echo "=== $st BUILD-FAILED"; continue; }
  echo "BUILT $st $rev"
  run "$st" "$rev"
done
echo ALL-DONE
