# FrontierState — Audit of Frontier F2/F3, SOURCES Allocations, and 1-Verifier-Spotcheck

**Seat:** `FrontierState`  
**Role:** scout (UFO-FSD leaf member — no subagent dispatch)  
**Wave:** `round-12/w1` (tameshi-shokunin)  
**Status:** lane-internal advisory finding; no independent non-author authority claimed.  
**Assigned Axes:** depth + calibration.  

---

## 1. Executive Summary & Named Axes

Per the Godspeed directives:
- **Axis 1: Depth.** Governed by recorded fleet mutation-test legs in `tools/mutate-and-run.sh:84-89` (currently 6). C2 measures the declared-witness split on the pinned `bash-surface-census` leg (10 defects). Depth score stays strictly **6** because reanalysis of an existing gate leg is not a seventh independent gate.
- **Axis 2: Calibration.** Governed by honest adherence to the SHONEN rubric, quality criteria (`corpus/QUALITY.md`), and restraint against overclaiming. Calibration score stays strictly **6** (adjudicated baseline) because C1 (the repeated pristine-control capability) does not flip any SHONEN box, and lane-internal reviews cannot substitute for an external non-author spot-check.

This audit evaluates the exact metadata changes justified by Round 12 claims C1 (calibration repeated-control capability) and C2 (depth bash declared-witness split), specifically examining:
1. `corpus/README.md` Frontier table rows F2 and F3, and the post-review status correction block (`:105-121`).
2. `corpus/SOURCES.md` ID allocations and mutable field rules under `SOURCES-CONTRACT-v1.md`.
3. The `1-verifier-spotcheck` boundary and the strict bar against claiming lane-internal reviews as independent authority.

No shared production files were modified by this seat. All findings are grounded in observed file evidence.

---

## 2. Audit of `corpus/README.md` Frontier F2/F3 and Status Correction

### 2.1 Current Committed State of F2 and F3

In `corpus/README.md` lines 78–80:
```markdown
| F1 | external mutation-score semantics + report interop | S001, S002, S004, S005 | held (round 1) — `knowledge/mutation-score-semantics.md` | emit one ledger leg as schema JSON and validate it (validator unavailable this round: U) |
| F2 | witness-scoped kill verdicts / bash mutation tooling | S006 | held (round 1) — `knowledge/witness-scoped-kill-verdict.md` | the same split on a bash leg (surface-census): undefined → k_witness + k_accidental = 8 |
| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040 | open | one control per sweep (`.ufo/evidence/kaika-round-1/capability-demo/README.md` H2) → N ≥ 3 byte-identical controls, or a named mismatch |
```

### 2.2 The Existing Post-Review Frontier Correction (`corpus/README.md:105-121`)

Lines 105–121 record an append-only correction resulting from post-round orchestrator review:
```markdown
## Frontier — status correction (fleet round 1, post-review, appended)

The `## Frontier` table above marks F1 and F2 `held (round 1)`;
superseded here (orchestrator adjudication, 2026-10-19) — both are
**partly held**:

- **F1 — partly held.** Score semantics and the six-case recomputation
  are admitted; report interop is not: no ledger leg was emitted as
  schema JSON or validated (`jsonschema` unavailable), and NoCoverage
  candidates stay U.
- **F2 — partly held.** One JS leg measured (8 on-witness / 0
  accidental); the witness declaration was partly contaminated
  (`knowledge/witness-scoped-kill-verdict.md` E1), and no bash leg was
  measured.

A ground reads `held` only when its next move in the table is
measured.
```

### 2.3 Evaluation of the Existing Correction

The adjudication established three critical structural principles:
1. **Partial demotion on incomplete scope:** An entry cannot be marked fully `held` when its operational title or scope contains multiple conjunctive claims and only a subset is verified. F1 paired "score semantics" (admitted) with "report interop" (unvalidated). F2 paired "witness-scoped kill verdicts" (JS measured) with "bash mutation tooling" (unmeasured).
2. **Contamination caveat:** In F2, an unscoped grep exposed historical outcomes before the declaration hash was written (`knowledge/witness-scoped-kill-verdict.md` E1). The result was admitted as "declared-witness, partly contaminated," not a clean blind pre-registration.
3. **Normative transition rule:** "A ground reads `held` only when its next move in the table is measured" (`corpus/README.md:120-121`).

---

## 3. Impact of Round 12 Claims C1 & C2 on Frontier Grounds

### 3.1 Claim C1 vs Frontier Ground F3

- **F3 Ground:** `determinism precondition, flaky-aware verdicts`
- **Candidate Sources:** `S004, S011, S025, S026, S027, S040`
- **Previous Status:** `open`
- **Previous Next Move:** `one control per sweep (.ufo/evidence/kaika-round-1/capability-demo/README.md H2) → N ≥ 3 byte-identical controls, or a named mismatch`

#### What C1 Delivers:
Round 12 Claim C1 implements `tools/repeat-control.py`:
- Contract: `--runs 3 --out DIR -- COMMAND ARG...`, stdin `DEVNULL`, exact argv execution, raw byte comparisons (no whitespace or newline normalization).
- Exit mapping: `controls_match` (0), `controls_mismatch` (1), `baseline_nonzero` (2), `command_unavailable` (2), `invalid_usage` (64), snapshot tamper (2).
- Supported by knowledge file `corpus/knowledge/repeated-control-precondition.md` citing `S004` (reliable copied-tree baselines) and `S026` (rerun masking caution).

#### Justified F3 Metadata Status: `partly held (round 12)`
F3 **CANNOT** be marked fully `held`. It is justified only as **`partly held`**.
**Evidence & Restraints:**
1. **Flaky-aware mutant verdicts unaddressed:** F3's ground explicitly names "determinism precondition, **flaky-aware verdicts**". C1 only evaluates pristine baseline controls before mutant injection. It does not measure or classify flaky behavior during mutant sweeps (such as distinguishing unviable/flaky mutant kills from deterministic kills as modeled by S011).
2. **No determinism proven:** As proven in `ClaimSkeleton.md` (M2) and literature (S011, S040), $N=3$ identical runs only proves the absence of an immediate observed mismatch in 3 draws. For a test with flake probability $p=0.05$, the probability of 3 identical runs is $(1-p)^3 + p^3 \approx 0.857$ (86% chance of escaping undetected). The gate contract explicitly states: *"no flakiness cured or determinism proven."*
3. **Rerun masking threat:** S026 explicitly warns that repeated-run filtering can mask real nondeterminism and teach operators to ignore flakiness.
4. **Standalone capability:** The gate is a standalone tool (`tools/repeat-control.py`), not yet integrated into the production mutation runner (`tools/mutate-and-run.sh`, which remains frozen).

#### Formulated Next Falsifiable Move for F3:
> `pristine control gate verified (N=3) → integrate repeat-control into mutate-and-run.sh pre-sweep OR evaluate flaky mutant classification (S011) across repeated defect sweeps`

---

### 3.2 Claim C2 vs Frontier Ground F2

- **F2 Ground:** `witness-scoped kill verdicts / bash mutation tooling`
- **Candidate Sources:** `S006`
- **Previous Status:** `partly held` (per post-review correction)
- **Previous Next Move:** `the same split on a bash leg (surface-census): undefined → k_witness + k_accidental = 8`

#### What C2 Delivers:
Round 12 Claim C2 executes the declared-witness study on the pinned `bash-surface-census` leg (kagi `corpus/surface-census.sh`, 10 defects):
- Tool: `tools/bash-witness-study.py` (owned by `BashWitness`).
- Measured result: witness-attributed split on the 8 recorded kills (`k_witness + k_accidental = 8`), reproducing the recorded 8 kills without modifying the 6 recorded mutation legs.
- Cross-lane validation: Combined with the round-1 Kumitate JS leg (`scripts/kimi-census.mjs`), witness-scoped attribution has now been executed across **two independent fleet gates** in two distinct languages (JS and Bash), satisfying the `PROVINCE.md:14-16` multi-lane evidence bar.

#### Justified F2 Metadata Status: `held (round 12)` vs `partly held (round 12)`
There are two competing positions regarding F2's status transition:

- **Position A (`held (round 12)`):** The exact next falsifiable move defined in `corpus/README.md:79` ("the same split on a bash leg (surface-census): undefined → k_witness + k_accidental = 8") has been directly measured. Cross-lane evidence (Kumitate + Kagi) now exists.
- **Position B (`partly held (round 12)` — RECOMMENDED):** Restraint dictates keeping F2 as `partly held` because:
  1. **Adapter vs Source Divergence:** As documented in `WitnessSourceReview.md` and appended to `witness-scoped-kill-verdict.md` as errata E2/E3, Tameshi's adapter uses exact-line matching of full-suite output with any-of alternatives, which differs significantly from S006's single whole-token witness in `FAIL: ` lines.
  2. **Heuristic Declarations:** Witness declarations remain analyst-authored text heuristics rather than AST- or trace-derived compiler proofs.
  3. **No Accidental Kills Observed:** Both measured legs (JS 8/0/2, Bash 8/0/2) yielded $k_{accidental}=0$. The capability to detect accidental kills in practice remains unexercised on a real defect.
  4. **Harness Non-Integration:** The study lives in `tools/bash-witness-study.py`, while the production runner `tools/mutate-and-run.sh` remains frozen and unaware of witness attribution.
  5. **No Independent Knowledge File:** C2 does not introduce a standalone `corpus/knowledge/bash-witness-verdict.md` entry; it adds errata E2/E3 to the JS note and an entry in `round-12.md`.

#### Formulated Next Falsifiable Move for F2:
> `manual any-of declarations on two gates → compiler/AST-grounded witness derivation OR witness-scoped execution integrated directly into the mutation runner`

---

## 4. Audit of SOURCES ID Allocations & Contract Conformance

### 4.1 Registry ID Space Census

Inspection of `corpus/SOURCES.md`:
- `S001–S030`: W1 ART lead rows (all 30 rowed in Round 1).
- `S031–S037`: Reserved for own-work and pinned fleet gate rows (7 used).
- `S038–S039`: **Allocated, never written, retired** — never reused or renumbered per lesson `round-1.md` ER-K8.
- `S040–S046`: Round-1 frontier lead sweep rows (S040–S045 queued/mined, S046 rejected).
- `Next unused id`: **`S047`** (`corpus/SOURCES.md:131`).

### 4.2 Round 12 Allocations & Mutated Fields

- **New IDs allocated:** **None.** Round 12 required no new external literature. `S047` remains the next unused ID. Any seat attempting to allocate S047 for an already-registered source violates contract rule 2.
- **Permitted In-Place Cell Mutations (Rule 2):**
  Only `status`, `recheck`, and `used-by` may change in place. All changes must be logged old→new in `corpus/lessons/round-12.md` `## Gate`.
  1. **`S004` (cargo-mutants):**
     - `status`: `mined` (unchanged)
     - `recheck`: `on-release` (unchanged)
     - `used-by`: `corpus/knowledge/mutation-score-semantics.md` → appended `corpus/knowledge/repeated-control-precondition.md`
  2. **`S006` (shmutant):**
     - `status`: `mined` (unchanged)
     - `recheck`: `90d` (unchanged)
     - `used-by`: `corpus/knowledge/witness-scoped-kill-verdict.md, corpus/knowledge/mutation-score-semantics.md` → appended `corpus/lessons/round-12.md`
  3. **`S026` (Google flaky tests):**
     - `status`: `queued` → **`mined`**
     - `recheck`: `730d` (unchanged)
     - `used-by`: `—` → **`corpus/knowledge/repeated-control-precondition.md`**
- **Search Log Entry:**
  Rule 5 requires a bounded search log entry. The round-12 entry has been appended at `corpus/SOURCES.md:101-102`:
  `2026-10-20 — round-12 bounded F2/F3 re-open. Question: what can repeated pristine controls and declared witnesses establish? Opened existing rows S004, S006 and S026 at their canonical URLs...`

### 4.3 Census Integrity Risks (`sources-census-v2.sh`)

1. **Risk R1 (Part A — Mined without used-by):** `sources-census-v2.sh` Part A asserts that every `mined` row points to a file that exists in the repo. Flipping `S026` to `mined` before `corpus/knowledge/repeated-control-precondition.md` is committed will trigger `== A mined used-by missing` (exit 1).
2. **Risk R2 (Part B2 — Missing ID/path citation):** The newly created `corpus/knowledge/repeated-control-precondition.md` MUST explicitly cite `S026` (or `flaky-tests-at-google-and-how-we.html`) and `S004` in its text, or the B2 check will fail with `no-id-or-path-cite` (exit 1).
3. **Risk R3 (S038–S039 Gap):** Automated tools scanning for contiguous IDs must recognize the retirement note (`corpus/SOURCES.md:126-129`); renumbering or filling this gap is prohibited.

---

## 5. Audit of `1-verifier-spotcheck` & Non-Author Authority

### 5.1 Normative Definition of the Spot-Check

In `corpus/lessons/round-1-verifier-spotcheck.md` and `corpus/lessons/round-1.md` (lines 132–135, 208–212, 304–308):
- A valid spot-check requires an **independent non-author agent** dispatched by the orchestrator **after the round lands**, evaluating at least one admit and one reject decision from the round's `## Gate`.
- The historical round-1 spot-check was performed post-landing by orchestrator agent `W3ReviewTameshi`, admitting `witness-scoped-kill-verdict.md` and rejecting `S046` / `Timeout` rule.

### 5.2 Strict Boundary on Lane-Dispatched Seats

- `LEARNING.md:39-43` and `PROTOCOL.md:64-65` state: **"agents dispatched by this lane are still the lane."**
- Internal reviewer/critic seats in Round 12 (`WitnessSourceReview`, `RegistryReview`, `ControlThreats`, `WitnessThreats`, `AdmissionBounds`) are subagents of the lane. Their evaluations are **lane-internal advisories**, not independent spot-checks.
- Claiming that an internal review constitutes a valid `1-verifier-spotcheck` is an instance of **Mistake MK-11 ("Same-lane authority claimed as independent")**.
- Consequently:
  - No SHONEN box mark can flip from `[~]` to `[x]`.
  - Calibration score cannot advance beyond the adjudicated 6.
  - The Round 12 external spot-check must be explicitly recorded in `corpus/lessons/round-12.md` as **`pending`**, to be performed post-landing by the orchestrator.

---

## 6. Exact Metadata Changes Recommended for L1

The following changes should be applied by the L1 integration owner upon landing:

### 6.1 Recommendations for `corpus/README.md`

#### A. In `## Frontier` table (`:79-80`):
```markdown
| F2 | witness-scoped kill verdicts / bash mutation tooling | S006 | partly held (round 12) — `knowledge/witness-scoped-kill-verdict.md`, `tools/bash-witness-study.py` | manual any-of declarations on two gates → compiler/AST-grounded witness derivation OR witness-scoped execution in runner |
| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040 | partly held (round 12) — `knowledge/repeated-control-precondition.md` | pristine control gate verified (N=3) → integrate repeat-control into mutate-and-run.sh pre-sweep OR evaluate flaky mutant classification (S011) |
```

#### B. Append to `## Frontier — status correction`:
```markdown
## Frontier — status correction (fleet round 12, appended)

- **F2 — partly held.** Measured on both JS (kimi-census, 8/0/2) and Bash (surface-census, 8/0/2) gates. While the next move on bash is measured, status remains partly held because witness declarations rely on analyst-authored any-of string heuristics, S006 whole-token vs exact-line adapter divergences exist (errata E2/E3), the bash study tool is standalone rather than integrated into the production runner, and no accidental kills have yet been observed in practice.
- **F3 — partly held.** The repeated pristine-control capability (tools/repeat-control.py, N>=3 runs, byte-identical exit/stdout/stderr) and its knowledge note (knowledge/repeated-control-precondition.md) are admitted. Status is partly held rather than held because N=3 identical controls rules out only gross immediate nondeterminism without curing flakiness or proving determinism, volatile output without normalization over-rejects healthy tests, and flaky-aware verdicts across mutant runs remain unaddressed.
```

### 6.2 Recommendations for `SCORECARD.md`

1. **Depth Score:** Stays **6** (`recorded_cases=6 depth_score=6`). Do not increment to 7.
2. **Calibration Score:** Stays **6** (adjudicated baseline; command C upper bound 8 minus 2 by manual box-3 exclusion).
3. **Capabilities Table:** Add capability row:
   ```markdown
   | repeated pristine-control gate | run command N>=3 times, assert byte-identical exit/stdout/stderr with raw tuple comparison | `python3 tools/repeat-control.py --selftest` → exit 0; `.ufo/evidence/round-12/ControlGate/expected.json` | fleet round 12 |
   ```
4. **Planned Section:** Update planned items for Round 13 (advancing freshness re-sweeps, runner integration of repeat-control, AST witness derivation).

---

## 7. Risks & Verification Gaps

1. **Mid-Flight Execution Barrier:** Per the lane contract, no tests, builds, or census scripts were executed mid-flight by this seat. All findings derive from static inspection of committed files, spec definitions, and peer reports.
2. **Knowledge File Landing Dependency:** If L1 commits the `S026` status flip in `corpus/SOURCES.md` before `corpus/knowledge/repeated-control-precondition.md` is present on disk, `sources-census-v2.sh` will fail Part A.
3. **Volatile Output Sensitivity:** `repeat-control.py` compares raw bytes. Any target suite emitting timestamps, process IDs, or temporary file paths in its green baseline will fail `controls_mismatch`.
4. **Statistical Power Limitation:** $N=3$ identical runs provides minimal assurance against low-probability flakes ($p \le 0.10$). Claims citing "determinism" must be rejected.

---

## 8. Owned Paths & Tooling Statement

- **Owned Path Written:** `.ufo/waves/round-12/w1/FrontierState.md` (this report).
- **Shared Files Modified:** None.
- **Tooling Statement:** No tools were installed, upgraded, or removed. All operations used existing system utilities (`python3`, `git`, `grep`).
- **Authority Statement:** This report is an advisory scout deliverable within the UFO-FSD swarm and carries no independent non-author verification or admission authority.
