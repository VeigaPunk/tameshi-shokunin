#!/usr/bin/env bash
# Replicate the gate's own "symbol gone" selftest case against a chosen binary.
# b.txt is in the baseline (so the file plane prints its DRIFT line first) and in the
# symbols file with pin 1 and ERE ^one$, while its content is "uno" (zero matches).
set -u
mut=$1
d=$(mktemp -d)
printf 'alpha\nbeta\n' > "$d/a.txt"
printf 'uno\n'       > "$d/b.txt"
base="$d/base.tsv"; sym="$d/sym.tsv"
printf '%s\t%s\t2\t%s\n' "$d/a.txt" "$(stat -c '%a' "$d/a.txt")" "$(sha256sum "$d/a.txt" | cut -c1-64)" >> "$base"
printf '%s\t%s\t1\t%s\n' "$d/b.txt" "$(stat -c '%a' "$d/b.txt")" "$(sha256sum "$d/b.txt" | cut -c1-64)" >> "$base"
printf '%s\t2\t^beta$\n' "$d/a.txt" >> "$sym"
printf '%s\t1\t^one$\n' "$d/b.txt" >> "$sym"
out=$("$mut" --baseline "$base" --symbols "$sym" 2>&1) && rc=0 || rc=$?
printf 'D=%s\nRC=%s\n--- OUT ---\n[%s]\n--- END ---\n' "$d" "$rc" "$out"
if grep -q 'GONE' <<< "$out"; then printf 'GREP GONE: MATCH\n'; else printf 'GREP GONE: no match\n'; fi
rm -rf "$d"
