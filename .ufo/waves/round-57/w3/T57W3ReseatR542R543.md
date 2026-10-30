# Blind re-seat: R54.2 / R54.3

Axes: calibration; blindness/provenance integrity. Both items: **fixed** in the lane record by `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Scope: only scratch clone bytes and history through `5e3569969b532310d2b8a3d130901757a3df356b`; no ledger or round-57 artifact read. Shared clone checked out detached at that base after asserting its top-level directory. The required clone initialization was the sole use of the source lane as a git source; no git command used lane cwd or `-C`.

## Evidence

Every command and its exact stdout/stderr and exit status is in `T57W3ReseatR542R543-receipts/commands.json`.

- `git -C CLONE log --diff-filter=A --format='%H %s' BASE -- ABSOLUTE_SPOTCHECK_PATH` identifies spot-check addition `650987a0d6fc285b37f0f9e63a3aae864af9cd5a`.
- `git -C CLONE merge-base --is-ancestor ADDITION FIX` and `FIX BASE`: both exit 0, empty output.
- `git -C CLONE blame -L 2569,2569 BASE -- ABSOLUTE_SCORECARD_PATH`: `9cf0146b ... 2569) 077d431e ... (5 amendments)`.
- The same command at `2609,2609`: `9cf0146b ... freeze 077d431e (amendments 1-5)`.
- `git -C CLONE show BASE:.ufo/evidence/round-54/after/frozen.stdout`: `FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c`.
- Blame at `2585,2585`: `9cf0146b ... unusable_exit2=3 docs=0 note=0 sources=0 total=13` with an explicit correction of the former inverted delta.
- `git -C CLONE show BASE:.ufo/evidence/round-54/before/c2.stdout`, line 8: `C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false`.
- Blame at `2642,2652` confirms the same fix commit explicitly labels the three former freeze pointers and the former total as old and supplies corrected values and receipt citations.

`CLONE` = `/fast/scratch/hyaku/tameshi-r57/T57W3ReseatR542R543/clone`; `BASE` is the full base hash above. Exact expanded commands are in the receipt.

## Residual risk / verification gaps

The original fleet report is not a tracked file in this clone (`git ls-tree BASE -- ABSOLUTE_REPORT_PATH` exits 0, empty output). Thus the verdict certifies the lane's explicit supersession of that report pointer at SCORECARD.md:2642-2647, not an in-place repair of external fleet bytes. Those bytes are outside the blind panel's permitted evidence.

R54.3's main false total is repaired. The historical contract's C2.before expands between 441c26be and 077d431e but is total=13 at both revisions; this supplemental disclosure observation does not undo the corrected numeric claim. No tool runtime rerun was needed for these documentary defects; receipts were inspected, not represented as newly executed counters.

LSP unavailable: `xd://lsp` returned `No such tool`; textual and git-history evidence is not semantic caller proof. No relevant executable/caller behavior changed in these two record fixes. No installs, edits to lane content, staging, tests, or admission performed.
