#!/usr/bin/env bash
# T91E4 probe (round 91, lane tameshi, seat T91E4): sealed-counter probe H.
# Hypothesis H: the sealed counter (measure-v91.py) (a) refuses (exit 2,
# replace-refs-present) on a repo carrying a local `git replace` ref, and
# (b) derives the same 12 verdicts with the seal on as with the raw fleet
# environment.
# Adapted step (1): the seat spec writes --repo as the lane path, but the lane
# is read-only (hard rule: no git mutation in the lane), so the probe measures
# a scratch clone at the frozen rev; the counter's guard checks whatever repo
# is passed via --repo, so the test is equivalent. Step (2) runs the same
# counter with deliberately polluted GIT_* env to show the seal overrides it.
# Usage: bash T91E4-probe.sh   (outputs land next to this file)
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
REV=50e59d59a5b0fffffe7a0e99da9a39397f2f94fc
COUNTER=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-91/c1/measure-v91.py
CTL1B=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-91/pre-freeze/controls/CTL1b-nowork-A.out
SEAT=T91E4
S=/fast/scratch/hyaku/tameshi-r91/T91E4
OUTDIR="$(cd "$(dirname "$0")" && pwd)"
CLONE="$S/clone"
P1="$OUTDIR/T91E4-phase1.out"
P2="$OUTDIR/T91E4-phase2.out"
SUM="$OUTDIR/T91E4-probe-trace.txt"
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT

{
echo "== T91E4 probe transcript =="
date -u +"%Y-%m-%dT%H:%M:%SZ"
echo "lane=$LANE rev=$REV"
echo "counter=$COUNTER"
"git" --version
python3 --version
echo "lane replace -l: [$(git -C "$LANE" replace -l 2>&1)]"
echo "fleet replace -l: [$(git -C "$FLEET" replace -l 2>&1)]"
echo "spec sha at REV: $(git -C "$LANE" cat-file blob "$REV:.ufo/evidence/round-91/c1/census-mutants.json" | sha256sum)"
echo "spec sha at ace200b5: $(git -C "$LANE" cat-file blob "ace200b50fe8cea1e05cde88dabf8fe075f86116:.ufo/evidence/round-91/c1/census-mutants.json" | sha256sum)"
echo "note sha at REV: $(git -C "$LANE" cat-file blob "$REV:corpus/knowledge/mutation-case-fleet-sources-census.md" | sha256sum)"
echo "note sha at ace200b5: $(git -C "$LANE" cat-file blob "ace200b50fe8cea1e05cde88dabf8fe075f86116:corpus/knowledge/mutation-case-fleet-sources-census.md" | sha256sum)"
} | tee "$SUM"

# --- scratch clone at frozen rev ---
rm -rf -- "$CLONE"
git clone -q --shared --no-checkout "$LANE" "$CLONE"
TOP="$(git -C "$CLONE" rev-parse --show-toplevel)"
echo "clone toplevel: $TOP" | tee -a "$SUM"
if [ "$(realpath "$TOP")" != "$(realpath "$CLONE")" ]; then
  echo "FATAL: toplevel mismatch" | tee -a "$SUM"; exit 3
fi
git -C "$CLONE" rev-parse --verify "$REV" | tee -a "$SUM"
PARENT="$(git -C "$CLONE" rev-parse "$REV^")"
echo "replace pair: $REV -> $PARENT" | tee -a "$SUM"

# --- phase 1: plant local replace ref, run counter -> expect exit 2 ---
git -C "$CLONE" replace "$REV" "$PARENT"
echo "replace -l (phase1): [$(git -C "$CLONE" replace -l)]" | tee -a "$SUM"
W1="$S/work1"; mkdir -p "$W1"
set +e
python3 -I "$COUNTER" --repo "$CLONE" --rev "$REV" --work "$W1" > "$P1" 2>&1
RC1=$?
set -e
echo "phase1 exit=$RC1" | tee -a "$SUM"
cat "$P1" | tee -a "$SUM"

# --- phase 2: delete ref, run counter under polluted env -> expect 12 rows ---
git -C "$CLONE" replace -d "$REV"
echo "replace -l (phase2): [$(git -C "$CLONE" replace -l)]" | tee -a "$SUM"
W2="$S/work2"; mkdir -p "$W2"
set +e
env GIT_NO_REPLACE_OBJECTS=0 GIT_CONFIG_NOSYSTEM=0 GIT_CONFIG_GLOBAL=/root/.gitconfig GIT_DIR=/nonexistent GIT_WORK_TREE=/nonexistent GIT_ALTERNATE_OBJECT_DIRECTORIES=/nonexistent \
  python3 -I "$COUNTER" --repo "$CLONE" --rev "$REV" --work "$W2" > "$P2" 2>&1
RC2=$?
set -e
echo "phase2 exit=$RC2" | tee -a "$SUM"
cat "$P2" | tee -a "$SUM"

# --- compare C1_ROW lines vs CTL1b baseline ---
echo "== C1_ROW diff vs CTL1b (phase2 rows vs CTL1b rows) ==" | tee -a "$SUM"
grep '^C1_ROW' "$P2"  > "$S/rows2.txt"
grep '^C1_ROW' "$CTL1B" > "$S/rows1.txt"
diff "$S/rows1.txt" "$S/rows2.txt" | tee -a "$SUM"
DIFF_RC=${PIPESTATUS[0]}
echo "rows2 count: $(wc -l < "$S/rows2.txt"); rows1 count: $(wc -l < "$S/rows1.txt")" | tee -a "$SUM"
if [ "$RC1" -eq 2 ] && grep -q 'C1_SETUP replace-refs-present:lane' "$P1" && [ "$DIFF_RC" -eq 0 ] && [ "$(wc -l < "$S/rows2.txt")" -eq 12 ]; then
  echo "VERDICT: sealed-holds" | tee -a "$SUM"
else
  echo "VERDICT: seal-broken" | tee -a "$SUM"
fi
echo "done"
