# Audit48 — frozen wave2 callback accounting

## Scope and axes

Calibration, exact identity/role binding, and preservation of frozen accounting authority. Population is exactly three wave2 seats: F03KnowledgeGate / TameshiR21.F03KnowledgeGate; F04FrontierPopulation / TameshiR21.F04FrontierPopulation; F05Source079 / TameshiR21.F05Source079. No other seats or round21 admission claims are assessed.

All paths below are relative to `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

## Evidence

- `.ufo/evidence/round-22/contract.json:1-22`: C1 is callback-authoritative seat accounting, not report-file success; retained callbacks are declared inputs, not authenticated provider telemetry. Relevant rejection predicates include failed-with-report-counted-completed, registry-id-mismatch, replacement-seat, and snapshot-tampering.
- `.ufo/waves/round-21/original-outcomes-final.json:1204-1237`: exact retained outcome rows and F05 completion payload.
- `.ufo/waves/round-21/w2/swarm-registry.json:575-601`: exact spawned membership, agent IDs, roles and calibration axes. These registry members have no status field; registry membership alone cannot establish completion.
- `.ufo/waves/round-21/spec2.json:514-537`: exact names, roles, calibration axes, and assignment prompts.
- `.ufo/waves/round-21/w2/F05Source079.md:1-23`: retained report, including `# Verdict: done`, findings, reported commands, and remaining historical-page-byte limitation.
- Report discovery: read the wave2 directory and globbed the project recursively (hidden and ignored paths included) for each exact F03KnowledgeGate, F04FrontierPopulation, and F05Source079 filename fragment. Only `.ufo/waves/round-21/w2/F05Source079.md` matched. No report path was invented for the failed seats. This is filename-based discovery, not proof that no differently named artifact exists.

## Per-seat findings

| Frozen wave2 seat | Callback declaration | Registry/spec agreement | Retained report and execution claim | Accounting finding |
| --- | --- | --- | --- | --- |
| F03KnowledgeGate / TameshiR21.F03KnowledgeGate | `role=reviewer`, `status=failed`, `report=null`, `actual_result=null`, `replaced=false`; last_error: `Original failure retained in delivered callback; not replaced.` (outcomes 1204-1215) | Registry 575-583 binds this exact name to this exact agent ID, `kind=spawn`, reviewer, calibration. Spec 514-521 matches name/role/axis and requests an advisory admission attack on hermetic-env-differential provenance and bounded invariants. | No matching report discovered; outcome declares none. Consequently no report completion claim was available to inspect. Null actual_result is not a completed callback. | Failed/dead seat, not completed. No identity/role contradiction observed. The error is a retained summary, not independently authenticated provider telemetry. |
| F04FrontierPopulation / TameshiR21.F04FrontierPopulation | `role=reviewer`, `status=failed`, `report=null`, `actual_result=null`, `replaced=false`; same retained failure summary (outcomes 1216-1227) | Registry 584-592 binds the exact name and agent ID, `kind=spawn`, reviewer, calibration. Spec 522-529 matches and requests an attack on F5-to-Core population wording and frozen denominator boundaries. | No matching report discovered; outcome declares none. No report completion claim available. | Failed/dead seat, not completed. No identity/role contradiction observed; no basis for inferring successful execution. |
| F05Source079 / TameshiR21.F05Source079 | `role=scout`, `status=completed`, `report=.ufo/waves/round-21/w2/F05Source079.md`, `replaced=false` (outcomes 1228-1237). Embedded task-result repeats the exact agent ID, `agent=scout`, `status=completed`, and says the report was written. | Registry 593-601 binds the exact name and agent ID, `kind=spawn`, scout, calibration. Spec 530-537 matches and assigns reopening S079, scoped A-tier/used-by checks, and immutable old-source-row comparison. | Report exists. Line 1 explicitly says `Verdict: done`; lines 5-18 claim the assigned source/quote, tier scope, linkage, and old-row comparison work was performed. Lines 21-23 retain uncertainty about the live page's exact historical bytes. These are retained execution claims, not checks rerun by this audit. | Completed declaration agrees with registry/spec identity/role and report text. Historical-page-byte uncertainty limits its substantive finding, not the callback status. Completion is supported by the retained outcome, not inferred from report existence. |

Scoped totals directly from these three rows: 3 seats, 1 completed declaration, 2 failed/dead declarations, 0 replaced declarations. No partial report was discovered for these three seats; this population does not itself demonstrate a failed-with-partial-report instance. Do not manufacture that contradiction or import one from another seat.

## One bounded gate recommendation

For these exact frozen wave2 members, assert a one-to-one `(wave, name, agent ID, role)` binding across spec/registry/outcome; require `replaced=false`; and count completion only from the declared outcome's exact `status=completed`. Require the scoped result to remain **1 completed and 2 failed/dead**, with the two failed identities fixed as above. Reject any accounting that rehabilitates either failed seat from an artifact's existence or a report's `done` prose; such an artifact would be partial/advisory evidence, not a status transition. Conversely, do not demote the F05 completed declaration merely because its report states a bounded substantive uncertainty. Persisted input digest validation can prevent snapshot substitution but cannot authenticate callback provenance.

## Preserved contract, contradictions, and tradeoff

No observed identity/role/status-versus-report contradiction in this scoped population. Registry/spec do not declare runtime status, so their agreement is membership/role agreement only. The authority distinction above removes report-as-status reasoning, not historical evidence. No deletion or production edit is proposed; the next broader move would leave the assigned three-seat scope. Existing round21 admission is untouched.

Read-only investigation except this new report. No builds, tests, linters, formatters, data-count commands, runtime invocation, installs, git/jj/index/ref mutations, or existing-evidence edits were performed. No shared-tree byte-identity verification was run; none is claimed. No semantic-caller deletion claim is made, so LSP references are not applicable. Tool installations: none.
