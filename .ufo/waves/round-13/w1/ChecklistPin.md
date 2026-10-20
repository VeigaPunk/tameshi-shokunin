# Reconnaissance Report: `bash-checklist-run` Pin & Current State (Round 13 — Scout ChecklistPin)

## 1. Axes & Posture (Godspeed)

- **Axes:**
  - **Depth ($C_1$):** Grounding the recorded `bash-checklist-run` leg to verifiable git blob and tree digests, establishing concrete current-content disposition rather than assuming static persistence.
  - **Calibration ($C_2$):** Separating immutable historical observations from current substrate reality; eliminating result-reuse assumptions and forbidding ungrounded live kill-rate projections.
- **Posture:** Iterate cheap, collect read-only git and hashlib facts in parallel, modify no sibling files, perform no test/build/lint executions, leaf restraint.

---

## 2. Runner Pins & Spec References in `tameshi-shokunin`

The leg `bash-checklist-run` is anchored across canonical references in `tameshi-shokunin`:

1. **Mutation Runner (`tools/mutate-and-run.sh`):**
   - **Target relative path (`:1133`):** `kagi-shokunin/corpus/checklist-run.sh`
   - **Pinned commit (`:551`):** `REV_CHECKLIST=fecee8743e52eb8fb5fbb40782934cb619a1a96e`
   - **Pinned blob SHA256 (`:550`):** `PIN_CHECKLIST=7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf`
   - **Recorded decision table (`:558`):**
     `TABLE_CHECKLIST='A1:SURVIVED,A2:KILLED,B1:SURVIVED,B2:KILLED,B3:SURVIVED,B4:KILLED,C1:SURVIVED,C2:KILLED,D1:SURVIVED,D2:KILLED,E1:KILLED,E2:SURVIVED,F1:KILLED,F2:SURVIVED,G1:SURVIVED'`
   - **Defect spec (`:770-891`):** Embedded generator writes `bash-checklist-run.spec` with 15 single-defect replacements (`A1`–`G1`) pre-registered across seven clauses (`A`–`G`), yielding 7 killed and 8 survived.
   - **Regression invocation (`:1132-1135`):**
     Invokes `regression_case_git` materializing `$PIN_CHECKLIST` from `$REV_CHECKLIST` via `git show`, mirroring mode `100755` (`:940-955`), running `bash "$MUTANT" --selftest`.
   - **Selftest mapping (`:1582`):** Embedded mapping `bash-checklist-run:bash-checklist-run.spec:TABLE_CHECKLIST:15:7` (7/15 killed = 47%).

2. **Source Registry (`corpus/SOURCES.md:47`):**
   - **Row S036:** Tier A code source; `kagi `corpus/checklist-run.sh` (fleet gate, read-only) — kagi-shokunin/corpus/checklist-run.sh @ fecee8743e52eb8fb5fbb40782934cb619a1a96e (blob sha256 7e5ec98b…76bf)`.

3. **Knowledge Ledger & Case Studies:**
   - `corpus/knowledge/mutation-case-kagi-checklist.md`: Documents round-8 T8-1 sweep on the 506-line (24,697 B) revision with mode 755; notes hermetic selftest over 34 cases building temporary fixtures.
   - `corpus/knowledge/fleet-kill-rate-ledger.md:276`: Records `bash-checklist-run` at `fecee874…` / `7e5ec98b…` as 7/15 (47%).

---

## 3. Substrate State: Git & Worktree Facts

Read-only inspection of `/home/vgpnk/Projects/shokunin/kagi-shokunin` reveals the following grounded facts:

| Dimension | Pinned / Original State | Current Substrate State |
|---|---|---|
| **Repository Path** | `/home/vgpnk/Projects/shokunin/kagi-shokunin` | `/home/vgpnk/Projects/shokunin/kagi-shokunin` |
| **File Path** | `corpus/checklist-run.sh` | `corpus/checklist-run.sh` |
| **Git Commit SHA** | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `c2cab35bc92e57e39e5489bac3386db078345b3f` |
| **Commit Subject** | `round-18: OMP/ufo-fsd re-census ...` | `Integrate remote documentation; preserve local round log` |
| **Commit Distance** | Baseline anchor | 18 commits ahead of `fecee874` |
| **Git Blob Object ID** | `78f2c45eed31ee00b01611556affa86a8db9c098` | `78f2c45eed31ee00b01611556affa86a8db9c098` |
| **Committed SHA256** | `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` | `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` |
| **Worktree SHA256** | N/A (historical) | `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` |
| **Target Git Status** | N/A | **clean** (`git status --porcelain corpus/checklist-run.sh` is empty) |
| **Target Diff vs HEAD** | N/A | 0 bytes (`git diff HEAD -- corpus/checklist-run.sh` empty) |
| **Target Diff vs Pin Rev**| N/A | 0 bytes (`git diff fecee874 c2cab35b -- corpus/checklist-run.sh` empty) |
| **Repo Dirty Status** | N/A | **clean** (`git status --short` is empty across entire repo) |
| **Line Count** | 506 lines | 506 lines (identical) |
| **Byte Size** | 24,697 bytes | 24,697 bytes (identical) |
| **Git File Mode** | `100755` (`-rwxr-xr-x`) | `100755` (`-rwxr-xr-x`) (identical) |
| **Original Availability**| **YES** (retrievable from git object store) | N/A |
| **Content Disposition** | N/A | **unchanged** (`7e5ec98b…` $==$ `7e5ec98b…`) |
| **Commit Disposition** | N/A | **moved** (HEAD is 18 commits ahead, but target file unchanged) |

---

## 4. No Inferred Live Rate

- **Finding:** No live kill rate is inferred for `bash-checklist-run`.
- **Grounding:**
  - Even though the content of `corpus/checklist-run.sh` is byte-identical (`7e5ec98b…`), F7 rules and Round 13 acceptance establish that: **`result_reuse=not_established` always**. Identical content is not safe result reuse.
  - The historical 7/15 (47%) kill rate was measured during round 8 under specific execution conditions.
  - Asserting or projecting a live 47% kill rate without executing an authorized, calibrated regression sweep would constitute an ungrounded attribution and result-reuse fallacy (violating QUALITY Criterion 12).

---

## 5. Dependency & Context Blindness Analysis

Treating `bash-checklist-run` purely as an isolated file-path pin introduces five distinct dimensions of context blindness:

1. **Selftest Synthetic Fixture Blindness vs. Live Execution Context:**
   - The regression harness runs `bash "$MUTANT" --selftest`.
   - In `--selftest` mode (`checklist-run.sh:340-430`), the script creates an isolated temporary directory with a synthetic 6-item `SKILL.md` section and a synthetic 6-row `checklist.tsv`. It exercises 34 hermetic policy test cases.
   - It **never** reads or tests the production 16-row `corpus/checklist.tsv` or the actual repo `SKILL.md`.
   - Consequently, mutation testing of the selftest suite proves only that the internal policy validator catches synthetic violations; it does not measure or prove live credential-hygiene verification of the repository.
2. **Declaration & Specification Context Drift:**
   - In production mode (default verify), `checklist-run.sh` loads `corpus/checklist.tsv` and `SKILL.md`.
   - While `corpus/checklist.tsv` and the `## Credential-hygiene checklist` section of `SKILL.md` remain unchanged, `SKILL.md` as a whole underwent a 4,909-byte diff across 18 commits between `fecee874` and `c2cab35b`.
   - Blindness to sibling repository context would miss parser interactions or section-boundary shifts if header formatting were touched.
3. **Delegated Gate & Substrate Blindness:**
   - Rows in `checklist.tsv` execute commands in `ROOT` (`/home/vgpnk/Projects/shokunin/kagi-shokunin`), delegating several credential checks to sibling scripts in `corpus/` (e.g. `surface-census.sh`, `op-ref-probe.sh`, `claim-ledger.sh`).
   - Multiple sibling scripts in `kagi-shokunin/corpus/` were modified across the 18 commits between `fecee874` and `c2cab35b` (such as `op-ref-probe.sh` and `sources-census.sh`).
   - A live execution of `checklist-run.sh` depends directly on these delegated scripts; pinning `checklist-run.sh` alone ignores changes in its transitive execution graph.
4. **Executable Mode (`100755`) Invariant Blindness:**
   - `checklist-run.sh` contains `SELF="$SCRIPT_DIR/$(basename -- "${BASH_SOURCE[0]}")"` and re-invokes `"$SELF"` during selftest runs (`:416`).
   - Materializing the file via `git show` without restoring the `100755` executable bit causes selftest failure (permission denied), as documented in the Round 12 ControlThreats probe construction incident.
   - The pin check must verify both file bytes and mode preservation.
5. **Host Environment & Shell Toolchain Invariants:**
   - The script relies on Bash built-in extended regular expressions (`=~`), arithmetic evaluation `((...))`, and external utilities (`mktemp`, `sed`, `awk`, `grep -E`).
   - Environmental changes (e.g., changes in Bash version or tool flags) represent unpinned dependencies outside the single file hash.

---

## 6. Coordination with Peer Seats

- Communicated pin coordinates to `TameshiR13.PinProbe` via peer channel (`agent://TameshiR13.PinProbe`):
  - Confirmed pinned repo `kagi-shokunin`, path `corpus/checklist-run.sh`, commit `fecee8743e52eb8fb5fbb40782934cb619a1a96e`, SHA256 `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf`, mode `100755`.
  - Confirmed live HEAD `c2cab35bc92e57e39e5489bac3386db078345b3f` (18 commits ahead), committed and worktree SHA256 `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf`.
  - Confirmed target file clean in worktree, original bytes retrievable, content status `unchanged`, commit status `moved`, `result_reuse=not_established`.

---

## 7. Checks for L1 Verification (Unexecuted)

L1 should run the following non-destructive verification commands during integration:

1. **Verify Pinned Blob Availability & Digest:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kagi-shokunin cat-file -p fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh | sha256sum
   # Expected: 7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf  -
   ```

2. **Verify Current Committed & Worktree Blob Digest:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kagi-shokunin cat-file -p HEAD:corpus/checklist-run.sh | sha256sum
   sha256sum /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh
   # Expected: both print 7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf
   ```

3. **Verify Target Cleanliness & Diff:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kagi-shokunin status --porcelain corpus/checklist-run.sh
   git -C /home/vgpnk/Projects/shokunin/kagi-shokunin diff fecee8743e52eb8fb5fbb40782934cb619a1a96e HEAD -- corpus/checklist-run.sh
   # Expected: both commands produce empty output
   ```

4. **Verify Executable Mode:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kagi-shokunin ls-tree HEAD corpus/checklist-run.sh | awk '{print $1}'
   # Expected: 100755
   ```

5. **Verify `pin-disposition.py` Output (Once Landed):**
   ```bash
   python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py \
     --manifest /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json \
     --root /home/vgpnk/Projects/shokunin
   # Expected: row for bash-checklist-run shows status="unchanged", result_reuse="not_established"
   ```

---

## 8. Tooling Record

No tools installed or upgraded. Read-only git (`rev-parse`, `ls-tree`, `cat-file`, `status`, `diff`, `log`) and standard python3 hashlib commands only.
