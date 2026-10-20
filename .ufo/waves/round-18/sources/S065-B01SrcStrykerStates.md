# S065 draft — Stryker mutant states and metrics

DUPLICATE S001

- URL: https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/
- Existing row: `corpus/SOURCES.md:12` — S001, kind `docs`, tier A, status `mined`, opened 2026-10-19, cadence 180d, used-by `corpus/knowledge/mutation-score-semantics.md`.
- Match: exact string match; `grep -cF` on the URL returns 1 in `corpus/SOURCES.md`.
- No new row drafted. Per the Target, no S065 row is written.

Verbatim excerpts from the page fetched 2026-10-20, for the C1 check against S001 (not a new row):

- Gate quote 1 (§Mutant states, Killed; 15 words): "When at least one test failed while this mutant was active, the mutant is killed."
- Gate quote 2 (§Metrics, Timeout counted as detected; 5 words): "It is counted as "detected"."
- Gate quote 3 (§Metrics, formula; verbatim): `detected / valid * 100`

[INFERENCE] The live page matches S001's description (eight mutant states, detected = killed + timeout, score = detected / valid × 100). S001 was fetched 2026-10-19; the 2026-10-20 read shows no drift in these sections, but no stored snapshot was compared.
