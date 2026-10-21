done — KillMB10, KillMB11, KillMB12: callback, registry, outcome row and report all agree on **completed / mutation-tester / replaced=false**. No contradiction for these three identities. One in-repo provenance gap (below) bounds what the round-22 gate can claim.

# Scoped population

Exactly three frozen wave2 identities; nothing else was audited or relitigated:

- `KillMB10` → `TameshiR21.KillMB10`
- `KillMB11` → `TameshiR21.KillMB11`
- `KillMB12` → `TameshiR21.KillMB12`

Axis: calibration (distinguish completed callback from report existence). Read-only; my only write is this report. No tools installed or updated. No build, lint, format or test run.

# Inputs (SHA-256 observed now)

| Path (repo-relative unless absolute) | SHA-256 |
|---|---|
| `.ufo/waves/round-21/original-outcomes-final.json` | `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` (equals `.ufo/evidence/round-22/derivation.json` pin) |
| `.ufo/waves/round-21/w2/swarm-registry.json` | `029acd0ed3c2d4a8f0fbdce2958667788e0f8bab212fa3f7b58239ea581f917f` (equals derivation pin) |
| `.ufo/waves/round-21/spec2.json` | `e07159109d91a2fea95a2722a45142a06f41e2e3225e25dbcc05eb375720f6b3` |
| `.ufo/waves/round-21/assignments2.json` | `a514a99b3c4cc2ce9c9c73ab3c32393af43f7abf573440d6c3c18d93053a3bad` |
| `.ufo/waves/round-21/record2.json` | `0893967687ac2a9b331cd50b953f97a56b81c334a228e3bca445c3e82127eb59` |
| `.ufo/waves/round-21/w2/KillMB10.md` | `ee81ed061a954efee636019ca131b7cfc57091d7c42f2e6cf1845272ffec5bb7` |
| `.ufo/waves/round-21/w2/KillMB11.md` | `3f5b05487a8a9773db63a16ffe30a494de719b3707ed241271bb303523d76d5b` |
| `.ufo/waves/round-21/w2/KillMB12.md` | `d038bd454853ae587bff80aeefb7b95bec08c201bb7aea4daf93ec18ef3d006f` |
| Parent L1 transcript `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-baa6-76c9-b209-ce1123c6cc22/TameshiR21.jsonl` | outside repo, live file; per-line hashes below |

# Per-identity agreement

Callback = the `async-result` `custom_message` delivered to the parent `TameshiR21.jsonl`: a job record (`jobId`, `status`, `agentId`) plus a `<task-result … status=…>` header. Line numbers are 1-based.

| Identity | spec2 / assignments2 / record2 / w2 registry | Outcome row (`original-outcomes-final.json`) | Original callback | Seat transcript terminal state | Report |
|---|---|---|---|---|---|
| `TameshiR21.KillMB10` | `spec2.json:319` name/role `mutation-tester`; `assignments2.json:40`; registry `members.KillMB10.agentId` at `w2/swarm-registry.json:357-366`, role `mutation-tester` | `:1003-1009` `status: completed`, `report: .ufo/waves/round-21/w2/KillMB10.md`, `replaced: false` | parent line 707, 2026-10-21T12:34:11.815Z: job `{jobId/agentId TameshiR21.KillMB10, status completed, durationMs 232380}`; `<task-result id="TameshiR21.KillMB10" agent="mutation-tester" status="completed" duration="3m52s">`; line SHA-256 `75a30f026c5788dbc9a663e70a588751fef46d8d21dc62829b70024959b465a2` | `TameshiR21/TameshiR21.KillMB10.jsonl` (SHA-256 `f74813b2…0922`): model `openai-codex/gpt-6.1-sol`; final assistant `done — MB10 genuinely discriminated` at 12:33:35Z; `session_exit kind=normal` | write tool result 12:33:21Z, 9171 bytes, equals on-disk size. Text claims completed execution (exact frozen command exit 0, `KILLED`, replay 0/1/0) |
| `TameshiR21.KillMB11` | `spec2.json:328`; `assignments2.json:41`; registry `:367-376` | `:1011-1017` completed, `KillMB11.md`, `replaced: false` | parent line 694, 12:32:45.097Z: job `{TameshiR21.KillMB11, completed, durationMs 165474}`; `<task-result … status="completed" duration="2m45s">`; SHA-256 `53ed780f8157ba35bfa3b881c18eb36944d67410daf8dcd6219bd7e746b685fb` | `TameshiR21.KillMB11.jsonl` (`2cc0bbae…5289`): same model; final `done — MB11 genuinely discriminated; KILLED` at 12:32:28Z; normal exit | write 12:32:20Z, 8775 bytes = disk. Completed-execution text (exit 0, `KILLED`, 51/51→50/51→51/51) |
| `TameshiR21.KillMB12` | `spec2.json:337`; `assignments2.json:42`; registry `:377-386` | `:1019-1025` completed, `KillMB12.md`, `replaced: false` | parent line 703, 12:33:14.168Z: job `{TameshiR21.KillMB12, completed, durationMs 197019}`; `<task-result … status="completed" duration="3m17s">`; SHA-256 `dca8b9634ce046899e069ef78ac856fa8360d66a91ede40d1779a7cdfe8e9fda` | `TameshiR21.KillMB12.jsonl` (`26ca8b4e…d834`): same model; final `done — MB12 genuinely discriminated (KILLED)` at 12:32:59Z; normal exit | write 8856 bytes = disk. Completed-execution text (exit 0, `KILLED`, replay 0/1/0) |

For all three, the report was written before the final assistant message, and that message came before the parent callback. Callback `status="completed"` is therefore primary, and the report is a by-product of a completed seat, not the source of its status. None of the three is a partial report of a dead seat. Transcripts record no `stopReason` of `error` or `aborted`.

The non-terminal snapshot `dispatch2-attempt-01.json:654-700` shows `status: "pending"` for indices 38-40. That is the dispatch-time state, not a contradiction. `run2.json` `registry.members.KillMB1x.agentId` is `null` (pre-spawn plan); the post-spawn `w2/swarm-registry.json` and `record2.json` carry the exact ids.

# Contradictions and gaps

1. **No contradiction** among callback, registry identity, role, outcome status, `replaced`, and report for the three identities. They appear identically in `original-outcomes2.json`, `original-outcomes2-corrected.json` and `-final.json`. The 40→38 correction changed only `ProfileBashTsukuroiCensus` and `V01WitnessTests` (completed→failed); the corrected→final diff changed only `Section0827.last_error/provider`. Neither touches this scope.
2. **In-repo provenance gap (calibration).** The registry has no status field (`ufo-swarm-registry-v1` members carry only kind/agentId/role/item/axes). The status therefore comes only from the outcome row. 19 of 38 wave2 `completed` rows in `original-outcomes-final.json` carry **no** `actual_result` or `resolved_model`, unlike the other 19: `Section1925, Section1938, Section1964, KillMB03…KillMB12, KillD02, KillD11, KillD12, KillR02, KillR05, KillR07, KillT04, KillT12, F10RegistryLean`. KillMB10-12 are among them. No round-21 `wait2-recovered-*.json` mentions them. Their `completed` status is corroborated **only** by the off-repo parent transcript lines above. Inside the repo, it is indistinguishable from the file-presence inference that `original-outcomes2-corrected.json` says it `supersedes`. `.ufo/evidence/round-22/derivation.json` freezes this status as a declared input, and the contract bound says "retained callbacks are declared inputs, not authenticated provider telemetry". So this is bounded, not a defect. The other 16 bare rows were not audited here: [INFERENCE] they likely share the same off-repo provenance.

# Gate recommendation (one, bounded)

For these three identities the accounting gate must assert, from declared inputs only:

> exactly one wave2 outcome row per `name` ∈ {KillMB10, KillMB11, KillMB12}; `id` == `w2/swarm-registry.json members[name].agentId`; `role` == registry role == `mutation-tester`; `status` == `completed` (in the closed enum); `replaced` is literal `false`; each row is counted in wave2 `completed: 38` / total `completed: 66`; and the count would be unchanged if every `report` field and report file were deleted (status never derived from report presence).

Narrow-scope move that improves calibration without harming the other axes: the gate output should label these rows `status_source: declared` and must not claim callback-verified, because no callback text is retained in the repo for 19 completed wave2 rows. Do not add a rejection predicate for missing `actual_result`. That would falsely fail three seats whose original callbacks are `completed`, and it would require altering frozen evidence. If L1 later wants corroboration, a new append-only sidecar mapping id → parent transcript path, line, and line SHA-256 (values above) would let a future gate check it. That sidecar would still not be provenance authentication.

Report: .ufo/waves/round-22/w1/Audit40.md
