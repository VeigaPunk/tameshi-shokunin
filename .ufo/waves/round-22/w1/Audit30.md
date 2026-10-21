# Audit30 — wave2 Section1155 / Section1246 / Section1272 callback vs registry vs report

Scoped population: exactly three round-21 wave2 identities — `TameshiR21.Section1155`, `TameshiR21.Section1246`, `TameshiR21.Section1272`. Read-only; nothing else judged. No tools installed.

## Inputs (sha256 at read time)

| File | sha256 |
|---|---|
| `.ufo/waves/round-21/original-outcomes-final.json` | `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` |
| `.ufo/waves/round-21/w2/swarm-registry.json` | `029acd0ed3c2d4a8f0fbdce2958667788e0f8bab212fa3f7b58239ea581f917f` |
| `.ufo/waves/round-21/spec2.json` | `e07159109d91a2fea95a2722a45142a06f41e2e3225e25dbcc05eb375720f6b3` |
| `.ufo/waves/round-21/w2/Section1155.md` | `ea60c13998286a441515c209e8600c0c98e3a00ea44c300126efeb9306e1f638` |
| `.ufo/waves/round-21/w2/sections/1155.json` | `867b8244441782959bec40cd333b12af2e6c1716c5e314c9951d703c1ca96162` |

Also read: `assignments2.json`, `record2.json`, `run2.json`, `dispatch2-attempt-01.json`, `original-outcomes2.json`, `original-outcomes2-corrected.json`, `wait2-recovered-01..22.json`, `.ufo/evidence/round-22/contract.json`.

## Per-identity rows

| Identity | Spec2 role | Registry `agentId` / role | Outcome-final row | Retained callback | Report on disk | Agreement |
|---|---|---|---|---|---|---|
| `TameshiR21.Section1155` | reviewer | `TameshiR21.Section1155` / reviewer | `status: completed`, `report: .ufo/waves/round-21/w2/Section1155.md`, `replaced: false`, model `openai-codex/gpt-6-luna:max` | `wait2-recovered-01.json` job `status: completed`, `durationMs: 441059` (= 7m21s); `resultText` `<task-result id="TameshiR21.Section1155" agent="reviewer" status="completed" duration="7m21s">` — identical to row `actual_result` | `w2/Section1155.md` (mtime 12:36:53Z) + `w2/sections/1155.json` (12:36:28Z); callback widget `updatedAt` 1792586214501 = 12:36:54Z | **Agree.** Callback id/agent/status match row and registry; report is a finished verdict (`no-blocking-gaps`, `blocking_gaps: 0`, `wrong_expectations: 0`), not a partial; report timing precedes callback by ~1 s. |
| `TameshiR21.Section1246` | critic | `TameshiR21.Section1246` / critic | `status: failed`, `report: null`, `replaced: false`, `provider: codex`, `last_error: "Retry budget exhausted after 5 retries: … (code=turn_rate_limit_exceeded)"` | **None retained.** Absent from all 22 `wait2-recovered-*.json` (not even as `running`); `dispatch2-attempt-01.json` shows only `status: pending`; `run2.json` member `agentId: null` | None. No `w2/Section1246.md`, no `w2/sections/1246.json` anywhere under `.ufo` | **Identity/role agree; status uncorroborated.** `failed` is asserted only by the outcome rows themselves (same in `original-outcomes2`, `-corrected`, `-final`). No report exists, so no rehabilitation risk. |
| `TameshiR21.Section1272` | critic | `TameshiR21.Section1272` / critic | same shape as 1246: `failed`, `report: null`, `replaced: false`, `provider: codex`, same `last_error` | **None retained** (same absences as 1246) | None. No `w2/Section1272.md`, no `w2/sections/1272.json` | **Identity/role agree; status uncorroborated** in the same way as 1246. |

Registry members carry no status field (`ufo-swarm-registry-v1`: `kind/agentId/role/item/axes` only), so status can only come from the outcome rows and callbacks, never from the registry.

## Contradictions and uncertainty

- **No contradiction** among spec2, registry, assignments2, record2, and the three outcome files for these identities. All three rows are byte-equivalent across `original-outcomes2.json`, `-corrected.json`, and `-final.json`. The 40→38 completed correction (`ProfileBashTsukuroiCensus`, `V01WitnessTests`) did not touch these seats.
- **Provenance gap (1246, 1272):** the `failed` status and `last_error` exist only in the hand-assembled outcome files. No raw failed callback is retained in round-21. This fits the contract bound that "retained callbacks are declared inputs, not authenticated provider telemetry". For these two seats the declared input is the outcome row itself.
- **1155:** its success is backed by the report file and by an independently retained completed callback whose `id` and `status` attributes match the row. Report existence alone was not used as evidence.
- Section1155's `read_rev` (`790abd21…`) is the round-21 read revision. It is not relitigated here, per the scope.

## Gate recommendation (bounded)

For each wave2 row, the accounting gate should assert:

1. The spec2 `name`/`role` and the registry `members[name].agentId`/`role` exactly equal the row's `name`/`id`/`role`. All three pass.
2. `status` ∈ {`completed`, `failed`}, and `replaced == false`. All three pass.
3. A row counts as **completed only if** `status == "completed"` **and** its retained `actual_result` opens with `<task-result id="<row.id>" … status="completed"`. Otherwise it counts as dead. The `report` field and file existence must never enter the predicate.

Under this rule, Section1155 is completed (it passes the callback-header match), while Section1246 and Section1272 are dead without needing any failure callback, because they have no completed callback. That makes the provenance gap above harmless for these seats. The rule maps onto the contract predicates `false-completion-count`, `failed-with-report-counted-completed`, and `registry-id-mismatch`.

The gate cannot authenticate the callback text itself. A tampered row that copies in a `completed` header would still pass. Only the persisted input digest (`snapshot-tampering`) bounds that case, and the gate's report should say so rather than imply provenance.
