# T50CritC1Contract — C1 design falsification findings

Seat: T50CritC1Contract (critic). Item: falsify C1's design; findings disclosed, never re-scored.

Method: all counter runs are probes, not verdicts — the frozen counter bytes at freeze
`cdbf24c07f9be3a991997c25b1f1d4bb375014ae` (`.ufo/evidence/round-50/c1/measure.py`, self-sha
`ceee320c9ad8`, identical to the committed control receipts) were run against scratch clones
(`git clone --shared` from the lane + `git checkout cdbf24c0`; toplevel asserted per fixture
before any mutation). All fabricated content lives only in scratch clones. Receipts:
`.ufo/waves/round-50/w1/{a-fab,b-underclaim,c0-base}.stdout`, `driver.out`.

## F1 (HIGH) — pure fabrication passes the whole counter, including the after-base floor

Reproduction (`a-fab.stdout`): on a scratch clone at freeze, one commit created
`corpus/dispositions.md` (49 lines, each embedding one frozen key, no ACK words) and a ledger
`corpus/routed-defects.json` with all 49 rows `fixed`, all citing that same commit, each evidence
line `i-i`. Frozen counter result:

`C1_R50: self=ceee320c9ad8 rev=08149c80… defects=49 rows=49 fixed=49 … fixed_this_round=49 … total=0 C1_R50_PASS=true` (exit 0).

No item was disposed by anyone; the text is nonsense ("<key> is fully delivered by the round-50
disposition service."). The excerpt's freshness is automatic: the path did not exist at `routed_at`
(`git -C $D show <routed_at>:corpus/dispositions.md` → rc 128), so *any* post-routing line with a
key is "new since routing". This is the exact gap CTL_FAB only half-opened: the fabrication control
stops at `fixed=40 … fixed_this_round=2 … this_round_short=3 total=5` (`control/c1-CTL_FAB.stdout:3`)
because it refuses to author new text; authoring one post-freeze commit is free. Therefore floor
`fixed_after_base_min=5` (and `fixed_min=20`) is bypassable by fabrication, and `C1_R50_PASS=true`
certifies textual novelty, not that any routed defect is disposed. Contract `cannot_see` (contract.json:35)
named semantic support, but the demonstrated hole is wider: the *after-base* term — the one floor the
design relies on — is equally syntactic.

## F2 (HIGH) — status is a free label; underclaim (fixed item marked open/declined) passes

Reproduction (`b-underclaim.stdout`): same keyed fix-like text present in the tree for all 49 items;
ledger declares 20 `fixed` / 17 `open` / 12 `declined` (+ `**Planned (round 51):**` paragraph naming
the 17). Frozen counter result:

`C1_R50: … fixed=20 open=17 declined=12 fixed_this_round=20 … total=0 C1_R50_PASS=true` (exit 0).

The same tree passes as all-fixed (F1) and as mixed open/declined (F2): the counter never asks whether
an open/declined item is actually fixed (`open` only needs the id in the newest Planned paragraph,
measure.py:95-111; `declined` only needs a ≥40-char reason). The contract admits "underclaim" in
`cannot_see`, but the consequence is that opposite dispositions of the same tree are indistinguishable.

## F3 (MEDIUM) — key design: shared keys, ACK-colliding key, path-suffix matches

- Shared keys (computed from defects.json; see `driver.out`): `[~]`/`SHONEN` shared by **5** items
  (R42.4, R46.5, R47.7, R48.6, R49.6); `S153` (R41.6/R42.3); `S026`/`S093`/`S108`
  (R45.4/R46.1); `brace_depth_at` (R47.5/R48.4/R49.5); `S205` (R48.4/R49.5); `located-name`
  (R47.5/R48.4); `six-leg regression ledger` (R47.1/R48.4); `selftest receipt` (R45.2/R47.2).
  One new sentence containing e.g. "SHONEN" can legally serve five rows (a single line cited by five
  rows is accepted).
- R49.5 has key `carried` (keys.json:50), which equals an ACK word (measure.py:54). A `fixed` row
  cannot cite `carried` in an excerpt (blocked by the ACK check); it is only usable via the
  path-suffix rule or another key. So one of the item's own keys is poisoned for the intended status.
- `has_key` accepts a path ending in a key (measure.py:114-117): a file literally named e.g.
  `corpus/S205` counts as keyed evidence with no key text in the excerpt.

## F4 (MEDIUM) — floors are not calibrated to anything load-bearing

CTL_FAB's own run shows 40 of 49 items already have a keyed post-routing non-ACK mention in history
(`control/c1-CTL_FAB.stdout:3`), so `fixed_min=20` sits below historical saturation and never bites
against honest-but-sloppy rows. `declined_max=12` only bites against the all-declined control
(CTL_DECLINE `declined_over=37`). The only term with teeth — after-base 5 — is the one shown
forgeable (F1). No derivation for 20/12/5 appears in contract.json:30-34; they add no semantic bar.

## F5 (INFO) — extraction is complete on the defined surface; unnumbered asks are the only fringe

Re-running `extract-defects.py` at freeze (frozen bytes) reproduces exactly the frozen set: 49 ids,
same order, same `routed_at` (driver.out: `ids equal: True`, `routed_at equal: True`; per-round counts
5/7/4/3/2/4/5/7/6/6). Bulleted lists (rounds 43/44) and numbered lists both parse. Two adjacent
*unnumbered* prose asks are not items and are excluded consistently with the contract's "list under
the routed heading" surface: round-40's trailing SHONEN/promotion paragraph
(`corpus/lessons/round-40-verifier-spotcheck.md:317-320`) and round-45's trailing SHONEN paragraph
(`round-45-verifier-spotcheck.md:90`). Note: base `e3729de8` does not contain the round-50 instrument
(`git show e3729de8:.ufo/evidence/round-50/c1/defects.json` → fatal: exists on disk, not in rev); the
counter only exists from the freeze commit onward.

## Commands (all from scratch; frozen counter bytes)

- `python3 $S/measure-freeze.py --lane $D --rev <HEAD> --explain` (receipts above).
- `python3 $S/extract-freeze.py --lane <LANE> --rev cdbf24c0` → 49/49 ids, routed_at equal.
- `git -C $D show <routed_at>:corpus/dispositions.md` → rc 128 (path absent at routing).

## Summary
- F1: one post-freeze fabricated commit + ledger makes `C1_R50_PASS=true` (fixed=49, after-base=49,
  total=0) with zero genuine dispositions — the after-base floor is forgeable, not load-bearing.
- F2: the same keyed text passes as 20 fixed/17 open/12 declined; open/declined never check whether
  the item is actually fixed, so status is a free label (underclaim passes by construction).
- F3: 11 keys are shared across items (SHONEN/[~] on five), R49.5's `carried` key collides with an
  ACK word, and path-suffix key matches need no key text.
- F4: fixed≥20 is below the 40/49 historical saturation CTL_FAB found; declined≤12 is near-void; the
  5-after-base floor is the only teeth and is the one bypassed.
- F5: extraction is exactly the 49 list items (bullets and numbers); only unnumbered SHONEN/promotion
  prose sits outside the set by design.
- The counter is a well-formed syntactic form-check; it cannot distinguish disposition truth from
  fabrication, so C1's PASS token should be read as "the ledger meets the stated textual contract",
  not "the routed defects were disposed".
