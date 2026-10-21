# Audit26 — callback/registry/report agreement for three frozen round-21 identities

Role: critic (read-only). Scope: exactly three identities. No production edits, no checks run, no tools installed.

## Scoped population

| Wave | Name | Agent id | Outcome status (final) |
|---|---|---|---|
| w1 | CN1SiblingOverlap | `TameshiR21.CN1SiblingOverlap-3` | failed |
| w2 | Section0001 | `TameshiR21.Section0001` | completed |
| w2 | Section0006 | `TameshiR21.Section0006` | failed |

## Inputs (sha256)

- `.ufo/waves/round-21/original-outcomes-final.json` — `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` (w1 CN1 at lines 624-632; w2 Section0001 at 641-649 and Section0006 at 651-661)
- `.ufo/waves/round-21/w1/swarm-registry.json` — `7756c3b1ff7fdd6f20f4db2e0f2652742f899c945c6210756092061795a105b2` (CN1 at 686-695)
- `.ufo/waves/round-21/w2/swarm-registry.json` — `029acd0ed3c2d4a8f0fbdce2958667788e0f8bab212fa3f7b58239ea581f917f` (Section0001 at 8-16, Section0006 at 17-25)
- `.ufo/waves/round-21/spec1.json` — `f78fe747…17af`; `.ufo/waves/round-21/spec2.json` — `e0715910…b6b3`
- Retained callbacks: `.ufo/waves/round-21/wait2-recovered-13.json` — `6498170d…c98a` (Section0006 failure); `.ufo/waves/round-21/wait2-recovered-16.json` — `abb63fdc…5b21` (Section0001 completion)
- Report: `.ufo/waves/round-21/w2/Section0001.md` — `a1b57f71…d2b`; mark `.ufo/waves/round-21/w2/sections/1.json` — `709ba953…d2b`

The registries contain `agentId` and `role` per member but no status field. The status enum can only come from outcome rows and retained callbacks; the registry cannot supply it.

## Per-identity findings

### CN1SiblingOverlap (w1): status agrees, but the callback is not retained raw

- **Registry vs. row:** The registry key `CN1SiblingOverlap` maps to agentId `TameshiR21.CN1SiblingOverlap-3` with role `connector`. The outcome row has the same id and role, and `assignments1.json:72` also agrees. `dispatch-attempt-03.json` shows the seat spawned as `connector`, `modelRole m_antigravity`, status `pending`.
- **Callback:** The row records `failed` from provider `antigravity` with `last_error` "Cloud Code Assist API error (429): … QUOTA_EXHAUSTED; quotaResetTimeStamp=2026-10-25T11:37:24Z" and `replaced:false`. **Uncertainty:** that error string appears only in the derived outcome tables (`original-outcomes1.json`, `-2.json`, `-2-corrected.json`, `-final.json`). Round-21 has no wave-1 wait/callback snapshot that holds the raw task-result. `original-outcomes1.json.outcome_source` asserts the tables came from "original delivered task completion/failure messages", but that is the author's declaration and is not retained as raw evidence. The row is byte-identical between `original-outcomes1.json` and `-final.json`.
- **Report:** The spec path is `.ufo/waves/round-21/w1/CN1SiblingOverlap.md` (from the `run1.json` task text). That file is **absent** (`ls` returns ENOENT), and the row has `report:null`.
- **Verdict:** The failed status, null report, and absent file are internally consistent, and there is no partial report to rehabilitate. Callback provenance cannot be checked against any raw record.

### Section0001 (w2): completed is real; the leading "partial" is a review verdict

- **Registry vs. row:** The ids match (`TameshiR21.Section0001`) and the role is `reviewer` in the registry, the row, `assignments2.json:2`, and `dispatch2-attempt-01.json`.
- **Callback:** The row says `completed`. This matches the raw retained task-result in `wait2-recovered-16.json`: `status="completed" duration="21m59s"` with resolvedModel `openai-codex/gpt-6-luna:max`. The seat was `running` with model `zai/glm-5.3-flash:max` in snapshots 01–15 and completed after a model fallback. The `widget.state` is `fallback` in the snapshots. The row's `resolved_model` equals the model at completion, and `replaced:false` holds because the same agent id carried the fallback.
- **Report:** The spec path `.ufo/waves/round-21/w2/Section0001.md` exists, and so does the mark `sections/1.json`. Both have mtime 09:51, which matches the completion snapshot. Both the callback output and the report begin with the literal word `partial`. That word is the review **verdict** (the probation suffix is unverifiable; the mark records `verdict:"unverifiable"`, `blocking_gaps:1`, `wrong_expectations:0`). It is not a claim about how far execution got. The report claims finished scoped work ("No mutation recipe, test suite, or runtime check was executed").
- **Verdict:** Callback, registry, and report agree. **Counterexample risk:** a gate or reviewer that keyed on the report or callback text "partial" would wrongly mark this seat dead, which would make the completed count 37 instead of 38.

### Section0006 (w2): failed status agrees; provider attribution contradicts the callback

- **Registry vs. row:** The ids match (`TameshiR21.Section0006`) and the role is `reviewer` everywhere. `dispatch2-attempt-01.json` shows `modelRole m_zfl`.
- **Callback:** The raw retained task-result in `wait2-recovered-13.json` is `status="failed (exit 1)" duration="13m42s"`, with output `[zai/glm-5.3-flash] Retry budget exhausted after 5 retries: 429 Rate limit reached for requests (type=1302)`. The seat was `running` in snapshots 01–12. The row's `failed` status agrees.
- **Contradiction:** The final row has `provider:"codex"`, and its `last_error` is a placeholder ("Original failure retained in delivered callback; not replaced.") rather than the callback error. The earlier `original-outcomes2.json` had `provider:"see-retained-result"`. The corrected and final files changed it to `codex`, which conflicts with the callback (zai) and with the row's own `resolved_model: zai/glm-5.3-flash:max`. As a result, `provider_counts_dead` in the final file shows `codex:50, zai:6`, matching a row-derived group count. With callback attribution it would be `codex:49, zai:7`. The totals (dead 80, completed 66, seats 146) are unaffected.
- **Report:** The spec path `.ufo/waves/round-21/w2/Section0006.md` is **absent**, and so is `sections/6.json`. The row has `report:null`.
- **Verdict:** The failed status, null report, and absent file are consistent, and there is no partial report present. The provider field is wrong.

## Wider context (not relitigated)

`original-outcomes2.json` (40/35) differs from the corrected file (38/37) in exactly two status rows: `ProfileBashTsukuroiCensus` and `V01WitnessTests`, both changed from completed to failed. Neither is in my scope. Both have report files present (mtimes 09:56 and 10:00), which shows that "report file exists" is not a safe success signal.

## Gate recommendation (bounded)

For each row, the accounting gate MUST assert all of the following:

1. `id == registry.members[name].agentId` and `role == registry.members[name].role`.
2. `status ∈ {completed, failed}`, taken from the retained callback's `status` attribute. `failed (exit N)` normalizes to `failed`.
3. `replaced == false`.
4. `failed ⇒ report == null`, and the row counts as dead **even if a file exists at the spec path**.
5. `completed ⇒ report == ` the spec-assigned path.

Report text, including a leading `partial`, MUST NOT influence status.

The smallest safe correction for the found defect is to **keep `provider_counts_dead` out of the C1 claim**, or to derive the provider from the retained callback text instead of the row's `provider` field. If neither is done, the gate would certify the wrong `codex:50 / zai:6` split. The contract already states the bound that retained callbacks are "declared inputs, not authenticated provider telemetry". CN1's callback exists only in derived tables, so no gate can verify its provenance. It should be listed as a declared input, not as evidence.

Impacted axis: calibration. Totals and status are correct for all three identities. The provider attribution for Section0006 is the only contradiction found.
