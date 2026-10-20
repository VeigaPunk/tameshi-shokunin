# PlannerDataWalk — Round 15 Wave 1 Connector Report

**Author:** `TameshiR15.PlannerDataWalk` (connector, leaf member)  
**Role:** UFO-FSD Connector / Bounded Canonical Planner Supplement  
**Lane Root:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`  
**Report Target:** `.ufo/waves/round-15/w1/PlannerDataWalk.md`  
**Head Read Revision:** `a9cf4da78f2514c7bedd91a850a88590009d7df0`  

---

## 1. Declared Lane Axes

Per `AXES.md` and `SCORECARD.md`:
1. **Calibration ($C_1$, scalar 6, tied lowest with depth 6):** Target of C1 capability acquisition this round. Bounded expectation reconciliation, rigorous classification of gates versus probes, hermetic exit-lattice verification ($0/1/2/64$), non-vacuous discriminators.
2. **Depth (scalar 6):** Preserved, unchanged. Exactly 6 historical recorded mutation cases; no unearned 7th case.
3. **Coverage (scalar 6):** Preserved, unchanged. No whole-frontier expansion claims.
4. **Operability (scalar 6):** Preserved, unchanged. `mutate-and-run.sh` runner unchanged; tool entry points and CLI contracts made explicit.
5. **Freshness (scalar 6):** Preserved, unchanged. Honest intake refusal retained; no unapproved successor sweeps.
6. **Adjacency (scalar 6):** Preserved, unchanged. Sibling repos read-only; no sibling gates executed.

---

## 2. Evidence: Data-Walk of Routed Defect 5

### 2.1 The Observed Mismatch (Origin & Verifier Ruling)
In Round 14, `capture-context.py` was created under `.ufo/evidence/round-14/` to prospective-capture ambient versus poisoned environment behavior and runner leg mappings. In `SKILL.md:1602`, it was registered as:
```text
invocation context capture | probe | python3 .ufo/evidence/round-14/capture-context.py | 0 bounded experiment/mappings agree; 1 observed mismatch or failed control; 2 could-not-evaluate setup | no standalone selftest ...
```
In `corpus/lessons/round-14-verifier-spotcheck.md:160`, the non-author closure issued **Routed Defect 5**:
1. **Functional Classification Mismatch:** `capture-context.py` reads persisted declarations (`.ufo/evidence/round-13/expected.json` input pins and `pin-manifest.json` derived digests), validates runner text against them (`evaluate()`, lines 476–515), and emits `("mismatch", 1, reasons)` via `decide()` (lines 553–580) on any disagreement. Under `SKILL.md:60–75` (§Gate standard), comparing durable persisted expectations and returning a pass/fail verdict (exit 0 vs exit 1) defines a **gate**, not a probe.
2. **Missing Standalone Selftest:** It lacked an isolated public CLI `--selftest` asserting literal exit codes and stable expected finding IDs. Ad-hoc helper checks (`guardrails.json`: `missing-field1`, `variable-name-swap rejection0`) do not satisfy this requirement.
3. **Exit 64 Discrepancy:** In code (`capture-context.py:613`), unexpected arguments exit 64. However, exit 64 was absent from its `SKILL.md` registry row. Additionally, C1's (`tools/evidence-disposition.py`) registry row labelled 64 merely as "usage", rather than grouping it under `could-not-evaluate` alongside exit 2.

### 2.2 The Artifact Criterion
- **Preservation Contract:** Historical scripts and receipts (`.ufo/evidence/round-14/capture-context.py` and `context-receipt.json`) must remain byte-identical.
- **Promoted Command:** Maintained active gate lives at `tools/context-capture.py`.
- **Trap Identified (Path Arithmetic):** Historical code derives `LANE_ROOT` via `os.path.dirname` $\times 4$ (line 46). At `tools/context-capture.py`, $\times 4$ resolves to `/home/vgpnk/Projects`, breaking lane path resolution, control execution, and output placement. The promoted tool must derive `LANE_ROOT = os.path.dirname(os.path.dirname(SELF))`.
- **Output Target:** Prospective executions write to `.ufo/evidence/round-15/context-receipt.json`, never overwriting Round 14 evidence.
- **Offline Receipt Check:** The tool must expose a `--check <receipt>` mode to verify retained receipts without executing live git commands or child subprocesses.

### 2.3 The Registry Criterion
`SKILL.md` must be updated to:
- Classify `tools/context-capture.py` as a `gate` (promoted from probe).
- Register `python3 tools/context-capture.py --selftest`.
- Align the exit lattice symmetrically across both gates (`tools/evidence-disposition.py` and `tools/context-capture.py`):
  - `0`: clean (all declared checks pass)
  - `1`: failed semantic expectations / observed mismatch / failing control
  - `2 and 64`: could-not-evaluate (`2` setup/tampered/unparseable input; `64` usage error)

### 2.4 The Selftest Criterion
- **Hermeticity:** Must execute inside `tempfile.TemporaryDirectory()`, reading zero live repository files and writing zero files outside the temporary directory.
- **Public CLI Execution:** Must invoke `subprocess.run([sys.executable, str(tool_path), ...])`, testing actual process boundaries.
- **Discriminative Coverage:** Must test literal exits and stable finding IDs across all four exit classes ($0, 1, 2, 64$).
- **Deterministic Assertions:** Must output a closing summary matching `CONTEXT_SELFTEST: N/N pass` / `VERDICT: PASS` and exit 0.

---

## 3. Distinguishing Minimum Fix from Broad Redesign

| Dimension | Broad Redesign (Reject / Anti-Pattern) | Minimum Bounded Fix (Admit / Target) |
|---|---|---|
| **Environment Scope** | Universal environment capture, full `os.environ` dumping, dynamic library / syscall tracing. | Explicit single-variable override (`GIT_DIR`); ambient scrub of `GIT_*` keys; key-name logging only (shape-only, zero secret content read). |
| **Historical Claims** | Attempting to retroactively prove Round 13's missing setup or infer general environment independence. | Retain `result_reuse: not_established`; treat Round 14/15 receipts strictly as bounded prospective experiments. |
| **Tool Architecture** | Complex multi-module framework, dynamic plugin discovery, external dependencies. | Single-file promotion to `tools/context-capture.py` (stdlib Python 3), reusing existing `decide()`, `comparison_block()`, and `mapping_block()` semantics. |
| **Verification Mode** | Forcing live re-execution of subprocesses during verification. | Dual-mode CLI: prospective capture (default) and deterministic offline check (`--check <receipt>`), paired with hermetic `--selftest`. |
| **Selftest Fixtures** | Copying live repo files into `/tmp` or testing internal Python functions only. | Pure synthetic stub probe and minimal synthetic runner/manifest fixtures created entirely in `mkdtemp`. |

---

## 4. UFO-FSD Connector Move: One Non-Obvious Move

### The Proposed Move
**Synthesized Dual-Anchor Verification with Tightened Positive Control and Positional Finding Vectors**

Across peer proposals (`GateClassification.md`, `ReviewControl.md`, `ReviewNames.md`, `ReconEnvironment.md`), one central friction emerges:
1. Historical `decide()` trusts raw stored booleans (`control.get("effective")`, `mapping.get("all_match")`), making receipt checking vacuous if not recomputed.
2. In `positive_control_block()`, the historical `effective` predicate (`baseline_ok and injected.exit != 0 and reflects`) was technically satisfied by *any* nonzero exit of injected `git`, even if the poison path was never reached (false positive risk H3).
3. In `mapping_block()`, mutating a runner constant produces a whole-file runner digest mismatch *before* the leg mapping mismatch reason is reached.

**The Move:**
1. **Tighten Positive Control Predicate:** In `positive_control_block()`, require that `POISON_PATH` literally appears in `injected.stderr` (preserving Round 14's retained receipt, where `fatal: not a git repository: '/nonexistent/tameshi-round14-poison'` was recorded, while eliminating vacuous failure modes).
2. **Deterministic Offline Receipt Check (`--check`):** Have `--check <receipt>` parse the JSON, recompute `effective` and `decide()` from the raw `runs` and `sources` payloads without re-executing git or probe subprocesses, and assert that the computed verdict matches the stored status and exit code.
3. **Structured Finding Vectors:** Have `decide()` return stable finding ID tokens (`CTX-CLEAN`, `CTX-POSITIVE-CONTROL-INEFFECTIVE`, `CTX-RUNNER-MAPPING-FAIL`, `CTX-PROBE-DIGEST-MISMATCH`, `CTX-RUNNER-DIGEST-MISMATCH`, `CTX-PROBE-MISMATCH`, `CTX-SETUP-INVALID`, `CTX-USAGE`) alongside free-text reasons, enabling selftest to pin stable machine-readable tokens.
4. **Symmetric 4-Class Exit Lattice:** Formally establish the unified `0 / 1 / 2 and 64` classification in `SKILL.md` for both C1 disposition and context gates.

### Second-Order Effects
- **Runtime Surface:** Offline verification runs instantaneously with zero git lock contention, zero subprocess overhead, and zero dependence on ambient git configuration.
- **Contract Surface:** Resolves Routed Defect 5 completely without exceeding the strict boundaries of C1 capability. No 7th mutation case is introduced; no unearned environment independence is claimed.
- **Substrate Surface:** Leaves `.ufo/evidence/round-14/` completely untouched and byte-identical. Round 15 output is isolated to `.ufo/evidence/round-15/context-receipt.json`.
- **Verification Surface:** Provides L1 and external closure with a sub-second, hermetic verification command (`python3 tools/context-capture.py --selftest`) that tests process exit boundaries on clean, mismatch, setup, and usage conditions.

---

## 5. Contradictions & Risks

1. **Stored Verdict Trust vs. Offline Verification:**
   - *Contradiction:* A naive `--check` that only reads `receipt["status"]` verifies nothing; re-running git subprocesses violates offline verification and risks flakiness.
   - *Resolution:* Recompute `decide()` over the stored raw outputs (`runs.baseline`, `runs.injected`, `sources`) without re-spawning processes.
2. **Exit 64 Ontology:**
   - *Contradiction:* Exit 64 is triggered by syntax/argument errors (a usage defect), but in the decision lattice it cannot evaluate the gate's target.
   - *Resolution:* Group exit 64 under `could-not-evaluate` alongside exit 2 in `SKILL.md` (`2 and 64 could-not-evaluate: 2 setup/tampered, 64 usage`), distinguishing it from semantic mismatch (exit 1).
3. **Runner Mutation Ordering:**
   - *Contradiction:* A runner variable swap causes both a whole-file runner digest mismatch and a mapping reason.
   - *Resolution:* Selftest fixtures for variable swaps must anticipate both finding IDs (`CTX-RUNNER-DIGEST-MISMATCH` and `CTX-RUNNER-MAPPING-FAIL`) or update the synthetic manifest digest to isolate the mapping discriminator.

---

## 6. Verification Checklist for L1 Closure

*(To be executed by L1 after all seats return; not executed by this leaf seat)*:
- [ ] Confirm `tools/context-capture.py` exists with `LANE_ROOT = os.path.dirname(os.path.dirname(SELF))`.
- [ ] Run `python3 tools/context-capture.py --selftest` → exits 0, outputs `CONTEXT_SELFTEST: PASS` (all $0, 1, 2, 64$ fixture cases pass).
- [ ] Run `python3 tools/context-capture.py --check .ufo/evidence/round-14/context-receipt.json` → exits 0, validates historical receipt.
- [ ] Run `git diff d6809df7775338f000e44c8a916067b8866867fb..HEAD -- .ufo/evidence/round-14/` → empty (historical evidence byte-preserved).
- [ ] Verify `SKILL.md` Round-14/15 registry rows classify context capture as a `gate` with explicit $0/1/2\text{ and }64$ exit lattice.
- [ ] Verify `SCORECARD.md` keeps calibration at scalar 6 without inflation.
