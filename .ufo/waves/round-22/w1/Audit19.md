done — all three identities agree as `completed` across the spec, the wave-1 registry, the final outcome rows, the harness callbacks, and the retained reports. One calibration hazard: RV12's verdict line is `partial` while its job status is `completed`.

# Audit19 — wave-1 RV11/RV12/RV13 callback, registry and report agreement

Axes: calibration (primary), provenance, identity.
Scope: exactly three frozen identities, all wave 1:
`TameshiR21.RV11CensusSources-3`, `TameshiR21.RV12F5Definition-3`, `TameshiR21.RV13PriorKills-3`.
This is a read-only audit. No tools were installed, no checks or builds were run, and no git, jj or index state was touched. Only `sha256sum`, `ls`/`find`, `rg` and read-only python JSON parsing were used.

## Inputs (sha256)

| Path (lane-relative unless absolute) | sha256 |
|---|---|
| `.ufo/waves/round-21/original-outcomes-final.json` | `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` |
| `.ufo/waves/round-21/w1/swarm-registry.json` | `7756c3b1ff7fdd6f20f4db2e0f2652742f899c945c6210756092061795a105b2` |
| `.ufo/waves/round-21/spec1.json` | `f78fe7472ed8243d46e23ca29f1bff34e646ff47832093fee815f858c22317af` |
| `.ufo/waves/round-21/assignments1.json` | `812af7c837a5eafd92c0a213e02b34406842424d920fb1e32288f368752fd9aa` |
| `.ufo/waves/round-21/record1.json` | `9ca4efc44df34131721de3cdc96779315c88c81f2ba0c347483a1f18ee7b54b0` |
| `.ufo/waves/round-21/w1/RV11CensusSources.md` | `ec4dbc4ea41bca9dcd1e912079a85f2911edf268142febfad17e7f40e1c29b4b` |
| `.ufo/waves/round-21/w1/RV12F5Definition.md` | `72ceaaff3ded734b28f521ab7c0a7c4fd8e7c414d5e417566cd1523c292834a0` |
| `.ufo/waves/round-21/w1/RV13PriorKills.md` | `aa06f549f1961d39c81bb7dcd25c158862c2490e07b632572a5181fd61133620` |
| `.ufo/evidence/round-22/bundle.json` (read only for context) | `dfb1027f80be935fe781ccb8c47d89639a88a9eff6e05d1b45b2a7a61845c18e` |
| `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-baa6-76c9-b209-ce1123c6cc22/TameshiR21.jsonl` (parent transcript, callbacks) | not hashed; it is still live, with mtime 10:25 |
| same session dir `TameshiR21/TameshiR21.RV11CensusSources-3.jsonl` | `e790e494d595aa07fd4a67b0d4f8fffbd57a8b69deb10fb6451bbade11fd17f2` |
| same session dir `TameshiR21/TameshiR21.RV12F5Definition-3.jsonl` | `1ff2af7d9054187b88ce368d0dd36d3aedbf8917fdbb03e208e8adda1aa22e8b` |
| same session dir `TameshiR21/TameshiR21.RV13PriorKills-3.jsonl` | `24baede8ccccfc632cbef4ba48e04ca1a515cc7a19906e551dfc55342470e5e2` |

## Per-identity rows

The same facts hold for all three identities:
- The spec (`spec1.json` items), `assignments1.json`, `record1.json` and `w1/swarm-registry.json` all have one member with `kind=spawn`, `role=reviewer`, and the exact `agentId`.
- `original-outcomes-final.json` `wave1.rows` has exactly one row per name, with matching `id`, `role=reviewer`, `status=completed`, and `report=.ufo/waves/round-21/w1/<name>.md`.
- None of the three appears in the wave-2 registry or in `wave2.rows`.
- The persisted `dispatch-attempt-03.json` progress shows only `status: pending`. It is a dispatch-time snapshot, not a callback.

| Identity | Harness callback (parent `TameshiR21.jsonl`) | Child transcript termination | Report bytes vs write call | Report's own verdict line | Agreement |
|---|---|---|---|---|---|
| `TameshiR21.RV11CensusSources-3` | Line 489, `async-result` at 2026-10-21T12:12:12.998Z: `<task-result … agent="reviewer" status="completed" duration="10m44s">` and `jobs[].status="completed"`, `durationMs=644760`. Exactly one task-result for this id. | Final assistant message at 12:11:49Z has `stopReason=stop`, then `session_exit` with `reason=dispose, kind=normal`. Earlier 429 rate-limit errors were retried in-session, not terminal. | One `write` call (3582 B), tool result "Successfully wrote 3582 bytes", `isError=false`. The payload is byte-equal to the disk file (sha `ec4dbc4e…`). | `**Verdict: done — AGREE.**` The report records the exact commands it ran with exit 0. | Full agreement. |
| `TameshiR21.RV12F5Definition-3` | Line 459, `async-result` at 12:10:13.154Z: `status="completed" duration="8m56s"` and `jobs[].status="completed"`, `durationMs=536483`. Exactly one task-result. | Final message at 12:10:00Z has `stopReason=stop`, then `session_exit` with `dispose/normal`. There was a mid-run model change and re-init after 429s at 12:06:39Z, and the run continued afterwards. | One `write` call (6672 B), `isError=false`. Byte-equal to disk (sha `72ceaaff…`). | The first line is `partial — the seven-profile matrix is a defensible extension, but the nine-surface population and receipt acceptance do not yet faithfully establish the F5 move.` The callback output also says `**Partial —**`. | Callback, registry and outcome agree on `completed`. **Divergence:** the report's verdict token is `partial`. See C1. |
| `TameshiR21.RV13PriorKills-3` | Line 508, `async-result` at 12:14:37.764Z: `status="completed" duration="12m30s"` and `jobs[].status="completed"`, `durationMs=750045`. Exactly one task-result. | Final message at 12:13:34Z has `stopReason=stop`, then `session_exit` with `dispose/normal`. A model change and re-init after 429s at 12:09:27Z, then continued. | One `write` call (6300 B), `isError=false`. Byte-equal to disk (sha `aa06f549…`). | `done`. The report records its git commands with exit 0 and states that it did not rerun the ruler. | Full agreement. |

Commands (exit 0 for all):
- `sha256sum` on the inputs above.
- A python scan of the parent transcript for `task-result id="TameshiR21.<id>"` and for `"jobId":"TameshiR21.<id>","type":"task","status":…`. It found exactly one hit per id, all `completed`, and zero `failed`, `cancel`, `aborted` or `error` mentions within 120 characters of each id.
- A python comparison of each child transcript's `write` tool-call `content` against the disk report. All three are byte-equal.

## Contradictions and hazards

**C1 — RV12: a `partial` verdict on a `completed` job (calibration).**
The wave-1 report contract (`spec1.json` context) says: "verdict line first (done / partial / blocked)". RV12 chose `partial`, but its job status is `completed`. In context, `partial` grades the subject under review: the C2 contract only partly operationalises F5. It does not say the review was cut short. RV12 answers every acceptance item: holds/fails with line refs, plus recommended bounds wording (the "Honest Core statement" section). It also names one deliberate scope limit: it was a frozen-document review and ran no selftests.

The spec, however, overloads one token for two meanings: subject verdict and execution completeness. A gate or reader that keys on the report's first-line token would score RV12 as a partial execution, which is a false negative. In the mirror case, a provider-dead seat whose partial report starts with `done` would be read as a completion, which is the false positive this round targets. Both errors share a cause: deriving job state from report text.

**C2 — `replaced` is absent from the source for completed wave-1 rows (provenance).**
In `original-outcomes-final.json`, all 28 wave-1 `completed` rows, including these three, have no `replaced` key. All 43 failed wave-1 rows and all wave-2 rows carry `replaced: false`. The round-22 `bundle.json` emits `replaced: false` for these three. For them, that value is therefore derived or defaulted, not copied from the outcome source.

I found no evidence of replacement. Each id has a single `-3` seat, a single task-result, and no wave-2 occurrence. A gate that "validates replacement=false" against the outcome source would be validating a value the source does not contain for these rows.

**C3 — the dispatch snapshot is not outcome evidence.**
`dispatch-attempt-03.json` lists all three as `pending`, with an empty `results` list. Only the parent transcript's `async-result` notices carry the terminal `completed` status. Those are harness-authored, but the lane gate cannot authenticate them. This matches the stated limit that the gate cannot authenticate callback provenance.

There are no other contradictions. Names, ids and roles are identical across spec, assignments, record, registry, outcome rows and callbacks. The `outcome_source` claim in `original-outcomes1.json`, "report files match all 28 delivered successful identities", holds for these three.

## Gate recommendation (bounded)

For these three identities, the accounting gate should assert:
- Each `(name, id, role)` matches the wave-1 registry member exactly and appears once.
- `status` is the registry-or-outcome enum value `completed`, taken **only** from the persisted outcome row. It must never be derived from report existence, report bytes, or the report's first-line verdict.
- The report path is set iff `status=completed`.
- The totals `wave1 = 71/28/43` hold.

The gate should not read `done/partial/blocked` from the report as job status. RV12 shows a completed job whose verdict is `partial`. Mapping that token to status would misclassify it, and it would let a dead seat's partial report claim `done`.

Smallest safe correction for C2: either persist `replaced: false` explicitly on completed wave-1 rows in a new outcome artifact (existing evidence must not be edited), or have the gate treat an absent `replaced` as a fail-closed error rather than defaulting it to `false`. Which is admissible is for the canonical judge, not this audit, to decide.

[INFERENCE] Reading RV12's `partial` as a subject verdict and not execution status rests on the report text and the fact that it answers every acceptance item. No artifact records RV12's intended meaning of the token.

## Residual uncertainty

- The callbacks are read from the harness parent transcript, which is still being appended. They are retained as plain JSONL that the lane cannot authenticate.
- Child transcripts were read only to check termination and write fidelity. I did not re-judge the substance of their findings, and the round-21 admitted claims were not relitigated.
- No tool installs or updates.
