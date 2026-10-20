# InstructionScope — SKILL Gate Registry & Repeat-Control Interface Analysis (Round 12, Wave w2)

**Seat:** `TameshiR12.InstructionScope` (scout, leaf, read-only analysis)  
**Report target:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/InstructionScope.md`  
**Status:** Complete, read-only. No tests, builds, lints, or test runs executed. Advisory and lane-internal; NOT an independent non-author promotion or admission.

---

## 1. Godspeed Axes

1. **Axis 1 (Contract Fidelity & Correctness):** Ground analysis strictly in the implementation of `tools/repeat-control.py`, the round-12 contract (`.ufo/waves/round-12/spec.json`), and the foundational knowledge entries (`corpus/knowledge/repeated-control-precondition.md`).
2. **Axis 2 (Epistemic Discipline & Line Citation):** All findings cite exact file locations (`path:line`) with strict separation of observed facts `[O]`, inferences `[I]`, and open gaps `[U]`. No fabricated passes or unbacked assertions.
3. **Axis 3 (Coldread & Anchor Preservation):** Preserve line-number stability across lines 1–1477 of `SKILL.md` and evaluate the exact cryptographic and evidentiary consequences of appending vs holding `SKILL.md`.

---

## 2. Repeat-Control Module Interface Analysis (`tools/repeat-control.py`)

`tools/repeat-control.py` (790 lines, SHA-256 `29d8025490f349c106bc8132da7bfecc2ae4f8fb00720b43636e52335d27467a`) implements the Capability C1 repeated-control gate.

### 2.1 Invocation Modes and Syntax
1. **Run Mode `[O]` (`tools/repeat-control.py:13, 211-248, 779`):**
   ```bash
   python3 tools/repeat-control.py --runs N --out DIR -- COMMAND [ARG...]
   ```
   - Separator `--` is mandatory before the command (`:239-242`).
   - `--runs N`: Requires an ASCII integer with $N \ge 3$ (`:243-247`). Any $N < 3$, non-integer, or missing value returns exit 64 (`invalid_usage`).
   - `--out DIR`: Directory where observations are persisted. The directory must not already exist; it is created fresh with exclusive byte writes (`open(path, "xb")`, `:167-170, 300-302`). An existing DIR exits 64 (`invalid_usage`).
   - Execution semantics: Executes the exact argv after `--` using `subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)` in the caller's working directory (`:264-272`). Environment is inherited unchanged.
   - Saved files in `DIR`:
     - Per run $k \in \{1 \dots N\}$: `run-<k>.stdout` (raw bytes), `run-<k>.stderr` (raw bytes), `run-<k>.exit` (decimal returncode + `\n`, or literal `unavailable\n`).
     - Metadata: `command.txt` (`tool`, `tool-sha256`, `interpreter`, `python`, `cwd`, `runs`, `argv`), and `finding.txt` (`finding_id` + exit code) written last (`:251-261, 306, 323-326`).
   - Comparison discipline: Raw byte-for-byte (`:22-24, 197-201`). No string decoding, whitespace trimming, or newline normalization.

2. **Snapshot Verification Mode `[O]` (`tools/repeat-control.py:14, 50-62, 412-434, 770-773`):**
   ```bash
   python3 tools/repeat-control.py --snapshot DIR
   ```
   - Validates committed observations under `DIR` against `expected.json` (schema `repeat-control-snapshot-v1`, `:124, 346-360`).
   - Verifies SHA-256 of all listed inputs and recomputes the classification finding directly from stored bytes without executing any subprocess (`:408, 412-434`).
   - Exits: Recorded exit on match; exit 1 (`controls_mismatch`) on expectation disagreement; exit 2 (`snapshot_tampered`) on missing, unlisted, modified, or symlinked files (`:56-60, 420-434`).

3. **Hermetic Selftest Mode `[O]` (`tools/repeat-control.py:15, 64-77, 545-757, 766-769`):**
   ```bash
   python3 tools/repeat-control.py --selftest
   ```
   - Hermetic execution under `/tmp/tameshi-r12-repeat-control-selftest.*` (`:626-628`).
   - Returns exit 0 on all cases passing (`SELFTEST: PASS (<N> cases)`, `:750-752`); exit 1 on case failure (`:747-749`); exit 2 on could-not-evaluate / harness crash (`:753-756`).

### 2.2 Finding IDs, Exit Codes, and Precedence
`tools/repeat-control.py:115-123` defines the stable exit map:
- `controls_match` $\to 0$: Clean pass. All $N$ runs produced identical exit 0, identical stdout bytes, identical stderr bytes.
- `controls_mismatch` $\to 1$: Disagreement in exit status, stdout bytes, or stderr bytes across runs.
- `baseline_nonzero` $\to 2$: Uniform, identical nonzero baseline across all $N$ runs (e.g. $[1,1,1]$ with matching streams).
- `command_unavailable` $\to 2$: Command could not be executed (`ENOENT`, `EACCES`, `ENOEXEC`).
- `snapshot_tampered` $\to 2$: Corrupted, unlisted, or modified files in `--snapshot DIR`.
- `setup_error` $\to 2$: Harness failure or unhandled exception.
- `invalid_usage` $\to 64$: CLI syntax violation ($N < 3$, missing `--`, existing `--out` directory).

**Fixed Precedence Rule `[O]` (`tools/repeat-control.py:30-40, 191-205`):**
1. `command_unavailable` takes top priority if any run could not execute.
2. `controls_mismatch` is evaluated next. Any divergence in exit or stream bytes triggers `controls_mismatch` (exit 1). A sequence such as $[0, 1, 0]$ or $[1, 2, 1]$ is strictly `controls_mismatch`, never `baseline_nonzero`.
3. `baseline_nonzero` applies only if all runs agree uniformly and exit status $\ne 0$.
4. `controls_match` applies only if all runs agree uniformly with exit status 0.

---

## 3. SKILL Gate Registry Sections & Insertion Location

### 3.1 Existing Candidate Registry Sections in `SKILL.md`
1. **Gate-Shape Decision Table `[O]` (`SKILL.md:58-65`):**
   - Header: `## Gate-shape decision table — hermetic vs live vs audit-lane`
   - Columns: `| Shape | Answers | Runs against | Green means (and only means) | Source |`
   - Defines taxonomic categories (Hermetic suite, Live gate, Audit lane).
2. **Artifact Map Table `[O]` (`SKILL.md:1380-1394`):**
   - Header: `### The map — where a reader enters, artifact by artifact`
   - Columns: `| Artifact | Holds | Read it when |`
   - Current rows include `operator-runbook.md`, `fleet-kill-rate-ledger.md`, `tools/mutate-and-run.sh`, etc.
3. **Six-Leg Regression Table `[O]` (`SKILL.md:1302-1318`):**
   - Lists the 6 mutation legs replayed by `tools/mutate-and-run.sh --regression`.
   - **Boundary Exclusion `[O]` (`spec.json:context`, `repeated-control-precondition.md:53`):** `tools/repeat-control.py` is an independent precondition check, **not** a 7th mutation leg. Inserting it into the leg regression table is strictly forbidden.
4. **Corpus Coverage Map `[O]` (`corpus/README.md:4-15, 38-62`):**
   - Columns: `| Note | Holds | Sources |`
   - Primary registry for lane knowledge entries and governed tools.

### 3.2 Insertion Location Analysis
- **Mid-file insertion in `SKILL.md` is strictly forbidden `[O]` (`SKILL.md:1460-1462`, `AdmissionBounds.md:68`):**
  `SKILL.md:1460-1462` mandates:
  > *"Append-only to the last line: nothing above this section was edited by this write; the recorded tables stand at their revisions, and a reader on a differing revision re-resolves rather than trusts."*
  Inserting rows mid-file (e.g. at line 65 or line 1395) shifts line numbers for the entire subsequent body of `SKILL.md`, instantly invalidating existing line-anchored citations across the lane (e.g. `reports/round-1-calibration.md`, `witness/README.md`, `SHONENReview.md:33, 68`).
- **Permissible `SKILL.md` Location `[I]`:**
  Strictly **append-only at EOF** (starting at line 1478, following line 1477).
  New section heading:
  ```markdown
  ## Capability C1 gate — repeated control (round 12, appended)
  ```
- **Alternative/Primary Location `[I]`:**
  `corpus/README.md:63` (`## Coverage map — addendum`), which is already structured for append-only entry additions without disturbing `SKILL.md`.

---

## 4. Complete Registry Row Fields

### 4.1 `SKILL.md` Artifact Map Format (`| Artifact | Holds | Read it when |`)
- **Artifact:** `tools/repeat-control.py` (supported by `corpus/knowledge/repeated-control-precondition.md`)
- **Holds:** Repeated pristine-control gate for C1 (runs exact argv $N \ge 3$ times with stdin `/dev/null`, compares raw bytes of stdout/stderr/exit; finding IDs: `controls_match` exit 0, `controls_mismatch` exit 1, `baseline_nonzero` exit 2, `command_unavailable` exit 2, `snapshot_tampered` exit 2, `setup_error` exit 2, `invalid_usage` exit 64; snapshot validation mode `--snapshot DIR`; hermetic `--selftest`). Finite-run stability observation only; not a determinism proof; not a 7th mutation leg.
- **Read it when:** Validating baseline stability before a mutation sweep, verifying committed control snapshot integrity, or checking for flaky-test drift on pristine code.

### 4.2 `SKILL.md` Gate-Shape Decision Table Format (`| Shape | Answers | Runs against | Green means (and only means) | Source |`)
- **Shape:** **Repeated-control gate** (`--runs N -- COMMAND` / `--snapshot DIR`)
- **Answers:** Did $N$ finite pristine control runs agree byte-for-byte in exit, stdout, and stderr? Or does a committed snapshot match stored bytes?
- **Runs against:** The exact argv after `--` in caller cwd with inherited env, stdin `/dev/null`; or committed snapshot directory `DIR` (`expected.json` + run files)
- **Green means (and only means):** `controls_match` (exit 0) — all $N$ runs produced identical exit 0, stdout bytes, stderr bytes (finite stability in this environment; NOT proof of determinism); or snapshot verified intact
- **Source:** `corpus/knowledge/repeated-control-precondition.md`, `tools/repeat-control.py`, S004, S026

### 4.3 `corpus/README.md` Coverage Map Format (`| Note | Holds | Sources |`)
- **Note:** `knowledge/repeated-control-precondition.md` — gate `tools/repeat-control.py`
- **Holds:** Repeated pristine-control gate for C1: runs exact argv $N \ge 3$ times, stdin `/dev/null`, raw byte comparison of stdout/stderr/exit; stable finding IDs `controls_match` (0), `controls_mismatch` (1), `baseline_nonzero` (2), `command_unavailable` (2), `snapshot_tampered` (2), `setup_error` (2), `invalid_usage` (64); snapshot validation `--snapshot DIR`; hermetic `--selftest`. Finite-run stability observation only; not a determinism proof; not a 7th mutation leg.
- **Sources:** S004 (mined), S026 (mined upon round-12 promotion), S040 (queued).

---

## 5. Assessment: Coldread Binding Affected by Append-Only Addition

### 5.1 The Historical Coldread Binding `[O]`
1. **Blob & SHA-256 Pin:**
   - `reports/round-1-kaika-coldread.md:58-62`: The cold-read explicitly binds to `SKILL.snapshot.md` with SHA-256 `33e3009c919cd0fb0b2c67bbd7927655289450750f4f69d9ca86758d81000f81`, 1477 lines, captured at commit `4eb4cf3`.
   - `SCORECARD.md:171-174`: `K1 evidence: reports/round-1-kaika-coldread.md (COLDREAD: SUFFICIENT ... SKILL.md sha256 33e3009c…0f81, unchanged by this round)`.
   - `SHONEN.md:10`: `[~] Instructions executable by an agent without oral context [lane assertion, scope-bounded: fleet round-1 cold-read of blob 4eb4cf3:SKILL.md — Appendix A + B sweep recipe only, 8/10 + 8/10 = recorded...]`.
2. **Explicit Re-run Trigger:**
   - `corpus/README.md:100-103`:
     > *"Left unedited so the cold-read stays bound to the executed bytes; the next SKILL.md edit re-runs it."*
   - `corpus/lessons/round-1.md:447-448`:
     > *"not edited this round, so box 3 stays bound to the executed bytes (git show 4eb4cf3:SKILL.md | sha256sum -> 33e3009c…0f81)."*

### 5.2 Impact of Append-Only Addition (Lines 1478+) `[I]`
1. **Line-Number Invariance (Preserved):**
   Because additions are strictly appended after line 1477, line numbers 1–1477 remain identical.
   - All historical line citations in Appendix A (`:527-592`), Appendix B (`:594-668`), mutation recipes (`:131-245`), uniqueness gates (`:171-178`), and arm taxonomy (`:497-525`) remain fully stable and resolvable.
2. **Digest Mutation (Broken):**
   - Modifying `SKILL.md` changes its working tree SHA-256 away from `33e3009c...0f81`.
   - Per `corpus/README.md:103`, any byte modification to `SKILL.md` formally expires the active claim that the working tree file has been verified by the cold-read, triggering the requirement that "the next SKILL.md edit re-runs it".
3. **SHONEN Box 3 Contractual Status:**
   - `SHONEN.md:10` explicitly bounds its scope to `blob 4eb4cf3:SKILL.md`. That git blob object remains immutable in the git store.
   - However, if the working tree `SKILL.md` is appended, the file in the working tree diverges from the cold-read-verified blob. Any report claiming the *current* `SKILL.md` is cold-read verified would be an overreach without a fresh non-author cold-read execution.
4. **Alignment with Wave-1 Review Findings (`SHN-2`):**
   In wave 1, `SHONENReview.md` explicitly reported (`SHONENReview.md:33-34, 73, 108`):
   - `SHN-2 (SKILL bytes bound by box 1/3): hold SKILL.md.`
   - "Any edit moves the bytes that box 1's line anchors ... and box 3's cold-read both bind to. Recommendation: keep `[~]`. No `SKILL.md` edit in this round. A C2 'witness case(s)' field proposal ... must land in `corpus/` only."

### 5.3 Concrete Recommendation for L1 Integration Owner
1. **Preserve `SKILL.md` Unchanged (Optimal):**
   To avoid invalidating the cold-read byte pin and triggering a mandatory full cold-read re-run under `corpus/README.md:103`, L1 should keep `SKILL.md` byte-identical to `blob 4eb4cf3` (`33e3009c...0f81`).
2. **Land Registration in `corpus/README.md` & `corpus/knowledge/`:**
   Apply the registry row to `corpus/README.md:63` (`## Coverage map — addendum`) and `corpus/knowledge/repeated-control-precondition.md`. This fulfills complete gate registration across the corpus without touching `SKILL.md`.
3. **If Appending to `SKILL.md` is Decided:**
   - Must be strictly placed at EOF (line 1478+) under `## Capability C1 gate — repeated control (round 12, appended)`.
   - `LOG.md` and round reports must explicitly record that lines 1–1477 are unchanged, that line anchors remain valid, but that `SKILL.md` SHA-256 has diverged from `blob 4eb4cf3`, and that SHONEN box 3 remains scope-bounded to `blob 4eb4cf3:SKILL.md` until a fresh cold-read is performed.

---

## 6. Tooling Record

No tools were installed or updated during this read-only scout assignment. All investigations used internal read tools.
