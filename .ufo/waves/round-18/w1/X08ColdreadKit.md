# Round 18 cold-read kit — X08

## Files and behavior

- Added `.ufo/evidence/round-18/measure.py`: default ledger and box-3 link now use the round-18 ledger; input exclusion retains both round-17 and round-18 ledger paths. `--explain` adds per-section `end` and deterministic `reasons` without changing the credit calculation (`measure.py:113-136, 540-550, 1535-1536`). Synthetic cases cover the round-17 link failing the round-18 box-3 rule, drifted carried input, both ignored ledger paths, and explanation bounds (`measure.py:994-1011, 1214-1242`).
- Added `.ufo/evidence/round-18/coldread/assemble.py`: `--carry PATH` preserves each prior entry and adds `carried_from`; no-report carry assembly is accepted. Receipts retain `tameshi-trace-inputs-v1` and the full trace-inputs receipt shape is covered synthetically (`assemble.py:928-982, 1153-1165, 1299-1348`). For carry summaries, the assembler selects current `HEAD:SKILL.md` when no expected page was supplied and checks carried section SHA-256s against that measured page; output explicitly labels this coverage informational, with `measure.py` authoritative (`assemble.py:987-998, 1053-1055, 2007-2028`).

## Evidence

- Before edits, both round-17 working files matched the pinned source bytes at `183f87b899e6cae46be98d251cbc87fb5118f6ca`: measure SHA-256 `d25d3d04cb26ca7c20ef7333baaa181c350c6ee912d58f648927fb835b3ce7f3`; assembler SHA-256 `8bcce2eafe37e5ca11e1a145e4c6c826071eca55917ddb464a1b6da190f6ccd1`.
- In the isolated `/tmp` checkout, `python3 .ufo/evidence/round-18/measure.py --selftest` → exit 0, `MEASURE_SELFTEST: 98/98 pass`.
- In the isolated `/tmp` checkout, `python3 .ufo/evidence/round-18/coldread/assemble.py --selftest` → exit 0, `SELFTEST: 80/80 pass`. Includes carry-only passthrough and a synthetic old-page-SHA carry case covering the measured HEAD page (`assemble.py:1319-1348`).
- No-report carry command, reading the round-17 ledger and writing only under the `/tmp` scratch directory → exit 0; `ledger written: .../round18-carried.json (68 entries)`, `coverage: 58/58 buckets covered`, `carry coverage basis: section sha256; informational (measure.py is credit authority)`.
- Requested base carry measurement at rev `183f87b899e6cae46be98d251cbc87fb5118f6ca`, using that temp carry ledger → exit 0; `sections_covered=58/58`, `reasons={'credited': 58}`, `box3_full_page=True`, `box3_link=False`, `restraint=6`. The base checklist still links round 17 (`SHONEN.md:11`), so this is the expected round-18-link result per L1 ruling.
- Round-17 meter comparison at the same base rev → exit 0; `sections_covered=58/58`, `box3_link=True`, `restraint=8`.
- Fixture commit `0b71a5f534bb2219a230e793f91e467be11cd828` in the scratch clone used the staged canonical `.ufo/waves/round-18/staged/SHONEN.md` (round-18 pointer at line 10). Round-18 measure with the same carried ledger → exit 0; `sections_covered=58/58`, `box3_full_page=True`, `box3_link=True`, `restraint=8`.
- `diff -u` against both round-17 source files returned the expected exit 1 (files differ). The hunks are confined to the round-18 ledger/link/input exclusions, `--explain`, carry/receipt/coverage behavior, and associated synthetic selftests/documentation.

## Risks and blockers

- The `--ledger-file` measurements are overrides (`trace_gate=legacy`) and are calibration comparisons only, not strict claims; the measurement itself remains the credit authority. Carry coverage is explicitly informational.
- No remaining blockers. No tools were installed; all Git-writing selftests and the staged-SHONEN fixture ran only in the `/tmp` clone.

**Verdict: built — 58/58 carried credit confirmed at base (restraint 6 as ruled), with the staged round-18 checklist fixture reaching 58/58 and restraint 8.**
