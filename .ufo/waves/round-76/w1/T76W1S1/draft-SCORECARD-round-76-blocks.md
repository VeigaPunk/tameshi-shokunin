## Round 76 — declared claims (2026-11-04), frozen before data

<!-- DRAFT by seat T76W1S1 (godspeed). SKELETON mirroring the round-75
     declared/measured blocks. PLACEHOLDER markers are the L1's to resolve. -->

Plan: `plans/round-76.plan.md` (predicates, counters, kill rules, arms,
controls; no pre-data corrections — the design-phase candidates, the
seven-defect spec, the five instrument mutants, the battery transcripts and
the measured kill matrices are committed with the plan itself).
Base `451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0` (= `origin/master`, the
round-75 non-author closure verdict). Declaration
`5b7bbe1afa209b477bc71872d2424f6993e5c69d`. Round shape: one v1 wave, 12
seats (4 executor · 1 scribe · 1 scout · 2 reviewer · 1 critic · 1
mutation-tester · 1 connector · 1 sentinel; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. `labrat` is a
frozen-topology seat the validator rejects, so no labrat item exists; the
planner seat stays with the L1 per the orchestrator ruling.

- **R76-C1 — operability (verdict-only; sourced on the re-opened S006).** The
  two round-75 survivors become measured arms: `arm19-seatreports-printed-required`
  in `tools/wave-reconcile.py` (plus the seventh spec defect
  `adv-seatreports-require-printed-bypass`) and `ARM11_doc_rev_cli_binding`
  in `tools/selfstate-freshness.py` (a CLI-level arm for the
  `--doc-rev-ignored` survivor). Before: `WAVE_RECONCILE_SELFTEST: 18/18
  pass` and `SELFSTATE_SELFTEST: 10/10 pass` with both survivors alive (base
  receipts). After: `19/19` and `11/11`, the seven-defect battery
  `killed=7` with the new mutant dying on arm19 only, and all five
  instrument mutants killed (`doc-rev-ignored` on ARM11 only).
- **R76-C2 — calibration (the lowest scored numeric axis at 8).** The
  selfstate population 17 → 20 rows: the three frozen tuples in the plan —
  the two routed dated-literal capability cells (`six-leg
  content-disposition probe` `18/18` → instrument token `19/19`; `effective
  expectation reconciliation` `34/34` → `66/66`) and the round-17 line's
  `56/56` as a standing stale span row — whose quoted figure must equal the
  instrument's own printed figure at the measured revision. Before (measured
  at base with the extended manifest): `SELFSTATE: rows=20 match=16 stale=4
  unexpected=2`, exit 1. After: `rows=20 match=18 stale=2 unexpected=0`
  exit 0, with the two cells superseded to their instruments' own output
  format (`SELFTEST: PASS (19/19)`, `SELFTEST: PASS (66/66)`), the round-17
  bash-instrument values (`95/95`, `cases=7`) disclosed as named gaps, never
  rows, and the round-17 values standing as dated history.

Capability to enter: none this round (one capability-less completed round —
round 75 declined acquisition credit — sits inside the stagnation window
N = 2; the nudge does not fire).

## Round 76 — measured claims (appended at the records commit, PLACEHOLDER-DATE)

Declaration `5b7bbe1a`; work commit PLACEHOLDER-WORK-COMMIT. Receipts under
`.ufo/evidence/round-76/`; the round's report cites the tip.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R76-C1 | PLACEHOLDER-VERDICT | `WAVE_RECONCILE_SELFTEST: 19/19 pass` exit 0; `SELFSTATE_SELFTEST: 11/11 pass` exit 0; battery `MUTATE: DONE (target=wave-reconcile-arms-r76 defects=7 killed=7 survived=0 inconclusive=0 kill-rate=100%)`; `adv-seatreports-require-printed-bypass` dies on arm19 only (got=`printed-none-reached-comparison`); the five instrument mutants die on their named arms (`echo-doc-token` → ARM2, collateral ARM3 + ARM9 disclosed; `expect-ignored` → ARM2; `capability-absent-deflected` → ARM4; `zero-rows-success` → ARM6; `doc-rev-ignored` → ARM11 only); control GREEN; restore byte-identical; arms 1–15 byte-identical base→landed | `python3 -I -X utf8 tools/wave-reconcile.py --selftest`; `python3 -I -X utf8 tools/selfstate-freshness.py --selftest`; `bash tools/mutate-and-run.sh --target tools/wave-reconcile.py --defects tools/wave-reconcile-mutants.spec --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir "$HYAKU_SCRATCH/tameshi-r76/l1/battery" --label wave-reconcile-arms-r76` | PLACEHOLDER-LANDING-REV |
| R76-C2 | PLACEHOLDER-VERDICT | `SELFSTATE: rows=20 match=18 stale=2 unexpected=0` exit 0; every live row `match`; the two stale-ok rows `r74-frozen-addr-six` and `r76-r17-evidence-disposition`; selftest `SELFSTATE_SELFTEST: 11/11 pass`; the 17-row base population still re-runs green (`rows=17 match=16 stale=1 unexpected=0` exit 0); the landed manifest's three new rows equal the plan's frozen tuples byte-wise | `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --doc-rev <landing-rev>`; `python3 -I -X utf8 tools/selfstate-freshness.py --selftest` | PLACEHOLDER-LANDING-REV |

**No axis harmed.** depth 10, calibration 8, freshness 9 unchanged as numbers.
Monitored edits this round: `SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md`,
`corpus/QUALITY.md`, `SKILL.md`, `tools/registry.json` → forecast
`REKEY_COST sections=64 planned=6 at_risk=16 predicted_lost=16`
(`.ufo/evidence/round-76/rekey-cost-full-r76.txt`). One rekey batch after
every content edit; the monitor's green receipt reads `credited=64/64` at the
landing tip (PLACEHOLDER).

**Named carries to round 77.** PLACEHOLDER (the named bash gaps `107/107` /
`cases=10` stay routed until a runner widening; any wave-found survivor; any
closure-routed defect).
