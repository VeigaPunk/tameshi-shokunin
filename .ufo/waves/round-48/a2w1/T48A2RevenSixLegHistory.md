# T48A2RevenSixLegHistory — value history of `bash tools/mutate-and-run.sh --regression` (cases=9 era) against the round-48 declared set

Seat: T48A2RevenSixLegHistory (revenger, leaf, no dispatch). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, read-only;
HEAD `17cc5ce1`, content revision `c7586b9a10effc63b4bd327f976edc094c1bdc17`, base `473336d9d789f6081195e7376d17836a24666bc3`.
Scratch `/fast/scratch/hyaku/tameshi-r48/T48A2RevenSixLegHistory` (deleted before exit; no clone, no fixture repo, no gate run).
No tool installed or upgraded (nothing was needed; no `pacman` call). I authored none of what I attack.

## 0. Verdict (short)

1. The plain/P0 command has printed **three distinct `(line, exit)` tuples since cases=9**: `REGRESSION: PASS (cases=9 passed=9|0`,
   `REGRESSION: FAIL (cases=9 passed=8|1`, `REGRESSION: SETUP (cases=9 passed=8|2`. All three are recorded at P0 (not merely under a
   profile variant), the FAIL as early as round 31 and the SETUP in this round's own wave 1.
2. The round-48 row (`SCORECARD.md:2334`) declares **one** member, `PASS passed=9|0`, class `stable`. Its declared set is a
   **proper subset** of the recorded P0 history: two recorded members are missing. No declared member is unrecorded — the PASS
   value is the most-recorded value on the axis.
3. `stable` is contract-legal (the counter attested exactly one member: `attested_extra=0`, `.ufo/evidence/round-48/calibration/emit-15b1521.stdout:118`)
   but factually contradicted by the lane's own record, including the sentence immediately above the row (`SCORECARD.md:2328`,
   "is known to be nondeterministic under concurrency"). Amendment 4 gives a compliant route to the second member — up to six
   `EXTRA` P0 observations — and that route was not taken (zero extras in the frozen invocation).
4. The round-47 declared member `FAIL (cases=9 passed=7` (`SCORECARD.md:2270`) is **not an observation anywhere**: its only exact
   textual sources are the runner's own selftest vectors (`tools/mutate-and-run.sh:2024,2026`). Round 48 correctly drops it; the
   round-47 prose that asserts it was "printed once under P0" (`SCORECARD.md:2314`) still stands in the record.
5. The w1 synthesis understates the history twice: the earliest organic non-PASS is round 31, not round 47
   (`.ufo/waves/round-31/w1/CtlLabelShortcut.md:227,242-253`, B7; `.ufo/waves/round-32/w1/CtlHeaderV2.md:111,117-120`, B9), and the
   SETUP face *has* been observed organically at P0 (`.ufo/waves/round-48/w1/T48CritLoad.md:59`) although
   `.ufo/waves/round-48/w1/T48RevenRegression.md:203` says it has not.

## 1. The object, reconstructed from the pinned bytes

`tools/mutate-and-run.sh` (`--regression` since r4-2, nine legs since r26; the row name "six-leg regression ledger" is kept as an
id). For the standing statement the frozen argv is **not** the bare command: `.ufo/evidence/round-47/calibration/statements.json`
(sha256 `924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56`, the same file the round-48 section pins) gives

```
"argv": ["bash","tools/mutate-and-run.sh","--regression","--workdir","{work}/regression-wd"], "cwd": "mirror",
"obs": "^(REGRESSION: \\w+ \\(cases=\\d+ passed=\\d+)", "sha_file": "tools/mutate-and-run.sh", "timeout": 2700
```

so the counter's P0 cell already includes `--workdir` and a mirror; "plain/P0" in this report therefore means: the frozen argv,
host environment, real sibling repos, no dependence-removing shim. Exit map (`tools/mutate-and-run.sh:1442,1449,1462`): FAIL 1,
SETUP 2, PASS 0 (`case-tally mismatch` is exit 2 as well, `:1457-1458`).

The observed value is a truncation: `obs` stops at `passed=\d+`, so the compared member is `REGRESSION: <WORD> (cases=9 passed=N`
plus the exit code. Class grammar (contract amendment 3): `stable` = exactly one member over the R=3 rounds; `nondeterministic` =
two or three; a member counts only if the counter observed it at REV in the same invocation (amendment 4), with up to six `EXTRA`
P0 observations as the only additional route. Committed files under `.ufo/evidence/round-48/calibration/observations/` are
"evidence for the report only, never attestation" (amendment 4).

Which command produced each recorded line matters, and the histories are not interchangeable:

- **R — raw receipt**: the invocation's own stdout committed under `.ufo/evidence/` or as a seat receipt file.
- **Q — report-quoted run**: the seat report quotes the run's stdout, the raw file lived in scratch and is not committed.
- **V — variant**: real invocation, but argv/profile/fleet layout deliberately differs from P0 (bare mirror, removed sibling,
  P4/P5 shims).
- **F — fixture**: the string was emitted by the tally harness with injected leg statuses, by a mutant of the tool, or by a
  doctored expected table. Never an observation of the tree.

## 2. Method (reproducible)

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin grep -n -E \
  'REGRESSION: (PASS|FAIL|SETUP) \(cases=' \
  c7586b9a10effc63b4bd327f976edc094c1bdc17 -- .ufo SCORECARD.md corpus
```

1743 matching captures. They were classified by two independent markers: (a) the file carries a real invocation header
(`REGRESSION_TOOL`/`REGRESSION_EXPECT`; 52 files) or a counter `PROFILES`/`STATEMENT` cell; (b) the surrounding line is a harness
vector (`tally harness`, `HARNESS_CHECK`, `witness.sh`, `SUMMARY_PROBE`, `Seal*`/`Ctl*` tables, `probe-tally`). Per-round
inventories of both classes were then read at the source. Every value in §3 was opened in its file; no value is inferred from a
row or from another report.

## 3. Value history since cases=9 (round 26) — the recorded table

### 3.1 `REGRESSION: PASS (cases=9 passed=9`, exit 0 — P0, organic

| round | profile / tier | source path:line |
|---|---|---|
| 26 | P0 + mirror, R | `.ufo/evidence/round-26/cite-check/regression-worktree.stdout:1,2,50` (tool `fb91ef76…`) |
| 26 | P0/Q | `.ufo/waves/round-26/w1/ColdreadPilot.md:276`; `ReplicateSweep.md:10,189,205` (clone, twice) |
| 27 | P0/Q ×8 | `round-27/w1/Read05.md:9`, `Read12.md:9` (272.95 s), `Read13.md:18`, `Read15.md:27`, `Read22.md:25`, `Read31.md:38`, `Read33.md:34`, `Read34.md:24` |
| 28 | P0/Q | `round-28/w1/Read04A.md:45` |
| 29 | P0/Q | `round-29/w1/Read02A.md:19`, `Read02B.md:44`, `Read02C.md:23` |
| 30 | P0/Q | `round-30/res/SampleBoundReads.md:92`; `round-30/wC/RegressionReplayHead.md:11,112` |
| 31 | P0/Q ×4 | `round-31/w1/DeterminismProbe.md:86` (2 in-counter + 2 isolated runs, distinct workdirs); `RemeasureA.md:21,53`; `RemeasureC.md:77` |
| 32 | P0/Q ×2 | `round-32/w2/ThenRegression.md:99,115` (runner and `--then-regression` arms) |
| 34 | P0/Q | `round-34/w1/LedgerDepth.md:260`; `ResiduePreambleSeeding.md:148,153` |
| 46 | P0, R | `.ufo/evidence/round-46/before/c1-at-freeze.stdout:3`; `.ufo/evidence/round-46/after/c1.stdout:3` |
| 46 | P0/Q | `round-46/w1/ExecStmt02.md:82`; `round-46/w2/T46ReobsB.md:15,91,100`; `T46ReobsC.md:205` |
| 47 | P0, R | `.ufo/evidence/round-47/control/emit-observed-pre-freeze.out:5,6`; `before/c1-at-freeze.stdout:5,6`; `after/c1.stdout:5,6` |
| 47 | P0/Q | `round-47/w1/T47ExecObsE.md:62,94` (run 1 and run 2 P0) |
| 48 | P0, R | `.ufo/evidence/round-48/calibration/emit-15b1521.stdout:7,30,53,76` (three rounds), `:98` (row) |
| 48 | P0/Q | `round-48/w1/T48ExecObs2.md:76` (counter run 1); `T48RevenRegression.md:65` (replay A, 449 s, load 70→87); `T48CritLoad.md:57,58,60,61,62` (base1, base2, load4, load5, load6) |

The PASS member is present in every round from 26 to 48 that ran the ledger; the rounds with no plain-command run recorded are 33
(only a mutant run, `round-33/w1/DevAccept.md:140-141`) and 36-45 (no invocation in any committed report or receipt — absence of
a run, not a different value).

### 3.2 `REGRESSION: FAIL (cases=9 passed=8`, exit 1 — organic

| round | profile / tier | source path:line | mechanism evidence |
|---|---|---|---|
| **31** | **P0, Q** | `.ufo/waves/round-31/w1/CtlLabelShortcut.md:227` (`claimed=PASS,6,6,0 observed=FAIL,9,8,1 (exit=1)`), `:242-253` (restored-source run; `REGRESSION_DEFECT bash-tsukuroi-census B7`) | B7 `measured=KILLED recorded=SURVIVED`, `flips=1` |
| **32** | **P0, Q** | `.ufo/waves/round-32/w1/CtlHeaderV2.md:111` (`claimed=PASS,9,9,0 observed=FAIL,9,8,1`), `:117-120` (B9); same report records the paired v1 log flipping **B7** | `match=9/10 recorded-killed=6 measured-killed=7 flips=1` |
| 47 | P3 (variant), R | `.ufo/waves/round-47/w1/T47ExecObsE.md:73,94` (run 2 only; run 1 P3 = PASS) | pure-`jj`-removal shim; same tsukuroi case |
| 48 | P0, R | `.ufo/evidence/round-48/calibration/observations/obs2-r47counter-base.emit.stdout:5,6` (P0, P1 and P2 cells) | round-47 counter, base tree |
| 48 | P0, R | `.ufo/waves/round-48/w1/T48ExecObs2.emit.stdout:5,6`; `T48ExecObs2.md:69,86` | run 2 of 2 on the same tree/argv; run 1 PASS |
| 48 | P0-family, Q | `.ufo/waves/round-48/w1/T48RevenRegression.md:66` (replay B, 233 s, load 32→36) | `REGRESSION_DEFECT bash-tsukuroi-census B7`, verbatim stdout at `:70-76` |

Round-18's `FAIL (cases=8` (`.ufo/evidence/round-18/coldread/traces/CR18/6.out.txt:46`) is excluded: it is a doctored-table
control (`rg-doctored`), tier F.

### 3.3 `REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1`, exit 2

| round | profile / tier | source path:line | what refused |
|---|---|---|---|
| 27 | V (sibling link removed), Q | `.ufo/waves/round-27/w1/Read12.md:11` | `bash-mado-verify: SETUP (repo_identity_mismatch …)` |
| 30 | V (empty `git init` sibling), Q | `.ufo/waves/round-30/wC/RegressionReplayHead.md:197` | `revision not found: …/mado-shokunin@eead56b2` |
| 47 | P1 (bwrap shim), R | `.ufo/evidence/round-48/calibration/observations/obs2-r47counter-base.emit.stdout:6` | profile variant |
| **48** | **P0, Q** | `.ufo/waves/round-48/w1/T48CritLoad.md:59` (base3, exit 2, wall 387.8 s) | tsukuroi **control** went RED: `CONTROL: RED … TSUKUROI_CENSUS_SELFTEST: FAIL (26 cases, 25 passed, 1 failed)` → `REGRESSION_CASE bash-tsukuroi-census: SETUP (sweep refused …)` |

Same root cause as 3.2, other face: `check()` is the same code path for the control run, so a spurious case failure makes the
pristine copy red and the sweep refuses instead of flipping a verdict (`tools/mutate-and-run.sh:533,1265`, cited at
`T48RevenRegression.md:203-206`).

### 3.4 Profile-deterministic SETUP (not P0, never counted as members)

`SETUP (cases=9 passed=4|2` = no `node`; `SETUP (cases=9 passed=0|2` = no fleet root/no other tool. Sources:
`.ufo/evidence/round-47/control/emit-observed-pre-freeze.out:6`, `before/c1-at-freeze.stdout:6`, `after/c1.stdout:6`;
`.ufo/evidence/round-48/calibration/emit-15b1521.stdout:30,53,76`. `SETUP (cases=9 passed=0 cannot-verify=9|2` = bare mirror with
no siblings: `round-31/w1/DeterminismProbe.md:90` (3/3), `round-32/w2/ThenRegression.md:29`,
`round-31/before/prefreeze-format-recon.txt:14`. All tier V.

### 3.5 `passed=7` and other tally values — fixtures only, never an observation

Every `REGRESSION: FAIL (cases=9 passed=7 …` string in the lane belongs to tier F:

- `tools/mutate-and-run.sh:2024` `'1 1 0 0 0 0 0 0 0:1:REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)'` and `:2026`
  `'1 2 0 0 0 0 0 0 0:1:REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)'` (the selftest's own tally vectors);
- the same vectors re-quoted/extracted at `.ufo/evidence/round-32/c1-measure.py:57-59`,
  `.ufo/waves/round-30/wA/MutateTallyExtra.md:80-83`, `.ufo/waves/round-30/wC/MutateHead.md:102-132`,
  `round-32/w1/CtlHarnessOnly.md:163-266`, `round-35/w2/SealStdoutWorkdir.md:34,41,48,55`;
- the behavioural witness shim with two injected failing legs, `round-35/w2/AttackQuotedHash.md:174`.

Other fixture-only strings for completeness: `PASS (cases=9 passed=8` (the dropped-operand mutant,
`round-29/w1/MutateLegSum.md:104,108,112`), `PASS (cases=9 passed=10` and `SETUP (case-tally mismatch: cases=9 counted=10)`
(`round-32/w1/EquivFamilies.md:148`, `round-30/wA/MutateTallyExtra.md:77-79`), `FAIL (cases=9 passed=1 failed=8`
(`round-30/wA/CtlS7Metadata.md:99`), `SETUP (cases=9 passed=0 cannot-verify=9` in a shim
(`round-35/w2/AttackQuotedHash.md:169`). All are harness/vector text, produced by injected statuses or mutated bytes, and none
describes a run of the frozen command on a real tree.

## 4. Answer to the two questions

**(a) Which values has the plain/P0 command ever printed since cases=9 (round 26)?**

```
V_P0(rounds 26-48) = {
  (REGRESSION: PASS  (cases=9 passed=9, exit 0),   first r26, last r48, every round that ran it (§3.1)
  (REGRESSION: FAIL  (cases=9 passed=8, exit 1),   first r31, r32, r48 (P0), + r47 under P3
  (REGRESSION: SETUP (cases=9 passed=8, exit 2)    r48 (P0, control-RED face)
}
```

`passed=7` has never been printed by the plain command. `SETUP (cases=9 passed=4|0` never appears outside P4/P5. Under the
contract's class grammar `V_P0` has three members → `nondeterministic` (the contract's cap is three); the honest class today is
`nondeterministic` with two members attested in this invocation's rounds plus one organic third that no current receipt attests
from inside the counter.

**(b) Does the round-48 row's declared set match that history?**

Row (`SCORECARD.md:2334`; emit `:98`):

```
| six-leg regression ledger | … | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9`, exit 0,
  tool sha256 `a7d3f2dd7d47`, deps `fleet-root,node`, runs 3 stable | … |
```

Declared `D = { (PASS passed=9, 0) }`.

| question | answer |
|---|---|
| recorded value missing from `D`? | **yes, two**: `(FAIL passed=8, 1)` and `(SETUP passed=8, 2)` — both organic at P0 (§3.2, §3.3). |
| declared member unrecorded anywhere? | **no**. `(PASS passed=9, 0)` is the best-recorded value on the axis (§3.1). |
| extra recorded values outside P0 that `D` omits? | P4/P5 SETUPs and the bare-mirror `passed=0` SETUP — correctly outside a P0 class. |
| class label `stable` supportable? | only as "the counter saw one member in these three rounds" (`attested_extra=0`, `:118`). Not as a property of the value: the same section says the statement "is known to be nondeterministic under concurrency" (`:2328`). |

## 5. Findings (path:line + the command that shows it)

**F1 — `stable` is a mislabel on a value the lane has recorded at three members.** `SCORECARD.md:2334` (`runs 3 stable`) versus
`SCORECARD.md:2328` ("is known to be nondeterministic under concurrency") and the receipts below it in the same section. The row is
amendment-4-conformant, but the class cell reads as a claim about the value, and the value has two other members recorded in the
same round's own wave 1. Show:
`git -C LANE show c7586b9a:.ufo/evidence/round-48/calibration/observations/obs2-r47counter-base.emit.stdout | sed -n '6p'`
→ `P0=REGRESSION: FAIL (cases=9 passed=8|1 P1=REGRESSION: SETUP (cases=9 passed=8|2 …`.

**F2 — the compliant route to the second member was available and not taken.** Amendment 4 admits up to six `EXTRA` P0
observations of the statement after the rounds; the frozen invocation reports `attested_extra=0`
(`.ufo/evidence/round-48/calibration/emit-15b1521.stdout:118`). With a ~7 % per-run failure rate measured on this host
(`T48RevenRegression.md:126-128`: 1 FAIL in 2 replays, 4/40 of the pinned selftest batch), six extras do not guarantee the
member — but the alternative taken (declare `stable`, disclose in prose) puts the contradicted word in the row and the truth
only in a neighbouring paragraph. Show: `grep -n 'attested_extra' .ufo/evidence/round-48/calibration/emit-15b1521.stdout`.

**F3 — the SETUP member is organically recorded at P0 and the w1 synthesis says it is not.**
`.ufo/waves/round-48/w1/T48RevenRegression.md:203` — "The same class also has a SETUP face that has not been observed
organically" — while `.ufo/waves/round-48/w1/T48CritLoad.md:59` records exactly `REGRESSION: SETUP (cases=9 passed=8
cannot-verify=1)`, exit 2, from `--regression --workdir` on a pristine clone with real siblings (its §3 gives the refused
control's verbatim `sweep.log`). The two w1 reports contradict each other, and the omitted member is the one that would make the
class three-member. Show: `git -C LANE show c7586b9a:.ufo/waves/round-48/w1/T48CritLoad.md | sed -n '57,62p'`.

**F4 — the flake's history is longer than round 47; the first organic FAIL is round 31.**
`.ufo/waves/round-31/w1/CtlLabelShortcut.md:227` (`observed=FAIL,9,8,1`) and `:242-253` (B7 defect, same leg), and
`.ufo/waves/round-32/w1/CtlHeaderV2.md:111,117-120` (B9, plus B7 in the paired v1 log) are counter-driven nine-leg replays that
printed the FAIL value at P0, with the same `bash-tsukuroi-census` defect-flip signature as round 48's replay B.
`.ufo/waves/round-48/w1/T48RevenRegression.md:128-129` states "0 in the committed replays of rounds 7-46" — true only for
committed *raw* receipts; two committed reports from rounds 31 and 32 record the FAIL. Consequence: the round-47/48 framing
("one-shot flake") understates a four-round, multi-site recurrence, which is precisely the evidence that would justify
`nondeterministic`.

**F5 — the round-47 declared member is a fixture string, and the record still asserts it as an observation.**
`SCORECARD.md:2270` declares `REGRESSION: FAIL (cases=9 passed=7`, exit 1; `SCORECARD.md:2314` asserts it "printed `FAIL
(cases=9 passed=7` once under P0". No organic occurrence exists: the only exact matches are `tools/mutate-and-run.sh:2024,2026`
(the tally vectors, whose capture is textually identical under the `obs` truncation) and the harness tables in §3.5. Round 48
dropped the member; the assertion at `:2314` and its restatement in `corpus/lessons/round-48.md:128` remain as dated literals and
still read as history. Show: `grep -n "passed=7 failed=2 setup=0" tools/mutate-and-run.sh` → `2024`.

**F6 — `SCORECARD.md:242` and `:1516` are still live cell references to a four/six-leg value.** `:242` states
`REGRESSION: PASS (cases=6 passed=6 …)`, `:1516` `cases=9 passed=9 …` with a literal `…`; `:2178` and `:2334` carry the truncated
capture. Not a defect of this round's row (the C1 counter reads the last round-48 row), but the same table carries three
non-comparable literals for one command; anyone reading `:242`/`:1516` as the current value gets an earlier leg count. Show:
`grep -n 'cases=6 passed=6 …' SCORECARD.md`.

## 6. Pre-26 ledger values (for the "every recorded six-leg ledger value" milestone)

The row id "six-leg regression ledger" was accurate only in rounds 10-15; the leg count and with it the printed `cases=` moved.
Recorded plain-command values by era:

| legs | value | exit | tier | source path:line |
|---|---|---|---|---|
| 4 | `PASS (cases=4 passed=4; …)` | 0 | R | `.ufo/evidence/round-18/coldread/traces/CR18-r3/9.out.txt:25` (historical rerun of the four-leg tool) |
| 6 | `PASS (cases=6 passed=6; …)` | 0 | R | `.ufo/evidence/round-12/runner-regression.txt:36`; `.ufo/evidence/kaika-round-1/capability-demo/h1b-regression.stdout:35` |
| 6 | `PASS (cases=6 passed=6)` | 0 | Q | `.ufo/waves/round-31/w1/RemeasureC.md:50` (old row's literal vs the 9-leg observation) |
| 7 | `PASS (cases=7 passed=7; …)` | 0 | R | `.ufo/evidence/round-16/round-gate/runner-regression.txt:41`; `.ufo/evidence/round-17/noharm-baseline-98bea7d.json:54` |
| 8 | `PASS (cases=8 passed=8; …)` | 0 | R | `.ufo/evidence/round-18/final/regression.stdout:45`; `.ufo/waves/round-21/w1/depth/regression.out:45` |
| 8 | `FAIL (cases=8 passed=7 failed=1)` | 1 | F | `.ufo/evidence/round-18/coldread/traces/CR18/6.out.txt:46` (doctored table control) |
| 8 | `SETUP (cases=8 passed=0 cannot-verify=8)` | 2 | V | `.ufo/waves/round-21/w1/depth/regression-attempt1-setup.out:13` (clone without siblings) |
| 9 | see §3 | | | |

No pre-26 round recorded a non-PASS value from the plain command on a real fleet tree; the whole non-PASS history on the plain
command begins at round 31.

## 7. Confidence and limits

- `[O]` Observed (file opened, line read): every path:line in §3, §3.5 and §6; `attested_extra=0`; the argv and `obs` regex in
  `statements.json`; the exit printers at `tools/mutate-and-run.sh:1442,1449,1457,1462`; the tally vectors at
  `:2010,2011,2024,2026,2027`.
- `[I]` Inferred: that the round-31/32 counter observations ran the same argv/environment as round 47's P0 cell (their counters
  predate the explicit P0-P5 machinery; the runs are described as counter-driven nine-leg replays in a fleet mirror with the
  frozen tool, so P0-equivalent, not P0-identical). That rounds 33 and 36-45 had no ledger run rather than a passing one — no
  invocation appears in any committed report or receipt for those rounds; absence of a run is not a value.
- Tier grading matters: the FAIL member's only committed raw stdout is the round-48 pair (`.ufo/waves/round-48/w1/T48ExecObs2.emit.stdout:6`,
  and the observations/ file that amendment 4 downgrades to report-only evidence); nothing raw is committed for rounds 31/32 or for
  replay B (all scratch, deleted). This does not make the value less real — it makes it attestation-ineligible in this invocation,
  which is exactly why the row reads `stable`.
- Not in scope, not touched: the `deps` clause of the row (`fleet-root,node`), the C1 predicate's arithmetic, the deciding run.
  `SCORECARD.md`, `corpus/`, `tools/` byte-clean under this seat: only this file was written.

## 8. Cleanup

Scratch `/fast/scratch/hyaku/tameshi-r48/T48A2RevenSixLegHistory` removed before exit (grep dump and one analysis script only; no
clone, no `/tmp` use, no fixture repo). Nothing installed; no disk-guard pass needed (no heavy pass).
