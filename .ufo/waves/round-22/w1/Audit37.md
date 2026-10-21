# Audit37 — round21 wave2 accounting: Section1964, KillMB03

- Seat: `TameshiR22.Audit37-2` (connector). Advisory, not non-author admission.
- Axes: **calibration** (status is grounded in a callback, not in a report file). Secondary: gate scope (what the round22 gate can and cannot assert).
- Scoped population: exactly two frozen identities: wave2 `Section1964` → `TameshiR21.Section1964`, and wave2 `KillMB03` → `TameshiR21.KillMB03`. No other seats audited. Round21 admission and its two claims are not relitigated.
- Read-only. Nothing executed beyond `jq`/`sha256sum`/`rg`/`stat` reads. No checks, builds or tests run. No tools installed or updated.

## Input identity (persisted digests)

The values equal `.ufo/evidence/round-22/derivation.json` `input_sha256` at the time of reading:

| Input | SHA-256 |
|---|---|
| `.ufo/waves/round-21/original-outcomes-final.json` | `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` (match) |
| `.ufo/waves/round-21/w2/swarm-registry.json` | `029acd0ed3c2d4a8f0fbdce2958667788e0f8bab212fa3f7b58239ea581f917f` (match) |

## Per-identity rows

| Field | Section1964 | KillMB03 |
|---|---|---|
| Outcome row (`original-outcomes-final.json` `/wave2/rows/30`, `/31`) | `TameshiR21.Section1964`, simplifier, `completed`, report `.ufo/waves/round-21/w2/Section1964.md`, `replaced:false` | `TameshiR21.KillMB03`, mutation-tester, `completed`, report `.ufo/waves/round-21/w2/KillMB03.md`, `replaced:false` |
| Same row in `original-outcomes2.json` and `-corrected.json` (`/rows/30`, `/31`) | identical | identical |
| w2 registry member | key `Section1964`, `agentId TameshiR21.Section1964`, role simplifier, axes `[calibration]` | key `KillMB03`, `agentId TameshiR21.KillMB03`, role mutation-tester, axes `[operability, calibration]` |
| `spec2.json` / `assignments2.json:32-33` | role simplifier; name→id `TameshiR21.Section1964` | role mutation-tester; name→id `TameshiR21.KillMB03` |
| `dispatch2-attempt-01.json` | index 30, `status: pending` (launch snapshot, `results: []`) | index 31, `status: pending` |
| Round22 `bundle.json` wave2 | member and outcome present; name, id and role equal; `completed`, `replaced:false`; listed in `reports` | same |
| **Callback** (L1 parent transcript `~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-…/TameshiR21.jsonl`, sha256 `4fed06b0…6d66`) | record `696a8a4a` at line 687, `custom_message/async-result` "background job delivery", 2026-10-21T12:31:30.574Z: `jobId=agentId=TameshiR21.Section1964`, `status: completed`, `durationMs 88654`, `<task-result … status="completed" duration="1m28s">` | record `2d808c8a` at line 703, 12:33:14.168Z: `jobId=agentId=TameshiR21.KillMB03`, `status: completed`, `durationMs 202629`, `<task-result … status="completed" duration="3m22s">` |
| Callback uniqueness | exactly one job-status record for this id in the parent transcript; nothing contradicts it | exactly one; nothing contradicts it |
| Retained callbacks in `.ufo/waves/round-21/wait2-recovered-01…22.json` | **absent** (these files hold only 25 unique ids, and this one is not among them) | **absent** |
| Seat transcript (`…/TameshiR21/TameshiR21.<name>.jsonl`) | sha256 `7e8a46a5…805bcb89`. First turn `stopReason: error` (xai-oauth 403 "run out of credits"), then fallback `cursor/composer-2.5-fast` (`resolvedModelIsFallback: true`). Final assistant message `stopReason: stop` with the "Section1964 audit complete" text, then `session_exit` `kind: normal` | sha256 `733a4979…7d609c`. Single route `openai-codex/gpt-6.1-sol`, no error turn. Final assistant `stopReason: stop` "done — MB03 genuinely discriminated / KILLED", then `session_exit normal` |
| Report and timing | report mtime 12:31:07Z, before the 12:31:30Z callback. The JSON mark `w2/sections/1964.json` exists (verdict `no-blocking-gaps`, 0 blocking, 2 wrong expectations) | report mtime 12:32:55Z, before the 12:33:14Z callback. `w2/mutations/MB03.exit` = `0`, and the MB03 replay, cleanup and stdout files exist |
| What the report text claims | A completed bounded audit, plus one executed check (`coldread/measure.py --selftest` → 12/12). It has no literal `Report:` trailer, but the path matches the spec (format only) | A completed probe: exact command exit 0, pristine/mutant/restored 0→1→0. It also records an earlier async launch refusal ("Background job limit reached (100)"). That is a launch observation inside a completed seat, not seat death |
| **Agreement** | Callback, registry, spec, outcome and bundle agree on name, id, role and `completed`. The report corroborates but is not the basis for the status | Same |

**Partial report versus completed callback.** Neither identity is a partial-report case. Each has a terminal `completed` async-result callback and a normal final assistant turn. The two wave2 seats whose reports exist despite failure are `ProfileBashTsukuroiCensus` and `V01WitnessTests` (`corpus/lessons/round-21.md:163-170`). That accounts for 40 report basenames against 38 completed in `bundle.json` wave2. Both are outside this scope.

## Contradictions and uncertainty

1. **The callback evidence is not a declared or retained repo input.** The lesson says `original-outcomes2-corrected.json` "retains actual callback metadata" (`corpus/lessons/round-21.md:170`). For these two completed rows, though, it contains no callback fields: no `durationMs`, no record id and no error text. Dead rows do carry `provider` and `last_error`. The only callback for either identity is in the L1 parent session transcript under `~/.omp`. That file is outside the repo, is not hashed in `derivation.json`, and is absent from every `wait2-recovered-*.json`. So `completed` is correct as observed, but inside the repo it is *declared*, not *retained*. A reader with only repo inputs cannot tell these rows apart from a report-inferred `completed`. The projection note "no status inferred from reports" (`derivation.json:9`) is an assertion the inputs cannot back for these rows.
2. **The intermediate provider error does not mean the seat died.** Section1964's first turn errored with an xAI 403 before the fallback route completed. A gate or auditor that scans transcripts for any `stopReason: error` would misclassify the seat as dead. The terminal callback status is the authoritative signal, not intermediate turns. The outcome row also carries no `provider`, and its effective provider was the `cursor` fallback, not the configured composer→xai route. This does not affect `provider_counts_dead`, which counts dead seats only. It does mean that completed rows give no route information.
3. Authenticity is out of reach. The transcript is harness-written and unsigned. This audit only confirms that it is internally consistent: one record per id, a terminal status, a duration that matches the task-result tag, and timestamps that follow the report writes. It does not authenticate provider telemetry, consistent with contract bound "retained callbacks are declared inputs, not authenticated provider telemetry".

## Gate assertion for these identities

For each of the two, the frozen gate (`tools/wave-accounting.py` via `.ufo/evidence/round-22/measure.py`) can and should assert only the following:
- The `(name, id, role)` triple is identical between the w2 registry member and the outcome row (`IDENTITY_MISMATCH`).
- The id is unique across wave2 (`DUPLICATE_AGENT`).
- Status is in the enum `{completed, failed}` (`UNKNOWN_STATUS`).
- `replaced == false` (`REPLACEMENT_FORBIDDEN`).
- Each counts once toward wave2 `claimed.completed = 38` (`TOTAL_MISMATCH`).
- The bundle bytes match `expected.json` (`SNAPSHOT_TAMPERED`).

Report presence MUST NOT be an input to status in either direction. Both rows would pass with or without `reports` containing their names.

## Recommendation

One bounded, non-blocking change to the derivation, not to the gate. For each `completed` row, persist a callback locator in the projection input or in `derivation.json`: source transcript path and sha256, record id, timestamp, `status`, `durationMs`. If that is not done, label completed status explicitly as "declared from L1 callback; callback not retained in repo". For this scope the locators are:

- `TameshiR21.Section1964`: `696a8a4a`, 12:31:30.574Z, 88654 ms.
- `TameshiR21.KillMB03`: `2d808c8a`, 12:33:14.168Z, 202629 ms.

Both sit in `TameshiR21.jsonl`, sha256 `4fed06b03af0e721f8405f74df3815001b91170d65d9e12df35ecc4105ce6d66`.

This improves calibration: "callback-authoritative" becomes checkable from declared inputs. It harms no axis: the eight gate predicates, the frozen counter and the round21 totals are unchanged.

Risks:
- The transcript lives outside the repo and can move or be rotated. Copying the excerpt into the repo would itself be new evidence, which is L1's decision.
- None of this authenticates the provider.

Verification for L1, if adopted: count the `details.jobs[]` entries per completed id in the cited transcript (expect exactly 1, `status: completed`), and keep the existing `measure.py` control and the 8 cases unchanged.

Report: `.ufo/waves/round-22/w1/Audit37.md`
