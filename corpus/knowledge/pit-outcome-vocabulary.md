source: S155 — Basic concepts (PIT docs) — https://pitest.org/quickstart/basic_concepts/ — §"Running the tests" (the outcome list, Killed, Survived, No coverage, Run error) — snapshot .ufo/evidence/round-42/sources/pit-basic-concepts.html sha256 c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a — opened 2026-10-25
source: S156 — FAQ (PIT docs) — https://pitest.org/faq/ — §"Is it random?" → §Timeouts — snapshot .ufo/evidence/round-42/sources/pit-faq.html sha256 ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1 — opened 2026-10-25
source: S158 — DetectionStatus.java (PIT source, hcoles/pitest@f7fe5adf) — https://github.com/hcoles/pitest/blob/f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6/pitest/src/main/java/org/pitest/mutationtest/DetectionStatus.java — enum constants and `isDetected()` — snapshot .ufo/evidence/round-42/sources/pit-DetectionStatus.java sha256 3bf295ad53126560ec284c42b384fc3288f7b2e674da987f38d7380ec5d419c6 — opened 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-open the three committed snapshots and re-locate the quotes below; live check `curl -fsSL 'https://pitest.org/quickstart/basic_concepts/' | grep -c 'there were no tests that exercised the line of code'` (1 on 2026-10-25)
ground: F1 (mutation-score semantics and report interop)

# PIT and Stryker name the same outcomes and score them differently

Assimilated from the shokuknow `corpus-expansion-1` package (`staged:S159`, `staged:S160`
renumbered to S155, S156), re-grounded in round 42 against pages this lane opened itself;
S158 is new this round. Gate: `corpus/lessons/round-42.md`.

## What the sources state

- PIT reports one of seven outcomes per mutation (S155, §"Running the tests", snapshot
  line 163: "For each mutation PIT will report one of the following outcomes"): Killed,
  Survived, No coverage, Non viable, Timed Out, Memory error, Run error.
- Two of those outcomes are easy to merge and PIT keeps them apart (S155, snapshot
  line 179): "No coverage is the same as Survived except there were no tests that
  exercised the line of code where the mutation was created" (23 words).
- A run error is not a kill in PIT's vocabulary (S155, snapshot lines 175, 192):
  "Killed means a test caught the mutation successfully." (8 words) and "A run error means
  something went wrong when trying to test the mutation." (13 words).
- PIT's results are not fully deterministic (S156, §"Is it random?", snapshot line 293):
  "Pitest works hard to be fully deterministic, but two factors might cause the results
  to differ slightly between two runs with the same input." (24 words). The FAQ names
  two factors, timeouts and static initializers; for the first it says "a mutant may be
  detected as timed out on one run, but killed or surviving on another" (§Timeouts,
  snapshot lines 298–299, 17 words).
- PIT's code scores a run error as detected (S158, snapshot line 63, `RUN_ERROR(true)`;
  the boolean is the `detected` field returned by `isDetected()`, lines 78 and 108).
  `getForErrorExitCode` (line 91) maps every non-zero child exit that is neither out of
  memory nor a timeout to `RUN_ERROR`.
- Stryker, which the lane already holds (S001, `corpus/SOURCES.md:12`), does the
  opposite. Its Runtime error state "is not represented in your mutation score"
  (S001 snapshot re-opened 2026-10-25, `.ufo/evidence/round-42/sources/stryker-mutant-states.html`
  line 26), and runtime errors count as invalid, outside `detected / valid`.

## What this means for the lane

- **Same label, different score.** Observation: PIT and Stryker both separate "run
  error" from "killed" by name (S155, S001). Observation: PIT counts it as detected
  (S158); Stryker leaves it out of the score (S001). Inference: two reports can quote
  the same mutation score while one of them counts crashes as detections. A score
  quoted without its outcome classes and their treatment cannot be compared across
  these two tools. That answers the lane's F1 interop question in the negative for
  this pair.
- **The lane's own rule sides with neither tool's treatment of timeouts.** The lane's
  rule makes a timeout or a crash before the summary Inconclusive, not a kill, and
  keeps it out of the rate (`SKILL.md:208-212`, mapped in
  `corpus/knowledge/mutation-score-semantics.md:10` and `:71`). Stryker counts a timeout as
  detected (S001); PIT's code does too (S158, `TIMED_OUT(true)`, line 37). Held S001
  semantics describe Stryker. They do not describe the lane's recorded convention.
  S156 adds a reason for the lane's choice: a timeout verdict depends on machine load.
- **What a lane report must publish.** Publish the outcome classes and say how each
  class enters the denominator, not just the percentage. The round-42 census counter
  follows this rule for its own mutants: a crash or unparseable output is
  `runtime_error`, never `killed` (`.ufo/evidence/round-42/census/measure.py`, oracle).
  That is the lane's rule and Stryker's, not PIT's.

## Boundary of this entry

- PIT's vocabulary is PIT's; this entry sets PIT's and Stryker's side by side and
  does not map one onto the other.
- S158 is a source file pinned at one upstream commit, not a documented contract;
  PIT can change `DetectionStatus` without a docs change. A later round must re-open
  it at the then-current head before relying on it.
- The PIT path `pitest.org/quickstart/mutationcoverage/` returned HTTP 404 on
  2026-10-25. The two docs pages above are the live carriers of the outcome
  definitions.
- No PIT run was executed. The scoring claim rests on PIT's source, not on a
  measured report.
