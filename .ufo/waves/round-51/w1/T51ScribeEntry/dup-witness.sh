#!/usr/bin/env bash
# Seat probe: off-suite witness for S_DUP_UNIQ (the DUP arm is reachable only
# with the DEFAULT baseline; the selftest always passes --baseline).
# Pristine and mutant gates from the pinned bytes; scratch HOME; no real $HOME read.
set -uo pipefail
S=${1:?scratch root}
D="$S/dup"
rm -rf "$D"; mkdir -p "$D/pr/corpus" "$D/mu/corpus" "$D/home"
cp -p "$S/drift-pins.sh" "$D/pr/corpus/drift-pins.sh"
cp -p "$S/w-id/mutant-S_DUP_UNIQ.target.sh" "$D/mu/corpus/drift-pins.sh"
chmod 755 "$D/pr/corpus/drift-pins.sh" "$D/mu/corpus/drift-pins.sh"
H="$D/home"

# every pinned FILES path, materialized under the scratch HOME
awk '/^FILES=\(/,/^\)/' "$S/drift-pins.sh" | grep -o '"\$HOME[^"]*"' | tr -d '"' |
while IFS= read -r rel; do
  p=${rel/\$HOME/$H}
  mkdir -p "$(dirname "$p")"
  printf 'AGENTS line one\nsecond line\n' > "$p"
done

# one symbol row: a file whose ERE matches exactly once at line 1
printf 'AGENTS line one\nsecond line\n' > "$H/.agents/AGENTS.md"
printf '$HOME/.agents/AGENTS.md\t1\t^AGENTS\n' > "$D/pr/corpus/drift-symbols.tsv"

env -i PATH="$PATH" HOME="$H" TMPDIR="$D" LC_ALL=C \
  bash "$D/pr/corpus/drift-pins.sh" --pin >"$D/pin.out" 2>&1
printf 'pin exit=%s: %s\n' "$?" "$(tail -1 "$D/pin.out")"

# duplicate baseline row (the defect the gate reports as DUP)
dup=$(grep -v '^#' "$D/pr/corpus/drift-baseline.tsv" | head -1)
printf '%s\n' "$dup" >> "$D/pr/corpus/drift-baseline.tsv"
cp -p "$D/pr/corpus/drift-baseline.tsv" "$D/pr/corpus/drift-symbols.tsv" "$D/mu/corpus/"

run() { # run <name> <tree>
  env -i PATH="$PATH" HOME="$H" TMPDIR="$D" LC_ALL=C \
    bash "$D/$2/corpus/drift-pins.sh" >"$D/$1.out" 2>&1
  printf '%-9s exit=%s  DUP-lines=%s  last=%s\n' "$1" "$?" \
    "$(grep -c '^DUP' "$D/$1.out")" "$(tail -1 "$D/$1.out")"
}
run pristine pr
run mutant   mu
printf -- '--- diff pristine vs mutant ---\n'
diff "$D/pristine.out" "$D/mutant.out" || true
printf -- '--- pristine output ---\n'
cat "$D/pristine.out"
printf -- '--- mutant output ---\n'
cat "$D/mutant.out"
