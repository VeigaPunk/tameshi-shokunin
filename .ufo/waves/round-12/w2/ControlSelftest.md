# ControlSelftest — round-12 w2 — repeat-control selftest (read-only)

Seat: `TameshiR12.ControlSelftest` (reviewer, leaf). Advisory, lane-internal. Not an independent non-author admission, promotion, or pass.

Scope: `tools/repeat-control.py` `--selftest` arm (`selftest()` at :545-756), its embedded fixtures (:439-509), the module contract in its docstring (:1-93), and the committed snapshot directories under `.ufo/evidence/round-12/ControlGate/` and `.../mismatch/`.

Method: source and evidence read only. **Nothing was executed.** Every "FAIL" or "pass" statement below is a reading-based prediction and is labelled `[INFERENCE]`. No file was edited. No tool was installed or updated (`~/.omp/agent/RULES.md` was not needed for a read-only seat with no install).

## 1. Findings by severity

### F1 — HIGH — pinned expected files are absent; the selftest cannot pass as shipped `[INFERENCE from reading]`
- Read `.ufo/evidence/round-12/ControlGate/expected.json` → not found.
- Read `.ufo/evidence/round-12/ControlGate/mismatch/expected.json` → not found.
- Directory listings of both directories hold only `run-{1,2,3}.{stdout,stderr,exit}`. Neither holds `command.txt` or `finding.txt`, which run mode writes (`tools/repeat-control.py:306`, `:323-326`).
- The selftest needs both files: `load_snapshot` opens `expected.json` first (`tools/repeat-control.py:337-341`) and raises `TamperError` if absent → `snapshot_tampered` / exit 2.
- Affected cases: `snapshot-committed-stable` (`:737`, expects `controls_match`/0) and `snapshot-committed-mismatch` (`:738-743`, expects `controls_mismatch`/1). Both record FAIL (`:592-596`).
- Predicted result: `SELFTEST: FAIL (2 of 24 cases failed: snapshot-committed-stable,snapshot-committed-mismatch)`, exit 1 (`:746-749`), scratch kept.
- Dangling references to the missing pin: `.ufo/waves/round-12/w1/GateRegistryScribe.md:33` (records ABSENT), `.ufo/waves/round-12/w1/FrontierState.md:212` (cites `ControlGate/expected.json` as the pinned verifier), and the module docstring `:60-62` and `:73-75`.
- Provenance gap: the committed run files have no `command.txt` and no `finding.txt`, so they are not in the layout run mode produces. Their origin is unrecorded in the directory.
- Consequence: no persisted expected ID or exit exists for the committed fixtures. The only expected IDs in the tree are literals in the selftest body (see §2).

### F2 — MEDIUM — exit contract disagrees with code for a damaged committed fixture
- Docstring `:75-76`: "Exit: 0 all cases pass · 1 at least one case fails · 2 could-not-evaluate (committed fixture root missing **or damaged**)."
- Code: a missing root → `COULD_NOT_EVALUATE` exit 2 (`:547-549`). An exception → exit 2 (`:753-756`). A **damaged** committed snapshot does not raise. `snapshot_case` records a FAIL (`:592-596`), so the run returns 1 (`:749`).
- The docstring and the code disagree on the exit for the damaged-fixture class. L1 must pick one. This seat does not choose.

### F3 — MEDIUM — mandatory branches stated in the module contract have no selftest arm
Each item below is a behaviour the module contract states, with no case in `selftest()`. Detail is in §3.
- Existing `--out` refused, exit 64 (contract `:24-25`; code `:300-302`).
- Snapshot "intact but recomputes to a different finding → exit 1" (contract `:55-58`; code `:425-434`). `snapshot-mismatch-pass` (`:716`) uses a matching expectation, so this arm is untested.
- Snapshot tamper classes named in contract `:58-60` but not tested: symlinked input (`:378-381`), malformed record / schema / expected pair / inputs shape / digest format (`:338-363`), unparsable `expected.json` (`:342-345`), exit-file grammar (`:394-399`).
- Precedence arms in contract `:30-40`: `[1,0,0]` and `[1,2,1]` → `controls_mismatch` (nonzero tuples that differ); uniform signal death → `baseline_nonzero` (`-9,-9,-9`); mixed unavailable + disagreement → `command_unavailable` (rule 1 over rule 2); `[0,1,0]` → mismatch.
- `setup_error` exit 2, defined at contract `:46-48`. No case forces a write failure: `run_once` `:287-288`, `run_controls` `:303-304`, `:307-308`, `:327-328`, `main` `:785-786`.
- `snapshot_tampered`/`baseline_nonzero`/`command_unavailable` in snapshot mode (`SNAPSHOT_IDS` `:125-130`). No snapshot case uses `baseline_nonzero` or `command_unavailable`. The `unavailable\n` exit-file form (`EXIT_FILE_RE` `:132`) is never exercised in snapshot mode.
- Persisted artifacts: no case reads `finding.txt` (`:323-326`) or per-run `.exit` for a mismatch.

### F4 — LOW — unlisted subdirectories inside a snapshot are never flagged
- `load_snapshot` builds `listed` from non-directories only (`:364-368`). An unlisted directory in a snapshot dir is silently accepted, and so is a symlink to a directory (`os.path.isdir` follows links).
- The skip is probably deliberate: the committed root holds a `mismatch/` subdirectory, and without the skip `snapshot-committed-stable` would be rejected as "unlisted". The design choice is defensible, but no arm pins it. The contract's "unlisted input → snapshot_tampered" (`:58-59`) reads as covering this case.

### F5 — LOW — docstring path drift
- Docstring `:65`: scratch under `/tmp/tameshi-r12-repeat-control-selftest.*`. Code `:550`: `tempfile.mkdtemp(prefix=...)` uses the platform temp dir (`TMPDIR`).

### F6 — LOW — inherited peer recommendation conflicts with the module contract
- `.ufo/waves/round-12/w1/LimitsConnector.md:113` asks the selftest to assert `[1,2,1]` and `[1,1,1]`-differing-stderr as `baseline_nonzero` (exit 2).
- Module contract `:36-39` and code `classify` `:197-205` make nonzero tuples that differ `controls_mismatch` (exit 1). The selftest must follow the contract; the LimitsConnector recommendation is not adopted here.

## 2. Persisted and embedded expected IDs and exits (24 cases)

Expected values are literals in `selftest()`. No persisted expected file exists for any case (F1). `obs` = the last non-empty stdout line checked by `last_finding_id` (`:512-520`).

| # | case | line | expected ID | exit | extra checks |
|---|---|---|---|---|---|
| 1 | stable | :644 | controls_match | 0 | `check_saved_bytes` :598-620 (run-1..3 stdout/stderr == direct run; exit == `0\n`) |
| 2 | mismatch-stdout | :645 | controls_mismatch | 1 | — |
| 3 | mismatch-run3-only | :646 | controls_mismatch | 1 | — |
| 4 | mismatch-newline-only | :647 | controls_mismatch | 1 | — |
| 5 | mismatch-stderr | :648 | controls_mismatch | 1 | — |
| 6 | mismatch-exit | :649 | controls_mismatch | 1 | — |
| 7 | nonzero-baseline | :650 | baseline_nonzero | 2 | — |
| 8 | child127-baseline | :651 | baseline_nonzero | 2 | — |
| 9 | command-unavailable-enoent | :652-657 | command_unavailable | 2 | — |
| 10 | command-unavailable-eacces | :658-663 | command_unavailable | 2 | — |
| 11 | command-unavailable-enoexec | :664-669 | command_unavailable | 2 | — |
| 12 | invalid-runs-2 | :670-681 | invalid_usage | 64 | — |
| 13 | invalid-runs-1 | :670-681 | invalid_usage | 64 | — |
| 14 | invalid-runs-0 | :670-681 | invalid_usage | 64 | — |
| 15 | invalid-runs-abc | :670-681 | invalid_usage | 64 | — |
| 16 | invalid-missing-separator | :682-687 | invalid_usage | 64 | — |
| 17 | stdin-devnull | :688-695 | controls_match | 0 | `check_stdin_isolated` :622-627 (stdout empty) |
| 18 | snapshot-pass | :715 | controls_match | 0 | `snap_stable` :697-703 |
| 19 | snapshot-mismatch-pass | :716 | controls_mismatch | 1 | `snap_mismatch` :704-714 (matching expectation) |
| 20 | snapshot-tamper-byte | :725 | snapshot_tampered | 2 | run-1.stdout bit flip |
| 21 | snapshot-tamper-missing | :730 | snapshot_tampered | 2 | run-2.stderr removed |
| 22 | snapshot-tamper-unlisted | :735 | snapshot_tampered | 2 | extra `run-4.stdout` |
| 23 | snapshot-committed-stable | :737 | controls_match | 0 | **root `ControlGate/`: expected.json absent → predicted FAIL (F1)** |
| 24 | snapshot-committed-mismatch | :738-743 | controls_mismatch | 1 | **`ControlGate/mismatch/`: expected.json absent → predicted FAIL (F1)** |

Exit map as implemented (`EXIT_BY_ID` `:115-123`) matches the contract map at `:41-43` and `:75-76` except F2.

Committed run-file observations (read, not run): `ControlGate/run-{1,2,3}.exit` = `0`; `ControlGate/mismatch/run-{1,2,3}.exit` = `0`. `mismatch/run-1.stdout` = `mismatch-out`, `mismatch/run-3.stdout` = `mismatch-out-changed`. The committed mismatch is a stdout-only disagreement with all exits 0. It therefore shows `controls_mismatch` / 1, not a nonzero baseline.

## 3. Child CLI coverage

Child invocations are `subprocess.run([sys.executable, SELF, ...])` (`:563-571`). Covered surfaces:
- Run mode, success: 1, 2 (plus stdin 17). Run mode, mismatch: 5. Run mode, nonzero: 2. Run mode, command unavailable: 3. Usage: 5 (4 runs values + missing `--`).
- Snapshot mode: pass 1, mismatch pass 1, tamper 3, committed 2.

Usage and dispatch arms in `dispatch`/`run_mode`/`snapshot_mode` with no case:
- `dispatch([])` no arguments (`:763-764`).
- `--selftest` with extra arguments (`:766-768`).
- `--snapshot` with arity ≠ 1 (`:770-772`), and `--snapshot` on a non-directory (`:414-415`).
- `-h`/`--help` (`:774-778`); the GateSecurity recommendation to state its class explicitly `[INFERENCE: not implemented as a case]`.
- Duplicate `--runs`/`--out` (`:223-224`), missing option value (`:226-227`), unexpected argument before `--` (`:234`), missing `--runs` (`:235-236`), missing `--out` (`:237-238`), empty command after `--` (`:241-242`).
- `--runs` forms outside the ASCII-digit regex: `" 3"`, `"+3"`, `"03"` (`:243-244`). GateSecurity's suggested checks (`.ufo/waves/round-12/w1/GateSecurity.md:176`) include `' 3'`; only `abc` is tested.
- Existing `--out` (`:300-302`), setup error (F3).
- Stream content: every case checks only exit code and last stdout line. Stderr text, `SNAPSHOT_TAMPER`, usage lines, and the "no stderr on success" property are not asserted.
- `invalid_usage` cases do not assert that `--out` was never created. The docstring (`:24-25`) implies a refused run leaves nothing behind.

## 4. Other observations (not defects by themselves)
- The selftest has no timeout on child calls (`:565-571`). The module docstring discloses that a hang has no verdict (`:79-82`). A hung selftest child would hang the selftest.
- N > 3 runs is untested. Not mandatory per the contract (`:12`).
- Two fixtures depend on Python behaviour, not on the gate: `noshebang` → OSError `ENOEXEC`, and `noexec.txt` mode 644 → `EACCES` (`:634-639`). The arms assume CPython raises `OSError` for both on this interpreter. `[INFERENCE]`, not checked here.
- Outside the selftest, BytesReview evidence exists for a signal arm (`C11-signal-kill9`) and other CLI cases under `.ufo/evidence/round-12/BytesReview/cli/`. That evidence was not re-run and is not selftest coverage.

## 5. Verification gaps
- Nothing was executed (per assignment). F1 and F2 are predictions from reading `selftest()` and the directory contents. A single run of `python3 tools/repeat-control.py --selftest` by L1 would confirm or refute them.
- The file sha256 was not recomputed. `BytesReview/cli/*/command.txt` records `d45d8e3948c24c2f6b2afcc336a5a44d2119e66b32eaea9fbe5c9eb08807d17d`; the current file may differ.
- The committed run files' origin is unknown (no `command.txt`). Their bytes were read in part only (exit files and mismatch stdouts).

## 6. Owned paths
- Written: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/ControlSelftest.md` (this file).
- Stray copy written earlier at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-12/w2/ControlSelftest.md` (outside the lane); removed by this seat.
- Not edited: `tools/repeat-control.py`, `.ufo/evidence/round-12/ControlGate/**`, any other seat's files.
- No installs or updates. No LOG entry (read-only seat).

## 7. Checks L1 should run once, after integration
- `python3 tools/repeat-control.py --selftest; echo exit=$?` (expect F1 failures until expected.json pins exist).
- Confirm `ControlGate/expected.json` and `ControlGate/mismatch/expected.json` absence versus the references in F1.
- Decide F2's exit contract (docstring vs code) before the SKILL registry row is written.
