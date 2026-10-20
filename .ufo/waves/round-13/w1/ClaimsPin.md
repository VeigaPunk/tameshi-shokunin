# Reconnaissance Report: `js-claims-check` Pin & Current State (Round 13 — Scout ClaimsPin)

## 1. Axes & Posture (Godspeed)

- **Axes:**
  - **Depth ($C_1$):** Grounding the recorded `js-claims-check` leg to exact verifiable git blob, commit, and worktree digests; establishing concrete current-content disposition (confirming identical content while noting repo HEAD movement).
  - **Calibration ($C_2$):** Enforcing that identical content is **not** safe result reuse; forbidding ungrounded live kill-rate projections (`result_reuse=not_established`); maintaining the boundary between synthetic `--selftest` mutation observations and live gate efficacy.
- **Posture:** Iterate cheap, collect read-only git and hashlib facts in parallel, modify no sibling files, perform no test/build/lint/gate executions.

---

## 2. Runner Pins & Spec References in `tameshi-shokunin`

The leg `js-claims-check` is anchored across canonical references in `tameshi-shokunin`:

1. **Mutation Runner (`tools/mutate-and-run.sh`):**
   - **Header declaration (`:89`):** `# js-claims-check kumitate-shokunin/scripts/claims-check.mjs 7/10 (70 %)`
   - **Target relative path (`:1138`):** `kumitate-shokunin/scripts/claims-check.mjs`
   - **Pinned commit (`:553`):** `REV_CLAIMS=175de6ba2e9e904010411b19cab27e0af9aad3d4`
   - **Pinned blob SHA256 (`:552`):** `PIN_CLAIMS=e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b`
   - **Recorded decision table (`:559`):**
     `TABLE_CLAIMS='D1:KILLED,D2:KILLED,D3:KILLED,D4:KILLED,D5:KILLED,D6:KILLED,D7:SURVIVED,D8:SURVIVED,D9:SURVIVED,D10:KILLED'`
   - **Defect spec generator (`:842-888`):** Writes `js-claims-check.spec` containing 10 single-defect replacements (`D1`–`D10`) targeting lines in the pinned blob.
   - **Expected rate line (`:1104`):** Recorded kill-rates includes `js-claims-check=7/10`.
   - **Regression invocation (`:1137-1140`):**
     `regression_case_git js-claims-check 'kumitate-shokunin/scripts/claims-check.mjs' "$PIN_CLAIMS" "$REV_CLAIMS" "$specs/js-claims-check.spec" 'node "$MUTANT" --selftest' "$TABLE_CLAIMS" "$root/js-claims-check"`
   - **Selftest table mapping (`:1583`):** `'js-claims-check:js-claims-check.spec:TABLE_CLAIMS:10:7'`.

2. **Source Registry (`corpus/SOURCES.md:48`):**
   - **Row S037:** Tier A code source; `kumitate-shokunin/scripts/claims-check.mjs @ 175de6ba2e9e904010411b19cab27e0af9aad3d4 (blob sha256 e9a21b44…0f61b)`.

3. **Knowledge Ledger & Case Studies:**
   - `corpus/knowledge/mutation-case-kumitate-claims.md`: Documents round-8 T8-2 sweep (2026-10-14); 926 lines (925 newlines), 48,265 bytes, git blob `fae4bbcd158c527e70d8a69bcd3add372ed99c2e` at kumitate HEAD `175de6ba`. Suite command `node "$MUTANT" --selftest`. Kill rate 7/10 (70%), survivors D7, D8, D9; 0 inconclusive.
   - `corpus/knowledge/fleet-kill-rate-ledger.md:348`: Records `js-claims-check` at `175de6ba…` / `e9a21b44…` as 7/10 (70%).
   - `SKILL.md` (`:1049, :1104, :1178, :1317, :1409`): Records `js-claims-check` at `175de6ba`, blob `e9a21b44`, 7/10 = 70%.

---

## 3. Substrate State: Git & Worktree Facts

Read-only inspection of `/home/vgpnk/Projects/shokunin/kumitate-shokunin` reveals the following grounded facts:

| Dimension | Pinned / Original State | Current Substrate State |
|---|---|---|
| **Repository Path** | `/home/vgpnk/Projects/shokunin/kumitate-shokunin` | `/home/vgpnk/Projects/shokunin/kumitate-shokunin` |
| **File Path** | `scripts/claims-check.mjs` | `scripts/claims-check.mjs` |
| **Git Commit SHA** | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `1770305fae20826b39905a8251ddeca6b4957ac4` |
| **Commit Subject** | Baseline r8 anchor | `Integrate remote documentation; preserve local round log` |
| **Commit Distance** | Baseline anchor | 27 commits ahead of `175de6ba` |
| **Target Commits in Range** | Baseline anchor | **0 commits** modifying `scripts/claims-check.mjs` between `175de6ba` and HEAD |
| **Git Blob Object ID** | `fae4bbcd158c527e70d8a69bcd3add372ed99c2e` | `fae4bbcd158c527e70d8a69bcd3add372ed99c2e` |
| **Blob Mode** | `100755` | `100755` |
| **Committed SHA256** | `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` | `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` |
| **Worktree SHA256** | N/A (historical) | `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` |
| **Target Dirty Status** | N/A | **clean** (`git status --porcelain -- scripts/claims-check.mjs` is empty) |
| **Line Count** | 926 lines (925 newlines; ends with `;` without trailing newline) | 926 lines (925 newlines; ends with `;` without trailing newline) |
| **Byte Size** | 48,265 bytes | 48,265 bytes |
| **Original Availability** | **YES** (present in git store at `175de6ba`, at HEAD, and in worktree) | **YES** |
| **Content Disposition** | Baseline | **unchanged** (`e9a21b44…` == `e9a21b44…`) |

---

## 4. No Inferred Live Rate

- **Finding:** No live kill rate is inferred for `js-claims-check`.
- **Grounding & Rule Adherence:**
  - In accordance with Round 13 acceptance and Criterion 11/12 (`lessons/round-12.md`): **identical content is not safe result reuse, and no new kill-rate or seventh case is claimed**.
  - Content disposition is **`unchanged`**, but result reuse is strictly **`result_reuse=not_established`**.
  - Re-evaluating identical bytes across rounds does not prove that historical defect sensitivity holds in live execution. The historical 7/10 (70%) rate remains an immutable record of the round-8 T8-2 experiment on isolated synthetic fixtures under Node v24.21.0, not an ambient property of the current live gate.

---

## 5. Dependency & Context Blindness Analysis

Treating `js-claims-check` purely as an isolated file-path pin introduces critical blindness dimensions:

1. **Selftest Sandbox vs. Live Context Blindness:**
   - The historical 70% kill-rate was evaluated exclusively against `node "$MUTANT" --selftest` (`mutate-and-run.sh:1139`).
   - `--selftest` executes in an isolated sandbox (`mkdtempSync(join(tmpdir(), 'kumitate-claims-selftest-'))`), generating ephemeral mock trees for `SCORECARD.md`, `corpus/knowledge`, and `corpus/lessons`.
   - `--selftest` explicitly bypasses origin directory resolution (`claims-check.mjs:903` skips `resolveSrcDefault()` when `--selftest` is active).
   - Consequently, the mutation sweep never exercised live filesystem interactions, real repository `SCORECARD.md` parsing, real member-section regex matching, or live origin paths.
2. **Substrate Repository Evolution Blindness:**
   - Although `scripts/claims-check.mjs` is byte-identical across the 27 commits between `175de6ba` and HEAD `1770305f`, kumitate-shokunin's surrounding repository state has evolved significantly:
     - Commits in the range modified `SCORECARD.md` rows, member sections, and corpus files (e.g. `round-32: complete the R11 note-honesty leg`, `round-32: land the measured layer re-census`, `round-34: sources-registry gate`).
     - In live execution (`node scripts/claims-check.mjs`), `claims-check.mjs` defaults `--self` to `..` relative to its script location (`/home/vgpnk/Projects/shokunin/kumitate-shokunin`).
     - A byte-identical gate running in a changed repository context can exhibit changed verdicts or unreached branches in production without any defect mutation.
3. **External Environment & Origin Tree Blindness:**
   - In production mode, `resolveSrcDefault()` probes environment variable `$UFO_SRC`, followed by candidates `~/Projects/ufo-fsd-alpha` and `~/Projects/origin-work/ufo-fsd-alpha`.
   - Live execution depends on the external existence, permissions, and HEAD state of that origin tree. An absent origin tree triggers the `SRC_NOT_A_DIR` fail-closed arm (exit 2).
4. **Subprocess Self-Invocation & Runtime Blindness:**
   - `claims-check.mjs` invokes itself recursively in `--selftest` via `spawnSync(process.execPath, [TOOL_FILE, ...args])` (`:581-586`).
   - In mutation runs, `TOOL_FILE` is the mutant copy. If the mutation harness runs in an environment where file execution permissions (`100755`) are not mirrored, or where the Node.js runtime ESM loader behaves differently, execution fails at setup rather than at gate assertion.
5. **Defect Sample Specificity:**
   - The 7/10 score was established on 10 hand-authored defects (6 asserted-surface kills D1–D6, plus 4 hole-aimed probes D7–D10).
   - Three defects survived intentionally (D7 finding cap, D8 symbol floor length, D9 prose unreached arm). Projecting this finite sample onto general gate reliability conflates sample survival with overall gate soundness.

---

## 6. Coordination with Peer Seats

- Communicated exact pin coordinates to `TameshiR13.PinProbe` via peer channel (`agent://TameshiR13.PinProbe`):
  - Confirmed leg: `js-claims-check`.
  - Confirmed repo: `kumitate-shokunin`, path: `scripts/claims-check.mjs`.
  - Confirmed pinned commit: `175de6ba2e9e904010411b19cab27e0af9aad3d4`.
  - Confirmed pinned SHA256: `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b`.
  - Confirmed blob SHA-1: `fae4bbcd158c527e70d8a69bcd3add372ed99c2e`, mode: `100755`.
  - Confirmed current HEAD commit: `1770305fae20826b39905a8251ddeca6b4957ac4`.
  - Confirmed committed blob SHA256 at HEAD: `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b`.
  - Confirmed worktree SHA256: `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b`.
  - Confirmed target dirty status: clean.
  - Confirmed content disposition: `unchanged`.
  - Confirmed result reuse: `not_established`.
  - Highlighted distinction between pinned commit `175de6ba` and current HEAD `1770305f` so the manifest records separate commit fields.

---

## 7. Checks for L1 Verification (Unexecuted)

L1 should run the following non-destructive verification commands during integration:

1. **Verify Pinned Blob Availability & Digest:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin cat-file -p 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs | sha256sum
   # Expected: e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b  -
   ```

2. **Verify Current Committed & Worktree Blob Digest:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin cat-file -p HEAD:scripts/claims-check.mjs | sha256sum
   sha256sum /home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs
   # Expected: both print e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b
   ```

3. **Verify Target Cleanliness in Worktree:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin status --porcelain -- scripts/claims-check.mjs
   # Expected: empty output (clean)
   ```

4. **Verify Target Invariance Across Kumitate Commit Range:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin log 175de6ba2e9e904010411b19cab27e0af9aad3d4..HEAD -- scripts/claims-check.mjs
   # Expected: empty output (0 commits modifying the target file)
   ```

5. **Verify `pin-disposition.py` Manifest Disposition (Once Landed):**
   ```bash
   python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py \
     --manifest /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json \
     --root /home/vgpnk/Projects/shokunin
   # Expected: row for js-claims-check displays status="unchanged", result_reuse="not_established"
   ```

---

## 8. Tooling Directive Log

- **Tooling installs / updates:** None. All observations were gathered using pre-existing host tools (`git`, `sha256sum`, Node.js v24.21.0, bash 5.3.15).
