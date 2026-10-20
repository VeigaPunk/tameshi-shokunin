# SurfacePin — Read-Only Reconnaissance for Recorded `bash-surface-census`

**Seat:** `TameshiR13.SurfacePin` (Scout, leaf)  
**Round:** Tameshi Round 13, Wave 1  
**Target:** `bash-surface-census` (`kagi-shokunin/corpus/surface-census.sh`)  
**Scope:** Read-only git show, object-database inspection, and hashlib evaluation. No sibling code executed. No test/build/lint runs.  
**Report Destination:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-13/w1/SurfacePin.md`  
**Tooling Directive:** No tools installed or updated.

---

## 1. Axes (Godspeed Posture)

- **Calibration ($C_1$):** Establish ground truth for pin coordinates without conflating commit SHAs, git blob object IDs, and full SHA-256 file hashes. Prevent false confidence by strictly withholding inferred live kill rates from static byte matches.
- **Depth ($C_2$):** Expose dependency and context blindness (sibling data tables, subshell self-invocation, external tools like `sqlite3`/`the-janitor`, environment variables) to substantiate the F7 doctrine that byte identity does not equal safe result reuse.

---

## 2. Pinned Target Identity & Runner References

In the canonical regression runner (`tools/mutate-and-run.sh`) and repository records:
- **Runner Pin Declaration:**
  - `tools/mutate-and-run.sh:544-545`:
    ```bash
    PIN_BASH=275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f
    REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e
    ```
  - `tools/mutate-and-run.sh:555`:
    ```bash
    TABLE_BASH='B1:KILLED,B2:KILLED,B3:KILLED,B4:KILLED,B5:SURVIVED,B6:KILLED,B7:KILLED,B8:KILLED,B9:KILLED,B10:SURVIVED'
    ```
  - `tools/mutate-and-run.sh:85`: Header catalog `# bash-surface-census kagi-shokunin/corpus/surface-census.sh 8/10 (80 %)`
  - `tools/mutate-and-run.sh:630-670`: Embedded defect spec `bash-surface-census.spec` heredoc (10 defects B1–B10)
  - `tools/mutate-and-run.sh:1117-1120`: Invocation invocation arm:
    ```bash
    regression_case_git bash-surface-census \
      'kagi-shokunin/corpus/surface-census.sh' "$PIN_BASH" "$REV_BASH" \
      "$specs/bash-surface-census.spec" 'bash "$MUTANT" --selftest' "$TABLE_BASH" \
      "$root/bash-surface-census"
    ```
  - `tools/mutate-and-run.sh:1579`: Sweep configuration entry `bash-surface-census:bash-surface-census.spec:TABLE_BASH:10:8`
- **Corpus & Registry References:**
  - `corpus/SOURCES.md:44` (Row S033): `kagi corpus/surface-census.sh (fleet gate, read-only) — kagi-shokunin/corpus/surface-census.sh | code | A | the gate's own behavior at the measured revision | kagi-shokunin/corpus/surface-census.sh @ fecee8743e52eb8fb5fbb40782934cb619a1a96e (blob sha256 275d8294…3009f)`
  - `corpus/PROVINCE.md:31-33`: Identified as core primary surface.
  - `corpus/knowledge/mutation-case-kagi-census.md`: Reproduce manifest and defect analysis.
  - `corpus/knowledge/fleet-kill-rate-ledger.md:346`: `bash-surface-census | fecee874… | 275d8294… | 8/10 (80 %) | match=10/10 … flips=0 | PASS`
  - `tools/bash-witness-study.py:99,105,199`: Round-12 study tool analyzing `bash-surface-census.spec`.

---

## 3. Grounded Hash & Git Facts

All observations derived strictly via read-only git queries and hashlib:

| Dimension | Pinned / Original Fact | Current Committed Fact (HEAD) | Current Working Tree Fact | Status |
|---|---|---|---|---|
| **Repository Path** | `/home/vgpnk/Projects/shokunin/kagi-shokunin` | `/home/vgpnk/Projects/shokunin/kagi-shokunin` | `/home/vgpnk/Projects/shokunin/kagi-shokunin` | Matched |
| **Relative Path** | `corpus/surface-census.sh` | `corpus/surface-census.sh` | `corpus/surface-census.sh` | Matched |
| **Commit SHA** | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `c2cab35bc92e57e39e5489bac3386db078345b3f` | — (uncommitted worktree) | HEAD advanced |
| **Git Blob Object SHA-1** | `dcf878b95e172253a282adf2dc2cc9e8dd8c0d7c` | `dcf878b95e172253a282adf2dc2cc9e8dd8c0d7c` | `dcf878b95e172253a282adf2dc2cc9e8dd8c0d7c` | Exact Match |
| **File Content SHA-256** | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` | Exact Match |
| **File Mode** | `100755` | `100755` | `0755` (`-rwxr-xr-x`) | Executable intact |
| **Byte Size** | 44,212 bytes (887 lines) | 44,212 bytes (887 lines) | 44,212 bytes (887 lines) | Exact Match |
| **Dirty Status (Target)** | Clean | Clean (`git diff fecee874..HEAD` empty) | Clean (`git status --porcelain` empty) | **Clean** |
| **Original Bytes Availability** | **Available** | **Available** | **Available** | Preserved |

### Key Observations
1. **Target Unchanged Despite HEAD Advance:** While `kagi-shokunin` repo HEAD moved from `fecee8743e52eb8fb5fbb40782934cb619a1a96e` to `c2cab35bc92e57e39e5489bac3386db078345b3f` across subsequent documentation and integration rounds, `git log -1 corpus/surface-census.sh` confirms that `fecee8743e52eb8fb5fbb40782934cb619a1a96e` was the last commit to modify `corpus/surface-census.sh`.
2. **Byte Equivalence:** The git blob object SHA (`dcf878b95e172253a282adf2dc2cc9e8dd8c0d7c`) and file SHA-256 (`275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`) at `fecee874`, at HEAD `c2cab35b`, and in the current working tree are identical.
3. **Availability:** Original bytes remain fully available in the local git repository object database and in the working tree.

---

## 4. No Inferred Live Rate (F7 Discipline)

- **Prior Recorded Verdict:** 8/10 (80%) killed (`B1:KILLED, B2:KILLED, B3:KILLED, B4:KILLED, B5:SURVIVED, B6:KILLED, B7:KILLED, B8:KILLED, B9:KILLED, B10:SURVIVED`).
- **Live Rate Claim:** **None**. In strict compliance with F7 discipline, Admission Rules 11 and 12, and S041 (PIT Incremental Analysis), identical content does **not** establish safe result reuse:
  - Byte identity verifies only that the source file text matches the prior baseline.
  - Reusing prior execution outcomes or asserting that the live gate kill rate remains 80% without re-running the sweep under the active execution environment is an ungrounded inference.
  - In all manifest models and disposition tables, `result_reuse` must be recorded as `not_established`.

---

## 5. Dependency & Context Blindness

Treating `corpus/surface-census.sh` as an isolated hash pin is subject to significant context blindness:

1. **Sibling Data Tables:**
   - In default `verify` mode, `surface-census.sh:76-78` loads:
     - `CENSUS="$SCRIPT_DIR/surface-census.tsv"`
     - `SHAPES="$SCRIPT_DIR/state-shape.tsv"`
     - `BASELINE="$SCRIPT_DIR/drift-baseline.tsv"`
   - These TSV tables define the declared surfaces, shape floors, and baseline permissions. Sibling table changes alter census behavior without altering `surface-census.sh`'s digest. (A git check reveals zero diff between `fecee874` and HEAD on these three files as well, but a runner probing only `surface-census.sh` is blind to them).
2. **Subshell Self-Invocation:**
   - The `--selftest` function invokes the script recursively via subshells (`bash "${BASH_SOURCE[0]}" verify ...` at line 762, and `bash "${BASH_SOURCE[0]}" --verbs ...` at lines 826 and 834).
   - This requires execution as a concrete filesystem file path (piping via standard input breaks `$BASH_SOURCE[0]`).
3. **Host Tooling & Substrate Dependencies:**
   - `sqlite3`: `sqlite_probe()` (line 268) and selftest cases 10–12 (`surface-census.sh:710,788,790`) require `sqlite3`. If missing, the gate enters `sqlite-unavailable` (exit 1 UNVERIFIED).
   - `python3`: Selftest case 14 (`surface-census.sh:796`) executes an inline Python 3 script to construct a fused-row failure. If `python3` is missing or altered, case 14 fails.
   - `the-janitor` (`$THE_JANITOR_BIN`): In `--selftest` (lines 817–845), cases 15 and 16 conditionally execute the live handler binary if present on `PATH`. If absent, they emit `skip-case ... substrate-absent`. Host installation or removal of this binary changes the executed test path.
   - `tmux`: Status verification (probe 9, line 686) runs `tmux has-session -t janitor 2>/dev/null`.
   - Core POSIX tools: `find`, `sort`, `mktemp`, `sed`, `awk`, `grep`, `head`, `cmp`, `chmod`.
4. **Environment Variables:**
   - The script branches on `CENSUS_BREAK`, `SQLITE3_BIN`, `THE_JANITOR_BIN`, `THE_JANITOR_ENV`, `THE_JANITOR_STATE_DIR`, `TMPDIR`, `HOME`, and `DEEP`. None of these variables are bound by hashing `surface-census.sh`.

---

## 6. Coordination with `PinProbe`

Delivered coordination message to `agent://TameshiR13.PinProbe` confirming:
- Leg ID: `bash-surface-census`
- Repository: `kagi-shokunin`
- Relative Path: `corpus/surface-census.sh`
- Pinned Revision: `fecee8743e52eb8fb5fbb40782934cb619a1a96e`
- Pinned SHA-256: `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`
- Pinned Git Blob SHA: `dcf878b95e172253a282adf2dc2cc9e8dd8c0d7c`
- Mode: `100755`
- Current HEAD Revision: `c2cab35bc92e57e39e5489bac3386db078345b3f`
- Current HEAD Blob SHA: `dcf878b95e172253a282adf2dc2cc9e8dd8c0d7c`
- Worktree SHA-256: `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`
- Content Status: `unchanged`
- Result Reuse: `not_established`

---

## 7. Exact Checks L1 Should Run (Not Run Here)

1. **Verify Pinned File Hash:**
   ```bash
   sha256sum /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh
   # Expected: 275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f  ...
   ```
2. **Verify HEAD and Historical Blob Object Identity:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh
   git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse HEAD:corpus/surface-census.sh
   # Expected: Both return dcf878b95e172253a282adf2dc2cc9e8dd8c0d7c
   ```
3. **Verify Zero Target Diff:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kagi-shokunin diff fecee8743e52eb8fb5fbb40782934cb619a1a96e..HEAD -- corpus/surface-census.sh
   # Expected: Empty output (exit code 0)
   ```
4. **Verify Clean Target Worktree Status:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kagi-shokunin status --porcelain corpus/surface-census.sh
   # Expected: Empty output (exit code 0)
   ```
5. **Verify New Pin-Disposition Tool Output for Leg:**
   ```bash
   python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py \
     --manifest /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json \
     --root /home/vgpnk/Projects/shokunin
   # Expected: Row for bash-surface-census reports:
   #   content_status == "unchanged"
   #   result_reuse == "not_established"
   ```
