# T48A2RevShonen — SHONEN.md boxes and pointers at content revision `c7586b9a10effc63b4bd327f976edc094c1bdc17`

Seat: T48A2RevShonen (a2w1 reviewer, leaf — no subagents). Read-only on the lane except this
report. Not an author of what is attacked. No tools installed (none needed). Scratch
`/fast/scratch/hyaku/tameshi-r48/T48A2RevShonen` deleted before submission.

## What was reviewed

`SHONEN.md` at `c7586b9a` (13 lines, 4 boxes, all `[~]`, one indented evidence line each —
shape per `PROTOCOL.md:419-431`). Working tree == HEAD `17cc5ce` == `c7586b9a` for every
file cited below (`git diff --stat c7586b9a HEAD -- SHONEN.md PROVINCE.md SKILL.md LOG.md
reports/round-1-calibration.md .ufo/evidence/round-21/` is empty).

Pointer resolution (all four resolve; no finding):

- Box 1 → `reports/round-1-calibration.md#box-1` → `## box-1` at `:71` (unique heading census;
  likewise `## box-2` `:105`, `## box-4` `:176`).
- Box 3 → `.ufo/evidence/round-21/coldread/ledger.json` — exists (3.4 MB, valid JSON, schema
  `tameshi-coldread-ledger-v2`, 497 entries; `entries[].skill_sha256` contains the current
  `SKILL.md` sha `2381873162fc…7d35a` and the blob contains the current `SHONEN.md` sha
  `55a4fceb62b0…32e09`, so the input-keyed credit keys the current inputs).

Round-48 blast radius on box-bearing files (`git diff --name-status 473336d9 c7586b9a -- …`):
**only `LOG.md` modified** — one append-only hunk at `:2343` (+23/−0). `SHONEN.md`,
`PROVINCE.md`, `SKILL.md`, `reports/round-1-calibration.md` and `.ufo/evidence/round-21/` are
byte-identical base→content. Box-2's cited trail `LOG.md:277-298` (round-3 task + historical
`[x]` verifier text, superseded in interpretation only, per round-1 report §supersession) is
intact. Box-4's `PROVINCE.md` cites a single SOURCES row (`S030`, not re-anchored) and its
"nine recorded mutation legs" still matches the runner ledger (probe `ledger_legs` = 9,
`recorded_cases=9`); the `:26` template-path correction resolves
(`/home/vgpnk/Projects/kimi-shokunin/templates/mint/PROVINCE.md` exists with the template
shape). Box-1's SKILL sections all present (`:58` decision table, `:94` mutation bar, `:314`
kill-rate bands, `:466` no-permissiveness recipe, `:497` fail-closed taxonomy). The `K1`
rubric literal `SHONEN.md:5-34` (SCORECARD.md:67) is a dated baseline literal covered by the
round-46 supersession-scope erratum; round-31's `SHONEN.md:5-12` still resolves.

Box-level state vs observed repo: no mismatch. Probe `shonen` block = `boxes=4 checked=0
asserted=4 marks=[~,~,~,~] box3_ledger_link=true box3_marked=true box3_points=false` —
matches the four `[~]` marks and the documented box-3 disposition (round-1 report `[ ]` →
round-37 erratum `[~]`, "input-keyed monitor only", never `[x]`).

## Finding 1 (Medium) — round-48 calibration standing row restates a stale monitor value: "60 of 64 sections credited" is false at both revisions the round declares it measured

- Where: `SCORECARD.md:2355` (round-48 "Current axes" calibration row): "…`box3_full_page=false`,
  **60 of 64 sections credited**…". The identical prose is carried from the round-47 row
  (`SCORECARD.md:2291`), i.e. copied forward, not re-observed. Same stale expectation in the
  frozen contract: `.ufo/evidence/round-48/contract.json` `no_harm_monitors` says
  "cold-read sections 60".
- Observed (probes, never verdicts): strict cold-read monitor
  `python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev REV`, run in a
  shared scratch clone of the lane, exit 0 each:
  - `473336d9` (base): `sections_covered: 60/64`, 4 uncovered, score 6, `box3_full_page=false`.
  - `15b1521e` (the emit revision the round's own rows are restated from): `sections_covered:
    57/64`, score 6, `box3_full_page=false`.
  - `c7586b9a` (content revision): `sections_covered: 57/64`, score 6, `box3_full_page=false`.
  Uncovered at 57/64 = the base four (Mutation-sweep recipe, Restore discipline, The map,
  Promotion-evidence calibration) **plus** `## Repeated controls and gate registry — round 12`,
  `## Pin disposition and provenance correction — round 13`, `## Effective expectation
  reconciliation — round 14`.
- Cause is inside round 48 itself: the three extra sections' drift reasons cite
  `corpus/SOURCES.md` and `corpus/knowledge/repeated-control-precondition.md` /
  `incremental-pin-disposition.md` — exactly the C2 records commit `5054532` ("rows S265-S268,
  snapshots and receipts, re-pointed entries"), which precedes the emit rev. So C2's own
  re-anchoring deepened the input-keyed credit decay 60→57 before the round restated its rows,
  and the restatement carried the base-era "60 of 64" anyway. No committed r47/r48 receipt
  prints `sections_covered` (grep over `.ufo/evidence/round-47`, `round-48` → no match), so
  nothing in the round's own evidence supports "60" at its measured revisions.
- Severity rationale: the numeric score 6 is correct at all three revisions (three credited
  boxes × 2; `box3_points=false` either way), so this is not a score error and not by itself a
  C1 kill — C1's frozen grammar (amendment 3) attests the score cell + tool sha + deps + runs
  class, not this prose. But the round's C1 exists precisely because "a one-shot/stale
  observation was restated as a standing value" (round-47 routed defect 1; LOG.md:2347); the
  round-48 restatement repeats that defect class for the monitor's section count while its own
  counter observed 57. It bears directly on box 3: the input-keyed credit behind box-3's `[~]`
  is 57/64 at the content revision, not the 60/64 the standing row states. The deciding run's
  no-harm check will print 57, not the contract's stated 60 — anticipated here so it is not
  misread as monitor breakage.

## Residual risk and verification gaps

- Probes were run at three revisions in one shared clone; a probe is never a verdict. Whether
  C1's deciding observation of the monitor statement passes depends on which stdout line the
  frozen statement pins (the restraint-score line is 6 at every revision; a
  `sections_covered` line would not be), which is the C1 reviewers' surface, not mine.
- Box-1's citation-level audit (every SKILL.md citation resolving line-by-line) was not
  redone; SKILL.md is unchanged since round 31 (`2da841b`) and the round-1 audit stands as the
  box's pointer content.
- The exact 60→57 commit attribution (5054532 vs the 15b1521 salvage) is inferred from the
  drift reasons naming files whose last-change commits are `5054532`/`c7586b9` (SOURCES.md,
  the three entries) and `c7586b9` (LOG/SCORECARD/QUALITY); I did not bisect the two.
- LOG.md's attempt-2 correction block calls `six-leg regression ledger` "disclosed as
  known-nondeterministic" while the SCORECARD row's class cell says `runs 3 stable`
  (amendment-3 grammar derives the class from the one-member value set). Not a SHONEN-box
  matter; left to the C1 calibration reviewers as an adjacent wording tension.
