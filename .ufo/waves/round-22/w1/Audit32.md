# Audit32 — wave2 Section1479 / Section1499 seat accounting (read-only)

Verdict: Both seats are **provider-dead with no report**. All retained artifacts agree on identity, role and failed status. No artifact contradicts this. No partial report exists that could rehabilitate either seat. The only uncertainty is provenance: no raw terminal callback for either seat is retained in the repo.

Scoped population: exactly 2 identities, `TameshiR21.Section1479` and `TameshiR21.Section1499` (round-21 wave2). Nothing else is audited. Other seats appear below only as a contrast case.

Tools installed: none.

## Inputs (sha256 at read time; paths relative to the repo)

| path | sha256 |
|---|---|
| `.ufo/waves/round-21/original-outcomes-final.json` | `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` |
| `.ufo/waves/round-21/w2/swarm-registry.json` | `029acd0ed3c2d4a8f0fbdce2958667788e0f8bab212fa3f7b58239ea581f917f` |
| `.ufo/waves/round-21/spec2.json` | `e07159109d91a2fea95a2722a45142a06f41e2e3225e25dbcc05eb375720f6b3` |
| `.ufo/waves/round-21/record2.json` | `0893967687ac2a9b331cd50b953f97a56b81c334a228e3bca445c3e82127eb59` |
| `.ufo/waves/round-21/dispatch2-attempt-01.json` | `3c50b0fa50e67d5d6a1e626982963b4b7b129b72f83731360934abd90122fc40` |

Also read: `assignments2.json` (lines 18–19), `run2.json` (lines 170–187, 828–835), `run2.err` (0 bytes), `original-outcomes2.json` and `original-outcomes2-corrected.json` (lines 170–189), `wait2-recovered-01..22.json`, and `.ufo/evidence/round-22/{contract.json,bundle.json}`.

## Per-identity rows

| identity | outcome row (final) | registry `w2` member | spec2 / record2 / assignments2 | retained callback | report on disk | agreement |
|---|---|---|---|---|---|---|
| `TameshiR21.Section1479` | lines 803–811: role `critic`, status `failed`, `report: null`, `replaced: false`, provider `codex`, `last_error` "Retry budget exhausted after 5 retries … Codex is at capacity … (code=turn_rate_limit_exceeded)" | lines 152–160: agentId `TameshiR21.Section1479`, role `critic`, axes `[calibration]`, no status field | spec2 lines 136–141: role `critic`. record2 lines 153–160: same agentId and role. assignments2 line 18 maps the name to this id | **none**: absent from all 22 `wait2-recovered-*.json`. dispatch2-attempt-01 lines 280–296: status `pending`, toolCount 0, tokens 0, durationMs 0 | **none**: `w2/Section1479.md` and `w2/sections/1479.json` are both absent (`ls -R w2` has no `14[79]9` entry). Not in bundle wave2 `reports[]` (lines 1809–1850) | Identity, role and status agree. Callback provenance is uncertain |
| `TameshiR21.Section1499` | lines 813–821: same fields as Section1479 | lines 161–169: agentId `TameshiR21.Section1499`, role `critic`, no status field | spec2 lines 144–149. record2 lines 162–169. assignments2 line 19 | **none** in the recovered callbacks. dispatch2-attempt-01 lines 298–307: status `pending`, zero activity | **none**: `w2/Section1499.md` and `w2/sections/1499.json` are absent. Not in bundle `reports[]` | Same as Section1479 |

Observations:

- **Status.** `failed` appears unchanged in `original-outcomes2.json`, `original-outcomes2-corrected.json`, `original-outcomes-final.json`, and the round-22 bundle (lines 1396–1407). It is in the gate's status enum, and `replaced=false` holds everywhere.
- **Report claims.** No report exists, so no text claims completed execution. These are not partial-report cases.
- **Totals.** Wave2 totals are seats 75, completed 38, dead 37 (outcomes-final lines 635–638; bundle `claimed` lines 899–902). Both seats belong in `dead`.

## Contradictions and uncertainty (stated, not smoothed)

1. **Where `failed` comes from cannot be traced to a raw callback.** The exact `last_error` string appears only in derived files (`original-outcomes*.json`). The recovered callbacks record 16 completed and 8 failed seats, and neither target seat is among them. The only raw dispatch record is `pending` with zero activity, taken before execution. So `failed` is a declared input that I cannot authenticate. This matches contract bound 1: "retained callbacks are declared inputs, not authenticated provider telemetry".
2. **The registry cannot supply status.** `w2/swarm-registry.json` has no `status` field for any member. A gate check described as "exact registry identities/status enum" therefore gets identity and role from the registry and status from the outcome row. If that division is not explicit, it is ambiguous.
3. **Outcome rows are not uniform.** The target rows have `provider` and `last_error`, but no `resolved_model` or `actual_result`. Other rows, such as V01WitnessTests at outcomes-final 1297–1305, have `resolved_model`, `actual_result: null` and `last_error: ""`. A strict per-row schema check would treat these two shapes differently.
4. **Contrast case (outside my scope, pointer only).** `V01WitnessTests` and `ProfileBashTsukuroiCensus` are `failed` in their recovered callbacks and in outcomes-final, yet each has a non-null `report` path and appears in bundle `reports[]`. These are the real "failed-with-report" cases. My two seats are the opposite case: dead with no report.
5. **`run2.json` agentId is null.** In `members` (lines 170–187), `agentId` is `null` for both seats, while record2 and the registry hold the real id. I read run2 as a pre-spawn plan, so it must not be used for identity matching. `[INFERENCE]`

## Bounded gate recommendation

For each of these two identities, the accounting gate should check all of the following:

- **Outcome row:** exactly one row whose `id` equals `w2/swarm-registry.json` `members[name].agentId`, whose `role` equals `critic`, whose `status` is `failed`, and whose `replaced` is `false`.
- **Count:** the identity is counted in wave2 `dead` (37) and not in `completed` (38).
- **Report independence:** report presence must never feed status or the completed count. If a file later appears at `w2/Section1479.md` or `w2/Section1499.md` (or the `sections/*.json` paths), the row stays `failed` and the totals do not change. That is the `failed-with-report-counted-completed` predicate.
- **Status source:** status comes only from the outcome row, because the registry has none.
- **Provenance claim:** the gate should not claim the callback is authentic. It can only check consistency with the persisted digests listed above.
