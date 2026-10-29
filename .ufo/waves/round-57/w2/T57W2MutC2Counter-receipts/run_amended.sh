set -u
S=/fast/scratch/hyaku/tameshi-r57/T57W2MutC2Counter
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=ca75c2674645ab6bdadeecb8584007c74342bfa9
OUT="$S/aout"; mkdir -p "$OUT" "$S/tmp"
run_one() {
  id="$1"; dir="$2"; w="$S/awork/$id"; rm -rf "$w"; mkdir -p "$w"
  ( cd "$w" && TMPDIR="$S/tmp" python3 "$dir/measure.py" --selftest --lane "$LANE" --rev "$REV" \
      >"$OUT/$id.stdout" 2>"$OUT/$id.stderr"; echo $? >"$OUT/$id.exit" )
}
export -f run_one; export S LANE REV OUT
printf '%s\n' "AMENDED $S/amended" "M3 $S/amended_mut/M3" "M5 $S/amended_mut/M5" "M6 $S/amended_mut/M6" "M8 $S/amended_mut/M8" "M9 $S/amended_mut/M9" "M12 $S/amended_mut/M12" \
 | xargs -P 4 -I{} bash -c 'set -- {}; run_one "$1" "$2"' _ {}
echo AMENDED_DONE
