# Round-16 environment hazard controls

Both probes ran the exact pinned `sources-check.mjs --selftest` bytes with `env -i`, private `HOME`, `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`, and `GIT_CEILING_DIRECTORIES` set to the scratch root. Both returned exit 0, 6,274 stdout bytes ending `SOURCES_SELFTEST: 46/46 pass` / `VERDICT: PASS`, and empty stderr. Their stdout SHA-256 is the same as each other and the pristine repeat-control run: `e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f`.

| Hazard | Setup | Result |
|---|---|---|
| Exported `GIT_DIR` | `GIT_DIR=/tmp/tameshi-r18w1-X10CaseControl-8p29q_6f/gitdir-canary/.git`, a temporary committed canary repo | Exit 0, 46/46; full canary filesystem snapshot unchanged (44 entries before and after). |
| `TMPDIR` inside a work tree | `TMPDIR=/tmp/tameshi-r18w1-X10CaseControl-8p29q_6f/fleet/tameshi-shokunin/.round18-hazard-tmpdir` | Exit 0, 46/46; selftest left the temp root empty, then the root was removed; lane-clone `git status --porcelain --untracked-files=all` was empty before and after cleanup. |

Raw stdout/stderr/exit and per-probe JSON are retained as `hazard-git-dir.*` and `hazard-tmpdir-worktree.*`. The `GIT_DIR` result is scoped to this selftest; the source-check selftest uses temporary fixtures and does not exercise round-gate's fixture Git operations.
