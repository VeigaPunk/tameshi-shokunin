# T50Disp47 — C1 disposer, round-47 spot-check items (R47.1–R47.7)

Seat T50Disp47 (scribe, leaf; no subagent dispatch). Judged axis: calibration. Date: 2026-10-26.
Method: read `.ufo/evidence/round-50/contract.json` and the frozen counter's docstring
(`.ufo/evidence/round-50/c1/measure.py:1-40`), the seven R47 items in
`.ufo/evidence/round-50/c1/defects.json` (ids, `keys`, `routed_at` = `473336d9d789f6081195e7376d17836a24666bc3`),
and the routed list at `corpus/lessons/round-47-verifier-spotcheck.md:103-109`. Every disposition is against the
lane tree at base `e3729de862f73ae080d98fcf522a7081ce16e40a` (read with `git -C <lane> show e3729de8:<path>`;
lane HEAD was `4afb060c` and every cited line was byte-equal at base and at HEAD). Fix commits were located with
`git -C <lane> log --format='%H %ad %s' -S'<fragment>' 473336d9..e3729de8 -- <path>`. Each excerpt below was
extracted from the cited lines and re-validated with the counter's own whitespace-collapse rule before commit.

## R47.1 — C1 standing row for `six-leg regression ledger` and a repeatable observation — **fixed**

Ask (`round-47-verifier-spotcheck.md:103`): append a superseding row for `six-leg regression ledger` stating the
stable observation (or a declared-unstable form the counter can score), make the C1 counter's observation
repeatable (N ≥ 3 per profile, or a declared nondeterministic class), and give `hermetic env-differential probe`
the same treatment. Found: `SCORECARD.md:2334` now carries
`| six-leg regression ledger | … deps \`fleet-root,node\`, runs 3 stable |` and `SCORECARD.md:2340` carries the
same `runs 3 stable` clause for `hermetic env-differential probe`; the counter that scores them is the R=3
counter, `.ufo/evidence/round-48/calibration/measure.py:3` ("R=3 repeated observation rounds and declares a value
class…") and `:8` ("carries a `runs 3` clause) declares a value set V (one member: `stable`; two or three
members: `nondeterministic`"). The rows entered the tree at `c7586b9a10effc63b4bd327f976edc094c1bdc17`
(round-48 content revision; `git diff-tree --name-only c7586b9a | grep -c SCORECARD.md` → 1) and
`git show 473336d9:SCORECARD.md | grep -c 'runs 3'` → 0, so the keyed text is new since routing. Both asks of the
item are met: a superseding row per statement with a declared class, and a counter that observes each row three
times and refuses an undeclared or unattested member (`corpus/lessons/round-48.md:304` records the miss this
repairs).

## R47.2 — commit selftest receipts for the round-47 counters, `addition-lint.py` and the criterion-93 falsifier — **open**

Ask (`:104`): commit selftest receipts for the three round-47 counters, `addition-lint.py` and the criterion-93
falsifier block (conformance defects 3 and 4). Found: `.ufo/evidence/round-47/selftest/` still holds zero files
(`ls -la .ufo/evidence/round-47/selftest/` → only `.` and `..`); the only committed occurrence of the criterion-93
label in the evidence tree is the script itself (`grep -rn 'CRITERION-93' .ufo/evidence/` → 1 hit,
`.ufo/evidence/round-47/quality/falsifiers.sh:36`), and the committed falsifier output
`.ufo/evidence/round-47/quality/c91-92-falsifiers.stdout` still stops at criterion 92. The tallies do exist as
raw captures, but only under a wave seat's directory:
`.ufo/waves/round-48/w1/selftest/{c1-measure,c2-pool,c3-coverage,addition-lint,falsifiers-verbatim}.{stdout,exit}`
(`C1_R47_SELFTEST: cases=35 failed=0`, `C2_R47_SELFTEST: cases=14 failed=0`, `C3_R47_SELFTEST: cases=24 failed=0`,
`ADDITION_LINT_SELFTEST: cases=7 failed=0`, `CRITERION-93-FALSIFIER-OK`, each with exit `0`), committed at
`755298415f8c4eef3bed0c0d7625e2aacb03d6c2`. That is the class conformance defect 3 named ("appear only in
lane-dispatched seat reports"), not the L1 evidence receipt the defect cites as precedent
(`.ufo/evidence/round-46/selftest/c{1,2,3}-selftest.{stdout,exit}`), and round 48's own counters did get
`.ufo/evidence/round-48/selftest/` receipts. The round-48 review scored this closed on the wave paths
(`.ufo/waves/round-48/a2w1/T48A2RevSpotcheckR47.md`, row RD2); I disagree on location, and the frozen counter
cannot cite a `.ufo/waves/` path here (no path ends with one of the item's keys). Smallest closing change
(`fix_plan`): copy the five stdout/exit pairs into `.ufo/evidence/round-47/selftest/`, cite them from the three
standing rows (`SCORECARD.md:2308-2310`), and name R47.2 in the newest Planned paragraph.

## R47.3 — lesson correction for `round-47.md:117-118` dependence sets — **fixed**

Ask (`:105`): append a named correction for `corpus/lessons/round-47.md:117-118` dependence sets (conformance
defect 5). Found: `corpus/lessons/round-48.md:178` opens `- **C1-R48-1 (corrects \`corpus/lessons/round-47.md:117-118\`;
the file is never rewritten).**` and `:179-189` names both sets, shows they are the freeze-time emission
(`.ufo/evidence/round-47/before/c1-at-freeze.stdout:5,17`), distinguishes the deciding-run sets, and states the
rule for later rounds. Added at `50545328e7ac4ba1703d70030e37dacec9362e68` (`git diff-tree --name-only 50545328 |
grep -c corpus/lessons/round-48.md` → 1); the file did not exist at `routed_at`
(`git cat-file -e 473336d9:corpus/lessons/round-48.md` → fatal: not in that revision), and the corrected file is
untouched (`git log 473336d9..e3729de8 -- corpus/lessons/round-47.md` → empty), which is what the correction's own
rule requires.

## R47.4 — reject citation for `r8-predictive-test-selection-cost.md` — **fixed**

Ask (`:106`): when refusing `r8-predictive-test-selection-cost.md` again, cite the unopened-row reason (QUALITY 10)
rather than `PROVINCE.md:14-18`. Found: `corpus/lessons/round-48.md:270` re-states the refusal as
`unopened row: its \`source:\` cites \`S205\` / arXiv 1810.05286 and the lane has no such row … — **QUALITY 10**
(decisive) and **QUALITY 2**. The round-47 \`PROVINCE.md:14-18\` cite is withdrawn as the decisive reason`, with the
flip condition kept checkable; the same correction is `:207` (`## Correction C1-R48-2`) and the round-48 closure
re-checked it (`corpus/lessons/round-48-verifier-spotcheck.md:101`: "The decisive reason is now the right one").
Added at `50545328e7ac4ba1703d70030e37dacec9362e68`; the file was absent at routing. The behaviour the ask names
(cite QUALITY 10 when refusing again) is now the written disposition, and the refusal is the one the lane still
holds (`corpus/QUALITY.md:1392`).

## R47.5 — carried items from `Planned (round 48)` — **open**

Ask (`:107`): four carried asks — the round-45 per-snapshot fetch receipt and S026/S093/S108 anchor refresh; the
dead `brace_depth_at` helpers; the C1 counter's 8 and the C3 counter's 10 mutation survivors; a located-name
(author) check. Compound item, so fixed only when every ask is met. Found: (a) done — `corpus/SOURCES.md:140-143`
carries S265-S268 and `.ufo/evidence/round-48/freshness/sources/{S026,S048,S093,S108}.receipt.json` are committed
(round-48 C2). (b) not done — `tools/tally-audit-v2.py:135` and `tools/tally-audit-v3.py:234` still define
`brace_depth_at`, the functions have no call site (`grep -rn 'brace_depth_at(' tools/ | grep -v 'def '` → empty),
and no commit touched either file after routing (`git log 473336d9..e3729de8 -- tools/tally-audit-v2.py
tools/tally-audit-v3.py` → empty). (c) not done — the round-47 counters are unchanged
(`git log 473336d9..e3729de8 -- .ufo/evidence/round-47/calibration/measure.py .ufo/evidence/round-47/coverage/measure.py
.ufo/evidence/round-47/hardening/pool.py` → empty), so their selftest cases for the eight and ten survivors were
never added. (d) not done — no located-name check exists (`grep -rln 'located-name' tools/` → empty; only prose in
`corpus/lessons/round-47.md:108` and `SCORECARD.md:2312`). The lane itself still lists (b)-(d) as carried at
`SCORECARD.md:2367` and `:2380`. Smallest closing change (`fix_plan`): delete the two dead functions, re-pin the
two tool sha256 values in their standing rows, and name R47.5 in the newest Planned paragraph; (c) and (d) are
larger and honestly belong to a later round.

## R47.6 — run the falsification wave in the round that lands the entries — **fixed**

Ask (`:108`): run the falsification wave in the round that lands the entries; a 40-seat round below the floor
leaves the additions and restated rows unattacked. Found: round 49 both landed its entries and dispatched a
falsification wave in the same round — `.ufo/waves/round-49/w2-results.json` records `"wave": "w2"`, `"seats": 33`
and 33 results, `w1` 55 seats (`w1-results.json`), 88 seats total inside the 64-100 floor; the wave attacked the
landed rows (`corpus/lessons/round-49.md:118`: "Wave-2 semantic re-reads … found 7 of 94 rows whose excerpt did not
carry"), and the wave's existence is recorded in the L1 surface (`SCORECARD.md:2401`, "wave-2 seat
T49W2ExecC1Probe at `f181a961`"). The round-49 lesson line entered at
`54a523654964f88afcdb4325012f1f1d52d3fdbb`; the file was absent at routing. (A `.ufo/waves/` path is not citable
in the ledger, so the row cites the lesson and SCORECARD lines; the wave counts above come from
`python3 -c "import json;d=json.load(open('.ufo/waves/round-49/w2-results.json'));print(d['seats'],len(d['results']))"` →
`33 33`.)

## R47.7 — SHONEN boxes — **declined**

Ask (`:109`): "SHONEN: all four boxes remain `[~]`, and none is fully checkable by a non-author this round.
Promotion stays operator-owned." Found: `SHONEN.md:5,7,9,11` still carry four `[~]` lines and no `[x]`; the item
is an observation about an operator-owned act (the spot-check says promotion stays operator-owned), so a lane seat
can neither promote a box nor manufacture the non-author check the boxes need. Reason for declining: an
observation, not a lane-owned defect — acting on it would mean a seat promoting its own boxes, which the province
rules refuse.

## Self-check (probe, not a verdict)

Scratch clone (`git clone -q --shared <lane> /fast/scratch/hyaku/tameshi-r50/T50Disp47/lane`, toplevel asserted),
my seven rows written into `corpus/routed-defects.json` as `{"defects": [...]}` and committed there with a scratch
identity (`716e2ed`, identity `T50Disp47 <t50disp47@scratch.invalid>`), then:

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-50/c1/measure.py \
  --lane /fast/scratch/hyaku/tameshi-r50/T50Disp47/lane --rev HEAD --explain
```

Observed last line (receipt `T50Disp47.selfcheck.stdout`): `C1_R50: self=ceee320c9ad8 rev=716e2ed7cf1c7fe228fcc398ff3ec80b915317b5
defects=49 rows=7 fixed=4 open=2 declined=1 fixed_this_round=0 missing=42 extra=0 duplicate=0
spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=2
declined_bad=0 fixed_short=16 declined_over=0 this_round_short=5 total=65 C1_R50_PASS=false`.

Every EXPLAIN line naming one of my ids is accounted for:

- `EXPLAIN open-unplanned R47.2` and `EXPLAIN open-unplanned R47.5` — expected. The newest `**Planned (round`
  paragraph, `SCORECARD.md:2410`, names no `R4x.y` id at all, so no open row can satisfy the counter until the L1
  writes the ids into that paragraph. This is an L1 edit (SCORECARD.md is outside my write scope); both ids must
  be named there for these two rows to score.
- No `evidence-bad`, `key-miss`, `fixed-bad` or `declined-bad` line names any of my ids: the four fixed rows and
  the one declined row score clean, and all twelve excerpts resolved at the cited lines.
- `missing=42` names only rounds 40-46 and 48-49 (other seats' items). `fixed_short=16`, `this_round_short=5` and
  `declined_over=0` are ledger-wide floors, not row faults: my four fixes landed at `c7586b9a` / `50545328` /
  `54a52365`, all ancestors of base `e3729de8`, so they contribute `fixed_this_round=0` by construction; the
  after-base floor must be met by fixes landed in round 50.

## Limits

- The self-check ran on a scratch clone at a scratch commit, not on the lane; it is a probe of my rows, never a
  verdict on C1. I did not run the counter against the lane at any revision, and I ran no `--selftest`.
- R47.2 is a close call and I record it as such: raw receipt files for all five asks exist and are committed, but
  only under `.ufo/waves/round-48/w1/selftest/`, which is the class conformance defect 3 named. A reader who
  accepts a wave directory as an L1 receipt would mark it fixed; the counter cannot cite that path either way.
- The lane was read-only throughout; no git mutation ran in the lane or the fleet repo, nothing was installed, and
  the scratch root `/fast/scratch/hyaku/tameshi-r50/T50Disp47` was deleted after the receipts were copied here.

## Summary

R47.1 fixed (`SCORECARD.md:2334,2340` `runs 3 stable` + `.ufo/evidence/round-48/calibration/measure.py:3,8`, at `c7586b9a`).
R47.2 open: no `.ufo/evidence/` receipt for the five asks; the captures exist only under `.ufo/waves/round-48/w1/selftest/`.
R47.3 fixed: correction C1-R48-1 at `corpus/lessons/round-48.md:178-189`, at `50545328`.
R47.4 fixed: refusal re-stated with QUALITY 10 decisive at `corpus/lessons/round-48.md:270`, at `50545328`.
R47.5 open: dead `brace_depth_at` (`tools/tally-audit-v2.py:135`, `v3.py:234`), no survivor cases, no located-name check.
R47.6 fixed: round 49 landed and ran wave 2 (33 seats) the same round, `corpus/lessons/round-49.md:118`, at `54a52365`.
R47.7 declined: SHONEN promotion is operator-owned; the four `[~]` boxes stand (`SHONEN.md:5,7,9,11`).
Self-check: `fixed=4 open=2 declined=1`, `fixed_bad=0 evidence_bad=0 key_miss=0`; the two `open-unplanned` lines need R47.2/R47.5 in `SCORECARD.md:2410`.
