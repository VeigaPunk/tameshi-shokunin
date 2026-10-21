Verdict: done — all three frozen identities agree across registry, spec, outcome rows, delivered callback, and retained report. Each is a genuine `completed` callback, not a partial report rehabilitating a dead seat. No contradiction was found; the bounded caveats are listed below.

# Audit17 — wave1 RV05/RV06/RV07 callback vs registry vs report

## Scoped population (exactly 3; nothing else audited)

| name | frozen id | role |
|---|---|---|
| RV05RouteMixReview | TameshiR21.RV05RouteMixReview-3 | reviewer |
| RV06MistakeSweep | TameshiR21.RV06MistakeSweep-3 | reviewer |
| RV07ProvinceRules | TameshiR21.RV07ProvinceRules-3 | reviewer |

## Evidence inputs (sha256 observed this audit)

- Outcomes: `.ufo/waves/round-21/original-outcomes-final.json` `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` (rows at :409-428; identical rows in `original-outcomes1.json:416-435`). Matches `.ufo/evidence/round-22/derivation.json` `input_sha256`.
- Registry: `.ufo/waves/round-21/w1/swarm-registry.json` `7756c3b1ff7fdd6f20f4db2e0f2652742f899c945c6210756092061795a105b2` (members :437-465, `kind: spawn`; the registry has no status field). Matches derivation.json.
- Spec: `.ufo/waves/round-21/spec1.json` `f78fe747…22317af`, `items[]` rows :393-411 (name and role only; agentId is assigned at dispatch).
- Dispatch: `.ufo/waves/round-21/dispatch-attempt-03.json:756-802`, indices 44-46, `modelRole: m_zfl`, `status: pending` (a launch snapshot, not an outcome). Attempts 01 and 02 (unsuffixed and `-2`) were refused with "Background job limit reached (100)", so `-3` is the only launched identity.
- **Delivered callback** (outside the repo, read-only): parent transcript `~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-baa6-76c9-b209-ce1123c6cc22/TameshiR21.jsonl` (sha256 `4fed06b03af0e721f8405f74df3815001b91170d65d9e12df35ecc4105ce6d66`). Each identity has exactly one `custom_message`/`async-result` record (`source: background job delivery`), and no other line mentions the id.
- Seat transcripts: `…/TameshiR21/TameshiR21.<name>-3.jsonl` plus the `.md` final output.

## Per-identity agreement

| identity | registry (id/role) | outcome row | delivered callback `details.jobs[]` | seat transcript terminal | report file | agreement |
|---|---|---|---|---|---|---|
| RV05RouteMixReview-3 | exact / reviewer | completed, report `.ufo/waves/round-21/w1/RV05RouteMixReview.md`, no `replaced` key | `status: completed`, durationMs 835402, 2026-10-21T12:14:59.852Z | zai/glm-5.3-flash had 2 `stopReason: error` turns (429 type=1302); fallback `model_change` to openai-codex/gpt-6-luna (`resolvedModelIsFallback: true`); final assistant `stop` 12:14:59.792Z; `session_exit` kind normal | sha256 `8f358df4…fa31e4`, 49 lines; opens "done — no defect…"; mtime 12:14:51.05Z equals the last successful `edit` toolResult 12:14:51.052Z | **agree** |
| RV06MistakeSweep-3 | exact / reviewer | completed, report `…/RV06MistakeSweep.md`, no `replaced` key | `status: completed`, durationMs 933664, 12:17:01.362Z | 6 zai 429 error turns, then fallback to openai-codex; final `stop` 12:16:38.058Z; normal exit. One intermediate `edit` returned `isError: true` (anchor mismatch); the next `edit` succeeded | sha256 `2cc7f989…dedb5`, 34 lines; opens "done"; mtime 12:16:27.63Z equals the last successful `edit` 12:16:27.635Z | **agree** |
| RV07ProvinceRules-3 | exact / reviewer | completed, report `…/RV07ProvinceRules.md`, no `replaced` key | `status: completed`, durationMs 704735, 12:13:15.861Z | 2 zai 429 error turns, then fallback to openai-codex; final `stop` 12:12:49.130Z; normal exit | sha256 `0dbcf790…9c29f`, 49 lines; opens "Verdict: done"; mtime 12:12:40.04Z equals the last successful `edit` 12:12:40.042Z | **agree** |

Partial-report versus completed-callback distinction: for all three, the completion status comes from the delivered `async-result` callback, not from the report's existence. Each report's final bytes were written by its own seat before that seat's terminal `stop`, and no file write happened after the seat exited. The report text claims completion ("done"), which is consistent with the callback. That consistency is corroboration only; it does not establish the status. The `-3` reports also cannot have come from an earlier refused attempt, because attempts 01 and 02 never launched.

Wave1 cross-check (a data count only): the 28 completed rows in wave1 have exactly the same name set as the 28 `w1/*.md` files, with zero completed seats lacking a report and zero reports lacking a completed status. Wave1 therefore gives the gate no discriminating case of its own; the discriminating partial-report cases are the two wave2 seats.

## Contradictions and uncertainties

1. **None blocking.** Identity, role, and status agree across all sources for all three seats.
2. **Interim 429s did not kill these seats.** The seats survived provider rate limiting through the harness fallback. An accounting rule that infers death from transcript 429/error turns would wrongly mark them dead. Only the terminal callback status is authoritative.
3. **The completing provider is not recorded.** Completed rows carry no `provider` or `resolved_model`. The work actually finished on openai-codex fallback, not on the spec's zai `m_zfl` route. This does not affect the completed/dead counts or `provider_counts_dead`, but these rows cannot support any per-provider success claim.
4. **`replaced: false` is supplied by normalization, not recorded in the row.** All 28 wave1 completed rows lack a `replaced` key. The bundle (`.ufo/evidence/round-22/bundle.json:678-697`) sets `replaced: false`. derivation.json declares this normalization explicitly, from the round21 lesson's no-replacement statement, so it is disclosed provenance rather than false provenance. Even so, it rests on a declaration, not on a callback field.
5. **The gate's inputs exclude the callback transcript.** derivation.json digests the outcomes file and the registries, not `TameshiR21.jsonl`. The gate therefore validates the L1 transcription of the callbacks, as the contract bound "retained callbacks are declared inputs, not authenticated provider telemetry" already states. For these three seats I verified that the transcription matches the callbacks. [INFERENCE] The gate cannot detect a transcription error on its own.

## Bounded gate recommendation

For these three identities the accounting gate must assert, from the outcome rows alone:

- each `(name, id, role)` equals the registry member's `(key, agentId, role)`;
- `status == "completed"`, from the closed enum `{completed, failed}`;
- `replaced == false`;
- each seat is counted toward wave1 completed 28 and seats 71.

Report existence must have zero weight in any of these assertions. The smallest falsifier is to delete or rename one of the three reports in a fixture: completed must stay 28. Flipping one row to `failed` while keeping its report must move it to dead (43→44). Optionally, the gate could record the parent-transcript digest and the async-result timestamps as a declared provenance pointer. That pointer must not count as an authentication claim.

## Process record

The audit was read-only. Commands used were `sha256sum`, `stat`, `wc`, `jq`, `rg`, `comm`, and `find`, run against the repo files and the omp session JSONL. No build, test, or lint was run; no git operation was performed; no tools were installed; and no agents were spawned. The only file written is this report.
