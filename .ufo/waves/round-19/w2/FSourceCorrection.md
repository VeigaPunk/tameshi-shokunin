# FSourceCorrection — falsification (2026-10-21)

## Strongest assertion selected; verdict
- SourceCorrection §Findings F4 / E7 says the predicate “never reads historical SOURCES bytes” and reports the in-flight predicate accepting M1–M4.
- **Disagree as a claim about delivered revision `55e1d312c4e8ac67aefad80099bd27581ff805c9`**: that observation is stale for the frozen delivery; it may describe the earlier changing ruler the report observed.

## Evidence
- Used `measure.py` from the explicit frozen commit, not the live worktree copy (which differs). Its `SOURCE_PINS` bind `source-baseline.txt` to `ac82b2df…c828d5` and `source-round18-final.txt` to `018ee9a8…a84e0e`.
- Read-only byte comparison: frozen baseline snapshot equals `git show 183f87b899e6cae46be98d251cbc87fb5118f6ca:corpus/SOURCES.md`; frozen final snapshot equals `git show 4b7c6823a462f5ea2eafcb262275300a545f3ed7:corpus/SOURCES.md`, with those exact pinned SHA-256 values.
- Frozen `measure.py` `main()` loads its `--rev` inputs through `git show <rev>:<path>` (:384–401). `compare_sources()` parses row IDs/cells and computes changes, removals, immutable-cell changes, and net non-row deletions (:99–126). `arithmetic()` checks both snapshot pins, exact changed-cell map (S001/S052/S056/S057 `used-by`; S008 `status` + `used-by`), six changed cells, no removed IDs/immutable changes/net non-row deletion, 62→76 rows, exact IDs, and the retained numstat record (:165–182).
- Independent read-only arithmetic agrees with the correction: `183f87b..4b7c682` is `25 5`; five changed row lines, six changed cells, zero row IDs removed. Per-window, the footer is absent at `58e5d53` and restored at `9ee1c80`.
- Round-18 lesson at the frozen revision now has a range/unit clarification (:157–181): five replacements, six cells, and the intermediate footer deletion/restoration are explicit. The round-19 sweep uncertainty in SourceCorrection F5 is resolved at `55e1d312`: `7243e7f..55e1d312` is `12 4`, S049/S063/S077/S078 `used-by` only.

## Concrete falsifier
The two ruler inputs are byte-identical to the named historical SOURCES blobs, and `arithmetic()` consumes `compare_sources()` on those inputs. This directly falsifies F4/E7’s “never reads historical SOURCES bytes” for the delivered frozen ruler. No selftest or mutant probe was run; the rejection paths are established by source inspection, not execution.

## Affected axes, move, risks, verification
- **Axes:** C1 calibration-measurement integrity and verification provenance; no numeric calibration promotion is supported.
- **Move:** treat F4’s transcript-only/mutant-blind conclusion as revision-stale; retain the delivered pinned-snapshot checks. Advisory wording cleanup only: lesson line 131 still says “five removed row IDs,” while lines 161–164 clarify these are replacements and no source rows were removed.
- **Residual / risk:** frozen `compare_sources()` checks endpoint multiset subtraction (`old_other - new_other`), not each intermediate commit; by itself it cannot detect delete-then-restore. The lesson records that event, but this ruler does not execute a per-commit append-only audit. Whether a separate receipt covers it was not established here. Do not interpret the net-zero result as proof of uninterrupted append-only compliance.
- **Verification performed:** read-only frozen-blob inspection, snapshot SHA/byte attribution, and independent SOURCES arithmetic only; no tests, selftests, builds, lint, or formatters run.