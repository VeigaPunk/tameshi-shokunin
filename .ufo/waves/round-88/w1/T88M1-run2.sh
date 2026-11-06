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
run M3-dup11     "$M/T88M1-M3.py"  "$(rev dup11)"
run FROZEN-dup11 "$S/measure.py"   "$(rev dup11)"
run M6-inert     "$M/T88M1-M6.py"  "$(rev inert)"
run FROZEN-inert "$S/measure.py"   "$(rev inert)"
wait
echo ALL_DONE
grep -H '^C1_R88 \|^EXIT=' "$S"/out/M3-dup11.out "$S"/out/FROZEN-dup11.out "$S"/out/M6-inert.out "$S"/out/FROZEN-inert.out | sed "s|$S/out/||"
