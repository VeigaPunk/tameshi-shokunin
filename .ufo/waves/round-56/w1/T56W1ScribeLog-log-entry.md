## 2026-10-28 — round 56, attempt 1 (this round)

L1 TameshiR56, hyaku run 11. The round repairs what the round-55 non-author
closure rejected (`corpus/lessons/round-55-verifier-spotcheck.md`): R55.3 (the
cold-read floor the round's own edits cost, unrepaired at HEAD) and R55.5 (the
deciding gate cannot compare the revision it certifies); R55.1, R55.2, R55.4,
R55.6 and R55.7 are disposed below. Base `981c5e8b`
(`.ufo/evidence/round-56/contract.json`); contract, both counters, the
receipt-revision gate, the controls and no-harm harnesses and the deciding
script frozen at `c3e2ca9f` (`.ufo/evidence/round-56/freeze.json`; its
`amendments` list is empty as this entry is drafted, `<L1 fills>` the final
count). Claims: **C1 calibration** — the lowest non-retired axis, where the
round-21 monitor reads `covered=46 score=6 box3=False`
(`.ufo/evidence/round-56/before/c1.stdout`, arm2): the 18 headings the round-55
edits cost (`.ufo/evidence/round-56/c1/lost-headings-at-base.json`) are re-read
at one content commit C0 and bound under one `rekey-r56-<c0>` directory; at base
`C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18
monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` (same receipt),
target `total=0` with the precheck at `lost=0`, the monitor at `64/64 score=8
box3=true`, and the standing calibration row stating the score the monitor reads
at the commit the row names — at base the row asserts 8 at `d33053f7` where the
monitor reads 6 (`SCORECARD.md:2579`; arm6 of the same receipt). **C2
operability** — every receipt the lane certifies is bound to the revision it was
measured against by `tools/receipt-revision-gate.py`, and the gate refuses the
real receipts the lane accepted: round-54's `CTL_POS_c1` names `rev=077d431e6996`
while the round measured `c21081008adb`
(`.ufo/evidence/round-54/control/controls-b.stdout`,
`.ufo/evidence/round-54/after/c1.stdout`), its `CTL_EXIT0` names
`rev=7df0e0426c98`, which is not an object in this repo
(`.ufo/waves/round-56/w1/T56W1ScribeLog-receipts/round-54-red-before.txt`), and
the round-54 gate accepted the set
(`.ufo/evidence/round-54/after/deciding-run.exit`); round-55's committed C2
verdict names no revision and stops mid-run
(`.ufo/evidence/round-55/after/c2.stdout`). At the freeze `C2_R56:
rev=c3e2ca9f0207 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT
red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing
docs=0/4 total=2 C2_R56_PASS=false` (`.ufo/evidence/round-56/before/c2.stdout`);
before the gate landed the same counter read `C2_R56: error=gate-missing total=1
C2_R56_PASS=false` (`.ufo/evidence/round-56/before/c2-at-base.stdout`).

Content (C0 `<L1 fills>`): the gate's cell in `tools/registry.json`;
`corpus/knowledge/receipt-revision-binding.md` (provenance trio plus a `mined`
S-row); a `corpus/QUALITY.md` criterion whose falsifier is the gate's own
refusal code on the real round-54 receipt (`<L1 fills>` the number; 106 is the
last at base, `corpus/QUALITY.md:1592`); one `corpus/SOURCES.md` row for the
source opened this round (`<L1 fills>` the row; 140 rows at base,
`.ufo/waves/round-56/w1/T56W1ScribeLog-receipts/lane-surface.txt`); the
`SKILL.md` `## Standing rules` rule — that section only, and it is the one
heading whose text changes, re-read at C0 with the other 17; the `SCORECARD.md`
round-56 block with the restated standing calibration row; and
`corpus/lessons/round-56.md` carrying `## Gate`, `## Mistakes` and the
dispositions below. Wave 1 (round-56-w1) carries the content and the frozen
instruments' falsifiers, wave 2 re-reads the 18 headings at C0, wave 3 binds
(`<L1 fills>` the settled seat counts). Waves, controls and deciding receipts
follow under this entry.

Dispositions of R55.1–R55.7 (`corpus/lessons/round-55-verifier-spotcheck.md`):

- **R55.1** (no C2 verdict at the measured revision) — C2's target is the
  counter's verdict at the certified revision plus the round's own control
  receipts gated there, and the deciding run refuses unless both hold
  (`deciding-run.sh` gates 0b/0c). Receipt: `<L1 fills>`.
- **R55.2** (a quoted total its own receipt contradicts) — every value in this
  round's records names the receipt that carries it, and the round quotes the
  counter's own line rather than a seat's paraphrase; the rule is stated in
  `corpus/QUALITY.md` (`<L1 fills>` the criterion number). Counter-instances
  adjudicated in `corpus/lessons/round-56.md`.
- **R55.3** (the calibration instrument regressed and the row still said 8) —
  this round's C1. Receipt: `<L1 fills>` under `.ufo/evidence/round-56/after/`.
- **R55.4** (a stale control sentence) — the round's control set is the frozen
  `.ufo/evidence/round-56/controls.sh`, scored at the revision it certifies,
  and the report quotes committed lines only. Receipt: `<L1 fills>`.
- **R55.5** (the deciding gate cannot compare the revision it certifies) —
  `tools/receipt-revision-gate.py` binds each receipt's `rev=` to the certified
  revision, and the deciding run applies it to the round's own receipts and to
  the verdicts the run just produced; red-before on the real receipts is
  `.ufo/evidence/round-56/before/c2.stdout` (three refusal codes).
- **R55.6** (uncommitted round work at closure) — the inherited round-55
  evidence was swept into the base (`981c5e8b`, contract `base_note`) and the
  round commits its evidence before the tip; at close `git status --porcelain`
  reads `<L1 fills>`.
- **R55.7** (closure-seat contamination) — post-tip closure rewrites were
  reverted to branch bytes at `6efd2a1` before the base, and closure seats work
  in scratch clones this round; any residue found at close: `<L1 fills>`.

  (update) `<L1 fills>` — wave 2/3 and the deciding receipts.
  (close) `<L1 fills>` — deciding verdicts at the measured revision, controls,
  no-harm, census, report commit.
