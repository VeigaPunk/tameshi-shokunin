# MadoPin — round-13 reconnaissance: bash-mado-verify leg pin disposition

Seat: `TameshiR13.MadoPin` (scout, leaf).
Status: Completed.
Modifications: Scoped exclusively to `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-13/w1/MadoPin.md`. Sibling code untouched; zero sibling gate executions.
Tool installs/updates: None (zero installs).

---

## 1. Executive Summary & Exact Pin Coordinates

Reconnaissance for recorded mutation leg `bash-mado-verify` comparing canonical runner pins in `tameshi-shokunin` against live `mado-shokunin`:

| Dimension | Pinned / Recorded Baseline | Current Committed HEAD | Current Worktree Target |
|---|---|---|---|
| **Repository** | `mado-shokunin` (sibling checkout) | `mado-shokunin` | `mado-shokunin` |
| **Path** | `tools/mado-verify.sh` | `tools/mado-verify.sh` | `tools/mado-verify.sh` |
| **Commit Rev** | `eead56b20ad2b28299ae4fa623d52a99b44c743c` | `95cbc41fe5d5db121b89c2ddd1f953728663c5f4` | N/A (worktree) |
| **Commit Subject** | `probation round 5 (training r4): see LOG` | `round-13: protocol boundaries and exact-set census` | N/A |
| **Git Blob OID** | `7ccc601f813933159de05902166cfdb584fc5025` | `656f1918ad5d124dd0de5beb1b5b53ea495a5bf4` | N/A |
| **Blob Mode** | `100755` | `100755` | `100755` |
| **Byte Count** | `45,334` B | `163,018` B | `163,018` B |
| **Line Count** | `1,098` L | `3,458` L | `3,458` L |
| **Full SHA256** | `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` | `037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569` | `037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569` |
| **Target Dirty** | N/A | N/A | **CLEAN** (`git diff tools/mado-verify.sh` is empty) |
| **Content Status** | Baseline reference | **`changed`** (+2,360 lines, +117,684 bytes vs pin) | **`changed`** (matches HEAD blob) |
| **Original Bytes** | **Available** in object store | N/A | N/A |
| **Result Reuse** | Recorded: 4/10 killed (40%) | **`not_established`** | **`not_established`** |

---

## 2. In-Repo Runner Pins and Spec References

All references under `/home/vgpnk/Projects/shokunin/tameshi-shokunin` anchor to the identical original pin:

1. **`tools/mutate-and-run.sh`**:
   - `PIN_MADO=d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` (line 548).
   - `REV_MADO=eead56b20ad2b28299ae4fa623d52a99b44c743c` (line 549).
   - Target table: `TABLE_MADO='D1:KILLED,D2:KILLED,D3:SURVIVED,D4:KILLED,D5:SURVIVED,D6:KILLED,D7:SURVIVED,D8:SURVIVED,D9:SURVIVED,R1:SURVIVED'` (line 557; 10 defects, 4 killed, 6 survived).
   - Embedded spec: lines 720–765 write `bash-mado-verify.spec` (defects D1–D9, R1 mapped to clauses A–F).
   - Invocation: line 1127–1130 invokes `regression_case_git bash-mado-verify 'mado-shokunin/tools/mado-verify.sh' "$PIN_MADO" "$REV_MADO" "$specs/bash-mado-verify.spec" 'bash "$MUTANT" --selftest' "$TABLE_MADO" "$root/bash-mado-verify"`.
   - Mode preservation: lines 952–956 check `blob_mode == 100755` and restore `chmod +x` on materialized target.

2. **`corpus/SOURCES.md`**:
   - Row `S035` (Tier A, mined): `mado-shokunin/tools/mado-verify.sh @ eead56b20ad2b28299ae4fa623d52a99b44c743c (blob sha256 d7edaab4…d0e13; round-5 sweep pin)`.

3. **`corpus/knowledge/mutation-case-mado-verify.md`**:
   - T6-1 service sweep: target `d7edaab4…d0e13` (1,098 L / 45,334 B), suite `bash "$MUTANT" --selftest`, control 28/28 passed green, 4/10 killed (40%).

4. **`corpus/knowledge/fleet-suite-census.md` & `fleet-kill-rate-ledger.md`**:
   - Pins `tools/mado-verify.sh` @ `d7edaab4…` (`eead56b2`).
   - Round 12 observation noted live drift to 2,887 L (`7da4ec50…`); round 13 live observation reveals further drift to 3,458 L (`95cbc41f…`).

---

## 3. Availability of Original Bytes

- **Git Object Store Verification:**
  - `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse --verify --quiet eead56b20ad2b28299ae4fa623d52a99b44c743c^{commit}` exits 0.
  - `git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh` exits 0.
  - `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh | sha256sum` produces `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13`.
- **Verdict:** Original bytes remain **100% available and bit-for-bit reproducible** from the local git object store.

---

## 4. Live Rate and Result Reuse Invalidation

- **No Inferred Live Rate:**
  - The historical 4/10 (40%) kill rate was measured strictly on `eead56b20ad2b28299ae4fa623d52a99b44c743c` (`d7edaab4...`).
  - No live kill rate is inferred, assumed, or projected for HEAD `95cbc41fe5d5db121b89c2ddd1f953728663c5f4` (`037b05dc...`).
- **Result Reuse Invalidation:**
  - Target content has extensively drifted (+2,360 lines, +259% length).
  - Even if bytes had been identical, under F7 depth discipline identical content is not safe result reuse without identical execution context.
  - Per round-13 contract, `result_reuse` is strictly **`not_established`**.

---

## 5. Dependency & Context Blindness Analysis

1. **Syntactic & Structural Spec Blindness:**
   - The 10 defect definitions in `bash-mado-verify.spec` were authored against line offsets in the 1,098-line round-5 gate.
   - Example: D1 mutates `MADO_VERIFY: CLEAN` at line 1088; D6 drops `xdph` from a 12-element config array at line 522; D7 checks a 17-element include list.
   - In HEAD (`95cbc41`), the include count changed to 18, local confs to 13, and the file expanded to 3,458 lines. Attempting to replay historical mutation specs against HEAD would cause patch application failures or mutate out-of-context blocks.

2. **Runtime Environment Dependencies:**
   - `python3` with `tomllib` (Python 3.11+): `mado-verify.sh` invokes python to parse TOML configurations (`walker`, `alacritty`). On hosts lacking Python 3.11+, fallback clause F triggers `UNKNOWN`, altering gate flow.
   - `hyprctl` compositor reads: In live mode (`--no-live` omitted), the gate queries compositor instances, binds, and layers. Absence or presence of an active Hyprland session changes execution paths.
   - Hermetic `--selftest` isolation: Selftest scenario C explicitly starves `PATH` to verify compositor absence handling; selftest scenarios depend on `$0` pointing to the executable. When invoked via `bash "$MUTANT" --selftest`, `$0` resolves to `$MUTANT`.

3. **Concurrency & Shared Namespace Blindness:**
   - Selftest creates temporary directories under `/tmp/w5-mado-m52-selftest.*` (or similar pattern).
   - Concurrent test runs across agents or sibling lanes risk namespace collisions or interference if scratch patterns overlap.

4. **Repository Location Assumption:**
   - `mutate-and-run.sh` derives `FLEET_ROOT` via relative path traversal from `$SELF`.
   - It assumes `mado-shokunin` exists at `$FLEET_ROOT/mado-shokunin` with an intact `.git` repository.

---

## 6. Coordination with Peers

- Grounded coordinates sent directly to `agent://TameshiR13.PinProbe` via peer write: confirmed `mado-shokunin`, `tools/mado-verify.sh`, pinned rev `eead56b20ad2b28299ae4fa623d52a99b44c743c`, pinned sha256 `d7edaab4...`, HEAD rev `95cbc41fe5d5db121b89c2ddd1f953728663c5f4`, HEAD sha256 `037b05dc...`, worktree clean, status `changed`, `result_reuse: not_established`.

---

## 7. Checks L1 Should Run (Advisory — Not Executed by This Seat)

1. **Verify Original Blob Availability:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh
   ```
   (Expect exit 0).

2. **Verify Target Cleanliness in Sibling Worktree:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --quiet tools/mado-verify.sh
   ```
   (Expect exit 0).

3. **Verify Pin Disposition Output for bash-mado-verify Row:**
   ```bash
   python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py \
     --manifest /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json \
     --root /home/vgpnk/Projects/shokunin | jq '.legs[] | select(.leg=="bash-mado-verify")'
   ```
   (Expect `content_status: "changed"`, `result_reuse: "not_established"`, `head_blob_sha256: "037b05dc..."`, `worktree_sha256: "037b05dc..."`, `target_dirty: false`).

4. **Verify Runner Still Materializes Original Pin for Regression:**
   ```bash
   git -C /home/vgpnk/Projects/shokunin/mado-shokunin show eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh | sha256sum
   ```
   (Expect `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13  -`).
