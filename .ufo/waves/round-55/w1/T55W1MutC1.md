# T55W1MutC1 — mutation probe of the frozen C1 counter (round 55, w1)

Seat: mutation tester, leaf. Item: mutate the frozen C1 counter in scratch copies,
score every mutant at `0a2010ac` (base) and at a tree that reaches `total=0`, and
report KILLED / SURVIVED per mutant. One survivor is the round's finding.

No lane production file was written. No lane git/jj mutation was run. The counter
under test was never edited in the lane; every mutant is a copy in scratch.

## 0. What was under test, and what moved while it ran

The counter's bytes were re-frozen **twice** during this seat's run. I pinned each
byte-set by hash and mutated the final one.

| when | `.ufo/evidence/round-55/c1/measure.py` sha256 | state |
|---|---|---|
| first read (14:00 local) | `77abe1e9daf40bec2c9d7a7c12724e766e2f98d222c287fde6097df819b60783` | committed at freeze `631cd64`, my first mutant set |
| 14:00–14:12 | `711507e7b5bdd060a67b42162d043aabaef339408b3291a3c6ca39599d566dcd` | **uncommitted, unregistered** in the worktree while `freeze.json` still pinned `77abe1e9` |
| final (freeze `e2979f2`, lane `9cf0146`) | `5e8f50d1815309e8c3a1c914191b6032b7dceff27ba42d87a676b3f78e30ac5e` | amendments 1–7 registered; manifest agrees |

Evidence for the middle row, taken at the time:

```
$ sha256sum .ufo/evidence/round-55/c1/measure.py        # 14:00:09
711507e7b5bdd060a67b42162d043aabaef339408b3291a3c6ca39599d566dcd
$ git status --short .ufo/evidence/round-55/c1/measure.py
 M .ufo/evidence/round-55/c1/measure.py
$ git show 631cd64:.ufo/evidence/round-55/c1/measure.py | sha256sum
77abe1e9daf40bec2c9d7a7c12724e766e2f98d222c287fde6097df819b60783
```

That was a frozen path edited after the freeze and before amendment 5 was
registered. It was later rectified by the freeze commit `e2979f2` ("amendments
1-7 — counters re-frozen on the amended bytes"), and at the final state every
manifest entry matches on disk:

```
$ python3 -c "… freeze.json['files'] vs sha256(on disk) …"
OK   .ufo/evidence/round-55/contract.json
OK   .ufo/evidence/round-55/c1/measure.py
OK   .ufo/evidence/round-55/c2/measure.py
OK   .ufo/evidence/round-55/no-harm.sh
OK   .ufo/evidence/round-55/deciding-run.sh
OK   .ufo/evidence/round-55/controls.sh
OK   .ufo/evidence/round-55/c1/staged-at-freeze.txt
```

**Reported, not fixed** (the frozen set is not mine to touch). No counter-external
harm resulted: the seat re-scored everything against `5e8f50d1`.

Every mutant is a single-edit copy of `5e8f50d1`; the earlier `77abe1e9` set is
kept only as provenance (`mutants/frozen-77abe1e9.py`).

## 1. Method

* Detector (identical on pristine, mutated and restored bytes): the counter's own
  verdict, i.e. `(exit code, C1_R55_PASS, total=N, the set of classes named FAIL)`.
* Kill rule: a mutant is **KILLED** only if it deviates from the correct answer on a
  tree where the **pristine** counter gave that correct answer. On a tree where
  pristine itself deviates, a mutant's coincidence is not evidence.
* Trees are `git clone --shared` scratch clones; every `git` call names `-C`, and
  `git -C <clone> rev-parse --show-toplevel` was asserted to equal the clone before
  any commit there. Probe-tree revs: `receipts-c0/../trees.txt`.
* Base revision is the contract's `0a2010acd1e92e4e332774050825e21bcfc7e079`.
  The `total=0` tree is the lane's own content commit **C0 `9cf0146`** (the executors
  had already landed the integration), plus 22 probe trees built around it.

### Mandated two adjudication points

```
$ measure.py --lane <clone at base> --rev 0a2010ac… --work <empty> --explain
C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false   [rc=1]

$ measure.py --lane current --rev 9cf0146… --work <empty> --explain
C1_R55: rev=9cf0146b94dd classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true    [rc=0]
```

Receipts: `receipts-c0/pristine@base.stdout`, `receipts-c0/pristine@C0.stdout`.

## 2. Mutants, scored at base and at `total=0`

18 single-edit mutants (one hunk each; `mutants/N*.diff`). Both mandated points:

| # | mutant (single edit) | base `0a2010ac` | C0 `9cf0146` (`total=0`) | verdict |
|---|---|---|---|---|
| N1 | R54.1 stale scan dropped (`stale = []`) | `total=10` false | `total=0` true | survives the two points — **KILLED** by `m1`, `m15` |
| N2 | R54.3 derived total hardcoded to `"13"` | `total=10` false | `total=0` true | survives the two points — **KILLED** by `m2` |
| N3 | `ok` no longer requires `premise` | `total=10` false | `total=0` true | survives the two points — **KILLED** by `noprem` |
| N4 | corrections block not trimmed at the next `## ` | `total=10` false | `total=0` true | survives the two points — **KILLED** by `tailsec` |
| N5 | record files read from the worktree, not `REV` | `total=10` false | `total=0` true | survives the two points — **KILLED** by `dirty` |
| N6 | R54.8 class deleted from the table | `classes=9 total=9` false | `total=0` true | **KILLED at base** (denominator breaks) |
| N7 | R54.5 corrected arm weakened to `"w1=" in corr` | `total=10` false | `total=0` true | survives the two points — **KILLED** by `m7` |
| N9 | first commit → last commit (`--reverse` dropped) | `total=10` false | `total=0` true | survives the two points — **KILLED** by `m9` |
| N10 | R54.4 digest hardcoded to `8528ee85…` | `total=10` false | `total=0` true | survives the two points — **KILLED** by `m10` |
| N11 | `total` counted from `corrected` only (premise+stale ignored) | `total=10` false | `total=0` true | survives the two points — **KILLED** by `noprem`, `tailsec`, `m1`, `m14`, `m15` |
| N12 | R54.9 staged count hardcoded to `81` (receipt not read) | `total=10` false | `total=0` true | survives the two points — **KILLED** by `m12` |
| N13 | R54.2 freeze pointer hardcoded to `077d431e…` | `total=10` false | `total=0` true | survives the two points — **KILLED** by `m13` |
| N14 | `scan_span` (wrapped-claim) arm dropped | `total=10` false | `total=0` true | survives the two points — **KILLED** by `m14` |
| N15 | `LOG.md` dropped from `RECORD` | `total=10` false | `total=0` true | survives the two points — **KILLED** by `m15` |
| N16 | R54.8 seat arm back to any `superseded` | `total=10` false | `total=0` true | survives the two points — **KILLED** by `m16` |
| N17 | corrections block opened by any `## Round 55` heading | `total=10` false | `total=0` true | **SURVIVED** (equivalent-or-stricter, §3) |
| N18 | corrections block no longer excluded from `scan` | `total=10` false | **`stale=3 total=3` false** | **KILLED at C0** |
| N19 | corrections block no longer excluded from `scan_span` | `total=10` false | **`stale=1 total=1` false** | **KILLED at C0** |

Verdict lines for the kills (each from `receipts-c0/<mutant>@<tree>.stdout`):

```
N6  @base   C1_R55: rev=0a2010acd1e9 classes=9 premise=8/9 stale=4 classes_corrected=0/9 total=9 C1_R55_PASS=false
N18 @C0     C1_R55: rev=9cf0146b94dd stale=3 total=3 C1_R55_PASS=false
N19 @C0     C1_R55: rev=9cf0146b94dd stale=1 total=1 C1_R55_PASS=false
N5  @dirty  C1_R55: rev=631cd6455e58 stale=0 total=0 C1_R55_PASS=true      (pristine here: total=10 false)
N3  @noprem C1_R55: rev=992334bb254f premise=9/10 stale=0 total=0 C1_R55_PASS=true   (pristine: total=1 false)
N4  @tailsec C1_R55: rev=b5e06d548871 stale=0 total=0 C1_R55_PASS=true     (pristine: total=3 false)
N1  @m1     C1_R55: rev=c9a11a891c15 stale=0 total=0 C1_R55_PASS=true      (pristine: total=1 false)
N2  @m2     C1_R55: rev=f7295096fe4d stale=0 classes_corrected=9/10 total=1 C1_R55_PASS=false (pristine: total=0 true)
N7  @m7     C1_R55: rev=24d45bf89826 stale=0 total=0 C1_R55_PASS=true      (pristine: total=1 false)
N9  @m9     C1_R55: rev=218fa021ad47 stale=0 classes_corrected=9/10 total=1 C1_R55_PASS=false (pristine: total=0 true)
N10 @m10    C1_R55: rev=a310908fdc1f stale=0 classes_corrected=9/10 total=1 C1_R55_PASS=false (pristine: total=0 true)
N12 @m12    C1_R55: rev=6a8b4342539d stale=0 classes_corrected=9/10 total=1 C1_R55_PASS=false (pristine: total=0 true)
N13 @m13    C1_R55: rev=678311c6dbff stale=0 classes_corrected=9/10 total=1 C1_R55_PASS=false (pristine: total=0 true)
N14 @m14    C1_R55: rev=6924c69523fa stale=0 total=0 C1_R55_PASS=true      (pristine: total=1 false)
N15 @m15    C1_R55: rev=5fb4cdbfdc76 stale=0 total=0 C1_R55_PASS=true      (pristine: total=1 false)
N16 @m16    C1_R55: rev=56773046f302 stale=0 total=0 C1_R55_PASS=true      (pristine: total=1 false)
N11 @noprem C1_R55: rev=992334bb254f premise=9/10 stale=0 total=0 C1_R55_PASS=true   (pristine: total=1 false)
```

Full matrix (17 sound trees + 7 blind, 18 mutants + pristine): `matrix-c0.md`,
`matrix-c0.json`. Tally: **KILLED 17 / SURVIVED 1**.

**How much of that depends on purpose-built probes.** On the two adjudication
points the round actually mandates — base and C0 — **15 of 18 mutants are
indistinguishable from the pristine counter**; only N6, N18 and N19 die there.
The other 14 kills come from probe trees I built to exercise the arm, which is the
normal circularity of hand-targeted mutation testing and is why the probe-tree
construction is reproduced in `build_trees.sh` and every verdict is a receipt.

## 3. The survivor: N17 (equivalent-or-stricter, not exploitable)

Edit: `if line.startswith(HEADING)` → `if line.startswith("## Round 55")`, i.e. the
corrections block opens at *any* `## Round 55` heading instead of the exact one.

* Verdict-identical to pristine on **all 17 sound trees** (full stdout identical on
  16 of them; only `tailsec` differs, and there the aggregate is the same:
  `stale=3 total=3` both, with different per-class attribution).
* On a tree built to expose it (`head55`: a `## Round 55 - wave 1 record` block
  placed *before* the corrections section, quoting `CTL_POS_c1 true` / `total=14`),
  the mutant is **stricter**, not weaker: `total=3` vs pristine `total=2`, because
  moving the block start forward stops the corrections section from being excluded,
  so its own `Old: …` erratum quotes become stale hits.
* Structurally the mutation can only ever be stricter or equal: the corrections
  section exists to quote the old values, so any block-boundary error that stops
  excluding it adds hits rather than removing them.

So this survivor **cannot produce a false pass** on any tree shape where the
corrections section quotes the values it corrects — which is the shape the round
requires. Reported as a survivor with that equivalence argument rather than
counted as a kill.

## 4. Findings — the counter passes records that still carry the wrong assertion

Seven trees where the **pristine** frozen counter prints `total=0 C1_R55_PASS=true`
while a wrong assertion the routed defect names is present **outside** the
corrections section. These are false negatives of arm (b) of the contract's target
("zero stale occurrences of the wrong assertion OUTSIDE the corrections section"),
and they are the substantive result of this seat.

Root cause, from the source: only four classes scan for a stale assertion at all;
the other six pass `[]`:

```
$ sed -n '/^def classes/,/^    return rows/p' measure.py | grep -n "stale = \|scan("
15:    stale = scan(lane, rev, RECORD, r"CTL_POS_c1 true")                                  # R54.1
16:    stale += scan(lane, rev, ("corpus/QUALITY.md", "corpus/lessons/round-54.md"), …)    # R54.1
27:    stale = scan(lane, rev, ("SCORECARD.md",), r"7883e0e5|fe70474d")                    # R54.2
35:    stale = scan(lane, rev, ("SCORECARD.md",), r"total=14")                             # R54.3
77:    stale = scan(lane, rev, ("corpus/lessons/round-54.md",), r"84 staged")              # R54.9
```

R54.4, R54.5, R54.6, R54.7, R54.8 and R54.10 are scored with `stale=[]`.

### F1 — five of ten classes' in-place repair is unverified (no probe needed)

The executor's own control shape — corrections section present, in-place fixes
reverted — and the counter still passes five classes:

```
$ measure.py --lane corronly2 --rev 871f8d93d23a --work <empty> --explain
EXPLAIN R54.1 FAIL …   EXPLAIN R54.2 FAIL …   EXPLAIN R54.3 FAIL …
EXPLAIN R54.4 ok premise=ok corrected=ok stale=0 derived=c2 digest=8528ee85
EXPLAIN R54.5 ok premise=ok corrected=ok stale=0 derived=w1=28 w2=25 sections=12
EXPLAIN R54.6 ok premise=ok corrected=ok stale=0 derived=sweep commit=ff2a821
EXPLAIN R54.7 ok premise=ok corrected=ok stale=0 derived=rename commit=7fa9a5e
EXPLAIN R54.8 FAIL premise=ok corrected=miss stale=0 …
EXPLAIN R54.9 FAIL …   EXPLAIN R54.10 ok premise=ok corrected=ok stale=0 derived=controls-a rekeyed=0/7
C1_R55: rev=871f8d93d23a classes=10 premise=10/10 stale=4 classes_corrected=9/10 total=5 C1_R55_PASS=false
```

Reverting the in-place repairs of R54.4, R54.5, R54.6, R54.7 and R54.10 costs
nothing. `receipts-c0/pristine@corronly.stdout`.

### F2 — R54.2's stale arm is an enumerating regex that omits the third pointer

ER-R54-2 names three wrong pointers (`7883e0e5`, `fe70474d`, `097985c1`); the arm
searches only the first two. With `097985c1` re-asserted outside the corrections
block:

```
$ measure.py --lane f1b2 --rev 72089fa75134 --work <empty> --explain
EXPLAIN R54.2 ok premise=ok corrected=ok stale=0 derived=freeze pointer=077d431e
C1_R55: rev=72089fa75134 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

`git -C f1b2 diff HEAD~1 HEAD -- SCORECARD.md` → `+Probe: the fleet report named
freeze \`097985c1\` for this round.` (inserted *before* the corrections heading).
Receipt `receipts-c0/blindspot-f1b2.stdout`.

### F3 — R54.3's stale arm is the single literal `total=14`

Any other wrong total passes:

```
$ measure.py --lane f2b2 --rev 15f0ee79d8bb --work <empty> --explain
C1_R55: rev=15f0ee79d8bb classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

`f2b2` rewrites the C2 claim row (before the corrections heading) to
`sources=0 total=16`. Receipt `receipts-c0/blindspot-f2b2.stdout`.

### F4 — R54.1's token is case-sensitive

```
$ measure.py --lane f3b2 --rev b8fd7dd8241d --work <empty> --explain
C1_R55: rev=b8fd7dd8241d classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

`f3b2` appends `Probe: ctl_pos_c1 true is asserted again, in lower case.` to
`corpus/QUALITY.md`. Receipt `receipts-c0/blindspot-f3b2.stdout`.

### F5 — R54.4 has no stale arm; the old digest can be re-asserted

```
$ measure.py --lane p7b --rev 136fdf2c6a5b --work <empty> --explain
C1_R55: rev=136fdf2c6a5b classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

`p7b` inserts `Probe: the deciding c2 counter was \`49280fe5\`.` before the
corrections heading — the exact value ER-R54-4 calls stale.
Receipt `receipts-c0/blindspot-p7b.stdout`.

### F6 — R54.9's stale arm is the single literal `84 staged`

```
$ measure.py --lane p9b --rev 68caf1b3cb70 --work <empty> --explain
C1_R55: rev=68caf1b3cb70 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

`p9b` appends `Probe: the other 86 staged entries were refused.` to
`corpus/lessons/round-54.md`. Receipt `receipts-c0/blindspot-p9b.stdout`.

### F7 — R54.5 and R54.10 have no stale arm either

```
$ measure.py --lane p5b  --rev d94a25fc04e0 --work <empty> --explain
C1_R55: rev=d94a25fc04e0 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
$ measure.py --lane p10b --rev 189fcd8a3007 --work <empty> --explain
C1_R55: rev=189fcd8a3007 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

`p5b` re-asserts the old finding counts (`22 wave-1 findings across 9 sections`);
`p10b` re-asserts `58/64, rekeyed=0/30` as the phase-A quote. Receipts
`blindspot-p5b.stdout`, `blindspot-p10b.stdout`.

**Counter-check that the arms which exist do work** — the same construction on a
class whose stale arm does exist is caught:

```
$ # p8b: the corrections section loses the word "fabricated"
C1_R55: … total=1 C1_R55_PASS=false        (receipts-c0/pristine@p8.stdout)
$ # m1/m14/m15/m16 (trees that only the R54.1 arms can see): pristine total=1, false
```

### What this means for C1

The counter is a sound *derivation* check: all thirteen derivation mutants (N2, N5,
N9, N10, N12, N13 and the corrected-arm weakenings N7, N3, N11…) are killed, and
`total=0` cannot be reached by hardcoding, by reading the worktree, by taking the
last instead of the first commit, or by dropping the corrections exclusion (N18,
N19 fail at C0). What it does **not** do is what arm (b) of its own contract asks:
6 of 10 classes have no stale arm, and the 4 that do search fixed literals, so a
re-stated falsehood in slightly different words/hex/case still scores `total=0`.
The round's C1 target ("zero stale occurrences of the wrong assertion outside the
corrections section") is therefore certified for 4 literal families, not for the
ten routed defects.

## 5. Restoration evidence

Scratch copy mutated, run, restored from the recorded bytes, re-run:

```
before=77abe1e9daf40bec2c9d7a7c12724e766e2f98d222c287fde6097df819b60783
mutated=548595060d6633ea29d4b057f45014ffefd82230c7f5705be4c380f21977e086
mutated-run: C1_R55: rev=0a2010acd1e9 classes=10 premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
after=77abe1e9daf40bec2c9d7a7c12724e766e2f98d222c287fde6097df819b60783
RESTORE-EXACT: bytes identical
restored-run: C1_R55: rev=0a2010acd1e9 classes=10 premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
```

(The demo used the first-revision bytes and its matching base receipt; the final
byte-set `5e8f50d1` is preserved unmodified at
`receipts-c0/mutants/frozen-current-5e8f50d1.py` and every run above used exactly
those bytes.)

The lane copy of the counter was never written by this seat: I only ever read it
(`cp` out) and the mutants are separate files.

## 6. Conformance

* Lane production files (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`,
  `tools/**`, `.ufo/evidence/**`) untouched by this seat.
* No mutating git/jj command in the lane; every clone/fixture commit names `-C`
  after asserting its `--show-toplevel`.
* Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → exit 0 (tail: `tameshi ok
  …/corpus/SOURCES.md`, W04 duplicate-url warnings only).
* No tool install or upgrade this round; nothing added to any PATH directory.

## 7. Artifacts

* `T55W1MutC1-receipts/mutants/` — the counter byte-sets (`frozen-current-5e8f50d1.py`,
  `frozen-77abe1e9.py`), the 18 mutants and their one-hunk diffs, `manifest-c0.txt`.
* `T55W1MutC1-receipts/matrix-c0.md` / `.json` — the full 18 × 24 matrix, with the
  per-mutant kill set and the sound/blind tree split.
* `T55W1MutC1-receipts/runs/` — every `--explain` stdout, one file per
  `<counter>@<tree>` (456 files), plus the seven `blindspot-*.stdout` receipts.
* `T55W1MutC1-receipts/trees.txt` — probe-tree revs.
* `T55W1MutC1-receipts/build_trees.sh`, `score_final_c0.py` — exact reproduction.
* `T55W1MutC1.json` — machine-readable matrix summary.
