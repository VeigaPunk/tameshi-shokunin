# T48RevSpotcheckRouting — round-47 verifier spot-check → round-48 dispositions

Seat: T48RevSpotcheckRouting (w1, leaf; no subagent dispatch). Judged axis: calibration.
Date: 2026-10-26. Base read at `473336d9d789f6081195e7376d17836a24666bc3` (working tree).

Method: read `.ufo/evidence/round-48/contract.json` (all three amendments), `corpus/lessons/round-47-verifier-spotcheck.md` (conformance defects 1-5, routed defects 1-7, Discernment spot-check), `corpus/lessons/round-47.md` (Hardening paragraph), `corpus/QUALITY.md` in full (1,377 lines; criteria inventory + keyword scans), `SCORECARD.md` Planned (round 48) (`SCORECARD.md:2312`), and the w1 directory. Read-only on the lane except this report; no scratch dir created (no clone needed — all reads direct); no tools installed.

## Disposition table

| # | Item (source) | What round 48 does about it | Route | Evidence |
|---|---|---|---|---|
| CD1 | Undispatched wave / below 64-100 L2 floor; no falsification wave attacked entries, additions, restated rows (conformance defect 1) | Disposed by contract `round_shape`: two v1 waves, w1 build (32) before freeze step 2, w2 falsify (32) at the content revision; total 64, at the floor. w2 attacks exactly what round 47 left unattacked (additions, restated rows) | disposed this round | contract `round_shape` |
| CD2 | Seat report rewritten after landing: `03facb22` rewrites `.ufo/waves/round-47/w1/T47ConnCross.md` (+228/-214); `6b5ea3b1` also uncited; status-neutral (conformance defect 2) | Nothing in the round-48 contract. No existing criterion makes a landed wave/seat report append-only: criteria 20/21 cover instruments, 35 corpus prose + receipts, 45 makes a report an orthogonal artifact, 57 binds the closure head — none covers seat reports post-landing | **route to round 49**: candidate rule "a landed seat/wave report is append-only; corrections are appended dated errata" (extends criterion 35's mechanics to `.ufo/waves/**`). Reason: recurred twice in round 47 and is invisible to every current criterion | spotcheck §Step-1 defect 2 |
| CD3 | Counter selftest tallies not committed as L1 receipts (round 46 committed `selftest/c*-selftest.stdout`; round 47 did not) (conformance defect 3) | Disposed: freeze step 2 commits the two counters **and their selftests** at the contract paths with sha256 recorded in `freeze-2.json`, and scores + commits the controls; both predicate labels carry `self_pin=1`. Seats run the counters only as `--selftest` / `--only` / `--no-live` probes (measurement bounds), so the committed tallies are the L1's | receipts seat / L1 freeze-2 commit | contract `freeze_plan`, `predicate_label`s |
| CD4 | Criterion 93 falsifier has no receipt (`quality/c91-92-falsifiers.stdout` carries 91+92 only; block 93 uncommitted) (conformance defect 4) | Routed defect 2's second half covers it: the receipts seat commits the `falsifiers.sh` block-93 receipt at/before freeze step 2 (L1-owned; seats never run it as a verdict). The general gap — a criterion landing without its falsifier receipt — stays open | receipts seat this round; **route to round 49** the standing rule "a criterion's falsifier receipt is committed when the criterion lands, or the debt is named" (93 landed round 47; 91 and 92 have receipts, 93 does not) | spotcheck §Step-1 defect 4; QUALITY 91-93 falsifier lines |
| CD5 | Lesson dependence sets disagree with rows: `corpus/lessons/round-47.md:117-118` gives `six-leg regression ledger` {fleet-root, node} and `hermetic env-differential probe` {env, node}; standing rows say {env, fleet-root, node} and {bwrap, node}; deciding run observed {fleet-root, node} and {bwrap, node} (conformance defect 5 = routed defect 3) | Lesson correction, executed in round 48's corrections sweep: append a named correction for the round-47 Hardening paragraph stating all three sets per statement (lesson-set, row-set, deciding-set) and that the instability is disclosed in SCORECARD. Append-only (admission bar 4; criteria 26, 35). No counter reads the lesson, so C1 truth does not depend on it | lesson correction this round | spotcheck §Step-1 defect 5; `corpus/lessons/round-47.md` Hardening paragraph |
| RD1 | C1 standing row + repeatability: append a superseding row stating the stable observation (or a declared-unstable form the counter can score); make observation repeatable (N ≥ 3 per profile or a declared nondeterministic class); `hermetic env-differential probe` needs the same treatment (routed defect 1) | **Claim C1** (calibration, lowest non-retired axis 6): R=3 independent observation rounds over profiles P0-P5; value classes `stable` (exactly one member) / `nondeterministic` (two or three); amendment 3 fixes row grammar (`runs 3 CLASS`, `oversize` pairing rule, skip rule for rows lacking `runs 3`); counter `.ufo/evidence/round-48/calibration/measure.py` (modes `--emit`, `--selftest`); observation receipts committed under `.ufo/evidence/round-48/calibration/observations/`. Red-before is the frontier step's mined mistake: the round-47 one-shot `six-leg regression ledger` row (FAIL passed=7) fails CTL_B under the R=3 counter. Both named statements are in the 22-statement frozen set. Kill rule keeps flakiness honest: a flaky deciding observation outside V is a mismatch, not a rerun. Generalized as QUALITY criterion 95 below | claim C1 | contract C1 + amendment 3; `SCORECARD.md:2314` disclosed limit |
| RD2 | Commit selftest receipts for the three round-47 counters, `addition-lint.py` and the criterion-93 falsifier block (routed defect 2) | Same mechanism as CD3/CD4: L1 freeze step 2 (counters + selftests + sha256 in `freeze-2.json`; controls CTL_A-CTL_E for C1 and CTL_F-CTL_H for C2 scored and committed) plus the receipts seat for the block-93 falsifier receipt. Note the asymmetry: round 48's freeze plan commits the **round-48** counters' selftests; committing the round-47 instruments' receipts is the receipts seat's carried item, not a contract field | receipts seat | contract `freeze_plan`, `cheapest_controls` |
| RD3 | Lesson correction for `corpus/lessons/round-47.md:117-118` (routed defect 3) | = CD5 | lesson correction | spotcheck routed defect 3 |
| RD4 | Reject citation: when refusing `r8-predictive-test-selection-cost.md` again, cite the unopened-row reason (QUALITY 10) rather than `PROVINCE.md:14-18` (routed defect 4) | QUALITY criterion (i) drafted this round (new criterion 94 below) makes the decisive-citation form binding. The re-refusal itself is not scheduled in round 48: no discernment claim exists (`exploratory: none`; claims are C1+C2 only) | QUALITY criterion now; **route to round 49** (or the next refusal of the entry): cite QUALITY 10 clause 2 — the entry cites a staged SOURCES row the lane never opened (`grep -c 1810.05286 corpus/SOURCES.md` → 0 at the cited rev) — never `PROVINCE.md:14-18` alone; keep the recorded flip condition (an opened row tied to an own-leg F7 re-sweep decision) | spotcheck routed defect 4 + Discernment row |
| RD5a | Round-45 per-snapshot fetch receipt + S026/S093/S108 anchor refresh (carried, SCORECARD Planned round 48) | **Claim C2** (freshness, sourced): four superseding rows S265+, committed snapshots `.ufo/evidence/round-48/freshness/sources/T.*`, per-snapshot fetch receipts (`url`, `fetched_at` 2026-10-26, `http_status` 200, matching sha256), Gate lines in `corpus/lessons/round-48.md` with ≤25-word located quotes carrying required phrases, entries re-pointed with `verified-at: 2026-10-26`. Target extended to S048 (round-45 non-author quote dispute), per the C2 `type` line. Amendment 1 fixes the URL-set semantics for S093's blob-vs-raw case; amendment 2 fixes the Gate-line grammar and the extraction pipeline (citing QUALITY 91's no-fold rule). Fetch receipts already landing in w1 (`T48ExecFetchS026/S048/S093/S108.md`) | claim C2 | contract C2 + amendments 1-2; `SCORECARD.md:2312` |
| RD5b | Dead `brace_depth_at` helpers (`tools/tally-audit-v2.py:135`, `tools/tally-audit-v3.py:234`, both sha-pinned in standing rows) | Not in the round-48 contract | **route to round 49** with reason: deleting or re-pinning sha-pinned tools breaks standing-row pins and requires the criterion-24/71/80 discipline (declare the pin blast radius before the edit, re-pin or supersede, run the registered entry command); no round-48 claim carries that work, and a seat must not touch pinned tools | `SCORECARD.md:2312` |
| RD5c | C1 counter's 8 and C3 counter's 10 selftest survivors (round-47 mutation reports) | Not pre-registered in round 48; the round-48 C1 counter is a new R=3 counter whose own selftest lands at freeze step 2, but nothing claims the round-47 counters' survivors | **route to round 49**: successor hardening claim under criteria 29/83/89 (each survivor classified or killed by a named fixture); reason: not in the frozen contract, and adding it post-freeze would be an amendment after data | `SCORECARD.md:2312` |
| RD5d | Located-name (author) check for entries | Not built in round 48 | **route to round 49** with reason: round-47 lesson already routed it as "not built this round" (the attribution mistake row: no counter reads authors; CORPUS.md rule 1 is the only guard); building it this round would be unbudgeted scope | `corpus/lessons/round-47.md` Mistakes, attribution row |
| RD6 | Run the falsification wave in the round that lands the entries (routed defect 6) | Disposed by contract `round_shape` (= CD1) | disposed this round | contract `round_shape` |
| RD7 | SHONEN: all four boxes `[~]`, none fully non-author-checkable; promotion operator-owned (routed defect 7) | No round-48 claim touches SHONEN; seats are barred from it (wave bounds) | **route to round 49 / operator**: promotion stays operator-owned; making a box fully checkable needs a non-author-runnable oracle no round-48 claim supplies | spotcheck routed defect 7 |
| D8 | The `reason partly` disagreement (Discernment spot-check, `r8-predictive-test-selection-cost` reject): verdict agreed, reason disagreed — decisive reason is QUALITY 10/2 (unopened row), the `PROVINCE.md:14-18` cite is weak, flip condition = opened row tied to an own-leg F7 re-sweep decision | Round 48's answer is criterion (i) (new criterion 94): it converts the spot-check's one-off critique into a binding form — a refusal must cite the line that alone decides it and state the flip condition. The recorded flip condition is preserved verbatim in the criterion's lesson line so a future admit has its trigger. Actual re-refusal routed per RD4 | QUALITY criterion + route round 49 | spotcheck §Discernment, last data row |

Nothing in the spot-check's per-claim re-check or trend verdicts requires round-48 action beyond the items above: calibration unchanged (C1 miss) is exactly C1's work; the freshness disputes (S048/S093) are inside C2's target set; no axis was harmed, so no no-harm route is needed.

## Newness check (both proposed criteria are new)

- Last criterion is **93** (round-47 section; the file ends with criterion 93's falsifier line; 1,377 lines). **85 stays reserved** (round-45 note), so the next free numbers are **94 and 95**.
- `grep -in 'decisive|scope line|weaker|PROVINCE' corpus/QUALITY.md` → only criterion 22's "weaker rule" (selftest fixtures per excluded rule) and criterion 88's `PROVINCE.md` note (a no-harm monitor's sub-measure). No criterion governs **which** rule a refusal cites: criterion 5 only keeps rejects; 50 freezes routed-item ledgers; 34 anchors citations into moving files. Criterion (i) is new.
- `grep -in 'nondeterministic|runs 3|observation rounds|three rounds|restated|standing (row|value)' corpus/QUALITY.md` → only criterion 76's "stale count is a self-assessment mismatch, not a dated restatement". Adjacent criteria do not cover it: 11 (repeated-control verdicts never prove determinism — about controls), 71 (a changed tool forces a new row), 75 (`measured` vs `target` labels), 76 (count must equal the tree), 92 (the `deps` clause). None fixes how many observations a standing-value restatement needs or allows a declared multi-member class. Criterion (ii) is new.
- `corpus/` contains no `round-48` reference yet (grep → 0 hits): `corpus/lessons/round-48.md` does not exist at base; both criteria's `lesson:` pointers are forward references to the lesson this round writes (consistent with the C2 Gate lines that target the same file).

## Draft criterion text (numbers 94, 95; QUALITY.md house style)

### Criterion 94 — a refusal cites its decisive criterion, not a weaker adjacent line

When this lane refuses a record, entry or row, the refusal names the criterion that alone
decides the outcome — anchored by criterion number and clause or by path:line — and states
the flip condition that would admit the refused item. Citing a weaker line is a mis-citation
even when the verdict is right: a scope refusal whose class does not contain the item's
actual defect lets no reader check the decision from the cited line. A mis-cited refusal is
corrected by an appended erratum naming the decisive line; the verdict itself is never
silently re-anchored.

Lesson: `corpus/lessons/round-48.md` (the `r8-predictive-test-selection-cost.md` reject
carried `PROVINCE.md:14-18`, which refuses product domains and sibling gates, not test
selection; the decisive reason is QUALITY 10 clause 2 — the entry cites a staged SOURCES row
the lane never opened); `lesson: corpus/lessons/round-48.md`;
`corpus/lessons/round-47-verifier-spotcheck.md` §Discernment, the `reason partly` row.

Falsifier sketch (how a committed fixture fires it): a committed two-form fixture in the
round evidence dir holds the same refusal twice — once citing `PROVINCE.md:14-18` alone,
once citing QUALITY 10 clause 2 — with the decisive-line test as oracle (`grep -c
1810.05286 corpus/SOURCES.md` at the named rev → 0 entitles the refusal; the PROVINCE lines
do not mention test selection). A checker must flag the PROVINCE-only form `WEAK-CITE` and
pass the QUALITY-10 form; deleting the decisive clause from the fixture must flip the
verdict, so the check is load-bearing (criterion 29's removal rule).

### Criterion 95 — a standing value is restated only from at least three observations, or with a declared nondeterministic class

A SCORECARD row that restates a standing value carries `runs 3` in its evidence cell and
declares a value class: `stable` (one observed (line, exit) member) or `nondeterministic`
(two or three observed members). A single observation never restates a standing value,
however unchanged the tool and inputs. A row restating from fewer observations than it
declares, or declaring members nothing attests, is a self-assessment mismatch
(`unparsed` / `unattested`), and a deciding observation outside the declared class is a
mismatch, never rerun away. This complements criterion 92 (the `deps` clause: what the
statement depends on) and criterion 71 (a changed tool forces a new row); neither fixes the
observation count. A `stable` class from three agreeing observations stays a finite sample
and proves no determinism (criterion 11 still applies to any control built on it).

`lesson: corpus/lessons/round-48.md` (the round-47 one-shot `six-leg regression ledger`
standing row — FAIL passed=7 — fails CTL_B under the R=3 counter; `hermetic env-differential
probe` printed 9/9 and 2/9 under the same profile P1, the SCORECARD disclosed limit);
`corpus/lessons/round-47-verifier-spotcheck.md` routed defect 1.

Falsifier sketch: the contract's own controls are the committed fixtures, landing under
`.ufo/evidence/round-48/control/` at freeze step 2. CTL_B re-appends the round-47 rows with
`runs 3 stable` and no re-observation → the counter must print `C1_R48_PASS=false` (the
six-leg row states FAIL passed=7 while the observation prints PASS passed=9). A `runs 1` row
is not a round-48 standing row (skipped; `unparsed` counts it) → must print false. CTL_C's
three invented members must be refused as `unattested`. A committed fixture that flips any
of these to green without a re-observation is the criterion's surviving mutant.

## Residual risk and verification gaps

- The round-48 contract does not name where criteria 94/95 falsifier receipts land; the established pattern is `quality/cNN-MM-falsifiers.stdout` (round 46/47). If 94/95 are adopted, their falsifier blocks belong in that receipt family at the L1, not in a seat report.
- Criterion 94 has no counter this round: nothing machine-reads a refusal's citation. It fires at the next discernment refusal and at spot-check review; until then it is prose discipline. Honest labeling, not a defect — but it should not be cited as enforced before a checker exists.
- CD2's round-49 rule has no owner yet; whoever closes round 48 should route it explicitly, or it will recur a third time.
- I did not verify the w1 fetch receipts' contents (C2 seats own them) nor run any counter (bounds): this report is document-level analysis of the contract, lesson, QUALITY.md and SCORECARD.md only.
- The round-47 spot-check line numbers I cite for `corpus/lessons/round-47.md` (117-118) are quoted from the spot-check itself; my read confirms the content (Hardening paragraph) at that location, not the byte offsets.
