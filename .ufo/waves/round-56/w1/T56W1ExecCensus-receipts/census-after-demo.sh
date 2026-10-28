#!/usr/bin/env bash
# census-after.sh demonstration driver (round-56, seat T56W1ExecCensus).
# One clean new row plus five shape mutants and one env mutant, each on its own copy of
# corpus/ + tools/ so the census's E11 used-by resolution stays honest.
set -u
S=$1; R=$2; LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
H=$LANE/.ufo/waves/round-56/census-after.sh
BASE=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["base"])' "$LANE/.ufo/evidence/round-56/contract.json")
insert() { # <file> <row> — insert after the last registry row; ENVIRON keeps backslashes
  ROW=$2 gawk '/^ {0,3}\| S[0-9]{3,} \|/ { last=NR } { lines[NR]=$0 }
    END { for (i=1;i<=NR;i++) { print lines[i]; if (i==last) print ENVIRON["ROW"] } }' \
    "$1" > "$1.new" && mv "$1.new" "$1"
}
for c in clean m10col escpipe baddate outside future; do
  mkdir -p "$S/$c/lane"
  cp -a "$LANE/corpus" "$LANE/tools" "$S/$c/lane/"
done
insert "$S/clean/lane/corpus/SOURCES.md"   '| S281 | Demo source — https://example.invalid/demo | docs | B | demo scope | §Demo | demo teaches text for a valid new row | queued | 2026-10-28 | 90d | — |'
insert "$S/m10col/lane/corpus/SOURCES.md"  '| S281 | Demo source — https://example.invalid/demo | docs | B | demo scope | §Demo | demo teaches text, used-by cell dropped | queued | 2026-10-28 | 90d |'
insert "$S/escpipe/lane/corpus/SOURCES.md" '| S281 | Demo source — https://example.invalid/demo | docs | B | demo scope | §Demo | pipe \| inside the teaches cell | queued | 2026-10-28 | 90d | — |'
insert "$S/baddate/lane/corpus/SOURCES.md" '| S281 | Demo source — https://example.invalid/demo | docs | B | demo scope | §Demo | bad opened date and bad status | watch | 2026-13-45 | 90d | — |'
insert "$S/future/lane/corpus/SOURCES.md"  '| S281 | Demo source — https://example.invalid/demo | docs | B | demo scope | §Demo | opened in the future | queued | 2027-01-01 | 90d | — |'
printf '%s\n' '| S281 | Demo source — https://example.invalid/demo | docs | B | demo scope | §Demo | row appended outside Registry | queued | 2026-10-28 | 90d | — |' >> "$S/outside/lane/corpus/SOURCES.md"
for c in clean m10col escpipe baddate outside future; do
  bash "$H" --sources "$S/$c/lane/corpus/SOURCES.md" --base "$BASE" --label "$c" \
    > "$R/census-after-demo-$c.stdout" 2> "$R/census-after-demo-$c.stderr"
  echo "case=$c exit=$?"
done
bash "$H" --sources "$S/clean/lane/corpus/SOURCES.md" --base 0000000000000000000000000000000000000000 --label badbase \
  > "$R/census-after-demo-badbase.stdout" 2> "$R/census-after-demo-badbase.stderr"
echo "case=badbase exit=$?"
bash "$H" --sources "$S/escpipe/lane/corpus/SOURCES.md" --base "$BASE" --label escpipe-shapeonly --shape-only \
  > "$R/census-after-demo-shapeonly.stdout" 2> "$R/census-after-demo-shapeonly.stderr"
echo "case=shapeonly exit=$?"
