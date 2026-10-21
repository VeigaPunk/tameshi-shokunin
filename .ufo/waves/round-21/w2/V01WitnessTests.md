# V01WitnessTests — bash-witness-study.py selftest delta review

Verdict: **done** — review complete, 2 defects found (1 high: cleanup-mutant residue + verdict masking; 1 high: missing falsifiers on monkeypatch/env restore), 3 confirmed kills, production guards byte-identical, pristine run green.

Target: `tools/bash-witness-study.py` @ `790abd2129f153c13b471e381d454186edbde65e` vs `33d03b7`. Delta = 1 file, +41/−6, commit `370f2df`, every hunk inside `cmd_selftest` (line numbers below are @790abd2).

## Commands actually run (all in private clone, GIT_* scrubbed from env)

- Clone: `/tmp/tameshi-r21-V01WitnessTests/clone` @ `790abd2` (local `git clone --no-hardlinks` from live repo; read-only corpus symlink; **byte-restored to pristine after mutants, asserted**). Live repo untouched; no production edits.
- `git diff --stat 33d03b7 790abd2 -- tools/bash-witness-study.py` → 1 file changed, 41(+)/6(−).
- `python3 tools/bash-witness-study.py selftest` → **exit 0, `WITNESS_SELFTEST: 51/51 pass`, `VERDICT: PASS`, /tmp residue before=0 after=0**.
- Five single-mutant probes (textual replacements, each uniquely anchored, applied+run+reverted):
  - **A cleanup-disabled** (both `shutil.rmtree(...)` in the `finally` → `pass`): exit 1, check `private root is removed` FAIL, then **`OSError: [Errno 39] Directory not empty: '/tmp/bash-witness-selftest-private.tzv00fc4'`** — no `WITNESS_SELFTEST`/`VERDICT` lines printed, **residue after=1** (left in /tmp; I removed it).
  - **A2 private-sweep-only** (only the private_root rmtree removed): exit 1, `50/51`, `VERDICT: FAIL`, residue 0 (empty leftover cleaned by `rmdir`).
  - **B envscrub-removed** (`git_clean_env` filter → `dict(os.environ)`): exit 1, `48/51`, `VERDICT: FAIL` — three checks fire: `scrubs inherited repository selectors`, `GIT_DIR/GIT_WORK_TREE cannot redirect materialization`, `... sweep` (defense in depth).
  - **C init-hooks-pin-dropped** (`-c core.hooksPath=/dev/null` removed from init call only): exit 1, `50/51`, `VERDICT: FAIL` — `fixture init pins hooks off` fires alone. Real argv inspection (`patch.object(subprocess, "run", wraps=...)`), **not sourcegrep**.
  - **D patch-restore-deleted** (`globals()["RUNNER"] = saved_runner` + `shutil.which = saved_which` deleted from inner `finally`): **exit 0, 51/51, `VERDICT: PASS` — SURVIVES.**
  - **E saved_env-restore-deleted** (the `saved_env` pop/restore loop deleted): **exit 0, 51/51, `VERDICT: PASS` — SURVIVES.**
- Guard identity check: `git_clean_env`, `sweep_env`, `materialize_target`, `run_sweep` function bodies **byte-identical** 33d03b7→790abd2. No `__file__` source-read anywhere in `cmd_selftest` (0 hits) — no sourcegrep checks; failing-path checks exercise true behavior (`SystemExit` 64 from parser, `EXIT_FAIL` from `cmd_check`, named `Fail`/`Cannot`).

## Findings

### HIGH-1 — cleanup mutant leaves scratch residue and an OSError masks the verdict (lines 1708–1710)

```python
check("private root is removed", not private_root.exists())
if private_root.exists():
    private_root.rmdir()
```

Empirically (mutant A): when both `finally` rmtree calls are removed, the residue tree is non-empty, so `rmdir()` raises `OSError: [Errno 39] Directory not empty` and (a) the scratch dir `/tmp/bash-witness-selftest-private.*` is **left behind** — violating the stated acceptance "cleanup mutant leaves no scratch residue" — and (b) the uncaught traceback replaces the `WITNESS_SELFTEST: n/m pass` / `VERDICT: FAIL` diagnostics (mutant is still killed by exit≠0, but blind). The partial-cleanup mutant (A2) is fine: empty leftover, `rmdir` succeeds, clean 50/51 FAIL. Fix direction: replace the `rmdir()` fallback with `shutil.rmtree(private_root, ignore_errors=True)` and/or print the summary before the residue check so the verdict survives any post-finally failure. Same failure shape occurs if a legitimate transient makes `rmtree` skip a file (check FAIL → crash instead of verdict).

### HIGH-2 — no falsifier pins restoration of monkeypatches / hostile env (lines 1357–1364)

The delta adds env-scrub and argv-pin contract checks but nothing observes the *restore* side. Mutants D and E both survive 51/51 PASS:
- D: process-global `RUNNER` keeps pointing at the scratch `probe_runner`; the later `sha256_file(RUNNER)` in the `cmd_check` fixture silently digests the probe (still on disk inside `root`), and after cleanup `RUNNER` is left dangling for the rest of the process. `shutil.which` stays patched.
- E: hostile `GIT_DIR`/`GIT_WORK_TREE` (pointed at the canary) remain exported in `os.environ` after the containment section — exactly the state that section exists to disprove.

Both are surviving mutants = missing kills on the "restoring monkeypatches" axis. Fix direction: after the restore `finally`, `check` that `RUNNER is saved_runner` (compare to the pre-saved value), `shutil.which is saved_which`, and `os.environ.get` for the three keys matches `saved_env` (absent-or-original). Cheap, kills D and E outright.

### Confirmed kills / agreements

- `private child is contained` (1248) pins the `mkdtemp(dir=private_root)` argument: a `dir="/tmp"` mutant flips `root.parent` and fails by construction (logic-conclusive; not separately executed).
- Env-scrub check (1282–1297) is behavioral: `patch.dict` really injects hostile selectors and `git_clean_env` (333–339) really drops the whole `GIT_*` namespace; removal is caught by three independent checks (B).
- Argv-pin check (1300–1312) is real subprocess capture, not sourcegrep; kills the hooks-pin drop (C).
- New cleanup check (1708) kills the private-sweep removal with a clean verdict (A2).
- Failing cases are true exit-1 behaviors (parser `SystemExit` 64, `cmd_check` `EXIT_FAIL`, `Fail`/`Cannot`), matching "true exit1 failing cases not sourcegrep".
- Production guards unchanged: all four guard functions byte-identical across the delta.

### LOW

- Argv-pin filter `if operation in call.args[0]` (1305) is substring matching over the whole argv. Safe today (`TARGET_GIT_PATH = "corpus/surface-census.sh"` line 98; repo name `command-pin-fixture`; message/user pins contain no `init`/`add`/`commit` substrings), but any future rename introducing one of those substrings into the path or name breaks `len(commands) == 1`. Positional match (`argv[i] == operation` right after `git`/`-C value`) would be robust.
- The residue check, `rmdir`, summary and verdict (1708–1715) sit after the `finally`: on a hard exception anywhere in the try body they are skipped (cleanup still happens, but the new cleanup check and diagnostics are only exercised on the success path). Consistent with pre-delta behavior; noting as a gap, not a regression.

## Residual risk / verification gaps

- Containment `dir="/tmp"` mutant asserted by logic, not executed. Partial-restore mutants (e.g., only `RUNNER` or only `which` restored) not separately run — same class as D/E, same fix covers them. `GIT_CONFIG_NOSYSTEM`/`GIT_CONFIG_GLOBAL` semantics assumed per the pinned env contract (values checked, not git-version behavior). All runs single-host Linux; `/tmp` residue measured only at `/tmp/bash-witness-selftest*`.
- Tooling: no installs or updates performed (report per operator directive 2026-10-19: none needed; python3/git/bwrap preexisting).
