# Audit52 — three frozen wave2 failed identities

Axes: identity fidelity, callback-authoritative calibration, historical evidence preservation. Read-only audit; the only write is this new report. No production changes, deletions, tests, builds, installs, dispatch, git operations, or execution of audited tools.

## Exact population and evidence

Exactly three seats, all in wave2; no conclusions about other seats or the admitted round21 claims. Paths below are relative to the project root.

- **O:** `.ufo/waves/round-21/original-outcomes-final.json`, wave2.rows, lines 1332–1361.
- **R:** `.ufo/waves/round-21/w2/swarm-registry.json`, members, lines 686–715.
- **S:** `.ufo/waves/round-21/spec2.json`, items, lines 613–639.
- **D:** `.ufo/waves/round-21/dispatch2-attempt-01.json`, exact-id objects (around lines 1233–1284); dispatched task text provides the intended report paths. Its `pending` status is a dispatch-time snapshot, not a final callback.
- **C:** `.ufo/evidence/round-22/contract.json`, especially predicates `failed-with-report-counted-completed`, `registry-id-mismatch`, `replacement-seat`, and the declared-input/provenance bound.

| Frozen identity | Retained final callback O | Registry/spec agreement | Existing report and completion claim |
|---|---|---|---|
| wave2 `V04TraceTests`, agent `TameshiR21.V04TraceTests` | `role=reviewer`, `status=failed`, `report=null`, `replaced=false`, `provider=codex` (1332–1341) | R 686–695: same name/id/role, `kind=spawn`; S 613–621: same name/role, axes operability/calibration. Registry contains no final-status field. | D assigns `.ufo/waves/round-21/w2/V04TraceTests.md`; no matching report discovered. No report text exists to inspect or claim completed execution. |
| wave2 `V05EnvDiffSafety`, agent `TameshiR21.V05EnvDiffSafety` | `role=sentinel`, `status=failed`, `report=null`, `replaced=false`, `provider=codex` (1342–1351) | R 696–705: same name/id/role, `kind=spawn`; S 622–630: same name/role, axes operability/calibration. Registry contains no final-status field. | D assigns `.ufo/waves/round-21/w2/V05EnvDiffSafety.md`; no matching report discovered. No report text exists to inspect or claim completed execution. |
| wave2 `V06FacadeSafety`, agent `TameshiR21.V06FacadeSafety` | `role=sentinel`, `status=failed`, `report=null`, `replaced=false`, `provider=codex` (1352–1361) | R 706–715: same name/id/role, `kind=spawn`; S 631–639: same name/role, axes operability/calibration. Registry contains no final-status field. | D assigns `.ufo/waves/round-21/w2/V06FacadeSafety.md`; no matching report discovered. No report text exists to inspect or claim completed execution. |

All three final rows record: `Retry budget exhausted after 5 retries: Codex error event: Codex is at capacity, please try again later (code=turn_rate_limit_exceeded)`. This is retained callback data, not independently authenticated provider telemetry.

Report discovery used hidden-file-inclusive, gitignore-disabled filename globbing under round21, then project-wide exact identity filename patterns (`**/V04TraceTests*`, `**/V05EnvDiffSafety*`, `**/V06FacadeSafety*`); the latter returned no matches. Reading the complete immediate `w2` directory listing corroborated absence of the three assigned Markdown filenames. Intended paths were obtained from D, not invented or opened as assumed files. This establishes observed report absence at audit time, not a claim that no report ever existed anywhere.

## Agreement, uncertainty, and bounded recommendation

Observed scoped accounting is **3 seats, 0 completed, 3 failed/dead, 0 replaced**. Identity and role agree across final outcomes, registry, spec and dispatch. There is no observed contradiction. Dispatch-time `pending` and retained final `failed` describe different lifecycle moments; the registry/spec do not independently assert a terminal status. These three seats do not demonstrate a partial-report conflict: all have null report pointers and no discovered assigned report. A report's existence, if later supplied, would still not establish a completed callback.

**One gate recommendation:** bind each of these exact `(wave2, member name, agentId, role)` tuples one-to-one to its retained final row; require `status=failed` and `replaced=false`, and make its contribution to completed count zero regardless of report existence or report prose. Reject missing/duplicate/mismatched identities, status mutation, replacement, or accounting that counts any of these three as completed. Preserve the null report pointers in the frozen input. This is a scoped assertion over declared retained inputs, not an authentication of callback provenance or a remeasurement of global totals.

Preserved contract: historical round21 evidence and admission remain untouched; partial artifacts cannot rehabilitate failed seats. Deletions made/candidates: none—this assignment audits accounting, not semantic code reachability. No LSP deletion proof or runtime behavior improvement is claimed. Tradeoff: byte/digest and identity/status validation can reject altered accounting inputs but cannot prove provider-origin authenticity. No build/lint/test or data-count command was run, and no whole-tree byte-identity check is claimed; all tool operations before this report were reads/searches.
