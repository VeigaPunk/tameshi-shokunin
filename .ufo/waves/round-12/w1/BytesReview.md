# BytesReview — exact-bytes comparison boundary (round 12, w1)

Seat: BytesReview (reviewer). Advisory, lane-internal. No independent authority. Observed results below are the seat's own runs against the published gate; they are not an admission or a non-author verification.

Gate under test: `tools/repeat-control.py`, sha256 `d45d8e3948c24c2f6b2afcc336a5a44d2119e66b32eaea9fbe5c9eb08807d17d`, python 3.14.7 (recorded in each `cli/<case>/command.txt`). No production edits by this seat.

## Scope and method
Axes: (a) boundary coverage of the byte-compare contract, (b) silent false-pass risk, (c) reproducibility of the evidence.
Tooling: no install or upgrade performed. Present and used: Python 3.14.7, `/usr/bin/cmp`, `/usr/bin/diff`, `sha256sum`.

Two layers were probed:
1. **Primitive layer** (before the gate existed): stdlib subprocess/shell behaviour that a comparison would rest on. Scripts in `.ufo/evidence/round-12/BytesReview/probe*.py`, outputs `probe*.out`.
2. **Gate layer** (after `tools/repeat-control.py` was published): 20 CLI cases run as `python3 tools/repeat-control.py --runs 3 --out <fresh dir> -- <argv>`, plus byte-fidelity checks on the saved `run-<k>.*` files and usage/setup arms. Evidence: `.ufo/evidence/round-12/BytesReview/cli/<case>/` (`command.txt`, `run-{1,2,3}.{stdout,stderr,exit}`, `finding.txt`).

## Primitive-layer evidence (observed)

`probe.out`: 13 cases, `PROBE_FAILURES=0`.

| Case | stdout / stderr pair | Observed | Expected |
|---|---|---|---|
| T1 trailing newline | `x\n` vs `x` | stdout DIFFER | DIFFER |
| T2 CRLF vs LF | `x\r\n` vs `x\n` | stdout DIFFER | DIFFER |
| T3 empty vs newline | `` vs `\n` | stdout DIFFER | DIFFER |
| T4 empty vs empty | `` vs `` | MATCH | MATCH |
| T5 trailing space | `a ` vs `a` | DIFFER | DIFFER |
| T6 NUL vs empty | `\0` vs `` | DIFFER | DIFFER |
| T7 NUL in middle | `a\0b` vs `ab` | DIFFER | DIFFER |
| T8 NUL at tail | `a\0b` vs `a\0c` | DIFFER | DIFFER |
| T9 invalid UTF-8 | `\377` vs `\376` | DIFFER | DIFFER |
| T10 stderr-only | stdout same; stderr `e1` vs `e2` | stdout MATCH, stderr DIFFER | DIFFER(stderr) |
| T11 stdout-only | stdout `a` vs `b`; stderr same | stdout DIFFER, stderr MATCH | DIFFER(stdout) |
| T12 identical | both streams identical | MATCH | MATCH |
| T13 stderr empty vs newline | `` vs `\n` (stderr) | stderr DIFFER | DIFFER(stderr) |

Traps (false passes a gate must not use), `probe.out` trap section:
- `.strip()` equality reports equal for T1, T2, T3.
- Truthiness equality reports equal for T1, T2, T7, T9.
- Bash `$(...)` capture reports equal for T1, T3, T6, T7 (trailing newlines and NUL bytes are dropped).
- `text=True` universal newlines (`probe2.out` P1/P2): `x\r\n` → `x\n`; lone `\r` → `\n`. Strict UTF-8 decode of `\xff` raises `UnicodeDecodeError` (P3): text mode either false-passes or crashes.

Process/availability/pipe boundaries (`probe2.out`, `probe3.out`, `probe4.out`):
- P4: SIGKILL child → returncode `-9`; shell `$?` 137.
- P5: missing binary → `FileNotFoundError` (errno 2); non-executable file and directory argv[0] → `PermissionError` (errno 13). An uncaught exception exits Python with 1.
- P6: child exit 64 is returned as data, not as the caller's exit.
- P7: `cat` with `stdin=DEVNULL` → `b""`.
- P8 (`probe3.out`): sequential `stdout.read()` then `stderr.read()` on 400 000 + 400 000 bytes deadlocks (8 s alarm fired; `probe2` re-run under `timeout 30` returned rc 124). `communicate()`/`run(capture_output=True)` completes with exact sizes (P9).
- P10: NUL in argv → `ValueError: embedded null byte` (NUL-bearing cases must come from files or stdin).
- P11/P12 (`probe4.out`): `wb`/`rb` round-trip of `a\r\n\0\xff\n` is byte-equal; text-mode readback differs.

Note on `probe2.out`: it was written from in-session output because the probe2 process (which contains the deliberate P8 deadlock) did not complete cleanly under the harness; P1–P7 are the observed values.

## Gate-layer evidence (observed, `cli/`)

All 20 cases returned the expected finding ID and exit (`TOTAL 20 UNEXPECTED 0`).

| Case | Runs | Observed ID | Exit | Expected |
|---|---|---|---|---|
| C01 stable `printf 'x\n'` | 3 | controls_match | 0 | match |
| C02 `x\n` then `x` ×2 | 3 | controls_mismatch | 1 | mismatch (no normalization) |
| C03 `true` stable (empty) | 3 | controls_match | 0 | match |
| C04 `true` then `echo` ×2 | 3 | controls_mismatch | 1 | mismatch (empty ≠ newline) |
| C05 `printf 'a\0b'` stable | 3 | controls_match | 0 | match |
| C06 `a\0b` then `ab` | 3 | controls_mismatch | 1 | mismatch |
| C07 stderr `e1` then `e2` ×2 (stdout same) | 3 | controls_mismatch | 1 | mismatch on stderr alone |
| C08 exit 0,0,1 | 3 | controls_mismatch | 1 | mismatch |
| C09 `exit 1` stable | 3 | baseline_nonzero | 2 | could-not-evaluate |
| C10 identical stdout+stderr, exit 3 | 3 | baseline_nonzero | 2 | could-not-evaluate |
| C11 `kill -9 $$` | 3 | baseline_nonzero | 2 | could-not-evaluate (exit file `-9`) |
| C12 child `exit 64` stable | 3 | baseline_nonzero | 2 | child 64 does not become gate exit 64 |
| C13 child `exit 127` stable | 3 | baseline_nonzero | 2 | child 127 is a baseline, not unavailable |
| C14 `/nonexistent/xyz-bytesreview` | 3 | command_unavailable | 2 | could-not-evaluate (exit file `unavailable`) |
| C15 non-executable file (mode 644) | 3 | command_unavailable | 2 | could-not-evaluate (no traceback, no exit 1) |
| C16 directory as argv[0] | 3 | command_unavailable | 2 | could-not-evaluate |
| C17 ENOEXEC (no shebang, mode 755) | 3 | command_unavailable | 2 | could-not-evaluate |
| C18 `cat` (stdin isolation) | 3 | controls_match | 0 | saved stdout empty |
| C19 400000 B stdout + 400000 B stderr | 3 | controls_match | 0 | no hang; saved sizes exact |
| C20 stderr-only `\n` stable | 3 | controls_match | 0 | stderr `\n` preserved |

Byte-fidelity checks on saved files (all PASS): C02 `run-1.stdout == b'x\n'`, `run-2.stdout == b'x'`; C05 `run-1.stdout == b'a\0b'`; C07 `run-2.stderr == b'e2\n'`; C04 `run-1.stdout == b''`, `run-2.stdout == b'\n'`; C11 `run-1.exit == '-9\n'`; C14 `run-1.exit == 'unavailable\n'`; C18 saved stdout empty; C19 sizes 400000/400000; C20 `run-1.stderr == b'\n'`.

Usage/setup arms (all exit 64 `invalid_usage`, no run directory created): `--runs 2`; `--runs 0`; `--runs abc`; missing `--`; empty command after `--`; `--out` already existing (refused, `C01-stable-newline`); no arguments. The `--runs 2` and `--runs 0` arms emit `must be >= 3`.

## Findings (status after observation)

- **R1 (was high; now closed by observation).** Non-executable path and directory argv[0] return `command_unavailable` exit 2 (C15, C16); no traceback exit 1 was observed. Residual: the guarantee depends on `run_once` catching `OSError`; any exception raised outside that path (e.g., `write_new` failure) is routed through `setup_failure` → exit 2 per the code, not separately exercised here.
- **R2 (was high; verified).** The gate does not normalize: T1/T2/T3/T6/T7-shaped pairs are `controls_mismatch` (C02, C04, C06). The primitive traps above are NOT present in the gate's comparison path.
- **R3 (was high; verified).** Dual-stream 400 KB output completes (C19); the gate uses `subprocess.run` (communicate semantics), not sequential reads.
- **R4 (medium; verified).** Signal baseline → exit 2 `baseline_nonzero` with exit file `-9` (C11).
- **R5 (was medium; resolved in code, partly observed).** Precedence is written in the gate docstring and `classify()`: unavailable → mismatch → nonzero baseline → match. Observed: `[0,0,1]` → mismatch (C08); `[1,1,1]` identical → baseline (C09, C10). Not run: `[0,1,0]`-shape as a separate case (covered by the same `classify()` branch as C08, but not independently exercised).
- **R6 (documentation; verified in source).** Docstring states that `controls_match` means N observations agreed on this host and "is not a determinism proof and cures no flakiness". Not a defect; the wording must be preserved in any downstream report.

## Residual risks and gaps (named, not hidden)
- No timeout. A hanging control hangs the gate (documented in the docstring; a `timeout` wrapper at the call site is the stated mitigation). Not exercised here.
- A background writer left by the command can append to a run file after its run ended (documented). Not exercised.
- Volatile stdout (timestamps, PIDs) produces `controls_mismatch`. This is intended per Main (strict byte equality). It is also the reason a `controls_match` on a volatile command is only observed sample stability.
- Platform: Linux, glibc, python 3.14.7, `/bin/sh`. Not verified elsewhere.
- The gate's own `--selftest` and `--snapshot` modes were not run by this seat (ControlGate's and SnapshotReview's assignments).
- Probe scripts used `/tmp/bytesreview/` for scratch (fixtures `noexec.txt`, `noexec_nosheb.sh`, counter files); copies of the scripts are in the evidence directory except the counter scripts in `/tmp/bytesreview/cli-scripts/`.

## Owned paths
- Report: `.ufo/waves/round-12/w1/BytesReview.md` (this file).
- Evidence: `.ufo/evidence/round-12/BytesReview/` — `probe.py`, `probe2.py`, `probe3.py`, `probe4.py`, `probe.out`, `probe2.out`, `probe3.out`, `probe4.out`, `cli/C01…C20/` (20 case directories, each with `command.txt`, `run-{1,2,3}.{stdout,stderr,exit}`, `finding.txt`), and usage-arm outputs remain stdout/stderr only (no directories created).
- No production files written. No edits to `tools/`, `LOG.md`, or sibling seats.

## Checks for the main agent to run
- Re-run the 20-case table against the same gate sha `d45d8e39…` and compare IDs/exits; a changed gate sha invalidates these observations.
- Confirm `cli/` case directories are intended to be committed (they are evidence for the round-12 BytesReview seat only; not an independent verdict).
