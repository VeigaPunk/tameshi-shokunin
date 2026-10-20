# ControlCritic — round 12 w2 (critic, advisory)

Target: `tools/repeat-control.py`, untracked, sha256
`29d8025490f349c106bc8132da7bfecc2ae4f8fb00720b43636e52335d27467a`, mtime 2026-10-19 23:24:06 -0300.
Axes: vacuity, empty sample, binary stream equality, nonzero child semantics.
Status: advisory critic evidence. This is not a judgment, admission or promotion. No repo file was edited except this report.

## Disclosure: probes executed (before L1's "no checks" IRC arrived)

Before the parent's IRC ("Do not run checks unless explicitly assigned"), this seat ran these counterexample probes against the tool:
- The snapshot-mode and run-mode probes ran in scratch `/tmp/tameshi-r12-controlcritic.iaGPZ0`, using commands `true`, `sh -c …` and a self-deleting script.
- One pure-function mutant model imported `classify` with `PYTHONDONTWRITEBYTECODE=1`, so no `__pycache__` was written.

The tool's `--selftest` was not run, and neither was any repo test, build or lint. Outputs are quoted below. Scratch stays in `/tmp` and is not committed evidence (QUALITY 9). L1 should treat these results as critic observations to re-run, not as pinned evidence.

## Findings (counterexample · evidence · axes · smallest safe correction)

### CC-1 — HIGH — An output-stream write failure exits 1, the `controls_mismatch` code (observed)
- **Counterexample:**
  - `python3 tools/repeat-control.py --runs 3 --out $T/full -- true >/dev/full` exits `1`.
  - `python3 tools/repeat-control.py --runs 2 --out $T/u -- true 2>/dev/full` is invalid usage, so it should exit 64. It exits `1`.
  - `--snapshot <valid dir> >/dev/full` also exits `1`.
- **Evidence:**
  - The traceback shows `emit` (`tools/repeat-control.py:146`) raising `OSError [Errno 28]` at `:298`.
  - `main`'s handler (`:785-786`) calls `setup_failure`. That calls `emit("REPEAT_CONTROL: setup_error")` (`:187`), which raises again inside the `except`. The exception is uncaught, so Python exits 1.
  - In the `/dev/full` case no `--out` directory was created, so no run had happened.
  - This falsifies the docstring guarantee at `:47-48` ("no uncaught Python exception can exit 1 and be read as `controls_mismatch`") and the comment at `:785`.
- **Axes:** nonzero semantics, calibration. A caller that keys on exit 1 reads a tool I/O failure as "the controls disagreed".
- **Smallest correction:** make the last-resort path unable to raise.
  - Wrap `setup_failure`'s writes in `try/except OSError: pass` (or write with `os.write` and ignore errors).
  - Then return `EXIT_BY_ID["setup_error"]` unconditionally.
  - `usage_failure` is reached from `main` only through `dispatch`, so this one guard covers it. Alternatively, `main` can catch a second exception and `os._exit(2)`.

### CC-2 — MEDIUM — The docstring's background-writer limitation is false for this implementation (observed)
- **Counterexample:** `--runs 3 -- sh -c '(sleep 1; echo late) & echo hi'`:
  - `controls_match` 0, with wall time 3.35 s for 3 runs.
  - Every `run-k.stdout` is exactly `hi\nlate\n`.
- **Evidence:**
  - Capture goes through `subprocess.PIPE` with `subprocess.run` (communicate semantics, `:265-272`). The run files are written later from memory with `'xb'` (`:279-281`).
  - So a grandchild that holds the pipe blocks the run until it exits, and its late bytes are counted **in that run**. It cannot "append to a run file after its run ended" as `:80-82` claims.
  - That sentence describes the direct-to-file design that GateSecurity recommended (`w1/GateSecurity.md` remediation 2), not the code as written. This is false provenance in a stated limitation.
  - The real residual risks are different:
    - (a) A hang until the grandchild exits (GateSecurity C1).
    - (b) A grandchild that redirects away from the pipe survives the run and can mutate shared state (cwd files) under run k+1. That makes it a cross-run contamination source with no record.
- **Axes:** calibration (claim honesty), binary equality (what a run's bytes contain).
- **Smallest correction:** rewrite `:80-82` to state the actual behaviour: the run blocks until every holder of the stdout/stderr pipes closes them; their output is attributed to that run; detached writers that left the pipes can affect later runs. No code change.

### CC-3 — MEDIUM — The selftest leaves three precedence/semantics mutants alive (model, executed)
A pure-function model imported the real `classify` and fed it the observation shapes of every selftest fixture:
- Fixtures: `:439-509` and cases `:644-683`.
- Snapshot fixtures: `:698-714`.

Each mutant was then compared against the original:

| mutant of `classify` (`:191-205`) | killed by any selftest shape? | wrong on |
|---|---|---|
| M1 baseline check on `records[0]` moved before the agreement loop | **no — survives** | `[1,0,0]`, `[1,2,1]` → `baseline_nonzero` |
| M2 `any(not available)` → `all(...)` (`:193`) | **no — survives** | `[0,U,U]` → `controls_mismatch` (exit 1, not 2) |
| M3 `exit_text != "0"` → `int(exit_text) > 0` (`:203`) | **no — survives** | stable `-15` (signal death) → `controls_match` 0 |
| M4 exit dropped from the comparison tuple (`:197-200`) | yes (`mismatch-exit` [0,0,1]) | — |
| M5 any-nonzero baseline before the loop | yes (`mismatch-exit`) | — |

- **Why they survive:**
  - No fixture has run 1 nonzero together with a disagreement.
  - No fixture has partial availability. All three unavailable cases (`:652-670`) are unavailable on every run.
  - No fixture has a negative return code. The nonzero fixtures are 7 and 127 only (`:650-651`), and every snapshot fixture is `0\n`.
- **The real tool does produce these shapes:**
  - P8: a script that deletes itself gave `0, unavailable, unavailable` → `command_unavailable` 2.
  - P9: `sh -c 'kill -TERM $$'` gave `-15` ×3 → `baseline_nonzero` 2.
  - Both results are correct in the current code but unprotected by the selftest.
- **Counterexample to a sibling:** `w2/ControlFlow.md:53` says dropping the exit from the tuple "would still pass selftest". The model shows M4 is **killed** by `mismatch-exit` (identical streams, exits [0,0,1]). The surviving reorder is the first-run-only variant M1, not the any-nonzero variant M5.
- **Axes:** vacuity of the selftest, nonzero semantics.
- **Smallest correction:** add three hermetic fixtures. Each uses the same state-file counter pattern as `:454-485`:
  1. Exits `[1,0,0]`, expect `controls_mismatch` 1.
  2. A script that runs once, then `chmod -x "$0"` or removes itself, expect `command_unavailable` 2.
  3. `sh -c 'kill -TERM $$'`, expect `baseline_nonzero` 2.

### CC-4 — LOW — Snapshot accepts non-canonical exit text and misclassifies it (observed; confirms ControlFlow F4 [INFERENCE])
- **Counterexample:** valid digests, recorded `controls_match`:
  - Exits `00,00,00` → observed `baseline_nonzero`.
  - Exits `0,00,-0` → observed `controls_mismatch`.
  - Exits `-0`×3 → observed `baseline_nonzero`.
  - All three exit 1 "expectation not reproduced" instead of 2 `snapshot_tampered`.
- **Evidence:** `EXIT_FILE_RE` `:132` accepts these values. `classify` then compares strings (`:197-203`, using text from `:402-403`). Run mode cannot emit these values (`str(returncode)`), so the defect is limited to authored or drifted snapshots.
- **Axes:** binary/text equality, nonzero semantics.
- **Correction:** `(?:0|-?[1-9][0-9]*|unavailable)\n`, as ControlFlow F4 already gives.

### CC-5 — LOW — Unlisted subdirectory is ignored (observed; confirms ControlFlow F2 / ControlSnapshot F3)
- **Counterexample:** a valid stable snapshot plus an empty directory named `run-4.stdout/` gives `controls_match` 0.
- **Evidence:** `:365-367`. This contradicts `:58-59`.
- **Correction:** as the siblings state: `lstat` every entry and reject any entry that is not a listed regular file, then move `mismatch/` out of the stable root.

### CC-6 — HIGH (state, not code) — Committed snapshots fail today (observed; confirms ControlFlow F1 / ControlSnapshot F1 [INFERENCE])
- **Observation:** `--snapshot .ufo/evidence/round-12/ControlGate` and `.../mismatch` both give `SNAPSHOT_TAMPER expected.json unreadable`, `snapshot_tampered`, exit 2.
- **Selftest exit code:** the selftest's root guard checks only `isdir` (`:547`). With the record missing, the selftest therefore ends in case FAIL (exit 1), not the "2 could-not-evaluate (committed fixture root … damaged)" that `:76-77` promises.
- **Correction:** commit `expected.json` for both directories (the owner is ControlFinish/L1). Alternatively, make the guard at `:547` also require both `expected.json` files, so that a damaged root is exit 2 as documented.
- **Provenance gap:** the committed directories hold no `command.txt`, so their origin is unrecorded. The run files have mtime 23:24:19, 13 s after the tool.

### CC-7 — Tradeoff for the judge, not a defect — vacuous and empty samples match
- **Observation:** `--runs 3 -- true` gives `controls_match` 0, with `stdout-bytes=0 stderr-bytes=0` on every run. BytesReview C03 had the same result.
- **Meaning:** a control that exercises nothing passes the gate. Examples are a test filter that selects zero tests and still exits 0, or a wrapper that no-ops. The gate asserts agreement, not non-vacuity, and the docstring never says so. The `:85-87` non-claim covers determinism, not emptiness.
- **Correction (documentation only):** add one line saying that `controls_match` makes no claim about the control's coverage or non-emptiness, and that zero-byte output is visible in `REPEAT_RUN … stdout-bytes=0`. Do not add a code-level emptiness rejection: empty output is a legitimate stable control (C18 `cat`, stdin isolation).

## Verified non-defects (axis: binary equality / empty sample)
- **Byte comparison:** compares raw `bytes` in memory (`:197-200`) with no decoding. Saved files are the same objects written with `'xb'` (`:279-281`). The snapshot re-hashes and compares raw bytes (`:374-385`).
- **Empty sample:**
  - `--runs` is ASCII digits and `>= 3` (`:243-247`).
  - Snapshot `runs` is an int, not a bool, and `>= 3` (`:348-350`).
  - `inputs` must equal exactly the required set (`:356-358`), so N=0, 1 and 2 and an empty `inputs` all exit 2.
  - An empty command after `--` exits 64 (`:240-241`).
- **Signal death:** saved as a signed decimal (`-15\n`, P9), giving `baseline_nonzero`. The child's raw code never becomes the gate's exit. Exits come only from `EXIT_BY_ID`, apart from CC-1.
- **Mixed availability:** the current code correctly gives `command_unavailable` 2 (P8). The weakness is only the test gap in CC-3.

## Probe outputs (quoted, `/tmp/tameshi-r12-controlcritic.iaGPZ0`)
```
P2a 00,00,00 recorded match   -> SNAPSHOT_OBSERVED id=baseline_nonzero exit=2; REPEAT_CONTROL: controls_mismatch; exit=1
P2b 0,00,-0 recorded match    -> SNAPSHOT_OBSERVED id=controls_mismatch exit=1; exit=1
P2c -0 x3 recorded match      -> SNAPSHOT_OBSERVED id=baseline_nonzero exit=2; exit=1
P5a subdir run-4.stdout/      -> REPEAT_CONTROL: controls_match; exit=0
P6  committed ControlGate     -> SNAPSHOT_TAMPER expected.json unreadable ... snapshot_tampered; exit=2 (both dirs)
P3a run >/dev/full            -> OSError Errno 28 at :146 via :298, re-raised at :187; exit=1; no --out dir created
P3b --runs 2 2>/dev/full      -> exit=1 (expected 64)
P3c --snapshot >/dev/full     -> exit=1
P4  (sleep 1; echo late)&     -> controls_match exit=0; run-{1,2,3}.stdout = "hi\nlate\n"; wall 3.35s
P7  true                      -> stdout-bytes=0 stderr-bytes=0 x3; controls_match exit=0
P8  self-deleting script      -> exits 0,unavailable,unavailable; command_unavailable exit=2
P9  sh -c 'kill -TERM $$'     -> exit=-15 x3; baseline_nonzero exit=2
Mutant model: M1, M2, M3 survive every selftest shape; M4, M5 killed by mismatch-exit.
```

## Owned paths
- Written: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/ControlCritic.md` (this file).
- Not written: `tools/repeat-control.py`, `.ufo/evidence/**`, `LOG.md`, sibling reports.

## Tools
None installed or updated. Observed `bc` absent (an elapsed-time helper); total wall time was taken from the harness instead. No install was needed.
