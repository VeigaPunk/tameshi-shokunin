# T57W1LabratFloor — cold-read floor cost of a ledger JSON edit (hypothesis H)

Lane base: `5e3569969b532310d2b8a3d130901757a3df356b`. Monitor: `.ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev <HEAD>` (round-18 credit algorithm, round-21 ledger `ledger.json`, 609 entries). Every probe is a commit on a fixture clone of the base (`git clone --shared`, detached at base, fixture identity, `-C`, top-level asserted). No lane or fleet file was edited.

## Result (credited / 64, calibration score)

| Path edited (probe) | Bytes change | Credited | Score | Lost headings | Ledger pins (internal / external) |
|---|---|---|---|---|---|
| base (control) | none | 64/64 | 8 | 0 | — |
| `corpus/routed-defects.json`, 51 synthetic rows, text splice | +663 lines | 64/64 | 8 | 0 | 0 / 0 |
| `corpus/routed-defects.json`, 51 rows, full json re-dump (first pass, superseded) | reformat | 64/64 | 8 | 0 | 0 / 0 |
| `tools/registry.json`, 3 rows, text splice | +99 lines | 53/64 | 6 | 11 | 148 / 38 |
| `tools/registry.json`, 3 rows, full json re-dump (first pass, superseded) | reformat | 53/64 | 6 | 11 | 148 / 38 |
| new `corpus/knowledge/probe-floor-r57.md` (3 lines) | new file | 64/64 | 8 | 0 | — (not in any pin) |
| `corpus/knowledge/verification-patterns-fleet.md`, +1 line (existing pinned entry; extra control) | +2 lines | 55/64 | 6 | 9 | 49 / 19 |
| new `corpus/lessons/round-57.md` (3 lines) | new file | 64/64 | 8 | 0 | — |
| `SCORECARD.md` (root), +2 lines | +2 lines | 64/64 | 8 | 0 | 6 / 29 (pins do not match base bytes, see below) |
| `LOG.md` (root), +2 lines | +2 lines | 64/64 | 8 | 0 | 6 / 19 (pins do not match base bytes) |

Lost headings (raw `reason` in receipts):

- registry (both variants, identical lost set): `## Standing rules` (start 17), `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (159), `### Triggers T1–T3 and the re-pin rule` (1100), `### The service's limits — what tameshi refuses to mutation-test` (1282), `## The operator's runbook and the six-leg regression (round 10, measured)` (1312), `## Context gate classification and explicit exit classes — round 15` (1652), `## Live-tree re-pin and entry-command monitor — round 17` (1857), `### Round-17 gate/probe registry — re-pin and monitor` (1889), `### Round-18 gate/probe registry — routed-defect closure` (1968), `### Round-21 gate/probe registry — finite environment differential` (2007), `### Round-26 gate/probe registry — report interop` (2175). Every reason is `input-drift:...tools/registry.json` (among other pins for some).
- verification-patterns-fleet.md (+1 line): `## Standing rules` (17), `## Source notes` (58), `## Gate-shape decision table` (86), `## Mutation-sweep recipe` (159), `## No-permissiveness audit recipe` (494), `### Triggers T1–T3` (1100), `### Six-case confidence statement` (1123), `### The service's limits` (1282), `## Live-tree re-pin and entry-command monitor — round 17` (1857).

## Findings against H

1. **routed-defects.json: confirmed, zero floor cost at any append size tested.** No entry in the 609-entry ledger pins `corpus/routed-defects.json` (0 internal, 0 external). The routed ledger can take the 51 rows without touching a cold-read heading. Only a future ledger that pins it would change this. Caveat: the rows were synthetic (same byte count class as the real 51-item append, not the real item text); since the cost is pin-based, row content does not enter the calculation.
2. **registry.json: H's mechanism holds, but the cost is not small and it is not proportional to the append.** `tools/registry.json` is pinned by 148 internal inputs, so any byte change to it drops 11 headings and the calibration score 8 -> 6. Three rows and a full reformat of the same file produce the identical 11-heading loss set, so the cost is a step on the first changed byte, not per row. I disagree with any reading that treats the registry append as cheap: the three gate rows cost 11/64 headings unless the 53/64 state is re-keyed in wave 3.
3. **New knowledge file: confirmed, zero cost.** A file no entry pins is invisible to the monitor. The cost of editing `corpus/knowledge/*.md` is set by pins, not by the directory: an existing pinned entry (`verification-patterns-fleet.md`, 49 pins) costs 9 headings, and that is already a cost on the L1's re-key list.
4. **Lesson file (new `round-57.md`): confirmed, zero cost.**
5. **SCORECARD.md and LOG.md (root): zero cost, but for a reason I checked rather than assumed.** Both are pinned by 6 internal entries and by external entries. The internal pins name sha prefixes `17449104f59f`, `dc8eec4d7f62`, `1b0124a79a81`, `766c6ee07521`, `3dcd2a0eb2d8`... and `533b5b6275ea` (external), none equal the base bytes (`git -C base show 5e35...:SCORECARD.md | sha256sum` -> `9f616fba3168`; `LOG.md` -> `a463d17f7128`; `.../w1/T57W1LabratFloor-receipts/base-scorecard-sha.txt`). They are stale pins that the credit algorithm does not select at base, so appending to them changes nothing that is credited. This is a property of the current ledger, not a guarantee: if a wave re-pins SCORECARD or LOG to base bytes, the same append would cost headings. Recommend the L1 keep appends to root SCORECARD/LOG out of any content-final commit that is meant to keep 64/64, or re-key after.

## Where I cannot confirm the other seat

T57W1ScoutDrift's report was not present in `.ufo/waves/round-57/w1/` when I wrote this (siblings present: ScoutSourceA/B, Connector*, Exec*, Crit*). I did not read peers' output, so I have no disagreement to record against it beyond items 2 and 5 above, which are my measured positions.

## Receipts

Directory: `.ufo/waves/round-57/w1/T57W1LabratFloor-receipts/`
- `<probe>.measure.json` — full monitor output for base and each probe (`coldread.sections[*].credited/reason/heading`).
- `summary.json` / `summary.txt` — per-probe credited, score, lost headings, rev.
- `probe-commits.txt` — probe commit ids and `git diff --shortstat` against base.
- `base-scorecard-sha.txt` — base sha256 of the root SCORECARD.md and LOG.md.

Commands run: the monitor as above (≈2 min each under current host load; not 40 s as the brief estimated), `git clone --shared`, `git checkout --detach`, `git commit` with fixture identity, `json.loads` of each spliced file, and a ledger scan (`python3` over `ledger.json`) for pin counts per path.

## Did not do / limits

- Did not run the 51 real routed items; the monitor does not read routed-defects.json, so content has no effect on credit.
- Did not measure the 51-row registry variant (not requested) or any combined probe; the registry result is one-step-per-file so the 3-row number is representative of the step.
- No installs or tool upgrades. Scratch under `/fast/scratch/hyaku/tameshi-r57/T57W1LabratFloor` is removed at the end of the run.
