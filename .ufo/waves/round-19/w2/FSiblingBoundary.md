# FSiblingBoundary — round 19 w2 (advisory)

**Axes in scope:** C1 calibration (five named defects, no numeric-score promotion); province/evidence boundary (repository identity and admissible evidence); no-harm (frozen baseline, sibling tree, and depth 8 unchanged).

**Strongest assertion attacked:** E9 / proposed move 1: same-id S008 rows in separate registries can share status/opened date, so R18-2 must bind to tameshi's pinned immutable cells rather than status/date/used-by alone.

**Verdict: agree; the identity correction is in delivered revision `55e1d312c4e8ac67aefad80099bd27581ff805c`.**

- [O] Tameshi S008 from `corpus/SOURCES.md@4b7c6823a462f5ea2eafcb262275300a545f3ed7` is cell-identical to `.ufo/evidence/round-19/source-round18-final.txt`; snapshot SHA-256 is `018ee9a86500efc6d07ea141d20c7de6b2ec76e5e808ffbf12508ada46a84e0e`, matching `measure.py@55e1d312` `SOURCE_PINS`.
- [O] Kumitate `corpus/SOURCES.md@1a8eed5`, row S008: `id`, `tier`, `status`, and `opened` match tameshi; immutable `source`, `kind`, `scope`, `anchor`, `teaches` differ; mutable `recheck` and `used-by` differ. The current nested sibling row still matches that cited row.
- [O] Frozen `measure.py@55e1d312`, `evaluate().source()` lines 149–164, requires the pinned snapshot digest and compares S008 cells at indexes 1,2,3,4,5,6,7,9 (identity plus immutable content/opened), then checks mined/date/used-by. Lines 330–336 encode a `kind=own-work` foreign-identity mutant expecting only `R18-2` open. This is static inspection; I did not run selftest.
- [O] Recomputed the saved E7 `external_inputs` classes against `/home/vgpnk/Projects/shokunin/kumitate-shokunin`: 110 keys = 95 live-tree, 13 revision-pinned, 2 scratch; live bytes = 63 same / 32 drift / 0 absent; pinned = 13/13. The named gate scripts and `PROVINCE.md` match; `corpus/SOURCES.md` differs as a whole. This reproduces the report's point-in-time arithmetic, not a claim about future sibling state.
- [O] `round18-final-measure.json:2–18` attributes that stdout to argv `python3 .ufo/evidence/round-18/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 4b7c6823a462f5ea2eafcb262275300a545f3ed7 --explain`, exit 0; stdout/stderr hashes match their files. The saved receipt is provenance, not a live sibling read.
- [O] Round-18 verifier spot-check §5 item 2 says S008 is “`mined` with this entry as used-by” (read 2026-10-21); this confirms the metadata defect's scope, not ownership of kumitate's gate.

**One concrete falsifier:** change only tameshi S008's kind to `own-work`, preserving the status/date and case used-by. If the frozen ruler still marks R18-2 corrected, the identity binding fails. The frozen selftest already declares this arm expecting `R18-2` open; outcome remains unexecuted here.

**Bounded move / remaining gap:** the substantive sibling-gate rejection is present in `round-19.md:212–218`, but the `## Gate` table (`:17–25`) has no corresponding row, despite the w1 recommendation. Consolidate the existing reject decision into that table and make the later paragraph a pointer/summary. This improves province/evidence-boundary traceability without changing C1 count, score, baseline, or sibling files.

**Risk:** duplicating the same decision in two places could create contradictory policy; keep one canonical Gate row. No-harm and province context: tameshi `PROVINCE.md:16–20,37–38,80–83` says “Out of province → report, never absorb” (read 2026-10-21).

**Residual unknowns:** no ruler/selftest or lane suite was run; this review does not establish a final same-ruler 0/5→5/5 receipt at `55e1d312`, producer authenticity, or an independent round-admission decision. The sibling hashes remain point-in-time external observations.