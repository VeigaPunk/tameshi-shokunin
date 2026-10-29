# T57W1ScribeItemsR56x5to7 — ledger rows R56.5, R56.6, R56.7

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base `5e3569969b532310d2b8a3d130901757a3df356b` (the commit that added the round-56 spot-check; `routed_at` for these items).
Rows: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScribeItemsR56x5to7/rows.json`.
Receipts: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScribeItemsR56x5to7-receipts/` (01-08).

## Result

| id | status at base | triage | one-line basis |
|---|---|---|---|
| R56.5 | open | fixable-cheap (fix staged by a sibling, not by me) | header of frozen `controls.sh` pre-registers only Phase A/B; arm 5 of the frozen C2 counter reads committed own receipts and checks presence only |
| R56.6 | open | fixable-costly | `tools/registry.json` holds only the `receipt-revision-gate-selftest` row; no gate-kind row names the gate; the 0/2/3 map lives in the gate header and branch only |
| R56.7 | open | fixable-cheap (errata staged) | `corpus/lessons/round-56.md` lines 318-319 still say no byte changed after C0/PIN; `877eede` changed QUALITY/SOURCES/knowledge between C0 and PIN |

No item is `fixed`: the spot-check commit is the base itself, so any fix commit would have to come after base, and none exists at base. No item is `declined`: each defect is still true at base and the fix is within the lane's remit.

## Evidence and verification

- Each row has 2-4 evidence items, each with a lane path, a span <= 30 lines, and an excerpt of 19-122 characters. The round-50 resolver functions (`check_evidence`, `has_key`) were imported from the committed `round-50/c1/measure.py` (not copied) and run against base. All 9 evidence items resolve; every row has at least one keyed item. Receipt 06.
- End-to-end fixture: a clone-only commit on top of base (`696f10fd`, not in the lane) carrying the ledger rows and a `**Planned (round 57):**` paragraph, scored by the round-50 `measure()` with `routed_at = base`. Result: `evidence_bad=0`, `key_miss=0`, `bad_status=0`, `missing=0`, `open=3`, and **`open_unplanned=3`**. Receipt 08.
- The `open_unplanned=3` is a rule gap, not a row defect. The round-50 `planned_ids` regex is `\bR4\d\.\d+\b`, so it cannot see `R56.x`. The staged round-57 counter (`.ufo/waves/round-57/w1/T57W1ExecC1Counter/stage/.ufo/evidence/round-57/c1/measure.py`, line 75) uses `\bR5[0-6]\.\d+\b`, which matches all three ids (regex check, receipt 08; the staged counter itself was not run by me). **L1 must make sure the counter that scores these rows admits `R5[0-6]`; the inherited R4-only regex fails every open row for round 56.**
- Round-56 frozen paths (`.ufo/evidence/round-56/`) were read only. Nothing in the lane was written; the only staged content is under this seat's `stage/`.

## Per-item basis

**R56.5 (open).** Routed as: pre-register the two controls generations in `controls.sh`'s header, and add a producer-provenance discriminator for the "own receipts" arm.
- Still true at base: `controls.sh` lines 3-5 pre-register Phase A/B only; `grep -c -i -E "generation|bootstrap|provenance|producer"` on `controls.sh` = 0 (receipt 03). C2 `measure.py` line 205 `a_raw = show(lane, rev, OWN_A)` reads the committed controls; lines 208-210 only test presence (`own-receipts-missing`); `grep -c -i -E "provenance|producer"` on that file = 0 (receipt 03).
- Fix: `T57W1ExecControls` has staged a round-57 `controls.sh` at `.ufo/waves/round-57/w1/T57W1ExecControls/stage/.ufo/evidence/round-57/controls.sh` whose header reads "ONE GENERATION. Controls are RECOMPUTED, never READ (round-56 lesson, Attempt 4, first Mistakes row; R56.5)". That design removes the bootstrap need and the read-the-receipt blind spot. I read the header only; I did not run it or check the discriminator in `T57W1ExecC2Counter`. No round-56 path is edited; no cold-read pinned input is touched. **I staged no duplicate.** Once that round-57 commit lands, the row can flip to `fixed` (the L1 must check the excerpt is absent at `routed_at` and present after).

**R56.6 (open).** Routed as: add a gate-kind registry row for `receipt-revision-gate.py` with the exit-code map.
- Still true at base: `tools/registry.json` line 1277 `"name": "receipt-revision-gate-selftest",` and line 1279 `"kind": "selftest",`. `grep -c receipt-revision` finds one row; the gate-kind count naming the gate is 0 (receipt 04). The gate header says `Codes (each a named refusal, exit 3):` (line 25); the unresolvable branch is `... codes=RECEIPT_REV_UNRESOLVABLE' % len(receipts)) return 2` (lines 192-194). So the map 0/2/3 exists in the lane only as prose.
- Fix cost: `tools/registry.json` is a pinned input of **148 cold-read entries under 16 headings**. Changing it uncredits every one of them until re-read. Headings (entry counts): `## Context gate classification and explicit exit classes — round 15` (17); `## Live-tree re-pin and entry-command monitor — round 17` (22); `### Round-17 gate/probe registry — re-pin and monitor` (14); `### Round-18 gate/probe registry — routed-defect closure` (20); `### Round-20 gate/probe registry — frozen receipt instruments` (13); `### Round-21 gate/probe registry — finite environment differential` (18); `### Round-26 gate/probe registry — report interop` (6); `## Standing rules` (4); `### The service's limits — what tameshi refuses to mutation-test` (5); `### Triggers T1–T3 and the re-pin rule` (5); `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (5); `## The operator's runbook and the six-leg regression (round 10, measured)` (14); `### Where to enter — four readers` (1); `## Seventh recorded case and full-page cold-read — round 16` (2); `## Ninth recorded case — round 26` (1); `## The cadence's first scheduled tick, and the service's limits (round 9, measured)` (1). Source: `coldledger.json` inputs, receipt 07 gives the pin totals.
- Classification: `fixable-costly`. No separate patch staged. The round-57 registry rows (`T57W1ExecRegistryRows`) have to edit the same file for the C2 target, so the L1 should fold R56.6's row into that edit and pay the re-read cost once.

**R56.7 (open).** Routed as: correct the "no byte changed after C0/PIN" phrasing.
- Still true at base: lesson `corpus/lessons/round-56.md` lines 318-319 read "No `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/`, `tools/` or ledger byte changed after C0/PIN". `git log --oneline c0137451..8c20d5c -- corpus/QUALITY.md corpus/SOURCES.md corpus/knowledge` = `877eede round-56: integrate wave-one and wave-two evidence` only. `git diff --stat c0137451 8c20d5c` for those paths = QUALITY +31, SOURCES +2, knowledge +39 (72 insertions). `8c20d5c..base` for the same paths: 0 commits. So the sentence is false for C0→PIN and true from PIN onward, which matches the spot-check's D-CF1 (receipt 02). The knowledge-entry evidence (`corpus/knowledge/receipt-revision-binding.md` line 207, `## Errata — round 56 wave-2 re-open`) is one of the lines that `877eede` added.
- Fix staged: `stage/corpus/lessons/round-56.md` = base file plus one appended errata block; the full diff is `round-56-lesson-errata.diff` beside this report. The original sentence is kept, the errata restates its scope. `corpus/lessons/round-56.md` has **0 cold-read pins** (receipt 07), so the change costs nothing in credit. The errata deliberately does not assess the deciding run's `FROZEN_UNCHANGED=1` or the monitor reading, which the lesson also mentions.
- Scope note: D-CF1 also names the report `.ufo/reports/round-56/tameshi.md`, which is not in the lane tree (it lives in the fleet commit), so I did not stage a change there.

## Dependencies for the L1

1. Open rows need the L1's newest `**Planned (round 57):**` paragraph to name `R56.5`, `R56.6`, `R56.7`. The base SCORECARD's newest planned paragraph is round 55. The SCORECARD is a live cold-read pin for **6 entries under 3 headings**: `## Standing rules` (2), `## The cadence's first scheduled tick, and the service's limits (round 9, measured)` (1), `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (3). Receipt 07 shows the totals; the 33 figure includes the external pins at historical revisions, which are not affected.
2. The round-50 `planned_ids` regex (R4-only) must not be inherited unchanged; see the verification note above.
3. If the L1 wants R56.5 or R56.7 to flip to `fixed` in a later commit, the excerpt must be absent at `routed_at` (the base) and present after; keys and the no-ack-words rule apply as in round 50.

## Sweeps run (no finding without its output)

- Sources of "fixed": `git log --oneline 5e3569969b..` returns 0 commits and lane HEAD equals base `5e3569969b` (receipt 09). Any later commit would need to be added to the `fixed` basis; none exists.
- Cold-read pins for each cited path: receipt 07.
- Negative searches for a fix already in the tree: receipts 03 and 04 (`generation|bootstrap|provenance|producer` in `controls.sh` and `c2/measure.py`; `receipt-revision` and `kind == gate` in `tools/registry.json`).
- Staged round-57 work checked for R56.5 only by reading the header; not executed.

## Tools

No tool was installed or upgraded. Scratch was under `/fast/scratch/hyaku/tameshi-r57/T57W1ScribeItemsR56x5to7` (removed at the end). The fixture clone and its commit were in that scratch path, not in the lane.
