# T55W3Connector4 — cross-lane lesson overlap

Item: compare this round's two mined mistake classes
(`corpus/lessons/round-55.md` at C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`) with
sibling lanes' lessons (`../*/corpus/lessons/round-5*.md`, read-only):
is either class already a fleet pattern, and if so does tameshi's statement add anything?

Read-only seat. Nothing in the lane or in a sibling repo was modified. Receipts live in
`.ufo/waves/round-55/w2/T55W3Connector4-receipts/` (the attack-discipline path this seat's
spec names); this report lives in `w3/` (its `Report:` trailer). No tool was installed.

Verdict up front: **both classes are already fleet patterns.** Class A's shape is what
kake records as `stale-premise` (a label it shares with two unrelated kama/mori defects);
class B is a *mined knowledge class* in mori
(`corpus/knowledge/vote-binding-r56.md`, "The failure class"), with a second same-week,
same-vector instance in mado and a tooled instance in kotodama. Tameshi's statements add
three things each and lack one each; one of its two class sentences is narrower than its
own evidence.

---

## 0. What the round says it mined

| # | class sentence, verbatim at C0 | line |
|---|---|---|
| A | "class: a control scored at a revision that predates the work it certifies." | `round-55.md:20` |
| B | "class: a predicate that counted a document as stating a rule when a line break had split it." | `round-55.md:35` |

Lesson bytes at C0 are byte-identical to the working tree:
`sha256 57c3d2e6b42d845414f4f8673f85284adf691a78ed9c476868e69951d519812c`
(`01-tameshi-lesson-at-c0.txt`). The lesson has exactly one location at C0 —
`corpus/lessons/round-55.md`; `git ls-tree` over `.ufo/evidence/round-55/` at C0 shows no
lesson copy there (only `assimilation/ before/ c1/ c2/ contract.json controls.sh
deciding-run.sh freeze.json no-harm.sh`), so a seat looking for "the lesson under the
evidence dir" would find nothing and might read the wave-1 *draft*
(`.ufo/waves/round-55/w1/T55W1ScribeLesson-draft-round-55.md`) instead. The A-class and
B-class problem statements, the
`captured-by: none` / `captured-by: the freeze-time dry run` clauses and both fixes are
quoted in that receipt, so every claim below resolves to bytes rather than to this prose.

## 1. Sweep and denominators

`02-inventory.txt`, `03-classA-sweep.txt`, `04-classB-sweep.txt`, `08-class-labels.txt`
(`sweep.sh`, `class-labels.sh` in the receipts dir — both re-runnable).

- `*/corpus/lessons/round-5*.md`: **183 files, 172 outside tameshi**, 13 lanes
  (kumitate 23, kake 23, kotodama 22, kotoba 22, mori 21, kama 20, chousa 20, mado 10,
  kengaku/kasegi/kagi 3 each, tabi/souji 1 each).
- Same calendar week as this round (week of Mon 2026-10-26; tameshi r55 is Wed 2026-10-28):
  **69 files** across chousa 14, mori 21, kama 18, mado 10, kake 5, kengaku 1.
- Class A family regex (9 alternatives around predating/ancestor/measured-revision/
  pre-receipt/positive-state/order): **37 hits in 26 files**.
- Class B family regex (10 alternatives around line break / wrapped / 78 col /
  stripped-line / exact-line / whitespace-collapsed / verbatim / substring): **251 hits in
  94 files** — most are quote-folding prose in chousa/kotoba/kotodama/kumitate Gate tables,
  so the family was filtered for rows that carry a *verdict*, not a transcription practice.
- Recall check: `08-class-labels.txt` extracts every mistake-class label in the corpus
  (both `- **class:` form and table first-cells) so a class recorded under a name my regex
  misses would appear unexamined. The neighbourhood labels are `stale-premise` (5 rows
  outside tameshi), `vacuous` (4+), `calibration-staleness`, `stale-count-recurrence`,
  `revision`, `reference-drift`; all five `stale-premise` rows and both staleness rows were
  read in full — and they are **not one class** (see §2, "the label is overloaded").

## 2. Class A — already a fleet pattern: **yes**, under kake's label `stale-premise`

`09-sibling-quotes.txt` holds the quoted lines.

| instance | what it records | week |
|---|---|---|
| `kake-shokunin/corpus/lessons/round-57.md:118` (`stale-premise`) — **closest twin** | "The frozen C1 pin rule contradicted itself: the measured revision had to be a strict ancestor of the commit that introduces the receipts, so a counter run at that revision necessarily printed the pre-receipt state and the honest C1 receipt could only record `met=False`". Fix: re-derive at T0 ("a commit holding all three receipts") pinned to the measured revision, with selftests "claim 1 tip predates the receipts". | latest dated source 2026-10-25 → **previous calendar week** (stated, not rounded) |
| `kake-shokunin/corpus/lessons/round-58.md:113` (`stale-premise`) — same week, inverse polarity | `c56_quote_truth.py` reads `8/8 met=True` at `4cb225fb` (2026-10-26) and `6/8 met=False` at the round-57 tip `20217f23`; the green verdict lives only at a revision that no later tree reaches, and the SKILL.md registry row advertises `0=met`. | same week |
| `kake-shokunin/corpus/lessons/round-56.md:90` (`stale-premise`) | the fixture-base variant: a selftest that rebuilds from the checked-out `HEAD` prints `17/18` at the round base. | previous week |
| `kotodama-shokunin/corpus/lessons/round-56.md:13` — the **enforcement half** | "receipts did not name the revision they measured" → `dry-run.py run --rev REV` measures in a sandbox clone and prints `# measured-revision`; `check` fails a receipt without it, shown able to fail. | previous week |

Tameshi's sentence is in fact the *more general* member of the family: read literally,
"scored at a revision that predates the work it certifies" also covers kake r58's
green-at-the-older-revision case, which kake's own label (`stale-premise`) describes as a
symptom rather than a shape.

**The label is overloaded — do not adopt it bare.** All five `stale-premise` rows outside
tameshi were read; they name three different defects:

| row | shape | class A? |
|---|---|---|
| kake `round-56.md:90`, `round-57.md:118`, `round-58.md:113` | the verdict is a function of *where the check runs* | **yes** |
| kama `round-56.md:24` | a lesson names artifacts that do not exist at the final tip | no — record/citation staleness |
| mori `round-59.md:16` | a counter was drafted but never frozen, dispatched or self-verified | no — freeze-process gap |

So "already a fleet pattern" is true of the *shape* (kake's three rows) but the fleet's
only name for it is shared with two other shapes; a next-round entry must state the shape
as well as the label, or the label will be read as the wrong one.

**What tameshi's statement adds**

1. **The locus.** Kake's three instances are all *instrument-pinned-wrong* (the counter's
   pin rule, a selftest that stamps `HEAD`, a mirror pinned to a 158-row registry).
   Tameshi's is *runner-pinned-wrong*: the counter bytes are fine, the harness that runs
   the control cloned the wrong revision. No sibling row separates these two loci.
2. **The laundering half.** Tameshi records that four lane records — including a QUALITY
   criterion written in the same round — asserted the pass the receipt refutes. Every kake
   `stale-premise` row is an honest `met=False`; none has a false record attached. That
   half is tameshi's alone in this corpus.
3. **The named missing arm and its closure**, not a missing criterion: "the phase-B
   harness had no arm requiring that its clone match the revision it scores" → closed at
   `controls.sh:37`, which scores each control at the clone's own
   `git -C "$d" rev-parse HEAD` (`06-classA-gate-gap.txt`). Kake's three rows all read
   `captured-by: none`.

**What tameshi's statement lacks.** Kake's *label*. Tameshi's class is unnamed, so it
cannot be found by a label search and does not join the fleet taxonomy — the practical
cost is that the round-55 lesson will not be discovered by the next lane looking up
`stale-premise`. (The label needs the shape qualifier above; adopting it bare would import
kama's and mori's unrelated shapes.) Second: tameshi adds a residual its own gate cannot fix this round —
`deciding-run.sh` "never compares the `rev=` a `CTL` line names with the revision under
test" — while kotodama r56:13 already shipped exactly that check shape. Verified:
`grep -c CTL deciding-run.sh` = **0**; the `CTL` lines *do* carry the fact
(`CTL CTL_0_c1 C1_R55: rev=0a2010acd1e9 …`), so the missing arm is a comparison over
committed bytes, not a new run.

**Not the same class — stated so the L1 does not read them as instances:** mado
`round-53.md:26` M53-4 and `round-54.md:24,27` M54-2/M54-4 (freeze not committed before
dispatch: an *ordering* defect); chousa `round-58.md:26`, `round-59.md:28`, kama
`round-55.md:80,105` (a control that cannot fire for *predicate* reasons: the
vacuous-control family). Same symptom, different cause; tameshi's lesson names neither.

## 3. Class B — already a fleet pattern: **yes**, and mined as a knowledge class in mori

| instance | what it records | week |
|---|---|---|
| `mori-shokunin/corpus/knowledge/vote-binding-r56.md` §"The failure class" — **the class itself, mined** | the frozen C1 counter "bound an agreeing vote only when the voter's captured output contained the exact `RECHECK <h> <w>` line as a stripped *text* line"; all 15 voters emitted JSON yields that quote the line; `voted=0`; "the same round's C2 counter binds by substring and accepted the identical shape (`entailed=15`) — the two counters disagreed on the same bytes because they implemented 'contains' differently". `verified-at: 2026-10-27`; `coverage-map: new capability — seat-output vote binding (no prior lane note)`. | **same week** |
| `mori-shokunin/corpus/lessons/round-55.md:58` and the Mistakes row at `:95` (`vote-emission format`), verified at `round-55-verifier-spotcheck.md:26`, landed fix contrasted at `round-56-verifier-spotcheck.md:46` (`voted=0` → 78 agreement under the dual-shape binder) | the instance and its repair | **same week** |
| `mado-shokunin/corpus/lessons/round-54.md:25` M54-3 — **same wrap vector as tameshi** | registered quotation `S375` reads `verbatim=False` solely because "`S375` wraps across physical lines"; runnable repro prints `[(375, False), (376, False), (377, True)]`. | **same week** (2026-10-27) |
| `kotodama-shokunin/corpus/lessons/round-54.md:184` + `round-55.md:17` — **tooled** | `ReviewGateQuoteTool` was built around the class: "five escape classes (hard-wrapped quote, guillemets, hyphenated compounds, inter-span ellipsis, `* ` bullets)"; r55 records that four of the five escape the round-54 checker. | previous week (2026-10-22) |
| `mori-shokunin/corpus/lessons/round-53.md:24` — the fix direction | quotes located "with a substring test that **joins** comment-decorated line breaks (12/12)". | — |

Reproduced on tameshi's own bytes, not argued (`05-classB-repro.txt`,
`classB-repro.py`): at C0 the grammar marker
`cannot create clone scratch under the scratch root: TMPDIR is not a usable directory` is
**absent** under a raw-substring predicate and **present** under the whitespace-collapsed
predicate amendments 2/3 installed; the `## Standing rules` scratch bullet carries **7
word-splitting newlines in 866 characters**, i.e. seven places where a raw marker can read
as absent. That is mado's M54-3 mechanism on tameshi's document.

**What tameshi's statement adds**

1. **The surface.** Siblings hit seat output (mori), a source quotation (mado) and a quote
   gate (kotodama). Tameshi is the only one in the corpus to hit the lane's *own normative
   text under a cold-read credit rule*, where the cost is `skill=0/1` on a correct edit and
   the forfeited credit of 18 SKILL.md sections. That consequence is what makes the class
   round-critical rather than cosmetic, and no sibling states it.
2. **The fix discipline.** "the predicate is unchanged … only the comparison is honest
   about typography" — the claim is not weakened to make the check pass. Mori's landed fix
   went the other way (a new dual-shape binder plus a knowledge entry); mado's added a
   pre-dispatch gate. Tameshi is the only one of the four to state the invariant.
3. **The capture route.** A freeze-time dry run on an *edited clone before* the controls
   score (`captured-by:`). Mori's failure was discovered at the landed revision, after its
   vote wave had been spent; mado's after dispatch. Tameshi's route turns the class into a
   pre-control finding, which is the cheapest of the three.

**What tameshi's statement lacks.** Mori's falsifier shape: a *second binder over the same
committed artefacts* printing a different verdict (`voted=0` vs `entailed=15`, and r56's
0 → 78). Tameshi's evidence is a dry run on a hand-edited clone; a same-bytes contrast is
strictly stronger and already costs nothing to produce here.

**One correction to the lesson, stated and not smoothed.** The class sentence names only
the line-break vector, but its own second arm is not a line break. Arm 2 is the note's
label `bash-witness-study selftest` (`corpus/knowledge/scratch-root-contract.md:79` at C0,
no `--`) against the counter's earlier expectation of `--selftest`; the C0 counter labels
the mode "AS INVOKED" with an inline comment
(`.ufo/evidence/round-55/c2/measure.py:95-97`). The vector is *spelling of invocation*, not
wrapping — verified, and it is the same class only under a wider sentence such as "a
predicate that compared typography or spelling instead of content". As written, the
sentence would not cover its own second arm if read literally, and `05-classB-repro.txt`
shows the arm 2 needle absent from `SKILL.md` entirely (it lives in the note), so a reader
checking the sentence against `SKILL.md` alone would find only one arm.

## 4. Answer

| class | already a fleet pattern? | lane and line | same week? | tameshi adds | tameshi lacks |
|---|---|---|---|---|---|
| A — control scored where it cannot fire | **yes**, kake's shape under a shared label `stale-premise` | kake `round-57.md:118`; `round-58.md:113`; `round-56.md:90`; enforcement half kotodama `round-56.md:13` | r58 yes; r57/r56 previous calendar week | runner-side locus; the laundering half (false record incl. a same-round QUALITY criterion); the named missing harness arm + its closure (`controls.sh:37`) | the label (and the label needs a shape qualifier — kama `round-56.md:24` and mori `round-59.md:16` use it for two other defects); cites no sibling, so the pattern is re-derived |
| B — predicate reads a present fact as absent | **yes**, and mined as a knowledge class | mori `corpus/knowledge/vote-binding-r56.md`; `round-55.md:58,95`; mado `round-54.md:25`; kotodama `round-54.md:184`, `round-55.md:17`; fix direction mori `round-53.md:24` | mori r55/r56 and mado r54 yes; kotodama previous week | the credit-rule surface; the "do not weaken the predicate" fix discipline; the pre-control dry-run capture route | a same-bytes second-binder falsifier; a class sentence that covers its own arm 2 |

Cross-lane citation between these four lanes is **zero in both directions** (`09`,
last block: every tameshi round-5x lesson scores 0 for mori/kake/kotodama/mado; no mori,
kake or mado round-5x lesson mentions tameshi). The overlap is therefore invisible to
every lane's own record: two lanes independently name class B as a new capture in the same
week — mori's knowledge entry claims "no prior lane note", tameshi's lesson claims a
capture route "no prior round had".

## 5. The one bounded move (connector role)

**Proposal — one row, next round's Gate, nothing this round.** Admit mori's
`corpus/knowledge/vote-binding-r56.md` as a single own-work source row in tameshi's next
Gate, in the row form mori itself already validated for a sibling-lane artefact, and let
the knowledge entry built on it state class B **once** with both repair strategies
(whitespace-collapse for prose markers; walk-every-string-scalar for structured seat
output), and state class A's shape with kake's `stale-premise` label **plus the qualifier**
("the verdict is a function of the revision the check runs at") — the bare label would
import kama `round-56.md:24` and mori `round-59.md:16`, two unrelated shapes.

Why this form and not a prose citation: the reusable fleet pattern is
`mori-shokunin/corpus/SOURCES.md:329` (S549) — a sibling lane's file cited as
`../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md`, tier C own-work, with a
pinned copy `corpus/evidence/sources-r57/…`, lines and `sha256`. Mori's census validates
with that row present (`exit=0`, 337 rows), while a bare `../lane/path` in a lesson is
reached by no counter at all and would rot exactly the way mori's 12-of-14 unresolvable
clone revisions did.

Why not this round: tameshi's Gate is closed (one theme, S280 admitted), `corpus/SOURCES.md`
appends are a Gate act rather than a wave act, and this wave's census requirement pins the
registry at 140 rows (`07-census.txt`: exit 0, 140 rows, pre-existing W04 warnings only
S267/S268/S274) — an append would move a number the round's report quotes.

**Affected axes.** Calibration and operability: **neutral** — no claim predicate, counter,
tool, registry cell or note byte changes; the swing is on the standing coverage /
adjacency / discernment axes, where the lane currently bills a rediscovery as a first
capture. Harm check: it spends one of the round's 1–3 entries on a class the lane has
already mined as a *mistake*, so the entry must be framed as the fleet's class with two
repair strategies, not as new knowledge — otherwise it is capacity taken from a fresh
theme (the same ground on which round 54 refused the delta-debugging entry).

**Risks.** (i) Capacity: one entry slot. (ii) The sibling file may move — mitigated by the
pinned copy plus sha, which is the S549 form and needs no re-verification against the
sibling. (iii) The census row count moves 140 → 141 and the round's report must quote the
new figure; the W04 duplicate check is per-URL and unaffected by a path row, but this must
be shown by running the validator after the append, not assumed. (iv) A row can only cite
one document, so the entry's prose must carry the mado and kotodama instances without
rows — they stay uncited and therefore unpinned, which is honest but means the entry is
asserting facts about sibling lanes from memory of a read, the very shape `stale-premise`
describes.

**Verification.** (1) `git -C mori-shokunin cat-file -e <sha>:corpus/knowledge/vote-binding-r56.md`
and the copied file's `sha256` equals the row's cell; (2) `sources-census.sh validate
--root /home/vgpnk/Projects/shokunin tameshi` exits 0 at the new count; (3) the pinned copy
contains the ≤25-word Gate quote, whitespace-collapsed, at the cited lines; (4) one round
later, the resolution check kotodama r56:13 shipped (`check` fails a receipt that does not
name its measured revision) applied to this row: a re-run that cannot re-open the pinned
copy is a red, not a shrug.

## 6. Limits

- Regex recall is bounded; the mitigation is `08-class-labels.txt`, which shows the
  corpus's own label vocabulary and that no label in the neighbourhood was left unread. A
  class recorded in prose with none of my 19 alternatives and none of those labels would
  still be missed.
- Sibling claims were **read, not re-run**. Their receipts belong to their lanes; my
  receipts prove tameshi's side (the C0 lesson bytes, the SKILL.md wrap, the gate's missing
  `CTL` comparison) and quote the sibling side with line numbers.
- "Same week" is keyed to the latest dated source access inside each file, not to a run
  timestamp; lanes do not all stamp a run date. Kake r57's twin is one calendar week
  earlier on that key and is reported as such rather than folded into the week.
- No fixture repo was created; no git command mutated anything (all reads are
  `git -C <lane> show`), so the fixture-toplevel assertion had nothing to guard.

## 7. Artifacts opened

`tameshi-shokunin/corpus/lessons/round-55.md` (at C0 and in the tree),
`corpus/lessons/round-54.md`, `.ufo/evidence/round-55/contract.json`,
`.ufo/evidence/round-55/controls.sh`, `.ufo/evidence/round-55/deciding-run.sh`,
`.ufo/evidence/round-55/control/controls-a.stdout`, `.ufo/evidence/round-55/c2/measure.py`,
`corpus/knowledge/scratch-root-contract.md` (at C0), `SKILL.md` (at C0);
`kake-shokunin/corpus/lessons/round-56.md`, `round-57.md`, `round-58.md`,
`kake-shokunin/corpus/lessons/round-52-verifier-spotcheck.md`;
`mori-shokunin/corpus/knowledge/vote-binding-r56.md`,
`mori-shokunin/corpus/lessons/round-53.md`, `round-54.md`, `round-54-verifier-spotcheck.md`,
`round-55.md`, `round-55-verifier-spotcheck.md`, `round-56-verifier-spotcheck.md`,
`mori-shokunin/corpus/SOURCES.md:329`;
`mado-shokunin/corpus/lessons/round-53.md`, `round-54.md`;
`kotodama-shokunin/corpus/lessons/round-54.md`, `round-55.md`, `round-56.md`;
`chousa-shokunin/corpus/lessons/round-58.md`, `round-59.md`;
`kama-shokunin/corpus/lessons/round-55.md`;
183 files under `*/corpus/lessons/round-5*.md` by grep, not by full read.

Receipts (`w2/T55W3Connector4-receipts/`): `sweep.sh`, `class-labels.sh`,
`classB-repro.py`, `01-tameshi-lesson-at-c0.txt`, `02-inventory.txt`,
`03-classA-sweep.txt`, `04-classB-sweep.txt`, `05-classB-repro.txt`,
`06-classA-gate-gap.txt`, `07-census.txt`, `08-class-labels.txt`, `09-sibling-quotes.txt`.
