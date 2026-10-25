#!/bin/bash
# Round-46 deciding run. Usage: deciding-run.sh LANE REV OUTDIR [WORKROOT]
#   REV     the content revision that carries the records (QUALITY criterion 86): the deciding receipts are
#           taken here and committed afterwards in a receipts-only commit.
#   OUTDIR  an existing directory inside LANE (receipts are written as files there).
# Steps (each prints one labelled line; the exit status is the AND of the claim counters):
#   0 FROZEN_UNCHANGED  git diff FREEZE..REV over the frozen counters, statements, manifest, snapshots,
#                       package copies, controls and contract is empty (a counter edited after the freeze
#                       would otherwise pass its own self_pin; round-46 CritC1Control finding Z)
#   1 no-harm monitors  .ufo/evidence/round-46/no-harm.sh at REV, all ok
#   2 C1, C2, C3        the three frozen counters at REV
#   3 ENTRY_NAMES_OK    every admitted C3 entry basename is one of the three package basenames (CritC3Control Vd3)
#   4 census            sources-census.sh validate --root FLEET tameshi, exit 0
set -u
LANE=$1; REV=$2; OUT=$3; WORK=${4:-/tmp/tameshi-r46-deciding}
FREEZE=745a583181648cfc7f9c1b476cd1be7dc68f7433
BASE=683eedde3a50441c34d85a22f5fd5346f8b1ec6d
FLEET=/home/vgpnk/Projects/shokunin
E=.ufo/evidence/round-46
cd "$LANE" || exit 2
rc=0
FROZEN="$E/contract.json $E/calibration/measure.py $E/calibration/statements.json $E/coverage/measure.py $E/coverage/sources $E/assimilation/package $E/assimilation/adoption-map.json $E/hardening/mutate.py $E/hardening/mutants.json $E/control/run-controls.py $E/no-harm.sh"
if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; else echo "FROZEN_UNCHANGED=0 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; git diff --stat "$FREEZE" "$REV" -- $FROZEN | tee -a "$OUT/frozen.stdout"; rc=1; fi
for f in calibration/measure.py coverage/measure.py hardening/mutate.py; do echo "COUNTER_SHA256 $f $(git show "$REV:$E/$f" | sha256sum | cut -c1-64)" | tee -a "$OUT/frozen.stdout"; done
bash "$E/no-harm.sh" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; cat "$OUT/no-harm.stdout"; grep -q RED "$OUT/no-harm.stdout" && rc=1
python3 "$E/hardening/mutate.py" --lane "$LANE" --rev "$REV" --targets hardened > "$OUT/c2.stdout" 2>&1; echo $? > "$OUT/c2.exit"; tail -1 "$OUT/c2.stdout"; [ "$(cat "$OUT/c2.exit")" = 0 ] || rc=1
python3 "$E/coverage/measure.py" --lane "$LANE" --rev "$REV" > "$OUT/c3.stdout" 2>&1; echo $? > "$OUT/c3.exit"; tail -1 "$OUT/c3.stdout"; [ "$(cat "$OUT/c3.exit")" = 0 ] || rc=1
names=$(grep '^ENTRY ' "$OUT/c3.stdout" | sed 's#^ENTRY .*/##; s# (not indexed)$##' | sort | tr '\n' ' ')
want=$(ls "$E/assimilation/package" | sort | tr '\n' ' ')
[ "$names" = "$want" ] && echo "ENTRY_NAMES_OK=1 $names" || { echo "ENTRY_NAMES_OK=0 got=[$names] want=[$want]"; rc=1; }
"$FLEET/scripts/sources-census.sh" validate --root "$FLEET" tameshi > "$OUT/census.stdout" 2> "$OUT/census.stderr"; echo $? > "$OUT/census.exit"; echo "CENSUS exit=$(cat "$OUT/census.exit")"; [ "$(cat "$OUT/census.exit")" = 0 ] || rc=1
rm -rf "$WORK"
python3 "$E/calibration/measure.py" --lane "$LANE" --rev "$REV" --base "$BASE" --work "$WORK" > "$OUT/c1.stdout" 2>&1; echo $? > "$OUT/c1.exit"; tail -1 "$OUT/c1.stdout"; [ "$(cat "$OUT/c1.exit")" = 0 ] || rc=1
echo "DECIDING_RUN_EXIT=$rc"
exit $rc
