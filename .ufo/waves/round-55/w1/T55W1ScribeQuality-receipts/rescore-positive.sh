#!/bin/bash
# Re-score round-54's phase-B positive control at the revision it certifies.
#
# Round-54 `control/controls.sh b` cloned the FREEZE commit (077d431e), which
# predates the re-key 7fa9a5e, so CTL_POS_c1 printed `rekeyed=3/7` and
# `CTL_MISMATCH` (R54.1). This script is that phase with one variable changed:
# the clone is taken at REV, the revision the claim certifies. Everything else
# is the committed script's shape - the FROZEN counter bytes are extracted from
# FREEZE, never the worktree, and the run leaves its own stdout behind.
#
#   rescore-positive.sh LANE FREEZE REV
#
# Exit 0 iff the pre-registered expectation (CTL_POS_c1 true) holds at REV.
# Scratch: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r55/T55W1ScribeQuality-rescore
set -u
LANE=$1; FREEZE=$2; REV=$3
case "$LANE" in /*) ;; *) echo "LANE must be absolute" >&2; exit 2;; esac
E=.ufo/evidence/round-54
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r55/T55W1ScribeQuality-rescore.$$
rm -rf "$SCR"; mkdir -p "$SCR/code/c1" "$SCR/work"
trap 'rm -rf -- "$SCR"' EXIT
export TMPDIR="$SCR"
FREEZE=$(git -C "$LANE" rev-parse --verify "$FREEZE^{commit}") || exit 2
REV=$(git -C "$LANE" rev-parse --verify "$REV^{commit}") || exit 2
for f in c1/measure.py c1/lost-headings-at-base.json; do
  git -C "$LANE" show "$FREEZE:$E/$f" > "$SCR/code/$f" || exit 2
done
echo "RESCORE counter=$E/c1/measure.py at=$(git -C "$LANE" rev-parse "$FREEZE:$E/c1/measure.py" | cut -c1-12) sha256=$(sha256sum "$SCR/code/c1/measure.py" | cut -d' ' -f1)"
echo "RESCORE lane=$LANE freeze=$FREEZE rev=$REV"
d="$SCR/clone"
git clone --shared --quiet "$LANE" "$d" >/dev/null 2>&1 || exit 2
git -C "$d" checkout --quiet -B r55-cert "$REV" >/dev/null 2>&1 || exit 2
HEAD=$(git -C "$d" rev-parse HEAD)
python3 "$SCR/code/c1/measure.py" --lane "$d" --rev "$HEAD" --work "$SCR/work" > "$SCR/c1.out" 2>&1
rc=$?
echo "RESCORE counter-exit=$rc"
if [ "$rc" = 2 ] || [ ! -s "$SCR/c1.out" ]; then
  echo "RESCORE setup refusal: the counter did not produce a verdict line" >&2
  sed 's/^/RESCORE counter: /' "$SCR/c1.out" 2>/dev/null >&2
  exit 2
fi
tail -1 "$SCR/c1.out" | sed 's/^/CTL CTL_POS_c1 /'
v=$(grep -oE 'C1_R54_PASS=(true|false)' "$SCR/c1.out" | tail -1 | cut -d= -f2)
if [ "$v" = "true" ]; then pass=1; fail=0; else pass=0; fail=1; echo "CTL_MISMATCH CTL_POS_c1 expected=true actual=$v"; fi
echo "CONTROLS_B: $pass/$((pass+fail)) as pre-registered"
[ "$fail" = 0 ] || exit 1
exit 0
