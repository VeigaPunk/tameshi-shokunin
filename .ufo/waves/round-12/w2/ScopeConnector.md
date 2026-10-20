# ScopeConnector — Round 12 Wave w2: Product Ownership Overlap, Sibling Gate Mutation, and Engine Nondeterminism

**Status:** Advisory, lane-internal connector report. Not an independent non-author promotion, admission, or pass. No fleet or sibling writes, no commits, no runner modifications, and no mid-flight suite runs (`PROTOCOL.md:63-65`, `spec-w2.json:3`).  
**Seat:** `TameshiR12.ScopeConnector` (connector, leaf).  
**Repo:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (working tree HEAD: `18ad5d050ef4bcd830fe513825baed878f025024`).  
**Wave:** `tameshi-r12-w2`.  
**Target:** Bound product ownership overlap with sibling gate mutation and engine nondeterminism. Read province and inherited SiblingOverlap report; name boundary/routing only. Read-only.

---

## 1. Named Axes (Godspeed Directive 1)

In accordance with Godspeed and fleet protocol (`AXES.md:9-16`, `shokunin.conf:55`):
- **calibration ($C_1$):** Truthful accounting of what an empirical check proves versus what remains unproven; strictly separating baseline repeatability ($N \ge 3$ matching pristine controls) from false determinism claims ("no flakiness cured or determinism proven", `repeat-control.py:86-88`); preventing uncalibrated engine crashes from masquerading as verified mutation kills (`verification-patterns-fleet.md:141`); maintaining the adjudicated baseline calibration restraint score at 6 (`measure.py:30-31`, `SCORECARD.md:209-220`).
- **adjacency (Core Province Defense):** Enforcing inviolable fleet boundaries between Tameshi's reusable verification craft and sibling product domains; refusing sibling gate code edits (`PROVINCE.md:16-17`); reporting out-of-province findings (engine flakiness, credential material, live endpoint health, product semantics) without absorbing them (`PROVINCE.md:20,44-48`).
- **depth ($C_2$):** Technical specification precision, complete decision tables, deterministic precedence rules, and concrete execution contracts across the six recorded fleet legs (`mutate-and-run.sh:84-89`) without runner mutation or unearned 7th-leg inflation.
- **operability:** Preserving hermetic, zero-dependency, fail-closed gate execution (`python3` stdlib only, `repeat-control.py:89`), zero runner code diffs, and zero runtime performance overhead.

---

## 2. Ground Evidence & Precedent Anchors

This synthesis grounds exclusively on local repository evidence, inherited wave artifacts, and fleet declarations:

### 2.1 Province & Agent Rules
1. **Product Domain Refusal (`PROVINCE.md:14-18`):**
   *"Refuses: product domains — every lane's gate remains its own; tameshi owns only the reusable craft (a pattern is admitted from evidence in TWO independent lanes before it is claimed general). Never edits a sibling's gate code (read-only probes; recommendations travel in round reports). Credential material (→ kagi), endpoint health (→ kama)."*
2. **Out of Province Refusal (`PROVINCE.md:20`):**
   *"Out of province → report, never absorb."*
3. **Core Governed Surfaces (`PROVINCE.md:28-39`):**
   Core surfaces comprise the reusable method and the six recorded mutation legs as read-only primary surfaces: kumitate `scripts/kimi-census.mjs` and `scripts/claims-check.mjs`, kagi `corpus/surface-census.sh` and `corpus/checklist-run.sh`, tsukuroi `tools/tsukuroi-census.sh`, and mado `tools/mado-verify.sh`.
4. **Adjacent Surfaces Defined (`PROVINCE.md:44-48`):**
   *"Adjacent — report, never absorb: every sibling gate's code and product clauses (owner lane); credential material (kagi); endpoint health (kama); visual/UI snapshot diffing (rejected row S030 — the adjacent UI lanes); engine-specific nondeterminism (game lanes)."*
5. **Read-Only Substrate Rule (`AGENTS.md:3-6`):**
   *"Substrates outside this repo are read-only unless PROVINCE.md declares otherwise. Secrets are shape-only, never content-read."*
6. **Admission & Verification Hygiene (`corpus/QUALITY.md:3-8, 24-26`):**
   Criterion 1–3: falsifiable claims, measured anchors (path:line), observation/inference separation. Criterion 9: scratch stays in `/tmp`; evidence copied into `.ufo/evidence/`.

### 2.2 Sibling Service Limits & Opt-in Protocol
1. **Intake Boundaries (`corpus/knowledge/service-limits.md:44-55`):**
   - **Row (b) (`:47`):** No one-command hermetic suite $\rightarrow$ refused before any suite run: `MUTATE: SETUP (<reason>)`, exit 2, no headline; a red control exits 2 (`SKILL.md:813-817, 840-844`).
   - **Row (c) (`:48`):** Moved substrate $\rightarrow$ re-pin recommendation to owner, never edit or repair sibling gate (`SKILL.md:823-825`).
   - **Row (d) (`:49`):** Live-substrate-coupled gates $\rightarrow$ PATH-level stubs only, live plane out of scope (`service-optin-protocol.md:129-132`).
   - **Row (e) (`:50`):** Secrets-adjacent code $\rightarrow$ credential material (kagi) and endpoint health (kama) reported, never absorbed (`PROVINCE.md:16-18`).
   - **Row (f) (`:51`):** Product semantics (truth) $\rightarrow$ never measured: sensitivity $\ne$ truth; a sweep measures what the suite can detect, never whether verdicts are right (`SKILL.md:879-881`).
2. **Owner-Hardens Discipline (`corpus/knowledge/service-optin-protocol.md:144-181`):**
   - **Rule 1 (`:144-148`):** Recommendations only; acceptance is strictly the owner's decision.
   - **Rule 2 (`:149-154`):** Owner hardens with a ledger in their own tree.
   - **Rule 3 (`:155-161`):** Closure is proven by the owner re-running the spec against the hardened revision.
   - **Rule 4 (`:162-170`):** Hardening closes what it covers; replay names what remains.
   - **Rule 5 (`:171-176`):** No acceptance means recorded unabsorbed.

### 2.3 Fleet Verification Patterns (Engine Nondeterminism Precedents)
1. **Pattern D4 (`corpus/knowledge/verification-patterns-fleet.md:139-142`):**
   *"A detected mutant must survive spoof attempts; engine errors never count as detection... A script/parse error never counts as intended mutant detection `run_battery.py:451-453`."*
2. **Pattern D6 (`corpus/knowledge/verification-patterns-fleet.md:148-152`):**
   *"The verifier writes its OWN instruments and recomputes from spec... Cross-run row comparison via `corpus/live/r68-verifier/compare_verdicts.py`; '0 mismatches in all five comparisons' after an explicit volatile scrub list (pids, elapsed/timing fields, run-dir paths, ASLR addresses, concat interleave order, a 4th-decimal wobble, one provenance_only_line_diff)."*

### 2.4 Runner Contracts & Gate Implementations
1. **Existing Mutation Runner (`tools/mutate-and-run.sh`):**
   - Materialization: `git show <rev>:<path>` into `/tmp`, sibling working tree never touched (`:98-108`).
   - Single Control Run: `run_one "$PRISTINE" "$EVID/control.out" CONTROL`; if `$ctl_rc != 0` $\rightarrow$ `die_setup` exit 2 (`:465-475`).
   - Nonzero Kills: `$mutant_rc -ne 0` $\rightarrow$ `KILLED` (`:486-490`).
   - Unexecutable / Timeout: 124, 126, 127 $\rightarrow$ `INCONCLUSIVE` (`:33, 57-58`).
2. **Repeat-Control Gate Contract (`tools/repeat-control.py`):**
   - Raw Byte Comparison: `stdin /dev/null`, `shell=False`, no decoding, stripping, or newline normalization (`:17-24`).
   - Exit Precedence: unavailable (2) $\rightarrow$ controls_mismatch (1) $\rightarrow$ baseline_nonzero (2) $\rightarrow$ controls_match (0) (`:30-40, 191-205`).
   - Stable IDs: `controls_match` 0, `controls_mismatch` 1, `baseline_nonzero` 2, `command_unavailable` 2, `snapshot_tampered` 2, `setup_error` 2, `invalid_usage` 64 (`:41-48, 115-123`).
   - Epistemic Limitation: *"A clean controls_match states that N finite observations agreed on this host in this environment — it is not a determinism proof and it cures no flakiness"* (`:86-88`).
3. **Inherited W1 Connector Reports:**
   - `SiblingOverlap.md:67-121`: RCBP proposal (In-gate invariance, caller encapsulation, precedence, report routing).
   - `SynthesisConnector.md:17-23, 76-94`: DAPP matrix, asynchronous attestation, decoupling C1 baseline stability from C2 witness causality.
   - `LimitsConnector.md:79-99`: All-Nonzero Baseline Domination Rule ($RC_i \ne 0 \ \forall i \rightarrow$ exit 2 `baseline_nonzero` regardless of stream/exit drift).
   - `ControlFlow.md:9-21`: Static review confirming `classify` logic matches docstring precedence (`[0,1,0]` $\rightarrow$ `controls_mismatch` exit 1).

---

## 3. Structural Overlaps & Contradictions Across Boundaries

When Tameshi interfaces with sibling gates and external substrates, three core boundaries intersect:
1. **Tameshi Core:** Reusable verification fixture craft, raw byte repeat-control, headless mutation engine, strict non-absorption (`PROVINCE.md:3-13, 28-39`).
2. **Sibling Gate Mutation:** Opt-in defect injection sweeps across sibling repos (`kumitate`, `kagi`, `tsukuroi`, `mado`), survivor ledgers, owner-hardens discipline (`service-limits.md:46-55`, `service-optin-protocol.md:144-181`).
3. **Engine Nondeterminism:** Substrates operated by game and engine lanes (`audio-shokunin`, `game-dev-2d-shokunin`, `game-dev-3d-shokunin`, `mado-shokunin`) exhibiting intrinsic jitter (frame timings, audio buffer jitter, ASLR addresses, GPU logs, unhandled engine aborts) (`shokunin.conf:81-83`, `verification-patterns-fleet.md:139-152`).

Tracing their interactions exposes four acute contradictions:

### Contradiction 1: In-Gate Telemetry Normalization vs. Raw Byte Invariance
- *The Trap:* Sibling engine lanes run headless engines (e.g. Godot in `game-dev-2d` or Three.js in `game-dev-3d`) that emit execution durations, ASLR pointer addresses, and temporary run directories on stdout/stderr. Under `repeat-control.py`, raw byte comparison triggers `controls_mismatch` (exit 1). Sibling operators are tempted to ask Tameshi to add regex filters, timestamp stripping, or ASLR redactions directly into `tools/repeat-control.py`.
- *The Violation:* Absorbing engine-specific filters into Tameshi Core directly violates `PROVINCE.md:48` (*"engine-specific nondeterminism (game lanes) — report, never absorb"*). It compromises gate portability and pollutes the reusable craft with domain workarounds.
- *The Resolution:* In-gate byte invariance is absolute (`repeat-control.py:22-24`). All volatile telemetry scrubbing belongs strictly to a **Sibling Ingress Wrapper** before handing argv to Tameshi (Pattern D6).

### Contradiction 2: Sibling Gate Mutation vs. Product Semantics
- *The Trap:* When a mutation sweep in `mutate-and-run.sh` produces surviving mutants (e.g. mado 4/10 or tsukuroi 6/10), or when a pristine baseline fails (`baseline_nonzero`, exit 2), operators might expect Tameshi to modify sibling gate code, diagnose product bugs, or relax test assertions.
- *The Violation:* Violates `PROVINCE.md:14-18` (*"Refuses: product domains — every lane's gate remains its own... Never edits a sibling's gate code"*), `service-limits.md` row (c) (*"the service never edits, repairs or re-pins a gate"*), and row (f) (*"sensitivity $\ne$ truth"*).
- *The Resolution:* Tameshi emits immutable run logs and recommendation ledgers; all remediation belongs exclusively to the owner lane under the **Owner-Hardens Discipline** (`service-optin-protocol.md:144-181`).

### Contradiction 3: The Pattern D4 Collision (Engine Crash Misclassified as Mutant Detection)
- *The Trap:* In `mutate-and-run.sh:486-488`, any non-zero exit from a mutant execution is counted as `KILLED`. In game/engine lanes, an injected mutant may cause an engine crash (SIGSEGV, GPU pipeline abort, parse error). The mutant exits non-zero, and `mutate-and-run.sh` marks it `KILLED`.
- *The Violation:* Violates Pattern D4 (`verification-patterns-fleet.md:139-142`): *"A script/parse error never counts as intended mutant detection"*. An engine crash is an unhandled substrate fault, not a verified assertion detection. Conflating substrate crashes with mutant kills inflates mutation scores with fraudulent kills.
- *The In-Gate Refusal:* Tameshi cannot inspect engine-specific crash logs without violating `PROVINCE.md:48`.
- *The Resolution:* The boundary must be enforced at the **Substrate Exit Boundary**: the sibling test harness must intercept engine crashes and map unhandled crashes/signals to exit 126 or 127. Under `mutate-and-run.sh:33,57-58`, exits 126/127 are classified as `INCONCLUSIVE` (exit 1 `MUTATE: DEGRADED`), preventing accidental engine crashes from entering the kill numerator!

### Contradiction 4: Persistent Broken Baseline vs. Flaky Control Precedence
- *The Trap:* A baseline command persistently fails across all runs with differing nonzero exit codes (e.g. `[1, 2, 1]`) or with dynamic crash dumps in stderr. If `classify` checks exit/stream disagreement before checking baseline viability, it emits `controls_mismatch` (exit 1, failed).
- *The Violation:* An exit of 1 (`controls_mismatch`) asserts that the test suite underwent meaningful evaluation and failed repeatability. But a suite that was never green has zero denominator (`service-limits.md` row b; S006: *"A red result would prove nothing"*). It is strictly a **setup refusal / could-not-evaluate** (exit 2).
- *The Resolution:* Apply the **All-Nonzero Baseline Domination Rule** (`LimitsConnector.md:79-91`): if $\forall i, RC_i \ne 0$, classify as `baseline_nonzero` (exit 2, could-not-evaluate) regardless of exit or stream divergence.

---

## 4. The Proposed Move: Autonomous Dual-Boundary Scope & Routing Architecture (DBSRA)

To improve **calibration ($C_1$)** and **adjacency** without harming **depth ($C_2$)** or **operability**, adopt the **Autonomous Dual-Boundary Scope & Routing Architecture (DBSRA)**. DBSRA establishes an unyielding two-tier contract separating Tameshi Core from Sibling Product Owners and Engine Lanes.

```
+---------------------------------------------------------------------------------------------------+
|                                      SIBLING PRODUCT / ENGINE DOMAIN                              |
|                                                                                                   |
|  [Sibling Engine/Gate] ---> [Sibling Ingress Wrapper]                                            |
|                             - Volatile Scrubbing (PIDs, timestamps, ASLR) [Pattern D6]             |
|                             - Crash Normalization (Engine crashes/parse errors -> exit 126/127)   |
+---------------------------------------------------------------------------------------------------+
                                              |
                                      Exact Argv / Ingress
                                              v
+---------------------------------------------------------------------------------------------------+
|                                         TAMESHI CORE CRAFT                                        |
|                                                                                                   |
|  [repeat-control.py]                                    [mutate-and-run.sh]                       |
|  - Raw Byte Comparison (no in-gate normalization)       - Materialized from git object store       |
|  - Precedence: Unavailable -> Mismatch -> Nonzero       - Inconclusive on 124/126/127 [Pattern D4]|
|  - Finding: controls_match / controls_mismatch / ...    - Kills on clean non-zero test assertion  |
+---------------------------------------------------------------------------------------------------+
                                              |
                                     Egress / Finding ID
                                              v
+---------------------------------------------------------------------------------------------------+
|                                    DBSRA ROUTING & ACTION MATRIX                                  |
|                                                                                                   |
|  Class 1 (Setup Refusal):    baseline_nonzero / command_unavailable (exit 2) -> Sibling Product   |
|  Class 2 (Telemetry Wobble): controls_mismatch on stdout/err only (exit 1)   -> Sibling Adapter   |
|  Class 3 (Test Flakiness):   controls_mismatch on exit codes (exit 1)        -> Sibling Product   |
|  Class 4 (Attributed Kills): controls_match (exit 0) + witness kill          -> Fleet Ledger      |
|  Class 5 (Substrate Crash):  INCONCLUSIVE (exit 1 DEGRADED via 126/127)      -> Engine Domain     |
+---------------------------------------------------------------------------------------------------+
```

### 4.1 Specification Tier 1: Ingress Boundary Specification (Precondition Phase)
1. **Core In-Gate Invariance:** `tools/repeat-control.py` evaluates exact argv with `stdin DEVNULL` and compares saved `stdout`, `stderr`, and `exit` byte-for-byte. It refuses in-gate regex, timestamp stripping, or ASLR masking.
2. **Sibling Ingress Wrapper Obligation:** Sibling callers executing commands with known volatile telemetry (e.g. Godot in `game-dev-2d`, audio buffers in `audio`, dynamic paths in `tsukuroi`) MUST encapsulate the command within a sibling-owned wrapper that scrubs volatile fields before stream output, adhering to Pattern D6 (`verification-patterns-fleet.md:151`).
3. **All-Nonzero Baseline Domination:** If every run in the sample produces a nonzero exit code ($\forall i, RC_i \ne 0$), the run is classified as `baseline_nonzero` (exit 2, `could-not-evaluate`), even if exit codes differ (`[1, 2, 1]`) or error byte streams vary.

### 4.2 Specification Tier 2: Execution Boundary Specification (Mutation Phase)
1. **Git Object Materialization:** Sibling gate mutation in `mutate-and-run.sh` operates exclusively on disposable copies materialized from the git object store (`git show <rev>:<path>`) in `/tmp` (`mutate-and-run.sh:98-108`). Fleet working trees are strictly read-only (`AGENTS.md:3-6`).
2. **Caller-Side Crash Isolation (Pattern D4 Enforcement):** In engine domains, the sibling suite adapter must isolate engine crashes/parse errors from test assertion failures:
   - Test assertion detection $\rightarrow$ exit with standard suite error code (e.g. `1`).
   - Unhandled engine abort, segfault, or parse crash $\rightarrow$ exit with code `126` or `127`.
   - Result: `mutate-and-run.sh:33, 57-58` cleanly marks unhandled engine crashes as `INCONCLUSIVE` (exit 1 `MUTATE: DEGRADED`), preserving Pattern D4 (*"engine errors never count as detection"*) without adding engine parsers to Tameshi Core.

### 4.3 Specification Tier 3: Exhaustive 5-Class Routing & Remediation Matrix

Every finding from `repeat-control.py` and `mutate-and-run.sh` routes according to a deterministic, immutable matrix:

| Finding Class | Observed Signal | Gate Exit | Evaluation Class | Primary Routing Target | Mandatory Action | Prohibited Action (Province Defense) |
|---|---|:---:|---|---|---|---|
| **Class 1: Setup Refusal** | `baseline_nonzero` (`[1,1,1]`, `[1,2,1]`) or `command_unavailable` | 2 | `could-not-evaluate` | **Sibling Product Owner** (`kumitate`, `kagi`, `tsukuroi`, `mado`) | Owner repairs failing baseline tests or execution environment in their own repo. | Tameshi NEVER inspects product internals or edits sibling gate code (`PROVINCE.md:16-17`). |
| **Class 2: Telemetry Wobble** | `controls_mismatch` (all exits 0, but stdout/stderr bytes differ) | 1 | `failed` (ingress jitter) | **Sibling Harness / Ingress Adapter** (or Game Lane) | Adapter owner implements/refines volatile scrub list per Pattern D6 (PIDs, timestamps, ASLR). | Tameshi NEVER adds in-gate normalization or stream filtering to `repeat-control.py` (`PROVINCE.md:48`). |
| **Class 3: Baseline Flakiness** | `controls_mismatch` (exit disagreement, e.g. `[0,1,0]`, `[1,0,0]`) | 1 | `failed` (control instability) | **Sibling Product Owner** | Owner investigates flaky suite logic using numbered artifacts (`run-k.stdout`, `run-k.stderr`). | Tameshi NEVER re-runs until passing, never relaxes gate, and never attributes kills on flaky baselines. |
| **Class 4: Calibrated Baseline** | `controls_match` (all exits 0, byte-identical stdout/stderr) | 0 | `clean` | **Mutation / Verification Sweep** | Proceed with mutation sweep. Output MUST record: *"N finite runs agreed; no flakiness cured or determinism proven"* (`repeat-control.py:86-88`). | Integrator NEVER cites `controls_match` as "proof of determinism" or "flakiness cured" (`SCORECARD.md`). |
| **Class 5: Mutation Findings** | Survivors, uncalibrated kills, or `INCONCLUSIVE` sweeps | 0 / 1 | `sweep-complete` | **Sibling Product Owner** via Owner-Hardens Ledger | Owner reviews ranked recommendation list and authors new selftest cases in own tree (`service-optin-protocol.md:144-181`). | Tameshi NEVER auto-patches sibling gates; unaccepted recommendations remain recorded unabsorbed (`:171-176`). |

---

## 5. Trace of Second-Order Effects Across Surfaces

1. **Runtime Surface:**
   - Zero edits to `tools/repeat-control.py` or `tools/mutate-and-run.sh`.
   - Zero runtime overhead: repeated control runs only during intake/precondition ($N \ge 3$ runs on pristine target), avoiding expensive $3 \times$ multipliers across the entire mutant corpus.
   - Stdlib-only hermeticism maintained: `repeat-control.py` uses only Python 3 stdlib (`:89-93`).
2. **Contract Surface:**
   - Eliminates the contradiction between `repeat-control.py:22-24` and `verification-patterns-fleet.md:151` by explicitly scoping telemetry scrubbing to sibling ingress wrappers.
   - Reconciles `mutate-and-run.sh:486-488` with Pattern D4 (`verification-patterns-fleet.md:139-142`) via caller-side crash exit mapping (126/127 $\rightarrow$ `INCONCLUSIVE`).
   - Solidifies `PROVINCE.md:14-20, 44-48` and `service-limits.md` rows (b), (c), (e), and (f) as enforceable operational boundaries.
3. **Substrate Surface:**
   - Sibling game engines (Godot, Three.js) and system tools (tsukuroi, mado) retain full domain autonomy over internal logging and frame rates; Tameshi dictates only the clean byte interface at the boundary.
   - Sibling working trees remain untouched (`AGENTS.md:3-6`).
4. **Verification Surface:**
   - Calibration restraint score ($C_1$) is defended at 6 (`SCORECARD.md:209-220`, `ScoreRubric.md:41-76`): no overclaiming of determinism, no uncalibrated mutation kills from engine crashes, and all four SHONEN boxes retain restrained `[~]` marks.
   - Depth ($C_2$) is defended at 6 recorded legs (`mutate-and-run.sh:84-89`): reanalysis of bash witness attribution remains a sub-measurement, preventing an illegitimate 7th-leg inflation.

---

## 6. Risks & Boundaries

1. **Risk 1 — Sibling Adapter Evasion:**
   A sibling owner might attempt to bypass the Ingress Wrapper and pass raw, unscrubbed engine commands to `repeat-control.py`, causing immediate `controls_mismatch` (exit 1).
   *Mitigation:* The gate's raw byte comparison is fail-closed. Tameshi provides the exact byte diffs in `--out DIR/run-k.{stdout,stderr}`. The Class 2 routing rule unequivocally sends the finding back to the sibling adapter owner without modifying Tameshi Core.
2. **Risk 2 — Process Hangs and Lack of Built-in Timeouts:**
   `tools/repeat-control.py` contains no internal timeout supervisor (`repeat-control.py:79-82`). A hanging sibling command will block the gate indefinitely.
   *Mitigation:* As documented in `repeat-control.py:82`, callers MUST wrap commands in external timeout tools (e.g. `timeout --kill-after=5s 30s COMMAND...`) at the call site.
3. **Risk 3 — Credential & Endpoint Health Leakage in Saved Evidence:**
   Target commands save unredacted stdout/stderr to `--out DIR/run-k.{stdout,stderr}` (`repeat-control.py:19-25`). If a sibling command prints credentials (`kagi`) or probes live endpoints (`kama`), secrets or live plane data land on disk.
   *Mitigation:* Reaffirm `service-limits.md` row (e) and `AGENTS.md:4-5` (*"Secrets shape-only, never content-read"*). Sibling callers must ensure target commands run hermetically under mock configurations.
4. **Risk 4 — Snapshot Tamper Blindness on Subdirectories:**
   As uncovered by `ControlFlow.md:30-35` (F2), `tools/repeat-control.py:364-370` skips subdirectories during `--snapshot` validation.
   *Mitigation:* Sibling snapshots must remain strictly flat directories containing only `expected.json` and `run-k.{stdout,stderr,exit}`.

---

## 7. Concrete Verification Steps for Integration Owner (L1)

The L1 canonical planner and integration owner can falsify and verify DBSRA through the following concrete checks:

1. **Verify Province Citations & Non-Absorption Invariants:**
   ```bash
   grep -n "Adjacent — report, never absorb" /home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md
   # Expected: line 44 matching with "engine-specific nondeterminism (game lanes)" at line 48
   ```
2. **Verify Refusal of Sibling Gate Code Edits:**
   ```bash
   grep -n "Never edits a sibling's gate code" /home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md
   # Expected: line 16-17 matching
   ```
3. **Verify Zero Sibling Tree Modifications:**
   ```bash
   git status --porcelain
   # Expected: only untracked .ufo/ waves/evidence directories in tameshi-shokunin; zero modified sibling files
   ```
4. **Verify Pattern D4 Precedent (Engine Error Separation):**
   ```bash
   grep -n "engine errors never count as detection" /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/verification-patterns-fleet.md
   # Expected: line 139 matching Pattern D4
   ```
5. **Verify Pattern D6 Precedent (Volatile Scrub List):**
   ```bash
   grep -n "explicit volatile scrub list" /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/verification-patterns-fleet.md
   # Expected: line 151 matching
   ```
6. **Verify Non-Claim Epistemic Limitation in Gate Implementation:**
   ```bash
   grep -n "no flakiness cured or determinism proven" /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/repeat-control.py
   # Expected: line 87 matching verbatim
   ```
7. **Verify Precedence [0,1,0] Yields controls_mismatch (Exit 1):**
   Inspect `classify` in `tools/repeat-control.py:191-205`; record 2 differing tuple triggers `controls_mismatch` before the `baseline_nonzero` check at line 203.

---

## 8. Exact Owned Paths

- **Written by this seat:**
  - `.ufo/waves/round-12/w2/ScopeConnector.md` (this report)
- **Not written / untouched:**
  - `tools/repeat-control.py` (read-only; owned by ControlFinish)
  - `tools/bash-witness-study.py` (read-only; owned by WitnessFinish)
  - `tools/mutate-and-run.sh` (read-only; frozen contract)
  - `corpus/` (read-only; owned by KnowledgeFinish / SourceLedger)
  - Sibling repos (`kumitate`, `kagi`, `tsukuroi`, `mado`, `audio`, `game-dev-2d`, `game-dev-3d`) (strictly read-only)
  - No subagent dispatch (leaf role honoured)
  - No commits made

---

## 9. Tooling Record (Operator Directive 2026-10-19)

In compliance with `/home/vgpnk/.omp/agent/RULES.md`:
- **Tools installed or updated:** None.
- Standard host tools (`python3 3.14.7`, `bash 5.3.15`, GNU coreutils) were sufficient for static inspection, boundary synthesis, and evidence cross-referencing. No package manager or remote script was invoked.
