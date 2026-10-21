done — MB04 is **genuinely discriminated** at `790abd2129f153c13b471e381d454186edbde65e`.

# Scope and axes

- **Operability:** replay exactly frozen C1 mutant MB04 against the owning selftest, with a green pristine control, a unique mutation anchor, and exact-byte restoration.
- **Calibration:** distinguish a constructed-environment contract failure from malicious configuration/hook execution, setup failures, and incidental assertions.
- Author-side advisory only; no admission, integration, shipping, expertise, depth, or broader-population claim. This probe covers one assigned mutant, not the other 17 C1 mutants.

# Frozen mutation and expected detector

Contract: `.ufo/evidence/round-21/c1-mutants.json:19-22`.

```diff
-    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
```

The frozen `old` includes the trailing newline; `new` is empty. Anchor count was **1** in both the prescribed receipt and the private restoration probe. The behavior-bearing point is `tools/bash-witness-study.py:337` at the full revision above, inside `git_clean_env()` (`:333-339`). The inherited `GIT_*` scrub remains in place (`:335-336`), so deleting the assignment leaves `GIT_CONFIG_GLOBAL` absent from the returned child environment.

Expected discriminator: **`pins global Git configuration`**, pinned source `tools/bash-witness-study.py:1283-1295`. The test patches the process environment with foreign Git selections, calls the actual `git_clean_env()`, then checks `child_env.get("GIT_CONFIG_GLOBAL") == os.devnull`. This is a runtime return-value assertion, not a source grep or source-hash assertion. Source hashes in the ruler are evidence bookkeeping.

# Prescribed command and actual result

Executed with inherited `GIT_*` variables removed (none were present), cwd at the repository:

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only MB04 --jobs 1 --json
```

**Command exit: 0.** Actual stderr:

```text
C1 MB04 tools/bash-witness-study.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

Full, unabridged stdout JSON is saved at `.ufo/waves/round-21/w2/mutations/MB04.json`; raw stderr and invocation/exit/hashes are in `MB04.stderr.txt` and `MB04.command.json` in the same directory.

| Observation | Pristine control | MB04 |
|---|---:|---:|
| Selftest exit | 0 | 1 |
| Timeout | false | false |
| Terminal verdict | `VERDICT: PASS` | `VERDICT: FAIL` |
| Ruler result | green control | `KILLED` |

Receipt identity:

- Ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`
- Frozen contract SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`
- Full JSON stdout SHA-256: `f2f0c36d532d444a1cddb73d79f4d003bf1d42ffc3462011d4040e80c88d3199`

# Same-detector pristine / mutated / restored probe

The prescribed ruler removes its private clones (`c1-survivors.py:131,139-140`); it does not provide a restored-byte run. To satisfy restoration evidence, I additionally used one private clone at `/tmp/tameshi-r21-KillMB04-otrlofm5/fleet/tameshi-shokunin`, pinned to the same revision. Its sibling fleet entries are symlinks; the detector exposes the host tree read-only and binds only this scratch root writable.

Setup commands, each **exit 0**, with inherited `GIT_*` scrubbed and `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, private `HOME`, and `LC_ALL=C` pinned:

```sh
git -c core.hooksPath=/dev/null clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillMB04-otrlofm5/fleet/tameshi-shokunin
git -c core.hooksPath=/dev/null -C /tmp/tameshi-r21-KillMB04-otrlofm5/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

Each phase invoked the **unchanged frozen ruler's `selftest()`**, not a replacement detector. A wrapper around its subprocess runner only retained complete stdout/stderr; it returned the original subprocess result unchanged. The detector command is below, with `S=/tmp/tameshi-r21-KillMB04-otrlofm5` and `PATH` the invoking value (the complete expanded argv for every phase is retained in `MB04.restoration.json`):

```sh
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind "$S" "$S" --unshare-net --die-with-parent \
  --chdir "$S/fleet/tameshi-shokunin" \
  env -i "PATH=$PATH" "HOME=$S/home" "TMPDIR=$S/tmp" \
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C \
  python3 "$S/fleet/tameshi-shokunin/tools/bash-witness-study.py" selftest
```

| Bytes under test | Exit | Actual terminal output | Actual failing case |
|---|---:|---|---|
| Pristine | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | none |
| Exact frozen MB04 | 1 | `WITNESS_SELFTEST: 50/51 pass`; `VERDICT: FAIL` | `pins global Git configuration` |
| Exactly restored | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | none |

All three selftest stderr streams were empty; no timeout occurred. The sole failing check was output line 3:

```text
  check pins global Git configuration                FAIL
```

The other 50 checks completed successfully, including actual fixture Git setup, the three hook-argv pin checks, materialization/sweep selector canaries, and final fixture cleanup. The failure counter/terminal verdict is implemented at pinned `tools/bash-witness-study.py:1231-1238,1711-1716`. There was no syntax/import error, traceback, setup refusal, or unrelated failing assertion.

The ruler's `fail_lines` also contains `check FAIL without denominator is inconclusive, not a crash ok` in **both** green and red runs. That is a passing case whose name contains `FAIL`, selected by the ruler's broad text filter (`c1-survivors.py:53`); it is not another failed case. Raw complete logs distinguish the trailing `ok` from the genuine trailing `FAIL`.

# Interpretation and limits

**Agreement:** the C1 `KILLED` classification is supported by a green baseline, exactly one frozen anchor, the intended runtime contract assertion failing, and the restored control returning green. Classification is genuinely discriminated, not incidental, equivalent, or inconclusive.

**Important limit:** this demonstrates the **constructed child-environment contract**. The hostile `foreign-config` value is a synthetic path in patched `os.environ`; this test does not plant malicious Git configuration or demonstrate its execution. Deletion of the explicit pin is observed directly in the function's returned environment. The benign temporary Git fixtures still work under the mutant, which is consistent with this narrower contract claim.

The related hook tests (`tools/bash-witness-study.py:1252-1279,1298-1311`) wrap actual `subprocess.run` calls and inspect constructed argv for `-c core.hooksPath=/dev/null`; all three pass here. The source explicitly calls them command-pin contracts, not proof that init/add have a reachable hook under the scrubbed environment. **No malicious-hook execution was attempted or observed.** No registry identity or real-PID-reuse claim is made by this MB04 probe.

No disagreement with the scoped C1 result; disagreement only with any extrapolation from this contract check to an observed malicious-hook/config execution defense.

# Restoration and retained evidence

Tool-byte SHA-256 values:

| State | SHA-256 |
|---|---|
| Pristine | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Mutated | `a4f69d3f98502babd0843556fdf25c8b70d501d087ad2ac8f853b9b83605471a` |
| Restored | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |

The scratch mutation equaled the exact frozen byte replacement and matched the prescribed ruler's mutated SHA-256. Restored bytes were compared directly with the original bytes and were identical. Pristine and restored stdout were also identical (SHA-256 `1755081d09ccdb98f4dbb2627883cc9b2ab0f58c833663ca293acb7873ddbdf1`); mutant stdout SHA-256 was `78d9b1cd4cb19f2002ec2ec196a9ba3cd8f820284a122c88eb7cfaf18ed04ea5`.

The production owning tool's before/after SHA-256 remained `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9`. No production source, contracts, ledgers, refs/index, or sibling source was edited. The private clone is left exactly restored.

Evidence, all relative to the repository:

- `.ufo/waves/round-21/w2/mutations/MB04.json` — prescribed full JSON.
- `.ufo/waves/round-21/w2/mutations/MB04.stderr.txt` and `MB04.command.json` — prescribed stderr, exact argv, exit, and production before/after hashes.
- `.ufo/waves/round-21/w2/mutations/MB04.restoration.json` — setup commands/exits, expanded bounded detector argv and results for all three phases, restoration equality and hashes.
- `.ufo/waves/round-21/w2/mutations/MB04.{pristine,mutated,restored}.{stdout,stderr}.txt` — complete per-phase output.
- `.ufo/waves/round-21/w2/mutations/MB04.source-anchors.json` — numbered source excerpts authenticated by the pinned tool SHA-256 and full revision.

Tools installed/updated: **none**. Only this item-specific probe was run; no full batteries, builds, lint, or formatter runs.

Report: `.ufo/waves/round-21/w2/KillMB04.md`
