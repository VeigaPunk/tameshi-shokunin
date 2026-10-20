# X10 — `sources-check` C1 control

**Axis:** C1 depth’s determinism precondition; calibration via first falsifiers. Scope is only the pinned selftest and the named environment hazards.

## Pinned bytes and repeated control

Materialized kumitate `scripts/sources-check.mjs` from `0acb7752d19058b953ebbeba253b1e35f6548de5` into `/tmp/tameshi-r18w1-X10CaseControl-8p29q_6f/materialized/sources-check.mjs`. Its SHA-256 was `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`, matching the assigned digest. The lane tool came from a `/tmp` clone checked out at `183f87b899e6cae46be98d251cbc87fb5118f6ca`.

Ran the requested eight controls through that clone’s `tools/repeat-control.py`, using the exact argv/environment retained in `control/repeat/command.txt:1-7`: `env -i PATH=<expanded dispatch PATH> HOME=<private> TMPDIR=<private> LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES=<scratch> node sources-check.mjs --selftest`.

- `repeat-control.py` exit **0**, `REPEAT_CONTROL: controls_match`, `REPEAT_EXIT: 0`; `REPEAT_COMPARE identical=yes runs=8` (`control/repeat-control.stdout:2-12`, `control/repeat/finding.txt:1-2`, `control/repeat-control.exit:1`).
- All eight selftests exited 0 and printed `SOURCES_SELFTEST: 46/46 pass` / `VERDICT: PASS` (`control/repeat/run-1.stdout:47-48`; each numbered raw stdout/stderr/exit is retained).
- Hash variability: stdout had one distinct SHA-256 across 8 runs (`e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f`, 6,274 bytes each); stderr had one distinct hash (empty, `e3b0c442…b855`, 0 bytes each); exit-file hash was also constant (`9a271f2a…86aa`, each `0\n`). Full per-run digests are in `control/repeat-hashes.json`.

## Hermeticity trace

Ran one `strace -f -e trace=%file,%network` selftest. Target and strace both exited 0; stdout ended `SOURCES_SELFTEST: 46/46 pass` / `VERDICT: PASS`; stderr was empty (`control/strace.exit:1`, `control/strace.stdout:47-48`). The complete trace is retained at `control/strace.log` (4,814 lines, SHA-256 `dbad6312c795ee5d3fa07db9b07572de7d1b443a93fd001e96cc922fdf156514`).

- No trace line referenced `/home/vgpnk/Projects`.
- The `%network` class recorded 1,108 syscalls, all observed socket family `AF_UNIX`: `socketpair=129`, `setsockopt=516`, `shutdown=43`, `getsockname=210`, `getsockopt=210`. No `AF_INET`/`AF_INET6`, `connect`, `bind`, send, or receive calls were seen. This was local Unix-domain IPC, not external network access.
- 315 successful filesystem operations resolved inside the private `TMPDIR`. The only successful write-capable open outside it was `/dev/null` for shell stderr redirection (a non-persistent special-device sink); an `O_RDWR` `/dev/tty` open failed with `ENXIO`. No successful regular-file or directory mutation outside `TMPDIR` was observed. Relative cleanup paths were resolved against traced directory FDs and remained under `TMPDIR`.
- The requested strace filter does not trace `write(2)`/`writev(2)` payload syscalls; the path-level accounting and this limitation are recorded in `control/strace-summary.md:9-13`.

## Round-16 hazard probes

- **Exported `GIT_DIR`:** injected `GIT_DIR=<scratch>/gitdir-canary/.git` for the selftest. Exit 0, 46/46; the canary’s full filesystem snapshot remained unchanged (44 entries before and after), recorded in `control/hazard-git-dir.json:16-23` and raw `control/hazard-git-dir.*`.
- **`TMPDIR` inside a work tree:** pointed `TMPDIR` into the temporary lane clone. Exit 0, 46/46; selftest left its temp root empty; after removing that root, lane-clone status was empty before and after (`control/hazard-tmpdir-worktree.json:15-24` and raw `control/hazard-tmpdir-worktree.*`).

The behavior matches this source’s stated contract (`kumitate-shokunin/scripts/sources-check.mjs:7-8`): selftest fixtures are created under the OS temporary directory and removed. The selftest creates its temp root at `:565`, runs a local shell/awk parity check at `:859`, and removes the root in `finally` at `:872-874`. The GIT_DIR probe is specific to this test; unlike round-gate’s fixture suite, this source-check selftest does not exercise Git fixture commits.

## Retained evidence, risks, and blockers

`control/` contains the repeat-control command and finding, all eight numbered raw outputs/exits, `repeat-hashes.json`, raw strace stdout/stderr/exit and full log plus `strace-summary.md`, and both hazard stdout/stderr/exit plus JSON and `hazard-summary.md`. No implementation files were changed and no tools were installed. No blocker.

Residual scope: this is eight finite repetitions of one pinned revision/environment. `strace` was intentionally run once with the requested `%file,%network` filter; it cannot establish general sandbox behavior or directly account for data-only `write(2)` calls.

**Verdict: holds — the pinned selftest was byte-identical across eight clean runs; both named hazards passed without canary/worktree changes, with local IPC and the `/dev/null` sink disclosed above.**
