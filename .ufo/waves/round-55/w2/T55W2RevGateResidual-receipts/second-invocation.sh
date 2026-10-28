#!/bin/bash
# Second-invocation probe. Builds one fixture clone at C0 whose control receipts are
# committed, then exercises the OUT-scoped `$OUT/$k.start` guard three ways.
# Usage: second-invocation.sh S
#  A) OUT1 already carries c1.start/c2.start (a completed first run's state, committed):
#     a second invocation into OUT1 must be refused.
#  B) the same first run, but the second invocation names OUT2 (different, empty): does it pass?
#  C) a first run interrupted before it wrote c1.start, then re-run into the SAME outdir.
set -u
S=$1; LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin; C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
FREEZE=e2979f277138da503af27b263b783f626f109be4
D=$S/fix-second; rm -rf -- "$D"
git clone --shared --quiet "$LANE" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "not a standalone repo"; exit 9; }
git -C "$D" -c advice.detachedHead=false checkout --quiet "$C0"
CTL=$D/.ufo/evidence/round-55/control; mkdir -p "$CTL"
for p in a b; do
  { echo "CTL CTL_POS_c1 C1_R55: rev=9cf0146b94dd classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true"
    echo "CTL CTL_POS_c2 C2_R55: rev=9cf0146b94dd grammar=8/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=0 C2_R55_PASS=true"
    echo "CONTROLS_${p^^}: 2/2 as pre-registered"; } > "$CTL/controls-$p.stdout"
  echo 0 > "$CTL/controls-$p.exit"
done
# A completed first run's OUT state, committed so the dirty-tree arm cannot see it.
OUT1=$D/.ufo/evidence/round-55/after-a; mkdir -p "$OUT1"
echo 2026-10-28T17:00:00Z > "$OUT1/c1.start"; echo 2026-10-28T17:00:00Z > "$OUT1/c2.start"
git -C "$D" add -A
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git -C "$D" -c user.name=fixture -c user.email=fixture@invalid \
  commit --quiet -m "fixture second: receipts + a completed first run in after-a"
REV=$(git -C "$D" rev-parse HEAD)
run () {  # run OUT T -> prints rc and refusal lines
  local out=$1 t=$2
  HYAKU_SCRATCH=$S/hyaku-second TMPDIR=$S/hyaku-second timeout "$t" \
    bash "$D/.ufo/evidence/round-55/deciding-run.sh" "$D" "$REV" "$FREEZE" "$out" \
    > "$S/second-$3.stdout" 2>&1
  echo "  rc=$? refusals: $(grep -h DECIDING_REFUSED "$S/second-$3.stdout" | tr '\n' ';' || true)"
}
mkdir -p "$S/hyaku-second"
echo "### A: second invocation into the SAME outdir (after-a carries c1.start/c2.start)"
run "$OUT1" 20 A
echo "### B: second invocation naming a DIFFERENT, empty outdir (after-b)"
OUT2=$D/.ufo/evidence/round-55/after-b; mkdir -p "$OUT2"
run "$OUT2" 20 B
echo "  after-b artefacts:"; ls -1 "$OUT2" | sed 's/^/    /'
echo "### C: first run interrupted before c1.start, then re-run into the SAME outdir (after-c)"
OUT3=$D/.ufo/evidence/round-55/after-c; mkdir -p "$OUT3"
run "$OUT3" 6 C1
echo "  after-c artefacts after the interrupted run:"; ls -1 "$OUT3" | sed 's/^/    /'
run "$OUT3" 20 C2
echo "  after-c artefacts after the re-run:"; ls -1 "$OUT3" | sed 's/^/    /'
echo "REV=$REV"
