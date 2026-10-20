# SiblingOverlap — Round 12 w1 Assessment & Synthesis

**Status:** Advisory, lane-internal connector report. Not an independent non-author promotion, admission, or pass. No fleet or sibling writes, no commits, and no mid-flight suite verifications.
**Seat:** SiblingOverlap (connector, leaf).
**Repo:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (working tree HEAD: `18ad5d050ef4bcd830fe513825baed878f025024`).
**Wave:** `tameshi-r12-w1`.

---

## 1. Named Axes

In accordance with Godspeed and fleet protocol (`AXES.md:9-16`, `shokunin.conf:55`):
- **calibration** (Primary focus of C1): Truthful accounting of what an empirical check proves versus what remains unproven; eliminating overclaims ("flakiness cured", "determinism proven") when observing $N \ge 3$ pristine runs; accurate classification of unrunnable baselines (`could-not-evaluate`) vs divergent controls (`failed`).
- **adjacency** (Core province defense): Maintaining strict fleet boundaries between tameshi's reusable verification craft and sibling product domains; reporting out-of-province findings (engine flakiness, credential material, live endpoint health, product semantics) without absorbing them (`PROVINCE.md:14-20,44-48`).
- **depth** (Primary focus of C2): Precise technical specification, decision tables, exact precedence rules, and concrete execution contracts without hand-waving.

---

## 2. Grounded Evidence & Sibling Declarations

### 2.1 The Province Mandates (`PROVINCE.md`)
1. **Refusal of Product Domains** (`PROVINCE.md:14-18`):
   - *"Refuses: product domains — every lane's gate remains its own; tameshi owns only the reusable craft (a pattern is admitted from evidence in TWO independent lanes before it is claimed general). Never edits a sibling's gate code (read-only probes; recommendations travel in round reports). Credential material (→ kagi), endpoint health (→ kama)."*
   - *"Out of province → report, never absorb."* (`:20`)
2. **Adjacent Domains Defined** (`PROVINCE.md:44-48`):
   - *"Adjacent — report, never absorb: every sibling gate's code and product clauses (owner lane); credential material (kagi); endpoint health (kama); visual/UI snapshot diffing (rejected row S030 — the adjacent UI lanes); engine-specific nondeterminism (game lanes)."*

### 2.2 Fleet Lane Declarations (`shokunin.conf` & `MANIFEST.json`)
The fleet divides domains cleanly (`shokunin.conf:44-84`):
- **Verification craft:** `tameshi` (`depth + calibration`).
- **Game & Engine lanes:** `audio` (`depth + coverage + calibration`), `game-dev-2d` (`depth + coverage + calibration`, Godot 4.7.2 fixtures), `game-dev-3d` (`depth + coverage + calibration`, Godot/Three.js/Unity/Unreal).
- **Secrets & Infrastructure:** `kagi` (`freshness + calibration`), `kama` (`operability + calibration`, model serving/endpoint health), `tsukuroi` (`operability + freshness`, host repair), `mado` (`coverage + operability`, compositor craft), `tabi` (`coverage + calibration`, browser craft).

### 2.3 Precedent on Engine Nondeterminism & Volatile Telemetry
1. **Engine Errors and Detection** (`corpus/knowledge/verification-patterns-fleet.md:139-142`, Pattern D4):
   - *"A script/parse error never counts as intended mutant detection" `run_battery.py:451-453`*.
   - In game lanes, engine-level anomalies or crashes are separated from intended assertion detections.
2. **Volatile Output Scrubbing** (`corpus/knowledge/verification-patterns-fleet.md:151`, Pattern D6):
   - In `game-dev-2d-shokunin` (Round 68 verifier), cross-run comparisons achieved *"0 mismatches in all five comparisons after an explicit volatile scrub list (pids, elapsed/timing fields, run-dir paths, ASLR addresses, concat interleave order, a 4th-decimal wobble, one provenance_only_line_diff)"*.
   - Game engines inherently emit non-deterministic telemetry (frame timings, audio buffer jitter, ASLR pointer values).

### 2.4 Precedent on Product Truth & Service Limits
1. **Product Semantics Refusal** (`corpus/knowledge/service-limits.md:51,138-142`, Row f):
   - *"Sensitivity, not truth — a sweep measures what the suite can detect, never whether the gate's verdicts are right"*.
   - Tameshi's tools measure execution repeatability and mutant detectability, never product correctness.
2. **Secrets Shape-Only** (`service-limits.md:50,118-120`, Row e; `PROVINCE.md:18`):
   - *"Secrets shape-only, never content-read."* Secret material (tokens, keys) must never be captured or echoed in retained run outputs.

### 2.5 The Round 12 Repeat-Control Gate Contract (`spec.json`)
- Interface: `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`
- Protocol: Run exact argv with `stdin DEVNULL`; save numbered `stdout`, `stderr`, and `exit`; **do not normalize bytes**.
- Stable IDs:
  - `controls_match` (exit 0, clean): all runs agree on exit, stdout, stderr, with baseline exit 0.
  - `controls_mismatch` (exit 1, failed): any output or exit disagreement.
  - `baseline_nonzero` (exit 2, could-not-evaluate): any nonzero baseline exit.
  - `command_unavailable` (exit 2, could-not-evaluate): execution failure / missing binary.
  - `invalid_usage` (exit 64, could-not-evaluate): invalid CLI invocation.
  - `snapshot_tampered` (exit 2, could-not-evaluate): digest mismatch in `--snapshot`.
- Explicit non-claim: *"no flakiness cured or determinism proven"*.

---

## 3. Assessment of Sibling Overlap

### 3.1 Repeat-Control Gate vs. Engine Flakiness (Game Lanes)

There is a fundamental structural tension between Tameshi's raw byte contract and engine-level nondeterminism:
1. **The Over-Rejection Hazard:**
   `repeat-control.py` specifies: *"do not normalize bytes; identical exit/stdout/stderr required"*.
   If an operator or sibling lane runs `repeat-control.py` against an unmodified headless game engine (e.g. Godot in `game-dev-2d` or audio rendering in `audio-shokunin`), the command will almost certainly emit execution durations, audio buffer offsets, temporary scratch paths, or ASLR memory addresses. Under pure byte comparison, this results in `controls_mismatch` (exit 1, failed).
2. **The Absorption Temptation (Boundary Violation 1):**
   A sibling might request that Tameshi add regex filtering, timestamp stripping, or engine-specific tolerances (e.g., Godot frame jitter allowances) into `repeat-control.py`.
   *Province ruling:* **Strictly forbidden.** `PROVINCE.md:48` explicitly defines *"engine-specific nondeterminism (game lanes)"* as `Adjacent — report, never absorb`. Incorporating engine filters into Tameshi's generic CLI control gate contaminates the reusable verification craft with domain-specific substrate workarounds.
3. **The False Determinism Trap (Boundary Violation 2):**
   If a game engine test passes $N=3$ runs of `repeat-control.py`, there is an acute risk of claiming the engine test is "deterministic" or that "flakiness was cured". As noted by `ClaimSkeleton.md:48-53` and paper S011 (`corpus/SOURCES.md:22`), $N=3$ has minimal statistical power against low-frequency flakiness ($p=0.05 \rightarrow \text{detection probability } 0.14$).
   *Calibration ruling:* Tameshi must strictly enforce the contract clause: observing 3 matching runs proves **only** that those 3 runs agreed under identical inputs; it cures nothing and proves no unbounded determinism.

### 3.2 Repeat-Control Gate vs. Product Ownership (Owner Lanes)

1. **Separation of Fixture Repeatability vs. Product Truth:**
   If a sibling lane's gate fails its pristine run with exit 1 (`baseline_nonzero`), whose job is it to diagnose and fix?
   *Province ruling:* **The owning lane.** Tameshi's role terminates upon emitting finding ID `baseline_nonzero` (exit 2, could-not-evaluate). Tameshi does not debug why the product failed, does not inspect product internals, and does not patch sibling code (`PROVINCE.md:16-17`: *"Never edits a sibling's gate code"*).
2. **Separation of Test Suite Flakiness vs. Verification Craft:**
   If a sibling suite produces divergent outputs (`controls_mismatch`, exit 1), Tameshi provides the exact numbered artifacts (`run_1.stdout`, `run_2.stdout`, etc.) and diff locations. Remediation belongs exclusively to the owner lane (e.g. implementing the "owner-hardens discipline" per `service-optin-protocol.md:143-181`).

### 3.3 Synthesis of Exit Precedence (`ExitReview.md` H1) & S006 Semantics

Sibling reviewer `ExitReview.md` identified an unstated precedence between `baseline_nonzero` (exit 2, could-not-evaluate) and `controls_mismatch` (exit 1, failed) for divergent runs containing nonzero exits (such as `[0, 1, 0]`).
- Source S006 (`shmutant`, `SourceWitness/S006.md:39`) establishes: *"baseline: The selected tests were not green before any defect was injected... A red result would prove nothing."*
- However, when a control run exhibits `[0, 1, 0]`, the run is **not merely unrunnable**; it is **actively flaky** during the baseline observation window!
- Treating `[0, 1, 0]` as `baseline_nonzero` (could-not-evaluate) would mask genuine test flakiness under an environmental/setup error code, hiding a critical failure from the sibling owner.
- Conversely, a run where all iterations fail identically (`[1, 1, 1]`) is unambiguously `baseline_nonzero` (could-not-evaluate) because the baseline was never green.

---

## 4. Proposed Move: Reusable Control Boundary Protocol (RCBP)

### 4.1 The Bounded Synthesis
To improve **calibration** and **adjacency** without harming **depth** or **operability**, adopt the **Reusable Control Boundary Protocol (RCBP)** across Tameshi and sibling lanes:

1. **Strict In-Gate Invariance (Tameshi Core):**
   `repeat-control.py` MUST remain byte-exact, raw, and domain-agnostic. It must never implement timestamp scrubbing, regex filtering, or engine-specific tolerances. It evaluates the exact argv passed to it.
2. **Caller-Side Ingress Encapsulation (Sibling Adjacent Responsibility):**
   Any sibling lane running a tool with known volatile telemetry (e.g. Godot headless runs in `game-dev-2d`, audio renders in `audio-shokunin`, or commands printing temp paths) MUST encapsulate volatile fields **within the target command wrapper** (e.g. redirecting volatile logs to a separate file, or piping through a caller-owned scrubber as established in Pattern D6) before handing the command to `repeat-control.py`. If unscrubbed engine telemetry reaches `repeat-control.py`, the gate must fail with `controls_mismatch` (exit 1).
3. **Deterministic Precedence Rule:**
   - **Case A: Consistent Nonzero Baseline** (`[1, 1, 1]`) $\rightarrow$ `baseline_nonzero` (exit 2, could-not-evaluate). Baseline was never clean.
   - **Case B: Intermittent Nonzero or Divergent Output** (`[0, 1, 0]`, or `[0, 0, 0]` with differing stdout/stderr) $\rightarrow$ `controls_mismatch` (exit 1, failed). The pristine control failed to replicate cleanly across runs.
   - **Case C: Unexecutable Command** (`ENOENT`, missing binary) $\rightarrow$ `command_unavailable` (exit 2, could-not-evaluate).
   - **Case D: Consistent Zero Baseline** (`[0, 0, 0]` with byte-identical stdout/stderr) $\rightarrow$ `controls_match` (exit 0, clean).
4. **Standardized Report Routing:**
   Every non-zero exit from `repeat-control.py` produces an artifact bundle in `--out DIR` and routes according to a fixed decision table:

| Gate Finding ID | Exit Code | Evaluation Class | Report Routing Target | Owning Action |
|---|---|---|---|---|
| `controls_match` | 0 | clean | Sibling / Integrator | Proceed with mutation/verification sweep. Record caveat: "no determinism proven". |
| `controls_mismatch` | 1 | failed | Sibling Product Owner (or Game Lane) | Owner investigates flakiness or unscrubbed volatile output. Tameshi refuses to modify gate. |
| `baseline_nonzero` | 2 | could-not-evaluate | Sibling Product Owner | Owner fixes broken baseline test. Tameshi halts evaluation immediately. |
| `command_unavailable` | 2 | could-not-evaluate | Invoking Operator / Harness | Fix execution environment, executable path, or shebang. |
| `snapshot_tampered` | 2 | could-not-evaluate | Security / Integrator | Review tampering or digest drift in committed snapshot. |
| `invalid_usage` | 64 | could-not-evaluate | Invoking Caller | Correct CLI arguments (e.g. $N \ge 3$, valid flags). |

---

## 5. Trace of Second-Order Effects

1. **Runtime Surface:**
   - Exact argv execution with `stdin DEVNULL` avoids shell-level exit code hijacking (e.g. shell 126/127 errors).
   - Caller encapsulation ensures `repeat-control.py` has no dependency on external sed/awk/python filters.
   - Hang risk: because `repeat-control.py` has no per-run timeout specified in the contract, a hanging sibling child will hang the gate. (Remains a known boundary risk to be addressed by timeout flags in future rounds).
2. **Contract Surface:**
   - Clarifying that `[0, 1, 0]` yields `controls_mismatch` (exit 1) rather than `baseline_nonzero` (exit 2) ensures that exit-code-only consumers in CI will treat flaky baselines as failures rather than silent infrastructure skips.
3. **Substrate Surface:**
   - Forbidding in-gate byte normalization forces test suites across the fleet to clean up unwanted stdout pollution (such as printing unredacted mktemp paths or PID numbers), reinforcing fleet-wide test hygiene.
4. **Verification Surface:**
   - Mandating that `controls_match` cannot be cited as "proof of determinism" prevents epistemic inflation across `SCORECARD.md` and round reports.

---

## 6. Risks & Boundaries

1. **Risk of Sibling Resistance:** Sibling lanes with noisy outputs may complain that `repeat-control.py` is "too strict".
   *Mitigation:* Reaffirm `PROVINCE.md:48` and pattern D6. Sibling lanes own their volatile scrubbing; Tameshi provides the unyielding standard of byte-identity.
2. **Risk of Circular Dependency in Snapshot Fixtures:**
   If snapshot fixtures are captured from live runs before the precedence rule is codified, the snapshot circularity noted by `ExitReview.md:50` (H2) will persist.
   *Mitigation:* The precedence rule must be asserted in a dedicated fixture authored to the specification, not recorded from ambient runs.
3. **Risk of Secret Leakage in Stored Outputs:**
   Commands passed to `repeat-control.py` save full stdout/stderr to `--out DIR`. If a sibling command prints credentials, secrets land on disk.
   *Mitigation:* Sibling callers must ensure target commands are hermetic and shape-clean (`service-limits.md` row e).

---

## 7. Verification

Verification steps for L1 integration owner:
1. Verify `PROVINCE.md` citations:
   ```bash
   grep -n "Adjacent — report, never absorb" PROVINCE.md
   # Expected: line 44 matching
   ```
2. Check precedence fixture behavior:
   When `tools/repeat-control.py` is implemented, verify that a fixture producing exits `[0, 1, 0]` emits finding ID `controls_mismatch` and exits with code `1`.
3. Check all-nonzero baseline fixture behavior:
   Verify that a fixture producing exits `[1, 1, 1]` emits finding ID `baseline_nonzero` and exits with code `2`.
4. Verify non-claim statement in documentation:
   Inspect `corpus/knowledge/repeated-control-precondition.md` and verify it contains the explicit clause: *"no flakiness cured or determinism proven"*.

---

## 8. Exact Owned Paths

- **Written by this seat:**
  - `.ufo/waves/round-12/w1/SiblingOverlap.md` (this report)
  - `.ufo/evidence/round-12/SiblingOverlap/overlap-mapping.json` (evidence mapping artifact)
- **Not written / untouched:**
  - `tools/` (no tools edited or created)
  - `corpus/` (no knowledge, lessons, or sources edited)
  - Sibling repos and fleet root files (strictly read-only)
  - No subagent dispatch (leaf role honoured)
  - No commits made

---

## 9. Tooling Record

In compliance with the tooling directive (`/home/vgpnk/.omp/agent/RULES.md`):
- **Tools installed or updated:** None.
- Standard pre-existing host tools (`python3 3.14.7`, `bash 5.3.15`, GNU coreutils) were sufficient for read-only analysis and evidence generation. No package manager invocations were made.
