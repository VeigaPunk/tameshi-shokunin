# ScoutQ118 — Quarantine hand-check: tameshi S118

## Verdict: REFUSE the quarantine verdict — the `payload-absent` row is a misbound lint record, not a fabrication

Row: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:218`
`| tameshi | round1 | S118 | payload-absent | https://zenn.dev/seckeyjp/articles/j-six-mutation-testing | を導く): "生存ミュータントは | …`

## Observed facts

1. The register binds **S118 to the wrong URL**. Underlying lint record
   (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/quote-lint-full-v5.json`):
   `{lane: tameshi, id: S118, verdict: ABSENT, url: https://zenn.dev/seckeyjp/articles/j-six-mutation-testing, quote: "を導く): \"生存ミュータントは", binding: "id"}`.
   But tameshi S118 cites a different source entirely:
   `/home/vgpnk/Projects/shokuknow/lanes/tameshi/SOURCES-PROPOSED.md:34` — S118 = arXiv 2212.11762
   (Ojdanić, Papadakis, Harman, "Keeping Mutation Test Suites Consistent and Relevant with
   Long-Standing Mutants"). The zenn article is **S122**'s source (same file, :38).

2. S118's actual claim verifies verbatim against the live source.
   Command: `curl -fsSL https://arxiv.org/abs/2212.11762` (fetched today, 41,423 bytes,
   saved `/tmp/tameshi-r40-ScoutQ118/s118-arxiv.html`).
   Claimed quote (SOURCES-PROPOSED.md:99):
   `"We measure this degradation in relevance for 143,500 mutants in 4 non-trivial systems
   finding that, on overage, 52% degrade."`
   → exact substring of the arXiv abstract block, **including the source's own "on overage"
   typo**. Exact match: True.

3. Even the misbound quote is present: `curl -fsSL
   https://zenn.dev/seckeyjp/articles/j-six-mutation-testing` (171,806 bytes) contains
   `生存ミュータントは「穴の候補」であり、1件ずつ分類する必要があります。` verbatim — so the
   `payload-absent` claim fails on its own terms too ("the quote is in none of them" is
   false; it is in the cited URL). The linter's ABSENT verdict is doubly wrong: wrong
   (id→url) binding, and wrong absence call on the quoted span it did check.

## Disposition

- S118 is sound: cited source fetched, quote verified verbatim, claim ("re-computing the
  mutant suite per release makes scores incomparable; 52% of 143,500 mutants degrade")
  matches the abstract. **Present for adoption** on the strength of the arXiv check.
- The register row at :218 should not stand as evidence against S118: it recorded a quote
  from S122 under S118's id, then failed to find even that quote in its own URL.
- Register and live lane checkout untouched; no `corpus/` files edited.
