verdict: done

# Audit27 — wave2 Section0017 / Section0131 callback vs registry vs report

Scoped population: exactly two frozen wave2 identities, `TameshiR21.Section0017` and `TameshiR21.Section0131`. Nothing else was audited. I only read files; nothing was executed, installed, or edited apart from writing this report.

## Rows

| Identity | Outcome row (final) | Registry/spec/assignment | Retained callback | Report on disk | Agreement |
|---|---|---|---|---|---|
| `TameshiR21.Section0017` | `status: failed`, `report: null`, `replaced: false`, `provider: codex`, `role: reviewer` (`original-outcomes-final.json:662-671`) | member `Section0017` → `agentId TameshiR21.Section0017`, `role reviewer`, `kind spawn` (`w2/swarm-registry.json:26-34`, `record2.json:27-35`); spec item role reviewer (`spec2.json:23-30`); `assignments2.json:4` | **None retained as a raw artifact.** Dispatch shows only `status: pending` (`dispatch2-attempt-01.json:42-48`). It is absent from every `wait2-recovered-*.json` (01–20), including the 20-entry "Still Running" list in `wait2-recovered-01.json:2`. The failure text appears only in the derived outcome files (`original-outcomes2.json:30-38`, `-corrected.json:31-39`, `-final.json:662-671`). | No `w2/Section0017.md` and no `w2/sections/17.json` (glob of `w2/` found neither), although the trailer assigned `.ufo/waves/round-21/w2/Section0017.md` (`dispatch2-attempt-01.json:49`). | Identity, role and membership agree. Status `failed` agrees with the missing report and missing evidence mark. **Uncertain:** the failure reason and provider attribution can't be traced to a retained callback in round-21. The row has no `resolved_model` or `actual_result` keys, unlike `Section0006` (`-final.json:650-661`). |
| `TameshiR21.Section0131` | `status: completed`, `report: .ufo/waves/round-21/w2/Section0131.md`, `replaced: false`, `resolved_model openai-codex/gpt-6-luna:max`, `role: reviewer` (`-final.json:672-681`) | member `Section0131` → `agentId TameshiR21.Section0131`, reviewer (`w2/swarm-registry.json:35-43`, `record2.json:36-44`); spec role reviewer (`spec2.json:31-37`); `assignments2.json:5` | `wait2-recovered-04.json:74-104`: `status: completed`, `durationMs 620274`, `resolvedModel openai-codex/gpt-6-luna:max`, `resultText` is `<task-result … status="completed" duration="10m20s">`. Running in recovered-01..03 (e.g. `-01.json:175-203`). The outcome `actual_result` is byte-identical in substance to `resultText`. | `w2/Section0131.md` exists, along with `w2/sections/131.json` (`start 131`, `end 245`, `verdict "blocking"`, `blocking_gaps 2`, `read_rev 790abd21…`). The report path matches the assigned trailer (`dispatch2-attempt-01.json:66`). | Callback, registry, spec, outcome row and report all agree on identity, role, status and report path. Duration 620274 ms matches 10m20s, and the model matches. |

## Partial-report vs completed-callback distinction

- **Section0017:** there is no report and no partial artifact, so nothing exists that could rehabilitate it. Its `failed` status rests only on the outcome-file assertion. I found no raw callback in round-21 to cross-check it against. `[INFERENCE]` It is absent from the first recovered snapshot's running list, which fits an early provider death, but absence isn't proof of a failure callback.
- **Section0131:** the report text opens with `verdict: blocked` (`Section0131.md:1`), and the callback says "**Verdict: blocked**". That word is the *content* verdict of the section audit, in the spec's `done/partial/blocked` vocabulary. It is not the seat's status. The seat status is `completed`, taken from the callback's `status` attribute. The evidence mark uses a different enum (`"blocking"`, `sections/131.json:6`). The same hazard appears in `Section0001`: its output says `partial` but its status is `completed` (`-final.json:648`).

## Contradictions / hazards

1. **Content verdict vs seat status (Section0131):** a gate that reads "blocked" or "partial" from report or callback text as accounting status would wrongly count a completed seat as failed. A gate that reads report existence as success would get this seat right only by coincidence.
2. **No raw callback provenance for Section0017:** its `last_error` can't be checked against any retained wait or callback file in round-21. This matches the contract bound "retained callbacks are declared inputs, not authenticated provider telemetry" (`round-22/contract.json:18`).
3. **Outcome-row schema is heterogeneous:** failed rows sometimes carry `resolved_model`/`actual_result: null` (`Section0006`) and sometimes omit them (`Section0017`). A strict schema gate must allow both forms or require one, but must not use key presence as a status signal.
4. Minor: `Section0131.md:30` ends with a bare path line, which looks like a trailer echo. It has no effect on accounting.

## Bounded gate recommendation

For these two identities, the accounting gate must assert:
- the outcome `status` is in the enum and equals the retained callback `status` attribute where a callback exists;
- the identity and role equal `w2/swarm-registry.json` member `agentId`/`role`;
- `replaced == false`;
- completed rows have a `report` equal to the assigned trailer path and the file exists;
- failed rows have `report == null`, and the file existing at the assigned trailer path does not change the status.

Concretely, `Section0017` must stay counted in wave2 `dead` (37), and `Section0131` must stay counted in `completed` (38). The status must never be derived from report presence or from `verdict:` text. This maps onto the contract predicates `failed-with-report-counted-completed`, `registry-id-mismatch` and `unknown-status`. Where no raw callback is retained (`Section0017`), the gate should label the row "declared failed, callback not retained" rather than "callback-verified".

No tools were installed or updated.
