# Audit43 — scoped wave-2 callback accounting

**Verdict:** For the three named identities only, the frozen outcome rows declare `completed`; each exact ID and `mutation-tester` role matches its wave-2 specification and registry membership, and each listed report exists and claims completed execution. No identity or role mismatch was found. The normalized outcome rows do not retain a raw callback-result envelope for these seats, so this audit does not authenticate callback provenance; the status conclusion is limited to the declared outcome source, consistent with the C1 contract.

## Frozen population and evidence

| Seat | Spec / registry membership | `original-outcomes-final.json` row | Existing report and completion claim | Finding |
|---|---|---|---|---|
| `KillR07` | `spec2.json:391-398`: role `mutation-tester`; registry `w2/swarm-registry.json:437-446`: key `KillR07`, kind `spawn`, agentId `TameshiR21.KillR07`, role `mutation-tester`, axes `operability`, `calibration` | `original-outcomes-final.json:1066-1073`: same name, ID, role; status `completed`; report `.ufo/waves/round-21/w2/KillR07.md`; `replaced:false` | File exists. It says “done” and reports the frozen command exit 0, green pristine control, intended mutant failure, and a 0→1→0 restoration run (`w2/KillR07.md:1-22`). | Identity/role match; declared outcome status is completed. Report claims executed work; it is not the status authority. |
| `KillT04` | `spec2.json:400-407`: role `mutation-tester`; registry `w2/swarm-registry.json:447-456`: key `KillT04`, kind `spawn`, agentId `TameshiR21.KillT04`, role `mutation-tester`, same axes | `original-outcomes-final.json:1075-1081`: same name, ID, role; status `completed`; report `.ufo/waves/round-21/w2/KillT04.md`; `replaced:false` | File exists. It says “genuinely discriminated” and records the frozen command exit 0, pristine 30/30, mutant 29/30, and restored 30/30 (`w2/KillT04.md:1-10,27-39`). | Identity/role match; declared outcome status is completed. Report claims completed execution; it is not the status authority. |
| `KillT12` | `spec2.json:409-416`: role `mutation-tester`; registry `w2/swarm-registry.json:457-466`: key `KillT12`, kind `spawn`, agentId `TameshiR21.KillT12`, role `mutation-tester`, same axes | `original-outcomes-final.json:1083-1089`: same name, ID, role; status `completed`; report `.ufo/waves/round-21/w2/KillT12.md`; `replaced:false` | File exists. It says “genuinely discriminated” and records the frozen command, pristine 30/30, mutant 29/30, and restored 30/30 (`w2/KillT12.md:1-8,31-38`). | Identity/role match; declared outcome status is completed. Report claims completed execution; it is not the status authority. |

The registry records membership, not terminal status; its three entries contain no `status` field. Status above is therefore taken from the designated outcome source, not inferred from registry membership or report contents. The frozen spec also assigns all three seats the same role and axes. The source’s wave-2 header declares 75 seats, 38 completed and 37 dead (`original-outcomes-final.json:635-639`); this audit does not independently recount the full wave.

## Callback evidence boundary and contradiction check

The three final-outcome rows contain the normalized fields shown above but no `actual_result`/raw `<task-result>` payload. The archived agent histories contain final assistant report text, not a separately retained callback envelope in these outcome rows. Thus the observed status is **declared completed**, not independently authenticated provider telemetry. This is a provenance limit, not a contradiction between the supplied outcome source and the reports.

`dispatch2-attempt-01.json:791-796,808-813,825-830` records these IDs as `pending` in the dispatch snapshot. That is an earlier dispatch state, not a competing terminal outcome; the later normalized outcome rows say `completed`. It does not show a membership mismatch. All three final rows say `replaced:false`.

## Bounded gate recommendation

For these identities, require exactly one outcome row per expected registry seat; bind the seat name to its exact registry key and `agentId`, require the row’s `id` and `role` to match the registry/spec, accept only the declared status enum, and count completion only when that exact outcome row says `completed` (with `replaced:false`). Never promote a missing, failed, or unknown-status row because its report exists or describes successful work. Recompute wave totals from the complete seat/outcome population; do not extrapolate this three-row check to the full 75-seat count. Preserve and validate the persisted input digests, while stating—as the contract does—that declared callbacks are not authenticated provider telemetry.

The three report files are consistent supporting documents for the recorded `completed` rows; their existence or prose alone would not satisfy the accounting assertion. No production changes, checks, or installs were made.
