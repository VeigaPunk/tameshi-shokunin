# T55W2MutC1 — mutation test of the frozen round-55 C1 counter at C0 (calibration, wave 2)

Target: `.ufo/evidence/round-55/c1/measure.py` at `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.
Counter bytes under test: `sha256 5e8f50d1815309e8c3a1c914191b6032b7dceff27ba42d87a676b3f78e30ac5e`
(identical to the lane worktree copy at the time of the run — see *Restoration evidence*).

Attack: 8 single-edit mutants (7 non-equivalent guards + 1 expected-equivalent
redundancy probe), each scored twice — **at C0** (does the certified run see the
weakened counter?) and **against a defect fixture** that reintroduces exactly the
record defect the mutated check guards (does the mutant let that defect through?).
Plus a 7-probe **drift sweep** with 5 positive controls, to separate "mutant is
equivalent" from "the detector is already blind".

Verdict: **7 KILLED, 1 SURVIVED (= redundant arm), 0 inconclusive.**
The kills come *only* from fixtures I authored: **at C0 all 8 mutants are
byte-identical to the frozen counter's output**, so the certified run itself
discriminates none of them (finding F1). The real finding is F2: the ten `stale`
arms match literal bytes, and 7/7 surface-drift restatements of the same
falsehoods pass the frozen counter while 5/5 exact-token controls at the same
insertion points fail it.

## 1. Protocol

* Every mutant is a copy of the C0 blob with **one** expression/statement edit
  (`mutants/M?.diff`, 1 hunk each). No lane file is ever edited in place; no
  fixture is built inside the lane.
* Fixtures are `git clone --shared` copies of the lane at C0 in scratch; each
  fixture's edit is committed there and each git call names `-C <fixture>`; each
  fixture asserts `rev-parse --show-toplevel` == its own directory before
  committing (regression guard against the wave-1 shared-parent/`rm -rf`
  incident).
* Score = exit code + the ten `EXPLAIN <id> ok|FAIL` row states + the `C1_R55:`
  verdict line. **KILLED** = mutant's score differs from the pristine score on
  some scenario. **SURVIVED** = identical on all 8 scenarios (C0 + D1..D7).
* Fills a gap the pristine counter itself cannot see: `stale=0`, `total=0` and
  `C1_R55_PASS=true` at C0 are reproduced verbatim by every mutant.

Reproduce (both scripts are self-contained; receipts dir is the lane's
`.ufo/waves/round-55/w2/T55W2MutC1-receipts`):

```
python3 reproduce.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb \
  --scratch $HYAKU_SCRATCH/tameshi-r55/T55W2MutC1/matrix --receipts $PWD
python3 variants.py  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb \
  --scratch $HYAKU_SCRATCH/tameshi-r55/T55W2MutC1/variants --receipts $PWD --suite drift
python3 variants.py  ... --suite control
```

## 2. Baseline (pristine counter at C0)

```
$ sha256sum mutants/M0-pristine.py
5e8f50d1815309e8c3a1c914191b6032b7dceff27ba42d87a676b3f78e30ac5e  mutants/M0-pristine.py
$ python3 mutants/M0-pristine.py --lane <clone@C0> --rev 9cf0146b94dd... --work <empty> --explain
EXPLAIN R54.1 ok premise=ok corrected=ok stale=0 derived=CTL_MISMATCH + 2/3
...
EXPLAIN R54.10 ok premise=ok corrected=ok stale=0 derived=controls-a rekeyed=0/7
C1_R55: rev=9cf0146b94dd classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
rc=0
```

## 3. Mutants and verdicts

| id | single edit | sha256 (first 12) | at C0 | killed by | verdict |
|----|-------------|-------------------|-------|-----------|---------|
| M1 | drop R54.3's stale scan (`total=14`) | `218e068bed60` | equivalent | D1, D4 | **KILLED** |
| M2 | replace R54.3's derived value with literal `total=13` | `8edbda78c27e` | equivalent | D2 | **KILLED** |
| M3 | `premise=false` treated as ok (`ok` drops `premise`) | `b972533f3473` | equivalent | D3 | **KILLED** |
| M4 | corrections not trimmed at the next `## ` heading | `e5f4f8e1671a` | equivalent | D4 | **KILLED** |
| M5 | reader files counted from the working tree, not `git` at REV | `d79cbb69f649` | equivalent | D5 | **KILLED** |
| M6 | span scan `re.IGNORECASE` (whole pattern, incl. `rekeyed=7/7`) | `f51f79750b5c` | equivalent | D6 | **KILLED** |
| M7 | drop R54.1's span arm, keep the line arm | `820db60d7acf` | equivalent | D7 | **KILLED** |
| M8 | drop R54.1's line arm over QUALITY/lessons, keep span arm | `b9df4302106b` | equivalent | — | **SURVIVED** |

"at C0 = equivalent" is measured, not assumed: the ten EXPLAIN lines + verdict
line at C0 hash identically for all nine counters:

```
$ for f in runs/C0__*.stdout; do printf '%-18s %s\n' "$(basename $f)" \
    "$(grep -E '^(EXPLAIN|C1_R55)' $f | sha256sum | cut -c1-16)"; done
C0__M0.stdout      3622501ccbf46368
C0__M1.stdout      3622501ccbf46368
...
C0__M8.stdout      3622501ccbf46368
```

### Defect fixtures (each reintroduces the defect its mutant guards)

| id | guard attacked | fixture rev | what it does | pristine | mutant that passes |
|----|----------------|-------------|--------------|----------|--------------------|
| D1 | R54.3 stale | `100b38521e9e` | `C2 claim row (round-54): total=14` re-enters SCORECARD before the corrections heading | FAIL R54.3 | **M1** |
| D2 | R54.3 derivation | `34fe5b496035` | `.ufo/evidence/round-54/before/c2.stdout` now prints `total=15` | FAIL R54.3 (`corrected=miss`) | **M2** |
| D3 | R54.1 premise | `6766a540af8b` | `controls-b.stdout` prints `CTL_MATCH ... actual=true` | FAIL R54.1 (`premise=miss`) | **M3** |
| D4 | corrections trim | `4c366407a730` | a new `## Round 56 - placeholder` section after the corrections carries `total=14` | FAIL R54.3 | **M4** (and M1) |
| D5 | R54.5 counts | `67b33940ecd9` | extra reader file committed, then deleted from the worktree only | FAIL R54.5 (`corrected=miss`, `w2=26 sections=13`) | **M5** |
| D6 | span case | `ee161a0963b9` | `Positive Control prints Rekeyed=7/7 on its arm.` | **PASS** | all incl. **M6** |
| D7 | span arm | `5bbf967aeb60` | same falsehood hard-wrapped: `The positive control`⏎`prints rekeyed=7/7 on its arm.` | FAIL R54.1 | **M7** |

## 4. Verdict lines (verbatim, per mutant × its killing fixture)

```
# M1 (D1)
$ python3 mutants/M0-pristine.py --lane fx-D1 --rev 100b38521e9e ... --explain
EXPLAIN R54.3 FAIL premise=ok corrected=ok stale=1 derived=total=13
EXPLAIN R54.3 stale: SCORECARD.md:2621: C2 claim row (round-54): total=14
C1_R55: rev=100b38521e9e classes=10 premise=10/10 stale=1 classes_corrected=10/10 total=1 C1_R55_PASS=false
$ python3 mutants/M1.py --lane fx-D1 --rev 100b38521e9e ... --explain
C1_R55: rev=100b38521e9e classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
→ M1 KILLED (the dropped scan lets the stale total=14 row through)

# M2 (D2)
$ ... M0 on fx-D2
EXPLAIN R54.3 FAIL premise=ok corrected=miss stale=0 derived=total=15
C1_R55: rev=34fe5b496035 ... total=1 C1_R55_PASS=false
$ ... M2 on fx-D2
EXPLAIN R54.3 ok premise=ok corrected=ok stale=0 derived=total=15
C1_R55: rev=34fe5b496035 ... total=0 C1_R55_PASS=true
→ M2 KILLED (the literal 13 "agrees" with a record whose receipt says 15)

# M3 (D3)
$ ... M0 on fx-D3
EXPLAIN R54.1 FAIL premise=miss corrected=ok stale=0 derived=CTL_MISMATCH + 2/3
C1_R55: rev=6766a540af8b ... premise=9/10 ... total=1 C1_R55_PASS=false
$ ... M3 on fx-D3
EXPLAIN R54.1 ok premise=miss corrected=ok stale=0 derived=CTL_MISMATCH + 2/3
C1_R55: rev=6766a540af8b classes=10 premise=9/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
→ M3 KILLED (and note the mutant's own line reads PASS while reporting premise=9/10)

# M4 (D4)
$ ... M0 on fx-D4
EXPLAIN R54.3 FAIL premise=ok corrected=ok stale=1 derived=total=13
EXPLAIN R54.3 stale: SCORECARD.md:2625: The C2 claim row quotes total=14.
C1_R55: rev=4c366407a730 ... total=1 C1_R55_PASS=false
$ ... M4 on fx-D4
C1_R55: rev=4c366407a730 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
→ M4 KILLED (untrimmed corrections swallow every later section of SCORECARD)

# M5 (D5)
$ ... M0 on fx-D5
EXPLAIN R54.5 FAIL premise=ok corrected=miss stale=0 derived=w1=28 w2=26 sections=13
C1_R55: rev=67b33940ecd9 ... classes_corrected=9/10 total=1 C1_R55_PASS=false
$ ... M5 on fx-D5   (worktree has the extra reader deleted again)
EXPLAIN R54.5 ok premise=ok corrected=ok stale=0 derived=w1=28 w2=25 sections=12
C1_R55: rev=67b33940ecd9 ... total=0 C1_R55_PASS=true
→ M5 KILLED (the worktree read makes the record agree with an uncommitted tree)

# M6 (D6)
$ ... M0 on fx-D6
EXPLAIN R54.1 ok premise=ok corrected=ok stale=0 derived=CTL_MISMATCH + 2/3
C1_R55: rev=ee161a0963b9 ... total=0 C1_R55_PASS=true          ← pristine MISSES the claim
$ ... M6 on fx-D6
EXPLAIN R54.1 FAIL premise=ok corrected=ok stale=1 derived=CTL_MISMATCH + 2/3
EXPLAIN R54.1 stale: corpus/lessons/round-54.md@8026: ... Positive Control prints Rekeyed=7/7 on its arm.
C1_R55: rev=ee161a0963b9 ... stale=1 ... total=1 C1_R55_PASS=false
→ M6 KILLED, but in the *widening* direction: the mutant is stricter than the frozen
  counter. This fixture is a frozen-counter blind spot (F2), not a mutant escape.

# M7 (D7)
$ ... M0 on fx-D7
EXPLAIN R54.1 FAIL premise=ok corrected=ok stale=1 derived=CTL_MISMATCH + 2/3
EXPLAIN R54.1 stale: corpus/lessons/round-54.md@8030: ... The positive control prints rekeyed=7/7 on its arm.
C1_R55: rev=5bbf967aeb60 ... stale=1 ... total=1 C1_R55_PASS=false
$ ... M7 on fx-D7
C1_R55: rev=5bbf967aeb60 ... stale=0 ... total=0 C1_R55_PASS=true
→ M7 KILLED (the span arm is the only thing that sees a hard-wrapped claim)

# M8 (all 8 scenarios)
$ ... M8 on fx-D7  (and C0, D1..D6)
EXPLAIN R54.1 FAIL ... stale=1 ... ; C1_R55: rev=5bbf967aeb60 ... total=1 C1_R55_PASS=false
→ M8 SURVIVED: identical to pristine everywhere. Equivalent mutant — finding F3.
```

## 5. Findings

**F1 (coverage, medium) — the certified run has zero discriminating power over
these guards.** All 8 mutants reproduce the C0 output byte for byte
(`runs/C0__M*.stdout`, identical digest). Expected for a clean tree, but it means
wave 1's `C1_R55_PASS=true` is evidence that the *record* is clean, never that the
*counter* is strong: each of the seven single edits would have passed the same
command at C0. The kills in §4 exist only because I authored fixtures. A future
wave should keep those fixtures as the counter's regression battery — without
them, the counter can silently lose any one arm.

**F2 (blind spot, high) — the `stale` arms match literal bytes; drift variants of
the same falsehoods pass.** Seven probes restate a routed defect with case,
spacing or one inserted word. The pristine counter passes all seven; five
positive controls that use the exact literal at the *same insertion point and
same file* fail as required. So the probes' PASSes are a property of the arms,
not of where the text was inserted.

```
$ python3 variants.py ... --suite drift
V1 R54.3 spacing drift          rc=0 failed=[] blind_spot=True    "total = 14"
V2 R54.3 case drift             rc=0 failed=[] blind_spot=True    "Total=14"
V3 R54.1 tab/space drift        rc=0 failed=[] blind_spot=True    "CTL_POS_c1  true"
V4 R54.9 word insertion         rc=0 failed=[] blind_spot=True    "84 files staged"
V5 R54.2 hash case drift        rc=0 failed=[] blind_spot=True    "FE70474D"
V6 R54.1 sentence-start capital rc=0 failed=[] blind_spot=True    "Positive control prints rekeyed=7/7 on its arm."
V7 R54.1 operator spacing       rc=0 failed=[] blind_spot=True    "the positive control requires rekeyed = 7/7"
blind_spots=7/7

$ python3 variants.py ... --suite control      # same positions, exact literals
K1 R54.3 exact token   rc=1 failed=['R54.3']    "total=14"
K2 R54.1 exact token   rc=1 failed=['R54.1']    "CTL_POS_c1 true"
K3 R54.9 exact token   rc=1 failed=['R54.9']    "84 staged"
K4 R54.2 exact token   rc=1 failed=['R54.2']    "fe70474d"
K5 R54.1 exact span    rc=1 failed=['R54.1']    "the positive control prints rekeyed=7/7"
blind_spots=0/5
```

V6 vs K5 is the sharpest pair: the two sentences differ **only** in the capital
`P`/`R` and the counter's verdict flips from PASS to FAIL. The frozen span arm is
case-sensitive (the arm exists precisely because the round-54 falsehood was
hard-wrapped, i.e. it was written as running prose where a sentence-initial
capital is normal), so a restatement beginning a sentence is invisible. Same
class of gap for `total = 14`, `Total=14`, `84 files staged`, `FE70474D`. The
arms detect the recorded *bytes*, not the recorded *claim*.

**F3 (redundancy, low) — M8 survives: R54.1's line arm over QUALITY/lessons is
subsumed by the span arm.** K5 shows `stale=2` (both arms hit the same sentence);
M8 on D7 shows `stale=1` and the identical FAIL, and M8 is identical to pristine
on all 8 scenarios. So the line-scoped arm at `measure.py:201-202` cannot fire
without the span arm also firing. Not a correctness failure — a dead arm the
counter's own docstring does not need (and a place where a future edit could
believe it is guarding something).

**F4 (latent, medium) — the corrections trim is unexercised at C0.** The section
runs from `SCORECARD.md:2621` to EOF (`wc -l` 2702); there is no `## ` heading
after it. `corrections()` trimmed and untrimmed therefore return the same string
at C0, so **M4 is byte-identical to the frozen counter at the certified rev**.
D4 shows the arm matters the moment any section is appended after the corrections
(the untrimmed reader silently strips every later stale token from the body it
searches). Any wave that appends a round-56 section to `SCORECARD.md` turns this
latent gap live with no counter edit.

**F5 (confirmation, positive) — amendment 7's receipt/rev anchoring holds.** D5
is the mutation that amendment 7 exists to prevent (worktree-derived numbers) and
it is detected: the rev-based reader list keeps the record honest while the extra
file is committed, and M5's worktree read silently accepts the pre-commit state.
Related live evidence, not mine to fix: the lane worktree currently shows
` M .ufo/evidence/round-55/before/c2.stdout` (another seat's change). No counter
arm reads the worktree, so that churn cannot move C1's verdict — which is exactly
the property amendment 7 bought.

**Observation (not a defect)** — M3's line is self-inconsistent
(`PASS=true` while printing `premise=9/10`). A human reading the line would
notice; the exit code would not. If a premise-blind counter is ever reintroduced,
the `premise=` field is the only tell.

## 6. Limitations

* Every KILLED verdict is a **fixture kill**, not a C0 kill. The fixtures encode
  what the routed defects mean; five of them (D1..D5) are confirmed by the
  pristine counter failing them, which is what makes the kill non-tautological.
  D6 is the exception: its pristine PASS is itself the finding (F2).
* M6's kill is in the over-detection direction. It is reported as KILLED because
  its score differs, but it does not represent a defect the mutant would let
  through — F2 does.
* Only the `stale`/`corrected`/`premise` logic was mutated. I did not mutate
  `staged_count`, `wave_numbers` or `derive_freeze_digest` beyond M5's source
  change; the 10 classes were attacked one arm at a time, not in combination.
* Scratch clones were disposable by tasking; fixture identities in this report
  are the committed revs printed by the runs plus the patch files under
  `fixtures/`, which regenerate the fixture content exactly.

## 7. Restoration evidence

Nothing was mutated in place, so there was nothing to restore — and the frozen
bytes are provably unchanged:

```
$ git show 9cf0146b94dd...:.ufo/evidence/round-55/c1/measure.py | sha256sum
5e8f50d1815309e8c3a1c914191b6032b7dceff27ba42d87a676b3f78e30ac5e  -
$ sha256sum .ufo/evidence/round-55/c1/measure.py
5e8f50d1815309e8c3a1c914191b6032b7dceff27ba42d87a676b3f78e30ac5e
$ sha256sum .ufo/waves/round-55/w2/T55W2MutC1-receipts/mutants/M0-pristine.py
5e8f50d1815309e8c3a1c914191b6032b7dceff27ba42d87a676b3f78e30ac5e
$ git diff --stat 9cf0146b94dd... -- .ufo/evidence/round-55/c1/   # no output
$ git status --porcelain -- .ufo/waves/round-55/w2                  # ?? .ufo/waves/round-55/w2/
```

Mutants live only under `mutants/` as separate files; the staged clones under
`$HYAKU_SCRATCH/tameshi-r55/T55W2MutC1/` were removed after the runs (`rm -rf --
"$S"`, never the shared parent). Lane write footprint = this dir only.

## 8. Artifacts

Scripts (runnable, self-contained):
`reproduce.py` (mutant matrix), `variants.py` (`--suite drift|control`).

| path | content |
|------|---------|
| `mutants/M0-pristine.py` | C0 counter bytes (sha `5e8f50d1…`) |
| `mutants/M1.py` … `M8.py`, `.diff` | seven+one single-edit mutant counters and their 1-hunk diffs |
| `mutants/SHA256SUMS` | hashes of all nine counters |
| `fixtures/D1..D7.patch` | the exact defect each fixture commits |
| `probes/V1..V7.patch`, `probes/K1..K5.patch` | drift restatements and exact-token controls |
| `runs/*.stdout` | 84 full counter runs (8 mutants × 8 scenarios, 12 probes) |
| `matrix.json` | mutant/fixture verdict table |
| `variants.json`, `variants-control.json` | drift sweep and its positive controls |

Artifacts opened (read-only): `.ufo/evidence/round-55/c1/measure.py` (at C0),
`SCORECARD.md` (at C0), `corpus/lessons/round-54.md`, `corpus/QUALITY.md`,
`.ufo/evidence/round-54/{control/controls-b.stdout,after/frozen.stdout,before/c2.stdout,freeze.json}`,
`.ufo/evidence/round-55/c1/staged-at-freeze.txt`, `.ufo/waves/round-54/w1-registry.json`,
`.ufo/waves/round-54/{w1,w2}/*Read*.json`.

Tool installs: none (python3 + git from the host; no package manager touched —
pacman is paused host-wide and no install was needed).
