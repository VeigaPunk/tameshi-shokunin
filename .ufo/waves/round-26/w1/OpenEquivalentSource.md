# OpenEquivalentSource — definition of an equivalent mutant and its score treatment

**Verdict.** A primary source was found and opened: Madeyski, Orzeszyna, Torkar and Józala,
“Overcoming the Equivalent Mutant Problem”, IEEE TSE 40(1), 2014, author preprint PDF. It both
defines an equivalent mutant and gives the mutation-score arithmetic that excludes or includes it.
A second, tool-level primary page (Stryker Mutator docs, “Equivalent mutants”) was also opened and
shows the same treatment from the vendor side. **No existing SOURCES.md row covers the ask**; the
three nearest rows are adjacent but each misses one half (ids and URLs below).

## 1. Existing-row check

Command, from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`:

```
grep -n -i -E "madeyski|equivalent-mutants|overcoming the equivalent" corpus/SOURCES.md
```

Observed: no matching line. So neither the TSE 2014 paper nor Stryker’s dedicated equivalence page
is registered.

Adjacent rows (from `grep -n -i "equivalent" corpus/SOURCES.md`, hits at lines 20, 66, 188):

| row | line | url | why it does not cover this item |
|---|---|---|---|
| S009 | 20 | https://discovery.ucl.ac.uk/id/eprint/1499169/ | Trivial Compiler Equivalence: detection rates for equivalent/duplicate mutants. No definition and no score arithmetic. |
| S057 | 66 | https://discovery.ucl.ac.uk/id/eprint/10056704/1/survey.pdf | Papadakis et al. survey §5.3.1: states the equivalent-mutant problem and the need for an off-suite non-equivalence witness. Tier B, and its `teaches` cell carries the consequence, not a definition or a score formula. |
| S001 | 12 | https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ | Gives `score = detected / valid x 100` with no equivalence state or exemption; the word “equivalent” does not appear on that page (page re-opened this session). |

So: S057 covers *handling* an equivalent survivor, S001 covers *score arithmetic*, but no row both
defines an equivalent mutant and says how a score counts it. That is the gap this item closes.

## 2. Opened source — definition plus score treatment

- **URL:** https://madeyski.e-informatyka.pl/download/Madeyski13TSE.pdf
- **Access date:** 2026-10-22, ordinary HTTP fetch of the author’s own PDF (no browser, no challenge
  bypass; the reader converted the PDF text).
- **Identity:** header reads `IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 40, NO. 1, JANUARY 2014
  (PREPRINT V.2)`; DOI `10.1109/TSE.2013.44`. The published IEEE text was **not** opened:
  https://doi.org/10.1109/TSE.2013.44 resolved through CrossRef metadata only, which reports
  “No abstract available” and serves no full text. Tier is therefore B (author preprint), the same
  limit S057 carries.
- **Anchor:** pp. 1–2, §1 *Introduction*.

Located quotes (each ≤25 words, verbatim from the opened text):

1. Definition by effect: “there are mutations which keep the program semantics unchanged and thus
   cannot be detected by any test suite” (18 words).
2. Why no tool settles it: “The problem of detecting equivalence either between two arbitrary
   programs or two mutants is an undecidable problem” (17 words).
3. Score treatment when equivalence is known: the score is given as `MS = MK / (MT − ME)` where
   “MT is the total number of produced mutants” and “ME is the number of equivalent mutants”
   (7 words for the second fragment).
4. Score treatment when equivalence is not known: “analysing real world software projects there is
   often a need (also in this paper) to ignore equivalent mutants” (18 words), after which only the
   “mutation score indicator” `MSI = MK / MT` can be measured.

Reading: equivalence is handled **arithmetically, not as a mutant state**. An identified equivalent
mutant is subtracted from the denominator, which raises the reported score; an unidentified one stays
in `MT` and depresses it. The paper records no automated way to identify all of them, so in practice
the second regime (`MSI`) is what a tool reports.

## 3. Opened source — vendor-side confirmation

- **URL:** https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/
- **Access date:** 2026-10-22, ordinary HTTP fetch. Page exposes no version or commit pin (Docusaurus
  v3.10.2 generator only), the same limitation S001 records.
- **Quotes:** “It is called equivalent mutant. There is no definitive way for Stryker to find and
  ignore them.” (17 words); “There is currently also no way yet to mark them to be ignored.”
  (14 words); and the stated consequence, “don’t be scared of not 100% mutation score” (9 words).
- **Mechanism, cross-checked against S001’s page opened this session:** the `Ignored` state “will not
  count against your mutation score”, but this page says equivalent mutants cannot be put into it.
  They therefore stay `Survived`; `Survived` is part of `Undetected`, and `Valid = detected +
  undetected`, so `detected / valid` counts every equivalent survivor as a miss. Stryker’s
  documentation thus confirms the `MSI` regime from §2 rather than the `MS` regime.

## 4. PIT is not a usable source here

Opened https://pitest.org/faq/ and https://pitest.org/ (both 2026-10-22, ordinary fetch). The FAQ has
no equivalent-mutant section: its nearest entry, “I have mutations that are not killed but should be”,
explains compiler-inlined `finally` blocks, not equivalence. The homepage defines only killed versus
lived and “percentage of mutations killed”. Neither page contains the word “equivalent”. PIT’s
mutators and incremental-analysis pages were already registered as S056/S041/S047/S048; no PIT page
opened this session defines equivalence or its score treatment.

## 5. What this changes for the lane

- The lane’s ledger arithmetic is Stryker’s `detected / valid`, i.e. Madeyski’s `MSI`, and Stryker’s
  own docs say equivalent mutants cannot be excluded from it. A survivor is therefore recorded as
  undetected by construction, and that is exact only when no survivor is equivalent.
- Consequence for the sweep’s hole-aimed mutants: calling a survivor a gate hole assumes it is not
  equivalent. The sources supply the honest alternatives — an off-suite non-equivalence witness
  (S057’s shape) or the plain statement that equivalence was not assessed and the figure is an `MSI`.
- If a survivor is ever argued equivalent, the documented correction is to remove it from the
  denominator (`MS`) and say so; there is no tool state for it, and Stryker must not be described as
  finding or ignoring such mutants.
- No claim is made here that any particular lane mutant is equivalent; only the score convention is
  sourced.

## 6. Suggested registry rows (draft only; the L1 integrator owns SOURCES.md)

```
| S088 | Overcoming the Equivalent Mutant Problem: A Systematic Literature Review and a Comparative Experiment of Second Order Mutation (Madeyski, Orzeszyna, Torkar, Józala; IEEE TSE 40(1), 2014; author preprint) — https://madeyski.e-informatyka.pl/download/Madeyski13TSE.pdf | paper | B | equivalent-mutant definition and the score arithmetic that excludes identified equivalents | §1 Introduction pp. 1–2 @ preprint v.2, DOI 10.1109/TSE.2013.44, fetched 2026-10-22 (published IEEE text not opened) | an equivalent mutant leaves semantics unchanged and no test can detect it; scores subtract ME from the denominator when known, else the mutation score indicator MK/MT keeps it in | queued | 2026-10-22 | 365d | — |
| S089 | Equivalent mutants (Stryker Mutator docs) — https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ | docs | A | Stryker’s own statement that equivalents cannot be found or ignored, so they remain survived | §Equivalent mutants, whole page @ fetched 2026-10-22, no version or commit pin exposed (Docusaurus v3.10.2) | Stryker cannot detect or ignore equivalent mutants, so they stay survived and count against detected/valid; 100% is declared unreachable | queued | 2026-10-22 | 180d | — |
```

## 7. Remaining unknowns

- The published IEEE text (paywalled) was not opened; the preprint’s wording may differ from the
  version of record.
- Stryker’s page carries no commit pin or last-updated date, so its tier-A anchor is a page snapshot,
  not a revision.
- Only PIT’s FAQ and homepage were checked for equivalence; the rest of the PIT site was not swept,
  so “PIT does not document equivalence” is not established beyond those two pages.

## 8. Tooling

Nothing installed or upgraded; no package manager was invoked.
