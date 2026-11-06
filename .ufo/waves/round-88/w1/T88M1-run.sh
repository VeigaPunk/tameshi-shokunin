#!/usr/bin/env bash
# T88M1 driver: run one counter byte-file against one fixture control rev, in parallel.
S=/fast/scratch/hyaku/tameshi-r88/T88M1
L="$S/ctrl/lane"
FLEET=/home/vgpnk/Projects/shokunin
W=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-88/w1
mkdir -p "$S/work" "$S/out"
M=$W

rev() { awk -v v="$1" '$1==v{print $2}' "$S/revs.txt"; }

run() { # <tag> <counter> <rev>
  tag=$1; counter=$2; crev=$3; w="$S/work/$tag"
  rm -rf "$w"; mkdir -p "$w"
  ( python3 -I "$counter" --repo "$L" --rev "$crev" --fleet "$FLEET" --work "$w" \
      >"$S/out/$tag.out" 2>"$S/out/$tag.err"; echo "EXIT=$?" >>"$S/out/$tag.out" ) &
}

run M1            "$M/T88M1-M1.py"   "$(rev lanetarget)"
run M2            "$M/T88M1-M2.py"   "$(rev cmp)"
run M3            "$M/T88M1-M3.py"   "$(rev dup)"
run M4            "$M/T88M1-M4.py"   "$(rev unprereg)"
run M5            "$M/T88M1-M5.py"   "$(rev doctored)"
run M6            "$M/T88M1-M6.py"   "$(rev trivial)"
run M8-badpin     "$M/T88M1-M8.py"   "$(rev badpin)"
run FROZEN-badpin "$S/measure.py"    "$(rev badpin)"
run FROZEN-cmp    "$S/measure.py"    "$(rev cmp)"
wait
echo ALL_DONE
grep -H '^C1_R88 ' "$S"/out/*.out | sed "s|$S/out/||"
grep -H '^EXIT=' "$S"/out/*.out | sed "s|$S/out/||"
