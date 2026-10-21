# Audit21: round-21 wave1 SB02 and SB03, checking callback, registry, report and deliverable against each other

**Agent:** `TameshiR22.Audit21-2` (critic, read-only)
**Scoped population (exactly two):** round-21 wave1 seats `SB02QualityDrafts` (`TameshiR21.SB02QualityDrafts-3`) and `SB03EntrySkeleton` (`TameshiR21.SB03EntrySkeleton-3`), both frozen as `status: failed`.
**Axes:** identity and membership agreement; how far the callback supports the status; whether any report exists and whether it claims completion; rehabilitation risk from things other than report files.
**Tooling:** nothing installed or updated. No builds or tests were run, no git mutation was made, and only this file was written.

## Evidence (sha256 values computed by this audit)

| Artifact | Path | sha256 |
|---|---|---|
| Outcome source | `.ufo/waves/round-21/original-outcomes-final.json` (rows at lines 495-514) | `029fc1e0…698785` (matches `derivation.json`) |
| Wave1 registry | `.ufo/waves/round-21/w1/swarm-registry.json` (lines 550-568) | `7756c3b1…a105b2` (matches `derivation.json`) |
| Spec | `.ufo/waves/round-21/spec1.json` (lines 493-510) | `f78fe747…22317af` |
| Assignments | `.ufo/waves/round-21/assignments1.json` (lines 58-59) | n/a |
| Dispatch snapshot | `.ufo/waves/round-21/dispatch-attempt-03.json` (`details.progress[56]` and `[57]`) | `951d710a…812674` |
| Earlier outcome | `.ufo/waves/round-21/original-outcomes1.json` (lines 502-520) | `3b83e588…e217` |
| R22 bundle | `.ufo/evidence/round-22/bundle.json` (`waves[0].members[56,57]`, `outcomes[56,57]`, `reports`) | n/a |
| Callback (outside the repo, read-only) | `~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-…/TameshiR21.jsonl`, line 286 (`custom_message`, 12:01:16Z) | n/a |
| Child transcripts (outside the repo) | `…/TameshiR21/TameshiR21.SB02QualityDrafts-3.jsonl` and `…SB03EntrySkeleton-3.jsonl` | `20999f22…57a`, `8208281b…9f68` |
| Child agent output files | `…/TameshiR21/TameshiR21.SB02QualityDrafts-3.md` and `…SB03EntrySkeleton-3.md` | both 0 bytes |

## Per-identity rows

| Field | SB02QualityDrafts | SB03EntrySkeleton |
|---|---|---|
| id in outcome, assignments1, registry `agentId`, record1, dispatch and bundle | `TameshiR21.SB02QualityDrafts-3` in all of them | `TameshiR21.SB03EntrySkeleton-3` in all of them |
| role | `scribe` in outcome, spec1, registry, dispatch (`agent`), bundle | `scribe` in all of them |
| registry status field | none (the registry records membership only and has no status) | none |
| outcome `status`, `replaced`, `report`, `provider` | `failed`, `false`, `null`, `haiku` | `failed`, `false`, `null`, `haiku` |
| Callback | `<task-result id="TameshiR21.SB02QualityDrafts-3" agent="scribe" status="failed (exit 1)" duration="4.4s">`, output `[anthropic/claude-haiku-5-5] 429 rate_limit_error … request_id req_011CgFM3wm6A8CBeUsqThpbZ … retry-after-ms=10131000` | the same, with `request_id req_011CgFM3wm6sUq5gpF848Wp8`, duration 4.4s |
| Child transcript | session_init, the user prompt, credential pin, then **one** assistant message with `stopReason: error` and the same 429 and request_id, then session_exit at 12:08:08Z. **Zero tool calls and zero text output.** | the same pattern, with request_id matching the callback. Zero tool calls. |
| Dispatch snapshot | `status: pending`, `toolCount: 0`, `tokens: 0`; this is a pre-run snapshot, not an outcome | the same |
| Spec report path | `.ufo/waves/round-21/w1/SB02QualityDrafts.md`: **absent** | `.ufo/waves/round-21/w1/SB03EntrySkeleton.md`: **absent** |
| Spec draft target | `.ufo/waves/round-21/w1/drafts/quality-43-44.md`: **absent** (the `drafts/` directory is empty) | `.ufo/waves/round-21/w1/drafts/hermetic-env-differential.md`: **absent** |
| Any report claiming completion | none. No file anywhere in the repo is named for either seat, and the agent output file is 0 bytes. | none |
| Partial report or completed callback? | Neither. The callback reports a provider failure before the first token. | Neither. |
| Bundle | member and outcome rows match, with `status: failed` and `replaced: false`; the name is not in `reports` | the same |
| Agreement | **Callback, registry, outcome and bundle all agree: the seat is dead and was not replaced.** | **Same: all four agree that the seat is dead and was not replaced.** |

On the earlier outcome file: `original-outcomes1.json` and `original-outcomes-final.json` contain identical rows for both seats, so nothing drifted between snapshots.

## Contradictions and the strongest counterexample

1. **The spec's deliverables exist, but the seats did not write them.** QUALITY criteria 43 and 44 (`corpus/QUALITY.md:423-440`) and `corpus/knowledge/hermetic-env-differential.md` are exactly SB02's and SB03's assigned content. Both were added by commit `370f2df` at 12:24:45Z, which is an ancestor of base `51d49d5`. That is about 23 minutes after both seats died with zero tool calls at 12:01:08Z. The content was written and integrated by L1.
   - A gate that infers success from the deliverable existing would rehabilitate two provider-dead seats. A gate that infers success from the spec target being filled would do the same.
   - This is a stronger failure mode than a partial report, because no report file is involved at all.
   - The frozen data is not contradicted: outcome and bundle still say `failed`. But a projection keyed on "work exists" would contradict them.
2. **No wave1 callback is retained in the repo.** Wave1 outcome rows have no `actual_result` field (0 of 71 rows). `round-21/` contains no wave1 wait or callback file; compare wave2's `wait2-recovered-*.json` and `original-outcomes2-corrected.json`. The callback I matched lives only in the omp session store, outside the repo and outside `derivation.json` inputs.
   - So for these two rows, the persisted `status: failed` is an L1 transcription of the callback, not a retained callback.
   - The transcription is faithful. `failed (exit 1)` was normalized to `failed`. `last_error` drops the `[anthropic/claude-haiku-5-5]` prefix, the JSON envelope and the `request_id`, but keeps the 429 message and `retry-after-ms=10131000` verbatim.
   - This is a provenance gap, not a status disagreement.
3. **The registry was written after the seats died.** Registry `createdAt` is 12:02:01Z, after both deaths (12:01:08Z) and after the callback (12:01:16Z). That is consistent with it being a membership record and not a status source.
   - The registry cannot corroborate status, and it should not be cited as if it does.
4. **`run1.json` has `agentId: null` for both rows.** This is the template written before spawning and is not authoritative. Identity agreement must be checked against the registry, assignments and bundle, not `run1.json`.

I found no contradiction in id, role, status, replacement or report fields across the authoritative artifacts.

## Bounded gate recommendation (C1 calibration)

For these two identities, the accounting gate should assert only facts that exist in the persisted inputs:

- **Identity:** `outcome.id == registry.members[name].agentId == bundle.members[name].id`.
- **Role:** `outcome.role == registry.role == "scribe"`.
- **Status:** `status == "failed"`, which must be an exact enum value. A raw callback string such as `failed (exit 1)` must be rejected under `unknown-status`, not silently normalized.
- **Report:** `report == null`.
- **Replacement:** `replaced == false`, with no second id for the same `name` (no `replacement-seat` or `duplicate-agent`).
- **Totals:** both seats are counted in `dead` (wave1 43) and never in `completed` (wave1 28).

Completion must be decided only by `status`. It must never be derived from:

- a report file existing (`failed-with-report-counted-completed`), or
- a spec deliverable or draft target existing. `corpus/QUALITY.md` 43-44 and `hermetic-env-differential.md` are the live counterexample.

The gate must **not** require a callback field for wave1 rows. No such field is persisted, so the requirement would either fail spuriously or invite fabricated backfill.

The gate's documented bound should also say that wave1 status is a declared L1 transcription. It is matched by this audit to the out-of-repo callback (request_ids `req_011CgFM3wm6A8CBeUsqThpbZ` and `req_011CgFM3wm6sUq5gpF848Wp8`), but the gate does not authenticate it. This is consistent with the contract bound "retained callbacks are declared inputs, not authenticated provider telemetry."

The smallest safe fixture addition, which is advisory and not judged: one frozen case that flips SB02 or SB03 to `completed` (or adds a report entry) while keeping the registry unchanged. The CLI must reject it under `false-completion-count` or `failed-with-report-counted-completed`.

## Summary

| Identity | Callback | Registry and outcome | Report | Read |
|---|---|---|---|---|
| SB02QualityDrafts | `failed (exit 1)`, 429, 4.4s, 0 tools | id and role agree; `failed`, `replaced: false` | none (0-byte agent output; spec path absent) | **dead seat, all sources agree; the deliverable exists but was written by L1, so it must not rehabilitate the seat** |
| SB03EntrySkeleton | `failed (exit 1)`, 429, 4.4s, 0 tools | id and role agree; `failed`, `replaced: false` | none (0-byte agent output; spec path absent) | **dead seat, all sources agree; the deliverable exists but was written by L1, so it must not rehabilitate the seat** |

Report: `.ufo/waves/round-22/w1/Audit21.md`
