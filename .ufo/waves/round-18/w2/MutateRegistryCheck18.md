# MutateRegistryCheck18 — round-18 registry-check mutation probe
## Scope and axes
- Read revision: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`. Source references below are to that immutable revision, not the changing live worktree.
- Axes: **depth** (single-point attacks on the new safeguards), **calibration** (distinguishing actual kills from surviving gaps), and **operability/no-harm** (bounded execution, isolated process trees, exact restoration). This seat reports detector evidence; it does not adjudicate the round.
- Owned scratch: `/tmp/tameshi-r18w2-MutateRegistryCheck18-vir_wgug`; initial checkout `/tmp/tameshi-r18w2-MutateRegistryCheck18-vir_wgug/fleet/tameshi-shokunin`. Twelve additional isolated clones are under `$W/probes/M01` through `$W/probes/M12`. Adjacent sibling repositories are read-only symlinks.
- Only this report was written in the live lane. No live/sibling source, Git index, jj state, registry, or fleet runtime was changed. No tool was installed or updated. No subagents, background jobs, or other runtime were invoked. Detector subprocesses were joined in batches of at most four.
## Result
**12 single-point mutants: 9 KILLED, 3 SURVIVED, 0 INCONCLUSIVE.** Every exact `@old` anchor had count 1 before editing. Each mutant had its own pristine and restored control using the identical command/path: all 24 controls exited 0 with `SELFTEST: PASS (46 cases)`. An additional initial-clone control also passed. All 37 detector invocations completed within the 55-second supervisor bound; no supervisor timeout occurred. All detector stderr streams were empty.
## Commands and containment
Checkout creation executed with all inherited `GIT_*` removed from the parent environment and explicit `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`. Initial clone and detached checkout both exited 0:
```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r18w2-MutateRegistryCheck18-vir_wgug/fleet/tameshi-shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR git -C /tmp/tameshi-r18w2-MutateRegistryCheck18-vir_wgug/fleet/tameshi-shokunin checkout -q --detach 01d586ddbc5fcd78659557c4e93a6ee8517b87d1
```
Per-probe clones used `git clone -q --shared "$C" "$D"`, followed by `git -C "$D" checkout -q --detach 01d586ddbc5fcd78659557c4e93a6ee8517b87d1`, with the same scrubbed environment and cwd inside `$W`. All 24 setup commands exited 0. Their expanded argv are retained in the raw receipt.
The following is the detector command shape actually executed, with `D` expanded to the clone listed in the control table. The exact same expanded argv/cwd was used for pristine, mutated, and restored bytes of each ID. Python `subprocess.run(..., capture_output=True, text=True, timeout=55)` imposed the outer bound. The extra PID namespace contains wrong-anchor signal mutants and makes namespace teardown dispose of any mutant survivor; the fleet remains read-only, and the network is unshared.
```sh
W=/tmp/tameshi-r18w2-MutateRegistryCheck18-vir_wgug
D="$W/probes/M01/fleet/tameshi-shokunin"  # substitute the table ID
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  bwrap --ro-bind / / --dev /dev --unshare-pid --proc /proc \
  --tmpfs /tmp --bind "$W" "$W" --unshare-net --die-with-parent \
  --chdir "$D" env -i PATH=/usr/bin:/bin HOME="$W/home" TMPDIR="$W/tmp" \
  GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C \
  /usr/bin/python3 "$D/tools/registry-check.py" --selftest
```
## Controls and exit evidence
For every row, `D=$W/probes/<ID>/fleet/tameshi-shokunin`. Both control columns printed exactly `SELFTEST: PASS (46 cases)`. Mutation case failures are reproduced below; elapsed times are observed wall seconds.
| ID | Pristine exit / seconds | Mutated exit / seconds | Restored exit / seconds | Verdict |
|---|---|---|---|---|
| M01 | 0 / 5.570 | 1 / 5.581 | 0 / 5.528 | KILLED |
| M02 | 0 / 5.568 | 0 / 5.565 | 0 / 5.526 | SURVIVED |
| M03 | 0 / 5.559 | 1 / 5.564 | 0 / 5.525 | KILLED |
| M04 | 0 / 5.554 | 1 / 5.564 | 0 / 5.525 | KILLED |
| M05 | 0 / 5.508 | 0 / 5.546 | 0 / 5.526 | SURVIVED |
| M06 | 0 / 5.524 | 1 / 5.549 | 0 / 5.516 | KILLED |
| M07 | 0 / 5.496 | 0 / 5.550 | 0 / 5.513 | SURVIVED |
| M08 | 0 / 5.512 | 1 / 11.333 | 0 / 5.514 | KILLED |
| M09 | 0 / 5.532 | 1 / 5.550 | 0 / 5.498 | KILLED |
| M10 | 0 / 5.548 | 1 / 5.549 | 0 / 5.495 | KILLED |
| M11 | 0 / 5.543 | 1 / 5.555 | 0 / 5.502 | KILLED |
| M12 | 0 / 5.537 | 1 / 5.515 | 0 / 5.490 | KILLED |

## Mutants, expected detectors, and actual output
Only the indicated behavior-bearing line/call was changed. Multiline `@old` text on M06/M07/M12 is a uniqueness anchor, not an additional change. Each mutant started from pristine bytes, never from another mutant.

### M01 — remove-finite-timeout-guard — KILLED

- Point: `tools/registry-check.py:240`; `@old count == 1`; anchor begins at line 240.
- Expected detector before execution: timeout-overflow. For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
                timeout_valid = math.isfinite(ts) and ts > 0
@new
                timeout_valid = ts > 0
```
Observed owning `--selftest` exit: **1**; stderr empty.

```text
SELFTEST_CASE timeout-overflow FAIL (exit=1)
SELFTEST: FAIL (1 of 46 cases: timeout-overflow)
```

### M02 — accept-zero-timeout-boundary — SURVIVED

- Point: `tools/registry-check.py:240`; `@old count == 1`; anchor begins at line 240.
- Expected detector before execution: timeout-zero (no named case observed). For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
                timeout_valid = math.isfinite(ts) and ts > 0
@new
                timeout_valid = math.isfinite(ts) and ts >= 0
```
Observed owning `--selftest` exit: **0**; stderr empty.

```text
SELFTEST: PASS (46 cases)
```

### M03 — remove-json-parse-constant — KILLED

- Point: `tools/registry-check.py:349`; `@old count == 1`; anchor begins at line 349.
- Expected detector before execution: timeout-nan, timeout-infinity, timeout-negative-infinity. For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
        data = json.loads(text, parse_constant=_reject_json_constant)
@new
        data = json.loads(text)
```
Observed owning `--selftest` exit: **1**; stderr empty.

```text
SELFTEST_CASE timeout-nan FAIL (exit=2)
SELFTEST_CASE timeout-infinity FAIL (exit=2)
SELFTEST_CASE timeout-negative-infinity FAIL (exit=2)
SELFTEST: FAIL (3 of 46 cases: timeout-nan, timeout-infinity, timeout-negative-infinity)
```

### M04 — disable-linux-child-subreaper — KILLED

- Point: `tools/registry-check.py:406`; `@old count == 1`; anchor begins at line 406.
- Expected detector before execution: normal-exit-kills-double-fork. For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
    if prctl(CHILD_SUBREAPER_PRCTL, 1, 0, 0, 0) != 0:
@new
    if prctl(CHILD_SUBREAPER_PRCTL, 0, 0, 0, 0) != 0:
```
Observed owning `--selftest` exit: **1**; stderr empty.

```text
SELFTEST_CASE normal-exit-kills-double-fork FAIL (exit=0 survivor=True)
SELFTEST: FAIL (1 of 46 cases: normal-exit-kills-double-fork)
```

### M05 — remove-baseline-child-exclusion — SURVIVED

- Point: `tools/registry-check.py:480`; `@old count == 1`; anchor begins at line 480.
- Expected detector before execution: unrelated/pre-existing-child preservation (no named case observed). For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
            return (current, observed_starttime) not in baseline_children
@new
            return True
```
Observed owning `--selftest` exit: **0**; stderr empty.

```text
SELFTEST: PASS (46 cases)
```

### M06 — remove-post-pidfd-starttime-check — KILLED

- Point: `tools/registry-check.py:510`; `@old count == 1`; anchor begins at line 509.
- Expected detector before execution: pidfd-revalidates-starttime. For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
        stat = read_stat(pid)
        if stat is None or stat[1] != starttime or not in_row_scope():
@new
        stat = read_stat(pid)
        if stat is None or not in_row_scope():
```
Observed owning `--selftest` exit: **1**; stderr empty.

```text
SELFTEST_CASE pidfd-revalidates-starttime FAIL (stale_identity_rejected=False signals=1)
SELFTEST: FAIL (1 of 46 cases: pidfd-revalidates-starttime)
```

### M07 — remove-post-pidfd-ancestry-check — SURVIVED

- Point: `tools/registry-check.py:510`; `@old count == 1`; anchor begins at line 509.
- Expected detector before execution: post-pidfd ownership-change rejection (no named case observed). For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
        stat = read_stat(pid)
        if stat is None or stat[1] != starttime or not in_row_scope():
@new
        stat = read_stat(pid)
        if stat is None or stat[1] != starttime:
```
Observed owning `--selftest` exit: **0**; stderr empty.

```text
SELFTEST: PASS (46 cases)
```

### M08 — wrong-pidfd-send-anchor — KILLED

- Point: `tools/registry-check.py:512`; `@old count == 1`; anchor begins at line 512.
- Expected detector before execution: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe, normal-exit-kills-double-fork, pidfd-revalidates-starttime. For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
        signal.pidfd_send_signal(pidfd, signum)
@new
        signal.pidfd_send_signal(pid, signum)
```
Observed owning `--selftest` exit: **1**; stderr empty.

```text
SELFTEST_CASE timeout-kills-setsid-pipe FAIL (exit=1 elapsed=2.733s survivor=True marker=False)
SELFTEST_CASE timeout-kills-setpgid-pipe FAIL (exit=1 elapsed=2.737s survivor=True marker=False)
SELFTEST_CASE normal-exit-kills-double-fork FAIL (exit=1 survivor=True)
SELFTEST: FAIL (3 of 46 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe, normal-exit-kills-double-fork)
```

### M09 — remove-communicate-drain-bound — KILLED

- Point: `tools/registry-check.py:608`; `@old count == 1`; anchor begins at line 608.
- Expected detector before execution: bounded-pipe-drain. For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
        return proc.communicate(timeout=PIPE_DRAIN_TIMEOUT_S)
@new
        return proc.communicate(timeout=None)
```
Observed owning `--selftest` exit: **1**; stderr empty.

```text
SELFTEST_CASE bounded-pipe-drain FAIL (communicate_timeout=None wait_timeout=None)
SELFTEST: FAIL (1 of 46 cases: bounded-pipe-drain)
```

### M10 — remove-wait-drain-bound — KILLED

- Point: `tools/registry-check.py:619`; `@old count == 1`; anchor begins at line 619.
- Expected detector before execution: bounded-pipe-drain. For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
            proc.wait(timeout=PIPE_DRAIN_TIMEOUT_S)
@new
            proc.wait(timeout=None)
```
Observed owning `--selftest` exit: **1**; stderr empty.

```text
SELFTEST_CASE bounded-pipe-drain FAIL (communicate_timeout=0.5 wait_timeout=None)
SELFTEST: FAIL (1 of 46 cases: bounded-pipe-drain)
```

### M11 — omit-stderr-pipe-close — KILLED

- Point: `tools/registry-check.py:615`; `@old count == 1`; anchor begins at line 615.
- Expected detector before execution: bounded-pipe-drain. For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
        for stream in (proc.stdout, proc.stderr):
@new
        for stream in (proc.stdout,):
```
Observed owning `--selftest` exit: **1**; stderr empty.

```text
SELFTEST_CASE bounded-pipe-drain FAIL (communicate_timeout=0.5 wait_timeout=0.5)
SELFTEST: FAIL (1 of 46 cases: bounded-pipe-drain)
```

### M12 — skip-normal-exit-daemon-cleanup — KILLED

- Point: `tools/registry-check.py:707`; `@old count == 1`; anchor begins at line 705.
- Expected detector before execution: normal-exit-kills-double-fork. For absent-case expectations, this denotes the required discriminator, not an invented existing case.
```text
@old
    else:
        got = proc.returncode
        cleanup_ok = _cleanup_row(
            proc, baseline_children, proc_starttime
        )
@new
    else:
        got = proc.returncode
        cleanup_ok = True
```
Observed owning `--selftest` exit: **1**; stderr empty.

```text
SELFTEST_CASE normal-exit-kills-double-fork FAIL (exit=0 survivor=True)
SELFTEST: FAIL (1 of 46 cases: normal-exit-kills-double-fork)
```

## Named survivor coverage gaps — routed, not patched
Routing destination for each finding is **TameshiR18, owning `tools/registry-check.py --selftest` fixture work**. This scoped report is the route; no blocker message or unauthorized state-file edit was needed. These survivors do not authorize weakening the positive-finite-timeout or row-identity contracts.
1. **R18-RC-ZERO-BOUNDARY (M02).** At `tools/registry-check.py:240`, changing `> 0` to `>= 0` retained all 46 passes. The timeout fixture list at `tools/registry-check.py:1490-1497` covers NaN, infinities, overflow, and a boolean, but not zero. [INFERENCE] A zero-valued timeout reaches execution instead of the required validation exit 2. Discriminator to route: registry containing `timeout_s: 0`, require exit 2 plus row identity and `finite positive number`; a side-effect canary must remain untouched.
2. **R18-RC-BASELINE-CHILD-EXCLUSION (M05).** At `tools/registry-check.py:480`, unconditional ownership of a checker child retained all 46 passes. This removes the exclusion for identities captured by `_direct_child_identities` at `tools/registry-check.py:449-458`. [INFERENCE] A pre-existing checker child or its subtree can be signalled/reaped as row-owned. Discriminator to route: an existing unrelated direct child (and descendant), with recorded PID/start time in `baseline_children`, must remain unowned/alive while a new row is cleaned up. Test the ownership function and preservation through actual cleanup in the isolated fixture.
3. **R18-RC-POST-PIDFD-OWNERSHIP (M07).** At `tools/registry-check.py:510`, removing only the second `in_row_scope()` check retained all 46 passes. The existing unit case at `tools/registry-check.py:1554-1576` changes start time but supplies `lambda: True` for ownership. [INFERENCE] Stable PID/start time with ownership changing between initial validation and the pidfd-open/recheck window can receive a signal. Discriminator to route: constant matching stat identity, fake pidfd, and ownership results `True` then `False`; require a false return and no signal, with descriptor closed.
### Calibration notes
- M03 was killed by diagnostics: child validation still exited 2 after removing `parse_constant`, but all three cases lost the required `non-finite JSON number` expectation. This is not evidence that those timeout values executed; the remaining finite-number guard rejected them.
- M08 was killed by the three real descendant-cleanup cases. The preregistered expectation also named `pidfd-revalidates-starttime`; that case did **not** fail, because its stale identity is rejected before the send call. This distinction is retained rather than inflating the failing-case set.
- M09/M10/M11 were killed by the existing `FakeTimedProcess`/`FakePipe` assertions at `tools/registry-check.py:1515-1552`. These are genuine detector kills but not a fresh real-world pipe-latency measurement.
- All conclusions are bounded to this selftest, these twelve mutations, and the stated PID-namespace envelope. No claim is made about UID changes, same-tick PID reuse, other mutational combinations, or overall round acceptance.
## Before / mutant / restored hashes
Let **B** = `e072fd3995ca1df1477613f009193e20f3797bc4673ee3045a04afb9927c2899` (SHA-256 of the exact pristine `tools/registry-check.py` bytes). Every row has before=B and restored=B; direct byte equality against the saved pristine bytes was also true for all twelve restored files. The original initial-clone file was never mutated and still has B.

| ID | Before SHA-256 | Mutant SHA-256 | Restored SHA-256 / exact equality |
|---|---|---|---|
| M01 | B | `f7934673c58c651323a14b2f0debe78674631bc34b9d29aaa1343c2a1c767e28` | B / true |
| M02 | B | `11527aa962ccab9769d92f49536ad7434759f39332145d71935fead4282bef38` | B / true |
| M03 | B | `f0ac69c54ff08dfe868bc28937d096d102dbffd1fc492ecf7900a7d14ea124b0` | B / true |
| M04 | B | `ad6a345de97cb1233ce1528c6a1704637767179c171e923bee2b7645caf3af43` | B / true |
| M05 | B | `ea38b22e36db764f86498621cb2e4dc8cc04faadb957a38f3140982417eabb76` | B / true |
| M06 | B | `76f2c83ba4830e7b088a854ad9423ee53cee2af0f3dd9b09d456d982ae6b95c5` | B / true |
| M07 | B | `50f400e7831dfc9fd48d0b959c418900642aab9e5c22528d5f1057e442f10b95` | B / true |
| M08 | B | `70c80baa3ab63019698bc559880d6aab855236f2c052a8ea7995efcfc3e26745` | B / true |
| M09 | B | `4b10f8f05d00e177eceb481346aebbaf8a76eaa15c9bd847148744c3b02bc030` | B / true |
| M10 | B | `5cfe899363656626b159495f13a6c1797d13d5a1d8d098dbe96e53be7988c110` | B / true |
| M11 | B | `7d861d454faede904da1d6a71679ed07b55a1333da89ee6a86261cac6417856f` | B / true |
| M12 | B | `552b1788ceb1b20b143de76f93328192e9c7a4177ef9297f8709485c3578fb78` | B / true |

Each mutated run recorded the observed on-disk mutant hash and matched the planned single replacement. Restoration used inverse surgical edits, returned every snapshot to the pristine tag, then passed the identical bounded behavioral detector. No mutant source remains.
## Retained raw evidence
- Raw JSON receipt: `/tmp/tameshi-r18w2-MutateRegistryCheck18-vir_wgug/registry-check-mutation-receipts.json`.
- Receipt SHA-256: `e26b15ae5dccb5bb78df8bc40ab8f57eded91b7e633af5d49f6f5209e566eaf5`.
- The receipt retains every exact argv, cwd, phase, exit, elapsed time, full stdout/stderr, `@old` count/recipe, and source hash for the initial control and all 36 per-mutant detector runs. The report embeds the decisive outputs so the findings do not depend on indefinite `/tmp` retention.

partial — 9/12 mutants KILLED; 3 named coverage gaps SURVIVED; all pristine/restored controls passed and exact source bytes were restored.
