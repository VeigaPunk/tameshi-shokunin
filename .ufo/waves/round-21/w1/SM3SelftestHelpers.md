# SM3SelftestHelpers — C1 reuse map

**Verdict: done**

**Source revision:** `33d03b716d3edcf1d8656d46d6df61801d232c52` (line numbers from `git show <rev>:<path>`; workspace read at same paths for spot-check).

**Godspeed axes (this pass):** operability (reuse existing selftest harness), coverage (kill C1 survivors without parallel git/temp scaffolding), isolation (private roots + scrubbed git env), maintainability (one convention per owning tool).

**Tooling:** none installed.

**Method:** read-only inventory of existing selftest helpers; no lane-tree mutation except this report.

---

## Reject list (do not duplicate in new C1 cases)

| Anti-pattern | Use instead |
|---|---|
| Ad-hoc `subprocess.run(["git", ...])` without scrubbed env | `git_clean_env()` / `fixture_repo()` (bash-witness); `_selftest_git_env()` + `_git()` (disposition); `git()` + `git_env()` (registry); nested `git()` + `fixture_env` (trace-inputs) |
| Fresh `tempfile.mkdtemp` layout unrelated to owning selftest | `private_root` + nested `root` (bash-witness); `scratch` + `case-*` lanes (disposition); `scratch` prefix `tameshi-r17-registry-check-selftest.` (registry); `tmp` tree + `trace()` (trace-inputs) |
| Inline `check`/`record` printers | `check()` in `cmd_selftest`; `record()` in disposition/registry selftests; `check()` in trace-inputs selftest |
| Subprocess CLI without `run_cli` / `run_child` / `trace()` | Those wrappers already set cwd, timeout, and env policy |

---

## `tools/bash-witness-study.py` — MB03–MB12

**Guard locus:** `git_clean_env` (:333–339), `fixture_repo` git argv (:1258–1274), `private_root` / cleanup (:1240–1246, :1676–1681).

**Shared module helpers**

| Helper | Line | Signature | One-line usage |
|---|---|---|---|
| `git_clean_env` | 333 | `() -> dict` | Source of truth for GIT_* scrub and config pins; every new git-env mutant case must assert through this, not a copied dict comprehension. |
| `sweep_env` | 582 | `() -> dict` | `git_clean_env()` plus `SCRUB_ENV` removal; use when exercising sweep path env, not a second scrub implementation. |
| `materialize_target` | 342 | `(kagi: Path, rev: str) -> bytes` | Production materialization under hostile inherited env; extend MB03/MB04–07 probes by calling this after exporting extra `GIT_*`. |
| `run_sweep` | 598 | `(evidence: Path, rundir: Path, timeout: int, tail: int) -> dict` | End-to-end sweep launcher; reuse with canary runner swap (existing block :1281–1322) for sweep-side git isolation. |

**Nested inside `cmd_selftest` (:1228+)**

| Helper | Line | Signature | One-line usage |
|---|---|---|---|
| `check` | 1231 | `(name: str, ok: bool) -> None` | Named pass/fail accounting; all new witness guard cases must register here. |
| `fixture_repo` | 1251 | `(name: str, contents: bytes) -> tuple[Path, str]` | Builds isolated repo with `core.hooksPath=/dev/null` and `git_clean_env()`; extend MB08–10 by asserting hook-sensitive behavior through this helper only. |
| `synth_log` | 1371 | `(bad=(), skip=..., omit=(), total=16, summary=None)` | Synthetic runner log builder for classification tests (unrelated to MB03–12 but do not fork for git cases). |

**Per-mutant reuse (new cases must plug into existing helpers)**

| ID | Mutant intent | Reuse (helper @ line) | One-line usage |
|---|---|---|---|
| **MB03** | Partial GIT_* scrub (`GIT_DIR`/`GIT_WORK_TREE` only) | `git_clean_env` 333; `materialize_target` 342; `run_sweep` 598; `fixture_repo` 1251; `check` 1231 | Clone the hostile-env block (:1284–1336): export extra `GIT_*` (e.g. `GIT_INDEX_FILE`), call `materialize_target` + `run_sweep`, assert via two existing `check` names or new names beside them. |
| **MB04** | Drop `GIT_CONFIG_GLOBAL=/dev/null` | `git_clean_env` 333; `fixture_repo` 1257 | Assert `git_clean_env()["GIT_CONFIG_GLOBAL"]` and/or that `fixture_repo` still uses returned env (no inline re-pin). |
| **MB05** | Point `GIT_CONFIG_GLOBAL` at repo `.gitconfig` | `git_clean_env` 333; `fixture_repo` 1251 | Hostile global config must be defeated via `safe_env = git_clean_env()` inside `fixture_repo`, not a parallel init path. |
| **MB06** | `GIT_CONFIG_NOSYSTEM=0` | `git_clean_env` 333 | Pin assertion on `git_clean_env()["GIT_CONFIG_NOSYSTEM"] == "1"` or behavioral probe using `fixture_repo`. |
| **MB07** | Remove `GIT_CONFIG_NOSYSTEM` | `git_clean_env` 333 | Same as MB04/MB06: key presence/value via `git_clean_env()`, execution via `fixture_repo`. |
| **MB08** | Drop `core.hooksPath` on `git init` | `fixture_repo` 1258–1261 | Only mutate hook coverage by extending `fixture_repo` call sites; do not add a second init subprocess template. |
| **MB09** | Drop `core.hooksPath` on `git add` | `fixture_repo` 1263–1266 | Same as MB08. |
| **MB10** | Drop `core.hooksPath` on `git commit` | `fixture_repo` 1268–1273 | Same as MB08. |
| **MB11** | Child workdir under `private_root.parent` | `check` 1231; `private_root` 1240–1246; nested `root` 1245–1246 | Add containment `check` that `root.resolve().is_relative_to(private_root)` (or equivalent) using existing temp layout variables. |
| **MB12** | Wrong `shutil.rmtree` target | `check` 1231; `finally` 1676–1681 | Pre-teardown assertion that `private_root` still exists and is non-empty; rely on existing outer `finally` cleanup pattern, do not duplicate `mkdtemp` hierarchy. |

---

## `tools/evidence-disposition.py` — D02, D11, D12

**Guard locus:** `resolve_historical_anchor` (:460–490), `TREE_MODES` / `historical_blob` (:549, :637–645).

**Selftest infrastructure**

| Helper | Line | Signature | One-line usage |
|---|---|---|---|
| `_selftest_git_env` | 2000 | `() -> dict` | Scrubbed git env for all fixture mutations; never copy its dict logic into a new `_setup_*`. |
| `_git` | 2015 | `(lane, *argv) -> bytes` | All fixture git operations; wrap new branch/mode setup as extra argv, not raw subprocess. |
| `_git_init_commit` | 2071 | `(lane, message="fixture commit") -> str` | Baseline commit for historical pins; use for D11 executable blob setup after `chmod` via `_git`. |
| `_git_commit_all` | 2056 | `(lane, message) -> str` | Subsequent commits on fixture lane. |
| `_write_bytes` | 1710 | `(path, payload) -> None` | Write pinned tool bytes at `SELFTEST_TOOL_REL`. |
| `_build_lane` | 1719 | `(lane, marker, variant) -> fx` | Creates lane tree + expected/disposition inputs; every case starts here. |
| `_dispositions_v2` | 1982 | `(fx, rows, historical=None, ...)` | v2 manifest with `historical_inputs`; used by historical cases. |
| `_rows` | 1928 | `(fx, **variant) -> list` | Default disposition rows for a lane. |
| `run_cli` | 2365 | `(lane, dispositions_path, env_extra=None)` | Subprocess invoke of tool under test with optional `fx["env_extra"]`. |
| `record` | 2356 | `(name, ok, detail)` | Case pass/fail ledger. |
| `case` | 2387 | `(name, expected_exit, expected_ids, variant=None, ..., git_setup=None)` | Full case runner: `_build_lane` → optional `git_setup(fx)` → `run_cli`. |
| `historical_case` | 2438 | `(name, expected_exit, expected_ids, git_setup)` | `case` + `_dispositions_v2` historical wrapper; **required** for G5 / anchor mutants. |

**Existing `git_setup` templates to extend (not reimplement)**

| Setup | Line | Relevance |
|---|---|---|
| `_setup_hist_jj_prebookmark` | 2190 | JJ + `lane.branch=master`; pattern for branch-tip vs HEAD (extend for non-`master` via `_git` config, not new clone flow). |
| `_setup_hist_jj_branch_tip` | 2213 | Branch tip distinct from HEAD; reuse `_jj_init_fixture_repo` + `_jj_commit_tool`. |
| `_setup_hist_gitdir_env` | 2313 | `fx["env_extra"]` for hostile `GIT_DIR`; reuse `run_cli(..., fx.get("env_extra"))` path in `case`. |
| `_setup_hist_clean` | 2076 | Standard historical pin + move at HEAD. |

**Per-mutant reuse**

| ID | Mutant intent | Reuse (helper @ line) | One-line usage |
|---|---|---|---|
| **D02** | Hardcode attached branch to `"master"` | `historical_case` 2438; `case` 2387; `_git` 2015; `_build_lane` 1719 | Add `_setup_hist_*` that runs `git init -b main` (or topic) **without** `lane.branch`, then `historical_case(..., git_setup=that_fn)`; must fail under mutant via `run_cli` JSON ids, not a standalone anchor script. |
| **D11** | Drop mode `100755` from `TREE_MODES` | `historical_case` 2438; `_write_bytes` 1710; `_git_init_commit` 2071; `_git` 2015 | In a new `_setup_hist_executable_pin`, commit pinned tool as mode `100755` using `_git(lane, "update-index", "--chmod=+x", "--", SELFTEST_TOOL_REL)` then `_git_commit_all`; expect clean historical waiver at `fx["hist_rev"]`. |
| **D12** | Hardcode `branch_ref` to `refs/heads/master` | `historical_case` 2438; `_jj_init_fixture_repo` 2162 (`lane.branch` 2167); `_git` 2015 | Configure `lane.branch` to non-`master` with distinct tip via `_git(lane, "config", "lane.branch", "<name>")` + branch setup; `historical_case` must observe wrong anchor under mutant. |

---

## `tools/registry-check.py` — R02, R05, R07

**Guard locus:** timeout validation (~:240), `_row_identity_is_owned` (:468–487), `_signal_process_identity` (:503–517).

**Selftest infrastructure**

| Helper | Line | Signature | One-line usage |
|---|---|---|---|
| `git_env` | 149 | `() -> dict` | Scrub inherited `GIT_*` for fixture git; used by nested `git()`. |
| `row_env` | 170 | `() -> dict` | Env for `run_child` / row execution (`git_env` + `PYTHONDONTWRITEBYTECODE`). |
| `run_child` | 928 | `(args, extra_env=None)` | Subprocess tool invoke with `row_env()` merge. |
| `write_registry` | 940 | `(name, rows, schema=SCHEMA, raw=None) -> str` | Registry JSON path under `scratch`. |
| `row` | 950 | `(name, code, exit_expect, needles=None, timeout=30, **kw) -> dict` | Row dict factory for registry payloads. |
| `check_lines` | 969 | `(proc, wants, stream="stdout") -> bool` | Substring assertions on child output. |
| `record` | 919 | `(name, ok, detail)` | Case ledger. |
| `git` | 1008 | `(args, cwd=None, extra_env=None)` | Fixture git with `git_env()`. |
| `head_of` | 1020 | `(repo) -> str \| None` | Stable HEAD digest for canary/lane repos (gitdir-scrub cases). |
| `process_identity_code` | 974 | `(path) -> str` | Emits row code writing `(pid, starttime)` for escape tests. |
| `read_process_identity` | 982 | `(path) -> tuple \| None` | Read back identity file from escape cases. |
| `process_identity_present` | 990 | `(identity) -> bool` | Verify process still alive with same starttime. |
| `stop_test_process` | 997 | `(identity) -> None` | SIGKILL helper for cleanup. |
| `run_escape_case` | 1160 | `(name, escape_call) -> None` | Template for timeout/ownership integration tests with `write_registry` + `run_child`. |

**Production helper invoked directly in selftest**

| Helper | Line | Signature | One-line usage |
|---|---|---|---|
| `_signal_process_identity` | 503 | `(pid, starttime, signum, in_row_scope, ...)` | R07 unit probe at :1577–1588; extend with `in_row_scope` flipping `True→False`, do not fork pidfd test harness. |

**Per-mutant reuse**

| ID | Mutant intent | Reuse (helper @ line) | One-line usage |
|---|---|---|---|
| **R02** | Accept `timeout_s: 0` | `write_registry` 940; `row` 950; `run_child` 928; `record` 919; `check_lines` 969; loop template 1500–1525 | Add `("timeout-zero", "0", "finite positive number")` tuple to the existing invalid-timeout loop; use `raw=` string replace pattern already there—no new registry writer. |
| **R05** | Ignore `baseline_children` exclusion | `run_child` 928; `write_registry` 940; `row` 950; `git()` 1008; `head_of` 1020; `process_identity_code` 974; `read_process_identity` 983 | Before `run_child`, spawn a long-lived direct child of the checker (pattern: `gitdir-scrub` fixture repos :1036–1074), record its identity, run a row that times out/cleans up; assert canary child survives via `head_of` / `process_identity_present`. |
| **R07** | Drop post-pidfd `in_row_scope()` check | `_signal_process_identity` 503; `record` 919; monkeypatch block 1566–1589 | Copy the existing pidfd test shape: fake `read_stat` stable identity, `in_row_scope` lambda that returns `False` on second call; expect signal suppressed under correct code, sent under mutant. |

**Reference cases to mirror (not duplicate):** `gitdir-scrub-rev` :1084, `gitdir-scrub-row` :1120, `timeout-kills-group` :1147, `pidfd-revalidates-starttime` :1586.

---

## `tools/trace-inputs.py` — T04, T12

**Guard locus:** `scrubbed_env` (:509–517), `digest`/`sha256_file` in `run_trace` (:651–657).

**Module + selftest helpers**

| Helper | Line | Signature | One-line usage |
|---|---|---|---|
| `scrubbed_env` | 509 | `(workdir) -> tuple[dict, list, str]` | Sets `PYTHONPYCACHEPREFIX` under workdir; T04 cases must assert via this function or `trace()` payload, not reimplement prefix logic. |
| `sha256_file` | 501 | `(path) -> str` | File-content hashing for inputs; T12 cases must expect digests from this helper, not path-string hashes. |
| `make_workdir` | 575 | `(root) -> str \| None` | Private workdir outside `--root`; already used by `run_trace`; selftest uses `trace()` which calls full CLI. |
| `check` | 776 | `(name, cond)` | Selftest pass/fail list. |
| `trace` | 779 | `(argv, use_root=None, env=None, capture=False, cwd_opt=None, extra=None)` | Runs CLI with fleet/lane/home fixtures; returns `(rc, data, stdout)`. |
| `git` (nested) | 756 | `(*args, cwd)` | Isolated git fixture for tracked-filter cases; uses `fixture_env` dict (:748–754)—reuse for git cases, do not duplicate `fixture_env` construction. |

**Per-mutant reuse**

| ID | Mutant intent | Reuse (helper @ line) | One-line usage |
|---|---|---|---|
| **T04** | `PYTHONPYCACHEPREFIX` outside workdir / system temp | `trace` 779; `check` 776; existing checks `env-scrubbed` 919, `pycache-prefix-private` 926 | Add assertion that `data["env_overrides"]["set"]["PYTHONPYCACHEPREFIX"]` stays under trace workdir and matches `scrubbed_env(workdir)[2]` semantics; extend `pycache-prefix-private`, do not new subprocess wrapper. |
| **T12** | Hash path string instead of file bytes | `trace` 779; `sha256_file` 501; `check` 776; `double-import-keeps-py` 934 | Run a trace that reads a known file, compare `data["inputs"][rel]` to `sha256_file(abs_path)`; failing mutant diverges without duplicating `digest()` from `run_trace` :651–657. |

---

## Evidence paths

| Artifact | Path |
|---|---|
| This report | `.ufo/waves/round-21/w1/SM3SelftestHelpers.md` |
| C1 mutant roster | `.ufo/evidence/round-21/c1-mutants.json` |
| Round-18 survivor rationale | `.ufo/waves/round-18/w2/Mutate{BashWitness,Disposition,RegistryCheck,TraceInputs}18.md` |

## Commands (read-only)

| Command | Exit |
|---|---|
| `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 33d03b716d3edcf1d8656d46d6df61801d232c52:tools/{bash-witness-study,evidence-disposition,registry-check,trace-inputs}.py` (via `rg`/`nl` for defs) | 0 |

No disagreements with frozen `c1-mutants.json` IDs or owning paths.
