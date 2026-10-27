#!/usr/bin/env bash
# Per-case probe: replicate the pinned selftest's fixture (drift-pins.sh:379-396)
# and run one mutant gate on it, so the case's own output can be read.
# Usage: case-probe.sh <mutant> <sandbox-root-name> <case>
#   case: gone | ambig | shape
set -uo pipefail
MUTANT=$1; ROOT=$2; ID=$3; CASE=$4
h="$ROOT/sandbox-$ID"; mkdir -p "$h/tmp" "$h/home"
export TMPDIR="$h/tmp"
d=$(mktemp -d)
trap 'rm -rf "$d" "$h"' EXIT

printf 'alpha\nbeta\n' > "$d/a.txt"
printf 'one\n' > "$d/b.txt"
amode=$(stat -c '%a' "$d/a.txt")
base="$d/base.tsv"; sym="$d/sym.tsv"
printf '%s\t%s\t2\t%s\n' "$d/a.txt" "$amode" "$(sha256sum "$d/a.txt" | cut -c1-64)" >> "$base"
printf '%s\t%s\t1\t%s\n' "$d/b.txt" "$amode" "$(sha256sum "$d/b.txt" | cut -c1-64)" >> "$base"
printf '%s\t2\t^beta$\n' "$d/a.txt" >> "$sym"
printf '%s\t#1\t^alpha$\n' "$d/a.txt" >> "$sym"
printf '%s\t1\t^one$\n' "$d/b.txt" >> "$sym"
printf 'A=1\nB=2\n' > "$d/env.txt"
printf '%s\t%s\t2\t-\n' "$d/env.txt" "$(stat -c '%a' "$d/env.txt")" >> "$base"
printf '%s\t#2\t^[A-Z][A-Z0-9_]*=\tshape\n' "$d/env.txt" >> "$sym"
export DRIFT_EXTRA_NOHASH="$d/env.txt"

case $CASE in
  gone)  printf 'uno\n' > "$d/b.txt";        word=GONE;  want=1 ;;
  ambig) printf 'one\none\n' > "$d/b.txt";  word=AMBIG; want=1 ;;
  shape) printf 'oops, not an assignment\n' >> "$d/env.txt"; word=SHAPE; want=1 ;;
esac

out=$(env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C DRIFT_EXTRA_NOHASH="$d/env.txt" bash "$MUTANT" --baseline "$base" --symbols "$sym" 2>&1) && rc=0 || rc=$?
printf '  fixture-dir: %s\n' "$d"
printf '  exit=%s want=%s\n' "$rc" "$want"
printf '  output:\n'
printf '%s\n' "$out" | awk '{print "    | " $0}'
if grep -q "$word" <<< "$out"; then w=YES; else w=NO; fi
printf '  grep -q %s <<< out -> match=%s\n' "$word" "$w"
