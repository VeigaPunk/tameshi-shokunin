# ExecV4Robustness — round 42 wave 2 (FALSIFY)

Attacked: `tools/write-path-census-v4.py` (C2 tool, L1-authored), robustness over every tracked `.py` file, plus a comparison against v3 text mode.
Lane HEAD during the sweep: `a21845f523b75adbd3e3f7a62af91294db224ad9` (the integration tip; no counter was run). `git status --porcelain` was the same before and after: the only untracked paths were `.ufo/waves/round-42/{dispatch-w2.json,spec-w2.json,w2/}`.
Python 3.14.8. No tools installed.

## Commands

- Driver: `/tmp/tameshi-r42w2-ExecV4Robustness-sweep/sweep.py` (deleted before return), run from the lane root. For each `f` in `git -C <lane> ls-files "*.py"` it ran:
  - `python3 -I tools/write-path-census-v4.py --file <f> --json`
  - `python3 tools/write-path-census-v3.py --file <f>`
- For each file it recorded the exit code, stderr, whether the output was exactly one JSON line, whether `file` matched the input path, the duplicate `(lineno, kind)` pairs, and the expected, unflagged and parse-error counts. From v3 it parsed the trailing `expected_sites=… unflagged=…` summary line and the per-site `expected=1` lines.
- Strict-JSON re-check: `json.loads(out, parse_constant=<raise>)` plus an ASCII check on every v4 output.

## Findings (lane sweep)

| Check | Result |
|---|---|
| Files | **172** |
| v4 non-zero exit | **0** |
| v4 stderr / Traceback | **0** |
| v4 invalid JSON (incl. strict: no NaN/Infinity, single line, ASCII) | **0** |
| v4 `file` field ≠ input path | 0 |
| Duplicate `(lineno, kind)` within one file | **0** |
| v4 parse-error records | 0 |
| v4 total sites / expected / **unflagged** | 500 / 25 / **1** |
| v3 non-zero exit / stderr / missing summary | 0 / 0 / 0 |
| v3 total sites / expected / unflagged | 500 / 25 / 5 |
| Files where the expected-value site count differs between v3 and v4 | **none** |
| Files where the expected-value (lineno, kind) set differs between v3 and v4 | none |

Selftests: `python3 -I tools/write-path-census-v4.py --selftest` printed `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0` (rc=0). `python3 tools/write-path-census-v3.py --selftest` printed `var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` (rc=0).

The full v4 sweep takes 6.7 s serially. The largest input is `tools/evidence-disposition.py` (120618 B).

### Where v3 and v4 differ: unflagged only, 4 sites in 3 files

I checked each one against the source. In all four, v4 is correct.

- `.ufo/evidence/round-23/replay.py:74` (v3 unflagged=1, v4 0, `explicit_out=True`). The write target is `(args.out / 'expected.json')`, and `--out` is declared at `replay.py:28`. The v4 `resolved` field reads `…expected.json argparse --out`.
- `tools/registry-replay.py:123` (v3 1, v4 0, `explicit_out=True`). The write is `(out / 'expected.json')` inside `publish(…, out)` (`:116`), and `out = Path(args.out)` at `:181` with `--out` declared at `:259`. This is the interprocedural case described in v4's docstring (`write-path-census-v4.py:12`).
- `tools/context-capture.py:1682` and `:1685` (v3 1+1, v4 0+0, `scratch=True`). The path is `os.path.join(self.case_dir(name), "expected.json")`, and `self.root = tempfile.mkdtemp(prefix="context-capture-selftest-", dir="/tmp")` at `:1624`. v4 follows `self.case_dir` into `self.root`. v3 stopped at `self.case_dir(name)`, so v3 was wrong here.

### The one remaining v4 unflagged site is a false positive (v3 flags it too)

`.ufo/evidence/round-12/SnapshotReview/probe.py:27` writes `(root / PIN).write_text(...)`, with `PIN = "expected.json"` (`:12`). Its `root` argument is a function parameter, and every caller passes `make(base / "A".."H")` with `base = Path(tempfile.mkdtemp(prefix="snapreview-"))` (`:84`, `:89`). That is a scratch write. v4 follows call sites for `--out` (`_param_args`/`_out_flag`, `write-path-census-v4.py:227-304`) but does not follow them for scratch roots. This does not differ from v3: both report unflagged=1.

## Edge-input probes (scratch files under `/tmp/…/edge/`, not lane files)

I ran `python3 -I tools/write-path-census-v4.py --file <probe> --json` on each probe:

| Probe | v4 result | Note |
|---|---|---|
| empty file | `{"sites": []}` rc 0 | ok |
| syntax error | 1 `parse-error` record, rc 0 | ok |
| NUL byte | `parse-error` with lineno 0, rc 0 | ok; CPython rejects it too |
| invalid UTF-8 | `parse-error` with lineno 2, rc 0 | ok; CPython rejects it too |
| 300 nested parens | `parse-error`, rc 0 | ok; this exceeds CPython's nesting limit |
| 2000-link assignment cycle `a0=a1…a2000=a0` | 1 site, rc 0, 0.043 s, `resolved` length 86 | terminates (`MAX_DEPTH = 8`, `:71`) |
| self-reference `p = join(p, "expected.json")` | 1 site, rc 0, `resolved` 1214 chars | terminates |
| 40 doublings `d = join(d, d)` | 1 site, rc 0, `resolved` 3885 chars, 4113 B output | stays bounded |
| **UTF-8 BOM** file `open("expected.json","w")` | **`parse-error`, 0 expected sites, rc 0** | CPython runs this file fine (rc 0, and it writes `expected.json`). v4 reads it with `encoding='utf-8'` (`:670`), so a leading U+FEFF reaches `ast.parse` and the `SyntaxError` branch (`:441`) swallows the file. v3 does the same: `parse_errors=1 expected_sites=0`. **No tracked `.py` file has a BOM** (I scanned all 172 for `ef bb bf`), so this has no effect on the lane today. |
| two writes on one line `open(…); open(…)` | **two records with the same `(1, 'open')`** | The record has no `col_offset`, so `(lineno, kind)` is not a unique site key by construction. The lane has 0 such collisions. |
| `--file <directory>` or `--file /nonexistent.py` | **Traceback**, rc 1 (`IsADirectoryError` / `FileNotFoundError` at `:670`) | Not reachable from `git ls-files`. v3 behaves the same (`IsADirectoryError`, rc 1). |

## Risks (none of these change the lane numbers)

1. A BOM-prefixed file is silently reported as `parse-error` with 0 expected sites and exit 0. This is a possible false-negative path that v3 shares. Opening with `encoding='utf-8-sig'` would close it. Currently 0 tracked files have a BOM.
2. Consumers that key on `(lineno, kind)` would merge two writes on the same line. The lane currently has none.
3. The scratch analysis does not follow function parameters through call sites, although the `--out` analysis does. This leaves one conservative false positive (`probe.py:27`) that v3 shares.

## Process note

One probe command (`python3 <edge>/bom.py`, to check that CPython accepts BOM files) ran with the lane as its working directory, and its `open("expected.json","w")` created `expected.json` in the lane root. I removed it in the same command (`rm -f expected.json`). `ls expected.json` then gave "No such file or directory", and `git status --porcelain` matched the pre-sweep state. No tracked file was touched. I deleted the scratch dir `/tmp/tameshi-r42w2-ExecV4Robustness-sweep` before returning.

Verdict: SURVIVES
