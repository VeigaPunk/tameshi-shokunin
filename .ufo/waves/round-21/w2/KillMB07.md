Verdict: done — **genuinely discriminated** for the constructed child-environment contract; frozen result **KILLED**.

# MB07: removal of the system-Git-configuration pin

- Axes: **operability** (the bounded detector runs and rejects the assigned defect) and **calibration** (environment-contract evidence is not malicious-hook-execution evidence).
- Scope: one frozen mutant, `MB07`, against `790abd2129f153c13b471e381d454186edbde65e`. This is author-side advisory falsification evidence, not outside admission or a round judgment. No production source, contracts, ledger, corpus, index, refs, or sibling source were edited.
- Mutant: delete the single line `    env["GIT_CONFIG_NOSYSTEM"] = "1"\n` from `git_clean_env()`. Frozen old/new: `.ufo/evidence/round-21/c1-mutants.json:36-41`; owning source: `tools/bash-witness-study.py:333-339` (deleted line **338**). Source-line references below are at the pinned revision.

## Exact frozen command and observed output

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only MB07 --jobs 1 --json
```

Executed with inherited `GIT_*` entries removed. Exit **0**; elapsed **0.727 s**. Full stdout JSON is retained verbatim at `.ufo/waves/round-21/w2/mutations/MB07.json`; full stderr is retained at `.ufo/waves/round-21/w2/mutations/MB07.stderr.txt`:

```text
C1 MB07 tools/bash-witness-study.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

Receipt facts:

| Observation | Actual |
|---|---|
| Anchor count | **1** |
| Pristine control | exit **0**, `VERDICT: PASS`, no timeout |
| Mutant | exit **1**, `VERDICT: FAIL`, no timeout |
| Population measured | **1**, killed **1**, survived **0**, inconclusive **0** |
| Ruler SHA-256 | `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396` |
| Frozen spec SHA-256 | `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c` |

The ruler checks the unique anchor and green control before mutation (`c1-survivors.py:106-123`) and decides KILLED from the nonzero mutant exit (`:125-130`). Its tool-specific invocation is the **`selftest` subcommand**, not `--selftest` (`c1-mutants.json:122-125`). Its read-only-root bwrap envelope, writable private scratch, network isolation, empty child environment and Git pins are at `c1-survivors.py:38-48`.

## Expected discriminator versus actual failing case

Expected: **`disables system Git configuration`**, `tools/bash-witness-study.py:1296-1297`.

The test patches inherited `GIT_CONFIG_NOSYSTEM` to `"0"`, together with other hostile Git values (`:1282-1288`), then calls the actual `git_clean_env()` (`:1289-1290`) and checks its returned dictionary. Pristine strips inherited `GIT_*` and re-adds `GIT_CONFIG_NOSYSTEM="1"` (`:335-338`). MB07 still strips the inherited value but no longer re-adds the pin, so `.get("GIT_CONFIG_NOSYSTEM") == "1"` is false. This exercises runtime function output, not source grepping or a source digest.

A supplemental same-envelope pristine → mutant → restored replay retained the complete selftest stdout/stderr and exact argv in `.ufo/waves/round-21/w2/mutations/MB07.replay.json`. It used the unmodified frozen ruler's `selftest()` function with an output-capturing wrapper around its subprocess runner. Only the frozen MB07 line deletion was applied in the private clone.

| Bytes under test | Exit | Actual terminal output | Actual failing case names |
|---|---:|---|---|
| Pristine | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | none |
| MB07 | 1 | `WITNESS_SELFTEST: 50/51 pass`; `VERDICT: FAIL` | **`disables system Git configuration`** only |
| Exact restored bytes | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | none |

The actual mutant line was:

```text
  check disables system Git configuration            FAIL
```

All three stderr streams were empty. All 51 checks completed; the normal selftest tally/exit path is `tools/bash-witness-study.py:1711-1716`. Thus the failure was not syntax, import, setup, timeout, an unrelated assertion, or the tool's separate evidence-hashing fixtures. Full raw streams are retained as `mutations/MB07.{pristine,mutated,restored}.{stdout,stderr}.txt` under this wave directory.

**Receipt interpretation caution:** the frozen ruler's `fail_lines` selection (`c1-survivors.py:53`) also captures the *passing* case named `FAIL without denominator is inconclusive, not a crash`, because its name contains ` FAIL`. The pristine receipt includes that line ending in `ok`; it is not a failed control. The mutant's `VERDICT: FAIL` is a terminal summary, not a second failed case. Complete stdout shows exactly one failed check.

## Calibration: environment/argv contracts, not malicious-hook execution

This probe establishes that the new test detects the missing **constructed environment pin**. It does **not** demonstrate that a malicious system Git configuration was read or blocked, nor that an attacker hook was executed or prevented. No malicious config or hook payload was installed.

The adjacent fixture tests execute Git under `safe_env=git_clean_env()` (`tools/bash-witness-study.py:1258-1278`) and observe the constructed `-c core.hooksPath=/dev/null` argv using `wraps=subprocess.run` (`:1298-1311`). Those three hook-pin checks remain green in this MB07 run. The source itself explicitly limits those checks to command-pin contracts rather than reachable hooks (`:1298-1299`). The passing canary-materialization/sweep tests are separate inherited-repository-selection checks, not evidence of MB07 malicious-system-config execution. Registry identity/PID-reuse testing is outside this assigned mutant and was not run.

Agreement: the frozen **KILLED** classification is supported by the intended behavioral assertion, so MB07 is genuinely discriminated under the explicit environment contract. There is no disagreement with the measured one-mutant result. Any stronger inference of malicious-hook execution/prevention, real system-config attack coverage, an 18-mutant sweep, or numeric expertise gain would be unsupported by this probe.

## Isolation, commands, hashes, and restoration

Supplemental scratch: `/tmp/tameshi-r21-KillMB07-x5x9o1ld`, with read-only sibling exposure through symlinks and the same bwrap read-only-root envelope. Setup commands, each exit **0** with empty stdout/stderr:

```sh
git -c core.hooksPath=/dev/null clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillMB07-x5x9o1ld/fleet/tameshi-shokunin
git -c core.hooksPath=/dev/null -C /tmp/tameshi-r21-KillMB07-x5x9o1ld/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

Clone/checkout used inherited `GIT_*` scrubbing plus `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`. Each of the three detector invocations used the exact argv retained in `MB07.replay.json`, ending in `python3 <private-clone>/tools/bash-witness-study.py selftest`, with the original ruler's bwrap/env envelope. Source inspection also used read-only `git show 790abd2129f153c13b471e381d454186edbde65e:tools/bash-witness-study.py` (exit **0**).

| Source bytes | SHA-256 |
|---|---|
| Pristine private-clone tool | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Mutated tool, matching frozen-run mutant hash | `00e2211ad5955b709fe572530dcb6ec8d61c858ccb252f01e9902a6cd3c5921f` |
| Restored tool, before and after restored detector | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Production tool, before and after supplemental replay | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |

Exact restored-byte equality to the original saved bytes was observed **true**. The restored selftest returned green. The scratch tree was then removed and its absence observed **true**. The frozen ruler separately disposes its private clones (`c1-survivors.py:131,139-140`); no restoration of production was necessary because it was never mutated.

Pristine/restored stdout SHA-256: `1755081d09ccdb98f4dbb2627883cc9b2ab0f58c833663ca293acb7873ddbdf1`. Mutant stdout SHA-256: `72df0fe9fa2520e39f34081ee5e1fadf93f44a6e758c65ca5d84bc38d88a89db`. Every selftest stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Both stdout hashes match the respective original frozen-run receipt values.

No installs or updates were performed. No full batteries, build, lint, formatter, integration, shipping, or judging runtime was invoked. The assigned MB07 probe is complete.

Report: .ufo/waves/round-21/w2/KillMB07.md
