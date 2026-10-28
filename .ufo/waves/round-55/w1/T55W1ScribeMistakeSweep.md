# T55W1ScribeMistakeSweep — mined-mistake sweep (rounds 50–54)

Seat `T55W1ScribeMistakeSweep`, round 55 wave 1, L1 `TameshiR55`. Axis **calibration**;
milestone **mined-mistake sweep**. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`,
base `0a2010acd1e92e4e332774050825e21bcfc7e079`, frozen counter set `631cd645`.

Read-only on every lane production file. I wrote only
`.ufo/waves/round-55/w1/T55W1ScribeMistakeSweep.{md,json}` and
`.ufo/waves/round-55/w1/T55W1ScribeMistakeSweep-receipts/`.
All three sweeps run in a `git clone --shared` of the lane checked out at base, and each
script is committed beside its receipt; all three reproduce byte-identically from a fresh
clone (`REPRODUCES_IDENTICALLY` / `SWEEP3_CELLS_REPRODUCES` in
`sweep1-recurrence.py`, `sweep2-planned.py`, `sweep3-cells.py` re-runs).

## Verdict up front

**The sweep found candidates; it did not find none.** Ranked by evidence:

| rank | candidate | class routed twice? | state | strongest single receipt |
|---|---|---|---|---|
| 1 | **C — a record value quoted against a receipt that does not print it** | **yes** (r53 R53.1 → r54 R54.3/R54.4/R54.10), and a **new instance survives round 55's own corrections** | **live in the working tree** | `.ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-base.out:9` |
| 2 | **A — uncommitted round work at closure** | **yes, three times** (r52 R52.4 → r53 R53.9 → r54 R54.6) | historical, no instrument has ever been added | `.ufo/evidence/round-54/after/clean-tree-after.txt` |
| 3 | **B — a `Planned` row naming work already in the tree** | no (first occurrence) | live: the plan line still stands | `git cat-file -e 0a2010ac:corpus/knowledge/delta-debugging-minimization-contract.md` |

**Strongest evidence: candidate C**, for four reasons set out in §3: it is the only
candidate whose wrong statement is *still in the tree after round 55 wrote its corrections
section*; the class is documented as routed twice already; the frozen C1 counter is blind to
both of its arms; and it comes with a committed receipt that falsifies the correction's own
headline. Candidates A and B are real but neither is a *record* defect that C1 can measure —
A is a missing instrument, B is a stale plan line.

---

## 1. A routed defect that recurred (a class routed twice)

Script `sweep1-recurrence.py`; receipt `sweep1-recurrence.stdout`, `sweep1-recurrence.json`.
Counting rule fixed before the run, stated in the script docstring: population = every
routed-defect item in `corpus/lessons/round-NN-verifier-spotcheck.md` (NN=50..54, both the
`N. **Rnn.k …**` and the older bare `N. **…**` forms) plus every `- **class: …**` entry in
`corpus/lessons/round-NN.md`; class = keyword family; "recurs" = ≥2 distinct rounds.

```
$ python3 sweep1-recurrence.py <clone@0a2010ac> 0a2010acd1e92e4e332774050825e21bcfc7e079 out.json
REV=0a2010acd1e92e4e332774050825e21bcfc7e079
POPULATION defect-items=41
  round 50: 3 items
  round 51: 8 items
  round 52: 6 items
  round 53: 12 items
  round 54: 12 items

CLASS uncommitted-work-at-closure
  rounds=[52, 53, 54] hits=3 verdict=RECURS
    r52 corpus/lessons/round-52-verifier-spotcheck.md: R52.4 uncommitted round work.
        matched: 'uncommitted round work'
    r53 corpus/lessons/round-53-verifier-spotcheck.md: R53.9 — uncommitted round work (found at closure).
        matched: 'uncommitted round work'
    r54 corpus/lessons/round-54-verifier-spotcheck.md: R54.6 — uncommitted round work at closure.
        matched: 'uncommitted round work'

CLASS record-quotes-a-value-its-receipt-does-not-print
  rounds=[53, 54] hits=2 verdict=RECURS
    r53 corpus/lessons/round-53-verifier-spotcheck.md: R53.1 — frozen C1 counter rekey arm structurally dead.
        matched: 'quote does not match'
    r54 corpus/lessons/round-54-verifier-spotcheck.md: R54.10 — the phase-A control quote does not match its cited receipt.
        matched: 'quote does not match'

CLASS stale-freeze-pointer
  rounds=[53, 54] hits=2 verdict=RECURS
    r53 corpus/lessons/round-53-verifier-spotcheck.md: R53.5 — stale freeze receipts/pointers.
        matched: 'stale freeze'
    r54 corpus/lessons/round-54-verifier-spotcheck.md: R54.2 — three different freeze pointers.
        matched: 'freeze pointer'

CLASS count-vs-committed-artifacts
  rounds=[54] hits=2 verdict=single-round only
    r54 ... R54.5 — finding counts do not match the committed artifacts.
    r54 ... R54.9 — wave-table numbers.

RECURRING_CLASSES=3
```

The regex counts only the items whose *text* names the class, so the class whose instances
are prose-quoted numbers is undercounted there. Enumerated by hand from the same files the
"record quotes a value its receipt does not print" class has **four** r54 instances, not one:

```
$ git show 0a2010ac:corpus/lessons/round-54-verifier-spotcheck.md | grep -nE "R54\.(3|4|10) "
112:**R54.3 — `SCORECARD.md:2584` quotes `total=14`** from `.ufo/evidence/round-54/before/c2.stdout`,
     but that receipt prints `total=13` … no `14` exists in any receipt
114:**R54.4 — stale c2 digest in the report.** … `49280fe5` is the **pre-amendment-4** blob … freeze.json pins `8528ee85`
233:**R54.10 — the phase-A control quote does not match its cited receipt.** … `rekeyed=0/30` … that file prints `rekeyed=0/7`
```
plus R54.3's neighbour in the same table row (`credited=41`), see §3.

Receipt: `sweep1-class-instances.stdout`.

**Why A is a recurrence rather than a repeated slip.** The three routed items are the same
observation at three consecutive closures, and each round's disposition is instance-level
("commit these files") — never an instrument. There is no counter for it anywhere:

```
$ git show 0a2010ac:corpus/QUALITY.md | grep -c "^### Criterion"                    → 30
$ git show 0a2010ac:corpus/QUALITY.md | grep -ciE "closing tree|close-time|zero untracked" → 0
$ grep -c 'echo "NOHARM' .ufo/evidence/round-55/no-harm.sh                          → 15
$ grep 'echo "NOHARM' .ufo/evidence/round-55/no-harm.sh | grep -ciE "track|dirty"    → 0
$ grep -rln "git status --porcelain" tools/ | wc -l                                  → 0
```

And the harness that *would* catch it gates only the tree **before** the run. The same gate
expression applied to the after-file would refuse:

```
$ OUT=.ufo/evidence/round-54/after
$ grep -vc '^?? \.ufo/evidence/round-54/after/' $OUT/clean-tree-before.txt   → 0  → PASS
$ grep -vc '^?? \.ufo/evidence/round-54/after/' $OUT/clean-tree-after.txt    → 3  → REFUSE exit 3
$ grep -n "clean-tree-after.txt" .ufo/evidence/round-54/deciding-run.sh
87:git status --porcelain > "$OUT/clean-tree-after.txt"          # recorded only, never tested
$ grep -n "DECIDING_REFUSED dirty-tree" .ufo/evidence/round-54/deciding-run.sh
61:… || { echo "DECIDING_REFUSED dirty-tree"; …; exit 3; }        # the only gate, before
```
Identical in `round-52`, `round-53`, `round-54` and the frozen `round-55` `deciding-run.sh`.
Receipt: `candidate-A-uncommitted.stdout`, `candidate-A-gate-asymmetry.stdout`.

Two aggravating facts: **R52.4 was never dispositioned at all** — it appears in no round-53,
round-54 or round-55 lesson (`grep -c "R52\.4"` → 0, 0, 0) — and the `clean-tree-after.txt`
shows the tree went dirty *during* the deciding run, i.e. the round-54 report's "clean" claim
was measured against a receipt that says otherwise.

## 2. The round-54 `Planned (round 55)` row vs the tree

Script `sweep2-planned.py`; receipts `sweep2-planned.stdout`, `sweep2-planned.json`.
Rule fixed before the run (in the script): an item is ALREADY-DONE iff the artifact it
proposes exists at REV with the property it claims; OPEN iff not.

```
$ python3 sweep2-planned.py <clone@0a2010ac> 0a2010ac… out.json
1  ALREADY-DONE  adopt the staged merge/tameshi delta-debugging-minimization-contract.md entry
    obs: {"present_at_rev": true, "introduced": ["79f44b5 2026-10-26"], "sources_rows_citing_it": ["S024", "S271"]}
2  OPEN          env-diff --contract residue
    obs: {"registry_cell_names_contract_mode": false,
          "base_receipt_line": "EXPLAIN unusable env-diff rc=1 line=\"RuntimeError: cannot create clone scratch …\""}
3  OPEN          C2 follow-on: every documented mode of the seven tools reports the class
    obs: {"tools": 7, "cells_naming_no_mode_list": 7, "cell_sample": "TMPDIR set but unusable => exit 2, could-not-evaluate …"}
4  OPEN          service-limits §5 U1 heading re-read (carried from round 53)
    obs: {"skill_carried_line": ["U1–U6, `service-limits.md` §5 — carried, not closed here."]}

ALREADY_DONE=1 OPEN=3
```

Item 1 is the finding. The plan line at `SCORECARD.md:2598` and the round-54 lesson's
`Rejects` entry both say the entry was "REFUSED this round on capacity … next-ranked entry
for round 55":

```
$ git cat-file -e 0a2010ac:corpus/knowledge/delta-debugging-minimization-contract.md   → PRESENT
$ git log --diff-filter=A --format="%h %ad" --date=short -- corpus/knowledge/delta-debugging-minimization-contract.md
79f44b5 2026-10-26
$ git show 0a2010ac:corpus/SOURCES.md | grep -c delta-debugging-minimization-contract.md → 2
$ find /home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge -name '*.md' | wc -l      → 81
```

The entry has been in `corpus/knowledge/` since **round 50** (`79f44b5`), is cited by two
SOURCE rows (S024, S271), and the staged package still holds the same name — so round 55's
plan proposes re-adopting an adopted entry. The round-54 spot-check's discernment table
already recorded this as a `reject/disagree` row, but it is **not** in R54.1–R54.10 and the
round-55 corrections section does not carry it, so both the plan line and the lesson's
`REFUSED` sentence stand in the working tree today.

Receipts: `candidate-B-planned-done.stdout`, `sweep2-planned.stdout`.

## 3. A round-54 receipt cited for a value it does not print

Script `sweep3-cells.py`; receipts `sweep3-quotes-cells-at-base.stdout` and `.json`.
Rule fixed before the run (in the script): population = every `total=N`, `CX_R54_PASS=…`,
`CTL_POS_cN`, `rekeyed=N/N`, `credited=N` token in the `## Round 54 — …` section; excluded
cells = claim text, axis and Target (a target is a prediction, not a quoted measurement);
attribution = last `.ufo/…` reference **in the token's own cell**, else its line, else its
paragraph; backing scope = every receipt under `.ufo/evidence/round-54`, `.ufo/evidence/round-53`
and `.ufo/waves/round-54` (1163 files); 8-hex tokens that resolve as commits are out of scope.

```
LABEL=at-base-cells REV=0a2010ac… SECTION_LINES=61 RECEIPTS=1163
SCORED_TOKENS=25 EXCLUDED_TARGET_OR_CLAIM_TOKENS=7

   26   3 credited=57  NAMED_PRINTS_IT  .ufo/evidence/round-54/before/c1.stdout
   26   3 rekeyed=0/7  NAMED_PRINTS_IT  .ufo/evidence/round-54/before/c1.stdout
   26   3 total=4      NAMED_PRINTS_IT  .ufo/evidence/round-54/before/c1.stdout
   26   3 credited=41 NAMED_SILENT     .ufo/evidence/round-54/before/c1.stdout
        receipts that DO print it: ['.ufo/waves/round-54/…/T54W1Crit02-receipts/c1-at-c0.stdout', …]
   27   3 total=14    NAMED_SILENT     .ufo/evidence/round-54/before/c2.stdout
        receipts that DO print it: ['.ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-base.out', …]
   27   3 total=13    NAMED_PRINTS_IT  .ufo/evidence/round-54/before/c2.stdout

SUMMARY NAMED_PRINTS_IT=6 NAMED_SILENT=2 NO_RECEIPT_NAMED=8 RESOLVES_AS_COMMIT=9
DEFECTS=2
```

The eight `NO_RECEIPT_NAMED` prose tokens (`credited=64`, `rekeyed=7/7`, `total=0`,
`C1/C2_R54_PASS=true` in the "measured close" bullets) are backed by `after/c1.stdout` and
`after/c2.stdout`; they name no receipt inside their own bullets, which is attribution style,
not a defect — recorded separately so the count is not over-read.

### 3a. `credited=41 lost=23` — the instance that survives round 55

`SCORECARD.md:2584` (base *and* working tree) is the C1 row's `Before` cell:

> `credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 total=4` false
> (`.ufo/evidence/round-54/before/c1.stdout`); at C0 the round's own edits drift it to
> **`credited=41 lost=23`**

```
$ git show 0a2010ac:.ufo/evidence/round-54/before/c1.stdout | grep -o "credited=[0-9]* lost=[0-9]*"
credited=57 lost=7
$ grep -rn "credited=41" .ufo/evidence/round-54 .ufo/evidence/round-53      → (no match)
$ grep -rn "credited=41" .ufo/evidence/round-54/control/                    → (no match)
$ sed -n '/^## Round 55 - round-54 record corrections/,$p' SCORECARD.md | grep -c "credited=41"  → 0
```

The value is **true**: re-derived at `59c38109` with the frozen counter
(`C1_R54: … credited=41 lost=23 … total=4`), receipt `c01-rederive-credited41-attempt.txt`.
The pointer is what is wrong — the cell names one receipt and prints two readings, and the
second reading is printed by no file under `.ufo/evidence/round-54/` at all; only wave seat
receipts (`T54W1Crit02-receipts/c1-at-c0.stdout`) carry it. Round 55's corrections section
does not mention it, so a reader who checks the row's pointer gets `57`, not `41`.
`R54.3` routed the *same table row's* `total=14`; this cell was not routed.

### 3b. `total=14` — the correction's own headline is false

The working tree's corrections section heads ER-R54-3 with a universal:

```
$ grep -n "a quoted total no receipt contains" SCORECARD.md
2649:**ER-R54-3 - a quoted total no receipt contains.**
```

A committed receipt prints it, and it was committed **before** the spot-check:

```
$ git grep -n "sources=0 total=14" 0a2010ac -- .ufo/waves/round-54/w1/T54W1ExecFreeze-receipts
….ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-base.out:9:
  C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0
          docs=0 note=0 sources=0 total=14 C2_R54_PASS=false
$ git merge-base --is-ancestor 077d431 650987a && echo yes   → yes   (receipt added 077d431; spot-check at 650987a)
$ git cat-file -e 650987a:.ufo/waves/round-54/w1/T54W1ExecFreeze-receipts/c2-frozen-bytes-at-base.out → PRESENT
```

`before/c2.stdout` and that receipt are the **same counter at the same base revision**, and
they differ in exactly one field:

```
before/c2.stdout        : usable_ok=7 … sources=0 total=13
c2-frozen-bytes-at-base : usable_ok=6 … sources=0 total=14
```

Round-54's own `T54W1ExecFreeze.md` F4 documents that arm as load-dependent ("[INFERENCE]
the same frozen bytes can print `usable_ok=7` on an idle host"), because the traced
`registry-check` self-test loses two `timeout`/`setsid` cases under load. So `14` is a real
reading of the frozen bytes, and ER-R54-3's headline ("no receipt contains") is false — it
is the same error the spot-check itself made, a universal asserted from a search of
`.ufo/evidence/` only (`git grep -c "total=14" 0a2010ac -- .ufo/evidence/round-54` → 0
files, which is where `14` was "not found"). The correction also publishes `13` as "the"
value without disclosing that the base reading is instrument-flaky.

Receipts: `candidate-C-credited41.stdout`, `candidate-C-total14-claim.stdout`,
`candidate-C-both-readings-real.stdout`, `candidate-C-corrections-headline.stdout`,
`sweep3-pointer-arm.stdout`.

### 3c. Why the frozen counter cannot see either arm

```
$ grep -c "no receipt contains\|credited=41" .ufo/evidence/round-55/c1/measure.py   → 0
```

The C1 counter's R54.3 arm greps `total=14` outside the corrections section and requires
`total=13` inside it; it does not read the headline's universal and it does not read
`credited=41`. So C1 can print `total=0 C1_R55_PASS=true` while the corrections section
carries a false universal and the C1 row still points at a receipt that prints another
number. That is the reason candidate C is the strongest finding: it is a live calibration
defect **inside the surface C1 measures**, invisible to C1.

## 4. Which candidate has the strongest evidence, and why

**Candidate C.** The ranking criteria were: (i) is the wrong statement still in the tree at
the revision under test, (ii) was the class already routed, (iii) can the round's own counter
see it, (iv) is every claim backed by a command and a committed receipt.

- (i) **Live.** Round 55 wrote its corrections section and the two defects survive it:
  `SCORECARD.md:2584` still prints `credited=41 lost=23` against a receipt that prints `57`,
  and `SCORECARD.md:2649` still asserts "no receipt contains" a total a committed receipt
  contains. Both are in the working tree, not history.
- (ii) **Routed twice already**, four instances: r53 `R53.1` (`total=6` vs the counter's
  `37`), r54 `R54.3` (`total=14` vs `13`), `R54.4` (digest `49280fe5` vs pinned `8528ee85`),
  `R54.10` (`rekeyed=0/30` vs `0/7`). Sweep 1 confirms the class in rounds 53 and 54.
- (iii) **Counter-blind**, proved above: `grep -c "no receipt contains\|credited=41"` on the
  frozen counter is `0`. The class can recur while C1 reads green.
- (iv) Every claim above is one command; the receipts are committed beside this report and
  all three sweep scripts reproduce byte-identically from a fresh clone.

**Candidate A** has the widest recurrence (three consecutive rounds, plus an undispositioned
R52.4) and the cleanest structural proof — the harness gates the before-tree and merely
records the after-tree, in rounds 52, 53, 54 and the frozen round 55. It ranks second only
because it is not a *record* defect C1 can measure: fixing it needs a new instrument
(after-tree gate or a no-harm monitor), which is out of this round's frozen contract.

**Candidate B** is the crispest single fact (one `git cat-file -e`) and it also survives in
the working tree, but it is a first occurrence, the round-54 spot-check's discernment table
already recorded it as a disagreement, and it is a plan-line defect rather than a measured
value.

## Conformance

```
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi ; echo exit=$?
tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
exit=0
$ git show 0a2010ac:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'   → 139   (at base)
$ grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md                      → 140   (working tree; S280 added by another seat)
```

## Limits and environment notes

- **The sweeps read committed bytes only** (`git show REV:path`), never the dirty working
  tree, except where a claim is explicitly about the working tree (§3a, §3b, §4(i)).
- **Attribution is a heuristic.** §3's cell rule undercounts: a value and its receipt can sit
  in different cells of the same table row (that is exactly what happens at `2584`), which is
  why cell-level attribution first moved `credited=41` from `NAMED_SILENT` to a weaker
  `NO_RECEIPT_NAMED` before the fix. The `.json` receipt carries every token and its verdict
  so a reader can re-score under a different rule.
- **The `14`/`13` question is not fully decidable from committed bytes.** I can prove both
  values were printed by the same counter at the same revision and that they differ only in
  `usable_ok`; I cannot prove from the tree which byte set produced `before/c2.stdout`
  (written 11:32, committed 11:51) — the load-dependence is ExecFreeze F4's `[INFERENCE]`,
  and I report it as theirs, not as measured.
- **Gap in `R52.4`:** it appears in no lesson; I could not find a disposition of it anywhere
  in `corpus/lessons/round-5{3,4,5}.md` (`grep -c "R52\.4"` → 0).
- **Scratch was wiped externally mid-run.** My scratch directory
  `/fast/scratch/hyaku/tameshi-r55/T55W1ScribeMistakeSweep/` (clone + scripts) disappeared
  between two tool calls while sibling seats' directories under the same parent survived; I
  re-cloned, and re-ran all three sweeps against the receipts — they reproduce identically,
  so no finding depends on the lost copy. Reported as an observation, cause unknown.
- **The lane tree was already dirty when this seat started** (`M SCORECARD.md`, `M SKILL.md`,
  `M corpus/QUALITY.md`, `M corpus/lessons/round-54.md`,
  `M corpus/knowledge/scratch-root-contract.md`, `M tools/registry.json`,
  `M tools/repeat-control.py`, `M tools/context-capture.py`, `M .ufo/evidence/round-55/*`).
  None of those are my writes: this seat wrote only the two files named in the header and the
  27 receipts, and every claim about the *working tree* above is a read of somebody else's
  in-flight integration. Flagged because it means a `git status` at this moment is not
  evidence of closure cleanliness either way.
- **Out of scope, named:** whether a corrections-section headline counts as a "stale
  assertion" under C1 (the frozen counter's `corrections()` body is stripped before the scan,
  so the section is unmeasured by construction — a contract question for the L1, not a seat
  edit); whether r55's own `clean-tree-after.txt` will be dirty at its closure.

## Receipts

`.ufo/waves/round-55/w1/T55W1ScribeMistakeSweep-receipts/` —

- `sweep1-recurrence.py`, `sweep1-recurrence.stdout`, `sweep1-recurrence.json`,
  `sweep1-class-instances.stdout`
- `sweep2-planned.py`, `sweep2-planned.stdout`, `sweep2-planned.json`,
  `candidate-B-planned-done.stdout`
- `sweep3-cells.py` (the operative rule), `sweep3-quotes-cells-at-base.stdout`,
  `sweep3-quotes-cells-at-base.json`, and the earlier coarser variants kept for audit:
  `sweep3-cols.py`, `sweep3-wide.py`, `sweep3-quotes-*.stdout`
- `candidate-A-uncommitted.stdout`, `candidate-A-gate-asymmetry.stdout`
- `candidate-C-credited41.stdout`, `candidate-C-total14-claim.stdout`,
  `candidate-C-both-readings-real.stdout`, `candidate-C-corrections-headline.stdout`,
  `c01-rederive-credited41-attempt.txt`, `sweep3-pointer-arm.stdout`
