# MalformedDesign — public CLI negative fixtures (four scoped predicates + bool totals)

Seat: `TameshiR22.MalformedDesign-2` (simplifier, leaf). Axis: **calibration**. Scope: design-only; no production edits, no subprocess checks run by this seat.

Report: `.ufo/waves/round-22/w1/MalformedDesign.md`

## Godspeed axes

| Axis | What “better” means here |
|------|---------------------------|
| **Discrimination** | Each fixture maps to one primary stable `finding_ids[]` entry; exit class (0 / 1 / 2) matches CLI contract. |
| **Authority** | Outcomes drive counts; `reports` is artifact inventory only (matches `tools/wave-accounting.py` module doc and `authority` field). |
| **Stability** | IDs are uppercase snake literals emitted by `finding(code, …)` — not stderr prose, not report paths. |
| **Hermetic public CLI** | Each case is `python3 tools/wave-accounting.py --bundle … --expected … --json` in a private temp dir (same shape as `.ufo/evidence/round-22/measure.py`). |
| **No false green** | Fixtures that only add or retain report names must not produce exit 0 or inflate `completed`. |

## Evidence read (frozen inputs)

| Path | Use |
|------|-----|
| `.ufo/evidence/round-22/contract.json` | C1 unit: eight predicates; this seat owns design for four named malformations + bool totals. |
| `.ufo/evidence/round-22/measure.py` | Frozen harness: control bundle, mutations for three of four scoped cases, `(exit, finding_id)` literals. |
| `tools/wave-accounting.py` | Authoritative finding IDs and evaluate semantics (read-only). |
| `.ufo/waves/round-21/original-outcomes-final.json` | Ground truth for callback vs report divergence (e.g. failed + report path). |
| `.ufo/evidence/round-22/before.json` | Census at round open: `tool_present: false` (integrator land state); design targets post-integrate CLI. |

Tool installs/updates: **none**.

## Bundle schema (shared control)

All fixtures share one **control** wave `probe` (verbatim from `measure.py`):

```json
{
  "schema": "wave-accounting-v1",
  "waves": [{
    "name": "probe",
    "members": [
      {"name": "pass", "id": "seat.pass", "role": "reviewer"},
      {"name": "dead", "id": "seat.dead", "role": "critic"}
    ],
    "outcomes": [
      {"name": "pass", "id": "seat.pass", "role": "reviewer", "status": "completed", "replaced": false},
      {"name": "dead", "id": "seat.dead", "role": "critic", "status": "failed", "replaced": false}
    ],
    "reports": ["pass", "dead"],
    "claimed": {"seats": 2, "completed": 1, "dead": 1}
  }]
}
```

**Expected sidecar** (per invoke): `wave-accounting-expected-v1` with `bundle_sha256` of canonical JSON (`sort_keys=True`, indent 2, trailing newline) — same as `measure.encode()`.

**Control acceptance:** exit **0**, `finding_ids == []`, observed `total.completed == 1`, `total.dead == 1`.

**Report non-authority invariant (all cases):** `reports` lists both seats including `dead`. No case may delete `dead` from `reports` to “fix” a mismatch; that would test report editing, not callback accounting.

---

## Fixture 1 — `missing-outcome` → `MEMBERSHIP_MISMATCH`

**Intent:** Registry/membership expects two seats; retained outcomes omit one row (provider-dead or never-callback), while a report artifact may still exist on disk.

**Delta from control:** remove the `dead` element from `outcomes` only. Leave `members`, `reports`, and `claimed` unchanged.

**Primary finding:** `MEMBERSHIP_MISMATCH` with detail containing `missing=['dead']`.

**Expected public CLI:** exit **1**, `"MEMBERSHIP_MISMATCH" in finding_ids`.

**Secondary finding (allowed, not pinned as primary):** `TOTAL_MISMATCH` because observed `dead` count is 0 while `claimed.dead` remains 1. Harness may pin only the membership ID (as `measure.py` does) or add an explicit `finding_ids` superset check; do not require exclusive single-ID output.

**Round-21 anchor:** Most wave1 `failed` rows have `"report": null` (callback-dead, no artifact). Wave2 `ProfileBashTsukuroiCensus` is the opposite stress: `"status": "failed"` with `"report": ".ufo/waves/round-21/w2/ProfileBashTsukuroiCensus.md"` — a gate must not treat the report as completion. This fixture models **missing outcome row**, not that row; integrator should add a separate bundle built from real seat names if binding to r21 bytes.

**Anti–report-derived-success:** With `reports` still `["pass","dead"]`, exit must remain **1**. A gate that equates report presence with a completed outcome would incorrectly pass if it skipped membership check.

---

## Fixture 2 — `duplicate-agent` → `DUPLICATE_AGENT`

**Intent:** Two distinct seat names share one agent id (collision across membership or outcomes).

**Delta from control:**

```text
members[1].id  := "seat.pass"   # was "seat.dead"
outcomes[1].id := "seat.pass"   # align outcome row with duplicated id
```

**Primary finding:** `DUPLICATE_AGENT` (wave `probe`, agent `seat.pass`).

**Expected public CLI:** exit **1**, `"DUPLICATE_AGENT" in finding_ids`.

**Note:** Implementation may emit duplicate `DUPLICATE_AGENT` records (member pass and outcome pass); `finding_ids` dedupes to one sorted entry.

**Anti–report-derived-success:** Do not remove duplicate by dropping a report name or renaming seats only in `reports`. Mutation must be on `id` fields.

---

## Fixture 3 — `unknown-status` → `UNKNOWN_STATUS`

**Intent:** Status string outside `{completed, failed}` — neither alive nor counted dead.

**Delta from control:** `outcomes[1].status := "unknown"` (seat `dead`).

**Primary finding:** `UNKNOWN_STATUS` with detail `dead:unknown`.

**Expected public CLI:** exit **1**, `"UNKNOWN_STATUS" in finding_ids`.

**Secondary:** `TOTAL_MISMATCH` (observed `dead: 0` vs `claimed.dead: 1`) may co-occur; same pinning policy as fixture 1.

**Anti–report-derived-success:** `dead` remains in `reports`; unknown status must not increment `completed` or `dead`. Exit 0 is forbidden even if a markdown report path exists in a real-world bundle adapter.

---

## Fixture 4 — `bool-totals` → `INVALID_INPUT`

**Intent:** `claimed` uses JSON booleans (or other non-int) where evaluate requires three nonnegative integers — schema rejection before invariant findings.

**Delta from control:** replace integer claims with booleans, e.g.

```json
"claimed": {"seats": 2, "completed": true, "dead": false}
```

(or all three bool — any `type(claimed[k]) is not int` triggers the same path).

**Primary finding:** `INVALID_INPUT` (top-level `run()` handler, not wave-scoped `findings[]`).

**Expected public CLI:** exit **2**, `finding_ids == ["INVALID_INPUT"]`, no `waves` summary in result.

**Gap vs frozen harness:** `.ufo/evidence/round-22/measure.py` `CASES` lists eight contract predicates and does **not** yet include `bool-totals`. Recommendation: add a ninth selftest row **or** fold into `--selftest` as `malformed-claimed-type` with literal `(2, INVALID_INPUT)` independent of the eight predicate counter (bool totals is input-shape, not C1 membership predicate).

**Distinction from `TOTAL_MISMATCH`:** Wrong **types** → exit 2 / `INVALID_INPUT`. Wrong **integers** with correct types → exit 1 / `TOTAL_MISMATCH` (see contract predicates `false-completion-count`, `failed-with-report-counted-completed`).

---

## Public CLI contract (pin in selftest)

| Case | `measure.py` name | Expected exit | Expected finding (primary) |
|------|-------------------|---------------|----------------------------|
| control | (baseline) | 0 | (none) |
| missing outcome | `missing-outcome` | 1 | `MEMBERSHIP_MISMATCH` |
| duplicate agent id | `duplicate-agent` | 1 | `DUPLICATE_AGENT` |
| unknown status | `unknown-status` | 1 | `UNKNOWN_STATUS` |
| bool totals | *(proposed)* `bool-totals` | 2 | `INVALID_INPUT` |

**Parse mode:** whole stdout JSON when `--json`; do not use last-line text mode for these cases.

**False positives to reject in selftest:**

1. **Report-only green:** exit 0 when an outcome row is missing but `reports` is full.
2. **Exit without ID:** assert `finding in result["finding_ids"]`, not `returncode != 0` alone (round-15 ReviewUsage criterion B).
3. **Reason substring:** do not match `detail` or `error` text; pin IDs only.
4. **Co-finding flakiness:** treat secondary `TOTAL_MISMATCH` on membership/status cases as allowed superset unless integrator tightens evaluate to single primary code.

---

## Optional persisted fixture layout (integrator)

Recommend committing canonical bytes under:

```text
.ufo/evidence/round-22/fixtures/wave-accounting/
  control/{bundle.json,expected.json}
  missing-outcome/{bundle.json,expected.json}
  duplicate-agent/{bundle.json,expected.json}
  unknown-status/{bundle.json,expected.json}
  bool-totals/{bundle.json,expected.json}
```

`measure.py` should either read these files or generate identical bytes (single source of truth). SHA-256 of each `bundle.json` belongs in expected sidecar.

---

## Bounded recommendations

1. **Integrator (`TameshiR22`):** Add `bool-totals` to public selftest with exit 2 / `INVALID_INPUT`; keep the four scoped mutations aligned with `measure.py` literals.
2. **Do not** derive expected findings from round-21 report file existence or markdown content; only declared `outcomes[].status` and membership sets.
3. **Optional r21 fidelity bundle:** One wave slice with seat `ProfileBashTsukuroiCensus`, status `failed`, report name listed in `reports` — expect `dead` count 1, `completed` unchanged, exit 0 only if `claimed` matches observed (separate from the four malformed negatives).

## Contradictions / uncertainty

- `before.json` records `tool_present: false` at census time; `tools/wave-accounting.py` exists in tree now — this seat did not execute CLI to reconcile.
- Dual findings on `missing-outcome` and `unknown-status` are consistent with current `evaluate()` but may surprise consumers expecting exactly one ID; document as intentional or narrow evaluate later (integrator choice).

Report: `.ufo/waves/round-22/w1/MalformedDesign.md`
