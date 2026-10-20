# Round 15 wave 2 — ReviewSelftestIsolation (C1 context gate)

Role: leaf member, static review only. Author-side advisory; not admission authority.
Target: selftest temp-fixture isolation for `tools/context-capture.py` and its round-15 registry row.

## Execution boundary

- No checks, builds, tests, `--selftest`, `--check`, or sibling gate was executed.
- No subprocess, network, or live-root read was performed by this seat.
- One directory listing was taken (`tools/**/__pycache__`, gitignore off): no files found.
- Tool installs/updates: none. No pacman transaction.

## Source read (exact)

- `tools/context-capture.py`: lines 1–123 (header, imports, constants), 124–363 (constants, read helpers), 300–305 (`tool_sha256`), 330–349 (`read_regular`), 480–491 (lane/fleet string checks), 805–846 (environment re-derivation), 1212–1216 (`load_expected`), 1221–1296 (`make_result`, `emit`, `apply_expected`), 1298–1344 (`run_check`), 1347–1603 (fixtures, `SELFTEST_ENV`, `SelftestHarness.__init__`/`case_dir`/`run`/`check_case` head), 1602–1733 (run/check/usage/finish), 1727–2003 (all selftest case registrations), 2005–2017 (`run_selftest` with `finally`), 2020–2116 (`parse_argv`, `main`).
- Whole-file grep for `os.path.|open(|os.stat|os.listdir|mkdtemp|tempfile|subprocess|os.environ|SELF|DEFAULT_LANE_ROOT|FROZEN_RECEIPT_REL|__pycache__`.
- `SKILL.md:1680` (round-15 gate registry row, raw), `SKILL.md:1649–1671` (retained-check semantics and exit classes), `SKILL.md:62` (hermetic suite standard).
- `corpus/lessons/round-14-verifier-spotcheck.md` routed defect 5 (lines 160–161): gate classification, registry, standalone self-invocation, exit64 mapping. Only the isolation-relevant part was checked.
- `AGENTS.md`, `~/.omp/agent/RULES.md` (tooling directive only).

## Findings (by severity)

### F1 — medium: lane-root leak check is disabled exactly when the temp root sits inside the lane

- `tools/context-capture.py:1581` — `tempfile.mkdtemp(prefix=...)` honors the ambient `TMPDIR`/`TMP`/`TEMP` (the harness is not run under `SELFTEST_ENV`).
- `tools/context-capture.py:1701–1707`:
  `lane_leak = any(DEFAULT_LANE_ROOT in text ...) if DEFAULT_LANE_ROOT not in self.root else False`
  The `else False` branch is taken whenever `self.root` contains the lane root, and the record is then `hermetic-no-lane-path` OK with the text "default lane root absent from subprocess output".
- Concrete counterexample (static reading; not executed): `TMPDIR=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.scratch python3 tools/context-capture.py --selftest`. Every `receipt.json`/`expected.json` lands under the lane tree, and every JSON `receipt.path` echoes that lane path (`make_result` line 1234). The check still records PASS and its printed label is false.
- Fix: if `DEFAULT_LANE_ROOT in self.root`, record the check as FAIL (refuse to run hermetically in-lane) instead of exempting it. Do not compare outputs against a root that is itself under the lane.

### F2 — low-medium: the "no live lane path read" claim is not literally true; the tool reads its own live source

- `tools/context-capture.py:302` — `tool_sha256()` opens `SELF`, which is `realpath(__file__)` (line 122), i.e. the live `tools/context-capture.py` inside the lane.
- `tools/context-capture.py:1227` — `make_result` calls `tool_sha256()` on every result path. Every `check_case` subprocess that reaches `run_check` therefore reads the live file. `check_case` is invoked 31 times (lines 1737–1994), so 31 live self-reads per selftest run.
- The docstring at lines 26–28 says "No live lane path is read or written". Registry `SKILL.md:1680` says "check reads receipt bytes only". Both overstate: the tool also reads the expected pin (`load_expected`, 1212–1216) and its own source (302).
- The finish check at 1701–1703 cannot detect this, because it inspects only stdout/stderr text and the hash is not a path.
- Fix options: (a) run selftest against a copy of the tool placed under the temp root, so `SELF`/`DEFAULT_LANE_ROOT` resolve inside the temp tree; or (b) narrow the docstring and registry wording to "reads no lane input other than its own source bytes".

### F3 — low: `hermetic-no-lane-path` is text-only and cannot exercise the frozen path

- `tools/context-capture.py:1702` checks only `self.outputs`.
- Frozen mode (`run_check` 1300–1302, 1318: reads `DEFAULT_LANE_ROOT/.ufo/evidence/round-14/context-receipt.json`) is never executed by selftest. `check_case` always passes `--receipt` (1638–1639). The usage cases that omit `--receipt` (1996–2002) fail in `parse_argv` (2069–2080) before any read.
- So the live frozen read is simply not covered, and a live read that does not echo its path cannot fail the check. The control verifies absence of an echoed path only.
- Fix: narrow the registry/docstring wording to "output-text check only", or accept the gap explicitly. Do not add a frozen-mode selftest case, because that would itself be a live read.

### F4 — low: temp-root cleanup and per-case contents are not verified

- `tools/context-capture.py:1717` and `2017`: `shutil.rmtree(..., ignore_errors=True)`. Nothing after removal checks that `self.root` still exists, so a silent failed removal still yields `SELFTEST: PASS`.
- `tools/context-capture.py:1708–1716`: `hermetic-temp-only` lists only the top-level entries of `self.root` against `\d{2}-[a-z0-9-]+`. It does not check the contents of each case directory. A subprocess that wrote an extra file into a case directory (e.g. `receipt.json.tmp` or `out.json`) passes. The docstring's "check mode writes nothing" (line 12) is therefore not pinned.
- Fix: after `rmtree`, record a check that `self.root` no longer exists; and per case, assert the directory contains exactly the files the harness wrote.

### F5 — low (coverage residual, temp-only): the non-regular-file guard has no fixture

- `tools/context-capture.py:339–340`: `stat.S_ISREG` check before `open`. No selftest case exercises a FIFO, directory, or symlink receipt. If the guard were removed, a FIFO receipt would block the child until its 60 s `timeout` (`run`, line 1605), which the harness reports as a setup error (2014), not as a fixture-level failure. The fixture would have to be created inside the temp root, so this is coverage, not a live read.

## Bounded agreements (static, no execution)

- No `__pycache__` source: the script imports only stdlib modules (lines 108–117); `sys.dont_write_bytecode = True` (119) is set before any code; children run the script as `__main__` under `-I` (1638, 1686). Glob of `tools/**/__pycache__` returned nothing.
- Environment: the tool never reads `os.environ` (grep, no hits). Children run with `SELFTEST_ENV` (1572–1576, 1604) plus `-I`. The only ambient-env dependence is `tempfile.mkdtemp` (see F1).
- Explicit-mode recomputation is string-only: `lane_root`/`fleet_root` are compared as strings (480–491); `recompute_sources` (1017–1036) compares declared digests, not disk bytes. The only filesystem reads in explicit mode are the receipt, the expected pin, and SELF (F2).
- Every `check_case` and `usage_case` writes only under `self.root` (`case_dir` 1587–1591, `check_case` 1615–1636); fixture lane/fleet strings (`/fixture/lane`, `/fixture`, 1398–1399) are literals that the tool never resolves against disk.
- `run_selftest` removes the root in `finally` (2016–2017) and returns 2 on setup error (2008–2014).

## Residual risk and verification gaps

- No selftest, check, or live read was executed; every statement above is a source reading with line citations. Counterexamples in F1 and F3 are static predictions, not observed results.
- F1 depends on the operator's ambient `TMPDIR`; the default `/tmp` does not trigger it.
- Hermeticity claims in SKILL.md:62 and the round-15 registry remain author-side advisory until the L1 runs `--selftest` once after wave 2.

## Messages to TameshiR15

F1 and F2 were sent as implementation-critical defects (the lane-root check and the live self-read claim).
