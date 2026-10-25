
source: S190 — https://doi.org/10.1109/TSE.2026.3729363 — §Abstract and §"Access to Document" (open-access flag) on the authors' institutional publication record (portal.fis.tum.de) — IEEE Transactions on Software Engineering, online date 2026-09-19 — fetched 2026-10-23
verified-at: 2026-10-23
recheck: 365d — re-run `curl -fsSL 'https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/' | grep -c 'up to 3'` (expect a non-zero count; the string was present in the copy opened 2026-10-23)
ground: F3 (determinism precondition, flaky-aware verdicts); also F5

# The rerun that decides a failure is flaky is the same mechanism that misses most flaky failures

## What the source states

S190 (Leinen, Gruber, Erdogan, Stahlbauer, Pretschner; IEEE TSE 2026, open
access per the institutional record):

- "We analyzed 8.8 billion test executions from four industry-scale projects
  over two-month periods."
- "All apparently deterministic failures were systematically validated
  **through reruns in fresh environments** within the projects' original CI
  infrastructure to identify undetected flaky failures."
- "We found that, across all projects, **undetected flaky failures account for
  9.8 %–16.3 % of failed pipeline runs**."
- "These flaky failure rates spike temporarily, triggered primarily by code
  changes and test reordering."
- "Additionally, **test environments significantly influence flakiness, with up
  to 3× variation in flake rates between them.**"

## What this means for the lane's F3 and F5

- **A rerun-based verdict has a known blind spot.** Modern CI reruns a failed
  test *in the same job* to decide whether it is flaky, and S190 measures that
  this mechanism misses a large class: 9.8 %–16.3 % of failed pipeline runs
  are flaky failures that the detection mechanism never flags. Inference: the
  lane's own "one green control" verdict is not merely weak (round 1's
  `S107`); it is *systematically* blind to a class of failures that a
  same-environment rerun cannot see.
- **The validation protocol is "rerun in a fresh environment".** S190 does
  not classify a failure as flaky by rerunning it where it just failed; it
  reruns it **in fresh environments inside the original CI infrastructure**.
  Inference: that is the protocol the lane's F3 precondition should state —
  a determinism claim requires a rerun in a *different* environment, not
  another run in the same one. The lane's F5 profile machinery is exactly the
  tool for that, which is why the F5 and F3 items are one measurement.
- **The environment's influence is independently confirmed and is larger than
  the lane assumed.** S190 measures up to **3×** variation in flake rates
  between environments. The lane's own F5 measurement (six gate selftests,
  none environment-sensitive) is consistent with this: the lane's *gates* are
  environment-insensitive, while real test suites are not. Inference: the
  lane should not generalise its own gates' insensitivity to the suites it
  verifies.
- **What is still unmeasured.** The lane's own F3 verdict remains unmade on
  the fleet legs; this source supplies the protocol and the blind-spot
  size, not the lane's measurement.

## Boundary of this entry

- S190's text was opened as the authors' institutional publication record
  (Pure portal) with the full abstract, the DOI and the open-access flag;
  `aaron` has no copy of this DOI (not in arXiv, no Semantic Scholar record,
  no mirror resolved).
- The numbers are four industry projects' CI data; they are not the lane's.

---
