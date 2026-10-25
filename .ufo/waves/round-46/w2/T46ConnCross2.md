seat: T46ConnCross2
item: cross-source synthesis of C3 snapshots (S258 arXiv:2504.16777, S259 TUM TSE 2026, S260 Google Testing Blog feed) and entries (r5, r6, r9) against held knowledge (repeated-control-precondition, r8-gtest-order-and-seed) and frontier F3 (corpus/README.md:80).

## Method
Read-only inspection of committed snapshot bytes under `.ufo/evidence/round-46/coverage/sources/`, new knowledge entries `corpus/knowledge/r5-undetected-flaky-failures.md`, `r6-flaky-failures-cluster.md`, `r9-false-red-rate.md`, held knowledge entries `repeated-control-precondition.md`, `r8-gtest-order-and-seed.md`, and specification tables in `corpus/README.md` and `SKILL.md`. Scratch workspace `/tmp/tameshi-r46-T46ConnCross2/`. No mutating git commands or external runtimes invoked.

---

## Findings (5 scoped findings with file:line on both sides)

### Finding 1: Conflict Between CI Rerun Mitigations and Flakiness Blindness / Clustering
- **Snapshot sources**:
  - Google (`.ufo/evidence/round-46/coverage/sources/google-flaky-feed-6277555988217606236.json:1` [entry.content.$t]): operational mitigation relies on reruns ("re-run tests automatically when they fail... report a failure only if it fails 3 times in a row. This reduces false positives, but encourages developers to ignore flakiness...").
  - TUM (`.ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html:366`): empirical finding that same-job reruns miss 9.8%–16.3% of flaky failures ("Modern CI systems commonly rerun failed tests within the same job to identify flaky failures. Existing research predominantly analyzes data from this detection mechanism, overlooking undetected flaky failures that cause the most severe disruptions... account for 9.8 %–16.3 % of failed pipeline runs").
  - arXiv (`.ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html:124`): empirical finding that failures cluster by shared root causes ("75% of flaky tests across all projects belong to a cluster, with a mean cluster size of 13.5 flaky tests... intermittent networking issues and instabilities in external dependencies").
- **Knowledge entries**:
  - `corpus/knowledge/r5-undetected-flaky-failures.md:46-48`: observes that same-job reruns inherit systematic blindness and miss their worst class.
  - `corpus/knowledge/r9-false-red-rate.md:28-29`: infers that 84% pass-to-fail transitions make a single red weak evidence, while retries create delay without separating 3-time flakes from true breakage.
  - `corpus/knowledge/r6-flaky-failures-cluster.md:37`: infers that rerun evidence is not independent when failures cluster.
- **Cross-source pattern**:
  The entries separately treat their respective mechanisms, but do not state the joint contradiction: Google's heuristic treats reruns (up to 3 consecutive failures) as an operational filter under the assumption that true code defects fail repeatedly while flakiness resolves immediately. TUM empirically refutes that assumption, proving that same-job reruns leave 9.8%–16.3% of failed pipeline runs misdiagnosed as deterministic code failures. arXiv supplies the underlying causal explanation for TUM's blindness rate: 75% of flaky tests cluster around shared external dependencies and intermittent networking. Because the failure cause is environmental/external and persistent across the immediate rerun window, back-to-back reruns within the same job repeatedly fail, converting transient flakiness into an apparently deterministic failure.

### Finding 2: Incommensurable Denominators and Population Conflation in Entry r9
- **Snapshot sources & populations**:
  - Google (`.ufo/evidence/round-46/coverage/sources/google-flaky-feed-6277555988217606236.json:1` [entry.content.$t]): 84% is strictly over **post-submit pass-to-fail test transitions** ("about 84% of the transitions we observe from pass to fail involve a flaky test"); 1.5% is over **individual test executions** ("1.5% of all test runs reporting a flaky result"); in a 1,000-test project, ~15 tests fail per run.
  - TUM (`.ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html:366`): 9.8%–16.3% is strictly over **failed CI pipeline runs** ("account for 9.8 %–16.3 % of failed pipeline runs" across 8.8 billion executions).
  - arXiv (`.ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html:124`): 75% is strictly over **flaky test cases** ("75% of flaky tests across all projects belong to a cluster").
- **Knowledge entries**:
  - `corpus/knowledge/r9-false-red-rate.md:6`: `# Four red builds in five are not defects, by the publisher's own numbers`
  - `corpus/knowledge/r9-false-red-rate.md:28`: `If about 84% of observed pass→fail transitions in a large corpus involve a flaky test, one red observation is weak evidence of a defect. A verdict rule that reads a single red as a defect carries a false-red share of that order`
  - `corpus/knowledge/r9-false-red-rate.md:31`: `Because developers are reported to ignore legitimate failures among flaky ones, a cadence that suppresses red builds without a stated detection floor moves a real failure into the ignored class.`
- **Cross-source pattern**:
  The populations (test state transitions vs failed pipeline runs vs flaky test cases) are mathematically incommensurable. `r9-false-red-rate.md:6, :28, :31` conflates Google's test-level transition rate (84% of pass→fail transitions) with pipeline build outcomes, asserting in its title and inferences that "four red builds in five are not defects" and equating a red gate/build observation to an ~84% false-red share. Under Google's own numbers (1.5% flake rate across 1,000 tests = ~15 failing tests per build), unmitigated build failure rates approach ~100%, not 84%. In contrast, TUM measures the actual pipeline-level population and finds undetected flaky failures in only 9.8%–16.3% of failed pipeline runs. No entry notes this ~6× denominator mismatch.

### Finding 3: Tightening of `repeated-control-precondition.md` (Breakdown of the Independent Bernoulli Assumption)
- **Held entry**:
  - `corpus/knowledge/repeated-control-precondition.md:29`: `controls_match states that the N runs actually taken produced identical (exit, stdout, stderr) tuples, back to back, on one host, in one environment. ... Measured in-lane: a control failing 10% of the time still produced three matching runs in 72.9% of tries.`
  - `corpus/knowledge/repeated-control-precondition.md:35`: `python3 tools/repeat-control.py --runs N --out DIR -- COMMAND ARG... — runs the exact argv N times with stdin /dev/null ... compares the captured bytes without normalizing them. --runs must be at least 3`
- **New snapshot sources & entries**:
  - arXiv (`.ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html:124` & `corpus/knowledge/r6-flaky-failures-cluster.md:28`): 75% of flaky tests belong to clusters of mean size 13.5 sharing root causes (external dependencies and networking).
  - TUM (`.ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html:366` & `corpus/knowledge/r5-undetected-flaky-failures.md:46-47`): same-job reruns in an unchanged environment miss 9.8%–16.3% of flaky failures; test environments produce up to 3× variation.
- **Cross-source pattern**:
  `repeated-control-precondition.md:29` calculates that a 10% failing control passes 3 runs in 72.9% of tries ($0.9^3$), which relies on an implicit assumption of independent Bernoulli trials across runs. The new evidence directly tightens this limitation: because 75% of flaky failures are driven by persistent external cluster causes (arXiv) and same-environment back-to-back reruns exhibit 9.8%–16.3% blindness (TUM), runs executed "back to back, on one host, in one environment" are strongly coupled. A transient external outage or environment-dependent state persisting across the 3 runs yields an apparent `controls_match` (or false `controls_mismatch`) far more frequently than the independent binomial model predicts.

### Finding 4: Contradiction and Boundary of `r8-gtest-order-and-seed.md` (Internal Test Order vs External Environmental Variance)
- **Held entry**:
  - `corpus/knowledge/r8-gtest-order-and-seed.md:14`: `**The framework ships a shuffle and publishes the seed.** "This helps to reveal bad dependencies between tests." (:1977) — the stated purpose of the --gtest_shuffle flag (:1975)...`
  - `corpus/knowledge/r8-gtest-order-and-seed.md:20-21`: `:20`: `- **The seed is the run's ordering identity; publishing it is the reproducibility mechanism.** Because the order is undefined (:896)... the explicit --gtest_random_seed=SEED form (:1982) pins it...`; `:21`: `- **Shuffle is a detection mechanism for the lane's hazard class, not a nuisance.**`
- **New snapshot sources & entries**:
  - arXiv (`.ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html:124` & `corpus/knowledge/r6-flaky-failures-cluster.md:24`): `Through manual inspection of stack traces... we identified intermittent networking issues and instabilities in external dependencies as the predominant causes of systemic flakiness.`
  - TUM (`.ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html:366` & `corpus/knowledge/r5-undetected-flaky-failures.md:26, :29`): confirms test reordering spikes flakiness (:26), but establishes that environment variation drives up to 3× flake rate differences (:29).
- **Cross-source pattern**:
  `r8-gtest-order-and-seed.md:20-21` treats test execution order and shared-state mutation as the central hazard class, presenting `--gtest_random_seed` as the reproducibility mechanism and shuffle as the primary detection mechanism. While TUM confirms that test reordering triggers flakiness spikes (`r5:26`), arXiv's qualitative root-cause findings (`r6:24`) contradict the sufficiency of order/seed control: the predominant causes of systemic flakiness across 75% of flaky tests are external networking and dependency instabilities. These external failure modes are completely unaffected by `--gtest_random_seed` pinning and undetectable by in-process test shuffling.

### Finding 5: Obsolete F3 Next-Move Sentence in `corpus/README.md:80`
- **Corpus specification**:
  - `corpus/README.md:80`: `| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040 | open | one control per sweep (.ufo/evidence/kaika-round-1/capability-demo/README.md H2) → N ≥ 3 byte-identical controls, or a named mismatch |`
- **New knowledge entries**:
  - `corpus/knowledge/r5-undetected-flaky-failures.md:47`: `- **A fresh-environment rerun is the precondition the lane can now state with a size attached.** Inference: F3's next move stops being only "N ≥ 3 byte-identical controls" and becomes "N ≥ 3 controls that agree while the environment tuple varies" — because the source's own flaky verdicts were produced by reruns in fresh environments (4), and the failures those reruns identified as undetected flaky failures are 9.8 %–16.3 % of failed pipeline runs (5), i.e. a same-job verdict would have called every one of them a real failure.`
  - `corpus/knowledge/r6-flaky-failures-cluster.md:28`: `Inference: the clustering itself needed 10,000 suite runs to become visible, so a three-control sweep cannot detect clustering at all, and the F3 rule's N ≥ 3 is a floor on controls that bounds the distinct causes a sweep can have touched only from above`
- **Cross-source pattern**:
  The standing next-move definition in `corpus/README.md:80` ("N ≥ 3 byte-identical controls, or a named mismatch") is directly contradicted by the newly admitted evidence. Running $N \ge 3$ byte-identical controls in an unvaried environment executes the same-job rerun protocol measured by TUM as blind to 9.8%–16.3% of flakiness, while $N=3$ controls cannot observe 13.5-member systemic clusters. A reader consulting `corpus/README.md:80` would follow a protocol that the lane's own newly admitted knowledge entries demonstrate is blind to undetected flakiness.

---

## Connector Synthesis: One Bounded Proposal

### Evidence
1. `r5-undetected-flaky-failures.md:46-47`: Rerunning in an unvaried environment is blind to 9.8%–16.3% of flaky failures, while fresh environments provide detection and reveal up to 3× variation.
2. `r6-flaky-failures-cluster.md:28`: Flaky failures cluster by external dependencies; back-to-back runs in an inherited environment violate sample independence.
3. `repeated-control-precondition.md:35`: `tools/repeat-control.py` currently executes $N$ runs with the inherited environment unchanged.
4. `corpus/knowledge/hermetic-env-differential.md:6`: The lane already possesses and verified `tools/env-diff.py` (F5), which generates isolated, systematically varied environment profiles (`TZ`, `LANG`, `TMPDIR`, process umask).

### Affected Axes
- **Coverage (C3 / F3)**: Advances the F3 determinism frontier from passive literature adoption to an active, cross-environment differential protocol without claiming universal determinism.
- **Operability (C2)**: Hardens verification against environment-dependent mutants that survive back-to-back runs in an unvaried environment.
- **Calibration (C1)**: No harm; preserves existing standing SCORECARD rows and frozen measurement scripts unchanged.

### Proposed Move
**Differential Repeated-Control Harness (Synthesizing F3 determinism with F5 hermeticity)**:
Extend `tools/repeat-control.py`'s contract with an optional `--env-profile-set PROFILE_SET` flag (borrowing `tools/env-diff.py`'s declared profile vectors). When passed, `repeat-control.py` cycles through distinct sanitized environment tuples across the $N \ge 3$ runs (e.g. `UTC` vs `Asia/Tokyo`, isolated `TMPDIR`, normalized `PATH`) rather than inheriting an identical environment. A `controls_match` verdict then certifies cross-environment stability rather than same-job stability.

### Risks
1. Gate commands that legitimately emit non-normalized timestamps or locale-sensitive formats will fail raw byte comparison under varied `TZ`/`LANG` (documented in `repeated-control-precondition.md:80` and `mutation-case-kumitate-round-gate.md:1788`).
2. Mitigation: `--env-profile-set` remains an explicit opt-in flag; unflagged `--runs N` preserves byte-exact backward compatibility for existing gates.

### Verification
1. `python3 tools/repeat-control.py --selftest`: all existing 29 test cases pass unperturbed (exit 0).
2. Synthetic fixture verification: execute `--runs 3 --env-profile-set basic` on (a) a hermetic exit0 script (produces `controls_match`, exit 0), and (b) a script outputting `date +%Z` (produces `controls_mismatch`, exit 1 under differing `TZ`), confirming detection of environment-coupled flakiness.
