done — MB10 genuinely discriminated, narrowly as a constructed Git commit-argv pin contract. Frozen detector: KILLED; pristine/mutated/restored owning selftest exits: 0/1/0.

# Scope and axes

- Operability: replay the exact frozen MB10 substitution at `790abd2129f153c13b471e381d454186edbde65e`, with a green pristine control, one anchor, and an intended failing case.
- Calibration: distinguish an observed subprocess argv contract from malicious-hook execution; do not promote this result into a broader security or capability claim.
- Production was read-only. The only mutation was in my private clone at `/tmp/tameshi-r21-KillMB10-s_4mg_uk/fleet/tameshi-shokunin`, checked out detached at the full revision above. Sibling links were read-only inside the detector's bwrap mount. No production tools, contracts, ledgers, corpus, index, or refs were edited. This is author-side advisory evidence, not admission or integration.

# Mutant and intended detector

The frozen definition is `.ufo/evidence/round-21/c1-mutants.json:54-59`; its owning command is `python3 tools/bash-witness-study.py selftest` (`c1-mutants.json:122-125`). MB10 removes only `"-c", "core.hooksPath=/dev/null"` from the fixture **commit** argv:

```python
# old — tools/bash-witness-study.py:1270-1271 at 790abd2129f153c13b471e381d454186edbde65e
                ["git", "-c", "core.hooksPath=/dev/null",
                 "-C", str(repo), "-c", "user.name=fixture",
# new
                ["git",
                 "-C", str(repo), "-c", "user.name=fixture",
```

The init/add hook pins and all other bytes remain unchanged. The frozen counter reports `anchor_count: 1`; the supplemental replay also observed one pristine anchor and matched the counter's exact mutated SHA-256.

The expected failing case is **`fixture commit pins hooks off`**, emitted by `tools/bash-witness-study.py:1302-1311` at the pinned revision. Lines 1300-1301 wrap the real `subprocess.run` with `unittest.mock.patch(..., wraps=subprocess.run)` and call `fixture_repo`. Lines 1303-1311 select the recorded operation argv, require exactly one such command, and require its actual argument list to contain adjacent `-c`, `core.hooksPath=/dev/null`. The exercised commit is lines 1269-1275; the environment helper is lines 333-339. The test reads neither its own source bytes nor a source hash to decide this check.

# Actual command and frozen receipt

Executed exactly:

```text
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only MB10 --jobs 1 --json
```

Exit: **0**. Full JSON: `.ufo/waves/round-21/w2/mutations/MB10.json`. Full stderr: `.ufo/waves/round-21/w2/mutations/MB10.stderr.txt`:

```text
C1 MB10 tools/bash-witness-study.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

Receipt observations:

| Observation | Pristine control | MB10 |
|---|---:|---:|
| Exit | 0 | 1 |
| Timeout | false | false |
| Final summary | `VERDICT: PASS` | `VERDICT: FAIL` |
| Elapsed seconds | 0.073 | 0.074 |
| Anchor count before substitution | — | 1 |

Recorded instrument identities:

- Ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.
- Contract SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.

One earlier asynchronous tool launch was rejected with `Background job limit reached (100)` before the command ran. It produced no detector measurement. The exact command above was then run once through a captured Python subprocess, and its stdout/stderr were saved without discarding a failure.

# Pristine, mutant, restored replay

To obtain raw per-case output and verify exact restoration, I additionally invoked the frozen counter's unchanged `selftest(w, d, tool, args)` function three times in my private clone: pristine, the same single substitution, and exact restored bytes. A capture-only wrapper around its subprocess helper retained stdout/stderr without changing argv, environment, or results. These were the same bounded owning behavioral detector, not another test battery.

The replay used the counter's `bwrap` envelope at `c1-survivors.py:38-57`: read-only `/`, fresh home/tmp under the private root, network unshared, `env -i`, invoking PATH, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, and `LC_ALL=C`. The outer environment drops inherited `GIT_*`. The replay clone/checkout commands additionally pinned Git global/system configuration and disabled hooks; their exact argv and exit-0 records are in `MB10-restoration.json`. Both checked out only the full pinned revision in the private clone.

For this replay, `W=/tmp/tameshi-r21-KillMB10-s_4mg_uk`, `D=$W/fleet/tameshi-shokunin`; the actual detector argv in each phase was:

```text
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind "$W" "$W" --unshare-net --die-with-parent --chdir "$D" env -i "PATH=<invoking PATH>" "HOME=$W/home" "TMPDIR=$W/tmp" GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C python3 "$D/tools/bash-witness-study.py" selftest
```

The literal expanded argv, including the inherited PATH, is retained in `.ufo/waves/round-21/w2/mutations/MB10-restoration.json`.

| Phase | Exit | Actual denominator | Actual final verdict | Stderr |
|---|---:|---|---|---|
| Pristine | 0 | `WITNESS_SELFTEST: 51/51 pass` | `VERDICT: PASS` | empty |
| Mutated | 1 | `WITNESS_SELFTEST: 50/51 pass` | `VERDICT: FAIL` | empty |
| Restored | 0 | `WITNESS_SELFTEST: 51/51 pass` | `VERDICT: PASS` | empty |

The **only** failed check in the raw mutant output was:

```text
  check fixture commit pins hooks off                FAIL
```

The init/add pin checks and the remaining 48 checks were `ok`; the private-root removal check was also `ok`. The selftest completed its full 51-case denominator. This excludes syntax, import, setup, timeout, and unrelated-assertion explanations for this kill. Failure aggregation is at `tools/bash-witness-study.py:1231-1238,1711-1716` at the pinned revision.

Calibration detail: the counter's `fail_lines` field also includes `check FAIL without denominator is inconclusive, not a crash ok`, even in the pristine control. This is a **passing case whose name contains FAIL**, captured by the lexical filter at `c1-survivors.py:53`; it is not a failed assertion. The mutant's `VERDICT: FAIL` entry is the final summary, not a second failing case. Full raw output makes the distinction explicit.

# Restoration evidence

| Phase | Source SHA-256 |
|---|---|
| Before / pinned Git blob | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| MB10 | `aaf630a29d156e39dd279e70ba4d209165593d7b761391375517c4c7b6fcb5cd` |
| Restored | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |

The restored private file was byte-equal to both its pristine bytes and `git show 790abd2129f153c13b471e381d454186edbde65e:tools/bash-witness-study.py`. The restored detector exited 0. Pristine and restored stdout were byte-equal, SHA-256 `1755081d09ccdb98f4dbb2627883cc9b2ab0f58c833663ca293acb7873ddbdf1`; mutant stdout SHA-256 was `1b02135db3c918d0ce6d2e131974e00123c08d980b22f923910890f703935eca`. All three stderr streams were empty (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). The supplemental pristine and mutant output hashes also match the frozen counter's receipt.

Raw replay evidence:

- `.ufo/waves/round-21/w2/mutations/MB10-restoration.json`
- `.ufo/waves/round-21/w2/mutations/MB10.pristine.stdout.txt` and `.stderr.txt`
- `.ufo/waves/round-21/w2/mutations/MB10.mutated.stdout.txt` and `.stderr.txt`
- `.ufo/waves/round-21/w2/mutations/MB10.restored.stdout.txt` and `.stderr.txt`

# Agreement, limits, verdict

**Agreement:** the frozen instrument's `KILLED` result is supported by a green control, exact single anchor, one intended runtime-argv assertion, full-denominator completion, matching hashes, and a green byte-restored replay. Verdict: **genuinely discriminated**, not incidental or inconclusive, for the explicit per-invocation hook-disable contract.

**Limit:** no malicious hook was planted or observed executing. `wraps=subprocess.run` lets real Git execute, but the discriminator observes constructed argv, not an adversarial hook's effect. The isolated benign fixture's commit succeeds with or without the removed option; the explicit pin assertion is what distinguishes them. The source itself marks these as command-pin contracts at lines 1298-1299. Therefore this result does not establish a hostile-hook execution kill or broader exploit resistance. The environment-pin checks passed, but they were not this mutant's discriminator. Registry PID identity/race claims are outside this assigned MB10 probe and were not tested.

No disagreement with the narrow C1 classification; disagreement with any broader characterization as demonstrated malicious-hook execution prevention. No tools were installed or updated. No full battery, build, lint, formatter, or additional mutation was run.

Report: `.ufo/waves/round-21/w2/KillMB10.md`
