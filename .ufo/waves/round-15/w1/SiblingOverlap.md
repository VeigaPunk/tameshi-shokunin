# Sibling Overlap & Boundary Mapping — Round 15 Wave 1

**Seat:** `TameshiR15.SiblingOverlap`  
**Role:** UFO-FSD connector  
**Wave:** `tameshi-r15-w1`  
**Target:** Read province plus routed items; map own context gate versus sibling product gates and operator closure checker. Ensure no source ownership absorbed; no sibling gate execution.  
**Report Path:** `.ufo/waves/round-15/w1/SiblingOverlap.md` (relative to lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`)

---

## 1. Named Axes (Godspeed Step 1)

1. **Calibration** (Active focus, lowest tied axis at 6): Resolve outside round-14 Routed defect 5; correct context gate classification from probe to gate; enforce standalone hermetic self-invocation with literal expected exit/finding pairs; make exit 64 explicit. Scalar baseline unchanged (6 → 6).
2. **Adjacency** (Protected invariant): Strictly maintain `PROVINCE.md` boundaries. Sibling product gates remain unabsorbed; sibling gate code is never executed; recommendations travel in round reports, not in absorbed authority.
3. **Operability** (Improved): Clear, runnable public CLI contracts (`--selftest`, `--receipt`, `--root`, `--manifest`) for active tools (`tools/context-capture.py` and `tools/evidence-disposition.py`) without requiring live sibling repos or operator execution rights.
4. **Freshness** (Neutral / unhurt): Observe sibling substrate movement as empirical drift data without executing unauthorized successor sweeps or pretending intake is sweep completion.
5. **Depth** (Neutral / unhurt): Grounded strictly in the six recorded mutation legs (`tools/mutate-and-run.sh:84-89`), with no manufactured seventh leg.
6. **Coverage** (Neutral / unhurt): Preserves the documented primary surfaces across the fleet without claiming whole-frontier completion.
7. **Learning Trends**:
   - *Expansion*: Unchanged (same ground, additive precision).
   - *Quality*: Improved (failure-backed discrimination, explicit supersession, no smoothed scores).
   - *Discernment*: Improved (strict tripartite boundary enforcement between intra-lane verification, sibling product gates, and operator closure checking).

---

## 2. Granular Tripartite Mapping

The table below maps the three surfaces active in the fleet:

| Dimension | 1. Own Context Gate (`tools/context-capture.py`) | 2. Sibling Product Gates (Kumitate, Kagi, Tsukuroi, Mado) | 3. Operator Closure Checker (`closure-check.py`, `root-ledgers.py`) |
|---|---|---|---|
| **Owner Lane** | `tameshi-shokunin` (lane-internal verification craft). | Sibling product lanes: `kumitate-shokunin`, `kagi-shokunin`, `tsukuroi-shokunin`, `mado-shokunin`. | `protocol-shokunin` / `aggregator-shokunin` (fleet operator / closure authority). |
| **Province Mandate** | Verification-fixture craft (`PROVINCE.md:3-12`): reusable method of honest checks, hermetic suites, fail-closed arms, before/after proof. | Product domains (`PROVINCE.md:15-20`): census integrity, boot-chain safety, config-plane syntax. *Tameshi refuses product domains.* | Fleet protocol orchestration (`PROTOCOL.md`): round-robin lifecycle, durability of dispatches, ledger closure. |
| **Target Surface** | Intra-lane execution environment (`GIT_*` isolation, `GIT_DIR` poison positive control), tameshi runner text mappings (`mutate-and-run.sh` 6 legs/constants to manifest), and pinned tool digests. | Sibling repo trees and release artifacts (e.g. `kimi-census.mjs`, `surface-census.sh`, `tsukuroi-census.sh`, `mado-verify.sh`). | Fleet-wide repository root: `MANIFEST.json`, `.ufo/watchdog.log`, `.ufo/reports/round-*/<lane>.md`, `.ufo/state/<lane>.round`, `.ufo/history-pin.json`. |
| **Invariants Checked** | Deterministic JSON comparison under environment perturbation; positive git control effectiveness; source digest stability; text variable-name & constant matching. | Domain-specific checks (e.g. update-safety gates, boot-hook integrity, line-count censuses, checklist rules). | Protocol invariants: report presence, counter progression, dispatch/termination durability, history-pin hash ancestry, frozen baseline integrity. |
| **Sibling Interaction** | Read-only git queries via subprocess `pin-disposition.py` (`git cat-file`, `git rev-parse`). **Never runs sibling gates; never runs `mutate-and-run.sh`.** | Native execution within sibling CI/harnesses. (Tameshi historically evaluated single-edit mutants on `/tmp` scratch copies under opt-in only). | Scans all registered lanes in `MANIFEST.json` and `.ufo/` logs. Does not execute lane gates or selftests (`round-14-verifier-spotcheck.md:8-9`). |
| **Sibling Drift Handling** | Recorded as empirical drift data (`content_status: "changed"`). Crucially: `result_reuse: "not_established"`. **Drift does NOT fail tameshi's gate.** | Sibling lanes own their own drift, remediation, and re-pinning. | Drift in an unclosed lane evaluates to `in-flight` or `failed` per fleet watchdog logs; closed history is append-only. |
| **Hermetic Mode (`--selftest`)** | Standalone public CLI invocation against isolated synthetic fixtures in `/tmp`. **Reads no live sibling paths; touches no network.** | Sibling gates maintain their own `--selftest` under `mktemp -d` (`SKILL.md:58-74`). | `closure-check.py` evaluates `--frozen NAME` baselines under `.ufo/waves/*/frozen`. |
| **Exit Lattice** | `0` clean; `1` mismatch; `2` could-not-evaluate (missing input, poison pre-exists, JSON error); `64` usage error (could-not-evaluate). | Standard 0 ok / 1 fail / 2 error / 64 usage lattice (`gates-survey-kagi.md:75-88`). | `0` clean; `1` debt/contradiction; `2` could-not-evaluate; `3` no-baseline; `64` usage (`root-ledgers.py`). |
| **Output Artifact** | Prospective receipt: `.ufo/evidence/round-15/context-receipt.json` (lane-relative). Round 14 historical receipt preserved byte-identical. | Sibling-local reports and logs; round reports in `.ufo/reports/`. | Fleet `MANIFEST.json` round entries, closure reports, or watchdog status lines. |

---

## 3. Contradictions & Second-Order Effects

1. **Gate Classification vs. Sibling Drift (The False Failure Contradiction)**:
   - *Observation*: Promoting `capture-context.py` to a **gate** (`tools/context-capture.py`) means that its `decide()` returns exit `1` on failure. If `decide()` were naively configured to assert that all six sibling legs match their historical pinned commits/hashes, the gate would permanently fail because 3 of the 6 sibling worktrees (`kumitate`, `tsukuroi`, `mado`) have drifted since round 13 (`context-receipt.json:84-98`).
   - *Contradiction*: Failing tameshi's context gate because a sibling repo changed would implicitly assert ownership over sibling product code—a direct breach of `PROVINCE.md:15-20` ("Refuses: product domains... Adjacent — report, never absorb").
   - *Second-Order Effect*: `tools/pin-disposition.py` already distinguishes observation from verdict: it records `content_status: "changed"` while setting `result_reuse: "not_established"` and emitting exit `0`. The context gate's `decide()` function compares baseline vs. injected runs: because both runs observe the *same* drifted state under identical argv/cwd, their normalized JSON outputs are identical (`comparison.equal == True`). Thus, the context gate checks *environment perturbation invariance* and *tameshi runner text mapping*, NOT sibling repo freezing. Sibling drift must remain data, not an intra-lane failure trigger.

2. **Live Fleet Probing vs. Hermetic Selftest (The Leakage Contradiction)**:
   - *Observation*: In live capture mode, `context-capture.py` invokes `pin-disposition.py --root /home/vgpnk/Projects/shokunin`. If `context-capture.py --selftest` attempted to do the same, it would violate the core definition of a hermetic suite (`SKILL.md:58-74`: "Hermetic suite (`--selftest`): does the tool's own machinery work; fixtures under `mkdtemp` only... no live path read").
   - *Contradiction*: If selftest touches live sibling directories, it will fail in any isolated check environment, or worse, create a hidden execution dependency on sibling substrates.
   - *Second-Order Effect*: `--selftest` must be strictly hermetic, synthesizing miniature mock git repositories and fixture files in a scratch directory under `tempfile.TemporaryDirectory()`. It must verify exit codes (`0`, `1`, `2`, `64`) and stable finding IDs entirely in isolation.

3. **Orchestration Debt vs. Province Creep (The Authority Contradiction)**:
   - *Observation*: Routed defect 2 (`corpus/lessons/round-14-verifier-spotcheck.md:152`) identifies open orchestration conformance debt in the operator lane (`scripts/hyaku/append-closure.py` is a serialized helper rather than a full committed closure-status checker).
   - *Contradiction*: A tameshi agent might attempt to "fix" or execute operator closure checks to prove round compliance.
   - *Second-Order Effect*: Tameshi is a *subject* of closure checks, not their execution authority. Tameshi's context gate must never inspect `MANIFEST.json` rounds, never parse `.ufo/watchdog.log`, and never attempt to evaluate fleet-wide closure. That responsibility belongs strictly to `protocol-shokunin` / non-author closure.

---

## 4. Proposed Move: Tripartite Boundary Pinning & Sealed Hermetic Contract

### The Move
**Structurally seal the three interface boundaries of `tools/context-capture.py` in its code, CLI, and registry contract:**

1. **Upper Boundary (Operator Closure Checker Separation)**:
   - `tools/context-capture.py` is explicitly scoped as an **intra-lane verification gate** for environment isolation and runner-to-manifest mapping.
   - It refuses fleet-level closure responsibilities. It does not read, validate, or write `MANIFEST.json`, `watchdog.log`, or sibling round reports.
   - Unrecognized CLI flags or attempts to pass fleet-level closure targets immediately return `exit 64` (Usage/could-not-evaluate) with no receipt generated.

2. **Lateral Boundary (Sibling Product Gate Protection)**:
   - When inspecting the six recorded mutation legs (`js-kimi-census`, `bash-surface-census`, `bash-tsukuroi-census`, `bash-mado-verify`, `bash-checklist-run`, `js-claims-check`), `tools/context-capture.py` relies exclusively on read-only git plumbing dispatched through `pin-disposition.py`.
   - **Zero Sibling Execution**: Sibling gate scripts (`kimi-census.mjs`, `surface-census.sh`, `tsukuroi-census.sh`, `mado-verify.sh`, `checklist-run.sh`, `claims-check.mjs`) and tameshi's runner (`mutate-and-run.sh`) are **never executed**.
   - **Zero Sibling Ownership Absorption**: Sibling worktree differences are recorded strictly as empirical drift with permanent marker `result_reuse: "not_established"`. `decide()` must never treat sibling worktree drift as a mismatch.

3. **Lower/Hermetic Boundary (Isolated Self-Invocation & Receipt Verification)**:
   - **Hermetic `--selftest`**: Operates entirely within temporary scratch roots, asserting literal exits (`0`, `1`, `2`, `64`) and stable finding IDs (`mismatch_normalized`, `control_ineffective`, `source_pin_mismatch`, `missing_input`, `usage_error`). Zero live repo reads.
   - **Retained-Receipt Checking Mode (`--check-receipt PATH`)**: Allows the gate to verify an existing receipt (e.g. `.ufo/evidence/round-14/context-receipt.json` or round 15 receipt) against pinned schemas and SHA256 digests without re-running child subprocesses.
   - **Historical Immutability**: Historical artifacts (`.ufo/evidence/round-14/capture-context.py` and `context-receipt.json`) remain byte-identical. Prospective capture writes strictly to `.ufo/evidence/round-15/context-receipt.json`.

---

## 5. Affected Axes

- **Calibration (Improved)**: Directly satisfies Routed defect 5. Clarifies the exact predicate boundaries of the context gate, separating deterministic environment isolation from sibling substrate observations.
- **Adjacency (Protected / Strengthened)**: Cements `PROVINCE.md:1-20`. Prevents accidental absorption of sibling product gates or operator closure responsibilities.
- **Operability (Improved)**: Provides a dependable, standalone CLI tool with `--selftest` and `--check-receipt` that can be audited and executed without side-effects or external dependencies.
- **Freshness, Depth, Coverage (Unhurt / Preserved)**: No unauthorized sweeps, no synthetic seventh mutation leg, no altered survey data.

---

## 6. Risks & Mitigations

1. **Risk: Sibling Repo Movement During Live Run**:
   - *Detail*: If a sibling repo worktree is modified between the baseline and injected runs, `baseline_run["stdout"]` and `injected_run["stdout"]` could differ in `content_status` or worktree SHA256, triggering a false-positive `comparison.equal == False` in `decide()`.
   - *Mitigation*: The baseline and injected runs are executed sequentially within milliseconds with identical cwd and arguments (`capture-context.py:539-540`). If transient flakiness is detected, the run classifies as `mismatch` without retrying (fail-closed discipline). Sibling trees remain read-only during the run.
2. **Risk: Confusion of Exit 64 as a Gate Failure**:
   - *Detail*: If an operator or evaluator treats exit 64 as an evaluated gate failure (exit 1), a bad CLI argument could be misinterpreted as a failed environment isolation test.
   - *Mitigation*: The CLI documentation, docstring, and `SKILL.md` registry must explicitly classify exit 64 under the **could-not-evaluate** bucket alongside exit 2, noting that no receipt is written.
3. **Risk: Historical Receipt Clobber**:
   - *Detail*: Running the promoted tool with default arguments might overwrite round 14 evidence.
   - *Mitigation*: Hardcode the default prospective output path to `.ufo/evidence/round-15/context-receipt.json` in `tools/context-capture.py`. Preserving round-14 bytes is an explicit invariant.

---

## 7. Verification Steps (For Main Agent / L1 Integration)

*Per leaf-agent contract, no verification commands were executed by this seat. The L1 canonical planner should execute the following once all seats land:*

1. **Structural Boundary Check**:
   ```sh
   # Verify historical round-14 context files are byte-identical to baseline d6809df
   git diff d6809df7775338f000e44c8a916067b8866867fb HEAD -- .ufo/evidence/round-14/capture-context.py .ufo/evidence/round-14/context-receipt.json
   ```
2. **Standalone Hermetic Selftest**:
   ```sh
   # Verify context gate passes standalone selftest without reading live roots or network
   python3 tools/context-capture.py --selftest
   ```
3. **Exit Lattice & Stable Finding Verification**:
   ```sh
   # Verify exit 64 on invalid arguments
   python3 tools/context-capture.py --invalid-flag; echo "Exit: $?"
   ```
4. **Retained Receipt Check (Read-Only / No Subprocess Re-execution)**:
   ```sh
   # Verify retained receipt verification mode against round-14 baseline
   python3 tools/context-capture.py --check-receipt .ufo/evidence/round-14/context-receipt.json
   ```
5. **No Sibling Mutation or Execution**:
   ```sh
   # Verify sibling repos remain untouched
   git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin status --porcelain
   git -C /home/vgpnk/Projects/shokunin/kagi-shokunin status --porcelain
   git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain
   git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain
   ```
