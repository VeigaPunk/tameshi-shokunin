# Round 50 — selftest receipts for routed items R45.2 and R47.2

Produced by `.ufo/evidence/round-50/routed/run-receipts.sh LANE 43bfa7ae1f28359cd67bee4197e6a428298a8450 OUT` in a scratch clone at the revision in `revision.txt` (each command's stdout, stderr and exit beside it).

R45.2 — the selftest receipt for each of the two round-45 counters, which no round had committed:
- `r45-c1-freshness.selftest.stdout` — `python3 .ufo/evidence/round-45/freshness/measure.py --selftest`, exit 0, last line `VERDICT: PASS`.
- `r45-c2-coverage.selftest.stdout` — `python3 .ufo/evidence/round-45/coverage/measure.py --selftest`, exit 0, last line `VERDICT: PASS`.
The survivor-kill half of R45.2 is the round-46 receipt `.ufo/evidence/round-46/after/c2.stdout` (declared 25, killed 25).

R47.2 — the selftest receipt for each of the three round-47 counters, `addition-lint.py` and the criterion-93 falsifier block, which existed only as round-48 wave-seat artifacts:
- `r47-c1-measure.selftest.stdout` — `python3 .ufo/evidence/round-47/calibration/measure.py --selftest`, exit 0, `VERDICT: PASS`.
- `r47-c2-pool.selftest.stdout` — `python3 .ufo/evidence/round-47/hardening/pool.py --selftest`, exit 0, `VERDICT: PASS`.
- `r47-c3-coverage.selftest.stdout` — `python3 .ufo/evidence/round-47/coverage/measure.py --selftest`, exit 0, `VERDICT: PASS`.
- `r47-addition-lint.selftest.stdout` — `python3 .ufo/evidence/round-47/quality/addition-lint.py --selftest`, exit 0, `ADDITION_LINT_SELFTEST: cases=7 failed=0`.
- `r47-falsifiers.selftest.stdout` — the criterion-93 falsifier block `bash .ufo/evidence/round-47/quality/falsifiers.sh`, exit 0, `CRITERION-93-FALSIFIER-OK`.
