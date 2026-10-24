# ScribeRoundLesson — round-37 lesson Gate and Mistakes draft audit

Seat: ScribeRoundLesson (scribe, w1). Task: draft the round-37 lesson Gate and
Mistakes entries from committed evidence, including S104 URL/date/located quote,
the class/evidence/captured-by/fix fields, and the explicit parser non-goals.

## Status

`corpus/lessons/round-37.md` is **already committed** at HEAD `e6185d5` ("round-37:
records — LOG/SCORECARD/QUALITY/lessons, S104 row, pending evidence, inherited
r36+r37 wave files"); `git status --porcelain` on it is empty. This seat therefore
drafts by **auditing the committed draft field-by-field** against committed bytes.
Verdict: all Gate fields and all four Mistakes tuples resolve; two precision
nuances found (report, not repair).

## Gate — S104 (verified)

- **URL** (`SOURCES.md:113`, `LOG.md:1982-1985`, lesson Gate):
  `https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303#L489-L493`.
- **Date**: "opened via official Savannah source on 2026-10-24" — consistent
  across row, lesson, LOG.
- **Located quote**: `@node ANSI-C Quoting`, "Character sequences of the form
  `$'string'` are treated as a special kind of single quotes." — 15 words
  (re-counted: 15 ≤ 25). Peer re-open this wave (`w1/ScoutBashSource.md:8-16`)
  fetched the pin: 415,804 B, sha256 `f3d37d57…32d5` — identical to the
  standing S097 pin, so the quoted bytes are digest-bound.
  - **Nuance (adverse, reported verbatim):** the committed cite says the quote
    sits at "lines 489–493" and the URL anchors `#L489-L493`; the peer re-open
    (`ScoutBashSource.md:44`) shows the quoted sentence physically occupies
    **lines 494–495**, while 489–493 is the `@node` header/`@cindex` block.
    Section and node anchor are exact; the numeric window is off by the header
    lines — same class as the r36 S103 erratum (19→18). Not repaired here.
- **Row fields**: tier `A`, status `mined`, opened 2026-10-24, recheck `365d`,
  `used-by` = `tools/tally-audit-v3.py, corpus/lessons/round-37.md` — both
  resolve (tool docstring cites S104 at `tools/tally-audit-v3.py:158`). Rows
  100 → 101; `Next unused id: S105` (`SOURCES.md:425-426`).
- **Census**: start `census/start.stdout` + `start.exit` = 0; end
  `census/end.stdout` + `end.exit` = 0. End carries `W04 S104 duplicate url
  cgit.git.savannah.gnu.org/... across scopes` — S104 shares the pinned
  bashref.texi URL base with S097 (different anchor); warning only, `ok` verdict.
- **S103 old→new**: `used-by` narrowed to `corpus/lessons/round-36.md`; quote
  recount `wc -w` → 18 ≠ 19 (`corpus/lessons/round-36.md:38` still reads
  "(19 words)"; the r36 lesson's append-only errata record the correction).
- Rejected this round: none; no `corpus/knowledge/` admission claimed.

## Mistakes — four tuples (all fields resolve)

1. **reference-drift** — evidence: r36 control receipts cite scratch commit
   `91373d55557f…`; `git cat-file -e 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f`
   → exit 1 (re-verified). Routed item: `round-36-verifier-spotcheck.md:88-90`
   ("Routed defects" item 1 — the cite "Routed defect 1" resolves to this
   numbered list). Red-before: `calibration/before-final-control.stdout` exit 1,
   `unresolved_control_inputs=1` at `d9c496b`. captured-by: none at write time;
   the non-author r36 closure routed it. fix: committed
   `control/empty-panel/manifest.json` (source tree `4f3d8af5…`, 9→0 specimens),
   `control/replay-at-final-control.stdout` (`mode=control`, v1
   `C1_R35_CONTROL_PASS=true` / v2 `C1_R36V2_CONTROL_PASS=false`, exit 0),
   SCORECARD append (`SCORECARD.md:1780`); `after-control-final.stdout` exit 0
   `unresolved_control_inputs=0` at `32826f3`. QUALITY 73 (`QUALITY.md:860-869`).
2. **scope** — evidence: r35 `AttackQuotedHash.md:264-273` (CRITICAL-2/BOUND);
   red-before `code-view/before.stdout` exit 1, `ansi_trailing_comment=0/1`.
   captured-by: no selftest coverage of ANSI-C; outside attack reported, r36
   routed. fix: `ansi-c` quote state `tools/tally-audit-v3.py:172-194`, selftest
   fixtures `:889-898`, bounded docstring `:156-161`. After: `code-view/after.stdout`
   `2/2` `C2_R37_PASS=true` at `ae9b771` (exit 0); selftest 35/35
   (`tool-selftest-after.stdout` exit 0); frozen r36 predicate re-attested
   `C2_R37_REPIN_PASS=true` (`c2-repin-after.stdout` exit 0) at pinned tool
   `da8c1ef4…` (`counter-pin.json`; re-derived from `ae9b771` bytes this seat).
   QUALITY 74 (`QUALITY.md:871-879`).
3. **number-drift** — evidence: `corpus/lessons/round-36.md:38` "(19 words)" vs
   recount `wc -w` → 18 (re-run this seat). captured-by: `CORPUS.md` "A count
   carries its command" — resolves at **fleet root** `../CORPUS.md:34` (r19
   convention confirmed: `w1/MistakesDraft.md:36`); a lane-local `CORPUS.md`
   does not exist — one-line resolution note for reviewers. fix: append-only
   r36 errata + S103 `used-by` narrowing; falsifiable by the cited command.
4. **attribution** — evidence: `control/replay-at-final-fixed.stdout` prints
   `mode=deciding` (lines 9, 18) on control inputs; flagged by r36 w2
   `W2ReviewC2Predicate.md:154-160` (and w1 `CriticC2Scope.md:100-103`).
   captured-by: no explicit-mode criterion. fix: `replay-at-final-control.stdout`
   `mode=control`, v1 PASS / v2 FAIL (exit 0). QUALITY 73.
   - **Nuance (minor):** the entry says "the first r37 replay output" but cites
     `replay-at-final-fixed.stdout`, which is the *second* replay; the truly
     first (`replay-at-final.stdout`) also prints `mode=deciding` (and fails on
     a `pub_kill_slots` wrapper bug). The cited file's claim is true; "first" is
     imprecise.

## Parser non-goals (retained, verified)

Explicit in lesson Holds (`round-37.md:21-23`), tool docstring
(`tools/tally-audit-v3.py:160-161` "bounded support, not a full Bash lexer"),
`LOG.md:1979-1980`, and QUALITY 74: nested `$(…)` quoting, unquoted
backslash-newline continuations, and parameter-branch quoting remain outside
the implemented surface (`AttackQuotedHash.md:66-83, 254-288` — regions
confirmed). Failed-attempt receipts honestly retained: `calibration/before.stderr`
`NameError: manifest_bytes`, `control/replay-at-final.stdout`
`EMPTY_PANEL_REPLAY_PASS=false`. Depth score `recorded_cases=9 depth_score=9`
at both revs — capability recorded, no fabricated tenth case.

## Touched surfaces / scope

- Wrote: this report only — `.ufo/waves/round-37/w1/ScribeRoundLesson.md`.
- Read-only: contract, all `.ufo/evidence/round-37/` receipts, lesson, SOURCES,
  QUALITY, LOG, SCORECARD, r35/r36 wave reports, fleet `CORPUS.md`.
- No lane file edited; no git index mutation; no installs.
- Out of scope: repairing the S104 line-window nuance or Mistake-4 "first"
  wording (adverse evidence reported, not repaired, per lane bounds).

## Artifacts

Report: `.ufo/waves/round-37/w1/ScribeRoundLesson.md`.
