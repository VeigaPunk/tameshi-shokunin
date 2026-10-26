# T48W2CritMistakes — attack on `## Mistakes` (`corpus/lessons/round-48.md:292-361`)

Seat: T48W2CritMistakes (round 48, attempt 2, wave a2w1; critic). Item: attack the `## Mistakes`
section — evidence pointers real, class right (CORPUS.md vocabulary), captured-by honest (would the
named criterion have caught it), and every fix shown able to fail by a **committed** red-before
receipt with the fix as the only delta (CORPUS.md:179-185: "the observed failure text is committed").
Read-only on the lane. No counter was run against the lane: every command below is a read (`cat`,
`git show`, `grep`, `ls`, `find`, `jq`, `diff`, `awk`) or a read-only check
(`quality/pointer-check.py` = `git cat-file -e`) into scratch. A probe is not a verdict.

Tree: CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17`; worktree HEAD `17cc5ce1` (diff vs CONTENT is
`.ufo/waves/round-48/{a2w1-dispatch.*,a2w1.ready,spec-a2w1.json}` only, so `corpus/` is identical).
Lesson blob at CONTENT = `715920382f9370fcf79e261626c186741bfd219e`, 39 533 B, sha256
`a6d5fd94e09336106650756b3b08683eaa7c450c872857ff9eb117818e7086f2`; `## Mistakes` starts at `:292`,
rows 1-7 at `:304-310`, the `d1`-`d7` block at `:316-330`, mined rows at `:354` and `:360`.
Contract sha256 `4fff75db…` (matches `freeze-2.json`); freeze-2 sha256 `47c1058b…`; round-47 report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-47/tameshi.md` sha256 `e341bea7…`.

## Verdict

- **Pointers**: all nine rows' *primary* pointers open and say what the row claims; three
  sub-pointers do not (F2, F8), and five rows name their report only as a bare word (F9).
- **Class**: all nine class tokens are in the CORPUS.md / `mistakes.md` §5 vocabulary; one does not
  fit the only defined class bearing that word (F6).
- **Captured-by**: seven `none`s are honest; two under-claim QUALITY 9 clause 2 (F5).
- **Fix able to fail (the item's bar)**: **1 of 9** rows ships a committed red-before receipt
  (mined-2, `quality/pointer-check-red-15b1521.stdout`), and its claimed green-after is false at
  CONTENT (F3). Row 1 — the only row the round *counts* ("it is the premise this round's C1 counter
  is built against", `:294-295`) — has no receipt at CONTENT, and the criterion that fixes it prints
  `VACUOUS` at CONTENT (F1). Rows 2-7 have none, and 5 of their 6 "red states" exit 0 (F4).

## F1 (blocking) — row 1's "Shown able to fail" is not shown; the fixing criterion is vacuous at CONTENT

`corpus/lessons/round-48.md:304` (fix cell, verbatim): "**Shown able to fail** by the pre-registered
relabel control CTL_B … the round-47 rows re-appended verbatim with `runs 3 stable` must print false
… Limits: CTL_B and the counter receipts are freeze-step-2 artifacts and were not executed for this
draft (`d1`)". The same row therefore says "shown" and "not executed". It was not:

```
$ ls .ufo/evidence/round-48/control/
c2-controls.exit  c2-controls.meta  c2-controls.py  c2-controls.stderr  c2-controls.stdout  run-controls.py
$ git cat-file -e c7586b9a:.ufo/evidence/round-48/control/c1-controls.stdout   # fatal: does not exist
```

CTL_B/kill: the fix is graded by QUALITY 95, whose falsifier reads that absent file
(`.ufo/evidence/round-48/quality/falsifiers.sh:32-35`, `R=$E/control/c1-controls.stdout`):

```
$ HYAKU_SCRATCH=$S bash .ufo/evidence/round-48/quality/falsifiers.sh
grep: .../.ufo/evidence/round-48/control/c1-controls.stdout: No such file or directory
grep: .../.ufo/evidence/round-48/control/c1-controls.stdout: No such file or directory
CRITERION-95-FALSIFIER-VACUOUS
$ bash .ufo/evidence/round-48/quality/falsifiers.sh >/dev/null 2>&1; echo $?
0                       # a VACUOUS block does not make the script exit non-zero
```

Impact: calibration axis (the round's lowest, score 6) — the C1 predicate's discriminating power rests
on this one control; and the pre-registered obligation, not just wording:
`freeze_plan` ("the controls are scored and committed", `contract.json`:7) and amendment 9
(`contract.json:61`: "the C1 controls are scored at the counter-freeze commit"). Commit `7552984`
("counter freeze (step 2) … controls …") ships `run-controls.py` and `c2-controls.py` and no C1
control receipt (`git show --stat --format='' 7552984 | grep control` → the two scripts only).
The CONTENT LOG entry itself says the receipt "lands with them", contradicting the lesson's "Shown".

Smallest safe correction: land `control/c1-controls.stdout` (scored at `7552984`, printing that
revision per amendment 9) before the lesson claims "shown", or replace "Shown able to fail" with
"to be shown by CTL_B (receipt pending, scored at the counter-freeze commit)" and keep the Limits
clause — and make the falsifier script exit non-zero when any block prints `VACUOUS`.

## F2 (blocking, reference-drift inside the fix column) — row 1's two contract pointers resolve to braces

```
$ awk 'NR==26||NR==33||NR==86||NR==93{printf "%d|%s\n",NR,substr($0,1,90)}' .ufo/evidence/round-48/contract.json
26|  },
33|  {
86|   "statement": "At REV, for each of the 22 frozen statements, the standing row (the last da…
93|   "cheapest_controls": "CTL_B relabel: the round-47 standing rows re-appended with `runs 3 stable`…
```

`:26` is the close of amendment 3 (row grammar), `:33` the open of amendment 5 (fleet/lane state);
neither carries "R=3 observation rounds with every declared member attested" (that is `:86`) nor
CTL_B (that is `:93`). The second pointer is also written without a directory (`contract.json:33`),
which names no file at the lane root. The section's own class for this defect is `reference-drift`
("quote/pointer does not say what is claimed", `.ufo/waves/kaika-w1/mistakes.md:79,101`): the row
commits the defect it classes.

Impact: a closure judge or critic following the fix lands on amendment 5 and cannot see the rule the
row claims to be scored by; criterion 97's checker cannot see it either (it tests existence of a
backticked lane path, not that the line says what is claimed —
`quality/pointer-check.py`: `exists()` = `git cat-file -e`). The same off-by-N class appears at F8.

Smallest safe correction: `contract.json:86` and `.ufo/evidence/round-48/contract.json:93`.

## F3 (blocking) — mined-2's fix has a real red-before but no green after, and its "after" tree splits identically

Row `:360` says: "Green after: the same two commands at the content revision, run by the L1 after the
content commit". The first command is red at CONTENT, identically to the red receipt:

```
$ python3 .ufo/evidence/round-48/quality/pointer-check.py --lane $PWD \
    --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 --file corpus/QUALITY.md \
    --start "## Criteria appended — round 48"
MISSING .ufo/evidence/round-48/control/c1-controls.stdout
MISSING .ufo/evidence/round-48/quality/c94-96-falsifiers.stdout
POINTERS: file=corpus/QUALITY.md checked=11 missing=2 skipped=0 rev=c7586b9a…
exit=1
```

and `.ufo/evidence/round-48/quality/pointer-check-red-15b1521.stdout` (committed, exit=1) prints the
same two `MISSING` lines. That is CORPUS.md's rejected exemplar M027 ("before/after trees that split
identically"). The second command is not a red-before at all: at the red revision it was already green
(same receipt: `POINTERS: file=LOG.md checked=8 missing=0 … exit=0`; at CONTENT `checked=15
missing=0 exit=0`). So one of the "two commands" was never red, and the other is still red.

Cause is a revision disagreement, not a code bug: the row names the **content revision** as the green
point while its own criterion says the **landing tip** (`QUALITY.md:1430`: "exists in the tree of the
round's landing tip"), and the two receipts it cites can only land after CONTENT.

Impact: `landing`; criterion 97 is the round's new gate against prospective records, and its own
lesson row asserts a green state that does not exist where it is asserted. A closure judge reading
CONTENT cannot reproduce "green after", and the *mistake the row mines* (a record citing receipts
that do not exist at the revision that carries it) is still present at that revision in QUALITY 94/95.

Smallest safe correction: name the receipts commit (not CONTENT) as the green point — "green at the
receipts-only commit that lands `control/c1-controls.stdout` and `quality/c94-96-falsifiers.stdout`" —
and, until that commit exists, label the green state pending, as the LOG entry already does.

## F4 — rows 2-7: no committed red-before, and 5 of 6 "red states" exit 0

The section's promise (`:297-298`): "a fix whose red state is shown by a command, not by prose."
CORPUS.md's bar is stricter: "the same command **exits non-clean** for the named reason, with the fix
as the only delta; the observed failure text is **committed**". Measured exit status of every red
state as written:

```
d2 jq '.items|length' spec-w2.json ; ls w2/*.md|wc -l   -> 32 / 0        exit=0
d3 find selftest -type f|wc -l ; find round-46…|wc -l   -> 0 / 6         exit=0
d4 grep -c '^CRITERION-' c91-92-falsifiers.stdout       -> 2             exit=0
d5 diff <(…) <(…)                                       -> 1c1 / env,node vs bwrap,node   exit=1
d6 find /fast/scratch/… | wc -l ; du -sh                -> 32 / 23G      exit=0
d7 git rev-list --count 663e0682..03facb22              -> 1             exit=0
d1 git show edd4ca44:…/c1.stdout | sed -n '5,6p'        -> the two lines exit=0
```

Every output reproduces (d2/d3/d4/d7 exactly as typed; d5 exactly). But five of seven are read
commands that exit 0: their "red" is the author's interpretation of a number, not a failing check.
Only d5 is a command that fails, and it is a one-off diff, not the fix's check ("every number a
lesson restates … names the receipt line it came from, **and the comparison runs**" — no script
exists that runs it). No red state is a receipt: `ls .ufo/evidence/round-48/{quality,control}` shows
one red-before file in the whole round (`pointer-check-red-15b1521.stdout`).

Self-referential defect: row 3 (`:306`) mines exactly this — "selftest tallies are cited as evidence
but no receipt for any of them is committed" — while the section cites d2-d7 tallies and commits no
receipt for any of them. The rows' own disclaimer ("Rows 2–7 are detectors only … none is scored
here", `:347-348`) is honest about scoring but does not change the record: a fix that is recorded and
unenforced is the shape the round-47 lesson itself recorded as conformance defects 1-5 (none had a
gate; every one recurred as a row here).

Impact: `landing` (rows 3, 4, 7), `scope` (row 2), `provider` (row 6), `reference-drift` (row 5).
A closure judge cannot distinguish "fixed this round" from "named this round" for any of them.

Smallest safe correction: either commit one receipt per row (`quality/d2-shape.stdout`… with the
command's own bytes and exit) and make rows 2, 3, 4, 6, 7's checks exit non-zero on the failing
state, or relabel the column "named, not yet enforced" and keep `none` out of the fix cell.

## F5 — rows 3 and 4 under-claim their captured-by (`none` where QUALITY 9 clause 2 applies)

Row 3 (`:306`): "`none` — criterion 88 … makes a committed receipt mandatory for the no-harm
falsifier script only; criteria 92 and 93 … require no committed output for it." Row 4 (`:307`):
"`none` — criterion 93 … requires no committed output". Both statements about 88/92/93 are true
(verified: `QUALITY.md:1291-1315`, `:1363-1377`). But criterion 9, second clause, is exactly the rule
they need:

```
QUALITY.md:24  9. Scratch stays in `/tmp`; evidence a claim rests on is copied into
QUALITY.md:25     the repo (`.ufo/evidence/…`) before the commit that cites it.
QUALITY.md:26     (MK-6)
```

Round 47's report cited `C1 35/35, C2 pool 14/14, C3 24/24` (report `:12`) and a falsifier receipt
for three criteria (report `:15`); both are "evidence a claim rests on" with no committed copy —
QUALITY 9 would have caught both. The section already uses criterion 9 for its *first* clause in row
6 (`:309`), so the omission is inconsistent, not a scope choice. Whether 9 had a gate is a separate
question (it has none), but the captured-by cell asks for "the criterion … that should have caught
it (or `none`)", not for a gate.

Smallest safe correction: row 3 → `QUALITY 9 clause 2 (QUALITY.md:24-26), no gate`; row 4 → same,
plus the round-46 precedent (`QUALITY.md:1312-1315`).

## F6 — row 2's class `scope` does not fit its only defined namesake; `provider` does

Row `:305` classes "a wave of the declared round shape was built, validated and never dispatched; the
round closed below its floor" as `scope`. The vocabulary (`CORPUS.md:171-175`) supplies names only,
but the only defined class carrying that word is C03 "Scope overreach — universal/'generalizes'
without a sweep" (`.ufo/waves/kaika-w1/mistakes.md:81,144-156`), whose five exemplars are all
unsupported claims, not undelivered shape. The row's own evidence names the cause report `:52`:
"the orchestrator reported the spawn cap at 0 and wrapped the run up" — C13 "Operational abort —
provider/quota/interrupt" (`mistakes.md:91,320-334`), i.e. the `provider` token already used by row 6.
Medium confidence: §5 defines no class semantics, so a lane reading `scope` as "round scope" is
defensible; under the defined taxonomy it is not.

Smallest safe correction: class row 2 `provider` (spawn-cap abort) and keep the undelivered-wave
diagnosis in the evidence cell, or add a one-line definition of `scope` to the lesson's vocabulary
note so the reading is fixed.

## F7 — mined-1's red-before is a different program at a different revision; criterion 96's falsifier does not test criterion 96

Row `:354` fix: "the round-48 counter refuses `--work` under `/tmp` … red-before: the round-47
counter accepts `--work /tmp/...` and prints the masked `2/9` (receipt above)". The receipt is real
(`.ufo/evidence/round-47/before/c1-at-freeze.stdout:18`, `P1=…2/9 pass|1`) and the mechanism is real
(`tools/env-diff.py:68-71` `--tmpfs /tmp`; `measure.py:395` `under_tmp`; selftest
`PASS T63_work_under_tmp_refused`, `selftest/c1-r48-selftest.stdout:74`). But "the same command … with
the fix as the only delta" is not met: the before receipt is the round-47 counter (which the freeze
patch rewrites, `freeze-diff-vs-w1.patch`) at a different revision. No control toggles the guard
(round-48 counter with `under_tmp` removed must accept `/tmp`), so the guard's discriminating power is
untested. The same-rev pair that would satisfy criterion 96 exists one hop away, in the wave-47 seat
report (`.ufo/waves/round-47/w1/T47ExecObsC.md:54,85`, quoted by `T48RevenEnvDiff.md` §2: same rev,
same counter, only the path string moves) — the row does not cite it.

Worse, the criterion the round appends for this row does not check its own text. Criterion 96
(`QUALITY.md:1420-1422`) requires "same revision, same counter, same profile, with exactly the named
variable changed"; its falsifier (block 96, `falsifiers.sh` §96) only asserts the two P1 tuples differ
and that the string `under_tmp` occurs in `measure.py`:

```
$ bash .ufo/evidence/round-48/quality/falsifiers.sh
tmp-work P1=ENVDIFF_SELFTEST: 2/9 pass|1
var-tmp-work P1=ENVDIFF_SELFTEST: 9/9 pass|0
CRITERION-96-FALSIFIER-OK
```

The two receipts it compares are at different revisions (`.ufo/evidence/round-47/before/` = freeze
tree, `after/` = `8b0e15d2…`), so the block passes on a pair that violates criterion 96's "same
revision, same counter".

Impact: calibration (`attribution` row) and the criterion set (96). Smallest safe correction: cite
`T47ExecObsC.md:54,85` in the row, add a guard-toggle case to the C1 selftest, and make block 96
assert the two receipts' revisions and counter sha are equal (or print `VACUOUS` when they differ).

## F8 (minor) — two sub-pointer drifts

- `:309` cites `QUALITY.md:1367` for criterion 92's "free disk in `/tmp`" clause; the phrase is at
  `:1365` (`grep -n "free disk" corpus/QUALITY.md` → `1365`); `:1367` is the `Lesson:` line.
- `:304` says QUALITY 92 "requires the value, its exit, the tool sha256 and a `deps` clause".
  Criterion 92 requires the printed line, the `deps` clause and a tool sha256; the exit enters only as
  an input to the deps comparison (`QUALITY.md:1365`). The requirement for the exit came from the
  round-47 contract (`claims.C1.statement`: "value, exit code and tool sha256 … under the live host
  profile P0"), not from 92. The row's conclusion (92 is silent on observation counts) still holds.

## F9 (minor) — five rows point at a report the lane never names

Rows 2, 3, 4, 6, 7 cite `report \`:52\``, `:12`, `:15`, `:17`, `:5` with no path. No file in the lane
contains either quoted phrase (`grep -rn "planned and not dispatched" --include='*.md' .` →
`round-48.md:305` and the seat draft `T48ScribeMistakes.draft.md:14` only); the artifact is the fleet report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-47/tameshi.md` (sha256 `e341bea7…`, 55 lines), where
all five lines check out (`:5` lane HEAD `663e0682…`; `:12` the three selftest tallies; `:15` the
falsifier chronology; `:17` the `/tmp` incident; `:52` "planned and not dispatched" and "40 seats,
below the 64–100 floor"). Criterion 97's checker cannot catch the omission: `report \`:52\`` is not a
backticked lane path.

Smallest safe correction: write the path once in the section header ("report = fleet
`.ufo/reports/round-47/tameshi.md`") and keep the line numbers.

## Verified clean (what I opened and confirmed, so the next seat does not redo it)

| row | pointer | state |
|---|---|---|
| 1 `:304` | `.ufo/evidence/round-47/after/c1.stdout:5` | claimed `FAIL (cases=9 passed=7`, observed `PASS (cases=9 passed=9`, `declared_deps=env,fleet-root,node` vs `observed=fleet-root,node` — exactly as stated |
| 1 `:304` | `SCORECARD.md:2318,2314` @`663e0682` | `:2318` "The row above states the flaky run and is wrong"; `:2314` "Disclosed limit (before the deciding run)" |
| 1 `:304` | round-47 `claims.C1.statement` | "under the live host profile P0", i.e. one observation — the captured-by's premise holds |
| 2 `:305` | `spec-w2.json` / `w2/` | `jq '.items\|length'` → 32; `w2/` holds `swarm-registry.json` only, 0 `*.md` |
| 3 `:306` | round-47 `selftest/`, report `:12`, `SCORECARD.md:2308-2310` | dir exists and is empty (0 files) vs round-46's 6; `addition-lint.py --selftest` → `cases=7 failed=0` at `:2310` |
| 4 `:307` | `c91-92-falsifiers.stdout`, `falsifiers.sh:26`, report `:15` | 7 lines, carries `CRITERION-91-FALSIFIER-OK` and ends `CRITERION-92-FALSIFIER-OK`; block 93 at `:26-36`; report `:15` says the receipt was taken "before 91 was added" — contradiction real |
| 5 `:308` | `round-47.md:118`, `after/c1.stdout:17` | d5 reproduces: `1c1 / < env,node / --- / > bwrap,node`, exit 1 |
| 6 `:309` | report `:17`, `T47ExecObsD.md:30,199`, `QUALITY.md:762-768` | all real (`clone/checkout failed` at both lines; criterion 67 binds `--regression --workdir`) |
| 7 `:310` | report `:5`, `rev-list`, `diff` | `1`; `.ufo/waves/round-47/w1/T47ConnCross.md` only; `QUALITY.md:1156` criterion 86; `:916-922` criterion 77 |
| mined-1 `:354` | `SCORECARD.md:2314`, `T48RevenEnvDiff.md` §1-§3, `env-diff.py:68-71` | mechanism and controlled pair as described (see F7 for the gap) |
| mined-2 `:360` | `15b1521e`, `QUALITY.md:1398,1418` @`15b1521`, LOG `:2355` | commit message "orchestrator salvage … not a landed round"; the two `MISSING` pointers; LOG states "w2 falsify (32 seats)" |

The sweep claim at `:336-342` also holds: round-47's `## Mistakes` carries five data rows at
:105-109, `c91-lesson-quote-red-green.stdout` is committed, and the deciding script's widened
`FROZEN` list is at `.ufo/evidence/round-47/deciding-run.sh:29-30`; restating those three would
indeed be a duplicate.

Not findings: the runtime scratch state the round's row 6 measures now reads larger than when written
(`find /fast/scratch/hyaku/tameshi-r48 -mindepth 1 -maxdepth 1 -type d | wc -l` → 32; `du -sh …` →
23G) because live seats hold it mid-wave — the row says so ("live seats included"), and its fix's own
test is "any tree surviving the round", which cannot be scored before the round ends.

## Limits

- I did not run CTL_A-E, the C1 counter or the deciding run; F1 is measured by the absence of the
  committed receipt and by the falsifier's own output, not by a control score.
- `d6`'s numbers were re-read at a different moment (32 / 23G) and are reported as a live reading, not
  as a contradiction.
- `falsifiers.sh` was run twice into `$S` and wrote only beneath it.
- Scratch: `S=/fast/scratch/hyaku/tameshi-r48/T48W2CritMistakes`, created, used (empty at removal) and
  `rm -rf`'d; `ls -d "$S"` → "No such file or directory". Nothing was written under `/tmp`.
- Tooling: none installed or upgraded (no version change to record).
- Every command above was run read-only against the lane; the lane tree, index, jj state,
  `corpus/`, `tools/` and `SCORECARD.md` were not touched by this seat.
