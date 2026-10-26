# T49W2Reread09 — C1 semantic re-read, `## Repeated controls and gate registry — round 12` (ordinals 0-10 named)

Candidate `f181a961ae44061af486f600e5ea257d2baf78f8`, base `8ca67421111fa354b47b803358391d0b07fc6db9`. All commands run from the lane root; every target opened with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961:<path>` (worktree copies extracted to scratch, never edited).

## Scope note

The item names ordinals 0-10; the section carries exactly 5 pointers (ordinals 0-4) at base and at the candidate — command: `python3 -c "import json;rows=json.load(open('.ufo/evidence/round-49/c1/reads.json'))['rows'];print([r['ordinal'] for r in rows if r['heading'].startswith('## Repeated controls')])"` → `[0, 1, 2, 3, 4]`. Base count 5 = contract floor `floors.r12: 5` (contract.json:29); the candidate keeps 5 (S004, S026, `corpus/knowledge/repeated-control-precondition.md` at SKILL.md:1481; `.ufo/evidence/round-12/verification-final.json` at :1482; `tools/repeat-control.py` at :1492). Ordinals 5-10 do not exist. `reads.json` at the candidate is byte-identical to the worktree copy (command: `git show f181a961:.ufo/evidence/round-49/c1/reads.json | sha256sum` vs worktree).

## Rows — verdicts

All five rows support their clause. None fails.

- **Ordinal 0 — `corpus/knowledge/repeated-control-precondition.md` — supports.** Excerpt verbatim at doc:26 (command: `git show f181a961:corpus/knowledge/repeated-control-precondition.md | grep -n "Stream agreement is stronger"` → `26:- **Stream agreement is stronger than pass/fail stability — and still weaker than determinism.** …`). Doc:26 is the section's own Bound ("not a determinism proof", SKILL.md:1487); doc:29 ("identical `(exit, stdout, stderr)` tuples, back to back, on one host, in one environment") grounds the corrected bound at :1487; doc:35 states the CLI (`--runs` at least 3, `DIR` must not exist) behind the recipe at SKILL.md:1491-1494. Doc unchanged base→candidate: `git diff 8ca67421 f181a961 -- corpus/knowledge/repeated-control-precondition.md` → empty.
- **Ordinal 1 — `.ufo/evidence/round-12/verification-final.json` — supports.** Excerpt at verification-final.json:73, inside check `real-pristine-three-controls` (`passed: True`), whose stdout carries `REPEAT_RUN 1/2/3 exit=0 stdout-bytes=1202 stderr-bytes=0`, `REPEAT_COMPARE identical=yes runs=3`, `REPEAT_CONTROL: controls_match` (command: `git show f181a961:.ufo/evidence/round-12/verification-final.json | grep -n "REPEAT_RUN"`). The quoted excerpt is runs 1-2 of the 3; run 3 and the raw-tuple compare verdict sit in the same located blob at :73. Supports SKILL.md:1482 ("runtime evidence") and the `controls_match` table row at :1487. File unchanged base→candidate.
- **Ordinal 2 — `tools/repeat-control.py` — supports.** Excerpt is the usage string at tool:13 (command: `git show f181a961:tools/repeat-control.py | sed -n '13p'`). Tool:262 `--runs must be >= 3`; tool:317 `--out already exists (refused, never overwritten)` = SKILL.md:1493-1494 "The output directory must not exist"; `--selftest`/`--snapshot` dispatch at tool:874-879 backs the registry commands at SKILL.md:1503. Tool unchanged base→candidate, sha256 `296fe566dc59…` = the tool-sha256 recorded inside the round-12 receipt itself (verification-final.json:73).
- **Ordinal 3 — `S004` — supports.** Exactly one S004 row, at SOURCES.md:15 at the candidate (command: `git show f181a961:corpus/SOURCES.md | grep -n "^| S004 "` → `15:`); the excerpt is verbatim in its lesson column. "tests must first pass reliably in a copied tree" is the precondition behind "choose a pristine command" (SKILL.md:1491) and the no-baseline/no-kill-rate row (SKILL.md:1489); the row's used-by names the doc. The candidate's +5 SOURCES.md lines (S265 at :140, staged-id notes at :490-493; `git diff --stat 8ca67421 f181a961 -- corpus/SOURCES.md` → `5 insertions`) do not shift line 15.
- **Ordinal 4 — `S026` — supports.** Exactly one S026 row, at SOURCES.md:37; excerpt verbatim. Flakiness prevalence (1.5% of runs; 84% of pass-to-fail transitions) is the reason the recipe forbids "retry until green" (SKILL.md:1495) — the S026 half of Source (SKILL.md:1481). Observation, not a defect: S265 (SOURCES.md:140) supersedes S026's anchor and quote only; S026 stays `mined` with used-by → the doc, so the pointer resolves to a row that supports. The reads row's note already records the supersession; keeping `S026` preserves the 5-pointer floor.

## Corrections in range (base → candidate)

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 8ca67421111fa354b47b803358391d0b07fc6db9 f181a961ae44061af486f600e5ea257d2baf78f8 -- SKILL.md` shows exactly four changed lines inside 1479-1515; all four are sound. No pointer text changed.

1. **SKILL.md:1483 — ok.** "six-leg runner" → "six-leg runner of round 12": disambiguation only, consistent with "the historical runner" at :1506. No meaning change.
2. **SKILL.md:1487 — ok.** Bound gains "on this host in this environment": grounded at doc:29 ("on one host, in one environment") and repeat-control.py:94 ("not a determinism proof and it cures no flakiness"). Tightens the bound; Decision unchanged.
3. **SKILL.md:1488 — ok, and it fixes a real base defect.** Base "Any available controls differ" misdescribed the tool: `classify()` at repeat-control.py:206-210 returns `command_unavailable` when any run did not execute, so `controls_mismatch` requires **all runs executed** plus a tuple difference (:211-219). The corrected Observation states exactly that. Decision label and Bound unchanged; the meaning change is toward the tool's actual contract (docstring :31-32 states the same precedence).
4. **SKILL.md:1489 — ok.** Added "(`baseline_nonzero` / `command_unavailable`, exit 2)" matches repeat-control.py:125-126 (`baseline_nonzero: 2`, `command_unavailable: 2`) and the precedence at :206-219 ("a stable nonzero baseline" → `baseline_nonzero`). New pointers are right.

## Side observations (outside this seat's correction scope, no action requested)

- The knowledge doc's own internal citations into the tool are drifted at the candidate bytes: doc:35 cites `tools/repeat-control.py:245-247` for the `--runs` floor (actual :262), doc:29 cites `:79-87` for the limitation text (actual :84-94), doc:52 cites `:337-435` for the snapshot validator. Command: `git show f181a961:corpus/knowledge/repeated-control-precondition.md | grep -n "245-247\|79-87\|337-435"`. This is the drift wave-1 reader T49Read14 already flagged ("not a stale SKILL line"); the contract's correction scope is the seven SKILL.md sections, so leaving the doc untouched is within plan. It does not weaken any of the five rows above.
- Cross-check vs contract's `cannot_see`: these five rows are not mechanical — each excerpt sits in the target at the located line and carries the semantic weight the section's sentences place on it.

## Tooling

No tools installed or upgraded this seat (pacman paused host-wide; nothing needed).

## Summary

- Re-read all 5 C1 rows (ordinals 0-4; ordinals 5-10 do not exist — section floor is 5 and the candidate keeps 5) of `## Repeated controls and gate registry — round 12` at `f181a961`.
- All 5 rows support their clause: excerpts verbatim at doc:26, verification-final.json:73, repeat-control.py:13, SOURCES.md:15 and :37; each carries the section's actual claim (bounds, runtime evidence, CLI contract, pristine/flakiness preconditions).
- All 4 L1 corrections in range (SKILL.md:1483, 1487, 1488, 1489) are correct; :1488 fixes a genuine base misdescription of the tool's mismatch precedence (repeat-control.py:206-219).
- No row fails; no correction changes meaning away from the pointed targets; no pointer text changed.
- Side note: the knowledge doc's internal line citations into the tool remain drifted (doc:29/:35/:52), already flagged in round 48/wave-1 and outside this round's correction scope.
- Deliverable: `.ufo/waves/round-49/w2/T49W2Reread09.json` (rows + corrections, evidence per entry).
