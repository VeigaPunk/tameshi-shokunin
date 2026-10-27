#!/bin/bash
# Round-52 deciding run. Usage: deciding-run.sh LANE REV FREEZE OUTDIR
#   LANE    absolute path of the lane repo        REV     the content revision
#   FREEZE  the counter-freeze commit             OUTDIR  an existing, EMPTY directory inside LANE for receipts
# Carried from rounds 49-51 (QUALITY 99): gate 0 refuses (exit 3, nothing run) unless every pre-registered control
# receipt is committed at REV in a commit that descends from FREEZE; a second invocation is refused; each counter
# gets a start receipt before it runs and an exit receipt after; the counters, no-harm and the precheck run from the
# bytes committed at REV (git show into scratch), never from the working tree; the working tree must be clean
# (witness files before and after). Work dirs live under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r52/deciding.
set -u
LANE=$1; REV=$2; FREEZE=$3; OUT=$4
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
BASE=ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4
FLEET=/home/vgpnk/Projects/shokunin
E=.ufo/evidence/round-52
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r52/deciding
cd "$LANE" || exit 2
REV=$(git rev-parse --verify "$REV^{commit}") || exit 2
FREEZE=$(git rev-parse --verify "$FREEZE^{commit}") || exit 2
[ -d "$OUT" ] || { echo "DECIDING_REFUSED outdir-missing"; exit 3; }
[ "$(git rev-parse HEAD)" = "$REV" ] || { echo "DECIDING_REFUSED head-is-not-rev"; exit 3; }
CONTROLS="$E/control/controls.stdout $E/control/controls.exit"
for f in $CONTROLS; do
  git cat-file -e "$REV:$f" 2>/dev/null || { echo "DECIDING_REFUSED control-receipt-missing $f"; exit 3; }
  c=$(git log -1 --format=%H "$REV" -- "$f")
  git merge-base --is-ancestor "$FREEZE" "$c" || { echo "DECIDING_REFUSED control-receipt-not-after-freeze $f"; exit 3; }
done
for k in c1 c2; do [ -e "$OUT/$k.start" ] && { echo "DECIDING_REFUSED second-invocation $k"; exit 3; }; done
git status --porcelain > "$OUT/clean-tree-before.txt"
[ "$(grep -vc "^?? ${OUT#$LANE/}" "$OUT/clean-tree-before.txt")" = 0 ] || { echo "DECIDING_REFUSED dirty-tree"; cat "$OUT/clean-tree-before.txt"; exit 3; }
rm -rf "$SCR"; mkdir -p "$SCR/code" "$SCR/c1"; export TMPDIR="$SCR"
for f in c1/measure.py c1/base-active.json c2/measure.py no-harm.sh; do mkdir -p "$SCR/code/$(dirname $f)"; git show "$REV:$E/$f" > "$SCR/code/$f" || exit 2; done
git show "$REV:.ufo/evidence/round-48/quality/coldread-precheck.sh" > "$SCR/code/precheck.sh" || exit 2
rc=0
FROZEN="$E/contract.json $E/freeze.json $E/c1/measure.py $E/c1/base-active.json $E/c2/measure.py .ufo/evidence/round-51/c3/measure.py .ufo/evidence/round-51/c3/tools-base.json tools/registry-check.py $E/control/controls.py $E/no-harm.sh $E/deciding-run.sh .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-18/measure.py .ufo/evidence/round-48/quality/coldread-precheck.sh"
if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; else echo "FROZEN_UNCHANGED=0 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; git diff --stat "$FREEZE" "$REV" -- $FROZEN | tee -a "$OUT/frozen.stdout"; rc=1; fi
bash "$SCR/code/no-harm.sh" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; echo $? > "$OUT/no-harm.exit"
cat "$OUT/no-harm.stdout"; grep -q RED "$OUT/no-harm.stdout" && rc=1
[ "$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")" = 11 ] || { echo "NOHARM_OK_COUNT!=11"; rc=1; }
bash "$SCR/code/precheck.sh" "$LANE" "$BASE" "$REV" > "$OUT/coldread-precheck.stdout" 2>&1; echo $? > "$OUT/coldread-precheck.exit"
tail -1 "$OUT/coldread-precheck.stdout"; [ "$(cat "$OUT/coldread-precheck.exit")" = 0 ] || rc=1
"$FLEET/scripts/sources-census.sh" validate --root "$FLEET" tameshi > "$OUT/census.stdout" 2> "$OUT/census.stderr"; echo $? > "$OUT/census.exit"
echo "CENSUS exit=$(cat "$OUT/census.exit")"; [ "$(cat "$OUT/census.exit")" = 0 ] || rc=1
for k in c1 c2; do
  date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/$k.start"
  case $k in
    c1) python3 "$SCR/code/c1/measure.py" --lane "$LANE" --rev "$REV" --work "$SCR/c1" --explain > "$OUT/c1.stdout" 2>&1 ;;
    c2) python3 "$SCR/code/c2/measure.py" --lane "$LANE" --rev "$REV" --explain > "$OUT/c2.stdout" 2>&1 ;;
  esac
  echo $? > "$OUT/$k.exit"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/$k.end"
  tail -1 "$OUT/$k.stdout"; [ "$(cat "$OUT/$k.exit")" = 0 ] || rc=1
done
git status --porcelain > "$OUT/clean-tree-after.txt"
rm -rf "$SCR"
echo "DECIDING_RUN_EXIT=$rc" | tee "$OUT/deciding-run.stdout"
exit $rc
