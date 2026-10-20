# Baseline Control Limitation Analysis (Round 12 — Scout BaselineControl)

## 1. Axes & Posture (Godspeed)

- **Axes:**
  - **Calibration ($C_1$):** Pristine-control repeatability, output/exit stability of baseline before mutation attribution.
  - **Depth ($C_2$):** Ground-truth defect attribution, preventing false-positive kills or uncalibrated suites from distorting kill-rates.
- **Posture:** Iterate cheap, generate direct evidence artifacts without mutating existing production tools or suites, keep moves improving calibration understanding while harming no existing contracts.

---

## 2. Source Line Evidence in Current Mutation Runner (`tools/mutate-and-run.sh`)

Inspection of `tools/mutate-and-run.sh` (version `r10-2 (tameshi-shokunin, 2026-10-14)`, sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`) establishes the following hard single-control constraints:

1. **Header Order-of-Operations Specification (`tools/mutate-and-run.sh:63-65`):**
   ```text
   Order of operations (fail-closed): (1) copy the target to a pinned pristine
   and pin both hashes; (2) parse the spec; (3) build every mutant and assert
   count==1 — any failure exits 2 before a single suite run; (4) control run on
   the pristine — a red control exits 2 (kills could not be attributed); (5)
   mutant runs with output tails; (6) re-check target+pristine sha256; (7)
   kill-rate report.
   ```
   *Finding:* The specification defines exactly one control step before mutant execution.

2. **Single Control Invocation (`tools/mutate-and-run.sh:465-475`):**
   ```bash
   local ctl_rc ctl_ms
   run_one "$PRISTINE" "$EVID/control.out" CONTROL
   ctl_rc=$RC
   ctl_ms=$DUR_MS
   if [[ "$ctl_rc" -ne 0 ]]; then
     printf 'CONTROL: RED (exit=%s duration-ms=%s pristine-sha256=%s)\n' "$ctl_rc" "$ctl_ms" "$PRISTINE_SHA"
     print_tail "$EVID/control.out"
     die_setup "control run on the pristine copy is red (exit=$ctl_rc); cannot attribute kills; log: $EVID/control.out"
   fi
   printf 'CONTROL: GREEN (exit=0 duration-ms=%s pristine-sha256=%s)\n' "$ctl_ms" "$PRISTINE_SHA"
   print_tail "$EVID/control.out"
   ```
   *Finding:*
   - `run_one "$PRISTINE" "$EVID/control.out" CONTROL` is executed **exactly once**.
   - The exit code check `[[ "$ctl_rc" -ne 0 ]]` only evaluates a scalar exit status on that single attempt.
   - Stdout/stderr are dumped to `$EVID/control.out` and the tail printed to stdout; no variance or repeatability check is performed on outputs.
   - A single nonzero exit aborts the entire sweep via `die_setup` (exit 2).

3. **No Repeat / Flake Configuration in CLI Parsing (`tools/mutate-and-run.sh:188-196, 1620-1635`):**
   - Options admitted: `--target`, `--defects`, `--suite`, `--workdir`, `--label`, `--timeout`, `--tail`, `--keep`, `--selftest`, `--regression`.
   - Zero options exist for repeated baseline runs, variance bounds, or flakiness thresholds.

---

## 3. Prior Capability-Demo H2 Evidence Review

In `.ufo/evidence/kaika-round-1/capability-demo/README.md:21,50-78`:
- **Hypothesis H2:** "exactly one control run per sweep, no repeat-control option" was **CONFIRMED**.
- **Measured Artifacts:**
  - `.ufo/evidence/kaika-round-1/capability-demo/h2-sweep.stdout`: 1 `CONTROL: GREEN` line followed immediately by mutant evaluations.
  - `.ufo/evidence/kaika-round-1/capability-demo/h2-sweep.exit`: `exit=0 duration-s=0`.
- **Recorded Assessment (`README.md:75-78`):**
  > "Consequence for F3 (determinism precondition, ART C3 'U'): a sweep gives a single control observation; there is no built-in repeat/flake probe. Whether that suffices for a "determinism precondition" is a rubric judgment, not measured here. [INFERENCE] A flaky suite can therefore be recorded as `CONTROL: GREEN` on one sample; the tool does not itself establish determinism."

---

## 4. Minimal Baseline Scenario Demonstration

A runnable probe script was developed and executed without modifying `tools/mutate-and-run.sh` or any sibling suite:
- **Probe Script:** `.ufo/evidence/round-12/BaselineControl/run_scenario.sh`
- **Target Fixture:** `.ufo/evidence/round-12/BaselineControl/fixtures/target.sh`
- **Spec Fixture:** `.ufo/evidence/round-12/BaselineControl/fixtures/spec.txt` (contains defect `D1` modifying a comment: `@new hello world # noop`, which is semantically identical and should survive).

Four operational scenarios were exercised:

### Scenario A: Flaky Suite (Run 1 Passes, Run 2 Fails) — False-Positive Kill
- **Suite Behavior:** Intermittent flakiness modeled via state counter; run 1 exits 0, run 2 exits 1.
- **Observed Runner Output (`scenario-a.stdout`):**
  ```text
  MUTATE_TARGET: .../target.sh sha256=... bytes=39
  MUTATE_SPEC: .../spec.txt defects=1
  CONTROL: GREEN (exit=0 duration-ms=2 pristine-sha256=...)
    | Suite run #1 for DEFECT_ID=CONTROL
    | Run 1 passes
  DEFECT D1: KILLED (exit=1 duration-ms=2) harmless change that should survive
    | Suite run #2 for DEFECT_ID=D1
    | Run 2 fails due to flakiness
  MUTATE_RESTORE: OK (...)
  MUTATE_EVIDENCE: .../workdir-scenario-a
  MUTATE: DONE (target=target.sh defects=1 killed=1 survived=0 inconclusive=0 kill-rate=100%)
  ```
- **Observed Exit (`scenario-a.exit`):** `0`.
- **Demonstrated Flaw:** The harmless mutant `D1` was recorded as `KILLED` in `results.tsv` and the suite was awarded a **100% kill-rate**. The runner returned exit 0 (success). A single control run is entirely blind to flakiness that manifests during mutant runs, producing spurious kills.

### Scenario B: Flaky Suite (Run 1 Fails, Run 2 Passes) — Premature Abort
- **Suite Behavior:** Run 1 exits 1 (transient flake), run 2 would exit 0.
- **Observed Runner Output (`scenario-b.stdout`):**
  ```text
  CONTROL: RED (exit=1 duration-ms=2 pristine-sha256=...)
    | Suite run #1 for DEFECT_ID=CONTROL
    | Run 1 flaked
  ```
- **Observed Exit (`scenario-b.exit`):** `2`.
- **Demonstrated Flaw:** The runner aborted immediately with `die_setup`. Zero mutants were evaluated, blocking legitimate testing because the single control sample hit the failure state.

### Scenario C: Nondeterministic Stdout (Exit 0 Every Run, Unstable Output)
- **Suite Behavior:** Emits dynamic timestamps, PIDs, and random seeds, but exits 0.
- **Observed Runner Output (`scenario-c.stdout`):**
  ```text
  CONTROL: GREEN (exit=0 duration-ms=2 pristine-sha256=...)
    | Timestamp: 1792462517201018422
    | PID: 26959
    | Random: 24989
  DEFECT D1: SURVIVED (exit=0 duration-ms=2) harmless change that should survive
    | Timestamp: 1792462517205559537
    | PID: 26968
    | Random: 12887
  MUTATE: DONE (target=target.sh defects=1 killed=0 survived=1 inconclusive=0 kill-rate=0%)
  ```
- **Observed Exit (`scenario-c.exit`):** `0`.
- **Demonstrated Flaw:** `mutate-and-run.sh` does not verify byte stability across runs. Dynamic or non-reproducible output passes undetected if exit code is 0.

### Scenario D: Persistent Nonzero Baseline (Always Exit 1)
- **Suite Behavior:** Suite command fails persistently on pristine (exit 1).
- **Observed Runner Output (`scenario-d.stdout`):**
  ```text
  CONTROL: RED (exit=1 duration-ms=1 pristine-sha256=...)
    | Baseline broken: cannot evaluate
  ```
- **Observed Exit (`scenario-d.exit`):** `2`.
- **Demonstrated Flaw:** Exit 2 conflates a broken baseline test with runner configuration errors (missing python, invalid flags, missing files).

---

## 5. Architectural Risks & Calibration Contrast

| Dimension | Existing Runner (`mutate-and-run.sh`) | Calibrated Gate Requirement ($C_1$) |
|---|---|---|
| **Control Run Count** | Exactly 1 sample | $N \ge 3$ consecutive executions |
| **Exit Code Agreement** | Checks single exit code ($RC == 0$) | Requires strict identity across all $N$ runs |
| **Stdout/Stderr Agreement** | Not compared; tail logged once | Exact byte-for-byte identity across all $N$ runs (no normalization) |
| **Flakiness Classification** | Blind; misclassifies flaky failures as mutant kills (100% false kill-rate in Scenario A) | Fails calibration with finding ID `controls_mismatch` (exit 1) |
| **Nonzero Baseline** | Aborts with `die_setup` (exit 2) | Returns finding ID `baseline_nonzero` (exit 2, could-not-evaluate) |
| **Claimed Authority** | Implicitly assumes single control establishes determinism | Explicit non-claim: does not cure flakiness or prove general determinism; only enforces an empirical repeat precondition |

---

## 6. Exact Owned Paths

- **Report:** `.ufo/waves/round-12/w1/BaselineControl.md`
- **Evidence Directory:** `.ufo/evidence/round-12/BaselineControl/`
  - `.ufo/evidence/round-12/BaselineControl/run_scenario.sh` (executable probe runner)
  - `.ufo/evidence/round-12/BaselineControl/fixtures/target.sh`
  - `.ufo/evidence/round-12/BaselineControl/fixtures/spec.txt`
  - `.ufo/evidence/round-12/BaselineControl/fixtures/state_a.txt`
  - `.ufo/evidence/round-12/BaselineControl/fixtures/state_b.txt`
  - `.ufo/evidence/round-12/BaselineControl/scenario-a.{stdout,stderr,exit}`
  - `.ufo/evidence/round-12/BaselineControl/scenario-b.{stdout,stderr,exit}`
  - `.ufo/evidence/round-12/BaselineControl/scenario-c.{stdout,stderr,exit}`
  - `.ufo/evidence/round-12/BaselineControl/scenario-d.{stdout,stderr,exit}`
  - `.ufo/evidence/round-12/BaselineControl/workdir-scenario-a/` (contains `results.tsv` confirming false-positive kill)
  - `.ufo/evidence/round-12/BaselineControl/workdir-scenario-b/`
  - `.ufo/evidence/round-12/BaselineControl/workdir-scenario-c/`
  - `.ufo/evidence/round-12/BaselineControl/workdir-scenario-d/`

---

## 7. Tooling Record

No package installations or updates were performed. Host toolchain was used:
- GNU bash 5.3.15
- Python 3.14.7
- GNU coreutils 9.7
