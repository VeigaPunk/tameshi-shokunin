# ReviewV1Pin — v2 tool does not modify tools/write-path-census.py

Verdict: CONFIRMED (no violation). `tools/write-path-census-v2.py` is read-only on every filesystem path; the v1 pin `bc8c660c…edc62` is intact before and after execution.

## Evidence

- Static read of the full 103-line file: the only `open()` is `tools/write-path-census-v2.py:46` — `open(path, encoding='utf-8')` in `load_fixtures`, read-only mode on the fixtures JSON. No `open(..., 'w')`, no `os.replace`, `os.rename`, `subprocess`, `shutil`, or `pathlib` call sites. Imports (lines 10–14) are `argparse, json, os, re, sys` only; `os` is used solely for `os.path.dirname/join` at lines 95–96.
- `os\.replace`, `os\.rename`, `.write_bytes`, `.write_text` appear only inside regex literals `WRITE_RE`/`EXPECTED_RE` (lines 16–27) — patterns applied to scanned text, never executed.
- The sole textual reference to the v1 filename is the docstring at `tools/write-path-census-v2.py:6`: "Does not edit tools/write-path-census.py. The v1 pin stays put."
- Empirical: `sha256sum tools/write-path-census.py` returned `bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62` (the contract `v1_sha256` pin, `.ufo/evidence/round-40/contract.json:27`) both before and after running `python3 tools/write-path-census-v2.py --selftest` (rc=0, `bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`). `git status --porcelain` on both tool paths: clean.
- Harness path also clean: `.ufo/evidence/round-40/census/measure.py` writes only inside `tempfile.TemporaryDirectory` (lines 151–186: tool copy at 153, fixtures copy at 156, mutants at 171/180) and reads v1 exclusively via `git show` (line 139, capture-only) for sha comparison at line 140. `load_mod` (lines 74–78) execs the tmp copy via `spec_from_file_location`, which does not write `__pycache__` and never targets the lane path.

## Residual risk

- None in scope. Pre-existing `tools/__pycache__/write-path-census.cpython-314.pyc` is a stale bytecode artifact, not a `.py` modification; neither v2 nor measure.py imports the v1 module, so this claim's execution paths cannot regenerate it.
- Verification gap: none. Lane checkout and shokuknow untouched; no counters run in default mode.

Command for re-verification:
`grep -nE "open\(|os\.(replace|rename)\(|subprocess|shutil|pathlib" tools/write-path-census-v2.py`
→ only `line 46` read-only `open`; all other hits are regex literals.
