# NegativeControls — scoped falsification (2026-10-21)

Axes: C1 calibration (five routed defects only); source-provenance/no-harm boundary.

## Strongest assertion and verdict

`w1/NegativeControls.md:14-21` reports all five mutations accepted by the ruler at `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9` (2026-10-21 02:48:27-03:00). **Agree historically; disagree as a falsifier of delivered `55e1d312c4e8ac67aefad80099bd27581ff805c9`** (03:13:53-03:00). I read the exact old ruler and the exact 55e1 ruler: old predicates omit the reported controls; 55e1 adds targeted checks for all five (`measure.py:139-222`). This is a stale-as-current observation, not evidence the w1 run was fabricated.

- NC-1: `guard()` now requires the exact `PROBES` path and matching retained digest/tally (`measure.py:139-148`); R18-1 names that path once (`guard-kill-closure.md:179-183`, erratum dated 2026-10-21).
- NC-2: `source()` pins S008's `opened=2026-10-19` and compares it to the SHA-pinned final source row (`measure.py:149-164`).
- NC-3: `arithmetic()` requires the full frozen `DIFF_COMMAND` (`measure.py:26-27,165-182`). Re-read its cited Git numstat: `25  5 corpus/SOURCES.md`; the before/after snapshot hashes match the ruler's two `SOURCE_PINS`, and their five changed rows contain six changed cells (S008 status+used-by; four other used-by cells). The exact R18-3 command and explanation are at `round-18.md:121-132` (2026-10-21).
- NC-4/5: witness now requires the pinned runner/tool hashes and exact supersession list (`measure.py:183-199`); receipts require timezone-aware `recorded_at >= FREEZE_TIME` (`85-96`). At 55e1, witness argv/revision/exit are `python3 tools/bash-witness-study.py selftest` / `4b7c682…` / 0; its stream hash matches. The tool hash recomputes from `4b7c682…:tools/bash-witness-study.py`. Measurement receipt argv exactly matches `measurement()`; `recorded_at=05:28:25Z` is 15.7s after the 05:28:10Z freeze. No receipt argv was executed.

## Concrete missed control

The report's NC-2 date mutation is fixed, but its proposed “every other cell” check is not complete: current S008 is `mined | 2026-10-19 | 365d | …` (`SOURCES.md:19`, 55e1). In `source()`, the parsed row checks indexes 1–7 and 9, status 8, and only membership of the expected path in used-by 11; it never compares index 10 (`recheck`) to `pinned_rows` (`measure.py:149-164`). `compare_sources()` covers only the two pinned snapshots, not live `SOURCES` (`99-126`). **[INFERENCE; not executed]** A snapshot changing only S008's live `recheck` cell from `365d` would leave R18-2 corrected: no current predicate reads that cell. This conflicts with round-19's “immutable cells” description (`round-19.md:212-215`), not with the currently correct S008 value.

Smallest safe correction: compare the normalized live S008 row to its pinned final row, including `recheck` and exact `used-by` (or explicitly enumerate allowed cell deltas).

Residual unknown: no mutation probe, ruler, or selftest was run from this read-only seat; the recheck case is a static counterexample only. The runner hash is value-pinned by the ruler, not re-derived there from scratch-runner bytes; producer authenticity remains outside this check.