# ReReplay17 — re-attack of round-23 Replay17 (row `mutate-and-run-selftest`)

## Verdict

The row's static exact binding holds, in the frozen round-23 artifacts and at lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df. I found no field-level false acceptance in the retained evidence for this row. My strongest adversarial delta, a receipt that reports `MUTATE_SELFTEST: 0/96 pass` with exit 0, does pass the ruler. But the producer at blob d22c40 cannot emit that output, so getting it accepted needs a forged receipt, and producer authentication is out of scope. That makes it a documented tradeoff, not a defect. Separately, I found one fixable provenance-labelling defect in the replay instrument. It did not produce a false value in this run.

Axes: A1 identity (argv, cwd, revision), A2 outcome fidelity (exit and stdout tokens on the same receipt), A3 provenance honesty (present versus inferred), A4 currency at c9ff09fb.

## What I checked (A1 and A2: frozen requirement against baseline source)

- `.ufo/evidence/round-23/requirements.json` `requirements[16]` is `{"name":"mutate-and-run-selftest","argv":["bash","tools/mutate-and-run.sh","--selftest"],"expect":{"exit":0,"stdout_contains":["MUTATE_SELFTEST:","VERDICT: PASS"]}}`. It is identical to `replay/bundle.json` `requirements[16]` (Python equality returned `True`).
- `registry-baseline.json` has sha256 `ebd2e69a…ec92a`. That equals `requirements.json.registry_sha256`, and it also equals `git show <rev>:tools/registry.json | sha256sum` at both 28cae179 (`source_revision`) and 496d212b (the replay revision). The baseline row is identical to the frozen requirement. `replay.py:36-41` refuses to run on any digest or projection mismatch.
- The executed script is the same file across all three revisions: `git show <rev>:tools/mutate-and-run.sh | sha256sum` gives `d22c4025…a8b` at 28cae179, 496d212b and c9ff09fb. The 28cae179 ≠ 496d212b revision gap therefore makes no difference to which script bytes this row ran.
- The receipt is `bundle.json` `receipts[16]`:
  - argv is identical.
  - cwd is `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`, equal to bundle `cwd`.
  - revision is `496d212b…`, equal to bundle `revision`.
  - exit is the integer `0`.
  - stderr is `""`.
- The stdout is 4515 bytes and 98 lines: 96 `PASS ` lines, then `MUTATE_SELFTEST: 96/96 pass`, then `VERDICT: PASS`. The tokens appear at byte offsets 4473 and 4501, once each, in the producer's order (`mutate-and-run.sh:1906-1908`).
  - No line starts with `FAIL `. The 7 lines containing "FAIL" are PASS-case descriptions, for example `PASS out-of-band FAIL names flips=2`.
  - 86 PASS names occur literally in the d22c40 source. The other 10 are loop-templated (`leg-count agreement…`, `embedded leg <8 names>…`).
- I checked the full output, not just the tail. `observations.json` `rows[16].runner_result.stdout` is byte-equal to the receipt stdout, and `stdout_tail` is a strict suffix of it. `elapsed_s` 5.457 matches the row `measurement_interval` (14:42:31.059684 to 14:42:36.516724). The row interval lies inside the replay interval in `replay-command-A.json`.
- I ran the read-only ruler on scratch copies (`/tmp/rr17-scratch.ZYl0`). The command was `python3 cb-{496,c9ff}.py --bundle bundle.json --expected expected.json --json`, using `git show` copies of `tools/command-binding.py` at 496d212b and at c9ff09fb. Both runs returned `{"bundle_sha256":"3d6c99b7…50b9","exit":0,"finding_ids":[]}` with rc=0, which matches `replay-gate-A.json`.

## Present versus inferred (A3)

- **Present in the retained artifacts:** the full stdout and stderr, the integer exit, the per-row wall-clock interval, `elapsed_s`, the requirement digests, and the replay command line (`observations.json.argv`, `--rev 496d212b…`).
- **[INFERENCE] from code, not observed:**
  - The receipt `argv` comes from `list(row['argv'])` (`replay.py:62`), and `cwd` and `revision` come from the same local variables used for the bundle header (`replay.py:62-69`). That means `ARGV_MISMATCH`, `CWD_MISMATCH` and `REVISION_MISMATCH` cannot fire on any bundle this instrument produces. They compare two copies of the same value.
  - That the child actually ran with that argv and cwd is inferred from `registry-check.py@496d212b:676-683` (`Popen(row["argv"], cwd=cwd, …)`, where `row` is the same object).
  - That the clone was at 496d212b is inferred from `git checkout --detach` with `check=True` (`replay.py:50`). No post-checkout `HEAD` or script blob hash was retained.
  - There is no pid, no resolved `bash` path and no environment capture.
- `expected.json` was written by the same producer in the same process (`replay.py:74-75`). Its digest check proves the bundle bytes were not changed after the run. It is not an independent caller commitment and does not authenticate the producer. I make no authentication claim, and I found no historical metadata retrofill for this row: the invocation fields were recorded beside the newly executed row (`replay.py:62-63`).

## Adversarial delta: unpinned count (tradeoff, not a defect)

I built scratch bundles containing only row 16 and recomputed `expected.json` for each. Both rulers (496d212b and c9ff09fb) gave the same result:

| receipt stdout (exit) | result |
|---|---|
| real 96/96 stdout (0) | rc=0, `[]` |
| `MUTATE_SELFTEST: 0/96 pass\nVERDICT: PASS\n` (0) | rc=0, `[]` |
| `PASS help exits 0\nMUTATE_SELFTEST: 1/1 pass\nVERDICT: PASS\n` (0) | rc=0, `[]` |
| `VERDICT: PASS\nFAIL x\nMUTATE_SELFTEST: 95/96 pass\nVERDICT: FAIL (…)\n` (0) | rc=0, `[]` |
| `xMUTATE_SELFTEST:yVERDICT: PASSED-ISH` (0) | rc=0, `[]` |
| `MUTATE_SELFTEST: 96/96 pass\n` (0), negative control | rc=1, `STDOUT_MISMATCH` |
| real stdout (1), negative control | rc=1, `EXIT_MISMATCH` |

The `MUTATE_SELFTEST:` token is a label only. It does not constrain the count, the position or the line boundary. Here is why I don't count this as a false acceptance of this row:

- At blob d22c40, `VERDICT: PASS` with exit 0 is printed only when `failed == 0` (`mutate-and-run.sh:1906-1913`). Every failure path exits 1 (`:1392-1393`, `:1912-1913`). So rows two to five are forged receipts.
- `--help` stdout contains neither token. Those tokens appear only at `:1392`, `:1436` (inside a captured fixture heredoc), `:1906` and `:1908`.
- A real weakening of the producer would still pass. If a mutant deleted `st` calls, the producer would print `MUTATE_SELFTEST: N/N pass` and `VERDICT: PASS` with exit 0, so it would be accepted. **[INFERENCE]:** I did not run this, because the item forbids running the suite.
- Pinning `96/96` per row would conflict with legitimate count drift, which round-23 Command17 already argued. `stdout_contains` cannot express "N/N with equal N".

The smallest safe correction, if the judge wants it, is to add an anchored token such as `\nVERDICT: PASS\n` and pin the count in a revision-scoped requirement, not in the timeless registry row. The ruler itself needs no change.

## Fixable provenance-labelling defect (latent, no false value here)

- `observations.json.runner_sha256` is computed as `sha256(args.repo/'tools/registry-check.py')`, which is the live working tree (`replay.py:78`). But the module that actually ran is `clone/'tools/registry-check.py'` (`replay.py:54-56`).
- `replay-command-A.json.instrument_sha256["tools/registry-check.py"]` has the same live-tree basis.
- In this run the value `cba16646…44ad` equals `git show 496d212b:tools/registry-check.py | sha256sum`, so nothing false was recorded. If the live tree is dirty or at a different HEAD, the field would name a runner that did not execute.
- Correction: hash `clone / 'tools/registry-check.py'` (or `git show <revision>:tools/registry-check.py`) before `exec_module`, and record `git -C clone rev-parse HEAD` after checkout.

This instrument is frozen round-23 evidence and is not a current production gate.

## Does it still apply at c9ff09fb?

- The row is not superseded. `git show c9ff09fb:tools/registry.json` (sha `a8f255f1…`, now different from the baseline file) still has the identical `mutate-and-run-selftest` row with `status:"active"`.
- `tools/mutate-and-run.sh` is unchanged (d22c40).
- Between 496d212b and c9ff09fb, `tools/command-binding.py` changed only in its selftest fixture loading: it now also reads `round-24/extra-cases.json`. `evaluate()` is byte-identical, which is why the scratch table above is identical under both versions.
- The on-disk `tools/command-binding.py` matches the c9ff09fb blob (`9230c68e…`).
- The round-24 replay (`.ufo/evidence/round-24/replay/bundle.json`, revision d2eaecd) also shows `MUTATE_SELFTEST: 96/96 pass` and `VERDICT: PASS` with exit 0 for this row.
- The round-25 multitoken fixtures (`multitoken-cases.json`, `multitoken-mutants.spec`) cover all-of versus any-of and first or last token. They do not cover count or anchoring, so the tradeoff above stands unchanged.

## Bounds

- I wrote only this report.
- Scratch files are in `/tmp/rr17-scratch.ZYl0` and `/tmp/rr17-*.sh|py`.
- I did not run the registry command, any suite or any selftest.
- Git use was read-only, with `GIT_OPTIONAL_LOCKS=0`.
- I installed or updated no tools.

R23-REATTACK Replay17: AGREE
