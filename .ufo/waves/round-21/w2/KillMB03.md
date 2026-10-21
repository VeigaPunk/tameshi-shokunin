done — MB03 genuinely discriminated; frozen detector verdict KILLED.

# MB03 mutation probe

- Seat: `TameshiR21.KillMB03`; author-side advisory, not outside admission or an integration decision.
- Axes: **operability** (the frozen MB03 detector runs and discriminates) and **calibration** (identify the actual failing case and limit the demonstrated claim).
- Target revision: `790abd2129f153c13b471e381d454186edbde65e`.
- Scope: MB03 only, owning `tools/bash-witness-study.py`; no production tools, contracts, corpus, refs, index, or sibling sources edited. No tools installed or updated.

## Mutant and expected detector

Frozen contract: `.ufo/evidence/round-21/c1-mutants.json:12-17`. One occurrence of the old anchor was observed (`anchor_count: 1`). The change at target-revision `tools/bash-witness-study.py:336` is:

```diff
-           if not name.startswith("GIT_")}
+           if name not in ("GIT_DIR", "GIT_WORK_TREE")}
```

The mutation keeps inherited Git variables other than `GIT_DIR` and `GIT_WORK_TREE`; the subsequent configuration assignments at lines 337-338 still override `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_NOSYSTEM`. The intended discriminator is **`scrubs inherited repository selectors`**, defined at target-revision `tools/bash-witness-study.py:1291-1293`. Its setup at lines 1283-1290 patches the live process environment with hostile `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, and Git-configuration values, calls the real `git_clean_env()`, and asserts that the first two keys are absent from the returned dictionary.

This is an executed environment-construction contract test, not a source-text grep, source-hash assertion, syntax/import failure, or incidental assertion. The ruler's string count gates mutation placement; its hashes identify bytes, not the test verdict. `materialize_target()` passes this helper's environment to Git at lines 347-350; `sweep_env()` calls it at lines 582-586, and `run_sweep()` passes that result at lines 614-616.

## Actual commands and outputs

Exact requested command, successfully executed with exit **0**:

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only MB03 --jobs 1 --json
```

Full JSON: `.ufo/waves/round-21/w2/mutations/MB03.json`.
Exit receipt: `.ufo/waves/round-21/w2/mutations/MB03.exit`.
Outer stderr, also preserved in `.ufo/waves/round-21/w2/mutations/MB03.stderr.txt`:

```text
C1 MB03 tools/bash-witness-study.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

The pristine control exited **0**, `VERDICT: PASS`, no timeout (0.078 seconds). The mutant exited **1**, `VERDICT: FAIL`, no timeout (0.078 seconds). Receipt totals: killed **1**, survived **0**, inconclusive **0**, total **1**.

Preserved unsuccessful launch observation: the initial asynchronous submission of this same command returned `Background job limit reached (100). Wait for running jobs to finish or cancel one.` No detector process/exit was obtained from that submission. The synchronous submission above succeeded; the launch refusal is not a baseline failure or a mutant kill.

## Pristine → mutated → restored replay

To satisfy exact-byte restoration and inspect complete case output, I additionally ran the **same frozen `selftest(w, d, tool, args)` function** from `.ufo/evidence/round-21/c1-survivors.py:38-57` on three states of one isolated clone. Only stdout/stderr capture around the real subprocess runner was added; no detector logic or assertions were replaced.

Private scratch: `/tmp/tameshi-r21-KillMB03-928wlv9p`. Preparation commands, each exit **0**, were:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 790abd2129f153c13b471e381d454186edbde65e:tools/bash-witness-study.py
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillMB03-928wlv9p/fleet/tameshi-shokunin
git -C /tmp/tameshi-r21-KillMB03-928wlv9p/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

Clone operations removed inherited `GIT_*` and set `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`. Sibling fleet entries were symlinked beside the private clone and remained read-only in the detector's root read-only mount. Each detector call used the ruler's unchanged bwrap/`env -i` argv, including private HOME/TMPDIR, inherited PATH, pinned Git configuration, `LC_ALL=C`, no network, and the same **900-second timeout**. The exact argv and complete raw stdout/stderr for every phase are retained in `.ufo/waves/round-21/w2/mutations/MB03.replay.json`.

| Phase | Exit | Actual terminal output | Seconds | Child stderr |
|---|---:|---|---:|---|
| Pristine | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | 0.071 | empty |
| MB03 | 1 | `WITNESS_SELFTEST: 50/51 pass`; `VERDICT: FAIL` | 0.072 | empty |
| Restored exact bytes | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | 0.076 | empty |

Complete case outputs: `.ufo/waves/round-21/w2/mutations/MB03.pristine.stdout.txt`, `MB03.mutated.stdout.txt`, and `MB03.restored.stdout.txt` in the same directory. The **only failing case** in the mutant is:

```text
  check scrubs inherited repository selectors        FAIL
```

It appears at `MB03.mutated.stdout.txt:2`; all other 50 checks pass, the full denominator remains 51, and cleanup completes. The two configuration-pin checks, all three hook-argv checks, and both GIT_DIR/GIT_WORK_TREE canary checks remain green (`MB03.mutated.stdout.txt:3-9`). Thus the failure is neither test setup nor an unrelated assertion.

## Hashes and restoration evidence

SHA-256 of the behavior-bearing tool:

| State | SHA-256 |
|---|---|
| Pinned/pristine | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| MB03 | `03e6056b6393064e88747647dcb6178a4909ad56a371a217ee238d5663adb028` |
| Restored | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |

The restored bytes equal both the saved original bytes and the pinned Git blob, not merely equivalent source. The production file hash was the pinned/pristine hash before and after the probe. Pristine and restored stdout are byte-identical; both have SHA-256 `1755081d09ccdb98f4dbb2627883cc9b2ab0f58c833663ca293acb7873ddbdf1`. Mutant stdout SHA-256 is `3b72361f492c58f76248cd6199da95cacfd6dde3cd7ece165b02133aadaaed0f`, matching the exact-command receipt. All child stderr hashes are the empty-byte SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Instrument identities from the exact-command receipt and replay:

- Ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.
- Frozen spec SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.

The disposable replay scratch was removed only after restoring the file and obtaining the restored green control. `.ufo/waves/round-21/w2/mutations/MB03.cleanup.json` records `tool_restored_before_disposal: true`, `restored_control_exit: 0`, and `scratch_exists_after_cleanup: false`. The frozen ruler separately removes its own mutant clone and scratch at lines 131 and 139-140.

## Agreements, disagreements, and limits

- **Agree: genuinely discriminated / KILLED.** The mutant is non-equivalent under the declared environment contract: its helper returns inherited repository selectors that pristine removes. The named discriminator observes exactly that behavior and alone turns red, with pristine/restored controls green.
- **Limit: constructed environment, not malicious execution.** For MB03 the hostile `GIT_INDEX_FILE`/`GIT_OBJECT_DIRECTORY` values are checked in the returned environment dictionary; this test does not launch Git under those hostile values or demonstrate foreign-index/object-store effects. The hook tests at target-revision lines 1298-1311 observe actual fixture command argv containing `-c core.hooksPath=/dev/null`; they do not plant or execute a malicious hook. Their green status is not evidence of an exercised hook exploit. The source explicitly calls these command-pin contracts.
- **Marker-extraction caveat, not a second failed case.** The ruler's `fail_lines` collector at `.ufo/evidence/round-21/c1-survivors.py:53` matches the substring ` FAIL`. It therefore includes the passing case `check FAIL without denominator is inconclusive, not a crash ok` in both control and mutant receipts. This case is **green**, as full stdout line 30 shows; it must not be counted as a failure. The genuine red case is line 2 and the final summary correctly reports 50/51.
- No registry identity test, synthetic PID-race control, or real PID reuse was exercised; no claim about those surfaces follows from MB03.
- No claim about the other 17 C1 mutants, F5 profiles, expertise scores, or round admission is made. Only the assigned owning selftest and its MB03 restoration replay were run; no full battery/build/lint/formatter was run.

Report: `.ufo/waves/round-21/w2/KillMB03.md`
