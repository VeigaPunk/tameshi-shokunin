# T51W2ExecTool30 — C3 registry row audit: `tools/write-path-census.py` (round 51, wave 2)

Seat: executor, round-51 wave 2 (falsify). Item: independently audit the round-51 C3 registry row for
`tools/write-path-census.py` at content candidate `6d8c11e378aa90b12650808e1b79270742935f15`; run the row's
exact self-test and the `--r51-no-such-flag` usage probe from a `--shared` clone at CAND; check every row field
against source; report mismatches, write no source, repair no row.

Read-only on the lane. All experiments ran in `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool30` (a
`git clone --shared` of the lane, `checkout --detach 6d8c11e3`, `git rev-parse --show-toplevel` printed the
clone dir before anything ran), deleted before yield. No tools installed. Raw receipts:
`.ufo/waves/round-51/w2/@P@ExecTool30/` (`summary.txt` is the index; every file cited below is there).
This report is also written byte-identically to `.ufo/waves/round-51/w2/@P@ExecTool30.md` (the seat item's
`@P@` path).

## Reader statement (for the L1's re-key)

I read the section `#### Gate/probe registry — round 51`, SKILL.md:2138-2171 at CAND, and verified its claims
about the row rather than restating them: the row is SKILL.md:2171 (8 cells, sha256 of the line
`52e11693d4b19db63567ac0092a9066b01f08e7798110b4f4e4bee09465457e7`), and every field was checked against
`tools/write-path-census.py` at CAND (blob sha256 `bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62`,
5444 B, 160 lines, mode 100644) and against executed output. Seat T51W2ExecTool30 is available as the named
reader for this heading. The older `### Gate/probe registry` at SKILL.md:1499-1517 holds only the round-12
rows (repeat-control, bash-witness-study) and no write-path-census row; if `refresh.py` computes that heading as
a target, this report does not cover its two rows.

The row under audit, verbatim:

```
| write-path census | gate | `python3 tools/write-path-census.py --census LANE_ROOT` | 0 clean; 1 failed (a listed gate tool missing under LANE_ROOT, or a planted expectation broken in the selftest); 2 could-not-evaluate (usage: no mode, unknown flag) | `python3 tools/write-path-census.py --selftest` → WRITE_CENSUS_SELFTEST: reports planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1 | none — PLANTED, expect and the 21-name GATES list are literals in `tools/write-path-census.py`; the census reads the lane at LANE_ROOT and compares against them | TMPDIR only: the selftest builds a TemporaryDirectory fixture; --census ROOT is read-only | tameshi |
```

## Verdict

**The row passes the frozen C3 predicate for this tool.** Imported from a scratch copy of the frozen
counter (`.ufo/evidence/round-51/c3/measure.py`), the row parses and runs clean:

```
ROW_LINE=2171 ROW_REASON=None ROW_CELLS=8 NAME='write-path census' KIND='gate'
SELFTEST_ARGV=['python3','tools/write-path-census.py','--selftest'] USAGE_ARGV=[...,'--r51-no-such-flag']
SELFTEST RC=0 MARKER_IN_ROW_CELL=True; USAGE RC=2 USAGE_CODE_DECLARED_IN_VERDICT_MAP=True
RUN_ROW=(None, 'WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1')
CLONE_STATUS=''
```

(`counter-runner.out`.) This row is **not** the known clone-context blocker (`round21-measure.py`): the self-test
is green with the tool copied alone into an empty directory, cwd there, under `python3 -I` too.

Two descriptive mismatches survive that pass (M1 material, M2 factual), one precision gap (M3), and three
informational limits of the tool not disclosed in the row (M4-M6). None of them is a false self-test, false exit
code, hidden write, or forged marker.

## Measured runs (exact row commands, stdin /dev/null, TMPDIR an existing scratch dir)

| # | command | rc | last line | wall |
|---|---|---|---|---|
| R1 | `python3 tools/write-path-census.py --selftest` | 0 | `WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1` | 0.027 s standalone; 0.028-0.033 s via the counter's `run_cmd` (3 runs) |
| R2 | `python3 tools/write-path-census.py --r51-no-such-flag` | 2 | stdout empty; stderr last `write-path-census.py: error: unrecognized arguments: --r51-no-such-flag` | 0.027-0.033 s |
| R3 | `python3 tools/write-path-census.py --census .` | 0 | `GATE witness-metadata.py write_sites=13 unflagged=0 sha256=df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4` | 0.038 s |
| R4 | `--census ROOT` with 20 of 21 listed tools absent / nonexistent path | 1 | `MISSING witness-metadata.py` (last of 21), `missing=21` on the summary line | 0.031-0.032 s |
| R5 | no mode; `--census ""` (empty argv value) | 2 | usage on stderr | 0.032 s / 0.028 s |
| R6 | selftest of a scratch copy with `expect` flipped (`unflagged: 2`) | 1 | `FAIL planted unflagged: want unflagged=2 got 1` | 0.028 s |
| R7 | `--census ROOT` with one listed tool `chmod 000` | 1 | stderr ends `PermissionError: [Errno 13] Permission denied: .../tools/env-diff.py` | 0.037 s |
| R8 | `--census ROOT` with a planted unflagged write in `golden-verdict.py` | 0 | summary line `WRITE_CENSUS: gates=21/21 live_write_sites=1 live_unflagged=1 missing=0` | 0.036 s |

R3's first line at CAND: `WRITE_CENSUS: gates=21/21 live_write_sites=99 live_unflagged=0 missing=0` — all 21
listed files exist and the lane currently has no unflagged expected-value write site by this pattern set.

## Field-by-field against source

| Field | Row | Source / observation | Verdict |
|---|---|---|---|
| Name | `write-path census` | tool docstring `tools/write-path-census.py:2-14`; unique row for this tool in SKILL.md | ok |
| Kind | `gate` | `census()` (`:117-143`) fails only when a `GATES` name is absent (`:122-126`, `:143`); the measured finding (`live_unflagged`) never affects the exit (R8) | letter-satisfied, effect overstated — **M1** |
| Entry command | `--census LANE_ROOT` | `main()` `:146-156`; R3 rc 0 at CAND, R4 rc 1 on missing, R5 rc 2 on no mode | ok |
| Verdict map | 0 clean; 1 failed (missing listed tool, or planted expectation broken); 2 could-not-evaluate (usage) | 0/1/2 are the only reachable codes; R1/R4/R6/R5 reproduce each stated cause. An uncaught `PermissionError` also exits 1 (R7), undeclared | ok codes, **M3** on the 1 description |
| Self-test command | `python3 tools/write-path-census.py --selftest` → `WRITE_CENSUS_SELFTEST: …` | `:148` defines the flag; `:151-152` dispatches; the marker is printed by the selftest at `:108-111` — the only place it exists (`python3 … --help` prints `usage: …` as its first token, so the marker is not derivable help text); R1 rc 0, output matches the quoted values exactly | ok |
| Pinned values | `none — PLANTED, expect and the 21-name GATES list are literals in the tool; the census reads the lane at LANE_ROOT and compares against them` | `GATES` 21 names (`:22-44`), `PLANTED` `:57-61`, `expect` `:89`; `census()` references only `GATES`; `PLANTED`/`expect` are consumed by `selftest()` only (`:88`, `:89-92`); no expected count is compared against lane output | `none` correct, "compares against them" **M2** |
| Write scope | `TMPDIR only: selftest builds a TemporaryDirectory fixture; --census ROOT is read-only` | strace `-f`: writes are exactly `<TMPDIR>/write-path-census-*/case.expected` plus one `tempfile.mkstemp` probe file, both unlinked; `--census` makes 0 write/creat/mkdir calls and 0 sockets, all opens under `<clone>/tools`; `git status --porcelain --ignored` empty after all runs | ok, **M5** nuance |
| Owner | `tameshi` | lane identity | ok |

## Mismatches

**M1 (material, `Kind`/`Verdict map`): the census's measured defect never fails the gate.** With an unflagged
expected-value write planted in a listed tool, `--census` prints `live_write_sites=1 live_unflagged=1` and exits
**0** (R8, `census-dirty.out`). The only failure condition is a missing filename from the 21-name literal
(`:122-126`, `:143`, R4). So the row's `0 clean` means "all 21 filenames present under LANE_ROOT", not "the census
found no unflagged write" — and the row never says that. PROTOCOL §Gate standard defines a gate as a script that
"reads surfaces, compares them against expected values persisted in its own repo, and returns a verdict", and "a
tool that cannot fail is a probe". This tool *can* fail (membership check), so `gate` is not literally
contradicted, but the verdict grades tool presence, not the write-path surface the row's Entry column names; the
counts and per-gate sha256s are printed and discarded. The three sibling rows in the same table (`write-form
census v2`, `write-path census v3`, `write-path census v4`, SKILL.md:2168-2170) are all `probe`. Whether the L1
relabels or narrows the `0` sentence is the L1's call; both are row edits, which this seat does not make.

**M2 (factual, `Pinned values`): "the census reads the lane at LANE_ROOT and compares against them".** In
`census()` (`:117-143`) there is no reference to `PLANTED` or `expect`; `expect` is local to `selftest()`
(`:89`) and `PLANTED` is read only at `:88`. Nothing in the tool compares lane content against those two
literals. The only lane-vs-literal comparison is `name in GATES` (`:122-126`), so the sentence is true only if
"them" means the GATES list alone; as written it joins `PLANTED`/`expect` to a comparison that does not exist.
R8 is the behavioural demonstration that no expected count is consulted.

**M3 (precision, `Verdict map`): exit 1 also means could-not-evaluate.** `--census ROOT` with a listed tool
that cannot be read raises an uncaught `PermissionError` and exits 1 (R7, `census-unread.err`); under PROTOCOL
that condition is `could-not-evaluate`, but the row's 1 is `failed` and its parenthetical names only
missing-tool and planted-break. The same table's `frozen registry replay` row (SKILL.md:2156) explicitly
declares "an uncaught traceback also exits 1", so the convention exists here and this row omits it. Low
severity: the code is declared, and the counter never triggers it (it runs only `--selftest` and the usage
probe).

## Informational limits the row does not state (not false claims)

**M4 — the census inventory is 21 of the lane's 30 frozen tools.** `GATES` (`:22-44`) omits, at CAND:
`write-path-census.py` itself, `write-path-census-v2/v3/v4.py`, `pbt-staged-id.py`, `round21-measure.py`,
`shrink-case.py`, `staged-id-guard.py`, `wave-parent-settle.py`. `--census` therefore reports `gates=21/21
missing=0` over a registry that lists 30 tools: a deleted or renamed post-round-39 gate is invisible to it. The
row does say "the 21-name GATES list", so this is not a misstatement; it is a limit a reader of `0 clean`
should see. It also matches the lane's own round-39 measurement (`.ufo/evidence/round-39/census/measure.py`,
which asserts `classified == 21`, `missing == 0`, the sha pin and the `FLAG_GATE` mutant kill — and never
asserts `live_unflagged == 0`).

**M5 — "TMPDIR only" is "a Python temp dir, no lane writes".** With `TMPDIR=/nonexistent-tmpdir-xyz` the
selftest still exits 0 and builds its fixture at `/tmp/write-path-census-bc4cm8al` (Python `tempfile`
fallback), removed (`strace-selftest-missing-tmpdir.txt`). Every TMPDIR-only row in this table shares that
property; no lane path is ever written (M5's strace), so the operative guarantee holds.

**M6 — mode 100644.** `git ls-tree` shows `100644` for this tool, `100755` for `write-path-census-v4.py`. The
row invokes `python3`, and the self-test is green under `python3 -I` from an empty directory, so no operability
impact; noted only because a future row could switch to a shebang invocation and break.

## What this audit does not settle

- I did not decide whether `kind=gate` must become `probe`: that is a row edit and an L1 judgement against
  PROTOCOL. The row's predicate-facing fields are all conforming; M1 is about what the verdict actually grades.
- Counter blind spots beyond this row are the wave-1 C3 findings (harness-masked claims, author-chosen markers,
  `none`/`non-empty` short-circuits). This row's marker is *not* author-chosen: it exists only in the tool's
  selftest print (`:108-111`), and the `--help` first token is `usage:`.
- The C3 blocker that can honestly fail the claim is `round21-measure.py`'s clone-context selftest (rc 1); this
  row does not share it and must not be used to paper over it.

## Cleanup

Scratch `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool30` removed before yield. Lane, fleet and sibling repos
untouched (lane reads via `git show`/clone only; clone `git status --porcelain --ignored` empty at the end).
Written paths: this report, its `@P@ExecTool30.md` twin, and the receipts directory.
