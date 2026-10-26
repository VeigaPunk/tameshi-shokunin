# T50ExecSuccC1 — C1 routed item R49.2, first half: a successor read counter

Seat `T50ExecSuccC1` (executor, round 50 wave 1), lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`,
base `e3729de862f73ae080d98fcf522a7081ce16e40a`. Read first: `.ufo/evidence/round-50/contract.json`,
`.ufo/evidence/round-49/c1/measure.py`, `.ufo/waves/round-49/w1/T49CritC1Contract.md` F1-F6,
`corpus/lessons/round-49.md:108-114`. **This is not a claim and not a verdict**: the round-50 C1 counter,
its controls and its deciding run belong to the L1. Nothing in the lane was written except this report
and the deliverable directory `.ufo/waves/round-50/w1/T50ExecSuccC1/`; the round-49 counter is
byte-unchanged (`sha256 a055e9297cc9…6065`, equal to `git cat-file blob bda60768…:.ufo/evidence/round-49/c1/measure.py`).

Axes named: **calibration** (does the read check still accept "no reading"?), **operability** (can a
successor counter be run, self-tested end to end, and audited from its receipts?).

## Deliverable

`.ufo/waves/round-50/w1/T50ExecSuccC1/reads-v2.py` — stdlib, `sha256 a01d88d119d0…42cc9`, 1124 lines.
Interface:

```
python3 -B reads-v2.py --lane LANE --rev REV --trace PATH [--trace PATH …]
                       [--reads PATH] [--headings JSON] [--floors JSON] [--fleet FLEET] [--list]
python3 -B reads-v2.py --selftest
```

Exit 0 pass / 1 measured not-pass / 2 setup error / 64 usage. `--trace` is mandatory: R3 refuses to
run on an unrecorded trace.

What is **unchanged from round 49** (transcribed, not rewritten, so the diff is auditable): the seven
pinned headings (`reads-v2.py:64-72`), the legacy extractor grammar — line pointers, path pointers,
S-ids, in that order, so legacy ordinals never move (`reads-v2.py:153-183`, round-49
`measure.py:86-91,139-169`) — the round-49 resolver (`reads-v2.py:249-272`), the paragraph/table-row rule, the
24-400 character collapsed-excerpt test against the pointed text, the `fleet_commit` handling for
`../` pointers, and an optional floors sidecar (`--floors`) worth the same term. The seven target
sections are read through a local mirror of the round-18 sectionizer (`reads-v2.py:352-403`); at
`bda60768…` it finds all seven, once each (`headings=7/7`).

## The three added rules

**R1 `absent_evidence`** (`reads-v2.py:451-482`, term `absent_bad` + `absent_overflow`). Round 49
accepts an `absent` row with no evidence and never scores it: `.ufo/evidence/round-49/c1/measure.py:271-279`
(`if p['file'] is None … res['absent'] += 1 … continue`), which is F1/F5 and the routed text at
`corpus/lessons/round-49.md:108-114`. v2 admits `absent` only for a path pointer whose token does not
resolve, and only with `absent_evidence = {path, history, not_a_file}` where

* `history` equals `git log --all --format=%H -- <path>` **and that list is empty** (the path never
  existed anywhere in the repository's history), and
* `not_a_file` is a 15-400 char collapsed quote that occurs in the section text, contains the raw
  token, and carries a not-a-file marker (`reads-v2.py:94-96`: "not a file", "placeholder",
  "not in-tree", "unversioned", "never existed", "naming convention", …), and

at most **1 evidenced absent row per section**; each further claim scores `absent_overflow`.

**R2 missed citation forms** (`reads-v2.py:87-89` regexes, `:196-247` extraction, `:309-350`
resolution). Section refs `§N` / `§N-§M` / `§N–§M` inherit the nearest preceding file token in the
paragraph (a table row is its own paragraph) and resolve to the **block** of each numbered heading
(`^#{1,6} N[.)]`) — heading line through the line before the next same-or-higher heading; `FILE#frag`
resolves to the block of the heading whose slug equals `frag` or starts `frag-`; a wildcard path
expands at REV through `git ls-tree -r` + fnmatch and the row's `files` must equal that list exactly.
Each form needs a read row under the unchanged R0 rules (glob rows carry `files` + a section-text
excerpt instead of file/ranges).

**R3 trace with zero inputs** (`reads-v2.py:581-626`, terms `trace_empty` + `trace_missing`). Every
receipt — a `tameshi-trace-inputs-v1` JSON, a doc with a `receipts` list, or a directory of receipts —
must record at least one input; an empty-input receipt scores `trace_empty`, an empty receipt set
scores `trace_missing`. This is the F6 hole: `.ufo/evidence/round-18/measure.py:373-431` lets
`inputs: {}` satisfy the gate.

`total =` missing headings + floor_short + unresolved + unverified + excerpt_miss + not_holds +
absent_bad + absent_overflow + glob_mismatch + trace_empty + trace_missing; the counter prints every
term (`reads-v2.py:661-698`).

## Fixture proof — selftest reaches measure() and each rule fails before / passes after

Command: `TMPDIR=$S python3 -B .ufo/waves/round-50/w1/T50ExecSuccC1/reads-v2.py --selftest`
receipt `selftest.stdout` (22 cases, exit 0):

```
READS_V2_SELFTEST: cases=22 failed=0 measure_calls=28
```

`measure_calls=28` is the point: round 49's selftest never calls `measure()` — 0 occurrences inside
`def selftest()` (`.ufo/evidence/round-49/c1/measure.py:416`, receipt command
`python3 -c "t=open('.ufo/evidence/round-49/c1/measure.py').read(); s=t[t.index('def selftest'):t.index('def main')]; print(s.count('measure('))"` → `0`),
which is the routed mistake at `corpus/lessons/round-49.md:101-103`. Each v2 case builds a real
fixture repo (`git init -q` under `$TMPDIR`, toplevel asserted), commits, and calls `measure()` on it;
before and after are two commits of the same fixture, asserting the **exact term** that fires first:

| rule | case(s) | before (term) | after |
|---|---|---|---|
| R0 end to end | `e2e-before-fails` / `e2e-after-passes` | `unverified=6 unresolved=1 trace_empty=1 total≥8` | `total=0` |
| R1 evidence | `R1-absent-needs-evidence` | `absent_bad=1` | `total=0` |
| R1 history | `R1-absent-history-empty`, `R1-absent-history-unrecorded` | `absent_bad=1` (deleted path has history; unrecorded history) | `total=0` |
| R1 quote | `R1-quote-not-a-file`, `R1-quote-not-in-section`, `R1-quote-token-missing` | `absent_bad=1`, reason matched exactly | `total=0` |
| R1 cap | `R1-absent-cap-per-section` | `absent=2, absent_overflow=1` | `total=0` |
| R2 § | `R2-section-needs-row`, `R2-section-region` | `unverified=1` (no row; wrong region) | `total=0` |
| R2 anchor | `R2-anchor-needs-row` | `unverified=1` twice | `total=0` |
| R2 glob | `R2-glob-expansion-bound` | `glob_mismatch=1` (short list; then a third file added) | `total=0`, `glob_mismatch=1` after growth |
| R3 empty | `R3-trace-empty-refused` | `trace_empty=1` of 2 receipts | `total=0` |
| R3 missing | `R3-trace-missing-refused` | `trace_missing=1` | `total=0` |
| floors | `floor-short` | `floor_short=1` | — |

Census cases (`census-*`) pin the extraction independently of the checker: raw order
`alphabet.md, disc.md, ghost.py, §1, §3-§4, disc.md#box-1, corpus/knowledge/case-*.md`; §3-§4 region
`[[5,6],[7,8]]`; anchor region `[[1,2]]`; glob expansion of two files; token inheritance; contiguous
ordinals. The region expectations are stated from the fixture's own line numbers, not read back from
the resolver.

## Read-only run at the round-49 deciding revision `bda60768afe172fe9e81359f51c835d8d53494d9`

Receipts: `measure-bda60768.stdout`, `measure-bda60768-floors.stdout` (same verdict with the
round-49 floors, `floor_short=0`), `list-bda60768.json`, `r49-list-bda60768.json`,
`legacy-alignment.json`, `forms-missing.txt`, `section-headings.txt`, `glob-expansion.txt`,
`absent-history.txt`.

```
$ python3 -B .ufo/waves/round-50/w1/T50ExecSuccC1/reads-v2.py --lane . --rev bda60768… \
    --trace .ufo/evidence/round-49/coldread/refresh-receipts.json \
    --trace .ufo/evidence/round-49/coldread/traces
READS_V2: self=a01d88d119d0 rev=bda60768… headings=7/7 pointers=113 legacy=94 new=17/1/1
  floor_short=0 unresolved=0 unverified=19 excerpt_miss=0 not_holds=0 absent=0 absent_bad=3
  absent_overflow=1 glob_mismatch=0 traces=14/14 trace_empty=0 trace_missing=0 total=23
  READS_V2_PASS=false
```

`total=23 = 19 (R2: no row) + 3 (R1: no evidence) + 1 (R1: cap)`. Nothing else fires: **the legacy
dimension is intact** — 94 rows match 94 legacy pointers on `(heading, ordinal, raw)` with 0 file and
0 range mismatches (`legacy-alignment.json`, `matched=94`, `pointer_without_row=0`, verdicts
`holds 91 / absent 3`). So v2 is a strict extension of the round-49 read check, not a redefinition.

### The rows the round-49 reads lack (19 pointers, all new forms)

`reads.json` has zero rows for any `§`, `#anchor` or glob pointer. `/tmp`-free census: the round-49
counter at the same revision reports 94 pointers of three kinds only —
`python3 -B .ufo/evidence/round-49/c1/measure.py --lane . --rev bda60768… --list` →
`Counter({'line': 45, 'path': 42, 'sid': 7})`, no `§`/`#`/`*` raw. v2 reports 113
(`section=17, anchor=1, glob=1`).

| form | raw | SKILL.md (REV) | resolves to today |
|---|---|---|---|
| section | `§1` | `SKILL.md:235` | `corpus/knowledge/mutation-case-kimi-census.md:39-78` |
| section | `§3-§6` | `SKILL.md:235` | kimi `109-146, 148-181, 183-191, 193-238` |
| section | `§1-§7` | `SKILL.md:236` | `mutation-case-kagi-census.md:62-103 … 208-246` |
| section | `§0 §2 §3 §4 §5 §6 §7 §10` | `SKILL.md:1384` | `operator-runbook.md:35-41, 93-129, 131-178, 180-241, 243-267, 269-343, 345-406, 462-479` |
| section | `§1–§4` | `SKILL.md:1385` | `fleet-kill-rate-ledger.md:41-88, 90-96, 98-130, 132-158` |
| section | `§1 §2 §3 §4` | `SKILL.md:1387` | `service-optin-protocol.md:54-107, 109-140, 142-180, 182-218` |
| section | `§8` | `SKILL.md:1567` | `incremental-pin-disposition.md:314-388` |
| glob | `corpus/knowledge/mutation-case-*.md` | `SKILL.md:1390` | 9 files (`glob-expansion.txt`; the row's "nine since round 26" claim is now falsifiable) |
| anchor | `reports/round-1-calibration.md#box-1` | `SKILL.md:1467` | `reports/round-1-calibration.md:71-103` |

All 29 resolved section headings exist at REV (`section-headings.txt`), so these are **rows missing
from the reads doc, not broken citations today**. The round-49 doc keeps the bare path
`reports/round-1-calibration.md` and silently drops `#box-1` (`r49-list-bda60768.json`: only
`line|path|sid`, no `#`).

**Correction of the count in the routed text (honesty note).** `corpus/lessons/round-49.md:110-111`
says "21 citation forms (`§` references, `#box-1` anchors, globs) are never extracted". At
`bda60768…` the seven sections carry **19** such pointers (17 `§` occurrences, 1 anchor, 1 glob):
the round-49 report counted *distinct textual forms* (`SKILL.md:235,236,1384,1385,1387,1390,1467,1567`,
plus the directory ref and digest forms in F4's table), while a counter must count *pointer
occurrences*. The difference is a definition, not a contradiction.

### The three `absent` rows

| reads.json | raw | section | v2 |
|---|---|---|---|
| `.ufo/evidence/round-49/c1/reads.json:768` | `mutate_driver.py` | Restore discipline | `absent:no-evidence` |
| `…:951` | `plans/round-N.plan.md` | The map | `absent:no-evidence` + cap |
| `…:975` | `plans/round-N-record-draft.md` | The map | `absent:no-evidence` + cap |

`absent-history.txt`: `git log --all --format=%H --` is **empty for all three** (never existed in any
commit), so R1's history clause is satisfiable by adding evidence — the defect is the missing
`absent_evidence` key and the cap, not a false absence. One further consequence the L1 must see: the
map's two tokens are template conventions and the sentence that declares them not-files
(`SKILL.md:1393`) names "`N`", not the paths, so no admissible `not_a_file` quote exists for them.
Under R1 the map can never carry two absent rows: either the round-50 census drops template tokens
(F4's recommendation) or one of them is cited by a sentence naming it. That is a census/contract
decision, not this seat's.

### Trace

`traces=14/14, trace_empty=0, trace_missing=0` — the two live trace stores are non-empty for all 14
receipts: 7 entries in `.ufo/evidence/round-49/coldread/refresh-receipts.json` (4/4/11/5/7/6/9 inputs)
and the 7 files under `.ufo/evidence/round-49/coldread/traces/` (4-11 inputs each). R3 therefore does
not fire at this revision; it is proven by fixture only, and it is what stops the F6 shape from
returning.

## Findings

1. **R49.2 first half closes with a counter, not prose.** `reads-v2.py` implements R1/R2/R3, runs
   end to end (`--selftest` 22/22 with 28 `measure()` calls), and at `bda60768…` reports
   `total=23, READS_V2_PASS=false` over the same seven sections with the legacy check untouched.
   Command in §"Read-only run"; receipt `measure-bda60768.stdout`. (severity: the deliverable)
2. **`absent` is no longer free.** The round-49 doc's three absent rows fail R1 for lack of
   `absent_evidence` (`reads.json:768,951,975`), and the map's second absent claim is an overflow
   (`absent_overflow=1`). A ghost-pointer flood now costs a `git log --all` per row, a section quote
   naming the token, and 1 row per section — the F1 "cheaper to pass than to fail" inversion is gone.
3. **Nineteen extracted-but-unread citations** (§ ×17, anchor ×1, glob ×1) at
   `SKILL.md:235,236,1384,1385,1387,1390,1467,1567`; every one resolves today
   (`section-headings.txt`, `glob-expansion.txt`), so the round-49 reads are silent where they claim a
   census. The glob is the sharpest: 9 files at REV, and a tenth `mutation-case-*.md` would change
   nothing in round 49's counter.
4. **The legacy dimension was preserved exactly.** 94/94 rows align on heading+ordinal+raw, 0 file or
   range mismatches (`legacy-alignment.json`) — no ordinal drift from appending the new kinds, so a
   round-50 reads doc can be repaired in place rather than rebuilt.
5. **Traces at this revision are non-empty** (14/14, 4-11 inputs each), so R3's cost is paid and not
   waived; the rule is fixture-proven against both the per-receipt and the empty-set shape
   (`selftest.stdout`, cases `R3-*`).
6. **Round-49's selftest gap is fixed in kind**: `measure()` cannot be bypassed in v2's suite because
   the suite only asserts on `measure()` summaries (28 calls). Command: the `python3 -c` one-liner in
   the fixture section returns `0` for the round-49 file and `28` v2 calls are observed in the receipt.

## What this counter cannot see (risks, stated for the L1)

* Path-pointer excerpts are still matched against the **whole file** (the round-49 F8 note, unchanged);
  v2 does not fix that because it was not in R49.2's first half.
* § regions are **blocks**, so appending a line inside a cited section does not invalidate a row, but
  inserting a heading inside it does — a staleness signal by design, at the cost of churn for
  append-only notes whose heading set is stable.
* Duplicate heading slugs are not detected (first match wins), so an anchor could resolve to the wrong
  duplicate; the map's own anchor today is unique (`reports/round-1-calibration.md:71`).
* Glob rows bind the **expansion**, not the prose count ("nine since round 26"); the counter catches a
  tenth file, not a reworded count.
* `absent` history is `git log --all` in the *lane*; a path that only ever existed in the fleet or a
  sibling lane would be admitted as absent if a section quote named it as a non-file.
* Receipts are read at REV only, from the paths passed: an undisclosed trace store is not seen
  (this run passed both stores).

## Operability

* No tool was installed or upgraded (Python 3.14.8, git 2.56.0 suffice); no pacman transaction was
  attempted (host-wide pause respected); no model was passed to any script.
* Every run is read-only against the lane (`git cat-file`, `git ls-tree`, `git log`, `git rev-parse`);
  no index, jj state, or worktree write. Fixture repos are created only under `$TMPDIR`
  (`/fast/scratch/hyaku/tameshi-r50/T50ExecSuccC1`), each `git init -q` with a toplevel assertion, and
  the scratch root is removed before this seat yields; nothing under `/tmp` and nothing under
  `~/.local/state` was read.
* Reproduction, from the lane root:

```
S=/fast/scratch/hyaku/tameshi-r50/T50ExecSuccC1; mkdir -p "$S"
TMPDIR="$S" python3 -B .ufo/waves/round-50/w1/T50ExecSuccC1/reads-v2.py --selftest
TMPDIR="$S" python3 -B .ufo/waves/round-50/w1/T50ExecSuccC1/reads-v2.py --lane . --rev bda60768… --list
TMPDIR="$S" python3 -B .ufo/waves/round-50/w1/T50ExecSuccC1/reads-v2.py --lane . --rev bda60768… \
  --trace .ufo/evidence/round-49/coldread/refresh-receipts.json \
  --trace .ufo/evidence/round-49/coldread/traces --floors .ufo/waves/round-50/w1/T50ExecSuccC1/floors.json
python3 -B .ufo/evidence/round-49/c1/measure.py --lane . --rev bda60768… --list
```

Receipts in `.ufo/waves/round-50/w1/T50ExecSuccC1/`: `reads-v2.py`, `selftest.stdout`,
`measure-bda60768.stdout`, `measure-bda60768-floors.stdout`, `list-bda60768.json`,
`r49-list-bda60768.json`, `legacy-alignment.json`, `forms-missing.txt`, `section-headings.txt`,
`glob-expansion.txt`, `absent-history.txt`, `floors.json`.

## Summary

1. `reads-v2.py` (stdlib, sha256 `a01d88d1…42cc9`) is the successor read counter: the round-49 check over the same seven sections, legacy extractor and ordinals unchanged, plus R1 evidenced/capped `absent`, R2 `§`/`#anchor`/glob pointers each needing a row, R3 non-empty trace receipts.
2. Its selftest runs `measure()` end to end on fixture repos — 22 cases, 0 failures, 28 `measure()` calls (round 49's suite calls it 0 times) — and every new rule is shown failing before and passing after on the same fixture.
3. Read-only at `bda60768…`: `total=23, READS_V2_PASS=false` — 19 pointers with no row (17 `§`, 1 anchor, 1 glob), 3 `absent` rows with no `absent_evidence`, 1 absent-cap overflow.
4. The legacy read dimension is exactly preserved (94/94 rows aligned, 0 file/range mismatches), so the failures are the new rules alone and a round-50 reads doc can be repaired in place.
5. All 19 new-form citations resolve today (29 headings, 9 glob files), so the gap is reads, not citations; the map's two template tokens also cannot carry an admissible not-a-file quote — a census decision the L1 owns.
6. The routed "21 forms" is 19 pointer occurrences at this revision (forms vs occurrences), stated rather than smoothed.
7. Risks: whole-file path excerpts (F8, unchanged), block-range churn, duplicate-slug anchors, glob binding expansion not prose, lane-only absence history, REV-only traces.
8. No tool installed, no lane write outside this report and its receipt directory, scratch removed.
