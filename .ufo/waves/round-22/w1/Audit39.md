# Audit39: wave2 KillMB07 / KillMB08 / KillMB09 callback and registry agreement

Verdict: **agreement, with one provenance gap.** All three identities agree on identity, role, status, report path and `replaced=false` across the outcome file, the registry, the assignments, the spec and the delivered callbacks. However, the delivered `completed` callbacks are **not persisted anywhere in the repository**: the three outcome rows have no `actual_result` body, and no repository file contains their `task-result`. The only callback evidence is in the parent session transcript outside the repository. Nothing here relitigates the round-21 claims.

- Axis: **calibration**. A report file must not stand in for a callback, and an unpersisted callback must not be presented as gate-verifiable.
- Scope: exactly the three frozen identities named below. Nothing else was opened for judgment.
- Mode: read-only. No checks, builds, tests or git mutations were run. No tools were installed or updated.

## Scoped population

| name | frozen identity | frozen status |
|---|---|---|
| KillMB07 | `TameshiR21.KillMB07` | completed |
| KillMB08 | `TameshiR21.KillMB08` | completed |
| KillMB09 | `TameshiR21.KillMB09` | completed |

## Inputs and digests (SHA-256, observed at audit time)

| Input | SHA-256 |
|---|---|
| `.ufo/waves/round-21/original-outcomes-final.json` | `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` |
| `.ufo/waves/round-21/w2/swarm-registry.json` | `029acd0ed3c2d4a8f0fbdce2958667788e0f8bab212fa3f7b58239ea581f917f` |
| `.ufo/waves/round-21/spec2.json` | `e07159109d91a2fea95a2722a45142a06f41e2e3225e25dbcc05eb375720f6b3` |
| `.ufo/waves/round-21/record2.json` | `0893967687ac2a9b331cd50b953f97a56b81c334a228e3bca445c3e82127eb59` |
| `.ufo/waves/round-21/run2.json` | `8dcdbbddd89d773d5a5ddadb8dffca052b246b818ea0d170f31710d9c59f3922` |
| `.ufo/waves/round-21/dispatch2-attempt-01.json` | `3c50b0fa50e67d5d6a1e626982963b4b7b129b72f83731360934abd90122fc40` |
| `.ufo/waves/round-21/w2/KillMB07.md` | `3099a234ecbd3994bf4f7ac2f86737bee483bb183c00ae0709c5529280aa776b` |
| `.ufo/waves/round-21/w2/KillMB08.md` | `3cffbd31a2eca8f4bc39f8cddcc04765f2ded30e6eeee394272f4dba66be9236` |
| `.ufo/waves/round-21/w2/KillMB09.md` | `fdb72a2ef7b0138e8dbced28e46208d99e46b97beadaea52b2e40e978a66d5fd` |

Out-of-repository callback carrier. This is a read-only session transcript, not a repository input and not authenticated provider telemetry:

- `~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-baa6-76c9-b209-ce1123c6cc22/TameshiR21.jsonl`, which contains L1's delivered callbacks.
- Per-seat transcripts `TameshiR21/TameshiR21.KillMB0{7,8,9}.jsonl`:
  - KillMB07: `07ae1840…4086c`
  - KillMB08: `85a02cb6…46c2`
  - KillMB09: `806a11d2…029c`

## Per-identity agreement

Every source below agrees for all three seats on:

- identity `TameshiR21.KillMB0N`
- role `mutation-tester`
- report path `.ufo/waves/round-21/w2/KillMB0N.md`
- `replaced: false`

| Identity | Outcome row (`original-outcomes-final.json`) | Registry (`w2/swarm-registry.json`) | Assignment / spec | Delivered callback (session transcript) | Report |
|---|---|---|---|---|---|
| `TameshiR21.KillMB07` | lines 978-985: `status: completed`; **no `actual_result` or `resolved_model` field** | lines 327-336: `kind: spawn`, same agentId and role | `assignments2.json:37` same id; `spec2.json:292-293` same role | exactly 1 `task-result … status="completed" duration="3m5s"`; output opens `Done — MB07 genuinely discriminated; frozen verdict KILLED` | exists, mtime 09:32:38 -0300. It claims completed execution: opens `Verdict: done`, says "The assigned MB07 probe is complete", and ends with a `Report:` trailer |
| `TameshiR21.KillMB08` | lines 986-993: `status: completed`; no `actual_result` | lines 337-346: same agentId and role | `assignments2.json:38`; `spec2.json:301-302` | exactly 1 `status="completed" duration="2m36s"`; output opens `Done — MB08 genuinely discriminated` | exists, mtime 09:32:06. Opens `# done — MB08 genuinely discriminated`, gives a final verdict, ends with a `Report:` trailer |
| `TameshiR21.KillMB09` | lines 994-1001: `status: completed`; no `actual_result` | lines 347-356: same agentId and role | `assignments2.json:39`; `spec2.json:310-311` | exactly 1 `status="completed" duration="2m41s"`; output opens `done — MB09 genuinely discriminated` | exists, mtime 09:32:14. Opens `done — MB09 is genuinely discriminated`, ends with a `Report:` trailer |

The timing is consistent with each callback closing after its report was written:

- The registry `createdAt` is `2026-10-21T12:29:56.575Z`, which is 09:29:56 -0300.
- The reports were written 2m10s to 2m42s after that.
- The callback durations are 2m36s to 3m5s.

Each verdict is therefore a callback status, not a status inferred from the report. Here the report and the callback happen to agree. None of these three is a partial report hiding a dead seat, and none had a dead callback that a report could rehabilitate.

## Contradictions and non-contradictions

1. **Provenance gap (real).** For these rows, `status: completed` in the repository rests only on the L1-authored row. The row carries `report != null` but no persisted callback body.
   - Other wave2 rows do carry one. For example, `Section0001` at lines 640-649 has `resolved_model` and an `actual_result` holding the full `task-result`.
   - No `.ufo/waves/round-21/wait2-recovered-*.json` file mentions KillMB07-09. Those snapshots cover non-auto-delivered results only.
   - A repository-wide search for `task-result id="TameshiR21.KillMB0[789]` returns nothing.
   - So a gate that reads only repository inputs cannot tell these three `completed` rows apart from "report exists, therefore completed". This is the exact failure the round-22 claim targets. It is a missing-evidence problem, not a wrong status.
2. **Not contradictions (temporal snapshots):**
   - `run2.json:345-372` has `agentId: null`. This is a pre-spawn plan.
   - `dispatch2-attempt-01.json` indices 35-37 have `status: pending` with `toolCount 0`. This is the spawn-time progress snapshot.
   - Neither is a terminal status. A gate must not treat either as the outcome, and must not flag either as a mismatch.
3. **Not a contradiction:** the registry has no status field (`ufo-swarm-registry-v1` members hold kind, agentId, role, item and axes only). Registry agreement is therefore identity and role only; status must come from the callback.
4. **Bound (from the contract):** the transcript callback is a declared, unauthenticated carrier. Its agreement here is corroboration, not provenance (`contract.json` bounds[0]).

## Gate assertion for these identities

For each of the three names, the accounting gate must assert all of the following:

- `outcome.id == registry.members[name].agentId == assignments2[name]`
- `outcome.role == registry.members[name].role == spec2[name].role == "mutation-tester"`
- `outcome.status ∈ {completed, failed}` (the exact enum)
- `outcome.status` equals the status token parsed from a **persisted** callback record bound to the same id
- `replaced == false`
- the report path equals `registry.reportDir + "/" + name + ".md"`

Report existence and report text must be neither necessary nor sufficient for `completed`.

## Bounded recommendation (one move)

Make the persisted callback status token the only source of `completed`. In practice:

- Require each outcome row to carry the retained `task-result` header, either as `actual_result` (the form `Section0001` already uses) or as a digest-pinned callback file.
- Compare the row's `id` and `status` against that header.
- Reject a row that has `status: completed` and `report != null` but no persisted callback. This reuses the existing `failed-with-report-counted-completed` and `false-completion-count` predicates instead of adding a new one.

Under that rule, KillMB07-09 **currently fail closed** on repository inputs alone. They become admissible once L1 persists the three already-delivered headers into a declared round-22 input. That persisting is L1's action; this audit does not write it.

- Affected axes: calibration improves, and operability is unharmed because the data already exists in the transcript.
- Risks: the transcript is mutable and unauthenticated. Persisting it only pins bytes; it does not prove the provider emitted them. Rows such as KillMB03-06 and KillMB10-12 probably have the same gap [INFERENCE: their rows at lines 946-1017 also lack `actual_result`; not audited here].
- Suggested verification for L1: a fixture in which a row has `status: completed` and an existing report but no callback record, which must be rejected; plus a re-check that these three rows pass once their headers are persisted.

Tools installed/updated: none.

Report: .ufo/waves/round-22/w1/Audit39.md
