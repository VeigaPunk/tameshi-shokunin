#!/usr/bin/env bash
# Descendant-commit + fuzz tests for the three receipt-gate registry rows.
# Runs in a scratch clone only; never in the lane.
set -u
S=/fast/scratch/hyaku/tameshi-r57/T57W2RevSkillTruth
D=$S/desc
C0=ca75c2674645ab6bdadeecb8584007c74342bfa9
BASE=5e3569969b532310d2b8a3d130901757a3df356b
RECV=c34e2b1486714ad6c1c6cbe706599ddfc9d60d55

top=$(git -C "$D" rev-parse --show-toplevel)
[ "$top" = "$(cd "$D" && pwd -P)" ] || { echo "TOPLEVEL_FAIL $top"; exit 2; }
echo "TOPLEVEL_OK $top"

run_rows () {   # $1 = rev label, $2 = rev
  echo "--- rows at $1 ($2)"
  ( cd "$D" && python3 tools/registry-check.py --rev "$2" --tag new-r57 ); echo "   rc=$?"
}

echo "=== A. baseline at C0"
run_rows C0 "$C0"

echo
echo "=== B. descendant commit that touches an UNRELATED file"
git -C "$D" checkout -q --detach "$C0"
echo "unrelated change $(date +%s%N)" > "$D/corpus/UNRELATED-TOUCH.txt"
git -C "$D" add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "descendant: unrelated file"
DE1=$(git -C "$D" rev-parse HEAD)
echo "descendant1=$DE1"
echo "  base resolvable in descendant? $(git -C "$D" rev-parse --verify --quiet "$BASE^{commit}" || echo NO)"
echo "  receipt rev resolvable?      $(git -C "$D" rev-parse --verify --quiet "$RECV^{commit}" || echo NO)"
run_rows DESC-UNRELATED "$DE1"

echo
echo "=== C. descendant commit that CHANGES the drift surface corpus/lessons/round-56-verifier-spotcheck.md"
echo "appended drift-surface text $(date +%s%N)" >> "$D/corpus/lessons/round-56-verifier-spotcheck.md"
git -C "$D" add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "descendant: change the drift surface"
DE2=$(git -C "$D" rev-parse HEAD)
echo "descendant2=$DE2"
run_rows DESC-DRIFT-SURFACE "$DE2"

echo
echo "=== C2. same, but the drift surface is DELETED"
git -C "$D" rm -q corpus/lessons/round-56-verifier-spotcheck.md
git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "descendant: delete the drift surface"
DE3=$(git -C "$D" rev-parse HEAD)
echo "descendant3=$DE3"
run_rows DESC-DRIFT-DELETED "$DE3"

echo
echo "=== C3. same, but the drift PATHS FIXTURE is edited to name another path"
git -C "$D" checkout -q --detach "$C0"
printf 'corpus/UNRELATED-TOUCH.txt\n' > "$D/tools/fixtures/receipt-gate/drift.paths"
git -C "$D" add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "descendant: repoint the drift paths fixture"
DE4=$(git -C "$D" rev-parse HEAD)
echo "descendant4=$DE4"
run_rows DESC-DRIFT-PATHS-EDITED "$DE4"

echo
echo "=== D. history rewrite: rebase-drop the round-56 commits the rows pin"
git -C "$D" checkout -q --detach "$C0"
git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q --allow-empty -m "empty descendant"
DE5=$(git -C "$D" rev-parse HEAD)
# simulate "the pinned revs became unreachable": build an orphan branch without them
git -C "$D" checkout -q --orphan orphan-test
git -C "$D" rm -rq --cached . 2>/dev/null
git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit -q --allow-empty -m "orphan without pinned history"
ORPH=$(git -C "$D" rev-parse HEAD)
echo "orphan=$ORPH"
run_rows ORPHAN-NO-PINNED-HISTORY "$ORPH"
