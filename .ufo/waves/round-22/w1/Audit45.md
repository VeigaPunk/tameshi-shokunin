# Audit45 — wave2 ProfileBash* seat calibration (C1)

Scope: exactly three frozen wave2 identities, base `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`. Read-only audit; no production edits; no installs performed.
Outcome source: `.ufo/waves/round-21/original-outcomes-final.json` (summary lines 1–16; wave2 = 75 seats, 38 completed, 37 dead, flag `partial_report_files_do_not_rehabilitate_failed_jobs: true`).

## Per-identity rows

| Identity | Registry/spec membership | Outcome status (final) | Retained callback | Report file | Report claims completed execution | Verdict |
|---|---|---|---|---|---|---|
| ProfileBashTsukuroiCensus | Agrees | `failed` | **None** (`actual_result: null`, `last_error: ""`) | EXISTS `.ufo/waves/round-21/w2/ProfileBashTsukuroiCensus.md` | YES (lines 16–19: real driver run, exit 0, "All profiles completed with exit 0") | **Partial report ≠ completed callback.** Dead-seat with orphaned report + surface evidence; gate must count it failed. |
| ProfileBashMadoVerify | Agrees | `failed` | None; failure cause recorded (`turn_rate_limit_exceeded`, retry budget exhausted after 5) | DOES NOT EXIST (glob `round-21/**/ProfileBashMadoVerify*` empty; no `surfaces/bash-mado-verify.json`) | n/a — no report text exists | Clean dead seat: status, absent report, absent evidence all agree. |
| ProfileBashChecklistRun | Agrees | `completed` | YES: task-result `status="completed" duration="11m15s"` retained in `actual_result` | EXISTS `.ufo/waves/round-21/w2/ProfileBashChecklistRun.md` (trailer line 50) | YES, and corroborated by retained callback + `surfaces/bash-checklist-run.json` | Completed callback, report, and evidence agree. |

## Evidence chain (exact paths and locations)

- **ProfileBashTsukuroiCensus** — outcome row `original-outcomes-final.json:1122-1133`: id `TameshiR21.ProfileBashTsukuroiCensus`, role `reviewer`, `status: "failed"`, `report` non-null pointing at the report, `replaced: false`, `resolved_model: zai/glm-5.3-flash:max`, `provider: codex`, `actual_result: null`, `last_error: ""` (no cause recorded). Registry `round-21/w2/swarm-registry.json:497-505`: `kind: spawn`, agentId identical, role `reviewer`, axes `[coverage, freshness]`. Spec `round-21/spec2.json:444-451`: same name/role/axes. The report exists and narrates a fully executed independent run (its lines 16–19 state the command exited 0 and all seven profiles completed); matching surface JSON and clean stdout/stderr artifacts exist. Thus the report claims work completed, but the retained final outcome has no callback (`actual_result: null`) and status failed. The execution claim is not callback-authenticated; its actual occurrence remains uncertain.
- **ProfileBashMadoVerify** — outcome row `original-outcomes-final.json:1134-1143`: `status: "failed"`, `report: null`, `last_error` names the cause (Codex at capacity, `code=turn_rate_limit_exceeded`). Registry `w2/swarm-registry.json:507-515` and spec `spec2.json:453-461` agree on identity/role/axes. No report file anywhere under `round-21/` (targeted glob negative); `w2/surfaces/` contains no `bash-mado-verify.json`. Nothing exists that could rehabilitate the seat.
- **ProfileBashChecklistRun** — outcome row `original-outcomes-final.json:1144-1153`: `status: "completed"`, `replaced: false`, resolved_model `openai-codex/gpt-6-luna:max`, retained `actual_result` contains the completed task-result naming the report and evidence paths. Registry `w2/swarm-registry.json:517-525`, spec `spec2.json:462-470` agree. Report text and `surfaces/bash-checklist-run.json` both exist and agree with the retained task-result's claims.

## Contradictions / uncertainty

1. **TsukuroiCensus is the live instance of the round-22 predicate `failed-with-report-counted-completed`.** Provider final status is `failed` with no callback, yet a complete-looking report and surface JSON exist on disk. Whether the narrated execution actually occurred is **unresolvable from retained evidence** — the gate must not rehabilitate it on report existence, and equally must not delete or distrust the artifacts; it must simply keep the seat dead. Cause of the failed finalization is unrecorded (`last_error: ""`).
2. MadoVerify and ChecklistRun show no contradiction: absent-report/failed and report/callback/completed respectively.
3. All three: registry `agentId` == outcome `id`, roles identical across registry/spec/outcome, and all three outcome rows have `replaced: false` — no `registry-id-mismatch`, no `replacement-seat`, no `unknown-status` (each observed status is `completed` or `failed`).

## Bounded gate recommendation (one)

For these identities the accounting gate should count from the frozen outcome rows' exact identity and status fields, never from report path or text: assert TsukuroiCensus=`failed`, MadoVerify=`failed`, ChecklistRun=`completed`; assert the three registry IDs and roles agree with those rows/spec, all three `replaced: false`, and the persisted wave2 totals remain 38 completed / 37 dead of 75. In particular the existing TsukuroiCensus report and surface evidence must not change its `failed` row into completion. The retained ChecklistRun task-result says `completed` and agrees with its row/report; TsukuroiCensus has no retained callback in `actual_result`. These are persisted declared inputs only: the gate cannot authenticate callback provenance or infer execution from artifacts. This is the bounded assertion for the contract's `failed-with-report-counted-completed` and `false-completion-count` predicates; it does not adjudicate report prose.
