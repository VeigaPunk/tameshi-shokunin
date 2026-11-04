# T72W1S05 — PROVINCE round-72 correction: measurement + draft (status: superseded by a landing, kept as an independent cross-check)

Seat: T72W1S05 (scribe, wave `w1`). **Status.** This draft was measured and
written against the lane at `HEAD=dfb534ca` (round-72 planning commit), before
any correction landed. While this seat was measuring, the C2 work landed
independently at `d618518a` ("round-72 C2: S303 supersedes S302 (§4.2, page
lines 2446-2449); PROVINCE append corrects :85-91 to :88-94/:88-97"), and the
lane has since moved to `de43f7dc`. The landed append is **not** derived from
this draft, and this draft's append bytes were **never** appended — doing so now
would duplicate the correction. The value of this file is therefore:
(1) an independent measurement of the same spans, (2) a byte-level comparison
against the landed text (§5), and (3) fixture receipts proving the tokens bind
and the two row shapes behave as measured (§6), plus the instrument findings
routed in the seat report.

Base revision `f20ba482c7441d4c75818e7cd8a3165fee7821a1` (= `origin/master`).
`tools/mutate-and-run.sh` is one blob at base and at `dfb534ca`:
`51fa5bc8ac2c863ec754ac87a1e3227a18c79d67`, sha256
`977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`.

## 1. Measured line map — `tools/mutate-and-run.sh` at base

| item | line |
|---|---|
| `--regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten)` header | **84** |
| prose continuation of the header ("mutation cases, replayed as legs…" / "and its recorded verdict table…" / "expectation:") | 85, 86, 87 |
| leg 1 `js-kimi-census` — **first leg line** | **88** |
| leg 2 `bash-surface-census` | 89 |
| leg 3 `bash-tsukuroi-census` | 90 |
| leg 4 `bash-mado-verify` | 91 |
| leg 5 `bash-checklist-run` | 92 |
| leg 6 `js-claims-check` | 93 |
| leg 7 `js-round-gate` | **94** |
| leg 8 `js-sources-check` | 95 |
| leg 9 `js-cite-check` | 96 |
| leg 10 `bash-drift-pins` — **last leg line** | **97** |

Spans, as the pointer tool's engine of record reads them
(`git cat-file blob <rev>:tools/mutate-and-run.sh | sed -n 'START,ENDp'`):

- **seven-leg cut = `:88-94`** — 7 lines; leg 7 at 94; needle `js-round-gate`
  occurs in the span (1 occurrence).
- **ten-leg ledger = `:88-97`** — 10 lines; leg 10 at 97; needle
  `bash-drift-pins` occurs in the span (1 occurrence).

Independent corroboration in committed bytes (r51 cold read measured the same
map): `.ufo/evidence/round-51/coldread/reads/T51W2Read12.md:29` — "header
`:84` '… r26 nine; r51 ten', leg list `:88-97`" — and `T51W2Read11.md:45` —
"the ten-entry list now lives at :88-97 (six-leg content :88-93)".

## 2. What base lines 85–91 actually carry (the stale cell's target)

First words of each line, base `f20ba48`:

```
85: # mutation cases, replayed as legs. Each leg carries its recorded revision pin
86: # and its recorded verdict table; the recorded kill-rate is the leg's
87: # expectation:
88: #   js-kimi-census        kumitate-shokunin/scripts/kimi-census.mjs   8/10 (80 %)
89: #   bash-surface-census   kagi-shokunin/corpus/surface-census.sh      8/10 (80 %)
90: #   bash-tsukuroi-census  tsukuroi-shokunin/tools/tsukuroi-census.sh  6/10 (60 %)
91: #   bash-mado-verify      mado-shokunin/tools/mado-verify.sh          4/10 (40 %)
```

So 85–91 = the header's three narrative lines + legs 1–4; leg 7
(`js-round-gate`) is not in the span, which is why the red arm
`province-r16-sevenleg-85-91` reads `miss ok`.

## 3. Why the cell was right when it landed (measured)

| rev | landing | header | leg 1 | leg 7 / leg 10 |
|---|---|---|---|---|
| `c699c8c3` | round 16 | 81 | 85 | leg 7 `js-round-gate` at 91 |
| `58e5d53d` | round 18 | 82 | 86 | leg 7 at 92, leg 8 at 93 |
| `a08e85c5` | round 26 | 83 | 87 | leg 7 at 93, leg 9 at 95 |
| `6d8c11e3` | round 51 | 84 | 88 | leg 7 at 94, leg 10 at 97 |
| `f20ba48` | base | 84 | 88 | leg 7 at 94, leg 10 at 97 |

At `c699c8c3` the seven legs sat exactly at 85–91, so the round-16 cell was true
at its own landing. The block then moved down one line per later landing (the
docstring above it grew by one line each time) while the legs' own bytes did
not change: `c699c8c3:85-91` is byte-identical to `f20ba48:88-94` (`diff`,
empty output). The correction is to the pointer, not to the method.

## 4. Draft append that was NOT landed (do not append)

These bytes were prepared for a clean `cat >> PROVINCE.md` on base (145-line)
bytes; they would have put a heading at 147 and the two tokens at 158 (`:88-94`)
and 155 (`:88-97`). **They were not used**: PROVINCE.md already carries a
differently written, independently authored correction at lines 147–160
(commit `d618518a`), and `git diff --numstat d618518a^ d618518a -- PROVINCE.md`
is `15	0`. Appending this block now would duplicate the correction, so it is
recorded here as a fenced sample only (no file on disk carries these bytes):

```

## Core — round 72 append (2026-11-03)

Correction to the round-16 append above (line 57), appended; line 57 stands
unchanged as the record of what round 16 measured. At base `f20ba48`
(byte-identical at this round's planning tip `dfb534ca`) `tools/mutate-and-run.sh`
— blob `51fa5bc8ac2c863ec754ac87a1e3227a18c79d67`, sha256
`977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda` — carries
its `--regression (r4-2; … r51 ten)` header line at line 84, then three prose
lines (85-87), and the ten-leg ledger at `:88-97`: leg 1 `js-kimi-census` at
line 88, leg 7 `js-round-gate` at line 94, leg 10 `bash-drift-pins` at line 97
(the last leg line). The seven-leg cut the round-16 append recorded is
`:88-94` at this base — legs 1-7, leg 7 at line 94; it sat at the `:85-91` that
append names when that append landed (`c699c8c3`: legs at lines 85-91, header
at 81). The seven legs' bytes have not changed since (`c699c8c3` lines 85-91
are byte-identical to base lines 88-94), and the pointer drifted one line per
later landing — r18, r26 and r51 put the header at 82, 83, 84 and leg 1 at 86,
87, 88 — as the docstring above the ledger grew by one line at each of those
landings. Leg names, order and recorded kill-rates are unchanged: the
correction is to the pointer, not to the method.
```

## 5. Comparison with the landed text (commit `d618518a`, PROVINCE 147–160)

Landed append (quoted from the committed bytes, first words per line):

```
147: Corrections, appended at round 72 (the round-16 append's spans, re-measured):
149: The round-16 append above says "the seven-leg list now sits at `:85-91`".
150: Measured this round on the committed bytes (`grep -n` over
151: `tools/mutate-and-run.sh`): line 84 is the `--regression` header, lines
152: 85-87 are the narrative that introduces the legs, and legs 1-4 sit at
153: 88-91 - so `:85-91` carries the narrative plus four legs, not seven. The
154: seven-leg cut (legs 1-7) is `:88-94`, leg 7 `js-round-gate` at line 94; the
155: ten-leg ledger (the r51 leg cut) is `:88-97`, leg 10 `bash-drift-pins` at
156: line 97. The stale cell stands append-only (the lane's correction rule), and
157: `tools/pointer-recheck.json` measures it on every sweep: the red row
158: `province-r16-sevenleg-85-91` still reads miss, and the round-72 rows
159: `province-r72-sevenleg-cut-88-94` and `province-r72-tenleg-88-97` read hit
160: against these spans.
```

| load-bearing fact | this draft | landed text | measured (base) | agree |
|---|---|---|---|---|
| header line | 84 | 84 | 84 | yes |
| narrative lines | 85–87 | 85–87 | 85–87 | yes |
| legs 1–4 | 88–91 | 88–91 | 88–91 | yes |
| seven-leg cut | `:88-94`, leg 7 at 94 | `:88-94`, leg 7 at 94 | 88–94, leg 7 at 94 | yes |
| ten-leg ledger | `:88-97`, leg 10 at 97 | `:88-97`, leg 10 at 97 | 88–97, leg 10 at 97 | yes |
| line 57 | untouched | untouched ("stands append-only") | untouched | yes |
| drift history (c699c8c3 / r18 / r26 / r51) | carried | not carried | measured (§3) | n/a |
| blob identity (oid + sha256) | carried | not carried | 51fa5bc8… / 977de470… | n/a |

Differences are additive vs terse, not factual: the landed text omits the blob
identity and the landing-history proof and cites the two manifest row ids by
name (both rows exist; §6 shows their verdicts). Tokens in the landed file:
`:88-94` at line 154, `:88-97` at line 155, `:85-91` at 149 and 153 (plus the
pre-existing line 57).

## 5b. Third correction (six-leg anchor), measured after it landed

The L1 accepted F3 and appended a second block at `PROVINCE.md:162-170`
(commit `b7b98375`, `10	0`, line 57 untouched), then pinned it: row
`province-r72-sixleg-cut-88-93` (record `PROVINCE.md @ d7eb02c2`, pointer
`:88-93`, target `tools/mutate-and-run.sh @ d7eb02c2`, span 88–93, needle
`js-claims-check`, `hit`), batch-2 rekey `d7eb02c2` (`REBIND OK sections=6
entries_added=6, ledger 814 -> 820`), sweep at `a533d7d3`
`POINTER_RECHECK: rows=12 met=12 unexpected=0` exit 0. Independent checks by
this seat: span 88–93 = legs 1–6 with `js-claims-check` at 93 (needle occurs
once); span 84–89 contains it zero times, so the stale cell's red shape would
read `miss ok`; the block's "eight lines above" resolves to the round-16 block
`49-57` (exactly 8 non-blank lines).

## 6. Receipts

Tool under test: the lane's committed `tools/pointer-recheck.py`, run as
`python3 -I -X utf8 tools/pointer-recheck.py --repo . --manifest <m>`.

**A. Standing sweep, committed manifest, lane HEAD `de43f7dc`** (reproduces
`.ufo/evidence/round-72/pointer-standings-r72.txt`):

```
POINTER_ROW province-r16-sevenleg-85-91 expect=miss measured=miss ok
POINTER_ROW sources-s303-sed-4-2 expect=hit measured=hit ok
POINTER_ROW province-r72-tenleg-88-97 expect=hit measured=hit ok
POINTER_ROW province-r72-sevenleg-cut-88-94 expect=hit measured=hit ok
POINTER_RECHECK: rows=11 met=11 unexpected=0
exit=0
```
(8 lines elided above; the full run printed 11 rows, all `ok`.)

**B. Hermetic fixture** (`git init` under `/fast/scratch/hyaku/tameshi-r72/T72W1S05/`,
base `mutate-and-run.sh` + base `PROVINCE.md` committed, then this draft's
append `cat >>`-ed and committed) — the draft's tokens bind and its spans hit:

```
POINTER_ROW province-r72-sevenleg-cut-88-94 expect=hit measured=hit ok
POINTER_ROW province-r72-tenleg-88-97 expect=hit measured=hit ok
POINTER_RECHECK: rows=2 met=2 unexpected=0
exit=0
```
Append-only check in the fixture: `20	0	PROVINCE.md`, single hunk
`@@ -143,3 +143,23 @@`.

**C. The same two rows scored with record and target revs = base** (the shape
the frozen plan calls the control):

```
POINTER_ROW province-r72-sevenleg-cut-88-94 expect=hit measured=- ERROR reason=pointer-absent-in-record
POINTER_ROW province-r72-tenleg-88-97 expect=hit measured=- ERROR reason=pointer-absent-in-record
POINTER_RECHECK: rows=2 met=0 unexpected=2
exit=1
```

**D. The plan's frozen control shape against the lane repo** — the three new
rows with record and target revs = base:

```
POINTER_RECHECK error=setup git show f20ba482c7441d4c75818e7cd8a3165fee7821a1:.ufo/evidence/round-72/corrections.md failed: fatal: path '.ufo/evidence/round-72/corrections.md' exists on disk, but not in 'f20ba482c7441d4c75818e7cd8a3165fee7821a1'
exit=2
```

**E. The same three rows with the record at the correction commit and the
target at base:**

```
POINTER_ROW sources-s303-sed-4-2 expect=hit measured=miss MISMATCH
POINTER_ROW province-r72-sevenleg-cut-88-94 expect=hit measured=hit ok
POINTER_ROW province-r72-tenleg-88-97 expect=hit measured=hit ok
POINTER_RECHECK: rows=3 met=2 unexpected=1
exit=1
```

**F. The landed control manifest** (`.ufo/evidence/round-72/control-manifest.json`,
2 rows), re-run at lane HEAD:

```
POINTER_ROW sources-s303-control-base expect=miss measured=miss ok
POINTER_ROW province-r72-control-stale-85-91 expect=miss measured=miss ok
POINTER_RECHECK: rows=2 met=2 unexpected=0
exit=0
```

**G. Stale-span shape (pointer `:85-91`, span 85–91, expect `miss`)** reads
`miss ok` at both base and tip record revs — non-discriminating, because the
target bytes are unchanged and the token exists in both records.

## 7. Not measured here (disclosed)

- The guard (`coldread-precheck-portable.py`) at any rev: receipts in
  `.ufo/evidence/round-72/live-red-r72.out`, `live-green-r72.out`,
  `live-green-hist-r72.out`, `live-revmode-r72.out` are sibling-produced; this
  seat did not re-run the guard.
- `corpus/SOURCES.md` S303 (R72-C2a) beyond the pointer row's verdict above.
- `PROVINCE.md:56`'s second cell, `tools/mutate-and-run.sh:84-89` ("the round-1
  six-leg anchor") was measured stale at base (lines 84–89 = header + narrative
  + legs 1–2; the six-leg cut is `:88-93`, corroborated verbatim by
  `.ufo/evidence/round-51/coldread/reads/T51W2Read11.md:45`). Routed in the
  seat report; **now landed** as the third correction block and its row (§5b).
