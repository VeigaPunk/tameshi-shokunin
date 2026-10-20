# SentinelKillCode — `tools/registry-check.py` descendant cleanup

Target: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`; `tools/registry-check.py` SHA-256 `e072fd3995ca1df1477613f009193e20f3797bc4673ee3045a04afb9927c2899`.

Axes: ownership integrity; subreaper/lifecycle isolation; cleanup liveness.

## Finding 1 — MEDIUM: unrelated adopted orphans can be signaled and reaped

**Exploit path.** `run_row` sets the checker process as a child subreaper and snapshots its direct children immediately before launching the row (`tools/registry-check.py:384-409,641-676`). For any process whose current ancestry reaches a direct child of the checker, `_row_identity_is_owned` classifies a newly adopted direct child as row-owned solely because its `(pid,starttime)` is absent from that snapshot (`:461-482`, especially `:479-480`). The subsequent cleanup sends TERM/KILL to that identity and can `waitpid` its zombie (`:520-531,534-553`). Thus a pre-existing unrelated checker child can fork a process after the baseline, exit, and have the process adopted by the checker; the row cleanup then treats it as the row's descendant. The adopted process can be in a different session; session ID is not part of the ownership decision.

**Evidence.** I ran the local experiment script in a bwrap sandbox with the pinned clone read-only and no network:

```text
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind /tmp/tameshi-r18w2-SentinelKillCode-N6lDRX /tmp/tameshi-r18w2-SentinelKillCode-N6lDRX \
  --ro-bind /tmp/tameshi-r18w2-SentinelKillCode-N6lDRX/fleet/tameshi-shokunin /tmp/tameshi-r18w2-SentinelKillCode-N6lDRX/fleet/tameshi-shokunin \
  --unshare-net --die-with-parent \
  --chdir /tmp/tameshi-r18w2-SentinelKillCode-N6lDRX/fleet/tameshi-shokunin \
  env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  HOME=/tmp/tameshi-r18w2-SentinelKillCode-N6lDRX/home \
  TMPDIR=/tmp/tameshi-r18w2-SentinelKillCode-N6lDRX/tmp \
  C=/tmp/tameshi-r18w2-SentinelKillCode-N6lDRX/fleet/tameshi-shokunin \
  LC_ALL=C PYTHONDONTWRITEBYTECODE=1 \
  python3 /tmp/tameshi-r18w2-SentinelKillCode-N6lDRX/kill-experiments.py
```

Exit: **0**. Key output:

```text
unrelated_orphan fragment_held=True orphan_session_escape=True term_handler=True orphan_survived=False signal=SIGTERM checker_subreaper_after_run_row=1
```

The unrelated process was spawned by a checker child that existed at the baseline, then was orphaned to the checker; the row itself only printed its expected output and exited successfully. The orphan installed a SIGTERM handler, called `setsid()`, and was gone after `run_row`. This is an observed signal to a process that was not a descendant of the row, followed by cleanup/reaping. In ordinary standalone CLI use the checker is normally sequential, so the trigger requires another child/process tree in the checker process; it is reachable when `run_row` is used in-process or the checker has concurrent/unrelated children.

**Smallest remediation.** Do not infer ownership of every post-baseline adopted child. Put each row and its cleanup under a dedicated per-row subreaper/supervisor whose only workload tree is that row, or otherwise retain verifiable row-tree provenance before reparenting; preserve PID/session escape handling within that isolated ownership boundary.

## Finding 2 — LOW: same-tick PID reuse can pass the identity check

`/proc/<pid>/stat` start time is stored as an integer tick (`:412-426`). The ownership walk accepts `current == proc_pid` when that tick equals the earlier row start time (`:471-477`), and `_signal_process_identity` opens a pidfd only after its first identity/scope check (`:496-512`). If the row leader has exited/reaped and its PID is reused within the same start-time tick, the replacement can satisfy both revalidation reads; `pidfd_open` then pins/signals the replacement. The normal success path calls cleanup after `communicate` (`:685-708`), so this PID-reuse window is not excluded by keeping the leader unreaped. The file's own contract acknowledges a “same-tick PID-reuse residual” (`:39-44`).

**Evidence.** The experiment included a deterministic synthetic same-tick identity (mocked `/proc` and pidfd boundary; not a reproduction of kernel PID reuse):

```text
synthetic_same_tick_reuse_owned=True pidfd_signal_requests=1
```

This confirms the predicate accepts the ambiguous `(pid,starttime)` and proceeds to signal; the actual kernel race is unobserved and remains narrow/inferred.

**Smallest remediation.** Retain a pidfd for the row leader from immediately after `Popen` and never treat a post-reap process with the same PID/tick as that leader; use stronger retained identity/provenance for cleanup targets rather than start-time ticks alone.

## Other requested failure modes

- **Caller/parent signal:** not observed. The ancestry predicate rejects the checker process's own parent (`own_parent_owned=False`); its start-time identity survived. The walk only returns true at the row leader or a newly adopted direct child, not by walking upward to the caller. This does not mitigate Finding 1.
- **Subreaper lifetime:** `_enable_child_subreaper` sets `PR_SET_CHILD_SUBREAPER=1` and has no matching reset (`:384-409`). In-process experiment output showed `checker_subreaper_after_run_row=1`: a caller that invokes `run_row` directly remains a subreaper for its lifetime. A separate actual checker CLI subprocess left its external parent unchanged (`cli_exit=0 parent_subreaper_before=0 after=0 held=True`), consistent with the process-local flag. Combined with Finding 1, the checker process may adopt/reap unrelated children while it remains alive.
- **Deadlock/drain:** no deadlock found in the tested setsid/pipe escape. A row leader exited while its setsid descendant held the row's output pipes; cleanup/drain returned held with no cleanup error in `0.349s` (`setsid_pipe_drain held=True elapsed_s=0.349 cleanup_error=False`). The TERM/KILL loops and pipe drain use bounded waits/close streams (`:570-622`). These are loop deadlines, not a hard real-time bound: `/proc` snapshots and ancestry walks complete before the deadline checks (`:431-446,570-602`), so heavy process churn can extend wall time.

## Reproduction provenance

Pinned clone verification command exited **0**:

```text
git -C /tmp/tameshi-r18w2-SentinelKillCode-N6lDRX/fleet/tameshi-shokunin rev-parse HEAD
sha256sum /tmp/tameshi-r18w2-SentinelKillCode-N6lDRX/fleet/tameshi-shokunin/tools/registry-check.py
```

Observed revision: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`; observed SHA-256: `e072fd3995ca1df1477613f009193e20f3797bc4673ee3045a04afb9927c2899`. Experiment source: `/tmp/tameshi-r18w2-SentinelKillCode-N6lDRX/kill-experiments.py`. No lane source files were modified.

**Verdict: falls — an unrelated adopted orphan is demonstrably signaled/reaped; same-tick PID reuse is a narrower residual.**
