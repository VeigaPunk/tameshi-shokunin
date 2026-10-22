# ReviewMonitorHarm — harmed intermediate coldread reading at a08e85c5

Seat: TameshiR26.ReviewMonitorHarm (reviewer, leaf). Date: 2026-10-22.
Item: run the round-21 coldread monitor at the wave-1 integration revision and report the harmed intermediate reading: scores, sections covered/total, and a reason for every uncovered heading.

## Verdict

The intermediate reading is harmed, and the harm is the monitor behaving as designed, not a defect. Every one of the 32 uncovered headings is either (a) a heading whose credit was revoked because a pinned input changed in wave 1 — the only two pinned inputs that changed are `tools/mutate-and-run.sh` (ninth leg `js-cite-check`) and `tools/registry.json` (two new `mte-interop` rows) — or (b) a brand-new round-26 heading that has no ledger entry yet. A base-revision control run proves the attribution: at `d4140796` the same monitor reads full coverage; every drift it names at `a08e85c5` that is not one of those two files was already drifting at base on non-credit-carrying ledger entries.

## Measured readings

| reading | base `d4140796` | wave-1 `a08e85c5` |
|---|---|---|
| calibration_restraint_score | 8 | 6 |
| depth_score | 8 | 9 |
| sections covered / total | 62 / 62 | 32 / 64 |
| uncovered headings | 0 | 32 |
| ledger guardrail | 8 legs, all agree | 9 legs, all agree |
| measure exit | 0 | 0 |

Interpretation, grounded in the scoring doc at `.ufo/evidence/round-18/measure.py:26-29`: "calibration_restraint_score — 2 * count of boxes 1,2,4 marked `~` + 2 * (box3 is `~`, box3_full_page, and the SHONEN box-3 block at REV contains ... ledger.json)". At `a08e85c5` the SHONEN marks are all `~` and the box-3 link is present (`shonen.box3_marked=true`, `box3_ledger_link=true`), but `box3_full_page=false`, so the score lands on 6 rather than 8. The full-page credit fails precisely because the box-3 cold read no longer verifies end to end (32/64). Depth rose 8 to 9 because C1 landed: the ninth leg is wired in `tools/mutate-and-run.sh:95` ("js-cite-check kumitate-shokunin/scripts/cite-check.mjs 5/10 (50 %)") and `ledger_legs` now ends with `js-cite-check`, with `recorded_cases=9` and guardrail `header_legs=9, lists_agree=true, regression_calls=9, selftest_tuples=9, unique_recorded_gates=9`.

## Commands run (all inside the private clone `/tmp/reviewmonitorharm-r26`, detached at `a08e85c5d7f899e8a5992e20517edb1a380d79eb`)

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/reviewmonitorharm-r26
git -C /tmp/reviewmonitorharm-r26 checkout -q --detach a08e85c5d7f899e8a5992e20517edb1a380d79eb
python3 .ufo/evidence/round-21/coldread/measure.py --repo /tmp/reviewmonitorharm-r26 \
  --rev a08e85c5d7f899e8a5992e20517edb1a380d79eb --explain
# -> calibration_restraint_score 6, depth_score 9, sections_covered 32, sections_total 64, exit 0
git checkout -q --detach d4140796f4e48e8ec81b793facba73fbd03b4443
python3 .ufo/evidence/round-21/coldread/measure.py --repo /tmp/reviewmonitorharm-r26 \
  --rev d4140796f4e48e8ec81b793facba73fbd03b4443 --explain
# -> calibration_restraint_score 8, depth_score 8, 62/62, zero missing, exit 0
git diff --name-only d4140796f4e48e8ec81b793facba73fbd03b4443 a08e85c5d7f899e8a5992e20517edb1a380d79eb
# -> 30 files: 26 under .ufo/evidence/round-26/, plus SKILL.md, tools/mte-interop.py,
#    tools/mutate-and-run.sh, tools/registry.json
```

Nothing was run inside `/home/vgpnk/Projects/shokunin/tameshi-shokunin` itself; no jj command was run anywhere; no write touched any production file.

## Every uncovered heading, with reason

Reason strings are verbatim from the measure's `missing` array (drift entries semicolon-joined across that heading's ledger entries). Breaker = which wave-1-changed pinned input sits in every entry that was clean at base (M = `tools/mutate-and-run.sh`, R = `tools/registry.json`). Any input named below that is neither M nor R did not change in wave 1 and was already drifting at base on secondary entries — the base run still credited those headings 62/62.

| # | heading (start line in SKILL.md) | reason class | breaker |
|---|---|---|---|
| 1 | ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence (131) | drift: corpus/README.md (pre-existing) + M | M |
| 2 | ### The protocol — ordered, fail-closed (827) | drift: M; tools/trace-inputs.py (pre-existing) | M |
| 3 | ### The boundaries — what a service run is not (858) | drift: corpus/knowledge/fleet-kill-rate-ledger.md (pre-existing) + M | M |
| 4 | ### The report shape — what the opting-in lane receives (883) | drift: M | M |
| 5 | ## The leg ledger — replay, receipt, and how it is read (round 7, measured) (921) | drift: M | M |
| 6 | ### Using the ledger (933) | drift: M | M |
| 7 | ### Reading a receipt — the discipline (965) | drift: M | M |
| 8 | ### The tick and the pin read (1021) | drift: M | M |
| 9 | ### Triggers T1–T3 and the re-pin rule (1069) | drift: 12 pre-existing inputs + M | M |
| 10 | ### Six-case confidence statement (round 8, measured) (1092) | drift: pre-existing knowledge-file drifts + M | M |
| 11 | ### The tick, executed (1164) | drift: M | M |
| 12 | ### The receipt at this boundary (1212) | drift: fleet-kill-rate-ledger.md (pre-existing) + M | M |
| 13 | ### The service's limits — what tameshi refuses to mutation-test (1246) | drift: PROVINCE.md (pre-existing) + M | M |
| 14 | ## The operator's runbook and the six-leg regression (round 10, measured) (1272) | drift: pre-existing + M (+ R on already-dirty entries) | M |
| 15 | ### The operator's runbook — `corpus/knowledge/operator-runbook.md` (1281) | drift: operator-runbook.md (pre-existing) + M | M |
| 16 | ### The six-leg regression — usage and this round's receipt (1302) | drift: pre-existing + M + one pin now missing `tools/mutate-and-run.sh@75ed934d…` | M |
| 17 | ### The map — where a reader enters, artifact by artifact (1380) | drift: pre-existing README/knowledge drifts + M; one entry already `verdict:wrong-expectation` at base | M |
| 18 | ### Gate/probe registry (1499) | drift: SHONEN.md, tools/bash-witness-study.py (pre-existing) + M | M |
| 19 | ## Pin disposition and provenance correction — round 13 (1517) | drift: pre-existing + M | M |
| 20 | ### Round-13 gate/probe registry (1548) | drift: corpus/SOURCES.md (pre-existing) + M | M |
| 21 | ## Effective expectation reconciliation — round 14 (1563) | drift: pre-existing + M | M |
| 22 | ## Context gate classification and explicit exit classes — round 15 (1609) | drift: pre-existing + M and/or R (not separable from the explanation output; both changed this wave) | M+R |
| 23 | ## Seventh recorded case and full-page cold-read — round 16 (1754) | drift: M | M |
| 24 | ### Round-16 gate/probe registry (1806) | drift: M; trace-inputs.py (pre-existing) | M |
| 25 | ## Live-tree re-pin and entry-command monitor — round 17 (1814) | drift: registry-check.py, evidence-disposition.py (pre-existing) + R | R |
| 26 | ### Round-17 gate/probe registry — re-pin and monitor (1846) | drift: pre-existing + M and/or R | M+R |
| 27 | ## Eighth recorded case — round 18 (1905) | drift: mutation-case-kumitate-sources-check.md (pre-existing) + M | M |
| 28 | ### Round-18 gate/probe registry — routed-defect closure (1925) | drift: corpus/SOURCES.md, registry-check.py (pre-existing) + R | R |
| 29 | ### Round-20 gate/probe registry — frozen receipt instruments (1938) | drift: corpus/QUALITY.md, corpus/SOURCES.md (pre-existing) + R | R |
| 30 | ### Round-21 gate/probe registry — finite environment differential (1964) | drift: corpus/SOURCES.md (pre-existing) + R | R |
| 31 | ## Ninth recorded case — round 26 (2086) | `no-ledger-entry` — new section, no drift | new |
| 32 | ### Round-26 gate/probe registry — report interop (2097) | `no-ledger-entry` — new section, no drift | new |

Counts: 24 headings breaker M only, 4 breaker R only, 2 breaker M and/or R, 2 new sections. Totals reconcile: 30 input-drift + 2 new = 32.

## Attribution proof

1. Wave-1 production diff (base to integration) is exactly `SKILL.md` (+17), `tools/mutate-and-run.sh` (+116/−22), `tools/mte-interop.py` (+5/−2 line change), `tools/registry.json` (+20), plus 26 evidence files under `.ufo/evidence/round-26/`. Of these, only `tools/mutate-and-run.sh` and `tools/registry.json` are pinned inputs of the round-21 ledger; `SKILL.md` is the measured document, `tools/mte-interop.py` appears in no drift list.
2. A clean-at-base ledger entry can only become dirty through bytes that changed between the two revisions. Hence every formerly-credited entry went dirty on M and/or R — nothing else is possible, and the base run confirms the converse: at `d4140796` all 62 headings are credited, so every other named drift (corpus/SOURCES.md, corpus/QUALITY.md, corpus/README.md, PROVINCE.md, SHONEN.md, tools/trace-inputs.py, tools/registry-check.py, tools/bash-witness-study.py, tools/evidence-disposition.py, knowledge files, lessons, `.ufo/evidence/round-17/*`, `.ufo/evidence/round-18/measure.py`) pre-existed on entries that did not carry credit.
3. The two round-26 headings are new this wave: `git diff` on SKILL.md adds exactly `## Ninth recorded case — round 26` and `### Round-26 gate/probe registry — report interop` (SKILL.md:2086, SKILL.md:2097), and the monitor classifies them `no-ledger-entry`, the same class every fresh round's sections carry until the round's ledger entry lands.
4. `tools/registry.json` gained the two routed-item-1 rows this wave: `registry.json:1001` `"name": "mte-interop-selftest"` and `registry.json:1011` `"name": "mte-interop-check"`, both tagged `new-r26`. This is the intended C2 item-1 fix; its side effect is that the four registry-citing sections (25, 28, 29, 30) lose credit until a re-pin.

## Correction guidance (for the L1 integrator; I changed nothing)

No code defect to fix. The monitor is fail-closed by design: input-keyed credit revokes on drift, and new sections start uncredited. The restoring move is the lane's standing re-pin path, not an edit to frozen instruments: when round 26 closes, record the round-26 ledger entry (pins for the ninth leg and the two new rows, plus the two new SKILL sections), as rounds 7 through 21 each did; the six-case cadence sections describe exactly this trigger. Do not edit `.ufo/evidence/round-21/coldread/ledger.json` or the round-18/21 measure scripts — the selector rejects overrides (`--ledger-file`, `--ledger-rev`, `--inputs-overlay` exit 64), and the C1 counter at `.ufo/evidence/round-26/c1-measure.py` already exits 0 (`recorded_cases=9 wired_legs=9 depth_score=9`).

## Residual risk and verification gaps

- Per-entry separation of M versus R for headings 22 and 26 is not uniquely recoverable from `--explain`, because the measure re-sorts each heading's reason elements between runs; both files changed in wave 1, so the harm attribution is unaffected either way.
- The `verdict:wrong-expectation` entry under heading 17 existed at base as well; I did not investigate it — out of scope for this reading.
- The monitor reads external inputs from sibling repos and the fleet tree; my runs observed them as of 2026-10-22 and all were consistent between the base and integration runs (identical drift sets apart from M/R).
- I did not run the mutation runner, selftests, or any gate; scope was the monitor reading only.

## Tooling record

No tools were installed or upgraded. None were needed; the pacman pause and channel order were respected trivially.

## Sources opened this session (2026-10-22)

- `/tmp/reviewmonitorharm-r26/.ufo/evidence/round-18/measure.py:26-29` — "calibration_restraint_score — 2 * count of boxes 1,2,4 marked `~` + 2 * (box3 is `~`, box3_full_page, ..."
- `/tmp/reviewmonitorharm-r26/tools/mutate-and-run.sh:95` — "js-cite-check kumitate-shokunin/scripts/cite-check.mjs 5/10 (50 %)"
- `/tmp/reviewmonitorharm-r26/tools/registry.json:1001-1013` — `"name": "mte-interop-selftest"` / `"name": "mte-interop-check"`
- `/tmp/reviewmonitorharm-r26/SKILL.md:2086,2097` — "## Ninth recorded case — round 26" / "### Round-26 gate/probe registry — report interop"
