# RevAnchorOldNew — S089/S160 append-only anchor review

## Findings

- **No in-place S089 anchor edit is permitted.** `corpus/SOURCES.md:10` defines mutable registry columns (status, opened, recheck, used-by); `corpus/QUALITY.md:4-7` says claims need measured anchors and “Errata are append-only blocks.” The requested `CORPUS.md` is absent from the lane checkout (checked root and corpus listings); therefore its named Rule 2 could not be quoted. The operative local contract is consistent: `corpus/SOURCES.md:84-87` uses a new S-row to supersede anchors/teaches while retaining prior row, and `:381-383` explicitly says “S059 stays as it is.”
- **S092 precedent (exact row, `corpus/SOURCES.md:101`):** “| S092 | Remote Caching (Bazel docs) — https://bazel.build/remote/caching | docs | A | supersedes S059's anchor only: the markdown digest of the known-issues false-hit | §Known issues, heading \"Bazel does not track tools outside a workspace\" at markdown line 343, prose at line 345 @ https://bazel.build/remote/caching.md fetched 2026-10-23T05:50:48Z and 05:51:42Z (seat ReopenS059) and again by the L1, all sha256 266915c5d73f2cfe7d4ddcd9bb36a78e6037a710a71f2bab7d35b16d67768a5b, 16210 bytes, version unstated…” (row continues beyond rendered excerpt). The precedent supersedes **anchor only**, not by rewriting S059.
- **Planned S160 is canonical in form and respects S089:** The round-44 contract `.../.ufo/evidence/round-44/contract.json:40-43` requires a new census-valid S160 row and old→new logging. `.../.ufo/waves/round-44/w1/ScribeLessonDraft.md:35-38, 54-58, 64-73` explicitly says S160 supersedes S089's anchor only, keeps S089 document/status/teaches/used-by unchanged, and logs `bc572676…e04d` → S160; snapshot digest is recorded as `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce` at lines 15-18 and 43-48. This is a draft/intended plan, not a landed S160 row or completed lesson: `corpus/SOURCES.md:456` still says `Next unused id: S160.`; no S160 row exists. Thus the form and logged transition are evidenced in the plan, but actual landing remains unverified.

## Evidence

- `read corpus/QUALITY.md:1-8` → exact local rule: `4. Errata are append-only blocks.`
- `read corpus/SOURCES.md:84-87` → established superseding-row pattern; S075–S078 are new rows.
- `read corpus/SOURCES.md:98-101` → S089 old digest and S092 precedent row.
- `grep S160` lane-wide → only historical unrelated references/draft and registry pointer; none in `corpus/SOURCES.md`.
- No tooling installed.
