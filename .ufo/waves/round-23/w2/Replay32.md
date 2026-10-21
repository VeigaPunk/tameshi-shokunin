**Verdict for row `round19-correction-ruler-selftest`:** the command binding (argv, expected exit, cwd, revision) is statically exact. But the gate still accepts a false receipt because of how weak the frozen stdout token is. The executed output for this row is genuinely present in the replay files. The argv, cwd and revision in the receipt are copied from the producer's own inputs, not observed independently.

I did not write `.ufo/waves/round-23/w2/Replay32.md`: the wave context forbids every file write, including the Report trailer, and that rule overrides the ticket's report line. I ran no registry command, suite, build or test. My only executions were JSON parsing in memory, `sha256sum`, `rg`, and read-only git object lookups (`cat-file`, `log`, `rev-parse`, `diff` with `GIT_OPTIONAL_LOCKS=0`). I installed nothing.

## Static binding (confirmed exact)
- **Requirement matches baseline.** The `requirements.json` row is exactly argv `["python3",".ufo/evidence/round-19/measure.py","--selftest"]` with expect `{exit:0, stdout_contains:["SELFTEST: "]}`. That equals the active row in `registry-baseline.json`. The baseline file's SHA-256 is `ebd2e69a…`, which matches `requirements.registry_sha256` and also matches `28cae179:tools/registry.json` hashed from git.
- **Bundle and receipt match the requirement.** The bundle's requirement equals the frozen one, and the receipt argv equals the requirement argv. In `registry-check.py:676-683`, `run_row` passes the same `row["argv"]` to `Popen` with `cwd=clone`, so the argv is exact with no shell normalization.
- **Source is identical across revisions.** `measure.py` has the same blob (`9ca9fb97`) at base `28cae179`, at replay revision `496d212b`, at delivered revision `336565fc`, and in the working tree. Its selftest prints `SELFTEST: N/M` and returns 1 if any case failed (`measure.py:391-392`).
- **Integrity holds.** `sha256(replay/bundle.json)` is `3d6c99b7…`, which equals `expected.json`.

## Evidence actually present
- **Full output is retained in the observation.** `observations.rows[].runner_result.stdout` is byte-equal to the receipt stdout: 1967 characters, 44 lines, 43 `CASE … PASS` lines, 0 FAIL, and a final line `SELFTEST: 43/43`. There is no U+FFFD replacement character, stderr is empty, the exit was 0, and the run took 1.437 s inside a row interval of 14:44:52.99–14:44:54.43 UTC.
- **The tail is not standing in for the output.** `stdout_tail` happens to equal the full output only because the output is short.
- **No historical retrofill.** The rows are newly produced by `replay.py`, and nothing writes into historical observations.

## What is inferred or self-attested, not evidenced
- **argv, cwd and revision are copies.** `replay.py:62-69` copies them from `row['argv']`, `str(clone)` and `rev-parse`; nothing observes the process command line. So the gate's `ARGV_MISMATCH`, `CWD_MISMATCH` and `REVISION_MISMATCH` checks are tautological for producer-built bundles.
- **The "trusted" commitment comes from the producer.** `expected.json` is written by the same `replay.py` run, so the "trusted caller-owned commitment" is self-attested. I reject producer authentication.
- **The replay ran at a different revision.** It ran at `496d212b`, the implementation commit, not at the delivered `336565fc` or at base. Nothing binds the bundle's `revision` to the contract. For this row the gap doesn't matter, because `measure.py` and `registry-check.py` are blob-identical across those revisions.
- **The runner hash comes from the wrong file.** `observations.runner_sha256` hashes `args.repo/tools/registry-check.py` (the live tree), not the module that was actually loaded from the clone. Both are `cba16646…` today; that they matched at replay time is my inference.
- **The historical R17-CMD-BIND row is not closed by this.**

## Field-level false acceptance
The token `stdout_contains: ["SELFTEST: "]` is an unanchored substring and is not tied to the pass count. `command-binding.py:111` accepts any stdout containing it, so all of these pass:
- `SELFTEST: 0/43` with exit 0, a combination the real `measure.py` cannot produce.
- `SELFTEST: 1/1`, which would hide deleted cases.
- `WITNESS_SELFTEST: 43/43 pass`, which contains the token as a substring.

At least 10 other receipts in the same bundle contain the token, for example `bash-witness-selftest`, `measure-round16-selftest` and `pin-disposition-selftest`.

There is a second leak in the receipt's fields. In the runner, `held` also requires `cleanup_ok` (`registry-check.py:720`), but the receipt keeps only `exit=got`. A row whose descendant processes survived bounded cleanup would therefore show `held=false` in the runner yet produce a receipt the gate passes as CLEAN.

## Concrete adversarial delta
1. In `replay/bundle.json`, set this row's `receipts[].stdout` to the genuinely produced stdout of the `bash-witness-selftest` receipt, and leave argv, cwd, revision and exit unchanged.
2. Recompute `expected.json` with the new hash. This is trivial, because the producer owns that file.

**Result:** I derived this from reading `evaluate()` at lines 99-113 and did not execute it. The gate should return exit 0 with no findings, CLEAN, even though the stdout came from a different command.

**Impacted axes:** stdout and outcome binding, the false-acceptance rate, and how far the gate can be trusted (provenance).

## Smallest safe correction
Freeze a stronger expectation for this row: either an anchored full line such as `\nSELFTEST: 43/43\n`, or the exact stdout SHA-256 (`78cc6528e07531fe5a00b831ea8dbe12162d6490521306f65168a9a3ddf02d21`). Add `cleanup_ok`, or the runner's `held`, as a required receipt field the gate checks. Have `expected.json` come from the L1 caller, pinned to the delivered revision, rather than from `replay.py`.

The first part is a defect that can be fixed. Self-attested argv and cwd are a disclosed tradeoff, which the gate's docstring already acknowledges, not a defect to fix in this row.
