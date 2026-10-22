# C2 tar-safety, staging and SETUP review: tools/mte-interop.py

## Verdict

Not clean, but no path lets a missing node or missing jsonschema reach PASS, and I found no write into a sibling repo.

- **F1 (Medium):** `--workdir` can PASS over fewer legs than its own regression table records.
- **F2 (Low, latent):** the tar guard in `official_metrics()` does not contain absolute member names. Exploiting it needs the vendored tgz and its source pin changed in the same commit.
- **F3 (Low):** a node timeout escapes as an uncaught `TimeoutExpired`, exit 1 (the FAIL code), not exit 2 (SETUP).
- **F4 (Low, static):** a runner FAIL (exit 1) is reported as `SETUP (regression exit 1)`.
- **F5 (Low):** auto workdirs are left behind on SETUP and FAIL, and their path is never printed. Node is checked only after the full sweep.
- **F6 (Low, latent):** the six unsandboxed pinned suites run in the caller's cwd and inherit the caller's `GIT_*` environment. Nothing wrote into a sibling in isolated tests.
- **F7 (informational):** an earlier revision crashed on a null mutation score (exit 1, no summary). The current revision fixes it.

## Scope and revision reviewed

- Target: `tools/mte-interop.py` `official_metrics()` (194-217), `run_regression()` (261-283), and the `check()` paths that reach them (286-335). Also `selftest()` (338-427) and `main()`, read for context.
- Final lane state: `sha256 8c24255c9e482751772e958e5ba9a615891ca7e5dfc9426d2fb5667ceae65552`, 455 lines. The file changed twice during the review. My first snapshot (`e0c5f2f3…`, 454 lines) differs in one hunk inside `check()` (the rounding line, F7). Line numbers below refer to the final state.
- Runner read: `tools/mutate-and-run.sh`, `sha256 d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`, 1940 lines, unchanged throughout.
- Vendored archives: the sha512 pins in source match the vendored tgz files, and both match the npm registry `dist.integrity` for 3.9.0 (read-only `npm view`).
- Nothing in the repo was edited. All execution happened on /tmp copies and /tmp fixtures.

## Coverage map

| Region (final state) | Reviewed | Evidence |
|---|---|---|
| 1-85 imports, PACKAGES pins, NODE_RUNNER, LEG_TABLE (74) | yes | pins vs. vendored bytes and npm |
| 175-187 `verified_tarball`, `load_schema` | yes | integrity probe; check-then-use review |
| 194-217 `official_metrics` | yes | F2, F3; temp-dir cleanup probes |
| 220-258 `recorded_verdicts`, `judge` | yes | no-ledger FAIL probe; selftest 16/16 |
| 261-283 `run_regression` | yes | F4, F5, F6; fleet staging probe; rmtree probe |
| 286-335 `check` | yes | F1, F5, F7; SETUP and PASS probes |
| 338-427 `selftest`, 430-455 `main` | yes | selftest run under pinned jsonschema |
| Runner regression path (1100-1296, 1296-1385) | yes | write targets, git calls, exit mapping, cwd |
| Runner sweep `run_one` (444-448), selftest `fixture_commit` (280, used from 1659) | yes | cwd/env inheritance; scope of write-capable git |

## Findings by severity

### F1 - Medium - `--workdir` PASSes over whatever legs are on disk

- `check()` derives the leg set from disk only: `legs = sorted(p.parent.name for p in workdir.glob('*/results.tsv'))` (line 305). The recorded tables from the regression stdout are parsed at 301-303 and used only per leg inside the loop at 314-316. Nothing compares the leg set with the tables or with the eight entries of `LEG_TABLE` (74).
- Probe: a workdir holding one leg directory (`js-round-gate`) and a `regression.stdout` with `REGRESSION_TABLE` lines for `js-round-gate` and `js-claims-check`:

  ```
  $ uv run --no-project --with jsonschema==4.25.1 python3 -B tools/mte-interop.py --check --workdir /tmp/c2-fx/partial-drop
  MTE_LEG js-round-gate: CONFORMS (schema=ok ... per_mutant=ok failed=none runner_pct=unavailable)
  MTE_INTEROP: PASS legs_conforming=1/1
  exit 0
  ```

  The `js-claims-check` table is silently ignored. A one-leg workdir with no stdout file exits 1 (FAIL, fail-closed). A one-leg workdir whose table matches exits 0 with `PASS legs_conforming=1/1` (`partial-pass`).
- Reach: the live mode (no `--workdir`) cannot reach this. `run_regression` raises unless the runner exits 0, and the runner exits 0 only when all eight cases pass (`mutate-and-run.sh:1365` FAIL branch, `:1371` SETUP branch). The gap is `--workdir`, which the module docstring offers for re-judging a kept workdir (lines 7-8).
- Smallest correction, inserted after line 305:

  ```python
  expected = set(LEG_TABLE)
  if set(legs) != expected or set(tables) != expected:
      raise Setup('incomplete leg coverage: legs=%d tables=%d expected=%d' % (len(legs), len(tables), len(expected)))
  ```

  Expected result on the partial-drop fixture: `MTE_INTEROP: SETUP (incomplete leg coverage ...)`, exit 2. I did not run this change; it is a proposal.

### F2 - Low (latent) - the tar guard does not contain absolute member names

- The guard at 205-206 checks `startswith('package/')` and `'..' not in Path(name).parts`. The target at 208 is `dest / member.name[len('package/'):]`. For a member named `package//tmp/x` the slice is `/tmp/x`, and `Path` joining discards `dest` when the right side is absolute. The write then lands outside the TemporaryDirectory.
- Probe (`/tmp/c2-harness/attack.py`, run on copies of the tool; the tgz is rebuilt with one extra member, and the pin is replaced only in the copy):

  ```
  VARIANT abs     pin_patched=True : RESULT {} | canary_written=['/tmp/c2-canary-abs/escape.txt']
  VARIANT abs     pin_patched=False: RAISED Setup mutation-testing-metrics-3.9.0.tgz integrity mismatch | canary_written=[]
  VARIANT dotdot  pin_patched=True : RAISED Setup unexpected tar member package/../c2-canary-dotdot/escape.txt | canary_written=[]
  VARIANT links   pin_patched=True : RESULT {} | canary_written=[]
  ```

  The `..` guard holds. Symlink and hardlink members are skipped by `member.isfile()` (207): they are not materialised, but they are not rejected either.
- Why Low: an attacker must change the vendored tgz and its source pin in the same commit. Node then runs the vendored `mutation-testing-metrics` JavaScript (lines 213-214) with the same privileges, so this adds no capability beyond a malicious vendored package. It is still a defect, because the guard claims containment and does not provide it.
- The shipped archives are clean: 93 and 17 members, all regular files, all under `package/` (read-only `tarfile` listing).
- No check-then-use gap: `verified_tarball` returns the same `raw` bytes it hashed (181), and those bytes are what gets extracted (203).
- Smallest correction, replacing the guard and the target line at 205-208:

  ```python
  rel = member.name[len('package/'):]
  if not member.name.startswith('package/') or not rel or PurePosixPath(rel).is_absolute() \
          or '..' in PurePosixPath(rel).parts:
      raise Setup('unexpected tar member %s' % member.name)
  if not (member.isfile() or member.isdir()):
      raise Setup('unexpected tar member type %s' % member.name)
  if member.isfile():
      target = dest / rel
      ...  # mkdir and write as before
  ```

  This needs `from pathlib import PurePosixPath`. A bare `package/` directory entry would now be rejected; none exist in the shipped archives.

### F3 - Low - a node timeout exits 1 instead of 2

- `subprocess.run(..., timeout=120)` (213-214) raises `subprocess.TimeoutExpired`. That is not an `OSError`, so it escapes the `except (Setup, OSError, ValueError, KeyError)` at 310 and the process dies with a traceback.
- Probe: a fake `node` that runs `exec sleep 130`, placed first on PATH, run through the real tool on the current copy:

  ```
  rc=1  secs=120.1
  stderr: subprocess.TimeoutExpired: Command '[.../node', '.../run.mjs', '.../reports.json']' timed out after 120 seconds
  stdout: (none; no MTE_INTEROP line)     temp dirs left behind: none
  ```

- Not a false PASS. But exit 1 is FAIL in the exit map (docstring line 36), so a hung node is reported as a failing gate.
- The regression subprocess (276-277) has no timeout at all. A hung sibling suite is bounded only by the runner's per-defect timeout.
- Smallest correction: add `subprocess.TimeoutExpired` to the except tuple at 310, or convert it to `Setup` inside `official_metrics`. Give the regression subprocess an explicit deadline that maps to `Setup`.

### F4 - Low - a runner FAIL is reported as SETUP (static; not executed)

- `run_regression` raises `Setup('regression exit %d')` for any non-zero runner code (281-282). The runner exits 1 when any case is out of band (`mutate-and-run.sh:1365-1368`). `check()` therefore prints `MTE_INTEROP: SETUP (regression exit 1)`, exits 2, and never prints the per-leg lines.
- Fail-closed, so not a PASS. But "a leg moved out of band" is a FAIL condition in the exit map, not a SETUP condition.
- Not executed: an out-of-band leg needs a real pinned sibling revision. The behaviour is read from code.
- Smallest correction: when the runner code is 1, print `MTE_INTEROP: FAIL (regression out of band; workdir <path>)` and return 1. Keep code 2 mapped to SETUP.

### F5 - Low - auto workdirs are left behind with no path printed; node is checked after the sweep

- `check()` creates `tameshi-mte-regression-*` (299) and removes it only on PASS (333-334). The SETUP returns (310-312) and the FAIL return (335) keep it, and no output line prints its path.
- Observed: the fleet probe on the current copy printed `MTE_INTEROP: SETUP (regression exit 2)` and exited 2, leaving `/tmp/tameshi-mte-regression-9kmqwntg` in place. It holds `regression.stdout` and the per-case directories. The first probe left `/tmp/tameshi-mte-regression-i1n1inlx` the same way.
- In the wild: five `tameshi-mte-regression-*` directories from other runs (mtimes 05:14-05:42) are still in /tmp. None matches a name my probes created, so I left them alone.
- `shutil.which('node')` is checked only inside `official_metrics` (195-197), which runs at 309, after `run_regression` (300) has already run all eight cases. A missing node therefore costs a full sweep and leaves the directory. The exit code for a missing node was observed as 2 (section 4). The ordering is read from code.
- Smallest correction: print the kept path on every non-PASS line. Move the `node` check, and the `bash` and `git` checks, before `run_regression`.

### F6 - Low (latent) - the six unsandboxed suites run in the caller's cwd and environment

- The regression subprocess (276-277) has no `cwd=` and no environment scrub. The runner's `run_one` (`mutate-and-run.sh:444-448`) does not `cd`. The only `cd`s in the regression region are the two sandboxed legs (1346, 1351). So six of the eight pinned `--selftest` suites run in whatever directory `--check` was started from, with the caller's `GIT_*` variables. Those six are js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify, bash-checklist-run and js-claims-check. The runner documents an R04 `GIT_DIR` clobber on this exact vector for its own selftest (lines 254-258).
- Probe, no sibling touched: each of the six pinned blobs was materialised with `git show <pin-rev>:<path>` and run as `bash|node <target> --selftest`. Its cwd was a one-commit scratch git repo, and HOME and TMPDIR pointed at empty scratch directories. All six exited 0, for example `SELFTEST: PASS (16 cases)`, `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)` and `CHECKLIST_SELFTEST: PASS (34 cases)`. None changed a file in cwd (including `.git`), HOME or TMPDIR. Statically, none of the six invokes git. The claims-check blob only contains the string `.git`.
- Nothing writes into a sibling at these pinned revisions. The exposure is latent: running `--check` from inside a sibling would run these suites there, and a future pinned revision that writes to cwd would do so silently.
- Smallest correction: `subprocess.run([...], cwd=str(stage), env={k: v for k, v in os.environ.items() if not k.startswith('GIT_')}, ...)`. The stage directory is private and is removed afterwards.

### F7 - informational - fixed in the final revision

- The earlier revision (`e0c5f2f3…`, line 321) computed `int(score + 0.5)` on the official `mutationScore`. When the score was null it raised `TypeError`, exited 1, and printed no summary. Reproduced with a one-leg fixture whose verdicts are all INCONCLUSIVE (`/tmp/c2-fx/allinc`).
- The final revision computes the rounding from killed and survived counts, guarded by `if rate and k + s`. The same fixture now prints `MTE_LEG js-round-gate: FAILS (...)` and `MTE_INTEROP: FAIL legs_conforming=0/1`, exit 1.

## Answers to the named questions

1. **Tar extraction path safety.** See F2. Also verified: `..` rejection works; `load_schema()` reads one named member and never writes to disk; the TemporaryDirectory is removed after success, after `Setup` (integrity and member-name failures), and after `TimeoutExpired`. Each of those runs reported no temp dirs left behind.
2. **Symlink staging: can anything write into a sibling repo?** No write path found.
   - `mte-interop.py` writes only into its TemporaryDirectory, the stage directory, the workdir and `--emit`. Siblings are only read, through git.
   - Staging creates symlinks inside the stage directory only (275). `shutil.rmtree(stage)` (279) does not follow symlinks. Probe: a symlink into a victim directory was removed, and `victim/keep.txt` survived (`survives=True`).
   - Fleet probe, with fake siblings: `kagi-shokunin` and `kumitate-shokunin` as git repos, `tameshi-shokunin` excluded by name, and `plainshoku` as a non-repo directory. Every file hash under the fleet was identical before and after the run, including each `.git`. The stage directory was gone afterwards. The runner printed `REGRESSION_TOOL: /tmp/tameshi-mte-fleet-…/tameshi-shokunin/tools/mutate-and-run.sh`. Cases resolved through the symlinks, for example `revision not found: /tmp/tameshi-mte-fleet-…/kumitate-shokunin@<rev>`, which shows the identity guard accepted the link. Absent siblings failed closed with `repo_identity_mismatch`.
   - Runner git calls in the regression path are all read-only: `rev-parse --show-toplevel` (1118), `rev-parse --verify` (1124), `cat-file -e` (1128), `show` redirected into the case directory (1133), and `ls-tree` (1142). The write-capable calls (`init`, `add`, `commit` through `git_clean`) are defined in `fixture_commit` (280) and used only from the selftest section (from 1659).
   - Runner writes stay under the workdir, case, root and specs directories (lines 1100-1296; sandboxes at 1346 and 1351). `rm -rf "$root"` (1380) runs only for an auto-created root, and Python always passes `--workdir`.
   - Git did not execute sibling-controlled commands on these read-only calls. A scratch repo with `diff.evil.textconv`, `core.fsmonitor` and `core.hooksPath` set produced no marker for `rev-parse`, `cat-file`, `ls-tree`, or `show` in the runner's shape. The four real siblings I checked carry only `filter.lfs.*` config (git-lfs).
   - The latent exposure is F6.
3. **Temp cleanup.** Verified for `official_metrics` (TemporaryDirectory removed on success, `Setup` and `TimeoutExpired`) and for the stage directory (`finally`, line 279). Leaks: F5, on SETUP and FAIL. F6 concerns the suites, not temp directories.
4. **SETUP rather than PASS for missing node or jsonschema.** Yes, see the table below.

## Exit-code evidence (section 4)

| Condition | Observed | Exit |
|---|---|---|
| jsonschema missing (`/usr/bin/python3` 3.14.8, no jsonschema) | `MTE_INTEROP: SETUP (python jsonschema not importable)`; selftest: `MTE_SELFTEST: SETUP (No module named 'jsonschema')` | 2 and 2 |
| node missing (`PATH=/tmp/c2-nonode/bin`, containing only uv and python3) | `MTE_INTEROP: SETUP (node not found)` | 2 |
| tar integrity mismatch (probe via `official_metrics`) | `Setup mutation-testing-metrics-3.9.0.tgz integrity mismatch`, nothing extracted. `check()` catches `Setup` at 310, so this maps to SETUP (code reading) | 2 (code) |
| node timeout | traceback `TimeoutExpired` (F3) | 1 |
| runner FAIL | `SETUP (regression exit 1)` by code (F4, static) | 2 |
| no ledger table (`--workdir`, no regression.stdout) | `MTE_INTEROP: FAIL legs_conforming=0/1` | 1 |
| selftest under pinned jsonschema 4.25.1 | `MTE_SELFTEST: 16/16 pass` | 0 |

## Residual risk

- The tar guard relies on the source pins for the vendored tgz. The pins match the npm registry values for 3.9.0 (read-only query). I make no authenticity claim beyond that.
- node, bash, git, timeout and uv are resolved from PATH without pinning. The tool trusts the caller's PATH.
- F6 becomes an active write if a future pinned selftest writes to cwd or calls git in cwd.
- The regression subprocess has no timeout (F3).
- `check()` reads its verdict table from the lane's runner (`recorded_verdicts((ROOT / 'tools/mutate-and-run.sh').read_text())`, line 304), but the live regression runs the staged copy. The bytes are the same today. They could drift if the staged copy ever stops being a copy of the same file.

## Verification gaps

- No live eight-leg regression was run. That would execute the eight real suites from the caller's cwd (F6), and it is a gate run, which the lane bounds exclude. The fleet probe used fake siblings, so it stopped at pin checks. The selftest-write probe covered the six pinned selftests in isolated scratch repos only.
- F4 is static only.
- F1 used a synthetic leg built from the runner's committed `TABLE_ROUNDGATE` and `TABLE_CLAIMS` verdicts. It contains no sibling content.
- Write probes observed cwd, HOME and TMPDIR only. Absolute-path writes by the pinned selftests were not traced.
- Exercised only on Linux, Python 3.14.8 and node v24.21.0.
- The lane counter command (`--check --fleet-root …`) was not run.
- Score semantics and the official metric values were not evaluated; this review covers containment, exit codes and coverage only.

## Tooling and installs

- No persistent install or upgrade. No pacman, no sudo, no partial upgrades.
- `uv` 0.13.0 (already at `~/.local/bin/uv`) ran `uv run --no-project --with jsonschema==4.25.1`. This used ephemeral environments from PyPI through uv. Reason: the lane's pinned validator, for the selftest and the probes.
- `npm view <pkg>@3.9.0 dist.integrity` for the two packages. Read-only registry queries.
- Pre-existing: node v24.21.0 (fnm), python 3.14.8 (`/usr/bin/python3`).
- I read `/home/vgpnk/.omp/agent/RULES.md` before any install decision.

## Process disclosures

- At the start I ran `python3 -S tools/mte-interop.py --check` once from the lane tree. That was a bounds deviation: the entry point should not be run in the tameshi tree. It exited at the jsonschema import guard (`MTE_INTEROP: SETUP`, exit 2) before creating any temp directory, staging, or sweep. Nothing was written there.
- Scratch lives under `/tmp` only: `/tmp/c2-harness` (probe scripts), `/tmp/c2tar-review` and `/tmp/c2tar-review2` (copies of the tool and runner), and `/tmp/c2-fx` (fixtures). Canary and leftover temp directories from my runs are removed after this report is written.
- The background-job cap blocked my first timeout probe, so I ran it synchronously in an eval cell instead.
