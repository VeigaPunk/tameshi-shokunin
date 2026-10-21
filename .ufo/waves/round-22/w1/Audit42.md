# Audit42 — wave2 KillR02 / KillR05 seat-accounting audit (round-22 C1 calibration)

Auditor: TameshiR22.Audit42-2 (leaf, read-only). Base `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`.
No tools installed or updated; no checks, builds, or mutations were run mid-flight. Read-only observation only.

## Scoped population (exact)

Exactly two frozen identities, each present exactly once per artifact (no duplicates found):

1. wave2 `KillR02` — agent `TameshiR21.KillR02`
2. wave2 `KillR05` — agent `TameshiR21.KillR05`

## Per-identity agreement

| Identity | Outcome row (callback-authoritative) | Registry membership | Dispatch/spec | Report exists | Report claims completed execution | Agreement |
|---|---|---|---|---|---|---|
| `KillR02` / `TameshiR21.KillR02` | `.ufo/waves/round-21/original-outcomes-final.json:1050-1057` — wave2 row, role `mutation-tester`, status `completed`, report path recorded, `replaced: false`, no `resolved_model` field | `.ufo/waves/round-21/w2/swarm-registry.json:417-425` — kind `spawn`, `agentId: TameshiR21.KillR02`, role `mutation-tester`, item `null`, axes `[operability, calibration]`; registry carries no per-member status | `assignments2.json:46` name→id map matches; `dispatch2-attempt-01.json:757-767` index 44, id matches, agent `mutation-tester`, `modelRole: m_sol`, status `pending` at dispatch; `spec2.json:372-380` same name/role/axes with R02 target prompt | Yes: `.ufo/waves/round-21/w2/KillR02.md` (complete, verdict + trailer at line 133) | Yes: frozen command exit 0, R02 `KILLED`, receipts cited | AGREE (identity, role, status basis, report) |
| `KillR05` / `TameshiR21.KillR05` | same file `:1058-1065` — wave2 row, role `mutation-tester`, status `completed`, report path recorded, `replaced: false`, no `resolved_model` field | same registry `:427-434` — `agentId: TameshiR21.KillR05`, role `mutation-tester`, axes `[operability, calibration]` | `assignments2.json:47`; `dispatch2-attempt-01.json:774-784` index 45, id matches, `modelRole: m_sol`, `pending` at dispatch; `spec2.json:381-389` R05 target prompt | Yes: `.ufo/waves/round-21/w2/KillR05.md` (complete, verdict + trailer at line 106) | Yes: frozen command exit 0, R05 `KILLED`, receipts cited | AGREE (identity, role, status basis, report) |

Status `completed` is a known enum value in this outcomes file (its wave2 summary counts only `completed`/`dead`: 38 + 37 = 75). Neither identity appears in any `wait2-recovered-*.json` recovery listing (grep over `.ufo/waves/round-21/` returned no hits there), consistent with non-dead seats. All three outcome snapshots (`original-outcomes.json` n/a here, `original-outcomes2.json:417-432`, `original-outcomes2-corrected.json:418-433`, `original-outcomes-final.json:1050-1065`) carry identical rows for both identities — no drift.

## Report text vs retained receipts (both corroborate completed execution)

- `KillR02.md` claims receipts `mutations/R02.json`, `mutations/R02.stderr`, `mutations/R02.command.json` — all exist. `R02.json` matches the report claim-for-claim: pristine exit 0 / 8.666 s / `SELFTEST: PASS (51 cases)`; mutant exit 1 / 8.956 s / fail lines `timeout-zero`; `mutated_sha256 11536e43…37f5d`; tool sha `cc4ed8e2…d451e`; ruler `a0ec5547…e9396`; spec `670dd59b…3e85c`; `killed=1 survived=0 inconclusive=0 total=1`, rev `790abd2…bde65e`. `R02.command.json` records exit 0 / 18.29 s and even preserves the disclosed rejected first launch (`Background job limit reached (100)`).
- `KillR05.md` claims `mutations/R05.json`, `mutations/R05-command.json`, `mutations/R05.stderr`, `mutations/R05-restoration.json` — all exist. `R05.json` matches: mutant exit 1, fail line `baseline-child-preserved FAIL (baseline_rejected=False adopted_owned=True)`; `mutated_sha256 b7ffc9ea…01287`; same ruler/spec/tool hashes; `killed=1 survived=0 total=1`. `R05-command.json`: exit 0 / 17.65 s.
- Frozen spec agreement: `.ufo/evidence/round-21/c1-mutants.json` R02 entry (`0 < ts` → `0 <= ts` at the timeout guard) and R05 entry (`return (current, observed_starttime) not in baseline_children` → `return True`) match exactly what both reports describe attacking.

## Partial report vs completed callback

For these two identities the distinction resolves cleanly: both are **completed callbacks with complete reports**. Neither report is partial (both end in a verdict and their own trailer path), and neither seat's status rests on the report file: status comes from the persisted outcome rows, per the declared invariant `partial_report_files_do_not_rehabilitate_failed_jobs: true` (`original-outcomes-final.json:1369`). No `failed-with-report-counted-completed` case exists in this population.

## Contradictions / narrow observations (non-blocking)

1. Receipt naming/schema drift between the two seats: R02 uses dotted artifacts with richer command metadata (`R02.command.json` carries stream digests, `live_before_sha256`, `first_launch` note; restoration is `R02.restoration.json`), while R05 uses hyphenated artifacts (`R05-command.json` = argv+exit+seconds only; `R05-restoration.json`). Each report cites its own convention correctly; harmless but a schema-consistency candidate for future fixtures.
2. Neither outcome row persists a provider/`resolved_model` field (dispatch shows only `modelRole: m_sol`). Provider liveness therefore cannot be cross-checked from the outcome rows for these identities — this is schema absence, not evidence of provider death, and must not be read as either.
3. `w2/swarm-registry.json` has top-level `wave: null` and no per-member status; it is a membership record only. Status authority for these seats lives solely in `original-outcomes-final.json`.

## Bounded gate recommendation (one)

For `TameshiR21.KillR02` and `TameshiR21.KillR05` the accounting gate must assert exactly: an outcome row exists in `wave2.rows` whose `id` equals the w2-registry member `agentId` verbatim, whose `status` is in the `{completed, dead}` enum (here `completed`), with `replaced: false`, and whose recorded `report` path exists on disk — while **excluding report-file existence or content from the completion decision** (a report neither creates nor upgrades status). Corollary: because these rows carry no provider field, the gate must not require provider liveness to accept a `completed` callback row, and must treat a missing provider attribution as `unknown`, never as `dead`.

Report: `.ufo/waves/round-22/w1/Audit42.md`
