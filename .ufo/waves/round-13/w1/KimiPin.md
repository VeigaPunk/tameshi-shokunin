# Reconnaissance Report: `js-kimi-census` Pin & Current State (Round 13 — Scout KimiPin)

## 1. Axes & Posture (Godspeed)

- **Axes:**
  - **Depth ($C_1$):** Grounding the recorded `js-kimi-census` leg to verifiable git blob and tree digests, establishing concrete current-content disposition rather than assuming static persistence.
  - **Calibration ($C_2$):** Separating immutable historical observations from current substrate reality; eliminating result-reuse assumptions and forbidding ungrounded live kill-rate projections.
- **Posture:** Iterate cheap, collect read-only git and hashlib facts in parallel, modify no sibling files, perform no test/build/lint executions.

---

## 2. Runner Pins & Spec References in `tameshi-shokunin`

The leg `js-kimi-census` is anchored across canonical references in `tameshi-shokunin`:

1. **Mutation Runner (`tools/mutate-and-run.sh`):**
   - **Target relative path (`:1113`):** `kumitate-shokunin/scripts/kimi-census.mjs`
   - **Pinned commit (`:543`):** `REV_JS=175de6ba2e9e904010411b19cab27e0af9aad3d4`
   - **Pinned blob SHA256 (`:542`):** `PIN_JS=83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`
   - **Recorded decision table (`:555`):**
     `TABLE_JS='D1:KILLED,D2:SURVIVED,D3:KILLED,D4:KILLED,D5:KILLED,D6:KILLED,D7:KILLED,D8:KILLED,D9:KILLED,D10:SURVIVED'`
   - **Defect spec (`:589-629`):** Embedded generator writes `js-kimi-census.spec` with 10 single-defect replacements (`D1`–`D10`) tailored to lines and patterns of the pinned blob:
     - `D1` (:105): `counted: 18` $\to$ `17`
     - `D2` (:378): `findings.slice(0, 6)` $\to$ `slice(0, 5)`
     - `D3` (:332): `!e.children.includes(n)` $\to$ `e.children.includes(n)`
     - `D4` (:351-353): delete root stray reporting loop
     - `D5` (:255): `gens.length > 0` $\to$ `true`
     - `D6` (:124): `0o600` $\to$ `0o644`
     - `D7` (:306): `(mode & floor) !== floor` $\to$ `=== 0`
     - `D8` (:396): `return 2` $\to$ `return 1`
     - `D9` (:292): `isLeaf(kind)` $\to$ `kind === 'file'`
     - `D10` (:145): `FROZEN = { K1: 3, K2: 25, ... }` $\to$ `K2: 24`
   - **Regression invocation (`:1112-1116`):**
     Invokes `regression_case_git` materializing `$PIN_JS` from `$REV_JS` via `git show`, running `node "$MUTANT" --selftest`.
   - **Selftest mapping (`:1580`):** Embedded mapping `js-kimi-census:js-kimi-census.spec:TABLE_JS:10:8` (8/10 killed = 80%).

2. **Source Registry (`corpus/SOURCES.md:43`):**
   - **Row S032:** Tier A code source; `kumitate-shokunin/scripts/kimi-census.mjs @ 175de6ba2e9e904010411b19cab27e0af9aad3d4 (blob sha256 83016d45…4f426)`. Pinned artifact behind the lane's first recorded kill rate (8/10).

3. **Knowledge Ledger & Case Studies:**
   - `corpus/knowledge/mutation-case-kimi-census.md`: Documents round-2 T2-1 sweep on the 896-line (43,273 B) revision, exit 0 control `43/43 pass`, 8/10 killed, survivors D2 and D10. Errata E1 (calibration on D7) and E2 (round 5 VER-T1 unreached-arm re-read).
   - `corpus/knowledge/fleet-kill-rate-ledger.md`: Rows 1 and 345 record `js-kimi-census` at `175de6ba…` / `83016d45…` as 8/10 (80%).
   - `corpus/knowledge/executor-test-sufficiency.md:46-47` & `witness-scoped-kill-verdict.md:27`: Cite the same pinned git rev and SHA256.

---

## 3. Substrate State: Git & Worktree Facts

Read-only inspection of `/home/vgpnk/Projects/shokunin/kumitate-shokunin` reveals the following grounded facts:

| Dimension | Pinned / Original State | Current Substrate State |
|---|---|---|
| **Repository Path** | `/home/vgpnk/Projects/shokunin/kumitate-shokunin` | `/home/vgpnk/Projects/shokunin/kumitate-shokunin` |
| **File Path** | `scripts/kimi-census.mjs` | `scripts/kimi-census.mjs` |
| **Git Commit SHA** | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `1770305fae20826b39905a8251ddeca6b4957ac4` |
| **Commit Subject** | `round-31 (final): multi-line-backtick class...` | `Integrate remote documentation; preserve local round log` |
| **Commit Distance** | Baseline anchor | 29 commits ahead of `175de6ba` (`175de6ba` is confirmed ancestor) |
| **Change Introducing Commit** | Baseline anchor | `1a8eed5aaa32043cf109dd28ceb5cd37ccd5555e` (round-34: skills 5 $\to$ 6, cursor-lane, K2 25 $\to$ 26) |
| **Git Blob Object ID** | `a2bf15c08ca08b073de2c72afc038547a9b284b4` | `e51e4cb9bbbdf0467bba9c7dfec3e3a1f65ae74f` |
| **Git Blob Mode** | `100644` | `100644` |
| **Committed SHA256** | `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426` | `5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0` |
| **Worktree SHA256** | N/A (historical) | `5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0` |
| **Target Dirty Status** | N/A | **clean** (`git status --porcelain scripts/kimi-census.mjs` is empty) |
| **Repo Dirty Status** | N/A | **clean** (`git status --porcelain` is empty) |
| **Line Count (newlines)** | 896 newlines (last byte `;`, no trailing newline) | 922 newlines (last byte `\n` closing brace, 922/923 lines, +26 newlines) |
| **Byte Size** | 43,273 bytes | 44,770 bytes (+1,497 bytes) |
| **Original Availability** | **YES** (retrievable from git object store via `git show 175de6ba...:scripts/kimi-census.mjs`) | N/A |
| **Content Disposition** | N/A | **changed** (`83016d45…` $\ne$ `5e8d5913…`) |

---

## 4. No Inferred Live Rate

- **Finding:** No live kill rate is inferred for `js-kimi-census`.
- **Grounding:**
  - The live substrate file has evolved in commit `1a8eed5aaa32043cf109dd28ceb5cd37ccd5555e` (round 34):
    - Member rules grew from 49 to 50 members.
    - `skills/` child count changed from 5 to 6 (`cursor-lane` directory added).
    - `FROZEN.K2` grew from 25 to 26.
    - The selftest suite expanded from 43 to 45 cases (added `UNLISTED: a 7th child under skills/` and `UNLISTED: root mcp.json remains undeclared...`).
    - Test assertions in selftest now explicitly verify `j.totals.frozen.K1 === 3 && j.totals.frozen.K2 === 26 && ...` (which directly eliminates the unasserted gap that allowed defect D10 to survive in round 2).
  - Under F7 rules and Round 13 acceptance: **`result_reuse=not_established` always**.
  - Pinned defect table `D1`–`D10` cannot be assumed to yield 8/10 on the current file. Projecting the historical 80% (8/10) kill rate onto the current substrate without executing an authorized, calibrated sweep would constitute an ungrounded attribution mistake.

---

## 5. Dependency & Context Blindness Analysis

Treating `js-kimi-census` purely as an isolated file-path pin introduces specific blindness dimensions:

1. **Runner vs. Worktree Blindness:**
   - In `tools/mutate-and-run.sh`, `regression_case_git` materializes the target via `git show ${rev}:${path}` into `${cwd}/target.kimi-census.mjs`.
   - As a consequence, running `--regression` passes on the historical object store bytes (`83016d45…`) while remaining completely blind to the fact that the committed and worktree state of `kumitate-shokunin/scripts/kimi-census.mjs` has drifted to `5e8d5913…`.
2. **Defect Spec Anchor Invalidation:**
   - The embedded defect spec `js-kimi-census.spec` hardcodes anchors from the round-2 version:
     - `D10`: `@old const FROZEN = { K1: 3, K2: 25, K3: 9, K4: 9, K5: 3 };`. In the current substrate, `K2: 25` does not exist (it is `K2: 26`). An in-place mutator matching exact strings will fail to find the target.
     - `D1`: `@old kind: 'dir', counted: 18 },`. In the current substrate, line numbers have shifted (+4 lines). While the replacement string still occurs, line references in reports and tools desynchronize.
3. **Semantic Evolution & Survivor Dynamics:**
   - In round 2 (`mutation-case-kimi-census.md`), D10 survived specifically because `FROZEN.K2` was reported but unasserted. In round 34, `kumitate-shokunin` added explicit assertions for `j.totals.frozen.K2 === 26` in selftest case 2. Thus, a re-cut defect mutating `K2: 26` would now be killed, shifting the theoretical kill rate. Assuming a constant kill rate ignores test-suite hardening.
4. **Execution Environment & Host Blindness:**
   - `kimi-census.mjs` relies on `node:fs` (`mkdtempSync`, `lstatSync`, `chmodSync`, `symlinkSync`), child processes (`runGate`), and host filesystem permissions.
   - Even if worktree bytes were identical, changes in the Node runtime (tested on Node v24.21.0 in r2) or umask could alter selftest outcomes. Safe result reuse requires verifying execution context equivalence, not just byte equality.

---

## 6. Coordination with Peer Seats

- Communicated pin coordinates to `TameshiR13.PinProbe` via peer channel (`agent://TameshiR13.PinProbe`):
  - Confirmed pinned repo `kumitate-shokunin`, path `scripts/kimi-census.mjs`, commit `175de6ba2e9e904010411b19cab27e0af9aad3d4`, blob SHA-1 `a2bf15c08ca08b073de2c72afc038547a9b284b4`, SHA256 `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`, mode `100644`.
  - Confirmed live HEAD `1770305fae20826b39905a8251ddeca6b4957ac4`, committed/worktree blob SHA-1 `e51e4cb9bbbdf0467bba9c7dfec3e3a1f65ae74f`, committed/worktree SHA256 `5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0`.
  - Confirmed target file clean in worktree (`git status --porcelain` empty), original bytes retrievable, content disposition **changed**, `result_reuse=not_established`.
  - Noted evolution in commit `1a8eed5aaa32043cf109dd28ceb5cd37ccd5555e` (skills 5 $\to$ 6, members 49 $\to$ 50, FROZEN.K2 25 $\to$ 26, selftest 43 $\to$ 45).

---

## 7. Checks for L1 Verification (Unexecuted)

L1 should run the following non-destructive verification commands during integration:

1. **Verify Pinned Blob Availability & Digest:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin cat-file -p 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs | sha256sum
   # Expected: 83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426  -
   ```

2. **Verify Current Committed & Worktree Blob Digest:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin cat-file -p HEAD:scripts/kimi-census.mjs | sha256sum
   sha256sum /home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs
   # Expected: both print 5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0
   ```

3. **Verify Target Cleanliness in Worktree:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin status --porcelain -- scripts/kimi-census.mjs
   # Expected: empty output (clean)
   ```

4. **Verify `pin-disposition.py` Row Generation (Once Landed):**
   ```bash
   python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py \
     --manifest /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json \
     --root /home/vgpnk/Projects/shokunin
   # Expected: row for js-kimi-census shows status="changed", result_reuse="not_established"
   ```

---

## 8. Tooling Log

- No external tools installed or upgraded during this reconnaissance seat (standard git and python3 hashlib used read-only).
