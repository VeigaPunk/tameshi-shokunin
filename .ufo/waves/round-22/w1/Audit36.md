# Audit36 — round-21 wave2 callback/registry/report agreement (Section1855, Section1925, Section1938)

**Seat:** TameshiR22.Audit36-2 (connector, leaf). Read-only audit; one write (this file).
**Scoped population:** exactly 3 frozen wave2 identities — `TameshiR21.Section1855`, `TameshiR21.Section1925`, `TameshiR21.Section1938`. No other rows judged.
**Axes:** calibration (status claim matches retained evidence), accounting fidelity (identity/role/status agreement across artifacts), provenance honesty (what is and is not authenticatable).
**Tool installs:** none. **Checks run:** none (static reads/greps only).

## Evidence paths (all relative to `tameshi-shokunin/`)

| Artifact | Path | Role for these 3 |
|---|---|---|
| Outcome source | `.ufo/waves/round-21/original-outcomes-final.json` (rows at L913–937; wave2 header L635–638; flag L1369) | Claimed status |
| Outcome predecessors | `.ufo/waves/round-21/original-outcomes2.json` (L280–304), `original-outcomes2-corrected.json` (L281–305) | Identical rows for all 3 (no drift across revisions) |
| Wave2 registry | `.ufo/waves/round-21/w2/swarm-registry.json` (L251–277) | `agentId` + role |
| Spec | `.ufo/waves/round-21/spec2.json` (L224–243) | name + role + prompt (no id field) |
| Assignments / record | `.ufo/waves/round-21/assignments2.json` (L29–31), `record2.json` (L252–275) | name → agentId |
| Dispatch snapshot | `.ufo/waves/round-21/dispatch2-attempt-01.json` (idx 27–29, L466–512) | modelRole; status `pending` (all 75 rows pending, `results: []`) |
| Pre-dispatch run | `.ufo/waves/round-21/run2.json` (L269–290) | `agentId: null` (expected before spawn) |
| Reports | `.ufo/waves/round-21/w2/Section1925.md`, `.ufo/waves/round-21/w2/Section1938.md` | Exist |
| Machine marks | `.ufo/waves/round-21/w2/sections/1925.json`, `.ufo/waves/round-21/w2/sections/1938.json` | Exist |
| Absent | `.ufo/waves/round-21/w2/Section1855.md`, `.ufo/waves/round-21/w2/sections/1855.json` | Glob: 0 matches anywhere under `.ufo/` |

## Per-identity rows

| Identity | Outcome status | Registry agentId / role | Spec / assignments / record / dispatch role | Report on disk | Report claims completed execution? | Agreement |
|---|---|---|---|---|---|---|
| `TameshiR21.Section1855` | `failed`, `report: null`, `replaced: false`, provider `haiku`, `last_error` 429 rate-limit (`retry-after-ms=8412000`) | `TameshiR21.Section1855` / `scribe` | `scribe` everywhere; dispatch `modelRole: m_haiku` (consistent with provider `haiku`) | **None** (no `.md`, no `sections/1855.json`) | n/a | **Agrees.** Dead seat with no partial artifact; nothing exists that could rehabilitate it. |
| `TameshiR21.Section1925` | `completed`, `report: .ufo/waves/round-21/w2/Section1925.md`, `replaced: false`; no `provider`/`resolved_model`/`actual_result` fields | `TameshiR21.Section1925` / `simplifier` | `simplifier` everywhere; `m_composer` | Yes (163 lines) + `sections/1925.json` | Yes — finished audit (verdict `blocking`, 2 blocking gaps, 2 wrong expectations, read_rev `790abd21…`, trailer `Report:` path matches the spec's assigned path). Report verdict and JSON mark agree (`blocking`, 2, 2). | **Agrees on identity/role/report path.** Completed status is *corroborated* by a complete, self-consistent report, but **not authenticated**: no retained callback text exists in the repo or under `~/.omp/agent` (grep 0 matches). |
| `TameshiR21.Section1938` | `completed`, `report: .ufo/waves/round-21/w2/Section1938.md`, `replaced: false`; no provider fields | `TameshiR21.Section1938` / `simplifier` | `simplifier` everywhere; `m_composer` | Yes (120 lines) + `sections/1938.json` | Yes — finished audit (verdict `no-blocking-gaps`, 0 blocking, 2 wrong expectations, read_rev `790abd21…`). Report and JSON mark agree. | **Agrees on identity/role/report path.** Same caveat: completed is asserted only by the L1-authored outcome row. |

## Contradictions / uncertainty

1. **No contradiction for these three.** Identity, role and report path match exactly across outcomes (all three revisions), registry, spec, assignments, record and dispatch. Nobody was replaced (`replaced: false`), and no identity carries a `-N` suffix.
2. **Asymmetric provenance (uncertainty, not contradiction).** Failed rows carry `provider` + `last_error`, which is evidence of a terminal callback. Completed rows (1925, 1938) carry only `status` + `report`, so a report file and a completed status that is otherwise unwitnessed look the same. For these two seats that is benign: the reports are complete, and the marks agree with them. Even so, the persisted artifacts cannot show that `completed` came from a callback rather than from the report's existence. This is the C1 failure mode in miniature, and contract bound 1 ("retained callbacks are declared inputs, not authenticated provider telemetry") already admits it.
3. **Dispatch snapshot is not a callback record.** `dispatch2-attempt-01.json` has `results: []`, and all 75 rows are `pending`. It shows the seats were spawned, not how they ended. Do not use it as a source for terminal status.
4. **Section1855 is the clean negative control.** It is failed, has no report and no mark, and was not replaced. It is the case where `report != null` would be the forbidden rehabilitation signal. For contrast, an out-of-scope row in the same file (`V01WitnessTests`, L1297–1307: `failed` with a non-null `report`) shows that this pattern occurs in the dataset. The top-level flag `partial_report_files_do_not_rehabilitate_failed_jobs: true` (L1369) records the policy. I am not judging that row.

## Gate recommendation (one, bounded)

For each of these identities, the accounting gate should assert a **status-first tuple equality**: `(name, id, role, status, replaced)` from the persisted outcome row must equal `(registry key, registry.agentId, registry.role, enum∈{completed,failed}, false)`, and the completed/dead tallies must be computed from `status` alone, never from `report`/file presence. Concretely:
- Section1855 must count toward wave2 `dead`, and that count must not change if a `w2/Section1855.md` file appears later. Adding such a file to a fixture should leave the totals unchanged, or should be rejected under the `failed-with-report-counted-completed` predicate.
- Section1925 and Section1938 count toward `completed` only because their `status` is `completed`. The gate should treat the report path as an optional pointer and never as evidence for the status.

**Narrow-scope note:** the gate cannot and should not claim that these `completed` statuses are callback-authentic. Doing that would need retained callback payloads, which are absent for completed rows. The honest claim is "outcome rows are internally consistent with the registry and counted by status". Adding provenance fields to completed rows is out of scope for C1; it is listed here only as a residual.

## Verification for L1

- Re-read `original-outcomes-final.json` L913–937 against `w2/swarm-registry.json` L251–277 (exact `agentId`/`role` strings).
- Glob `.ufo/waves/round-21/w2/{Section1855.md,sections/1855.json}` should return 0 files.
- In a negative fixture, add `report` to the Section1855 row (or create the file). The gate's wave2 `completed` must stay 38 and `dead` 37 (header L636–638), or the fixture must be rejected.

Report: `.ufo/waves/round-22/w1/Audit36.md`
