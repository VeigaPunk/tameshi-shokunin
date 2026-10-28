# T55W1Connector2 — routed-defect overlap: R54.1–R54.10 against rounds 51–53

seat: T55W1Connector2 (connector, wave 1, round 55)
lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
base read at: `0a2010acd1e92e4e332774050825e21bcfc7e079` (all quotes below are `git show 0a2010a:<path>` unless a commit is named)
frozen counter set: `631cd6455e58dce969310b4c0466c3383d9f5108` (`.ufo/evidence/round-55/`)
scratch: `/fast/scratch/hyaku/tameshi-r55/T55W1Connector2` (clone `lane` at base; removed on exit)
machine-readable matrix: `T55W1Connector2.json` (beside this file)
receipts: `T55W1Connector2-receipts/` (index at the end)

**Verdict.** The ten rows the round-54 spot-check routed are **seven classes, not ten**, and **nine of the ten rows are a class the lane had already routed in round 51–53**. Only R54.7 has no same-class predecessor (same family, different mechanism). Of the earlier instances, **five were marked FIXED by a later round and every one of those fixes was partial or narrower than the class**, and **one (R52.3) was never dispositioned at all**. The round's corrections section treats all ten as new; the `## Mistakes` section should say what they are: recurrences, with the earlier "FIXED" verdicts as the evidence.

---

## 1. Method

Read at base, not at the dirty working tree (other seats are writing into it). Every quote is `git show 0a2010a:<path>`, with the line number the counter itself prints where one exists.

Commands (full output in the receipts named in §8):

```
git show 0a2010a:corpus/lessons/round-5{1,2,3}-verifier-spotcheck.md   # routed rows, line-anchored
git show 0a2010a:corpus/lessons/round-5{2,3,4}.md                      # dispositions each round filed
git show 0a2010a:SCORECARD.md | grep -n 'total=6\|total=14\|7883e0e5\|fe70474d\|097985c1'
git show 0a2010a:.ufo/evidence/round-54/control/controls-b.stdout      # the receipt R54.1 cites
git show 077d431e:.ufo/evidence/round-54/freeze.json                   # amendment count (5)
git show 0a2010a:.ufo/evidence/round-54/c2/measure.py | sed -n '60,110p'
git cat-file -e d33053f7:<p>  /  git cat-file -e 0a2010a:<p>           # R52.4 / R53.9 tracking
git show 0a2010a:corpus/lessons/round-5{3,4}.md | grep -c 'R52\.[1-6]'
python3 …  # R54.5 recount from the committed reader JSONs; R54.9 from w1-registry.json
```

I did **not** run any frozen counter. C1's stale hits are quoted from the committed `before/c1.stdout`; the two corrected values I lean on (R54.5, R54.9) I re-derived myself (§5).

---

## 2. The matrix

Legend for `strength`: **dup** = same class, same mechanism; **dup-near** = same class, adjacent mechanism (different artifact, same failure of the record); **family** = same family of imprecision, not the same class.

| # | R54 row (filed) | class | predecessor | strength | fixed by | earlier fix partial? |
|---|---|---|---|---|---|---|
| 1 | R54.1 false positive-control claim | phase-B control claim not bound to its receipt | **R53.3** | dup | round 54 (disposition `R53.3 … FIXED`) | **yes** — the fix committed the receipt, then contradicted it |
| 2 | R54.2 three freeze pointers | freeze pointer / freshness of the freeze record | **R53.5** | dup | round 54 (disposition `R53.5 … FIXED`) | **yes** — manifest regenerated; prose carried 3 pointers; the disposition's own "no amendment is recorded" is false (5 amendments) |
| 3 | R54.3 `total=14` vs receipt `13` | quoted value the named artifact does not print | **R53.1** (second half: "correct the SCORECARD quote") | dup | **never** — round 54's R53.1 disposition names the pathspec only | **yes, by omission** — `total=6` still stands at `SCORECARD.md:2551` at base |
| 4 | R54.4 stale c2 digest `49280fe5` | citation names bytes other than the deciding bytes | **R53.4** + round-53 conformance (d)(e) | dup-near | round 54 (disposition `R53.4 … FIXED`) | **yes** — fixed revision resolvability, not byte-identity with `freeze.json` |
| 5 | R54.5 finding counts 25/22-in-9 | count asserted, never derived | **R52.3** ("under one written counting rule") | dup | **never** — no later lesson names R52.3 (0 mentions) | **n/a — dropped without disposition** |
| 6 | R54.6 uncommitted round work | uncommitted round work at closure | **R52.4**, **R53.9** | dup | round 53 (R52.4 instance) and round 54 (R53.9 instance, "CLOSED") | **yes** — instance committed each time; no clean-tree monitor exists in round 54's or round 55's `no-harm.sh` |
| 7 | R54.7 "deletion lands in 7fa9a5e0" | a record misdescribes what a commit did | R53.7, R53.8 | **family only** | n/a | **not a duplicate** — R53.7/R53.8 are wrong *pointers*; R54.7 is a wrong *verb* (rename written as deletion) |
| 8 | R54.8 incident half-recorded | (a) false/superseded claim left where it lives; (b) pointer to a record that does not exist | (a) **R51.2** + round-51 quality verdict; (b) **R53.2** | dup (both halves) | round 52 (statement set 27→0), round 54 (`R53.2 … FIXED by construction`) | **yes** — both repairs are bounded to the enumerated/frozen set; the offending records were created in the same round |
| 9 | R54.9 wave-table numbers, 84 vs 81 | count asserted, never derived | **R52.3** (same class as R54.5) | dup | **never** | **n/a — dropped** |
| 10 | R54.10 `0/30` under `controls-a.stdout` | quoted value the named artifact does not print | **R54.3** (same document) + **R53.1** | dup | **never** | **yes, by omission** |

**Counts.** Rows duplicating an earlier routed class: **9** (all but R54.7). Distinct classes: **7**. Earlier instances marked FIXED by a later round: R53.3, R53.4, R53.5, R53.2, R52.4/R53.9 — **5, all partial**. Earlier instance never dispositioned: R52.3 — **1**.

---

## 3. The chains, both sides quoted

### Chain A — phase-B control claimed vs the receipt that decides it (R54.1 ← R53.3)

Round 53 routed:

> **R53.3 — phase-B break-one controls unbacked.** `control/break-fixtures.py` is committed and well-formed, but no `CONTROLS_B:` tally receipt exists anywhere under `.ufo/`; SCORECARD's "each printed false … (receipts control/)" overstates.
> — `corpus/lessons/round-53-verifier-spotcheck.md:80`

Round 54 dispositioned it:

> **R53.3** (phase-B controls unbacked) — FIXED: `control/controls-b.stdout` and `controls-b.exit` are committed before the deciding run, which refuses to run without them.
> — `corpus/lessons/round-54.md:108-110`

And then routed the same class against its own record:

> **R54.1 — false positive-control claim (gravest).** … prints `CTL_MISMATCH CTL_POS_c1 expected=true actual=false`, `CONTROLS_B: 2/3 as pre-registered`, exit 1. Yet the record asserts the opposite in four places
> — `corpus/lessons/round-54-verifier-spotcheck.md:107`

The receipt R53.3's fix supplied (line-numbered, my read):

```
1:CTL CTL_POS_c1 C1_R54: rev=077d431e6996 … total=4 C1_R54_PASS=false
2:CTL_MISMATCH CTL_POS_c1 expected=true actual=false
5:CONTROLS_B: 2/3 as pre-registered
```

**Fixed by round 54. Partial, and the partiality is the whole defect:** the round satisfied R53.3's letter (a `CONTROLS_B:` receipt now exists) and broke its intent (the receipt was never bound to the prose). R53.3 said the SCORECARD *overstates*; the fix made the overstatement falsifiable and left it standing, in four files, one of them a QUALITY criterion written that round.

### Chain B — freeze pointer (R54.2 ← R53.5)

Round 53:

> **R53.5 — stale freeze receipts/pointers.** committed `verify-freeze.stdout` is amendments=5-era (final freeze: amendment 7 at 9e09db2); LOG.md pins "freeze e62d9971 (amendments 1–5)" and never names `cf872769`. Refresh the receipt at the final freeze and correct the pointer.
> — `corpus/lessons/round-53-verifier-spotcheck.md:82`

Round 54:

> **R53.5** (stale freeze receipts) — FIXED: `freeze.json` is regenerated at freeze time and the deciding run prints `FROZEN_UNCHANGED=1` against it; **no amendment is recorded**.
> — `corpus/lessons/round-54.md:114-116`

Round 54's own row:

> **R54.2 — three different freeze pointers.** `SCORECARD.md:2564-2567` calls `7883e0e5` "the freeze pointer the deciding run uses" …; `SCORECARD.md` "measured close" says "freeze `fe70474d` (amendments 1-5)" …; report `:157` says the freeze pointer is `097985c1` … The receipt says `freeze=077d431e` with 5 amendments.
> — `…round-54-verifier-spotcheck.md:110`

**Fixed by round 54. Partial, and the disposition sentence is itself false:** `freeze.json@077d431e` lists amendments 1–5 (verified), and at base `SCORECARD.md:2564,2567` call `7883e0e5` the freeze pointer while `:2608` prints `freeze fe70474d (amendments 1-5)`. Regenerating the manifest did not bind the prose to it — the exact failure R53.5 named.

### Chain C — a quoted value the named artifact does not print (R54.3, R54.4, R54.10 ← R53.1 second half, R53.4)

Round 53, one row with two halves:

> **R53.1 — frozen C1 counter rekey arm structurally dead.** … the SCORECARD's `total=6` quote does not match the counter's actual `total=37` output. Fix the pathspec …, re-run at the final revision, commit receipts, **correct the SCORECARD quote**.
> — `corpus/lessons/round-53-verifier-spotcheck.md:78`

Round 54 disposition — the second half is not mentioned:

> **R53.1** (the frozen round-53 C1 counter's rekey arm was dead) — FIXED: this round's counter lists the re-key directory with `git ls-tree -r` … and the arm is proven live by the positive control (`CTL_POS_c1`, which prints `rekeyed=7/7`).
> — `corpus/lessons/round-54.md:98-104`

Three recurrences inside round 54's own record:

> **R54.3 — `SCORECARD.md:2584` quotes `total=14`** from `.ufo/evidence/round-54/before/c2.stdout`, but that receipt prints `total=13` … and hides that no `14` exists in any receipt.
> **R54.4 — stale c2 digest in the report.** … `49280fe5` is the **pre-amendment-4** blob … `freeze.json` pins `8528ee85…`
> **R54.10 — the phase-A control quote does not match its cited receipt.** … that file's `CTL_R53` line prints `rekeyed=0/7` … `0/30` belongs to … `control/r53-counter-at-88afa941.stdout`.
> — `…round-54-verifier-spotcheck.md:112,114,233`

**Fixed by round 54 for the counter half only; the quote half was never fixed.** At base `SCORECARD.md:2551` still reads "`total=6`." — the exact string R53.1 asked to correct — and the same class produced R54.3 and R54.10 in the same document that fixed R53.1. R54.4 is the digest variant: round 54's R53.4 disposition ("every receipt this round names revisions resolved in the lane's own object store") fixed *resolvability*, not *byte-identity with the pin* — so a resolvable-but-superseded digest passed.

### Chain D — a count asserted, never derived (R54.5, R54.9 ← R52.3)

Round 52:

> **R52.3 over-count review overstated (this closure's finding).** … claims "0 of 14" reader-marked failures …; independent re-derivation found ≥2–6 … **Re-derive the "8 over-count" verdict … under one written counting rule**
> — `corpus/lessons/round-52-verifier-spotcheck.md:85`

Round 54:

> **R54.5 — finding counts do not match the committed artifacts.** Report `:62` says the 23 wave-1 readers returned **25** findings; the committed `w1/*Read*.json` carry **28** … Report `:79,100` says wave 2 returned **22 findings in 9 of 23 sections**; the committed w2 readers carry **25 findings in 12 sections** … Re-derive both counts with a command.
> **R54.9 — wave-table numbers.** … the report itemizes 75 seats with **4** reviewers and states a 26.3 % attack share. `attack_seats` = 21 → 27.6 %. Also "the other **84** staged `merge/tameshi` entries": the package holds **81** …
> — `…round-54-verifier-spotcheck.md:116,124`

**Never fixed, never dispositioned.** `R52\.[1-6]` occurrences: `round-53.md` 3 (R52.1 ×2, R52.5 ×1), `round-54.md` **0**, round-55 draft **0**. No "written counting rule" exists — `git grep 'counting rule'` at base returns only the axis-table column header and R52.3 itself. Two rounds after the repair was specified, the class returned twice in one closure pass.

### Chain E — uncommitted round work (R54.6 ← R52.4 ← R53.9): three consecutive rounds

> **R52.4 uncommitted round work.** 4 untracked files (`.ufo/evidence/round-52/integrate/build-readers.py`, `.ufo/waves/round-52/w3.ready`, `w3.ready.dispatched`, `w3/`): commit under the round-53 entry or revert; **a lane repo must not carry uncommitted round work into the next round.**
> — `corpus/lessons/round-52-verifier-spotcheck.md:86`

> **R53.9 — uncommitted round work (found at closure).** six lane-authored round-53 files are untracked at the push tip: … **a lane repo must not carry uncommitted round work into the next round.**
> — `corpus/lessons/round-53-verifier-spotcheck.md:86`

> **R54.6 — uncommitted round work at closure.** `T54W2Sent03.md` … plus the two receipts it cites … were untracked at closure; the deciding run's own `after/clean-tree-after.txt` records them as `??` … the lane must not leave seat deliverables uncommitted again.
> — `corpus/lessons/round-54-verifier-spotcheck.md:118`

**Instance fixed every round; class never gated.** R52.4's four paths are tracked at `0a2010a`; R53.9's six are tracked at `d33053f7` (all six `TRACKED`, receipt `uncommitted-work-chain.stdout`). The only check that ever fires is the closure's `git status --porcelain`: `no-harm.sh` at round 54 and at round 55 (frozen `631cd64`) contains no `porcelain`/`clean`/`untracked` monitor (grep empty, receipt `no-harm-tree-monitors.stdout`). Round 54's own `after/clean-tree-after.txt` shows the tree dirty *during* the run the gate calls clean — so even the round that fixed R53.9 did not notice.

### Chain F — a false claim left where it lives, and a pointer to a record that is not there (R54.8 ← R51.2/round-51 verdict, R53.2)

Round 51's quality verdict:

> **quality: harmed** … But some records are now false and **left unmarked where they live**: the `mte-interop-check` registry row; SKILL.md `:2136` "nine ledger legs"; the re-key entries' `wrong_expectations: 0`.
> — `corpus/lessons/round-51-verifier-spotcheck.md:116`

> **R53.2 — deciding receipts never committed.** `.ufo/evidence/round-53/after/` (cited by SCORECARD and LOG.md in past tense) **does not exist** … correct the past-tense pointers.
> — `corpus/lessons/round-53-verifier-spotcheck.md:79`

Round 54:

> **R54.8 — config-write incident record is half-done.** … (a) the seat's own file `:324` still asserts the edit was "on the operator's direct instruction in-session, which is the higher authority" …; (b) the report says the incident is "recorded here **and in the lesson**", but `corpus/lessons/round-54.md` contains no mention of `config.yml` or a host write.
> — `…round-54-verifier-spotcheck.md:122`

**Fixed by rounds 52 and 54, both partially.** Round 52's C2 went 27→0 on its *frozen* statement set; round 54 marked R53.2 "FIXED by construction" (the deciding run writes `after/`). Both repairs are bounded sets: a record written in the same round (the report's "and in the lesson", the seat file's sentence) is outside any frozen set, so the class reappears as soon as a new record is written.

**Second-order note the L1 must carry, or the Mistakes row will repeat an error.** Round 55's `ER-R54-8` withdraws R54.8's premise: the operator turn exists in `~/.omp/agent/history.db` (row 690), so the seat file's sentence was true and the report's word *fabricated* was the false claim. Consequence for this matrix: R54.8(a) is **not** an instance of "unmarked false claim" any more — it is an instance of the K1 family (a record asserting more than its evidence: the report's *fabricated*). The duplicate of the R51 class is the report's overstatement, not the seat's text. Do not cite R54.8(a) as motivation for supersession marks.

### R54.7 — family, not duplicate

> **R53.7 — "inputs pinned at C7" imprecise.** … as the rekey-final commit message asserts. … restate the pin claim or re-pin.
> **R53.8 — S275 locator.** anchor cell "camera-ready p. 4" is physical page 3 …
> — `…round-53-verifier-spotcheck.md:84,85`

R53.7 commits a claim about *where* a pin is; R53.8 is a wrong page number. R54.7 is a wrong verb about a commit's action ("the deletion lands in `7fa9a5e0`" for a rename). Same family — a record's pointer to its own history is not checked against the object — but a different mechanism (rename detection). **I do not call it a duplicate**, and the round should not either; counting it as one would inflate the recurrence claim and weaken the four rows that are exact.

---

## 4. Self-duplicates inside R54.1–R54.10

The closure counted rows, not classes:

- **K1 quoted-value-vs-artifact: R54.3, R54.4, R54.10** — three rows, one mechanism.
- **K4 count-not-derived: R54.5, R54.9** — two rows, one mechanism.
- R54.5 is even routed twice in the document ("R54.5" at `:116` and "R54.5 extended" in the erratum at `:241`).

Ten rows → seven classes. This matters twice: the corrections section is keyed `ER-R54-1..10`, so it can look like ten independent repairs; and a closure that reports "ten routed defects" against a round that fixed "five classes" cannot tell a recurrence from an improvement next round.

---

## 5. Values I re-derived (so the matrix does not inherit a number either)

| value | my command | observed |
|---|---|---|
| R54.5 wave-1 findings | `findings` length over `git ls-tree` of `.ufo/waves/round-54/w1`, `-receipts/` excluded, at `0a2010a` | 23 readers, **28** findings |
| R54.5 wave-2 | same over `w2` | 23 readers, **25** findings, **12** sections with findings |
| R54.9 role mix / attack / seats | `json.load` of `.ufo/waves/round-54/w1-registry.json` | `reviewer: 5`, `attack_seats 21`, seats 76 → 27.6 % |
| R54.9 staged entries | `find …/merge/tameshi/knowledge -name '*.md' \| wc -l` | **81** |
| R54.4 pinned c2 digest | `freeze.json@077d431e`, key `c2/measure.py` | `8528ee8555da068519af4159f5f9e0efac8b29de88a53534a7043d7ec007e790` |
| R54.10 controls-a | `controls-a.stdout` line 3 | `… rekeyed=0/7 …` |
| R54.2 amendments | `freeze.json@077d431e` | `[1,2,3,4,5]` |
| R54.3 receipt | `.ufo/evidence/round-54/before/c2.stdout` | `total=13` |

All match the corrections section's corrected column. The corrections section's **values** are right; what is missing is the recurrence account around them.

---

## 6. What is *not* overlap (checked, so the sweep is visible)

| earlier row | checked against | result |
|---|---|---|
| R51.1 registry gate made unsatisfiable | R54.1–10 | **no duplicate** — no R54 row is about a registry row lagging its tool |
| R51.3 stale runner line pointers | R54.7 | **family** (pointer vs verb); not a duplicate |
| R51.4 round21-measure hermeticity | all | no duplicate |
| R51.5 C3 mutation attack never ran | all | no duplicate |
| R52.1 cold-read re-key debt | R54.1 | no duplicate — round 54's C1 is a new claim (57→64 credited), not a record-falsehood row |
| R52.2 LOG.md round-52 entry missing | R54.8(b) | **fixed** — `LOG.md:2444` has `## 2026-10-27 — round 52 …` at base; no R54 row |
| R52.5 `/tmp` hardcode in `registry-check.py` | R54.x | **fixed by round 53** (`tmp_hits=0` in round-53's C2 and round-55's `tmp_mkdirs=0`); no R54 row |
| R52.6 report-contract items | R54.6 | **family** — R52.6(c) is the opposite error (report said "not committed" while committed); not a duplicate |
| R53.6 CR47 exit class in 4 of 7 tools | R54.x | **not a R54 row** — but see §7 row 5: round 54 marked it FIXED and its instrument could not see the residual that round 55's C2 now measures |

---

## 7. What this feeds: proposed `## Mistakes` rows

The round-55 lesson draft already carries two rows (a control scored at a revision that predates the work; a predicate defeated by a line break). These are the rows the overlap analysis adds. Style matches the draft.

- **class: `routed-defect-marked-FIXED-while-its-class-returned-in-the-same-round`.**
  evidence: round 54 marks R53.3 FIXED by committing `control/controls-b.stdout`
  (`corpus/lessons/round-54.md:108-110`) and R53.5 FIXED with "no amendment is
  recorded" (`:114-116`); the same round's records are R54.1 and R54.2, and its
  `freeze.json@077d431e` holds 5 amendments. Five of the six earlier instances this
  seat traced were closed as FIXED, none fully.
  captured-by: none — a disposition table is written by the author of the fix and
  no arm re-reads the round's own new records against the receipt it just committed.
  fix: the round-55 corrections section names, per `ER-R54-N`, the artifact that now
  contradicts the old sentence (it does); the Mistakes row states the recurrence count
  (9 of 10 rows; 5 earlier FIXED verdicts that were partial), so the next closure can
  distinguish a repeat from a new class.

- **class: `routed-defect-dropped-without-disposition`.**
  evidence: `R52.3` (a count must be re-derived under a written counting rule) is named
  by no later lesson — `R52\.[1-6]` counts: round-53 lesson 3 (R52.1 ×2, R52.5), round-54
  lesson **0**, round-55 draft **0** — and the class returns as R54.5 and R54.9.
  captured-by: none; each round dispositions only the previous round's rows, so a row
  routed two rounds back falls out of scope silently.
  fix: the round-55 dispositions section carries R52.3 for the first time (or records it
  as deliberately dropped with a reason); the `## Gate`/disposition rule should cover the
  last two closures' open rows, not only the last one.

- **class: `one-class-routed-many-times`.**
  evidence: R54.3 / R54.4 / R54.10 are one class (a quoted value or digest the named
  artifact does not print); R54.5 / R54.9 are one class (a count never derived). Ten rows,
  seven classes.
  captured-by: none — the closure counts rows.
  fix: the corrections section keeps its per-row keys (a receipt per fact is right) and
  the Mistakes row records the class count so "ten defects" is not read as ten mechanisms.

- **class: `instance-fix-without-a-class-check`.**
  evidence: uncommitted round work at closure, three consecutive rounds — R52.4
  (`round-52-verifier-spotcheck.md:86`), R53.9 (`round-53-verifier-spotcheck.md:86`),
  R54.6 (`round-54-verifier-spotcheck.md:118`); each instance is committed
  (`git cat-file -e` TRACKED at `d33053f7` and `0a2010a`), and neither round's
  `no-harm.sh` has a clean-tree monitor, so round 54 measured on a dirty tree.
  captured-by: the closures' `git status --porcelain`, which is not a lane gate.
  fix (for the round-56 contract, not for this round's frozen bytes): a no-harm monitor
  `NOHARM tree-clean $(git status --porcelain | wc -l) $s` with `s=ok` only at 0, or the
  equivalent in the commit-then-push step. I am not patching `no-harm.sh` this round: it
  is frozen in `.ufo/evidence/round-55/`.

- **boundary row (not a R54 defect): `claim-wider-than-the-instrument`.**
  evidence: round 54's C2 arm read `text = (proc.stdout + proc.stderr).decode(...)`
  (`.ufo/evidence/round-54/c2/measure.py`, my read of `:60-110`) and asserted
  `unusable_exit2` + a naming match, so its claim "seven tools share one scratch-root
  exit class" held while `after/c2.stdout` shows `repeat-control: setup: RuntimeError: …`
  and `SELFTEST: FAIL (setup error: RuntimeError: …` — two of seven outside the grammar.
  Round 55's C2 measures exactly that residual (`grammar=6/8`).
  captured-by: none — the claim and the arm were written together.
  fix: the round-55 C2 claim already states the grammar and the stream; the Mistakes row
  records that R53.6 was called FIXED on an arm that could not see it, so the next round
  does not treat "exit code correct" as "class correct".

---

## 8. Receipts (command → file)

| receipt | command |
|---|---|
| `controls-b.stdout` | `git show 0a2010a:.ufo/evidence/round-54/control/controls-b.stdout \| grep -n 'CTL_MISMATCH\|CONTROLS_B\|CTL_POS_c1'`; `…controls-b.exit`; `git show 0a2010a:SCORECARD.md \| grep -n 'each printed false'` |
| `freeze-and-total-pointers.stdout` | `git show 0a2010a:SCORECARD.md \| grep -n '7883e0e5\|fe70474d\|097985c1\|077d431e'` and `grep -n 'total=14\|total=6'` |
| `freeze53-pointers.stdout` | `git show 0a2010a:SCORECARD.md \| sed -n '2495,2506p'`; `git show 0a2010a:LOG.md \| grep -n 'e62d9971\|cf872769\|7d8aaac6'` |
| `uncommitted-work-chain.stdout` | `git cat-file -e d33053f7:<p>` / `0a2010a:<p>` for the R52.4 and R53.9 path sets |
| `r531-and-counter-bytes.stdout` | `git grep -n 'total=37' 0a2010a -- .ufo/evidence/round-53`; `git show 0a2010a:.ufo/evidence/round-54/c1/measure.py \| grep -n 'ls-tree'`; same for round 53 |
| `tools-scratch-surface.stdout` | `git show 0a2010a:tools/{repeat-control,context-capture,registry-check,env-diff}.py \| grep -n 'RuntimeError\|ScratchRootUnusable\|could-not-evaluate'` |
| `r536-partial-fix.stdout` | `git show 88afa941:tools/{repeat-control,context-capture}.py \| grep -n 'ScratchRootUnusable\|raise RuntimeError'`; round-54 `before/c2.stdout` and `after/c2.stdout` |
| `routed-line-anchors.stdout` | `git show 0a2010a:corpus/lessons/round-5{1,2,3}-verifier-spotcheck.md \| grep -n '<R-ids>'`; `git grep -n 'counting rule'` |
| `r545-r549-rederive.stdout` | python recount of `w1/w2/*Read*.json` findings; `json.load` of `w1-registry.json`; `find …/merge/tameshi/knowledge -name '*.md' \| wc -l` |
| `disposition-coverage.stdout` / `disposition-coverage2.stdout` | `git show 0a2010a:corpus/lessons/round-5{3,4}.md \| grep -n 'R52\.[1-6]'`; `grep -c` on the round-55 draft |
| `round54-dispositions.stdout` | `git show 0a2010a:corpus/lessons/round-54.md \| sed -n '96,132p'` (the full R53.1–R53.9 disposition block) |
| `r54-line-anchors.stdout` | `git show 0a2010a:corpus/lessons/round-54-verifier-spotcheck.md \| grep -n '^\*\*R54\.'` |
| `r544-r547-r5410-values.stdout` | `controls-a.stdout`; `freeze.json@077d431e` c2 digest; fleet report `grep -n '097985c1…'` |
| `predecessor-quotes.stdout` | the six verbatim predecessor lines (`round-5{2,3}-verifier-spotcheck.md` :79,:80,:82,:85,:86 and round-51 :116) |
| `no-harm-tree-monitors.stdout` | `git show 0a2010a:.ufo/evidence/round-54/no-harm.sh \| grep -n 'porcelain\|clean\|untracked'`; same for `631cd64:…/round-55/no-harm.sh`; `clean-tree-after.txt` |
| `freeze-amend-and-c2-arm.stdout` | `freeze.json@077d431e` amendments; round-54 `c2/measure.py` unusable arm |
| `r542-pointer-crosscheck.stdout` | `git show -s --format='%H %s' 7883e0e5`; `git show fe70474d:.ufo/evidence/round-54/freeze.json` and `097985c1:…` amendment counts; `git show 0a2010a:corpus/lessons/round-54.md \| grep -n 'total=6\|SCORECARD quote'` (empty) |
| `round55-noharm-and-log.stdout` | round-55 `no-harm.sh` monitor labels; `LOG.md` round-52 entry |
| `registry-shape-and-c2-arm.stdout` | registry `rows` shape and the seven `scratch_root` cells; round-54 c2 `run_tool` |

---

## 9. Limits

- The matrix is a **class** judgment. Two rows are one class only if the same failure of the record produces both; R54.7 is the honest counter-example and I left it unclassified rather than stretch the fit.
- "Fixed by" is read from the disposition text the round filed, not from the fix's effectiveness. Where the two disagree I quoted both (chains A, B, C).
- I read round-51's class from its **quality verdict**, not from a routed R-number: round 51 did not route "false record left in place" as `R51.x`; it was named in the trend verdict at `:116`. Counting it as a routed row is a mild extension of the word "routed" and I say so here.
- R53.7/R53.8 remain "family" only; if the L1 prefers a wider definition of duplicate, the recurrence count rises to 10 of 10, and I would record it as 10-of-10 with the caveat rather than silently widening.
- No counter was executed; no frozen byte was edited; no lane production file was touched. Scratch under `/fast/scratch/hyaku/tameshi-r55/T55W1Connector2` was removed on exit.

Tooling: no installs or upgrades were needed; nothing was written to any PATH directory.
