done — **genuinely discriminated / KILLED**. MB05 changes the constructed child-environment contract; the intended assertion is the sole failing case. Pristine and exact-byte-restored controls both pass. This is author-side advisory mutation evidence, not outside admission or an integration decision.

# Scope and axes

- **Operability:** replay exactly frozen C1 mutant MB05 against `790abd2129f153c13b471e381d454186edbde65e`; require anchor count 1 and a green pristine control.
- **Calibration:** distinguish a runtime environment-construction assertion from source inspection, incidental failure, and malicious-hook execution. Preserve all actual outputs and restoration hashes.
- Only this mutant and the owning tool's bounded `selftest` were exercised. No other mutant, F5 profile, repository-wide battery, build, lint, or formatter was run. No subagents, other agent runtime, installation, or update was invoked.

# Mutant and source anchors

All owning-tool line references below are to `tools/bash-witness-study.py` at `790abd2129f153c13b471e381d454186edbde65e`, read from the private detached clone.

- Frozen definition: `.ufo/evidence/round-21/c1-mutants.json:25-28`; owning invocation is `selftest` at lines 123-125.
- Single behavior-bearing change: `git_clean_env()` line 337:

```diff
-    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
+    env["GIT_CONFIG_GLOBAL"] = str(REPO / ".gitconfig")
```

- Existing contract: `git_clean_env()` lines 333-339 removes inherited `GIT_*`, pins global configuration to `/dev/null`, disables system configuration, and returns the child environment. `materialize_target()` passes that return value to the real Git child at lines 347-350.
- Intended new discriminator: lines 1283-1290 patch hostile inherited Git selections and execute `git_clean_env()`. Lines **1294-1295**, exact case **`pins global Git configuration`**, require `child_env.get("GIT_CONFIG_GLOBAL") == os.devnull`.
- Failure collection is ordinary executed test logic, lines 1231-1238. Completion and nonzero exit come from the actual failed-case count at lines 1711-1716.
- Read-only `git blame --line-porcelain -L 1282,1311 790abd2129f153c13b471e381d454186edbde65e -- tools/bash-witness-study.py` in the private clone exited **0** and attributes this discriminator and adjacent command-pin tests to **`370f2dffe66f00c3c7412c962bf3e8fcbe75dfdb`**, with predecessor `33d03b716d3edcf1d8656d46d6df61801d232c52`.

# Frozen replay: actual command, exit, stderr

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only MB05 --jobs 1 --json
```

- Actual exit: **0**; elapsed observation: **0.844 s**.
- Full, unabridged stdout JSON: [`mutations/MB05.json`](mutations/MB05.json).
- Full stderr, also retained in [`mutations/MB05.stderr.txt`](mutations/MB05.stderr.txt):

```text
C1 MB05 tools/bash-witness-study.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

- Observed `anchor_count`: **1**.
- Pristine: exit **0**, terminal `VERDICT: PASS`, no timeout.
- Mutant: exit **1**, terminal `VERDICT: FAIL`, no timeout.
- Ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.
- Frozen-spec SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.

The invocation environment dropped all inherited `GIT_*` and used fresh scratch HOME, XDG_CONFIG_HOME, and TMPDIR. The frozen detector itself creates private clones and supplies its scrubbed/pinned sandbox environment (`c1-survivors.py:34-45,60-67,93-123`). Its cleanup removes those clones (`:131,139-140`); production was not mutated.

# Same-detector pristine → mutant → restored probe

A second private clone supplied raw selftest output and the explicit restored-byte control required for this probe:

```text
W=/tmp/tameshi-r21-KillMB05-k4mykzvc
D=/tmp/tameshi-r21-KillMB05-k4mykzvc/fleet/tameshi-shokunin
```

Actual setup commands, each exit **0**, empty stdout/stderr:

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillMB05-k4mykzvc/fleet/tameshi-shokunin
git -C /tmp/tameshi-r21-KillMB05-k4mykzvc/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

Sibling entries beside the clone are symlinks into the fleet. The sandbox makes `/` read-only and binds only this private scratch writable, so those sibling targets remain read-only. Before the first run, the owning file had exactly one frozen old anchor. A surgical one-line edit applied MB05; the inverse edit restored the original bytes before the third run.

Each phase used the **same argv** and 900-second bound as the frozen detector's `selftest()` envelope, with these scratch paths:

```sh
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind "$W" "$W" --unshare-net --die-with-parent --chdir "$D" env -i "PATH=$PATH" "HOME=$W/home" "TMPDIR=$W/tmp" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C python3 "$D/tools/bash-witness-study.py" selftest
```

This is an argv rendering, not a separately executed shell wrapper. Full literal argv, including the inherited PATH value, outer-environment controls, setup receipts, all raw stdout/stderr, and exit codes are retained in [`mutations/MB05.restoration.json`](mutations/MB05.restoration.json).

| Bytes exercised | Exit | Actual terminal summary | Actual failing case |
|---|---:|---|---|
| Pristine | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | None |
| MB05 | 1 | `WITNESS_SELFTEST: 50/51 pass`; `VERDICT: FAIL` | `pins global Git configuration` |
| Restored | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | None |

Exact failing output, mutant stdout line 3:

```text
  check pins global Git configuration                FAIL
```

All three stderr streams are empty. The other 50 cases pass under MB05, including fixture init/add/commit hook pins, materialization redirection, sweep redirection, and final private-root removal. There is no syntax/import/setup failure or unrelated failing assertion.

## Restoration and raw-output evidence

| Evidence | SHA-256 |
|---|---|
| Original owning-tool bytes | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| MB05 owning-tool bytes | `fd47219e52c9c0522f05dd13c6fc2a0ba8e4c401d912043ff0a68f2daa14e333` |
| Restored owning-tool bytes | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Pristine/restored stdout, each | `1755081d09ccdb98f4dbb2627883cc9b2ab0f58c833663ca293acb7873ddbdf1` |
| Mutant stdout | `78d9b1cd4cb19f2002ec2ec196a9ba3cd8f820284a122c88eb7cfaf18ed04ea5` |
| Each phase's empty stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Observed direct byte equality after restoration is **true**; restored old-anchor count is **1**. Both stdout and stderr are byte-identical between pristine and restored. The supplemental pristine/mutant output and owning-file hashes also match the frozen receipt exactly. The restored private clone is retained at the path above; no production source, contract, index/ref, or sibling source was edited.

Individual raw streams are retained as `mutations/MB05.{pristine,mutated,restored}.{stdout,stderr}.txt`.

# Discriminator assessment and limits

**Agreement:** the frozen result `KILLED` is genuinely discriminated for the declared safe-global-configuration environment contract. The replacement redirects the environment value away from `/dev/null`; an executed call to the real helper returns that wrong value, and the specifically named runtime assertion alone fails. This is not detection by hashing or grepping the tool's source. The frozen ruler's anchor count and SHA reporting identify the mutation; they are not the failing selftest assertion.

**Calibration qualification:** this demonstrates the **constructed environment** contract, not malicious-config effects or malicious-hook execution. The fixture's hostile `GIT_CONFIG_GLOBAL` value is a path value supplied to the helper; this probe does not install a malicious global configuration or hook and does not establish that such a hook executed. The adjacent `fixture init/add/commit pins hooks off` cases (lines 1298-1311) observe constructed argv through `subprocess.run` with `wraps=subprocess.run`; their green results assert `-c core.hooksPath=/dev/null`, not execution of an attacking hook. The source explicitly states this limitation at lines 1298-1299. No registry identity test or real PID-reuse claim is involved in MB05.

**Receipt parsing caveat:** frozen `fail_lines` also contains `check FAIL without denominator is inconclusive, not a crash ok` in the pristine receipt. That is a **passing** case whose name contains `FAIL`, caught by the ruler's broad substring extraction (`c1-survivors.py:53`). Raw logs show its `ok` suffix in all phases. It is not a baseline failure or a second mutant failure; the control's exit is 0 and its actual summary is 51/51. No disagreement with the single-mutant KILLED verdict; no aggregate population or expertise claim is inferred from this one probe.

Report: .ufo/waves/round-21/w2/KillMB05.md
