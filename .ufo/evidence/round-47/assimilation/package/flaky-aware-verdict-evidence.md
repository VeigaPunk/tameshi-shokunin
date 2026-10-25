
source: S155 — https://arxiv.org/abs/2302.09330 — §Abstract — arXiv:2302.09330v2 (v1 2023-02-18; last revised 2023-03-18) — fetched 2026-10-23
source: S158 — https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf — §Guidelines (RQ1 & RQ3; RQ2 & RQ3), p. 2 — author-hosted camera-ready — fetched 2026-10-23
source: S160 — https://pitest.org/faq/ — §"Is it random?" → §Timeouts and §Static initializers — pitest.org/faq/ as fetched 2026-10-23 — fetched 2026-10-23
verified-at: 2026-10-23
recheck: 365d — re-run `curl -fsSL 'https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf' | grep -c '5 reruns'` (expect 1; the string was present in the copy opened 2026-10-23)
ground: F3 (determinism precondition, flaky-aware verdicts)

# A green control is not a determinism claim: a flaky-aware verdict has a rerun budget and a run-dependent class

## What the sources state

- S158's guideline box: "one can use ≤ 5 reruns (50% less than Google's
  default ten reruns [6]) and still check correctly ≥ 82% of the time"
  (§Guidelines, RQ1 & RQ3), and for detection, "run tests in a test suite
  instead of in isolation, and run tests in different orders with fewer
  times each, rather than fewer orders with more times each" (§Guidelines,
  RQ2 & RQ3).
- S155 predicts flakiness "without such requirements on the underlying
  programming language, CI, build or test execution framework", using only
  "the tests' outcomes and durations, as well as basic information about the
  code evolution"; it "does not require additional reruns, since it gathers
  this data from existing test executions", reaching F1 95.5% from the tests'
  flip rates, the number of changes to source files in the last 54 days, and
  the number of changed files in the most recent pull request.
- S160 is the tool vendor's own admission that a verdict class is not
  absolute: mutants causing infinite loops are detected by comparing run
  times, "Both these measurements can be affected by external factors (other
  processes on the machine etc), so a mutant may be detected as timed out on
  one run, but killed or surviving on another."

## What this means for the lane's verdicts

- **A rerun budget can be small but must be non-zero.** S158 gives a
  defensible number: five reruns classify ≥ 82% of failures correctly.
  Inference for the lane's F3 move ("one control per sweep → N ≥ 3
  byte-identical controls, or a named mismatch"): the repetition requirement
  stands and a small N is defensible *if* the control is byte-identical
  rather than merely green. S158 also says the cheaper axis is *order*
  diversity, not more repeats of one order.
- **Flakiness evidence can come from records the lane already keeps.**
  S155's flip-rate feature is computable from the lane's retained per-case
  outcome tuples (the lane's own ledger keeps outcomes and exit codes per
  case). Inference: the lane can enrich a flaky-aware verdict without
  adding reruns to every sweep — the precondition S155's method satisfies.
- **Some verdict classes are run-dependent by construction.** S160 shows a
  timeout verdict changing class between runs on the same input, under
  external load. Inference: a gate that scores a timeout as a kill (the
  lane's own convention, per its held S001) must either exclude timeouts
  from its score or record the load condition — otherwise the same code can
  produce two different scores on two runs. This is a live inconsistency in
  the lane's own conventions that these sources expose; it is **not** fixed
  here.
- **None of this upgrades a single green control into a determinism claim.**
  The lane's QUALITY bar still holds: a repeated-control clean verdict never
  proves determinism (`corpus/QUALITY.md:34-37`, criterion 11).

## Boundary of this entry

- S158's and S155's results are measured on large Java systems and one
  industrial system; the lane's six fleet gates are bash/JS CLI suites with
  case counts in the tens. The transfer is **not measured** and is not
  claimed.
- S158's camera-ready was opened from the author-hosted copy; the ACM
  version was access-controlled.

---
