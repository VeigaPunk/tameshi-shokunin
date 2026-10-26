# T48W2ScoutCensus — census BASE vs CONTENT (tameshi, round 48 attempt 2)

Judged on: freshness. Milestone: census start vs end. Read-only; evidence below is observed output.

## Preconditions
- `git -C tameshi-shokunin diff --stat c7586b9a... -- corpus` printed nothing (rc 0): working-tree corpus/ equals CONTENT. Lane HEAD is 17cc5ce (spec commit on top of c7586b9).
- BASE 473336d9 and CONTENT c7586b9a were each extracted with `git archive <rev> | tar -x` (excluding .ufo) into scratch trees, so the BASE numbers are read from BASE bytes, not inferred. Live-lane numbers match the CONTENT extraction exactly.
- The frozen manual census is in `/home/vgpnk/Projects/shokunin/CORPUS.md:131-148` (fleet root file; there is no `corpus/CORPUS.md` in the lane). Its commands were run with `corpus/SOURCES.md` paths from each tree root, with the commands copied verbatim.

## Manual census (CORPUS.md 131-148), BASE -> CONTENT
| metric | BASE | CONTENT (= live lane) |
|---|---|---|
| rows | 124 | **128** (+4: S265, S266, S267, S268) |
| malformed (NF!=13) | 0 | 0 |
| tier | A=111 B=10 C=3 | A=114 B=11 C=3 (+3 A: S265-S267, +1 B: S268) |
| status | mined=96 queued=22 rejected=6 | mined=100 queued=22 rejected=6 (+4 mined) |
| duplicate ids | none | none |
| enum violations / tier inflation | none | none |
| mined used-by paths missing | none | none |

Note for the used-by check: it resolves paths from the lane root. Run in a scratch tree without tools/ it reported missing tools/tally-audit.py and tally-audit-v3.py; that was an extraction artifact (corpus-only archive), gone once the full tree was extracted. Not a lane finding.

## sources-census.sh validate, BASE -> CONTENT
Command: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` on the live tree prints 16 lines (15 findings + `ok .../corpus/SOURCES.md`). The same script on the BASE and CONTENT extractions printed 12 lines and 16 lines, rc 0 both (clean lane, warnings only). **No E-lines at BASE or CONTENT.**

W/E lines: BASE 11 warnings (W04 x10: S047 S048 S075 S076 S077 S078 S081 S092 S104 S160; W01 x1: S101 tierC mined). CONTENT adds exactly four, all W04, all naming a new row:
- `W04 S265 duplicate url testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html across scopes` (partner S026)
- `W04 S266 duplicate url pitest.org/quickstart/incremental_analysis across scopes` (partners S041, S047, S048)
- `W04 S267 duplicate url github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml across scopes` (partner S093)
- `W04 S268 duplicate url www.tensorflow.org/federated/golden_tests?hl=zh-cn across scopes` (partner S108)
No other line changed (`diff` of BASE vs CONTENT outputs, path column stripped, showed only those four additions). No W01/W02/W03 on a new row; no existing warning disappeared (S048 keeps its W04 from BASE).

## Observations
1. The W04s are the expected shape of a supersession: same URL as the held row, different scope string ("supersedes Sxxx's anchor and quote only: ..."). The census script does not read the `supersedes` marker, so superseded rows S026/S048/S093/S108 stay `mined`, keep tier, and keep the same used-by file as their successor (S026/S265 -> repeated-control-precondition.md; S048/S266 -> incremental-pin-disposition.md; S093/S267 -> regression-tally-completeness.md; S108/S268 -> r8-golden-update-flag.md). The histograms therefore count both old and new; the census cannot show the supersession as a state change. Any freshness claim that the held rows are "retired" must come from the C2 counter, not from this census.
2. S266 is the only new row whose URL has 3 earlier holders (S041, S047, S048); its W04 is one line, the script flags every later occurrence once.
3. Tier mix of the new rows mirrors the held ones (S268 B like S108; S265-S267 A like their originals): no tier change and no tier-inflation hit.
4. Unchanged pre-existing warnings (10 W04 + W01 S101) are baseline noise, not introduced by round 48.

## Scratch
All work under /fast/scratch/hyaku/tameshi-r48/T48W2ScoutCensus (9.1 MB); removed before yielding. Tools installed: none.
