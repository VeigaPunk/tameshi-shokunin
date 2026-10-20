# S066 draft — DUPLICATE S008

Decision: `DUPLICATE S008`

Evidence:
- Source: Practical Mutation Testing at Scale (Petrović, Ivanković, Fraser, Just), https://arxiv.org/abs/2102.11378
- Access: 2026-10-20 via the `read` tool (arXiv API route, method `arxiv`); the first fetch succeeded, so no mirror was tried.
- Duplicate check: `grep -c "2102.11378" corpus/SOURCES.md` → `1`; the only hit is line 19, row `S008` (`queued`, opened 2026-10-19, recheck 365d).
- No row drafted and no Gate line written, per the duplicate rule. SOURCES.md is not edited by this seat.

Candidate quotes for the L1 (only if S008 is advanced `queued` → `mined`; not a new row):
- Q1 (19 words, verbatim, abstract, item (3)): "Mutants are selected based on the historical performance of mutation operators, further eliminating irrelevant mutants and improving mutant quality."
- Q2 (13 words, verbatim, abstract, item (2)): "Mutants are filtered, removing mutants that are likely to be irrelevant to developers"
- Anchor: `## Abstract` of the fetched arXiv record (arXiv:2102.11378, published 2021-02-22, cs.SE).
