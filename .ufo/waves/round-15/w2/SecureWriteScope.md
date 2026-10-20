# SecureWriteScope: check/selftest write confinement (sentinel, leaf, wave 2)

Seat: `TameshiR15.SecureWriteScope`. Static review only. I executed nothing: no gate, no selftest, no probe, no git, no sha256sum. Tool installs or updates: none. I accessed no credentials and no agent DB.

## Exact source read

- `tools/context-capture.py` snapshot `#472A` (2116 lines), the delivered wave-1 code.
  - Read in full: `:1-363`, `:1218-1350`, `:1569-2116`.
  - Whole-file grep for every write or path sink: `open(`, `write`, `makedirs`, `mkdtemp`, `rmtree`, `unlink`, `rename`, `replace(`, `symlink`, `chmod`, `os.remove`, `subprocess`, `DEFAULT_LANE_ROOT`, `FROZEN_RECEIPT_REL`, `TMPDIR`, `tempfile.`, `realpath`, `capture-context`, `round-15`, `FROZEN_TOOL_SHA256`, `*_REL`.
  - Not read line by line: `:364-1217` and `:1351-1568`. They are covered for write sinks only by the grep above. Their hits are literal `*_REL` strings used as data (`:225-228`, `:651-654`, `:1401`, `:1462-1542`) and one constant comparison (`:1175`).
- `SKILL.md:1681` (the registry write-scope cell) and `:62`, `:68-72` (the hermetic standard).
- `.ufo/waves/round-15/w1/TempScope.md` F6/F7 (wave-1 recommendations).
- `corpus/lessons/round-14-verifier-spotcheck.md:154-162` (Routed defects 1-5).
- `AGENTS.md`.

## Bounded agreement

### Check mode never writes a file

- **`--check` writes to stdout only.**
  - It has two file opens. `read_regular` (`:342`) uses mode `"rb"`, after `os.stat` and an `S_ISREG` check. `tool_sha256` (`:302`) reads SELF with mode `"rb"`.
  - The only writes are `sys.stdout.write` in `emit` (`:1250-1261`) and the usage text on stderr (`:2089-2092`).
  - No `makedirs`, `replace`, `rename`, `unlink` or `mkstemp` is reachable from `run_check` (`:1298-1344`) or `main` (`:2083-2112`).
- **Frozen mode opens only the round-14 receipt, read-only.**
  - It opens only `DEFAULT_LANE_ROOT/.ufo/evidence/round-14/context-receipt.json` (`:1301-1302`), with `"rb"`.
  - `DEFAULT_LANE_ROOT` is `dirname(dirname(realpath(__file__)))` (`:122-123`). This is the two-level form, so the wave-1 four-dirname hazard (TempScope F1) is absent.
- **The historical script is never touched.**
  - `capture-context.py` appears only in the docstring (`:10`).
  - `FROZEN_TOOL_SHA256` is compared to the receipt's recorded field (`:1175`). The script is never opened, imported or run.
  - Nothing names `.ufo/evidence/round-15/`. There is no capture mode, so "never overwrite round14" holds structurally.
- **No bytecode is written.** No lane module is imported: the imports are stdlib only (`:108-117`). The script runs as `__main__`, and `sys.dont_write_bytecode = True` (`:119`). Selftest children run `python -I SELF` (`:1638`, `:1686`).

### Selftest writes stay inside its own mkdtemp root

- **Each write goes into a fresh case directory.**
  - The root is created by `tempfile.mkdtemp(prefix="context-capture-selftest-")` (`:1581`), which gives a fresh directory with mode 0700.
  - Case directories are `os.makedirs(root/NN-<literal name>)` (`:1587-1591`).
  - Fixture writes are `open(case/receipt.json,"wb")` and `open(case/expected.json,"w")` (`:1622`, `:1634`), always in a case directory created just before.
  - So no pre-existing file, historical or otherwise, can be opened for writing.
- **Children run check mode only, so they write nothing.**
  - Every child gets an explicit `--receipt` and `--expected` (`:1638-1639`), so no case reaches frozen mode or the live lane receipt.
  - Usage cases (`:1996-2002`) exit 64 in `parse_argv` before any file I/O.
  - Child settings: `env=SELFTEST_ENV` (only PATH, LC_ALL and a poison GIT_DIR), `stdin=DEVNULL`, `timeout=60`, `cwd=` the case directory (`:1602-1606`).
- **Cleanup is covered for Python-level exits.**
  - `rmtree(root)` runs in both `finish()` and the `finally` block (`:1717`, `:2017`).
  - `except Exception` maps a setup error to exit 2 (`:2010-2014`).
  - `KeyboardInterrupt` still reaches `finally`.
  - A `TimeoutExpired` from `subprocess.run` kills the child and then hits `except Exception`.

## Findings

### W1: MEDIUM (conditional on caller env). The selftest temp root follows ambient `TMPDIR`, and the lane-leak assertion turns itself off in exactly that case

- **Evidence.**
  - `:1581` uses a bare `mkdtemp(...)` with no `dir=`, so the root honours the parent's `TMPDIR`. The parent's env is not sanitised; only the children get `SELFTEST_ENV`.
  - `:1701-1703` sets `lane_leak = any(DEFAULT_LANE_ROOT in text ...) if DEFAULT_LANE_ROOT not in self.root else False`.
  - Wave-1 `TempScope.md` F6 named this exact path and gave the fix `mkdtemp(..., dir="/tmp")`. The delivered code did not adopt it.
- **Concrete counterexample (static trace, not executed).**
  - Run `TMPDIR=<lane>/.ufo/evidence/round-14 python3 tools/context-capture.py --selftest`.
  - The root becomes `<lane>/.ufo/evidence/round-14/context-capture-selftest-XXXXXXXX/`.
  - About 37 `NN-<case>/{receipt.json,expected.json}` trees are created inside the frozen round-14 evidence directory.
  - Every child's JSON names a receipt path that contains `DEFAULT_LANE_ROOT`. The leak check would catch that, but `DEFAULT_LANE_ROOT in self.root` is true, so the check is skipped.
  - `hermetic-no-lane-path` therefore records `OK`, `hermetic-temp-only` records `OK` (its regex only checks names inside the root), and the run ends `SELFTEST: PASS`.
- **Impact.**
  - No historical byte is overwritten, because every file is created fresh in new directories.
  - The selftest does write into the historical evidence tree, and the round-14 directory's mtime changes.
  - If the parent is killed by SIGTERM or SIGKILL (for example an outer runner timeout), Python's `finally` does not run. The fixture tree then persists inside `.ufo/evidence/round-14/` and dirties `git status`.
  - The hermetic PASS is credited in exactly the configuration that violates the registry's write scope ("selftest isolated temporary fixtures only", `SKILL.md:1681`) and the "no live-tree write" standard.
  - This is a false-readiness assertion, not just missing hardening.
- **Smallest remediation.**
  - Use `tempfile.mkdtemp(prefix="context-capture-selftest-", dir="/tmp")`.
  - Delete the `if DEFAULT_LANE_ROOT not in self.root else False` bypass, so the leak check always runs.
  - Or, without the `/tmp` pin: take `realpath(self.root)` and refuse with a setup error (exit 2) when `os.path.commonpath([root, realpath(DEFAULT_LANE_ROOT)]) == realpath(DEFAULT_LANE_ROOT)`.

### W2: LOW (honesty). `hermetic-temp-only` cannot observe writes outside the temp root

- **Evidence.** `:1708-1716` lists only the top-level entries of `self.root` and matches them against `\d{2}-[a-z0-9-]+`.
- **Why it is vacuous.** Those entries are created only by `case_dir` with literal names (`:1589`), so the check can never fail. It observes nothing outside the root, including the lane, round-14 or `/tmp` siblings.
- **Impact.** The case name overstates what it proves. The real write confinement rests on the source structure argued above, not on this assertion.
- **Smallest remediation.** Either rename it to describe what it does, e.g. `temp-root-entries-expected`, or drop the case. Do not cite it as hermetic proof in the registry or claims.

### W3: LOW (residual, disclose only). A killed parent leaves the fixture tree behind

- **Evidence.** Under SIGTERM or SIGKILL, the `finally` at `:2016-2017` does not run.
- **Impact.**
  - With the default `/tmp` root, a stray `context-capture-selftest-*` directory is left in `/tmp`. It contains only synthetic fixtures and no secrets.
  - The residue lands inside the lane only together with W1.
- **Remediation.** None needed beyond W1. Disclose it as a residual.

## Not claimed

- No execution result. The W1 counterexample is a static trace of the source above.
- Not claimed: that L1's runner sets `TMPDIR`. `.ufo/evidence/round-15/verify.py` had no `TMPDIR`, `tempfile` or `env=` hits in my grep.
- No review of read containment, symlinks or FIFOs (SecureSymlinkScope's seat).
- No review of secrets or env capture (SecureSecrets' seat).
