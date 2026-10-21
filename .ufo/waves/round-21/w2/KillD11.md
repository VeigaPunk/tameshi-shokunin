# done — D11 genuinely discriminated

**Operational verdict:** KILLED. **Discriminator classification:** genuinely discriminated, not incidental, equivalent, or inconclusive.

Axes: **operability** (the frozen bounded detector runs and detects the specified regression) and **calibration** (the observed failure is attributed narrowly to rejecting executable historical blobs). This is an author-side advisory mutation probe, not round admission or a claim of numerical expertise improvement.

## Mutation and pinned source

Target revision: `790abd2129f153c13b471e381d454186edbde65e` in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

The frozen D11 contract is `.ufo/evidence/round-21/c1-mutants.json:79-82`; its owning detector argv is at lines 126-128. It changes exactly one behavior-bearing line, `tools/evidence-disposition.py:549`:

```diff
-TREE_MODES = ("100644", "100755")
+TREE_MODES = ("100644",)
```

The frozen instrument observed **anchor_count = 1**. The additional isolated replay also counted exactly one old anchor. Source citations below are to the target revision; the private clone's complete source SHA-256 matched the frozen receipt's pristine tool hash.

The defect rejects a valid executable regular Git blob (`100755`) while leaving non-executable regular blobs (`100644`) accepted. The owning tool's G5 contract explicitly permits both at `tools/evidence-disposition.py:58`. The actual check is `historical_blob`, lines 636-650, particularly the mode-membership guard at lines 644-648.

## Required frozen command: actual output

Executed with inherited `GIT_*` variables removed from the invoking environment:

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only D11 --jobs 1 --json
```

**Exit: 0.** Full, unmodified JSON stdout is saved as `.ufo/waves/round-21/w2/mutations/D11.json` (1783 bytes, SHA-256 `2b8a89d267d448cc3e99f9afe5f36079ddd9c30e6c9ba43fdc5c86ca480d1baa`). Stderr is saved as `mutations/D11.stderr.txt`; the exit is saved as `mutations/D11.exit.txt`, relative to the same wave directory.

Actual stderr:

```text
C1 D11 tools/evidence-disposition.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

Frozen receipt observations:

| Run | Exit | Timeout | Actual summary |
|---|---:|---|---|
| Pristine control | 0 | false | `SELFTEST: PASS (66/66)` |
| D11 mutant | 1 | false | `SELFTEST: FAIL (1/66 failed: v2-historical-executable-mode; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.s3lgfc7w)` |

Both runs had empty stderr. The sole failing case was:

```text
SELFTEST_CASE v2-historical-executable-mode FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
```

Thus the detector process exits 1 because its real child CLI returns 2 for a case that must return 0. These are different exit levels, not a contradiction.

Instrument provenance, as observed in the saved receipt:

- Ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.
- Frozen-spec SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.
- Pristine control stdout SHA-256: `cf74b01b8886b86a24b4dfcf5db5af60e5cae5ac73526f1b4b65b483a8774540`.
- Mutant stdout SHA-256: `16c3a54a2ec16bb21f936fec8ad85a5d110a2db29981dae1d6e740dba8c9712a`.

## Why this is the intended discriminator

At the pinned revision:

1. `tools/evidence-disposition.py:2711-2713` defines `setup_executable_historical`, which applies `chmod(0o755)` to the fixture's pinned tool before calling `_setup_hist_clean`.
2. `_setup_hist_clean`, lines 2076-2082, commits the initial pinned tool bytes at historical revision A, then commits different live bytes. The Git helper calls are genuine fixture Git commands, not a model of Git; their environment/identity pins are at lines 2000-2033 and 2056-2073.
3. Lines 2721-2723 register **`v2-historical-executable-mode` with expected exit 0 and no finding IDs**. `historical_case`, lines 2438-2452, constructs the v2 historical-input manifest for that fixture.
4. `run_cli`, lines 2365-2385, launches the actual same Python CLI with `--root`, `--dispositions`, and `--json`, under a 120-second child timeout.
5. The four assertions at lines 2411-2425 check child exit, parsed finding IDs, JSON payload exit, and JSON status. They expect `0`, `[]`, `0`, and `clean`. The mutant produces `2`, `['historical_input_unavailable']`, `2`, and `could_not_evaluate`, exactly the refusal introduced by removing `100755` from the allowed modes.
6. Fixture/import/process exceptions are separately reported as `setup/process error` at lines 2408-2410. That is not the observed failure. No syntax/import failure, malformed JSON, unrelated assertion, or timeout appears; the other 65 cases pass.

The selftest's phrase **“4 literal checks” refers to behavioral values from the executed CLI**, not grepping source literals. Source-anchor counting is only the mutation-application prerequisite (`c1-survivors.py:108-116`). Output/source hashes are receipt evidence; they are not the failing case's oracle. The runner's behavioral kill classification is at lines 123-130.

## Same detector on pristine, mutated, and restored bytes

Because the frozen ruler deletes its private clones (`c1-survivors.py:131,139-140`) and does not run a restored control, I additionally replayed **only D11** in `/tmp/tameshi-r21-KillD11-_p3jfex0`. Full raw stdout/stderr, actual argv, setup commands/exits, hashes, and restoration comparison are saved in `.ufo/waves/round-21/w2/mutations/D11-restoration.json`.

Actual setup commands, both exit 0 with empty stdout/stderr:

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillD11-_p3jfex0/fleet/tameshi-shokunin
git -C /tmp/tameshi-r21-KillD11-_p3jfex0/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

The same detector argv/envelope was used in all three phases, matching `c1-survivors.py:38-57`: `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind R R --unshare-net --die-with-parent --chdir R/fleet/tameshi-shokunin env -i PATH=<inherited literal PATH> HOME=R/home TMPDIR=R/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C python3 R/fleet/tameshi-shokunin/tools/evidence-disposition.py --selftest`, where `R=/tmp/tameshi-r21-KillD11-_p3jfex0`. The exact expanded argv, including the inherited PATH, is in the restoration receipt. The top-level command environment again omitted inherited `GIT_*`; the detector deadline was 900 seconds per phase. Sibling fleet entries were symlinks alongside the private clone, read-only under the bubblewrap root mount.

| Phase | Exit | Actual executable-mode case | Actual overall summary |
|---|---:|---|---|
| Pristine | 0 | `PASS (4 literal checks)` | `SELFTEST: PASS (66/66)` |
| Mutated | 1 | Same exact failure quoted above | `SELFTEST: FAIL (1/66 failed: v2-historical-executable-mode; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.qq4l3uml)` |
| Restored | 0 | `PASS (4 literal checks)` | `SELFTEST: PASS (66/66)` |

All three stderr streams were empty; no phase timed out. The mutated source hash exactly matched the frozen run's mutated hash. The two mutant stdout hashes differ because their failure summaries include different random fixture directory names; this did not change the failure case or assertions. Failed observations are preserved verbatim in both receipts. The printed fixture directories were inside the per-run `/tmp` tmpfs, so their path strings are observations, not a claim that those fixtures persist on the host.

### Exact-byte restoration evidence

| State | SHA-256 of `tools/evidence-disposition.py` |
|---|---|
| Before mutation | `39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8` |
| Mutated | `680234fa2773e900054074951c8dadc1ff152dab482abe78e0c81c12430e5fdb` |
| Restored | `39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8` |

Restoration ran in a `finally` block and compared the restored bytes directly against the saved pristine bytes: **equal**. The restored selftest then passed. Pristine/restored stdout also matched exactly, both SHA-256 `cf74b01b8886b86a24b4dfcf5db5af60e5cae5ac73526f1b4b65b483a8774540`. The production owning source hash remained the same before and after; no production source, contract, ledger, Git index/ref, sibling, or routing file was edited.

## Agreements, limits, and handoff

- **Agree:** this landed implementation genuinely kills the frozen D11 regression; pristine green plus the one intended failing case supports the frozen `KILLED` result.
- **No disagreement found** for this assigned mutant. This is not evidence that all 18 mutants are genuine, that arbitrary executable-mode defects are detected, or that all environment attacks are covered.
- Witness hook/environment-pin and registry PID-identity mutation claims are **not applicable to D11**. This probe claims neither malicious-hook execution nor real PID reuse. The sandbox/env pins described above are the observed constructed execution envelope, not a separate malicious-hook test.
- Only the assigned owning selftest was run, through the frozen command and the required pristine/mutant/restored replay. No full registry battery, build, lint, formatter, alternate runtime, integration, or admission action was performed.
- Tool installs/updates: **none**. Production code/tests/docs intentionally unchanged; this assignment is an investigation. All durable findings are the item-named report and evidence files above.

Report: `.ufo/waves/round-21/w2/KillD11.md`
