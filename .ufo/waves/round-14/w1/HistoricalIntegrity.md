# Round 14 w1 — HistoricalIntegrity: Historical Evidence, Closure Ownership, and Restraint Baseline Audit

Lane: `tameshi-shokunin`. Seat: `TameshiR14.HistoricalIntegrity` (leaf, read-only research scout).  
Target: Historical round12/round13 evidence inventory, newest closure note ownership, SHONEN scalar restraint baseline, and precise once-only L1 guardrail commands.  
Checks run: None mid-flight. Only static git tracking queries, file digest readings, and JSON schema inspection. No gates, selftests, mutation runners, or harness scripts were executed.  
Tool installs/updates: None.

---

## 1. Godspeed Axes & Frontier Orientation

1. **Axes (from `AXES.md` & `SCORECARD.md`):**
   - **depth** (current baseline: **6** / 10; 6 recorded mutation legs in `tools/mutate-and-run.sh:84-89`)
   - **calibration** (current baseline: **6** / 8; boxes 1, 2, 4 restrained `[~]` × 2, box 3 unscored)
   - **coverage** (unpinned; F7 prerequisite open)
   - **operability** (runner selftest / regression intact)
   - **freshness** (unpinned; successor sweeps open)
   - **adjacency** (strict boundary; sibling gates read-only, never absorbed)
2. **Current frontier state:**
   - Depth and calibration are tied-lowest at 6.
   - Round 14 targets capability acquisition C1 (effective expectation reconciliation, structured disposition gate `tools/evidence-disposition.py`), resolving outside routed defects 1–3 without scalar promotion credit.
   - Restraint baseline holds: zero scalar score inflation. Historical evidence remains byte-identical.

---

## 2. Historical Evidence Inventory (round-12 & round-13)

Historical evidence paths must remain strictly immutable. No file under `.ufo/evidence/round-12/` or `.ufo/evidence/round-13/` may be edited, moved, rewritten, or deleted.

### 2.1 File Count Baseline
- **Round-12 evidence files:** `562` tracked files (across 80 directory paths).
- **Round-13 evidence files:** `16` tracked files.
- **Combined historical evidence total:** `578` files.

### 2.2 Complete Round-13 Evidence Inventory (16 files with SHA-256 digests)

All 16 files reside in `.ufo/evidence/round-13/`:

| Path | SHA-256 Digest | Role in Evidence Architecture |
|---|---|---|
| `.ufo/evidence/round-13/after-committed.json` | `15a1df37f04fef0a7d5efbcb22f0699e699d8105d1246ecdee29891eae829506` | Post-commit state measurement |
| `.ufo/evidence/round-13/before-final.json` | `ba1a1605b617df3ab4ddec337d14095e1dfc71178ce7117a42534ab7209db644` | Pre-closeout state snapshot |
| `.ufo/evidence/round-13/before.json` | `a051564d28ed6e4b4038acac8d39b9fe64bea7c420aa9df80da4993a3d59733f` | Initial baseline state snapshot |
| `.ufo/evidence/round-13/claims.json` | `ba187b01459ea6a038a29bc038d7945033854c123a20330c7e1992abe5b8be5f` | Declared claims C1 and C2 |
| `.ufo/evidence/round-13/expected.json` | `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336` | Historical expectations file (13 inputs, 12 expected checks) |
| `.ufo/evidence/round-13/measure.py` | `27f959af9e51dcff2dd3bb755d1a3f71042f3f166611027d8564c682d8b294f9` | Round 13 counting/measurement script |
| `.ufo/evidence/round-13/pin-dispositions.json` | `210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637` | Pin probe observations across all 6 legs |
| `.ufo/evidence/round-13/pin-manifest.json` | `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6` | Pin manifest defining legs and commit SHAs |
| `.ufo/evidence/round-13/producer-before.py` | `592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0` | Unrepaired producer variant |
| `.ufo/evidence/round-13/producer-oracle-repair.json` | `df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d` | Red/green oracle repair receipt |
| `.ufo/evidence/round-13/producer-oracle.py` | `d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b` | Location-neutral failure oracle script |
| `.ufo/evidence/round-13/sources-after.json` | `568f044454be92ee1f3e2fdc0166ab24846394ffc74592769e3d12d97877220c` | Census output receipt after S047/S048 additions |
| `.ufo/evidence/round-13/verification-verdict.json` | `1d128a44e0417eb29ca75195bc7f97b8d0ceae246f520710faf67c397ef35a4c` | Integrated verification evaluation output |
| `.ufo/evidence/round-13/verification.json` | `a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f` | Raw integrated run receipt (12 input digests, 13 check entries) |
| `.ufo/evidence/round-13/witness-metadata-old-null.json` | `28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3` | Negative metadata fixture (`declaration.kind: null`) |
| `.ufo/evidence/round-13/witness-metadata.json` | `463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d` | Corrected metadata companion |

### 2.3 Round-12 Major Evidence Subtrees (562 files)

The 562 round-12 files span 80 distinct directories under `.ufo/evidence/round-12/`:
- **`BashWitness/` (99 files):** Contains `declaration.json`, `summary.json`, `declared.tsv`, `crashed-20261020T034646Z-sweep/` (25 files), `rerun-20261020T035435Z/` (29 files), and `sweep/` (27 files).
- **`BytesReview/` (217 files):** 20 scenarios (`C01`–`C20`, 11 files each) verifying CLI stream/exit behaviors, plus 8 top-level review files.
- **`FailureOracle/` (73 files):** Single-mutant/single-pristine baselines, actual pristine, red-before, restored-baseline gate runs, and alternate sequences.
- **`BaselineControl/` (34 files):** Scenarios A–D workdirs, fixtures, and execution logs.
- **`oracle-repair/` (28 files):** Green-after restored repetition and red-before single control mutant runs.
- **`ControlGate/` (20 files):** Determinism gate probes and mismatch logs.
- **`replayed-controls/` (11 files):** Three repeated control run outputs.
- **Top-level / Source surveys / Connectors / Bounds (80 files):** Including `verification-final.json`, `oracle-repair.json`, `verify-round.py`, `resumed-before.json`, `SourceFlakyPaper/`, `SourceSurvey/`, `AdmissionBounds/`, `BashDenominator/`.

### 2.4 Four Critical Round-12 Files Pinned in `round-13/expected.json`
1. `.ufo/evidence/round-12/BashWitness/summary.json`: `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9`
2. `.ufo/evidence/round-12/BashWitness/declaration.json`: `e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901`
3. `.ufo/evidence/round-12/BashWitness/declared.tsv`: `0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3`
4. `.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json`: `6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0`

---

## 3. Newest Closure Note Ownership & Integrity

### 3.1 Provenance & Identity
- **File:** `corpus/lessons/round-13-verifier-spotcheck.md`
- **Header:** `author: hyaku closure (non-author integrator, @m_strong)`
- **Delivered commit:** `d6809df7775338f000e44c8a916067b8866867fb`
- **Commit Author:** `protocol-shokunin <protocol@shokunin.local>`
- **Date:** `Tue Oct 20 02:13:46 2026 -0300`
- **Baseline Relationship:** This exact commit is the **round 14 baseline commit**.

### 3.2 Ownership Rules & Boundary Discipline
- **Strict non-author ownership:** Owned solely by protocol-level closure / hyaku integrator (`@m_strong`). No seat in `tameshi-shokunin` (neither L1 nor any leaf seat) has write, edit, or append authority over this file.
- **Historical status:** It is the non-author closure note for round 13 that established:
  - Bounded capability claims C1 (pin disposition) and C2 (metadata companion & producer oracle repair) admitted as `status ok; admitted true`.
  - All scalar scores held at **6**; no promotion credit, no 7th recorded mutation leg, no full F7 reuse claim.
  - S048 quote verification admitted; source census duplicate warnings recognized as intentional append-only corrections.
  - Three routed defects (contract expectation mismatch, missing GIT_DIR receipt, knowledge section 6 backlink) assigned to round 14 as append-only corrections.
- **Immutability rule:** `corpus/lessons/*-verifier-spotcheck.md` files are immutable historical records. Any modification by lane agents violates protocol and triggers an immediate invalidation.

---

## 4. SHONEN Scalar Restraint Baseline

### 4.1 Checkpoint State (`SHONEN.md`)
The file contains exactly 4 checklist items:
1. `SKILL.md contains real decision tables...` -> `[~]`
2. `At least one end-to-end domain task executed...` -> `[~]`
3. `Instructions executable by an agent without oral context...` -> `[~]`
4. `No cross-domain bleed (PROVINCE.md still accurate)...` -> `[~]`

### 4.2 Restraint Baseline & Scoring Mechanics
- **Mark Census (Command C from `SCORECARD.md`):**
  - Total boxes: `4`
  - Checked `[x]`: `0`
  - Asserted `[~]`: `4`
  - Untouched `[ ]`: `0`
  - `asserted_mark_upper_bound`: `8` (`min(8, 2 * 4)`)
- **Restraint Rubric:**
  - Box 3 is an unscored mark (Appendix A + B cold-read only, reconstructed survivor fixtures, not full SKILL cold-read; awards 0 score points per orchestrator adjudication in fleet round 1).
  - Boxes 1, 2, and 4 earn 2 points each = **6 points**.
  - Final 2 promotion points (to reach 8) require full independent promotion verification across all boxes, which lane-dispatched seats cannot award.
- **Depth Baseline (Command D from `SCORECARD.md`):**
  - Replay ledger in `tools/mutate-and-run.sh:84-89` lists exactly `6` recorded cases (js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify, bash-checklist-run, js-claims-check).
  - Depth score: `6` / 10.
- **Baseline Invariant for Round 14:**
  - `depth=6`, `calibration=6` (tied-lowest axes).
  - **Zero scalar promotion inflation:** `SHONEN.md` must not be edited. Round 14 adds structured capability (C1), not scalar promotion score.

---

## 5. Concrete Changes & Identified Risks for Round 14

### 5.1 Permitted Concrete Additions in Round 14
- `.ufo/evidence/round-14/` (new evidence directory: `claims.json`, `context-receipt.json`, `dispositions-before.json`, `dispositions.json`, `capture-context.py`).
- `tools/evidence-disposition.py` (new gate tool owned by Gate seat).
- `.ufo/waves/round-14/w1/*.md` (seat reports).
- `LOG.md` (append-only entry appended by L1 at round landing).

### 5.2 Key Risks & Falsification Conditions
1. **Historical Evidence Tampering (CRITICAL):**
   - *Risk:* Accidental mutation, deletion, or in-place overwrite of `.ufo/evidence/round-12/` or `.ufo/evidence/round-13/` files.
   - *Mitigation:* Explicit path-level git diff guardrail in L1 before integration.
2. **Cardinality Conflation (HIGH):**
   - *Risk:* Confusing the 13 `inputs` in `expected.json` / 13 `checks` in `verification.json` with the 12 `expected_checks` entries.
   - *Fact:* `expected_checks` has exactly **12** rows: 11 effective and 1 superseded (`producer_before`). The gate contract must enforce 11 effective + 1 superseded, not invent a 13th check.
3. **Producer Stale-Row Bypass (HIGH):**
   - *Risk:* Treating `exit_matches: true` as sufficient to pass `producer_before`, ignoring the missing `contains` phrase and the underlying `FileNotFoundError`.
   - *Fact:* `producer_before` failed raw `contains`; supersession requires binding the raw failure and enforcing both replacement oracle checks (`producer_before_oracle` and `producer_after_oracle`).
4. **Promotion Overreach (MEDIUM):**
   - *Risk:* Modifying `SHONEN.md` to claim promotion or unearned score advancement.
   - *Mitigation:* Guardrail ensuring byte-identity of `SHONEN.md`.
5. **Non-Author File Editing (CRITICAL):**
   - *Risk:* Modifying `corpus/lessons/round-13-verifier-spotcheck.md`.
   - *Mitigation:* Verifying zero git diff against commit `d6809df7775338f000e44c8a916067b8866867fb`.

---

## 6. Precise Once-Only L1 Guardrail Commands

L1 must run these precise guardrail commands once after all wave seats finish, before committing:

### Guardrail 1: Historical Evidence Immutability (Round-12 & Round-13)
```sh
git diff --exit-code d6809df7775338f000e44c8a916067b8866867fb HEAD -- \
  .ufo/evidence/round-12 .ufo/evidence/round-13
```
*Expected:* Exit 0, 0 lines diff.

### Guardrail 2: Historical File Count Baseline Check
```sh
test "$(git ls-files .ufo/evidence/round-12 | wc -l)" -eq 562 && \
test "$(git ls-files .ufo/evidence/round-13 | wc -l)" -eq 16 && \
echo "HISTORICAL_COUNTS: OK (562 + 16 = 578)"
```
*Expected:* Exit 0, `HISTORICAL_COUNTS: OK (562 + 16 = 578)`.

### Guardrail 3: Critical Frozen Digest Verification
```sh
python3 -c '
import hashlib
checks = {
    ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
    ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
    ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
    ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
    ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
    ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
    ".ufo/evidence/round-13/pin-dispositions.json": "210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637",
    ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6"
}
for path, expected_hash in checks.items():
    actual_hash = hashlib.sha256(open(path, "rb").read()).hexdigest()
    assert actual_hash == expected_hash, f"Digest mismatch at {path}: {actual_hash} != {expected_hash}"
print("HISTORICAL_DIGESTS: PASS (11/11 verified)")
'
```
*Expected:* Exit 0, `HISTORICAL_DIGESTS: PASS (11/11 verified)`.

### Guardrail 4: Non-Author Closure Note Immutability & Provenance Check
```sh
git diff --exit-code d6809df7775338f000e44c8a916067b8866867fb HEAD -- \
  corpus/lessons/round-13-verifier-spotcheck.md && \
test "$(git log -1 --format='%an <%ae>' -- corpus/lessons/round-13-verifier-spotcheck.md)" = "protocol-shokunin <protocol@shokunin.local>" && \
echo "CLOSURE_NOTE_IMMUTABILITY: OK"
```
*Expected:* Exit 0, `CLOSURE_NOTE_IMMUTABILITY: OK`.

### Guardrail 5: SHONEN Promotion Restraint Mark Census Check (Command C)
```sh
python3 -c '
import re
content = open("SHONEN.md").read()
m = re.findall(r"^- \[([x~ ])\] ", content, re.M)
print(f"boxes={len(m)} checked={m.count(\"x\")} asserted={m.count(\"~\")} untouched={m.count(\" \")}")
assert len(m) == 4, f"Expected 4 boxes, found {len(m)}"
assert m.count("~") == 4, f"Expected 4 asserted [~], found {m.count(\"~\")}"
assert m.count("x") == 0, f"Expected 0 checked [x], found {m.count(\"x\")}"
assert m.count(" ") == 0, f"Expected 0 untouched [ ], found {m.count(\" \")}"
print("SHONEN_RESTRICTION_CHECK: PASS (all 4 asserted, 0 checked, score baseline 6)")
'
```
*Expected:* Exit 0, `SHONEN_RESTRICTION_CHECK: PASS (all 4 asserted, 0 checked, score baseline 6)`.

### Guardrail 6: Depth Score Replay Ledger Gate Count Check (Command D)
```sh
python3 -c '
import re
content = open("tools/mutate-and-run.sh").read()
gates = re.findall(r"^#   (?:js|bash)-\S+\s+(\S+)\s+\d+/\d+", content, re.M)
n = len(gates)
unique = len(set(gates))
print(f"recorded_cases={n} unique_recorded_gates={unique} depth_score={min(10, n)}")
assert n == 6 and unique == 6, f"Expected 6/6 recorded cases, got {n}/{unique}"
print("DEPTH_SCORE_CHECK: PASS (6 recorded cases)")
'
```
*Expected:* Exit 0, `DEPTH_SCORE_CHECK: PASS (6 recorded cases)`.

### Guardrail 7: Leaf Seat Unauthorized File Modification Check
```sh
test -z "$(git diff --name-only d6809df7775338f000e44c8a916067b8866867fb HEAD -- \
  SKILL.md PROVINCE.md SHONEN.md corpus/lessons/*-verifier-spotcheck.md .ufo/evidence/round-12 .ufo/evidence/round-13)" && \
echo "SEAT_BOUNDARY_CHECK: PASS"
```
*Expected:* Exit 0, `SEAT_BOUNDARY_CHECK: PASS`.
