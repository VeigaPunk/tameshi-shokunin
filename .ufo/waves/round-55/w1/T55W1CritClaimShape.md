# T55W1CritClaimShape — claim shape: separability, no-harm, axis, controls

Seat T55W1CritClaimShape (critic, wave 1). Item: judge the **claim shape**, not the
work — causal separability of C1 and C2, axis harm, axis selection/naming, and a
do-nothing control per claim. Leaf member; no subagent dispatch; no lane production
file edited; no mutating git on the lane.

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Base: `0a2010acd1e92e4e332774050825e21bcfc7e079`
- The tree moved while I measured (three freeze commits, then a content commit).
  Everything below names the revision it was measured at. At the end of my run:
  `HEAD=133b2ce` (freeze amendment 8), content commit `C0=9cf0146`.
- Receipts: `.ufo/waves/round-55/w1/T55W1CritClaimShape-receipts/`
- Scratch: `$HYAKU_SCRATCH/tameshi-r55/T55W1CritClaimShape` (removed at exit except
  the fixtures still needed by the receipts above).
- Tooling: nothing installed; no tool upgrade was needed.

## Verdicts

| # | Question | Verdict |
|---|---|---|
| 1 | Are C1 and C2 causally separable — can each verify with the other unlanded? | **C1: yes, proved** (C1 passes with every C2 byte reverted; C1's rows are byte-identical at base and at a C2-only tree). **C2: yes by construction and measurement**, with one load-sensitive arm that produced a single false failure (F4). No deterministic coupling in either direction. |
| 2a | Does the C1 record edit damage freshness? | **No.** Freshness's population is `corpus/SOURCES.md` rows with `status=mined`, id ≤ S160; C1 edits no mined row and the round adds only id > S160. Structurally impossible to move. |
| 2b | Does the C2 SKILL.md edit cost cold-read credit the round must repay? | **Yes, and the round under-books it by 17.** The SKILL.md edit costs 1 section (2 axis points, `8 → 6`); the round's edits taken together cost **18 of 64 sections** at C0. The declared obligation is "that one cold-read section". Until 18 sections are re-keyed the no-harm `coldread-floor` monitor is RED (`score=6 credited=46`). **F1, the round's blocking defect.** |
| 3 | Is at least one claim on the lowest non-retired axis (calibration 8), and is the axis named by the surface rather than the number? | **Yes to both, with one caveat.** The standing table reads depth 10, calibration 8, freshness 9, `Retired: none` — 8 is the lowest. Each claim carries a `surface` (C1 "the lane's record against the tree"; C2 "the scratch-root exit class across every documented mode"). Caveat: C1 does not move the calibration axis's own instrument (the cold-read monitor), so the round can claim 8 **held**, never 8 **moved** (see F7). |
| 4 | Is there a do-nothing control for each? | **Yes.** `controls.sh` phase A runs one do-nothing clone at base and checks each counter separately (`CTL_0_c1` and `CTL_0_c2`, each expecting its own `false`), and each claim also has a skip control plus a positive control at the revision it certifies. Gap: no pre-registered control isolates the claims *from each other* — I supply that with fixtures (Q1). **One of the C2 controls can no longer fire (F6).** |

Claims I would **reject**: none of the two claims. I would reject (a) the "one
SKILL.md section" re-key obligation as written, and (b) `CTL_BREAK_c2` as a
pre-registered control at the current frozen bytes. I would reject the round's
calibration no-harm claim if it ships with only the single-section re-key.

---

## Q1 — Causal separability

**Static basis.** The C1 counter reads `SCORECARD.md`, `corpus/QUALITY.md`,
`corpus/lessons/round-54.md`, `LOG.md` plus `git show` blobs of the round-54
evidence; the C2 counter reads `tools/*`, `tools/registry.json`,
`corpus/knowledge/scratch-root-contract.md`, `SKILL.md`. The file sets are disjoint.
And no tool reads the record files at all:

```
$ grep -lnE "SCORECARD\.md|QUALITY\.md|LOG\.md" tools/*.py tools/*.sh
(no output)
```

That covers the ninth allocating mode too (`registry-check --rev`), so the
`tools/` disjointness holds for every mode the C2 counter runs, not only the eight
that existed at the original freeze.

**Direction C1 ⟂ C2 (measured).** C1's verdict is unchanged by landing C2:

```
$ python3 .ufo/evidence/round-55/c1/measure.py --lane <base clone>   --rev 0a2010ac… --work <empty>
C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
$ python3 .ufo/evidence/round-55/c1/measure.py --lane <base + the five C2 files> --rev 2bd8270 --work <empty>
C1_R55: rev=2bd8270ba0f5 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
```
Per-class rows are identical (same six R54.1 stale hits, same three R54.2, same
one R54.3, same `premise` miss on R54.9). `receipts/c1-base.stdout`,
`receipts/c1-c2only.stdout`.

**The strong form — C1 verifies with every C2 byte reverted.** Fixture: C0
(`9cf0146`) with `tools/repeat-control.py`, `tools/context-capture.py`,
`tools/registry-check.py`, `tools/registry.json`,
`corpus/knowledge/scratch-root-contract.md`, `SKILL.md` reverted to base
(`diff --name-only 9cf0146 HEAD` prints exactly those six files):

```
C1_R55: rev=992d2c996969 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```
`receipts/c1-c0minusC2.stdout`. On the same tree the C2 counter collapses to the
base state (`grammar=6/9 docs=0/7 note=0/9 skill=0/1 total=20`), i.e. each counter
moves only with its own bytes. C1 also reads `total=0 C1_R55_PASS=true` at C0
(`9cf0146`) and again at `HEAD=133b2ce` under the amendment-8 counter bytes
(`receipts/c1-head-133b2ce.stdout`).

**Direction C2 ⟂ C1 (measured, one flake).** C2 at a tree carrying only C1's four
record files (pre-amendment-6 bytes):

```
C2_R55: rev=13abf750f2d6 grammar=6/8 lazy=5/5 empty=12/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=19
```
Base is `total=18`. The whole delta is one arm —
`empty:registry-check --selftest rc=1 expected=0` (`receipts/c2-at-C1-only-oldbytes-receipts.json`) —
and the mode then passed 3/3 at the C1-only tree and 3/3 at base, 23.7–26.6 s per
run (`receipts/cross-tree-measurements.txt`). So it is a load-sensitive flake in
`registry-check`'s own timeout cases, not coupling. Limitation stated honestly: this
direction was measured with the pre-amendment-6 counter bytes; the added ninth mode
is covered by the static disjointness above, and amendment 6 gives it the grammar
arm only (`cheap=False`), so it never enters empty/usable.

Also measured on C2's own tree (frozen bytes): `grammar=8/9 … note=8/9 … total=3`.
C2 does not yet pass — its ninth mode and the note's ninth name are still open
(C2's own work, not a coupling finding).

## Q2 — Axis harm

**Freshness: no harm.** `freshness/measure.py`'s population is
`{r : r.status == 'mined' and int(id) <= 160 and r.url}`. The round's only
`corpus/SOURCES.md` change is one added row, `S280` (`git diff 0a2010ac..HEAD --
corpus/SOURCES.md`), id 280 > `MAX_ID = 160`, status `mined`, plus a trailing
newline on the round-54 note line. No mined row and no id ≤ 160 row is touched, so
`population` and `fresh` cannot move. (The row still drifts cold-read entries that
list `corpus/SOURCES.md` as an input — see below. Two different monitors, two
different answers.)

**Cold-read: yes, 18 sections and 2 axis points.** The ledger binds every entry to
its input bytes by sha256 (`input gate`, round-18 `measure.py` rule 4), and the box-3
credit requires `sections_covered == sections_total`. Measured at four trees:

| tree | edits | score | covered | uncovered |
|---|---|---|---|---|
| base `0a2010ac` | — | 8 | 64 | 0 |
| base + `SKILL.md` only | the one section the round names | 6 | 63 | **1** (`## Standing rules`, `no-ledger-entry`) |
| base + tools/registry/note only | C2's four byte files | 6 | 49 | **15** (`input-drift:tools/…`) |
| base + all five C2 files | what C2 lands | 6 | 49 | 15 |
| **C0 `9cf0146`** | the whole round | **6** | **46** | **18** |

`receipts/coldread-C0.json`, `cross-tree-measurements.txt`; the round never touches
the ledger (`git diff 0a2010ac..HEAD -- .ufo/evidence/round-21/coldread/ledger.json`
is empty). The 18 headings, from the C0 receipt:

```
## Standing rules                                   no-ledger-entry
## Mutation-sweep recipe — numbered steps; …        input-drift: tools/context-capture.py, tools/registry.json, …
## The leg ledger — replay, receipt, and how …      input-drift: corpus/SOURCES.md
### Triggers T1–T3 and the re-pin rule               input-drift: corpus/QUALITY.md, corpus/SOURCES.md, …
### The service's limits — what tameshi refuses …   input-drift: tools/context-capture.py, tools/registry-check.py, …
## The operator's runbook and the six-leg …         input-drift: tools/registry.json
## Repeated controls and gate registry — round 12   input-drift: tools/repeat-control.py, corpus/SOURCES.md
### Gate/probe registry                              input-drift: tools/bash-witness-study.py, tools/repeat-control.py, …
## Pin disposition and provenance correction — r13  input-drift: corpus/SOURCES.md
### Round-13 gate/probe registry                     input-drift: corpus/SOURCES.md
## Effective expectation reconciliation — r14       input-drift: tools/context-capture.py
## Context gate classification and explicit exits   input-drift: tools/bash-witness-study.py, tools/context-capture.py, …
### Round-15 gate/probe registry                     input-drift: tools/context-capture.py
## Live-tree re-pin and entry-command monitor — 17  input-drift: tools/context-capture.py, tools/registry.json, …
### Round-17 gate/probe registry — re-pin …         input-drift: tools/context-capture.py, …
### Round-18 gate/probe registry — routed-defect …  input-drift: tools/registry.json
### Round-21 gate/probe registry — finite env diff  input-drift: .ufo/evidence/round-15/verify.py, corpus/QUALITY.md, …
### Round-26 gate/probe registry — report interop   input-drift: tools/context-capture.py, tools/registry-check.py, …
```

15 are attributable to C2's tool/note/registry bytes (isolated above), 3 to the
`corpus/SOURCES.md` row added for C2's grammar citation. The axis is dragged
`8 → 6` by the round's own edits, on the round's own lowest axis, and the record's
declared obligation is **one** section (`LOG.md`: "The one SKILL.md section the edit
drifts (`## Standing rules`) is re-keyed with a fresh reader at C0"; `no-harm.sh`'s
header says the same). The monitor that will catch it is the frozen
`coldread-floor` line, which requires `score >= 8` **and** `credited >= 64` — at C0
it reads `score=6 credited=46` → RED.

## Q3 — Axis selection and naming

- Standing axis table (`SCORECARD.md:2574-2580`, unchanged since round 54):
  `depth 10 · calibration 8 · freshness 9`; `## Retired` reads "none retired". So
  calibration 8 **is** the lowest non-retired scored axis; the contract's
  `lowest_axis` string is accurate, and it is checkable from the record, not only
  from the number.
- Both claims name a **surface**, not just a number: C1 `surface` = "the lane's
  record against the tree: the ten routed defects … each with the receipt the defect
  names"; C2 `surface` = "the scratch-root exit class across every documented mode
  of the seven tools that call `strict_scratch_root()`, not the self-test only".
  A reader can tell what is being measured without knowing the score.
- Caveat (not a defect): the calibration row's counting rule **is** the round-21
  cold-read monitor. C1 is record-vs-tree work; it does not move that instrument.
  So round 55 can only claim calibration **held at 8** (and only after F1), never
  "improved". Any "axis moved" wording in the round-55 block would be a saturation
  claim the instrument does not support — calibration is already at its
  lane-attainable ceiling (the last 2 points need independent promotion review).
- Record gap: at `133b2ce` `SCORECARD.md` has **no round-55 claim block** (only the
  corrections section, `grep -nE '^#{2,3} Round 55' SCORECARD.md` → line 2621 only).
  The axis-by-surface naming therefore exists in the contract but not yet where a
  reader meets the round.

## Q4 — Do-nothing controls

`controls.sh` phase A (`REV=BASE`), read at the frozen digest:

- `CTL_0`: one do-nothing clone at base; `score` the C1 counter → require
  `C1_R55_PASS=false`, then the C2 counter → require `C2_R55_PASS=false`. Two
  separate checks (`CTL_0_c1`, `CTL_0_c2`) on one clone, printed as
  `CTL CTL_0_c1 <line>` / `CTL CTL_0_c2 <line>`.
- Per-claim "did the work without doing it": `CTL_SKIP_c1` (a values-only corrections
  block, no in-place fix — must stay false), `CTL_SKIP_c2` (documentation only, no
  tool edited — must stay false).
- Per-claim fabrication: `CTL_FAB_c1` (invented values), `CTL_BREAK_c2` (raw
  exception type back on one line — must lose exactly that mode).
- Per-claim positive control at the revision it certifies: `CTL_POS_c1`, `CTL_POS_c2`
  in phase B (round 54's `CTL_POS_c1` was scored at the freeze and so could not fire
  — ER-R54-1; this round re-scores at `REV`, which is the right repair).

So yes: a do-nothing control exists per claim, and the do-nothing clone is shared
while the verdicts are separate. What is **missing** is a control for independence —
nothing lands C1 alone and asserts C2 unchanged, or the reverse. I supplied that with
fixtures (Q1); if the round wants it pre-registered, the smallest addition is a
`CTL_PARTIAL` in phase B that reverts one claim's file set and requires the other
counter's verdict to be unchanged.

---

## Findings

### F1 (blocking) — the cold-read repayment is 18 sections, not 1
Evidence: `receipts/coldread-C0.json` (`score=6 sections=64 covered=46`) and
`receipts/coldread-HEAD.json` at `133b2ce` (`score=6 sections=64 covered=46` — the
amendment-8 commit changes no ledger input), the per-tree table in Q2, and `LOG.md`'s
"The one SKILL.md section the edit drifts".
`no-harm.sh`'s header comment repeats the same wrong obligation (frozen file — report,
do not edit). The `coldread-floor` monitor cannot pass at C0 as it stands.
**Smallest safe correction:** re-key the 18 headings listed in Q2 with fresh readers
bound to the *current* input digests (tools/context-capture.py, tools/registry-check.py,
tools/repeat-control.py, tools/bash-witness-study.py, tools/registry.json, the note,
corpus/QUALITY.md, corpus/SOURCES.md, .ufo/evidence/round-15/verify.py), each entry
listing its inputs, a committed trace and `commands_executed_count>0`; then re-point
`LOG.md` and the round-55 block at "18 sections re-keyed", not one. Budget it as a
reader wave: round 54 re-keyed 23 in one round, so 18 is feasible — but it is not a
one-line edit, and it must be in the plan before the deciding run.

### F2 (blocking for the record, not for the counters) — three freeze pointers
`631cd64` (the assignment's and the first contract's freeze) → `e2979f2`
(amendments 1-7) → `133b2ce` (amendment 8). Verified now:
`FREEZE_INTEGRITY: OK files=7 amendments=8` at `133b2ce` and
`FROZEN_UNCHANGED=1` against HEAD (`receipts/gate0-amendment8.stdout`). The gates
pass, but **only if the deciding run is given `FREEZE=133b2ce`**. This is ER-R54-2's
defect ("three freeze pointers for one round; the receipt names one") recurring in
the round that corrects it, and the assignment text still names `631cd64` with
`total=18 / 8 allocating / 13 modes` (now `total=21 / 9 allocating / 14 modes`).
**Smallest safe correction:** name exactly one pointer — `133b2ce`, the one the
receipts print — everywhere the round's record speaks (report, SCORECARD block,
LOG entry), and put the superseded pointers only inside the erratum text. Do not run
`deciding-run.sh` with `631cd64`: `contract.json`, `c1/measure.py`, `c2/measure.py`
and `freeze.json` no longer match it, so `FROZEN_UNCHANGED` would be 0 and the run
would fail for the wrong reason.

### F3 (sharpness, disclose in the round's limits) — C1's stale arm is a 160-char proximity predicate
The arm is `(positive control[^\n]{0,160}rekeyed=7/7)|(rekeyed=7/7[^\n]{0,160}positive control)`
plus the whitespace-collapsed variant. A **truthful, corrected** sentence trips it:

```
$ python3 .ufo/evidence/round-55/c1/measure.py --lane <C1 record files> --rev 13abf75 --explain
EXPLAIN R54.1 stale: corpus/lessons/round-54.md:75: (`rekeyed=7/7`); the pre-registered positive control was cloned at the freeze
```
The full sentence reads "…the arm's own count is read at the deciding revision
(`rekeyed=7/7`); the pre-registered positive control was cloned at the freeze commit,
printed `CTL_MISMATCH` (`rekeyed=3/7`) and therefore never fired [ER-R54-1, round-55
correction]" — it states the correction correctly, and the counter still counts it as
stale. So "zero stale outside the corrections section" is satisfiable by *phrasing*
(keep the two tokens >160 characters apart) as well as by truth. That is a real limit
of arm (b) and it belongs in the round's `cannot_see`-adjacent disclosure.
**Smallest safe correction:** keep the plain statement in the corrections section
(which is excluded from the scan) and phrase the lesson so the deciding-revision
count and the failed control do not sit inside one 160-character window; do not edit
the counter.

### F4 (hazard) — one C2 arm is load-sensitive
Observed once: `empty:registry-check --selftest rc=1 expected=0` (this is the *only*
difference between `total=18` and `total=19` at a C1-only tree). The same mode passed
6/6 on aimed re-runs at both trees (23.7–26.6 s each). Round-54 amendment 4 records
the same sensitivity for `registry-check`'s timeout cases. A deciding run on a loaded
host can therefore return a false RED on one cheap-arm mode.
**Smallest safe correction:** nothing in the frozen counter — run the single deciding
invocation on a quiet host, and if a lone cheap-arm mode fails with every other arm
green, treat it as measured unavailability and say so; do not re-run the deciding
script (it refuses a second invocation by design).

### F5 (record accuracy) — the pre-registered `before` receipt predates the frozen counter
`before/c2.stdout` prints `total=21`, but the frozen (amendment-8) formula gives 20
for its own printed arms; 21 is exactly the **pre**-amendment-8 arithmetic
(`len(table)=14` in the empty/usable terms, `8` in the note term):

```
e2979f2  printed total=21   amendment-8 formula=20   pre-amendment-8 formula=21
133b2ce  printed total=21   amendment-8 formula=20   pre-amendment-8 formula=21
```
(`receipts/before-receipt-total.stdout`.) The contract's C2 `before` narrative quotes
that total verbatim. This is ER-R54-3's class — "a quoted total no receipt contains" —
inside the round that is correcting it. Note also that `before/*.stdout` is cited by
the contract but is **not** in `freeze.json`'s file list, so a post-freeze rewrite of
the pre-registered evidence is ungated.
**Smallest safe correction:** re-run the frozen counter at base `0a2010ac`, commit
the new `before/c2.stdout`, and correct the `before` quote; declare the re-measure as
an amendment. For a future round: put `before/*.stdout` in the freeze manifest.

### F6 (control defect) — `CTL_BREAK_c2` can no longer fire
The frozen break control edits `emit_err(f"repeat-control: could-not-evaluate: {exc}")`;
C0's tool now emits `… {message}` (line 233). The control's own assertion therefore
fails and — because `controls.sh` does not check the heredoc's exit status — the
"broken" clone is committed unmodified, so the control would score the *green* tree:

```
anchor occurrences: 0
AssertionError: anchor not unique: 0
snippet_exit=1
```
(`receipts/ctl-break-anchor.stdout`.) With C2 green, `CTL_BREAK_c2` would print
`CTL_MISMATCH` and controls phase B would read 3/4 — a control that does not fire
looks exactly like a control that passed, which is round 54's ER-R54-1 failure mode.
**Smallest safe correction:** re-freeze `controls.sh` (a) with the anchor that exists
in the C0 tool, and (b) with `|| exit 2` after the edit snippet so a stale anchor is
loud; then re-score phase B. Also note `deciding-run.sh` only greps for the
`CONTROLS_B: n/n as pre-registered` line, so a 3/4 line would not refuse the run — the
ratio needs its own gate or the round must read it.

### F7 (disclosure) — the premise arm for R54.9 cannot hold at base
After amendment 7 the R54.9 premise reads `c1/staged-at-freeze.txt`, a **round-55**
committed receipt, so `premise=9/10` in `before/c1.stdout` is structural, not a lost
round-54 receipt. The contract's C1 target says "every class prints premise=ok"; that
is unreachable at base by construction.
**Smallest safe correction:** state in the round's report that the base premise is
9/10 by construction and that the target's premise=10/10 is a property of the content
revision; do not weaken the arm.

---

## Sweeps that found nothing (so the record shows they ran)

- **Tool scope** — `git diff --stat 0a2010ac..HEAD -- tools` = `context-capture.py`,
  `registry-check.py`, `registry.json`, `repeat-control.py`, all inside
  `no-harm.sh`'s `tools-scope` allowlist (`M:tools/registry-check.py` is listed), and
  `registry-row-names-unchanged` compares base vs REV row names. No out-of-scope
  tool edit.
- **C1→C2 file references** — no `tools/*.py|*.sh` mentions `SCORECARD.md`,
  `QUALITY.md` or `LOG.md` (grep, no output).
- **Registry denominators** — the re-frozen C2 counter's `9/9 · 5/5 · 13/13 · 7/7 ·
  /9 · /1` match its own `modes()` table (`9 allocating`, `5 lazy`, `13 cheap`; the
  ninth mode is `cheap=False`, which is why the empty/usable arms stay 13).
  The contract's C2 target text matches the counter after amendments 6-8.
- **Cold-read ledger untouched** — `git diff 0a2010ac..HEAD --
  .ufo/evidence/round-21/coldread/ledger.json` empty (that is why F1 is open, not
  hidden).
- **`evidence-disposition --json` on a branch vs detached HEAD** — the mode reads 2
  on a detached HEAD (the counter's amendment 1) and 0 on a branch, at base, C1-only
  and C2-only trees alike; no coupling, and the counter's clone is on a branch.
- **`registry-check --selftest` determinism** — 3/3 at the C1-only tree and 3/3 at
  base, so F4's once-seen rc=1 is load, not revision.

## What this seat did not do

No lane production file edited; no `git add/commit/checkout` in the lane; no `jj`;
every git mutation was inside my own scratch clones with `rev-parse --show-toplevel`
asserted first; the frozen counters, contract, freeze manifest, controls, no-harm and
deciding scripts were read only, and their defects are reported above rather than
repaired.
