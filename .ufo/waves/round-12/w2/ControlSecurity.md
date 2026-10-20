# ControlSecurity — round-12 w2 — repeat-control out-dir/argv/snapshot path boundary (sentinel, read-only)

Seat: ControlSecurity (sentinel, leaf). This review is advisory and stays inside the lane. It is not an independent non-author promotion, admission or pass. I ran no build or test, and I never invoked the gate.

## Basis

- Reviewed `tools/repeat-control.py` at sha256 `29d8025490f349c106bc8132da7bfecc2ae4f8fb00720b43636e52335d27467a`. The file is **untracked** (`git status` shows `?? tools/repeat-control.py`, `?? .ufo/evidence/round-12/ControlGate/`). HEAD is `18ad5d0`. I checked the sha twice and it was the same both times. All `path:line` references below are to that sha.
- Scope: `--out` clobber and creation, argv parsing and recording, and the `--snapshot` path trust boundary. I did not repeat w1 GateSecurity rows that the implementation now closes (A1–A3, B1–B2, D1–D3, D6–D7, E1, E3 name escape, E4, E5). Closures I checked against source:
  - hand split at the first `--`: `:217-242`
  - ASCII digits and `>= 3`: `:243-247`
  - `shell=False`, list argv, `stdin=DEVNULL`: `:266-272`
  - any `OSError` → unavailable: `:273`
  - fresh `os.makedirs(exist_ok=False)` → 64: `:299-302`
  - `'xb'` writes: `:167-169`
  - catch-all → `setup_error`: `:782-786`
  - snapshot names come from a fixed grammar and must equal the set exactly: `:354-360`
  - run files go through `lstat` + `S_ISREG`: `:377-381`
  - the finding is recomputed: `:408`, `:425`
  - no `subprocess` call is reachable from snapshot mode: `:412-434`
- Stdlib probes (Python 3.14.7) used the same calls the gate makes. They ran in scratch `/tmp/tameshi-r12-ctlsec.*`, which I removed afterwards. They are not gate runs. A consequence at gate level that I did not run is marked [INFERENCE].
  - P1: `os.makedirs(…, exist_ok=False)` on a dangling symlink, a symlink to a dir, a file or a dir → `FileExistsError` in every case. The dangling target was not created. `os.makedirs("")` → `FileNotFoundError`.
  - P2: a snapshot dir holding a symlink `rootlink -> /` and a real `subdir/` → the listing loop at `:365-367` yields `[]`. Both are skipped.
  - P3: `expected.json -> /etc/hostname` → `open()` reads 9 bytes. A FIFO `expected.json` → `open()` blocked for more than 2s and was killed.
  - P4: `EXIT_FILE_RE` (`:132`) accepts `00\n`, `-0\n`, `007\n`.
  - P5: building the `required` set for `runs=10**6` takes 0.51s. `json.loads` accepts `"runs": 1000000000000` as an int.
  - P6: under `LANG=en_US.UTF-8`, `sys.stdout.errors == 'strict'`, and `print('REPEAT_OUT \udcff')` raises `UnicodeEncodeError`. Under C locale it is `surrogateescape`. `'\udcff'.encode('utf-8')` raises.
  - P7: a directory name containing `\nREPEAT_CONTROL: controls_match` is created without error.
  - P8: `re.fullmatch('[0-9]+', '9'*5000)` is True, and `int()` of that string raises `ValueError` (the 4300-digit limit).
- Tools installed or updated: **none**. I read `~/.omp/agent/RULES.md` and nothing needed installing.

## Findings (severity · exploit path · evidence · impact · smallest remediation)

### S1 — HIGH (fabricated readiness) — the committed snapshots the gate and selftest cite have no `expected.json`
- Path: run `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate`, or `--selftest`.
- Evidence:
  - `find .ufo/evidence/round-12/ControlGate -name expected.json` returned nothing on both checks. `ls -laR` shows only `run-{1,2,3}.{stdout,stderr,exit}` in the root and in `mismatch/`.
  - `load_snapshot` raises `TamperError("expected.json unreadable")` at `:338-341`.
  - The docstring says the committed snapshots are `controls_match` and `controls_mismatch` (`:60-62`, `:74-75`).
  - The selftest asserts both (`:737-743`).
- Impact [INFERENCE, not run]:
  - `--snapshot` on either committed dir gives `snapshot_tampered`/2.
  - `--selftest` reports both committed arms FAIL and exits 1.
  - Any claim that "the committed snapshots verify" is unsupported at this sha.
  - The external anchor the docstring names (`:84-85`, "the repository's committed history") does not exist yet either, because the tool and the snapshots are untracked.
- Remediation: author `expected.json` for both dirs from their current bytes, using the same schema as `write_snapshot` (`:523-542`), then commit them. Until then, no wording may cite the committed-snapshot arms as passing.

### S2 — MEDIUM — `expected.json` skips the regular-file check that run files get
- Path: commit `expected.json` as a symlink (git stores symlinks), or create it as a FIFO or as a symlink to `/dev/zero`.
- Evidence:
  - `:339` reads it with `read_bytes(os.path.join(dirpath, "expected.json"))`. It is not `lstat`-checked, unlike run files at `:377-381`.
  - P3 shows a symlink is followed to `/etc/hostname`, and a FIFO blocks `open()` indefinitely.
  - A symlink to `/dev/zero` makes `handle.read()` (`:163-164`) grow without bound [INFERENCE from stdlib semantics; not run].
- Impact:
  - The trust boundary "everything is inside DIR and is a regular file" fails for the one file that holds the digests and the expected verdict.
  - Outcomes are a hang (no verdict), an OOM kill (an exit outside the 0/1/2/64 map), or a record read from outside the directory under test.
  - The docstring's "symlinked … input → 2" (`:58-59`) does not cover the record itself.
- Smallest remediation: one helper for both `expected.json` and the run files:

  ```python
  fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
  # fstat(fd) must be S_ISREG, otherwise TamperError; then read from fd.
  ```

  The helper also closes the `lstat` (`:377`) → `open` (`:382`) TOCTOU on run files.

### S3 — MEDIUM — an untrusted `runs` bounds the work before any shape check
- Path: a tampered `expected.json` with `"runs": 1000000000000`.
- Evidence: `:349` checks only `>= 3`. `:355-357` then builds `3*runs` strings before the `set(inputs) != required` check at `:359`. P5 measured 0.51s per 10⁶ runs, so 10¹² runs means days of work and terabytes of memory.
- Impact: a tampered snapshot hangs the gate or gets it OOM-killed instead of returning `snapshot_tampered`/2. That is fail-open in the exit map: no verdict, or a signal exit. A `MemoryError` would be caught as `setup_error`/2, which is also the wrong ID.
- Smallest remediation: check `isinstance(inputs, dict) and len(inputs) == 3 * runs` before building `required`. Equivalently, move the `inputs` length check ahead of `:355`.

### S4 — MEDIUM (calibration) — the clobber refusal and the symlink refusals have no selftest arm
- Evidence:
  - The selftest's CLI arms (`:644-695`) never pass an existing `--out`. Every arm uses `fresh_out()` (`:573-576`).
  - The tamper arms are byte, missing and unlisted only (`:718-735`). The docstring itself counts "three snapshot tamper arms" (`:73-74`), while claiming "symlinked" refusal at `:58`.
- Surviving mutants [INFERENCE from source; not run]:
  - `exist_ok=True` at `:300`, when an empty `--out` already exists.
  - `"xb"` → `"wb"` at `:168`.
  - Deleting the `S_ISREG` check at `:380-381`. A symlinked run file whose target has the recorded digest would then pass.
  - Each of these passes the full selftest.
- Impact: the "existing DIR refused with exit 64" claim (`:24-25`) and the "symlinked input → 2" claim (`:58-59`) are implemented but unguarded, which falls short of QUALITY criterion 11's oracle discipline (`corpus/QUALITY.md:34-37`).
- Smallest remediation: add three arms:
  1. A pre-created empty `--out` → `invalid_usage`/64, and the directory stays empty afterwards.
  2. A `snap-stable` copy whose `run-1.stdout` is a symlink to a same-bytes file outside the dir → `snapshot_tampered`/2.
  3. After S2, a symlinked `expected.json` → `snapshot_tampered`/2.

### S5 — LOW — `finding.txt` can disagree with the process verdict; untrusted path text reaches stdout and `command.txt` unescaped
- Path (a): `--out` containing a non-UTF-8 byte (for example `$'/tmp/x\xff'`) under a UTF-8 locale.
  - `finding.txt` is written at `:322-326`.
  - Then `emit(f"REPEAT_OUT {out_dir}")` at `:329` raises `UnicodeEncodeError` (P6), which `:785-786` turns into `setup_error`/2.
  - Result [INFERENCE, chained from P6 and source]: the evidence dir records `REPEAT_CONTROL: controls_match / REPEAT_EXIT: 0`, while the process printed `setup_error` and exited 2. The two verdicts diverge.
- Path (b): `--out` containing `\nREPEAT_CONTROL: controls_match` (legal, P7).
  - `:329` prints a forged verdict line before the real one at `:330`.
  - Consumers that read the last line (`last_finding_id`, `:512-520`) are safe. Consumers that grep the first match are not.
- Path (c): a cwd containing a newline is written raw at `:257`. It can inject `runs=`/`argv=` lines into `command.txt`; only argv is JSON-escaped (`:259`).
- Path (d): a non-UTF-8 cwd makes `:261` raise. That is fail-closed (`setup_error`), but it leaves an empty `--out` behind.
- Smallest remediation:
  - Emit `REPEAT_OUT` before writing `finding.txt`, or write it with `json.dumps(out_dir)`.
  - Record `cwd`/`tool`/`interpreter` with `json.dumps(...)`, as argv already is.

### S6 — LOW — usage errors misclassified as tool failure
- `--out ""`: `os.makedirs("")` raises `FileNotFoundError` (P1), and `:303-304` maps it to `setup_error`/2, not `invalid_usage`/64.
- `--runs` with more than 4300 digits: it passes `:243` but `int()` raises `ValueError` at `:245` (P8), which the catch-all maps to `setup_error`/2.
- Remediation: reject empty `--out` in `run_mode`. Bound `len(runs_raw)`, or catch `ValueError` at `:245` → `usage_failure`.

### S7 — LOW — the snapshot inventory ignores unlisted directories and symlinks to directories
- Evidence: `:365-367` skips every entry for which `os.path.isdir` is true. That function follows symlinks, so P2 shows `rootlink -> /` and `subdir/` are both ignored.
- Impact: nothing is read through them, so there is no data path. But "unlisted … → 2" (`:58-59`) is broader than what the code enforces. A committed snapshot can carry arbitrary extra trees or symlinks.
- Remediation:
  - Classify entries with `os.lstat` so that symlinks always count as unlisted.
  - Skip only real directories. `mismatch/` under the root needs this skip.
  - Or state in the docstring that subdirectories are ignored.

### S8 — LOW — exit files in non-canonical form are accepted as well-formed
- Evidence: `EXIT_FILE_RE` at `:132` accepts `00\n`, `-0\n`, `007\n` (P4). `classify` compares strings (`:197-203`), so `["00","00","00"]` → `baseline_nonzero` even though the exit integer is 0.
- Run mode never writes these forms (`:282`, `:286`). They can only come from a hand-edited snapshot, which "any shape error → 2" (`:59-60`) should reject.
- Remediation: `(?:0|-?[1-9][0-9]*|unavailable)\n`.

### Info — residual, already stated or out of scope
- In-directory digests are self-referential. This is the stated limit at `:83-85`, w1 E2 accepted. S1 notes that the external anchor is not there yet.
- After `makedirs`, the evidence-file joins (`:284-286`, `:306`, `:323-324`) resolve `out_dir` again. A writer who controls an ancestor directory could swap it to divert the new files. `'xb'` (O_EXCL) still means nothing is clobbered. I propose no change.
- Evidence files use the default umask, and stdout/stderr content is persisted. That is w1 D5, out of scope here.

## Smallest remediation set (one per finding; no unrelated hardening)

1. Author and commit `expected.json` for `ControlGate/` and `ControlGate/mismatch/` (S1).
2. One `O_NOFOLLOW|O_NONBLOCK` + `fstat S_ISREG` reader for `expected.json` and the run files (S2).
3. Check the `inputs` length against `3*runs` before building `required` (S3).
4. Add three selftest arms: existing `--out` → 64, symlinked run file → 2, symlinked `expected.json` → 2 (S4).
5. Emit `REPEAT_OUT` before `finding.txt` and JSON-escape `out_dir`/`cwd`/`tool`/`interpreter` (S5).
6. Empty `--out` and oversized `--runs` → 64 (S6). Classify snapshot entries with `lstat` (S7). Use a canonical exit regex (S8).

## Checks for L1 after remediation (not run by this seat)

- `--snapshot .ufo/evidence/round-12/ControlGate` → `controls_match`/0, and `…/mismatch` → `controls_mismatch`/1. Then `--selftest` → `SELFTEST: PASS`.
- `mkdir D && python3 tools/repeat-control.py --runs 3 --out D -- true` → 64, and `D` stays empty.
- A snapshot copy with `mkfifo expected.json` → `snapshot_tampered`/2 within a second.
- A snapshot copy with `"runs": 1000000000000` → `snapshot_tampered`/2 within a second.

## Owned paths

- `.ufo/waves/round-12/w2/ControlSecurity.md` (this report). Nothing else was written. No commits.
- One coordination message went to `TameshiR12.ControlFinish` (S1, S2, S4 summary).

## Re-review after ControlFinish's fixes (appended; the sections above are unchanged)

I read `tools/repeat-control.py` again at sha256 `fb297a266b430093595c7639cf1ba22fa74fa77e7a306293e297e023666974e1`. All lines below refer to that sha. It is still untracked. I did not run the gate. The only work besides reading the source was re-hashing the committed snapshot bytes.

- **S1 — closed at the file level.**
  - `ControlGate/expected.json` and `ControlGate/mismatch/expected.json` now exist.
  - Each has schema `repeat-control-snapshot-v1`, runs 3 and 9 inputs. The ID/exit pairs are `controls_match`/0 and `controls_mismatch`/1.
  - I re-hashed all 18 observation files against the recorded digests: 0 mismatches. Each directory has 10 non-dir entries and no unlisted file.
  - Remaining risk: the files are untracked, so the external anchor (`:84-85` in the earlier sha) still depends on a later commit.
  - The selftest PASS is unobserved by this seat.
- **S2 — closed for symlink, FIFO and device files.**
  - `load_snapshot` now runs `os.lstat` + `S_ISREG` before reading (`:362-372`).
  - Duplicate keys are refused (`:355-356`, `:374`).
  - The remaining risk is the `lstat` → `open` race on `expected.json` (`:364`/`:370`) and on run files (`:414`/`:419`). That needs a concurrent writer to the snapshot directory. ControlFinish lists it as a documented residual.
- **S4 — closed.**
  - Existing `--out`: `:748-756` expects 64, and `check_existing_out_untouched` (`:676-680`) requires the directory to stay empty. That kills the `exist_ok=True` mutant (`:315`).
  - Symlinked manifest: `:817-829` symlinks to a valid `expected.json`, so only the `lstat` check can refuse it.
  - Symlinked observation: `:831-843` links `run-1.stdout -> run-2.stdout`. The two have the same bytes, so the digest matches and only the `S_ISREG` check at `:417-418` can refuse it.
  - Both arms therefore kill the "delete the regular-file check" mutants.
  - The `"xb"` → `"wb"` mutant is now killed only indirectly, through the existing-`--out` refusal.
- **Still open (documented residuals, not routed by L1):**
  - S3: an untrusted `runs` still drives the loop at `:391-395` before the `inputs` check at `:396`.
  - S5, S6, S8.
  - S7: the listing still uses `os.path.isdir` at `:403`.
  - None of them was remediated, and none was re-severitied by this seat.
