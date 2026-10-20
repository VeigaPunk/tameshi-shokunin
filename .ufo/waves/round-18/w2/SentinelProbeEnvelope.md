# SentinelProbeEnvelope — round-18 read-revision safety review

**Reviewed revision:** `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` (confirmed by `git rev-parse HEAD`, exit 0, in the `/tmp` clone). Axes: write containment, repository/config isolation, provenance, and cleanup. No source files were changed; this report is the only lane write.

## HIGH — `git-env-canary.py` still runs registry commands with host write access

**Exploit path.** The canary reads the registry from its clone and accepts each selected selftest row's string `argv` after only type/name/timeout checks (`.ufo/evidence/round-18/git-env-canary.py:173-197`). `make_fleet_clone()` creates `$scratch/fleet/<sibling>` symlinks to the real sibling repositories (`:76-100`, especially `:81-91`). It then launches the row's `argv` directly, with `cwd=clone` and no bwrap/filesystem sandbox (`:222-238`). A child can therefore reach a live sibling via a relative traversal through the fleet symlink; it can also target the live lane or other caller-writable paths by absolute path or path traversal. The `/tmp` clone is not a write boundary.

The row environment is copied from the caller except for `GIT_*`, then populated with canary selectors (`:222-231`). It retains host `HOME`, `XDG_CONFIG_HOME`, `JJ_CONFIG`, `PATH`, and other non-Git variables. Unlike the control Git helper at `:34-47`, the row launch does not disable global/system Git configuration or use private config directories. A row can invoke Git/JJ or other code that writes user config; Git may also load host config and run configured hooks. This matches N01's HIGH findings at `N01ProbeSafety.md:13-27`.

**Impact.** A selected row is executable code, not passive canary data. Depending on its `argv` and implementation, it can modify the live lane, a sibling repo, user Git/JJ configuration, or any other user-writable location. The row has no network isolation. **No canary row was run in this review.**

**Smallest remediation.** Run every row in the same read-only-root / scratch-only bwrap envelope as `defect-probes.py`; do not expose live sibling symlinks as writable paths. Use an `env -i` allowlist with private `HOME`, `XDG_CONFIG_HOME`, `TMPDIR`, `JJ_CONFIG=`, `GIT_CONFIG_GLOBAL=/dev/null`, and `GIT_CONFIG_NOSYSTEM=1`; disable hooks for fixture Git operations.

## HIGH — canary snapshot and timeout handling still permit a false clean / live descendant

**Evidence and exploit path.** Although `tree_fingerprint()` exists (`:135-154`), `component_snapshot()` records only `.git/HEAD`, refs/packed-refs, index/index.lock, and objects (`:157-170`); it omits the canary worktree and other `.git` files such as `config`. A row can change the canary's `seed.txt` or `.git/config` without changing a measured component, yielding `canary=clean`. On timeout, cleanup signals only the original process group (`:207-219`); the row runs in a new session (`:235-238`), and the after-snapshot happens immediately after that cleanup (`:241-250`) before scratch removal (`:264-281`). A descendant that creates a new session can survive, write after the snapshot, or outlive scratch cleanup. This is the remaining N01 finding at `N01ProbeSafety.md:53-59`.

**Impact.** The canary can miss worktree/config tampering and can return before an escaped descendant is done; such a process can continue writing outside scratch because there is no filesystem boundary.

**Smallest remediation.** Snapshot the complete canary tree and all `.git` state, and supervise all descendants with a PID namespace/cgroup or equivalent, waiting for them to exit before taking the after-snapshot and deleting scratch. Filesystem confinement is still required; snapshots are detection, not containment.

## MEDIUM — `defect-probes.py` has a narrow host-side execution gap; PATH trusts the caller's `jj` directory

The normal command children are well-contained: the probe makes a fresh `/tmp` work root (`:1053-1057`), uses realpath/commonpath checks (`:115-126`), maps work paths to `/mnt` and source paths to `/mnt/source` (`:129-147`), launches children with `env -i` and the bwrap wrapper (`:183-205`), and cleans only the checked work root (`:1082-1085`). The wrapper makes `/` read-only, binds W at W and `/mnt`, optionally read-only-binds the fleet at `/mnt/source`, and binds W/tmp at `/tmp` (`:191-205`). The source/fleet symlinks are created at `:283-307`, but the source tree is exposed read-only; `/mnt` is only another alias of W. The private `HOME`, XDG dirs, `TMPDIR`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_NOSYSTEM`, and empty `JJ_CONFIG` are set in `:150-175`. In the traced run, clone writes appeared under `/mnt/fleet/...` (the W bind), while no write-capable open/rename/unlink to `/mnt/source` or a host home/system path was found.

Two residual trust points:

- P08 imports the cloned `tools/evidence-disposition.py` directly into the unsandboxed probe process (`:403-415`) and invokes its fixture helpers directly (`:466-471`, `:516-527`). At this revision the module top level is imports/constants, and `_build_lane()` writes below the passed fixture directory (`tools/evidence-disposition.py:1719-1728`); the fixture is checked under W at `defect-probes.py:462-476`. No escape was observed. However, a selected revision can supply module-level code that executes during import before bwrap; this leaves code from the target revision outside the stated envelope. **[INFERENCE]** A hostile or compromised `--rev` can use that path to write outside W.
- `JJ_COMMAND = shutil.which("jj")` resolves using the caller's PATH (`:49`), then `child_environment()` prepends its directory to child PATH (`:153-166`). In this run `jj` resolved to `/home/vgpnk/.local/bin/jj`; with that prefix, `git` resolved to `/usr/bin/git` (checked without executing it). The directory is on the read-only root bind during child execution, so this does not itself enable a filesystem escape, but it trusts a user-controlled executable directory and gives its commands precedence over system tools. Pin the intended JJ binary and avoid adding its directory to the general child PATH (or explicitly allowlist trusted executables).

**Smallest remediation.** Move P08 fixture construction into trusted probe code or execute it in bwrap. Resolve JJ from an explicit trusted path and use a fixed minimal PATH. Keep the current read-only source mount and private config environment.

## Trace run and write inventory

Ran the requested probe once, with `strace` itself outside bwrap and tracing its descendants:

```text
strace -f -e trace=openat,rename,unlink -o /tmp/tameshi-r18w2-SentinelProbeEnvelope-JEcsYz/probe.strace python3 /tmp/tameshi-r18w2-SentinelProbeEnvelope-JEcsYz/fleet/tameshi-shokunin/.ufo/evidence/round-18/defect-probes.py --rev 01d586ddbc5fcd78659557c4e93a6ee8517b87d1 --json
exit=2
```

Output: P01-P04 and P08-P11 were reported closed; P05-P07 were errors because the pristine `tools/trace-inputs.py --selftest` returned 1 (`SELFTEST: 5/30`); final line was `DEFECT_PROBES: could-not-evaluate (3 probe error(s))`. Thus the run is useful for containment evidence but not a complete pass of all eleven probe cases. The trace had 211,838 lines. Successful write-mode opens and renames in the sampled trace target `/mnt/fleet/tameshi-shokunin/.git/...` (for example trace lines 383-435); this is the probe's W mounted at `/mnt`, not the live lane. The only out-of-`/tmp` write-capable opens visible were bubblewrap namespace setup (`uid_map`, `setgroups`, `gid_map`, trace lines 201-203) and device-node creation in its private `/dev` (`newroot/dev`, lines 211-229); `/dev/null` was also opened O_RDWR. Searches found no write-mode open/rename/unlink targeting `/home`, `/root`, `/etc`, `/usr`, `/var`, `/opt`, `/run`, `/srv`, `/boot`, or `/mnt/source`. The requested trace set excludes `write(2)`/`writev(2)`, so this is a path/open/rename/unlink inventory, not a byte-write syscall audit.

## N01 delta

The new `defect-probes.py` substantially closes N01's A-probe filesystem/config boundary: its ordinary children are bwrap-confined and the `/mnt/source` mapping is read-only. N01's Bash witness TMPDIR concern is also fixed in this revision: its selftest explicitly creates a private root under `/tmp` and nests the fixture there (`tools/bash-witness-study.py:1240-1247`), then checks/respects those roots during cleanup (`:1678-1681`). The separate `git-env-canary.py` risks above remain.

Verdict: **falls** — `defect-probes.py`'s ordinary bwrap children showed no path escape, but `git-env-canary.py` still executes rows without filesystem or config isolation, and P08 imports target code outside bwrap.