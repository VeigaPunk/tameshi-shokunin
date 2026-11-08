#!/usr/bin/env bash
# R93SN1 probe 16: does the driver's control state content come from the lane
# WORKING TREE rather than from --rev?
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe16.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CTRL="$LANE/.ufo/evidence/round-93/c1/controls-v93.py"
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
probe() { printf 'PROBE %-56s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "R1 hidden-c001 state: note content from the WORKING TREE or from --rev?"
git clone -q --shared --no-checkout "$LANE" "$S/lane" 2>/dev/null
git -C "$S/lane" checkout -q --detach "$REV" 2>/dev/null
# mutate ONLY the working tree (index/HEAD untouched)
printf '\n<!-- WORKTREE-ONLY-MARKER-R1 -->\n' >> "$S/lane/corpus/knowledge/mutation-case-fleet-sources-census.md"
probe "R1.worktree-differs-from-rev" "$(git -C "$S/lane" status --porcelain | head -2 | tr '\n' ' ')"
mkdir -p "$S/w" "$S/o"
python3 -I "$CTRL" --lane "$S/lane" --rev "$REV" --base "$REV" \
  --work "$S/w" --outdir "$S/o" --only hidden-c001 --jobs 1 >"$S/r1.log" 2>&1
probe "R1.driver-rc" "$?"
probe "R1.receipt-contains-worktree-marker" "$(grep -c 'WORKTREE-ONLY-MARKER-R1' "$S/o/hidden-c001.out" 2>/dev/null)"
probe "R1.receipt-verdict-tables" "$(grep -o 'verdict_tables=[0-9]*' "$S/o/hidden-c001.out" | head -1)"
probe "R1.receipt-C001-rows" "$(grep -c '^C1_ROW C001' "$S/o/hidden-c001.out" 2>/dev/null)"

sec "R2 same, but the working tree carries a HOSTILE note (extra verdict table)"
printf '\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n| C001 | x | y | KILLED | differs |\n' \
  >> "$S/lane/corpus/knowledge/mutation-case-fleet-sources-census.md"
mkdir -p "$S/w2" "$S/o2"
python3 -I "$CTRL" --lane "$S/lane" --rev "$REV" --base "$REV" \
  --work "$S/w2" --outdir "$S/o2" --only hidden-c001 --jobs 1 >"$S/r2.log" 2>&1
probe "R2.driver-rc" "$?"
probe "R2.receipt-verdict-tables" "$(grep -o 'verdict_tables=[0-9]*' "$S/o2/hidden-c001.out" | head -1)"
probe "R2.expected-at-rev" "verdict_tables=1 (one table) -> 2 means the WORKING TREE note was used"
probe "R2.badrows" "$(grep -o 'badrows=[0-9]*' "$S/o2/hidden-c001.out" | head -1)"

sec "R3 the same clone, but the working tree RESTORED: does the state revert?"
git -C "$S/lane" checkout -q -- . 2>/dev/null
probe "R3.worktree-clean" "$(git -C "$S/lane" status --porcelain | wc -l) changed lines"
mkdir -p "$S/w3" "$S/o3"
python3 -I "$CTRL" --lane "$S/lane" --rev "$REV" --base "$REV" \
  --work "$S/w3" --outdir "$S/o3" --only hidden-c001 --jobs 1 >"$S/r3.log" 2>&1
probe "R3.receipt-verdict-tables" "$(grep -o 'verdict_tables=[0-9]*' "$S/o3/hidden-c001.out" | head -1)"

printf '\n===== done =====\n'
