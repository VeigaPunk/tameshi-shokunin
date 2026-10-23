# CriticC1Exploratory — exploratory declaration review

Seat: CriticC1Exploratory

Assigned axis: **operability**. Review dimensions: declaration chronology, delivered-object identity, meaningful detector work versus execution-method evidence, and the boundary between a supporting receipt and a claim judgment. Calibration is implicated by inaccurate receipt summaries; this report makes no axis-admission judgment.

All lane-relative paths below resolve under `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. This is a read-only adversarial review, not a C1 judgment.

## 1. Was C1 declared exploratory before the content revision?

**Yes. The exploratory declaration is in the content revision's immediate parent.** This is established by committed bytes and ancestry, not merely the amendment's `before_any_data` assertion.

Evidence:

- `.ufo/evidence/round-30/contract-amendment-4.json:7-10` declares exploratory status and removes the counting target. Reading the same file with `git show 713dee6a0cae8979cf8df58944e5c82825414674:.ufo/evidence/round-30/contract-amendment-4.json` also returned that declaration, including the five-case change description at line 25. Thus these are not solely later working-tree assertions.
- `.ufo/evidence/round-30/contract-amendment-3.json:33` had already specified the pre-data response to a control meeting v4: redesign before data or declare C1 exploratory.

Exact command executed from `/tmp` (exit 0):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format="%h %cI %s" 9ed6db840dc97a0a5f4758b6b5f60cee83a61645..bb681566b18211adf8ae9c28df91e17678e3f545
```

Observed output:

```text
bb68156 2026-10-23T03:11:04-03:00 round-30: content revision — runner tally guard + behavioral selftest (23 vectors + guard stress), S092-S094 and S087 used-by, QUALITY 58-65, README round-30, knowledge entry
713dee6 2026-10-23T03:08:50-03:00 round-30 (attempt 2): C1 declared exploratory after CtlS2SymEval met v4 before data; wave-A control receipts and spec
f09d342 2026-10-23T02:37:05-03:00 round-30 (attempt 2): C1 counter v4 (sealed set sha256 only, sandboxed selftests) after CtlK8NoRun met v3 and K9 met the v4 draft, before data; control receipts
8a8d254 2026-10-23T02:12:39-03:00 round-30: C1 counter v3 after control CtlK7Keyed met v2 (before data); control receipts so far; reachability witness
e59728d 2026-10-23T01:59:47-03:00 round-30: C1 counter v2 (held-out seeded mutants) before any control or data
dcdf2d0 2026-10-23T01:56:43-03:00 round-30: freeze C1 contract and counter (operability, runner --regression tally) with base receipts
```

The separate executed command

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --no-patch --format='%H %P%n%cI%n%s' 713dee6 bb681566b18211adf8ae9c28df91e17678e3f545 9207f226e177c8a1a9a82de677df3cd9f8d1cda3
```

returned, among its metadata, these exact commit/parent lines:

```text
713dee6a0cae8979cf8df58944e5c82825414674 f09d3425258403a51422c9959e25340807982947
bb681566b18211adf8ae9c28df91e17678e3f545 713dee6a0cae8979cf8df58944e5c82825414674
```

A read-only `git ls-tree -r --name-only 713dee6a0cae8979cf8df58944e5c82825414674 -- .ufo/evidence/round-30/contract-amendment-4.json .ufo/evidence/round-30/v4/ctl2 .ufo/waves/round-30/wA/MutateTallyExtra.md .ufo/evidence/round-30/c1-measure-v4.py`, with the same environment wrapper and repository, listed the amendment, counter, and all ten `ctl2` receipt files, including `CtlS2SymEval-v4.stdout`. The decisive control receipt therefore also predates the content revision.

Smallest safe correction: none to the ordering. Say **before the content/data wave**, not literally before all observations: witness and control measurements necessarily already existed.

## 2. Did the five extra cases change an object after judgment?

**Before the exploratory judgment, not after it. The full runner changed; the frozen tally block did not.** Earlier witness/control results must not be represented as judgments of the later complete selftest.

Evidence:

- The already committed declaration, `.ufo/evidence/round-30/contract-amendment-4.json:23-27`, explicitly describes the four extra status vectors and the incomplete-loop guard stress case, and reserves the claim verdict for a named non-author reviewer.
- `.ufo/evidence/round-30/witness/fix.diff:25-57` contains the original 19-vector harness, ending without those five assertions. `tools/mutate-and-run.sh:2022-2040` contains the four vectors and guard stress. These are additions to the detector, not a changed numeric predicate or a rewritten sealed tally.
- `tools/mutate-and-run.sh:1998-2006` runs the extracted block in Bash and compares the exit and first output line. The guard stress at lines 2033-2040 requires the specific mismatch output and exit 2, not merely an arbitrary selftest failure.
- `.ufo/evidence/round-30/v4/head.stdout:59-61` names the delivered revision `bb681566b18211adf8ae9c28df91e17678e3f545` and records `sealed_block_match=1`, with `C1_R30_PASS=true` and `exit=0`. This is a fresh receipt for the final runner, not a transferred witness result.
- `.ufo/waves/round-30/spec-wC.json:198-204` assigns the subsequent judge the delivered revision, including its five extra cases. The pinned tree at `9207f226e177c8a1a9a82de677df3cd9f8d1cda3` contains no judgment report at either named wave-B or wave-C path (command below).

Exact change command executed, exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --no-ext-diff 713dee6a0cae8979cf8df58944e5c82825414674 bb681566b18211adf8ae9c28df91e17678e3f545 -- tools/mutate-and-run.sh
```

Its patch adds the runtime guard and behavioral harness in the content commit. The extra-case portion includes all four vectors `1 1 0…`, `2 2 0…`, `1 2 0…`, and `3 0 0…`, followed by the assertion `tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2`.

Smallest safe correction: preserve the distinction **same tally bytes, different full selftest** and keep every eventual judgment pinned to `bb681566…`. The available record does not support a post-judgment object swap. The older coverage findings remain development evidence, not blind confirmation of the added cases.

## 3. Is CtlS2SymEval a control that skips the work?

**It skips native execution by the new detector, but it does not skip semantic detector work. It is a different implementation of that work.** Its passing receipt demonstrates a limit on execution-method evidence, not by itself a functionally empty detector defeating v4.

Strongest local counterexample to the broad skip-work characterization:

- `.ufo/evidence/round-30/wA/CtlS2SymEval-11.diff:274-328` implements arithmetic state transitions; lines 447-481 interpret loops, case arms, conditions, exits and output; lines 484-510 parse the actual current block, independently discover nine status names, and compare modeled exit/output against all 19 expected observations. This is not an unconditional success, label lookup, or byte allowlist.
- `.ufo/waves/round-30/wA/CtlS2SymEval.md:64-74` records removal of the last tally operand causing the same detector to report modeled SETUP instead of expected PASS and fail; restoring the original bytes passes. These are existing recorded probe results, not executions by this review.
- `.ufo/evidence/round-30/v4/ctl2/CtlS2SymEval-v4.stdout:60-62` records:

```text
C1_R30: rev=a94e51a09dcc0c31b492a716f1423a8cf3babfc9 pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8 insert_equiv=4/4 sealed_block_match=1 sealed_killed=6/6 sealed_equiv=6/6
PREDICATE: C1_R30_PASS=true
exit=0
```

- In contrast, the actual no-detector control, `.ufo/evidence/round-30/v4/ctl2/CtlK4GuardOnly-v4.stdout:47-48`, has `refused_drops=9/9` but `killed=0/13` and `C1_R30_PASS=false`.
- The written predicate in `.ufo/evidence/round-30/contract-amendment-3.json:17` scores behavior, not a trace proving which interpreter executed the selftest block. The counter itself executes the real block for its harness/runtime checks (`c1-measure-v4.py:376-417`), even when the candidate detector models it. Saying that the entire successful control run never executes the tally would therefore be false.

Impacted axis: operability, specifically what the receipt establishes about detector behavior versus implementation technique. A second interpreter introduces its own semantic authority and bounded syntax support; the control report explicitly limits that support (`CtlS2SymEval.md:23-26`). Its acceptance is not proof of complete Bash equivalence either.

Smallest safe correction: describe this as **an alternative semantic implementation that the behavioral predicate cannot distinguish from native detector execution**. Retain the exploratory declaration and frozen receipts; do not claim this proves a no-work functional bypass, universal unverifiability, or saturation. No counter change is needed for this wording correction.

### Fixable defect in the declaration's receipt summary

The control outcomes remain false, but two explanations are wrong in `.ufo/evidence/round-30/contract-amendment-4.json:12-13`:

| Control | Amendment says | Actual receipt |
|---|---|---|
| CtlS1Normalize | `sealed_killed=0/6` | `sealed_killed=6/6 sealed_equiv=5/6`; the last equivalent is rejected (`CtlS1Normalize-v4.stdout:48-62`). |
| CtlS4Sniff | `sealed_equiv=5/6` | `sealed_killed=0/6 sealed_equiv=6/6` (`CtlS4Sniff-v4.stdout:48-62`). |

This is a factual reporting defect, not evidence that CtlS2SymEval failed or that chronology reversed. Smallest safe correction: an explicit factual erratum using the committed receipts, leaving frozen files and results intact. Calibration is implicated by copying the wrong failure reasons.

## 4. Is the v4 head receipt reported only as supporting evidence?

**Yes in the existing declaration and wave specifications; not yet verifiable for a final round report, because no tameshi round-30 report was present in the inspected report locations.** Do not turn this limited finding into an assertion that final reporting has already complied.

Evidence:

- `.ufo/evidence/round-30/contract-amendment-4.json:26-27` explicitly labels the landed-head receipt supporting evidence, not the claim verdict, and names the separate reviewer rule.
- `.ufo/waves/round-30/spec-wC.json:184-188` calls the head rerun “C1 supporting evidence” and asks whether the receipt reproduces; lines 198-204 separately assign the exploratory judgment. Those artifact prompts are evidence of separation, not instructions to this critic.
- `.ufo/evidence/round-30/v4/head.stdout:59-61` is an ordinary counter receipt with a predicate line, not an exploratory-review verdict. `corpus/knowledge/regression-tally-completeness.md:2-7,45,67` expressly disclaims a lane-head result on that page.
- The executed path inventory `glob(path="/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/*;/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/**/*report*;/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-30/wB/*", hidden=true, gitignore=false, limit=100)` listed six fleet round-30 reports (`chousa.md`, `kaidoku.md`, `mori.md`, `tsukuroi.md`, `kake.md`, `kotodama.md`), none named tameshi; the lane report directory contained only `round-1/tameshi.md`. Wave B's report path was missing.

Exact pinned-presence command executed, exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 9207f226e177c8a1a9a82de677df3cd9f8d1cda3 -- .ufo/reports/round-30 .ufo/waves/round-30/wB/JudgeC1.md .ufo/waves/round-30/wC/JudgeC1.md
```

Observed output: none.

Smallest safe correction: the eventual final report must place `v4/head.stdout` under supporting observations and cite the separate named review and its reasons for any exploratory verdict. Until that report exists, final-report compliance remains unobserved. This critic does not supply the missing judgment.

## Execution and bounds

Only this report was written. No production edits, Git writes, `jj` commands, subagents, additional model runtimes, gates, selftests or counter reruns were performed. Forbidden scratch trees were not opened. All shell commands were finite read-only Git queries with the Git environment variables unset and optional locks disabled; they returned. No process tree or service was started that needs termination. Receipt outputs above are identified as recorded evidence rather than newly exercised verification. Tools installed or updated: none.
