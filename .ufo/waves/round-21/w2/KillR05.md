# done — R05 genuinely discriminated (KILLED)

Author-side advisory measurement only; no admission, integration, or numeric expertise judgment.

## Axes and scope

- **Operability:** execute the frozen R05 detector against landed revision `790abd2129f153c13b471e381d454186edbde65e`; require green pristine control and exactly one mutation anchor.
- **Calibration:** establish that the named failure tests the changed behavior, while distinguishing synthetic process-identity controls from real PID reuse or demonstrated collateral-process survival.

Only R05 was probed. No full battery, build, lint, formatter, other mutant, or F5 reproduction was run. No tools were installed or updated.

## Mutant and exact source anchors

All implementation line references below are to `tools/registry-check.py` at `790abd2129f153c13b471e381d454186edbde65e`. The private clone's complete original file was compared byte-for-byte with `git show 790abd2129f153c13b471e381d454186edbde65e:tools/registry-check.py` before the additional restoration probe.

- Frozen contract: `.ufo/evidence/round-21/c1-mutants.json:98–101`; R05 changes exactly:

  ```python
              return (current, observed_starttime) not in baseline_children
  ```

  to:

  ```python
              return True
  ```

- Changed behavior: `_row_identity_is_owned`, lines **468–489**, specifically **486–487**. A process whose parent is the checker is accepted even when its `(pid, starttime)` was in the pre-row child baseline.
- Baseline construction and intent: `_direct_child_identities`, **456–465**. The mutation removes the exclusion of pre-existing checker children rather than changing parsing or setup.
- Owning discriminator: **1592–1607**, case **`baseline-child-preserved`**. `_read_proc_stat` is patched to return `(os.getpid(), 1234, "S")`. The test calls the production classifier twice for fake PID `987654`: once with baseline `{(987654, 1234)}`, which must be rejected, and once with the empty baseline, which must be owned. Its assertion is `baseline_rejected and adopted_owned` at **1605**.
- Case-result recording: **919–926**. A named failed case reaches the overall exit-1 path at **1809–1812**; all-pass reaches exit 0 at **1813–1814**.

The frozen instrument SHA-256 is `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`; contract SHA-256 is `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c` (recorded in the requested receipt).

## Required frozen command and actual outputs

Executed exactly:

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only R05 --jobs 1 --json
```

Outer command **exit 0**, elapsed **17.650 s**. Full, unmodified JSON stdout is saved at `.ufo/waves/round-21/w2/mutations/R05.json`; command/exit metadata is `mutations/R05-command.json`; complete outer stderr is `mutations/R05.stderr`:

```text
C1 R05 tools/registry-check.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

| Frozen measurement | Exit | Actual summary | Timeout |
|---|---:|---|---|
| Pristine control | 0 | `SELFTEST: PASS (51 cases)` | false |
| R05 mutant | 1 | `SELFTEST: FAIL (1 of 51 cases: baseline-child-preserved)` | false |

**Anchor count: 1.** Totals: killed 1, survived 0, inconclusive 0. The exact mutant failure is:

```text
SELFTEST_CASE baseline-child-preserved FAIL (baseline_rejected=False adopted_owned=True)
SELFTEST: FAIL (1 of 51 cases: baseline-child-preserved)
```

Both owning-selftest stderr streams were empty (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). The frozen ruler records stdout digests rather than retaining full selftest stdout; the separate triplet below retains the complete streams as well.

## Same detector on pristine, mutated, restored bytes

A separate private clone at the pinned revision was created under `/tmp/tameshi-r21-KillR05-gwx38fb8/fleet/tameshi-shokunin`, with read-only sibling symlinks under the same sandbox arrangement. Clone setup used `git clone -q --no-hardlinks` and `git checkout -q --detach` at the pinned revision; both succeeded. The exact frozen `c1-survivors.py:selftest` function (**38–57**, 900-second bound) was reused without changing its detector. A wrapper retained subprocess stdout/stderr and the constructed argv; it did not change assertions or outcomes.

For each stage, the actual command was the following argv (shown shell-rendered; the full expanded PATH and argv are retained separately for all three stages in `mutations/R05-restoration.json`):

```sh
W=/tmp/tameshi-r21-KillR05-gwx38fb8
D=$W/fleet/tameshi-shokunin
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind "$W" "$W" --unshare-net --die-with-parent --chdir "$D" env -i "PATH=$PATH" "HOME=$W/home" "TMPDIR=$W/tmp" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C python3 "$D/tools/registry-check.py" --selftest
```

The outer subprocess environment had **no `GIT_*` keys** in each recorded invocation; the inner `env -i` explicitly constructed the pins above. These are observed argv/environment-construction facts, **not evidence that a malicious Git hook was installed or executed**. Hook attacks are not the R05 discriminator.

| Stage | Exit | Seconds | `baseline-child-preserved` output | Overall |
|---|---:|---:|---|---|
| Pristine | 0 | 9.211 | `PASS (baseline_rejected=True adopted_owned=True)` | 51 cases PASS |
| Mutated | 1 | 9.262 | `FAIL (baseline_rejected=False adopted_owned=True)` | Only that case failed |
| Restored | 0 | 9.058 | `PASS (baseline_rejected=True adopted_owned=True)` | 51 cases PASS |

All three runs completed without timeout and with empty stderr. Full streams are `mutations/R05-{pristine,mutated,restored}.stdout` and corresponding `.stderr` files. The named case is at line **35**, the overall summary at line **52**, in each saved stdout.

### Hashes and restoration

| Bytes | SHA-256 |
|---|---|
| Pinned original / pristine | `cc4ed8e215f01a7ef3693f2f98b2973ad401047b473efb1e7b1fbea92a5d451e` |
| Exact single-point R05 mutant | `b7ffc9eaea517f2c108b343b374b6f4890e2b34eb7bcf0aeee3e7f1994701287` |
| Restored original | `cc4ed8e215f01a7ef3693f2f98b2973ad401047b473efb1e7b1fbea92a5d451e` |

Before the mutant run, the complete scratch file was checked against the frozen single replacement. Restoration was in a `finally` block, using the saved complete original UTF-8 bytes. Exact restored-byte equality was **true** before the restored detector ran. The private scratch was subsequently removed; `scratch_removed: true` is recorded in `mutations/R05-restoration.json`.

Isolation caveat, preserved rather than hidden: importing the frozen ruler for this extra triplet emitted `__pycache__/c1-survivors.cpython-314.pyc` under its live evidence directory. That generated cache had birth/mtime `2026-10-21 09:30:36 -0300`, after this seat's command receipt at `09:30:26 -0300`. The directory contained only that cache. The generated file and then the empty cache directory were removed using `rm -- <exact-cache-path> && rmdir -- <exact-cache-directory>`; the cleanup command completed successfully without output. This transient cache write was outside the intended read-only envelope. No live tool source, contract, ledger, corpus, Git index/ref, or sibling source was edited. The required frozen-command receipt was produced before the import side effect.

## Discrimination and limits

**Verdict: genuinely discriminated; killed, not incidental/equivalent/inconclusive.** The green controls, single exact anchor, mutant-only named failure, and green restored run show that the changed baseline-membership behavior is what the detector observes. The assertion directly calls the production ownership function; it does not grep its source or compare its source hash. Hashes and anchor counting belong to measurement provenance, not the case's behavioral oracle. Execution reached all 51 case records, with no syntax/import/setup failure or unrelated failing assertion.

This is a **synthetic ownership-classification control**, not real PID reuse. The case supplies fake PID/starttime data and does not signal a host process. It does not itself demonstrate that a real pre-existing sibling survives a complete cleanup cycle. The neighboring `pidfd-revalidates-starttime` case at **1567–1589** simulates a starttime change with controlled reads, rather than forcing real PID recycling; it passed in pristine, mutated, and restored output (line 34). Likewise `pidfd-revalidates-ownership` passed in all three (line 36). Neither neighboring case caused this kill.

**Agreement:** the frozen C1 instrument's R05 `KILLED` classification is supported by the intended behavioral discriminator. **Disagreement with any broader reading:** these receipts cannot support claims of exercised real PID reuse, malicious-hook execution, or admission of the overall round. No such broader execution or conclusion is claimed here.

Report: .ufo/waves/round-21/w2/KillR05.md
