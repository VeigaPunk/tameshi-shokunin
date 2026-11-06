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
run M5-forged        "$M/T88M1-M5.py"  "$(rev forged)"
run FROZEN-forged    "$S/measure.py"   "$(rev forged)"
run M8-forgedbadpin  "$M/T88M1-M8.py"  "$(rev forged-badpin)"
run FROZEN-forgedbadpin "$S/measure.py" "$(rev forged-badpin)"
wait
echo ALL_DONE
grep -H '^C1_R88 \|^EXIT=' "$S"/out/M5-forged.out "$S"/out/FROZEN-forged.out "$S"/out/M8-forgedbadpin.out "$S"/out/FROZEN-forgedbadpin.out | sed "s|$S/out/||"
