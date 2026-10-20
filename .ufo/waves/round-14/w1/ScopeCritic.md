# ScopeCritic: round 14 W1, scope creep and no-axis-harm

Seat: `TameshiR14.ScopeCritic` (critic, leaf). Baseline: `d6809df7775338f000e44c8a916067b8866867fb`.
Status of the code under review: `tools/evidence-disposition.py`, `.ufo/evidence/round-14/capture-context.py`, `dispositions-before.json` and `dispositions.json` are **absent** (glob result). I reviewed them only as retained contracts in `spec.json`, `claims.json` and `measure.py`. L1's uncommitted integration drafts are present and I reviewed them as drafts: `LOG.md`, `corpus/QUALITY.md` 15–16, `corpus/SOURCES.md` S049, knowledge §8, and `corpus/lessons/round-14.md`.
I ran no checks, gates, selftests or sibling commands. I used only file reads, JSON parses of retained receipts, sha256 of the 13 `expected.inputs` paths, and `git status`/`git log`/`git diff` reads. Tool installs or updates: none.

## Bottom line

C1 stays a single bounded calibration claim if L1 applies the corrections below. I found no new kill rate, seventh case, runner edit, SHONEN edit or freshness execution in the files on disk now. The real risks are attribution risks:
- folding routed items 2 and 3 into C1;
- counting round-13 C2 a second time;
- a constructed "before" file presented as historical state;
- forward-referencing prose written before any results exist.

## Static forecast from the retained receipts (data reads, not a gate run)

- All 13 `expected.inputs` digests match the current worktree bytes. `expected_checks` has **12** keys, not 13. `measure.py`/`before.json` already record 12, and so does the "count-assumption" row of the round-14 lesson.
- A naive all-effective ledger fails on **exactly one** row. `producer_before`: the exit matches (1 = 1), but the expected substring is absent from both stdout and stderr. The stderr is a `FileNotFoundError` for `.ufo/evidence/tools/mutate-and-run.sh`. The other 11 rows pass their original predicates:
  - `contains` holds on stdout for pin_selftest, metadata_selftest, producer_after, witness_check, witness_count, producer_before_oracle and producer_after_oracle.
  - metadata_old_null and metadata_corrected match on `id`/`reason` from the parsed stdout.
  - source_census is checked on exit only.
- **Trap:** the pin_live stdout has **no** top-level `rows` or `statuses` keys. The available fields are `counts={legs:6,unchanged:3,changed:3,unavailable:0}` plus `legs[].content_status` and `legs[].result_reuse`. If the Gate reads `j["rows"]` literally, both files fail and C1 collapses. The mapping `rows=len(legs)`, `statuses=` a tally of `legs[].content_status` (cross-checked against `counts`), and per-leg `result_reuse` must be explicit and documented as a derived predicate. It must not be hidden.
- Receipt checks that have no expected row: `pin_env_scrub`, `metadata_emit` and `frozen_and_guardrail_unchanged` in verification.json, plus `baseline_final_count` in the verdict. These must not become rows, and they must not fail the gate. Report them as informational. `producer_before_oracle` and `producer_after_oracle` exist only in `producer-oracle-repair.json`.

## Counterexamples → impacted axes → smallest safe correction

1. **C1 absorbs routed items 2 and 3 (scope creep / multi-claim bundling).**
   - **Evidence:** `claims.json` C1 before/after mentions only the expectation ledger. But `lessons/round-14.md:66` reads "Prior outside items1–3 are lane-owned, addressed by C1 and its context/backlink artifacts". The LOG draft also groups all three under C1 in its motivating evidence.
   - **Impact:** calibration attribution, plus depth or operability by implication. If the context receipt fails, for example because a sibling moves mid-run (item 7), a reader could think C1 failed. If it passes, a reader could credit C1 with an environment experiment.
   - **Correction:** change the wording to "Item1 is addressed by C1. Items2–3 are routed-debt dispositions with their own artifacts and no axis credit. C1's verdict does not depend on the context-receipt outcome." Use the same wording in the SCORECARD round-14 row.

2. **Round-13 C2 counted twice.**
   - **Evidence:** the round-13 closure already admitted the producer red/green from `producer-oracle-repair.json`: "explicit supersession … is valid proof and was used here". The round-14 lesson and QUALITY15 say "checked oracle receipts" or "checked replacement evidence".
   - **Impact:** calibration inflation.
   - **Correction:** C1's novelty is a machine-checked ledger that rejects stale rows. The supersession fact itself is not new. Say "recorded round-13 oracle receipts, evidence-verified, not rerun." Make no new red/green execution claim.

3. **The "before" file is constructed, not historical.**
   - **Evidence:** the baseline has no dispositions file (`before.json`: `disposition_name_coverage 0`, `gate_artifact 0`). `dispositions-before.json` is a round-14 artifact encoding the naive all-effective reading.
   - **Impact:** false provenance.
   - **Correction:** label it a "constructed naive ledger (all 12 rows effective)". It discriminates the gate's behaviour, but it is not a historical before-state. Keep the baseline counts from `before.json` as the historical before-state.

4. **Forward references in shared prose written before any results (round-13 defect-3 pattern recurring).**
   - **Evidence:** knowledge §8 says "Read `.ufo/evidence/round-14/dispositions.json` and its checker receipt", and "context capture, if clean". Neither the gate, the dispositions nor the receipt exist yet. The LOG draft says the new artifacts "address those gaps" in the present tense.
   - **Impact:** calibration, and reading clarity, which is the very item 3 being fixed.
   - **Correction:** before commit, L1 should name the exact receipt file path and land the gate, both dispositions files and that receipt in the same commit. It should then replace "if clean" with the observed outcome, or delete the line. If any artifact is rescoped, update §8 and the LOG before commit.

5. **The selftest tally or the runner table read as a kill rate.**
   - **Evidence:** the runner header lines `tools/mutate-and-run.sh:84-89` carry historical rates such as 8/10 and 4/10. ReceiptHarness is told to retain a "six-leg runner table". The Gate selftest will print an N/N tally.
   - **Impact:** the "no new kill rate" guardrail, and freshness.
   - **Correction:** in context-receipt.json, label the runner rates `recorded_historical_rate`, not measured. In SCORECARD and README, present the selftest tally only as gate selftest cases, never as a mutation score, case count or kill rate. `measure.py` `recorded_cases` uses the runner regex and must stay at 6. Do not add the new gate to `mutate-and-run.sh`.

6. **Durability tradeoff, not a defect.**
   - **Evidence:** the Gate must verify all 13 `expected.inputs` digests against **live** paths before evaluating predicates. Those paths include `tools/pin-disposition.py`, `tools/witness-metadata.py`, `tools/bash-witness-study.py` and `tools/mutate-and-run.sh`.
   - **Impact:** any legitimate future edit to those tools makes round-13 reconciliation exit 2 permanently. This round, the same rule acts as a free guard against editing tools.
   - **Correction:** disclose in the registry row that exit 2 after any future edit to a pinned tool is the correct "could-not-evaluate" result, and that re-evaluation happens at baseline bytes (a git worktree at that rev). Do not add a `--rev` mode this round; that would be scope creep.

7. **The context receipt misread as a freshness result, or as an injection failure, while siblings move.**
   - **Evidence:**
     - `mado-shokunin` committed `32118fc` (round-14), which touches `tools/mado-verify.sh`, at 03:10 today.
     - `tsukuroi-shokunin` showed 16 dirty paths during my reads, then 0. TsukuroiR14, MoriR14 and MadoR14 are running.
     - The pin probe reads sibling HEAD and worktree bytes for each leg.
   - **Impact:**
     - Freshness: new changed/unchanged values, or new HEAD digests, are a content observation and not a successor sweep.
     - Calibration: if a sibling commits between the baseline and injected runs, a false "poison differs" result appears. If L1 then retries until the two runs are equal, that is cherry-picking.
   - **Correction:**
     - The harness records the six sibling HEADs before the baseline run and after the injected run. If they differ, the result is classified `indeterminate_sibling_motion`, not a pass and not an injection failure.
     - L1 records every attempt.
     - Never compare the new counts against round-13 `pin_live` 3/3. That is a frozen expectation of the old receipt.
     - SCORECARD freshness stays "unchanged".

8. **The freshness plan is silently replaced.**
   - **Evidence:** SCORECARD:392 "Next intended claim: freshness — … or an honest intake refusal." `lessons/round-14.md:74-77` handles this correctly.
   - **Impact:** discernment, if the plan is lost.
   - **Correction:** SCORECARD round 14 must state that the plan was not executed and give the exact missing prerequisite (from FreshnessIntake). Carry the plan forward as the next intended claim. Run no sibling gate.

9. **An uncorrected historical sentence (small, inside item 2).**
   - **Evidence:** `corpus/lessons/round-13.md:120` says "Injecting GIT_DIR did not change probe data except the observation time". The retained `pin_live` and `pin_env_scrub` stdout are **byte-identical, including** `observed_at` 04:59:26Z. The two runs started 49 ms apart, and the timestamp has one-second resolution.
   - Knowledge §8 already notes the identity. The round-14 lesson's missing-setup row does not point at `round-13.md:120`.
   - **Correction:** add one append-only erratum pointer in the round-14 lesson. Leave the round-13 bytes untouched.

10. **Outside review and box3 are respected.** No change needed; keep it this way.
    - **Evidence:** `SHONEN.md` boxes 1–4 are all `[~]`, and `git status` shows SHONEN unmodified. The lesson says "separate non-author closure owns round14 admission", with no `[x]`, promotion or cold-read. `measure.py` restraint scoring uses boxes 1/2/4 only.
    - **Guard:**
      - The SCORECARD row reads "lane verdict; scalar 6→6; pending non-author closure".
      - Lane seats, this one included, are not outside authority.
      - Knowledge §8's "independent outside verification" of round 13 should say "non-author closure", matching the closure note's own wording.

## No-axis-harm table, as currently drafted

| Axis | Risk observed | Status if corrections 1–10 are applied |
|---|---|---|
| calibration | Double credit (2), constructed before-file (3), forward refs (4) | improved by C1 only, scalar 6 |
| depth | Context receipt mapping booleans could be credited | unchanged; no claim |
| coverage | None | unchanged |
| operability | New gate and registry row; pinned-tool exit-2 decay (6) | unchanged; disclosed tradeoff |
| freshness | Live receipt misread (7); plan dropped (8) | unchanged |
| adjacency | Pin probe reads moving siblings (read-only; the probe scrubs inherited `GIT_*`, `tools/pin-disposition.py:197-210`) | unchanged; no sibling writes |

Shared-file note: L1 has already modified `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md` and knowledge §8, and added `lessons/round-14.md`. SOURCES shows one deleted line, the old "Next unused id: S049" line, which is replaced by the S049 entry and "Next unused id: S050". This is the next-ID bookkeeping only, not a rewrite of a source row. All S047–S049 rows parse to 13 cells. No round-12 or round-13 evidence file appears in `git status`.

## Checks for L1 (after all seats finish; none run here)

1. `python3 tools/evidence-disposition.py --selftest`: exit 0, with stable finding IDs per fixture.
2. Gate run against `dispositions-before.json`: exit **1** with exactly one semantic finding, on `producer_before` (missing assertion). Any other finding, or exit 2, contaminates the red/green.
3. Gate run against `dispositions.json`: exit 0. Expected: 12 rows (11 effective, 1 superseded), pin_live rows/statuses derived from `legs[]`, and the unmapped receipt checks reported as informational.
4. A diff of the two dispositions files changes only the `producer_before` row (state, reason, `superseded_by`).
5. `git diff --quiet d6809df -- .ufo/evidence/round-12 .ufo/evidence/round-13 tools/mutate-and-run.sh tools/pin-disposition.py tools/witness-metadata.py tools/bash-witness-study.py SHONEN.md corpus/lessons/round-13-verifier-spotcheck.md` exits 0.
6. `python3 .ufo/evidence/round-14/measure.py --rev <delivered>`: recorded_cases 6, calibration_restraint_score 6, runner and frozen-summary SHAs unchanged, historical_expected_rows 12, coverage 12.
7. capture-context: confirm the sibling HEAD sets before and after match; record every attempt; confirm no ambient environment in the receipt; confirm runner rates are labelled historical.
8. Before commit, grep the LOG, knowledge §8 and the lesson for "if clean", "its checker receipt" and "addressed by C1". Then reconcile them with the observed receipts and the item-1 wording.
9. Run the sources census (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`) once for the S049 row.
