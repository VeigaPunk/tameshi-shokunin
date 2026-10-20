# ControlFlow — repeat-control run/classify review (round-12 w2)

Seat: TameshiR12.ControlFlow (reviewer, read-only, advisory). No edits, no checks run, no tools installed.
Scope: `tools/repeat-control.py` (790 lines, read in full), plus read-only listings of `.ufo/evidence/round-12/ControlGate/` and `.../mismatch/`.
Method: static reading only. Items marked [INFERENCE] are deduced from code and were not executed.

## Requested evaluations

**Sequence [0,1,0] → controls_mismatch, exit 1. Correct.**
`classify` (`tools/repeat-control.py:191-205`) compares each record's `(exit_text, stdout, stderr)` tuple against record 1 at `:196-202`. Record 2 has `exit_text="1"`, so the tuple differs and `controls_mismatch` is returned before the baseline check at `:203`. `run_controls` then prints `identical=no` (`:320-321`). This matches the docstring at `:30-34`.
Gap: no selftest fixture produces `[0,1,0]` (see F6).

**Nonzero-baseline precedence. Order is correct; coverage is thin.**
Order in `classify`: unavailable (`:193-194`) → any disagreement (`:195-202`) → nonzero baseline (`:203-204`) → match (`:205`).
- `[1,1,1]`, `[7,7,7]`, stable signal death → `baseline_nonzero` 2. Correct.
- `[1,0,0]`, `[1,2,1]` → `controls_mismatch` 1, because disagreement is checked before the baseline. Correct by reading.
- Selftest covers only uniform nonzero (`NONZERO_SH` `:487-491`, `CHILD127_SH` `:493-498`; cases `:650-651`). No disagreeing-nonzero-first fixture exists (see F6).

**Missing or non-executable command → command_unavailable 2. Correct for ENOENT, EACCES, ENOEXEC, and directory argv0.**
`run_once` (`:264-294`) catches `OSError` around `subprocess.run(shell=False)` (`:273`). It sets `available=False` and `exit_text="unavailable"` (`:274-277`), and stores the OSError text in `run-k.stderr` (`:276`). `classify` `:193-194` returns `command_unavailable` before any comparison. Python does not fall back to `/bin/sh` on ENOEXEC, so that case also raises `OSError` and is classified correctly. A mid-sweep availability change (available then unavailable) also yields `command_unavailable`, because precedence 1 wins. All N runs still execute after an unavailable run. That is wasteful but not incorrect.

## Findings by severity

### F1 — HIGH — Committed snapshots have no `expected.json`; the documented gate cannot validate them
- Evidence: `.ufo/evidence/round-12/ControlGate/` contains only `run-{1,2,3}.{stdout,stderr,exit}` and the `mismatch/` subdirectory. `.../ControlGate/mismatch/` contains only its nine run files. Direct reads of `.../ControlGate/expected.json` and `.../ControlGate/mismatch/expected.json` both return "not found".
- Code path: `load_snapshot` `tools/repeat-control.py:337-341` raises `TamperError("expected.json unreadable")`; `snapshot_mode` `:419-421` then exits 2 `snapshot_tampered`.
- Consequence [INFERENCE, not executed]: `--snapshot` on both committed directories exits 2 rather than 0 and 1. Selftest cases `snapshot-committed-stable` (`:737`, expects 0) and `snapshot-committed-mismatch` (`:738-743`, expects 1) would FAIL, making selftest exit 1 (`:749`). The docstring claims these directories are the committed frozen snapshots (`:60-62`, `:73-74`).
- Action for owner: author `expected.json` for both directories (or remove the claim). The owner must also resolve F2 at the same time.

### F2 — MEDIUM — `load_snapshot` silently ignores subdirectories and symlinks to directories
- Evidence: `tools/repeat-control.py:364-370`. The loop at `:365-367` adds an entry to `listed` only `if not os.path.isdir(...)`. A subdirectory is therefore never checked against `required` or `expected.json`. Because `os.path.isdir` follows symlinks, a symlink to a directory is also skipped.
- Live instance: the committed stable snapshot root contains `mismatch/` (confirmed by listing). Its entire contents are unhashed and unlisted, and the root still validates under this code path.
- Contract conflict: the docstring says an "unlisted" input or "symlinked" input is `snapshot_tampered` 2 (`:58-59`). Neither case is covered by the tamper arms (`:718-735` cover changed byte, missing file, and unlisted regular file only).
- Fix direction: `lstat` every directory entry; any entry other than `expected.json` and the listed run files, including directories and symlinks of any kind, must raise `TamperError`. Relocating `mismatch/` out of the stable root is part of this cut-over (interacts with F1).

### F3 — LOW-MEDIUM — `expected_exit` shape not type-checked
- Evidence: `tools/repeat-control.py:352` uses `record.get("expected_exit") != EXIT_BY_ID[expected_id]`. Python equality means JSON `false` and `0.0` match `0`. `runs` is type-checked with a bool exclusion at `:349`; `expected_exit` is not.
- Effect: the snapshot passes validation, and `:423` prints `exit=False`. The process exit is unaffected because `finish()` uses `EXIT_BY_ID` (`:426`), so this is a shape gap, not a wrong verdict.
- Fix direction: `isinstance(x, int) and not isinstance(x, bool)`, mirroring `:349`.

### F4 — LOW — `EXIT_FILE_RE` accepts non-canonical exit text
- Evidence: `tools/repeat-control.py:132` `(?:-?[0-9]+|unavailable)\n`. This accepts `-0`, `00`, `007`.
- Effect: the snapshot classify path (`:203`) treats `"00"` as `!= "0"` and returns `baseline_nonzero`. A hand-authored or drifted record for an exit-0 observation therefore yields a wrong could-not-evaluate verdict instead of `snapshot_tampered`. Run mode cannot emit these forms (`str(returncode)` at `:282`).
- Fix direction: `(?:0|-?[1-9][0-9]*|unavailable)\n`.

### F5 — LOW — `REPEAT_COMPARE identical=yes` printed for `baseline_nonzero`
- Evidence: `tools/repeat-control.py:320` sets `agreed` to true for `baseline_nonzero`, and `:321` prints `identical=yes`. The docstring classifies `baseline_nonzero` as could-not-evaluate (`:44-46`).
- Effect: a consumer reading that line alone can take it as an agreement signal. The observations did agree, so the line is literally true, but it is a log-consumer hazard.
- Fix direction: print `identical=yes` only for `controls_match`, or drop the field in favour of the finding name.

### F6 — LOW (test gap, MEDIUM for precedence regressions) — Selftest does not exercise the precedence cases the docstring calls out
- Evidence: the docstring names `[0,1,0]` (`:33`), `[1,0,0]` and `[1,2,1]` (`:36-38`) as the shapes that define precedence. `SELFTEST_FIXTURES` (`:500-509`) and cases (`:644-651`) contain no `[0,1,0]` fixture, no disagreeing-nonzero-first fixture, and no mid-sweep unavailable case. The only exit-mismatch fixture is `MISMATCH_EXIT_SH` `[0,0,1]` (`:478-485`, case `:649`).
- Effect: a regression that moved the baseline check ahead of the disagreement check (or dropped the exit from the tuple at `:197-200`) would still pass selftest for the shapes that matter.
- Fix direction: add fixtures for `[0,1,0]`, `[1,0,0]`, `[1,2,1]`, and a run-2-unavailable case; each with its expected finding and exit.

### F7 — LOW — Non-UTF-8 cwd raises outside the handler that should catch it
- Evidence: `command_record` `tools/repeat-control.py:257` embeds `os.getcwd()`, and `:261` calls `.encode("utf-8")` with strict errors. `write_new` for `command.txt` is wrapped only in `except OSError` (`:305-308`).
- Effect: a surrogate-escaped cwd raises `UnicodeEncodeError`, which propagates to `main` (`:786`) and exits 2 `setup_error` with no `command.txt`. This is could-not-evaluate, not a wrong verdict. Edge case.
- Fix direction: encode with `errors="surrogateescape"` or `"replace"` and document it.

## Verified non-defects
- Disagreement tuple includes exit (`:197-200`); stdout and stderr are compared as bytes with no normalization. Matches docstring.
- `classify` reads `records[0]` for the baseline only after all records have been proven equal (`:196-202`), so the single-record read at `:203` is sound.
- stdin is `DEVNULL` (`:268`), `shell=False` (`:271`), no decoding of observations.
- Unavailable runs store `b""` stdout and OSError text stderr; `unavailable` exit text matches `EXIT_FILE_RE` (`:132`), so an unavailable snapshot round-trips.
- `--runs` ASCII-only regex (`:243`) and `<3` rejection (`:246-247`) match the `invalid_usage` cases.

## Residual risk and verification gaps
- Nothing executed. All selftest and snapshot outcomes above are [INFERENCE] from reading the code and listing directories.
- No timeout (documented at `:79-82`); a hanging control yields no verdict.
- Snapshot digests are self-referential (`:83-85`), and `expected.json` itself is not hashed; F1 and F2 both bear on this.

## Tools
None installed or updated by this seat.

## Owned paths
- Read-only: `tools/repeat-control.py`, `.ufo/evidence/round-12/ControlGate/**`.
- Written: this file only.
