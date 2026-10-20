# SourceFlakyPaper — S011 Paper Analysis & Empirical Limitation of Repeated Controls

**Lane / Seat:** UFO-FSD scout (`SourceFlakyPaper`), Wave 1, Round 12.  
**Role:** Leaf scout advisory. No independent non-author promotion/admission authority; no subagent dispatch; leaves only.

---

## 1. Named Axes

1. **Depth:** Rigorous empirical evaluation of repeated execution limitations grounded in Shi, Bell, & Marinov (ISSTA 2019, S011).
2. **Calibration:** Exact, located quote ($\le 25$ words), verified access date, URL, and explicit distinction of source availability against unavailable/opaque sources.
3. **Epistemic Discipline:** Clear separation between observed facts, empirical lower bounds, and the non-determinism fallacy (passing $N$ controls $\neq$ proof of determinism).
4. **Hermetic Provenance & Integrity:** Complete capture within owned `.ufo/evidence/round-12/SourceFlakyPaper/` without mutating unassigned registry files or sibling worktrees.

---

## 2. Located Quote, Access Date, & URL

- **Source ID:** S011
- **Title:** *Mitigating the Effects of Flaky Tests on Mutation Testing*
- **Authors:** August Shi, Jonathan Bell, Darko Marinov (University of Illinois at Urbana-Champaign & George Mason University)
- **Publication Venue:** Proceedings of the 28th ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA ’19), July 15–19, 2019, Beijing, China.
- **DOI:** `10.1145/3293882.3330568`
- **Canonical Target URL:** `https://mir.cs.illinois.edu/awshi2/publications/ISSTA2019.pdf`
- **Access Date:** `2026-10-19`
- **Source Availability & Status:** **Available** (Active, public HTTP 200 PDF fetched and verified; SHA-256 `a5c8d2a222cc1d3c53a68c4675c4c64070e94c29f5a6ab5b6dcac3c5e8bdc21c`, size 295,496 bytes). Distinguished from unavailable, dark, or paywalled sources.

### Located Primary Quote ($\le 25$ words)

> "some flaky tests may continue to show the same coverage even on our repeated executions, only to appear flaky another day."

- **Location:** Section 5 ("DISCUSSION"), Page 9, Right Column, Lines 17–21.
- **Exact Word Count:** 21 words ($\le 25$ words).

### Supporting Located Quotes

1. **Conservative Lower-Bound / Understatement:**
   > "Our results are conservative, providing a lower-bound on the impact of flakiness on mutation, and may be understating the effect."  
   *(Section 5 "DISCUSSION", Page 9, Right Column, Lines 14–16; Word count: 20 words)*

2. **Full Sentence Context (Page 9, Section 5):**
   > "Our results are conservative, providing a lower-bound on the impact of flakiness on mutation, and may be understating the effect. Our methodology requires flaky tests to demonstrate differing coverage on repeated execution, yet some flaky tests may continue to show the same coverage even on our repeated executions, only to appear flaky another day. As research on flaky tests finds new and better ways to detect them, mutation testing can benefit as well."

3. **Flakiness in Repeated Execution Outcomes:**
   > "mutation scores vary by four percentage points on average between repeated executions, and 9% of mutant-test pairs have an unknown status."  
   *(Abstract, Page 1, Column 1, Lines 13–16; Word count: 21 words)*

4. **Underestimation in Repeated Sampling:**
   > "which can provide an indication (although perhaps an underestimation) of the flakiness of each test."  
   *(Section 2.1 "Motivating Study", Page 1–2, Column 2; Word count: 15 words)*

---

## 3. Empirical Limitation of Repeated Controls

In Round 12, Capability C1 implements a repeated pristine-control gate (`repeat-control.py`: $N \ge 3$ repeated runs requiring identical exit, stdout, and stderr). S011 provides the foundational empirical boundary for why this mechanism detects manifest flakiness but **cannot prove determinism or cure flakiness**:

1. **Repeated Runs Form Only an Empirical Lower Bound:**  
   Repeatedly executing a command or test suite against pristine baselines samples only a finite slice of execution states. In Shi et al., rerunning tests 16 times in isolated JVMs uncovered significant non-deterministic coverage across 30 open-source projects (e.g., 22% of statements were non-deterministically covered across 30 projects, with up to 74% in `cloudera.oryx`). However, the authors explicitly state that this technique represents a conservative lower bound: flaky tests can pass identical runs repeatedly throughout the sample window, revealing flakiness only on a subsequent execution or under different environmental conditions ("only to appear flaky another day").

2. **Absence of Failure $\neq$ Determinism:**  
   In Table 1 of S011, the motivating study observed *zero* test assertion failures across 17 runs across all 30 projects ("to the casual observer, there are no flaky tests"). Despite zero outcome failures, massive internal non-determinism was present (5,736 tests non-deterministically covered statements, affecting 987,788 statement-test pairs). Thus, identical pass outcomes across $N$ repeats do not guarantee deterministic execution.

3. **Implications for Gate Calibration (C1):**
   - **Fail-Closed on Mismatch:** When $N \ge 3$ control runs diverge in exit code, stdout, or stderr (`controls_mismatch` exit 1), the gate definitively catches non-determinism.
   - **Could-Not-Evaluate on Baseline Non-Zero:** If the pristine command itself fails (`baseline_nonzero` exit 2), the control cannot serve as a valid reference.
   - **No Flakiness Cured / No Determinism Proven:** Passing $N \ge 3$ control runs (`controls_match` exit 0) confirms that the baseline was consistent across those specific $N$ runs. It **does not cure flakiness** and **must never be claimed as mathematical or empirical proof of determinism**.

---

## 4. Owned Paths & Evidence Retention

All generated artifacts are strictly contained within this seat's assigned directory boundaries:

- **Owned Evidence Directory:** `.ufo/evidence/round-12/SourceFlakyPaper/`
  - `.ufo/evidence/round-12/SourceFlakyPaper/ISSTA2019.pdf`: Full pristine PDF downloaded directly from Illinois MIR repository (295,496 bytes; SHA-256 `a5c8d2a222cc1d3c53a68c4675c4c64070e94c29f5a6ab5b6dcac3c5e8bdc21c`).
  - `.ufo/evidence/round-12/SourceFlakyPaper/page-9.txt`: Exact text dump of Page 9 extracted with `pdftotext`, capturing Section 5 Discussion and Threats to Validity.
  - `.ufo/evidence/round-12/SourceFlakyPaper/page-2.txt`: Exact text dump of Page 2 capturing Section 2 Background, Listing 1, and Section 2.1 Motivating Study.
  - `.ufo/evidence/round-12/SourceFlakyPaper/excerpt.txt`: Human-readable summary of located quotes, page offsets, and context.
  - `.ufo/evidence/round-12/SourceFlakyPaper/evidence.json`: Machine-readable metadata record (DOI, URL, SHA-256, access date, located quote, word count, location).
- **Owned Wave Report:** `.ufo/waves/round-12/w1/SourceFlakyPaper.md`
- **Unmodified Production Files:** `corpus/SOURCES.md`, `PROVINCE.md`, `tools/mutate-and-run.sh`, and all sibling workspaces remain completely untouched.

---

## 5. Risks & Threat Analysis

1. **Epistemic Overreach (False Confidence):**  
   Systems using repeated control gates risk assuming that $N=3$ identical runs guarantee determinism. Downstream lanes must explicitly preserve the invariant: *controls_match establishes only that non-determinism was not observed in $N$ trials; it does not prove determinism.*
2. **Latent Coverage Non-Determinism:**  
   Even CLI tools that emit byte-identical stdout/stderr may execute different internal code paths due to thread scheduling, hash randomization, or garbage collection (as S011 observed with Java finalizers). Repeated blackbox executions cannot detect latent state drift if output is coarse-grained.
3. **Distinction from Unavailable Sources:**  
   S011 is fully available and digested. However, when evaluating empirical claims across the corpus, any secondary citation lacking direct accessible PDF/source artifacts must be tagged as an unavailable source rather than assumed verified.

---

## 6. Tooling Record

- `curl`: Pre-installed `/usr/bin/curl` (curl 8.11.1). Used to fetch PDF artifact.
- `sha256sum`: Pre-installed `/usr/bin/sha256sum` (GNU coreutils 9.5). Used to compute SHA-256 digest.
- `pdftotext`: Pre-installed `/usr/bin/pdftotext` (poppler 24.12.0). Used to extract verbatim page text.
- No new packages or tools installed or updated.
