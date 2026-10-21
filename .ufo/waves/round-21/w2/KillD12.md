done — **genuinely discriminated**. Frozen C1 mutant **D12 KILLED**, with pristine green, anchor count **1**, exactly the two intended non-master branch cases failing, and exact-byte restoration followed by a green control.

# KillD12 — round-21 FALSIFY

- Axes: **operability**, **calibration**. This is an author-side advisory mutation receipt, not outside admission, a score change, or a claim about the other 17 mutants.
- Landed source: `790abd2129f153c13b471e381d454186edbde65e` in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- Owning tool: `tools/evidence-disposition.py`.
- Production was read-only. The additional mutation/restoration sequence used only `/tmp/tameshi-r21-KillD12-lcgc3qlt`. Beside its private clone, sibling lanes were symlinks behind the detector's read-only `/` bind. Only this report and D12-named evidence were written in the lane.

## Mutant and expected detector

Frozen contract `.ufo/evidence/round-21/c1-mutants.json:85-88` specifies the single behavior-bearing replacement at `tools/evidence-disposition.py:477`:

```diff
-        branch_ref = "refs/heads/" + branch
+        branch_ref = "refs/heads/master"
```

The landed resolver first reads `lane.branch`, otherwise derives the attached branch from `HEAD` (`tools/evidence-disposition.py:460-474`), then resolves that selected local branch (`:476-490`). D12 ignores the selected name and always resolves master. This is a real contract violation for a non-master attached or explicitly configured branch, not an equivalent mutation.

Expected detector: the owning `--selftest`, under the frozen C1 bubblewrap/environment envelope, should remain green pristine and fail the two positive non-master branch cases under D12. The frozen ruler checks the anchor exactly once and requires pristine exit 0 before crediting a kill (`.ufo/evidence/round-21/c1-survivors.py:106-130`).

## Required frozen command: actual execution

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only D12 --jobs 1 --json
```

- Process exit: **0**.
- Full stdout JSON, saved byte-for-byte: `.ufo/waves/round-21/w2/mutations/D12.json`.
- Receipt: total **1**, killed **1**, survived **0**, inconclusive **0**; `anchor_count=1`.
- Pristine: exit **0**, `SELFTEST: PASS (66/66)`, no failed lines, empty stderr, no timeout.
- Mutant: exit **1**, `SELFTEST: FAIL (2/66 failed: v2-nonmaster-attached-branch, v2-nonmaster-configured-branch; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.osfmdvop)`, empty stderr, no timeout.
- Actual detector stderr:

```text
C1 D12 tools/evidence-disposition.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

Actual failing case output:

```text
SELFTEST_CASE v2-nonmaster-attached-branch FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
SELFTEST_CASE v2-nonmaster-configured-branch FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean')
```

The reported retained fixture path is inside a per-run tmpfs; its appearance in the raw output is not a claim that those fixtures survived sandbox teardown.

An initial **async bash tool dispatch** was refused with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` It did not launch the detector and has no process exit. The identical command was then executed synchronously through Python `subprocess.run(..., capture_output=True, timeout=2000)`, producing the receipt above. This dispatch failure is preserved, not relabeled as a detector pass.

## Why this is the intended discriminator

All tool line references here are to the source at the full landed revision above, materialized with `git show` and again in the private clone.

1. `_setup_hist_clean` commits pinned original tool bytes and then a committed instrument move (`tools/evidence-disposition.py:2076-2082`).
2. `setup_nonmaster_attached` renames the fixture branch to `verification` (`:2702-2704`). The configured case additionally sets `lane.branch=verification` and detaches HEAD (`:2706-2709`). These create actual private Git repositories; the case runner reports fixture exceptions separately as `setup/process error` (`:2391-2410`). Neither failure has that signature.
3. The two positive tests explicitly expect exit **0** and no findings: `v2-nonmaster-attached-branch` at `:2715-2717`, and `v2-nonmaster-configured-branch` at `:2718-2720`.
4. The selftest invokes the public CLI with `--root`, `--dispositions`, and `--json` (`:2365-2385`), then checks process exit, finding IDs, payload exit, and semantic status (`:2411-2425`). Under D12 both cases return valid JSON with exactly `historical_input_unavailable`, exit **2**, and `could_not_evaluate`, instead of clean. This is the erroneous branch-resolution result at `:484-488`, not syntax/import failure, source-hash pin mismatch, grepping, or an unrelated assertion. The other **64/66** cases pass.
5. The frozen ruler records hashes for identity (`c1-survivors.py:55-57,104,122`); the behavioral selftest's four assertions do not compare the implementation's source hash. The failing IDs are not any digest-mismatch ID.

**Agreement:** the frozen ruler's `KILLED` classification is backed by the intended public-CLI branch-selection behavior, and both positive cases revert to PASS with exact original bytes.

**Calibration limit:** these fixtures exercise a renamed non-master branch with master absent. They do not separately demonstrate conflicting, simultaneously present `master` and `verification` tips, arbitrary branch names, or every branch topology. No disagreement with this scoped kill was observed. D12 is neither a witness hook/env-pin mutant nor a registry-identity mutant: no malicious-hook execution or real PID reuse is claimed. Git fixture environment scrubbing and identity/config pins are observable setup (`tools/evidence-disposition.py:2000-2025`), not evidence that a malicious hook was executed.

## Same detector on pristine, mutated, restored bytes

The required frozen script uses disposable private clones and cleans them (`c1-survivors.py:93-100,117-121,131,139-140`). An additional **D12-only** restoration probe retained a unique private scratch clone and ran the same owning behavioral detector on all three byte states. This is not an unrelated battery.

Private setup commands (both exit **0**, empty stdout/stderr), with all inherited `GIT_*` removed and `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` set:

```sh
git -c core.hooksPath=/dev/null clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillD12-lcgc3qlt/fleet/tameshi-shokunin
git -c core.hooksPath=/dev/null -C /tmp/tameshi-r21-KillD12-lcgc3qlt/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

Identical selftest argv in every phase (the exact expanded PATH and argv are retained in `D12-restoration.json`):

```sh
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind /tmp/tameshi-r21-KillD12-lcgc3qlt /tmp/tameshi-r21-KillD12-lcgc3qlt --unshare-net --die-with-parent \
  --chdir /tmp/tameshi-r21-KillD12-lcgc3qlt/fleet/tameshi-shokunin \
  env -i "PATH=$PATH" HOME=/tmp/tameshi-r21-KillD12-lcgc3qlt/home TMPDIR=/tmp/tameshi-r21-KillD12-lcgc3qlt/tmp \
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C \
  python3 /tmp/tameshi-r21-KillD12-lcgc3qlt/fleet/tameshi-shokunin/tools/evidence-disposition.py --selftest
```

Outer process environment: invoking environment minus every `GIT_*`; timeout **900 seconds** per phase, as in the frozen detector. Each phase has a fresh tmpfs `/tmp`. The only source edit was line 477 in this private clone. Exact original bytes were restored in a `finally` block before the restored run, even though the mutant detector exited nonzero.

| Phase | Exit | Actual output | Tool SHA-256 | Raw stdout SHA-256 |
|---|---:|---|---|---|
| pristine | 0 | PASS 66/66 | `39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8` | `cf74b01b8886b86a24b4dfcf5db5af60e5cae5ac73526f1b4b65b483a8774540` |
| mutated | 1 | FAIL 2/66 (64 PASS) | `99a54325a69975b23b80b67c40dac6d2eadee0957ead204d84daefd1935db50c` | `a82c3876ae0fedfc9a7aa843703a4b9230953326e7d2bf651b93b5aa08668f11` |
| restored | 0 | PASS 66/66 | `39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8` | `cf74b01b8886b86a24b4dfcf5db5af60e5cae5ac73526f1b4b65b483a8774540` |

- Every phase had empty stderr: SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Mutated SHA matches the required frozen detector's mutant exactly: **true**.
- Restored bytes equal the original **byte-for-byte: true**; restored hash equals original.
- Pristine and restored raw stdout are identical: **true**.
- Production owning-tool hash before and after: `39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8` / `39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8` (equal). No production source, index, refs, sibling source, routing, state, ledger, or corpus was edited.

## Evidence and source identities

- `.ufo/waves/round-21/w2/mutations/D12.json`: full required detector stdout, including both controls and failure details.
- `.ufo/waves/round-21/w2/mutations/D12-restoration.json`: exact clone/selftest argv, environment pins, actual exits, timeouts, hashes, output paths, and exact-byte restoration result.
- `.ufo/waves/round-21/w2/mutations/D12-pristine.stdout` / `.stderr`: full pristine output.
- `.ufo/waves/round-21/w2/mutations/D12-mutated.stdout` / `.stderr`: full mutated output, preserving both failures and its own randomized fixture path.
- `.ufo/waves/round-21/w2/mutations/D12-restored.stdout` / `.stderr`: full restored output.
- Frozen ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.
- Frozen contract SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.
- Original landed owning-tool SHA-256: `39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8`.
- Mutant owning-tool SHA-256: `99a54325a69975b23b80b67c40dac6d2eadee0957ead204d84daefd1935db50c`.

No installs or updates; existing Python, Git, bubblewrap, and jj were used. No other runtime, subagents, full batteries, builds, linters, or formatters were invoked. Verdict is confined to D12; it does not admit round claims or increase numeric expertise.

Report: `.ufo/waves/round-21/w2/KillD12.md`
