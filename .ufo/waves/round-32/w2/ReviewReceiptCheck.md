# ReviewReceiptCheck — round 32, wave 2

Seat: `TameshiR32.ReviewReceiptCheck` (reviewer, calibration axis).
Target: `.ufo/evidence/round-32/receipt-check.py` (sha256 `3a82410750846f8be3a3493f61f0a7ea901a06b89a007a4e1f21e40cddf88a44`), the mined-mistake fix for receipts without an exit file. All runs were done in my scratch dir `/fast/scratch/hyaku/tameshi-r32-seats/ReviewReceiptCheck/`; the target tree was only read (see read-only evidence). No tools installed; no installs needed. No `lsp` device is available in this session, so findings are execution-based, not server-semantic.

## Verdict

The fix behaves as claimed on every exercised path: selftest passes (6/6, exit 0); round-31 is scanned with `after/commandD-at-final.stdout` listed (exit 1) together with four extra legacy control captures; round-32 is clean (0/8, exit 0); usage errors exit 2. The four `ctl/*.stdout` listings are **mechanical true positives but out-of-scope extras relative to the mined mistake, which the lesson must disclose** (Finding 1). Two smaller defects: fail-open on unreadable trees contradicting the documented exit 2 (Finding 2), and absent exclusion machinery for non-receipt stdout captures (part of Finding 1's correction).

## Findings

### 1. [MEDIUM] The four round-31 `ctl/bind-v5-*.stdout` listings are outside the mined mistake; the lesson must disclose them

The mined mistake is exactly one receipt: the round-31 verifier spot-check records `after/commandD-at-final.stdout` has no `.exit` file (`corpus/lessons/round-31-verifier-spotcheck.md:36-38`), and routes "give command D an `.exit` file" (`:204-205`). The checker reports five items on round-31:

```
$ python3 receipt-check.py <lane>/.ufo/evidence/round-31
after/commandD-at-final.stdout
ctl/bind-v5-new-shapes.stdout
ctl/bind-v5-old-controls.stdout
ctl/bind-v5-old-shapes.stdout
ctl/bind-v5-real-r30.stdout
RECEIPT_CHECK: missing_exit=5 files=12
$ echo $?
1
```

The four `ctl` files are the binding-v5 pre-data control re-scoring captures, which the lane itself designates as receipts ("the receipts here are the record" — `ctl/README-bind-v5.txt`), and none of them has a sibling `.exit`. Under the checker's stated rule (any `*.stdout` without a sibling `.exit` is an incomplete receipt) they are **not** false positives in the mechanical sense — they are genuinely missing exit-status siblings. But they **are** false positives relative to the claim this fix targets: the round-31 lesson counted one evidence gap (command D), and the four ctl files are not part of that gap and were never flagged by any round-31 record. A reader of the tool's round-31 output would reasonably infer five separate mistakes, not one.

Required disclosure in the lesson: list the four `ctl/bind-v5-*.stdout` files, state they are pre-existing binding-v5 control-capture records whose exit statuses were never recorded as siblings, and either (a) add the missing `.exit` files (each run completed and printed its final kept-count, so exit 0 is recoverable — `[INFERENCE]`, the harnesses themselves live in other seats' scratch and were not re-run), or (b) give the checker an explicit scope/exclusion mechanism. Without one of the two, this tool will keep failing round-31 on five items, and any future non-receipt `*.stdout` capture (e.g. `ctl`-style records) will trip a gate forever.

### 2. [LOW] Fail-open on unreadable trees contradicts the documented exit 2

The docstring says exit 2 means "the checker could not run (missing or non-directory argument, or an unreadable tree)". In practice an unreadable tree exits 0:

```
$ mkdir t5 && echo hi > t5/x.stdout && chmod 000 t5
$ python3 receipt-check.py t5
RECEIPT_CHECK: missing_exit=0 files=0
$ echo $?
0
```

`os.walk` silently yields nothing on an unreadable root (and silently skips unreadable subdirectories), so the scan reports `files=0`, `missing=0`, and exits 0. Same for an unreadable subdirectory containing a `.stdout`. For a completeness gate this is a false PASS on an unscanned tree. Smallest safe correction: probe the root with `os.scandir` before the walk, catch `OSError` during the walk, emit `RECEIPT_CHECK: error=unreadable ...` and exit 2; add two selftest fixtures (unreadable root, unreadable subdir). Low severity because evidence trees are normally readable and the documented contract is the only victim.

### 3. [INFO] Everything else in scope checked and passed

- **Selftest:** `python3 receipt-check.py --selftest` → `case ... ok` × 6, `RECEIPT_CHECK_SELFTEST: cases=6 failed=0`, exit 0. It builds fixtures in a `tempfile` dir; the target is untouched.
- **Round-32 clean:** `missing_exit=0 files=8`, exit 0. All eight stdout files have exit siblings (`before/c1-at-base`, `before/c1monitor-at-base`, `before/census-start`, `before/commandD-at-base`, `repair/c1monitor-at-r31-base-36c1d393`, `repair/commandD-at-r31-67c0e013`, `repair/commandD-at-r31-final-08125328`, `v2/dev/devsweep-200`).
- **Can fail — demonstrated on scratch copies of round-31:** adding the missing `after/commandD-at-final.exit` drops the list to the four ctl files (exit 1); deleting the four ctl stdouts leaves only command D (exit 1); adding all five exits yields `missing_exit=0 files=12`, exit 0. Arbitrary minimal trees: `{a.stdout}` → 1/1, exit 1; complete pair → 0/1, exit 0; nested missing → 1/2, exit 1; FIFO named `*.stdout` is listed and exits 1 (no hang; a single earlier stall was not reproducible and was an environment artifact).
- **Exit codes:** FAIL = 1, PASS = 0, usage errors = 2 (`--selftest` conflict none; no arg → stderr usage + `RECEIPT_CHECK: error=no_dir`; missing dir → `error=not_found`; file arg → `error=not_a_dir`). All error lines prefixed `RECEIPT_CHECK:`.
- **Read-only on target:** after all runs, round-31 newest mtimes are still the round's own 07:13:20 receipts (no writes by me); `receipt-check.py` mtime unchanged; symlinked directories are skipped (`followlinks=False`); a directory named `*.stdout` is ignored (walk `filenames` only). Listing is relative-posix and sorted; non-stdout artifacts (`.stderr`, `.exit` without stdout, text files) are ignored.
- Environment: Python 3.14.8; the tool runs as a plain script with no dependencies.

## Residual risk / verification gaps

- The four ctl runs' exit statuses were not re-derived (harnesses need the source seats' fixtures); their `exit 0` is `[INFERENCE]` from completed summaries and is not load-bearing for the verdict.
- Exotic trees (very deep nesting, permission transitions mid-walk, broken symlinks inside directories) were not exhaustively enumerated; the exercised matrix (empty / pair / missing / nested / mixed / dir-named-stdout / symlink / unreadable / FIFO) covers the realistic space.

## Smallest safe correction

1. Lesson must disclose the four `ctl/bind-v5-*.stdout` files as legacy control captures outside the mined command-D gap, and resolve them by adding `.exit` siblings or adding a scoping mechanism to the checker.
2. Make unreadable trees return the documented exit 2 instead of a silent pass (root probe + `OSError` handling + two selftest fixtures).
