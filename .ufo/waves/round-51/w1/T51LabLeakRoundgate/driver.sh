#!/usr/bin/env bash
# T51LabLeakRoundgate probe driver; mirrors mutate-and-run.sh run_one semantics.
# Suite A: recorded suite (sandbox-$DEFECT_ID). Suite B: single-variable probe
# (sandbox-n<ordinal>). Verdict map (runner): 0 -> SURVIVED, 124/126/127 ->
# INCONCLUSIVE, else KILLED.
set -u
S=/fast/scratch/hyaku/tameshi-r51/T51LabLeakRoundgate
WORKDIR="$S/work"
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"

suite_A='h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest'
suite_B='h="$WORKDIR/sandbox-$ORDINAL"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest'

printf 'run\tvariant\tsandbox\tmutant-sha256\texit\n' > "$WORKDIR/exits.tsv"

run() { # name mutant defectid ordinal variant
  local name="$1" mutant="$2" id="$3" ord="$4" var="$5"
  local ev="$WORKDIR/$name.out"
  local rc start now
  start=$(date +%s%N)
  if [[ "$var" == A ]]; then
    MUTANT="$mutant" WORKDIR="$WORKDIR" DEFECT_ID="$id" \
      timeout 300 bash -c "$suite_A" </dev/null >"$ev" 2>&1
    rc=$?
  else
    MUTANT="$mutant" WORKDIR="$WORKDIR" ORDINAL="$ord" \
      timeout 300 bash -c "$suite_B" </dev/null >"$ev" 2>&1
    rc=$?
  fi
  now=$(date +%s%N)
  local dur=$(( (now - start) / 1000000 ))
  printf '%s\t%s\tsandbox-%s\t%s\t%s\t(%sms)\n' "$name" "$var" "${id:-n$ord}" \
    "$(sha256sum "$mutant" | cut -d' ' -f1)" "$rc" "$dur" | tee -a "$WORKDIR/exits.tsv"
}

run ctl_A "$S/round-gate.mjs" CONTROL n0 A
run ctl_B "$S/round-gate.mjs" CONTROL n0 B
i=1
for id in A1 A3 B1 E3 C1060 C1059 A2 B2 CKIND E1; do
  run "mut_A_$id" "$S/mutant-$id.mjs" "$id" "n$i" A
  run "mut_B_$id" "$S/mutant-$id.mjs" "$id" "n$i" B
  i=$((i+1))
done
