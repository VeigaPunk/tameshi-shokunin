# T55W2RevMistakes — are the two `## Mistakes` entries in `corpus/lessons/round-55.md` real?

Seat: T55W2RevMistakes (wave 2, attack lane). Target: the two entries under
`## Mistakes` in `corpus/lessons/round-55.md` at
`9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (C0). Everything below is measured on
`git clone --shared` copies in scratch; no lane production file, no frozen file and no
wave spec was touched. Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W2RevMistakes`
(removed at the end of the run).

Receipts: `.ufo/waves/round-55/w2/T55W2RevMistakes-receipts/` (r1..r15, named per
finding below). Lane invariants checked while I worked: census
`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ `ok ... tameshi`, `CENSUS_EXIT=0`.

## Verdict

| # | entry | evidence pointer real? | class supported by its own evidence? | fix | can the fix fail? |
|---|---|---|---|---|---|
| 1 | a control scored at a revision that predates the work it certifies | **yes** — receipt, ancestry, and all four records re-read | **yes**, but the `captured-by` clause misdescribes the harness (F2) | record binding is real and falsifiable; the two harness clauses are carried-over behaviour, not changes (F2); the cited `QUALITY 106` **does not exist** (F1) | **yes** — demonstrated (r3) |
| 2 | a predicate that counted a document as not stating a rule when a line break split it | **yes for the SKILL arm** (first-hand at C0, r4); **no for the note arm** — that was a mislabelled mode id, not a wrap (F4) | **partially** — one class, two causes | real: pre-amendment `9d076812` reads `note=7/8 skill=0/1`, frozen `36ca47d3` reads `9/9`, `1/1` (r4, r5, r8) | **yes** — demonstrated (r5) — **but the frozen counter cannot convert the repaired arm into a PASS at all** (F3) |

An entry whose `captured-by` names no committed artifact is prose; entry 2's
`captured-by` is prose (F5). Entry 1's `captured-by: none — ...` is honest and correct.

---

## F1 (high) — entry 1's fix cites `QUALITY 106`, which is not in the tree

Entry 1's fix ends: *"QUALITY 106 states the rule and its falsifier is that same
receipt."* `corpus/QUALITY.md` at C0 ends at criterion 105.

```
$ git show 9cf0146:corpus/QUALITY.md | grep -oE "Criterion 1[0-9]{2}" | sort -u | tail -4
Criterion 102
Criterion 103
Criterion 104
Criterion 105
$ git grep -n "Criterion 106\|criterion 106" 9cf0146 -- .
9cf0146:.ufo/waves/round-54/w1/T54W1ScribeQuality.md:132:### Criterion 106 — ...
9cf0146:.ufo/waves/round-55/w1/T55W1ScribeConsiderthese.md:167:### 5a. Primary: QUALITY criterion 106 (append after 105)
   (only wave drafts and dispatch text; nothing in corpus/QUALITY.md)
```

The same absent artifact is asserted twice more at C0: `corpus/lessons/round-55.md`
("criterion 106 is appended") and `LOG.md:2545-2546` ("QUALITY 106 (a control is scored
at the revision it certifies) with an erratum on 105"). The 105 erratum **is** present
(the falsifier now reads "the control never fired; [ER-R54-1]").

Why it matters: this is the class the round's C1 claim exists to remove — a record
asserting a landed artifact the tree does not carry. It is invisible to C1: the counter's
record set is `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-54.md`, `LOG.md`
(`c1/measure.py:34-39`); the round-55 lesson is not scanned, and the LOG/QUALITY scan
looks only for the R54.1..R54.10 stale values. Recommendation: land 106 from the wave
draft, or withdraw the three sentences; and add `corpus/lessons/round-55.md` to `RECORD`.

*Post-C0 status:* criterion 106 was landed later — `corpus/QUALITY.md:1592` at lane HEAD
("### Criterion 106 — a pre-registered control is scored at the revision it certifies",
commit `4c04c1d`). At C0, the revision this seat reviews, the three sentences above were
false and C0's erratum-only 105 was the only landed part.

## F2 (medium) — entry 1's `fix` and `captured-by` misdescribe *where* the repair is

The claim: *"round 55's `controls.sh` phase B clones the revision it certifies and its
`deciding-run.sh` gate refuses any control receipt not descending from the freeze."*
Both are true at C0 — and both were already true in the round that carried the defect:

```
$ git show 077d431:.ufo/evidence/round-54/control/controls.sh | sed -n '141,146p'
  # CTL_POS — the real repair at REV must pass both counters.
  d=$(clone_at "$LANE" "$REV" pos) || exit 2
  ... echo "CTL CTL_POS_c1 $(tail -1 "$SCR/cposa")"; check CTL_POS_c1 true "$v"
$ diff -u <r54 controls.sh> <r55 controls.sh>   →  r11-controls-sh-r54-vs-r55.diff
-  # CTL_POS — the real repair at REV must pass both counters.
+  # CTL_POS -- the real repair AT THE REVISION IT CERTIFIES must pass both counters.
-  echo "CTL CTL_POS_c1 $(tail -1 "$SCR/cposa")"; ...
+  echo "CTL CTL_POS_c1 $(tail -1 "$SCR/cposa.out")"; ...
```

Phase B cloned `"$REV"` in round 54 as well; round 54's harness already printed
`CTL_MISMATCH ... expected=true actual=false` and exited 1 (`.ufo/evidence/round-54/control/controls-b.stdout`,
whose own line I re-read: `CONTROLS_B: 2/3 as pre-registered`). The `deciding-run.sh`
`merge-base --is-ancestor` line is also identical at `077d431` (line 55). So the two
named mechanisms are comment/cosmetic on the clone line, and cannot be what repaired
the class.

The operative repair is real and is **not** what the entry credits: C1's `R54.1` arm
binds the corrections section to the receipt's own tokens
(`c1/measure.py:196-206`: `premise = "CTL_MISMATCH" in cb and "CONTROLS_B: 2/3" in cb`;
`corrected = "CTL_MISMATCH" in corr and "2/3" in corr`). That is falsifiable — see
"Falsifier 1".

`captured-by: none — the phase-B harness had no arm requiring that its clone match the
revision it scores` is also imprecise: the harness *did* clone exactly the `REV` it
scored (`--rev $(git rev-parse HEAD)` of that clone, r11 diff). What no arm required was
that `REV` be the revision that *carries the work* — the invocation passed the freeze.
The lesson's wording should say that; the class survives, the mechanism sentence does not.

## F3 (high, instrument-level) — the frozen C2 counter cannot return `PASS` at C0

Entry 2's fix is verified (r4/r5/r8), but the instrument the round froze cannot express
it as a pass. At C0, *every* arm is ok and the verdict is still false:

```
$ python3 frozen_c2.py --lane LANE --rev 9cf0146b94dd --work <empty> --explain
EXPLAIN grammar registry-check --rev               rc=2  ok
...
EXPLAIN docs                                      7/7 ok
EXPLAIN note                                      9/9 ok
EXPLAIN skill                                     1/1 ok
C2_R55: rev=9cf0146b94dd grammar=9/9 lazy=5/5 empty=13/13 usable=13/13
        tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false      (exit 1)
```
(receipt `r12-c2-frozen-at-C0-receipts.json`: `{"grammar":9,"lazy":5,"empty":13,
"usable":13,"docs":7,"note":9,"skill":1,"bad":{}}`; reproduced a second time from an
empty work dir, full 43-line `--explain` output in `r15-c2-frozen-at-C0.out`, same
verdict line, exit 1 both times.)

The `total` expression was not updated with amendment 6's denominators
(`c2/measure.py:271-273`; the arms iterate `cheap` at `:218` and the note target is
`len(allocating)` at `:261`; sha256 `36ca47d3…`, exactly the bytes `freeze.json` pins):

```
total = (len(allocating)-grammar_ok) + (len(lazy)-lazy_ok)
      + (len(table)-empty_ok) + (len(table)-usable_ok)
      + tmp_total + (7-docs) + (8-note) + (1-skill)
```

with `len(allocating)=9`, `len(table)=14`, `len(cheap)=13`. Three leftovers:
`(8 - note)` is −1 for the now-correct `note=9`; `len(table) - empty_ok` and
`len(table) - usable_ok` are **+1 each** because the arms iterate `cheap` (13), not
`table` (14), where `registry-check --rev` is deliberately excluded.

```
$ python3 - <frozen_c2.py>     → r6-frozen-c2-total-arithmetic.out
len(allocating)=9 len(lazy)=5 len(table)=14 len(cheap)=13
BASE receipt reproduction (6/9,5/5,13/13,13/13,0,0,0,0) = 21  [committed before/c2.stdout says total=21]
PERFECT C0 tree  (9/9,5/5,13/13,13/13,0,7,9,1)      = 1  [PASS requires 0]
PERFECT except skill=0                                = 2
```

The base reproduction returning exactly the committed `total=21` proves the formula was
read correctly and that the committed base receipt was produced by *these* bytes. The
consequence for the wave: `controls.sh b` will print `CTL_POS_c2 … total=1 …
C2_R55_PASS=false` → `CTL_MISMATCH` → `CONTROLS_B` short of pre-registration and exit 1, and the
deciding run cannot certify C2. Suggested fix (a freeze amendment 8, before the
deciding invocation, announced as such): `(len(allocating)-note)` and
`(len(cheap)-empty_ok)/(len(cheap)-usable_ok)`.

*Post-C0 status:* the round took exactly that repair at commit `133b2ce` ("freeze
amendment 8 — c2/measure.py totals use the denominators they measure (cheap 13 in the
empty/usable terms, allocating 9 in the note term); at the all-green state the verdict
read total=1 with an empty bad map"), which is my r15 observation word for word; the
lane HEAD's `c2/measure.py:271-273` now carries `(len(cheap) - empty_ok)`,
`(len(cheap) - usable_ok)` and `(len(allocating) - note)`, and
`.ufo/evidence/round-55/after/c2.stdout` in the worktree prints
`C2_R55: rev=4c04c1d33377 … note=9/9 skill=1/1 total=0 C2_R55_PASS=true`. So F3 is a
defect of the bytes frozen at `e2979f2` (the assignment's counter) and of the C0 lesson
that cites them — not of the round as it finally landed; the lesson at C0 nevertheless
states the repaired predicate "is unchanged", which the then-frozen verdict could not
score.

Note this also disposes of a claim in entry 2 — "the predicate is unchanged … only the
comparison is honest about typography": at the arm level that is exactly true (r8), but
the verdict predicate `total == 0` is unreachable, so the honest comparison cannot be
scored.

## F4 (low) — entry 2's class covers the `skill` arm, not the `note` arm

Entry 2 classifies "a predicate that counted a document as not stating a rule when a
**line break** had split it", and folds in "the note arm had the same shape for the
`bash-witness-study selftest` label, which the counter itself spelled `--selftest`."
The note arm's failure has nothing to do with a line break — the note spells the mode
correctly, on one line:

```
$ git show 9cf0146:corpus/knowledge/scratch-root-contract.md | grep -n "bash-witness"
79:`registry-check --rev`, `bash-witness-study selftest`,
91:`bash-witness-study count`, `pin-disposition --read`,
$ python3 - <arm probe>  → r8-doc-arm-probe-pre-vs-frozen.out
PRE e2979f2^ (sha 9d076812)    allocating=8 note_names=7/8 missing=['bash-witness-study --selftest'] raw_skill=0/1 collapsed_skill=1/1
FROZEN C0 (sha 36ca47d3)       allocating=9 note_names=9/9 missing=[]                                        raw_skill=0/1 collapsed_skill=1/1
```

That is a *mislabeled identifier in the counter*, repaired by amendment 3, not by
whitespace normalisation (amendment 2). The entry discloses both amendments, so nothing
is hidden; the class sentence, however, claims one cause for two. A precise class is:
"a predicate compared text by an exact spelling that the document's typography or the
counter's own label did not share."

For the SKILL arm the line-break claim is exact: the marker spans `SKILL.md:39-40`
(line 39 is 76 chars — near the stated 78), `MARKER in raw` is `False`,
`MARKER in " ".join(split())` is `True`.

## F5 (low) — entry 2's `captured-by` is prose, and its parenthetical is false

*"captured-by: the freeze-time dry run on an edited clone (no prior round had a dry run
*before* the controls)"*. No artifact of that dry run is committed: the phrase appears
only in `contract.json`/`freeze.json` prose (amendments 1-4, "found by the L1 dry run
before any control score"), and the nearest committed observation of the phenomenon is a
wave-1 receipt made later (`T55W1ExecGrammarBreak-receipts/freeze-counter-9d0768.out`:
`note 7/8 FAIL` / `skill 0/1 FAIL` / `total=3` at `8a678ac3`). So the capture is a claim
about an unrecorded event.

The parenthetical is literally false: round 54's freeze amendment 1 reads *"found by the
binder dry run before any deciding invocation and before any control score"*
(`.ufo/evidence/round-54/freeze.json`). What was new in round 55 is a dry run *of the
counters on an edited clone*; the clause should say that, or `captured-by: none`.

## F6 (medium) — the lesson header's freeze pointer does not name the frozen bytes

Header: *"counter freeze `631cd645` + amendments 1-4 (all in `freeze.json` …)"*.
At `631cd645` `freeze.json` has **zero** amendments; the committed freeze manifest has
**seven**, and only from `e2979f2` onward:

```
$ python3 - <self-pin check>   → r7-freeze-pointer-selfpins.out
REV 631cd6455e58 amendments=0
   OK  .ufo/evidence/round-55/c2/measure.py  want=9d076812d9c0 got=9d076812d9c0
   OK  .ufo/evidence/round-55/contract.json  want=2388cb50323f got=2388cb50323f
REV e2979f277138 amendments=7
   OK  .ufo/evidence/round-55/c2/measure.py  want=36ca47d36c4b got=36ca47d36c4b
   OK  .ufo/evidence/round-55/contract.json  want=31d5c8adf961 got=31d5c8adf961
REV 9cf0146b94dd amendments=7   (identical to e2979f2)
```

`before/c2.stdout` — the receipt this lesson cites — reads `grammar=6/9 … note=0/9 …
total=21`, which only the nine-mode (`36ca47d3`) bytes produce (the `631cd645` bytes give
`grammar=6/8 … note=0/8 … total=18`, as `T55W1CritFreeze-receipts/snapshot/before_c2.stdout`
records). So the header's pointer cannot be the counter that produced the receipt two
lines below it; `631cd645` is the *pre-amendment* freeze. The same defect is in
`LOG.md:2526` ("frozen at `631cd645`, amended four times … all four recorded in
`freeze.json`") and `LOG.md:2543-2545` ("the eight allocating modes" — nine landed).
This matters because a reader verifying entry 2 from the header lands on bytes that
predate amendment 2 — and reproduces the defect rather than the repair (r4).

*Post-C0 status:* live at lane HEAD. `corpus/lessons/round-55.md:3` still reads
"counter freeze `631cd645` + amendments 1-4", while `freeze.json` at HEAD lists
**nine** amendments (`[1..9]`) and the freeze pointer has moved twice (`133b2ce`,
`e2979f2`). The LOG entry carries the same stale shape.

---

## Falsifiers run (the "can the fix fail" question)

### Falsifier 1 — the R54.1 record binding (entry 1)

Fixture: `git clone --shared` at C0, ER-R54-1's `Corrected:` clause replaced by
`CTL_POS_c1 true` (diff `r9-fixture-1-c1-corrections-claim-a-pass.diff`), committed at
`45b750c15906`.

```
$ python3 frozen_c1.py --lane <fixture> --rev 45b750c15906 --work <empty> --explain
EXPLAIN R54.1 FAIL premise=ok corrected=miss stale=0 derived=CTL_MISMATCH + 2/3
C1_R55: rev=45b750c15906 classes=10 premise=10/10 stale=0 classes_corrected=9/10 total=1 C1_R55_PASS=false
$ echo $?  → 1                                          (r3-c1-mutated-claim-in-corrections.out)
```

Clean at C0 for contrast: `C1_R55: … total=0 C1_R55_PASS=true` (exit 0,
`r1-c1-frozen-at-C0.out`). So the arm that repairs this class really fires on the
sentence it forbids, and it is bound to the receipt's tokens, not to prose.

### Falsifier 2 — the whitespace-normalised `skill` arm (entry 2)

Fixture: clone at C0 with the grammar sentence deleted from `SKILL.md` (diff
`r10-fixture-2-skill-grammar-removed.diff`), committed at `2d0ca2d74bce`.

```
$ python3 frozen_c2.py --lane <fixture> --rev 2d0ca2d74bce --work <empty> --explain
EXPLAIN docs 7/7 ok   EXPLAIN note 9/9 ok   EXPLAIN skill 0/1 FAIL
C2_R55: … docs=7/7 note=9/9 skill=0/1 total=2 C2_R55_PASS=false        (exit 1)
```

`1/1` at C0 (r12) → `0/1` here (r5): normalisation did not make the arm vacuous, and the
arm contributes exactly +1 to `total`.

### Necessity of the fix (entry 2's `0/1` claim, first-hand)

The pre-amendment bytes are `e2979f2^:.ufo/evidence/round-55/c2/measure.py`
(sha256 `9d076812…`), run against the *correct* C0 tree:

```
$ python3 pre_c2.py --lane LANE --rev 9cf0146b94dd --work <empty> --explain
EXPLAIN grammar registry-check --rev               rc=2  ok      (8-mode table; amendment 6 not yet)
...
EXPLAIN docs                                      7/7 ok
EXPLAIN note                                      7/8 FAIL
EXPLAIN skill                                     0/1 FAIL
C2_R55: rev=9cf0146b94dd grammar=8/8 lazy=5/5 empty=13/13 usable=12/13
        tmp_mkdirs=0 docs=7/7 note=7/8 skill=0/1 total=3 C2_R55_PASS=false
```
(`r4-c2-pre-amendment-at-C0.out`). `skill=0/1` on a correct edit reproduces exactly as
entry 2 states; `note=7/8` reproduces the second half. (`usable=12/13` is amendment 4's
known tracer defect, unrelated.)

### The control discriminates revisions (entry 1's premise)

```
$ python3 frozen_c1.py --lane LANE --rev 0a2010acd1e9 …  → C1_R55 … total=10 C1_R55_PASS=false  (exit 1)
$ python3 frozen_c1.py --lane LANE --rev 9cf0146b94dd …  → C1_R55 … total=0  C1_R55_PASS=true   (exit 0)
```
(`r2-c1-frozen-at-base.out`, `r1-c1-frozen-at-C0.out`.) A phase-B clone anchored at a
pre-work revision therefore prints `CTL_MISMATCH expected=true actual=false`, i.e. the
harness's own `check CTL_POS_c1 true "$v"` refuses it — the round-54 failure mode is now
loud *and* recorded.

## Residual risk and verification gaps

- I did not run `controls.sh b` end to end (it needs the round's own invocation and the
  L1's receipt directory). The phase-B verdict for C2 is inferred from (a) the harness's
  `check CTL_POS_c2 true "$v"` and (b) my C0 run printing `C2_R55_PASS=false` with every
  arm ok. Seat T55W2RevGateResidual owns that check.
- The "four lane records" count is verified as: fleet report `.ufo/reports/round-54/tameshi.md:161-162`
  ("proven live by the phase-B positive control"), `SCORECARD.md:2583` at `c210810`,
  `corpus/QUALITY.md:1590` at `c210810`, `corpus/lessons/round-54.md:74,101` at
  `c210810` — matching R54.1's own enumeration.
- Entry 2's `captured-by` cannot be verified or refuted: no receipt of a freeze-time dry
  run exists (F5). I treat the claim as prose, not as a finding either way.
- Whether the round's own `controls.sh b` is invoked with `REV=C0` (rather than the
  freeze, round 54's mistake) is outside my seat; the harness still does not forbid it
  (F2).

## Artifacts opened

`corpus/lessons/round-55.md` @C0 (whole), `.ufo/evidence/round-55/freeze.json` @631cd645,
@e2979f2, @C0, `.ufo/evidence/round-55/contract.json` @C0, `.ufo/evidence/round-55/c1/measure.py`
@C0, `.ufo/evidence/round-55/c2/measure.py` @C0 and @`e2979f2^`, `.ufo/evidence/round-55/controls.sh`
@C0, `.ufo/evidence/round-55/deciding-run.sh` @C0, `.ufo/evidence/round-55/before/c2.stdout`,
`.ufo/evidence/round-54/control/controls-b.stdout`, `.ufo/evidence/round-54/control/controls.sh`
@077d431, `.ufo/evidence/round-54/deciding-run.sh` @077d431, `.ufo/evidence/round-54/freeze.json`
@C0, `corpus/lessons/round-54-verifier-spotcheck.md` @C0, `corpus/QUALITY.md` @C0 and
@c210810, `SCORECARD.md` @C0 and @c210810, `LOG.md` @C0, `SKILL.md` @C0,
`corpus/knowledge/scratch-root-contract.md` @C0, `.ufo/reports/round-54/tameshi.md`,
`.ufo/waves/round-55/w1/T55W1ExecGrammarBreak-receipts/freeze-counter-9d0768.out`,
`.ufo/waves/round-55/w1/T55W1CritFreeze-receipts/snapshot/{before_c2.stdout,freeze.json,contract.json}`.

Tooling: nothing installed or upgraded (no pacman transaction, no `uv`/`npx`/binary
install was needed).
