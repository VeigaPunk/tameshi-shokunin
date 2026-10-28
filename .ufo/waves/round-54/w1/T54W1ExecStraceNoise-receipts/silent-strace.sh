#!/usr/bin/env bash
# MUTANT strace: consumes strace's own options, emits an EMPTY log, runs the program.
out=""
args=("$@"); i=0
while [ $i -lt ${#args[@]} ]; do
  case "${args[$i]}" in
    -o) out="${args[$((i+1))]}"; i=$((i+2));;
    -e|-p|-s|-u|-a|-b|-I|-X) i=$((i+2));;
    -f|-ff|-F|-tt|-ttt|-T|-q|-qq|-v|-y|-yy|-c|-C|-z) i=$((i+1));;
    --) i=$((i+1)); break;;
    *) break;;
  esac
done
[ -n "$out" ] && : > "$out"
exec "${args[@]:$i}"
