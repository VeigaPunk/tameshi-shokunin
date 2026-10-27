# T51W2ExecTool29 — independent audit, C3 registry row `write-path census v4`

Round 51, wave 2 (falsify), seat T51W2ExecTool29. Lane `tameshi-shokunin` at
candidate `6d8c11e378aa90b12650808e1b79270742935f15` (base `9962033f`). Read-only on the
lane: every run used a `git clone --shared` fixture under
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool29/`, `TMPDIR` inside that root, stdin
`/dev/null`. No lane/fleet/sibling git or jj mutation; no source repair; no row repair.

**Row under audit:** `SKILL.md:2170`, inside the canonical section
`#### Gate/probe registry — round 51` (heading at `SKILL.md:2138`; the table spans
2140–2171 and the section runs to EOF at 2171). It is the only row in the file naming
`tools/write-path-census-v4.py`.

```
| write-path census v4 | probe | `python3 tools/write-path-census-v4.py --file SOURCE.py` (add --json for one JSON object) | 0 clean — every expected-value site reported; 1 failed — selftest mismatch or unreadable input; 2 could-not-evaluate — usage (no arguments, or an unknown flag) | `python3 tools/write-path-census-v4.py --selftest` → WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0 | none — expected classifications are literals in the tool's SELFTEST table | none — reads the named file and prints records; writes no file, selftest classifies in-memory sources | tameshi |
```

## Bottom line

**The row is counter-conformant and passes every field check the frozen C3 predicate runs,
but two of its prose claims are falsified by measurement, and its self-test does not
exercise the behaviour its verdict map describes.** It is *not* the disclosed row-16
blocker (`tools/round21-measure.py`) and it has no clone-context dependency.

1. `# ExecTool29: row is COVERED` — `row_reason` → `None`, `run_row` → `None`, last stdout
   line `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0`, wall 0.09 s (receipt
   `10-counter-row-check.txt`). Full counter at CAND: `covered=29 missing=1
   selftest_fail_rows=2 total=1 C3_R51_PASS=false`; the single `MISSING` is
   `tools/round21-measure.py` (receipt `17-c3-counter-full-at-cand.txt`).
2. **Exit-0 gloss falsified**: "0 clean — every expected-value site reported" is false for
   unparsable input and for writes inside `match`/`case` (findings F1, F2). Both exit 0.
3. **Self-test teeth gap**: the selftest never runs `main()`; killing the whole text-mode
   report, hardcoding `return 0`, and hardcoding the marker all leave the registered
   selftest green with the identical last line — and the counter still accepts a clone whose
   census reports nothing (F4, receipt `11-decisive-mutant-clone.txt`).

## Row cells against the source

Tool read at `git show 6d8c11e3:tools/write-path-census-v4.py` (695 lines). Line cites below
are that file unless stated.

| # | Cell | Row says | Measured against source | Verdict |
|---|---|---|---|---|
| 1 | Name | write-path census v4 | docstring line 2: "F4 write-path census v4" | TRUE |
| 2 | Kind | `probe` | census mode (`--file`) always exits 0 when the file is readable, including when it reports `unflagged=1`; it returns no verdict ⇒ PROTOCOL "a tool that cannot fail is a probe" | TRUE |
| 3 | Entry command | `--file SOURCE.py`, "(add --json for one JSON object)" | `--file`/`--json` exist (:663-665); `--json` prints exactly one object with `file` and `sites` (:673) | TRUE |
| 4a | Verdict map, 0 | "0 clean — every expected-value site reported" | **FALSE as a completeness claim** — F1, F2 | **MISMATCH** |
| 4b | Verdict map, 1 | "1 failed — selftest mismatch or unreadable input" | exit 1 = selftest mismatch (:658) and unreadable input (uncaught `FileNotFoundError`/`PermissionError`/`IsADirectoryError` at :670) | TRUE — and *more* accurate than the tool's own docstring, see D1 |
| 4c | Verdict map, 2 | "2 could-not-evaluate — usage (no arguments, or an unknown flag)" | no args → 2 (`print_usage` + `return 2`, :690-691); unknown flag → 2 (argparse) | TRUE |
| 5 | Self-test command | `` `python3 tools/write-path-census-v4.py --selftest` `` → `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0` | exit 0, stdout exactly that one line, stderr empty, 45 ms, from a `git clone --shared` at CAND with scratch TMPDIR and stdin `/dev/null`; `cases=15` = `len(SELFTEST)` (15 literal keys, :462-643) | TRUE |
| 6 | Pinned values | "none — expected classifications are literals in the tool's SELFTEST table" | true: 15 inline `(source, want)` literals at :462-643; no external pinned file; flipping one literal flips the verdict (`failed=1`, exit 1) | TRUE |
| 7 | Write scope | "none — reads the named file and prints records; writes no file, selftest classifies in-memory sources" | true: only file open is the read at :670; selftest classifies string literals only; after all runs `git status --porcelain` = 0 lines, TMPDIR residue 0, no `__pycache__`/`.pyc` | TRUE |
| 8 | Owner | `tameshi` | — | TRUE |

## Findings

### F1 (material) — exit 0 does not mean "every expected-value site reported": unparsable input is silently clean

`classify_source` catches `SyntaxError` and appends one record with `kind='parse-error'` and
**`'expected': False`** (:441-461, `'expected': False` at :447). The text-mode printer filters
`if rec['expected']:` (:676), so the parse-error record is **dropped from the output that the
row's own entry command produces**. Measured on a 1-line file with a syntax error:

```
exit=0  stdout_bytes=0  stderr_bytes=0
```

— indistinguishable from "this file has no expected-value writes". The record *is* visible in
`--json` mode (`"kind": "parse-error"`), but the row's entry command is the text form and the
row carries no parse-error caveat (receipt `13-exit0-gloss-falsified.txt`, item (a)/(b)).

A second instance of the same bucket: a file containing a NUL byte also exits 0 with
`stdout_bytes=0` in text mode, and emits `{"kind": "parse-error", "lineno": 0}` only under
`--json` (receipt `12-extra-exit1-paths.txt`, items (a)/(a2)). Both are parse failures graded
`clean`.

Class under PROTOCOL §Verdict: exit 0 = `clean`. A file the tool could not parse is graded
`clean`.

### F2 (material) — expected-value writes inside `match`/`case` are never reported, and exit is still 0

`_walk_stmts` (:409-432) descends only into `('body', 'orelse', 'finalbody')` (:427) plus
`stmt.handlers` (:431). `ast.Match` stores its bodies in `.cases`, which is never visited.
Minimal repro, exit 0, no output in text mode and `sites: []` in JSON mode:

```python
match 1:
    case 1:
        with open("expected.json", "w") as fh:
            fh.write("x")
```

The identical write under `if 1:` is reported. A 6-write fixture (if/else/for/while/try/match)
reports 5. This is the sharpest falsification of cell 4a: an expected-value site exists, is not
reported, and the exit code is 0 (`clean`). Receipt `08-coverage-gap-match-and-mode.txt`.

Corroborating inconsistency: the tool's docstring says "Control flow ... stay out of scope"
(:40-41) yet `if`/`else`/`for`/`while`/`try` bodies **are** walked. A reader trusting the
docstring will not know that every control-flow form except `match` is scanned, so the
`match` hole is easy to miss. See D2.

### F3 (minor) — a second undocumented exit-1 path: an uncaught traceback on unreadable input

`--file` on a missing path, a directory, or a mode-000 file produces an uncaught Python
traceback and exit 1 (receipt `04-exit-sweep.txt`):

```
FileNotFoundError: [Errno 2] No such file or directory: '.../missing.py'   exit=1
IsADirectoryError: [Errno 21] Is a directory: '.../edge/dir_target'        exit=1
PermissionError:  [Errno 13] Permission denied: '.../edge/noperm.py'       exit=1
```

The row declares this under 1 ("or unreadable input"). The tool's own docstring (:49) declares
only `0 pass · 1 selftest fail · 2 usage`, i.e. the tool's documented contract is *narrower*
than the row. This is a tool-docstring defect, not a row defect (D1).

Also undeclared: **130** on SIGINT (`KeyboardInterrupt`, measured). PROTOCOL's escape hatch
applies ("an undeclared nonzero code reads as could-not-evaluate"), and **no row in the whole
`SKILL.md` declares 130** — this is a lane-wide convention, not a defect of this row
(receipt `07-undeclared-exit-codes.txt`).

### F4 (material, decisive) — the registered self-test does not exercise the behaviour the row's verdict map describes, and the counter cannot tell

`selftest()` (:645-658) only calls `classify_source()` on in-memory strings. It never calls
`main()`, so it never exercises `--file`, the text-mode print loop (:675-689), the JSON print
(:673), the exit-code mapping, or the usage path.

Mutation battery against the row's exact self-test command (copies of the CAND tool, run
outside the clone; receipt `06-mutation-battery.txt`, `14-literal-sensitivity.txt`):

| Mutation | Selftest |
|---|---|
| `write_text`/`write_bytes` detection removed (:329) | **KILLED** `failed=3` |
| `OUTPUT_FLAGS` emptied | **KILLED** `failed=8` |
| `MAX_DEPTH 8 → 1` | **KILLED** `failed=10` |
| `WRITE_MODES` emptied | **KILLED** `failed=9` |
| `expected = False` (:373) | **KILLED** `failed=15` |
| `unflagged` always False | **KILLED** `failed=8` |
| `EXPECTED_RE` neutered (:57) | **KILLED** `failed=15` |
| `golden|snapshot` dropped from `EXPECTED_RE` | **KILLED** `failed=2` |
| `'tempfile'` **and** `'mkdtemp'` markers both removed | **KILLED** `failed=2`, exit 1 (receipt `19-joint-marker-mutant.txt`) |
| text-mode filter `if rec['expected']:` → `if False:` (:676) | survives, `failed=0`, exit 0 |
| text filter → `if rec['expected'] and not args.json:` | survives, `failed=0`, exit 0 |
| `selftest()` `return 0` unconditionally (:658) | survives, `failed=0`, exit 0 |
| marker hardcoded to `cases=15 failed=0` (:657) | survives, `failed=0`, exit 0 |
| one of `'tempfile'`/`'mkdtemp'` removed singly | survives — equivalent mutant (the other marker still matches) |

So: the classifier core is well covered (9 mutants killed, including the joint-marker one),
but **the reporting path, the exit-code discipline and the marker's derivation have zero
coverage**. That is exactly the surface cell 4a and the row's Self-test cell are about.

**Decisive test.** I built a clone at CAND whose tool has (a) the text-mode report dead
(`if False:`), (b) `return 0` unconditionally, (c) the marker hardcoded. The counter's own
`run_row` against that clone:

```
run_row verdict = None   <-- the counter STILL ACCEPTS the row
last stdout line = 'WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0'
```

while the same clone's tool reports nothing at all:

```
python3 tools/write-path-census-v4.py --file writer.py   -> exit=0, stdout_bytes=0
python3 tools/write-path-census-v4.py --selftest         -> exit=0, same marker
```

Receipt `11-decisive-mutant-clone.txt`. Consequence for the frozen predicate as applied to
this row: "self-test exits 0 and prints a last-line finding id recorded in the row" is a
*receipt* check, not a capability check. For this row it admits a census that reports nothing.

### F5 (minor) — `EXPECTED_RE` over-classifies (false positives), so "expected-value site" is not a tight notion

`EXPECTED_RE = re.compile(r'expected\.json|expected\.txt|\.expected\b|golden|snapshot')` (:57)
is unanchored. Measured, all classified `expected=1` and exit 0:

```
mygoldens/notes.txt      -> expected=1
goldens/notes.txt        -> expected=1
snapshotter/x.bin        -> expected=1
expected.json.bak        -> expected=1
notes.txt                -> (not reported)
```

Receipt `15-sibling-census-rows.txt` (second half). Cell 4a's gloss is falsified in both
directions: under-reporting (F1, F2) and over-reporting (F5).

### F6 (minor) — a non-literal `open()` mode is not a write form

`_write_call` requires the mode to be an `ast.Constant` in `WRITE_MODES` (:318-327). A fixture
with three expected-value writes (`class` body, `async def`, `open(p, mode_var)`) reports 2.
Same class as F2 (silent under-report with exit 0); arguably inside the docstring's
"unrecognized ... calls stay out of scope" wording.

## Disclosures (not row defects, recorded for the L1)

- **D1 — the row is more accurate than the tool's docstring.** `tools/write-path-census-v4.py:49`
  says `Exit codes: 0 pass · 1 selftest fail · 2 usage`; the row adds "or unreadable input" to
  exit 1, which is what the code actually does (F3). Anyone reconciling the two should fix the
  docstring, not the row.
- **D2 — the docstring's scope sentence is imprecise.** ":40-41" says control flow stays out of
  scope, but five of six control-flow forms are walked (F2). Only `match`/`case` is dropped.
- **D3 — the marker is genuinely computed, but only the first token is counter-checked.**
  `print('WRITE_CENSUS_V4_SELFTEST: cases=%d failed=%d' % (len(SELFTEST), len(failed)))`
  (:657) really derives both numbers, and the number moves under real breakage (F4 table).
  The counter takes `last.split()[0]` = `WRITE_CENSUS_V4_SELFTEST:` and only requires that
  token in the row's cell, so the row's `cases=15 failed=0` is **independently true but not
  counter-guarded** (verified: `len(SELFTEST)=15`, `failed=0`).
- **D4 — `probe` vs `gate`.** The census entry command genuinely cannot fail on findings, so
  `probe` is right for PROTOCOL §Gate standard. The row's "1 failed" class exists only for the
  selftest and crash paths, exactly as in the sibling `write-path census v2`/`v3` rows — lane
  convention, not a defect.
- **D5 — the row is new at CAND; the tool is untouched.** `git diff base..CAND --
  tools/write-path-census-v4.py` is empty; the tool is in the frozen 30 at base and carries
  `selftest`; base `SKILL.md` has **0** occurrences of `write-path-census`, CAND has 1. This
  row is one of the 12-tool gap in the L1's disclosed N1 correction (receipt
  `16-base-vs-cand.txt`).

## Not the row-16 blocker

The disclosed C3 blocker is `tools/round21-measure.py --selftest` exiting 1 inside the
counter's fresh clone because its fixture expects sibling fleet repos (data row 16 of the
round-51 table = `SKILL.md:2157`; reproduced at receipt `09-clone-independence.txt` (d)):
`CalledProcessError: git -C ... show 08175c62...:tools/mutate-and-run.sh ... exit status 128`.

**The row under audit is not that row, and its tool has no clone-context dependency.** The
registered self-test exits 0 in three independent contexts: (a) the counter's fresh
`git clone --shared` at CAND, (b) the tool file copied alone into an empty directory with
cwd there, (c) cwd `/` with an absolute path. It classifies in-memory string literals and
reads no repo file (receipt `09-clone-independence.txt` (a)-(c)).

## The other counter failure (context, not this row)

`selftest_fail_rows=2`: one is round21-measure (above). The second is the **round-12**
`bash declared-witness study` row at `SKILL.md:1504`, whose Self-test cell is a bare
`` `python3 tools/bash-witness-study.py selftest` `` with no finding-id token, so the
counter's marker check fails; the round-51 row at `:2142` supersedes it and passes, and the
tool's own selftest exits 0 either way. Neither is row 2170 (receipt
`18-counter-failing-rows.txt`).

## Risks the L1 should weigh (not decisions I take)

- Cell 4a is the only falsified field, and it is prose inside a verdict-map cell. The frozen
  predicate reads it for the tokens `0` and `1` only, so it cannot see the mismatch. An
  operator reading "0 clean — every expected-value site reported" gets a false completeness
  guarantee on unparsable files and on `match`/`case` writes (F1, F2).
- F4 means the row's evidence for "the census works" is weaker than it reads. This does not
  invalidate C3's counter for this row (the row *is* covered), but it does mean a
  census-tool row cannot be taken as behavioural evidence on the strength of its selftest.

## Receipts

All under `.ufo/waves/round-51/w2/@P@ExecTool29/`:

| File | Contents |
|---|---|
| `00-fixture.txt` | clone path, `rev-parse --show-toplevel`, HEAD = CAND |
| `01-row-raw.txt` | `SKILL.md:2170` verbatim |
| `02-selftest.txt` / `.stdout` / `.stderr` | row's exact self-test: exit, wall, last line, stderr bytes |
| `03-usage.txt` / `.stdout` / `.stderr` | usage probe `--r51-no-such-flag`: exit, wall, stderr |
| `04-exit-sweep.txt` | exit codes over 13 argv/input shapes |
| `05-write-scope.txt` | clone git status, TMPDIR residue, `__pycache__` count |
| `06-mutation-battery.txt` | 16 mutants of the tool vs the row's self-test |
| `07-undeclared-exit-codes.txt` | SIGINT → 130; EPIPE |
| `08-coverage-gap-match-and-mode.txt` | F2/F6 repros and controls |
| `09-clone-independence.txt` | selftest in clone / isolated dir / cwd `/`; round21 blocker contrast |
| `10-counter-row-check.txt` | counter `row_reason` / `run_row` on row 2170 |
| `11-decisive-mutant-clone.txt` | dead-report clone still accepted by the counter |
| `12-extra-exit1-paths.txt` | NUL byte, deep nesting, control |
| `13-exit0-gloss-falsified.txt` | F1 repro, JSON contrast, control, `unflagged=1` at exit 0 |
| `14-literal-sensitivity.txt` | expected literals drive the verdict |
| `15-sibling-census-rows.txt` | all four census rows at CAND; F5 false positives |
| `16-base-vs-cand.txt` | tool unchanged; row new; frozen-30 membership |
| `17-c3-counter-full-at-cand.txt` | full counter `--explain` output at CAND |
| `18-counter-failing-rows.txt` | the two failing rows are 2157 and 1504, not 2170 |
| `19-joint-marker-mutant.txt` | both scratch markers removed → selftest KILLED (exit 1, failed=2) |

Scratch root `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool29/` deleted before this seat
yielded. No pacman/install activity.
