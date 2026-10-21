# FinalRevision — scoped falsification

Scope: one attack on `.ufo/waves/round-19/w1/FinalRevision.md`; advisory only. No suite, selftest, build, or production edit.

## Strongest assertion and verdict

**Agree** with the historical core: the three-revision ladder is non-discriminating for four routed items, while R18-5 is a receipt-attribution problem, not a reason to treat `a85f710` as a measurement endpoint. The report's preferred endpoints—frozen `7243e7f` baseline and delivered revision—are the sound choice.

Reopened evidence:
- At `a85f710`, `4b7c682`, and `7243e7f`, Git blob IDs match for the guard note (`9f9b60bf…`), case note (`ea61d7fa…`), round-18 lesson (`b1991bb8…`), and old checks (`d8c98a92…`). The old `measure-final-60.json` is absent at `a85f710`; its identical `4b7c682`/`7243e7f` blob says `revision=rev_input=a85f710`. This confirms the report's central provenance objection.
- The delivered `55e1d312` ruler and round-18 lesson are the exact Git blobs read here (blob IDs `d13dc4fb…` and `276cdd8a…`). The new R18-5 receipt names argv `python3 .ufo/evidence/round-18/measure.py --repo … --rev 4b7c682… --explain`, exit 0; its stdout/stderr hashes match, and parsed output has `revision=rev_input=4b7c682…`, `overrides_used=false`, 60/60 and restraint 8. This is a late repair, not evidence the receipt existed in round 18.
- Recomputed from the ruler's two SHA-pinned source snapshots: 62→76 rows; added 14, removed 0; changed rows are S001/S052/S056/S057 (`used-by` each) and S008 (`status`,`used-by`), hence 6 changed cells; 5 deleted table lines, 0 deleted non-row lines. This agrees with `sources-diff.txt` (`25 5`) and the lesson's R18-3 account.

## Concrete falsifier to the report's acceptance sufficiency

The report's minimal R18-3 acceptance asks for “line-79 arithmetic corrected to five” (FinalRevision §Minimal defensible acceptance, lines 103–105). The delivered lesson also corrects the distinct full-range statement at line 48: dated 2026-10-21, it says both line-48 and line-79 statements are “superseded as descriptions of the full range” (`corpus/lessons/round-18.md:157–172`). This is not a sixth defect.

But `measure.py` at `55e1d312` checks only the first R18-3 erratum section (`measure.py:165–182`); it does not require that later range/unit clarification or mention line 48. **Static counterexample [INFERENCE; not executed]:** remove that later clarification while retaining the first R18-3 erratum and the pinned source snapshots. The arithmetic predicate still sees its required “five deleted table lines”, IDs, diff command, six cell changes, and snapshot pins, so R18-3 can remain `corrected` despite line 48's full-range claim no longer being superseded. QUALITY 38 (`corpus/QUALITY.md:344–351`) also distinguishes line counts from cell counts.

**Impacted axes:** calibration (C1 measurement false-pass risk), discernment (subrange vs full-range attribution), quality (dated correction completeness).

**Smallest safe correction:** extend only the R18-3 predicate to require the line-48/full-range clarification and its five-replacement/six-cell distinction, while preserving the existing exact snapshot comparison. Do not add a denominator item.

## Residual unknown

At the delivered revision, `before.json` is 0/5 at `7243e7f` and `after-21e7932.json` is 5/5 at `21e7932`; both record ruler SHA `c538c33d…`, whereas the delivered ruler hashes to `bb651eef…`. The frozen revision contains no `after-55e1d31.json` (only the 21e receipt). Thus the final 55e1d312 5/5 result under the strengthened ruler is not yet evidenced here; the planned L1 final same-ruler audit must supply it before closure. No admission judgment made.