# Audit20 — round-21 wave1 callback/registry/report agreement (3 frozen identities)

Lane: `TameshiR22.Audit20-2`, critic, read-only. Scope is exactly the three identities below. No build, lint, format, test, or gate was run; no tools installed or updated. The only write is this file.

## Scoped population

| name | frozen agent id | role | frozen status |
|---|---|---|---|
| RG1IntentWitnessPins | `TameshiR21.RG1IntentWitnessPins-3` | revenger | completed |
| RG2IntentRegistryGuards | `TameshiR21.RG2IntentRegistryGuards-3` | revenger | completed |
| SB01LessonDraft | `TameshiR21.SB01LessonDraft-3` | scribe | failed |

## Sources (sha256 where hashed)

- Outcomes: `.ufo/waves/round-21/original-outcomes-final.json` (`029fc1e0…98785`, equal to `derivation.json` input pin), rows at `:472-494`. Predecessor `original-outcomes1.json:479-500` has identical rows for all three.
- Registry: `.ufo/waves/round-21/w1/swarm-registry.json` (`7756c3b1…105b2`, equal to the derivation pin), members at `:522-549`. `record1.json` is byte-identical to it except for the added `"path"` key. The registry carries **no status field** (zero matches for `status`/`state`/`completed`/`failed`), so status cannot be checked against it, only identity and role.
- Spec: `.ufo/waves/round-21/spec1.json:469-491` (name, role, axes, prompt; no id). `assignments1.json:55-57` maps name→`-3` id. `dispatch-attempt-03.json:910-950` shows all three at dispatch with `status: "pending"`. That is a dispatch snapshot, not a callback. `run1.json:540-566` has `agentId: null` (pre-dispatch).
- Delivered callbacks, in the parent L1 transcript outside the repo: `~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-…/TameshiR21.jsonl`. Each identity has exactly one `<task-result>`: SB01 at line 286 (`2026-10-21T12:01:16Z`), RG1 and RG2 at line 508 (`12:14:37Z`). No other line mentions the `-3` ids, so there was no follow-up or second callback.
- Seat transcripts: `…/TameshiR21/TameshiR21.{RG1IntentWitnessPins,RG2IntentRegistryGuards,SB01LessonDraft}-3.jsonl` (sha `5373b7fb…`, `46c5b845…`, `0feb068a…`), plus their output sidecars `…-3.md` (298 B, 384 B, **0 B**).
- Gate input: `.ufo/evidence/round-22/bundle.json`, wave1 members `:277-289`, outcomes `:741-760`, reports `:867-896`. `wrong-count-bundle.json` differs from it only in the wave2 `claimed` block (`38/37` → `40/35`). For these three rows the two files are identical.

## Per-identity agreement

| identity | callback (raw) | outcomes row | registry id/role | report on disk | report self-claim | agreement |
|---|---|---|---|---|---|---|
| RG1 `…RG1IntentWitnessPins-3` | `status="completed" duration="12m53s"`, output "Done. Findings are written to …RG1IntentWitnessPins.md" | completed; report path set; `replaced` key **absent** | match / match | `.ufo/waves/round-21/w1/RG1IntentWitnessPins.md`, 12,986 B, sha `4e075f28…1376e`, mtime 12:13:45Z | Line 1: "done — pin intent and evidence reconstructed …; no code or tests run." | **Agree.** The bytes written by the seat's single `write` tool call equal the current file. The write landed 52 s before the callback. |
| RG2 `…RG2IntentRegistryGuards-3` | `status="completed" duration="12m55s"`, output "done — report written to …" | completed; report path set; `replaced` key **absent** | match / match | `.ufo/waves/round-21/w1/RG2IntentRegistryGuards.md`, 12,172 B, sha `a5be8067…2a3`, mtime 12:13:48Z | Line 1: "done — reconstructed …; all three round-18 guard-removal mutants survived …" | **Agree.** Single `write`, bytes equal the current file, written before the callback. |
| SB01 `…SB01LessonDraft-3` | `status="failed (exit 1)" duration="4.4s"`, output `[anthropic/claude-haiku-5-5] 429 … retry-after-ms=10131000` | failed; `report: null`; provider haiku; `replaced: false` | match / match | **None.** No `SB01LessonDraft.md` anywhere under `.ufo`. The target `w1/drafts/` exists but is empty, and it was created at 11:45Z, before the 12:01Z dispatch, so it is not a seat artifact. | n/a | **Agree.** The seat has one assistant turn: `stopReason: "error"`, zero tokens, zero tool calls, no `write`. Its output sidecar is 0 bytes. It is a genuine provider-dead seat with no partial report. |

Bundle projection for all three: name, id, and role match the registry; status matches the outcomes; `replaced: false`. RG1 and RG2 are in `reports`; SB01 is not. Wave1 totals hold: 71 rows, 28 completed, 43 failed, matching `claimed` 71/28/43. There are no failed-with-report rows, no completed-without-report rows, and no registry/outcome identity or role mismatches. All of this was checked across the full wave1 for context; the findings above cover only the three scoped identities.

## Contradictions and uncertainty

No status contradiction exists for any of the three. Five calibration points remain:

1. **Status normalization is upstream of the gate.** The raw callback literal is `failed (exit 1)`, while the outcome and bundle say `failed`. That mapping happens in hand-built outcome files and is not re-derived from the callback. The gate validates the enum, not this mapping.
2. **`replaced` is not callback-sourced for RG1/RG2.** `original-outcomes-final.json` omits `replaced` on both completed rows. The bundle sets it to `false` from the round-21 lesson's no-replacement declaration (`corpus/lessons/round-21.md:119,169`; see `derivation.json` "projection"). That is a declared input, not an observed fact. It is consistent with the transcript, which shows exactly one task-result per id and no re-dispatch.
3. **Report self-claims are not evidence.** Both RG reports open with "done". RG1/RG2 count as completed because their callbacks say `completed`, not because of that text or the file's existence. A partial report from a dead seat could carry the same "done" header.
4. **The scoped real data does not exercise the partial-report hazard.** SB01 left no file, so the real bundle cannot show whether a dead seat's report gets rehabilitated. Only the synthetic `failed-with-report-counted-completed` fixture in `measure.py:62-64` covers that case. It puts the dead seat in `reports` and claims `completed=2`.
5. **Provenance is unauthenticated, as the contract already bounds.** The callback evidence above is in an out-of-repo session transcript, which this lane could read. The gate takes outcomes as declared input and cannot bind them to that transcript.

## Bounded gate recommendation

For these three identities, the accounting gate should make one concrete assertion: **status comes from the outcome row alone, and report presence is never an input to counting.**

- Each name/id appears exactly once in members and once in outcomes, with id and role equal to the registry (`TameshiR21.RG1IntentWitnessPins-3`/revenger, `TameshiR21.RG2IntentRegistryGuards-3`/revenger, `TameshiR21.SB01LessonDraft-3`/scribe).
- Status is in `{completed, failed}` and `replaced` is `false`.
- RG1 and RG2 contribute 2 to `completed`; SB01 contributes 1 to `dead`.
- Adding `"SB01LessonDraft"` to `reports` must leave the counts at 28/43. Pairing that with `claimed.completed=29` must be rejected as `TOTAL_MISMATCH`.

Narrow-scope suggestion (advisory): the C1 claim is about real-bundle rehabilitation, but the real bundle has no dead-seat report. A cheap real-data mutation would close that gap: copy the frozen bundle, add `SB01LessonDraft` to wave1 `reports`, and require the identical 28/43 verdict. Without this, the only evidence is the two-seat synthetic fixture. Do not upgrade the claim to authenticated callback provenance; the contract bound "retained callbacks are declared inputs" stays correct.
