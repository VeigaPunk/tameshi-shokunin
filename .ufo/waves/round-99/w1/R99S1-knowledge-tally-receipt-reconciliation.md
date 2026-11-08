# Tally-receipt reconciliation — a recorded selftest tally is re-read from the receipt it cites

> Draft by seat R99S1 (scribe) for the L1's integration, round 99 wave w1. Proposed full
> text of `corpus/knowledge/tally-receipt-reconciliation.md`. Every figure below is a line a
> named receipt prints; the source quotes were located in the committed snapshots by the
> lane's own tag-strip convention, and the two facts the renderer cannot show are cited by
> raw snapshot line and named as such (§6).
>
> **Status at hand-off:** the L1 landed the records revision `808a4377` and the landing
> `7cd85a42` while this draft was being written. `corpus/knowledge/tally-receipt-reconciliation.md`
> and `corpus/QUALITY.md` criterion 178 now exist, built from this seat's draft. The two
> figures that moved under the landing are corrected below: the instrument at R is the
> **amended** one (`a1c50bb4…`, amendments A2-A4, A9, A10) whose `--selftest` prints
> `25/25`, and the receipt paths at R are `.ufo/evidence/round-99/records/`. The
> twelve-record numbers are unchanged (re-derived at R below). The S325 anchor correction
> in §6 and the pairing-limit correction in §4 stand and are **not** reflected in the landed
> corpus entry — see `R99S1.md` §7.

source: S324 — Nuijten, Hartgerink, van Assen, Epskamp, Wicherts, "The prevalence of
statistical reporting errors in psychology (1985-13)", *Behavior Research Methods* 48(4),
2016 (Europe PMC record `PMC5101263`, DOI `10.3758/s13428-015-0664-2`); the Europe PMC REST
record was fetched 2026-11-08 (HTTP date `Sun, 08 Nov 2026 22:55:22 GMT`), snapshot
`.ufo/evidence/round-99/sources/s324.json` 6409 B sha256
`346dcf46d3e6ccfe20d269b5b74ca4d21df98c8731c57858808d4c856d0f0349`, headers
`.ufo/evidence/round-99/sources/s324.headers`;
S325 — statcheck // web, FAQ (`http://statcheck.io/`, Nuijten, Epskamp et al.), fetched
2026-11-08 (HTTP date `Sun, 08 Nov 2026 22:55:32 GMT`), snapshot
`.ufo/evidence/round-99/sources/s325.html` 27778 B sha256
`477e0088c987eabd845a81bd38e716959296c2a691b0ae57d9df45e66cb3e9a7`, headers
`.ufo/evidence/round-99/sources/s325.headers`
verified-at: 2026-11-08 — every figure in §3–§5 is a line a named receipt prints at the
named revision; the two source quotes are located in the committed snapshots by the lane
renderer `.ufo/waves/round-93/w1/R93S1-tagstrip.py`. The instrument figures below are the
**frozen** ones at the instruments revision `46651051` (`sha256 60d59bea…bf40c`,
`.ufo/evidence/round-99/pre-freeze/`); at the records revision R the instrument is the
amended one (`sha256 a1c50bb4…b09b482`) and its selftest prints `25/25`
(`.ufo/evidence/round-99/records/c1-selftest.out`) — the twelve-record numbers are the same
at both revisions (re-derived at R: `records=12 tallies=28 pairs=9 matched=2 mismatched=1
unbound=6 uncited=19`, rc 1)
recheck: 365d — reopen S324/S325 and re-run the reconciler over the newest six rounds; a
change to the tool's grammar (the tally forms, the citation forms, the pairing rule)
changes §3 and §4
ground: calibration — the lane's own records (the round-93..98 lessons and plans); not a
frontier row, and no coverage-map ground is claimed by this entry

## 1. The question

A round record states a figure it did not compute in place: "the selftest prints
`DISPOSITION_SELFTEST: 8/8 pass`", followed by the path of the receipt that holds the run.
The figure is the lane's self-assessment; the receipt is the observed state. Nothing forces
the two to agree. The figure is typed when the sentence is written, and the instrument keeps
moving: a case is added, a battery is repaired before the records run, and the receipt
prints `9/9` while the sentence still says `8/8`.

Two non-author closures found this by reading. Round 94's frozen C2 tally `8/8` stood
beside a receipt printing `9/9` (`corpus/lessons/round-94.md:66`; the round-94 closure's
finding at `corpus/lessons/round-94-verifier-spotcheck.md:100`), and the claim landed
`unprovable` on that alone — the reconciler prints that pair verbatim
(`.ufo/evidence/round-99/pre-freeze/c1-r94-only.out`: `claimed=8/8 … observed=9/9`). Round
98's report said the C1 selftest was `18/18` "at the freeze", citing a freeze receipt that
prints `12/12` (round-98 spot-check D2); the reconciler reproduces that shape as a selftest
arm (`.ufo/evidence/round-99/pre-freeze/c1-selftest.out`, `selftest-word-r98-d2-shape`).
The lane held QUALITY 169 ("a frozen tally cites its receipt path") but no instrument read
the citation.

## 2. What the outside practice says

statcheck is the reference case of reading a reported figure back against its inputs: it
extracts each reported test result, recomputes the p-value from the reported statistic and
degrees of freedom, and flags disagreement. S324 measured how often the two drift — "half
of all published psychology papers that use NHST contained at least one p-value that was
inconsistent with its test statistic and degrees of freedom" (25 words; located in the
`abstractText` field of the Europe PMC record at offset 344). The authors were not careless
people; the figure and its source simply live in different places and are edited at
different times.

S325 states the other half of the lesson, the grammar boundary. statcheck is a "spellchecker"
for statistics: it "checks whether your p-values match their accompanying test statistic and
degrees of freedom" (21 words) — but only for results reported completely and in APA style,
and "Statcheck usually can't find statistics in tables" (7 words). A result outside the
grammar is **unchecked, not consistent**. A reconciler's silence is evidence only inside its
declared grammar.

## 3. The lane's rule, as an instrument

`tools/tally-reconcile.py` (round 99, sha256
`60d59bead569157fb888dbb68301e290522e5837a482e84f36f858d2566bf40c` at `46651051`) reads
records and receipts as blobs at one revision and, for every recorded tally on a line that
cites a receipt, compares the claim with the receipt:

| item | rule |
|---|---|
| tally forms | `TOKEN: N/M pass` (TOKEN upper-case, ≥3 chars); the word `selftest` followed within 12 non-digit characters by `N/M` |
| citation | a path on the same line ending `.out`/`.txt`/`.log`/`.json`, not in a URL and not the record itself |
| resolution | the tree path, else the record's own round dirs (`.ufo/evidence/round-NN`, `.ufo/waves/round-NN`); none → `unbound unresolved`, several → `unbound ambiguous-path` |
| grading | `matched` only when every receipt line carrying the token shows the claimed N/M; any other value → `mismatched`; token absent → `unbound` |
| no citation | `uncited`, counted and never graded |

Over the twelve round-93..98 lessons and plans it prints
`TALLY_RECONCILE records=12 tallies=28 pairs=9 matched=2 mismatched=1 unbound=6 uncited=19`
and exits 1 (`.ufo/evidence/round-99/pre-freeze/c1-population.out`): the single mismatch is
the round-94 line the closure found; two pairs confirm; six cited receipts could not be
bound by the grammar; nineteen tallies cite nothing on their line. The round-94 lesson alone
prints `TALLY_RECONCILE records=1 tallies=1 pairs=1 matched=0 mismatched=1 unbound=0 uncited=0`
and exits 1 (`.ufo/evidence/round-99/pre-freeze/c1-r94-only.out`), naming the pair:
`TALLY mismatched corpus/lessons/round-94.md:66 token DISPOSITION_SELFTEST claimed=8/8
receipt=.ufo/evidence/round-94/pre-freeze/c2-selftest.out observed=9/9 detail=differs`.
The instrument's own battery prints `TALLY_RECONCILE_SELFTEST: 17/17 pass` and exits 0
(`.ufo/evidence/round-99/pre-freeze/c1-selftest.out`).

## 4. Why same-line pairing, and why the grammar limits, are the rule

**Same-line pairing.** The reconciler pairs a tally with a receipt only when the citation
sits on the tally's own line, and with *each* citation on that line. That is what makes the
round-98 shape detectable: the report sentence "Selftest `18/18`
(`pre-freeze/c1-audit-selftest.out` at the freeze; `records/c1-audit-selftest.out` at R)"
names two receipts for one figure, and the two receipts disagree — the freeze receipt prints
`CONTROL_ASSERT_SELFTEST: 12/12 pass` while the records receipt prints
`CONTROL_ASSERT_SELFTEST: 18/18 pass`. The instrument's selftest arm
`selftest-word-r98-d2-shape` reproduces that shape: one line, two citations, one pair
`matched` and one `mismatched` (`.ufo/evidence/round-99/pre-freeze/c1-selftest.out`,
`records=1 tallies=1 pairs=2 matched=1 mismatched=1`). Pairing per line is what turns "the
figure disagrees with its receipt" into a counted mismatch rather than a reading task.

**Which lines exemplify the multi-citation shape.** The *rule* is exercised by the tool's
own selftest arm, above. In the twelve committed records the shape has **no instance**: at
both the freeze and R, a sweep of all twelve records finds zero tally lines carrying more
than one citation (`multi_citation_tally_lines=0`). The two round-98 lesson lines the lane's
own frozen wording names (`corpus/lessons/round-98.md:124` and `:127`) each carry exactly
one citation — `records/c2-refusals-red.out` and `records/registry-green-r97-records.out`
— and they grade `unbound no-selftest-line` for a different reason: their single cited
receipt contains no `*_SELFTEST` line. The enforceable property is therefore two clauses:
*a line citing several receipts pairs the tally with each* (the tool's
`selftest-word-r98-d2-shape` arm), and *a line whose single cited receipt carries no
`*_SELFTEST` line grades `unbound no-selftest-line`* (the round-98 lesson lines). The
frozen `plans/round-99.plan.md` wording, which calls those two lines "such pairs" (i.e.
instances of the several-receipts case), over-attributes; `.ufo/waves/round-99/w1/claims.json`
worded the same limit without that clause and is correct.

**The grammar limits are the rule, not a defect.** A reconciler that recognises only
`TOKEN: N/M pass` and the `selftest` word-form leaves `6/6 killed`, `9 of 9` and bare table
cells unrecognised; a citation that resolves only as a tree path or a basename at the top of
the record's own round dirs leaves a sub-directory receipt unbound. The instrument counts
these rather than hiding them: six of the nine pairs are `unbound`, and the exit code is 1
whenever any pair is unbound or mismatched, so an unbound pair is visible rather than
silently green. This is statcheck's lesson applied to the lane: **silence outside the
grammar is not agreement.** The counts measure the twelve records as committed; they are a
calibration measurement of the lane's records, not a claim that every unbound pair is a
record error.

## 5. What the numbers say about the lane, and what they do not

- **Only 2 of 28 recorded tallies are mechanically confirmed** (the `matched=2` of
  `.ufo/evidence/round-99/pre-freeze/c1-population.out`). Most tallies are stated in prose or
  code blocks with the receipt named elsewhere in the paragraph, or not at all. That is a
  calibration finding about how the lane writes, not a claim that 26 tallies are wrong.
- **Unbound is not wrong.** Four of the six unbound pairs cite a receipt by basename under a
  sub-directory the grammar does not search (`detail=unresolved`); two pair a tally with a
  single cited receipt that carries no `*_SELFTEST` line at all (`detail=no-selftest-line`).
  Whether a given unbound pair has a confirming receipt elsewhere under the same round's
  dirs is a separate question the round's wave answered
  (`.ufo/waves/round-99/w1/R99L1.md`).
- **The practice that makes the counter useful:** state a tally on the same line as the
  receipt that prints it, by a path the tree resolves. A record written that way is
  checkable by a non-author with one command; a record written otherwise is only readable.

## 6. Boundaries and the citations' own limits

- The reconciler reads records and receipts as blobs at the revision it is given, through
  `git cat-file`, never the worktree; its selftest arm `worktree-edit-ignored` proves a
  worktree edit does not move the verdict
  (`.ufo/evidence/round-99/pre-freeze/c1-selftest.out`).
- The tool reads **one repository**. The round-98 report sentence that carries D2 lives in
  the fleet repo (`.ufo/reports/round-98/tameshi.md`), which the lane repository does not
  carry at `ab598d03` (`git cat-file -e ab598d03:.ufo/reports/round-98/tameshi.md` exits
  128); that is why the D2 shape is reproduced only as a selftest arm.
- Pairing is per line; two tally spellings only; a bare basename resolves only at the top of
  the record's round dirs; an append-only erratum elsewhere does not clear a record line.
- **[Inference]** The lane's rule is the same rule as statcheck's, one layer down: a reported
  figure is checked against the artifact it was computed from, and a figure the checker
  cannot reach is unchecked rather than consistent. S324 and S325 establish the outside
  practice and its prevalence; the lane's counts are the local measurement. The sources do
  not make any claim about tameshi's records.
- **Two source quotes are located by raw snapshot line, not by the lane renderer.** The lane
  renderer (`.ufo/waves/round-93/w1/R93S1-tagstrip.py`) removes tags with `<[^>]+>`, which
  also swallows a bare `<` that begins no tag; the S325 FAQ's literal `p < .05` therefore
  deletes the sentence that follows it. The "recalculates the p-value using the reported
  test statistic and degrees of freedom" sentence is at **raw snapshot lines 142–145**
  (the "flag the result as an error" wording) and **raw lines 188–190** (the "flag the
  result as an inconsistency" wording); under the lane renderer neither sentence is present
  in the stripped text at all. The two quotes this entry leans on — the "spellchecker"
  sentence (renderer lines 135–137) and the tables sentence (renderer line 163) — do survive
  the renderer, and the raw snapshot carries them at lines 136–138 and 166.

## 7. Evidence

- `.ufo/evidence/round-99/pre-freeze/c1-population.out` — the twelve records:
  `records=12 tallies=28 pairs=9 matched=2 mismatched=1 unbound=6 uncited=19`, exit 1,
  with the round-94 mismatch line named.
- `.ufo/evidence/round-99/pre-freeze/c1-r94-only.out` — the round-94 lesson alone:
  `records=1 tallies=1 pairs=1 matched=0 mismatched=1 unbound=0 uncited=0`, exit 1.
- `.ufo/evidence/round-99/pre-freeze/c1-selftest.out` — `TALLY_RECONCILE_SELFTEST: 17/17
  pass`, exit 0; arms `token-mismatched-r94-shape`, `selftest-word-r98-d2-shape`,
  `two-tallies-one-line`, `worktree-edit-ignored`.
- `.ufo/evidence/round-99/pre-freeze/c1-before-token.out` — at the round base no committed
  tool prints a `TALLY_RECONCILE` line (`git grep -c TALLY_RECONCILE ff93fa16 -- .`, exit 1).
- `.ufo/evidence/round-94/pre-freeze/c2-selftest.out:10` — `DISPOSITION_SELFTEST: 9/9 pass`,
  the receipt the round-94 record's `8/8` claim sits beside.
- `.ufo/evidence/round-98/pre-freeze/c1-audit-selftest.out:13` —
  `CONTROL_ASSERT_SELFTEST: 12/12 pass` (the freeze receipt the round-98 report's "18/18 at
  the freeze" cites); `.ufo/evidence/round-98/records/c1-audit-selftest.out:19` —
  `CONTROL_ASSERT_SELFTEST: 18/18 pass` (the records receipt the same sentence cites).
- `.ufo/evidence/round-99/sources/s324.json` (sha256 `346dcf46…f0349`) and
  `.ufo/evidence/round-99/sources/s325.html` (sha256 `477e0088…c3e9a7`) — the committed
  source snapshots; the S324 quote is located in the record's `abstractText` field, the S325
  quotes at renderer lines 135–137 and 163 (raw lines 136–138 and 166), and the recompute
  sentence at raw lines 142–145 and 188–190.
