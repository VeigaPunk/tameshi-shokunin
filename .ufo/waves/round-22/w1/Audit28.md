# Audit28: callback, registry, and report agreement for wave2 Section0314, Section0375, and Section0405

**Verdict: agree. No contradictions.** These three are the correct positive controls. The retained callback status for each one is `completed`. The wave2 registry identity and role match the outcome row. The retained report exists and contains a full review, not a partial stub. The gate should count each of the three as completed because the callback says so, not because the report file exists.

## Scoped population (exactly 3; nothing else audited)

wave2 / `TameshiR21.Section0314`, `TameshiR21.Section0375`, `TameshiR21.Section0405`.

## Inputs (read-only; sha256 at audit time)

| path (relative to tameshi-shokunin) | sha256 |
|---|---|
| `.ufo/waves/round-21/original-outcomes-final.json` | `029fc1e0e93a5d351ffa646fe34ed56bf478d1d3a16d7ce7f0cd2bed86698785` |
| `.ufo/waves/round-21/w2/swarm-registry.json` | `029acd0ed3c2d4a8f0fbdce2958667788e0f8bab212fa3f7b58239ea581f917f` |
| `.ufo/waves/round-21/spec2.json` | `e07159109d91a2fea95a2722a45142a06f41e2e3225e25dbcc05eb375720f6b3` |
| `.ufo/waves/round-21/w2/Section0314.md` | `bcc03d32c4f99188370b4f55b2ba3d431af24bb94b54044d87c62bbca5f10c66` |
| `.ufo/waves/round-21/w2/Section0375.md` | `c9bf1a10cab126a99279642aca067fae52405235715312f04d38f05aa76f85a1` |
| `.ufo/waves/round-21/w2/Section0405.md` | `36eea505a69e540726728b1cd54db75b0bdfc7b6dc3f827b395b726267e7d7aa` |

Also read: `record2.json`, `run2.json`, `wait2-recovered-01..22.json`, `w2/sections/{314,375,405}.json`, `.ufo/evidence/round-22/contract.json`.

## Per-identity rows

| identity | outcomes row (final) | registry `members[name]` | spec2 | callback `<task-result>` status | callback provenance | report | report content | agreement |
|---|---|---|---|---|---|---|---|---|
| `TameshiR21.Section0314` | role reviewer, status completed, `replaced:false`, report `w2/Section0314.md` | kind spawn, agentId `TameshiR21.Section0314`, role reviewer | name Section0314, role reviewer | `completed`, 31m34s | byte-identical (sha256 `fc2daf6c…`) to the first terminal callback in `wait2-recovered-22.json`; `running` in waits 01–21 | exists, 5715 B | full review, verdict no-blocking-gaps; `sections/314.json` verdict `no-blocking-gaps`, 0/0 | **agree** |
| `TameshiR21.Section0375` | role reviewer, status completed, `replaced:false`, report `w2/Section0375.md` | kind spawn, agentId `TameshiR21.Section0375`, role reviewer | name Section0375, role reviewer | `completed`, 9m52s | byte-identical (`a2ea4aaa…`) to `wait2-recovered-03.json`; `running` in waits 01–02 | exists, 4270 B | full review, verdict **blocking** (1 gap, 1 wrong expectation); `sections/375.json` matches | **agree** |
| `TameshiR21.Section0405` | role reviewer, status completed, `replaced:false`, report `w2/Section0405.md` | kind spawn, agentId `TameshiR21.Section0405`, role reviewer | name Section0405, role reviewer | `completed`, 12m52s | byte-identical (`ceee4beb…`) to `wait2-recovered-10.json`; `running` in waits 01–09 | exists, 6463 B | full review, verdict no-blocking-gaps (2 non-blocking wrong expectations); `sections/405.json` matches | **agree** |

`original-outcomes2.json` and `original-outcomes2-corrected.json` contain the same id, role, status, report, and `replaced` values for all three. None of the three changed status between the outcome versions.

## Observations that matter for calibration

1. **Not partial.** Each callback opening tag says `status="completed"`, and each one is the terminal transition in the recovered waits. Every earlier sighting says `running`, and no `failed` value appears for any of the three. Each report contains a full located review with commands, and each section JSON matches its callback's verdict.
2. **The review verdict is separate from the seat status.** Section0375 completed with verdict `blocking`. That verdict is review content, not a dead seat. A gate that turns a `blocking` verdict into a non-completed seat would undercount.
3. **Callbacks have inconsistent trailers.** Section0314's callback ends with a `Report:` line, but Section0375 and Section0405 name the report only in prose. spec2 prompts for these seats contain no `Report:` path. They only require `w2/sections/<n>.json`, and the `.md` path comes from the registry `reportDir` (`.ufo/waves/round-21/w2`) plus the member name. **[INFERENCE]** A gate that requires a parsed `Report:` trailer as proof of completion would wrongly reject two of these three positive controls.
4. **Provenance limit.** Matching bytes between the final outcomes file and the recovered waits show that the retained data is internally consistent. They do not authenticate provider telemetry. This matches the contract bound "retained callbacks are declared inputs, not authenticated provider telemetry".
5. **Out of scope, not checked here.** Wave2 totals (`seats 75, completed 38, dead 37`) and the file-wide status count (66 completed, 80 failed across all rows) were observed but not reconciled.

## Bounded gate recommendation

For each of these three rows, the accounting gate should assert all of the following, and nothing beyond them:

- `row.id == registry.members[row.name].agentId`
- `row.role == registry.members[row.name].role`
- `row.status ∈ {completed, failed}`, and `row.status` equals the `status` attribute in the opening tag of `row.actual_result`, whose `id` attribute equals `row.id`
- `row.replaced == false`

The row should count as completed only through that callback status. Report existence, report text, the review verdict (`blocking` / `no-blocking-gaps`), and a `Report:` trailer should never be used to set or override status. This makes Section0314, Section0375, and Section0405 positive controls: they are counted completed, while a failed row that has a report (predicate `failed-with-report-counted-completed`) is still rejected.

No tools were installed. No checks, builds, or tests were run. This file is the only write.
