# ScoutSHONEN — SHONEN checklist recon at the refresh commit

Round 36, wave 1. Scope: run the mark census (SCORECARD command C) against
`SHONEN.md` at the round-36 refresh commit, confirm the four boxes still read
`[~]` with resolvable pointers, and confirm no box was silently flipped this
round. Leaf scout seat — read-only, no dispatch.

## Revisions

- Lane tip (HEAD): `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` ("round-36: receipts …")
- Refresh commit under recon: `b455001` ("round-36: cold-read refresh — four L1 author source re-anchor entries …")
- Round-36 content commit: `e423c41`
- Before baseline (contract C1 `before.rev`): `796e08b888849308d0c4d5e932e56833600a139f`

## Commands run (from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`)

1. `git show "<REV>:SHONEN.md" | python3 -c 'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); print("boxes="+str(len(m))+" checked="+str(m.count("x"))+" asserted="+str(m.count("~"))+" untouched="+str(m.count(" "))+" asserted_mark_upper_bound="+str(min(8,2*m.count("~"))))'` — SCORECARD command C verbatim (`SCORECARD.md:74-75`), run at `b455001`, `d9c496b`, `e423c41`, `796e08b`.
2. `git diff 796e08b..d9c496b -- SHONEN.md | wc -l` and `git show <rev>:SHONEN.md | sha256sum` at `796e08b` and `b455001`.
3. `git show b455001:SHONEN.md | grep -nE '^- \[' -A1` — box lines and pointer lines.
4. `git cat-file -e b455001:<pointer-target>` for `reports/round-1-calibration.md` and `.ufo/evidence/round-21/coldread/ledger.json`.
5. `git show <rev>:.ufo/evidence/round-21/coldread/ledger.json | python3` — entry counts at `796e08b` and `b455001`; inspection of appended entries.

## Observed

- Command C output, **identical at all four revisions** (`796e08b`, `e423c41`, `b455001`, `d9c496b`):
  `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8`.
- `SHONEN.md` is **byte-identical** across the entire round-36 range:
  `git diff 796e08b..d9c496b -- SHONEN.md` = 0 lines; sha256 at `796e08b` and
  `b455001` both `55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09`.
  The last commit touching `SHONEN.md` is `370f2df` (round 21). **No box was
  flipped this round — silently or otherwise; the file was never touched.**
- Box states at `b455001` (`SHONEN.md:5-12`): all four `[~]` —
  box 1 (SKILL.md decision tables) → `reports/round-1-calibration.md#box-1`;
  box 2 (end-to-end task in LOG.md) → `…#box-2`;
  box 3 (executable without oral context) → `.ufo/evidence/round-21/coldread/ledger.json`;
  box 4 (no cross-domain bleed) → `…#box-4`.
- Pointers resolve at `b455001`: `reports/round-1-calibration.md` exists and
  contains anchors `## box-1` (:71), `## box-2` (:105), `## box-4` (:167);
  `ledger.json` exists. Box 3 has no `## box-3` section in the report by design
  — its pointer targets the cold-read ledger, not the report.
- Box-3 pointer target enriched by this round: cold-read ledger `entries`
  count `796e08b`=493 → `b455001`=497 (+4). The four appended entries are
  SKILL-heading re-anchors — "## Mutation-sweep recipe — numbered steps;
  bounded cold-read evidence" (start 131), "## Restore discipline —
  before/after identity, not continuous non-write proof" (start 375), "### The
  map — where a reader enters, artifact by artifact" (start 1380), "### Where
  to enter — four readers" (start 1436) — matching the refresh commit message
  and the contract's C1 "four round-35-drifted headings" scope.

## Inference

- The mark census (`asserted=4`, `checked=0`) is the C1-visible state: all four
  boxes carry the restrained `[~]` mark, so the mark-census upper bound stays
  at its lane cap of 8. Whether the *credit* rises 6 → 8 depends on the
  cold-read monitor (`measure.py`) scoring, not on SHONEN.md — this seat only
  confirms the checklist surface the claim rests on.
- No drift vector observed in `SHONEN.md` itself; the round-36 delta relevant
  to C1 lives entirely in `ledger.json` (+4 entries), consistent with the
  contract kill rule ("the refresh ledger entries and trace receipts are the
  only delta").

## Remaining unknowns

- Whether the four appended ledger entries *score* under
  `.ufo/evidence/round-21/coldread/measure.py` (that's the C1 measurement the
  wave's verifier runs, not this seat's recon).
- `reports/round-1-calibration.md` contains no `## box-3` anchor, but box 3's
  pointer doesn't target that file — no unresolved pointer, noted only for
  completeness.

## Verdict

**PASS (recon clean):** at refresh commit `b455001`, command C prints
`boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8`; all
four `[~]` boxes carry pointers that resolve; `SHONEN.md` is byte-identical
across `796e08b..d9c496b` — no box was silently flipped this round.
