# EvidenceCensus — Round 12 Inherited Evidence Inventory & Defect Census

**Seat:** `EvidenceCensus` (Scout, leaf member)  
**Round:** Tameshi Round 12, Wave 2  
**Target Root:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`  
**Assigned Report Path:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/EvidenceCensus.md`  
**Baseline HEAD:** `18ad5d050ef4bcd830fe513825baed878f025024`  
**Advisory Notice:** Lane-internal scout findings only. Read-only audit; zero test, suite, or check commands executed. Not an independent non-author admission, promotion, or verdict.

---

## 1. Scope, Posture & Axes (Godspeed)

- **Axes:**
  - **Calibration ($C_1$):** Integrity and verification fidelity of repeated pristine-control artifacts, preventing ungrounded runtime claims or unpersisted fixtures from masquerading as operational capabilities.
  - **Depth ($C_2$):** Ground-truth defect attribution in mutation testing, preventing unexecuted witness studies or phantom summary files from falsely claiming deepened test evaluation.
  - **Evidence Discipline (`corpus/QUALITY.md`):** Strict adherence to criteria 2 (no oral knowledge / verified anchors), 3 (strict separation of observation vs inference vs unknown), 8 (unreported runs are debt, not passes), 9 (scratch stays in `/tmp`, evidence copied into repo before citation), 11 (finite control sample boundaries), and 12 (frozen witness declaration integrity).
- **Target of Census:**
  1. Complete inventory of inherited round-12 evidence in `.ufo/evidence/round-12/`.
  2. Identification of all runtime claims across repo files and wave-1 reports that lack actual outputs.
  3. Identification of all temporary-path-only links (`/tmp/...`) where evidence was not persisted in-repo.

---

## 2. Complete Inventory of Inherited Evidence (`.ufo/evidence/round-12/`)

The inherited evidence tree under `.ufo/evidence/round-12/` comprises 7 root files and 26 seat/topic subdirectories (containing 125 total regular files):

### 2.1 Root Manifest and Measurement Files
| Path | Metrics | Purpose & Observation |
|---|---|---|
| `before.json` | 18 lines, 334 B | Baseline metrics at `18ad5d0`: records `"bash_witness_summary": {}`, `"repeat_control_artifact": 0`, 6 recorded legs, 44 source rows. |
| `before-with-score-exclusions.json` | 28 lines, 483 B | Baseline metrics including explicit calibration box exclusions (`calibration_restraint_score: 6`, `calibration_excluded_boxes: [3]`). |
| `claims.json` | 14 lines, 1,326 B | Round-12 claim declarations for C1 (calibration repeated-control capability) and C2 (depth bash witness attribution). |
| `measure.py` | 46 lines, 1,939 B | Artifact counting script scoring boxes 1, 2, 4 while excluding box 3; attempts to load `.ufo/evidence/round-12/BashWitness/summary.json` (returns `{}` when absent). |
| `sources-before.txt` | 3 lines, 178 B | Verification receipt of `scripts/sources-census.sh validate` against `corpus/SOURCES.md` (exit 0, CLEAN). |
| `runner-selftest.txt` | 6 lines, 219 B | Execution record of `bash tools/mutate-and-run.sh --selftest` (exit 0, `MUTATE_SELFTEST: 80/80 pass`, `VERDICT: PASS`). |
| `runner-regression.txt` | 40 lines, 3,467 B | Execution record of `bash tools/mutate-and-run.sh --regression` (exit 0, `REGRESSION: PASS (cases=6 passed=6)`). |

### 2.2 Subdirectory Evidence Breakdown
| Directory | File Count | Retained Files | Completeness Status & Integrity Gaps |
|---|---:|---|---|
| `AdmissionBounds/` | 2 | `pristine-repeat-probe.txt`, `pristine-selftest.stdout.1` | Complete probe capture; runs executed against scratch copy in `/tmp`. |
| `BashDenominator/` | 2 | `cases.tsv`, `parser.py` | Complete grammar definition and parser; purely static analysis. |
| `BashWitness/` | 2 | `pristine.sh`, `selftest.out` | **INCOMPLETE / SEVERE DEFECT:** Contains only pinned script and tool selftest. Missing all study outputs: `declared.tsv`, `declaration.json`, `summary.json`, `manifest.json`, and run outputs `D1.out`..`D10.out`. |
| `BaselineControl/` | 14 | `run_scenario.sh`, `fixtures/target.sh`, `fixtures/spec.txt`, `scenario-{a,b,c,d}.{exit,stdout,stderr}`, `workdir-scenario-{a..d}/` | Complete; fully self-contained demonstrations of single-control runner blindspots. |
| `BytesReview/` | 88 | `probe{,2,3,4}.py`, `probe{,2,3,4}.out`, `cli/C01`..`C20/` (each containing `command.txt`, `finding.txt`, `run-{1..3}.{exit,stdout,stderr}`) | Complete run matrix (20 cases); **TEMPORARY PATH DEFECT:** `command.txt` files point to uncopied `/tmp/bytesreview/` scripts. |
| `ClaimSkeleton/` | 1 | `witness_recount.py` | Static script; re-evaluates historical *JS* kimi-census evidence (`kaika-round-1/witness`), NOT the bash leg. |
| `ControlGate/` | 18 | `run-{1..3}.{exit,stdout,stderr}`, `mismatch/run-{1..3}.{exit,stdout,stderr}` | **INCOMPLETE / SEVERE DEFECT:** Contains raw run files but completely lacks `expected.json` (required by `--snapshot`), `command.txt`, and `finding.txt`. |
| `ControlKnowledge/` | 2 | `README.md`, `quotes.tsv` | Contains located quote table; **TEMPORARY PATH DEFECT:** Primary fetched HTML bodies kept in `/tmp/tameshi-r12-ck/fetch/` and not committed. |
| `ControlThreats/` | 3 | `gate-probes.sh`, `probes.py`, `probes.out` | Probe capture complete; `gate-probes.sh` was not executed against `tools/repeat-control.py`. |
| `EvidenceScribe/` | 1 | `inventory.md` | Complete inventory of expected values; no runtime executions. |
| `ExitReview/` | 2 | `cases/run-cases.sh`, `cases/seq.py` | **INCOMPLETE:** Fixture scripts present; target output directory `run/` was never created or executed. |
| `FailureOracle/` | 24 | `fixture.sh`, `fixture-mutation.diff`, `verify_gate.py`, `single_control_baseline.py`, `pristine-baseline/`, `red-before/`, `restored-baseline/`, `actual-pristine/`, etc. | Verified model runs present; `actual-pristine/` contains live pristine run of `repeat-control.py`; mutated `repeat-control.py` was not executed. |
| `GateRegistryScribe/` | 2 | `registry-row-draft.md`, `observed-probes.txt` | Draft documentation; records absence of `expected.json` at observation time. |
| `GateSecurity/` | 4 | `probes.py`, `probes.out`, `tty_probe.py`, `tty_probe.out` | Complete probe capture; `tty_probe.out` notes TTY path was unexercised due to harness limits. |
| `LessonScribe/` | 2 | `capture.txt`, `outline.md` | Draft notes. |
| `LimitsConnector/` | 1 | `decision-table.tsv` | Static mapping table. |
| `MinimalityReview/` | 1 | `probes.md` | Static review notes; cites `/tmp/mr-surface-census.sh`. |
| `MistakeMining/` | 2 | `finding.md`, `fourth-run-diverges.sh` | Revenger data walk notes and probe script. |
| `ReportScribe/` | 1 | `probe-capture.txt` | Probe capture of HEAD state and environment. |
| `SiblingOverlap/` | 1 | `overlap-mapping.json` | JSON mapping of sibling province boundaries. |
| `SnapshotReview/` | 2 | `probe.py`, `probe-output.txt` | Probe script and output evaluating snapshot design; notes `expected.json` absence. |
| `SourceBazel/` | 1 | `source-excerpt.txt` | Excerpt from Bazel Test Encyclopedia (S028). |
| `SourceFlakyPaper/` | 5 | `ISSTA2019.pdf`, `evidence.json`, `excerpt.txt`, `page-2.txt`, `page-9.txt` | Complete primary source retention for S011. |
| `SourceSurvey/` | 4 | `S040-excerpt.txt`, `evidence.json`, `opened.tsv`, `SHA256SUMS.txt` | Excerpts for S040; **TEMPORARY PATH DEFECT:** `2021a.pdf` omitted from repo (retained only in `/tmp/2021a.pdf`). |
| `SourceWitness/` | 2 | `S006.md`, `capture-meta.json` | Complete primary source retention for S006. |
| `SynthesisConnector/` | 4 | `connector_eval.py`, `decision_table.json`, `observed_eval.json`, `probes.out` | Synthesis decision evaluation. |

---

## 3. Runtime Claims Without Actual Outputs

A rigorous line-by-line inspection of repository documents, claims, and wave-1 reports reveals eight distinct runtime claim defects where files are cited as evidence, claims of completed runs are asserted, or required artifacts are absent:

### RC-1: Citations of Non-Existent `verification.json`
- **Citing Locations:**
  - `SKILL.md:1482`:
    > `runtime evidence: .ufo/evidence/round-12/verification.json.`
  - `corpus/README.md:127`:
    > `| knowledge/repeated-control-precondition.md / F3 | ... | S004, S026; tools/repeat-control.py; .ufo/evidence/round-12/verification.json |`
- **Finding:** The file `.ufo/evidence/round-12/verification.json` **does not exist** anywhere in the repository tree. Citing a nonexistent file violates `corpus/QUALITY.md` Criterion 2 ("Every claim carries a source: a measured anchor ... never oral knowledge") and Criterion 8 ("an executed-but-unreported verification is named debt, never cited as a pass").

### RC-2: Missing BashWitness Study Run Outputs & Phantom `summary.json`
- **Citing Locations:**
  - `corpus/README.md:128`:
    > `| knowledge/witness-scoped-kill-verdict.md / F2 | ... | S006; .ufo/evidence/round-12/BashWitness/summary.json; lessons/round-12.md |`
  - `SKILL.md:1504`:
    > `Pinned values: .ufo/evidence/round-12/BashWitness/declaration.json, declared.tsv, manifest.json`
  - `claims.json:7`:
    > `{"id": "C2", "axis": "depth", "type": "measured evidence deepening", ... "after_acceptance": "all ten defects have declared-witness classifications and captured failing labels with full denominator; aggregate result unchanged or discrepancy disclosed"}`
  - `measure.py:26-27, 36`:
    ```python
    summary_text = content('.ufo/evidence/round-12/BashWitness/summary.json')
    summary = json.loads(summary_text) if summary_text else {}
    ...
    'bash_witness_summary': summary,
    ```
  - `before.json:2` & `before-with-score-exclusions.json:2`:
    > `"bash_witness_summary": {}`
- **Finding:** `.ufo/evidence/round-12/BashWitness/` contains **only** `pristine.sh` and `selftest.out`. Missing completely from inherited state are:
  - `declared.tsv` (the frozen pre-sweep witness declarations)
  - `declaration.json` (the declaration input digests)
  - `summary.json` (the per-defect witness classification results)
  - `manifest.json` (the execution artifact digests)
  - `D1.out` through `D10.out` (the actual mutant execution log receipts)
- **Sub-finding:** In `ClaimSkeleton.md:29-35`, a witness split of `8 killed-on-witness, 0 accidental, 2 survived` is recounted. However, `ClaimSkeleton/witness_recount.py:15` proves that this script re-evaluates `.ufo/evidence/kaika-round-1/witness/` (the historical **JS** `kimi-census` leg), not the bash leg. The bash witness study was never executed in inherited state.

### RC-3: Incomplete Snapshot Gate Artifacts in `ControlGate/` (`expected.json` Absent)
- **Citing Locations:**
  - `SKILL.md:1503`:
    > `Pinned values: .ufo/evidence/round-12/ControlGate/expected.json, mismatch/expected.json; literal expected IDs/exits in tool selftest`
  - `tools/repeat-control.py:50-62, 339-371, 737-743`:
    - Lines 50–52: `--snapshot DIR: read-only validation ... DIR holds expected.json (schema repeat-control-snapshot-v1...)`
    - Lines 60–62: `Committed snapshots live at .ufo/evidence/round-12/ControlGate/ (stable -> controls_match) and its mismatch/ subdirectory (controls_mismatch).`
    - Lines 737–743: `repeat-control.py --selftest` executes `snapshot_case("snapshot-committed-stable", root, "controls_match", 0)` and `snapshot_case("snapshot-committed-mismatch", os.path.join(root, "mismatch"), "controls_mismatch", 1)`.
  - `GateRegistryScribe/registry-row-draft.md:31`:
    > `| Pinned fixture | .ufo/evidence/round-12/ControlGate/expected.json (persisted by ControlGate) | spec.json item ControlGate, Target — ABSENT at observation time |`
  - `corpus/knowledge/repeated-control-precondition.md:66`:
    > `[O] The snapshot directories .ufo/evidence/round-12/ControlGate/ and .../mismatch/ hold bare run-<k>.{stdout,stderr,exit} files only. No expected.json exists anywhere under .ufo/evidence/round-12/ at this write (find . -name expected.json -> no hits), so no snapshot verdict is claimed here.`
- **Finding:** Neither `.ufo/evidence/round-12/ControlGate/` nor `.ufo/evidence/round-12/ControlGate/mismatch/` contains `expected.json`. Additionally, both directories lack `command.txt` and `finding.txt` (specified in `tools/repeat-control.py:25-27`). In this inherited state, running `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate` or `--selftest` fails with `TamperError: expected.json unreadable` (exit 2 `snapshot_tampered`).

### RC-4: Unexecuted ExitReview Case Runs (`run/` Directory Absent)
- **Citing Locations:**
  - `.ufo/evidence/round-12/ExitReview/cases/run-cases.sh:11-14`:
    ```bash
    OUT=$EV/run
    mkdir -p "$OUT"
    SUMMARY=$OUT/summary.tsv
    ```
  - `ExitReview.md:93-94, 98, 111`:
    > Lines 93–94: `Not written: no evidence directory created (.ufo/evidence/round-12/ExitReview/ not needed; no probes executed).`  
    > Line 111: `Verification gap unchanged: the gate is still absent from the tree; no observed IDs exist yet.`
- **Finding:** `.ufo/evidence/round-12/ExitReview/` contains only `cases/run-cases.sh` and `cases/seq.py`. The execution output directory `run/` was never created, and no observed output files (`gate.stdout`, `gate.stderr`, `gate.exit`, `summary.tsv`) exist.

### RC-5: Unexecuted Mutation Run on `tools/repeat-control.py` in `FailureOracle`
- **Citing Locations:**
  - `FailureOracle.md:3, 30`:
    > Line 3: `The actual tools/repeat-control.py check remains pending because the file was absent on the latest check.`  
    > Line 30: `The actual tools/repeat-control.py was absent on the latest check, so the required production-gate green-after result and a one-observation mutation of its isolated /tmp copy are not claimed.`
- **Finding:** In `.ufo/evidence/round-12/FailureOracle/`, the red-before counterexample was executed against an evidence-only model script (`single_control_baseline.py`). Although `actual-pristine/` contains a valid green run of `tools/repeat-control.py` against `fixture.sh`, no mutant of `tools/repeat-control.py` was ever constructed, executed, or persisted.

### RC-6: Unexercised TTY Escape Path in `GateSecurity`
- **Citing Locations:**
  - `GateSecurity.md:13, 93-94`:
    > `tty_probe.py / tty_probe.out: no result. No pty was available, so the tty path was not exercised.`
  - `.ufo/evidence/round-12/GateSecurity/tty_probe.out:5`:
    > `note: harness reported 'pty requested but unavailable'; no controlling tty, so P15 is NOT a test of the tty-escape path`
- **Finding:** Probe P15 in `GateSecurity` recorded zero evidence for TTY session handling because the execution harness did not provide a controlling terminal.

### RC-7: Unexecuted Gate Refusal Suite in `ControlThreats`
- **Citing Locations:**
  - `ControlThreats.md:18-20`:
    > `gate-probes.sh holds 23 refusal rows for the gate (R1–R12 plus the note R13). I have not run it against the gate because the gate is absent. Its only observed run is bash gate-probes.sh -> GATE_PROBES: SETUP (gate missing …) with exit 2.`
- **Finding:** `.ufo/evidence/round-12/ControlThreats/probes.out` contains output from `probes.py` (which probed Python stdlib / platform primitives). The 23 refusal rows authored in `gate-probes.sh` were never executed against `tools/repeat-control.py`.

### RC-8: Unexecuted Gate Verifications in Wave-1 Scribes
- **Citing Locations:**
  - `EvidenceScribe.md:25`: `repeat-control not on disk. tools/repeat-control.py absent at read time; all C1 rows are unobserved expectations (O).`
  - `EvidenceScribe/inventory.md:58-71`: Tables C1-1 through C1-9 are explicitly marked "Expected (contract, not observed)".
  - `ReportScribe.md:19-23, 96`: Lists repeat-control selftest, repeat-control controls_match/mismatch, snapshot verification, and bash witness study as "PENDING — absent at HEAD".

---

## 4. Temporary-Path-Only Links (`/tmp/...`)

`corpus/QUALITY.md` Criterion 9 states: *"Scratch stays in `/tmp`; evidence a claim rests on is copied into the repo (`.ufo/evidence/…`) before the commit that cites it. (MK-6)"*

The census identified multiple evidence sets that link directly to `/tmp/...` without copying the underlying artifacts into `.ufo/evidence/round-12/`:

### TP-1: `BytesReview/cli` Execution Arguments Point Exclusively to `/tmp`
In `.ufo/evidence/round-12/BytesReview/cli/`, 20 test cases were executed and logged. For 7 of those cases, `command.txt` records commands executing ephemeral scripts in `/tmp/bytesreview/`:
- `cli/C02-trailing-newline-alt/command.txt:7`:  
  `argv=["/bin/sh", "/tmp/bytesreview/cli-scripts/C02-trailing-newline-alt.sh"]`
- `cli/C04-empty-vs-newline/command.txt:7`:  
  `argv=["/bin/sh", "/tmp/bytesreview/cli-scripts/C04-empty-vs-newline.sh"]`
- `cli/C06-NUL-vs-joined/command.txt:7`:  
  `argv=["/bin/sh", "/tmp/bytesreview/cli-scripts/C06-NUL-vs-joined.sh"]`
- `cli/C07-stderr-only/command.txt:7`:  
  `argv=["/bin/sh", "/tmp/bytesreview/cli-scripts/C07-stderr-only.sh"]`
- `cli/C08-exit-0-0-1/command.txt:7`:  
  `argv=["/bin/sh", "/tmp/bytesreview/cli-scripts/C08-exit-0-0-1.sh"]`
- `cli/C15-non-executable-file/command.txt:7` & `run-{1..3}.stderr:1`:  
  `argv=["/tmp/bytesreview/noexec.txt"]`, `[Errno 13] Permission denied: '/tmp/bytesreview/noexec.txt'`
- `cli/C17-ENOEXEC-no-shebang/command.txt:7` & `run-{1..3}.stderr:1`:  
  `argv=["/tmp/bytesreview/noexec_nosheb.sh"]`, `[Errno 8] Exec format error: '/tmp/bytesreview/noexec_nosheb.sh'`
- **Author's Disclosure (`BytesReview.md:98`):**  
  > *"Probe scripts used `/tmp/bytesreview/` for scratch (fixtures noexec.txt, noexec_nosheb.sh, counter files); copies of the scripts are in the evidence directory except the counter scripts in `/tmp/bytesreview/cli-scripts/`."*
- **Impact:** The counter scripts (`C02`, `C04`, `C06`, `C07`, `C08`) and fixtures (`noexec.txt`, `noexec_nosheb.sh`) were left in `/tmp/bytesreview/`. Any reboot or scratch wipe renders `command.txt` un-reproducible.

### TP-2: `ControlKnowledge` Full Source Bodies Omitted from Repo
- **Evidence References:**
  - `.ufo/evidence/round-12/ControlKnowledge/README.md:8, 14`:  
    > `Per the wave's evidence rule, small located quotes only — the full fetched bodies are scratch (/tmp/tameshi-r12-ck/fetch/, not committed)... Commands, run 2026-10-20T02:13:47Z from /tmp/tameshi-r12-ck/fetch`
  - `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv:4`:  
    > `# Location = line number in the fetched body as served (full bodies are scratch under /tmp/tameshi-r12-ck/fetch/, not committed).`
- **Impact:** The raw fetched primary HTML files for S004 (`S004.html`, 29,579 B) and S026 (`S026.html`, 236,385 B) reside strictly in `/tmp/tameshi-r12-ck/fetch/`. The repo evidence holds only `quotes.tsv` and `README.md`.

### TP-3: `SourceSurvey` Primary PDF Omitted from Repo
- **Evidence References:**
  - `.ufo/evidence/round-12/SourceSurvey/evidence.json:7-8`:  
    > `"pdf_sha256": "deab832cf2d89d641193568952b47df5487dfbb833b1e62ca1d7c8cf4bed661f", "pdf_byte_size": 1807374`
- **Impact:** While `SourceFlakyPaper` committed `ISSTA2019.pdf` directly into `.ufo/evidence/round-12/SourceFlakyPaper/`, `SourceSurvey` left `2021a.pdf` in `/tmp/2021a.pdf` and committed only `S040-excerpt.txt` and metadata.

### TP-4: Pinned Source README Scratch Citations
- **Evidence References:**
  - `WitnessSourceReview.md:17, 61`:  
    > `Pinned README fetched independently from https://raw.githubusercontent.com/... into /tmp/s006-readme-pinned.md (scratch)... Scratch only: /tmp/s006-readme-pinned.md.`
- **Observation:** `SourceWitness` did commit `S006.md` into `.ufo/evidence/round-12/SourceWitness/`, but `WitnessSourceReview.md` bases its audit on an independent scratch copy in `/tmp`.

### TP-5: Pinned Target Blob Scratch Citations
- **Evidence References:**
  - `MinimalityReview.md:59` & `MinimalityReview/probes.md:3`:  
    > `Scratch copy of pinned kagi blob: /tmp/mr-surface-census.sh (outside repo, per QUALITY.md criterion 9)`
  - `WitnessThreats.md:11, 70, 80`:  
    > `W=/tmp/tameshi-r12-witnessthreats ... Scratch: /tmp/tameshi-r12-witnessthreats/.`
  - `AdmissionBounds.md:87, 104`:  
    > `Scratch: /tmp/tameshi-r12-AdmissionBounds-probe/.`
  - `SnapshotReview.md:108`:  
    > `Scratch dirs under /tmp/snapreview-*.`
  - `GateSecurity.md:10, 190`:  
    > `Evidence probes are hermetic fixtures under mktemp /tmp/tameshi-r12-gatesec.* ... Scratch left at /tmp/tameshi-r12-gatesec.3jjxrxn9.`

### TP-6: Stale Worktree Paths in Inherited Round-1 Evidence
- **Evidence Reference:**
  - `MinimalityReview/probes.md:35`:  
    > `P6 — stale evidence paths: .ufo/evidence/kaika-round-1/witness/README.md and declared.tsv cite .tower/worktrees/kaika/… pins; that path does not resolve on this host.`

---

## 5. Summary Matrix of Defects

| Finding ID | Class | Target Surface | Affected Files & Lines | Required Remediation / Action for L1 |
|---|---|---|---|---|
| **RC-1** | Missing Artifact | Precondition Verification Receipt | `SKILL.md:1482`, `corpus/README.md:127` | Produce and persist `.ufo/evidence/round-12/verification.json`, or remove the citation. |
| **RC-2** | Unexecuted Study | Bash Witness Attribution | `corpus/README.md:128`, `SKILL.md:1504`, `claims.json:7`, `measure.py:26` | Execute `tools/bash-witness-study.py run` (owned by `WitnessFinish`), generate and commit `declared.tsv`, `declaration.json`, `summary.json`, `manifest.json`, and run outputs. |
| **RC-3** | Incomplete Fixture | Snapshot Gate Fixture | `SKILL.md:1503`, `tools/repeat-control.py:50-62, 737-743`, `ControlGate/` | Author and commit `expected.json` (schema `repeat-control-snapshot-v1`) in `ControlGate/` and `ControlGate/mismatch/`. |
| **RC-4** | Missing Run Output | Repeat-Control Exit Cases | `.ufo/evidence/round-12/ExitReview/cases/run-cases.sh:11` | Either run `run-cases.sh` to capture `run/` outputs or document as fixture-only. |
| **RC-5** | Unexecuted Mutation | Gate Mutation Verification | `FailureOracle.md:30`, `.ufo/evidence/round-12/FailureOracle/` | Record clearly that only the model was subjected to red-before mutation, not `tools/repeat-control.py`. |
| **RC-6** | Inconclusive Probe | TTY Escape Boundary | `GateSecurity.md:13`, `GateSecurity/tty_probe.out:5` | Document P15 as inconclusive due to headless environment. |
| **RC-7** | Unexecuted Probes | Gate Refusal Verification | `ControlThreats.md:18`, `ControlThreats/gate-probes.sh` | Disclose that `gate-probes.sh` was authored against the contract prior to gate availability. |
| **RC-8** | Unexecuted Gates | Gate Status in Scribe Reports | `EvidenceScribe.md:25`, `ReportScribe.md:19-23` | Replace PENDING rows with actual execution receipts once L1 lands integration runs. |
| **TP-1** | Ephemeral Link | Command Invocation Scripts | `BytesReview/cli/C02,C04,C06,C07,C08,C15,C17/command.txt:7` | Copy `cli-scripts/` and fixtures from `/tmp/bytesreview/` into `.ufo/evidence/round-12/BytesReview/`. |
| **TP-2** | Ephemeral Source | Source Body Retention | `ControlKnowledge/README.md:8`, `quotes.tsv:4` | Acknowledge that full bodies are retained only as online URLs + hashes, or copy HTML into evidence. |
| **TP-3** | Ephemeral Source | Survey PDF Retention | `SourceSurvey/evidence.json:7-8` | Copy `/tmp/2021a.pdf` into `.ufo/evidence/round-12/SourceSurvey/` to mirror `SourceFlakyPaper`. |
| **TP-6** | Dead Path | Historical Worktree Citation | `kaika-round-1/witness/README.md`, `MinimalityReview/probes.md:35` | Preserve as historical errata; do not reuse `.tower/worktrees/kaika` paths in new citations. |

---

## 6. Verification Checks for Main / L1 Integrator

The following concrete verification commands should be evaluated by the L1 integrator:
1. `test -f /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/verification.json || echo "RC-1 CONFIRMED: verification.json is absent"`
2. `test -f /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/BashWitness/summary.json || echo "RC-2 CONFIRMED: BashWitness/summary.json is absent"`
3. `test -f /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/ControlGate/expected.json || echo "RC-3 CONFIRMED: ControlGate/expected.json is absent"`
4. `grep -rn '/tmp/bytesreview' /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/BytesReview/cli/`
5. `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/measure.py` (verify `"bash_witness_summary": {}`).
