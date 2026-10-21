# FrozenPopulation — focused falsification

Review date: 2026-10-21. Scope: current C1 receipt freshness and the report’s R18-3 arithmetic assertion.

## Strongest assertion tested

FrozenPopulation Cx-1 (§ lines 37–50) says the only `corrected=5/open=0` after-receipt was uncommitted, and recommends committing it plus checking its inputs. **Agree as a dated observation at `21e7932`; disagree as a sufficient/current acceptance condition at delivered `55e1d312c4e8ac67aefad80099bd27581ff805c9`.** The report itself correctly called for re-checking this status.

## Evidence and concrete falsifier

- `after-21e7932.json` is now in the `55e1` tree; its JSON reports `revision=21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`, `corrected=5`, `open=0`, and `ruler_sha256=c538c33d…`. It is absent from the `21e` tree. All 13 recorded input SHA-256s match `git show 21e:<path>`, so its input/revision attribution is internally consistent, but the receipt itself was committed later.
- Concrete falsifier to the report’s proposed sufficiency: `55e1:.ufo/evidence/round-19/measure.py` hashes to `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`, not the receipt’s `c538c33d…`; that file’s Git blob matches the `55e1` tree entry. The only 5/5 receipt therefore predates and does not attest the delivered ruler or delivered revision. Matching `before.json` and old after-receipt ruler hashes to each other is not enough; both are stale against the new ruler.
- R18-3 arithmetic Cx-2 is repaired in the delivered ruler: `measure.py:99–126,165–182` compares SHA-pinned source snapshots by row/cell; snapshot SHA-256s match `git show 183f87b:corpus/SOURCES.md` and `git show 4b7c682:corpus/SOURCES.md`. Read-only `git diff --numstat 183f87b 4b7c682 -- corpus/SOURCES.md` reproduces `25 5`; its five deleted old lines are S001/S008/S052/S056/S057. The row comparison expects five changed rows/six changed cells (four `used-by`, S008 `status`+`used-by`), no removed rows, 62→76 rows. Thus Cx-2’s “never recomputed” description is stale for this build; `sources-diff.txt` is only a corroborating check.
- Attribution cross-check: the committed R18-4 witness receipt names argv `["python3","tools/bash-witness-study.py","selftest"]`, revision `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, exit 0 and digest-bound streams; the tool hash matches the source at that revision. R18-5 names argv `["python3",".ufo/evidence/round-18/measure.py","--repo","/home/vgpnk/Projects/shokunin/tameshi-shokunin","--rev","4b7c6823a462f5ea2eafcb262275300a545f3ed7","--explain"]`, revision 4b7c682, exit 0; output/receipt stream hashes and the companion instrument pin match. These attestations do not prove execution independently.

## Impact and smallest safe correction

Impacted axes: C1/calibration evidence freshness and A3 receipt commitment; A2 arithmetic gap Cx-2 is fixed. L1 should produce and commit fresh baseline and delivered-revision results with the frozen ruler (both `ruler_sha256=bb651…`), then run the planned public selftest. Until those results exist, this review does not treat C1 as independently closed.

Residual unknowns: no fresh same-ruler before/after receipt or current-ruler selftest result was present in the reviewed `55e1` evidence. No execution-authenticity claim is made. No ruler, suite, or selftest was run; no install.