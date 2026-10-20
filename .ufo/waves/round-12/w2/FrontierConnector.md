# FrontierConnector — Frontier F2/F3 Connection, Scope Analysis, and Statistical Limits

**Seat:** `TameshiR12.FrontierConnector` (Connector, Leaf Member — No Subagent Dispatch)  
**Round:** Tameshi Round 12, Wave w2  
**Status:** Lane-internal advisory finding; no independent non-author authority claimed.  
**Report Target:** Connect F2/F3 planned before-after with actual existing corpus; provide exact scope of held/partial statuses, statistical limitation. Read-only review.  
**Target File:** `.ufo/waves/round-12/w2/FrontierConnector.md`

---

## 1. Executive Summary & Declared Axes (Godspeed Posture)

Under the Godspeed directives (Name the axes; Iterate cheap in parallel; Keep moves that improve any axis and harm none; Don't aim — let the frontier walk itself), this review connects Round 12 claims $C_1$ (calibration repeated-control capability) and $C_2$ (depth bash declared-witness split) to the existing corpus structure, evaluates the exact scope of `held` versus `partly held` statuses in the Frontier table (`corpus/README.md`), and rigorously analyzes the statistical limitations of repeated controls.

### Named Axes
1. **Axis 1: Calibration ($C_1$).** Governed by promotion restraint, honest adherence to the SHONEN rubric (`SHONEN.md`), and strict quality criteria (`corpus/QUALITY.md:3-30`). The calibrated baseline score remains strictly **6** (`SCORECARD.md:216-220`; upper bound 8 minus 2 by manual Box-3 exclusion). $C_1$ introduces a new standalone verification capability (`tools/repeat-control.py`), but does not advance the scalar score ($6 \to 6$) because capability rows do not advance SHONEN boxes, and lane-internal reviews cannot substitute for an independent non-author spot-check (`SCORECARD.md:163-164`; `corpus/lessons/round-1-verifier-spotcheck.md:8-13`).
2. **Axis 2: Depth ($C_2$).** Governed by the count of independently recorded fleet mutation-test legs in `tools/mutate-and-run.sh:84-89` (currently 6). The depth score stays strictly **6** because reanalysis of an existing gate leg (`bash-surface-census`, already recorded at `tools/mutate-and-run.sh:85` as 8/10) is attribution deepening, NOT an independent seventh gate.

---

## 2. Connection of F2/F3 Planned Before-After with Actual Existing Corpus

### 2.1 Frontier Ground F2: Witness-Scoped Kill Verdicts / Bash Mutation Tooling

#### A. Planned State in Existing Corpus
- **`corpus/README.md:79`:**
  - *Ground:* `witness-scoped kill verdicts / bash mutation tooling`
  - *Candidate Sources:* `S006` (`shmutant`)
  - *Committed Status:* `held (round 1) — knowledge/witness-scoped-kill-verdict.md`
  - *Next Falsifiable Move:* `the same split on a bash leg (surface-census): undefined → k_witness + k_accidental = 8`
- **`corpus/README.md:115-118` (Post-Review Adjudication Correction):**
  - Demoted to **`partly held`**:
    > "F2 — partly held. One JS leg measured (8 on-witness / 0 accidental); the witness declaration was partly contaminated (`knowledge/witness-scoped-kill-verdict.md` E1), and no bash leg was measured. A ground reads `held` only when its next move in the table is measured."
- **`SCORECARD.md:271-272` (Inherited Stale Round-2 Plan):**
  - Planned: `witness-scoped split on a bash leg (surface-census) recorded as a ledger case. Before: command D 6 → after 7.`

#### B. Actual Corpus Reality Delivered in Round 12
1. **Measured Leg:** `tools/bash-witness-study.py` (742 lines) was created and executed by `BashWitness` against `kagi-shokunin/corpus/surface-census.sh` @ `fecee874` (blob `275d8294...`, S033).
2. **Observed Split:** Measured outcome reproduced the 8 recorded kills as **8 killed-on-witness, 0 accidental, 2 survived** (`8 + 0 = 8`), with 0 inconclusive runs (`tools/bash-witness-study.py:34-46`).
3. **Cross-Lane Breadth:** Combined with Kumitate `scripts/kimi-census.mjs` (8/0/2 in `corpus/knowledge/witness-scoped-kill-verdict.md:31-45`), witness-scoped attribution has now been executed across **two independent fleet gates** in two distinct languages (JS and Bash), satisfying the `PROVINCE.md:15-16` general-pattern rule.
4. **Resolution of Stale Plan Contradiction:** The planned move in `SCORECARD.md:271-272` ("Before: command D 6 → after 7") was a planning error. `tools/mutate-and-run.sh` remains frozen (`75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`), reanalysis is not a 7th gate, and command D's regex (`SCORECARD.md:72-73`) only counts ledger rows in `tools/mutate-and-run.sh`. As confirmed in `.ufo/evidence/round-12/claims.json:7, 12` and `IntentDataWalk.md:17-20`, depth stays strictly **6**.

---

### 2.2 Frontier Ground F3: Determinism Precondition, Flaky-Aware Verdicts

#### A. Planned State in Existing Corpus
- **`corpus/README.md:80`:**
  - *Ground:* `determinism precondition, flaky-aware verdicts`
  - *Candidate Sources:* `S004, S011, S025, S026, S027, S040`
  - *Committed Status:* `open`
  - *Next Falsifiable Move:* `one control per sweep (.ufo/evidence/kaika-round-1/capability-demo/README.md H2) → N ≥ 3 byte-identical controls, or a named mismatch`
- **`SCORECARD.md:268-270` (Inherited Stale Round-2 Plan):**
  - Planned: `repeated-control determinism gate: one control per sweep (…/capability-demo/README.md H2) → N ≥ 3 byte-identical controls or a named mismatch.`

#### B. Actual Corpus Reality Delivered in Round 12
1. **Implemented Tool:** `tools/repeat-control.py` (790 lines) implements the repeated pristine-control consistency precondition gate.
2. **Contract & Interface:** Invocation `python3 tools/repeat-control.py --runs N --out DIR -- COMMAND ARG...` enforces $N \ge 3$ (`:246-247`), executes exact argv with stdin `/dev/null` (`:268`), and saves raw stdout, stderr, and exit files without whitespace or newline normalization (`:22-24`).
3. **Exit Lattice:** Implements the six-class exit lattice (`:41-48`): `controls_match` (0), `controls_mismatch` (1), `baseline_nonzero` (2), `command_unavailable` (2), `snapshot_tampered` (2), `invalid_usage` (64), `setup_error` (2).
4. **Knowledge Note:** Created `corpus/knowledge/repeated-control-precondition.md`, citing `S004` (clean-tree pass reliability) and `S026` (retry masking risks).
5. **Committed Evidence:** Snapshot observations under `.ufo/evidence/round-12/ControlGate/` and `mismatch/`.

---

## 3. Exact Scope of Held / Partial Statuses

A critical architectural discipline established in post-round reviews (`corpus/README.md:105-121`; `FrontierState.md:62-66`) is that **a ground cannot be marked fully `held` when its title constitutes a conjunction of claims and only a subset has been measured**.

### 3.1 Scope Evaluation for Frontier F2
- **Assigned Status:** **`partly held (round 12)`** (MUST NOT be marked fully `held`).
- **Exact Operational Boundary:**
  1. *Held Component:* Witness-scoped kill attribution on two independent fleet gate legs (`js-kimi-census` 8/0/2 and `bash-surface-census` 8/0/2) with pre-sweep declared mappings and verbatim failing-case label capture (`corpus/knowledge/witness-scoped-kill-verdict.md:31-45`; `tools/bash-witness-study.py:34-46`).
  2. *Unheld Component 1 (Compound Scope):* The ground title names *"witness-scoped kill verdicts / **bash mutation tooling**"*. Round 12 implemented a standalone study script (`tools/bash-witness-study.py`), but did NOT deliver general bash mutation tooling (e.g. automated mutant operators, AST mutators like `shmutant` S006).
  3. *Unheld Component 2 (Harness Non-Integration):* The production mutation runner (`tools/mutate-and-run.sh`) remains frozen and completely unaware of witness attribution. The capability lives in a sidecar script.
  4. *Unheld Component 3 (Adapter Divergence — Erratum E2):* `witness-scoped-kill-verdict.md` erratum E2 (`:67`) establishes that `shmutant` (S006) enforces a single whole-token witness in `FAIL: ` lines. Tameshi's adapter matches full-line selftest labels (`bad-case`) with any-of alternatives.
  5. *Unheld Component 4 (Analyst Heuristics & Contamination):* Witness declarations are analyst-authored string heuristics rather than compiler proofs, created with prior exposure to the test suite and defect identities (`tools/bash-witness-study.py:47-57`; `witness-scoped-kill-verdict.md:54, 60-65`).
  6. *Unheld Component 5 (Zero Accidental Kills Observed):* In both measured legs, $k_{accidental} = 0$. The capability to discriminate accidental kills on a real defect remains empirically unexercised.
  7. *Unheld Component 6 (Denominator Nuance):* The bash selftest defines 16 case slots, but cases 15-16 are `skip-case` when `the-janitor` is absent (`BashDenominator.md:47-52`). The active executed denominator is 14.

### 3.2 Scope Evaluation for Frontier F3
- **Assigned Status:** **`partly held (round 12)`** (Transitions from `open` $\to$ `partly held`; CANNOT be marked fully `held`).
- **Exact Operational Boundary:**
  1. *Held Component:* Pristine control consistency precondition gate (`tools/repeat-control.py`), enforcing $N \ge 3$ raw byte-identical stream comparisons and distinguishing mismatch (exit 1) from unrunnable baseline (exit 2).
  2. *Unheld Component 1 (Compound Scope):* The ground title names *"determinism precondition, **flaky-aware verdicts**"*. Round 12 only evaluates pristine baselines prior to mutation sweeps. Flaky-aware mutant verdicts (e.g. discriminating flaky mutant kills from true kills across repeated defect runs, as modeled by S011) are entirely unaddressed.
  3. *Unheld Component 2 (No Determinism Proven):* As proven below in §4, finite matching runs cannot prove determinism or cure flakiness.
  4. *Unheld Component 3 (Volatile Output Over-Rejection):* Strict unnormalized byte comparison (`tools/repeat-control.py:22-24`) fails healthy suites emitting PIDs, timestamps, or temp paths (`ClaimSkeleton.md:45`). Fleet pattern P3 (`verification-patterns-fleet.md:32-35`) requires a volatile-scrub list, which `repeat-control.py` currently lacks.
  5. *Unheld Component 4 (Runner Non-Integration):* The production runner (`tools/mutate-and-run.sh:465-475`) remains frozen and continues to sample the control exactly once.

---

## 4. Rigorous Analysis of Statistical Limitations ($N \ge 3$ Controls)

The term "determinism gate" in `SCORECARD.md:268` is an epistemic overstatement. A finite sequence of matching control runs establishes sample stability, not mathematical or empirical determinism.

### 4.1 Binomial Flakiness Model
Let a test suite exhibit intermittent failure (flakiness) governed by a Bernoulli distribution with parameter $p \in (0, 1)$, representing the independent probability that an execution under identical inputs diverges or fails:
- Probability of all $N$ runs passing: $P(\text{all pass}) = (1-p)^N$
- Probability of all $N$ runs failing: $P(\text{all fail}) = p^N$
- Probability of observed agreement across $N$ runs:
  $$P(\text{agreement}) = (1-p)^N + p^N$$
- Probability of detecting flakiness (observing at least one passing and at least one failing run):
  $$P(\text{detect}) = 1 - P(\text{agreement}) = 1 - (1-p)^N - p^N$$

### 4.2 Power Calculations for $N = 3$ (Round 12 Floor)

| Flakiness Probability ($p$) | Flakiness Description | $P(\text{detect})$ for $N=3$ | Escape Probability ($P(\text{escape})$) | Epistemic Assessment |
|:---:|:---|:---:|:---:|:---|
| **$0.50$** | Coin-flip intermittent failure | **$75.00\%$** | $25.00\%$ | High detection; 1 in 4 escapes |
| **$0.25$** | Frequent flake (1 in 4 runs) | **$56.25\%$** | $43.75\%$ | Coin-flip detection power |
| **$0.20$** | Moderate flake (1 in 5 runs) | **$48.00\%$** | $52.00\%$ | More likely to escape than be caught |
| **$0.10$** | Typical CI flake (1 in 10 runs) | **$27.10\%$** | **$72.90\%$** | Nearly $3/4$ of flaky suites escape |
| **$0.05$** | Subtle flake (Google S026 regime) | **$14.24\%$** | **$85.76\%$** | Over $85\%$ of flaky suites escape undetected |
| **$0.01$** | Rare flake (1 in 100 runs) | **$2.97\%$** | **$97.03\%$** | Almost completely blind ($>97\%$ escape) |

### 4.3 Second-Order Epistemic Inferences
1. **Gross Instability Filter Only:** $N = 3$ controls reliably filter out only massive, catastrophic nondeterminism ($p \ge 0.50$). For typical industrial flakiness ($p \approx 0.01 - 0.05$, as reported by S026), $N = 3$ has an escape rate exceeding **$85\%$**.
2. **Determinism vs. Agreement:** S026 (`testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html`) and S011 (`ISSTA 2019`) demonstrate that rerun schemes do not remove flakiness; they merely delay detection.
3. **Normative Grounding in Corpus:**
   - `corpus/knowledge/repeated-control-precondition.md:26`: *"Determinism is a property of the program across runs, including runs not taken. `controls_match` records observed stability; no line in either source upgrades it to determinism."*
   - `tools/repeat-control.py:86-87`: *"A clean `controls_match` states that N finite observations agreed on this host in this environment — it is not a determinism proof and it cures no flakiness."*

---

## 5. Contradictions Across Surfaces

Tracing second-order effects reveals four explicit contradictions across the round's artifacts:

### 5.1 Contract Surface: Scorecard Stale Plan vs. Frozen Runner
- **Contradiction:** `SCORECARD.md:271-272` planned: *"witness-scoped split on a bash leg (surface-census) recorded as a ledger case. Before: command D 6 → after 7"*.
- **Reality:** `PROVINCE.md:28-35`, `tools/mutate-and-run.sh:84-89`, and the round-12 contract explicitly freeze the 6 recorded legs. Reanalysis of an existing gate leg is attribution deepening, NOT an independent 7th gate.
- **Resolution:** As affirmed in `IntentDataWalk.md:17-20` and `ClaimSkeleton.md:14, 41-42`, command D remains strictly **6**.

### 5.2 Verification Surface: Pinned Calibration Score (6) vs. Command C (8)
- **Contradiction:** Literal execution of Command C (`SCORECARD.md:75`) gives `asserted_mark_upper_bound=8` at `121696b` and HEAD (`ScoreRubric.md:24-25, 39-55`).
- **Reality:** The pinned score of 6 derives from an explicit manual adjudication excluding Box 3 (`SCORECARD.md:216-220`; `measure.py:30-31`).
- **Resolution:** The scorecard must explicitly document that 6 is an adjudicated score (`Command C − 2 by Box-3 exclusion`), avoiding mechanical inflation.

### 5.3 Runtime Surface: Snapshot Mode Missing `expected.json`
- **Contradiction:** `tools/repeat-control.py:60-62, 73-75` claims frozen snapshots live at `.ufo/evidence/round-12/ControlGate/` and `mismatch/`.
- **Reality:** `ControlSnapshot.md:16-21` and `ControlFlow.md:24-29` discovered that neither directory contains an `expected.json` file. Executing `--snapshot` triggers `TamperError` and exits with code 2 (`snapshot_tampered`), failing selftest cases `:737-743`.
- **Resolution:** Pinned `expected.json` manifests must be authored and committed for `ControlGate/` and `mismatch/`.

### 5.4 Contract Surface: All-Nonzero Baseline vs. Mismatch Precedence
- **Contradiction:** If a baseline command consistently fails with differing exit codes (e.g. `[1, 2, 1]`) or divergent crash stderr, `repeat-control.py:195-202` emits `controls_mismatch` (exit 1).
- **Reality:** Under `service-limits.md` row (b) (`:47`) and `mutate-and-run.sh:63-65`, a baseline that never succeeded is a **setup refusal / could-not-evaluate** (exit 2). Emitting exit 1 conflates an unrunnable test with an unstable green baseline.
- **Resolution:** LimitsConnector's All-Nonzero Baseline Domination Rule (§6 below).

---

## 6. One Non-Obvious Move: Two-Sided Frontier Ledger Anchor (T-SFLA)

To improve round axes without harming existing invariants, we synthesize proposals from `LimitsConnector`, `SynthesisConnector`, `FrontierState`, and `IntentDataWalk` into one compatible move:

### The Move: The "Two-Sided Frontier Ledger Anchor" (T-SFLA)
Rather than treating F2 and F3 as monolithic rows or prematurely attempting runner integration, decompose both F2 and F3 into explicit two-sided ledger anchors within the Frontier documentation:

1. **Frontier F2 Decomposition:**
   - **F2-A (Witness-Scoped Kill Verdicts):** `HELD (Round 12)` — Proven across $\ge 2$ independent gates (`kimi-census` 8/0/2, `surface-census` 8/0/2) per `PROVINCE.md:15-16`.
   - **F2-B (Bash Mutation Tooling & Runner Integration):** `OPEN` — Runner remains frozen; general AST bash tooling unbuilt.
   - **Aggregate Status:** **`partly held (round 12)`**.
2. **Frontier F3 Decomposition:**
   - **F3-A (Pristine Control Repeatability Precondition Gate):** `HELD (Round 12)` — Standalone gate (`tools/repeat-control.py`) enforcing $N \ge 3$ raw byte comparison with 6-class exit lattice.
   - **F3-B (Flaky-Aware Mutant Verdicts & Runner Integration):** `OPEN` — Rerun-based mutant flakiness classification during sweeps (S011) and pre-sweep runner integration unbuilt.
   - **Aggregate Status:** **`partly held (round 12)`**.
3. **Decoupled Attribution Integration:**
   Adopt the **Asynchronous Attestation Interface** (`SynthesisConnector.md:69-73`): $C_1$ emits a Baseline Attestation Receipt (`expected.json`), $C_2$ emits a Witness Classification Ledger (`summary.json`), and the joint decision table evaluates valid attribution without editing `mutate-and-run.sh`.

### Axis Impact
- **Calibration ($C_1$):** **Improved.** Eliminates overclaiming on determinism; establishes mathematically grounded limits for $N \ge 3$; provides clear boundary criteria for partial status.
- **Depth ($C_2$):** **Unharmed.** Depth score strictly preserved at 6; prevents illegitimate 7th leg claims; preserves the frozen runner contract.
- **Contract & Substrate:** **Unharmed.** Zero edits to `tools/mutate-and-run.sh`; sibling repositories remain read-only.

---

## 7. Concrete Metadata Recommendations for L1 Integration

When L1 integrates Round 12 changes, apply the following exact edits:

### 7.1 In `corpus/README.md` `## Frontier` Table (`:79-80`):
```markdown
| F2 | witness-scoped kill verdicts / bash mutation tooling | S006 | partly held (round 12) — `knowledge/witness-scoped-kill-verdict.md`, `tools/bash-witness-study.py` | manual any-of declarations on two gates → compiler/AST-grounded witness derivation OR witness-scoped execution in runner |
| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040 | partly held (round 12) — `knowledge/repeated-control-precondition.md` | pristine control gate verified (N=3) → integrate repeat-control into mutate-and-run.sh pre-sweep OR evaluate flaky mutant classification (S011) |
```

### 7.2 Append to `corpus/README.md` `## Frontier — status correction`:
```markdown
## Frontier — status correction (fleet round 12, appended)

- **F2 — partly held.** Measured on both JS (kimi-census, 8/0/2) and Bash (surface-census, 8/0/2) gates. While the next move on bash is measured, status remains partly held because witness declarations rely on analyst-authored any-of string heuristics, S006 whole-token vs exact-line adapter divergences exist (errata E2/E3), the bash study tool is standalone rather than integrated into the production runner, and no accidental kills have yet been observed in practice.
- **F3 — partly held.** The repeated pristine-control capability (tools/repeat-control.py, N>=3 runs, byte-identical exit/stdout/stderr) and its knowledge note (knowledge/repeated-control-precondition.md) are admitted. Status is partly held rather than held because N=3 identical controls rules out only gross immediate nondeterminism without curing flakiness or proving determinism (P(escape) > 85% for p=0.05), volatile output without normalization over-rejects healthy tests, and flaky-aware verdicts across mutant runs remain unaddressed.
```

### 7.3 In `SCORECARD.md`:
1. **Capabilities Table (`:238-244`):** Add capability row:
   ```markdown
   | repeated pristine-control gate | run command N>=3 times, assert byte-identical exit/stdout/stderr with raw tuple comparison | `python3 tools/repeat-control.py --selftest` → exit 0; `.ufo/evidence/round-12/ControlGate/expected.json` | fleet round 12 |
   ```
2. **Scores:** Keep depth strictly at **6** (`recorded_cases=6 depth_score=6`). Keep calibration strictly at **6** (adjudicated baseline; 8 upper bound minus 2 by manual Box-3 exclusion).
3. **Planned Section (`:261-273`):** Update stale Round-2 entries to reflect Round 13 priorities (freshness re-sweeps of tsukuroi/mado, runner integration of repeat-control, AST-grounded witness derivation).

---

## 8. Risks, Verification Gaps, and Owned Paths

### 8.1 Risks & Gaps
1. **Missing Snapshot Manifests:** The committed directories `.ufo/evidence/round-12/ControlGate/` and `mismatch/` lack `expected.json`. Until authored, `--snapshot` fails with exit 2.
2. **Volatile Scrubbing:** Healthy suites printing timestamps or temp dirs fail `repeat-control.py` with `controls_mismatch` (exit 1). Future rounds must introduce explicit volatile scrubbing (Fleet Pattern P3).
3. **External Spot-Check:** Per `PROTOCOL.md:64-65`, all wave seats are lane-internal. Independent non-author verification remains pending post-landing orchestrator dispatch.

### 8.2 Owned Paths & Tooling Statement
- **Owned Path Written:** `.ufo/waves/round-12/w2/FrontierConnector.md` (this report).
- **Shared Files Modified:** None (read-only seat).
- **Tooling Statement:** No tools were installed, updated, or removed. System Python 3.14.7, GNU bash, coreutils, and git were used exclusively.
- **Authority Statement:** Advisory lane-internal review; no independent non-author authority claimed.
