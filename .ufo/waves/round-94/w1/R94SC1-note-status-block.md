# R94SC1 — draft block 1: the case note's round-94 status block

**For:** TameshiR94 (L1), for integration into
`corpus/knowledge/mutation-case-fleet-sources-census.md`.
**Lane mode:** read-only; this seat wrote nothing under `corpus/`.

## What the L1 must decide before integrating

The committed note already carries a round-94 section, `## Certification attempt
(appended round 94) — the self-anchored gate identity` (note line 297 at `6b19eb92`).
The text below is drafted as a **replacement for that section**, not as a second
round-94 section: it keeps the section's existing three fixes (the self-anchored gate
identity, the fence-blind `coverage` scan, the delimiter row) and adds the three things
the seat item asks for and the committed section does not have —

1. an explicit statement of **what the reader certifies** (the twelve cells),
2. an explicit statement of **what it does not certify**, split into the three classes
   the item names (how the cells were obtained; fenced presentations; a table with no
   `verdict` header),
3. **S320, S321 and S322 cited with their located quotes** — the committed round-93
   section names S320/S321/S322 but gives no quoted span and no file:line, and the
   committed round-94 section cites none of the three.

If the L1 prefers append-only, the same text works as an amendment section appended
after the committed round-94 section; the wording contains no admission claim either
way. **The section as committed ends with "Admission remains the non-author closure's."**
— a deferral, not an admission claim — and the drafted text keeps that deferral and
makes no admission claim of its own.

## Hard constraints this block obeys (all four verified, see below)

The round-94 reader is a **verdict-content** reader, so the block is read by the very
instrument that certifies it. Verified against the frozen counter:

1. **No second verdict table.** The block contains no pipe-delimited table at all, so
   `verdict_tables` stays `1` (`badrows=0`).
2. **No stray verdict token.** The block contains no line with two or more pipes, so
   the reader's one-rule stray-verdict scan finds nothing outside the verdict table.
3. **No second figure.** No line of the block begins `measured:`, so the reader's
   `figure` conjunct still sees exactly one block-level figure — the note's own
   `measured: 5/12 killed` at line 83.
4. **No admission claim.** The last sentence defers admission to the non-author
   closure; it does not claim it.

Applying the block to a clone of the lane at `6b19eb92` and re-running the frozen
counter blob (`a22563b0c2b4a2b43922cec3d1ab3fa511110e035b9edfdfdc6eaebb97023010`)
gives `C1_R94_PASS=true`, exit 0, `verdict_tables=1`, `badrows=0`, `mismatched=0`, and
**all nineteen conjuncts identical to the control run** — the block moves nothing.

--- BEGIN INTEGRATION TEXT ---

## Certification attempt (appended round 94) — the verdict-content reader

Appended; the entry and the round-92/93 blocks above are unchanged. Round 93's counter was
killed by three sentences of its own record: its `coverage` scan was fence-blind, it never
read the delimiter row so it could not see a GFM-invalid table, and its seal compared the
spec to itself — one lane commit repointing the spec and regenerating `pins.json` made it
execute a foreign gate while printing `pin=true pins=true`. Round 94's successor,
`.ufo/evidence/round-94/c1/measure-v94.py`, answers each:

- **The gate identity is anchored in the counter's own self-pinned bytes.**
  `GATE_COMMIT` and `GATE_SHA256` are constants inside the file whose sha256 is itself
  pinned; when the spec-derived identity disagrees the counter refuses at setup
  (`C1_SETUP gate-identity-mismatch`, exit 2) and never materialises or runs the subject.
  The battery's `gate-foreign` state repoints `gate.path` to another real fleet blob with
  its real sha and gets exactly that refusal.
- **`coverage` skips fenced blocks and matches the note path as its own cell.** The scan
  runs through `block_lines` (S322) and requires a backtick-delimited cell whose first
  token is the path, so a fenced denial row cannot flip a committed assertion and a longer
  filename cannot satisfy it (S321's cell rule).
- **The delimiter row is read and checked.** `tables()` returns the delimiter cells; a
  table whose delimiter width differs from its header adds a `delim:` finding; a
  remainder row is padded or truncated when its one verdict token sits in the verdict
  column and refused when the verdict-bearing cells are ambiguous (S321's pad/ignore rule).

**What this reader certifies.** The twelve cells of the single verdict table above — one
cell per spec id `C01` to `C12`, in the header-named `verdict` column — agree with the
verdicts the counter itself re-derives, by re-running the pinned gate's own `selftest`
twice per mutant over the twelve single-edit mutants: `n=12 killed=5 survived=7`,
`mismatched=0`, every survivor's witness registry rebuilt and differing between pristine
and mutant, the spec still carrying its twelve ids, and the note's own figure line
matching the re-derived kill count. The committed receipt is `C1_R94_PASS=true`, exit 0,
with `verdict_tables=1`, `badrows=0`, `mismatched=0`.

**What this reader does not certify.** It certifies those twelve cells and nothing about
how they were obtained: a note that copies the committed predictions instead of the
measured receipt carries the same cells and passes, because the reader compares the cells
against its own re-execution and not against the provenance of the text. It does not
certify a fenced presentation: a fenced block is literal text (S322), so a fenced
inverted table, or a fenced figure line, is neither keyed nor counted, and the figure it
checks is the block-level one. And it does not certify a table whose header row carries
no `verdict` cell: such a table is not a verdict table at all (S321), so an id-keyed
table that asserts no verdict is never refused, and §2's survivor table and §2b's impact
table are outside the reader's scope by construction, not by accident.

The three ground rules are cited by their located quotes, each in the snapshot the reader
itself reads:

- S320 (sha256sum(1), the self-pin's digest ground) — "Print or check SHA256 (256-bit)
  checksums." (`.ufo/evidence/round-94/sources/s320.html:88`).
- S321 (GitHub Flavored Markdown Spec, §4.10 Tables) — "a single header row, a delimiter
  row separating the header from the data"
  (`.ufo/evidence/round-94/sources/s321.html:4506-4507`) and "The table is broken at the
  first empty line, or beginning of another block-level structure"
  (`.ufo/evidence/round-94/sources/s321.html:4607-4608`).
- S322 (CommonMark Spec 0.31.2, §4.5 Fenced code blocks) — "A fenced code block begins
  with a code fence, preceded by up to three spaces of indentation."
  (`.ufo/evidence/round-94/sources/s322.html:2732-2733`).

Round 94's battery registers 45 states — 6 positive, 30 hostile, 1 gate-identity setup, 3
setup, 5 removal mutants — and every hostile state names the conjunct it must falsify.
Admission remains the non-author closure's.

--- END INTEGRATION TEXT ---

## Evidence for the block's claims (each re-derived by this seat)

### The located quotes

`R94SC1-quote-locations.py` (saved beside this file) reproduces the counter's own rule —
`located_quotes()` over the lesson, `norm_text()` over the snapshot, the same
`SOURCE_ROWS` paths — at the instrument revision `7084358c`, and prints the file:line
each accepted quote occupies. Output (`R94SC1-quote-locations-r94.out`):

```
== S320  .ufo/evidence/round-94/sources/s320.html  bytes=12127  sha256=b968bc09…
  ACCEPT words=6   [(84, 88)]  Print or check SHA256 (256-bit) checksums.
== S321  .ufo/evidence/round-94/sources/s321.html  bytes=508310  sha256=b153d814…
  ACCEPT words=15  [4607, …]  The table is broken at the first empty line, or beginning of another block-level structure
  ACCEPT words=13  [(4503, 4507)]  a single header row, a delimiter row separating the header from the data
== S322  .ufo/evidence/round-94/sources/s322.html  bytes=514698  sha256=c85f56cc…
  ACCEPT words=17  [2732, 2733, …]  A fenced code block begins with a code fence, preceded by up to three spaces of indentation.
ACCEPTED 4
```

The script's `locate()` reports the smallest contiguous line span whose normalised text
contains the quote; the block cites the **narrowest** such span, re-derived by a second
probe that checks the quote is contained in exactly the cited lines:

| id | quote | cited lines | quote inside the cited span |
|---|---|---|---|
| S320 | "Print or check SHA256 (256-bit) checksums." | `s320.html:88` | yes |
| S321 | "a single header row, a delimiter row separating the header from the data" | `s321.html:4506-4507` | yes |
| S321 | "The table is broken at the first empty line, or beginning of another block-level structure" | `s321.html:4607-4608` | yes |
| S322 | "A fenced code block begins with a code fence, preceded by up to three spaces of indentation." | `s322.html:2732-2733` | yes |

All four are `ACCEPT` under the counter's own rule, so the block's citations are the
sentences the counter's `source` conjunct is satisfied by, not prose chosen after the
fact. The round-93 snapshots are byte-identical to the round-94 ones for all three
(`sha256 b968bc09…`, `b153d814…`, `c85f56cc…` in both), so the same quotes locate at
the same lines in either round — verified by running the probe in `r93` mode
(`R94SC1-quote-locations-r93.out`, `ACCEPTED 4`).

### The certificate is unmoved by the block

`R94SC1-note-block-fixture.py` (saved beside this file) clones the lane `--shared` at
`6b19eb92`, asserts `git rev-parse --show-toplevel` equals the clone before any commit,
replaces the committed round-94 section with the drafted text, commits under the fixture
identity `ctl <ctl@fixture.invalid>`, and runs the **frozen counter blob** — extracted
with `git cat-file` from `6b19eb92`, never the working tree — against the fixture commit.
It compares the two runs conjunct by conjunct and fails if any moved. Output
(`R94SC1-note-block-fixture.out`):

```
== CONTROL (note unmodified at 6b19eb92) ==
  C1_SUMMARY rev=HEAD n=12 killed=5 survived=7 inconclusive=0 unstable=0 invalid=0 trivial=0 witnessed=7/7 note=present mismatched=0 badrows=0 verdict_tables=1
  C1_CONJUNCTS selfpin=true pins=true spec=true pin=true green=true canary=true valid0=true trivial0=true inconclusive0=true unstable0=true note=true verdict_tables=true ids=true mismatched0=true figure=true witnessed=true source=true coverage=true n_min=true
  C1_R94_PASS=true
  exit=0
FIXTURE_ADD rc=0 stdout= stderr=
FIXTURE_STATUS M  corpus/knowledge/mutation-case-fleet-sources-census.md
FIXTURE_DIFF_CACHED .../mutation-case-fleet-sources-census.md          | 46 ++++++++++++++++++----
 1 file changed, 38 insertions(+), 8 deletions(-)
FIXTURE_COMMIT 7d869c4e (parent 6b19eb92)
FIXTURE_BLOCK_PRESENT_IN_COMMIT true
== WITH DRAFTED BLOCK (fixture commit 7d869c4e) ==
  C1_SUMMARY rev=7d869c4eb5482bf27f7633239644c974ecc6d94c n=12 killed=5 survived=7 inconclusive=0 unstable=0 invalid=0 trivial=0 witnessed=7/7 note=present mismatched=0 badrows=0 verdict_tables=1
  C1_CONJUNCTS selfpin=true pins=true spec=true pin=true green=true canary=true valid0=true trivial0=true inconclusive0=true unstable0=true note=true verdict_tables=true ids=true mismatched0=true figure=true witnessed=true source=true coverage=true n_min=true
  C1_R94_PASS=true
  exit=0
CONJUNCTS_MOVED none
BLOCK_PRESERVES_CERTIFICATE true
```

The fixture **asserts** that the edit was committed and that the block is present in the
committed note before it runs the counter (`FIXTURE_COMMIT`, `FIXTURE_BLOCK_PRESENT_IN_COMMIT`),
so a no-op commit cannot pass for a green result. (An earlier run of this fixture did
exactly that — the write step was missing and the commit was a no-op, giving a vacuous
"pass"; the assertion was added in response and the result above is from the fixed
script.)

## Two facts the L1 should know before integrating this block

**1. The block's `coverage` claim is about the reader, not about this note.** The reader
grades the LAST `corpus/README.md` row naming the note. At `6b19eb92` that row is line
782 (`certificate revision-bound to the round-94 instrument revision … not an
admission`) and it carries no denial token, so `coverage=true` at HEAD. If the L1
integrates a note change **and** edits the README, the README's last naming row is what
decides `coverage`; the note's own text never enters that conjunct. The block makes no
README claim, so it is safe either way — but a denial token in a later README row would
flip `coverage` regardless of this block.

**2. The round-93 section this block's `Appended; … unchanged` sentence refers to is
the *committed* round-93 section, and it is correct as committed.** The committed
round-93 section at lines 277–295 states the reader's rule and its two limits; it cites
S321/S322 without a quoted span and does not mention S320. This block does not modify
it. If the L1 wants S320's located quote to appear under the round-93 heading as well,
that is a second, separate edit to a committed section and is not part of this draft.

VERDICT: drafted
TOOLS: none
