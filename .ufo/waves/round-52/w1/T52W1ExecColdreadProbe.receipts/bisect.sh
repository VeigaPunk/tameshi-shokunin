#!/bin/bash
# Round-52 cold-read bisect driver.  All git mutations happen inside the
# scratch clone; the lane is only read.
set -u
S=/fast/scratch/hyaku/tameshi-r52/T52W1ExecColdreadProbe
C=$S/clone
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4
M=$C/.ufo/evidence/round-21/coldread/measure.py
OUT=$S/out
mkdir -p "$OUT"

top=$(git -C "$C" rev-parse --show-toplevel) || exit 2
[ "$top" = "$C" ] || { echo "ABORT toplevel=$top"; exit 2; }

run_variant() {  # name edits...
  local v=$1; shift
  git -C "$C" checkout -q -B "$v" "$BASE" || return 2
  git -C "$C" reset -q --hard "$BASE" || return 2
  if [ "$#" -gt 0 ] && [ "$1" != "-" ]; then
    python3 "$S/apply_edits.py" "$C" "$@" >> "$OUT/edits-$v.log" 2>&1 || {
      echo "VARIANT $v EDIT-FAIL"; return 2; }
  fi
  git -C "$C" add -A >/dev/null 2>&1
  git -C "$C" -c user.name='hyaku-fixture' -c user.email='fixture@tameshi.invalid' \
      commit -q -m "fixture: round-52 coldread probe variant $v" || { echo "VARIANT $v COMMIT-FAIL"; return 2; }
  local sha; sha=$(git -C "$C" rev-parse HEAD)
  printf '%s %s\n' "$v" "$sha" >> "$OUT/shAs.txt"
  local pre pstat meas mstat
  HYAKU_SCRATCH="$S" bash "$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh" \
      "$C" "$BASE" "$sha" > "$OUT/precheck-$v.txt" 2>&1
  pstat=$?
  python3 "$M" --repo "$C" --rev "$sha" --explain > "$OUT/measure-$v.json" 2> "$OUT/measure-$v.err"
  mstat=$?
  echo "VARIANT $v sha=$sha precheck_exit=$pstat measure_exit=$mstat"
}

# base itself (floor), no edit
run_variant vbase -
for v in va vb vc vd ve vall; do
  case $v in
    va) run_variant "$v" a ;;
    vb) run_variant "$v" b ;;
    vc) run_variant "$v" c ;;
    vd) run_variant "$v" d ;;
    ve) run_variant "$v" e ;;
    vall) run_variant "$v" a b c d e ;;
  esac
done
echo "--- precheck summaries ---"
for v in vbase va vb vc vd ve vall; do
  echo "## $v"; cat "$OUT/precheck-$v.txt"
done
