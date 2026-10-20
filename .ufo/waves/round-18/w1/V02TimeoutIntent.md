# `registry-check.py` timeout/process-group reconstruction

Pinned target: `183f87b899e6cae46be98d251cbc87fb5118f6ca`.

## Axes

- **Depth:** distinguish session/group escape, orphaning, stop state, and signal-permission failures.
- **Calibration:** separate source/test-fixture facts from OS-behavior inference; do not imply an unrun timeout test passed.
- **Operability:** determine whether the configured row timeout also bounds cleanup.

## Evidence and provenance

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 183f87b899e6cae46be98d251cbc87fb5118f6ca:tools/registry-check.py` — exit **0**; pinned source emitted. The same pinned bytes were checked out in `/tmp/tameshi-r18w1-V02TimeoutIntent-sYkIgL/fleet/tameshi-shokunin` (clone and checkout exit **0**) to read exact source lines.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 183f87b899e6cae46be98d251cbc87fb5118f6ca:corpus/lessons/round-17-verifier-spotcheck.md` — exit **0**; pinned §7 emitted.
- I did **not** run `registry-check.py` or another runtime. The process outcomes below are source-based Linux process-semantics inferences, not fresh observations. No LSP device was mounted; source definitions and fixture were read from the pinned file rather than treating grep as semantic proof.

## Existing contract and divergence

`run_row` starts the registered argv with stdin at `/dev/null`, stdout/stderr pipes, the lane cwd and scrubbed row environment, and `start_new_session=True` (`tools/registry-check.py:366-376`). **[INFERENCE]** The launched row process is therefore the new session/process-group leader; ordinary descendants inherit its process group. This isolates normal rows from the monitor's group and lets cleanup target that row group.

On timeout, `communicate(timeout=timeout_s)` raises and the code calls `_kill_group`, then calls `communicate()` again with **no timeout** (`tools/registry-check.py:382-393`). Cleanup discovers the group with `getpgid(proc.pid)`, sends `SIGTERM`, waits up to five seconds for only the direct `Popen` process, then sends `SIGKILL` to the saved group ID (`:306-323`). Thus the intended invariant is “row and ordinary same-group descendants are terminated”; the implementation assumes processes remain in that group and signalable by the monitor. It does not walk/reap an arbitrary descendant tree. The initial timeout is not a hard upper bound on the whole call: **[INFERENCE]** an escaped process that retains an inherited output pipe can keep the second, unbounded `communicate()` waiting after group cleanup.

A further conditional weakness follows from the exact lookup: if `getpgid(proc.pid)` no longer succeeds when cleanup begins, `_kill_group` returns without signaling anything (`:308-311`). **[INFERENCE]** A row leader that has already been reaped while a pipe-holding descendant remains can therefore leave that descendant outside cleanup as well.

| Class | Existing group cleanup | Subreaper + `/proc` descendant walk |
|---|---|---|
| **`setsid`** | **[INFERENCE]** A descendant (the row itself is already a session leader) can create a new session/process group; `killpg` of the original group misses it. This is the disclosed escape. | **[INFERENCE]** A subreaper does not prevent `setsid`, but a walk by descendant ancestry can find and signal the process even after a session change. |
| **Double fork** | **[INFERENCE]** Forking and becoming reparented alone does **not** escape `killpg` if the process remains in the original group. The usual daemon pattern also calls `setsid`; that new group is missed. | **[INFERENCE]** Orphaned grandchildren are adopted by the nearest subreaper rather than escaping to the system reaper; an iterative walk can find them. |
| **Daemonized** | **[INFERENCE]** Classic daemonization (fork/`setsid`/fork) escapes the original group; if it keeps stdout/stderr open, the unbounded post-timeout `communicate()` can hang. | **[INFERENCE]** The daemon remains in the monitor's descendant/adopted-child tree despite its session change; a complete walk plus signaling can close this class. |
| **Stopped process** | If still in the original group, `SIGTERM` may remain pending while it is stopped; the direct-child wait is bounded at five seconds and the subsequent group `SIGKILL` is not catchable or blocked, so a stopped same-group process is **not by itself** an escape. A stopped `setsid` descendant reduces to the setsid case. | A walk can find it; use `SIGKILL` (or ensure escalation) rather than relying on `SIGTERM` to resume it. This adds no signal privilege. |
| **UID change** | **[INFERENCE]** A changed-UID descendant may be present in the group but unsignalable to an unprivileged monitor (`EPERM`); group signaling does not confer authority. | The walk can identify it, but subreaper status and `/proc` visibility do not grant permission to kill it. Root/appropriate capability, or an explicit privilege/containment policy, is still required. |

For the proposed fix, “walk” must mean a repeated/complete descendant traversal, not just one snapshot of direct children: after intermediate parents exit, the subreaper adopts their orphans. Kill/reap until the descendant set is empty, and avoid an unbounded pipe drain being the only completion condition. These are design conditions, not behavior implemented at the pinned revision.

## Last-known-good invariant and test limit

The pinned selftest fixture at `tools/registry-check.py:765-794` launches one sleeping grandchild while its parent also sleeps, then expects timeout and no marker file. It is specifically a same-process-group case; it does not exercise `setsid`, double-fork daemonization, stopped tasks, or UID change. The fixture supports the ordinary-group invariant, not complete descendant confinement. No selftest result is claimed here.

The pinned round-17 verifier spot-check routes this as **R17-TIMEOUT**: “registry NaN/Infinity timeout parsing and setsid escape; retained as disclosed tool-operability edge debts, not proofs of baseline-row regression” (`corpus/lessons/round-17-verifier-spotcheck.md:440-443`). The timeout validator only checks numeric type and `ts <= 0` (`tools/registry-check.py:221-227`); it does not check finiteness, matching that disclosed parsing debt. The round-17 report's wording is a debt disclosure, not evidence that a particular baseline registry row leaked.

**Verdict: built — the pinned static contract and all requested escape classes are classified; dynamic outcomes remain explicitly inferred because runtime execution was out of scope.**