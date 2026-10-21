# FRegistryNoHarm — round 19 attempt 1, w2 falsifier (2026-10-21)

Target `.ufo/waves/round-19/w1/RegistryNoHarm.md` (observed at 21e7932). Re-opened at frozen `55e1d312c4e8ac67aefad80099bd27581ff805c9`;
master `e7039fd` equals it on every path below (adds only `current-ledger-monitor-55e1d31.json` + wave files). Read-only git blobs/JSON/
static code; no gate, suite, selftest or ruler executed; no installs; no git writes; only this file written.

## Strongest material assertion
§Finding ¶1 (w1, 2026-10-21): "No active registry row or round-13 pin/evidence-disposition input directly names the three round-18
corpus files being corrected" → those registry/disposition receipts need no rewrite.

## Verdict: AGREE on the conclusion at 55e1d312; DISAGREE that the report's evidence establishes it
Observed/reproduced: `tools/registry.json` sha256 3e6785ee… is identical at 7243e7f, 55e1d312, e7039fd and worktree: 35 rows,
0 added/removed/changed; no active argv contains `corpus/`. Every other attribution matches: pin-manifest has 6 legs (kumitate 2,
kagi 2, tsukuroi 1, mado 1); pin-dispositions 2026-10-20T04:59:26Z, 3/3/0, `not_established`; dispositions(-before) inputs =
round-13 expected/producer-oracle-repair/verification + round-14 file; final/disposition.stdout effective 11, superseded 1,
exit 0, tool dated 2026-10-20, 13 expected_inputs_verified (round-12/13 + tools, no corpus); round18-final-measure.json
`--rev 4b7c682… --explain`, exit 0, 2026-10-21T05:28:25.715990+00:00, stdout sha 55c530bb… matches, score 8.
Gap, because matching argv text is not a valid no-harm test:
- Active gate `sources-census` (expects `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`) reads `corpus/SOURCES.md`
  (`kaika-round-1/sources-census-v2.sh:9`) and via Part A/B2 (:16-19) opens every mined used-by file, i.e. all three corrected
  files: S008→mutation-case-kumitate-sources-check.md, S077/S078→lessons/round-18.md, and (new at 55e1d312)
  S063/S077/S078→guard-kill-closure.md.
- SOURCES.md is outside the report's "three files" yet is a pinned after input, and is edited in place: numstat 7243e7f→21e7932
  9/1, 21e7932→55e1d312 3/3 (S049,S063,S077,S078 used-by). The three named files are pure insertions (21/0,12/0,36/0 then
  17/0,6/0,46/0).
- `measure-round16-rev` reads SHONEN.md + corpus/SOURCES.md at HEAD (round-16/measure.py:57-59,271-274); its expect (exit 0 +
  two keys) is value-agnostic and the file has no sys.exit: not harmed.
The decisive evidence is mine. Read-only Python emulation of census :9-19 over `git show REV:` blobs (rows `^\|\s*S\d{3,}\s*\|`
split on `|`, len 13; enum/dup checks; per mined `[,;]` used-by p: `git cat-file -e REV:p` and ID or basename(URL after last
" — ") in blob) returns CLEAN at 7243e7f (75 pairs), 21e7932 (76), 55e1d312 (79), e7039fd (79); 76 rows each. New pairs are
cited by pre-existing lines (guard S063 l.1, S077 l.164 plus basename l.1, S078 l.163; round-19.md S049 l.27). B2 is a
contains test, so insertions cannot drop a cite.

## Stale/missing correction overlooked (frozen surface; report predates it)
- The fallback "If the intended append is already included in 21e7932, this receipt is already the corresponding round-19
  measurement" is false at 55e1d312. All four pinned corpus digests changed (SOURCES 3ecc4a09→b684833d, guard
  7728d56a→9d231b1a, case a69d9a86→d961a0d6, round-18 179677b0→88b17f6d; other 9 equal). The ruler moved c538c33d…
  (recorded in before.json AND after-21e7932.json) → e9b44cad… (7af123b) → bb651eef… (55e1d312 = master).
- The delivered ruler pins 17 PATHS (measure.py:46-51) against the receipts' 13. Three of them (INSTRUMENT, source-baseline.txt,
  source-round18-final.txt) are ABSENT at 21e7932. `--rev` maps absent → None (:394); `strict_json(data[INSTRUMENT])` (:206)
  raises TypeError; check() then marks R18-5 open (:132-136). So the delivered ruler cannot give 5/5 at 21e7932 [static, not run].
- `frozen-runs.json` (added 7af123b, when the ruler was already e9b44cad) still declares after = 21e7932 / after-21e7932.json /
  expected 5/0/exit 0. Its only ruler pin is "present in each receipt" (= c538c33d); no consumer found. before.json is also
  first-ruler, so "after-21e7932 is the only receipt … to refresh" misses that the same-ruler baseline needs re-measuring too.
- Neither 55e1d312 nor e7039fd holds a bb651eef before/after receipt, so C1 5/5 at the delivered revision is unreceipted until
  L1's declared final run. Both receipts lack argv/exit/stream digests. QUALITY.md:352 (read 2026-10-21): "A final-success
  claim names one effective receipt with matching argv, measured revision, integer exit, retained stdout/stderr and both digests."

## Concrete falsifier
AGREE flips if the registered `sources-census` run on 55e1d312's tree prints `SOURCES_CENSUS: VIOLATIONS`, or if any active row's
outcome at 55e1d312 differs from 7243e7f. Failure-capable: the in-memory control B2(S077, guard) = True. Dropping the guard lines
holding S077 or its URL basename (1, 164, 202, 205) gives False, so census would print
`no-id-or-path-cite: S077 corpus/knowledge/guard-kill-closure.md` while the report's argv selector still returns zero rows.

## Residual unknowns
- Gates were not run (bound); CLEAN comes from emulating committed blobs, not a worktree gate run.
- Transient worktree ruler: before mtime 03:28:01-03:00, `.ufo/evidence/round-19/measure.py` hashed 8b6eb1fe… (440 lines); it was
  then restored to bb651eef… (0-line diff). Actor unknown, refs unaffected. Since ruler_sha256 = digest(__file__), final receipts
  must show bb651eef… or name their ruler.
- Status of R18-1/2/4 under the delivered ruler at 21e7932; whether L1's final run will mark frozen-runs.json as superseded.
