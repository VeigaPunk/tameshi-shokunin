#!/usr/bin/env bash
S=/fast/scratch/hyaku/tameshi-r88/T88M1
L="$S/ctrl/lane"; FLEET=/home/vgpnk/Projects/shokunin
W=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-88/w1
M=$W; mkdir -p "$S/out"
rev() { awk -v v="$1" '$1==v{print $2}' "$S/revs.txt"; }
run() { tag=$1; counter=$2; crev=$3; w="$S/work/$tag"
  rm -rf "$w"; mkdir -p "$w"
  ( python3 -I "$counter" --repo "$L" --rev "$crev" --fleet "$FLEET" --work "$w" \
      >"$S/out/$tag.out" 2>"$S/out/$tag.err"; echo "EXIT=$?" >>"$S/out/$tag.out" ) & }
run M8-liebadpin      "$M/T88M1-M8.py" "$(rev lie-badpin)"
run FROZEN-liebadpin  "$S/measure.py"  "$(rev lie-badpin)"
run M5-liebadpin      "$M/T88M1-M5.py" "$(rev lie-badpin)"
wait
echo ALL_DONE
grep -H '^C1_R88 \|^EXIT=' "$S"/out/M8-liebadpin.out "$S"/out/FROZEN-liebadpin.out "$S"/out/M5-liebadpin.out | sed "s|$S/out/||"
grep -h 'py-kake' "$S"/out/M8-liebadpin.out "$S"/out/FROZEN-liebadpin.out
