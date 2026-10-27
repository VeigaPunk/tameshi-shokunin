source: S263 — https://arxiv.org/abs/2607.09345 — §Abstract — arXiv:2607.09345v1
verified-at: 2026-10-25
recheck: 365d — `curl -fsSL 'https://arxiv.org/abs/2607.09345' | grep -cF 'C-IDoFT is a controlled counterfactual, not a benchmark for reuse'` (expect a non-zero count; ran 2026-10-25 → 3, page 44,459 bytes, sha256 `16ecdefca1f247d3acef2439576ca380bd0bacdd2fa1215e16c71006547a925d`, `cmp`-identical to the committed snapshot)
ground: F3 — determinism precondition, flaky-aware verdicts (`corpus/README.md` F3 row: one control per sweep → N ≥ 3 byte-identical controls, or a named mismatch). F7 is not claimed here; §3 states why.

# Flakiness is not a static property of test code: the posted counter-case an execution-evidence verdict has to answer

Snapshot: the arXiv abstract page of arXiv:2607.09345v1 [cs.SE], *How Far Are We from Detecting Flaky Tests? On the Limits of Code-Based Detection* — Ömer Oktay Gültekin, Alexander Berndt, Jonathan Bell, Thomas Bach, Sebastian Baltes — `[Submitted on 10 Jul 2026]`, submission history `[v1] Fri, 10 Jul 2026 12:24:25 UTC (34 KB)`, `Comments: 15 pages, 7 figures, under review`, `Subjects: Software Engineering (cs.SE)`. Committed at `.ufo/evidence/round-47/coverage/sources/arxiv-2607.09345-abs.html` (sha256 `16ecdefca1f247d3acef2439576ca380bd0bacdd2fa1215e16c71006547a925d`, 44,459 bytes), fetched and re-fetched byte-identically on 2026-10-25; its text was extracted with `.ufo/evidence/round-45/freshness/measure.py` (sha256 `ba64041f49ffcf15bb0d881604a5fe3ccf9d24e56f72bef055035fbe3d27c6ed`). Every quotation below was re-located in the extracted text of the committed snapshot; the number beside each quote is its whitespace-token count after the coverage counter's fold, and all of them are absent from the committed package copy `.ufo/evidence/round-47/assimilation/package/r8-flakiness-not-static.md` except the thesis sentence the package already quoted (marked below). The paper is posted 2026-07 and is marked `under review`; no venue is stated in this entry. **This entry is grounded on the abstract text alone** — the abstract is not the paper's evidence, and the paper body (PDF/HTML) was not fetched.

## 1. What the snapshot states

**The phenomenon.** "Flaky tests pass and fail on the same code version, weakening the signal of test results and disrupting continuous integration (CI) pipelines" (22 tokens).

**The state of the field as the authors see it.** "Code-based flakiness detectors report strong benchmark results, yet their use in practice remains limited" (14 tokens).

**The thesis.** The authors' own sentence is "Flakiness is not a static property of test code, which often lacks the information needed to decide whether a test is flaky" (22 tokens) — this is the sentence the package copy already carried; the rest of the quotations in this entry are absent from it.

**The finding stated about detectors and benchmarks.** "Analyzing three code-based detectors operating on test code, we found that widely used benchmarks contain shortcuts that inflate reported F1 scores" (21 tokens), and the same clause adds "shortcuts that inflate reported F1 scores and that evaluation protocols overstate generalizability" (12 tokens).

**The counterfactual dataset.** "The first, C-IDoFT (54,468 unit tests from 57 GitHub projects), keeps a developer-confirmed subset of IDoFT's flaky tests" (18 tokens), and the abstract closes its description with the caution "C-IDoFT is a controlled counterfactual, not a benchmark for reuse" (10 tokens).

**The measurement that matters for a protocol.** The authors' reimplementations "scored far above its constant baselines under the published cross-validation protocol but no better than them once projects were separated" (20 tokens). Their reading: "The high scores rested on the labeling shortcut and the evaluation protocol, not on the test code" (17 tokens).

**The second dataset.** Mined from CI logs, it "contains 86 flaky end-to-end tests that passed and failed on the same commit" (13 tokens). The split is stated: "The test code and CI log yielded a cause for 42% of them" (13 tokens) and "the other 58% required further execution evidence" (7 tokens).

**The reframing.** "we reframe it around whether an observed failure is flaky and how likely a test is to fail given its execution environment" (22 tokens).

## 2. What this does and does not say about the lane's F3 control

The F3 move (`corpus/README.md` F3 row) moves from one control per sweep to `N ≥ 3 byte-identical controls, or a named mismatch`, and its capability is `tools/repeat-control.py`, which runs one exact argv N ≥ 3 times and compares the streams. The snapshot's unit is different: detectors scored against benchmarks, and flaky tests whose cause is recovered from test code and CI logs. Neither the lane's gates nor its profile comparisons appear in it.

What the abstract can bear on is the *evidence class* of a verdict. It states that the test code and the CI log yielded a cause for 42% of the cases in its second dataset and that the remaining 58% required further execution evidence (§1, quoted in full). That is a published measurement that a static artifact — code, logs — is insufficient to decide a flaky outcome for the majority of the authors' cases. It states nothing about the lane's two-profile comparison, about bash/JS CLI suites, or about byte-identical streams. [INFERENCE] If the same insufficiency holds for the lane's cases, an F3 verdict that rests on a pin, a revision or a documented environment rather than on repeated execution is a static property read as a behavioural verdict, and the paper is the published case for not doing that.

The benchmark-shortcut finding is a protocol warning with a concrete analogue: the collapse under project separation (§1) is a score that survived the published protocol and fell once a separation the protocol omitted was applied. [INFERENCE] The lane's own kill rates and control verdicts are measured on a corpus it also curates; a protocol that never separates a case from its gate (or a sweep from its environment) is the shape of protocol this abstract reports inflating scores.

## 3. Why this is not an F7 row

F7 (`corpus/README.md`) is incremental re-sweep granularity: pin-level cadence → per-leg reuse decisions classified. The snapshot contains no statement about re-sweeping, about a cadence, or about reusing a prior leg's result; its 58% figure is about recovering the *cause* of a flaky failure, not about deciding whether an earlier sweep's verdict may be reused. [INFERENCE] A reused verdict is a static record, so the thesis is adjacent to F7 — but adjacency is not grounding, and this entry claims F3 only.

## 4. Fixture-craft meaning for this lane (the lane's reading; Inference)

- **Every F3 control verdict should carry the evidence class that decided it.** The concrete rule this entry argues for: a verdict is `execution` only when N ≥ 3 byte-identical controls decided it; when the deciding evidence is a pin, a revision or a documented environment, the verdict prints and records `static-only` and may not print a pass. `tools/repeat-control.py`'s output and any SCORECARD row that consumes it should carry that field beside the verdict, so a reader can tell which half of the evidence a pass rests on. This is the lane's reading of the abstract, not a claim the abstract makes about this lane.
- **The 42%/58% split is the shape of the record to keep.** Inference: for each case whose flakiness or environment-sensitivity is asserted, the record should state whether the deciding evidence was a repeated execution or a static read, because the abstract's own dataset found the static side sufficient for a minority of cases and insufficient for the majority.

## 5. Boundary of this entry

- The snapshot is the arXiv abstract page only. It carries no journal-reference field; `Comments: 15 pages, 7 figures, under review` is the whole of its status, so no venue and no peer-review outcome is claimed.
- The abstract reports the authors' own datasets (C-IDoFT, the CI-log mined set) and their own reimplementations; no gate of this lane is in it. The transfer in §2 and §4 is an analogy about method, marked as inference.
- The abstract gives no per-detector F1 value, no project-level breakdown and no environment-differential result; none is restated here. The dataset contents and the shortcut list are not read here — they are stated as the authors' claims, not verified.
- The F7 row is deliberately not grounded by this entry (§3).
- Provenance note: the package copy names four authors (Baltes, McKim, Zaidman, Wagner) while the snapshot's author list is the five names given above; this entry follows the snapshot. The package copy's `verified-at: 2026-10-24` and its 2026-07-10 posting date agree with the snapshot's submission history.
---
