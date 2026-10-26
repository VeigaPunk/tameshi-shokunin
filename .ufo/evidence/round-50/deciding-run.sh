#!/bin/bash
# Round-50 deciding run. Usage: deciding-run.sh LANE REV FREEZE OUTDIR
#   LANE    absolute path of the lane repo        REV     the content revision (ledger, shrinker, records)
#   FREEZE  the counter-freeze commit             OUTDIR  an existing, EMPTY directory inside LANE for receipts
# Carried from round 49 (QUALITY 99): gate 0 refuses (exit 3, nothing run) unless every pre-registered control
# receipt is committed at REV in a commit that descends from FREEZE; a second invocation is refused; each counter
# gets a start receipt before it runs and an exit receipt after; the frozen path list names code and contract only.
# New at round 50 (round-49 review T49RevDeciding F1): the counters, no-harm and the precheck run from the bytes
# committed at REV (git show into scratch), never from the working tree; the working tree must be clean.
# The hidden C2 panel is read from REV (revealed before this run); its digest is checked by the counter.
# Work dirs live under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r50/deciding, never /tmp.
set -u
LANE=$1; REV=$2; FREEZE=$3; OUT=$4
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
BASE=e3729de862f73ae080d98fcf522a7081ce16e40a
FLEET=/home/vgpnk/Projects/shokunin
E=.ufo/evidence/round-50
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r50/deciding
cd "$LANE" || exit 2
REV=$(git rev-parse --verify "$REV^{commit}") || exit 2
FREEZE=$(git rev-parse --verify "$FREEZE^{commit}") || exit 2
[ -d "$OUT" ] || { echo "DECIDING_REFUSED outdir-missing"; exit 3; }
CONTROLS="$E/control/c1-controls.stdout $E/control/c1-controls.exit $E/control/c2-controls.stdout $E/control/c2-controls.exit"
for f in $CONTROLS; do
  git cat-file -e "$REV:$f" 2>/dev/null || { echo "DECIDING_REFUSED control-receipt-missing $f"; exit 3; }
  c=$(git log -1 --format=%H "$REV" -- "$f")
  git merge-base --is-ancestor "$FREEZE" "$c" || { echo "DECIDING_REFUSED control-receipt-not-after-freeze $f"; exit 3; }
done
for k in c1 c2; do [ -e "$OUT/$k.start" ] && { echo "DECIDING_REFUSED second-invocation $k"; exit 3; }; done
rm -rf "$SCR"; mkdir -p "$SCR/code"; export TMPDIR="$SCR"
for f in c1/measure.py c2/measure.py no-harm.sh; do mkdir -p "$SCR/code/$(dirname $f)"; git show "$REV:$E/$f" > "$SCR/code/$f" || exit 2; done
git show "$REV:.ufo/evidence/round-48/quality/coldread-precheck.sh" > "$SCR/code/precheck.sh" || exit 2
git show "$REV:$E/c2/panel-hidden.json" > "$SCR/hidden.json" || { echo "DECIDING_REFUSED hidden-panel-not-revealed"; exit 3; }
git show "$REV:.ufo/evidence/round-49/c2/panel.json" > "$SCR/public.json" || exit 2
rc=0
FROZEN="$E/contract.json $E/freeze.json $E/c1/measure.py $E/c1/defects.json $E/c1/keys.json $E/c1/extract-defects.py $E/c2/measure.py $E/control/c1-controls.py $E/control/c2-controls.py $E/no-harm.sh $E/deciding-run.sh .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-18/measure.py .ufo/evidence/round-48/quality/coldread-precheck.sh tools/staged-id-guard.py"
if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; else echo "FROZEN_UNCHANGED=0 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; git diff --stat "$FREEZE" "$REV" -- $FROZEN | tee -a "$OUT/frozen.stdout"; rc=1; fi
bash "$SCR/code/no-harm.sh" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; echo $? > "$OUT/no-harm.exit"
cat "$OUT/no-harm.stdout"; grep -q RED "$OUT/no-harm.stdout" && rc=1
[ "$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")" = 10 ] || { echo "NOHARM_OK_COUNT!=10"; rc=1; }
bash "$SCR/code/precheck.sh" "$LANE" "$BASE" "$REV" > "$OUT/coldread-precheck.stdout" 2>&1; echo $? > "$OUT/coldread-precheck.exit"
tail -1 "$OUT/coldread-precheck.stdout"; [ "$(cat "$OUT/coldread-precheck.exit")" = 0 ] || rc=1
"$FLEET/scripts/sources-census.sh" validate --root "$FLEET" tameshi > "$OUT/census.stdout" 2> "$OUT/census.stderr"; echo $? > "$OUT/census.exit"
echo "CENSUS exit=$(cat "$OUT/census.exit")"; [ "$(cat "$OUT/census.exit")" = 0 ] || rc=1
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/c2.start"
python3 "$SCR/code/c2/measure.py" --lane "$LANE" --rev "$REV" --work "$SCR/c2" --panel "$SCR/public.json" --hidden "$SCR/hidden.json" > "$OUT/c2.stdout" 2>&1; echo $? > "$OUT/c2.exit"
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/c2.end"
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/c1.start"
python3 "$SCR/code/c1/measure.py" --lane "$LANE" --rev "$REV" --explain > "$OUT/c1.stdout" 2>&1; echo $? > "$OUT/c1.exit"
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/c1.end"
tail -1 "$OUT/c2.stdout"; [ "$(cat "$OUT/c2.exit")" = 0 ] || rc=1
tail -1 "$OUT/c1.stdout"; [ "$(cat "$OUT/c1.exit")" = 0 ] || rc=1
rm -rf "$SCR"
echo "DECIDING_RUN_EXIT=$rc" | tee "$OUT/deciding-run.stdout"
exit $rc
