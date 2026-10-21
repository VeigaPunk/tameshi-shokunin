done — MB11 is **genuinely discriminated** (frozen detector: KILLED).

# Scope and axes

- Item: C1 MB11 only; owning tool `tools/bash-witness-study.py`.
- Implementation revision: `790abd2129f153c13b471e381d454186edbde65e`.
- Axes: **operability** (the assigned bounded detector executes and detects the defect), **calibration** (attribute the failure to its actual discriminator, without broader safety claims), and **isolation/restoration** (private clones only; exact-byte restoration).
- This is author-side advisory evidence, not integration, admission, or an expertise increase. No other mutant or full battery was run.

# Mutant and intended discriminator

The frozen contract is `.ufo/evidence/round-21/c1-mutants.json:60-65`; its owning CLI is `selftest`, not `--selftest` (`:122-125`). Exactly one old anchor was present.

```diff
-            prefix="bash-witness-selftest.", dir=private_root))
+            prefix="bash-witness-selftest.", dir=private_root.parent))
```

At the pinned revision, `tools/bash-witness-study.py:1240-1248` creates an absolute private root under `/tmp`, creates an actual child directory with `tempfile.mkdtemp`, and checks:

```python
check("private child is contained", root.parent == private_root)
```

The mutation at line 1246 instead creates the working directory alongside the private root. The expected discriminator is therefore the **runtime path-containment check**, named **`private child is contained`**, at line 1248. It compares the actual directory paths returned by `mkdtemp`; it does not grep or hash source text. `check` records failures at `:1231-1238`, and `:1711-1716` emits the final summary and exit status. The invariant being tested is the selftest fixture's own private-child placement, not an unrelated production classification algorithm.

# Assigned frozen detector

Actual command (invoking environment minus inherited `GIT_*`):

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only MB11 --jobs 1 --json
```

Exit **0**, elapsed **0.736 s** for invocation and evidence capture. Full, unmodified stdout JSON: `mutations/MB11.json`; complete stderr: `mutations/MB11.stderr.txt`; invocation/exit/digests: `mutations/MB11.command.json`. These paths are relative to this report's directory.

Actual stderr:

```text
C1 MB11 tools/bash-witness-study.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

Receipt: `total=1`, `killed=1`, `survived=0`, `inconclusive=0`, `anchor_count=1`. Pristine control exit **0**, `VERDICT: PASS`, no timeout; mutant exit **1**, `VERDICT: FAIL`, no timeout. Both selftest stderr streams were empty. The outer exit 0 means the mutation was killed, not that the mutated selftest passed.

The first attempt to launch this command through asynchronous `bash` was rejected before execution: `Background job limit reached (100). Wait for running jobs to finish or cancel one.` The successful execution above used a directly captured subprocess with the same argv; that rejected launch is not a detector observation and is not counted as a pass.

# Pristine / mutated / restored behavioral evidence

To satisfy the exact-restoration protocol and retain full case output, I used a second, isolated clone at the same revision in `/tmp/tameshi-r21-KillMB11-xmfqgcr6/fleet/tameshi-shokunin`. This was the same MB11 probe, not another mutation. Siblings were symlinked beside it and read-only during execution. Clone/checkout commands, both exit **0**, were:

```sh
git -c core.hooksPath=/dev/null clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillMB11-xmfqgcr6/fleet/tameshi-shokunin
git -c core.hooksPath=/dev/null -C /tmp/tameshi-r21-KillMB11-xmfqgcr6/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

Clone setup dropped inherited `GIT_*`, pinned `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`, and disabled hooks. Each detector phase used the identical bounded bwrap argv/environment from `.ufo/evidence/round-21/c1-survivors.py:38-48`: read-only `/`, isolated `/tmp`, the scratch bind, no network, `env -i`, inherited PATH, scratch HOME/TMPDIR, pinned Git config and `LC_ALL=C`, followed by `python3 <private-clone>/tools/bash-witness-study.py selftest`. The complete literal argv, setup commands/exits, phase records, and restoration results are retained in `mutations/MB11.restoration.json`. Timeout was 900 seconds per phase.

| Bytes | Exit | Elapsed | Actual selftest summary | Actual failing checks |
|---|---:|---:|---|---|
| Pristine | 0 | 0.073 s | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | none |
| MB11 | 1 | 0.073 s | `WITNESS_SELFTEST: 50/51 pass`; `VERDICT: FAIL` | `private child is contained` only |
| Restored | 0 | 0.070 s | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | none |

Each stdout contains 53 lines; each stderr is empty. Full streams are `mutations/MB11.{pristine,mutated,restored}.{stdout,stderr}.txt`. In the mutant stdout, line 1 is the sole failed check, line 51 confirms `private root is removed ... ok`, and lines 52-53 show the normal selftest summary and verdict. All other 50 checks pass. There was no syntax/import/setup exception, premature abort, unrelated failed assertion, or source-digest refusal. Pristine and mutated stdout digests also match the respective frozen-detector receipt, and restored stdout is byte-identical to pristine stdout.

# Calibration and limits

- **Agreement:** the recorded KILLED result is attributable to the intended runtime containment discriminator, not merely any nonzero exit. This is not an equivalent mutation: actual child placement changes and the matching test alone turns red.
- **Receipt presentation caveat:** the frozen ruler's `fail_lines` list also includes `check FAIL without denominator is inconclusive, not a crash ok` in both pristine and mutated output. That case at `tools/bash-witness-study.py:1485-1489` **passes**. `.ufo/evidence/round-21/c1-survivors.py:53` collects any line containing ` FAIL`; it therefore includes this name as a substring false positive. Its list is diagnostic text, not a count of failing checks. The actual kill decision uses process status (`:125-130`); the only failed check ends with `FAIL` and is the containment check. No detector or contract was modified.
- Git environment pins at `tools/bash-witness-study.py:1282-1297` inspect the constructed child environment. Hook-pin checks at `:1298-1311` wrap real fixture Git calls and inspect their constructed argv; the source explicitly describes them as command-pin contracts. Their green results do **not** demonstrate execution or suppression of a malicious hook. MB11 neither removes those pins nor uses them as its failing discriminator.
- MB11 is not a registry identity/PID-reuse mutation. No registry race or real PID-reuse behavior was exercised, and no such conclusion is drawn.
- This item supports the narrow MB11 kill only, not an independent recount of all 18 frozen survivors or a broader production-security claim.

# Hashes and restoration

SHA-256 of the owning tool:

| State | SHA-256 |
|---|---|
| Pinned pristine / live before | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| MB11 scratch mutant | `69e9c892c75cf71eab9ac5b4959448fca87b869d5934f25e66e18783f95b24ef` |
| Exact restored scratch / live after | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |

The restored scratch bytes were compared directly with the saved original bytes: **equal**. The restored behavioral detector was green before cleanup. The scratch tree was then removed, and absence was observed. The frozen ruler also disposes its own private clone trees (`c1-survivors.py:131,139-140`).

Additional before/after identities, unchanged:

- Ruler `.ufo/evidence/round-21/c1-survivors.py`: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.
- Frozen contract `.ufo/evidence/round-21/c1-mutants.json`: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.
- Pristine/restored stdout: `1755081d09ccdb98f4dbb2627883cc9b2ab0f58c833663ca293acb7873ddbdf1`.
- Mutant stdout: `a5117fbc645602dbd63cb685b71c1047a6cc3713ff9784f4dceb913b67188e01`.
- Empty selftest stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Only this report and MB11-named evidence were written in the production checkout; the implementation, ruler, contract, index, refs, fleet state, and siblings were not edited. No tools were installed or updated. No unrun check is represented as green.

Report: .ufo/waves/round-21/w2/KillMB11.md
