done — **genuinely discriminated**. D02 is KILLED by its intended attached-nonmaster-branch behavioral case, not by an incidental harness failure.

# KillD02 — round-21 FALSIFY

- Axes: **operability** (the frozen detector runs and kills D02) and **calibration** (identify the actual discriminator and bound the claim).
- Measured implementation: `790abd2129f153c13b471e381d454186edbde65e`.
- Scope: D02 only, `tools/evidence-disposition.py`. Production was read-only; mutation/restoration edits were confined to `/tmp/tameshi-r21-KillD02-veuntk5e/fleet/tameshi-shokunin/tools/evidence-disposition.py`.
- This dispatched seat supplies author-side advisory evidence, not independent admission, integration, or a numeric expertise increase.

## Frozen mutant and expected detector

The frozen contract `.ufo/evidence/round-21/c1-mutants.json:73-77` specifies exactly:

```python
# old
branch = ref[len(prefix):]
# new
branch = "master"
```

At the measured implementation this is `tools/evidence-disposition.py:472`, inside `resolve_historical_anchor` (`460-490`). Its intended behavior is to derive an unconfigured attached local branch from `symbolic-ref HEAD`, not silently assume master.

The owning discriminator is `v2-nonmaster-attached-branch` (`tools/evidence-disposition.py:2715-2717`). Its fixture calls `_setup_hist_clean` and renames the attached branch to `verification` (`2702-2704`); the setup commits pinned bytes and then a moved instrument (`2076-2082`). It expects CLI exit **0**, no findings, payload exit **0**, and status **clean**. The adjacent explicitly configured branch case (`2706-2709`, `2718-2720`) is a useful specificity control: it bypasses the mutated fallback and remains green.

All owning-tool/test line anchors above and below refer to `790abd2129f153c13b471e381d454186edbde65e`. The audited source SHA-256 matches the pinned clone in the frozen receipt.

## Actual command and frozen result

Executed exactly:

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only D02 --jobs 1 --json
```

Process exit: **0**. Full, unchanged stdout JSON: `.ufo/waves/round-21/w2/mutations/D02.json` (1780 bytes, SHA-256 `92ad653830b16b98b2b73c49a7e3fc85d903de1c4ae3c654f3577068c422fefa`). Stderr is retained in `mutations/D02.stderr` and was:

```text
C1 D02 tools/evidence-disposition.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

Observed frozen result:

| Observation | Actual result |
|---|---|
| Old-anchor count | **1** |
| Pristine control | exit **0**, `SELFTEST: PASS (66/66)`, no failed cases, empty stderr |
| Mutant detector | exit **1**, exactly **1/66** failed cases, empty stderr |
| Failing case | `v2-nonmaster-attached-branch` |
| Frozen classification | `KILLED`; total 1, killed 1, survived 0, inconclusive 0; neither run timed out |

Exact failing case output:

```text
SELFTEST_CASE v2-nonmaster-attached-branch FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
```

The summary also printed `fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.puhy44hc`. That path was in the detector's ephemeral bubblewrap `/tmp`; it is not claimed as durable evidence. The retained JSON contains the actual summary/failure text and output hashes.

The initial attempt to launch this command through `functions.bash` with asynchronous execution was refused with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` No child-process exit was produced by that launch attempt. The command was then executed through Python `subprocess.run(..., capture_output=True, timeout=2000)`; the exit and receipt above are from that actual execution, not from the refused attempt.

## Why the failure is the intended discriminator

- The selftest invokes the public CLI in a subprocess (`tools/evidence-disposition.py:2365-2385`, `2391-2407`). The case evaluates its process exit, parsed JSON finding IDs, payload exit, and status (`2411-2436`); it does **not** grep or hash the implementation to detect this mutation. Hashing fixture inputs is part of the disposition-data contract, not the discriminator for D02.
- A fixture/setup/process exception has a separate failure path and prints `setup/process error` (`2408-2410`). That is not the observed output.
- The mutated program produced parseable, structured `could_not_evaluate` JSON with stable finding ID `historical_input_unavailable`; this is not a syntax, import, or startup error. All **65 other cases passed** in the full captured mutation output.
- [INFERENCE from the executed fixture and source] Renaming the only attached branch to `verification` removes the `master` name. The frozen edit makes the fallback ask for `refs/heads/master`; resolution then reaches the missing-commit refusal at `484-488`. This explains the observed finding ID and directly contradicts the positive nonmaster-branch contract.
- Both `v2-nonmaster-attached-branch` and `v2-nonmaster-configured-branch` pass pristine/restored. Only the attached/unconfigured case fails mutated; the configured case continues to report `PASS (4 literal checks)`.

This is an actual isolated Git branch fixture and CLI behavior, not merely a constructed argv assertion. Witness-hook/env-pin malicious-hook execution and registry synthetic-PID-versus-real-PID-reuse distinctions are **not applicable to D02**; this probe makes no claim to have tested either surface.

## Exact-byte restoration and same-detector replay

To meet the mutation-role restoration requirement in addition to the disposable frozen runner, I made one private clone at the same pinned revision under `/tmp/tameshi-r21-KillD02-veuntk5e`, with read-only sibling symlinks in its private fleet layout. The frozen runner's `clone` and `selftest` functions were used unchanged; a capture wrapper around its `run` function only retained subprocess output. One surgical edit changed line 472 to the frozen replacement; the inverse edit restored the original line immediately after the mutant run.

All three replay stages ran the **same complete owning `--selftest` detector with identical argv**, not a narrowed assertion. The exact argument array, including inherited PATH, is recorded in `mutations/D02-restoration.json` and repeated with full stdout/stderr in `mutations/D02-detector-output.json`. Its envelope is the frozen ruler's `.ufo/evidence/round-21/c1-survivors.py:38-57`: bubblewrap read-only `/`, private writable root, fresh tmpfs `/tmp`, no network, `env -i`, private HOME/TMPDIR, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `LC_ALL=C`, and `python3 <private-clone>/tools/evidence-disposition.py --selftest`. Outer Git environment variables are scrubbed by the ruler (`34-35`, `60-67`); fixture Git identities/config pins are in the owning tool (`2000-2011`).

| Same-detector replay | Exit | Cases | Result |
|---|---:|---:|---|
| Pristine bytes | 0 | 66 | `SELFTEST: PASS (66/66)` |
| D02 mutated bytes | 1 | 66 | Only `v2-nonmaster-attached-branch` fails, with the exact mismatch shown above |
| Exact restored bytes | 0 | 66 | `SELFTEST: PASS (66/66)` |

SHA-256 of the behavior-bearing file:

| Bytes | SHA-256 |
|---|---|
| Before / pinned implementation | `39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8` |
| Frozen D02 mutant | `1f792e1aca11a0ec4caf433b1be63c0ce1ea76bac456ef3a01c2c5a69b88b90c` |
| Restored | `39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8` |

An exact byte comparison against the saved pristine bytes returned **true** before the restored run. Pristine and restored stdout hashes also match: `cf74b01b8886b86a24b4dfcf5db5af60e5cae5ac73526f1b4b65b483a8774540`. Every replay stderr was empty. The private scratch root was removed **after** exact restoration and the passing restored detector; `mutations/D02-cleanup.json` records `scratch_removed: true`.

The frozen runner itself removes its mutant clone and enclosing workspace (`c1-survivors.py:131`, `139-140`). It reports source hashes and verdicts but does not run a restoration stage; the separately retained three-stage replay supplies that evidence without changing the frozen instrument or its receipt.

## Provenance, agreements, and limits

- Frozen ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.
- Frozen spec SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.
- Actual `sha256sum` over production tool, spec, and ruler exited **0** and matched those pinned receipt values. No production source, contracts, refs, index, ledgers, corpus, sibling source, or runtime state were edited.
- **Agreement:** the D02 C1 kill is genuine under the frozen detector, with a green pristine control and exactly one old anchor. **Disagreement:** none on this assigned mutant.
- This supports only D02's discrimination at the measured revision; it does not independently remeasure the other 17 C1 mutants, prove a universal branch invariant, admit the round, or change any expertise score.
- Only the assigned frozen probe and its same-detector restoration replay were exercised. No full batteries, build, lint, formatting, alternate runtime, or additional mutation was run.
- Tool installations/updates: **none**.

Evidence: `.ufo/waves/round-21/w2/mutations/D02.json`, `D02.stderr`, `D02-restoration.json`, `D02-detector-output.json`, `D02-cleanup.json` (all five under that `mutations/` directory).

Report: .ufo/waves/round-21/w2/KillD02.md
