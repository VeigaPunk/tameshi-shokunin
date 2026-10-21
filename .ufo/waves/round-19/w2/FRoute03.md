# FRoute03 — R18-3 arithmetic review (2026-10-21)

Axes: evidence fidelity; correction precision; failure-capable detection.

## Strongest assertion — agree, historical defect; corrected in delivered revision

Route03 §Finding (w1/Route03.md:7-18) is right that the pinned full-range SOURCES diff deletes five table lines: S001, S008, S052, S056, S057, with S008 changing both status and used-by. Primary: `corpus/lessons/round-18-verifier-spotcheck.md` §5.3, lines 192-195: “5 deleted lines (S001, S008, S052, S056, S057)” (opened 2026-10-21).

Independent read-only parse of the SHA-pinned snapshots in the delivered 55e1d312c4e8ac67aefad80099bd27581ff805c9 tree reproduced: 62→76 rows; no removed row IDs; changed fields are S001/S052/S056/S057 `used-by`, and S008 `status` + `used-by` (six changed cells); no immutable-cell changes or deleted non-row lines. Snapshot hashes match the blobs at 183f87b899e6cae46be98d251cbc87fb5118f6ca and 4b7c6823a462f5ea2eafcb262275300a545f3ed7. `sources-diff.txt` records `git diff --numstat 183f87b… 4b7c682… -- corpus/SOURCES.md` → `25 5 corpus/SOURCES.md`.

The delivered frozen `measure.py` is byte-identical to the inspected file (SHA-256 `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`). Its `DIFF_COMMAND` (lines 26-27) pins the same revisions/path; `arithmetic()` (165-182) checks pinned snapshots, exact changed cells/count, no removed IDs/immutable changes/non-row deletions, row counts and the expected IDs. No selftest or lane suite was run.

Correction status: at 55e1…, `corpus/lessons/round-18.md` §“Erratum R18-3” (lines 121-129) corrects the old line-79 statement. Its §“R18-3 range and unit clarification” (157-164) adds the missing precision Route03's proposal did not state: the five deleted lines are replacements, not removed IDs, and the full-range result is six changed cells (not “four cells”). Quote: “are five replacements, not removed source rows” (2026-10-21). Thus Route03 identified a real historical error, but it is not an open defect at the delivered revision.

Concrete falsifier: the assertion fails if the pinned full-range row/cell comparison does not equal the five listed changed IDs and fields above (in particular, if S008 lacks either `status` or `used-by`). It equals that expectation here.

## Low — citation/attribution gap

Route03:7 attributes the routing to `.ufo/waves/round-19/contract.json:9`; that exact path is absent from the current wave tree and from the 55e1… tree (`git show 55e1…:.ufo/waves/round-19/contract.json` reports no such path). The route-ID linkage is therefore unverified at that citation. The cited spot-check §5.3 independently supports the underlying R18-3 defect, so this does not change agreement on the arithmetic.

## Residual risk / verification gaps

Route03's proposed predicate (lines 32-38) checks the removed-ID list only; unlike the delivered ruler, it does not itself validate replacements or changed-cell semantics. The recorded `sources-diff.txt` is a transcript, not an authenticated execution receipt for Route03's historical command/author. No arbitrary historical authenticity is claimed. No LSP caller checks were needed for this Markdown/evidence review.