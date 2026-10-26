#!/bin/bash
# Round-48 deciding run (contract amendment 8). Usage: deciding-run.sh LANE REV FREEZE OUTDIR
#   LANE    absolute path of the lane repo
#   REV     the content revision carrying the records; every counter reads git objects at REV
#   FREEZE  the counter-freeze commit (freeze step 2, .ufo/evidence/round-48/freeze-2.json)
#   OUTDIR  an existing directory inside LANE; receipts are written there and land in a receipts-only commit
# Steps: 0 FROZEN_UNCHANGED (git diff FREEZE..REV over both counters, statements, contract, controls, the C2
# snapshots and receipts, the no-harm script and every tool a C1 statement pins); 1 no-harm monitors from REV and
# the cold-read credited-section count (>= 60); 2 C2 (live) once; 3 census exit 0; 4 C1 once (three rounds).
# Work dirs live under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r48/deciding, never /tmp.
set -u
LANE=$1; REV=$2; FREEZE=$3; OUT=$4
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
BASE=473336d9d789f6081195e7376d17836a24666bc3
FLEET=/home/vgpnk/Projects/shokunin
E=.ufo/evidence/round-48
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r48/deciding
cd "$LANE" || exit 2
REV=$(git rev-parse --verify "$REV^{commit}") || exit 2
mkdir -p "$SCR"; export TMPDIR="$SCR"
rc=0
FROZEN="$E/contract.json $E/freeze-2.json $E/calibration/measure.py $E/freshness/measure.py $E/control $E/no-harm.sh $E/deciding-run.sh .ufo/evidence/round-47/calibration/statements.json tools .ufo/evidence/kaika-round-1 .ufo/evidence/round-15 .ufo/evidence/round-21 .ufo/evidence/round-45 .ufo/evidence/round-46 .ufo/evidence/round-47"
if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; else echo "FROZEN_UNCHANGED=0 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; git diff --stat "$FREEZE" "$REV" -- $FROZEN | tee -a "$OUT/frozen.stdout"; rc=1; fi
for f in calibration/measure.py freshness/measure.py; do echo "COUNTER_SHA256 $f $(git show "$REV:$E/$f" | sha256sum | cut -c1-64)" | tee -a "$OUT/frozen.stdout"; done
git show "$REV:$E/no-harm.sh" > "$SCR/no-harm.sh"
bash "$SCR/no-harm.sh" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; nh=$?; echo "$nh" > "$OUT/no-harm.exit"
cat "$OUT/no-harm.stdout"; grep -q RED "$OUT/no-harm.stdout" && rc=1
[ "$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")" = 8 ] || { echo "NOHARM_OK_COUNT!=8"; rc=1; }
sections=$(python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$REV" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(sum(1 for s in d["coldread"]["sections"] if s["credited"]))')
echo "COLDREAD_SECTIONS_CREDITED=$sections (base 60)" | tee "$OUT/coldread-sections.stdout"
[ "$sections" -ge 60 ] || rc=1
python3 "$E/freshness/measure.py" --lane "$LANE" --rev "$REV" > "$OUT/c2.stdout" 2>&1; echo $? > "$OUT/c2.exit"; tail -1 "$OUT/c2.stdout"; [ "$(cat "$OUT/c2.exit")" = 0 ] || rc=1
"$FLEET/scripts/sources-census.sh" validate --root "$FLEET" tameshi > "$OUT/census.stdout" 2> "$OUT/census.stderr"; echo $? > "$OUT/census.exit"; echo "CENSUS exit=$(cat "$OUT/census.exit")"; [ "$(cat "$OUT/census.exit")" = 0 ] || rc=1
cp "$OUT/census.stdout" "$E/census-end.stdout"; cp "$OUT/census.stderr" "$E/census-end.stderr"; cp "$OUT/census.exit" "$E/census-end.exit"
rm -rf "$SCR/c1"
python3 "$E/calibration/measure.py" --lane "$LANE" --rev "$REV" --base "$BASE" --work "$SCR/c1" > "$OUT/c1.stdout" 2>&1; echo $? > "$OUT/c1.exit"; tail -1 "$OUT/c1.stdout"; [ "$(cat "$OUT/c1.exit")" = 0 ] || rc=1
rm -rf "$SCR"
echo "DECIDING_RUN_EXIT=$rc" | tee "$OUT/deciding-run.stdout"
exit $rc
