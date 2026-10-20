# LimitsConnector — Round 12 Wave w1 (Connector)

**Seat:** `LimitsConnector` (connector, leaf). Advisory, lane-internal. Not an independent non-author promotion, admission, or pass.  
**Mandate:** Compare `repeat-control` policy with existing service limits (`corpus/knowledge/service-limits.md`) and mutation-score-semantics timeout/inconclusive treatment (`corpus/knowledge/mutation-score-semantics.md`, `tools/mutate-and-run.sh`). Identify regressions and semantic contradictions. Synthesize one bounded non-obvious move that improves round axes without harming others.

---

## 1. Axes Named

- **Calibration ($C_1$):** Repeatable pristine-control precondition, strict distinction between failure vs. could-not-evaluate, empirical sample stability without overclaiming determinism ($N \ge 3$ matching runs $\ne$ proof of general determinism; flakiness uncured).
- **Depth ($C_2$):** Grounded defect attribution across fleet gates; preventing false-positive kills or uncalibrated test suites from contaminating the 6 recorded legs (`tools/mutate-and-run.sh:84-89`); ensuring witness-split reanalysis remains a sub-measurement rather than an unearned 7th leg.

---

## 2. Ground Evidence Across the Three Surfaces

### Surface A: Existing Mutation Runner (`tools/mutate-and-run.sh`)
1. **Single Control Sample (`tools/mutate-and-run.sh:63-65, 465-475`):**
   - The runner executes `run_one "$PRISTINE" "$EVID/control.out" CONTROL` **exactly once**.
   - If `$ctl_rc == 0`, it logs `CONTROL: GREEN` and proceeds immediately to mutant runs.
   - If `$ctl_rc != 0`, it triggers `die_setup` and exits with code **2** (`MUTATE: SETUP`).
2. **Timeout and Inconclusive Treatment (`tools/mutate-and-run.sh:33, 57-58, 486-490`):**
   - Mutants timing out (exit 124) or unexecutable (126/127) are classified as `INCONCLUSIVE`.
   - The sweep completes with headline `MUTATE: DEGRADED` and exits with code **1** (`done-with-inconclusive`).
   - If the *control* run times out (exit 124), it is caught by `$ctl_rc != 0` and exits with code **2** (`could-not-evaluate`), because kills cannot be attributed.
3. **Flakiness Blindspot Proven by Round 12 Probes (`BaselineControl.md`):**
   - In Scenario A, a suite that flaked on run 2 (run 1 green, run 2 red) passed the runner's single control check and falsely awarded a **100% kill-rate** to a harmless no-op mutant (`D1`).

### Surface B: Service Limits (`corpus/knowledge/service-limits.md`)
1. **Intake Refusal Boundary (§1 row (b)):**
   - Refuses intake when no one-command hermetic suite exists: `MUTATE: SETUP (<reason>)`, exit **2**, no headline; "a red control also exits 2 (kills could not be attributed)".
   - Exit 2 is strictly reserved for *could-not-evaluate / refusal before effect*; it is never an exit 1 test failure.
2. **Volatile Scrubbing vs. Strict Byte Identity (row (d) & `verification-patterns-fleet.md` P3):**
   - Live planes and volatile paths are excluded at intake. Fleet pattern P3 explicitly recognizes that suites emitting timestamps or scratch paths require scrubbing before comparison.

### Surface C: Mutation-Score Semantics (`corpus/knowledge/mutation-score-semantics.md`)
1. **Timeout Exclusion Rule (§2, §3, §4):**
   - Tameshi explicitly rejects Stryker's rule of counting timeouts as detected kills (`k/(k+s)` vs `(k+t)/(k+s+t)`). A timeout is inconclusive; it cannot provide evidence for either numerator ($k$) or denominator ($k+s$).
2. **Baseline as Harness Guard, Not Outcome (S006 / §1):**
   - A non-green baseline is an intake guard refusal (`baseline`), never a mutant outcome or test failure.

### Surface D: New Repeat-Control Policy (`spec.json` & Peer Probes)
1. **Interface Contract:** `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`.
   - `controls_match` $\rightarrow$ exit **0** (clean).
   - `controls_mismatch` $\rightarrow$ exit **1** (failed).
   - `baseline_nonzero` $\rightarrow$ exit **2** (could-not-evaluate).
   - `command_unavailable` $\rightarrow$ exit **2** (could-not-evaluate).
   - `invalid_usage` $\rightarrow$ exit **64** (could-not-evaluate).
   - `snapshot_tampered` $\rightarrow$ exit **2** (could-not-evaluate).
2. **Preservation on Pinned Fleet Legs (`ControlThreats.md` Probe P9):**
   - All 6 recorded fleet legs in `mutate-and-run.sh` pass repeated 3-run control with identical exit 0 and byte-identical stdout/stderr when git file modes (`100755` for `checklist-run.sh`) are preserved.

---

## 3. Comparison, Regressions & Semantic Contradictions

| Dimension | Existing Service Limits & Runner | New `repeat-control` Gate Policy | Semantic Status |
|---|---|---|---|
| **Flakiness on Control** | Blind: single sample admits flakiness $\rightarrow$ false mutant kill (exit 0) | Detected: exit/stream divergence yields `controls_mismatch` (exit 1) | **Strict Upgrade** for Calibration; fixes unchecked service limit |
| **Persistent Nonzero Baseline** | Red control yields `MUTATE: SETUP` (exit 2, could-not-evaluate) | Identical nonzero exits yield `baseline_nonzero` (exit 2, could-not-evaluate) | **Exact Semantic Match** across both tools |
| **Process Hang / Timeout** | Bound by `timeout "$TIMEOUT_S"`; exit 124 handled in-band | No built-in timeout supervisor; relies on caller/command timeout | **Operational Risk** (hanging child blocks gate indefinitely) |
| **Intermittent Timeout** | Mutant timeout = `INCONCLUSIVE` (exit 1 `DEGRADED`, excluded from score) | Control timeout = `controls_mismatch` (exit 1 `failed`) | **Valid Distinction**: Mutant = attribution question; Control = stability precondition |
| **Volatile Streams (PIDs, timestamps)** | P3 pattern notes scrub requirement; runner checks exit code only | Raw byte identity required; no normalization permitted | **Potential Over-Refusal** for unhermetic suites (6 pinned legs safe) |
| **Nonzero Exit Mismatch (`[1, 2, 1]`)** | Both exits are red; baseline fails intake setup (exit 2) | Main IRC precedence ("compare first") triggers `controls_mismatch` (exit 1) | **Semantic Contradiction**: Broken baseline misreported as test failure |

### Contradiction Detail: All-Nonzero Baseline vs. Mismatch Precedence
Under parent IRC guidance ("Precedence: run N controls and compare first. `[0,1,0]` or `[1,0,0]` -> `controls_mismatch` exit 1; `[1,1,1]` identical -> `baseline_nonzero` exit 2"), an unaddressed edge case emerges:
- **Case 1: `[1, 2, 1]`** (runs exit with differing nonzero exit codes).
- **Case 2: `[1, 1, 1]` with divergent stderr** (e.g. failing stack trace containing system timestamps or PIDs).

If "compare first" evaluates stream/exit equality before verifying whether *any* run succeeded:
- The gate emits `controls_mismatch` (exit 1, **failed**).
- **Contradiction:** An exit of 1 asserts that the test suite underwent a meaningful evaluation and failed stability. But in reality, the suite was **never green on any run**. Under `service-limits.md` row (b) and `mutate-and-run.sh:63-64`, a non-green baseline has zero denominator and is strictly a **setup refusal / could-not-evaluate** (exit 2). Reporting exit 1 conflates an unrunnable/broken environment with an unstable green baseline.

---

## 4. One Non-Obvious Move (Compatible Synthesis)

### Proposed Move: "All-Nonzero Baseline Domination Rule"
Synthesize the precedence order in `repeat-control.py` as follows:

$$\text{Precedence:} \quad \text{Usage (64)} \ > \ \text{Command Unavailable (2)} \ > \ \text{Snapshot Tampered (2)} \ > \ \mathbf{All\text{-}Nonzero\ Baseline\ (2)} \ > \ \text{Controls Mismatch (1)} \ > \ \text{Controls Match (0)}$$

Specifically:
1. **If $\forall i \in \{1 \dots N\}, \ RC_i \ne 0$:**
   Classify as `baseline_nonzero` (exit **2**, `could-not-evaluate`), **regardless** of whether exit codes differ across runs (e.g. `[1, 2, 1]`) or error byte streams differ across runs (e.g. dynamic crash traces).
2. **If $\exists i, j$ such that $RC_i = 0$ and $(RC_j \ne 0 \lor \text{stdout}_i \ne \text{stdout}_j \lor \text{stderr}_i \ne \text{stderr}_j)$:**
   Classify as `controls_mismatch` (exit **1**, `failed`). At least one green run demonstrated the baseline *can* pass, proving that the divergence is genuine control flakiness / instability.
3. **If $\forall i, \ RC_i = 0$ and all stdout/stderr byte streams are identical:**
   Classify as `controls_match` (exit **0**, `clean`).

### Second-Order Effects & Cross-Surface Impact:
- **Runtime Surface (`repeat-control.py`):** Prevents crash-trace jitter in broken test suites from escaping as spurious exit 1 failures. Stdlib-only implementation requires simply checking `all(rc != 0 for rc in exits)` before running stream equality checks on failing runs.
- **Contract Surface (`service-limits.md`):** Harmonizes `repeat-control` with row (b) and the fleet exit lattice (`0=clean`, `1=failed`, `2=could-not-evaluate`).
- **Timeout Interaction:** If a command persistently times out under an external wrapper (`[124, 124, 124]`) with slight timing variations in stderr, it cleanly yields `baseline_nonzero` (exit 2, could-not-evaluate). If it times out intermittently (`[0, 124, 0]`), rule 2 triggers `controls_mismatch` (exit 1, failed), properly exposing intermittent hangs.
- **Axes Impact:**
  - **Calibration ($C_1$):** Improved. Eliminates false "failed" classifications on uncalibrated/dead suites; reinforces honest three-valued semantics.
  - **Depth ($C_2$):** Unharmed. Zero changes to the 6 recorded fleet legs or their defect scores; preserves frozen runner contract.

---

## 5. Risks and Boundary Limits

1. **Child Timeout Absence:** Because `repeat-control.py` does not include a process supervisor or `--timeout` argument (by contract), callers MUST wrap commands if execution duration is bounded. If a child hangs indefinitely, `repeat-control.py` hangs indefinitely.
2. **Volatile Scrubbing Limit:** Gates outside the 6 recorded legs that emit unscrubbed volatile output (PIDs, temp paths) will be rejected with `controls_mismatch` (exit 1). This is a known boundary condition of the unnormalized byte contract.
3. **Statistical Power Bound:** As established by `ScorecardReview` and `ClaimSkeleton`, $N=3$ identical runs provides an empirical sample of stability, not mathematical proof of determinism ($P(\text{all pass}) = (1-p)^3$). Wording must remain restrained.

---

## 6. Verification and Integration Checks for L1

When L1 integrates the wave outputs:
1. **Precedence Arm in Selftest:** Ensure `tools/repeat-control.py --selftest` includes an isolated fixture for `[1, 2, 1]` and `[1, 1, 1]`-differing-stderr asserting `baseline_nonzero` (exit 2).
2. **Intermittent Flake Arm:** Ensure selftest verifies `[0, 1, 0]` asserts `controls_mismatch` (exit 1).
3. **Usage Error Code:** Verify bad CLI arguments yield exit 64, not Python's default exit 2 or exit 1.
4. **Frozen Runner Invariant:** Confirm `tools/mutate-and-run.sh` remains bit-identical to HEAD sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`.

---

## 7. Exact Owned Paths

- **Report:** `.ufo/waves/round-12/w1/LimitsConnector.md` (this file).
- **Evidence:** `.ufo/evidence/round-12/LimitsConnector/decision-table.tsv`.
- **Read-Only Inspected Surfaces:** `tools/mutate-and-run.sh`, `corpus/knowledge/service-limits.md`, `corpus/knowledge/mutation-score-semantics.md`, `corpus/QUALITY.md`, `PROVINCE.md`, `SCORECARD.md`, `.ufo/waves/round-12/spec.json`, `.ufo/evidence/round-12/*`.
- **Production Files Modified:** None.

## 8. Tooling Record

No packages or tools were installed or updated during this read-only synthesis pass. Standard host Python 3.14.7 and GNU coreutils were utilized.
