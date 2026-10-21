done — **genuinely discriminated**. Frozen C1 mutant **R02** is **KILLED**, with a green pristine control, exactly one mutation anchor, and a green exact-byte-restored control. Only the intended `timeout-zero` case fails. This is dispatched author-side advisory evidence, not outside admission or an integration decision.

# Scope and axes

- Axes: **operability** (the frozen detector actually runs and distinguishes R02) and **calibration** (attribute the failure to the intended behavioral check without widening the claim).
- Repository: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- Measured revision: `790abd2129f153c13b471e381d454186edbde65e`.
- Owning tool: `tools/registry-check.py`; only frozen mutant R02 was challenged. No full 18-mutant battery, F5 reproduction, build, lint, or formatter was run.

# Mutant and expected detector

Frozen definition: `.ufo/evidence/round-21/c1-mutants.json:90-95`, receipt spec SHA-256 `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.

At measured revision, `tools/registry-check.py:245` changes only:

```diff
-                    math.isfinite(ts) and 0 < ts <= MAX_TIMEOUT_S
+                    math.isfinite(ts) and 0 <= ts <= MAX_TIMEOUT_S
```

This admits zero as a registry timeout instead of requiring a strictly positive timeout. Both the frozen detector and the additional private restoration replay found **anchor_count = 1**.

The owning new case is `timeout-zero`, `tools/registry-check.py:1501`, within the fixture loop at `1500-1526`. A read-only provenance command:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin blame -L 1500,1526 790abd2129f153c13b471e381d454186edbde65e -- tools/registry-check.py
```

completed successfully (exit 0) and attributes the `timeout-zero` tuple to `370f2df`; the surrounding fixture and assertion are attributed to `58e5d53`.

## Why this is the intended discriminator

All owning-tool line references below are at `790abd2129f153c13b471e381d454186edbde65e`; the inspected live tool had the same SHA-256 as the pinned pristine clone.

1. `registry_errors`, lines `238-256`, owns the finite, strictly-positive, capped numeric timeout rule and its row-specific `timeout_s` diagnostic.
2. The fixture helper at `950-960` creates an otherwise valid row. The case at `1501` selects the numeric JSON token `0`; lines `1511-1519` write it into a temporary registry.
3. Line `1520` exercises the **public CLI**, through `run_child` at `928-938` (`[sys.executable, SELF] + args`), not a helper-only model.
4. Lines `1523-1524` require **exit 2** and diagnostic substrings `timeout-zero`, `timeout_s`, and `finite positive number`. `check_lines` at `969-972` checks the child's output, not source text. This is not a source-hash or source-grep kill.
5. `load_registry` at `347-372` calls the actual validation; `evaluate` at `832-846` returns 2 on that validation error, before the row-execution path at `869`. The observed mutant subcase exits **1**, not the required validation exit 2.

Both mutation executions finish the entire 51-case owning selftest with exactly `timeout-zero` failing; the other 50 cases pass. The selftest's stderr is empty. Pristine and restored bytes pass all 51 cases. These observations exclude a whole-file syntax/import failure, failed suite setup, and an unrelated failing case as the kill mechanism. I did not separately capture the nested `timeout-zero` child's stdout/stderr or assert that its `print('should-not-run')` body printed; the decisive observation is loss of the expected validation rejection.

# Actual frozen command and output

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only R02 --jobs 1 --json
```

Executed with inherited `GIT_*` variables removed. **Exit 0**, elapsed **18.290 s**. Complete, unnormalized stdout is saved as `.ufo/waves/round-21/w2/mutations/R02.json`; stderr as `mutations/R02.stderr`; argv, exit, duration and stream hashes as `mutations/R02.command.json`.

Actual stderr:

```text
C1 R02 tools/registry-check.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

The receipt records:

| Stage | Exit | Timeout | Duration | Result |
|---|---:|---|---:|---|
| Frozen pristine control | 0 | false | 8.666 s | `SELFTEST: PASS (51 cases)` |
| Frozen R02 mutant | 1 | false | 8.956 s | `SELFTEST: FAIL (1 of 51 cases: timeout-zero)` |

Exact mutant failure lines:

```text
SELFTEST_CASE timeout-zero FAIL (exit=1)
SELFTEST: FAIL (1 of 51 cases: timeout-zero)
```

Frozen ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.

Preserved failed launch observation: the initial `functions.bash` asynchronous request was rejected before execution with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` It produced no process exit or measurement. The same requested command was then executed synchronously through Python `subprocess.run`, producing the receipt above; the rejected launch is not counted as a failed control or a kill.

# Exact-byte restoration replay

The frozen ruler removes its private mutant clone (`c1-survivors.py:117-140`). To supply an explicit restored-bytes control, I also performed the **same R02 mutation** in my unique private scratch, not in the lane or another seat's source:

```text
/tmp/tameshi-r21-KillR02-cdk2vxz0
```

Both private setup commands exited 0, with empty stdout/stderr:

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillR02-cdk2vxz0/fleet/tameshi-shokunin
git -C /tmp/tameshi-r21-KillR02-cdk2vxz0/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

Clone setup scrubbed inherited `GIT_*` and pinned `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`. Sibling symlinks were placed beside the clone and remained read-only under the detector sandbox. The same bounded owning-tool detector argv, matching `c1-survivors.py:38-45`, was used on pristine, mutated and restored bytes:

```sh
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind /tmp/tameshi-r21-KillR02-cdk2vxz0 /tmp/tameshi-r21-KillR02-cdk2vxz0 \
  --unshare-net --die-with-parent \
  --chdir /tmp/tameshi-r21-KillR02-cdk2vxz0/fleet/tameshi-shokunin \
  env -i PATH="$PATH" \
  HOME=/tmp/tameshi-r21-KillR02-cdk2vxz0/home \
  TMPDIR=/tmp/tameshi-r21-KillR02-cdk2vxz0/tmp \
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C \
  python3 /tmp/tameshi-r21-KillR02-cdk2vxz0/fleet/tameshi-shokunin/tools/registry-check.py --selftest
```

The actual expanded PATH and complete argv are retained in `mutations/R02.restoration.json`. The tool's line 245 was changed and restored using surgical `edit` calls; the intermediate bytes matched exactly the frozen old/new replacement and the frozen receipt's mutated digest.

| Private stage | Exit | Duration | Output |
|---|---:|---:|---|
| pristine | 0 | 9.029 s | `SELFTEST_CASE timeout-zero PASS (exit=2)`; `SELFTEST: PASS (51 cases)` |
| mutated | 1 | 9.021 s | `SELFTEST_CASE timeout-zero FAIL (exit=1)`; `SELFTEST: FAIL (1 of 51 cases: timeout-zero)` |
| restored | 0 | 9.032 s | `SELFTEST: PASS (51 cases)` |

All three private runs have empty stderr and no timeout. Full raw streams are retained in `mutations/R02.{pristine,mutated,restored}.{stdout,stderr}`; per-stage hashes, exact-byte equality results and setup receipts are in `mutations/R02.restoration.json`. Raw stdout hashes differ between runs, which include measured elapsed times; equality of stdout bytes is not the behavioral oracle for this C1 detector.

## Before/after SHA-256 evidence

| Bytes | SHA-256 |
|---|---|
| Pinned pristine tool / private pre-mutation tool | `cc4ed8e215f01a7ef3693f2f98b2973ad401047b473efb1e7b1fbea92a5d451e` |
| Frozen mutant / private mutated tool | `11536e4313f9c70a43bce445e3590d6bcef8d66b425d225e1164bb35d9e37f5d` |
| Exact-byte-restored private tool | `cc4ed8e215f01a7ef3693f2f98b2973ad401047b473efb1e7b1fbea92a5d451e` |
| Live owning tool before and after the probe | `cc4ed8e215f01a7ef3693f2f98b2973ad401047b473efb1e7b1fbea92a5d451e` |

The restored file was byte-for-byte equal to the saved pristine bytes, not merely semantically equivalent. The live owning tool was also byte-for-byte unchanged. My private scratch was removed **after** restoration and the restored detector run; `scratch_removed=true` is recorded. No production tool, contract, ledger, corpus, index, ref, or sibling source was edited.

# Agreements, limits, and disposition

- **Agree** with the frozen ruler's `KILLED` verdict for R02: this is genuinely behavioral discrimination of zero-timeout acceptance, not an incidental failure or equivalent edit.
- **No disagreement** found for this assigned mutant. This one-mutant result does not independently establish the full `18/18` population result or any expertise-score change.
- R02 is not a witness-hook/environment-pin or PID-identity mutation. This probe makes **no malicious-hook execution claim** and **no real PID-reuse claim**. Passing identity cases elsewhere in the owning selftest are not promoted to such claims.
- No installs or tool updates were performed. No production change is proposed. All assigned checks are complete; only this scoped mutation probe was performed.

Report: `.ufo/waves/round-21/w2/KillR02.md`
