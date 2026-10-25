
source: S206 — https://arxiv.org/abs/2607.09345 — "How Far Are We from Detecting Flaky Tests? On the Limits of Code-Based Detection" (Baltes, McKim, Zaidman, Wagner), arXiv 2607.09345, v1 posted 2026-07-10, marked "15 pages, 7 figures, under review"
verified-at: 2026-10-24
recheck: 365d — `curl -fsSL 'https://arxiv.org/abs/2607.09345' | sed -e 's/<[^>]*>//g' | grep -c 'Flakiness is not a static property of test code'` (expect a non-zero count; the string was present in the copy opened 2026-10-24)
ground: F7 (the counter-case to a code-based re-sweep predictor) and F3 (the determinism precondition)

# The published negative result a prediction-side F7 row has to be read against

## What was observed

The authors "argue that the field is studying the wrong problem: Flakiness is
not a static property of test code, which often lacks the information needed to
decide whether a test is flaky." Analysing three code-based detectors on test
code, they "found that widely used benchmarks contain shortcuts that inflate
reported F1 scores" and that "evaluation protocols overstate
generalizability".

## What is inferred

- **This is the counter-evidence round 7's F7 needed.** Round 7 could only
  source F7's *cost* side. A cadence justified by predicting which tests to
  re-sweep needs both halves: what the prediction saves (S205) and what the
  prediction is worth believing (this row). Without the second, the first is
  a marketing number.
- **The paper's objection is aimed at exactly the lane's own method.** The lane
  measures environment sensitivity by comparing a gate's output under two
  profiles and classifying the difference — that is a *static* property (a blob
  pin, a revision, a documented environment) read as a *behavioural* verdict.
  The paper's argument is that static properties of test code are frequently
  insufficient to decide flakiness, and that benchmarks reward detectors for
  shortcuts. The lane's `S152` receipt is a standing example of the hazard: a
  static property (which revision a gate is pinned at) was read as a verdict
  about that gate's behaviour, and this round's own measurement shows the
  verdict is a coin flip (S208).
- **The benchmark-shortcut finding transfers to the lane's own corpus.** The
  lane's corpus holds measured kill rates, exactly the kind of number that can
  be inflated by a benchmark that rewards the easy case. The lane's own
  cross-language comparison note already distinguishes a narrow kill width from
  a wide one; this paper says the *measurement protocol* is where the inflation
  enters.

## What is still unknown

- The paper is marked "under review"; its claims are not peer-reviewed as
  read.
- The lane's gates are not flaky-test detectors, and the paper does not study
  environment-differential instruments. The transfer above is an analogy about
  *method*, not a claim about the lane's results.
- The datasets the authors curated and the shortcut list are not read here.

---
