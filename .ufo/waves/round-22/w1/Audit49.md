# Audit49 — wave2 F06 / F07 / F08 callback–registry–report calibration

**Agent:** `TameshiR22.Audit49-2`  
**Scoped population (exactly three):** round-21 wave2 seats `F06Source080Reject`, `F07Source081Precision`, `F08SourceTransitions` as frozen in `original-outcomes-final.json`.  
**Axes:** identity/membership agreement; callback status vs nested `<task-result>`; report presence vs completion claims; contradictions for C1 seat accounting.

**Tooling:** no installs or updates (read-only audit).

**Primary evidence paths**

| Artifact | Path |
|----------|------|
| Outcome source | `.ufo/waves/round-21/original-outcomes-final.json` |
| Wave2 registry | `.ufo/waves/round-21/w2/swarm-registry.json` |
| Wave2 spec | `.ufo/waves/round-21/spec2.json` |
| Assignments | `.ufo/waves/round-21/assignments2.json` |
| Record mirror | `.ufo/waves/round-21/record2.json` |
| R22 contract | `.ufo/evidence/round-22/contract.json` |

---

## Per-identity rows

### F06Source080Reject

| Field | Observed |
|-------|----------|
| **name** | `F06Source080Reject` |
| **id / agent** | `TameshiR21.F06Source080Reject` |
| **role** | `scout` (outcome, spec2, swarm-registry, record2, assignments2 — all agree) |
| **outcome status** | `completed` |
| **replaced** | `false` |
| **report path (outcome)** | `.ufo/waves/round-21/w2/F06Source080Reject.md` |
| **report on disk** | present (verified) |
| **callback (`actual_result`)** | present; nested `<task-result id="TameshiR21.F06Source080Reject" agent="scout" status="completed" …>` matches outer `status: completed` |
| **Report completion claim** | body opens with **Verdict: done — agree, with a boundary caveat**; callback output says “Done.” and cites the report path — not a partial stub |

**Agreement:** registry `agentId`, assignments map, spec `name`/`role`, and outcome row align. Callback-completed seat with a substantive report; report text claiming finished execution is **consistent with** the callback, not a substitute for it.

**Partial vs completed callback:** completed callback; report is full scoped audit, not a partial placeholder.

---

### F07Source081Precision

| Field | Observed |
|-------|----------|
| **name** | `F07Source081Precision` |
| **id / agent** | `TameshiR21.F07Source081Precision` |
| **role** | `scout` (outcome, spec2, swarm-registry, record2, assignments2 — all agree) |
| **outcome status** | `completed` |
| **replaced** | `false` |
| **report path (outcome)** | `.ufo/waves/round-21/w2/F07Source081Precision.md` |
| **report on disk** | present (verified) |
| **callback (`actual_result`)** | present; nested `<task-result … status="completed" …>` matches outer `status: completed` |
| **Report completion claim** | line 1 is `done`; body is a full S081 precision audit with commands section — not a partial stub |

**Agreement:** same cross-artifact identity/role alignment as F06.

**Partial vs completed callback:** completed callback; report self-claims `done` in prose, aligned with callback.

**Note (scope, not accounting contradiction):** F07’s git diff touches overlapping `corpus/SOURCES.md` / lesson territory that F08’s spec assigned to the transitions seat; that overlap does **not** supply F08’s missing report or callback and must not be used to count F08 complete.

---

### F08SourceTransitions

| Field | Observed |
|-------|----------|
| **name** | `F08SourceTransitions` |
| **id / agent** | `TameshiR21.F08SourceTransitions` |
| **role** | `scribe` (outcome, spec2, swarm-registry, record2, assignments2 — all agree) |
| **outcome status** | `failed` |
| **replaced** | `false` |
| **report path (outcome)** | `null` |
| **spec/dispatch report path** | `.ufo/waves/round-21/w2/F08SourceTransitions.md` |
| **report on disk** | **absent** (no file at spec path; repo-wide glob finds no `F08SourceTransitions*` report) |
| **callback (`actual_result`)** | **absent** |
| **last_error** | `429 … rate limit … retry-after-ms=8412000` |
| **provider** | `haiku` |

**Agreement:** membership and failed disposition are consistent across outcome, registry, and spec. No report exists; no report text claims completion.

**Partial vs completed callback:** neither — provider failure with no deliverable report and no `actual_result` task-result block.

**Uncertainty:** none on whether this seat completed; it did not. Overlap from sibling source audits (F05/F07) is not evidenced as F08 execution.

---

## Contradictions

| Check | Result |
|-------|--------|
| Outcome `id` vs `assignments2` / `swarm-registry.agentId` | no mismatch for all three |
| Outcome `role` vs spec/registry | no mismatch |
| Outer `status` vs nested `<task-result status>` (F06/F07) | agree (`completed`) |
| Failed seat with report counted as complete (`failed-with-report-counted-completed`) | **not applicable** — F08 has `report: null` and no file |
| Report-only completion without callback (F08) | **not observed** — no F08 report |
| `run2.json` pre-spawn rows show `agentId: null` | **non-authoritative template**; authoritative membership uses `swarm-registry.json` + `assignments2` + outcomes (agentIds populated there) |

No evidence in scoped artifacts that F08 should be relabeled `completed` from report files.

---

## Bounded gate recommendation (C1 / round-22 contract)

For this three-seat slice, an accounting gate should assert **structural** facts on the frozen outcome snapshot (and matching wave2 registry row), not report prose alone:

1. **Identity:** for each `name`, `outcome.id === assignments2[name] === swarm-registry.members[name].agentId`, and `outcome.role === spec2.role === registry.role`.
2. **Completed seats (F06, F07):** `status === "completed"`, `replaced === false`, non-null `report` path, file exists at repo-relative path, and when `actual_result` is present it contains `<task-result … status="completed">` with the same `id`. Count toward completed **only** when (2) holds; treat report existence as corroboration, not primary authority (per contract: “callback-authoritative seat accounting, not report-file success”).
3. **Failed seat (F08):** `status === "failed"`, `report === null`, expected spec report path absent on disk, no `actual_result` completion block — **exclude** from completed count; classify as provider-dead / incomplete delivery, not “missing-outcome row” (row exists with explicit `failed`).
4. **Provenance limit (explicit):** gate validates persisted fields and digest-stable inputs; it **cannot** authenticate that `actual_result` was provider-telemetry-genuine (stated in round-22 contract bounds).

**Predicate mapping:** F06/F07 support honest `completed` tally if rule (2) is applied; F08 guards against inflating completeness via sibling reports or implied transitions work (`false-completion-count` / overlap rehab risk). No `replacement-seat` signal (`replaced: false` everywhere).

---

## Summary

| Identity | Callback | Report | Calibration read |
|----------|----------|--------|------------------|
| F06Source080Reject | `completed` (nested agrees) | present, claims done | **aligned completed seat** |
| F07Source081Precision | `completed` (nested agrees) | present, claims done | **aligned completed seat** |
| F08SourceTransitions | `failed`, no callback body | none | **aligned dead seat — do not count complete** |

Report: `.ufo/waves/round-22/w1/Audit49.md`
