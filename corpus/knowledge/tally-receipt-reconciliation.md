# Tally-receipt reconciliation — a recorded selftest tally is re-read from the receipt it cites

source: S324 — Nuijten, Hartgerink, van Assen, Epskamp, Wicherts, "The prevalence of
statistical reporting errors in psychology (1985-2013)", Behavior Research Methods 2016,
Europe PMC record (abstract) fetched 2026-11-08, snapshot
`.ufo/evidence/round-99/sources/s324.json` 6409 B sha256
`346dcf46d3e6ccfe20d269b5b74ca4d21df98c8731c57858808d4c856d0f0349`;
S325 — statcheck web FAQ `http://statcheck.io/`, fetched 2026-11-08, snapshot
`.ufo/evidence/round-99/sources/s325.html` 27778 B sha256
`477e0088c987eabd845a81bd38e716959296c2a691b0ae57d9df45e66cb3e9a7`
verified-at: 2026-11-08; receipts `.ufo/evidence/round-99/records/c1-population.out`,
`c1-r94-only.out`, `c1-r93-only.out`, `c1-selftest.out` (bytes executed from the records
revision `808a43778701cf1b05762584954d435481dc6fa2`); instrument `tools/tally-reconcile.py`
sha256 `a1c50bb41599cfd663749855c7924c03360a46be2811812fb66f25c37b09b482` at that revision
(round-99 amendments A2-A4, A9, A10 over the frozen `60d59bea…` at `46651051`)
recheck: 365d; reopen S324/S325 and re-run the reconciler over the newest six rounds
ground: calibration — the lane's own records (rounds 93-98 lessons and plans); not a
frontier row, no coverage-map ground is claimed by this entry

## 1. The question

A round record states figures it did not compute in place: "the selftest prints
`DISPOSITION_SELFTEST: 8/8 pass`", followed by the path of the receipt that holds the
run. The figure is the lane's self-assessment; the receipt is the observed state. Nothing
forces the two to agree. The figure is typed when the sentence is written, and the
instrument keeps moving: a case is added, a battery is repaired before the records run,
and the receipt prints `9/9` while the sentence still says `8/8`.

Two non-author closures found this by reading. Round 94's frozen C2 tally `8/8` stood beside a
receipt printing `9/9` (`corpus/lessons/round-94.md:66`; round-94 spot-check line 102); the
claim landed `unprovable` on that alone. Round 98's report said the C1 selftest was `18/18`
"at the freeze", citing a freeze receipt that prints `12/12` (round-98 spot-check D2). The
lane held QUALITY 169 ("a frozen tally cites its receipt path") but no instrument read the
citation.

## 2. What the outside practice says

statcheck is the reference case of reading a reported figure back against its inputs.
It extracts each reported test result, recomputes the p-value from the reported statistic
and degrees of freedom, and flags disagreement. S324's abstract measured how often the
two drift: "half of all published psychology papers that use NHST contained at least one
p-value that was inconsistent with its test statistic and degrees of freedom" (25 words).
The authors were not careless people; the figure and its source simply live in different
places and are edited at different times.

S325 states the other half of the lesson, the grammar boundary: statcheck "checks whether
your p -values match their accompanying test statistic and degrees of freedom" only for
results reported completely and in APA style, and "Statcheck usually can't find statistics
in tables." A result outside the grammar is unchecked, not consistent. A reconciler's
silence is evidence only inside its declared grammar.

S326 (GRIM, rejected) shows what this is not: GRIM asks whether a reported mean is
arithmetically possible for its sample size — a feasibility test with no binding to the
artifact that produced the figure. Tameshi's tallies are integer counts copied from
receipts; the useful check is the binding, not feasibility.

## 3. The lane's rule, as an instrument

`tools/tally-reconcile.py` (round 99) reads records and receipts as blobs at one revision
and, for every recorded tally on a line that cites a receipt, compares the claim with the
receipt:

| item | rule |
|---|---|
| tally forms | `TOKEN: N/M pass` (TOKEN upper-case, ≥3 chars); the word `selftest` followed within 12 non-digit characters by `N/M` |
| citation | a path on the same line ending `.out`/`.txt`/`.log`/`.json` where the suffix ends the path, not after a `scheme://` (a scheme-less host path is cited and grades unbound) |
| resolution | the tree path, else the record's own round dirs (`.ufo/evidence/round-NN`, `.ufo/waves/round-NN`); none → `unbound unresolved`, several → `unbound ambiguous-path` |
| grading | `matched` only when every receipt line carrying the token (`TOKEN: n/m`, whatever follows it) shows the claimed N/M; any other value → `mismatched`; token absent → `unbound`; a non-UTF-8 record or receipt is refused at setup |
| no citation | `uncited`, counted and never graded |

Over the twelve round-93..98 lessons and plans it prints
`TALLY_RECONCILE records=12 tallies=28 pairs=9 matched=2 mismatched=1 unbound=6 uncited=19`
(`.ufo/evidence/round-99/records/c1-population.out`; the same line at the freeze in `pre-freeze/`): the single mismatch is the round-94
line the closure found; two pairs confirm; six cited receipts could not be bound by the
grammar; nineteen tallies cite nothing on their line.

## 4. What the numbers say about the lane, and what they do not

- **Only 2 of 28 recorded tallies are mechanically confirmed.** Most tallies are stated in
  prose or code blocks with the receipt named elsewhere in the paragraph, or not at all.
  That is a calibration finding about how the lane writes, not a claim that 26 tallies are
  wrong.
- **Unbound is not wrong.** Four unbound pairs cite a receipt by basename under a
  sub-directory the grammar does not search; two pair a tally with a different receipt on
  the same line (a line citing the red receipt and stating the selftest tally). The round's
  own wave tested which unbound pairs have a confirming receipt (`.ufo/waves/round-99/w1/`).
- **The practice that makes the counter useful:** state a tally on the same line as the
  receipt that prints it, by a path the tree resolves. A record written that way is
  checkable by a non-author with one command; a record written otherwise is only readable.

## 5. Limits

Per-line pairing; two tally spellings only (`6/6 killed`, `9 of 9` and bare table cells are
not recognised); one repository per run (a fleet-repo report is outside); an append-only
erratum does not clear the original line. These are the statcheck lesson applied to the
lane: silence outside the grammar is not agreement.
