done — MB09 is **genuinely discriminated**, limited to the constructed Git argv contract. Frozen ruler: **KILLED**, anchor count **1**, pristine exit **0**, mutant exit **1**. Independent same-detector round trip: **0 → 1 → 0** with exact source-byte restoration.

# Scope and axes

- Revision: `790abd2129f153c13b471e381d454186edbde65e`.
- Owning file: `tools/bash-witness-study.py`.
- Operability: execute the frozen item-specific detector and the actual owning selftest in isolated, revision-pinned clones.
- Calibration: identify the exact discriminator without treating constructed command pins as evidence of malicious-hook execution or broader security coverage.
- Production source, contracts, Git index/refs, fleet siblings, and other seats' files were not modified. No subagents, other runtimes, full batteries, builds, lint, or formatters were invoked. No tools were installed or updated.

# Mutant and intended discriminator

The frozen contract at `.ufo/evidence/round-21/c1-mutants.json:49-52` removes only the `-c core.hooksPath=/dev/null` pair from fixture `git add`:

```python
# old
                ["git", "-c", "core.hooksPath=/dev/null",
                 "-C", str(repo), "add", "--", TARGET_GIT_PATH],
# new
                ["git",
                 "-C", str(repo), "add", "--", TARGET_GIT_PATH],
```

All following source anchors refer to the full revision above:

- `tools/bash-witness-study.py:1252-1280`: `fixture_repo` constructs real repositories; the mutation is at **1265**, in the `subprocess.run` call at **1264-1268**. The child retains `check=True` and `env=safe_env`.
- `tools/bash-witness-study.py:333-339,1258`: fixture Git environment drops inherited `GIT_*`, pins global configuration to `/dev/null`, and disables system configuration.
- `tools/bash-witness-study.py:1298-1311`: the new test expressly calls itself a **command-pin contract**, not a claim that init/add has a reachable hook in the scrubbed environment. `patch.object(subprocess, "run", wraps=subprocess.run)` observes actual subprocess calls while forwarding them to real Git. The `add` case requires exactly one matching invocation and the runtime argv token pair `["-c", "core.hooksPath=/dev/null"]`.
- `tools/bash-witness-study.py:1231-1238,1711-1716`: a failed check increments the selftest failure count and returns exit 1 normally, rather than crashing.
- `.ufo/evidence/round-21/c1-survivors.py:38-57,106-140`: the frozen runner executes the bounded bwrap selftest, requires anchor count 1 and a green pristine control, and classifies nonzero mutant exit as killed before deleting its private clone.

Expected failing case: **`fixture add pins hooks off`**, generated at `tools/bash-witness-study.py:1307-1311` with `operation == "add"`.

# Commands and observed exits

The required attack was run exactly as dispatched:

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only MB09 --jobs 1 --json
```

Exit: **0**. Full, unmodified JSON stdout is saved at `.ufo/waves/round-21/w2/mutations/MB09.json`; stderr and exit are saved at `mutations/MB09.stderr` and `mutations/MB09.exit` under the same directory. Actual stderr:

```text
C1 MB09 tools/bash-witness-study.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

Frozen receipt: total 1, killed 1, survived 0, inconclusive 0; anchor count 1; pristine `VERDICT: PASS`, exit 0; mutant `VERDICT: FAIL`, exit 1; neither timed out. Both stderr streams were empty.

For exact restoration evidence and full case output, a separate private clone was created at `/tmp/tameshi-r21-KillMB09-o8gj0it_/fleet/tameshi-shokunin`, with read-only production sibling symlinks beside it. These setup commands both exited **0**, with empty stdout/stderr:

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillMB09-o8gj0it_/fleet/tameshi-shokunin
git -C /tmp/tameshi-r21-KillMB09-o8gj0it_/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

The same bwrap detector argv was used on pristine, mutated, and restored bytes. Its exact argv, setup outputs, 900-second timeout, source hashes, and output hashes are retained in `.ufo/waves/round-21/w2/mutations/MB09.roundtrip.json`. Readably, with `R=/tmp/tameshi-r21-KillMB09-o8gj0it_` and `D=$R/fleet/tameshi-shokunin`, it was:

```sh
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind "$R" "$R" --unshare-net --die-with-parent --chdir "$D" env -i "PATH=$PATH" "HOME=$R/home" "TMPDIR=$R/tmp" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C python3 "$D/tools/bash-witness-study.py" selftest
```

The invoking subprocess environment had inherited `GIT_*` removed; private-clone setup additionally pinned `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`. PATH was inherited and its literal value is in the round-trip receipt. The specimen was changed only at the frozen anchor, then restored before cleanup.

| Specimen | Exit | Terminal output | Actual failed checks |
|---|---:|---|---|
| Pristine | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | None |
| MB09 | 1 | `WITNESS_SELFTEST: 50/51 pass`; `VERDICT: FAIL` | `fixture add pins hooks off` only |
| Restored | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | None |

All three stderr streams were empty. Full output files are `mutations/MB09.{pristine,mutated,restored}.{stdout,stderr}` under this report's directory. Pristine/restored stdout SHA-256 is `1755081d09ccdb98f4dbb2627883cc9b2ab0f58c833663ca293acb7873ddbdf1`; mutant stdout SHA-256 is `93b1e770b208ef35a048f6fe2d299207d144fa0beef6d7fe7cf98d8ea33deeb3`. These match the corresponding frozen receipt output hashes.

Read-only `git show` of both `790abd2129f153c13b471e381d454186edbde65e:tools/bash-witness-study.py` and `790abd2129f153c13b471e381d454186edbde65e:.ufo/evidence/round-21/c1-mutants.json` exited **0**. The pinned spec digest matches the frozen receipt: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`. Frozen runner digest: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.

# Discriminator assessment and limits

**Genuinely discriminated, not incidental:** the mutant completes all 51 cases, fails exactly the intended `fixture add pins hooks off` assertion, retains passing init/commit pin checks and Git-selector canary checks, and returns through the ordinary selftest summary. This is not a syntax/import/setup failure, unrelated assertion, source-hash check, or source grep. The killing assertion examines **runtime argv** captured by a wrapping spy; source and stdout hashes serve provenance/restoration only.

**Claim boundary:** this probe observes construction of the explicit hook-disable option in a real fixture Git invocation. It does **not** install or execute a malicious hook, demonstrate a reachable `git add` hook, or prove exploit prevention. The mutation affects the selftest's fixture helper, not an independently demonstrated production-hook execution path. Environment-pin checks also remain green; that does not expand MB09 into an adversarial environment-execution test. Registry identity/PID reuse tests are outside this item's scope.

The frozen receipt's `fail_lines` includes `check FAIL without denominator is inconclusive, not a crash ok` even for the pristine pass, because the runner at `c1-survivors.py:53` selects lines containing `" FAIL"`. That is a **passing case name**, not an extra failed assertion. The full mutated output at `mutations/MB09.mutated.stdout:6,30,52-53` preserves the distinction.

Agreement: the frozen **KILLED** result is supported for this precise command-pin contract. Disagreement with any stronger interpretation: no malicious-hook execution or general security guarantee was measured. No score, expertise, contract, or integration changes were made.

# Restoration evidence

| Source state | SHA-256 |
|---|---|
| Before mutation | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Mutated | `ed3d573d3fcc252dfff69eb187bb5388f2bc2f00976bca77ce18deb1afb3d600` |
| Restored | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |

Restored bytes were compared directly with the original byte buffer: **equal**. The restored detector passed 51/51. Production source SHA-256 before/after was also `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9`. The supplemental scratch tree was removed only after restoration and the restored run; `MB09.roundtrip.json` records `scratch_removed: true` and `restored_before_removal: true`. The frozen runner independently cleans its own disposable clones. No mutation was left in production or another seat's source.

Report: `.ufo/waves/round-21/w2/KillMB09.md`
