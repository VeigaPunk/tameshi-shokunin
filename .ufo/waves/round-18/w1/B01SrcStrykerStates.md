# B01SrcStrykerStates — frontier step report (C1 mutant-state definitions)

## Verdict
DUPLICATE S001. No S065 row drafted, no rejection.

## Evidence
- Source opened: https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ via `read`. Fetch succeeded on the first attempt; no mirror used. Title "Mutant states and metrics | Stryker Mutator"; Docusaurus v3.10.2.
- Duplicate check: `grep -nF '<URL>' corpus/SOURCES.md` → line 12, row `S001`. `grep -cF` → 1. The URL strings are identical.
- Existing S001 row (`corpus/SOURCES.md:12`): kind docs, tier A, status mined, opened 2026-10-19, cadence 180d, used-by `corpus/knowledge/mutation-score-semantics.md`, §Mutant states and §Metrics cited.

## Page content relevant to C1 (verbatim, read 2026-10-20)
- §Mutant states, Killed (15 words): "When at least one test failed while this mutant was active, the mutant is killed."
- §Mutant states, Timeout: "It is counted as "detected"." (5 words, from §Mutant states Timeout entry)
- §Metrics, Mutation score (formula): `detected / valid * 100`
- §Metrics, Detected: `killed + timeout`; Undetected: `survived + no coverage`; Valid: `detected + undetected`.
- §Mutant states lists eight states (Pending, Killed, Survived, No coverage, Timeout, Runtime error, Compile error, Ignored). Matches S001's gloss "eight mutant states".

## Drift
[INFERENCE] No drift in the read sections versus S001's description. No stored snapshot exists to compare byte-for-byte; S001's recheck cadence (180d) stands.

## Tooling
None installed or updated.

## Out of scope / not done
- No S065 row written (duplicate).
- No edits to SOURCES.md, CORPUS.md, or any registry; the L1 decides whether S001 is cited for C1.
