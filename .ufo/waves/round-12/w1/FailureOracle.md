# FailureOracle — repeated-control counterexample

Status: the same verifier has a red-before result against the evidence-only one-observation model on the alternate-output mutant, with green model results on pristine and byte-restored fixtures. The actual `tools/repeat-control.py` check remains pending because the file was absent on the latest check. Advisory evidence only; no independent admission or promotion.

## Axes and probe

- **Depth:** the fixture's first observation is green, while subsequent observations change stdout without changing exit status. This targets repeated-control detection rather than an unrelated selftest.
- **Calibration:** the same bytes are expected to yield `controls_match` on pristine/restored source and `controls_mismatch` on the alternate-output mutation, with exit codes 0 and 1 respectively.

`fixture.sh` is a deterministic command fixture. It increments a state file supplied as `FAILURE_ORACLE_STATE`; pristine bytes always emit `CONTROL\n` and exit 0. `fixture-mutation.diff` changes only the output point: first call emits `CONTROL\n`, subsequent calls emit `ALTERNATE\n`, all with exit 0. The raw runs are captured under `single-pristine/`, `single-mutant/`, and `alternate-sequence/`.

## Observations captured

- Single pristine observation command: `FAILURE_ORACLE_STATE=.ufo/evidence/round-12/FailureOracle/single-pristine/state.txt sh .ufo/evidence/round-12/FailureOracle/fixture.sh`. Captured stdout `CONTROL\n`, stderr empty, exit `0` (`single-pristine/{stdout.bin,stderr.bin,exit.txt}`).
- Single alternate-output mutant observation command: `FAILURE_ORACLE_STATE=.ufo/evidence/round-12/FailureOracle/single-mutant/state.txt sh .ufo/evidence/round-12/FailureOracle/fixture.sh`. Captured stdout `CONTROL\n`, stderr empty, exit `0` (`single-mutant/{stdout.bin,stderr.bin,exit.txt`). A one-observation green result therefore does not distinguish the fixture from the pristine command.
- Direct fixture sequence on the alternate-output mutation: three invocations with one shared state file; observed stdout `CONTROL\n`, `ALTERNATE\n`, `ALTERNATE\n`, stderr empty for all, exit `0` for all (`alternate-sequence/run-{1,2,3}.*`). This confirms the fixture exercises output disagreement without introducing a nonzero baseline.

Fixture SHA-256: pristine `a64c7515cb518e78d6bcb06057805a4044422f8697d5bb087a231fef09cb5c9e`; alternate-output mutation `8008b11ae9044fdd21097d9523989da31d11cd978c0edea5995cd02c948cbedc`; restored `a64c7515cb518e78d6bcb06057805a4044422f8697d5bb087a231fef09cb5c9e`. Exact byte restoration is confirmed by the matching original/restored digest. The mutation patch is retained as `fixture-mutation.diff`.

## Same-verifier baseline and production-gate probe

`verify_gate.py` is the standalone black-box verifier, not a gate implementation. It submits the exact `--runs 3 --out DIR -- sh fixture.sh` interface, preserves gate stdout/stderr and process exit, and checks the stable finding ID plus exit (`controls_match`/0 or `controls_mismatch`/1).

The same verifier was run against `single_control_baseline.py`, an evidence-only one-observation model, on pristine bytes, the alternate-output mutant, and the byte-restored source:

- Pristine SHA `a64c7515cb518e78d6bcb06057805a4044422f8697d5bb087a231fef09cb5c9e`, expected `controls_match`: gate output `controls_match\n`, gate exit 0; verifier `VERDICT: PASS`, exit 0 (`pristine-baseline/`).
- Alternate-output mutant SHA `8008b11ae9044fdd21097d9523989da31d11cd978c0edea5995cd02c948cbedc`, expected `controls_mismatch`: gate output `controls_match\n`, gate exit 0, finding absent; verifier `VERDICT: FAIL`, exit 1 (`red-before/`). This is the observed red-before counterexample: a single green observation misses the later output change.
- Restored SHA again `a64c7515cb518e78d6bcb06057805a4044422f8697d5bb087a231fef09cb5c9e`, expected `controls_match`: gate output `controls_match\n`, gate exit 0; verifier `VERDICT: PASS`, exit 0 (`restored-baseline/`).

The actual `tools/repeat-control.py` was absent on the latest check, so the required production-gate green-after result and a one-observation mutation of its isolated `/tmp` copy are not claimed. When available, run the same verifier expecting `controls_mismatch` against the one-observation scratch copy (expect verifier exit 1), then against the unmodified gate (expect verifier exit 0). The evidence-only model is not claimed to be the previous production gate. No production file was changed; no build, test suite, lint, or formatter was run. No tool was installed or updated.

## Owned paths

- `.ufo/evidence/round-12/FailureOracle/fixture.sh`
- `.ufo/evidence/round-12/FailureOracle/fixture-mutation.diff`
- `.ufo/evidence/round-12/FailureOracle/verify_gate.py`
- `.ufo/evidence/round-12/FailureOracle/single_control_baseline.py`
- `.ufo/evidence/round-12/FailureOracle/red-before/`
- `.ufo/evidence/round-12/FailureOracle/red-before-verifier.stdout.bin`
- `.ufo/evidence/round-12/FailureOracle/red-before-verifier.stderr.bin`
- `.ufo/evidence/round-12/FailureOracle/red-before-verifier.exit.txt`
- `.ufo/evidence/round-12/FailureOracle/pristine-baseline/`
- `.ufo/evidence/round-12/FailureOracle/pristine-baseline-verifier.stdout.bin`
- `.ufo/evidence/round-12/FailureOracle/pristine-baseline-verifier.stderr.bin`
- `.ufo/evidence/round-12/FailureOracle/pristine-baseline-verifier.exit.txt`
- `.ufo/evidence/round-12/FailureOracle/restored-baseline/`
- `.ufo/evidence/round-12/FailureOracle/restored-baseline-verifier.stdout.bin`
- `.ufo/evidence/round-12/FailureOracle/restored-baseline-verifier.stderr.bin`
- `.ufo/evidence/round-12/FailureOracle/restored-baseline-verifier.exit.txt`
- `.ufo/evidence/round-12/FailureOracle/single-pristine/`
- `.ufo/evidence/round-12/FailureOracle/single-mutant/`
- `.ufo/evidence/round-12/FailureOracle/alternate-sequence/`
- `.ufo/waves/round-12/w1/FailureOracle.md`
