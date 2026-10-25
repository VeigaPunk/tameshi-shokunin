# Sibling overlap scan

Axes in the round-44 contract: calibration and freshness (`.ufo/evidence/round-44/contract.json:8-15`). Scan objective was adjacency: detect same registry-row and S-id parsing mechanisms in sibling lanes.

Command: read-only Python recursive scan over `/home/vgpnk/Projects/shokunin/{kumitate,kagi,kaidoku,kake,kotoba,mado,tsukuroi}-shokunin`, searching source/docs for `supersed`, `anchor`, `ASSIGN_ID`, S-id/value/citation markers. Results below distinguish actual lane files from stored round/wave artifacts (which are not current implementation).

## Findings

- **kumitate**: `corpus/SOURCES.md:94` includes ordinary `supersedes S004` style rows; its lessons describe append-only correction rows, e.g. `corpus/lessons/round-24.md:59-72`. `corpus/lessons/round-25.md:50` explicitly discusses a gate accepting an in-place `recheck` update (a narrow metadata exception), while round 26 says other row fields were not rewritten (`corpus/lessons/round-26.md:55,121`). No current extractor distinguishing assignment-bound S-ids from citation S-ids surfaced in the source-pattern scan. No `ASSIGN_ID` match surfaced. This is related registry practice, but S160 is not a duplicate: it is a new source-row superseding a stale source anchor; the recheck exception is metadata, not replacement of source identity/content.
- **tsukuroi**: round-24 lesson appends S104–S114 correction rows, each explicitly superseding an earlier row (`corpus/lessons/round-24.md:59-73`). The scan found no matching extractor/ASSIGN_ID in current tools. The append-only supersede practice is analogous to S160, not duplicate; there is no identified Stryker-specific or assignment-mask overlap.
- **Other requested lanes — kagi, kaidoku, kake, kotoba, mado**: no relevant current implementation match surfaced for in-place source-row anchor edits/superseding source rows or S-id assignment-vs-citation extraction in this scan. Registry supersede terminology may occur in prose or unrelated records; no overlap with S160/ASSIGN_ID identified.

## Caveat / verification

The initial broad recursive scan traversed archived `.ufo/waves` scratch copies as well as lane files, so those matches were excluded as non-current implementation. Searches are string-pattern evidence, not a formal exhaustive semantic audit. No changes made and no tests run. No tools installed.