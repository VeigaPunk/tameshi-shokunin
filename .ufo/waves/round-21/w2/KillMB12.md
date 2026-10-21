done — MB12 genuinely discriminated; frozen C1 verdict KILLED.

# Scope and axes

- Item: C1 mutant **MB12**, `tools/bash-witness-study.py`, at `790abd2129f153c13b471e381d454186edbde65e`.
- **Operability:** execute the exact frozen detector with a green pristine control and exactly one mutation anchor.
- **Calibration:** distinguish the intended cleanup-postcondition failure from syntax/import/setup failure, unrelated checks, and source-hash/grep detection; demonstrate exact-byte restoration with the same detector.
- This is a dispatched author-side advisory probe, not outside admission, integration, shipping, or a numerical expertise increase. No other mutant was exercised.

# Mutant and expected detector

The frozen specification is `.ufo/evidence/round-21/c1-mutants.json:66-71`; its selftest command is at lines 122-125. Exactly one old anchor was observed.

```python
# tools/bash-witness-study.py:1707, original
        shutil.rmtree(private_root, ignore_errors=True)
# MB12
        shutil.rmtree(private_root / "missing", ignore_errors=True)
```

All owning-tool line references below are to revision `790abd2129f153c13b471e381d454186edbde65e`.

- Lines 1240-1248 create a real private root and its contained child.
- Lines 1702-1707 remove the child and then the private root in `finally`.
- **Line 1708:** `check("private root is removed", not private_root.exists())` is the intended discriminator. MB12 directs removal at a nonexistent child, so the real parent still exists at this observation point.
- Lines 1231-1238 count and print behavioral check results; lines 1711-1716 select the terminal verdict and exit from the failure count.
- Lines 1709-1710 provide an emergency `rmdir` after the check. Therefore the failure proves omission of the intended `finally` cleanup before that fallback, **not** a directory persisting after selftest completion. The mutant is not equivalent at the tested cleanup postcondition.

The owning check consults filesystem state, not source bytes. The ruler records source/output hashes for provenance; those hashes are not this kill's discriminator.

# Exact frozen command and output

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only MB12 --jobs 1 --json
```

Actual outer exit: **0**. Full, unmodified stdout JSON: `.ufo/waves/round-21/w2/mutations/MB12.json`; stderr: `mutations/MB12.stderr`; exit: `mutations/MB12.exit` (all relative to this report's directory).

Actual stderr:

```text
C1 MB12 tools/bash-witness-study.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

| Observation | Actual result |
|---|---|
| Frozen anchor count | 1 |
| Pristine owning selftest | exit 0, `VERDICT: PASS`, no timeout, 0.082 s |
| Mutated owning selftest | exit 1, `VERDICT: FAIL`, no timeout, 0.085 s |
| Frozen result | killed=1, survived=0, inconclusive=0, total=1 |

The ruler's relevant source is `.ufo/evidence/round-21/c1-survivors.py:38-57` (detector envelope/output capture), 106-130 (single anchor, control gate, mutation, verdict), and 139-150 (private clone cleanup/receipt). Its exercised bytes and the specification were also compared to the same files in the pinned private clone and matched:

```text
ruler SHA-256 a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396
spec  SHA-256 670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c
```

# Same-detector pristine / mutated / restored replay

The frozen command disposes of its own clones. To meet the restoration obligation and retain full raw selftest output, one additional private clone was created at `/tmp/tameshi-r21-KillMB12-d782amqt/fleet/tameshi-shokunin`, checked out detached at the assigned revision, with sibling symlinks beside it. Only line 1707 was changed, then restored, using anchored edits. The unchanged frozen module's `selftest` function was called in all three states:

```python
c1.selftest(w, private, "tools/bash-witness-study.py", ["selftest"])
```

Here `w=/tmp/tameshi-r21-KillMB12-d782amqt`. A wrapper around the module's subprocess-return helper only retained its returned stdout/stderr and argv; it did not change the subprocess or detector. Full expanded argv for all three calls is in `mutations/MB12-restoration.json:raw_runs`. The common command shape was:

```sh
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind "$w" "$w" --unshare-net --die-with-parent \
  --chdir "$w/fleet/tameshi-shokunin" \
  env -i "PATH=$PATH" "HOME=$w/home" "TMPDIR=$w/tmp" \
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C \
  python3 "$w/fleet/tameshi-shokunin/tools/bash-witness-study.py" selftest
```

The bwrap invocation's inherited environment had all `GIT_*` removed. Only the private scratch was writable over the read-only host bind; sibling symlinks therefore remained read-only to the selftest. Fixture Git configuration was pinned as shown above and by the owning fixture's calls at lines 1258-1275.

| Bytes | Actual exit | Actual summary | stderr | Runtime |
|---|---:|---|---|---:|
| Pristine | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | empty | 0.076 s |
| MB12 | 1 | `WITNESS_SELFTEST: 50/51 pass`; `VERDICT: FAIL` | empty | 0.074 s |
| Exact restored | 0 | `WITNESS_SELFTEST: 51/51 pass`; `VERDICT: PASS` | empty | 0.075 s |

All three runs completed without timeout. The **only failing case** was:

```text
  check private root is removed                      FAIL
```

Full raw outputs are `mutations/MB12-{pristine,mutated,restored}.{stdout,stderr}`. Output lines 1-50 were identical and successful in pristine and mutated runs. Only output line 51 (the cleanup check), line 52 (51/51 versus 50/51), and line 53 (verdict) differed. The replay pristine and mutant stdout hashes exactly match the frozen command's corresponding hashes. Restored stdout equals pristine stdout byte for byte.

This excludes syntax/import/setup failures and unrelated assertions: the mutant completed all 51 checks, reported exactly one failing cleanup case, printed the normal terminal summary, emitted no stderr, and returned the normal failure code.

# Calibration and scope limits

- **Agreement:** MB12 is genuinely behaviorally discriminated by the intended filesystem cleanup check. The frozen KILLED result is supported, not incidental or inconclusive.
- **Diagnostic disagreement:** the ruler's `fail_lines` heuristic at `c1-survivors.py:53` also captures `check FAIL without denominator is inconclusive, not a crash ok`. This is a **passing case name**, visible in all three raw outputs at line 30, not another failure. The heuristic's substring match must not be read as an assertion count. It does not alter this mutant's verdict.
- Nearby environment-pin cases at owning-tool lines 1283-1297 inspect the constructed environment returned by `git_clean_env` (implementation lines 333-339). Hook-pin cases at lines 1298-1311 observe the constructed Git argv while wrapped calls execute ordinary private fixture operations. Their source explicitly disclaims a reachable init/add hook under the scrubbed environment. The passed cases do **not** demonstrate malicious-hook execution, successful exploitation, or a hostile hook being blocked.
- The separate GIT_DIR/GIT_WORK_TREE canaries at lines 1321-1368 do exercise actual private fixture subprocess materialization/sweep behavior. They remained green here and are not MB12's discriminator.
- No registry identity detector was run. This item provides neither a synthetic PID-race result nor evidence of real PID reuse.
- No claim is made about exceptional cleanup paths not reached by this normal-completion mutant probe.

# Restoration evidence and containment

| State of `tools/bash-witness-study.py` | SHA-256 |
|---|---|
| Pinned pristine / scratch before | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Scratch MB12 | `c221aa9be73de675380545680f7237bce13f99bb1408ed4a033d67dc46df7b24` |
| Scratch restored | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |
| Production before and after | `60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9` |

Restored bytes were compared directly with the retained original bytes and were exactly equal before the restored detector ran. The restored detector passed. The restored scratch was subsequently removed; closeout observations are in `mutations/MB12-closeout.json`. Production tools/contracts/index/refs and siblings were not edited; only this report and MB12-named evidence were written in the lane. No tool installation/update, alternate runtime, full battery, build, lint, formatter, integration, or shipping was performed.

Report: .ufo/waves/round-21/w2/KillMB12.md
