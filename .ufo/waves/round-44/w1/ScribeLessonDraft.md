# ScribeLessonDraft — round-44 lesson draft (Gate + Mistakes)

Seat: L1Tameshi44.ScribeLessonDraft (scribe, leaf member). Read-only on the
lane; no file in the lane was edited. This report carries the drafted `## Gate`
and `## Mistakes` sections for `corpus/lessons/round-44.md` (the lesson itself
is NOT written here), plus the grounding each claim is built on.

## Behavior

- Read `round-43.md` for the lesson shape (Gate admit/re-open blocks, Mistakes
  table, append-only and instrument-limit sections).
- Read `.ufo/evidence/round-44/contract.json` (C1/C2 claims, targets, controls)
  and `.ufo/evidence/round-44/calibration/measure.py` (m7 masks, ASSIGN_ID at
  `:89` applied at `:109`, T6 cases at `:418-431`).
- Verified the committed snapshot bytes:
  `sha256sum .ufo/evidence/round-44/sources/stryker-equivalent-mutants.html` →
  `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce`;
  `wc -c` → 38687; `wc -l` → 23.
- Counted quote words on lines 15–16 with `split()` on the tag-stripped lines:
  line 15 quote = 20 words, line 16 quote = 12 words (both ≤25; the full lines
  are 28 and 30 words, so the located quotes must be the fragments below).
- Read `.ufo/evidence/round-44/before/c2-old-at-base.stdout` (old-counter receipt,
  the m7 evidence pointer) and `.ufo/evidence/round-44/before/c2-new-at-base.stdout`.
- `git status --porcelain`: the only modified tracked file is
  `.ufo/waves/round-43/w1/RevC2Classes.md`; `git diff --stat` → 61 insertions / 46
  deletions (A13 pin/line-reference updates). Confirms the round-43 verifier
  spot-check defect (`.ufo/...` in `corpus/lessons/round-43-verifier-spotcheck.md:12`).
- Read `.ufo/waves/round-44/w1/MutMaskRemove.md` (red-before receipt for the
  ASSIGN_ID mask: selftest 16 cases, failed=2, `['r unknown S256']`, exit 1).
- Registry tail: `corpus/SOURCES.md:456` still reads `Next unused id: S160.`;
  no S160 row exists yet (the draft describes the intended landing row).

## Gate (draft for round-44.md)

Theme: **the anchor is not the document** — the live Stryker equivalent-mutants
snapshot is admitted as a census-valid row S160 that supersedes S089's stale
html-digest anchor only; S089's document, status, teaches and used-by are
unchanged. No assimilation from the shokuknow package this round
(`Assimilation: none`).

### Admit — S160 (new row): Stryker Mutator, *Equivalent mutants*

- URL https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/,
  fetched 2026-10-25 with `curl -fsSL`, 38687 B, 23 lines, `<title>` `Equivalent
  mutants | Stryker Mutator`, sha256
  `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce`; byte-identical
  to the round-43 re-open fetch of the same page. Snapshot:
  `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html`.
- Located quotes (both ≤25 words, `split()` counts on the committed snapshot lines):
  - line 15 (20 words): "even if we change >= to <= and even < or > we will get
    the same output each time!"
  - line 16 (12 words): "There is no definitive way for Stryker to find and
    ignore them."
- Teaches: **supersedes S089 — anchor only**.
- Scope: this row supersedes S089's html-digest anchor cell; it does not change
  S089's status, teaches, or used-by. Status mined; cited by a knowledge entry
  (intended: the entry/entries that use S089 — `mutation-case-kumitate-cite-check.md`
  and/or `r43-survivor-resolution-rule.md` — to be named by the L1 at landing).
- Census/quality notes for the L1: the row must match the census-valid shape
  (`grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` → 1 at landing; the registry
  tail's `Next unused id` line moves past S160); the standing row's count cell
  and the backticked counting command cell must be restated as in round 43.

### Re-open — S089 (held): Stryker Mutator, *Equivalent mutants*

- Digest drift: S089's 2026-10-22 anchor (`html sha256 bc572676…e04d`,
  `corpus/SOURCES.md:98`) is stale — the page drifted (round-43 lesson recorded
  `last-modified: Sat, 24 Oct 2026 15:08:38 GMT`; `corpus/lessons/round-43.md:45-49`).
  The text survives at the same offsets and byte count (38687 B, lines 15–17
  identical), so the cited content stands.
- Old → new log: S089 anchor cell `bc572676…e04d` → superseded by S160
  (anchor-only), logged in this lesson. S089's status, teaches and used-by are
  unchanged.

## Mistakes (draft for round-44.md; CORPUS.md vocabulary)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| scope/extractor-narrower | m7 missed the underscore form `safe_floor=S256`: the round-43 counter at base prints `C2_R43: … m7=1 … total=1 … first=m7:SCORECARD.md#round-43_unknown_S256 C2_R43_PASS=false` (`.ufo/evidence/round-44/before/c2-old-at-base.stdout`); the SCORECARD C3 deciding-run field `safe_floor=S256` (`SCORECARD.md:2091`) read as an unknown citation because the value masks matched `safe floor` / `next unused id` phrases only, never the key=`S###` assignment form | none — no round-43 criterion required the mask to cover assignment forms | ASSIGN_ID mask (`measure.py:89`, applied in `m7_citations` at `:109`) + T6 selftest cases (`measure.py:418-431`: `T6_safe_floor_value_not_citation`, `T6_assign_with_spaces_masked`, `T6_genuine_unknown_still_flagged`, `T6_unmined_flagged`). Shown able to fail by the mask-removed control: with the `ASSIGN_ID.sub(...)` line removed, the selftest fails `T6_safe_floor_value_not_citation` and `T6_assign_with_spaces_masked` with `['r unknown S256']` (`.ufo/waves/round-44/w1/MutMaskRemove.md:16-21`; the contract-referenced receipt `.ufo/evidence/round-44/control/mask-removed.selftest.stdout` does not exist yet — the wave report carries the verbatim output it would contain) |
| landing | the round-43 wave-1 note `.ufo/waves/round-43/w1/RevC2Classes.md` was left modified in the worktree at closure — its diff updates A13 pin/line references (61 insertions, 46 deletions, `git diff --stat`); recorded by the round-43 verifier spot-check (`corpus/lessons/round-43-verifier-spotcheck.md:12`) and still modified at this draft (`git status --porcelain`) | none — no criterion swept the worktree at closure | committed under round 44 (or reverted), disposition named in this lesson |

## Gates (verified facts and their sources)

- Snapshot digest/size match the contract and the round-43 lesson:
  `79f6501a…`, 38687 B — `sha256sum`/`wc -c` on
  `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html`.
- Quotes located at snapshot lines 15 and 16; word counts 20 and 12 (≤25) —
  `python3` `split()` counts on the tag-stripped lines.
- Old-counter base receipt exists and carries the declared m7 alarm:
  `.ufo/evidence/round-44/before/c2-old-at-base.stdout`.

## Touched surfaces

- None: no lane file edited, no git/jj command run beyond read-only
  `git status`/`git diff`. Report written at `.ufo/waves/round-44/w1/ScribeLessonDraft.md`.

## Out-of-scope items (noted, not drafted)

- The new counter's own base run shows `m12=1 first=m12:newest_block_is_round_43,_the_contract_round_is_44`
  (`.ufo/evidence/round-44/before/c2-new-at-base.stdout`) — a distinct class
  (scorecard block round vs contract round) not in this item's scope.
- C1 measure, census exits, and the knowledge-entry citation for S160 are the
  L1's landing-time checks (the S160 row and its used-by cell do not exist yet).

## Tooling

No tool installed or upgraded; `python3` and read-only `git` used.
