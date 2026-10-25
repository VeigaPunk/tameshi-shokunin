#!/bin/bash
# Round-46 deciding run. Usage: deciding-run.sh LANE REV OUTDIR [WORKROOT]
#   LANE    absolute path of the lane repo (the counters read git objects at REV, never the worktree)
#   REV     the content revision that carries the records (QUALITY criterion 86): the deciding receipts are
#           taken here and committed afterwards in a receipts-only commit.
#   OUTDIR  an existing directory inside LANE (receipts are written as files there).
# Every step reads REV (git show / ls-tree / archive), not the worktree (wave-2 T46CritLanding findings 1-3):
#   0  FROZEN_UNCHANGED   git diff FREEZE..REV over the frozen counters, statements, manifest, snapshots, package
#                         copies, controls, no-harm script and contract is empty (a counter edited after the
#                         freeze would pass its own self_pin; wave-1 CritC1Control finding Z)
#   0b HARDENED_REBUILD   the two hardened counters at REV are byte-identical to assemble.py over the wave-1
#                         additions at REV (they are outside the frozen pathspec: absent at the freeze)
#   1  no-harm monitors   .ufo/evidence/round-46/no-harm.sh taken FROM REV, its exit status and RED lines checked,
#                         plus the cold-read monitor's credited-section count (60 at the base; a PROVINCE.md edit
#                         dropped it to 55 in a wave-2 attack and was reverted)
#   2  C1, C2, C3         the three frozen counters at REV
#   3  ENTRY_NAMES_OK     every admitted C3 entry basename is one of the three package basenames AT REV
#   4  census             sources-census.sh validate --root FLEET tameshi, exit 0
set -u
LANE=$1; REV=$2; OUT=$3; WORK=${4:-/tmp/tameshi-r46-deciding}
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
FREEZE=745a583181648cfc7f9c1b476cd1be7dc68f7433
BASE=683eedde3a50441c34d85a22f5fd5346f8b1ec6d
FLEET=/home/vgpnk/Projects/shokunin
E=.ufo/evidence/round-46
W1=.ufo/waves/round-46/w1
cd "$LANE" || exit 2
REV=$(git rev-parse --verify "$REV^{commit}") || exit 2
rc=0
FROZEN="$E/contract.json $E/calibration/measure.py $E/calibration/statements.json $E/coverage/measure.py $E/coverage/sources $E/assimilation/package $E/assimilation/adoption-map.json $E/hardening/mutate.py $E/hardening/mutants.json $E/control/run-controls.py $E/no-harm.sh"
if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; else echo "FROZEN_UNCHANGED=0 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; git diff --stat "$FREEZE" "$REV" -- $FROZEN | tee -a "$OUT/frozen.stdout"; rc=1; fi
for f in calibration/measure.py coverage/measure.py hardening/mutate.py hardening/freshness-counter.py hardening/coverage-counter.py; do echo "COUNTER_SHA256 $f $(git show "$REV:$E/$f" | sha256sum | cut -c1-64)" | tee -a "$OUT/frozen.stdout"; done
T=$(mktemp -d)
git archive "$REV" .ufo/evidence/round-45 "$E/hardening" "$W1" | tar -x -C "$T"
python3 "$T/$E/hardening/assemble.py" --group freshness --out "$T/f.py" --add "$T/$W1/HardGrade.addition.py" --add "$T/$W1/HardPopulation.addition.py" --add "$T/$W1/HardReviews.addition.py" --add "$T/$W1/HardMeasure.addition.py" > /dev/null
python3 "$T/$E/hardening/assemble.py" --group coverage --out "$T/c.py" --add "$T/$W1/HardCover1.addition.py" --add "$T/$W1/HardCover2.addition.py" > /dev/null
if git show "$REV:$E/hardening/freshness-counter.py" | cmp -s - "$T/f.py" && git show "$REV:$E/hardening/coverage-counter.py" | cmp -s - "$T/c.py"; then echo "HARDENED_REBUILD=1" | tee -a "$OUT/frozen.stdout"; else echo "HARDENED_REBUILD=0" | tee -a "$OUT/frozen.stdout"; rc=1; fi
rm -rf "$T"
git show "$REV:$E/no-harm.sh" > "$OUT/no-harm.sh.copy"
bash "$OUT/no-harm.sh.copy" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; nh=$?; echo "$nh" > "$OUT/no-harm.exit"; rm -f "$OUT/no-harm.sh.copy"
cat "$OUT/no-harm.stdout"; echo "NOHARM_EXIT=$nh"
[ "$nh" = 0 ] || rc=1
grep -q RED "$OUT/no-harm.stdout" && rc=1
[ "$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")" = 6 ] || { echo "NOHARM_OK_COUNT!=6"; rc=1; }
sections=$(python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$REV" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(sum(1 for s in d["coldread"]["sections"] if s["credited"]))')
echo "COLDREAD_SECTIONS_CREDITED=$sections (base 60)" | tee "$OUT/coldread-sections.stdout"
[ "$sections" -ge 60 ] || rc=1
python3 "$E/hardening/mutate.py" --lane "$LANE" --rev "$REV" --targets hardened > "$OUT/c2.stdout" 2>&1; echo $? > "$OUT/c2.exit"; tail -1 "$OUT/c2.stdout"; [ "$(cat "$OUT/c2.exit")" = 0 ] || rc=1
python3 "$E/coverage/measure.py" --lane "$LANE" --rev "$REV" > "$OUT/c3.stdout" 2>&1; echo $? > "$OUT/c3.exit"; tail -1 "$OUT/c3.stdout"; [ "$(cat "$OUT/c3.exit")" = 0 ] || rc=1
names=$(grep '^ENTRY ' "$OUT/c3.stdout" | sed 's#^ENTRY .*/##; s# (not indexed)$##' | sort | tr '\n' ' ')
want=$(git ls-tree --name-only "$REV" -- "$E/assimilation/package/" | sed 's#.*/##' | sort | tr '\n' ' ')
[ "$names" = "$want" ] && echo "ENTRY_NAMES_OK=1 $names" || { echo "ENTRY_NAMES_OK=0 got=[$names] want=[$want]"; rc=1; }
"$FLEET/scripts/sources-census.sh" validate --root "$FLEET" tameshi > "$OUT/census.stdout" 2> "$OUT/census.stderr"; echo $? > "$OUT/census.exit"; echo "CENSUS exit=$(cat "$OUT/census.exit")"; [ "$(cat "$OUT/census.exit")" = 0 ] || rc=1
cp "$OUT/census.stdout" "$E/census-end.stdout"; cp "$OUT/census.stderr" "$E/census-end.stderr"; cp "$OUT/census.exit" "$E/census-end.exit"
rm -rf "$WORK"
python3 "$E/calibration/measure.py" --lane "$LANE" --rev "$REV" --base "$BASE" --work "$WORK" > "$OUT/c1.stdout" 2>&1; echo $? > "$OUT/c1.exit"; tail -1 "$OUT/c1.stdout"; [ "$(cat "$OUT/c1.exit")" = 0 ] || rc=1
echo "DECIDING_RUN_EXIT=$rc"
exit $rc
