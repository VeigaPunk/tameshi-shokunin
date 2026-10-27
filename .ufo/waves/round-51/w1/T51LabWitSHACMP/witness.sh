#!/usr/bin/env bash
# T51LabWitSHACMP — C2 S_SHA_CMP off-suite witness driver.
# Builds a minimal fixture: one hashed file pinned by baseline (mode/lines/sha)
# plus one symbol row, runs pristine and mutant gates on the same witness.
set -u
S=/fast/scratch/hyaku/tameshi-r51/T51LabWitSHACMP
W="$S/fix/w"; HOME_S="$S/home"; OUT="$S/out"
mkdir -p "$W" "$HOME_S" "$OUT"
PRIS="$S/drift-pins.pristine.sh"
MUT="$S/fix/drift-pins.mutant.sh"

cd "$W"

# --- fixture -------------------------------------------------------------
printf 'alpha\nbeta\n' > f.txt            # pristine content, 2 lines
MODE=$(stat -c '%a' f.txt)
SHA=$(sha256sum f.txt | cut -c1-64)
printf '%s\t%s\t2\t%s\n' "$W/f.txt" "$MODE" "$SHA" > base.tsv
printf '%s\t1\t^alpha$\n' "$W/f.txt" > sym.tsv

run_gate() { # $1=label $2=gate $3=suffix; prints "exit=<rc> last=<last>"
  local rc last
  out=$(env -i HOME="$HOME_S" TMPDIR="$S" PATH="$PATH" bash "$2" \
        --baseline "$W/base.tsv" --symbols "$W/sym.tsv" 2>&1); rc=$?
  last=$(printf '%s\n' "$out" | tail -n1)
  printf '%s\n' "$out" > "$OUT/$1.$3.out"
  printf '%s exit=%s last=<%s>\n' "$1" "$rc" "$last"
}

echo "== control A: pristine gate on pristine f.txt (expect CLEAN/0) =="
run_gate control-pristine "$PRIS" clean
echo "== control B: mutant gate on pristine f.txt (expect CLEAN/0) =="
run_gate control-mutant "$MUT" clean

echo "== mutate f.txt: same line count, same mode, new bytes =="
printf 'alpha\nBETA\n' > f.txt
echo "mode now: $(stat -c '%a' f.txt) (was $MODE); lines now: $(wc -l < f.txt)"
echo "sha now : $(sha256sum f.txt | cut -c1-12)... (was ${SHA:0:12}...)"

echo "== witness: pristine gate x3 =="
for i in 1 2 3; do run_gate witness-pristine "$PRIS" "$i"; done
echo "== witness: mutant gate x3 =="
for i in 1 2 3; do run_gate witness-mutant "$MUT" "$i"; done

echo "== diff of outputs (pristine vs mutant, run 1) =="
diff -u "$OUT/witness-pristine.1.out" "$OUT/witness-mutant.1.out" || true
