# The set-aware witness rule for sealed held-out copies (tameshi, round 34)

Author: tameshi-shokunin L1 (TameshiR34). Landed with the round-34 C1 measurement.

## The rule

A sealed held-out copy (a JSON of edits against the pinned runner) is only *valid* when its
witness demonstrates the labeled behavior, with the check branching on the copy's set:

- **kill + `kind=head`** — the head must differ on a *leg-assignment line*: the multiset of bare
  `st_x=$?` captures or of all `st_*=` assignments in the head must change, AND the tally block
  must be byte-identical. An inert head edit (a comment, an unused-variable rename) validates as
  **invalid**, never as a must-kill the tool would blamelessly pass.
- **accept + `kind=head`** — the head may differ cosmetically but the tally block must be
  byte-identical: a lethal block mutation riding behind a benign head edit is refused
  (`head-with-block-edit`).
- **accept + `vector`** — behavioral **equivalence**: the pristine and mutated tally blocks must
  produce the same `(exit, first-line)` tuple on the named 9-status vector, with the bytes
  changed. Cosmetic/decoy clones (comments, nonces, spacing) are satisfiable — as they must be,
  because the audit tool correctly accepts them.
- **kill + `vector`** — behavioral **difference** on the named len-9 vector, with the block
  changed. (Vector length 9 is enforced at validation; shorter vectors only compare crash
  signatures, never tally behavior — round-33 amendment.)

## Why the set-blind predecessor was voidable (RevengerWitness, round 33)

The frozen gate ran one author-chosen witness and only required a textual difference, with no
branch on the set. Consequences, both demonstrated by execution:

- a `kill` copy whose only edit was an inert head rename validated as a must-kill; the tool
  PASSes it → the claim voids with a blameless tool;
- an `accept` copy carrying a lethal block edit behind a benign head change validated as a
  must-accept; the tool KILLs it → the claim voids;
- a genuinely-equivalent `accept` clone could carry **no** valid witness (equivalence demands
  `a == b`, the old rule demanded `a != b`) → any cosmetic clone in the set voided the whole
  claim.

The rule is set-aware precisely so the sealed set tests the tool's real failure surfaces
(head leg-assignment integrity; tally counting behavior) instead of the author's construction
tricks.

## Evidence

- Implementation: `ho_witness_ok` in `.ufo/evidence/round-33/c1/c1-measure.py` (amendment 6,
  disclosed in `.ufo/evidence/round-33/contract-amendments.json`), adopted BEFORE any sealed
  authoring.
- Probe battery (8/8 exact): `.ufo/evidence/round-34/dev/witness-probes.{json,stdout}`.
- Sealed set: `.ufo/evidence/round-33/heldout/` — 8 must-kill (2 head-surface, 6 block classes:
  arm swap, fail-threshold escape, setup-arm skip, count-field swap, setup-threshold escape,
  fail-exit swap) + 6 must-accept (2 head-cosmetic, 4 block-equivalent); per-copy authoring
  receipts `.ufo/evidence/round-34/dev/authoring-receipts.json`.
- Deciding run: `C1_R33: … ho_kill=8/8 ho_accept=6/6 ho_invalid=0 … C1_R33_PASS=true` at
  `c17e593b` (`.ufo/evidence/round-34/measure/`).

## Sources

- **S097** — GNU Bash Reference Manual (Bash 5.3 `bashref.texi`): the runner's tally block
  communicates through the process exit status (0 success, 1/2 failure classes, special
  statuses) plus the first stdout line, and its `case` arms match the first pattern — exactly
  the `(exit, first line)` tuple the vector witness compares and the arm semantics the kill
  copies perturb (`corpus/SOURCES.md` row S097, opened in an earlier round).
- **S101** — Major Mutation Framework (mutation-testing.org): equivalent mutants are a
  first-class, named concern in mutation-testing frameworks ("suppressing equivalent
  mutants… the set of live mutants") — the reason the accept+vector witness demands
  equivalence (`a == b`), not difference (`corpus/SOURCES.md` row S101, opened this round;
  committed snapshot `.ufo/evidence/round-34/src/s101-mutation-testing.html`).
