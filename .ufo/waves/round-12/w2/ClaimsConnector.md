# ClaimsConnector — Causal Separability of C1 (Control Capability) vs C2 (Witness Attribution) and No-Axis-Harm Assessment

**Lane / Seat:** `TameshiR12.ClaimsConnector` (UFO-FSD connector, leaf advisory).  
**Round / Wave:** Round 12, Wave w2.  
**Mandate:** Assess causal separability between C1 control capability (`repeat-control.py`) vs C2 witness attribution (`bash-witness-study.py`) and verify no-axis-harm across calibration and depth. Read `claims.json` and implementation contracts; cite concrete evidence with `path:line`. Stop after one bounded proposal.  
**Authority & Boundary:** Advisory, lane-internal only. Not an independent non-author admission, promotion, or pass. No subagent dispatch. Read-only on production code and runner; write strictly owned report. Zero tools installed or updated (standard host Python 3.14.7, GNU bash 5.3.15, GNU coreutils 9.7).

---

## 1. Declared Axes Named

Under the Godspeed protocol and the canonical round assignment, the two declared axes are:

1. **Calibration ($C_1$):**
   - **Definition:** Rigor and repeatability of measurement, disciplined promotion restraint, and adherence to the three-valued exit lattice (`0=clean`, `1=failed`, `2=could-not-evaluate`).
   - **Baseline & Score Delta:** Pinned at **6** (`claims.json:6`, `SCORECARD.md:67, 216-219`; based on adjudicated restraint on SHONEN boxes with box 3 excluded). **Score delta: 0** (stays 6).
   - **Target Capability:** Standalone repeated-control gate (`tools/repeat-control.py`) running $N \ge 3$ pristine baseline controls to eliminate single-sample flakiness blindspots.

2. **Depth ($C_2$):**
   - **Definition:** Corpus breadth, defect specification coverage, and assertion attribution granularity across fleet gates.
   - **Baseline & Score Delta:** Pinned at **6** recorded legs (`tools/mutate-and-run.sh:84-89`, `SCORECARD.md:66, 72-73`). **Score delta: 0** (stays 6).
   - **Target Measurement:** Evidence deepening on the existing pinned bash-surface-census leg (10 defects B1–B10) via declared witness attribution (`tools/bash-witness-study.py`), separating kills into `killed-on-witness`, `accidental`, and `survived`. Reanalysis is an attribution deepening, **never an unearned 7th gate leg**.

---

## 2. Concrete Evidence & Implementation Contracts (path:line)

The analysis is grounded in the local repository artifacts and round-12 evidence:

### A. The C1 Implementation Contract (`repeat-control.py`)
- **CLI Interface (`tools/repeat-control.py:13-16, 211-248`):**
  - `python3 tools/repeat-control.py --runs N --out DIR -- COMMAND [ARG...]`
  - `python3 tools/repeat-control.py --snapshot DIR`
  - `python3 tools/repeat-control.py --selftest`
- **Execution Model (`tools/repeat-control.py:17-29`):** Executes argv $N \ge 3$ times with `stdin=/dev/null`, `shell=False`, in caller's cwd, inheriting environment. Raw stdout, stderr, and exit codes are persisted as `DIR/run-<k>.{stdout,stderr,exit}`.
- **Strict Byte-Identity Comparison (`tools/repeat-control.py:22-24`):** Streams are compared as raw bytes without decoding, stripping, newline normalization, or whitespace folding.
- **Stable Finding IDs & Exit Lattice (`tools/repeat-control.py:41-48, 115-122`):**
  - `controls_match` $\to$ exit **0** (clean).
  - `controls_mismatch` $\to$ exit **1** (failed).
  - `baseline_nonzero` $\to$ exit **2** (could-not-evaluate).
  - `command_unavailable` $\to$ exit **2** (could-not-evaluate).
  - `snapshot_tampered` $\to$ exit **2** (could-not-evaluate).
  - `setup_error` $\to$ exit **2** (could-not-evaluate).
  - `invalid_usage` $\to$ exit **64** (could-not-evaluate).
- **Snapshot Verification (`tools/repeat-control.py:50-62, 337-434`):** Read-only verification of frozen directory against `expected.json` (schema `repeat-control-snapshot-v1`). No subprocess executed; tamper yields exit 2 `snapshot_tampered`.
- **Precedence Defect (`tools/repeat-control.py:30-40, 191-205`):**
  - Lines 196-202 evaluate stream/exit equality before verifying if any run exited 0.
  - *Observation:* Nonzero runs that differ in exit code (e.g. `[1, 2, 1]`) or emit differing crash stderr (dynamic PIDs/timestamps) trigger `controls_mismatch` (exit 1), misreporting an unrunnable baseline as a test failure rather than `baseline_nonzero` (exit 2).

### B. The C2 Implementation Contract (`bash-witness-study.py`)
- **Target & Revision Pinning (`tools/bash-witness-study.py:78-85, 497-502`):**
  - Materializes `kagi-shokunin/corpus/surface-census.sh` at revision `fecee8743e52eb8fb5fbb40782934cb619a1a96e` (blob sha256 `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`, matching `PIN_BASH` in `tools/mutate-and-run.sh:544`).
- **Frozen Witness Mapping (`tools/bash-witness-study.py:102-160`):**
  - 10 pre-declared defect rows (B1–B10) with witness case labels or `NONE`. Hashed into `declared.tsv` and `declaration.json` before sweep.
- **Runner Invocation (`tools/bash-witness-study.py:522-550`):**
  - Executes `bash tools/mutate-and-run.sh --target ... --defects ... --suite 'bash "$MUTANT" --selftest' --workdir ...`.
  - Scrubs `THE_JANITOR_BIN`, `SQLITE3_BIN`, `CENSUS_BREAK` from environment (`:94, 506-510`).
- **Classification Grammar (`tools/bash-witness-study.py:34-45, 411-430`):**
  - `killed-on-witness`: full denominator (16 declared cases) + red run + $\ge 1$ declared witness case failed.
  - `accidental`: full denominator + red run + zero declared witness cases failed (including all `NONE` rows).
  - `survived`: full denominator + green run + zero failing cases.
  - `inconclusive`: missing `SELFTEST:` line, total $\ne 16$, accounting mismatch, or unexpected skips.

### C. Existing Mutation Runner Baseline Limits (`tools/mutate-and-run.sh`)
- **Single Control Sampling (`tools/mutate-and-run.sh:63-65, 465-475`):**
  - The runner executes `run_one "$PRISTINE" "$EVID/control.out" CONTROL` **exactly once**.
  - If `$ctl_rc == 0`, it emits `CONTROL: GREEN` and proceeds directly to mutant runs.
- **Empirical Flakiness Vulnerability (`.ufo/evidence/round-12/BaselineControl/` & `BaselineControl.md:74-91`):**
  - *Scenario A:* A test suite passing on run 1 and flaking on run 2 was evaluated against harmless comment mutant `D1`. The single-sample runner reported `CONTROL: GREEN`, marked `D1: KILLED (exit=1)`, and awarded a fraudulent **100% kill-rate**.
  - *Scenario C:* A suite emitting dynamic timestamps/PIDs exited 0 and passed `CONTROL: GREEN` undetected.

### D. Scorecard & Claims Specification
- **`claims.json:5-11`:**
  - C1: `repeated pristine-control gate`, score before 6 $\to$ after 6 (delta 0).
  - C2: `measured evidence deepening`, score before 6 $\to$ after 6 (delta 0).
  - Separability: *"C1 fixture CLI is independent of C2 pinned gate experiment; C2 attribution does not depend on new repeat-control tool"*.
- **`SCORECARD.md:66-75, 216-219`:**
  - Depth command D counts header comments in `tools/mutate-and-run.sh:84-89` (value 6).
  - Calibration command C yields 8 at HEAD, pinned at 6 via manual exclusion of SHONEN box 3 (`ClaimSkeleton.md:25-28, 40`, `ScorecardReview.md:73-90`).

---

## 3. Assessment of Causal Separability

Evaluating the claim in `claims.json:10` across second-order runtime, contract, substrate, and verification surfaces reveals an essential dual structure:

### A. Operational Separability (CLI / Runtime Surface): FULLY SEPARABLE
At the mechanical and execution layer, C1 and C2 are strictly independent:
1. `tools/repeat-control.py` is a self-contained CLI utility using standard library only (`tools/repeat-control.py:95-104`). It has no imports, calls, or references to `bash-witness-study.py`, `mutate-and-run.sh`, or `kagi-shokunin`.
2. `tools/bash-witness-study.py` invokes `tools/mutate-and-run.sh` directly (`tools/bash-witness-study.py:80, 525`). It does not invoke, depend on, or require `tools/repeat-control.py`.
3. `tools/mutate-and-run.sh` is frozen (`sha256: 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`). It retains its single control execution (`tools/mutate-and-run.sh:466`).
*Conclusion:* Operational separability is 100% factually true. Neither tool requires the other to execute.

### B. Epistemic Separability (Scientific Causality Surface): CAUSALLY COUPLED
At the scientific measurement layer, C2 witness attribution is fundamentally dependent on C1 baseline stability:
1. **The Causal Attribution Postulate:** A mutant failure can be causally attributed to defect intervention $\Delta$ if and only if the null hypothesis $H_0$ holds: the unmutated baseline does not exhibit spontaneous failure or flakiness under identical execution conditions.
2. **The Flakiness Hazard:** As proven by `BaselineControl` (Scenario A), an uncalibrated single-control runner can mistake an ambient baseline flake for a mutant kill. If the flaking test case coincides with a pre-registered witness, C2 will spuriously classify the defect as `killed-on-witness`.
3. **The S004/S006 Foundations:**
   - S004 (`cargo-mutants`, `repeated-control-precondition.md:12-14`): *"cargo-mutants can’t do anything until you have a tree where cargo test passes reliably..."*
   - S006 (`shmutant`, `witness-scoped-kill-verdict.md:15`): *"baseline: The selected tests were not green before any defect was injected."*
*Conclusion:* Epistemically, C2's attribution validity presupposes C1's baseline repeatability. Ignoring C1 in C2 risks attribution laundering.

### C. The Operational Coupling Hazard (Axis Harm)
Why must we NOT resolve this epistemic coupling by embedding C1 inside C2?
1. **Contract Harm:** Modifying `tools/mutate-and-run.sh` to enforce repeat controls violates the frozen runner contract (`PROVINCE.md:14-17`, `spec-w2.json:3`).
2. **Runtime Overhead:** Forcing $N \ge 3$ repeated controls on every mutant loop creates an unacceptable $3 \times$ multiplier.
3. **Volatile Stream Rejection:** `repeat-control.py` requires bit-exact unnormalized byte streams (`repeat-control.py:22-24`). If forced onto `mutate-and-run.sh` (which generates mktemp evidence paths and timing data) or test suites emitting timestamps, legitimate sweeps would crash with `controls_mismatch` (exit 1), causing severe depth harm.

---

## 4. No-Axis-Harm Verification

| Surface | Calibration Axis ($C_1$) | Depth Axis ($C_2$) | Cross-Surface Status |
|---|---|---|---|
| **Score Invariant** | Pinned 6 $\to$ 6 (delta 0). Retains SHONEN box 3 exclusion discipline. | Pinned 6 $\to$ 6 (delta 0). Leg 2 reanalysis is not a 7th gate. | **Harm None:** Zero scalar score inflation on either axis. |
| **Runner Contract** | Frozen sha `75ed934d...` preserved; zero edits to `mutate-and-run.sh`. | All 6 recorded legs intact (`:84-89`); no new header comment row. | **Harm None:** Strict bit-exact preservation of fleet runner. |
| **Tool Interface** | `repeat-control.py` operates as standalone CLI; handles arbitrary argv. | `bash-witness-study.py` reanalyzes pinned bash leg with 10 defects. | **Harm None:** Orthogonal CLI footprints; zero symbol collisions. |
| **Precedence Lattice** | Fixes `[1, 2, 1]` misclassification; aligns with `service-limits.md`. | No effect on mutant outcome classification. | **Improves Calibration:** Eliminates false exit-1 on dead baselines. |
| **Execution Denominator**| Evaluates exact $N \ge 3$ integer run counts. | Discloses 14 executed vs 16 declared cases (2 skipped without handler). | **Improves Calibration & Depth:** Honest accounting without skip inflation. |

---

## 5. One Non-Obvious Move (Compatible Synthesis)

### Proposed Move: "Asynchronous Baseline-Attestation Receipt Protocol (ABVR)"

Synthesize the round proposals (`SynthesisConnector`'s DAPP matrix, `LimitsConnector`'s all-nonzero domination rule, `ControlThreats`' precedence fix, and `WitnessThreats`' denominator disclosure) into **one cohesive, non-obvious architecture**:

Instead of coupling C1 and C2 synchronously at runtime (which harms depth and violates contracts) or ignoring C1 during C2 evaluation (which harms calibration via flakiness laundering), C1 and C2 compose **asynchronously at the evidence artifact boundary**.

```text
+-----------------------------------------------------------------------------------+
|  PHASE 1: Baseline Attestation (C1 Gate)                                          |
|  $ python3 tools/repeat-control.py --runs 3 --out .ufo/evidence/round-12/...      |
|    -- bash corpus/surface-census.sh --selftest                                    |
|    ==> Emits: run-{1,2,3}.{stdout,stderr,exit}, command.txt, finding.txt          |
|    ==> Authors & validates committed: expected.json (repeat-control-snapshot-v1)  |
|    ==> Status: controls_match (exit 0)                                            |
+-----------------------------------------------------------------------------------+
                                          |
                        [Baseline Attestation Receipt]
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|  PHASE 2: Witness Attribution Sweep (C2 Study)                                    |
|  $ python3 tools/bash-witness-study.py run                                        |
|    ==> Runs pinned mutation sweep under tools/mutate-and-run.sh                    |
|    ==> In manifest.json: records "baseline_control_snapshot": <path_to_c1_receipt> |
|    ==> Classifies 10 defects into killed-on-witness / accidental / survived       |
|    ==> Reports dual denominator: executed=14, declared=16                         |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|  PHASE 3: Asynchronous Two-Evidence Verification (L1 / Auditor)                   |
|  $ python3 tools/repeat-control.py --snapshot <c1_receipt_dir>                    |
|    ==> Proves pristine baseline was independently certified stable & green        |
|    ==> Verifies C2 witness attributions are causally valid (not flakiness)        |
+-----------------------------------------------------------------------------------+
```

### Specific Protocol Components:

1. **Precedence Correction in `repeat-control.py:191-205` (All-Nonzero Domination):**
   ```python
   def classify(records):
       if any(not record["available"] for record in records):
           return "command_unavailable"
       # If ALL runs exited non-zero, it is baseline_nonzero (exit 2, could-not-evaluate),
       # regardless of whether exit codes or crash stderr differed across runs.
       if all(record["exit_text"] != "0" for record in records):
           return "baseline_nonzero"
       # If there is any disagreement in exit code or byte streams:
       first = records[0]
       for record in records[1:]:
           if (record["exit_text"], record["stdout"], record["stderr"]) != (
               first["exit_text"],
               first["stdout"],
               first["stderr"],
           ):
               return "controls_mismatch"
       return "controls_match"
   ```
   *Second-Order Effect:* Resolves the contradiction where an unrunnable baseline `[1, 2, 1]` or dynamic crash trace was misreported as `controls_mismatch` (exit 1). Exit 1 is strictly reserved for suites that demonstrated the capacity to pass ($RC=0$) but diverged.

2. **Asynchronous Attestation Linkage:**
   `bash-witness-study.py` records the SHA-256 digest of C1's committed `expected.json` in `manifest.json`. This proves that the pinned target baseline underwent repeated-control certification without modifying the runner execution loop.

3. **Dual Denominator Reporting:**
   `summary.json` and reports explicitly state: `executed_denominator: 14`, `declared_total: 16`, with `skip_labels: ["verbs-sandboxed", "verbs-break-injection"]`.

---

## 6. Risks and Boundary Limits

1. **No Process Supervisor in C1:** `repeat-control.py` contains no timeout or process tree supervisor (`repeat-control.py:79-82`). If a command hangs indefinitely, the gate hangs. Callers must wrap long-running commands with external `timeout` if bounded execution is required.
2. **Volatile Stream Over-Refusal:** C1's raw unnormalized byte contract rejects suites emitting timestamps, PIDs, or randomized temp paths with `controls_mismatch`. While the pinned bash and JS legs are byte-clean in pristine selftest, unscrubbed external suites cannot be swept directly under C1 without sanitizing wrappers.
3. **Statistical Power Bound ($N=3$):** Passing 3 matching control runs confirms empirical stability within that observation window; it does **not** prove general determinism ($P(\text{pass } 3) = (1-p)^3 \approx 0.73$ at $p=0.10$ flake rate; `ClaimSkeleton.md:46-52`, `ControlThreats.md:46-54`). Wording must remain disciplined: "observed baseline stability", never "proven determinism".
4. **Contamination Disclosure:** As disclosed in `bash-witness-study.py:47-56` and `WitnessThreats.md:26-34`, prior aggregate outcomes were known before witness authoring; the mapping is declared-witness, not a blind preregistration.

---

## 7. Verification and Integration Checks for L1

When Main L1 verifies the integrated changes once after all seats land:

1. **C1 Gate Selftest Verification:**
   Run: `python3 tools/repeat-control.py --selftest`  
   *Expected:* Exit `0`, final line `SELFTEST: PASS (<N> cases)`.
2. **C1 Committed Snapshot Verification:**
   Run: `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate`  
   *Expected:* Exit `0`, `REPEAT_CONTROL: controls_match`.
3. **C1 Tamper Rejection Verification:**
   Run: `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch`  
   *Expected:* Exit `1`, `REPEAT_CONTROL: controls_mismatch`.
4. **C2 Witness Study Verification:**
   Run: `python3 tools/bash-witness-study.py count`  
   *Expected:* Exit `0`, exactly 10 defects classified, executed denominator 14, declared total 16.
5. **Frozen Runner Invariant Check:**
   Run: `sha256sum tools/mutate-and-run.sh`  
   *Expected:* `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`.
6. **Depth Score Command Invariant Check:**
   Run: `python3 -c 'import re; print(len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+", open("tools/mutate-and-run.sh").read(), re.M)))'`  
   *Expected:* Exactly `6`.
7. **Calibration Score Invariant Check:**
   Run: `python3 .ufo/evidence/round-12/measure.py`  
   *Expected:* `calibration_restraint_score: 6`, `unique_recorded_gates: 6`.

---

## 8. Exact Owned Paths

- **Report Written:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/ClaimsConnector.md` (this file).
- **Production / Runner / Sibling Paths Modified:** **None.** (Strictly read-only per leaf mandate).
- **Tooling Changes:** **None.** Standard pre-existing host environment utilized.
