# Round 14 — C1 counting design: effective expectation reconciliation

Seat: `TameshiR14.ClaimMeasurement` (leaf, read-only research). Baseline `d6809df7775338f000e44c8a916067b8866867fb`.
Scope of this report: measurement design and guardrails for C1. No code was written. No gate, probe, selftest, build, or suite was executed. Every observation below is from a file read.

**Status of the code:** contract-only for the new pieces. `tools/evidence-disposition.py` does not exist. `.ufo/evidence/round-14/capture-context.py` does not exist. `.ufo/evidence/round-14/` holds only `claims.json`. Dispositions files do not exist. The round-13 artifacts that the reconciliation reads are present (code and receipts).

**Tools:** none installed or updated by this seat.

## 1. Axes

| Axis | Claim-level meaning for round 14 | Credit rule |
|---|---|---|
| C1 calibration (capability) | Same command reconciles all historical expectations: effective, or superseded by checked mechanism evidence | Only the semantic closed-count delta (section 3, S5) earns credit |
| G-hist | Old raw evidence byte-identical | Guardrail, hard fail on change |
| G-cases | Six recorded cases stay six | Guardrail |
| G-scalar | depth 6 / calibration 6, no promotion credit | Guardrail |
| G-fresh | No successor sweep, no sibling gate run | Guardrail |

## 2. Facts observed (with citations)

**Expectation denominator is 12, not 13.**
- `.ufo/evidence/round-13/expected.json:19-74` has **12** `expected_checks` keys: pin_selftest, metadata_selftest, metadata_old_null, metadata_corrected, producer_before, producer_before_oracle, producer_after_oracle, producer_after, witness_check, witness_count, pin_live, source_census.
- `expected.json:4-18` has **13** `inputs` digests. The Interfaces text ("All13 expected rows", "Enumerate expected_checks exactly once") conflates the two. The denominator for rows must be 12. Recorded in section 6 as spec risk R1.

**Receipt records.** 15 check records exist in total.
- `verification.json` checks: 13 records (pin_selftest, metadata_selftest, metadata_old_null, metadata_corrected, producer_before, producer_after, witness_check, witness_count, pin_live, pin_env_scrub, metadata_emit, source_census, frozen_and_guardrail_unchanged).
- `producer-oracle-repair.json` checks: 2 records (producer_before_oracle, producer_after_oracle).
- `verification-verdict.json` lists 15 names. It includes `baseline_final_count`, which has **no receipt record anywhere in round 13**. Its `matched` flags are a hand-written verdict, not a receipt, and must not be counted as one.

**Each of the 12 expectations resolves to exactly one receipt record** (names unique per file):
- `producer_before_oracle` and `producer_after_oracle` come from `producer-oracle-repair.json`. All other 10 come from `verification.json`.

**Raw predicate outcomes (read in full from receipt stdout, not from `exit_matches`):**

| Expectation | Expected | Receipt exit | Receipt exit_matches | Raw stdout contains expected string? |
|---|---|---|---|---|
| producer_before | exit 1, contains `summary preserves top-level exposed declaration kind` | 1 | true | **NO** (verification.json:91; stderr is FileNotFoundError traceback at producer-before.py:218 via cmd_selftest:1478) |
| producer_before_oracle | exit 1, contains `… kind FAIL` | 1 | true | yes (repair:20, `VERDICT: FAIL`) |
| producer_after_oracle | exit 0, contains `WITNESS_SELFTEST: 41/41 pass` | 0 | true | yes (repair:37) |
| producer_after | exit 0, contains `WITNESS_SELFTEST: 41/41 pass` | 0 | true | yes (verification:105) |
| pin_selftest | exit 0, contains `SELFTEST: PASS (18/18)` | 0 | true | yes (verification:29) |
| metadata_selftest | exit 0, contains `SELFTEST: PASS 39/39` | 0 | true | not re-read in full; carried from the closure note |
| metadata_old_null | exit 1, id/reason JSON | 1 | true | JSON id/reason present (verification:60) |
| metadata_corrected | exit 0, id JSON | 0 | true | JSON id present (verification:77) |
| witness_check | exit 0, contains `WITNESS_CHECK: CLEAN` | 0 | true | yes (verification:119) |
| witness_count | exit 0, contains `witness_classified=10` | 0 | true | yes (verification:133, `counts … witness_classified=10`) |
| pin_live | exit 0, rows 6, statuses u3/c3/x0, result_reuse | 0 | true | JSON counts/result_reuse present (verification:150); "rows" needs a defined mapping (R6) |
| source_census | exit 0 | 0 | true | n/a |

**The trap in one line:** `producer_before` has `exit_matches: true` (verification.json:93) while its `contains` predicate fails. A gate that trusts `exit_matches` marks it passing. This is the single most important discriminator for C1.

**Other observed facts:**
- `pin-disposition.py:197-211` (`git_env`) strips every `GIT_*` variable and sets `GIT_CONFIG_NOSYSTEM`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, and the others. A GIT_DIR injection therefore reaches only the probe's own subprocess env, which is scrubbed. The injected run is expected to equal baseline. The test is only non-vacuous if an unscrubbed `git -C` with the same GIT_DIR is shown to fail (see section 5, D2).
- `verification.json` `pin_env_scrub` (lines 154-170) has argv **identical** to `pin_live` (lines 137-153) and no injected env field. This is routed item 2 in the round-13 lesson, confirmed.
- `pin-manifest.json` cites runner lines `84-89` (leg/path), `542-553` (PIN_/REV_), `1112-1140` (six ledger calls). `mutate-and-run.sh` lines `84-89`, `542-553`, `1112-1140` match these (grep observed). Six `PIN_*` and six `REV_*` assignments observed.
- `round-13/measure.py` is a read-only counter (`git show <rev>:<path>` plus JSON parsing). It already counts `pin_probe_artifact` 0→1, `recorded_cases` 6/6, `calibration_restraint_score` 6, `source_rows` 44→46. It reports **artifact existence** next to semantic counts without distinguishing them. Round 14 must separate the two.
- Pre-existing round-13 `verification.json` sibling-index hashes (kumitate, kagi, tsukuroi, mado sizes, mtimes, sha256) are a reusable no-mutation guard.

## 3. Measurement design: the same counting command before/after

### 3.1 Command (same binary, two dispositions files)

```
python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --dispositions .ufo/evidence/round-14/dispositions-before.json --json   # expect exit 1, one finding
python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --dispositions .ufo/evidence/round-14/dispositions.json --json          # expect exit 0, zero findings
```

Recommendation to Gate seat: emit a `summary` object in the JSON output with these integer fields, so the counter reads the gate's own output and does not re-derive it. L1 then recomputes the same fields independently (section 4).

Before/after files must be identical except for one row. Enforce with a stdlib diff: remove `rows[name=="producer_before"]` from both and require equality. The producer_before row must change `state` effective→superseded, with its `reason` and `superseded_by` added.

### 3.2 Semantic metrics (earn credit)

| ID | Metric (from raw receipts, not flags) | Before | After | Notes |
|---|---|---|---|---|
| S1 | expected rows enumerated exactly once = `len(expected_checks)` | 12 / 12 | 12 / 12 | denominator; must equal 12 (R1) |
| S2 | effective rows whose predicates pass | 11 | 11 | predicates: exit, contains on parsed stdout, id/reason, rows/statuses/result_reuse |
| S3 | effective rows failing a predicate, each with a stable finding ID | **1** (`producer_before`, contains absent) | 0 | the before-state must reject for this ID, not exit 2 |
| S4 | superseded rows whose both replacements pass their original expectations | 0 | **1** (`producer_before`) | replacements: `producer_before_oracle`, `producer_after_oracle` |
| S5 | **closed expectations = S2 + S4** | **11/12** | **12/12** | the C1 delta is +1 closed expectation |
| S6 | gate exit code | 1 (semantic) | 0 | a before-exit of 2 means vacuous rejection and counts as a failed control |
| S7 | finding-ID set | `{EVD-PRED-FAIL:producer_before:contains}` (exact) | ∅ | exact set equality, not a count |
| S8 | exit-only reading (contrast only, not credited) | 12/12 | — | shows why `exit_matches` must not be used |

Credit rule: C1 closed-count moves 11→12 **only if** S3 names exactly the expected ID before, and S7 is empty after, and S6 is 1 then 0. A naive "12/12 matched" reading is explicitly not credited.

### 3.3 Artifact existence (zero capability credit)

Reported separately; none of these adds to S5.
- `tools/evidence-disposition.py` present: 0→1.
- `dispositions-before.json` and `dispositions.json` present: 0→2.
- `.ufo/evidence/round-14/context-receipt.json` present (after L1 runs the harness): 0→1.
- `--selftest` exit 0: a self-consistency fact about the gate's own fixtures.

### 3.4 Mutant control set (gate selftest; kill count reported, not credited to S5)

Each mutant must produce its exact stable ID and exit code. Kill counts only if both match.

| Mutant | Expected exit | Expected ID (recommended) |
|---|---|---|
| M1 producer_before effective (before file) | 1 | `EVD-PRED-FAIL:producer_before:contains` |
| M2 **exit-only reading** of producer_before (exit_matches true, contains absent) | 1 | same as M1 (discriminator against R2) |
| M3 superseded with missing replacement (`producer_after_oracle` dropped) | 1 | `EVD-SUP-NO-REPLACEMENT:producer_before` |
| M4 superseded without raw receipt/check | 1 | `EVD-SUP-NO-RAW:producer_before` |
| M5 expected.json digest changed | 2 | `EVD-INPUT-DIGEST:expected.json` |
| M6 receipt digest changed | 2 | `EVD-RECEIPT-DIGEST:verification.json` |
| M7 one expected row dropped | 1 | `EVD-ROW-MISSING:<name>` |
| M8 duplicate row | 1 | `EVD-ROW-DUP:<name>` |
| M9 unknown row name | 1 | `EVD-ROW-UNKNOWN:<name>` |
| M10 superseded_by cycle | 1 | `EVD-CYCLE` |
| M11 metadata_old_null id mutated | 1 | `EVD-PRED-FAIL:metadata_old_null:id` |
| M12 pin_live statuses mismatch | 1 | `EVD-PRED-FAIL:pin_live:statuses` |
| M13 receipt argv sentinel (argv would create a marker if executed) | gate exit unchanged; marker absent | gate never executes argv |

IDs are a recommendation. The Gate seat owns the names and must publish the table before L1 runs it.

## 4. Independent guardrails (must not depend on gate code)

L1 should compute these with a stdlib script in `/tmp` (QUALITY 9), not by importing `tools/evidence-disposition.py`:

- **G1 historical bytes:** `git diff --quiet d6809df7775338f000e44c8a916067b8866867fb -- .ufo/evidence/round-12 .ufo/evidence/round-13 tools/mutate-and-run.sh SHONEN.md tools/pin-disposition.py tools/witness-metadata.py tools/bash-witness-study.py` must exit 0. Also sha256 of every round-13 receipt against the expected.json digests.
- **G2 denominator and pins:** recompute the 13 `expected.json` input digests and the 12 expectation keys; independent of the gate.
- **G3 six cases:** count `^#   (js|bash)-` in `mutate-and-run.sh` → 6, unique 6; `PIN_*` 6; `REV_*` 6.
- **G4 manifest/runner mapping:** from `pin-manifest.json` `legs`, check each `pinned_commit`/`expected_sha256` equals the `REV_*`/`PIN_*` value at the cited line, and each `repo`/`path` equals the `CANONICAL_LEGS` tuple at `mutate-and-run.sh:84-89` (in `pin-disposition.py:128-135`).
- **G5 scalar:** depth 6, calibration 6 (no SCORECARD change unless L1 decides otherwise).
- **G6 freshness:** no new `BashWitness/rerun-*`, `sweep/`, or mutation result dirs created in round 14; `tools/mutate-and-run.sh` not invoked (no new `results.tsv`).
- **G7 sibling indexes:** size, mtime_ns, and sha256 of `kumitate`, `kagi`, `tsukuroi`, `mado` indexes unchanged before and after (same mechanism as `round-13/verification.json:221-265`).
- **G8 source rows:** 46 SOURCES rows and 0 malformed (round-13 `measure.py` `source_rows`), unless round 14 explicitly admits rows.

## 5. Context receipt (routed item 2) — distinct from frozen checks

- `capture-context.py` is run only by L1, once. It records `argv`, `cwd`, `injected_env={"GIT_DIR":"/nonexistent/tameshi-round14-poison"}` (no ambient dump), baseline and injected exit codes, and comparable JSON with `observed_at` removed. It records source and manifest digests and a six-leg mapping table with explicit booleans for PIN_/REV_/leg-call.
- It is **not** a retrospective repair of the round-13 omitted setup. It does not count toward S5. Count it only as routed item 2 disposition and artifact existence.
- **D1 (required):** injected vs baseline comparable JSON equal (minus observed_at), probe exit 0 in both.
- **D2 (recommended, non-vacuity control):** run plain `git -C <repo> rev-parse --show-toplevel` with `GIT_DIR` set to the poison value and show it fails. This proves the poison bites without the scrub and that the D1 equality is caused by `git_env()`, not by an inert variable. This is read-only git plumbing against the lane repo, not a sibling gate run.
- **D3:** `mapping_booleans` parsed from `mutate-and-run.sh` lines 84-89, 542-553, 1112-1140, compared to `pin-manifest.json`. Booleans written, not reconstructed by the reader.

## 6. Risks (concrete)

- **R1 — denominator.** Spec says "All13 expected rows". `expected.json` has 12 expected_checks; 13 is the input count. A DispositionSpec that builds 13 rows, or a gate that requires 13, is wrong. Fix the spec text; S1 = 12.
- **R2 — `exit_matches` trap.** `producer_before` passes `exit_matches` (verification:93) and fails `contains`. Any gate that checks exit only reports 12/12 before. Mandatory mutant M2.
- **R3 — superseded schema conflict.** The Interfaces say superseded rows carry `name/state/reason/superseded_by`, but also that they "must retain observed raw receipt/check". The schema has no field for it. Recommend an explicit `raw_receipt: {file, check}` required field on superseded rows; this is then part of the one-row diff (3.1).
- **R4 — unmapped receipt checks.** Receipt checks not referenced by any expectation: `pin_env_scrub`, `metadata_emit`, `frozen_and_guardrail_unchanged` (all in verification.json), and verdict-only `baseline_final_count` (no receipt). Rows must be the 12 expectations only. The gate should list these as `unmapped_receipt_checks` (informational) rather than count them as rows or drop them silently. `baseline_final_count` must be reported as unsupported, not as matched.
- **R5 — verdict as receipt.** `verification-verdict.json` must not be read as a receipt (it is a hand verdict, and it omits `producer_before`). Gate must treat it as input-only or ignore it.
- **R6 — pin_live mapping.** Expected "rows: 6" can be read as `len(legs)` or `counts.legs`. Recommend asserting both equal 6.
- **R7 — digests.** Round-13 closure reported 13/13 expected input digests matching (carried from `round-13-verifier-spotcheck.md`, not recomputed here). L1 must recompute, not trust the note.
- **R8 — before-file validity.** If `dispositions-before.json` is malformed (exit 2), the before "rejection" is vacuous. The before file must be valid input, differing only in the producer_before row.
- **R9 — self-certifying fixtures.** The gate's selftest builds its own fixtures; the counter must recompute S1–S5 from raw receipts (section 4), not from the gate's output alone.
- **R10 — expected.json rows vs capture-context.** Expected checks and the context receipt are different artifact classes. Mixing them would double-count the env item as retrospective repair. Keep separate (section 5).
- **R11 — producer_after_oracle receipt location.** Its `contains` value is in `producer-oracle-repair.json`, not `verification.json`. The row's `receipt` field must point there (`producer-oracle-repair.json`), or the gate reads the wrong file.

## 7. Checks L1 should run (after all seats finish; none run here)

1. `python3 tools/evidence-disposition.py --selftest` — exit 0; the mutant IDs in 3.4 match exactly.
2. `python3 tools/evidence-disposition.py --root <LANE> --dispositions .ufo/evidence/round-14/dispositions-before.json --json` — exit 1, finding set = `{EVD-PRED-FAIL:producer_before:contains}`, S5 = 11/12.
3. Same with `dispositions.json` — exit 0, zero findings, S5 = 12/12, S1 = 12.
4. Stdlib diff: both dispositions files identical after removing the producer_before row; producer_before row differs only as specified.
5. Independent counter in `/tmp` recomputing S1–S5 from raw receipts and comparing to gate `summary`.
6. `python3 .ufo/evidence/round-14/capture-context.py` once — D1 equal, D2 control shows failure, D3 mapping booleans true.
7. Guardrails G1–G8 (section 4).
8. Confirm `dispositions-before.json` and `dispositions.json` are the only round-14 disposition inputs; no historical byte changed (G1).

## 8. Changes this seat recommends (for the owning seats; none made here)

- Gate seat: add a `summary` object with S1–S8 fields; publish the finding-ID table; treat `exit_matches` as non-authoritative; add `raw_receipt` to superseded rows (R3); emit `unmapped_receipt_checks` (R4).
- DispositionSpec: use 12 rows (R1); build before/after as a one-row diff; set `receipt: producer-oracle-repair.json` for the two oracle rows (R11).
- ReceiptHarness: add D2 and D3 to the context receipt; keep `injected_env` explicit (routed item 2).
- DispositionSpec or L1: fix the spec text "All13" → 12.

## 9. Residual gaps

- Gate and harness do not exist; all predicates above are contract-level.
- Input digests (R7) and the 13 `expected.json` inputs are not recomputed in this seat.
- `metadata_selftest` stdout (`SELFTEST: PASS 39/39`) was not re-read in full here; carried from the closure note.
- The six-leg `mapping_booleans` are a recommended output, not observed.
- No independent verifier claim is made by this seat.
