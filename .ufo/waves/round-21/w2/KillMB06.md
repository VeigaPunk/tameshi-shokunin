done — MB06 is **genuinely discriminated** (`KILLED`) at `790abd2129f153c13b471e381d454186edbde65e`. This is author-side advisory evidence, not outside admission.

# Scope and axes

- **Operability:** reproduce the frozen MB06 detector, require a green pristine control and exactly one mutation anchor, and exercise the same bounded detector on pristine, mutated, and byte-restored source.
- **Calibration:** identify the actual failing case and limit the result to the constructed Git environment contract. Do not infer malicious-hook execution, real PID reuse, or an expertise-score increase.
- Production source, contracts, ledgers, index/refs, fleet state, and sibling sources were not edited. Durable deliverables are this report and MB06-named evidence; the mutation was confined to a unique private scratch clone. See the import-cache hygiene observation below. No installs or updates were needed.

# Mutant and expected discriminator

Frozen contract: `.ufo/evidence/round-21/c1-mutants.json:30-35`; detector arguments at `:122-125` are `["selftest"]` (not `--selftest` for this tool).

At `tools/bash-witness-study.py:338`, replace exactly:

```python
    env["GIT_CONFIG_NOSYSTEM"] = "1"
```

with:

```python
    env["GIT_CONFIG_NOSYSTEM"] = "0"
```

`git_clean_env()` at `tools/bash-witness-study.py:333-339` removes inherited `GIT_*` settings, then pins global and system configuration inputs. The expected discriminator is the named case **`disables system Git configuration`** at `:1296-1297`, checking the returned mapping's `GIT_CONFIG_NOSYSTEM == "1"` after invoking `git_clean_env()` under a hostile inherited Git environment (`:1282-1290`). This executes the helper and inspects its runtime result; it does not grep or hash the implementation to decide this case.

All owning-tool source line references above and below are at `790abd2129f153c13b471e381d454186edbde65e`. The private clone's complete tool bytes were compared with `git show 790abd2129f153c13b471e381d454186edbde65e:tools/bash-witness-study.py`; they matched, as did the production tool bytes read before the probe.

# Required frozen command and actual result

Executed:

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only MB06 --jobs 1 --json
```

- Exit: **0**.
- Full, unmodified stdout JSON: `.ufo/waves/round-21/w2/mutations/MB06.json`.
- Stderr: `.ufo/waves/round-21/w2/mutations/MB06.stderr`.
- Exit receipt: `.ufo/waves/round-21/w2/mutations/MB06.exit`.
- `anchor_count`: **1**.
- Pristine control: exit **0**, `VERDICT: PASS`, no timeout.
- Mutant: exit **1**, `VERDICT: FAIL`, no timeout.
- Frozen counts: **killed=1, survived=0, inconclusive=0, total=1**. These are the MB06-only diagnostic subset, not a new full-population measurement.

Exact stderr:

```text
C1 MB06 tools/bash-witness-study.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

Instrument SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.
Frozen spec SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.

# Pristine / mutated / restored replay

The required instrument deletes its private clones (`c1-survivors.py:131,139-140`). To obtain an explicit restoration control and complete owning-test output, I additionally used a separate private clone at:

```text
/tmp/tameshi-r21-KillMB06-pycnp6ti/fleet/tameshi-shokunin
```

Clone setup commands, both exit **0**, with empty stdout/stderr:

```sh
git -c core.hooksPath=/dev/null clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillMB06-pycnp6ti/fleet/tameshi-shokunin
git -c core.hooksPath=/dev/null -C /tmp/tameshi-r21-KillMB06-pycnp6ti/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

Clone setup dropped all inherited `GIT_*` variables and set `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`. Sibling symlinks were placed beside the private clone; the detector's read-only root bind prevented writes through them.

For each of the three source states, I invoked the **same unmodified** `c1-survivors.py:selftest` implementation (`:38-57`), with `tool="tools/bash-witness-study.py"`, args `["selftest"]`, and its existing **900-second** timeout. Its `run` wrapper was wrapped only to retain subprocess output; argv, environment, timeout, result, and classification logic were not altered. Exact argv for every invocation is preserved in `MB06.replay.json`. The command shape was:

```sh
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind /tmp/tameshi-r21-KillMB06-pycnp6ti /tmp/tameshi-r21-KillMB06-pycnp6ti \
  --unshare-net --die-with-parent \
  --chdir /tmp/tameshi-r21-KillMB06-pycnp6ti/fleet/tameshi-shokunin \
  env -i PATH="$PATH" \
  HOME=/tmp/tameshi-r21-KillMB06-pycnp6ti/home \
  TMPDIR=/tmp/tameshi-r21-KillMB06-pycnp6ti/tmp \
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C \
  python3 /tmp/tameshi-r21-KillMB06-pycnp6ti/fleet/tameshi-shokunin/tools/bash-witness-study.py selftest
```

Only the frozen line-338 MB06 replacement was applied, then reversed. No additional mutant was introduced.

| Source state | Exit | Actual terminal tally | Actual failed cases | Stderr | Timeout |
|---|---:|---|---|---|---|
| Pristine | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | none | empty | no |
| MB06 | 1 | `WITNESS_SELFTEST: 50/51 pass`; `VERDICT: FAIL` | `disables system Git configuration` | empty | no |
| Restored | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | none | empty | no |

The full pristine-to-mutant stdout diff contains exactly these three changed lines:

```diff
-  check disables system Git configuration            ok
+  check disables system Git configuration            FAIL
-WITNESS_SELFTEST: 51/51 pass
-VERDICT: PASS
+WITNESS_SELFTEST: 50/51 pass
+VERDICT: FAIL
```

The remaining **50 cases passed**, including fixture Git setup and later cleanup. The selftest's `check()` records a failed boolean without aborting (`tools/bash-witness-study.py:1231-1238`), and its final tally/exit are at `:1711-1716`. Thus the nonzero result is not a syntax/import/setup failure, unrelated assertion, source-digest trap, or crash.

**Receipt parsing caveat:** the frozen instrument's broad `fail_lines` filter (`c1-survivors.py:53`) also captures the passing case `check FAIL without denominator is inconclusive, not a crash ok` in every state because its *name* contains `FAIL`. That case is defined at `tools/bash-witness-study.py:1487-1489` and passes in all three full outputs. It is not a second failure. The instrument's verdict is based on exit status (`:114-130`), so this diagnostic false positive does not affect the MB06 classification.

# Calibration: what was and was not observed

- **Observed:** the constructed child-environment mapping changes from system-config-disabled to system-config-enabled, and the specifically named runtime contract check detects that one-line defect.
- **Related fixture checks:** `fixture_repo()` passes the helper-produced environment to actual fixture Git calls (`tools/bash-witness-study.py:1258-1279`). The hook-pin tests wrap real `subprocess.run` calls and inspect the constructed `-c core.hooksPath=/dev/null` argv (`:1298-1311`). They passed in every state; MB06 did not kill on a hook-pin failure.
- **Not observed:** a malicious Git hook executing, a malicious system configuration being consumed, or a demonstration of host compromise. The source explicitly describes the hook tests as command-pin contracts, not reachable-hook claims (`:1298-1299`). No malicious hook was installed or executed by this probe.
- This mutant is not a registry identity test. No synthetic PID-race or real PID-reuse result is claimed.
- **Agreement:** the frozen `KILLED` verdict is supported by the intended discriminator, with pristine and restored green controls.
- **Disagreement/limit:** none with the measured MB06 result; any stronger interpretation as malicious-hook execution or complete Git-isolation proof would exceed this evidence. No numeric expertise or full-round admission verdict is asserted.

# Hashes and restoration evidence

| Bytes | SHA-256 |
|---|---|
| Pinned/private pristine tool | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| MB06-mutated tool | `22ab0d39648f07ad7f3858bceaca13e9c69f970fc750240bd4934588420c6956` |
| Restored tool | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Production tool before and after probe | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Pristine/restored stdout | `1755081d09ccdb98f4dbb2627883cc9b2ab0f58c833663ca293acb7873ddbdf1` |
| Mutant stdout | `72df0fe9fa2520e39f34081ee5e1fadf93f44a6e758c65ca5d84bc38d88a89db` |
| Stderr in every selftest state (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Restored source was compared byte-for-byte with the captured original: **equal**. Pristine/restored stdout and stderr were also byte-identical. The restored scratch clone is retained; durable receipts do not depend on its survival. Production tool bytes remained unchanged. The supplementary replay's source and output hashes match the required frozen receipt's corresponding pristine/mutant hashes.

Evidence, relative to this repository:

- `.ufo/waves/round-21/w2/mutations/MB06.json` — complete required frozen receipt.
- `.ufo/waves/round-21/w2/mutations/MB06.stderr` and `MB06.exit` — exact required-command stderr and exit.
- `.ufo/waves/round-21/w2/mutations/MB06.replay.json` — exact replay/setup argv, exits, source/output hashes, output diff, and byte-restoration results.
- `.ufo/waves/round-21/w2/mutations/MB06.pristine.stdout` / `.stderr` — full pristine replay output.
- `.ufo/waves/round-21/w2/mutations/MB06.mutated.stdout` / `.stderr` — full failed mutant replay output, preserved unchanged.
- `.ufo/waves/round-21/w2/mutations/MB06.restored.stdout` / `.stderr` — full restored replay output.

No full batteries, build, lint, formatter, other mutant probes, corpus edits, commits, or admission actions were run.

Import-cache hygiene observation: loading the frozen Python detector for the supplementary replay was not initially bytecode-disabled. Its declared cache path, `.ufo/evidence/round-21/__pycache__/c1-survivors.cpython-314.pyc`, was observed present with mtime/ctime `1792585836.8306508` (about 22.987 seconds after the required command began). A subsequent direct ranged read of that path returned `Path ... not found`, before this agent attempted any removal. Concurrent creation/removal ownership is unestablished; I do not claim that I restored or deleted this shared cache. Further bytecode writing in this Python session was disabled. This transient observation is disclosed rather than claiming that no path outside the requested output/scratch scope could have been written. No source bytes were changed by the import.

Report: .ufo/waves/round-21/w2/KillMB06.md
