# S10 — subprocess-timeout escape sweep (round 18, wave 1)

Base rev `183f87b899e6cae46be98d251cbc87fb5118f6ca` (detached clone in a /tmp fleet
mirror; every command below ran in /tmp, no lane process was started). Host:
Linux 7.2.11, GNU coreutils 9.12 (`/usr/bin/timeout`), Python 3.14.8.

## Answer

**Every timed kill in the lane is escapable.** A descendant that calls `setsid()`
survives all of them; for the Python `subprocess.run(timeout=)` sites even a plain
background child survives (setsid not required), because `run()` SIGKILLs only the
direct child and then `wait()`s (POSIX path — no group kill, no pipe hang). Two
`killpg` sites (`registry-check.py`) are additionally escaped by a mere
`setpgid(0,0)`. Double-forking *without* a new session keeps the pgid and is killed —
except in `registry-check`'s no-kill path, where a row that exits before its
`timeout_s` leaves any daemonized child alive while reporting the row `held`.

One `setsid` child does not only survive: `registry-check.py:387` then calls
`proc.communicate()` **with no timeout**, so an escapee that inherited the row's
pipes holds the monitor open past `timeout_s` (measured 6037 ms for `timeout_s: 1`).

## Method

- Mechanism probes with `/usr/bin/timeout` (GNU 9.12): `/usr/bin/timeout 1 bash -c …`.
- Real tools from the clone: `tools/registry-check.py --root <tmp> --registry <tmp>`,
  `tools/mutate-and-run.sh --target … --defects … --suite … --timeout 1`,
  `tools/evidence-disposition.py`/`tools/pin-disposition.py` imported as modules with
  a `git` PATH shim.
- Note for reproducibility: the omp persistent shell exposes a **builtin** `timeout`
  (clap-style usage) that shadows `/usr/bin/timeout` for interactive one-liners. A
  child bash has no such builtin, so lane scripts resolve `/usr/bin/timeout`; all
  numbers here were re-taken with the explicit `/usr/bin/timeout` after discovering
  the shadow (first-pass builtin numbers agreed, but are not cited).
- No `lsp` device is mounted in this seat. The call inventory is a Python `ast` walk
  over every `tools/*.py` (all `subprocess.*` calls, line numbers, `timeout=` keyword
  presence) plus direct reads of the enclosing functions — not literal grep evidence.

## Site inventory (lane `tools/` only; no `scripts/` exists at this rev)

| # | Site (path:line) | Kill mechanism | setsid escape | other escape | Exposure |
|---|---|---|---|---|---|
| 1 | `tools/registry-check.py:306-322` `_kill_group` used by `run_row` (`Popen` 368, `start_new_session` 375, `communicate` 383) | `killpg(pgid, TERM)`, `proc.wait(5)`, `killpg(pgid, KILL)` | **yes** | `setpgid(0,0)` also escapes; row that exits first leaves daemons (no kill at all) | production gate |
| 2 | `tools/registry-check.py:387` post-timeout `proc.communicate()` (no timeout) | — | **yes** (pipe-holder hangs the monitor) | — | production gate |
| 3 | `tools/mutate-and-run.sh:439-444` `run_one`, `timeout "$TIMEOUT_S"` at 443 | GNU `timeout` process-group TERM (no `--kill-after`) | **yes** | TERM-ignoring suite stretches the run past `--timeout` (no KILL fallback) | production sweep/regression |
| 4 | `tools/mutate-and-run.sh:1110` regression leg re-execs `"$SELF"` | inherits #3 | **yes** | same | production `--regression` (C1 leg 8) |
| 5 | `tools/evidence-disposition.py:386-399` `git_call` (`subprocess.run`, timeout 389/393) | SIGKILL direct child only | **yes** | plain background child survives too; no hang | production evidence read |
| 6 | `tools/pin-disposition.py:224-243` `git_run` (timeout 227) | SIGKILL direct child only | **yes** | same | production |
| 7 | `.ufo/evidence/round-17/coldread/trace-inputs.py:520-524` `git_run` (timeout 522) | SIGKILL direct child only | **yes** (shared mechanism) | same; this file is contract B's promotion source | production (to be promoted) |
| 8 | selftest-only timed `run()` sites: `evidence-disposition.py:1916,1930,2102,2756`; `pin-disposition.py:770,931`; `context-capture.py:1647`; `witness-metadata.py:1133`; `registry-check.py:602,651`; `repeat-control.py:612,646`; `trace-inputs.py:757,798` | SIGKILL direct child only | **yes** | same | fixtures leak descendants (≤60/120 s) |
| 9 | **no timeout at all**: `registry-check.py:411,451,465,476` (rev-parse/clone/checkout/HEAD); `bash-witness-study.py:337` (`materialize_target`), `:604` (`run_sweep`); `repeat-control.py:281` (`run_once`, documented at 84-89); `trace-inputs.py:565` (`probe_flags`), `:633` (`strace` run); `mutate-and-run.sh:257-268` `git_clean` | none | moot — nothing ever kills | a hung child hangs the whole gate; a setsid child also outlives any external kill | production |

Findings 7/8/9 are shared-mechanism readings plus the demos below; not every row was
executed individually (marked [INFERENCE] where extrapolated).

## Demos and observed output

### D1 — GNU `timeout` signals the process group, but not a new session

```
/usr/bin/timeout 1 bash -c 'bash -c "exec -a tameshi_g1a sleep 8" & sleep 5'
  -> rc=124; no survivor                      (plain background grandchild: killed)
/usr/bin/timeout 1 bash -c 'setsid bash -c "exec -a tameshi_g1b sleep 8" & sleep 5'
  -> rc=124; pgrep: 2603727 tameshi_g1b 8     (setsid: SURVIVES)
/usr/bin/timeout 1 bash -c '( bash -c "exec -a tameshi_g1c sleep 8" & ) ; sleep 5'
  -> rc=124; no survivor                      (double-fork, same pgid: killed)
```

### D2 — `--timeout` is not a wall bound; `--kill-after` fixes only half

```
/usr/bin/timeout 1 bash -c 'trap "" TERM; sleep 3'
  -> rc=124 elapsed_ms=3002                   (waits for the TERM-ignoring child; 30 s child = 30 s hold)
/usr/bin/timeout -k 1 1 bash -c 'trap "" TERM; sleep 30'
  -> rc=137 elapsed_ms=2001                   (kill-after bounds the ignore)
/usr/bin/timeout -k 1 1 bash -c 'trap "" TERM; setsid bash -c "exec -a tameshi_k2 sleep 8" & sleep 30'
  -> rc=137 elapsed_ms=2001; pgrep: 3092452 tameshi_k2 8   (setsid still survives)
```

### D3 — real `mutate-and-run.sh` suite run (`--timeout 1`)

```
bash tools/mutate-and-run.sh --target mr/target.sh --defects mr/spec.spec \
  --suite 'if grep -qF -- "- $2" "$MUTANT"; then trap "" TERM; setsid bash -c "exec -a tameshi_mr_escape sleep 8" & sleep 4; fi' \
  --workdir mr/run --label demo --timeout 1
-> CONTROL: GREEN (exit=0 duration-ms=2 ...)
-> DEFECT K: INCONCLUSIVE (exit=124 note=timeout duration-ms=4002) escaped suite descendant
-> MUTATE: DEGRADED (target=demo defects=1 killed=0 survived=0 inconclusive=1 kill-rate=0%)
tool exit=1, wall 4044 ms (not 1 s); pgrep: 2342265 tameshi_mr_escape 8
```
Two facts in one run: a TERM-ignoring suite stretches the "timeout" 4×, and the
`setsid` descendant outlives the whole sweep. Regression legs (`:1110`) re-enter the
same `run_one`, so C1 leg 8 inherits this.

### D4 — real `registry-check.py`, `timeout_s: 1`

Row A (setsid + devnull + row sleeps 20):
```
python3 tools/registry-check.py --root rc/lane --registry rc/regA.json
-> ROW escape-row expect=0 got=timeout differs
-> REGISTRY_CHECK: held=0/1 superseded=0
exit=1 elapsed_ms=1028; pgrep: 2387199 tameshi_rc_escape 20   (P10 OPEN)
```
Row B (setsid, inherits the row's pipes):
```
-> ROW pipe-escape-row expect=0 got=timeout differs
exit=1 elapsed_ms=6037   (timeout_s=1; blocked in the no-timeout communicate at :387)
```
Row C (`setpgid(0,0)` instead of setsid):
```
-> ROW setpgid-escape expect=0 got=timeout differs
exit=1 elapsed_ms=1027; pgrep: 2760613 … os.setpgid(0,0) … time.sleep(20)   (escaped)
```
Row D (daemon-and-exit, plain child with devnull, row exits in 0.1 s):
```
-> ROW daemon-and-exit expect=0 got=0 held
-> REGISTRY_CHECK: held=1/1 superseded=0
exit=0 elapsed_ms=139; pgrep: 2707845 tameshi_rc_daemon 6   (no timeout -> no kill path)
```
Row E (daemon-and-exit holding pipes, writes a marker at 3 s):
```
-> ROW daemon-pipe-exit expect=0 got=timeout differs
exit=1 elapsed_ms=1025; marker_exists=no     (same-pgid daemon WAS group-killed at timeout)
```
Baseline guard quality: `registry-check.py --selftest` → exit 0,
`SELFTEST: PASS (34 cases)`, including `SELFTEST_CASE timeout-kills-group PASS`.
The case's grandchild (`:765-780`) never changes pgid, so the escape is invisible to
the tool's own falsifier. `mutate-and-run.sh --selftest` → exit 0,
`MUTATE_SELFTEST: 95/95 pass`; its hang fixture is a plain `sleep 30`, same blind spot.

### D5 — Python 3.14.8 `subprocess.run(timeout=1)` primitive

```
PY-plain  TimeoutExpired elapsed_ms=1001  survivor_plain=True    (no setsid needed)
PY-setsid TimeoutExpired elapsed_ms=1000  survivor_setsid=True
PY-pipe   TimeoutExpired elapsed_ms=1000  survivor_pipe=True     (no post-kill hang: run() waits)
```
POSIX `run()` does `process.kill(); process.wait()` after `TimeoutExpired` — it never
signals the group and never blocks on the inherited pipe.

### D6 — the two production git helpers, with a `git` PATH shim that setsids

```
# shim: setsid bash -c 'exec -a tameshi_git_escape sleep 8' & sleep 6
ed.git_call(lane, ["status"], timeout=1)
-> git_call raised CouldNotEvaluate after 1001ms; survivor_git_escape=True
pd.GIT_TIMEOUT = 1; pd.git_run(lane, ["status"])
-> git_run reason=git_timeout elapsed_ms=1001; survivor_git_escape=True
```

## What this means for the round's contracts

- **C (registry-check)**: the required descendant kill is not cosmetic. The current
  `killpg` guard is bypassed by `setsid` **and** `setpgid(0,0)` (D4 A/C), and the
  post-timeout `communicate()` is itself unbounded (D4 B). A `PR_SET_CHILD_SUBREAPER`
  + `/proc` descendant walk must run after the group kill **and** the second
  `communicate()` must be bounded (close the pipes or give it a deadline), otherwise
  an escaped pipe-holder still hangs the gate. A selftest case for P10 must spawn
  `setsid` (and should also assert the monitor returns within a small multiple of
  `timeout_s`); the existing `group-row` fixture does neither.
- **C/mutate-and-run**: `timeout` can only kill the monitored process group. No
  `timeout` flag catches a `setsid` suite; `--kill-after` fixes the TERM-ignore hold
  (D2) but not the escape (K2). The runner needs a subreaper/cgroup wrapper if suite
  descendants are in scope; at minimum add `--kill-after` so `--timeout` is a wall
  bound. Regression legs inherit the same behaviour via `:1110`.
- **B/D/E git helpers**: `subprocess.run(timeout=)` gives a bound on the *direct*
  child only; a git child that spawns a credential helper / filter / hook descendant
  that setsids (or merely backgrounds) is left running. Low likelihood for the
  read-only git argv used today (`show`, `rev-parse`, `ls-tree`, `cat-file`,
  `merge-base`), but the bound is not what the sites appear to promise.
- **No-timeout sites** (table row 9) are outside the escape question but are the
  weaker operability edge: a hung `git`/`strace`/`run_once` has no bound at all, and
  `bash-witness-study.py:604` wraps a runner whose own suite timeout can be stretched
  by D2.

## Remaining unknowns

- I did not audit sibling-repo or kumitate suites; only the lane's `tools/`.
- I did not execute every selftest-only site individually (shared `run()` mechanism,
  [INFERENCE] from D5); none of them guards a shipped artefact.
- The live `tools/registry.json` (29 rows) contains no `setsid`/`Popen`/background
  argv, so the registry-check escape is latent, not currently triggered by any row.
- Whether the fix should also adopt a pid-namespace/cgroup wrapper is a design call
  outside this sweep.

verdict: falls — every lane timeout is escaped by a setsid (and the killpg sites by setpgid) descendant; registry-check additionally hangs past timeout_s on an escaped pipe-holder, and mutate-and-run's --timeout is stretched by a TERM-ignoring suite.
