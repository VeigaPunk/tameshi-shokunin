## Round 76 — measured (appended at the records commit, PLACEHOLDER-DATE)

<!-- DRAFT by seat T76W1S1 (godspeed). SKELETON mirroring the round-75
     measured entry's shape. PLACEHOLDER markers are the L1's to resolve at
     the records commit. -->

Declaration `5b7bbe1a`; work commit PLACEHOLDER-WORK-COMMIT. Receipts under
`.ufo/evidence/round-76/`; the round's report cites the tip.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R76-C1 | PLACEHOLDER-VERDICT (verifies (measured) / fails-as-declared, per the frozen kill rule) | `WAVE_RECONCILE_SELFTEST: 19/19 pass` exit 0; `SELFSTATE_SELFTEST: 11/11 pass` exit 0; battery `MUTATE: DONE (target=wave-reconcile-arms-r76 defects=7 killed=7 survived=0 inconclusive=0 kill-rate=100%)`; the new defect `adv-seatreports-require-printed-bypass` dies on arm19 only (got=`printed-none-reached-comparison`); the five instrument mutants each die on their named arm (`echo-doc-token` → ARM2 with disclosed collateral ARM3 + ARM9; `expect-ignored` → ARM2; `capability-absent-deflected` → ARM4; `zero-rows-success` → ARM6; `doc-rev-ignored` → ARM11 only); control GREEN; restore byte-identical; arms 1–15 byte-identical base→landed | `python3 -I -X utf8 tools/wave-reconcile.py --selftest`; `python3 -I -X utf8 tools/selfstate-freshness.py --selftest`; `bash tools/mutate-and-run.sh --target tools/wave-reconcile.py --defects tools/wave-reconcile-mutants.spec --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir "$HYAKU_SCRATCH/tameshi-r76/l1/battery" --label wave-reconcile-arms-r76` | PLACEHOLDER-LANDING-REV (tool bytes sha256 PLACEHOLDER; battery receipt `.ufo/evidence/round-76/PLACEHOLDER`; selfstate battery receipt `.ufo/evidence/round-76/PLACEHOLDER`) |
| R76-C2 | PLACEHOLDER-VERDICT | `SELFSTATE: rows=20 match=18 stale=2 unexpected=0` exit 0; every live row `match`; the two stale-ok rows the frozen `r74-frozen-addr-six` and `r76-r17-evidence-disposition`; selftest `SELFSTATE_SELFTEST: 11/11 pass`; the 17-row base population still re-runs green at the landing rev (`rows=17 match=16 stale=1 unexpected=0` exit 0); the landed manifest's three new rows equal the plan's frozen tuple table byte-wise | `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --doc-rev <landing-rev>` | PLACEHOLDER-LANDING-REV (repairs; after receipt `.ufo/evidence/round-76/c2-after-r76.txt`) |

**No axis harmed.** depth 10, calibration 8, freshness 9 unchanged as numbers
(the round records axis moves, not new scores). Monitored edits this round:
`SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
`SKILL.md`, `tools/registry.json` → forecast
`REKEY_COST sections=64 planned=6 at_risk=16 predicted_lost=16`
(`.ufo/evidence/round-76/rekey-cost-full-r76.txt`, pre-data). One rekey batch
after every content edit; the monitor's green receipt must read
`credited=64/64` at the landing tip (PLACEHOLDER for the green receipt path).

**Named carries to round 77.** PLACEHOLDER (mirror the round-75 form: the
named bash gaps `107/107` / `cases=10` stay routed until a runner widening;
any survivor the wave found; any closure-routed defect; the stagnation-window
state after this round).

**Routed payments landed this round (round work, not claims).** the
receipt-exists scratch-leak fix (red-before
`.ufo/evidence/round-76/receipt-exists-leak-r76.txt` `leftover_count=2` →
green-after PLACEHOLDER `leftover_count=0`, selftest stays `4/4 pass`); the
round-73 plan erratum (appended to `plans/round-73.plan.md`); the round-74
S294 used-by old→new append (`corpus/lessons/round-74.md`, append-only); the
queue reconciliation (recorded in `corpus/lessons/round-76.md`); QUALITY
criteria 126/127; the registry home (SKILL.md gate-registry rows +
`tools/registry.json` rows for the standing instruments, with verdict-map /
pinned-value / write-scope / owner fields); the disclosed out-of-population
`wave-record reconciliation` cell repair (18/18 → 19/19); the four registry
re-pins (wave-reconcile selftest 18/18 → 19/19, wave-reconcile mutants
defects=6 → 7, selfstate selftest 10/10 → 11/11, selfstate sweep rows=17 →
rows=20).
