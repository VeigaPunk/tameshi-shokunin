#!/usr/bin/env bash
# T92S2 end-to-end: run the frozen counter against three committed fixture states
# that add a contradicting table to the honest note in three different forms.
set -u
S=/fast/scratch/hyaku/tameshi-r92/T92S2
D="$S/fx.clone"
C=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-92/c1/measure-v92.py
declare -A REVS=(
  [A]=26ee4ee2afa4c8deacf200a0d1539b80779cccec   # second table, note's own survivor-row shape, UPPERCASE KILLED
  [B]=41d489ad32dbccb62067aeaf6d3b8b4379b576b6   # second table, note's own survivor-row shape, LOWERCASE killed
  [C]=252b0ba5b7770c401ede02bb3f7e5271ecf4e934   # fenced code block holding a contradicting table
  [D]=654845fccb1e8539e6e749672cc93a0b550052bd   # escaped pipe ( \| ) inside a cell
)
for k in A B C D; do
  rev=${REVS[$k]}
  W="$S/w-$k"; rm -rf "$W"; mkdir -p "$W"
  echo "=== state $k rev=$rev ==="
  python3 -I "$C" --repo "$D" --rev "$rev" --work "$W" > "$S/state-$k.out" 2>&1
  echo "exit=$?"
  grep -E "C1_SUMMARY|C1_CONJUNCTS|C1_R92_PASS|C1_SETUP" "$S/state-$k.out"
done
