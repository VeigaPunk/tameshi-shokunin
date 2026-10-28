# T55W1ExecCensusAfter — the census guard on the round-55 candidate append

Round 55, wave 1, seat `T55W1ExecCensusAfter`. Base `0a2010acd1e92e4e332774050825e21bcfc7e079`;
lane HEAD `631cd6455e58dce969310b4c0466c3383d9f5108` (the frozen counter set); lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Access **2026-10-28**.

**Item.** Build the append block the L1 will land, in scratch: copy the lane's `corpus/` to
`$S/corpus`, add the proposed rows to the Registry table, run
`scripts/sources-census.sh validate --file $S/corpus/SOURCES.md`, then prove the guard catches a
defect — an indented duplicate id (`  | S280 |`) must produce E03/E04 or equivalent, and an
11-column row with a literal `|` must fail parsing. Report exit codes and findings; never touch the
real registry.

**Verdict.** Done, with two results the L1 needs.

1. **The candidate append is conformant.** 140 rows, `NF=13` on every row, **exit 0**, 0 E, 16 W,
   stderr empty — identical to the round's base-rev warning set (16/16, empty diff). The append adds
   no finding.
2. **The guard is load-bearing exactly where the item asked, and has three measured holes.** The
   indented duplicate is reported twice (E03 + E04) at 0–3-space indent; the literal pipe fails as
   `E01 … fields=12`. But a 4-space or tab indent makes a row *invisible* (exit 0, not counted), a
   literal pipe **compensated by one missing cell** parses silently with reassigned columns (exit 0,
   141 rows), and a duplicate URL under a *reworded* scope is only a warning (exit 0).

Everything below is a command and its output; nothing is asserted that was not run.

---

## 1. What the append block actually is (read from the wave's own files)

`T55W1ScribeSources.json` is present and its `rows_to_append` is **empty** — both drafted rows were
withdrawn (S280 already existed; the `sysexits(3)` draft duplicated S090):

```
$ jq -r '.rows_to_append | length' .ufo/waves/round-55/w1/T55W1ScribeSources.json
0
```

So "the proposed rows" is, in this tree, **one row**: **S280**, already the last Registry row
(`corpus/SOURCES.md:155`, immediately before `## Paths` at line 158), with the round's footer note at
line 517. Three variants of that row exist in the wave's deliverables, all at 11 cells / `NF=13`:

| # | variant | source | row text |
|---|---|---|---|
| 1 | as landed in the lane's working tree (`kind=spec`, teaches states the casing and no-period rules) | `corpus/SOURCES.md:155` | `S280-variant-1-lane.txt` |
| 2 | the scribe's in-place correction | `T55W1ScribeSources.json` `.corrections[0].proposed_row` | `S280-variant-2-scribe.txt` |
| 3 | the reviewer's rewrite (scope qualified as GNU's own convention, anchor with revision stamp) | `T55W1RevSources.json` `.verdicts[0].row_as_reviewer_would_write` | `S280-variant-3-reviewer.txt` |

Variant 1 is **not** the scribe's pre-patch bytes (`c78c0ab…`) nor its post-patch bytes
(`a3267ab…`): the registry sha256 is now `57ece0e5…`, mtime `2026-10-28 14:00:16 -0300`, and the
appended row's `teaches` no longer carries the unsourced "verdict vocabulary" clause the scribe
flagged. Freshness note for the L1: the row was rewritten after the scribe's audit, so *which*
variant lands is a substance decision (see F5 — the census cannot tell them apart).

Build, per the item: `rsync -a --exclude .git <lane>/corpus/ $S/corpus/`, plus
`$S/tools/tally-audit.py` and `tally-audit-v3.py` because two mined rows point their `used-by` at
`tools/` and `--file` resolves `used-by` against the *parent of `corpus/`* (F4).

## 2. Candidate validation (the deliverable measurement)

`$S = /fast/scratch/hyaku/tameshi-r55/T55W1ExecCensusAfter`. Command, in every row of the table:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-28 \
    --file <root>/corpus/SOURCES.md
```

| candidate | root | exit | rows | E | W | stderr | receipt |
|---|---|---|---|---|---|---|---|
| cand0 — lane as-is (variant 1) | `$S` | **0** | **140** | 0 | 16 | 0 B | `cand0-lane-as-is.tsv/.err` |
| cand1 — scribe's corrected row (variant 2) | `$S/fx/cand1-corrected-s280` | **0** | **140** | 0 | 16 | 0 B | `cand1-corrected-s280.tsv/.err` |
| cand2 — reviewer's rewrite (variant 3) | `$S/fx/cand2-reviewer-s280` | **0** | **140** | 0 | 16 | 0 B | `cand2-reviewer-s280.tsv/.err` |
| cand-lane — same corpus addressed as a lane dir (the round-end code path) | `$S/fx/cand-lane/tameshi-shokunin` | **0** | **140** | 0 | 16 | 0 B | `cand-lane-validate.tsv`, `cand-lane-census.tsv` |

The item's literal command (default `--today`) also exits 0:
`cand0-default-today.tsv` → `file ok /fast/scratch/…/T55W1ExecCensusAfter/corpus/SOURCES.md`, rc 0.

`census` on the candidate, both modes agreeing:

```
tameshi-shokunin	rows	140
tameshi-shokunin	tier.A	125	tier.B	12	tier.C	3
tameshi-shokunin	status.mined	113	status.queued	21	status.rejected	6
```

Field structure, every Registry row, all three variants:

```
== T55W1ExecCensusAfter/corpus/SOURCES.md               NF=13 rows=140
== …/fx/cand1-corrected-s280/corpus/SOURCES.md          NF=13 rows=140
== …/fx/cand2-reviewer-s280/corpus/SOURCES.md           NF=13 rows=140   (cand2 row: NF=13)
```

### 2a. The append adds no finding

Candidate warning set against the round's own base-rev receipt
(`T55W1ExecCensus-receipts/base-validate.tsv`, 17 lines):

```
$ diff -u <base 16 W lines, label stripped> <cand0 16 W lines, label stripped>
diff_rc=0   diff lines: 0   base W count: 16   cand0 W count: 16
```

and cand1 vs cand0 (`append-warning-delta.stdout`): **0 bytes** — replacing the row with the
proposed variant changes no finding. So the round-end conformance claim "exit 0, 140 rows" is
reproducible from a scratch copy of the tree, not only from the live lane.

## 3. Guard proofs the item asked for

| fixture | what was inserted (last Registry row) | exit | rows | findings (verbatim, pre-existing warnings elided) | receipt |
|---|---|---|---|---|---|
| **fx-dup-2sp** (required) | `␠␠\| S280 \| …` — exact S280 row, 2-space indent | **1** | 141 | `E03 S280 duplicate id` · `E04 S280 duplicate url www.gnu.org/prep/standards/html_node/Errors.html within scope the line shape of a noninteractive program's error message` | `fx-dup-2sp.tsv` |
| fx-dup-0sp / 1sp / 3sp | same row at 0/1/3-space indent | **1** | 141 | identical E03 + E04 pair | `fx-dup-{0,1,3}sp.tsv` |
| **fx-pipe-11col** (required) | 11-column row with a literal `\|` in `teaches` | **1** | 141 | `E01 S281 fields=12` | `fx-pipe-11col.tsv` |
| fx-dup-diff-url | S280's id on a different URL/scope | **1** | 141 | `E03 S280 duplicate id` (id guard, URL-independent) | `fx-dup-diff-url.tsv` |
| fx-supersedes | new id, **same URL + same scope**, teaches opens `supersedes S280` | **0** | 141 | none — the contract's correction form is admissible | `fx-supersedes.tsv` |
| fx-supersedes-absent | same URL + same scope, new id, **no** supersedes token | **1** | 141 | `E04 S281 duplicate url … within scope …` | `fx-supersedes-absent.tsv` |
| fx-eof-outside | row appended at EOF, after `## Id allocation` | **1** | 141 | `E12 S281 row outside Registry section` | `fx-eof-outside.tsv` |
| fx-dup-4sp | duplicate at 4-space indent | **0** | **140** | none — F1 | `fx-dup-4sp.tsv` |
| fx-dup-tab | duplicate at tab indent | **0** | **140** | none — F1 | `fx-dup-tab.tsv` |
| fx-pipe-4sp | the pipe row at 4-space indent | **0** | **140** | none — F1 | `fx-pipe-4sp.tsv` |
| fx-pipe-absorbed | literal pipe **plus one omitted cell** | **0** | **141** | none — F2 | `fx-pipe-absorbed.tsv` |
| fx-pipe-shift | literal pipe, omission lands on an enum | **1** | 141 | `E07 S281 status=pipe` · `E08 S281 opened=mined` — F2 | `fx-pipe-shift.tsv` |
| fx-dup-reworded-scope | same URL under a reworded scope, no supersedes | **0** | 141 | `W04 … across scopes` only — F3 | `fx-dup-reworded-scope.tsv` |

Every fixture: stderr 0 bytes; the 16 base warnings are unchanged in all of them; the only new
non-E line anywhere is the pre-existing `W01 S101` and the ones named above. Machine-readable:
`fixtures-summary.tsv`; fixture construction: `driver.sh` (copied into receipts).

**The two required defects are caught.** `  | S280 |` gives E03 *and* E04 and exit 1;
an 11-column row carrying a literal `|` gives `E01 … fields=12` and exit 1.

## 4. Findings from the sweep (each with the command that produced it)

**F1 — the indentation window is 0–3 spaces; a 4-space or tab indent makes the row invisible.**
`validate` parses `^ {0,3}\|` only; 4+ spaces are "indented code", a tab is not matched at all:

```
fx-dup-4sp   rc=0 rows=140 E=0        fx-dup-tab  rc=0 rows=140 E=0
```

This is the highest-risk append hazard for the L1: a row pasted with a tab (common from a browser or
another Markdown table) is **not counted, not validated, exit 0** — the append silently does not
exist. The 2-space form the item names is safely inside the window; 3 spaces is the last safe width.

**F2 — E01 is arithmetic, not structural: a literal pipe that "pays for itself" parses silently.**
`E01` prints `fields=NF-2`, so any split count that lands on 11 groups passes. A row written with
10 cells whose `teaches` contains a literal pipe has 11 groups:

```
row:   | S281 | Pipe absorbed — https://example.example/absorb | docs | B | … | §1 | teaches text | queued | 2026-10-28 | 30d | — |
validate: rc=0 rows=141 E=0
census:   file	rows	141	mined 113	queued 22	rejected 6     (queued was 21 before the insert)
overdue:  file	cadence	S281 recheck=30d opened=2026-10-28
```

The `queued` count moving 21 → 22 proves the parser manufactured `status` from the pipe's tail: the
row was written without a status column and validated clean as a different row. The companion
fixture shows the detectable case — when the shifted values are *not* enum-valid, the misparse
surfaces as unrelated noise (`E07 status=pipe`, `E08 opened=mined`), never as "malformed row".
**Consequence for the L1: never put a `|` inside a cell; the census will not reliably tell you.**

**F3 — E04 keys on exact scope-string equality, so a reworded-scope duplicate is only a warning.**

```
fx-dup-reworded-scope: same URL as S280, scope reworded, no supersedes token
  -> rc=0, W04 S281 duplicate url www.gnu.org/prep/standards/html_node/Errors.html across scopes
```
W-codes never move the exit code. A second row for a source already held passes if the author
rewords the scope; only the `supersedes S###` token path and exact-scope E04 are enforced. Practical
reading: the two "in place vs new superseding row" forms of the S280 correction are *both*
admissible to the census, and only exact-scope reuse is refused.

**F4 — E11's root under `--file` is `dirname(file)/..`**, so a bare `corpus/` copy must also carry
the `tools/` files that mined rows name in `used-by` (two rows). Measured during setup before the
`tools/` copy existed:

```
MISSING tools/tally-audit.py
MISSING tools/tally-audit-v3.py        (twice, two rows)
```
With the two files present the candidate has **0 E11** — the round-55 row's `used-by`
(`corpus/knowledge/scratch-root-contract.md, corpus/lessons/round-55.md`) resolves.

**F5 — the census cannot arbitrate the S280 correction.** All three variants are `NF=13`, exit 0,
0 E, 16 W. Whatever the L1 lands must be chosen on C1/substance grounds (the reviewer requires the
scope be qualified as GNU's own convention; the scribe's patch widens scope and anchor), not because
one of them validates and another does not.

**F6 — a duplicate id is caught even when the URL differs** (`fx-dup-diff-url` → `E03` alone), so
re-using a number for a different source is refused; that is the guard the append depends on.

**F7 — an EOF append is refused as `E12`** when the registry ends with `## Id allocation`
(`fx-eof-outside`). The round-55 row was inserted correctly (line 155, before `## Paths`), and the
file ends with a newline (`od -c` → `… e ) . \n`), so the earlier no-trailing-newline hazard is gone.

## 5. Freshness and the round's conformance claim

| captured (UTC) | registry sha256 | rows | validate rc | E | W |
|---|---|---|---|---|---|
| 17:16:56Z | `57ece0e5…` | 140 | 0 | 0 | 16 |
| 17:19:30Z (`conformance-end.tsv`) | `57ece0e5…` | 140 | 0 | 0 | 16 |
| 17:20:25Z (`freshness-final.txt`) | `57ece0e5…` | 140 | 0 | 0 | 16 |

The registry did not move during this seat (same sha256 at start and end), and the lane's own
conformance command is exit 0:

```
$ cd /home/vgpnk/Projects/shokunin
$ ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
… 16 W lines …
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
rc=0
```

**HEAD moved under this seat** (integrator commits — this seat ran no git mutation):
`631cd64` (observed at 17:14Z, the round's frozen counter set) → `e2979f2` 17:16:25Z → `9cf0146`
17:16:39Z → **`133b2ce` 17:21:00Z** ("freeze amendment 8 … Freeze pointer moves to this commit").
At `133b2ce` the registry is **committed**, and committed bytes equal the worktree bytes
(`git show HEAD:corpus/SOURCES.md` → sha256 `57ece0e5…`, 140 rows), so the candidate validated here
is the committed registry, not merely a working-tree state. Two consequences to report, not fix:
(a) the freeze pointer the seat spec named (`631cd64…`) has been superseded by the L1's own
amendment commit; (b) that commit swept this seat's `registry-hashes-start.txt` (written 17:19:30Z)
into git, so it now shows as modified after this seat appended two lines to it.

Row-count reconciliation: the seat spec's "139 rows now (S001–S279)" is the **round-start** state
(the prior census seat measured 139 at base with the same command); S280 is this round's one append,
so 139 → **140**. `corpus/lessons/round-55.md:16` now says "exit 0, 140 rows", which matches the
tree — the earlier "141 rows" claim the scribe reported has been corrected. No discrepancy remains.

## 6. Report-only notes for the L1

1. **Land the row in place at line 155** (last Registry row, before `## Paths`) — not at EOF, which
   is E12, and not with a tab/4-space indent, which is invisible (F1).
2. **Pick variant 1/2/3 on substance.** All three are census-conformant (F5). If you land variant 1
   unchanged, note it is neither the scribe's pre-patch bytes nor its post-patch bytes — it was
   rewritten at 17:00Z after the scribe's audit (its `teaches` no longer carries the unsourced
   "verdict vocabulary" clause, but its `scope` is still unqualified).
3. If a later round adds a second row for the same held source, the `supersedes S###` token is the
   only path that avoids E04 — and a reworded scope avoids even that (F3, warn-only).
4. Nothing in the frozen counter set was edited by this seat. The two integrity observations the
   prior census seat reported are **resolved** as of 2026-10-28T17:23:37Z: the freeze manifest now verifies 7/7
   (`jq -r '.files|to_entries[]|"\(.value)  \(.key)"' freeze.json | sha256sum -c -` → all `OK`) and
   `before/c2.stdout` is populated (1672 B), so the amendment commits re-froze the set on the
   amended bytes. Recorded here only to close the earlier finding out.

## 7. Scope, tooling, reproduction

- Wrote only: this report, `T55W1ExecCensusAfter.json`, and
  `.ufo/waves/round-55/w1/T55W1ExecCensusAfter-receipts/` (62 files). No lane production file
  (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`) was created, modified or deleted;
  `corpus/SOURCES.md` has the same sha256 (`57ece0e5…`) before and after this seat.
- Scratch: `HYAKU_SCRATCH=/fast/scratch/hyaku`,
  `S=/fast/scratch/hyaku/tameshi-r55/T55W1ExecCensusAfter`; all fixture roots live under `$S/fx/`;
  no `git` mutation was run anywhere (no clone was needed — the append is a working-tree row and the
  copy is `rsync`), no `jj`, nothing under `/tmp`.
- Tooling: **no installs, no upgrades** — `bash`, `gawk`, `rsync`, `coreutils`, `python3` and the
  pre-existing `/home/vgpnk/.local/bin/jq` sufficed. pacman is paused host-wide and was not touched.
- Reproduction: `receipts/driver.sh` regenerates every fixture and every `.tsv` from the lane's
  `corpus/`; the three candidate row strings are in `receipts/candidate-append-block.md`.

### Receipts (`.ufo/waves/round-55/w1/T55W1ExecCensusAfter-receipts/`)

`fixtures-summary.tsv` (all fixtures: rc/rows/E/W), `cand{0,1,2}-*.tsv|.err`,
`cand-lane-validate.tsv`, `cand-lane-census.tsv`, `cand0-default-today.tsv`,
`append-warning-delta.stdout` (empty), `warnings-vs-base.stdout` (empty),
`candidate-field-counts.stdout`, `candidate-append-block.md`, `driver.sh`,
`fx-*.tsv|.err` (15 fixtures), `S280-variant-{1,2,3}-{lane,scribe,reviewer}.txt`,
`fx-pipe-absorbed-{parsed-columns,census}.stdout`,
`fx-pipe-shift-parsed-columns.stdout`, `registry-hashes-start.txt`, `freshness-final.txt`,
`conformance-{start,end,final}.tsv`.
