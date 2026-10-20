# SourceSurvey — S040 Survey of Flaky Tests Evaluation Report

- **Seat**: `SourceSurvey` (UFO-FSD scout, leaf member — no subagent dispatch)
- **Wave**: Round 12, Wave 1 (`tameshi-r12-w1`)
- **Target**: S040 (`https://o-parry.github.io/papers/2021a.pdf`, DOI `10.1145/3476105`)
- **Assigned Question**: Open S040; return exact flaky definition $\le 25$ words with location and date; evaluate whether finite reruns prove determinism; own capture directory only. No invented pass or independent authority.

---

## 1. Named Axes

1. **Depth**: Comprehensive examination of S040 (*A Survey of Flaky Tests*, TOSEM 2021), grounding the nature of test flakiness, its empirical manifestations, rerun-based detection strategies, and architectural limits.
2. **Calibration**: Exact, located definition ($\le 25$ words), verified publication date, venue details, and cryptographic artifact digest matching the source registry.
3. **Epistemic Boundary Discipline**: Explicit separation between observed facts, empirical sampling limits, and universal invariants: finite repeated executions ($N \ge 3$) screen for baseline stability but **never prove determinism or cure flakiness**.
4. **Hermetic Provenance & Integrity**: Strict containment of artifacts within owned seat directory `.ufo/evidence/round-12/SourceSurvey/` and wave report `.ufo/waves/round-12/w1/SourceSurvey.md`; zero mutations to sibling directories or unassigned core files.

---

## 2. Source Metadata & Cryptographic Integrity

- **Source ID**: `S040`
- **Title**: *A Survey of Flaky Tests*
- **Authors**: Owain Parry, Gregory M. Kapfhammer, Michael Hilton, and Phil McMinn
- **Affiliations**: University of Sheffield (UK), Allegheny College (USA), Carnegie Mellon University (USA)
- **Journal**: *ACM Transactions on Software Engineering and Methodology* (TOSEM), Vol. 31, No. 1, Article 17, 74 pages
- **DOI**: `10.1145/3476105`
- **Canonical URL**: `https://o-parry.github.io/papers/2021a.pdf`
- **Publication Date**: `October 2021`
- **Access Timestamp**: `2026-10-19T23:14:00Z`
- **PDF Artifact SHA-256**: `deab832cf2d89d641193568952b47df5487dfbb833b1e62ca1d7c8cf4bed661f`
- **PDF Byte Size**: 1,807,374 bytes
- **Status**: Available (Direct author-copy PDF verified and text extracted via `pdftotext`).

---

## 3. Exact Flaky Definition ($\le 25$ Words), Location, & Date

### Primary Located Definition

> "Tests that fail inconsistently, without changes to the code under test, are described as flaky."

- **Exact Word Count**: 15 words ($\le 25$ words).
- **Location**: Abstract, Page 17:1, Line 1 of Abstract (lines 7–8 of PDF text).
- **Publication Date**: October 2021.

### Secondary In-Text Formulation

> "...a test that can be observed to both pass and fail without changes to the code under test."

- **Exact Word Count**: 20 words ($\le 25$ words).
- **Location**: Section 1 ("INTRODUCTION"), Page 17:2, Lines 57–58 of text.
- **Publication Date**: October 2021.

---

## 4. Evaluation: Do Finite Reruns Prove Determinism?

### Executive Answer

**NO. Finite reruns do NOT prove determinism.**

Finite reruns are an empirical sampling technique that can **disprove** determinism (if an inconsistent outcome or output diff is observed), but can **never prove** determinism.

### Grounding & Evidence from S040

1. **Passive Exploration Limitation (§6.2.2, p. 17:59)**:
   > "Second, a general limitation of any strategy based upon rerunning tests, is that it passively explores the non-deterministic space of test executions. In other words, repeatedly executing a test under the exact same conditions means that the more elusive flaky tests that are manifested only in rarely occurring scenarios, such as a particular execution order of multiple threads, are unlikely to be identified without a significant number of repeats." (Terragni et al. [169], cited in S040 §6.2.2).
   Rerunning a test under identical conditions passively samples the same narrow region of the execution state space. Non-deterministic thread interleavings, OS scheduling delays, garbage collection pauses, or memory layouts may require millions of executions or active stress to trigger.

2. **Persistence Beyond High Rerun Counts (§5.1.6, p. 17:39)**:
   > "...across the test suites of 24 open-source Java projects, flaky tests were still being detected after up to 10,000 reruns. This demonstrated the impracticality of straight-forward rerunning as an approach for detecting flaky tests, highlighting the need for alternative methods." (Alshammari et al. [62], cited in S040 §5.1.6).
   If flaky tests continue to emerge even after 10,000 repetitions, observing 3, 5, or 10 identical runs provides zero mathematical or empirical guarantee of determinism.

3. **Burst Lengths and Probabilistic Failure Masking (§5.1.2, p. 17:33)**:
   > Lam et al. [124] showed that flaky tests exhibit consecutive failure and pass "burst lengths"; approximately 12% of flaky tests failed more than five times consecutively before passing. Kowalczyk et al. [116] modeled flakiness probabilistically (entropy and flip rate). A test with pass probability $p = 0.99$ will pass 3 consecutive runs $97\%$ of the time by pure chance, masking its non-determinism.

4. **Threat to Experimental Validity (§Abstract, p. 17:1)**:
   > "In general, one can think of flaky tests as being a threat to the validity of any methodology that assumes the outcome of a test only depends on the source code it covers."

### Application to Round 12 Capability C1 (`repeat-control.py`)

In Tameshi Round 12, Capability C1 implements a repeated pristine-control gate:
`python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`
- Mandates $N \ge 3$ repeated runs with identical exit code, stdout bytes, and stderr bytes.
- Findings: `controls_match` (exit 0), `controls_mismatch` (exit 1), `baseline_nonzero` (exit 2), `command_unavailable` (exit 2).

**Epistemic Boundary**:
- When $N \ge 3$ runs match (`controls_match` exit 0), the gate confirms that the baseline was **consistent across those specific $N$ observed executions**.
- In strict adherence to the Round 12 contract: **"no flakiness cured or determinism proven."**
- A matching control run is a necessary screening filter against blatant non-determinism or unviable baselines, **not** a certificate of determinism.

---

## 5. Owned Paths & Artifact Retention

All artifacts produced by this seat are strictly confined to assigned paths:

- **Owned Wave Report**:
  - `.ufo/waves/round-12/w1/SourceSurvey.md` (this report)
- **Owned Evidence Directory**:
  - `.ufo/evidence/round-12/SourceSurvey/`
    - `opened.tsv`: Standard source registration record (ID, URL, access time, SHA-256, quote, location, recheck command).
    - `S040-excerpt.txt`: Exact text excerpts from S040 (Abstract, §1 Introduction, §5.1.2 Repeating Tests, §5.1.6 10,000 reruns, §6.2.2 Passive exploration).
    - `evidence.json`: Machine-readable metadata record (DOI, URL, SHA-256, quotes, word count, determinism evaluation).
    - `SHA256SUMS.txt`: Checksums for all retained evidence artifacts.

**Unmodified Files**:
No changes were made to `corpus/SOURCES.md`, `PROVINCE.md`, `tools/mutate-and-run.sh`, or any sibling worktree files.

---

## 6. Risks & Threats to Validity

1. **Epistemic Overreach (False Confidence in Determinism)**:
   - *Threat*: Engineers or downstream analysis gates may misinterpret `controls_match` (exit 0) as proof that the underlying command is deterministic.
   - *Mitigation*: Round 12 documentation and the repeated-control gate specification must explicitly state that $N=3$ runs only filter out observed flakiness; determinism remains an unproven hypothesis.
2. **Elusive Flakiness Under Low Sampling**:
   - *Threat*: Flaky tests with low transition rates ($p < 0.05$ or $p > 0.95$) or long burst lengths will pass $N=3$ controls routinely, only to fail during mutation testing, causing false kill or false survivor classifications.
   - *Mitigation*: Combine repeated controls with witness-scoped kill verdicts (C2), ensuring that mutant kills are attributed strictly to declared witness criteria rather than incidental harness flakiness.
3. **Passive Exploration Incompleteness**:
   - *Threat*: Repeated control runs without resource or concurrency stress (e.g., standard sequential execution without CPU/memory pressure) fail to trigger race conditions.
   - *Mitigation*: Maintain awareness of S040's findings that passive reruns under identical conditions miss elusive flakiness, requiring environmental variation or stress if determinism testing is to be deepened in future rounds.

---

## 7. Tooling Record

In compliance with the operator tooling directive (2026-10-19):
- `curl`: `/usr/bin/curl` (curl 8.11.1). Used to fetch author PDF.
- `sha256sum`: `/usr/bin/sha256sum` (GNU coreutils 9.5). Used to verify PDF and file digests.
- `pdftotext`: `/usr/bin/pdftotext` (poppler 26.08.0). Used to extract verbatim text from S040 PDF.
- `python3`: `/usr/bin/python3` (Python 3.13.2). Used for verification scripting.
- **Installs/Updates**: None. System tools were fully sufficient and verified.
