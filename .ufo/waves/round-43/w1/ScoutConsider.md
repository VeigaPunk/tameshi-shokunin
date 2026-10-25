# ScoutConsider — considerthese inventory, and the one survivor-classification proposal

Seat: `L1Tameshi43.ScoutConsider` (scout, leaf). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Revision read: freeze `17f6ef0c72ec27e1aea305b5c95806b43bb2caef` (`git rev-parse HEAD` = same).
Method: read all five files in `considerthese/` (23 proposals total: 4 + 4 + 5 + 5 + 5); every
lane claim below is `git show 17f6ef0c:<path>` (read-only) with file:line. No counter was run
(this seat measures records, not claims), no tool was installed, and nothing outside this
report file was written. `considerthese/` was not edited.

Status vocabulary: a proposal's "status line" is the sentence a later reflection's
`## Status of (yesterday's|earlier) ideas` section devotes to it. A proposal with no such
sentence has never been triaged, whatever the tree contains.

---

## 1. Every proposal and its status line

### `considerthese/2026-10-19.md` (4 proposals; this file has no status section of its own)

| Line | Proposal | Status line that exists | State now |
|---|---|---|---|
| :34 | Contract-debt tracker | **none** — phrase occurs exactly once, at its definition | partly built elsewhere: standalone `## Capabilities`/`## Saturation`/`## Planned`/`## Retired` (`SCORECARD.md:236,253,264,281`) and round-43 C2 class m12 checks the newest round block carries `**Planned (round N+1):**`; the "how many days each has been open" aging report does not exist |
| :36 | Read-only pin drift check | `considerthese/2026-10-20.md:53`: "The read-only pin drift check (idea 2) is now largely covered inside the lane by `tools/pin-disposition.py` (round 13); I would only re-report its output, not duplicate it." | closed (covered) |
| :39 | PR hygiene watch | `2026-10-20.md:55`: "The PR hygiene watch (idea 3) is still relevant: PR #1 is still an open draft and has fallen further behind `master`."; `2026-10-22.md:61`: "PR hygiene (2026-10-19, idea 3) still applies: PR #1 is an open draft and far behind `master`." | open; last triage 2026-10-22 |
| :41 | Receipt resolution audit | **none** | landed in counter form: round-42 C1 classes m8 (path cites resolve) and m11 (revision reachability), carried into round-43 C2 (`contract.json` `claims.C2.classes.m8/m11`) |

### `considerthese/2026-10-20.md` (4)

| Line | Proposal | Status line | State now |
|---|---|---|---|
| :59 | Routed-defect ledger across rounds | `2026-10-22.md:59`: "The routed-defect ledger (2026-10-20, idea 1) is more relevant than before: the round-26 closure alone routes seven items, one of them (the `--regression` leg-sum check) knowingly deferred, and kumitate owner findings keep accumulating." | open — `git grep -iE "routed-defect ledger\|routed items ledger\|routed queue" 17f6ef0c`: 0 hits |
| :63 | Lead with the outside verdict, not the lane's self-verdict | **none** | open (authoring practice; unverifiable in-tree) |
| :66 | Scalar-versus-capability drift flag | `2026-10-22.md:57`: "…is now handled inside the lane: depth moved, and the closure itself runs a drift sentinel on repeated axis claims. I would only re-report it." | retired (handled in-lane) |
| :70 | Seat-attrition and credited-work tracker | **none** | partly: round-22 callback-authoritative wave accounting (`corpus/knowledge/callback-authoritative-accounting.md`) and QUALITY criterion 78 (wave-parent settlement); no standing dispatched/died/credited line per round |

### `considerthese/2026-10-22.md` (5)

| Line | Proposal | Status line | State now |
|---|---|---|---|
| :65 | Cover every day since the last reflection | `2026-10-23.md:56`: "no day was missed this time; today's window is stated above." | adopted as practice |
| :67 | Cold-read coupling map | `2026-10-23.md:57`: "the lane now does this itself (ReviewRoutedR30 counted 270 of 456, round 32 recounted 282 of 480), and it drove the outside-tool route. Retired." | retired |
| :70 | Ledger diversity readout | `2026-10-23.md:59`: "more relevant. Depth has sat at 9 for six rounds, all three recent cases are kumitate JS, and one slot remains under the cap of 10."; `2026-10-24.md:59`: "still open; I did not re-measure depth in this pass." | open |
| :72 | Lane verdict versus closure outcome table | `2026-10-23.md:61`: "more relevant. Six closures landed in about 24 hours, and only rounds 29 and 31 had a claim verified." | open — `git grep -iE "closure outcome\|verdict-vs-outcome\|vs closure"`: 0 hits |
| **:75** | **Survivor reclassification tracker** | **none, in any file** | **open, never triaged — the pick (§2)**. The round independently built the label half from C1 (criterion 83 + `r43-survivor-resolution-rule.md`, worktree); the register/overturn-rate half is still absent |

### `considerthese/2026-10-23.md` (5)

| Line | Proposal | Status line | State now |
|---|---|---|---|
| :66 | Instrument-churn readout | `2026-10-24.md:54`: "more relevant … the useful readout is churn per round next to the closure outcome." | open |
| :69 | Carried-queue aging | `2026-10-24.md:56`: "one item resolved cleanly. `code_view` ANSI-C was routed r35 → r36 → landed r37." | open (one item of the queue closed) |
| :72 | "Runnable here" check for claimed capabilities | **none** | open |
| :75 | Provider-filter seat deaths watch | **none** | open |
| :78 | Closed head versus reported head | `2026-10-24.md:57`: "the round-33 closure flagged it itself (two commits after the report, two untracked seat reports); rounds 35 and 36 were clean and pushed at closure. Handled inside the lane now; retired." | retired |

### `considerthese/2026-10-24.md` (5 — all five mined by the lane; no status section is owed)

| Line | Proposal | Where it landed |
|---|---|---|
| :63 | Pin blast-radius report before a tool edit | QUALITY criterion 80, `corpus/QUALITY.md:967-999` ("`considerthese/2026-10-24.md` proposal 1, mined 2026-10-25, not edited"); `LOG.md:2141` |
| :66 | Unreachable-provenance check | QUALITY criterion 76 + round-43 C2 m11; `corpus/lessons/round-38.md:86-89` ("proposal 2, 'Unreachable-provenance check' … becomes QUALITY criterion 76"); `LOG.md:2036` |
| :68 | Persistently unreachable sources | QUALITY criterion 79, `corpus/QUALITY.md:944-965` ("proposal 3, mined 2026-10-24, not edited") |
| :70 | Attempt and dispatch health per round | QUALITY criterion 78, `corpus/QUALITY.md:931-942` ("proposal 4, mined 2026-10-24, not edited") |
| :73 | SHONEN promotion readiness | mined as a four-box table, `corpus/lessons/round-42.md:142-156`; `LOG.md:2208` |

---

## 2. The one still-unimplemented proposal closest to this round's claims

**`considerthese/2026-10-22.md:75-76`, proposal 5 — verbatim:**

> 5. **Survivor reclassification tracker.** Record each survivor's first label (suite hole or equivalent) and any later relabel by a
>    closure or by the F8 anchored probe, so the lane's "suite hole" calls get a measured overturn rate.

Why this one, over the other 11 still-open proposals (23 total: 11 closed or landed, 12 open, this one among them):

- It is the only proposal in the corpus that names **survivor labels** at all, and round 43's C1 is exactly a relabel event: the two
  round-42 survivors move from unclassified-survivor to `killed` (`outflag_no_parse_args_check`, by `F11_outflag_namespace`) and
  `dead_code_only` (`method_fold_several_returns`) under the pre-declared K/D/E/U rule (`contract.json` `claims.C1.rule`).
- It is simultaneously a **record-agreement** object (C2's axis: a register whose rows must agree with the records that declared and
  decided them) and an **id-registry** object (its key is the declared mutant id in `.ufo/evidence/round-42/census/mutants.json`).
  Of the open proposals, only this one touches all three claim areas of the round.
- It was written the same day an overturn was narrated but not counted: `considerthese/2026-10-22.md:19` records "the closure agreed
  that one round-26 survivor (`S_EMPTY_GUARD`) is equivalent, not a suite hole", and line 46 records the four cite-check survivors
  re-judged at F8. Both are relabel events living only in prose — exactly what the tracker would key and count.

Evidence it is still unimplemented:

```
$ grep -rF -c "Survivor reclassification tracker" considerthese/
considerthese/2026-10-22.md:1          # its own definition, and nothing else
$ git grep -iE "survivor (register|ledger|index|tracker)|overturn rate|first labelled" 17f6ef0c -- corpus SCORECARD.md LOG.md SKILL.md
17f6ef0c:corpus/lessons/round-16.md:110:- RX1 first labelled the preamble (a record) `executed-ok`.   # unrelated in-round label
$ git grep -c -i "overturn" 17f6ef0c -- corpus SCORECARD.md LOG.md SKILL.md
17f6ef0c:corpus/lessons/round-39-verifier-spotcheck.md:1      # prose: "does not overturn the gate"
$ git show 17f6ef0c:corpus/QUALITY.md | grep -c "Criterion 83"
0
```

And the omission is in the reflections themselves: the immediately following file's status section
(`considerthese/2026-10-23.md:56-62`) covers 2026-10-22 ideas 1, 2, 3 and 4 and stops before 5; `2026-10-24.md:54-59` never
mentions it either. No text records a decision to defer or refuse it.

**Worktree note (same day, after the freeze — read, not relied on for any claim above).** While writing this report the lane
worktree already carried this round's own records, uncommitted: `corpus/QUALITY.md` now has **criterion 83** ("a survivor is
classified, never relabelled") and **criterion 84** (census-pattern counting), and `corpus/knowledge/r43-survivor-resolution-rule.md`
exists with a table "The two round-42 survivors, resolved" (columns `Mutant | Round-42 outcome | Round-43 verdict | Evidence`) plus a
`corpus/README.md:548` row. That changes the *residual* gap, not the pick: the lane has independently built the **label vocabulary**
half of the proposal this round (from C1, not from the proposal: the round-43 `LOG.md` section now in the worktree carries no `considerthese:` line) but not the **tracker**
half: no register keyed by `(gate, mutant id)`, no per-survivor history, no computed overturn rate. The free QUALITY slot is now **85**,
and criterion 83's title must be read before landing anything here (see §4).

---

## 3. What the lane already implements (freeze `17f6ef0c`, plus the round-43 worktree where marked)

The parts of the proposal the lane already has, and where:

1. **Per-gate survivor lists with measured classes.** `corpus/knowledge/fleet-kill-rate-ledger.md:43` header
   `| # | Gate (owner · file) | Suite (at sweep) | Kill-rate (composition) | Survivors (measured classes) | Hardened | …`; rows 45-48 list each
   survivor with its class (e.g. "B5 deleted exec x-bit arm (fixture-absent / unreached arm)").
2. **Two in-cell relabels in the ledger** — the lane does record some label changes, inside the gate row rather than in a survivor register:
   - `fleet-kill-rate-ledger.md:47` (row 3) `Hardened` cell: "**yes, owner** (lane S5-1): 26 → 35 cases at `aae45531`; replay of the 4
     survivors: **B10 killed, B7/B8/B9 still survived**";
   - `:48` (row 4): "**yes, owner** (lane M6-1): +88/−0 … 28 → 53 assertions at `c4c1afb7`; **same spec re-run: 10/10 (100 %)**"
     (all six listed survivors killed).
3. **A per-survivor class table against expectations fixed outside the mutated code** (frontier F8):
   `corpus/knowledge/oracle-anchored-survivors.md:45-52`, four rows with a `class` column (`anchored-hole` all four), plus the
   negative-control paragraph that shows the probe fails when the anchor is unsupported.
4. **One suite-hole→anchored-hole relabel pair** — recorded, but only as prose across two documents, never joined by survivor id:
   `corpus/knowledge/mutation-case-kumitate-cite-check.md:85` "## 4. Survivors — four suite holes, one equivalent mutant" and `:93`
   (`S_EMPTY_GUARD` → **equivalent**), against `corpus/knowledge/oracle-anchored-survivors.md:10` "Round 26 called four of the five
   `cite-check.mjs` survivors suite holes" and the re-judgment to `anchored-hole`.
5. **The vocabulary a label must be drawn from:** QUALITY criterion 82 (`corpus/QUALITY.md:1023-1043`: a kill is a completed run with
   a failed check, a crash is not a kill), `corpus/knowledge/pit-outcome-vocabulary.md`, and the round's own K/D/E/U rule in
   `.ufo/evidence/round-43/contract.json` `claims.C1.rule`.
6. **This round's two first labels, already written down:** `SCORECARD.md:2040-2042` and `corpus/lessons/round-42.md:216-219` —
   `outflag_no_parse_args_check` "killable only by a fixture that registers `--out` and reads `.out` off a non-parse_args object";
   `method_fold_several_returns` "differs only on dead code".
7. **This round's own verdict record (worktree, uncommitted).** `corpus/knowledge/r43-survivor-resolution-rule.md` states the K/D/E/U
   rule and, under "The two round-42 survivors, resolved", a table `Mutant | Round-42 outcome | Round-43 verdict | Evidence` with one
   row per mutant — that is a first-label → later-verdict record for these two, kept inside a knowledge entry rather than a register.
   Its consequence 1 is "**A survivor is never relabelled.** D and E are named classes with their own evidence; dropping a survivor
   from the declared set is not a verdict under this rule." QUALITY criteria 83 and 84 (same worktree) encode the rule and the
   census-pattern rule; `corpus/README.md:548` carries the coverage row.

What is absent is the tracker, not the vocabulary: no register keyed by `(gate, mutant id)` that survives the lesson rotating, no
first-label column for survivors outside this round, and no computed overturn rate. Counting relabels today means reading
`fleet-kill-rate-ledger.md:47-48`, `mutation-case-kumitate-cite-check.md:85,93` against `oracle-anchored-survivors.md:10`,
`r43-survivor-resolution-rule.md`'s table, and every lesson by hand — which is the cost the proposal exists to remove.

---

## 4. Two corrections to carry into any landing, and a landing sketch

**Correction 1 (label space).** The proposal's label space is two-way — "suite hole or equivalent". Round 43's declared rule has four
classes (K/D/E/U), and the two survivors land in **K** and **D**; neither is `equivalent` (E is expressly "reserved; not reached this
round", `contract.json` `claims.C1.rule.E_equivalent`). A criterion transcribed literally from the proposal would have no column for
this round's own outcome. The landing must key on the declared vocabulary.

**Correction 2 (it is not a licence to relabel).** Criterion 83 in the worktree reads "a survivor is classified, never relabelled",
and `r43-survivor-resolution-rule.md` consequence 1 repeats it. That fixed the flattering direction — no dropping a survivor, no
`equivalent` by assertion. It must not be read as forbidding an evidence-backed verdict *transition*: the two round-42 survivors
themselves moved from `survived (4/6)` to K and D. The tracker is criterion 83's complement, not its rival: 83 fixes what a label may
be and what evidence it needs; the tracker keeps that evidence attached to the mutant id across rounds and counts how often the lane's
own earlier calls were overturned. A criterion written as "record every relabel" without the deciding-input requirement would violate
83; one written with it implements the proposal.

**Sketch — the free QUALITY slot is 85** (at the freeze the last criterion was 82 at `corpus/QUALITY.md:1023`; the worktree has since
appended 83 and 84, uncommitted). The lane's established shape is
`### Criterion NN — <title>` + body + `Lesson:` + `Falsifier that must fail`, citing the proposal as "mined <date>, not edited"
(exactly as criteria 76, 78, 79, 80 do):

> ### Criterion 85 — a survivor's label change carries its first label and the input that overturned it
>
> Every change to a recorded survivor's class (`killed`, `dead_code_only`, `equivalent`, `unresolved`) is appended as a row keyed by
> gate and mutant id: the first label and the round that assigned it, the new label and the round that decided it, and the deciding
> evidence (fixture id or probe receipt). The ledger cell and the case note carry the same label in the same round; the overturn count
> is computed from the register, never asserted in prose. A relabel with no new discriminating input is not a relabel.
>
> Lesson: `corpus/lessons/round-43.md`; source `considerthese/2026-10-22.md` proposal 5, mined 2026-10-25, not edited.
> Complements criterion 83: 83 fixes the four verdicts and their evidence and forbids a drop or an asserted equivalence; this
> criterion keeps those verdicts attached to the mutant id across rounds and makes the overturn count a computed number.
> Falsifier that must fail: with a register row's deciding evidence removed, the check must report the row as unsupported and exit
> non-zero; at the milestone the register must hold `outflag_no_parse_args_check` `survived (4/6)` (r42, U under this rule) →
> `killed` (r43, `F11_outflag_namespace`) and `method_fold_several_returns` `survived (4/6)` (r42) → `dead_code_only` (r43). The
> first label is the record's own wording, not the round-43 name for it.

Its C2 audit form (if the lane wants it inside a counter rather than a lesson alone): a class `m14` requiring every register row's
first label to equal the class recorded by the declaring round, the new label to equal the class in the deciding round's counter
output, and every keyed mutant id to exist in `.ufo/evidence/round-42/census/mutants.json`. That binds the register to the same
record-agreement object m6–m13 already audit, and to the id discipline C3's guard enforces for staged rows.

---

## 5. Near-misses and why they lose

- **`2026-10-24.md:66` unreachable-provenance / `2026-10-19.md:41` receipt resolution** — the two closest "record agreement"
  proposals, and both are **already landed**: criterion 76 + C2 m11 (revision reachability) and m8 (path cites). Not unimplemented.
- **`2026-10-19.md:34` contract-debt tracker** — the closest open record-agreement proposal, but it reports SCORECARD placeholder
  age; the lane built the four sections and m12 covers the planned line, and it names no survivor, so it would not record the round's
  K/D outcome.
- **`2026-10-20.md:59` routed-defect ledger** and **`2026-10-22.md:72` verdict-vs-outcome table** — both open and both
  record-agreement, but they are queues/verdicts across rounds. Either could carry a later criterion; neither is survivor
  classification, and landing one now would not capture round 43's relabel.
- **`2026-10-22.md:70`, `2026-10-23.md:66,72,75`** — open, but on axes (ledger diversity, instrument churn, capability runnability,
  provider filtering) disjoint from this round's three claims.

## Remaining unknowns

1. Whether a tracker criterion (slot 85) lands at all, and in which round. At the freeze 83/84 did not exist; in the worktree they
   are uncommitted and `corpus/lessons/round-43.md` — which both cite — is not yet written.
2. Whether the operator treats the ledger's in-row replay cells (`fleet-kill-rate-ledger.md:47-48`) as a sufficient implementation of
   the proposal. I read them as partial: per-gate, no survivor key, no first-label column, no computed rate.
3. Whether `2026-10-23.md:56-62` skipping 2026-10-22 idea 5 was deliberate triage or an oversight. No text says, and the omission is
   the only evidence either way.
