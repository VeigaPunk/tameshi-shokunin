# N01ProbeSafety — A/E and canary write-safety review

Axes: write containment, repository/config isolation, provenance, and cleanup.

## Scope and evidence

Static review only; I did not execute any selftest, probe, canary row, migration, or mutating `jj` command. The new A probe was absent when checked (`.ufo/evidence/round-18/defect-probes.py` read returned “not found”), so A findings below are contract-level requirements plus observed clone/canary patterns, not claims about its implementation. The active X09 canary and X07 staged copy were read as-is; neither was run.

Committed source snapshots at `183f87b899e6cae46be98d251cbc87fb5118f6ca` were fetched into `/tmp/tameshi-r18w1-N01ProbeSafety-pZe96Y` with `git show` (bash commands exited 0): `tools/bash-witness-study.py`, `tools/registry-check.py`, `tools/evidence-disposition.py`, `tools/mutate-and-run.sh`, `tools/registry.json`, and the R17 disposition/registry mutation reports. `jj --ignore-working-copy --version && jj --ignore-working-copy help config` exited 0 (`jj 0.45.1`); `jj --ignore-working-copy help -k config` exited 0. Official Jujutsu config docs confirm user config comes from `$HOME/.jjconfig.toml` and/or `$XDG_CONFIG_HOME/jj/config.toml`; `JJ_CONFIG` overrides the default locations, and an empty value disables user config loading: <https://docs.jj-vcs.dev/latest/config/#user-config-files>.

## Findings

### HIGH — The `/tmp` clone is not a filesystem write boundary; sibling symlinks are live

**Exploit path.** X09 reads registry `argv` records and passes them directly to `subprocess.Popen` ( `.ufo/evidence/round-18/git-env-canary.py:173-197,222-238`). It runs with `cwd=clone` (`:235-238`), while `make_fleet_clone()` creates symlinks from the scratch fleet to the actual sibling repositories (`:76-100`, especially `:81-91`). Therefore a command using a relative path such as `../kumitate-shokunin/...` from the clone reaches a live sibling through the scratch symlink. Absolute paths and arbitrary file writes are also possible: subprocesses run as the caller with no filesystem sandbox. `registry-check.py`'s separate `_argv_outside_fleet()` guard only recognizes absolute tokens (`tools/registry-check.py:326-339`), so it cannot protect this relative traversal; X09 has no equivalent check. X09 also accepts a caller-selected `--root` and checks only that it is a directory (`git-env-canary.py:264-270`), not that its real path is the intended lane.

**Impact.** A selftest can modify the live lane, any symlinked sibling, or other caller-writable paths even though its checkout and canary are under `/tmp`. A pinned `argv` list is still executable code, not inert registry data. The child also inherits non-Git environment values (`:224-231`), including `HOME`, credentials, and caller `PATH`; a test can read them and has no network restriction.

**Smallest remediation.** Execute probe/canary children in a filesystem sandbox: read-only bind `/`, writable bind only the fresh `$W` (and a private `/tmp` below it), disable network, and isolate PIDs. R17 already records a working precedent: `MutateRegistryCheck.md:31-39` ran the detector with `bwrap --unshare-all`, `--ro-bind / /`, and only scratch binds. Require an absolute source `--root` and assert `realpath(root)` is the expected lane path; assert `realpath(clone)`, `realpath(canary)`, `cwd`, and every writable fixture path stay under the unique scratch root. Keep the source lane read-only, and do not symlink live sibling repos into a writable run (use scratch snapshots or read-only mounts).

### HIGH — Git config and user environment still reach the canary rows and E's fixture commits

**Exploit path.** X09's helper `git_environment()` does scrub Git variables and sets `GIT_CONFIG_GLOBAL=/dev/null` / `GIT_CONFIG_NOSYSTEM=1` (`git-env-canary.py:34-47`), but `run_row()` builds a different environment (`:224-231`) and launches with it (`:235-238`). That row environment has the deliberately injected `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`, but no global-config override, private `HOME`, or private `XDG_CONFIG_HOME`; it otherwise copies the caller environment. Separately, the staged E source filters `GIT_*` in `git_clean_env()` (`.ufo/waves/round-18/staged/tools/bash-witness-study.py:332-346`) but does not disable global/system Git config. Its new selftest runs `git init/add/commit` through that environment (`:1247-1265`), including `git commit` at `:1256-1260`. The committed R17 runner also scrubs `GIT_*` but does not replace global config (`tools/mutate-and-run.sh:257-267`); its fixture commit path is `:275-286`.

**Impact.** `GIT_*` repository redirection is addressed in the staged E helper, but the test still reads the host's Git configuration. A user-level `core.hooksPath` can execute a configured hook during fixture commits; other Git config may alter behavior. X09 child rows can likewise invoke user-configured hooks. The private canary catches only Git metadata changes routed to its own `.git`; it does not make host hooks or host config safe.

**Smallest remediation.** For every internal Git child, first filter *all* inherited `GIT_*`, then add only deliberate variables. Set `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, and disable hooks (`-c core.hooksPath=/dev/null`) for fixture Git writes. Launch outer commands with a clean allowlist (or at minimum `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`, plus code-level filtering of every `GIT_*`). Set `HOME=$W/home`, `XDG_CONFIG_HOME=$W/xdg`, and a harmless fixed `PATH`; never pass caller credentials to registry rows.

### HIGH — E selftest scratch follows caller `TMPDIR` and is recursively removed

**Exploit path.** The committed E selftest uses `tempfile.mkdtemp(prefix="bash-witness-selftest.")` with no explicit `dir` (`tools/bash-witness-study.py:1230`) and unconditionally removes the result (`:1571`). The staged copy retains the same pattern (`.ufo/waves/round-18/staged/tools/bash-witness-study.py:1236,1664`). Python's default temp-directory selection honors the process temp environment; setting `TMPDIR` into a live lane or sibling makes the fixture tree appear there, and the final `rmtree()` removes that generated tree. This is an inferred consequence of the source and Python temp-path behavior; I did not execute it.

**Impact.** A selftest can write into (and later delete its own newly created subtree from) the live lane or sibling, violating the no-live-write boundary. A symlinked temp root also defeats a lexical path check.

**Smallest remediation.** Create a unique scratch root with explicit `dir="/tmp"` or under an already private `$W/tmp`, set `TMPDIR` to that private directory for every child, and immediately assert its resolved real path is inside `$W` before creating fixtures or allowing cleanup. Apply the same root assertion before `shutil.rmtree()`.

### MEDIUM — E's ordinary write modes default to lane-owned evidence

**Exploit path.** `REPO` is derived from the script location and `EVIDENCE_DEFAULT` is `REPO/.ufo/evidence/round-12/BashWitness` (`tools/bash-witness-study.py:93-95`). `declare` creates that directory and writes target/spec/declaration artifacts (`:836-867`); `run` writes a sweep below it (`:1000-1005`); `rerun` creates a rerun and rewrites the evidence manifest (`:1008-1023`). Running these modes from the live script therefore writes into the lane by default. E's relative `--evidence` also depends on caller cwd; the separate registry/disposition check invocations' relative registry/dispositions and `--root .` depend on cwd as well.

**Impact.** A verification or migration invocation accidentally run from the live lane can alter lane evidence. The specified round-18 `dispositions.json` is intentionally a new lane file, but its creation must remain an explicit lane-owned write; its validation must not be confused with a scratch run.

**Smallest remediation.** Run mutating E modes only from a `/tmp` clone with explicit `--evidence "$W/evidence"`; check the resolved evidence path is contained in `$W` before the first `mkdir`/write. Validate manifests from the clone root using absolute `--root "$C"` and absolute disposition paths, not a bare `.` from an ambient cwd. Let only the designated integrator create the one explicitly authorized new lane manifest.

### MEDIUM — Jujutsu fixture needs private config and a verified fixture cwd

**Exploit path.** The A/P08 plan calls for a `jj git init --colocate` fixture and branch/HEAD divergence (`.ufo/waves/round-18/dispatch1.json:503-505`); no such `jj` setup or `JJ_CONFIG` isolation was present in the staged disposition tool when checked (`grep` found no `jj`, `JJ_CONFIG`, `HOME`, or `XDG_CONFIG_HOME`; its existing scratch root is explicit `/tmp` at `.ufo/waves/round-18/staged/tools/evidence-disposition.py:2081-2083`). Jujutsu discovers user config via `HOME`/`XDG_CONFIG_HOME` unless controlled by `JJ_CONFIG`. If fixture `cwd` or a relative path resolves into the lane/sibling, `jj git init --colocate` and later commit/bookmark operations can mutate that repository's `.jj` and `.git` state.

**Impact.** User configuration can affect fixture authorship/behavior, and a wrong cwd can mutate a real colocated repository. This is a planned-path risk, not an observed write.

**Smallest remediation.** Put each Jj fixture in a fresh `mkdtemp` below `$W`, pass absolute `cwd`/repository paths, assert the fixture's real path is strictly under `$W`, set `HOME=$W/home`, `XDG_CONFIG_HOME=$W/xdg`, and `JJ_CONFIG=` (or a private controlled config). Set synthetic `JJ_USER`/`JJ_EMAIL` if commits are needed. Never invoke the fixture against the live lane or sibling. I did not execute mutating `jj` commands.

### MEDIUM — Canary can report clean after worktree/config writes or an escaped child

**Exploit path.** X09 compares only `.git/HEAD`, refs/packed-refs, index/index.lock, and objects (`git-env-canary.py:157-170`); it does not fingerprint the canary working tree or other `.git` files such as `config`. A row can alter `canary/seed.txt` or `.git/config` without changing any measured component. On timeout, `kill_process_group()` signals only the original process group (`:207-219`); `run_row()` fingerprints immediately after that cleanup (`:241-250`), and the outer `finally` removes scratch (`:268-281`). A child that calls `setsid()` can outlive that group, write after the snapshot, or traverse a sibling symlink. This is an inferred failure path; no process was launched.

**Impact.** The canary can return `clean` despite canary worktree/config writes, and a timed-out descendant may continue writing after the verdict or cleanup.

**Smallest remediation.** Snapshot the entire canary worktree and all `.git` state, not only four metadata components. Run rows under a PID namespace/cgroup (or equivalent descendant supervision), wait until all descendants are dead before the after-snapshot and scratch deletion, and keep their writable filesystem confined to `$W`.

## Minimum launch envelope for A/E/X09

Use a fresh `W=$(mktemp -d /tmp/tameshi-r18w1-<seat>-XXXXXX)`; create private `home`, `xdg`, and `tmp` beneath it; run from the absolute clone path. Use a clean env allowlist (or the required `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR` plus code-level filtering of all other `GIT_*`), set `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `HOME="$W/home"`, `XDG_CONFIG_HOME="$W/xdg"`, `TMPDIR="$W/tmp"`, and `JJ_CONFIG=` for any Jujutsu fixture. Assert `realpath(source_root)` equals the expected lane; assert `realpath(clone)`, fixtures, canary, `cwd`, and every write/cleanup path are contained under `$W`. A `/tmp` pathname alone is not containment while its fleet symlinks point back to writable live siblings.

No tool was installed or updated. No dynamic verification was run; the source and contract review found the paths above.

Verdict: **falls** — the staged E and X09 paths still permit host-config execution, TMPDIR-directed lane writes, and unsandboxed relative writes through live sibling symlinks.