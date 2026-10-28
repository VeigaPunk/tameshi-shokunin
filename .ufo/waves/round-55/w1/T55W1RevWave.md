# T55W1RevWave — self-audit of the round-55 wave-1 spec

Seat `T55W1RevWave`, reviewer, round 55 wave 1, milestone *self-audit of the wave*.
Spec audited: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/spec-w1.json`
(67 544 B, 75 items, built 13:39 2026-10-28 by `build-spec-w1.py` in the same directory).
Read-only audit: I edited no spec, no lane file, no frozen file. No tool installed
(nothing was needed; `python3` + `git` only, so the RULES.md install path was not entered).

Receipts (all under `.ufo/waves/round-55/w1/T55W1RevWave-receipts/`):

| receipt | what it holds |
|---|---|
| `audit-counts.txt` | all five checks in one `python3` pass over the spec + dispatch |
| `path-conformance.txt` | per-item absolute-path table, 75 rows |
| `distinctness.txt` | pairwise token Jaccard (2 775 pairs) + attack-target token scan |
| `edit-scope-sweep.txt` | every item that names a production/frozen path, with verb + guard |
| `collision.txt` | the six instruction clauses that name `T55W1Er10.{json,md}`, byte evidence, and the broken producer/consumer edge |
| `collision-recurrence.txt` | occurrence 2 at 14:01:39: the `seat` field of the overwriter and byte identity with `T55W1ExecRekeyPrep.json` |
| `frozen-dirt.txt` | frozen-set state at 14:00, `before/c2.stdout` vs its HEAD blob, `freeze.json` re-derivation |
| `wave-dir-snapshot.txt` | `ls -la` of the wave dir at 13:59:45 |

---

## 1. Verdict table

| # | Check | Requirement | Measured | Verdict |
|---|---|---|---|---|
| A | seat count | v2 band 64–128 | **75** items; dispatch `spawn=75 resume=0 total=75`; policy `waveMinLanes=64 waveMaxLanes=128` | **PASS** |
| B | attack-role share | ≥ 25 % reviewer/critic/mutation-tester/labrat | **28/75 = 37.33 %** (reviewer 18, critic 6, mutation-tester 4; labrat 0) | **PASS** |
| C | distinctness + naming what it attacks | every item distinct, names its target | 75/75 unique names, 75/75 unique milestone strings, 75/75 unique item texts, 28/28 attack items name a target; **but** 45 pairs ≥ 0.60 token Jaccard (all inside Rev01–Rev10) and 9/10 R54 rows are covered twice | **PASS with reservation** (§4) |
| D | no frozen / production edit ask | no item instructs a seat to edit a frozen file or a lane production file | **0 hard violations** after adjudication of the 10 keyword hits (§5); 6 items do instruct writes to *another seat's* report path — that is finding F1 | **PASS on the stated criterion, FAIL on deliverable-path safety** |
| E | every item names absolute paths | absolute paths only | **55/75 conform; 20/75 violate** (8 relative-only, 12 name no path at all) | **FAIL** |

Findings by severity: **F1 HIGH**, **F2 MEDIUM**, **F3 MEDIUM**, **F4 LOW**, **F5 LOW**;
one out-of-item observation that must not be attributed to this spec (§9).

---

## 2. Check A — seat count (PASS)

```
$ python3 -c "…" over spec-w1.json and w1-dispatch.json
spec items           : 75
dispatched (spawn)   : 75 resume: 0 total: 75
dispatch policy band : waveMinLanes= 64 waveMaxLanes= 128
v2 band 64<=N<=128   : True | items==dispatched: True
```
(`audit-counts.txt` §A.) Cross-checked against the harness's own bookkeeping:
`swarm-registry.json` `members` = 75 with the identical role histogram, and
`w1.ready.partial` carried 60 seat→agent keys at 13:59:45 (the wave was still ramping;
`rampBatchSize 5`, `rampIntervalMs 700`, and `members[].agentId` is `null` for all 75 —
the registry records intent, not liveness). 75 sits 11 seats above the floor (64) and 53 below
the ceiling (128), so the wave is neither padded to the ceiling nor below the floor.

One shape note, not a defect: the wave is **build-heavy by instruction and draft-heavy by
output** — 15 of the 22 scribes are told to draft a piece of production text (2 say verbatim
"Draft only; the L1 lands it"), the other 7 verify and report read-only, and 17 executors
demonstrate the application on a clone. So the L1 is the serial integrator for roughly a fifth
of the wave. That is a design choice, not padding: each scribe's artifact is a distinct
production file.

---

## 3. Check B — attack-role share (PASS)

```
scribe             22   29.3%
reviewer           18   24.0%  ATTACK
executor           17   22.7%
critic              6    8.0%  ATTACK
mutation-tester     4    5.3%  ATTACK
scout               2    2.7%   sentinel 2   connector 2   revenger 1   simplifier 1
attack total       28   37.3%   pass=True
labrat role present: False
```
(`audit-counts.txt` §B.)

- 37.33 % is comfortably above the 25 % floor; the margin is 9 seats (28 vs the 19 needed).
- The audit set names `labrat` but the spec's vocabulary has no `labrat` role: the two lab-style
  probes (`T55W1LabMode`, `T55W1LabEmpty`) are filed as `mutation-tester` and count in the
  attack share either way. This is a vocabulary mismatch in the audit criterion, not a
  shortfall in the wave — recording it so the next wave's checker does not read "labrat: 0"
  as a deficit.
- Attack coverage is *distributed*, not clumped: the 28 attacks land on 3 of the 4 axes
  (**calibration 21, operability 5, coverage 2** — no attack on freshness, which is carried
  by the no-harm and census executors) and on every artefact the round must land
  (both counters, the freeze, the deciding-run, the note, the registry cells, the two tool
  patches, the SKILL.md re-key, SOURCES rows, QUALITY 105/106, the spec itself).

---

## 4. Check C — distinctness and naming what it attacks (PASS with reservation)

**Uniqueness is total:** 75 unique `name`s, 75 unique `milestone` strings (no milestone has
two owners), 75 unique `item` texts (byte-distinct, verified by set cardinality).

**But the ten row-reviewers are one template.** Pairwise token Jaccard over the 75 items
(2 775 pairs) returns 45 pairs ≥ 0.60 — and **all 45 are ≥ 0.927** (max 0.963); every one of
them sits inside Rev01–Rev10, e.g. `Rev06 ↔ Rev10 = 0.963`, `Rev03 ↔ Rev09 = 0.963`. The only
varying tokens are the two `R54.N` ids. That is defensible on its merits (see below) but it means the
"distinct" criterion is met *lexically*, not structurally: a reviewer cannot tell its item
from its neighbour's without diffing the two row ids.

**Row coverage is deliberately redundant and complete:**

```
R54.1  Rev01 Rev06      R54.6  Rev03 Rev09
R54.2  Rev01 Rev07      R54.7  Rev04              <- single-covered
R54.3  Rev02 Rev09      R54.8  Rev04 Rev10
R54.4  Rev02 Rev08      R54.9  Rev05 Rev07
R54.5  Rev03 Rev06 Rev10  R54.10 Rev05 Rev08
rows covered >1x: [1,2,3,4,5,6,8,9,10]   rows never covered: []
```
No row is orphaned; nine of ten are double-blind, R54.5 is covered three times (it is the
row whose value the C1 counter derives from a committed reader census, so it is the most
error-prone), R54.7 once. On the **lowest non-retired axis (calibration 8)** this redundancy
is the right way to buy detection, so I do **not** reject Rev06–Rev10 as padding — and I say
that having measured that they are the most copy-pasted items in the wave.

**Naming what it attacks:** all 28 attack items name a falsifiable target — an `R54.N` id
plus the receipt that decides it (Rev01–Rev10), the spotcheck itself (RevR54Honesty), a
frozen counter path (CritC1, MutC1, MutC2), `freeze.json`/`contract.json`/`deciding-run.sh`
(CritFreeze, CritGate), the credit machinery (RevColdread, RevLedger, RevRekeyByteProof),
the note/QUALITY/SOURCES artefacts (RevNote, RevQuality, RevSources), a mode inventory
(LabMode, LabEmpty, ScoutModes), or the wave (RevWave). Three name their target only by
description and not by path (`RevNote` "the drafted section", `LabMode` "the five modes the
counter calls lazy", `ScribeScratchDoc` "the note or runbook") — see F2/F3.

**F5 (LOW) — three build deliverables have no attacker.** Inverting the cross-reference map:
every artefact that C1 or C2 *measures* has a dedicated attacker, but the prose artefacts do
not. `T55W1ScribeLog` (LOG.md entry, item 16), `T55W1ScribeLesson` (round-55 lesson, item 13)
and `T55W1ScribeScorecard`'s round-55 *block prose* (item 17; only its corrections half is
attacked, by Rev01–Rev10 and RevR54Honesty) have no reviewer, critic or mutation-tester.
Their only check is the counter reading them indirectly, and the counters do not read LOG.md
at all. On a round whose whole thesis is "records must agree with the tree", the LOG entry is
the one artefact nobody re-derives. That is a coverage gap, not a padding finding — the items
should stay and one attacker each should be added (a cheap one: extend item 21's sweep (3) to
the round-55 LOG entry, and let RevColdread own the lesson file, since it already reads the
SKILL.md section the lesson cites).

---

## 5. Check D — no item asks a seat to edit a frozen file or a lane production file (PASS)

Method: for every item, find any production path (`SKILL.md`, `SCORECARD.md`, `LOG.md`,
`corpus/`, `tools/`) or frozen path (`.ufo/evidence/round-55/`), then classify the governing
verb and look for a draft-only / scratch-clone / read-only / never-edit guard.
Receipt: `edit-scope-sweep.txt` — 50 items name such a path; the classifier flagged 10 for
manual adjudication; **all 10 clear on reading the clause**:

| item | flagged because | adjudication |
|---|---|---|
| T55W1Er01/02/03 | "Draft: the exact old->new text … Write `…/T55W1ErNN.json`" | the write is to its *own report*; the production text is drafted, never landed. PASS |
| T55W1ScribeSkill | "Draft the exact old->new replacement … Touch NOTHING else" | explicit no-touch; PASS |
| T55W1ScribeCells | "Draft one replacement cell text per row … Write `T55W1Er10.json`" | drafts only (and see F1 for the filename) |
| T55W1ScribeLog | "Draft the `## 2026-10-28 - round 55` LOG.md entry" | draft only; PASS |
| T55W1ExecCensus | "run it against a **scratch copy** of the lane's corpus" | scratch copy; PASS |
| T55W1RevSources | "Report per row: admit/reject" | read-only; PASS |
| T55W1RevColdread | "read the SKILL.md `## Standing rules` edit" | read; PASS |
| T55W1CritClaimShape | "does the C1 record edit damage freshness?" | question, not instruction; PASS |

The fourteen items that *do* mutate production text (22, 23, 24, 25, 26, 27, 28, 29, 30, 34,
55, 56, 69, 71) all say "in a scratch clone at `631cd645…`" / "in scratch copies" / "copy,
never edit" — and item 72 says "copy the lane's `corpus/` to `$S/corpus`" — so the mutation is
demonstrated against a clone and the L1 lands it. Item 30's
"adapt `…/round-54/integrate/binder.py` in your scratch (it is frozen for round 54 — copy,
never edit)" is exactly the right instruction. **No item asks a seat to write a frozen file.**

Caveat that belongs to the *wave*, not the spec: seats nonetheless wrote one frozen file —
see §9. Nothing in the spec authorises it (`items containing a shell redirect onto
before/c2.stdout: []`), and two items are *harmed* by it (item 17 quotes
`before/c2.stdout`; item 31 `cmp`s against it).

---

## 6. Check E — every item names absolute paths (FAIL: 20/75)

The lane's own rule is "absolute paths only: seat tools start at the fleet root, so every
read/edit/write names an absolute path under the lane". Measured (`path-conformance.txt`):

- **55/75** items name at least one `/home/vgpnk/...` path. PASS.
- **8/75** name only lane-relative paths — `corpus/knowledge/scratch-root-contract.md`,
  `SCORECARD.md`, `SKILL.md`, `tools/registry.json`, `corpus/SOURCES.md`, `tools/scratch_root.py`:
  `T55W1ScribeMistakeSweep`, `T55W1ExecNote`, `T55W1ExecC1Full`, `T55W1ExecC2Full`,
  `T55W1ExecRekeyPrep`, `T55W1ExecModeDiscovery`, `T55W1Simplifier`, `T55W1CritSourcedClaim`.
- **12/75** name no path at all: `T55W1ScribeScratchDoc`, `T55W1ExecC1FixOnly`,
  `T55W1ExecGrammarBreak`, `T55W1RevNote`, `T55W1CritC2`, `T55W1ScoutModes`,
  `T55W1ScoutReceipts`, `T55W1Connector1`, `T55W1Connector2`, `T55W1LabMode`,
  `T55W1LabEmpty`, `T55W1CritClaimShape`.

Severity is MEDIUM, not HIGH, because the shared `context` block does name the lane root once
and most of the 12 still name their target by an unambiguous proper noun (`the seven tools`,
`the five modes the counter calls lazy`, `every receipt the round-54 spotcheck cites`). The
cost is real but bounded: a worker whose cwd is the fleet root must resolve a relative
`corpus/knowledge/...` against the lane by inference, and the two connector items reach into
*sibling lanes* (`kumitate`, `kagi`, `tsukuroi`, `mado`) whose roots are not given at all —
`T55W1Connector1`'s globs `scripts/*.mjs`, `corpus/*.sh` are resolvable only by guessing that
they belong to the sibling lane, not the tameshi lane, which is a genuinely ambiguous
instruction. My own item is the near-miss case: it names
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w1/../spec-w1.json`,
absolute but routed through `..`, instead of the canonical
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/spec-w1.json`.

Fix is mechanical: prefix the lane root in the 8 relative-only items, and give the 12
no-path items the absolute path of their target (for `CritC2`/`MutC2` that is
`…/.ufo/evidence/round-55/c2/measure.py`; for `ScoutReceipts` the spotcheck path; for the
connectors a `--root`-style absolute sibling path).

---

## 7. Findings

### F1 (HIGH) — six seats are told to write the same two report paths; the collision destroyed a seat's deliverable

`T55W1Er10.{json,md}` is the report path of seat **T55W1Er10** (item 9, R54.10 correction
draft). Five *other* items instruct their seat to write that same pair:

```
[ 9] T55W1Er10             (owner)          "…/w1/T55W1Er10.json` as {"id": "R54.10", …} … and the same facts in `T55W1Er10.md`"
[10] T55W1ScribeNote       draft only        "Draft only; write `T55W1Er10.md`."
[12] T55W1ScribeCells      cells             "Write `T55W1Er10.json` (row name -> new cell) and `T55W1Er10.md`."
[14] T55W1ScribeSources    source rows       "Write `T55W1Er10.json` (rows) + `T55W1Er10.md`."
[19] T55W1ScribeConsiderthese                "Write `T55W1Er10.md`."
[21] T55W1ScribeMistakeSweep                 "… and write `T55W1Er10.md` with the command and output for each:"
[29] T55W1ExecRekeyPrep                      "Write the JSON the L1's binder needs as `T55W1Er10.json`."
```
(`collision.txt` §A — six writers plus the owner; the string `T55W1Er10` appears in 7 items.)

This is not hypothetical. Observed in the live wave:

- At 13:56:04 `T55W1Er10.json` and `T55W1ScribeSources.json` were **byte-identical**
  (`sha256 21973e575585f7ea9b017fea89caa2b0eaf8ba3228b92a23997d739ee191ca27`, both 12 697 B)
  and `T55W1Er10.md` carried the sources report (`sha256 fbf17903…`, 12 400 B, first line
  `# T55W1Er10 — the sources C2's uniform-line claim rests on`).
- The seat that did it then filed its own admission and the only reason the data came back:
  `T55W1ScribeSources-receipts/peer-er10-restore.txt` — *"collision: seat T55W1ScribeSources
  wrote .ufo/waves/round-55/w1/T55W1Er10.{json,md} at 13:51-13:56 … overwriting seat
  T55W1Er10's own deliverables … recovery: the peer's exact write/edit payloads were read
  from its session log ~/.omp/agent/sessions/…/T55W1Er10.jsonl … replayed in order."*
- Restored at 13:58:54: `T55W1Er10.json` 3 640 B `sha256 2e15a6401a4aaa609dafd2feb0aabac170e743da0aecd106ee8cd6b824bfd45d`,
  `T55W1Er10.md` 11 366 B. Recovery was **by session-log replay**, i.e. by luck of a
  transcript, not by any property of the wave.
- **It happened again, from a different co-writer.** At **14:01:39** item 29's seat obeyed its
  own instruction ("Write the JSON the L1's binder needs as `T55W1Er10.json`") and wrote
  `T55W1Er10.json` = 11 908 B, `sha256 a70ea19db384b077a731fe20a99501a2ef097685a79db84f1db0e1c224abf7a5`,
  **byte-identical to `T55W1ExecRekeyPrep.json`**, whose own `seat` field reads
  `"T55W1ExecRekeyPrep"`. The R54.10 JSON draft is therefore **absent from the tree again**
  at 14:02:46, while its `.md` (13:58:54, 11 366 B) still survives. Receipt:
  `collision-recurrence.txt`. This is the decisive datum: the defect is not a one-off race
  between two seats but a property of the spec — *each* of the six co-writers that lands
  re-destroys the owner's file, and nobody is told to check first.

Two further consequences of the same defect, both verified:

1. **The producer/consumer edge is broken.** Item 24 (`T55W1ExecCells`) is told to
   "use the draft from `…/w1/T55W1ScribeCells.json` if it exists" — but item 12 told that
   scribe to write `T55W1Er10.json`. `ls T55W1ScribeCells.json` → *No such file or
   directory*; the cells exist only inside `T55W1ScribeCells-receipts/cells.diff`. The
   consumer's stated input never existed, so it silently fell into its "else derive the
   template yourself" branch (`collision.txt` §E).
2. **`T55W1ScribeCells` has no report at all.** Its milestone is "C2 registry cells"; the
   wave dir holds only its `-receipts/`. Its drafted cells survive, but the artefact the L1
   is told to integrate is unnamed.

Receipt for occurrence 2: `collision-recurrence.txt`.

Why it is HIGH: the clobbered path is the JSON that feeds the L1's
`## Round 55 - round-54 record corrections` section for **R54.10**, i.e. one of C1's ten
classes. It has now been destroyed twice in six minutes — restored once only by a peer's
goodwill, and lost again by the next co-writer — so at integration time the R54.10 JSON does
not exist and must be replayed from the session log a second time.

Fix: six one-line item edits — item 10 → `T55W1ScribeNote.md`, 12 → `T55W1ScribeCells.json`
+ `.md`, 14 → `T55W1ScribeSources.json` + `.md`, 19 → `T55W1ScribeConsiderthese.md`,
21 → `T55W1ScribeMistakeSweep.md`, 29 → `T55W1ExecRekeyPrep.json`; and item 24's dependency
then resolves to the path item 12 actually writes. The build script should assert
`len({path for item in items for path in deliverables(item)}) == len(items)` before dispatch —
one `re` over `Write \`(T55W1\w+\.(json|md))\`` and any `deliverable ⊄ {item.name` prefix}
fails the build. I am reporting this rather than patching it: `build-spec-w1.py` produced the
dispatched spec and the wave is live, so the L1 owns the decision; a repaired spec would need
a re-dispatch (75 seats), which is not mine to start.

### F2 (MEDIUM) — 20/75 items violate the absolute-path rule

See §6 and `path-conformance.txt`. Two of the 20 are *ambiguous*, not merely imprecise:
`T55W1Connector1` (relative globs into four sibling lanes, none of whose roots are given) and
`T55W1Connector2` (round-52/53/51 lessons given as bare `corpus/lessons/round-5N*.md` from a
cwd that is the fleet root). Both can be read as pointing at the *tameshi* lane, where
`round-5N` lesson files also exist — a worker taking the literal reading audits the wrong
repository and reports a clean sweep.

### F3 (MEDIUM) — items I would reject as padding (3)

| item | why padding | what to do |
|---|---|---|
| **`T55W1ScribeScratchDoc`** (item 20, scribe, operability) | No target file, no output path, no acceptance test. Its product ("a five-line operator snippet … how to parse the scratch-root class … what an empty TMPDIR means … cite the frozen grammar verbatim") is the same content as item 10's note section (a), (c) and item 53's critique of the same grammar. Three seats would restate one regex. | Drop, or fold one line into item 10 ("…and a five-line copy-pasteable parse snippet"). |
| **`T55W1ScribeSeat`** (item 18, scribe, calibration) | Duplicates item 8 (`T55W1Er08`, R54.8) on two of its three deliverables: item 8 asks for "(a) the superseded annotation to append to `…/T54W1ExecStraceNoise.md` … (b) the incident paragraph for the lesson, containing `config.yml` and `fabricated`"; item 18 asks for "(a) a short, appended `SUPERSEDED` block for the end of that file … (b) the paragraph for the lesson naming the incident (`config.yml`, `fabricated` …)". Only 18's (c) — the lane rule — is new. | Merge 18's (c) into item 8 and drop 18; two scribes drafting one annotation is exactly the lost-update pattern of F1 without the collision. |
| **`T55W1CritClaimShape`** (item 68, critic, calibration) | The only attack item that asks for **no command**: "Report a verdict per question with the evidence you read." Every other attack item names a counter, a clone, a mutant or a fixture. Its five questions are already owned: separability and the axis choice are fixed by the frozen `contract.json` (which the L1 froze before any seat ran), the freshness cost is measured by item 50 (`RevColdread`) and item 29 (`ExecRekeyPrep`), and "name any claim you would reject" is what 52/53/74 already do with commands. Downstream of the rule *"a finding without a command and its output is not a finding"*, this item can only produce opinions. | Drop, or convert it into one executable check: "run both counters with the other claim's artefacts absent and show each still reaches its target" (a real separability test, and nobody has it). |

Together: 3 of 75 items (4 %) removed, none of them on a critical path, no milestone orphaned.

### F4 (LOW) — the Rev01–Rev10 template identity (no action required)

45 pairs at Jaccard ≥ 0.927, all within the reviewer block; 9/10 rows double-covered, R54.7
once, R54.5 thrice. I keep these because double-blind re-derivation on the lowest axis is the
cheapest detection the round can buy, and the *assignments* differ (different receipt → different
command → independent value). Recording the number so a future wave does not read "75 distinct
items" as "75 distinct problems".

### F5 (LOW) — three prose artefacts with no attacker

See §4: LOG.md entry (16), round-55 lesson (13), round-55 SCORECARD block prose (17) — the
counters do not read LOG.md, and the lesson is only mined, never refuted. Add one attacker
each rather than one more reviewer of the same ten rows.

---

## 8. Residual risk this audit cannot remove

- **The spec was audited while it ran.** 60 of 75 seats were up at 13:59:45 and files were
  being rewritten under me (the Er10 pair twice, `before/c2.stdout` three times). Every count
  in this report is a snapshot; `audit-counts.txt`, `path-conformance.txt` and
  `distinctness.txt` are deterministic functions of the spec file, which did not change
  (mtime 13:39, size 67 544 B at both reads), so A/B/C/E are stable; D's live-state evidence
  in §9 is time-stamped.
- **Checks A–E are structural, not semantic.** I verified that every item names a target and
  a distinct milestone; I did not verify that each item's *stated* premise is true. Item 14's
  premise, for instance, was already false at dispatch: it offered `sysexits(3)` as a
  candidate row while `corpus/SOURCES.md:99` already holds it as **S090**, and the L1 appended
  **S280** (GNU Errors) at 13:51, mid-wave. The sources scribe caught both and withdrew its
  rows (`T55W1ScribeSources-receipts/`, and `corpus/SOURCES.md:517`). So one item arrived
  pre-empted — that is a *spec-freshness* defect of the same family as F1 (the spec assumes a
  tree state the wave then changes), and its symptom is a seat spending its budget on a
  withdrawal notice.
- **No LSP-backed check was applicable.** This is a JSON spec and Markdown report audit;
  `lsp` has no server for either, so all evidence here is `python3`/`git`/`ls` output, quoted.

---

## 9. Out-of-item observation (do not attribute to this spec): the frozen set is dirty *now*

`git status --porcelain -- .ufo/evidence/round-55/` at 14:00:22:

```
 M .ufo/evidence/round-55/before/c2.stdout
 M .ufo/evidence/round-55/c1/measure.py
 M .ufo/evidence/round-55/c2/measure.py
 M .ufo/evidence/round-55/contract.json
 M .ufo/evidence/round-55/freeze.json
?? .ufo/evidence/round-55/assimilation/
```
- `before/c2.stdout`: worktree **139 B at 13:59:44** vs HEAD blob **2 634 B**. The worktree
  copy is the verdict line plus a stray `Wall time: 3.49 seconds` — an eval-cell footer — and
  has lost all 43 `EXPLAIN` lines. Earlier in the same wave I observed it at **0 B** (13:53:52).
  `before/c1.stdout` is intact (2 276 B, identical to HEAD).
- `freeze.json` re-derivation: **MISMATCH** for `contract.json`, `c1/measure.py`,
  `c2/measure.py`; MATCH for `no-harm.sh`, `deciding-run.sh`, `controls.sh`. `freeze.json`
  lists amendments `[1,2,3]`, `contract.json` lists `[1,2,3,4,5]`.

Reading: the L1 is amending the counters mid-wave (five recorded amendments, each claiming
"predicate unchanged") and the manifest has not been re-hashed for amendments 4–5. The
truncated before-receipt breaks two spec items as written — item 17 must quote
`before/c2.stdout`, item 31 must `cmp` against it. **Nothing in the spec asks for any of
this** (`items containing a shell redirect onto before/c2.stdout: []`), so check D passes for
the spec while the *environment* violates the freeze. Adjudication belongs to
`T55W1CritFreeze` (item 54), `T55W1SentScope` (59) and `T55W1SentConfig` (60); I flag it, I
do not fix it, and I am not naming a seat as the author because mtime cannot distinguish the
L1's own regeneration from a seat's redirect.

---

## 10. Bottom line

The wave is **lawful in shape**: 75 seats (in band), 28 attackers (37.3 %), all names and
milestones distinct, every attack aimed at a named falsifiable target, and not one item
asking a seat to touch a frozen or production file. It **fails on path discipline** (20/75
items name no absolute path) and it carries **one HIGH defect that has already cost data
twice**: six items route into `T55W1Er10.{json,md}`, producing two lost updates on the R54.10
C1 draft (13:56:04 by item 14, 14:01:39 by item 29), the first recovered only by replaying a
peer's session log and the second still unrepaired when this audit closed. Three items (20,
18, 68) are padding I would drop; one gap (F5) leaves the round's own LOG.md, lesson and
SCORECARD prose unattacked.
