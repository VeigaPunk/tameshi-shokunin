# RedBefore — FailureOracle command review (round 12, w2)

Axes: (1) detect the one-run false match, (2) isolate the gate-only fix delta, (3) preserve a reproducible non-destructive experiment. No behavioral detector was run and no repo source was changed. Temporary, unmutated scratch gate copies had equal SHA-256 `29d8025490f349c106bc8132da7bfecc2ae4f8fb00720b43636e52335d27467a` and were removed. No tooling was installed or updated.

## Observed inherited evidence

- `verify_gate.py:17-18` binds the fixture to a sibling `fixture.sh`; `:31-50` invokes the candidate with `--runs 3` and gives each output directory its own `FAILURE_ORACLE_STATE`; `:56-60` requires both the expected finding text and its mapped exit; `:73-80` records the observed output/verdict and returns nonzero on a failed expectation.
- `single_control_baseline.py:9-13,18-32` parses `--runs` but calls `subprocess.run` exactly once and reports `controls_match` whenever that one child exits 0. This is the red-before defect: it cannot compare repeated observations.
- The recorded mutation `.ufo/evidence/round-12/FailureOracle/fixture-mutation.diff:1-9` changes stdout after the first invocation (`CONTROL` then `ALTERNATE`). The associated alternate-sequence evidence records count `3` and stdout `CONTROL`, `ALTERNATE`, `ALTERNATE` (`alternate-sequence/state.txt:1`, `run-1.stdout.bin:1`, `run-2.stdout.bin:1`, `run-3.stdout.bin:1`).
- The inherited red-before verifier record expected `controls_mismatch`/exit 1, but observed exit 0, no expected finding, and `verifier_pass: false` (`red-before/manifest.json:2-19`); its captured gate stdout is `controls_match` (`red-before/gate.stdout:1`) and its sole saved child stdout is `CONTROL` (`red-before/gate-runs/run-1.stdout:1`).
- The fixed candidate classifies disagreement in exit/stdout/stderr as `controls_mismatch` before stable nonzero handling (`tools/repeat-control.py:191-205`); its run mode writes and emits the finding with its mapped exit (`:319-331`). Existing `actual-pristine/manifest.json:2-19` only demonstrates `controls_match` on the unchanged fixture, not the mutated-fixture delta.

## Concrete proposed command (not executed)

This makes an isolated scratch copy of the verifier and an alternating fixture. Both checks use that exact verifier, fixture, and expected finding; only `--gate` changes. Fresh output dirs keep state independent. The first verifier failure is captured so the second check still runs.

```sh
repo=/home/vgpnk/Projects/shokunin/tameshi-shokunin
cd "$repo"
tmp=$(mktemp -d /tmp/failure-oracle-r12.XXXXXX)
cp .ufo/evidence/round-12/FailureOracle/verify_gate.py "$tmp/verify_gate.py"
cat > "$tmp/fixture.sh" <<'SH'
#!/bin/sh
set -eu
state=${FAILURE_ORACLE_STATE:?FAILURE_ORACLE_STATE is required}
count=0
if [ -f "$state" ]; then
    IFS= read -r count < "$state" || :
fi
count=$((count + 1))
printf '%s\n' "$count" > "$state"
if [ "$count" -eq 1 ]; then
    printf 'CONTROL\n'
else
    printf 'ALTERNATE\n'
fi
SH
/usr/bin/python3 "$tmp/verify_gate.py" \
  --gate "$repo/.ufo/evidence/round-12/FailureOracle/single_control_baseline.py" \
  --out "$tmp/red-before" --expect controls_mismatch
red_rc=$?
/usr/bin/python3 "$tmp/verify_gate.py" \
  --gate "$repo/tools/repeat-control.py" \
  --out "$tmp/fixed" --expect controls_mismatch
fixed_rc=$?
printf 'red_before_verifier_exit=%s fixed_verifier_exit=%s\n' "$red_rc" "$fixed_rc"
test "$red_rc" -eq 1 && test "$fixed_rc" -eq 0
```

Expected stable reason: the fixed gate should report `controls_mismatch` (gate exit 1), because the three successful child runs have different stdout bytes (`CONTROL\n` versus `ALTERNATE\n`). Red-before should still emit `controls_match` (gate exit 0) from its single successful run, so the verifier expecting `controls_mismatch` should fail (verifier exit 1); the fixed-candidate verifier should pass (verifier exit 0). These are predictions from the inspected source and inherited records, not newly observed outcomes.

Owned report: `.ufo/waves/round-12/w2/RedBefore.md`. No production or sibling files changed.