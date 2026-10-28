#!/bin/bash
# Round-56 C1 falsification runner: build each fixture state in the scratch clone,
# then run the frozen C1 counter against it. Receipts land in $S/out.
set -u
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r56/T56W1CritC1
L=$S/lane
C=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c1/measure.py
BASE=981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1
mkdir -p "$S/out"

run() { # name rev
  local name=$1 rev=$2 w=$S/work-$1
  rm -rf "$w"; mkdir -p "$w"
  python3 "$C" --lane "$L" --rev "$rev" --work "$w" --explain > "$S/out/$name.txt" 2>"$S/out/$name.err"
  local rc=$?
  echo "=== $name exit=$rc rev=$rev"
  grep '^EXPLAIN' "$S/out/$name.txt" || true
  tail -1 "$S/out/$name.txt"
}

# E0: base, untouched clone
git -C "$L" checkout -f --detach "$BASE" >/dev/null 2>&1
run E0-base "$BASE"

for st in del18 delfail row6 row6wrong repin fabricate unstable tamper; do
  rev=$(python3 "$S/build.py" "$st") || { echo "=== $st BUILD-FAILED"; continue; }
  run "$st" "$rev"
done

# E7: uncommitted working-tree tamper at base (REV stays the base commit)
python3 "$S/build.py" wttamper >/dev/null
run wttamper "$BASE"

echo "ALL-DONE"
