#!/usr/bin/env bash
# R93SN1 probe 10: (a) empty --rev reads the INDEX (git ':path' semantics);
#                  (b) the driver's control states are built from the lane WORKING TREE,
#                      while the clone is checked out at --rev.
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe10.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
probe() { printf 'PROBE %-50s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "L1 git ':path' (empty rev) reads the INDEX, not a commit"
git init -q "$S/idx"
git -C "$S/idx" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
printf 'COMMITTED\n' > "$S/idx/f.txt"
git -C "$S/idx" add f.txt && git -C "$S/idx" -c user.name=t -c user.email=t@t commit -q -m c1
printf 'STAGED-BUT-NOT-COMMITTED\n' > "$S/idx/f.txt"
git -C "$S/idx" add f.txt
probe "L1.commit-versions" "$(git -C "$S/idx" cat-file blob HEAD:f.txt)"
probe "L1.index-version(:path)" "$(git -C "$S/idx" cat-file blob :f.txt)"

sec "L2 the counter with --rev '' measures the INDEX of the lane"
mkdir -p "$S/wL2"
python3 -I "$LANE/.ufo/evidence/round-93/c1/measure-v93.py" --repo "$LANE" --rev "" --work "$S/wL2" >"$S/l2.log" 2>&1
probe "L2.rc" "$?"
probe "L2.PASS" "$(grep '^C1_R93_PASS' "$S/l2.log")"
probe "L2.summary-rev-field" "$(grep '^C1_SUMMARY' "$S/l2.log" | grep -o 'rev=[^ ]*')"

sec "L3 driver control states are built from the lane WORKING TREE, not from --rev"
git clone -q --shared --no-checkout "$LANE" "$S/laneL" 2>/dev/null
git -C "$S/laneL" checkout -q --detach "$REV" 2>/dev/null
# make the working tree's NOTE differ from the rev's NOTE
printf '\nWORKING-TREE-ONLY-MARKER\n' >> "$S/laneL/corpus/knowledge/mutation-case-fleet-sources-census.md"
mkdir -p "$S/wL3" "$S/oL3"
python3 -I "$LANE/.ufo/evidence/round-93/c1/controls-v93.py" --lane "$S/laneL" --rev "$REV" \
  --base "$REV" --work "$S/wL3" --outdir "$S/oL3" --only pos-real --jobs 1 >"$S/l3.log" 2>&1
probe "L3.driver-rc" "$?"
probe "L3.receipt-note-has-worktree-marker" "$(grep -c 'WORKING-TREE-ONLY-MARKER' "$S/oL3/pos-real.out" 2>/dev/null)"
probe "L3.receipt-note-has-rev-marker" "$(grep -c 'WORKING-TREE-ONLY-MARKER' "$S/oL3/pos-real.out" 2>/dev/null) (the rev's note has none)"
probe "L3.cloned-fixture-note-has-marker" "$(find "$S/wL3" -name 'mutation-case-fleet-sources-census.md' -exec grep -c 'WORKING-TREE-ONLY-MARKER' {} \; 2>/dev/null | tr '\n' ' ')"
probe "L3.receipt-verdict-tables" "$(grep -o 'verdict_tables=[0-9]*' "$S/oL3/pos-real.out" | head -1)"
probe "L3.PASS-line" "$(grep '^C1_R93_PASS' "$S/oL3/pos-real.out" 2>/dev/null)"

sec "L4 same, but the working-tree note is mutated to a HOSTILE shape (extra verdict table)"
printf '\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n| C001 | x | y | KILLED | differs |\n' \
  >> "$S/laneL/corpus/knowledge/mutation-case-fleet-sources-census.md"
mkdir -p "$S/wL4" "$S/oL4"
python3 -I "$LANE/.ufo/evidence/round-93/c1/controls-v93.py" --lane "$S/laneL" --rev "$REV" \
  --base "$REV" --work "$S/wL4" --outdir "$S/oL4" --only pos-real --jobs 1 >"$S/l4.log" 2>&1
probe "L4.driver-rc" "$?"
probe "L4.PASS-line" "$(grep '^C1_R93_PASS' "$S/oL4/pos-real.out" 2>/dev/null)"
probe "L4.verdict-tables" "$(grep -o 'verdict_tables=[0-9]*' "$S/oL4/pos-real.out" | head -1)"
probe "L4.note-the-control-was-supposed-to-certify" "the committed note at REV (not the working tree)"

printf '\n===== done =====\n'
