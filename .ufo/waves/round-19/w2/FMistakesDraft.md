# FMistakesDraft — w2 falsifier of w1 `MistakesDraft.md` (round 19, advisory)

Seat TameshiR19-2.FMistakesDraft (leaf reviewer), read 2026-10-21; frozen build `55e1d312c4e8ac67aefad80099bd27581ff805c9` (master `e7039fd` changes no lesson/ruler byte). Installs: none.
Edits: this report only. Git read-only (`show/grep/log/diff/rev-list`, `--no-optional-locks`, `GIT_*` unset); blobs in disposable `/tmp/fmistakes-r19w2-2967303`. No ruler/selftest/suite/build/lint run.

## Strongest material assertion
MistakesDraft findings 2–3 + rows A/E: the landed captured-by for rows 3–4 is wrong; row 4's "Evidence standard, criterion 26" should be
QUALITY 2; §5 item 1 had "Captured-by: none at round-18 admission". L1 adopted it at 55e1d31 `corpus/lessons/round-19.md:134–137`:
"the missing exact-revision receipt by QUALITY2. QUALITY26/35 cover correction mechanics, not the original prevention duty."

## Verdict: SPLIT — agree on row 3; disagree on row 4 and on row A's "none"
- Agree, row 3: QUALITY 17 at 183f87b `QUALITY.md:80–81` "Explicitly classify every nonzero exit, including usage"; QUALITY 15 `:61–65` also predates
  round 18. `final/checks.json` row: argv `--selftest`, rev `921ef80…`, exit 64, stdout `e3b0c442…` (empty). Landed "QUALITY 26/35 lacked…" omits both.
- Disagree, row 4 / row A: MistakesDraft never opens PROTOCOL.md (0 "PROTOCOL" hits in its 93 lines) and reads "Evidence standard, criterion 26"
  as criterion 26 alone. "Evidence standard" is the fleet PROTOCOL section this lane's corpus already cites at 183f87b
  (`lessons/round-1.md:117–118` claimed-vs-re-executed; `lessons/round-16-verifier-spotcheck.md:205` "corrections sweep every mention").

## Evidence (observation)
1. Fleet `PROTOCOL.md` at `7c5b34f` (2026-10-19T19:08:33-03:00; round-18 launch 2026-10-20T16:23:30-03:00), §Evidence standard:
   `:347` "an unreachable claim in a lane report does not exist."; `:361` Claimed ≠ re-executed: "a re-run performed at write time with its
   observed output — never an output quoted from memory or a prior session"; `:363–365` "a corrected fact left standing in a sibling file is
   still a defect." Same text now at fleet `:347/361/363` and kimi `skills/shokunin/protocol/PROTOCOL.md:360/374/376`.
2. Round-18 lane report, fleet `a85e4d8` `.ufo/reports/round-18/tameshi.md:53`: "the same no-override count at final `4b7c682…` returned
   **60/60,8**, exit0." No pointer of its own; the adjacent receipt `final/measure-final-60.json` is revision `a85f7107…`.
3. QUALITY 8 at 183f87b `QUALITY.md:21–23`: "an executed-but-unreported verification is named debt, never cited as a pass."
4. QUALITY 2 `QUALITY.md:4–5` (same 183f87b→55e1d31): "Every claim carries a source: a measured anchor (path:line, command, evidence id) — never
   oral knowledge." MistakesDraft row E adds "at the revision it describes"; that qualifier is not in the source.
5. 55e1d31 `round-19.md` names no PROTOCOL.md, re-executed, sweep-every-mention or criterion 8 (`grep -i -E`: sole hit `:138`, a `…/protocol/CORPUS.md` path); "Evidence standard" survives only in row-4 cell `:53`.

## Concrete falsifier
`git -C /home/vgpnk/Projects/shokunin show 7c5b34f:PROTOCOL.md | grep -n "Claimed ≠ re-executed\|Corrections sweep every mention\|unreachable claim in a lane report"`
→ `347`, `361`, `363`. If MistakesDraft were right that row 4's landed capture is wrong and §5 item 1 had no prior capture, this pre-round-18
text would be absent. It is present. An unretained "returned 60/60,8, exit0" at `4b7c682` is an unreachable, claimed-not-re-executed
lane-report claim (or, if it ran, QUALITY 8's executed-but-unreported pass). PENDING at guard-kill `:2` beside EG-1, and S008 "queued" at
kumitate `:1` beside ER8-1, are corrected facts left standing. QUALITY 2 is the weakest fit: naming a command satisfies its literal text.
Inference: §5 items 1–2 repeat a rule the round-16 verifier already enforced on this lane. "QUALITY 35 partly" (row 1) and "QUALITY2" (row 4)
hide that repeat. Repair: dated named erratum after `:134–137` adding PROTOCOL §Evidence standard and QUALITY 8; no in-place rewrite.
C1 impact: none on the count — 55e1d31 `measure.py` has no captured-by/Mistakes/QUALITY/PROTOCOL predicate (`grep -i`: 0 hits); not a sixth defect.

## Secondary (stale or already repaired at 55e1d31 — not current build defects)
- Row C's numstat falsifier cannot fail its own immutable case. In-memory difflib over blobs: control 183f87b→4b7c682 = 25 added/5 deleted, IDs
  S001/S008/S052/S056/S057; mutant with S001 `opened` 2026-10-19→2026-01-01 gives the same 25/5 and IDs (QUALITY 38: deletion counts do not prove
  cell compliance). Delivered `measure.py:101–126,172–175` rejects `immutable_changes` and pins 6 changed cells. Superseded.
- Range overlooked: 58e5d53→9ee1c80 numstat 11/4 (S001,S052,S056,S057); 183f87b→58e5d53 15/2 (S008 + footer "Next unused id"). Repaired by
  w1 SourceCorrection (`QUALITY.md:377–386` at 55e1d31).
- Self-count: the verdict reports "Four landed-table findings" but the report lists five; the citation-path finding is omitted.
- C-12 lacks a revision. `grep -c not4b7c682` = 2 at 55e1d31 (`:53`, `:139` integration quote). The report's 1 predates integration [inference].

## Arithmetic reproduced (agree)
C-6–C-8 as reported: complete stdout sha recomputed `316b9713…`, lines 44–45 `WITNESS_SELFTEST: 43/43 pass` / `VERDICT: PASS`; `supersedes` names both failed rows; failed-run stderr `:14` FileNotFoundError for `tools/mutate-and-run.sh`. C-9: `a85f7107…`. C-10: argv `--rev
4b7c6823… --explain`, exit 0, 2026-10-21T05:28:25Z; recomputed stdout sha `55c530bb…` matches; stderr 0 B; 60 / 8 / `overrides_used=false`.
C-11: before 0/5/5 at 7243e7f, after 5/0/5 at 21e7932 (initial ruler; strengthened before/after still pending L1). C-3: 55e1d31 PENDING lines
2,10,53,65,91,97,114,118,120,122,132,136,143,173,174,194,197. The erratum's `:134` is a "Not run…landed tip" statement, `:143` is EG-1, `:173+` errata.

## Residual unknowns
- Whether round 18 actually ran measure at 4b7c682. This decides QUALITY 8 vs Claimed ≠ re-executed; both rules predate round 18.
- Canonical copy: fleet `CORPUS.md` (sha `885564…`) and kimi `protocol/CORPUS.md` (`b6ed4476…`) differ but both carry the count rule at `:34`.
- Whether L1 intends the `:53` "Evidence standard" cell to stand beside the `:134–137` QUALITY2 correction. The prose does not retract it.
