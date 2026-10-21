# Audit38 — wave-2 KillMB04 / KillMB05 / KillMB06 callback vs registry vs report

Verdict: all three seats are **genuinely completed** according to their original task callbacks. Callback, registry, outcome row, and report agree on identity, role, and status. **Caveat:** none of the three outcome rows retains its callback. The callback that settles status lives only in the host session transcript, which sits outside the gate's persisted inputs. Advisory only; this is not admission, and it does not relitigate round 21.

Axes: calibration (primary). Scoped population: exactly 3 seats — wave 2, ids `TameshiR21.KillMB04`, `TameshiR21.KillMB05`, `TameshiR21.KillMB06`. No other seat was audited.

## Evidence sources (read-only)

- Outcome rows: `.ufo/waves/round-21/original-outcomes-final.json:954-977`. Each row has the same rows in `original-outcomes2.json:321-344` and `original-outcomes2-corrected.json:322-345`. The corrected file did not change these rows.
- Registry: `.ufo/waves/round-21/w2/swarm-registry.json:297-325`, with duplicate content in `record2.json:298-326`. The registry has no status field. Its rows hold only `kind/agentId/role/item/axes`.
- Spec: `.ufo/waves/round-21/spec2.json:264-290`. In `run2.json:315-344` the `agentId` is null because this is the pre-spawn plan.
- Dispatch snapshot: `.ufo/waves/round-21/dispatch2-attempt-01.json:552-594`. It reads `status: "pending"` with `toolCount: 0`. This is the state at spawn time, not a terminal status. It MUST NOT be used as a status source.
- Callbacks: the parent transcript `~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-baa6-76c9-b209-ce1123c6cc22/TameshiR21.jsonl`. Line 694 (`custom_message`, 2026-10-21T12:32:45.097Z) holds MB04 and MB05. Line 707 (12:34:11.815Z) holds MB06. Each identity has exactly one `<task-result>` in this file.
- Child transcripts: `…/TameshiR21/TameshiR21.KillMB0{4,5,6}.jsonl`.
- Reports: `.ufo/waves/round-21/w2/KillMB0{4,5,6}.md`. Mutation receipts: `.ufo/waves/round-21/w2/mutations/MB0{4,5,6}.*`.

## Per-identity rows

| Identity | Outcome row (final) | Registry (w2) | Original callback header | Child transcript terminal state | Report | Agreement |
|---|---|---|---|---|---|---|
| `TameshiR21.KillMB04` | role `mutation-tester`, `completed`, `replaced:false`, report `w2/KillMB04.md`; **no `actual_result`/`resolved_model` keys** | `agentId` match, role `mutation-tester` | `id="TameshiR21.KillMB04" agent="mutation-tester" status="completed" duration="2m46s"` | 1 user prompt (MB04 target + matching Report path); 11 `toolUse` + 1 `stop`; 0 `errorMessage`; model `openai-codex/gpt-6.1-sol`; final assistant 12:32:28.932Z; `session_exit kind=normal reason=dispose` 12:39:28Z | exists (mtime 12:32:18Z, before final assistant); claims `done` and genuinely discriminated; receipts MB04.json/stderr/command/restoration present (12:30:13–12:31:38Z) | **Agree.** Completed callback, not a report-only rehabilitation |
| `TameshiR21.KillMB05` | same shape, `completed`, `replaced:false`, report `w2/KillMB05.md`; no callback keys | match | `id="TameshiR21.KillMB05" agent="mutation-tester" status="completed" duration="2m54s"` | 1 user prompt (MB05 target + matching Report path); 10 `toolUse` + 1 `stop`; 0 errors; same model; final assistant 12:32:36.766Z; normal exit 12:39:36Z | exists (12:32:26Z); claims `done`, KILLED; receipts present (12:30:13–12:31:20Z) | **Agree** |
| `TameshiR21.KillMB06` | same shape, `completed`, `replaced:false`, report `w2/KillMB06.md`; no callback keys | match | `id="TameshiR21.KillMB06" agent="mutation-tester" status="completed" duration="4m7s"` | 1 user prompt (MB06 target + matching Report path); 15 `toolUse` + 1 `stop`; 0 errors; same model; final assistant 12:33:50.570Z; normal exit 12:40:50Z | exists (12:33:37Z); claims `done`, KILLED; receipts present (12:30:14–12:31:34Z) | **Agree.** The report itself flags an unowned transient `__pycache__` observation. That is a hygiene note, not a status issue |

Timing is consistent across all three. Child sessions started at 12:29:42Z, and the registry was written at 12:29:56Z. In each case the report was written, then the final assistant turn ended with `stop`, then the parent received the callback. Each duration equals the time from the child's first entry to its final assistant turn. For example, MB04 runs 12:29:42 → 12:32:28, which is 2m46s. No seat was replaced, and no follow-up user message rewrote the run.

Minor non-contradiction: the MB04 callback cites the detector at `:1294-1295`, and the report cites the test body `:1283-1295`. The assertion lines are the same.

## Contradiction / gap the gate must close

1. **These rows carry no callback.** Wave 2 has 75 rows in `original-outcomes-final.json`, which break down as follows:
   - 16 `completed` rows with a callback.
   - 22 `completed` rows with **no `actual_result` key at all**. All three of my seats are in this group.
   - 8 `failed` rows with the key.
   - 29 `failed` rows without it.

   Totals are 38 completed and 37 dead, which matches the header. For my three seats, `completed` can only be authenticated from the host transcript, which is not among the persisted inputs.
2. **The demotion rule treats an absent key differently from a null one.** The `-corrected` file demoted two rows, `ProfileBashTsukuroiCensus` and `V01WitnessTests`, from `completed` to `failed`. Both had `actual_result: null`. That is the "partial report does not rehabilitate" rule (`"rule"` key, corrected file line 6). Rows with the key **absent** kept `completed`. A gate keyed on `actual_result === null` would therefore accept a fabricated `completed` row simply by omitting the key. My three seats are correctly completed, but **only** because the transcript confirms it, not because of anything the row shows.
3. The registry has no status. Status agreement can only be checked between the outcome row and the callback, never between the outcome row and the registry. The registry pins only identity and role.

## Bounded gate recommendation

Every `completed` row MUST be rejected unless the gate's declared inputs include a callback record for it. The callback must satisfy:

- Its header `id` equals the row `id`, which equals the registry `agentId`.
- Its header `agent` equals the row `role`, which equals the registry `role`.
- Its header `status` is `"completed"`.

A missing key and a null value MUST be treated the same way: the row is `unknown-status` or a false completion, never completed. Report-file existence and report text MUST NOT count. This maps to the contract predicates `false-completion-count` and `failed-with-report-counted-completed`. The fixture set should include a variant where the callback key is omitted, not only one where it is null.

Applied to these three seats, the gate needs to snapshot the three `<task-result>` headers (`TameshiR21.jsonl` lines 694 and 707) as declared inputs. Each header should be bound by digest, per the contract bound "retained callbacks are declared inputs, not authenticated provider telemetry". With those inputs, all three should pass as completed, `replacement=false`. Without them, the honest classification is `unknown-status`, not `completed`.

## Limits

- Callback provenance is from the omp session store, read from host files. It is not authenticated provider telemetry, and I did not check it cryptographically.
- I did not re-run the mutation claims.
- Read-only. The only write is this report. No tools were installed or updated, and no build, test, or lint commands were run.

Report: .ufo/waves/round-22/w1/Audit38.md
