# FlakySources — S026 Blog Post Analysis, Accessibility & Finite Rerun Caveats

**Lane / Seat:** UFO-FSD scout (`TameshiR12.FlakySources`), Wave 2, Round 12.  
**Role:** Leaf scout advisory. No independent non-author promotion or admission authority; no subagent dispatch; leaves only.  
**Target:** Article body of `https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html` (Source `S026`).  
**Scope:** Read-only inspection of source accessibility, exact located quote ($\le 25$ words), and technical evaluation of the finite rerun caveat.

---

## 1. Godspeed Framing & Named Axes

1. **Axis 1: Quotation Precision & Brevity:** Verbatim, located excerpts strictly constrained to $\le 25$ words with exact line numbers from the served HTML artifact.
2. **Axis 2: Source Accessibility & Structural Transparency:** Live verification of HTTP status, payload digests, and documentation of the Blogger duplicate-body architecture that causes scraper omission.
3. **Axis 3: Finite Rerun Caveat Rigor:** Formal technical analysis of why finite reruns mitigate false alarms but cannot cure flakiness, mask legitimate regressions, multiply feedback latency, and fail to prove determinism.
4. **Axis 4: Epistemic Bounds & Non-Interference:** Strict adherence to leaf scout boundaries; no tests or mutation runs executed; zero fleet writes outside the assigned absolute report path.

---

## 2. Source Accessibility & Structural Analysis

- **Source ID:** `S026`
- **Canonical URL:** `https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html`
- **Article Title:** *Flaky Tests at Google and How We Mitigate Them*
- **Author:** John Micco
- **Publication Date:** Friday, May 27, 2016
- **Live Access Verification (UTC):** `2026-10-20T02:44:10Z` (HTTP 200 OK)
- **Content-Type:** `text/html; charset=UTF-8`
- **Payload Dimensions:** 236,385 bytes, 6,172 lines (last line lacks trailing newline)
- **Cryptographic Digest (SHA-256):** `ca1145fbe56de30b43b66baf7372206a38abe08a55b3db13f6c7a0114d7a6c8c`
- **Accessibility Status:** **Available** (Publicly accessible, open HTTP 200 without authentication, CAPTCHA, or paywall).

### Structural Architecture & Headless Reader Hazard

The page is served via Blogger's dynamic template framework. In the raw served payload, the article body is present **twice**:
1. Inside `<script type='text/template'>` at lines **1095–1102** (for dynamic client-side template evaluation).
2. Inside `<noscript>` at lines **1124–1137** (for clients with JavaScript disabled).

**Reader Omission Hazard:**  
Standard DOM readers and headless scrapers (including the baseline `read` tool in text extraction mode) often extract post header metadata, skip the template and `<noscript>` blocks, and jump directly to `#comments` (line 1184+). This structural behavior explains why earlier round assessments noted *"reader omitted the article body"*. Raw HTML extraction of either block (`:1095-1102` or `:1124-1137`) reveals the full 5,577-character article body.

**Recheck Signature:**  
Because the text appears twice in the served document, recheck grep commands return a count of `2`, not `1`:
```bash
curl -fsSL https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | grep -c 'hardly a perfect solution'
# Returns: 2 (drift if 0)
```

---

## 3. Located Quotes ($\le 25$ Words)

### Primary Quote: Finite Rerun Caveat & Developer Behavior ($\le 25$ words)

> "This reduces false positives, but encourages developers to ignore flakiness in their own tests unless their tests start failing 3 times in a row"

- **Location:** Line 1136 (`<noscript>`) / Line 1101 (`<script type='text/template'>`)
- **Word Count:** 24 words ($\le 25$ words)
- **Context:** Discusses the unintended behavioral side-effect of introducing a 3-consecutive-failure policy for flaky tests in presubmit CI.

---

### Supporting Located Quotes ($\le 25$ words)

1. **Feedback Latency & Cost of Finite Rerun Thresholds:**
   > "The breakage will not be discovered until 3 executions of the test complete, or 45 minutes"
   - **Location:** Line 1137 (`<noscript>`) / Line 1102 (`<script type='text/template'>`)
   - **Word Count:** 16 words ($\le 25$ words)
   - **Significance:** Illustrates the direct wall-clock cost of finite retries on longer integration tests (3 iterations of a 15-minute test).

2. **Core Operational Definition of a Flaky Test:**
   > "We define a "flaky" test result as a test that exhibits both a passing and a failing result with the same code."
   - **Location:** Line 1130 (`<noscript>`) / Line 1095 (`<script type='text/template'>`)
   - **Word Count:** 21 words ($\le 25$ words)
   - **Significance:** Standardized definition anchoring flakiness in inconsistent outcomes across identical revisions, establishing non-determinism as a run-level property.

3. **Prevalence Across the Corpus:**
   > "we see a continual rate of about 1.5% of all test runs reporting a "flaky" result"
   - **Location:** Line 1130 (`<noscript>`) / Line 1095 (`<script type='text/template'>`)
   - **Word Count:** 16 words ($\le 25$ words)

4. **Pass-to-Fail Transition Noise:**
   > "about 84% of the transitions we observe from pass to fail involve a flaky test"
   - **Location:** Line 1132 (`<noscript>`) / Line 1097 (`<script type='text/template'>`)
   - **Word Count:** 15 words ($\le 25$ words)

5. **Retry Mechanisms Inventory:**
   > "the ability to re-run only failing tests, and an option to re-run tests automatically when they fail"
   - **Location:** Line 1136 (`<noscript>`) / Line 1101 (`<script type='text/template'>`)
   - **Word Count:** 17 words ($\le 25$ words)

---

## 4. Evaluation of the Finite Rerun Caveat

In the context of verification fixtures, mutation testing, and test engineering (specifically Capability `C1`, repeated pristine controls):

### 4.1 The Mitigation vs. Resolution Dichotomy
Google's presubmit testing employs three rerun mitigations:
1. Re-running only failing tests.
2. Automatically re-running tests upon initial failure.
3. Denoting tests as flaky so they only report failure if they fail 3 times consecutively.

John Micco explicitly warns that while these mechanisms filter transient noise and reduce developer interruptions, they **do not resolve or cure flakiness**. They are operational accommodations for an unstable test harness.

### 4.2 Key Caveats Documented by S026

1. **Erosion of Test Discipline & Flakiness Habituation:**  
   When developers know a test will not fail presubmit unless it fails three times in a row, they stop investigating intermittent failures. Retries normalize flakiness, allowing root causes (unhandled concurrency, timing dependencies, shared environmental state) to fester.
2. **Multiplied CI Latency:**  
   Rerunning failing tests multiplies execution time. For a 15-minute test, discovering a genuine code breakage takes 45 minutes (3 consecutive runs), dramatically delaying the developer feedback cycle.
3. **Masking Genuine Bugs and Race Conditions:**  
   Quarantining tests or auto-retrying failures until a pass is achieved risks dismissing legitimate race conditions and synchronization bugs in the production system under test as "just flakes."
4. **Statistical Inadequacy (The Determinism Fallacy):**  
   A finite rerun mechanism simply alters the detection probability under repeated independent Bernoulli trials:
   - If a test has a genuine intermittent failure probability $p = 0.20$, the probability of observing 3 consecutive failures is $p^3 = 0.008$ (0.8%). Under an auto-retry or 3-run threshold, the test will pass at least once in 3 attempts $99.2\%$ of the time ($1 - p^3 = 0.992$). The failure is concealed, not fixed.
   - Conversely, for Capability `C1` (`repeat-control.py`), executing $N=3$ identical pristine controls tests for immediate manifest disagreement. If a test has an intermittent failure rate $p = 0.05$, the probability that 3 runs all match identically is $(1-p)^3 + p^3 \approx 0.857 + 0.000125 \approx 85.7\%$. In $85.7\%$ of trials, 3 runs will show no mismatch, despite underlying instability.

### 4.3 Conclusion for Gate Architecture
- Passing $N$ repeated controls (`controls_match`, exit 0) confirms stability within that finite sample window only.
- Reruns must **never** be cited as mathematical or empirical proof of determinism.
- Retries should never be used to mask a mismatch into a match; any disagreement across $N \ge 3$ controls must immediately fail closed (`controls_mismatch`, exit 1).

---

## 5. Concrete Findings with Path:Line References

| File / Artifact | Line Range | Finding / Citation | Context |
|---|---|---|---|
| `S026.html` (served raw) | `1101` / `1136` | `"This reduces false positives, but encourages developers to ignore flakiness in their own tests unless their tests start failing 3 times in a row"` | Finite rerun caveat: developer habituation & erosion of test discipline |
| `S026.html` (served raw) | `1102` / `1137` | `"The breakage will not be discovered until 3 executions of the test complete, or 45 minutes"` | Finite rerun caveat: latency cost on long-running integration suites |
| `S026.html` (served raw) | `1095` / `1130` | `"We define a \"flaky\" test result as a test that exhibits both a passing and a failing result with the same code."` | Normative definition of flaky test result |
| `S026.html` (served raw) | `1095` / `1130` | `"we see a continual rate of about 1.5% of all test runs reporting a \"flaky\" result"` | Measured flakiness prevalence at Google scale |
| `S026.html` (served raw) | `1097` / `1132` | `"about 84% of the transitions we observe from pass to fail involve a flaky test"` | Noise ratio in CI pass-to-fail transitions |
| `S026.html` (served raw) | `1095–1102` | Client template body (`<script type='text/template'>`) | First copy of post body; often skipped by DOM text scrapers |
| `S026.html` (served raw) | `1124–1137` | Fallback body (`<noscript>`) | Second copy of post body; identical text |

---

## 6. Owned Paths & Verification

- **Absolute Written Report Path:**  
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/FlakySources.md`
- **Read-Only Inspected Surfaces:**  
  `https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html` (live HTTP 200)  
  `tameshi-shokunin/corpus/SOURCES.md`  
  `tameshi-shokunin/corpus/QUALITY.md`  
  `tameshi-shokunin/PROVINCE.md`  
  `tameshi-shokunin/AGENTS.md`
- **Unmodified Surfaces:**  
  No production code, no test suites, no gate implementations, and no sibling worktrees were modified.
- **Tooling Record:**  
  Python 3 standard library (`urllib.request`, `hashlib`, `bs4` for initial inspection). No packages or external tools were installed or updated.
