# CounterThreats — eight-item denominator attack (round 22 w1)

Seat: `TameshiR22.CounterThreats-2` (simplifier, calibration). Read-only audit;
recommendations only. Base: `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`.
Contract: `.ufo/evidence/round-22/contract.json`.

## Axes

| Axis | What this seat protects | Harm if conflated |
|---|---|---|
| **Calibration** | C1 score tracks *callback-authoritative* reconciliation, not artifact counts | Partial Markdown rehabilitates dead seats; calibration rises on file presence |
| **Operability** | Public CLI exists and selftest discriminates predicates | `8/8` claimed while `tools/wave-accounting.py` absent on before branch |
| **Honesty / authority** | Declared retained inputs ≠ authenticated provider telemetry | Gate prose implies cryptographic or independent verification |

Round 21 admission (C1 eighteen-kill operability, C2 F5 nine-profile capability) is **out of scope** for relitigation; this seat attacks only the round-22 **eight-predicate denominator** and its relationship to r21 accounting.

## Three populations (do not merge)

### A — Frozen capability fixture count (`8`)

- **Unit** (contract): `eight frozen malformed or mismatched accounting fixtures rejected by public CLI`.
- **Counter**: `.ufo/evidence/round-22/measure.py` — `CASES` length 8, `total: 8`, synthetic 2-seat probe wave mutated per predicate name.
- **Before receipt**: `.ufo/evidence/round-22/before.json` — `discriminated: 0`, `tool_present: false`, `cases: []`, exit `1`. At the frozen base commit the counter reports **tool absence**, not “eight failed discriminations.”
- **Tool docstring** (`.ufo/evidence/round-22/measure.py:2`): explicitly *not an authenticity claim*.
- **Selftest chain**: `tools/wave-accounting.py --selftest` delegates to the same frozen `measure.py` (`.ufo/evidence/round-22/measure.py` via import).

**What 8/8 means when it lands:** each named predicate produces the expected exit (`1` or `2` for tamper) and stable finding ID on an **isolated temp bundle**, not on the historical r21 JSON.

### B — Actual round-21 seat accounting (`146`, not `8`)

Authoritative terminal population: `.ufo/waves/round-21/original-outcomes-final.json`.

| Scope | Seats | Completed | Dead | Failed ∧ report path |
|---|---:|---:|---:|---:|
| wave1 | 71 | 28 | 43 | **0** |
| wave2 | 75 | 38 | 37 | **2** |
| **total** | **146** | **66** | **80** | **2** |

The two **failed callbacks with retained report artifacts** (status still `failed`, `replaced: false`):

| Seat | Agent id | Report path | Callback status |
|---|---|---|---|
| ProfileBashTsukuroiCensus | `TameshiR21.ProfileBashTsukuroiCensus` | `.ufo/waves/round-21/w2/ProfileBashTsukuroiCensus.md` | `failed` |
| V01WitnessTests | `TameshiR21.V01WitnessTests` | `.ufo/waves/round-21/w2/V01WitnessTests.md` | `failed` |

Superseded file-presence inference: wave2 was once summarized as 40 completed / 35 dead and round total 68/78; corrected rule and rows live in `.ufo/waves/round-21/original-outcomes2-corrected.json` (`rule`: original callback status wins). Narrative erratum: `corpus/lessons/round-21.md` § Outcome-accounting erratum; `LOG.md` Round 21 outcome accounting correction; `SCORECARD.md` § Original-outcome correction.

**Report-file overlap (filesystem, not authority):** `68` Markdown files under `.ufo/waves/round-21/` (`find … -name '*.md' | wc -l`) vs **66** completed callbacks — excess **2** matches the partial-report dead seats, not an eighth synthetic case.

The historical bug class is **one** (count artifacts as completions), with **two** observed instances — not eight independent r21 malformations.

### C — Independent-authority claim (explicitly bounded)

Contract `bounds`:

- Retained callbacks are **declared inputs**, not authenticated provider telemetry.
- **No** numeric expertise or independent review credit from this calibration alone.
- r21 outputs retained; round-22 does not re-admit r21’s two axis claims.

`tools/wave-accounting.py` `evaluate()` returns `authority`: `declared retained callbacks; report presence never completion; not provider authentication` (lines 114–116). Gate text in `spec1.json` context: gate validates digests and registry fields; **cannot authenticate callback provenance**.

**Not in scope for “8/8”:** blind/independent cold-read, required-command coverage, provider-death causality proofs, or replay of all **146** identities as eight CLI cases (separate wave-1 audit lanes + executor counts).

## Eight predicates vs r21 empirical incidence

| Predicate (contract) | Finding ID (measure) | r21 observed? | Notes |
|---|---|---|---|
| `false-completion-count` | `TOTAL_MISMATCH` | No (as miscounted seats) | Wrong *seat* total; r21 error was wrong *completed* inference |
| `failed-with-report-counted-completed` | `TOTAL_MISMATCH` | **Yes (class)** | Models counting dead+partial as completed; **2** seats, not 8 |
| `missing-outcome` | `MEMBERSHIP_MISMATCH` | No | Synthetic pop of outcome row |
| `duplicate-agent` | `DUPLICATE_AGENT` | No | — |
| `unknown-status` | `UNKNOWN_STATUS` | No | Status enum is `completed` / `failed` in final JSON |
| `registry-id-mismatch` | `IDENTITY_MISMATCH` | No* | *Separate r22 audits check registry ↔ callback; not part of “8” |
| `replacement-seat` | `REPLACEMENT_FORBIDDEN` | No | All `replaced: false` in final outcomes |
| `snapshot-tampering` | `SNAPSHOT_TAMPERED` | No | Input digest guard on bundle, not r21 wave JSON |

**Partial reports on failed seats:** the CLI **does not** fail clean reconciliation when `status=failed` and a report path is listed — it increments `dead` and records `failed_with_report` in the wave summary (`tools/wave-accounting.py` lines 96–99, 112). That is correct callback authority. The r21 harm came from **external** counting (Markdown inventory ⊃ completed), which predicate `failed-with-report-counted-completed` only **simulates** via wrong `claimed` totals on a toy bundle.

## Overclaim language to forbid

Treat the following as **calibration threats** (reject in SCORECARD, lessons, gate admit prose, and lane reports):

1. **“Eight r21 accounting errors fixed”** — only **two** partial-report false completions were observed; the other six predicates are **capability guardrails** with no matched r21 row.
2. **“8/8 ⇒ round-21 seat accounting complete”** — `SCORECARD.md:973-974` already separates full **146** replay from the eight-predicate counter; do not collapse.
3. **“Calibration 8 from fixture count”** — `SCORECARD.md:968-970`: numeric expertise stays **8**; the eight named predicates are the **unit**, not a second score equal to “number of selftest cases passed.”
4. **“Report file present ⇒ seat completed”** or **`len(*.md)` as completed denominator** — contradicted by `original-outcomes-final.json` and the two named dead identities.
5. **“Callback-authoritative ⇒ provider-authenticated”** or **“gate verified terminal execution”** — bounds forbid; gate cannot authenticate callback provenance (`spec1.json` context).
6. **“Independent review / blind cold-read credit from wave-22 audits”** — wave-1 audits are advisory; r21 source re-anchors remain L1-author input-keyed (`corpus/lessons/round-21.md`, coldread refresh specs).
7. **“Before 0/8 means eight predicates already failed”** — `before.json` shows **`tool_present: false`**; baseline is **non-measurement**, not disproof.
8. **“Partial report rehabilitated / replaced dead seat”** — forbidden by contract and `partial_report_files_do_not_rehabilitate_failed_jobs: true` on final outcomes.
9. **Retroactive “wave-accounting rejected the two r21 cases at round-21 close”** — tool and measure bundle postdate the erratum; credit only after frozen replay with persisted r21 bundle + expected digest.

## Contradictions and narrow-scope recommendations

**Held (consistent):**

- Triple separation in `SCORECARD.md` Round 22 block: one calibration claim + runnable capability; **146** population replay; no provider-authenticity claim.
- Final outcomes align totals with callback status; partial reports are annotated, not promoted.

**Risk:**

- Wording like “corrected counter is shown able to reject those two false-positive completions” (`corpus/lessons/round-21.md:173-174`) reads as **historical tool proof**; until an r21-shaped bundle is run through `wave-accounting.py` with a persisted expected digest, phrase as **design intent**, not exercised gate output.

**Bounded recommendations for L1 / gate:**

1. Score round-22 C1 **primary** on frozen `measure.py` discriminated count; **secondary** acceptance: bundled replay of `original-outcomes-final.json` (or normalized export) with `claimed` matching callback-derived totals — expect **clean** on truth, **failed** only if someone reintroduces file-presence `claimed` totals.
2. In any admit sentence, pair **8** with the phrase **synthetic public-CLI rejection predicates**, and **146** with **retained callback census**.
3. Keep **`failed-with-report-counted-completed`** naming in score prose so the r21 mistake class stays visible; do not rename to imply eight real wave seats.
4. Executor lanes (`CountReportOverlap`, `CountCallbacks`, `CountUniqueIdentities`) own numeric overlap proofs; this seat does not duplicate their commands.

## Tooling

No installs or updates this lane.

Report: `.ufo/waves/round-22/w1/CounterThreats.md`
