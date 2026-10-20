# Round 18 W1 — descendant-kill safety review

Axes: **depth** and **calibration**; operability is monitored, not scored.

## Severity and verdict

**High — timeout containment can fail open, hang the checker, or signal an unrelated same-user process after PID reuse.** The committed implementation does not meet contract C's detached-descendant requirement. A `/proc` walker is viable only with process-identity checks, strict row ownership, and bounded cleanup. Starttime revalidation plus pidfds substantially reduces signaling races, but neither binds a pidfd atomically to a prior `/proc` snapshot.

## Exploit path and evidence

Read committed source with:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 183f87b899e6cae46be98d251cbc87fb5118f6ca:tools/registry-check.py
```

**Exit 0.** At `tools/registry-check.py:306-324`, `_kill_group` looks up a PGID from the numeric `proc.pid`, sends TERM to that group, waits up to five seconds for the leader, then sends KILL to the group. `tools/registry-check.py:368-387` starts a new session, handles timeout by calling `_kill_group`, then calls unbounded `proc.communicate()`.

A registry row can fork a worker that calls `setsid()` (or otherwise leaves the original process group) and retains inherited stdout/stderr. At timeout, group signaling misses it; the subsequent `communicate()` waits for the worker to close the pipes, so the checker can remain stuck and the row's workload survives. If the row leader exits first while a descendant still holds a pipe, `_kill_group` can instead return at `os.getpgid(proc.pid)` with `ProcessLookupError`, and the unbounded `communicate()` still waits. The current selftest at `tools/registry-check.py:765-794` covers only a same-process-group grandchild; it does not falsify either path.

There is also a PID-reuse race in the current approach: after the row leader exits, `proc.pid` is only a number. If that PID is reused before `os.getpgid(proc.pid)`, the lookup can identify the new process's group and `killpg` can signal unrelated members permitted to the checker (commonly same-UID processes). A future `/proc` walk that signals a PID after only one start-time check retains a check-to-signal race.

**Impact:** timeout is not a bound on execution or return time; escaped work may mutate files after a row is declared timed out. A stale-PID/group lookup can terminate unrelated user work. Broadening cleanup to all processes sharing UID, session, or PGID would make that collateral-damage risk substantially worse.

## Smallest safe algorithm

1. Before starting any row, set `PR_SET_CHILD_SUBREAPER` in the checker and treat failure as inability to provide the declared cleanup guarantee (do not silently fall back to process-group-only cleanup). Run one row at a time. The checker is then the nearest subreaper for row orphans; an outer systemd/omp subreaper does not take those children while the checker is alive and marked. Capture the checker's existing direct-child identities before each row so pre-existing children are never mistaken for this row's adopted orphans.
2. Snapshot `/proc` process leaders and build a PPID graph rooted at the row process. Parse `/proc/<pid>/stat` by finding the **last** `)` in the parenthesized `comm`, then splitting the remainder: `ppid` is field 4 (remainder index 1), `starttime` is field 22 (remainder index 19), and state is field 3 (remainder index 0). Keep `(pid, starttime)` identities and ancestry, not UID, session, or process-group membership. Track new direct children adopted by the checker only while this single row is the active child-producing operation and only if they were absent from the pre-row baseline; use a dedicated per-row supervisor if the checker can have other concurrent children.
3. At timeout, take a fresh snapshot. For every candidate, re-read its stat and require the captured starttime to match and its current ancestry/row-adoption record still to place it in this row's owned set. Open a pidfd, re-read/validate starttime and scope after opening, and signal through `pidfd_send_signal`; never use a later numeric-PID `kill`. The pidfd pins the identity after it is opened, but a PID can be reused between discovery and `pidfd_open`, and field-22 starttime has clock-tick granularity. Thus this is a strong practical guard, not a proof against same-tick reuse.
4. Signal only those row-owned identities: TERM, bounded grace, resnapshot to catch children forked during shutdown, then KILL and repeat bounded sweeps until no live owned processes remain. Do not enumerate `/proc/<pid>/task/*` as processes: those are threads/TIDs; walk process leaders, signal the process identity once, and let process termination end its threads. Zombies cannot be killed; reap only known row-owned children (including adopted children), not arbitrary children with `waitpid(-1)`. Avoid an unbounded final `communicate()`; drain/close pipes under a bound and never report successful cleanup while owned live descendants remain.

For a strict guarantee against PID reuse (including same-tick reuse), or `CLONE_PARENT`/other parentage escape, use a per-row delegated cgroup established before exec, prevent rows from migrating out, and use `cgroup.kill`; if that boundary is unavailable, state the weaker guarantee rather than claiming race-free cleanup. The cgroup must contain only the row's work, not same-UID/session siblings.

## Required selftest cases

- **Escaped session + inherited pipe:** row forks a `setsid()` worker that holds stdout/stderr open and would create a marker later. Assert timeout returns within the configured timeout plus bounded cleanup, marker stays absent, and the worker identity is gone.
- **Exited leader / double fork:** row leader exits before timeout while a double-forked descendant holds a pipe. Assert subreaper adoption finds and kills the remaining row work and the checker does not hang.
- **Unrelated same-UID processes:** keep a same-UID sibling alive in another session (and, separately, one in the same session) while a row times out. Assert both survive while the row's escaped-session child is gone; assert no UID/session-wide signaling.
- **Outer subreaper:** run the checker under a synthetic helper that is itself a subreaper, with an unrelated helper-owned child. Have a row double-fork and `setsid()`. Assert the checker, as the nearer subreaper, cleans/reaps only that row's descendants; the outer helper's unrelated child remains alive. Do not use live systemd/omp processes as fixtures.
- **PID reuse / stale identity:** deterministic synthetic `/proc` snapshots or injected stat/pidfd wrappers change the candidate's starttime between snapshot and pre-signal validation. Assert no signal is sent to the replacement PID. Add an assertion that signal delivery uses the pidfd for the validated identity, not a later numeric-PID lookup.
- **Zombie and threads:** row creates a child that exits unreaped and a multithreaded worker. Assert the zombie is not treated as killable, row-owned adopted zombies are reaped, no unrelated child is reaped, and no TID is separately targeted.
- **Resnapshot during grace:** a row-owned child spawns another child after TERM. Assert the second sweep finds it and cleanup finishes boundedly.

## Checks performed

- Committed-source inspection command above: **exit 0**; relevant evidence is `tools/registry-check.py:306-324`, `:368-387`, and `:765-794`.
- No selftest or live-process experiment was run; this was a source review, and no process was created or signaled.

**Verdict: falls — committed timeout cleanup is process-group-only and cannot safely guarantee descendant cleanup or PID-reuse isolation.**