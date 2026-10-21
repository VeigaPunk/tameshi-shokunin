# Audit50 — three frozen wave2 seats

## Scope and axes

Population is exactly three original wave2 identities: `TameshiR21.F09LessonRestraint`, `TameshiR21.F10RegistryLean`, and `TameshiR21.F11ScopeOverlap`. Axes: exact identity/role binding, callback-status fidelity, report-versus-execution calibration, and append-only scope. This is an advisory read-only audit, not admission or authentication of provider callbacks. No earlier round21 claims were re-audited.

All evidence paths below are relative to the project root.

## Per-identity findings

| Frozen identity | Retained outcome | Registry/spec/membership agreement | Report evidence and completion claim | Accounting conclusion |
|---|---|---|---|---|
| wave2 `F09LessonRestraint`; agent `TameshiR21.F09LessonRestraint` | `failed`, role `scribe`, report `null`, `replaced:false`; provider `haiku`; retained error is HTTP 429 account rate limit. | `w2/swarm-registry.json:629–637` binds this exact name to this exact agent ID, role `scribe`, `kind:spawn`, axis `calibration`. `spec2.json:562–569` agrees on name/role/axis; `assignments2.json:68` agrees on agent ID. | No matching retained report was found by exact-prefix recursive discovery within `.ufo/waves/round-21`; the complete immediate `w2` listing also contains no F09 report. The dispatch prompt names the intended `.ufo/waves/round-21/w2/F09LessonRestraint.md`, but an assigned path is not an existing file. No report text claiming completion was available. | Keep failed/dead, not completed. Report absence agrees with the outcome's null report; it is not the authority for failure. |
| wave2 `F10RegistryLean`; agent `TameshiR21.F10RegistryLean` | `completed`, role `simplifier`, report `.ufo/waves/round-21/w2/F10RegistryLean.md`, `replaced:false`. | `w2/swarm-registry.json:638–646` binds the exact name/agent ID/role with `kind:spawn`, axis `calibration`. `spec2.json:570–577` agrees; `assignments2.json:69` agrees on ID. | The exact outcome-linked report exists. Lines 1–7 identify the seat and explicitly claim `Verdict: done (read-only audit ...)`; line 115 repeats its report path. Its content matches the registry-audit assignment. Lines 29, 100, and 111 explicitly leave full registry replay unrun: the completion claim is for a static audit, not full runtime replay. | Count one completed callback, consistent with report text, but not because a report exists. Do not convert this into an independently observed replay or provider-authenticated success. |
| wave2 `F11ScopeOverlap`; agent `TameshiR21.F11ScopeOverlap` | `failed`, role `connector`, report `null`, `replaced:false`; provider `antigravity`; retained error is Cloud Code Assist HTTP 429 `QUOTA_EXHAUSTED`, with quota reset timestamp. | `w2/swarm-registry.json:647–655` binds the exact name/agent ID/role with `kind:spawn`, axis `calibration`. `spec2.json:578–585` agrees; `assignments2.json:70` agrees on ID. | No matching retained report was found by exact-prefix recursive discovery within `.ufo/waves/round-21`; the immediate `w2` listing also contains no F11 report. The dispatch prompt names intended `.ufo/waves/round-21/w2/F11ScopeOverlap.md`; no report body was available to inspect for a completion claim. | Keep failed/dead, not completed. Neither the assignment nor a future/partial report can rehabilitate the retained failed callback. |

## Evidence and interpretation

- Outcome authority for this audit: `.ufo/waves/round-21/original-outcomes-final.json:1268–1295`. Exact scoped accounting derived from those three rows: **3 seats, 1 completed, 2 failed/dead, 0 replacements**. These are scoped totals, not a fresh global census.
- Membership authority: `.ufo/waves/round-21/w2/swarm-registry.json:629–655`. This registry has identity, role, kind, item and axes, **not callback status**. Therefore status agreement with the registry cannot be claimed; the registry binds membership, while the retained outcome supplies status.
- Original specifications: `.ufo/waves/round-21/spec2.json:562–585`, also read through a structured exact-name selector to obtain the full prompts. F09 is a lessons/SCORECARD restraint audit; F10 is a registry/source-anchor static audit with no full battery; F11 is a read-only sibling scope-overlap audit. All three require evidence-backed scoped reports, not production edits.
- Exact original agent bindings: `.ufo/waves/round-21/assignments2.json:68–70`.
- `.ufo/waves/round-21/dispatch2-attempt-01.json` contains the exact original IDs and roles at lines 1132–1136, 1149–1153 and 1166–1170. Its `pending` statuses are dispatch-time observations, not contradictory final callbacks. Its prompts provide the intended F09/F10/F11 report locations. No missing report was opened or invented.
- Retained report: `.ufo/waves/round-21/w2/F10RegistryLean.md:1–115`. Its reported historical commands are target evidence, not checks executed by this audit. Its older audited revision `790abd2129f153c13b471e381d454186edbde65e` is explicitly historical context, not a claim that the present round22 frozen base equals that revision.
- Calibration contract: `.ufo/evidence/round-22/contract.json:1–21`; in particular, declared callback inputs are not authenticated provider telemetry. `.ufo/waves/round-21/original-outcomes-final.json:1369` also explicitly says partial reports do not rehabilitate failed jobs.

No identity/role contradiction was found among the three final outcome rows, registry entries, specifications and assignments. F10's done report agrees with its completed outcome. F09/F11 have no discovered reports; these seats do not supply a concrete failed-with-partial-report specimen, and should not be represented as such. Absence here is bounded to the retained round21 tree searched, not every possible external artifact.

## One bounded gate recommendation

For these exact three original wave2 membership bindings, require one outcome each with exact agent ID and role, recognized status, and `replaced:false`; preserve final status vector **`[failed, completed, failed]`** and derived scoped counts **`seats=3, completed=1, dead=2`**. Compute completion from the persisted declared outcome status only. Report existence, `Verdict: done`, missing report, or dispatch-time `pending` must never overwrite that status or supply a replacement seat. Bind these assertions to persisted input digests; this validates consistency, not callback provenance. No gate implementation or extra acceptance criterion is proposed here.

## Changes, limits and tradeoff

Only this new report was written. No deletions or deletion candidates are proposed: removing the registry, specs, dispatch history or retained report would harm provenance and identity/status calibration. No source edits, subagent dispatch, installation, git/index/ref mutation, build, lint, formatter or test command was performed. No runtime check or byte-identity measurement was run, and none is claimed. The retained report's underlying static-audit results were not independently revalidated. The deliberate tradeoff is narrow consistency evidence without asserting provider authenticity or broadening historical admission.

Report: `.ufo/waves/round-22/w1/Audit50.md`
