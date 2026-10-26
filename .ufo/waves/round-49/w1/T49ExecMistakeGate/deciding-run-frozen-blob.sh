#!/bin/bash
# Round-49 deciding run. Usage: deciding-run.sh LANE REV FREEZE OUTDIR
#   LANE    absolute path of the lane repo        REV     the content revision (all records, reads, ledger)
#   FREEZE  the counter-freeze commit             OUTDIR  an existing, EMPTY directory inside LANE for receipts
# Round-48 fixes built in (routed defects 2 and 3; lesson round-49 `## Mistakes`):
#   * gate 0 refuses (exit 3, nothing run) unless every pre-registered control receipt is committed at REV in a
#     commit that is an ancestor of REV and descends from FREEZE — controls are scored before any deciding run;
#   * gate 0 refuses when OUTDIR already holds a start receipt — one deciding invocation per counter;
#   * every counter gets a start receipt BEFORE it runs and an exit receipt after; no output is read before both;
#   * the frozen path list names code and contract only, never a receipt directory.
# Work dirs live under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r49/deciding, never /tmp.
set -u
LANE=$1; REV=$2; FREEZE=$3; OUT=$4
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
BASE=8ca67421111fa354b47b803358391d0b07fc6db9
FLEET=/home/vgpnk/Projects/shokunin
E=.ufo/evidence/round-49
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r49/deciding
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
mkdir -p "$SCR"; export TMPDIR="$SCR"
rc=0
FROZEN="$E/contract.json $E/freeze.json $E/c1/measure.py $E/c2/measure.py $E/control/c1-controls.py $E/control/c2-controls.sh $E/control/c2-fixed-gen.py $E/control/c2-fixed-fixtures.json $E/no-harm.sh $E/deciding-run.sh .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-18/measure.py tools/staged-id-guard.py"
if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; else echo "FROZEN_UNCHANGED=0 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; git diff --stat "$FREEZE" "$REV" -- $FROZEN | tee -a "$OUT/frozen.stdout"; rc=1; fi
git show "$REV:$E/no-harm.sh" > "$SCR/no-harm.sh"
bash "$SCR/no-harm.sh" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; echo $? > "$OUT/no-harm.exit"
cat "$OUT/no-harm.stdout"; grep -q RED "$OUT/no-harm.stdout" && rc=1
[ "$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")" = 9 ] || { echo "NOHARM_OK_COUNT!=9"; rc=1; }
bash .ufo/evidence/round-48/quality/coldread-precheck.sh "$LANE" "$BASE" "$REV" > "$OUT/coldread-precheck.stdout" 2>&1; echo $? > "$OUT/coldread-precheck.exit"
tail -1 "$OUT/coldread-precheck.stdout"; [ "$(cat "$OUT/coldread-precheck.exit")" = 0 ] || rc=1
"$FLEET/scripts/sources-census.sh" validate --root "$FLEET" tameshi > "$OUT/census.stdout" 2> "$OUT/census.stderr"; echo $? > "$OUT/census.exit"
echo "CENSUS exit=$(cat "$OUT/census.exit")"; [ "$(cat "$OUT/census.exit")" = 0 ] || rc=1
git show "$REV:$E/c2/panel.json" > "$SCR/panel.json" || { echo "PANEL_NOT_REVEALED"; rc=1; }
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/c2.start"
python3 "$E/c2/measure.py" --lane "$LANE" --rev "$REV" --work "$SCR/c2" --panel "$SCR/panel.json" > "$OUT/c2.stdout" 2>&1; echo $? > "$OUT/c2.exit"
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/c2.end"
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/c1.start"
python3 "$E/c1/measure.py" --lane "$LANE" --rev "$REV" --work "$SCR/c1" > "$OUT/c1.stdout" 2>&1; echo $? > "$OUT/c1.exit"
date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/c1.end"
tail -1 "$OUT/c2.stdout"; [ "$(cat "$OUT/c2.exit")" = 0 ] || rc=1
tail -1 "$OUT/c1.stdout"; [ "$(cat "$OUT/c1.exit")" = 0 ] || rc=1
rm -rf "$SCR"
echo "DECIDING_RUN_EXIT=$rc" | tee "$OUT/deciding-run.stdout"
exit $rc
