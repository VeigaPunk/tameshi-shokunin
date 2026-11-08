# R94SC1 — draft block 3: a `## Mistakes` row for the round-93 lesson

**For:** TameshiR94 (L1), for integration into `corpus/lessons/round-93.md`.
**Lane mode:** read-only; this seat wrote nothing under `corpus/`.

## What the L1 must decide before integrating

The class the item names — **"a duplicated rule hides which removal is load-bearing"** —
is **already recorded** in the round-93 lesson as `M2`, at
`corpus/lessons/round-93.md:38`, and in QUALITY.md as criterion **159**:

```
| M2 | **a duplicated rule hid which removal was load-bearing.** The stray-verdict rule existed
twice (per-table and per-block-line); `D01` removed only the second copy, so the mutant still
refused `renamed-result` and the control read `MISMATCH`, not `PASS`. | first subset run
`D01.out` (`mutant=D01 state=renamed-result`, `exit=1`, `C1_R93_PASS=false`); the counter now
states the rule once, outside the verdict table (`measure-v93.py` rev `855f0c1c`), and `D01`
prints `C1_R93_PASS=true` | ...
```

That row and criterion 159 are **frozen history**: `lessons/round-93.md` was committed at
`d817ffcd` (round-93 records) and has not been touched since, and QUALITY 159 is committed.
So this draft is **not** a re-statement of M2. It is the **evidence-pointer correction**
that the round-93 row's own pointer needs, which only becomes visible when the row is read
against the tree as committed.

## The defect in the round-93 row's evidence pointer

The committed M2 row points at:

> "first subset run `D01.out` (`mutant=D01 state=renamed-result`, `exit=1`,
> `C1_R93_PASS=false`)"

**No such receipt exists.** Checked over the whole lane history, not just the tip:

| candidate | what it actually says |
|---|---|
| `.ufo/evidence/round-93/pre-freeze/controls-firstrun/D01.out` (the "firstrun" directory) | `exit=0`, `C1_R93_PASS=true` |
| `.ufo/evidence/round-93/pre-freeze/controls/D01.out` | `exit=0`, `C1_R93_PASS=true` — **byte-identical** to the firstrun file (sha256 `63fd5f80…` for both) |
| every `D01.out` blob in every revision of the lane | `exit=0`, `C1_R93_PASS=true` |

The only artifact in the entire tree that shows a D01 mutant refusing `renamed-result` is
`.ufo/waves/round-93/w1/R93SC1-revc-d01-repro.out` — the **wave seat's own re-derivation
output**, not a committed battery receipt:

```
mutant=D01 state=renamed-result
counter_sha=162aff7612bbfb82e375837c840ababe11f3ae90e780883b8d0462376f67df28
exit=1
...
C1_SUMMARY rev=HEAD ... badrows=2 verdict_tables=1
C1_BADROWS stray-verdict:299:C01 stray-verdict:300:C02
C1_CONJUNCTS ... ids=false ...
C1_R93_PASS=false
```

That output is produced by `.ufo/waves/round-93/w1/R93SC1-revc-d01-repro.sh`, which runs
the **pre-A3** counter `b34c929e` (two copies of the stray-verdict rule) against the
**A3** counter `855f0c1c` (one copy). The `counter_sha` above (`162aff76…`) is the
**mutated rev-C counter** — the rev-C bytes with the block-line copy of the rule replaced
by `pass` and the self-pin recomputed. Re-derived here from committed bytes, that
construction reproduces the digest exactly:

```
anchor occurrences in rev-C counter: 1
   mutated+repinned sha256: 162aff7612bbfb82e375837c840ababe11f3ae90e780883b8d0462376f67df28  MATCHES
```

So the receipt is a **mutation study over a scratch copy of the counter**, not a battery
receipt produced by the frozen driver — which is why no committed `D01.out` carries
those values.

The construction is reproduced byte for byte by
`R94SC1-d01-counter-sha.py` (saved beside this file; output
`R94SC1-d01-counter-sha.out`), which rebuilds the driver's own mutation —
replace the anchor with `pass`, strip the self-pin line, re-pin, hash:

```
b34c929e  rev-C (pre-A3, two copies of the rule)
   stray-verdict append sites in the counter: 2
   D01 anchor occurrences: 1
   mutated+re-pinned sha256: 162aff7612bbfb82e375837c840ababe11f3ae90e780883b8d0462376f67df28  MATCHES
855f0c1c  rev-A3 (one copy of the rule)
   stray-verdict append sites in the counter: 1
   D01 anchor occurrences: 1
   mutated+re-pinned sha256: 4bd4b77ce8b5ae4268b4bfb631cc71650306d4ed8e80126bf5d97509bb0c2d35  MATCHES
```

Both digests reproduce exactly, and the `stray-verdict` site count (**2** at rev-C, **1**
at rev-A3) is the defect's own fingerprint, read straight off the two counter blobs.

**And the D01 mutant is not a `MISMATCH` in the committed receipts.** The driver's
expectation for D01 at the frozen A3 counter is `(0, {"__pass": True})` — D01 *should*
print `C1_R93_PASS=true` — and the committed A3 receipt does exactly that
(`.ufo/evidence/round-93/pre-freeze/controls/D01.out`: `exit=0`, `C1_R93_PASS=true`).
The `MISMATCH` the row describes occurred only at the **pre-A3** revision, which is
precisely the point: the row is about a defect of the *pre-A3* instrument, and its pointer
must name that instrument, not a receipt that happens to be called `D01.out`.

### The row as it stands is therefore not wrong about the defect, only wrong about where the
### witness lives

Re-derived by this seat from committed bytes: at `b34c929e` the counter has **two**
`stray-verdict` append sites (lines 260 and 266), and the driver's D01 anchor matches only
the second; at `855f0c1c` it has **one** (line 262). The re-derivation reproduces the
pre-A3 behaviour exactly:

```
== the two copies of the stray-verdict rule at b34c929e ==
260:                bad.append("stray-verdict:%d:%s" % (ln + 1, cells[0][:24] if cells else ""))
266:            bad.append("stray-verdict:%d:%s" % (oi + 1, raw.strip()[:24]))
== the single copy at 855f0c1c59ee2af7f184d8de62d02cdd576eb94e ==
262:            bad.append("stray-verdict:%d:%s" % (oi + 1, raw.strip()[:24]))
== the D01 anchor in the driver (rev C) ==
    a = """        toks = [c for c in split_cells(raw) if c in VERDICTS]
        if toks:
            bad.append("stray-verdict:%d:%s" % (oi + 1, raw.strip()[:24]))
    """
== running the rev-C battery with --only D01 ==
CONTROL_INSTRUMENT sha256=8f41c34248f5237fd61b1aa36d661017d84d364bf32d42c683020417f509b307
D01 MISMATCH exit=1
C1_CONTROLS states=1 matched=0 mismatches=1 missing=0 [D01]
```

(re-run by this seat; output saved as `R94SC1-d01-repro.out` beside this file. The
committed round-93 wave output is byte-identical to this re-run **except for the two
`C1_BADROWS` line numbers** — `299/300` then, `330/331` now — because the pre-A3 driver
appends its fixture text to the note **as it stands in the working tree**, and the note has
grown by 31 lines since. The `D01 MISMATCH exit=1`, `ids=false` and `C1_R93_PASS=false`
verdicts are unchanged.)

So the honest witness for the class is: **the pre-A3 instrument `b34c929e` (two sites)
against the A3 instrument `855f0c1c` (one site)**, witnessed by the committed wave
re-derivation and reproducible from committed bytes — not by a `D01.out` receipt, which
reads `exit=0` everywhere it is committed.

--- BEGIN INTEGRATION TEXT ---

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M2 | **a duplicated rule hid which removal was load-bearing.** The stray-verdict rule existed twice (per-table and per-block-line); `D01` removed only the second copy, so the mutant still refused `renamed-result` and the control read `MISMATCH`, not `PASS`. | the pre-A3 counter `b34c929e` carried the rule twice (`measure-v93.py` lines 260 and 266) and the A3 counter `855f0c1c` carried it once (line 262), and the driver's `D01` anchor matched only the block-line copy; the witness is the re-derivation committed at `.ufo/waves/round-93/w1/R93SC1-revc-d01-repro.out` (`D01 MISMATCH exit=1`, `C1_BADROWS stray-verdict:299:C01 stray-verdict:300:C02`, `ids=false`, `C1_R93_PASS=false`), reproducible from committed bytes by `.ufo/waves/round-93/w1/R93SC1-revc-d01-repro.sh`. The committed battery receipts `.ufo/evidence/round-93/pre-freeze/controls/D01.out` and `controls-firstrun/D01.out` are byte-identical (`sha256 63fd5f80…`) and read `exit=0` / `C1_R93_PASS=true` — they witness the **repaired** counter at `855f0c1c`, not the defect, and the first-run directory does not hold the `exit=1` receipt the earlier pointer named. | the removal-mutant control itself; no rule required a rule to have one implementation site | QUALITY 159. Able to fail: the D01 control (a rule with two sites leaves the mutant alive) |

--- END INTEGRATION TEXT ---

## Two things the L1 must weigh

**1. This row edits a committed lesson.** `corpus/lessons/round-93.md` was committed at
`d817ffcd` and is not in the frozen-artifacts list (that list names
`plans/round-93.plan.md`, `.ufo/waves/round-93/claims.json` and everything under
`.ufo/evidence/round-93/`), and `corpus/lessons/round-93.md` has been edited by later
rounds before (its history includes `2083af6c` and `09cd271c`, both after `d817ffcd`). So
amending it is within the lane's practice — but it rewrites a closed round's record, and the
L1 may prefer to leave round 93 closed and record the pointer correction in round 94's
lesson instead. **That alternative changes the file and the row id, so it is the L1's
call, not this seat's.**

**2. The correction does not weaken the class.** The row's *claim* — a duplicated rule hid
which removal was load-bearing — is confirmed here from committed bytes, from the two
pre-A3 `stray-verdict` sites against the driver's single-copy anchor, and from the
re-derivation's `D01 MISMATCH exit=1` / `ids=false` / `C1_R93_PASS=false`. What changes
is only *where the witness lives*: it is the wave seat's re-derivation and the two
instrument revisions, not a committed `D01.out` receipt, which reads `exit=0` at every
path where it is committed. QUALITY 159's "Able to fail" clause — "round 93's `D01`
removed only the second copy of the stray-verdict scan and the mutant still refused
`renamed-result` (`exit=1`, `C1_R93_PASS=false`)" — states the same fact and points at the
same condition; the row and the criterion stay consistent after the pointer is repaired.

### The row id

`M2` is the **existing** row's id in `corpus/lessons/round-93.md` — this draft replaces
that row in place, keeping its id, so the row count does not change and no other row's
numbering moves. If the L1 instead records the correction in round 94's lesson
(`corpus/lessons/round-94.md`, whose `## Mistakes` table currently holds M1–M4), the id
would be `M5` and the row text would need the "for the round-93 lesson" framing above
removed. Both variants are one edit apart; this draft carries the round-93 variant because
the item names the round-93 lesson.

VERDICT: drafted
TOOLS: none
