#!/bin/bash
# Round-49 C2 controls, scored with the frozen C2 counter at freeze bytes before any deciding run.
# Usage: c2-controls.sh LANE FREEZE PANEL WITNESS OUTDIR
#   CTL_ABSENT  the freeze tree as it is (no generator at tools/pbt-staged-id.py)
#   CTL_FIX     the fixture-replay stub control/c2-fixed-gen.py (the guard's own 14 selftest fixtures, golden outputs)
#   WITNESS     non-equivalence receipt: 11 hand-made cases confirm every panel mutant (no PASS label)
# The panel is hidden until the deciding run (commit-reveal: contract pins its sha256); PANEL is its path outside
# the lane, and so is WITNESS (the hand-made cases, revealed with it). Work dirs live under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r49/c2-controls.
set -u
LANE=$1; FREEZE=$2; PANEL=$3; WITNESS_CASES=$4; OUT=$5
E=.ufo/evidence/round-49
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r49/c2-controls
cd "$LANE" || exit 2
rm -rf "$SCR"; mkdir -p "$SCR"; export TMPDIR="$SCR"
rc=0
python3 "$E/c2/measure.py" --lane "$LANE" --rev "$FREEZE" --work "$SCR/absent" --panel "$PANEL" > "$OUT/c2-CTL_ABSENT.stdout" 2>&1; a=$?
python3 "$E/c2/measure.py" --lane "$LANE" --rev "$FREEZE" --work "$SCR/fix" --panel "$PANEL" --generator-path "$E/control/c2-fixed-gen.py" > "$OUT/c2-CTL_FIX.stdout" 2>&1; f=$?
python3 "$E/c2/measure.py" --lane "$LANE" --rev "$FREEZE" --work "$SCR/wit" --panel "$PANEL" --witness "$WITNESS_CASES" > "$OUT/c2-WITNESS.stdout" 2>&1; w=$?
echo "CTL_ABSENT exit=$a $(tail -1 "$OUT/c2-CTL_ABSENT.stdout")"
echo "CTL_FIX exit=$f $(tail -1 "$OUT/c2-CTL_FIX.stdout")"
echo "WITNESS exit=$w $(tail -1 "$OUT/c2-WITNESS.stdout")"
grep -q 'C2_R49_PASS=false' "$OUT/c2-CTL_ABSENT.stdout" || rc=1
grep -q 'C2_R49_PASS=false' "$OUT/c2-CTL_FIX.stdout" || rc=1
grep -q 'witness_confirmed=12' "$OUT/c2-WITNESS.stdout" || rc=1
rm -rf "$SCR"
echo "C2_CONTROLS ok=$([ $rc = 0 ] && echo true || echo false)"
exit $rc
