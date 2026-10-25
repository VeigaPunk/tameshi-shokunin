# Critic: C2 kill-oracle sourcing — "PIT Run error and Stryker RuntimeError, which neither tool counts as a kill"

Seat: L1Tameshi42.CriticOracleSource. Round 42, wave 1. Access date for every quote: 2026-10-25.
Target claim (contract `claims.C2.kill_oracle`, .ufo/evidence/round-42/contract.json:46; mirrored in
.ufo/evidence/round-42/census/measure.py:16-21): *"killed iff every battery run exits 0 with parseable
output and at least one battery case differs from its declared classification; non-zero exit, Traceback or
unparseable output is runtime_error (PIT Run error, Stryker RuntimeError), not killed."*

**Verdict: the citation is half-true.** Both tools define a run/runtime-error outcome *distinct from
Killed* (label level: true). But only Stryker *excludes it from the score*; PIT's documentation defines its
score over all mutations, and PIT's own source counts `RUN_ERROR` as **detected** (`RUN_ERROR(true)`), i.e.
kill-equivalent for scoring — the opposite of the cited claim. The analogy (mutants edit the census tool,
battery = test suite) is directionally sound, but the oracle is stricter than either vendor, and its timeout
handling diverges from both. Smallest safe correction: drop or annotate the PIT citation; rest the exclusion
on Stryker alone.

## Findings

### F1. Stryker supports the claim in full — RuntimeError is not Killed and is excluded from the score
Source: https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ (fetched via
`read <url>`, 2026-10-25; snapshot
/tmp/tameshi-r42-CriticOracleSource/docs/stryker-mutant-states.html, 27,068 B,
sha256 ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11).

- Section "Mutant states": "**Killed** When at least one test failed while this mutant was active, the mutant
  is killed." (runtime error is not that); "**Runtime error** The running of the tests resulted in an error
  (rather than a failed test) … for dynamic languages where the mutant resulted in unparsable code …
  Don't spend too much attention looking at this mutant. It is not represented in your mutation score."
- Section "Metrics": "**Valid** `detected + undetected`", "**Invalid** `runtime errors + compile errors`",
  "**Mutation score** `detected / valid * 100`". Runtime errors are therefore excluded from the denominator
  and cannot be a kill. The claim holds verbatim for Stryker.

### F2. PIT's docs label Run error as its own outcome, but never say it is excluded from the score
Sources (both fetched via `read <url>`, 2026-10-25; snapshots in
/tmp/tameshi-r42-CriticOracleSource/docs/):
- `https://pitest.org/quickstart/basic_concepts/` (pit-basic-concepts.html, 12,155 B,
  sha256 c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a), §"Running the tests":
  "**Killed** means a test caught the mutation successfully." / "A **run error** means something went wrong
  when trying to test the mutation … Under normal circumstances you should see no non viable mutations or run
  errors." Seven outcomes are listed (Killed, Survived, No coverage, Non viable, Timed out, Memory error, Run
  error); the page contains **no score formula** and no statement that run errors are excluded.
- `https://pitest.org/quickstart/commandline/` (pit-commandline.html, 23,170 B,
  sha256 f8727f23db45c8e0f077807e4ac02905405d6b694797628b74dec8a1caabec85), §"Configuration":
  "`--mutationThreshold` … a percentage (0-100) that represents **the fraction of killed mutations out of all
  mutations**." The only PIT metric that excludes anything is test strength: "`--testStrengthThreshold` …
  (killed / (killed + survived), excluding mutants where no coverage information is available)" — it excludes
  *no-coverage*, not run errors. So PIT's docs give no support for "excluded from the score"; its score is
  defined over **all** mutations.

### F3. PIT's implementation counts RUN_ERROR as detected — the operative contradiction
PIT source fetched 2026-10-25 from https://github.com/hcoles/pitest (tarball
/tmp/tameshi-r42-CriticOracleSource/pitest-master.tar.gz, 580,270 B, sha256
1a7296931ce799d3343fb6b9aad728056b718227da8d14ef04f92c4b155767d6; per-file hashes in
/tmp/tameshi-r42-CriticOracleSource/SNAPSHOTS.sha256):

- `pitest/src/main/java/org/pitest/mutationtest/DetectionStatus.java` (2,988 B):
  `RUN_ERROR(true)` — the enum's boolean is the `detected` flag; `isDetected()` returns it. `KILLED(true)`,
  `TIMED_OUT(true)`, `NON_VIABLE(true)`, `MEMORY_ERROR(true)` too. Also `getForErrorExitCode(ExitCode)` maps
  every non-OOM, non-timeout child-JVM **non-zero exit to RUN_ERROR** — i.e. PIT itself routes a crashing run
  into the class the oracle calls "not killed", but then scores it detected.
- `pitest-entry/src/main/java/org/pitest/mutationtest/statistics/ScorePrecursor.java`: `getTotalMutations()`
  sums **all** `StatusCount`s (every `DetectionStatus` value, run errors included);
  `getTotalDetectedMutations()` filters `isDetected()` (run errors included).
- `pitest-entry/src/main/java/org/pitest/mutationtest/statistics/Score.java`: score =
  `getPercentage(totalMutations, totalDetected)` — run errors raise the score.
- `pitest-html-report/src/main/java/org/pitest/mutationtest/report/html/MutationTotals.java`:
  `getMutationCoverage()` = `getPercentage(numberOfMutations, numberOfMutationsDetected)`;
  `MutationTestSummaryData.getNumberOfMutationsDetected()` counts `getStatus().isDetected()`.

Net: under PIT, a run error is scored **as detected**, kill-equivalent — the exact opposite of the claim's
"which neither tool counts as a kill" at the operational level. (The claim is only true at the label level:
a run error is not the *KILLED* status label.)

### F4. The oracle's own wording inherits the misattribution
- `.ufo/evidence/round-42/census/measure.py:16-21` (docstring): "…is `runtime_error` — PIT's 'Run error'
  and Stryker's RuntimeError, which neither tool counts as a kill — and a mutant with no differing case is
  `survived`."
- Contract `.ufo/evidence/round-42/contract.json:46` mirrors it: "non-zero exit, Traceback or unparseable
  output is runtime_error (PIT Run error, Stryker RuntimeError), not killed".
- The oracle's runtime classification (measure.py:229-260,311-317): any non-zero exit or `Traceback` in
  stderr → error; unparseable JSON → error; `TimeoutExpired` → `'timeout'` error; `oracle()` returns
  `'runtime_error'` if any error, `'killed'` iff ≥1 case differs, else `'survived'`.
- Note: the staged knowledge entry the contract says this cites
  (…/merge/tameshi/knowledge/corpus/knowledge/pit-outcome-vocabulary.md, lines 24-34) is **accurate** — it
  explicitly says the lane holds *Stryker's* score definition (S001: score = detected ÷ valid, runtime/compile
  errors excluded) and does **not** hold PIT's vocabulary, stating the two are "not the same lattice". The
  overreach is in the oracle docstring/contract paren, not in the staged entry.

### F5. Analogy assessment (our mutants mutate a census tool; theirs mutate code under test)
Sound in direction: the mutant is the edit to `tools/write-path-census-v4.py` (code under test), the battery
(fixtures + live sites) is the test suite, a kill = ≥1 case differs from its declared classification (≈ ≥1
test fails), survive = no difference, run error = the tool process cannot produce a parseable, comparable
result — a fair match to Stryker's "dynamic languages where the mutant resulted in unparsable code" and to
PIT's "something went wrong when trying to test the mutation". Epistemically the classification is right: no
observable difference ⇒ no kill claim.

Divergences (why the analogy is not a faithful *joint* PIT+Stryker authority):
1. **PIT would score the crash as detected** (F3). If PIT semantics were applied wholesale, a crashing
   mutant would satisfy "killed" — so the choice of cited tool materially changes the gate's verdict; the
   oracle silently picks Stryker while citing both.
2. **Harness granularity.** The oracle runs the tool once per battery; any non-zero exit/Traceback aborts
   every case (measure.py:229-260). PIT/Stryker run tests individually, so a mutant that makes *one* test
   fail (exception raised by mutant code, runner still completes) is a kill there. The oracle is therefore
   stricter than even Stryker: such a mutant is `runtime_error`, never `killed`. Conservative and safe
   (cannot fabricate kills), but not the vendors' semantics.
3. **Timeout.** `run_tool` maps `TimeoutExpired` → `'timeout'` → `runtime_error` (measure.py:234-235,314).
   Both vendors count timeouts as **detected** (Stryker: "It is counted as 'detected'"; PIT:
   `TIMED_OUT(true)`). The oracle's timeout handling diverges from both tools and is cited to neither — a
   second un-sourced strictness.

## Smallest safe correction
1. In `measure.py` docstring lines 19-21 and contract line 46, drop the PIT citation: "non-zero exit,
   Traceback or unparseable output is runtime_error (Stryker RuntimeError — an invalid mutant, not represented
   in the mutation score); PIT diverges and scores Run error as detected." This preserves the oracle's
   behavior (it is the right epistemic choice) while making the sourcing true.
2. Optionally record in the docstring that timeout→runtime_error is the lane's own stricter convention, not
   a vendor semantics (both vendors count timeouts as detected).

## What I could not check
- I did not execute PIT itself (no Java/PIT runtime here); the score behavior is grounded in PIT's source
  (F3) and its published threshold definitions (F2), not in a live run.
- PIT's rendered HTML report table (visual grouping of run errors) was not inspected beyond
  `MutationTotals`/`MutationTestSummaryData`; those are the classes that compute the displayed percentages.

## Tooling record
No tools installed or updated (read/curl built-ins only; `curl` preinstalled). No pacman transactions.
