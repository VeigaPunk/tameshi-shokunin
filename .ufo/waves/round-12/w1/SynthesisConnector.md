# SynthesisConnector — Decoupling Baseline Precondition (C1) and Witness Causality (C2)

**Lane / Seat:** UFO-FSD connector (`SynthesisConnector`), Round 12, Wave 1.  
**Role:** Leaf connector advisory. No independent non-author promotion or admission authority; no subagent dispatch; leaves only.  
**Assigned Target:** Connect repeated-control C1 to witness C2 without creating an operational runtime dependency: green baseline attribution precondition vs intended assertion causality. Produce a decision table scoped to observed outcomes within own evidence directory.

---

## 1. Executive Summary & Declared Axes

Under the Godspeed protocol, this connector synthesizes the proposals of Round 12 into **one non-obvious move** that improves measurement fidelity while preserving existing frozen invariants:

1. **Named Axes:**
   - **Calibration ($C_1$):** Measurement fidelity, restraint of promotion assertions, baseline repeatability across $N \ge 3$ control runs (`controls_match` exit 0, `controls_mismatch` exit 1, `baseline_nonzero` exit 2, `command_unavailable` exit 2, `snapshot_tampered` exit 2, `invalid_usage` exit 64). Pinned baseline: 6 points (adjudicated restraint on SHONEN `[~]` boxes).
   - **Depth ($C_2$):** Corpus breadth and defect assertion granularity. Pinned baseline: 6 recorded legs (`tools/mutate-and-run.sh:84-89`). Reanalysis of the pinned bash-surface-census leg (10 defects) deepens assertion resolution without counting as an illegitimate 7th gate.
2. **The Non-Obvious Move:**
   **Decoupled Attribution-Precondition Protocol (DAPP)** via an **Orthogonal Verdict Composition Matrix**.  
   Rather than coupling the two mechanisms at runtime (e.g., forcing `repeat-control.py` inside `mutate-and-run.sh` or having `bash-witness-study.py` execute repeated controls per mutant), C1 and C2 remain operationally decoupled. C1 evaluates whether the unmutated baseline is empirically stable and green (**Attribution Precondition**), while C2 evaluates whether mutant failures match pre-registered witness assertions (**Assertion Causality**). They compose asynchronously at the verdict layer via an immutable $C_1 \times C_2$ Decision Table.
3. **Axis Impact:**
   - **Calibration (Improved):** Directly eliminates the false-positive kill vulnerability proven by `BaselineControl` (Scenario A), where single-control runners award 100% kill-rates to flaky suites. Spurious kills on uncalibrated baselines are demoted to `SPURIOUS_KILL_HAZARD` (`valid_attribution=False`).
   - **Depth (Unharmed):** Retains exact defect counts (10 defects on bash-surface-census) and the frozen 6 recorded legs without runner modification or score inflation.
   - **Contract & Operability (Unharmed):** Zero edits to `tools/mutate-and-run.sh`. Zero runtime overhead during mutation testing loops.

---

## 2. Evidence Base (Round 12 Wave w1 & Local Repo)

The synthesis is grounded strictly in current round evidence and local repo artifacts:

### A. The Single-Control Limitation & Flakiness Vulnerability
- **Runner Reality (`tools/mutate-and-run.sh:465-475`):** The mutation runner executes `run_one "$PRISTINE" "$EVID/control.out" CONTROL` **exactly once**. A single exit 0 permanently marks the sweep `CONTROL: GREEN`.
- **Observed Exploit (`.ufo/evidence/round-12/BaselineControl/`):**
  - In `scenario-a`, a suite that passes run 1 but fails run 2 due to internal state was executed against harmless comment mutant `D1`.
  - The runner reported `CONTROL: GREEN` (run 1 passed), evaluated `D1: KILLED (exit=1)` (run 2 flaked), and reported `MUTATE: DONE ... killed=1 survived=0 kill-rate=100%` (`scenario-a.stdout:8-13`).
  - *Evidence:* A single control run is blind to flakiness occurring during mutant sweeps, converting ambient test flakiness into fraudulent 100% mutation kills.
- **Nondeterministic Stdout (`BaselineControl/scenario-c`):** Suites emitting timestamps, PIDs, or random seeds pass `CONTROL: GREEN` undetected under the existing runner as long as exit code is 0.

### B. Epistemic Limits of Repeated Controls (C1)
- **S011 Verification (`SourceFlakyPaper` / ISSTA 2019):**  
  Shi, Bell, & Marinov demonstrated that repeated executions form only a conservative lower bound: *"some flaky tests may continue to show the same coverage even on our repeated executions, only to appear flaky another day"*. Passing $N \ge 3$ control runs confirms baseline consistency across that sample window; **it does not prove determinism and does not cure flakiness**.
- **Countermodel (`MistakeMining/fourth-run-diverges.sh`):** A deterministic state specimen that passes runs 1–3 as `CONTROL: GREEN` and diverges on run 4 as `CONTROL: FLAKE`. This demonstrates why $N=3$ matching runs cannot be treated as a mathematical proof of determinism.
- **S028 Specification Boundary (`SourceBazel`):**  
  Bazel Test Encyclopedia (§Role of the test runner) mandates that test pass/fail is determined exclusively by process termination status (`exit 0`). Stream outputs (`stdout`/`stderr`) have *"no significance to the test runner"*. Therefore, **exact byte-for-byte output equality across runs is strictly a Tameshi lane calibration policy**, not an external standard requirement.

### C. Witness Attribution Semantics (C2)
- **S006 Grammar (`WitnessSourceReview` / `witness-scoped-kill-verdict.md`):**  
  Derived from `shmutant`: `killed-on-witness` (fails on declared assertion), `accidental` (fails, but not on declared assertion), `survived` (suite passes green), `inconclusive` (timeout/unsettled/lost).
- **Mechanical Reproduction (`ClaimSkeleton` / `witness_recount.py`):**  
  The 10 defects of JS `kimi-census` reproduce mechanically under exact string matching as **8 killed-on-witness, 0 accidental, 2 survived** (D2, D10).
- **Contamination Disclosure (`MistakeMining` / `witness-scoped-kill-verdict.md` E1):**  
  The JS preregistration was partly contaminated by an unscoped grep exposing historical outcomes before hashing. The same risk exists for bash-surface-census (B1–B10) if declarations are copied from `SKILL.md:652-663` rather than pinned gate source at `fecee874`.

---

## 3. The Core Tension: Precondition vs. Causality

A naive integration commits one of two fatal architectural errors:

| Trap | Failure Mechanism | Architectural Violation |
|---|---|---|
| **Operational Coupling** (Embedding C1 inside C2) | Modifying `mutate-and-run.sh` or wrapping `repeat-control.py` inside the mutant loop. | Violates contract: *"no edits to existing mutation runner; existing 6 recorded gate legs unchanged"*. Creates excessive runtime overhead ($3 \times$ multiplier). Causes suites with benign stream jitter (timestamps) to crash the entire mutation study. |
| **Epistemic Conflation** (Ignoring C1 in C2) | Treating C2 witness kills as definitive without checking baseline stability. | Commits **evidence-scope laundering** (`MistakeMining`). Spurious kills from flaky suites (`BaselineControl/scenario-a`) are misattributed as "killed-on-witness", granting false credibility to broken tests. |

### The Synthesis
C1 and C2 belong to distinct, orthogonal phases of the scientific measurement protocol:
- **C1 (Calibration):** Evaluates the **Null State** ($H_0$). Is the baseline unmutated fixture stable, reproducible, and green? (Precondition Gate).
- **C2 (Depth):** Evaluates the **Intervention State** ($\Delta$). When the defect is injected, did the failure occur through the hypothesized causal channel? (Assertion Causality Discriminator).

Because the properties are logically orthogonal, they compose via an **Asynchronous Attestation Interface**:
1. C1 executes against the pristine target once, emitting an immutable **Baseline Attestation Receipt** (`expected.json` / `receipt.json`).
2. C2 executes the mutation sweep and witness classifier once, emitting an immutable **Witness Classification Ledger** (`summary.json` / `results.tsv`).
3. The **Synthesis Decision Table** reads both artifacts and determines the final epistemic validity of the mutation sweep.

---

## 4. The C1 $\times$ C2 Joint Decision Table

The decision table defines the exhaustive mapping between observed C1 baseline states and C2 mutant execution outcomes:

| Row | $C_1$ Baseline Finding | $C_1$ Exit | $C_2$ Mutant Outcome | Joint Epistemic Verdict | Valid Attribution? | Enters Witness Kill Rate? | Enters Aggregate Kill Rate? | Epistemic Rationale & Bounds |
|:---:|---|:---:|---|---|:---:|:---:|:---:|---|
| **1** | `controls_match` | 0 | `killed-on-witness` | **`ATTRIBUTED_KILL`** | **YES** | **YES** | **YES** | Calibrated causal detection: Baseline observed green and byte-identical ($N \ge 3$); mutant failed on pre-registered witness assertion. |
| **2** | `controls_match` | 0 | `accidental` | **`ACCIDENTAL_KILL`** | **YES** | **NO** | **YES** | Calibrated collateral detection: Baseline stable; mutant detected, but by unasserted test collateral. Highlights test specificity gap. |
| **3** | `controls_match` | 0 | `survived` | **`CONFIRMED_SURVIVOR`** | **YES** | **NO** (in denom) | **NO** (in denom) | Calibrated test gap: Baseline stable; suite failed to detect defect. Valid surviving mutant or equivalent code. |
| **4** | `controls_match` | 0 | `inconclusive` | **`BENCHMARK_INCONCLUSIVE`** | NO | NO | NO | Execution anomaly on valid baseline: Timeout, crash, or missing denominator. Excluded from scores per `SKILL.md:208-212`. |
| **5** | `controls_mismatch` | 1 | `killed-on-witness` | **`SPURIOUS_KILL_HAZARD`** | **NO** | **NO** | **NO** | **Attribution Refusal:** Baseline exhibits exit or stream divergence (flakiness). Failure cannot be causally attributed to the mutant. |
| **6** | `controls_mismatch` | 1 | `accidental` | **`SPURIOUS_FAILURE_HAZARD`** | **NO** | **NO** | **NO** | **Attribution Refusal:** Baseline unstable; suite failure cannot be distinguished from ambient test drift. |
| **7** | `controls_mismatch` | 1 | `survived` | **`FRAGILE_SURVIVOR`** | **NO** | **NO** | **NO** | Unreliable survival: Suite passed, but baseline is nondeterministic; survival is conditional on flakiness state. |
| **8** | `controls_mismatch` | 1 | `inconclusive` | **`UNSTABLE_INCONCLUSIVE`** | NO | NO | NO | Compound failure: Baseline unstable and mutant execution aborted. |
| **9** | `baseline_nonzero` | 2 | `*` (Any outcome) | **`COULD_NOT_EVALUATE_BASELINE_DIRTY`** | **NO** | **NO** | **NO** | **Invalid Experiment:** Pristine target exits non-zero. S006 rule holds: *"A red result would prove nothing."* All mutant runs discarded. |
| **10** | `command_unavailable` | 2 | `*` (Any outcome) | **`COULD_NOT_EVALUATE_SETUP_FAULT`** | **NO** | **NO** | **NO** | **Harness Refusal:** Binary missing, execution permissions lacking, or shebang broken at `execve`. |
| **11** | `snapshot_tampered` | 2 | `*` (Any outcome) | **`COULD_NOT_EVALUATE_INTEGRITY_COMPROMISED`** | **NO** | **NO** | **NO** | **Integrity Refusal:** Snapshot input digests diverged or unlisted files detected. Fixture untrusted. |
| **12** | `invalid_usage` | 64 | `*` (Any outcome) | **`COULD_NOT_EVALUATE_USAGE_ERROR`** | **NO** | **NO** | **NO** | **Invocation Refusal:** CLI arguments malformed or run count $N < 3$. |

---

## 5. Empirical Evaluation Scoped to Observed Evidence

The decision table was implemented in `.ufo/evidence/round-12/SynthesisConnector/connector_eval.py` and evaluated against the actual evidence retained in the round cache:

```text
=== Evaluated 16 cases across C1 x C2 Decision Table ===
[BaselineControl_ScenarioA] C1:(controls_mismatch, exit=1) x C2:killed-on-witness => SPURIOUS_KILL_HAZARD (valid=False)
[BaselineControl_ScenarioB] C1:(baseline_nonzero, exit=2) x C2:inconclusive => COULD_NOT_EVALUATE_BASELINE_DIRTY (valid=False)
[BaselineControl_ScenarioC] C1:(controls_mismatch, exit=1) x C2:survived => FRAGILE_SURVIVOR (valid=False)
[BaselineControl_ScenarioD] C1:(baseline_nonzero, exit=2) x C2:survived => COULD_NOT_EVALUATE_BASELINE_DIRTY (valid=False)
[JS_KimiCensus_D1] C1:(controls_match, exit=0) x C2:killed-on-witness => ATTRIBUTED_KILL (valid=True)
[JS_KimiCensus_D2] C1:(controls_match, exit=0) x C2:survived => CONFIRMED_SURVIVOR (valid=True)
[JS_KimiCensus_D3] C1:(controls_match, exit=0) x C2:killed-on-witness => ATTRIBUTED_KILL (valid=True)
[JS_KimiCensus_D4] C1:(controls_match, exit=0) x C2:killed-on-witness => ATTRIBUTED_KILL (valid=True)
[JS_KimiCensus_D5] C1:(controls_match, exit=0) x C2:killed-on-witness => ATTRIBUTED_KILL (valid=True)
[JS_KimiCensus_D6] C1:(controls_match, exit=0) x C2:killed-on-witness => ATTRIBUTED_KILL (valid=True)
[JS_KimiCensus_D7] C1:(controls_match, exit=0) x C2:killed-on-witness => ATTRIBUTED_KILL (valid=True)
[JS_KimiCensus_D8] C1:(controls_match, exit=0) x C2:killed-on-witness => ATTRIBUTED_KILL (valid=True)
[JS_KimiCensus_D9] C1:(controls_match, exit=0) x C2:killed-on-witness => ATTRIBUTED_KILL (valid=True)
[JS_KimiCensus_D10] C1:(controls_match, exit=0) x C2:survived => CONFIRMED_SURVIVOR (valid=True)
[Synthetic_AccidentalKill] C1:(controls_match, exit=0) x C2:accidental => ACCIDENTAL_KILL (valid=True)
[Synthetic_SnapshotTampered] C1:(snapshot_tampered, exit=2) x C2:killed-on-witness => COULD_NOT_EVALUATE_INTEGRITY_COMPROMISED (valid=False)
```

### Key Demonstrations
1. **Flakiness Interception (`BaselineControl_ScenarioA`):**
   - The uncalibrated runner credited `D1` as `KILLED` with 100% kill-rate (`scenario-a.stdout:13`).
   - The DAPP matrix mapped `controls_mismatch` (exit 1) $\times$ `killed-on-witness` $\to$ **`SPURIOUS_KILL_HAZARD`** (`valid_attribution=False`). The fraudulent kill is completely suppressed.
2. **Causal Attribution Fidelity (`JS_KimiCensus` D1–D10):**
   - On the byte-stable JS baseline (`controls_match` exit 0), D1 and D3–D9 are validated as **`ATTRIBUTED_KILL`** ($8/10 = 80\%$), while D2 and D10 are validated as **`CONFIRMED_SURVIVOR`** ($2/10 = 20\%$).
   - Aggregate kill-rate matches witness kill-rate because accidental kills are 0, with every verdict backed by exact line-label anchors (`WitnessSourceReview`).
3. **Refusal Precedence Enforced:**
   - In Scenarios B and D, non-zero baselines immediately force **`COULD_NOT_EVALUATE_BASELINE_DIRTY`**, preventing any uncalibrated scores from entering the record.

---

## 6. Second-Order Effects Across Surfaces

1. **Runtime Surface:**
   - `tools/repeat-control.py` runs $N \ge 3$ times on the target prior to mutation.
   - `tools/mutate-and-run.sh` runs once as a standard sweep.
   - No cross-process pipe nesting; eliminates the pipe-buffer deadlock risk discovered by `BytesReview` ($400\,\text{KB}$ dual-stream hang).
2. **Contract Surface:**
   - Preserves `tools/mutate-and-run.sh:84-89` frozen ledger comment; Depth Score Command D returns `recorded_cases=6 depth_score=6` without alteration.
   - Respects `QUALITY.md` Criterion 10 (external sources require `source:`, `verified-at:`, `recheck:` trios).
   - Preserves `SCORECARD.md` Planned section without fraudulent scalar increments.
3. **Substrate Surface:**
   - Cleanly handles volatile streams: If a tool emits timestamps or PIDs (`BaselineControl/scenario-c`), the suite harness can be calibrated (e.g. wrapper stripping) to satisfy C1 without altering the defect specification or mutant injection logic.
4. **Verification Surface:**
   - Adheres to `verification-patterns-fleet.md` P1 (declared claim before run), P3 (byte identity with volatile exclusion), and P5 (regression fence).
   - Resolves the exit precedence ambiguity identified by `ExitReview` and `MinimalityReview`:
     $$\text{usage (64)} > \text{tamper (2)} > \text{command\_unavailable (2)} > \text{baseline\_nonzero (2)} > \text{controls\_mismatch (1)} > \text{controls\_match (0)}$$

---

## 7. Residual Risks & Invalidation Hazards

1. **Finite Sample Fallacy (Epistemic Bound):**
   - $N=3$ identical runs proves baseline repeatability within that sample; it **does not prove determinism** (S011, `MistakeMining/fourth-run-diverges.sh`). Downstream records must maintain the contract disclaimer: *"no flakiness cured or determinism proven"*.
2. **Volatile Output False-Mismatch:**
   - Because lane policy enforces bitwise stream equality (`SourceBazel` vs `BytesReview`), any test suite that outputs timestamps, elapsed durations, or temp directory paths will trigger `controls_mismatch` (exit 1). Testers must ensure pristine control commands produce clean streams.
3. **Declaration Contamination Hazard:**
   - C2 witness declarations must be cryptographically hashed (`sha256sum`) from pristine source and selftests *before* inspecting mutant execution logs. Post-hoc alignment based on `SKILL.md` tables invalidates causal attribution (`SHONENReview` finding SHN-1).

---

## 8. Owned Paths & Tooling Record

- **Owned Wave Report:**
  `.ufo/waves/round-12/w1/SynthesisConnector.md` (this report)
- **Owned Evidence Directory:**
  `.ufo/evidence/round-12/SynthesisConnector/`
  - `decision_table.json`: Machine-readable specification of the $C_1 \times C_2$ decision table.
  - `connector_eval.py`: Executable probe and decision function.
  - `observed_eval.json`: Complete evaluated output across 16 historical and synthetic cases.
  - `probes.out`: Verbatim execution trace of `connector_eval.py`.
- **Unmodified Production Files:**
  `tools/mutate-and-run.sh`, `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `LOG.md`, and all sibling workspaces remain unmodified.
- **Tooling Record:**
  No tools were installed or updated. Standard system binaries utilized:
  - Python 3.14.7 (`/usr/bin/python3`)
  - GNU coreutils 9.7 (`sha256sum`, `cat`)
  - GNU bash 5.3.15 (`/bin/bash`)
