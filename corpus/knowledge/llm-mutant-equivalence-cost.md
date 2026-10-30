source: S286 — https://arxiv.org/abs/2406.09843 — §Abstract — arXiv:2406.09843 landing page (v5; v1 2024-06-14, revised 2026-01-22) — fetched 2026-10-30, 44019 B HTML, sha256 7af7e470fca3ef38e97d858b308dca20e815a4b919c9c235adae4d4f59c4a86e, extract `.ufo/waves/round-58/l1/sources/arxiv-2406.09843-abstract.txt`
source: S287 — https://pdf.dfcfw.com/pdf/H3_AP202503221646031757_1.pdf — lines 230-241 of the pdftotext extract — 大语言模型时代的变异分析 deck (王博, 北京交通大学) — fetched 2026-10-30, 5409054 B PDF, sha256 531abe11d23f2e37 (prefix), extract `.ufo/waves/round-58/l1/sources/dfcfw-deck.txt`
verified-at: 2026-10-30 — both sources opened by this lane this round (L1 fetch receipts under `.ufo/waves/round-58/l1/sources/`)
recheck: 365d — `curl -fsSL 'https://arxiv.org/abs/2406.09843' | grep -c 'equivalent mutant rates'` (expect 1; string verified in the copy opened 2026-10-30)
ground: F9 (LLM-era mutant generation + equivalence)

# LLM-era mutants raise fault detection and raise equivalence at the same time, and equivalence is declared undecidable

Admitted in round 58 from the shokuknow `corpus-expansion-1` package
(`merge/tameshi/knowledge/corpus/knowledge/llm-mutant-equivalence-cost.md`, staged ids S156/S165,
re-pointed by document to S286/S287 after the id-collision check; package text adapted before
landing — this entry is the lane's own re-grounding, not a byte copy).

## What the sources state

- S286 evaluates LLM-generated mutants against rule-based ones on 851 real
  bugs from two Java bug benchmarks: the LLM mutants are "more diverse ...
  behaviorally closer to real bugs and, most importantly, with 111.29% higher
  fault detection", but "the LLM-generated mutants have worse non-compilability,
  duplication, and equivalent mutant rates by 26.60, 10.14, and 3.51 percentage
  points, respectively" (§Abstract, verified present in the copy opened 2026-10-30).
- S287 states the equivalence class — "等价变异体：变异后的程序与原始程序在功能上完全相同" — and records
  the hazards of that class: it "影响变异分数计算的精确度" (degrades the precision of the
  mutation score), and deciding equivalence is undecidable in general:
  "判断等价变异体是不可判定问题：不存在一个自动算法完美解决" (extract lines 230-241; the class
  definition itself is line 231).

## What this means for the lane's survivor classes

- **A survivor is not yet a test hole.** The lane's survivor classes (its
  own arm-class matrix, and the B5 / D2 / D10 survivors) are all cases where
  a mutant was *not killed*. S286 shows that in an LLM-mutant setting a
  materially larger share of un-killed mutants are equivalent. Inference: an
  LLM-era survivor must be classified against an equivalence witness before
  it is counted as a gap in the suite — the same non-equivalence witness the
  lane already requires for rule-based mutants.
- **Three counters, not one.** S286 reports non-compilability, duplication
  and equivalence as three separate rates. The lane's F1 note (compile and
  runtime errors excluded from the score, per its held S001) means a
  non-compilating LLM mutant must not silently enter the denominator.
  Inference: an LLM-era sweep needs three counters.
- **The two literatures agree on the hazard.** S286 quantifies the
  equivalence rate in English; S287 states the same hazard in Chinese and
  adds an explicit statement that the problem admits no automatic solution.

## Boundary of this entry

- S286 is measured on Java and on real-world bug benchmarks; the lane's legs
  are one JavaScript gate and one bash gate. The transfer is **not
  measured**: no lane sweep has produced an LLM-generated mutant yet, and
  the entry supplies the counting contract, not a measurement.
- Equivalence stays undecidable (S287): a witness is per-mutant evidence
  (an input where the mutant and the original differ), never a general
  decision procedure. The lane's 1-minimality witness
  (`corpus/knowledge/delta-debugging-minimization-contract.md`) reduces a
  failing case; it does not decide equivalence.
- The F9 pilot move (a bounded LLM-mutant pilot with an independent outcome
  check) remains unmeasured; this entry does not close it.
