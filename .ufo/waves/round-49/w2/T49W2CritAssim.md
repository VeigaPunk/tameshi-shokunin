# T49W2CritAssim — assimilation decisions at `f181a961ae44061af486f600e5ea257d2baf78f8`

Review axes: assimilation grounding, QUALITY 94 decisiveness, document-keyed IDs, exact `used-by`, and CORPUS rule 4.

## Finding A1 — `used-by` omits the lesson that cites both new rows

**Counterexample.** The newly added S269 and S270 rows list only `corpus/knowledge/pbt-generator-pilot.md` in `used-by` (`corpus/SOURCES.md:144-145`), but the round lesson itself cites S269 and S270 and reproduces their source-grounding quotes in its Gate (`corpus/lessons/round-49.md:18-29`). CORPUS defines `used-by` as paths of knowledge entries or lessons citing the row (`/home/vgpnk/Projects/shokunin/CORPUS.md:107-108`); therefore the values are not exact/complete.

**Evidence and command.** `grep -nE 'S269|S270|pbt-generator-pilot' corpus/SOURCES.md corpus/lessons/round-49.md corpus/knowledge/pbt-generator-pilot.md` shows both new rows at `SOURCES.md:144-145`, with only the pilot path in each `used-by`, while the lesson references S269 at `round-49.md:18,44-45` and S270 at `:25,46-49`. Observed output includes:

```text
corpus/SOURCES.md:144:... | mined | 2026-10-26 | 365d | corpus/knowledge/pbt-generator-pilot.md |
corpus/SOURCES.md:145:... | mined | 2026-10-26 | 365d | corpus/knowledge/pbt-generator-pilot.md |
corpus/lessons/round-49.md:18:- **S269** ...
corpus/lessons/round-49.md:25:- **S270** ...
```

**Impacted axes:** assimilation record integrity; provenance / exact source-use accounting. This is a correction needed even if all admission decisions stand.

**Smallest safe correction:** append `corpus/lessons/round-49.md` to the `used-by` cell of S269 and S270, logging the old→new values in the lesson as CORPUS rule 2 requires. Do not add rows for the rejected/deferred entries: neither is cited by the two new rows' admitted pilot entry.

## Checks of the other requested decisions

- **Admits re-grounded:** lesson Gate gives 2026-10-26 access dates, fetch details, hashes, located quotes and source locations for both S269/S270 (`corpus/lessons/round-49.md:18-29`). The admitted pilot independently cites the corrected snapshot-backed locators and opened date (`corpus/knowledge/pbt-generator-pilot.md:1-4,17-29`). S270's incorrect staged §4.1/p.44 locator is expressly corrected to §2.10/p.34 (`round-49.md:46-49`). Evidence: `grep -nE 'S269|S270|accessed 2026-10-26|§2.10|print out a histogram' corpus/lessons/round-49.md corpus/knowledge/pbt-generator-pilot.md`.
- **Reject reasons vs QUALITY 94:** the QuickCheck-correction rejection cites QUALITY 2, identifies the false receiving-lane lead-history premise and gives no flip (`round-49.md:50-53`); its triage evidence reports no DOI hit in the receiving lane/history and 404 resolution (`w1/T49ScribePkgQuickCheckCorr.md:11-28,115-122`). This is a decisive truth/anchoring defect, not the weaker locator or retrieval defects. The craft-author rejection cites QUALITY 2/3 and states false premise, unresolved S116, contradiction with held rows, plus a flip condition (`round-49.md:54-57`); the triage report identifies QUALITY 3 + 2 as decisive (`w1/T49ScribePkgCraftAuthor.md:37-52,141-146`). Both match QUALITY 94's requirement to cite the criterion that alone decides and state a flip (`corpus/QUALITY.md:1382-1390`). Evidence: `grep -nE 'Reject|Decisive reason|Flip|criterion 94|Criterion 94' corpus/lessons/round-49.md corpus/QUALITY.md`.
- **Document-based renumbering:** the lesson explicitly maps staged S182→S269 (QuickCheck) and S183→S270 (Smallbone) (`round-49.md:37-42`); `SOURCES.md:144-145` names the corresponding documents. The map is consistent; no row is assigned by staged identifier alone.
- **CORPUS rule 4 / unused appended rows:** S269/S270 are both cited by the admitted pilot entry (`corpus/knowledge/pbt-generator-pilot.md:1-2,17-29`), and the coverage row lists those same sources (`corpus/README.md:597`). The staged S157/S166 rows were not appended, consistent with the decision to defer their entry; no uncited row among the two additions was found. CORPUS rule 4 is at `/home/vgpnk/Projects/shokunin/CORPUS.md:123-125`. Evidence: `grep -nE 'S269|S270' corpus/SOURCES.md corpus/knowledge/pbt-generator-pilot.md corpus/README.md`.

## Summary

- One concrete defect: S269/S270 `used-by` omits `corpus/lessons/round-49.md`, which cites both rows.
- Smallest correction: add that lesson path to both cells and log the append-only change.
- Re-grounding, QUALITY 94 reject rationale, ID-by-document mapping, and no-unused-row checks otherwise hold on inspected evidence.
