# Audit51 — wave2 V01–V03 callback/report calibration

## Scope and axes

Exact scoped population: three original wave2 seats, `TameshiR21.V01WitnessTests`, `TameshiR21.V02DispositionTests`, and `TameshiR21.V03RegistryTests`. Axes: calibration (callback-authoritative accounting), identity fidelity (spec/registry/outcome binding), and provenance preservation (retain reports without promoting their seats). This is an advisory read-only audit, not admission, a replacement, or a reassessment of round21's admitted claims.

## Evidence

All paths below are relative to the tameshi-shokunin project root.

- `.ufo/evidence/round-22/contract.json:1–21`: frozen base `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`; C1 is callback-authoritative accounting rather than report-file success. Bounds explicitly distinguish declared callback inputs from authenticated provider telemetry.
- `.ufo/waves/round-21/original-outcomes-final.json:1296–1331`: exact scoped retained outcome rows.
- `.ufo/waves/round-21/w2/swarm-registry.json:1–7,656–685`: report directory, original member names, exact agent IDs, reviewer roles, spawn membership and axes. Registry has no per-member callback status field; its top-level `wave` is null, so wave2 is established by the supplied w2 registry path and wave2 outcome membership, not that field.
- `.ufo/waves/round-21/spec2.json:586–612`: all three named seats are reviewers, with axes `operability` and `calibration`; prompts request surgical read-only correctness/safety review of the respective witness, disposition, and registry selftest deltas.
- `.ufo/waves/round-21/w2/V01WitnessTests.md:1–58`: discovered retained report. Lines 3 and 7–19 explicitly claim completion and execution; lines 55–58 state residual gaps/tooling.
- Report discovery using `.ufo/waves/round-21/**/V0[123]*` returned only `w2/V01WitnessTests.md`. This establishes no V02/V03 named report discovered under that pattern in round21; it does not prove that arbitrarily renamed or externally stored reports cannot exist.

## Per-identity findings

| Original wave2 identity | Retained callback/outcome | Registry/spec agreement | Existing report and completion claim | Calibration result |
| --- | --- | --- | --- | --- |
| `V01WitnessTests` / `TameshiR21.V01WitnessTests` | `role=reviewer`, `status=failed`, `replaced=false`, `actual_result=null`, `last_error=""`; report pointer is `.ufo/waves/round-21/w2/V01WitnessTests.md` (outcomes 1296–1307). | Exact name, agent ID and reviewer role agree with registry 656–665; spec 586–594 agrees on name/role/axes and witness-review target. Registry supplies membership, not a completed status. | Report exists. Line 3 says `Verdict: **done** — review complete`; line 11 claims selftest exit 0 / 51 of 51 pass, and lines 12–19 claim mutant probes and guard checks. These are retained report assertions, not checks exercised by this audit. | Explicit tension between self-described completed review and failed retained callback. Preserve the report as a report artifact from a failed seat; do not relabel its text as unfinished, but do not count a completed callback or infer provider success. Empty error text does not overturn `failed`. |
| `V02DispositionTests` / `TameshiR21.V02DispositionTests` | `role=reviewer`, `status=failed`, `replaced=false`, `actual_result=null`, `report=null`; error says `Original failure retained in delivered callback; not replaced.` (outcomes 1308–1319). | Exact name, agent ID and reviewer role agree with registry 666–675; spec 595–603 agrees on name/role/axes and disposition-review target. No registry callback status to compare. | No report pointer; no named report discovered within the scoped round21 search. No report text available to assess execution/completion claims. | No observed contradiction in membership, role or declared status. Missing report is not proof no work occurred; retained callback nevertheless remains failed. |
| `V03RegistryTests` / `TameshiR21.V03RegistryTests` | `role=reviewer`, `status=failed`, `replaced=false`, `actual_result=null`, `report=null`; error says `Original failure retained in delivered callback; not replaced.` (outcomes 1320–1331). | Exact name, agent ID and reviewer role agree with registry 676–685; spec 604–612 agrees on name/role/axes and registry-review target. No registry callback status to compare. | No report pointer; no named report discovered within the scoped round21 search. No report text available to assess execution/completion claims. | No observed contradiction in membership, role or declared status. Neither assignment nor registry membership is evidence of successful execution; retained callback remains failed. |

Scoped accounting contribution from the three displayed rows: three original seats, zero completed callbacks, three failed/dead seats, zero replacements, one retained report pointer whose file was observed, two null report pointers. These are scoped row observations, not a recomputation of global wave totals.

## One bounded gate recommendation

For these exact three wave2 registry-bound tuples `(name, agentId, role)`, require exactly one retained outcome each, with exact `status=failed` and `replaced=false`, contributing **0 completed / 3 dead** regardless of report presence or report prose. In particular, reject any accounting input that promotes V01 to completed because its report exists or says `done`; retain that report without rewriting it. Null report pointers for V02/V03 must not manufacture either reports or successful callbacks. Apply the contract's persisted-input digest binding so changing the input row to `completed` is not silently accepted as the same frozen observation. This is a single callback-authority invariant over the named population, not a recommendation to authenticate provider provenance through report contents.

## Preserved contract, deletion candidate, and tradeoff

No deletions made. Bounded conceptual deletion candidate: remove any report-existence or report-`done` fallback from completion accounting, if one is present; this audit did not inspect implementation or establish semantic callers, so this is not a proven code-deletion candidate. The sole production integrator owns any implementation change.

Preserve both facts: V01's artifact claims a finished review, while its retained callback is failed. Treating the artifact as partial/unadmitted callback evidence does not establish that its underlying review work was partial. The tradeoff is intentionally withholding completed-seat credit despite possibly substantive work; provenance and the report remain intact. Stop before deleting report history or substituting provider-success inference for the declared callback status.

## Execution limits

Only this new report was written. No production edits, existing-evidence edits, git/jj/index/ref operations, subagents, runtime invocations, installs, builds, tests, lint, formatting, or data-count commands were performed. No narrow behavioral check was run and no implementation improvement is claimed. Reads establish the persisted declarations and observed artifact text, not authenticated callback provenance or revalidated report execution. Shared-tree byte identity was not independently measured; no claim is made about concurrent changes by others. Tool installations/updates: none.
