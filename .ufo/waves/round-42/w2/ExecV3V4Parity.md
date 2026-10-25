# ExecV3V4Parity — round 42 wave 2 (FALSIFY): census v3 vs v4 parity

Seat: `L1Tameshi42.ExecV3V4Parity`. Attacked object: `tools/write-path-census-v4.py` (C2). Lane checkout read at
HEAD `a21845f523b75adbd3e3f7a62af91294db224ad9`, labelled **pre-run**. No counter was run in default mode. No lane
file was edited except this report. The scratch dir `/tmp/tameshi-r42w2-ExecV3V4Parity-out` was deleted before return.
Tools installed: none.

## Findings

### F1. Text-mode parity: only 4 lines differ, in 3 of 26 files; none is a regression

Command (cwd lane): for every `git ls-files 'tools/*.py'` (26 files), `python3 tools/write-path-census-v3.py --file F`
with the last line dropped (`head -n -1`), diffed against `python3 tools/write-path-census-v4.py --file F`. Every run
exited with code 0. 23 files are byte-identical. These are the differing lines:

| Site | v3 text | v4 text | Cause | Verdict |
|---|---|---|---|---|
| `tools/context-capture.py:1682` (open `wb`) | `scratch=0 unflagged=1 …self.case_dir(name)…` | `scratch=1 unflagged=0 …os.path.join(self.root, "{:02d}-{}".form` | attribute/method fold | correct hide (v3 false positive) |
| `tools/context-capture.py:1685` (open `w`) | same as 1682 | same as 1682 | attribute/method fold | correct hide (v3 false positive) |
| `tools/registry-replay.py:123` (write_bytes) | `scratch=0 unflagged=1 expected.json` | `scratch=0 unflagged=0 expected.json argparse --out` | output flag | correct hide (v3 false positive) |
| `tools/wave-accounting.py:165` (write_text) | `scratch=1 unflagged=0 …'tam` | `scratch=1 unflagged=0 …tame` | depth raise (4 to 8) | text only; classification unchanged |

Evidence for the causes:
- **context-capture 1682 and 1685.** `tools/context-capture.py:1660` `directory = self.case_dir(name)`. At `:1631-1635`,
  `case_dir` has one top-level `return path`, with `path = os.path.join(self.root, …)` at `:1633`. `self.root` has
  exactly one assignment in the class: `:1624-1625` `self.root = tempfile.mkdtemp(prefix="context-capture-selftest-", dir="/tmp")`
  (`rg -n 'self\.root\s*[+]?='` finds only `:1624`). The site is the selftest harness writing into a mkdtemp dir, so
  v3's `unflagged=1` was a false positive. The v4 code paths are `tools/write-path-census-v4.py:195-199` (method
  fold) and `:207-209` (attribute bind).
- **registry-replay 123.** It writes `out / 'expected.json'` inside `publish` (`tools/registry-replay.py:116`). Its
  only two in-module callers are `:185 publish(…, out)`, with `out = Path(args.out)` at `:181`, and
  `:282 publish(…, Path(a.out))`, with `a = p.parse_args()` at `:262` and `p.add_argument('--out')` at `:259`.
  `run_replay` is called only at `:287 run_replay(a)`. The destination is therefore operator-chosen, so v3's
  `unflagged=1` was a false positive. The v4 code paths are `:278-309` (`_out_flag`) and `:227-275`.
- **wave-accounting 165.** v3 at depth 4 stops before the `prefix=` constant. v4 at depth 8 folds it, so the
  80-character text gains the unquoted `tameshi-r22-accounting-`. The scratch bit was already 1 and stays 1.

The text-mode `unflagged=1` lines in v3 are exactly the three contract sites. All three became 0 in v4, and no site
that v3 printed is missing from v4.

### F2. Record-level parity: every changed record has exactly one cause, with zero unexplained changes

Method: load both modules in-process and compare `classify_source` record by record on all 26 files. Sites are 111
in v3 and 111 in v4, with an identical `(lineno, kind)` set. `unflagged` totals are 3 in v3 and 0 in v4.

Attribution: each record was compared across v3, v3 patched to `MAX_DEPTH=8`, v4, v4 with `_out_flag` returning
None, v4 with `ClassInfo.attrs={}` and `method_return` returning `(None, None)`, and v4 patched to `MAX_DEPTH=4`.

- 45 records differ between v3 and v4. Each one has exactly one cause, and none has the cause `NONE`.
- **Depth raise (35 records).** For each, v3@8 equals v4 and v4@4 equals v3. Only two of these change a
  classification bit:
  - `tools/env-diff.py:171` scratch 0 to 1. It is `expected=0`, so `unflagged` is unaffected.
  - `repeat-control.py:811`, `:820` and `wave-accounting.py:165` are `expected=1`, but only their resolved text
    changed. Scratch was already 1.
- **Attribute/method fold (3 records).** `context-capture.py:1667` is the `receipt.json` write, scratch 0 to 1 with
  `expected=0`. The other two are `:1682` and `:1685`, with `unflagged` 1 to 0.
- **Output flag (7 records).**
  - `registry-replay.py:123` changes `unflagged` from 1 to 0.
  - `:122`, `:125`, `:183`, `env-diff.py:239` and `trace-inputs.py:690` gain `argparse --out` text, with `expected=0`.
  - `registry-replay.py:211` is depth-only and is counted under the depth raise.
- No record changed `expected`.

### F3. The fold and flag hides depend on their stated cause, not on names or line numbers

Each probe applies a single in-memory textual mutation to the live source and then calls v4's `classify_source`:

| Mutation | Result |
|---|---|
| context-capture baseline | 1682 and 1685: `scr=1 unf=0` |
| `self.root` = `os.path.join(REPO, "fixtures")` | `scr=0 unf=1` (lines shift to 1681/1684) |
| extra `self.root = "fixtures"` in `__init__` (ambiguous binding) | `unf=1` |
| `case_dir` given two returns | `unf=1` |
| `case_dir` renamed to `bucket` (3 occurrences) | still `scr=1 unf=0`, so the hide is not name-keyed |
| registry-replay baseline | 123: `out=1 unf=0` |
| `--out` changed to `--source` | `out=0 unf=1` |
| `--output-dir` with `dest='out'` | `out=1 unf=0` |
| extra caller `publish(…, Path("fixtures"))` | `out=0 unf=1` |
| `a = p.parse_args()` changed to `a = load_cfg()` | `unf=1` |
| `run_replay(a)` changed to `run_replay(cfg)` | `unf=1` |
| `out = Path(args.out)` changed to `Path("fixtures")` | `unf=1` |

Selftests: `python3 tools/write-path-census-v3.py --selftest` printed
`WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` and exited 0.
`python3 tools/write-path-census-v4.py --selftest` printed `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0` and exited 0.

JSON needle check: `python3 tools/write-path-census-v4.py --file tools/context-capture.py --json` gives
`"mkdtemp" in resolved` = True for 1682 and 1685, with scratch True and unflagged False. For
`tools/registry-replay.py`, 123 has `"--out" in resolved` = True, explicit_out True and unflagged False.

### F4. Latent regression vector from the depth raise (synthetic only, not live)

The scratch bit is a substring test of `SCRATCH_MARKERS` over the whole trace (`tools/write-path-census-v4.py:373-375`).
The trace of a Call includes every argument's source text. Raising `MAX_DEPTH` from 4 to 8 (`:71`) lets a marker from
a non-root argument five or more hops upstream mark a repo-bound expected site as scratch. Probe source:

```python
import os
def repo_root(log):
    return "."
r0 = repo_root(log="/tmp/census.log")
r1 = r0
r2 = r1
r3 = r2
r4 = r3
with open(os.path.join(r4, "fixtures", "expected.json"), "w") as fh:
    fh.write("x")
```

- v3 gives `L9 scr=0 unf=1`, which is correct because the destination is `./fixtures/expected.json`.
- v4 gives `L9 scr=1 unf=0`, so it **hides** a site that v3 flagged correctly.
- Control, the same code using `r0` (one hop): v3 and v4 both give `scr=1 unf=0`. The heuristic weakness predates v4,
  and the depth raise extends its reach.
- Live impact on this lane: none. Per F2, no `expected=1` record changed scratch through the depth raise.
- No contract fixture or declared mutant covers "depth-only scratch hide". It cannot be killed by the attr, method or
  outflag mutant classes.

### F5. Minor text-mode divergences (not classification)

- v4 text mode prints no trailing totals line, while v3 prints one (`tools/write-path-census-v3.py:339`, compared with
  v4 `:675-688`). The contract `tool_interface` only requires "v3's line format". A consumer that reads the v3 totals
  line from v4 text output gets nothing.
- The 80-character text truncation (`v4:686`) hides the `mkdtemp` needle for 1682 and 1685, which is only visible in
  `--json`. The contract's "resolved text naming mkdtemp" holds in JSON mode only.

## Verdict

SURVIVES. Every v3/v4 difference across the 26 tracked `tools/*.py` files is explained by the attribute/method fold,
the output flag, or the depth raise. The only three live hides are the contract's v3 false positives, and there is no
live regression. The F4 latent depth-raise hide is a synthetic risk to route, not a live break.
