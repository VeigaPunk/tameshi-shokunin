# Audit29 — round-21 wave-2 seats Section0668 / Section0827 / Section0933

Lane: connector, read-only. Population is exactly three frozen identities; no other seat is assessed.
No tools installed; no checks, builds, or counts run. All paths relative to `tameshi-shokunin/`.

## Verdict

All three seats agree on identity, role, and `replaced=false` across the outcomes file, the wave-2 registry, the spec, the record, and the round-22 bundle. Status is consistent: 0668 and 0827 failed, and 0933 completed. Report presence matches status: neither dead seat has a report file or a section-evidence file. One provenance contradiction exists. Section0827's `provider` and `last_error` text changed across three outcome versions. Neither dead seat's error text is backed by a retained wave-2 callback snapshot.

## Per-identity rows

| Seat | outcomes-final (status / report / replaced) | registry `w2/swarm-registry.json` | report on disk | callback evidence | agreement |
|---|---|---|---|---|---|
| Section0668 | `failed` / `null` / `false` (`original-outcomes-final.json:713-721`) | `agentId=TameshiR21.Section0668`, `role=reviewer` (`:71-79`) | none: no `w2/Section0668.md`, no `w2/sections/668.json` | No retained terminal callback. Absent from all 20 `wait2-recovered-*.json`. Last retained state is `pending` (`dispatch2-attempt-01.json:127-135`). | Identity, role, status, and report agree. **Error provenance unverified.** |
| Section0827 | `failed` / `null` / `false` (`:723-731`) | `agentId=TameshiR21.Section0827`, `role=reviewer` (`:80-88`) | none: no `w2/Section0827.md`, no `w2/sections/827.json` | No retained terminal callback. Absent from all 20 wait snapshots. Last retained state is `pending` (`dispatch2-attempt-01.json:144-152`). | Identity, role, status, and report agree. **Provider/error drift (see contradiction 1).** |
| Section0933 | `completed` / `.ufo/waves/round-21/w2/Section0933.md` / `false` (`:733-741`) | `agentId=TameshiR21.Section0933`, `role=reviewer` (`:89-97`) | `w2/Section0933.md` plus `w2/sections/933.json` (verdict `blocking`, 6 blocking gaps, 3 wrong expectations) | Retained terminal callback `status: completed`, `durationMs 1343157` (`wait2-recovered-17.json:44-50`). Matches `actual_result` `duration="22m23s"` in outcomes-final. | Full agreement: callback, row, registry, report, and evidence JSON. |

Cross-file membership:
- Spec: `spec2.json:64-84`. Name, `role=reviewer`, and `axes=[calibration]` match for all three.
- Record: `record2.json:72-97` duplicates the registry exactly.
- Run file: `run2.json:89-115` holds the pre-spawn plan (`agentId: null`). It assigns report paths `w2/Section0668.md`, `w2/Section0827.md`, and `w2/Section0933.md` (`:783-795`).
- Round-22 bundle: `bundle.json:941-953` (membership) and `:1333-1351` (status rows) match outcomes-final. The bundle's `reports` list includes `Section0933` (`:1815`) and excludes 0668 and 0827.

## Partial report versus completed callback

- 0668 and 0827: no report, partial or otherwise, exists. Neither the wave-2 directory nor `sections/` holds a file for these seats. Report existence therefore cannot rehabilitate them here. Their dead status rests only on the outcomes row, because no raw failure callback was retained.
- 0933: the report's first line claims completion ("done — Section 933 audit complete; verdict: blocking"). That claim is corroborated independently by the retained `completed` callback. Completion credit comes from the callback, not from the file.
- 0933 model fallback under one identity: `wait2-recovered-01.json:299-327` shows `resolvedModel: zai/glm-5.3-flash` with `state: "fallback"`. `wait2-recovered-15/16/17` show `openai-codex/gpt-6-luna:max` through completion. The agent ID never changed, so `replaced=false` is consistent with seat-level replacement semantics. A gate reading only `replaced` cannot see a model fallback inside the seat. [INFERENCE] The contract counts replacement per seat, so this is not a violation.

## Contradictions

1. **Section0827's provider and error text drifted while its status stayed `failed`:**
   - `original-outcomes2.json:96-97`: `provider: "see-retained-result"`, `last_error: "Original failure retained in delivered callback; not replaced."`
   - `original-outcomes2-corrected.json:97-98`: `provider: "codex"`, same placeholder `last_error`.
   - `original-outcomes-final.json:729-730`: `provider: "zai"`, `last_error: "Retry budget exhausted after 5 retries: 429 Rate limit reached for requests; Rate limit reached for requests (type=1302)"`.

   The `last_error` placeholder cites a "delivered callback", but no retained wave-2 snapshot contains a callback for 0827. The final `type=1302` wording appears verbatim in retained callbacks for other seats (for example `wait2-recovered-13.json:72` for Section0006), never for 0827. [INFERENCE] The final 0827 error text may be reconstructed or harmonized rather than transcribed. The status itself is not contradicted.
2. **Section0668's error text has no retained backing.** The string "Codex is at capacity" appears in `.ufo/` only in outcome files (round-20 and round-21) and `round-22/w1/Audit52.md`. It appears in no wave-2 wait snapshot.
3. Not a contradiction: `run2.json` has `agentId: null` for all three seats because it is the pre-dispatch plan. The bound identities appear only after spawn, in the registry and record.

## Gate recommendation (bounded)

For these identities, the accounting gate should assert only fields that agree across the declared inputs:

- `id == registry.agents[name].agentId == "TameshiR21." + name`.
- `role` equals the registry role equals `reviewer`.
- `replaced == false`.
- `status` is in the enum.
- Coupling between status and report:
  - A `failed` row must have `report == null`. A non-null report on a failed row must reject, not credit.
  - A `completed` row's `report` must equal `.ufo/waves/round-21/w2/<name>.md`.
- Wave-2 `completed` must equal the count of `status == "completed"` rows. It must never be derived from the bundle's `reports` list or from report files on disk.

The gate should neither validate nor rely on `provider` or `last_error`. Contradiction 1 shows they are unstable across snapshots and have no callback backing for 0668 or 0827. The gate cannot authenticate them, as the contract already bounds: "retained callbacks are declared inputs, not authenticated provider telemetry". Making the gate depend on them would turn harmonized annotations into false authority.

Affected axis: calibration, which improves because dead-seat evidence is not overstated. No other axis is harmed, since the predicate set in `evidence/round-22/contract.json` already covers status, registry identity, and replacement.

Out of scope, observation only: the bundle's `reports` list (`bundle.json:1840`, `:1849`) names `ProfileBashTsukuroiCensus` and `V01WitnessTests`. Both have retained `failed` callbacks (`wait2-recovered-11.json:227`, `wait2-recovered-07.json:444`). This is the exact pattern the `failed-with-report-counted-completed` predicate targets. It was not audited here.

## Suggested verification (for L1)

Confirm that the gate fixture for `failed-with-report-counted-completed` sets a failed row's `report` to non-null and expects rejection. Confirm that no gate field reads `provider` or `last_error`.
