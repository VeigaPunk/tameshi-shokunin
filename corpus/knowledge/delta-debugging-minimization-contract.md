source: S271 — https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf — §I Introduction ("Simplification of test cases"), §III-A Definition 10, §III-C Proposition 11, §IV-B Figs. 11-12, Abstract — Zeller & Hildebrandt, IEEE TSE 28(2), February 2002, DOI 10.1109/32.988498; course-mirror PDF re-opened 2026-10-26, 247,738 B, sha256 7ed0c812, snapshot `.ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf`
source: S024 — https://www.fuzzingbook.org/html/Reducer.html — §Delta Debugging — The Fuzzing Book (held tier-B restatement of the same criterion; re-fetched 2026-10-26 byte-identical to the round-29 snapshot, `.ufo/waves/round-50/w1/T50ScribeSrcHeld.md`)
verified-at: 2026-10-26 — snapshot sha256 7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa; the mirror is 17 pages paginated 1-17 with no journal folios, so anchors are sections, definitions and figures, never printed pages
recheck: 730d — `curl -fsSL 'https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf' | pdftotext - - | tr -s ' \n' ' ' | grep -c 'removing any single input entity'` (expect 1; default reading-order extraction — `-layout` hyphen-folds "simplifies")
ground: F6 (fixture minimization for survivors)

# A reduced fixture states its minimality witness and its cost in test runs

Admitted in round 50 from the shokuknow `corpus-expansion-1` package (staged S167, theme F6), re-grounded on
the lane's own fetch; the package's text was edited before landing (14 edits, `.ufo/waves/round-50/w1/T50ScribePkgDD.md`
`## Required edits`), and one of its two claims was refused (below).

## What the source states

- **The minimality criterion.** §I: the algorithm "is fed with a failing test case, which it simplifies by
  successive testing. It stops when a minimal test case is reached, where removing any single input entity
  would cause the failure to disappear." Definition 10 (§III-A) states n-minimality formally, and
  Proposition 11 (§III-C) states that ddmin's result "is 1-minimal in the sense of definition 10".
- **The cost is reported in test runs, per reduction.** §I: "After 57 tests, the original 896-line HTML input
  is reduced to the minimal failing test case"; §IV-B (Fig. 11): "After 82 test runs (or 21 minutes), only 3 out
  of 95 user actions are left". The Abstract reports the case study's total: "The case study required 139
  automated test runs, or 35 minutes on a 500 MHz PC" — 82 + 57 = 139. The line-to-tag stage that follows took
  "26 steps" (§V-A); it is a second reduction of an already one-line input, not a competing count for the first.

## What it means for the lane

- **The witness is a removal that loses the failure.** A reduced fixture is 1-minimal when removing any single
  unit makes the kill disappear. The direction matters: the witness is not an entity whose removal restores a
  failure. The lane's round-50 counter checks exactly this, unit by unit, on the emitted case
  (`.ufo/evidence/round-50/c2/measure.py`, docstring "minimal").
- **A reduction without its run count is not comparable.** Inference: the lane should report runs spent next to
  units removed, per reduction, and compare like with like — the source's 57 is one reduction (896 lines to 1),
  139 is two reductions summed. The lane's own earlier datum, round 29's "171 oracle tests" for a reduction that
  kept nothing (`corpus/knowledge/survivor-fixture-minimization.md:53`), is a spent cost with no reduction, so it
  is not a counterpart to 57.
- **What is new against the lane's holdings.** The lane already held the 1-minimal criterion as a tier-B
  restatement (S024, `corpus/knowledge/survivor-fixture-minimization.md:3,16`). This entry adds the tier-A origin,
  the formal definition and guarantee (Definition 10, Proposition 11), and a published per-reduction cost datum.
- **B5 stays where round 29 left it.** The lane's B5 probe was tried: ddmin "made 171 oracle tests and kept
  nothing" because B5 is masked under the pinned declaration (`corpus/knowledge/survivor-fixture-minimization.md:53,57`).
  The live F6 move is the round-50 shrinker over the round-49 generator's killing cases
  (`corpus/knowledge/fixture-shrinking-pilot.md`); the F6 status line is `corpus/README.md` `## Round 50`, not this entry.

## Refused from the package

- The package attributed "139 automated test runs, or 35 minutes" to the 896-line reduction. The source gives 57
  for that reduction (§I, §IV-B Fig. 12); 139 is the Abstract's two-reduction total. Refused under QUALITY 2.

## Boundary

- The carrier is a university course mirror, not IEEE Xplore; the running head ("IEEE TRANSACTIONS ON SOFTWARE
  ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002") and the title block identify the article.
- The source's inputs are a web browser's HTML input, recorded user actions, GCC and fuzz inputs — not a test
  gate. The criterion and the cost unit transfer; the domain does not.
