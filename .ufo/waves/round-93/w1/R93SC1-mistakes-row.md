# R93SC1 — draft block 3: a `## Mistakes` row for the round-93 lesson

**For:** TameshiR93 (L1), for integration into `corpus/lessons/round-93.md`.
**Lane mode:** read-only; this seat wrote nothing under `corpus/`.

## Where the row goes

`corpus/lessons/round-93.md` currently ends with `## Claim and kill` and says: "the
`## Mistakes`, `## Measurements` and `## Wave` sections are appended in the records
commit." The house format (round 91 `:70-73`, round 92 `:15-22`) is a table with the
columns `| id | class | evidence pointer | captured-by | fix |`, one row per mistake, the
class in bold, and the `captured-by` column naming the QUALITY criterion that catches the
class. The id below is **`M1`** — the round-93 lesson's first mistake row — but the L1
owns the final numbering, since other seats may also have found round-93 mistakes.

--- BEGIN INTEGRATION TEXT ---

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **a duplicated rule hides which removal is load-bearing.** The counter carried the stray-verdict rule in two places at once, and the battery's first removal mutant (`D01`) edited only one of them, so the mutant did not test what the removal was supposed to test. At the pre-A3 instrument revision `b34c929e` the reader had the rule twice: once inside the table loop (for a table whose header row carries no `verdict` cell, `bad.append("stray-verdict:%d:%s" % (ln + 1, cells[0][:24] …))`) and once in the block-line scan (`bad.append("stray-verdict:%d:%s" % (oi + 1, raw.strip()[:24]))`). The driver's `D01` anchor matches only the second copy, so with the first copy still live the `renamed-result` state was still refused: the D01 mutant printed `C1_R93_PASS=false`, `ids=false`, `badrows=2`, `C1_BADROWS stray-verdict:299:C01 stray-verdict:300:C02` — the opposite of the expected `C1_R93_PASS=true` — and the driver scored the control `D01 MISMATCH exit=1`. Two copies of one rule mean a reader (or a reviewer reading the diff) cannot tell which copy is load-bearing, and a single-site removal mutant then measures the wrong thing: it reports a defect that is not the one it was built to find. The repair is one rule in one place. | the instrument diff `git diff b34c929e 855f0c1c -- .ufo/evidence/round-93/c1/measure-v93.py` (the two `stray-verdict` sites at `b34c929e` — `:260` and `:266` — collapse to one at `855f0c1c:262`, under the comment "One rule, one place"); the driver's D01 anchor (`.ufo/evidence/round-93/c1/controls-v93.py:196-204` at `69d377a0`), which is the same anchor at both revisions; the pre-A3 mutant reproduced from committed bytes by this seat's `.ufo/waves/round-93/w1/R93SC1-revc-d01-repro.sh` (output `R93SC1-revc-d01-repro.out`: `D01 MISMATCH exit=1`, mutant `counter_sha=162aff7612bbfb82e375837c840ababe11f3ae90e780883b8d0462376f67df28`); the frozen A3 receipt `.ufo/evidence/round-93/pre-freeze/controls/D01.out` (mutant `counter_sha=4bd4b77ce8b5ae4268b4bfb631cc71650306d4ed8e80126bf5d97509bb0c2d35`, `exit=0`, `C1_R93_PASS=true`, `badrows=0`) — the same anchor, the same state, the opposite verdict, because the rule is now single-site | none — QUALITY 149 asks that a removal control turn a refusal into a pass, but says nothing about the removed rule existing in more than one place, so a removal that edits one copy of a duplicated rule still "removes the rule" in the letter and measures the wrong defence in the fact; QUALITY 151 (the header count as a defence in its own right) is the neighbouring lesson on duplicated defences | the reader carries the stray-verdict rule once, in the block-line scan, and the table loop no longer has a second copy (`.ufo/evidence/round-93/c1/measure-v93.py:262` at `855f0c1c`); the D01 removal mutant now flips the cheat back (`C1_R93_PASS=true`, exit 0), so the control measures the defence it names. A rule duplicated across two call sites is removed from both, or the removal mutant is stated over the whole rule, not over one site of it |

--- END INTEGRATION TEXT ---

## Notes for the L1

- **The evidence pointer in the item is `.ufo/evidence/round-93/c1/measure-v93.py` rev
  `855f0c1c` vs the D01 run.** The row above cites that pair explicitly: the A3
  instrument (one rule, one place) and its D01 receipt
  (`.ufo/evidence/round-93/pre-freeze/controls/D01.out`, `exit=0`,
  `C1_R93_PASS=true`) — the D01 run *the frozen claim rests on*.
- **The defect itself is pre-A3, so the A3-vs-D01 pair alone does not show it.** The
  committed receipts for the pre-A3 instrument were not kept; the lane's `D01.out` was
  re-run against the A3 counter and the earlier receipt is not in the tree. This seat
  therefore **re-derived** the pre-A3 D01 outcome from committed bytes — the rev-C
  counter blob and the rev-C driver blob, both read with `git cat-file` — and committed
  the reproduction script and its output next to this draft
  (`R93SC1-revc-d01-repro.sh` / `.out`), so the L1 can re-run it from committed bytes.
  The row cites that script as its evidence pointer for the defect, and the committed
  A3 receipt for the repair. The claim in the row is stated as a re-derivation, not as a
  citation of a receipt this lane never committed.
- **The class is stated in the item's words** — "a duplicated rule hides which removal is
  load-bearing" — and the row body shows why that is the class: with two copies, the
  single-site removal mutant reported `ids=false` on a state where the *second* copy
  had been deleted, so the mutant's failure said nothing about the rule it named.
- **The row does not claim the round-93 D01 receipt was wrong.** The committed
  `.ufo/evidence/round-93/pre-freeze/controls/D01.out` is correct for the A3 counter
  (`counter_sha=4bd4b77c…` recomputed from the A3 bytes by this seat matches the receipt
  exactly). The mistake is in the earlier instrument revision, before the freeze.

VERDICT: drafted
TOOLS: none
