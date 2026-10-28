# T55W2MutReceipts — mutation probe of the frozen C1 counter against the corrections section

Seat: `T55W2MutReceipts` (mutation-tester, wave 2, round 55, lane `tameshi-shokunin`).
Axis attacked: **calibration** — the frozen C1 counter
`.ufo/evidence/round-55/c1/measure.py` and the `## Round 55 - round-54 record
corrections` section it scores at content commit C0
`9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Assigned item: flip one derived value, remove one ER entry, move one old->new pair
above the `##` heading; every mutation must be caught; the third must show why
position matters; name any mutation the counter misses.

**Result: 3/3 required mutations killed (`C1_R55_PASS=false`). 4 probes survived —
each is a coverage finding about the counter, not about the section.**

## Setup (every mutation ran in its own `git clone --shared` at C0)

```
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r55/T55W2MutReceipts
git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/mut<X>
git -C $S/mut<X> checkout -q 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
git -C $S/mut<X> rev-parse --show-toplevel      # -> that clone dir (asserted per clone)
```

The counter is invoked from the lane's frozen bytes, never from the clone:

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/c1/measure.py \
  --lane $S/mut<X> --rev <mutant commit> --work <fresh empty dir> --explain
```

`--work` is a fresh empty dir per run (the counter writes `c1-derivations.json`
into it and refuses a non-empty one). Receipts:
`.ufo/waves/round-55/w2/T55W2MutReceipts-receipts/{<name>.cmd,<name>.stdout,<name>.stderr,<name>.diff}`.

Section under attack at C0: `SCORECARD.md` lines 2621-2702; it is the **last**
section of the file (no `## ` heading follows it), so `corrections()`
(`measure.py:67`) runs the section to EOF and `scan()` (`measure.py:83`) excludes
exactly those bytes from the record search.

## Baseline (pristine C0) — detector is live, PASS is real

`T55W2MutReceipts-receipts/base-C0.stdout`:

```
C1_R55: rev=9cf0146b94dd classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
rc=0
```

## Required mutations

### M1 — flip one derived value (`total=13` -> `total=12`)

```
$ python3 $S/mutate.py A $S/mutA
$ git -C $S/mutA commit -am mutA          # rev 85b040b16aeacdef59eff1807ac69a342092fd95
$ python3 .../c1/measure.py --lane $S/mutA --rev 85b040b16aea... --work <empty> --explain
EXPLAIN R54.3 FAIL premise=ok corrected=miss stale=0 derived=total=13
C1_R55: rev=85b040b16aea classes=10 premise=10/10 stale=0 classes_corrected=9/10 total=1 C1_R55_PASS=false
rc=1
```

Diff (`T55W2MutReceipts-receipts/mutA.diff`, SCORECARD.md:2650):

```
-Old: `total=14` in the C2 claim row. Corrected: `total=13`.
+Old: `total=14` in the C2 claim row. Corrected: `total=12`.
```

**Verdict M1: KILLED.** The counter derives `total=13` from
`.ufo/evidence/round-54/before/c2.stdout` and refuses the author's `12`; only the
corrected arm moves, the stale arm stays clean (the old value `total=14` was not
re-introduced).

### M2 — remove one ER entry (ER-R54-6, "round work uncommitted at closure")

```
$ python3 $S/mutate.py B $S/mutB
$ git -C $S/mutB commit -am mutB          # rev 525b167eec8c792b5e25e2135c7da6e632e41285
EXPLAIN R54.6 FAIL premise=ok corrected=miss stale=0 derived=sweep commit=ff2a821
C1_R55: rev=525b167eec8c classes=10 premise=10/10 stale=0 classes_corrected=9/10 total=1 C1_R55_PASS=false
rc=1
```

Diff: 6 deletions (`T55W2MutReceipts-receipts/mutB.diff`).

**Verdict M2: KILLED.** Absence is caught even though removal leaves no stale
token: the corrected arm is a positive membership test, so a missing entry fails
its own class by name (R54.6) rather than silently dropping a denominator —
`classes=10` is unchanged.

### M3 — move one old->new pair above the `##` heading (ER-R54-3, bytes unchanged)

The whole ER-R54-3 entry (header + `Old:` + `Corrected:` + `Receipt:`) was moved,
byte-identical, from inside the section to just above the `## Round 55 -
round-54 record corrections` heading:

```
$ python3 $S/mutate.py C $S/mutC
$ git -C $S/mutC commit -am mutC          # rev 25b1608adf0ec0f9cd694d952717982b78fcaf96
EXPLAIN R54.3 FAIL premise=ok corrected=miss stale=1 derived=total=13
EXPLAIN R54.3 stale: SCORECARD.md:2622: Old: `total=14` in the C2 claim row. Corrected: `total=13`.
C1_R55: rev=25b1608adf0e classes=10 premise=10/10 stale=1 classes_corrected=9/10 total=1 C1_R55_PASS=false
rc=1
```

Diff: `5 insertions(+), 4 deletions(-)`, no token changed (`mutC.diff`).

**Verdict M3: KILLED, and position is load-bearing in two independent ways.**
The same bytes outside the heading are simultaneously (a) no longer a correction —
`corrected=miss`, the section no longer carries the derived value — and (b) a live
falsehood in the record — `stale=1`, reported at `SCORECARD.md:2622`, because
`scan()` strips only `corrections(lane, rev)` before searching and that offset is
now above the heading. So the erratum's own `total=14` becomes a stale hit while
its absence from the section unsets the class: the counter's boundary is the
heading line `measure.py:33`, not a file-level allow-list.

## Mutations the counter misses (coverage findings about the counter)

Each survived with the section's *stated value* wrong. All four are presence /
substring tests, never equality against the derived fact.

### P1 — `total=13` -> `total=130` (substring membership) — SURVIVED

```
EXPLAIN R54.3 ok premise=ok corrected=ok stale=0 derived=total=13
C1_R55: rev=6bebed7523da classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
rc=0
```
`measure.py:221` tests `("total=%s" % n23) in corr`; `total=13` is a substring of
`total=130`. A ten-fold wrong total passes.

### P2 — digest and staged count extended by one digit — SURVIVED

```
-`8528ee85`            +`8528ee850`
-`staged=81`           +`staged=810`
EXPLAIN R54.4 ok ... derived=c2 digest=8528ee85
EXPLAIN R54.9 ok ... derived=reviewers=5 attack=21/76 seats=76 staged=81
C1_R55: rev=eba840f7a8ba classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
rc=0
```
`measure.py:227` uses `digest[:8] in corr` (a 9-hex-char non-digest passes) and
`measure.py:264` uses `("staged=%d" % staged) in corr` (a count of 810 passes).

### P3 — a contradictory duplicate inside the section — SURVIVED

```
+The same row was also recorded as `total=12` in the round-54 report.
C1_R55: rev=b67040a4e68f classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
rc=0
```
The counter asks whether the right value is *present*, not whether it is the only
value stated. The section now carries both `total=13` and `total=12` and still
credits.

### P4 — a NEW wrong value outside the section — SURVIVED

```
+The round-54 C2 counter printed `total=12` at its deciding revision.   (inserted above the heading)
C1_R55: rev=1da4994102bd classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
rc=0
```
The stale arm is a **closed token list** (`measure.py:200,212,220,262`:
`CTL_POS_c1 true`, `7883e0e5|fe70474d`, `total=14`, `84 staged`, plus the
`rekeyed=7/7`+`positive control` span patterns). A falsehood phrased with a token
the list does not contain is invisible, even in the record set the claim names
(`SCORECARD.md` outside corrections).

**Mechanism summary:** the corrected arm is `in` (P1/P2/P3-type misses) and the
stale arm is a fixed grep list (P4-type misses). The section is scored as
"contains the right tokens" rather than "equals the derived fact". A repair would
be equality on the derived value plus a stale sweep keyed on the *values* the
receipts contradict, not on the literals round 54 happened to print — but that is
a contract change, not something this seat may make.

## Restoration evidence

Mutations lived only in disposable `git clone --shared` copies under
`$S`; no lane file was written. Each clone was reset to C0 afterwards; the C0 blob
of `SCORECARD.md` is `54faed3847839e90ac84ae378c96d3b9fdc4f393`,
sha256 `22b9fffd0109b5490a432c91970279c8438204b6618fafd3ef22dda8959c75ce`.

| clone | mutated rev | blob after mutation | sha256 after mutation | restored to | `git diff C0` lines |
|---|---|---|---|---|---|
| mutA | 85b040b16aea | 0dadfba2de40 | f6dbaae871cc | 9cf0146b94dd | 0 |
| mutB | 525b167eec8c | 2a8633babede | a2bc7b4d63b9 | 9cf0146b94dd | 0 |
| mutC | 25b1608adf0e | b1912535cb2f | 80b6312c915a | 9cf0146b94dd | 0 |
| mutP1 | 6bebed7523da | 36b63a638b33 | a574c7a1d61d | 9cf0146b94dd | 0 |
| mutP2 | eba840f7a8ba | f308366f3749 | 23c804717b5a | 9cf0146b94dd | 0 |
| mutP3 | b67040a4e68f | 14fe8e546656 | 4bc3a33ddd01 | 9cf0146b94dd | 0 |
| mutP4 | 1da4994102bd | 09d28d692434 | d64314c65304 | 9cf0146b94dd | 0 |

Post-restore `sha256sum $S/mut*/SCORECARD.md` on all seven clones:
`22b9fffd0109b5490a432c91970279c8438204b6618fafd3ef22dda8959c75ce` (== C0).

Lane verification (before and after, unchanged):

```
22b9fffd…c75ce  SCORECARD.md                    (== C0 blob)
b4e6eabb…e576a  corpus/QUALITY.md
10068fb8…2e74a  corpus/lessons/round-54.md
4482f48a…b66d1  LOG.md
git status --porcelain -- <those four files>   -> empty
```

Frozen files were never written: `.ufo/evidence/round-55/*` is read-only for this
seat; the counter was executed from the lane path, not copied or edited.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
-> `rc=0` (ends `tameshi ok …/corpus/SOURCES.md`).

No tool was installed or upgraded for this seat (Python 3 + git only).

## Artifacts opened

- `.ufo/evidence/round-55/c1/measure.py` (all 325 lines; cited `33, 67, 83, 200,
  212, 220-222, 227-228, 262-265`)
- `.ufo/evidence/round-55/contract.json` (C1 claim, frozen paths, amendments 1-8)
- `.ufo/evidence/round-55/before/c1.stdout` (base failure at `0a2010ac`)
- `.ufo/evidence/round-55/c1/staged-at-freeze.txt`
- `SCORECARD.md` at C0 (`git show 9cf0146b94dd:SCORECARD.md`), lines 2615-2702
- `.ufo/waves/round-55/w2/` (existing seat outputs, read-only)
- `scripts/sources-census.sh` (executed, output not opened)

## Verdict lines (verbatim, one per required mutation)

```
M1 C1_R55: rev=85b040b16aea classes=10 premise=10/10 stale=0 classes_corrected=9/10 total=1 C1_R55_PASS=false   KILLED
M2 C1_R55: rev=525b167eec8c classes=10 premise=10/10 stale=0 classes_corrected=9/10 total=1 C1_R55_PASS=false   KILLED
M3 C1_R55: rev=25b1608adf0e classes=10 premise=10/10 stale=1 classes_corrected=9/10 total=1 C1_R55_PASS=false   KILLED
```

Counter misses found: P1 (substring `total=130`), P2 (`8528ee850` /
`staged=810`), P3 (contradictory duplicate), P4 (new wrong value outside the
section). All four are presence-only scoring; none is a section defect at C0.
