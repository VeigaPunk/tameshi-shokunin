#!/usr/bin/env bash
# R93SN1 probe 3: exploit demos for the round-93 C1 drivers.
# All fixtures live under $S; the lane and fleet repos are only ever READ.
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe3.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CTRL="$LANE/.ufo/evidence/round-93/c1/controls-v93.py"
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
BASE=4a7e259b407d582d2010197f32d7524d6bed5370
probe() { printf 'PROBE %-40s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "X1 real driver: ambient GIT_DIR - where does the control commit land?"
git init -q "$S/hijack"
git -C "$S/hijack" -c user.name=t -c user.email=t@t commit -q --allow-empty -m base
mkdir -p "$S/w1"
GIT_DIR="$S/hijack/.git" python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" \
  --work "$S/w1" --outdir "$S/o1" --only pos-real --jobs 1 >"$S/x1.log" 2>&1
probe "X1.driver-rc" "$?"
probe "X1.log-tail" "$(tail -4 "$S/x1.log" | tr '\n' '|')"
probe "X1.hijack-repo-log" "$(git -C "$S/hijack" log --oneline --all 2>&1 | tr '\n' '|')"
probe "X1.hijack-has-fixture-commit" "$(git -C "$S/hijack" log --oneline --all 2>/dev/null | grep -c 'r93 control' )"
probe "X1.hijack-refs" "$(git -C "$S/hijack" show-ref 2>&1 | tr '\n' '|')"

sec "X2 real driver: RELATIVE --outdir lands in the process cwd"
mkdir -p "$S/cwd2" "$S/w2" && cd "$S/cwd2" || exit 1
python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" \
  --work "$S/w2" --outdir relative-receipts --only nowork-base --jobs 1 >"$S/x2.log" 2>&1
probe "X2.rc" "$?"
probe "X2.cwd-listing" "$(ls -A "$S/cwd2" | tr '\n' ' ')"
probe "X2.receipt-landed-in-cwd" "$( [ -f "$S/cwd2/relative-receipts/nowork-base.out" ] && echo YES || echo no )"

sec "X3 real driver: M4 guard vs a pre-existing DANGLING symlink in --outdir"
mkdir -p "$S/o3" "$S/w3"
ln -s "$S/ESCAPED-receipt.txt" "$S/o3/pos-real.out"
python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" \
  --work "$S/w3" --outdir "$S/o3" --only pos-real --jobs 1 >"$S/x3.log" 2>&1
probe "X3.rc" "$?"
probe "X3.escape-file-created" "$( [ -f "$S/ESCAPED-receipt.txt" ] && echo YES || echo no )"
probe "X3.escape-content" "$(head -c 60 "$S/ESCAPED-receipt.txt" 2>/dev/null | tr '\n' '|')"
probe "X3.outdir-listing" "$(ls -A "$S/o3" | tr '\n' ' ')"

sec "X4 measure-v93: --work '' in an EMPTY cwd materialises the gate into the cwd"
mkdir -p "$S/cwd4"
( cd "$S/cwd4" && python3 -I "$MEAS" --repo "$LANE" --rev "$REV" --work "" >"$S/x4.log" 2>&1 )
probe "X4.rc-and-head" "$(head -2 "$S/x4.log" | tr '\n' '|')"
probe "X4.cwd4-tree" "$(cd "$S/cwd4" && find . -maxdepth 3 | head -12 | tr '\n' ' ')"
probe "X4.gate-written-into-cwd" "$( [ -f "$S/cwd4/scripts/sources-census.sh" ] && echo YES || echo no )"

sec "X5 receipt provenance: does a receipt attest the counter bytes that made it?"
for r in pos-real timeout hidden-c001 D01; do
  f="$LANE/.ufo/evidence/round-93/pre-freeze/controls/$r.out"
  probe "X5.$r.has-counter-digest" "$(grep -c -i 'sha256\|counter_sha\|instrument' "$f" 2>/dev/null)"
done
probe "X5.receipt-head-pos-real" "$(head -2 "$LANE/.ufo/evidence/round-93/pre-freeze/controls/pos-real.out" | tr '\n' '|')"

sec "X6 measure-v93: is the gate EXECUTED even when pin/pins are false?"
mkdir -p "$S/w6"
python3 -I "$MEAS" --repo "$LANE" --rev "$REV" --work "$S/w6" >"$S/x6.log" 2>&1
probe "X6.rc" "$?"
probe "X6.conjuncts" "$(grep '^C1_CONJUNCTS' "$S/x6.log" | tr ' ' '\n' | grep -E '^(pins|pin|green)=' | tr '\n' ' ')"
probe "X6.gate-executed" "$(ls -d "$S/w6/pristine" "$S/w6/canary" 2>&1 | tr '\n' ' ')"

printf '\n===== done =====\n'
