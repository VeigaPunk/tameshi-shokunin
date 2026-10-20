# Reconnaissance Report: `bash-tsukuroi-census` Pin & Current State (Round 13 — Scout TsukuroiPin)

## 1. Axes & Posture (Godspeed)

- **Axes:**
  - **Depth ($C_1$):** Grounding the recorded `bash-tsukuroi-census` leg to verifiable git blob and tree digests, establishing concrete current-content disposition rather than assuming static persistence.
  - **Calibration ($C_2$):** Separating immutable historical observations from current substrate reality; eliminating result-reuse assumptions and forbidding ungrounded live kill-rate projections.
- **Posture:** Iterate cheap, collect read-only git and hashlib facts in parallel, modify no sibling files, perform no test/build/lint executions.

---

## 2. Runner Pins & Spec References in `tameshi-shokunin`

The leg `bash-tsukuroi-census` is anchored across canonical references in `tameshi-shokunin`:

1. **Mutation Runner (`tools/mutate-and-run.sh`):**
   - **Target relative path (`:1123`):** `tsukuroi-shokunin/tools/tsukuroi-census.sh`
   - **Pinned commit (`:547`):** `REV_TSUKUROI=165307fe4746a8807b02ec4a7d7ecac0368454a6`
   - **Pinned blob SHA256 (`:546`):** `PIN_TSUKUROI=084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5`
   - **Recorded decision table (`:556`):**
     `TABLE_TSUKUROI='B1:KILLED,B2:KILLED,B3:KILLED,B4:KILLED,B5:KILLED,B6:KILLED,B7:SURVIVED,B8:SURVIVED,B9:SURVIVED,B10:SURVIVED'`
   - **Defect spec (`:675-715`):** Embedded generator writes `bash-tsukuroi-census.spec` with 10 single-defect replacements (`B1`–`B10`) tailored to lines and patterns of the pinned blob.
   - **Regression invocation (`:1122-1125`):**
     Invokes `regression_case_git` materializing `$PIN_TSUKUROI` from `$REV_TSUKUROI` via `git show`, running `bash "$MUTANT" --selftest`.
   - **Selftest mapping (`:1580`):** Embedded mapping `bash-tsukuroi-census:bash-tsukuroi-census.spec:TABLE_TSUKUROI:10:6` (6/10 killed = 60%).

2. **Source Registry (`corpus/SOURCES.md:45`):**
   - **Row S034:** Tier A code source; `tsukuroi-shokunin/tools/tsukuroi-census.sh @ 165307fe4746a8807b02ec4a7d7ecac0368454a6 (blob sha256 084951be…c78c5)`.

3. **Knowledge Ledger & Case Studies:**
   - `corpus/knowledge/mutation-case-tsukuroi-census.md`: Documents round-5 T5-1 sweep on the 976-newline (44,947 B) revision; notes incident I1 (substrate moved mid-run to `aae45531…`, adding selftests).
   - `corpus/knowledge/fleet-kill-rate-ledger.md:347`: Records `bash-tsukuroi-census` at `165307fe…` / `084951be…` as 6/10 (60%).

---

## 3. Substrate State: Git & Worktree Facts

Read-only inspection of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` reveals the following grounded facts:

| Dimension | Pinned / Original State | Current Substrate State |
|---|---|---|
| **Repository Path** | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` |
| **File Path** | `tools/tsukuroi-census.sh` | `tools/tsukuroi-census.sh` |
| **Git Commit SHA** | `165307fe4746a8807b02ec4a7d7ecac0368454a6` | `9574a189a758251da5957eee8ff0f38ba2d03c7f` |
| **Commit Subject** | `probation round 4 (training r3): see LOG ...` | `round-12 verifier spot-check (integrator, hyaku) ...` |
| **Commit Distance** | Baseline anchor | 22 commits ahead of `165307fe` |
| **Git Blob Object ID** | `dfcf6f596fab2437c69fde6c0067606761af4106` | `4610af7b3450ee3d3158590fb7a3300d0a86bee0` |
| **Committed SHA256** | `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5` | `d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e` |
| **Worktree SHA256** | N/A (historical) | `d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e` |
| **Target Dirty Status** | N/A | **clean** (`git status --porcelain tools/tsukuroi-census.sh` is empty) |
| **Line Count** | 976 newlines (977 lines) | 2,679 lines (+1,702 lines) |
| **Byte Size** | 44,947 bytes | 145,062 bytes (+100,115 bytes) |
| **Original Availability**| **YES** (retrievable from git object store) | N/A |
| **Content Disposition** | N/A | **changed** (`084951be…` $\ne$ `d17d32a3…`) |

---

## 4. No Inferred Live Rate

- **Finding:** No live kill rate is inferred for `bash-tsukuroi-census`.
- **Grounding:**
  - The live substrate file has grown from 976 lines to 2,679 lines (over $3.2\times$ byte expansion).
  - Under F7 rules and Round 13 acceptance: **`result_reuse=not_established` always**.
  - Pinned defect table `B1`–`B10` cannot be assumed to yield 6/10 on the current file; projecting a 60% kill rate (or any other scalar) onto the current substrate without executing an authorized, calibrated sweep would constitute an ungrounded attribution mistake.

---

## 5. Dependency & Context Blindness Analysis

Treating `bash-tsukuroi-census` purely as an isolated file-path pin introduces specific blindness dimensions:

1. **Architectural & Semantic Expansion Blindness:**
   - The pinned version was a 4-plane census (`packages`, `systemd`, `drivers`, `journal-boot`).
   - The current HEAD version is a 6-plane census (`packages` [with root metadata arm], `systemd-user`, `drivers` [with memory pressure arm], `journal-boot`, `update-safety`, `oom` [kill-event watch]).
   - The rollup logic, failure arms, and status reporting have expanded significantly.
2. **Defect Spec Anchor Invalidation:**
   - The embedded defect spec `bash-tsukuroi-census.spec` in `mutate-and-run.sh` hardcodes line numbers (e.g., `:473`, `:281`, `:434-452`, `:578`, `:615`, `:210`, `:160`, `:935`, `:967`, `:487-493`).
   - On the 2,679-line HEAD file, line indices have shifted by hundreds or thousands of lines. Defects targeting old line locations or replaced syntax will fail uniqueness checks or mutate unintended blocks.
3. **Execution Environment & Host Blindness:**
   - In live mode, `tsukuroi-census.sh` probes host tooling (`pacman`, `systemctl`, `journalctl`, `dmesg`, `lspci`, `nvidia-smi`, `smartctl`), reading kernel logs and systemd user sessions.
   - In `--selftest` mode, it constructs an unprivileged mock tree with stub dispatchers in `/tmp/tsukuroi-r3-2-selftest.XXXXXX`.
   - The selftest case suite has expanded substantially beyond the original 26 cases.
4. **Safe Reuse Fallacy:**
   - Even if worktree content were identical to the pin (which it is not), executing a script across rounds without verifying environmental, shell (`bash 5.3.15`), and dependent tool invariants makes result reuse invalid without explicit re-verification.

---

## 6. Coordination with Peer Seats

- Communicated pin coordinates to `TameshiR13.PinProbe` via peer channel (`agent://TameshiR13.PinProbe`):
  - Confirmed pinned repo `tsukuroi-shokunin`, path `tools/tsukuroi-census.sh`, commit `165307fe4746a8807b02ec4a7d7ecac0368454a6`, SHA256 `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5`.
  - Confirmed live HEAD `9574a189a758251da5957eee8ff0f38ba2d03c7f`, committed/worktree SHA256 `d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e`.
  - Confirmed target file clean in worktree, original bytes retrievable, content changed vs pin, `result_reuse=not_established`.

---

## 7. Checks for L1 Verification (Unexecuted)

L1 should run the following non-destructive verification commands during integration:

1. **Verify Pinned Blob Availability & Digest:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -p 165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh | sha256sum
   # Expected: 084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5  -
   ```

2. **Verify Current Committed & Worktree Blob Digest:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -p HEAD:tools/tsukuroi-census.sh | sha256sum
   sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh
   # Expected: both print d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e
   ```

3. **Verify Target Cleanliness in Worktree:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain tools/tsukuroi-census.sh
   # Expected: empty output (clean)
   ```

4. **Verify `pin-disposition.py` Row Generation (Once Landed):**
   ```bash
   python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py \
     --manifest /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json \
     --root /home/vgpnk/Projects/shokunin
   # Expected: row for bash-tsukuroi-census shows status="changed", result_reuse="not_established"
   ```
