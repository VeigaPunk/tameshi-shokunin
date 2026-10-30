#!/bin/bash
# Round-57 before receipts: the frozen counters against BASE + the frozen instruments (no new ledger rows).
# Usage: bash before-runs.sh   (writes .ufo/evidence/round-57/before/{c1,c2}.stdout)
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=5e3569969b532310d2b8a3d130901757a3df356b
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r57/L1-before
rm -rf "$S"; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT
E=.ufo/evidence/round-57

run_c1() {  # $1 = clone dir, $2 = out path
  local D=$1 OUT=$2 REV
  REV=$(git -C "$D" rev-parse HEAD)
  mkdir -p "$S/w1"
  python3 "$D/$E/c1/measure.py" --lane "$D" --rev "$REV" --work "$S/w1" --explain > "$OUT" 2>&1 || echo "counter exit=$? (expected: PASS=false)" >> "$OUT"
  echo "c1 rev=$REV exit=$?" >> "$OUT"
}

# ---- C1 before: BASE + frozen instruments, BASE ledger (rows=0/51 expected) ----
D=$S/c1b; git clone -q --shared "$LANE" "$D"
git -C "$D" checkout -q --detach "$BASE"
rm -rf "$D/$E"; cp -r "$LANE/$E" "$D/$E"
rm -rf "$D/$E/after" "$D/$E/before" "$D/$E/integrate"
git -C "$D" add -A && git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "before: BASE + frozen instruments"
run_c1 "$D" "$LANE/$E/before/c1.stdout"

# ---- C2 before: BASE + frozen instruments (gate absent at BASE) ----
D=$S/c2b; git clone -q --shared "$LANE" "$D"
git -C "$D" checkout -q --detach "$BASE"
rm -rf "$D/$E"; cp -r "$LANE/$E" "$D/$E"
rm -rf "$D/$E/after" "$D/$E/before" "$D/$E/integrate"
git -C "$D" add -A && git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "before: BASE + frozen instruments"
REV=$(git -C "$D" rev-parse HEAD)
mkdir -p "$S/w2"
TMPDIR="$S/w2" timeout 420 python3 "$D/$E/c2/measure.py" --lane "$D" --rev "$REV" --work "$S/w2/x" --explain > "$LANE/$E/before/c2.stdout" 2>&1 || echo "counter exit=$? (expected: PASS=false)" >> "$LANE/$E/before/c2.stdout"
echo "c2 rev=$REV exit=$?" >> "$LANE/$E/before/c2.stdout"
echo "before receipts written"
