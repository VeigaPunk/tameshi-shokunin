# ScoreRestraint — round 13 (read-only review)

Scope: scalar restraint for depth and calibration, and the no-seventh-gate rule. Read-only. No checks, tests, or gates run. No implementation edited. No tools installed or upgraded.

Baseline: `546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50` (HEAD). Tracked `tools/`, `SHONEN.md`, `SCORECARD.md`, `corpus/SOURCES.md`, `.ufo/evidence/` were clean against it at inspection (`git diff --quiet 546b371 -- …` passed). Untracked at inspection: `.ufo/waves/round-13/` and `.ufo/evidence/round-13/` (`before.json`, `claims.json`, `measure.py`).

Implementation state at inspection: `tools/pin-disposition.py`, `tools/witness-metadata.py`, `corpus/knowledge/incremental-pin-disposition.md`, and any round-13 pin/companion receipts are absent. Nothing to review yet beyond the planning and measurement surface. Messages sent: `TameshiR13.PinProbe` (no seventh leg, no runner `#   js-`/`#   bash-` rows, no SHONEN edits), `TameshiR13.MetadataRepair` (metadata cannot move either scalar; do not touch SHONEN, runner, or round-12 evidence).

## Scalars (carried, not re-scored)

- depth = 6: SCORECARD.md:315, 322-324 (round-12 table); command D `recorded_cases=6` (SCORECARD.md:73); measure.py `recorded_cases` (`.ufo/evidence/round-12/measure.py:45`).
- calibration = 6: SCORECARD.md:316, 322-324; pin from outside adjudication, boxes 1, 2, 4 only (`measure.py:30-31`, `.ufo/evidence/round-12/measure.py`; SCORECARD.md:216-220). Command C prints `asserted_mark_upper_bound=8`; this is not the pin and is not awarded (SCORECARD.md:306-311).
- Historical row SCORECARD.md:64-68 still reads calibration 0 at `284ab0f`. It is a superseded baseline row. Do not rewrite it; the round-13 entry must state the live value is 6.

## Findings

**F1 (gap — scalars unmeasured in round-13 evidence).** `.ufo/evidence/round-13/measure.py:27-33` emits `pin_dispositions`, `metadata_companion`, source counts, and `frozen_summary_sha256`. It emits no `recorded_cases`, `unique_recorded_gates`, or `calibration_restraint_score`. `claims.json:5-6` nonetheless declares "6 -> 6" for C1 and C2. No committed round-13 receipt computes either scalar. Fix: the round report must either cite the round-12 `measure.py --rev` and command D/C outputs at both `546b371` and the round commit, or state the scalars as carried-forward and unmeasured.

**F2 (guard — depth is a raw regex count).** Depth is `re.findall(r"^#   (?:js|bash)-…")` over `tools/mutate-and-run.sh` only (`measure.py:45`, round-12). Duplicate header rows count; the round-12 probe appended one extra row and got `recorded_cases=7`, `unique_gates=6` (`.ufo/waves/round-12/w2/ScoreRubric.md:30,88-92`). The current runner is clean: `git show 546b371:tools/mutate-and-run.sh | sha256sum` = `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`, which matches the pin in `corpus/knowledge/repeated-control-precondition.md:54`. Six matching lines at `tools/mutate-and-run.sh:84-89`. Any round-13 edit adding a `#   js-`/`#   bash-` line to that file inflates depth without a new gate. `pin-disposition.py`'s own leg table is outside the counted file and is safe as long as it stays there.

**F3 (decoupling — calibration cannot move from C2).** Calibration is `2 × [~]` at SHONEN boxes 1, 2, 4 (`measure.py:31`). `SHONEN.md` at `546b371` = `3b1dc52601bc1e5636909764c10f6a2ccfacbb8d9ca7991a0a8f2358a145ac58`. The companion metadata (C2) is never read by `measure.py`. C2 must be reported as delta 0 on calibration and "capability/quality" only. Any "calibration improved" wording for C2 is overreach; the round-12 `calibration 6 → 6, no promotion points` precedent applies (SCORECARD.md:316).

**F4 (null is ambiguous in measurement output).** Round-13 `measure.py:19-20` (`obj()`) returns `None` for a missing file and `json.loads` raises on malformed JSON. Output shows `"metadata_companion": null` (`before.json:4`), which is the same shape as the original defect (`declaration.kind=null`). An absent companion must be reported as `absent`, distinct from an observed null value, and a malformed companion must be an honest could-not-evaluate state. Forwarded to MetadataSecurity for the checker itself; the measurement-side ambiguity is mine.

**F5 (frozen-input integrity is printed, not asserted).** `measure.py:33` prints `frozen_summary_sha256`; baseline value `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9` (`before.json:2`). Nothing compares it to a pinned expectation. Round report must state the expected digest and that the round commit matches it. Also `git diff --quiet 546b371 -- .ufo/evidence/round-12` must pass (`measure.py:26-33` reads `…/round-12/BashWitness/summary.json`).

**F6 (no-seventh-gate language — currently clean).** `claims.json:5` says "no seventh recorded case"; `SCORECARD.md:282-285` rejects the stale "6 → 7" plan. Grep over LOG/SCORECARD/knowledge found no round-13 claim of seven. Watch for "7", "seventh", or "depth 6 → 7" in the round report and SCORECARD append.

**F7 (source-status mismatch — advisory, Main-owned).** `claims.json:5` says S003 and S041 were "reopened this round", but `corpus/SOURCES.md:14` still reads S003 `queued`, opened 2026-10-19. Main must update the mutable cells through the SourceScribe path or KnowledgeSupport's citation has no registry support. Not a scalar issue.

**F8 (honesty of the table).** SCORECARD baseline table (`:64-68`) and the kaika section (`:219-220`) disagree on calibration. Both stay as written; the round-13 section must name which is live (6) and why.

## Exact checks for L1 (not executed here)

1. `git show <round>:tools/mutate-and-run.sh | sha256sum` → `75ed934d…adc5`; `git show <round>:SHONEN.md | sha256sum` → `3b1dc526…58ac58`.
2. `git diff --quiet 546b371 -- tools/mutate-and-run.sh SHONEN.md .ufo/evidence/round-12` (must pass; any named exception must be a declared path).
3. Command D at `<round>` and `546b371`: `recorded_cases=6 depth_score=6`.
4. Command C at `<round>`: `asserted_mark_upper_bound=8` (reported as upper bound only).
5. `python3 .ufo/evidence/round-12/measure.py --rev <round>` and `--rev 546b371`: `calibration_restraint_score: 6`, `recorded_cases: 6`, `unique_recorded_gates: 6`, identical scalars at both revisions.
6. `python3 .ufo/evidence/round-13/measure.py --rev <round>` (only after the round commit contains the companion and disposition files): `frozen_summary_sha256 == acc01268…547b9`; `pin_dispositions` and `metadata_companion` are non-null objects; `source_rows=44`, tiers A37/B5/C2, statuses mined15/queued26/rejected3 unless Main names a delta.
7. Confirm `tools/pin-disposition.py` and `tools/witness-metadata.py` contain no `#   js-`/`#   bash-` ledger lines that would be counted if pointed at the runner (grep only; no execution).
8. Companion negative: the round-12 `BashWitness/summary.json` (declaration.kind null) must fail the new companion gate. Run the MetadataSelftest suite, not this review.

## Residual risk

- Scalars for round 13 are carried, not measured, until check 5 runs at the round commit.
- Command D's raw-regex fragility (F2) is a standing hazard for any future runner edit; only this round's file set is verified.
- Round-13 `measure.py` itself is untracked at inspection; its output is only as good as the committed blobs it reads.
