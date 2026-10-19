# round-1 — non-author verification and spot-check (orchestrator, kaika)

Written by the integrator, not the lane (CORPUS.md: corrections and outside reviews are new
files; the lane owns `round-1.md`). Verifiers were fresh agents dispatched by the orchestrator
after the round landed at `01b358c30`; full reports are committed in the fleet repo at
`.ufo/waves/kaika-w3/tameshi-review.md` and `tameshi-critic.md`.

## Spot-check (LEARNING.md — at least one admit and one reject)

| decision | sample | verifier | result |
|---|---|---|---|
| admit | `corpus/knowledge/witness-scoped-kill-verdict.md` and `mutation-score-semantics.md` — reviewer re-opened S006 (pinned shmutant README) and S001 (Stryker metrics); agree, scoped (not a blind preregistration) | W3ReviewTameshi | agree |
| reject | S046 (PBT bibliography) rejected as a discovery index, not operational support; S029 and the Timeout rule — agree (reason and flip present) | W3ReviewTameshi | agree |

## Adjudication

ADMITTED after post-review fixes `01b358c`: calibration improved (QUALITY 5→10 criteria grounded in 11 mined mistake classes; SHONEN box-4 overreach corrected) with the score re-pinned at 6 — the box-3 increment is not credited (cold-read covered Appendix A+B only, probes reconstructed); capability `sources-registry` admitted (44 rows A=37 B=5 C=2, fleet census ok under UTC, lane census v2 CLEAN); depth/coverage/operability/freshness/adjacency unchanged. Trends: expansion improved (2 entries on new frontier ground), quality unchanged, discernment improved. Debts: box 3 needs a fresh reader to run the full page-defined procedure; 19 legacy entries lack provenance headers (L0: migration approach).
