#!/usr/bin/env bash
# Witness harness for S_HARDLINK (round-51 C2).
# Witness: baseline path a.txt is a hardlink with link count 2.
# Pristine gate: nlink>1 guard fires -> LINK line, DRIFT summary, exit 1.
# Mutant gate  : nlink>2 guard does not fire -> CLEAN summary, exit 0.
set -u
S=/fast/scratch/hyaku/tameshi-r51/T51LabWitHARDLINK
W="$S/w"
GATE_PRISTINE="$W/pristine.sh"
GATE_MUTANT="$W/mutant.sh"
HOME_DIR="$W/home"

run() { # $1=label $2=gate
  local label="$1" gate="$2" rc i
  for i in 1 2 3; do
    env -i HOME="$HOME_DIR" TMPDIR="$W" PATH="/usr/bin:/bin" \
      "$gate" --baseline "$W/wh-baseline.tsv" --symbols "$W/wh-symbols.tsv" \
      > "$W/out.$label.$i.txt" 2>&1
    rc=$?
    printf '%s run %d: exit=%d\n' "$label" "$i" "$rc"
  done
}

# Pre-run gate hashes (restoration evidence)
sha256sum "$GATE_PRISTINE" "$GATE_MUTANT" > "$W/gates.before.sha256"
run pristine "$GATE_PRISTINE"
run mutant "$GATE_MUTANT"
# Post-run gate hashes
sha256sum "$GATE_PRISTINE" "$GATE_MUTANT" > "$W/gates.after.sha256"
printf 'gates diff before/after: '; diff -q "$W/gates.before.sha256" "$W/gates.after.sha256" >/dev/null && echo identical || echo DIFFER
echo "--- pristine outputs (last lines) ---"
for i in 1 2 3; do echo "== run $i =="; tail -n 3 "$W/out.pristine.$i.txt"; done
echo "--- mutant outputs (last lines) ---"
for i in 1 2 3; do echo "== run $i =="; tail -n 3 "$W/out.mutant.$i.txt"; done
echo "--- differing line (pristine run1 vs mutant run1) ---"
diff "$W/out.pristine.1.txt" "$W/out.mutant.1.txt" || true
