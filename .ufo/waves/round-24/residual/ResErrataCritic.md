# ResErrataCritic — round-24 residual: lesson errata E–P and the Mistakes addendum vs the w1 seat reports

Seat: TameshiR24-2.ResErrataCritic-5 (critic, read-only). Target: `corpus/lessons/round-24.md` at the
lane tip `4903959687d16623adeeeae059bc010dcfc9d23f`: "After measurement" (:58-77), "Fresh wave 1"
errata E–P (:79-213), "Mistakes addendum" (:215-220), plus the Mistakes rows added at 250069f (:54-56).
Compared against all 64 `.ufo/waves/round-24/w1/*.md` reports. Read-only: file reads, `rg`, `stat`,
`sha256sum`, JSON parsing, and `git` with `GIT_OPTIONAL_LOCKS=0` (`show`, `cat-file`, `diff`, `log`,
`merge-base`). Nothing executed beyond that, because this item has no "Run" clause. Tools installed or
updated: none.

## Verdict

**The errata are directionally honest, and every check the assignment named holds.** The Erratum H
addendum's refutation of RevLiveRows' pruned-pin claim is correct. All 38 cited seat names exist in
`w1/`. The errata are append-only. They do, however, contain **two factual misstatements**, **one
scope narrowing**, **one calibration defect** (static or inferred seat results recorded as fact), and
**six omitted seat findings of medium weight**. All are fixable with an append-only erratum. None is a
tradeoff that the judge must reject, and none moves the measured 1/11 → 11/11.

## Checks the assignment named: all hold

| Check | Observed |
|---|---|
| `git -C kagi-shokunin cat-file -t fecee874` | `commit`. It resolves to `fecee8743e52eb8fb5fbb40782934cb619a1a96e`, and `merge-base --is-ancestor fecee874 HEAD` exits 0, so it is reachable, not pruned. |
| The pinned blobs | `git show fecee874…:corpus/surface-census.sh \| sha256sum` gives `275d8294…`, and `:corpus/checklist-run.sh` gives `7e5ec98b…`. Both equal `c2-contract.json:27,30` `blob_sha256`. |
| The seat's typo | `git cat-file -t feece8743e52eb8fb5fbb40782934cb619a1a96e` gives `fatal: could not get object info`. RevLiveRows.md:57-61 used this mistyped id, and its "unreachable entirely" claim (:62) rests on it. The addendum's refutation (:184-187) is correct. |
| `round21-measure.py:73-77` | At 4903959, lines 73-77 hold `git -C ROOT.parent/<repo> show rev:path`, `check=True`. This is a structural live-sibling read, as the addendum says. |
| Seat names cited in the lesson | 38 distinct names. All exist in `w1/`; none is invented. |
| Append-only | `git diff --numstat c8c5b88 4903959` gives 167 additions and 0 deletions in `lessons/round-24.md`. The knowledge entry (56/0), `QUALITY.md` (21/0) and `SCORECARD.md` (20/0) are also append-only. |
| Erratum E size | `stat -c %s replay/observations.json` = `265728`. |
| Mistakes: misrooted seat | Lane `RowAudit01.md` sha256 = `3bc5633c…`. `/home/vgpnk/Projects/shokunin/.ufo/waves/round-24` is absent. Fleet `git status --porcelain` no longer lists it. |
| Mistakes: dangling promise | `git cat-file -e c8c5b88:.ufo/evidence/round-24/after.json` exits 128; at `04657a6` it exits 0. The cited seats CorpusLesson:6, ScribeLimits:20, PredK2:191 and CorpusQuality48:21 do say this. |
| Mistakes: wave dispatch | `validation1-refused.stderr`: `unknown_role … "labrat"`. Attempts 1 and 2: "Background job limit reached (100)". Attempt 3: "Spawned 64 background agents". |
| Mistakes: monitor drift (intermediate B) | `monitor-intermediate-B.json`: rev `250069f`, 60/62, restraint 6. |
| After measurement | RunRulerAfter:3 reports 11/11, exit 0. RunRulerBase:8,44 reports output byte-identical to `before.json`. `noharm-c8c5b88.json` reports registry held 47, superseded 7. |
| RevBundleDiff transcription | 17 of 43 rows differ in bytes, none in exit codes or tokens, and 13 of the 41 pinned rows are run-varying (RevBundleDiff:14,111). Both are faithfully transcribed. |
| Wave-1 mistakes row | MutProject M05: frozen K7–K10 give T/T/T/T, and the selftest kills it (MutProject:115). MutPlan M2 survives both detectors (MutPlan:8). Both are correctly cited. |

## Defects

### D1 (medium, misstatement): Erratum I says the loose-token decision was "never recorded until now"

Lesson :133-134 says: "the loose stdout tokens are left frozen, a no-retrofill decision that was never
recorded until now (ClosureCarry, PlanWalk)."

- **Counterexample.** `git show 6a1821a:.ufo/waves/round-23/fresh-adjudication.json`, line 104, reads:
  "Preexisting loose stdout substring tokens in frozen rows. They are kept unchanged by the
  no-retrofill/frozen-argv rule."
- `git show 6a1821a:corpus/lessons/round-23.md`, lines 109-112, reads: "loose substring tokens are
  named old limitations; frozen argv/expect values are not silently strengthened".
- Both cited seats say only that the decision is absent from *round-24* artifacts:
  - ClosureCarry:46 calls the round23 adjudication's no-retrofill rule "the only stated reason".
  - ClosureCarry:80-83: "only `fresh-adjudication.json` does … the record is absent".
  - PlanWalk:23,55: R8 is "still open by explicit policy", and round23 lesson `:111` names it.
- **Impacted axes:** calibration and provenance fidelity, because the erratum misreports its own sources.

### D2 (medium, miscount, propagated): "ten predicates … cover seven mechanisms"

Lesson :66-69 says: "K4 is a carried control, so ten predicates were movable… They cover seven
mechanisms." The lesson's own grouping is:

- K1/K2 share one argv comparison;
- K5/K6 share one pin;
- K7/K8/K9 end in one refusal branch;
- K3, K10 and K11 are one mechanism each.

That gives **six** mechanisms for the ten, not seven. The source seat, CorpusContract:18-19 and
mapping table :44-52, says the eleven predicates cover seven mechanisms, "only six of those are new";
the seventh is K4's all-of-tokens control. ClosureCarry:92-93 counts differently ("9 new discriminating
mechanisms, not 11"), and the lesson does not reconcile the two counts. The same "ten … seven" wording
was copied into the knowledge errata (`replay-projection-hardening.md:46-47`) and `SCORECARD.md`
("The ten moved predicates cover seven mechanisms"). **Axis:** calibration. It overstates breadth by one.

### D3 (medium, scope narrowed): Erratum H says the row hits "live kagi objects"; it reads four siblings

Lesson :125-127 says: "`mutate-and-run-regression` executes against live kagi objects through the
sibling symlinks". The knowledge errata :80-82 repeat "against kagi `fecee874`".

- **Counterexample (executed seat evidence).** RunRegistry:21 graded from a /tmp root whose mirror had
  only a kagi sibling. 6 of the 8 ledger legs went to SETUP:
  `repo_identity_mismatch: …/fleet/{kumitate,tsukuroi,mado}-shokunin is not its own repository`. The
  row then exited 2, and the battery reported held=45/47 with exit 1 (RunRegistry:7).
- CodeLiveList:104-108 records `REGRESSION_PIN js-kimi-census … repo=…/fleet/kumitate-shokunin`, and
  "All eight ledger legs point at …/fleet/<sibling>".
- The cited ProvinceFit:35,47 also says "eight recorded fleet-ledger legs" and "live sibling repos".
- Only OverlapKagi is kagi-scoped by assignment, and the lesson inherited that narrow scope.

The same RunRegistry run is the only *executed* demonstration of the hidden live dependency. It covers
both `mutate-and-run-regression` and `round21-measure-selftest`, yet Erratum H and its addendum cite
neither RunRegistry nor CodeLiveList. CodeLiveList:30-31,145-167 independently found
`round21-measure-selftest` and reproduced it under the replay topology. The addendum credits only
RevLiveRows. **Axes:** attribution and completeness.

### D4 (medium, calibration): static and inferred seat results are recorded as fact in Errata F, G and P

The round23 adjudication marked such claims "[seat inference, not executed]"; the lesson's own S085
quote line 53 uses that form. Errata F, G and P drop the distinction:

- **Erratum F, K8**: "reading `cleanup_error` only when not held — nothing (PredK8)". PredK8:4 says:
  "static review only … I executed no selftest, ruler or mutant. Every claim about what a mutant does
  is traced from the code, not observed."
- **Erratum F, K10**: every PredK10 weakening W1–W5 is tagged `[INFERENCE]` (PredK10:52-56).
  MutProject's executed M05/M06 back only the "either disjunct" half.
- **Erratum F, K3**: PredK3:170-171 says "R4 — unexecuted by me … rest on static evaluation". The
  "sign-blind negative-exit check" case has no executed backing; MutFixtures executed only `abs` and
  `truthy`.
- **Erratum F, K9**: PredK9:7 says "static trace". The character-counting case is executed only by
  MutProject M04, which is correctly cited.
- **Erratum P**: "`--tag new-r23` now selects zero active rows and exits 0". CodeSupersession:156
  says: "derived statically … I did not execute `registry-check.py --tag new-r23`".
- **Erratum G**, bullets 4-5 (:120-121): CorpusSkill:36 marks the `--run` exit-1 cases `[STATIC]`
  (LabPlanLaneLink:120 says "[INFERENCE, not run]"). The bullets carry no citation at all; the
  "(CorpusSkill)" tag at :122 attaches only to bullet 6.

**Axis:** calibration, because tested and trusted results are conflated. The executed survivors
(MutFixtures, MutProject, MutPlan, LabPlanLaneLink, CodeProjectInputs, CodePublish) are fine as stated.

### D5 (medium, omitted findings): six seat findings appear in no erratum, no routed item and no knowledge erratum

1. **ClosureCarry F1 (:58-67): a projection that drops tokens passes K7–K11.** Changing
   `registry-replay.py:101` to keep only `stdout_contains[:1]` publishes a weaker bundle "while K7-K11
   stay green". CodeSelftestOracle F1 (:122) makes the related point: "nothing in the round asserts
   that the published `bundle.json` bytes are the bytes … `expected.json` commits to", and two of its
   weakenings "also survive the frozen eleven-predicate ruler" (:23-24). Erratum N reports only the
   selftest side ("never reads bundle.json"). The round25 route list (:150-154) has no bundle-fidelity
   or two-token fixture item, though ClosureCarry:165 routes one.
2. **MutProject M07/M08/M09 (:117-119, :127): three executed survivors of *both* detectors.** These are
   the schema check, the requirement-name type check and the stream type check. The selftest's single
   invalid fixture `{'schema':'other'}` fails for several reasons at once. Under M09, a null stdout
   raises `AttributeError` instead of exit 2. Erratum F lists only M04 from MutProject; Erratum G cites
   CodeProjectInputs' pristine-tool gaps, not these coverage gaps. `rg 'M07|M08|M09' corpus/` finds no
   round-24 hit.
3. **PredK10 W3/W4 (:54-55): survive K10 *and* the selftest.**
   - W3: deleting the `live-dependent.json` write.
   - W4: marking every row live if any row is external.

   Erratum F's K10 line (:107-108) says "the selftest only", which understates the gap. Both are
   `[INFERENCE]`, see D4.
4. **CorpusScorecard D1/D2 (:6-7, :57-69).** The SCORECARD capability row points at
   "`.ufo/evidence/round-24/` final receipts", which names no file. The harmed intermediate
   `monitor-intermediate-A.json` (rev `bd38c02`, 47/62, restraint 6; verified) appears nowhere in the
   lesson. The Mistakes addendum records the same failure class for intermediate B only.
5. **SourceS085 D2 (:23-25).** S085's teaching cell says "turn **each** routed hardening gap into a
   named predicate" (verified at `SOURCES.md:94`). By Erratum I's own count, 6/8 routed defects got a
   predicate. Erratum J records SourceS085's D1 (the range clip) but not this overclaim.
6. **CorpusContract (:55-69).**
   - K8 is "a label refinement of K7", because the real runner never emits `cleanup_error` with
     `held=True`.
   - The mutant `if max_bytes != DEFAULT_MAX or len(…) > max_bytes` passes K9 and is killed only by
     the selftest's `stream-at-limit` case. Erratum F's K9 line omits it.

Lower-weight omissions, for completeness:

- PredK4:48: checking only the first sorted requirement's stdout.
- PredK11:68-70: M5 (`realpath(normpath())`), M6 and M7 survive.
- PredK7 F5 (:140-158): weakening the runner's own `held` computation leaves K7 green; only K5/K6 flip.
- RevBundleDiff F6 (:119): exit-only rows and label-only token rows.
- RunMonitor:5: the no-harm monitor is flat across the wave and cannot discriminate.
- SentinelRun "High — selected revision code runs with the caller's authority" (:20-28): `--rev` is
  in-process code execution. Erratum K keeps only the environment inheritance.
- CodeProjectInputs A4: duplicate rows also break report accounting.

### D6 (low): the "restored" monitor claim at 671a6e2 has no retained receipt

Mistakes addendum :220 says: "two actual traced re-reads … restore 62/62 at 671a6e2". `rg 671a6e2` over
`.ufo/evidence/round-24/`, the round-21 ledger, `LOG.md` and `SCORECARD.md` finds nothing; the string
appears only in the lesson. The only post-B 62/62 receipt is
`.ufo/evidence/round-24/final-verification.json`. It is at rev `4903959` (62/62, restraint 8, depth 8,
strict), it is untracked (`git status --porcelain` shows `??`), and it was written after the tip. The
claim is very likely true, since 4903959 measures 62/62, but as written it violates QUALITY6
(executed outcome in the same entry).

### D7 (low): denominator, tally and provenance gaps

- **Erratum I's "eight routed defects" ignores three routed items.** MANIFEST `rounds[421].notes`
  routes "eight deferred repairs …, multi-token stdout fixture in the ruler, re-run guard sweep, and
  dead-falsifier coverage gap". That is 11 items, and ClosureCarry maps all 11: 9 with a mechanism,
  item 9 delegated, item 10 partial, item 11 criterion-only. The contract's `sources` cites that
  MANIFEST note, and the lesson records none of the three dispositions.
- **Erratum J's S085 "clips the array" is contested.** SourceCensus N2 (:53-55) and CorpusEntry:22
  judge `53–104` to be exactly the eight `defect` strings, matching the row title. The erratum records
  one side only. The array is `:48`–`:106`; SourceCensus:31's ":105" is wrong.
- **Erratum P undercounts the false superseded rows.** It names one, but four of the seven superseded
  rows hold false in `noharm-c8c5b88.json`:
  - `evidence-disposition-round17` (got 2);
  - `-round17-before` (got 2);
  - `evidence-disposition-round14-superseded` (got 2);
  - `command-binding-selftest`.

  RunRegistry:52 says "the 4 red superseded rows".
- **The census claim in "After measurement" cites no receipt.** It says "Census exit 0 at base 6a1821a
  (81 rows) and at c8c5b88 (83 rows)". `noharm-c8c5b88.json` has no `census` key; its keys are
  revision, observer, monitor and registry. Support exists only indirectly:
  - c8c5b88: the `sources-census` registry row inside `noharm` (`SOURCES_CENSUS: CLEAN`) and
    `measure-round16-rev` (`rows: 83`);
  - base: the round23 MANIFEST `no_harm`.

  `scripts/sources-census.sh` has no `--rev`, so "census exit 0 at <rev>" is ambiguous unless the
  receipt is named.

### Checked, no defect

- `defect-probes-selftest` is *not* a third hidden live row, although CorpusErrataCarry:33 noted that
  it clones live kagi. `ensure_kagi_clone` is reached only from probe P11 (`defect-probes.py:875`).
  `selftest()` (:960-1021) never calls it, and the replayed stdout contains no kagi or P11 line.
- The `bash-witness-count` row likewise never materialises kagi (CodeLiveList:216-219).
- Errata E, K, L, M, N and O match their cited seats on every fact checked: CorpusEntry:51,
  CorpusContract:78, SentinelRun, OverlapKumitate:64-65, CodeRunReplay F1/F2/F4/F6,
  CodeSelftestOracle F1-F4/F7, and CodePublish F1-F4.
- The RowAudit01–08 verdicts are all "no false acceptance". Errata omitting them is correct.

## Smallest safe correction

Append one erratum, "Erratum Q — errata corrections", to `corpus/lessons/round-24.md`, and add one
matching clause each to the knowledge errata and SCORECARD. Change no tool, fixture, ruler, registry or
receipt bytes. It should:

1. **For D1**, replace "never recorded until now" with "recorded in round23
   (`fresh-adjudication.json:104`, `lessons/round-23.md:109-112`) but in no round-24 artifact until now".
2. **For D2**, say "the ten movable predicates cover six mechanisms; with the K4 control, eleven
   predicates cover seven". Apply the same fix to `replay-projection-hardening.md:46-47` and SCORECARD.
3. **For D3**, change "live kagi objects" to "all four sibling object stores (kumitate, kagi, tsukuroi,
   mado: 8 legs)". Cite RunRegistry (executed: 45/47 without the sibling layout) and CodeLiveList
   alongside RevLiveRows.
4. **For D4**, tag the following `[static, not executed]`: PredK8, PredK10, PredK3's sign-blind case,
   PredK9's non-M04 cases, Erratum P's `--tag new-r23`, and Erratum G bullets 4-5. Attribute bullets
   4-5 to CorpusSkill/LabPlanLaneLink.
5. **For D5**, record each omitted item (ClosureCarry F1 with CodeSelftestOracle F1, MutProject
   M07–M09, PredK10 W3/W4, CorpusScorecard D1/D2 with intermediate A, SourceS085 D2, and CorpusContract
   K8/K9) and route them to round25. Add "a bundle-fidelity assertion plus a two-token fixture" and
   "single-cause malformed-input fixtures" to the routed list.
6. **For D6 and D7**:
   - land or cite `final-verification.json` for the post-B restoration, or retain a 671a6e2 monitor
     receipt;
   - name the 11-item closure route and its three non-defect dispositions;
   - note the contested S085 range;
   - state that four of the seven superseded rows hold false;
   - point the census sentence at the `sources-census` registry row in `noharm-c8c5b88.json`.

Not claimed: producer authentication, promotion, historical R17-CMD-BIND closure, or any numeric score
uplift.
