# T55W1RevQuality — attack on QUALITY 105/106 (calibration)

Seat `T55W1RevQuality`, round 55 wave 1. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
(`$LANE` below). Base `0a2010ac`, counter freeze `631cd645`. I edited no lane production file;
the only lane writes are this report and `T55W1RevQuality-receipts/`. Scratch:
`/fast/scratch/hyaku/tameshi-r55/T55W1RevQuality`. No tool installed or upgraded (nothing was
needed; `pacman` untouched).

## The two questions, answered from the receipts

**Q1 — does criterion 105's claimed falsifier actually fail on
`.ufo/evidence/round-54/control/controls-b.stdout`?**

Yes, and it fails as a *factual claim about that receipt*, not as a check that needs
tightening. 105 landed (QUALITY.md:1590 at base) saying:

> while the round-54 counter's arm prints `rekeyed=7/7` **on its positive control**; the two
> receipts are … `.ufo/evidence/round-54/control/controls-b.stdout` (**the round-54 positive
> control**)

The named receipt prints `rekeyed=3/7` and `CTL_MISMATCH CTL_POS_c1 expected=true actual=false`
(`CONTROLS_B: 2/3`, exit 1). `grep -c 'rekeyed=7/7'` on it returns **0**. So the sentence 105
uses to identify its bad state is false about its own receipt: **105 needs an erratum**, not a
clarification. 105's *rule* ("an arm is proven only on a control where it must fire") is not
withdrawn — the failure is that the receipt which refutes the claim was cited as the proof.

Commands and output (`T55W1RevQuality-receipts/01-c105-falsifier.stdout`,
`01b-c105-greps.stdout`):

```
$ python3 c105-falsifier.py            # reads 105 from 0a2010ac, then the named receipt
FALSIFIER-TEXT (landed at 0a2010acd1e9): Falsifier that must fail: the round-53 C1 counter's rekey
arm prints `rekeyed=0/30` at its own final content revision `88afa941` (the pathspec …) , while the
round-54 counter's arm prints `rekeyed=7/7` on its positive control; the two receipts are
…/r53-counter-at-88afa941.stdout … and …/controls-b.stdout (the round-54 positive control) …
CLAIM full-count-on-control=True names-controls-b-as-positive=True
RECEIPT line: CTL CTL_POS_c1 C1_R54: rev=077d431e6996 … rekeyed=3/7 … total=4 C1_R54_PASS=false
RECEIPT rekeyed-now=3/7 expectation=false mismatched(expected=true actual=false)
CLAIM-HOLDS full-count-present=False
ARM1 zero-count-fires=False (rekeyed=3)
ARM2 preregistered-without-tree-fires=True (re-key ancestor of control rev=False)
C105-FALSIFIER: full-count-claim=False check-fires=True -> FALSIFIER FAILS as landed
EXIT=1

$ grep -c 'rekeyed=7/7' .ufo/evidence/round-54/control/controls-b.stdout
0
$ cat .ufo/evidence/round-54/control/controls-b.exit
1
```

The falsifier's *other* half verifies: `r53-counter-at-88afa941.stdout` prints
`rekeyed=0/30` at `88afa941`, and `git ls-tree --name-only 88afa941 .ufo/evidence/round-21/coldread`
returns the directory itself.

Is 105 "merely imprecise" as well? Partly, and separately. Its check has two arms, and arm 2 —
"a control run that pre-registers the arm's value **without a tree that carries it**" — names no
derivation for "carries it": the receipt carries only `rev=`, and nothing in 105 says what makes a
tree carry the round's work. My scorer had to import the re-key commit (`7fa9a5e`) from the record
to fire arm 2 (`git merge-base --is-ancestor 7fa9a5e 077d431e` → rc 1, i.e. the freeze predates the
re-key). That is the imprecision the drafted **106 repairs mechanically**: 106's `rev` arm requires
the control's own `rev=` to resolve to the certified revision, which is a checkable form of "a tree
that carries it". So: **105 needs an erratum for the falsifier sentence; 105's check needs 106's
rev arm to be executable; the erratum should say both.**

**Q2 — does 106's falsifier fail on `controls-b.stdout` and pass on a re-scored control?**

Both confirmed, and the positive arm was re-run by me from the frozen bytes rather than accepted
from the draft (`02-c106-fail-at-base.stdout`, `11-c106-positive-mine.stdout`):

```
$ c106-controls.py --lane $LANE --rev 0a2010ac --certifies c21081008adb \
    --control CTL_POS_c1=.ufo/evidence/round-54/control/controls-b.stdout \
    --expect CTL_POS_c1=true --record SCORECARD.md --record corpus/lessons/round-54.md
FAIL CTL_POS_c1 rev scored_at=077d431e6996 certifies=c21081008adb
FAIL CTL_POS_c1 verdict line=C1_R54_PASS=false expected=true
FAIL CTL_POS_c1 paraphrase SCORECARD.md+294678 bare `true` receipt=false
FAIL CTL_POS_c1 paraphrase corpus/lessons/round-54.md+4354 rekeyed=7/7 receipt=rekeyed=3/7
FAIL CTL_POS_c1 paraphrase corpus/lessons/round-54.md+5819 rekeyed=7/7 receipt=rekeyed=3/7
FAIL CTL_POS_c1 quote NOT_QUOTED in any --record: CTL CTL_POS_c1 C1_R54: rev=077d431e6996 … monitor=6/6
C106: controls=1 pass=0 fail=1
EXIT=1                                  # byte-identical to the retained c106-fail.stdout

$ bash …/T55W1ScribeQuality-receipts/rescore-positive.sh $LANE 077d431e c21081008adb
RESCORE counter=.ufo/evidence/round-54/c1/measure.py at=e96da3547e3d sha256=d7749f84…
RESCORE lane=… freeze=077d431e… rev=c21081008adb…
RESCORE counter-exit=0
CTL CTL_POS_c1 C1_R54: rev=c21081008adb c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7
  readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
CONTROLS_B: 1/1 as pre-registered
EXIT=0
```

My independent run (script sha256 `169d74bc…`, 202 s) reproduces the retained
`c106-pass.stdout` line for line. Disclosure: when I first read that receipt at 13:59:24 it held
only the two `RESCORE` header lines (294 B); the scribe's re-run at 14:00:28 completed it (499 B).
The receipt 106 cites is now complete and is corroborated, not merely asserted.

106's rule is also not a restatement of a landed criterion by the letter, but see F5.

## Findings

### F1 (calibration, must fix before the content commit) — the in-place rewrite of 105 is forced by the frozen C1 counter and collides with criterion 35 / admission bar 4

The round integrates 105's falsifier by **rewriting the landed line in place**
(`git diff 0a2010ac -- corpus/QUALITY.md` → `1 1`, one deletion), and the corrections section says
"the same corrections were applied in place above". That deletion is not discretionary: C1's R54.1
stale arm scans `corpus/QUALITY.md` for `(positive control … rekeyed=7/7)|(rekeyed=7/7 … positive
control)` and excludes **only** the SCORECARD corrections section, so the landed bytes must go
(`03-c1-base-explain.stdout`: `stale: corpus/QUALITY.md:1590 …`).

An append-only correction cannot satisfy it — demonstrated, not argued. Fixture clone at base,
erratum appended with **zero deleted lines** (`04a-append-only-numstat.stdout`: `9 0`):

```
$ python3 .ufo/evidence/round-55/c1/measure.py --lane clone --rev 0b724b0a --work … --explain
EXPLAIN R54.1 FAIL premise=ok corrected=miss stale=4 derived=CTL_MISMATCH + 2/3
EXPLAIN R54.1 stale: SCORECARD.md:2583: … `CTL_POS_c1 true` …
EXPLAIN R54.1 stale: corpus/QUALITY.md:1590: Falsifier that must fail: …
EXPLAIN R54.1 stale: corpus/QUALITY.md:1595: `rekeyed=7/7` on its positive control; the receipt it names
EXPLAIN R54.1 stale: corpus/lessons/round-54.md:101: proven live by the positive control …
C1_R55: … stale=4 … total=10 C1_R55_PASS=false
```

The erratum's own verbatim quote of the false text **adds** a stale hit (1595). So criterion 35's
"the named erratum must exist in the file under its own dated heading" and C1's stale arm are
mutually unsatisfiable: name the false text in QUALITY.md and the counter counts it stale; do not
name it and the erratum does not "name the false text". This is a defect of the **frozen counter
(reported, not fixed)**, and the round must dispose it explicitly rather than ship a silent
`1 1` against criterion 35:

- name criterion 35 in the erratum, state that the change is `1 1` by necessity, and record that
  criterion 35's in-place clause is narrowed for this class (old bytes preserved in SCORECARD's
  corrections section, which C1 excludes);
- precedent to cite: round 54's `8da3539` rewrote the same falsifier in place with the same
  `1 1` numstat and no erratum at all (`08-criterion35-numstat-and-precedent.stdout`). Round 55's
  form is strictly better; it is still a `1 1` under a criterion whose check expects `0`
  deletions, and that must be said.

### F2 (medium, calibration) — 106's paraphrase arm fails the honest record that R54.1 requires

A record carrying **both** scorings of `CTL_POS_c1` — the mis-scored line and the re-scored line,
i.e. exactly what the corrections section must preserve — fails 106's check under *either* control
(`05-c106-both-scorings.stdout`, fixture record `fixture-record.md`):

```
(a) mis-scored receipt vs both-scorings record
FAIL CTL_POS_c1 paraphrase .ufo/fixture/record.md+658 credited=64 receipt=credited=60
FAIL … lost=0 / rekeyed=7/7 / readers=7/7 / monitor=8/64 / total=0          (6 hits, EXIT=1)
(b) re-scored receipt vs the same record
FAIL CTL_POS_c1 paraphrase .ufo/fixture/record.md+4 credited=60 receipt=credited=64
FAIL … lost=4 / rekeyed=3/7 / readers=6/7 / monitor=6/60 / total=4          (6 hits, EXIT=1)
```

So 106 as drafted forbids a single record from carrying both truthfully quoted verdict lines. The
round's own report has to carry both (one to show the defect, one to show the repair), and 106's
own text quotes both readings. The arm cannot distinguish a paraphrase from a verbatim quote of a
*different* scoring of the same control.

**Proposed patch** (`12-c106-paraphrase.patch`, applied copy `c106-controls-patched.py`): treat
verbatim verdict lines as the quote arm's subject and exclude them from paraphrase material.

```diff
 def paraphrases(body, rel, name, keys, verdict):
-    """Restatements of the control after a mention of its name."""
+    """Restatements of the control after a mention of its name.
+
+    Verbatim verdict lines (a line beginning with `CTL <name> `) are the quote
+    arm's subject, not paraphrase material: a record that carries the receipt's
+    line and its re-scored sibling must not be failed for the sibling's values.
+    """
     out = []
-    for m in re.finditer(re.escape(name), body):
-        tail = body[m.end():m.end() + CLAIM_WINDOW]
+    prose = "\n".join(l for l in body.splitlines() if not l.startswith("CTL "))
+    for m in re.finditer(re.escape(name), prose):
+        tail = prose[m.end():m.end() + CLAIM_WINDOW]
```

Demonstration the patch does not weaken the discriminating arm
(`13-c106-patch-demonstration.stdout`): at base the FAIL set is **identical** (rev, verdict, three
prose paraphrases, quote — still exit 1); the both-scorings record passes for the re-scored control
(`OK … C106: controls=1 pass=1 fail=0`, exit 0); and for the mis-scored control it still fails on
`rev` and `verdict` (exit 1), which is correct — that receipt cannot certify `c21081008adb`.

### F3 (low) — 106's positive receipt carries no exit classification

`c106-fail.stdout` has its `c106-fail.exit` (`1`); the positive run has no sibling `.exit` and does
not print its exit. 106 claims the control "passes". My `11-c106-positive-mine.stdout` carries
`EXIT=0` and can serve as the sibling. (Criterion 17's "explicitly classify every nonzero exit" is
satisfied on the red side only.)

### F4 (low, calibration) — the corrections section preserves the false text normalized, not verbatim

SCORECARD says it carries "the old text (preserved here as the erratum)", but ER-R54-1's quote
drops the code-span backticks (`09-corrections-preserved-bytes.stdout`):

```
SCORECARD: (`the round-54 counter's arm prints rekeyed=7/7 on its positive control`);
QUALITY 105 at base:        the round-54 counter's arm prints `rekeyed=7/7` on its positive control
```

Once F1's in-place rewrite lands, the corrections section is the **only** surviving copy of those
bytes, so it should quote them exactly.

### F5 (medium, calibration) — 106 does not cite criterion 86, which already says an
ancestor-measuring receipt certifies nothing

Criterion 86 (`corpus/QUALITY.md:1160-1174`) reads: "A receipt written before C measures an
ancestor and certifies nothing about C". Round 54's phase-B control receipt was written before
C=`c21081008adb` and measures `077d431e`, so 86's sentence already condemns it in spirit; 106's
distinct contribution is mechanical (the control's own `rev=` must equal CERT, the verdict line
quoted verbatim, prose restatements refused). As drafted, 106 reads like a new rule beside a
landed one with no boundary stated. The corpus's own style for this is explicit supersession or an
explicit "extends" clause (criteria 21, 22, 28, 35). Recommend 106 name 86 and say what it adds;
otherwise the corpus gains a near-duplicate and the next reader has to re-derive the boundary.

### F6 (low) — 106's instrument lives under a seat's wave receipts dir

106's check path is `.ufo/waves/round-55/w1/T55W1ScribeQuality-receipts/c106-controls.py`. Every
preceding criterion of this shape cites `.ufo/evidence/round-NN/quality/…` (100, 103, 104 and the
round-47/48 instruments). A landed criterion should not depend on one seat's receipts directory,
even though criterion 100 makes it append-only. Move the instrument and its two receipts to
`.ufo/evidence/round-55/quality/` and point 106 at them.

Also: the instrument has no `--selftest`/falsifier entry point that prints an OK line of its own
(cf. criterion 100's `c100-falsifier.py` → `CRITERION-100-FALSIFIER-OK`). The two receipts are a
good base for one; the round should wrap them.

### F7 (observed, not a finding against the round) — 106's "four record files" is four *places*,
one of which is fleet-side

R54.1 names report `:162`, `SCORECARD.md:2583`, `QUALITY.md:1590`, `lessons/round-54.md:74,101`.
C1's `RECORD` set is `SCORECARD.md, corpus/QUALITY.md, corpus/lessons/round-54.md, LOG.md`, so it
can see three. The fourth is `.ufo/reports/round-54/tameshi.md:162` — "proven live by the phase-B
positive control" — which **still stands** and is outside the lane
(`14-fleet-and-premise-counts.stdout`). ER-R54-1 corrects the three lane files and does not name
this one; ER-R54-9 shows the form (name the fleet file, route the substitution). Without that
sentence, C1's `stale=0` reads as "no stale occurrence anywhere", which is not what it measures.

### F8 (low, adjacent) — the premise file's own count says nine while ten are filed

`corpus/lessons/round-54-verifier-spotcheck.md:11` says "nine routed record/instrument defects" and
`:247` says "R54.1–R54.9 as filed above are unaffected by this pass", but R54.10 is filed at `:233`
and the round-55 contract cites "the ten routed defects … R54.1-R54.10". Same class as R54.3/R54.5
(a count that does not match the artifact). The round's corrections section does not record it.
Cheap to add as an appended item in the section or a row in the lesson.

## Residual risk and verification gaps

- F1 is the calibration risk that matters: the round ships a `1 1` numstat over `corpus/QUALITY.md`
  while criterion 35's check expects zero deletions for an erratum-only change. I did **not**
  edit `QUALITY.md`, `SCORECARD.md` or the frozen counters; the disposition wording is the L1's.
- I did not verify 106's paraphrase arm against every record file the round will land (only
  `SCORECARD.md`, `corpus/lessons/round-54.md`, `corpus/QUALITY.md`, and one fixture). The
  window-layout sensitivity (120 chars) is disclosed in 106's text but makes a prose restatement
  pass or fail by distance, not content; F2's patch removes that sensitivity for quoted lines only.
- The `rescore-positive.sh` I ran is the scribe's current bytes (sha256 `169d74bc…`). The retained
  `c106-pass.stdout` was still being written when I first read it; it is complete now and agrees.
- Criterion 105's arm 1 (zero-count) cannot fire on the round-54 receipt (3/7), so 105's
  discrimination rests entirely on arm 2 and its unstated derivation — see Q1.
- Census at my run: `scripts/sources-census.sh validate --root … tameshi` exit 0
  (`10-census.stdout`), matching the round's start/end conformance expectation.

## Receipts (all under `.ufo/waves/round-55/w1/T55W1RevQuality-receipts/`)

| file | what it shows |
|---|---|
| `01-c105-falsifier.stdout`, `c105-falsifier.py` | 105's falsifier scored against its named receipt; claim false, check fires |
| `01b-c105-greps.stdout` | `rekeyed=7/7` count 0; the 3/7 line; exit 1 |
| `02-c106-fail-at-base.stdout` | 106 red at base, identical to the retained receipt |
| `03-c1-base-explain.stdout` | frozen C1 at base; R54.1 stale hits incl. `QUALITY.md:1590` |
| `04a-append-only-numstat.stdout`, `04b-append-only-c1.stdout` | append-only erratum `9 0`; still stale=4 |
| `05-c106-both-scorings.stdout`, `fixture-record.md`, `fixture-rescored.stdout` | paraphrase arm fails both scorings (6 hits each) |
| `06-c106-over-own-block.stdout` | 106's own block over `QUALITY.md` (no paraphrase hit; window-dependent) |
| `07-ancestry-and-certified-line.stdout` | `077d431e` ancestor of `7fa9a5e`, not the reverse; the certified line |
| `08-criterion35-numstat-and-precedent.stdout` | round-55 `1 1`; round-54 `8da3539` `1 1` |
| `09-corrections-preserved-bytes.stdout` | preserved old text vs base bytes (backticks) |
| `10-census.stdout` | census validate exit 0 |
| `11-c106-positive-mine.stdout` | independent re-score: exit 0, the certified line, `CONTROLS_B: 1/1` |
| `12-c106-paraphrase.patch`, `c106-controls-patched.py` | the proposed paraphrase patch |
| `13-c106-patch-demonstration.stdout` | patched: base unchanged red, both-scorings green, mis-scored still red |
| `14-fleet-and-premise-counts.stdout` | fleet report `:162`; "nine" vs ten filed |

## Verdict

- **105 needs an erratum** (its falsifier asserts a fact its own receipt refutes) **and** an
  acknowledged imprecision (arm 2's "tree that carries it" has no derivation; 106's `rev` arm
  supplies one). Land the erratum append-only, name criterion 35 and the forced `1 1`, and do not
  let the in-place rewrite stand as an undisclosed violation.
- **106's falsifier is sound**: red at base, green on the re-scored control, both reproduced.
  Before it lands, take F2's patch (or an equivalent scoping), cite criterion 86 (F5), move the
  instrument to `.ufo/evidence/round-55/quality/` (F6), and add the positive run's exit (F3).
