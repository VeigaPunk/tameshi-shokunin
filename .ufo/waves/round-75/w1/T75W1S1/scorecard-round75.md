# SCORECARD.md round-75 block draft

Append target: `SCORECARD.md`, after the round-74 blocks (the file's last block
is the round-74 floor-sequence correction). Two sections in the round-74 shape:
the declared block, then the measured block.

---

## Round 75 — declared claims (2026-11-03), frozen before data

Plan: `plans/round-75.plan.md` (predicates, counters, kill rules, arms,
controls). Base `21ef81e99966198cf8cdb2c6d8e56aa3c482da56` (= `origin/master`,
the admitted round-74 non-author closure,
`corpus/lessons/round-74-verifier-spotcheck.md` §7). Declaration
`640d3fccfba7f6fab8e0341723b0fe6dbc200570`; pre-freeze correction 1
`7745d0e0` (kill rule (ii), append-only). Round shape: one v1 wave, 12 seats
(4 executor · 1 scribe · 1 scout · 2 reviewer · 1 critic · 1 mutation-tester ·
1 connector · 1 sentinel; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. `labrat` is a frozen-topology
seat the validator rejects, so no labrat item exists; the planner seat stays
with the L1 per the orchestrator ruling.

- **R75-C1 — operability (verdict-only; sourced on the re-opened S006).** The
  three mutants the round-74 wave measured as survivors become measured arms of
  `tools/wave-reconcile.py`: `M-C` (printed integer bound to the whole record
  instead of the row's span) plus the selective `_record_claim` bypass on
  `roles` and on `attack_share`. Before: `WAVE_RECONCILE_SELFTEST: 15/15 pass`
  (tool sha256 `97bb9272…`) and all three mutants alive. After: `18/18 pass`
  and each R75 mutant killed on its named arm (`arm16`/`arm17`/`arm18`) under
  the lane runner, with a committed six-defect spec that kills all six
  (three round-74 defects plus three new).
- **R75-C2 — calibration (the lowest scored numeric axis at 8).**
  `tools/selfstate-freshness.py` + `tools/selfstate-freshness.json`: 17 declared
  rows (16 live SCORECARD `## Capabilities` figures + 1 frozen historical
  statement) whose quoted figure must equal the instrument's own printed figure
  at the measured revision. Before (control scan at base): 16 rows, `match=9
  stale=7`, exit 1. After: `SELFSTATE: rows=17 match=16 stale=1 unexpected=0`
  exit 0, with the frozen row measuring `stale` every sweep and the seven live
  cells superseded to their instrument's figure.

Capability to enter (if it verifies): `<L1 fills — the plan carries no
capability-to-enter sentence; if selfstate-freshness is to enter as a
"self-state freshness check", add the Capabilities row with its counting
command now.>`

## Round 75 — measured claims (appended at the receipts commit, `<L1 fills: date>`)

Declaration `640d3fcc`; pre-freeze correction 1 `7745d0e0`; work commits
`<L1 fills>`. Receipts under `.ufo/evidence/round-75/`; the round's report cites
the tip.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R75-C1 | `<L1 fills: verifies / fails>` | `<L1 fills: measured>` — the frozen target is `WAVE_RECONCILE_SELFTEST: 18/18 pass` exit 0 and battery `MUTATE: DONE (target=wave-reconcile-arms-r75 defects=6 killed=6 survived=0 inconclusive=0 kill-rate=100%)`, each R75 mutant on its named arm only, control GREEN, restore byte-identical | `python3 -I -X utf8 tools/wave-reconcile.py --selftest`; `bash tools/mutate-and-run.sh --target tools/wave-reconcile.py --defects tools/wave-reconcile-mutants.spec --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --label wave-reconcile-arms-r75` | `<L1 fills>` |
| R75-C2 | `<L1 fills: verifies / fails>` | `<L1 fills: measured>` — the frozen target is `SELFSTATE: rows=17 match=16 stale=1 unexpected=0` exit 0, every live row `match`, the frozen row `expect=stale measured=stale ok` | `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --doc-rev <rev>`; `python3 -I -X utf8 tools/selfstate-freshness.py --selftest` | `<L1 fills>` |

**No axis harmed.** depth 10, calibration 8, freshness 9 unchanged as numbers
(the round records axis moves, not new scores). Monitored edits this round:
`SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md` → forecast
`REKEY_COST sections=64 planned=4 at_risk=13 predicted_lost=13`
(`.ufo/evidence/round-75/rekey-cost-r75.txt`). One rekey batch
(`r75-batch-1`) after every content edit; the monitor must read
`credited=64/64` at the landing tip `<L1 fills: receipt path>`.

**Named carries to round 76.** The `SKILL.md` gate-registry table still lists
neither `tools/wave-reconcile.py` nor `tools/additivity-range.py` (round-74
closure defect 4; no `SKILL.md` edit is planned this round, so the carry stays
open); the six older standing instruments still carry no `tools/registry.json`
row (T74W1SC1); the echo-stub disclosure stands — no printed line is an
authenticator, only the derived populations and the per-row tokens are
(T74W1R2); round-73 routed items 3–4 remain open
(`corpus/lessons/round-74-verifier-spotcheck.md` §6 item 6); rounds 61–71 carry
no `results.json` and round 60's vocabulary is `agent='task'` (round-73 carry).
If R75-C1 verifies, the two round-74 arm carries (`M-C` and the selective
`_record_claim` bypass) close; `<L1 fills: confirm or amend>.`
