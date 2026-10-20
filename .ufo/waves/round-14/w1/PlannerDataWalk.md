# Round 14 w1 — PlannerDataWalk: Bounded Data-Walk and Synthesis for `producer_before`

Seat: `TameshiR14.PlannerDataWalk` (connector, leaf).
Role: UFO-FSD connector.
Assignment: Perform bounded data-walk of one `producer_before` row through expected -> receipt -> replacement -> disposition result; give minimal complete design before generalizing all rows.
Destination: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-14/w1/PlannerDataWalk.md`
Tool installs/updates: none.
Mid-flight checks: none (no test, gate, runner, or verification executed).

---

## 1. Axes in Scope

- **Calibration (primary):** Distinguish setup/relocation infrastructure crash from genuine semantic defect; eliminate exit-only false positives (`exit_matches: true` masquerading as verification); enforce fail-closed bi-directional supersession guards (a superseded row must retain its failing raw receipt, and replacements must pass their own expectations).
- **Depth:** Ground the reconciliation in bit-exact SHA-256 digests, literal line numbers, and the single source delta (`declaration.get("declared", {}).get("kind")` → `declaration.get("kind")`) with exact failure/pass strings (`... kind FAIL` vs `... kind ok`).
- **Coverage, Operability, Freshness, Adjacency (guardrails — harm none):** 
  - *Coverage:* Retains all 12 historical expectation rows without omission or invention.
  - *Operability:* Pure standard-library Python CLI; zero receipt `argv` execution; isolated selftest via subprocess self-invocation on temporary fixtures.
  - *Freshness:* Pre-claims no un-opted sibling mutation sweeps; historical evidence remains bit-exact and immutable.
  - *Adjacency:* Sibling repositories remain strictly read-only.

---

## 2. Evidence Chain and Cardinality Grounding

All evidence is read directly from committed repository artifacts:
- Baseline: `d6809df7775338f000e44c8a916067b8866867fb`
- Historical expectation: `.ufo/evidence/round-13/expected.json` (SHA-256: `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336`)
- Historical execution receipt: `.ufo/evidence/round-13/verification.json` (SHA-256: `a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f`)
- Historical repair receipt: `.ufo/evidence/round-13/producer-oracle-repair.json` (SHA-256: `df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d`)
- Historical verdict: `.ufo/evidence/round-13/verification-verdict.json` (SHA-256: `1d128a44e0417eb29ca75195bc7f97b8d0ceae246f520710faf67c397ef35a4c`)

### Cardinality Resolution (The 12 vs 13 Discrepancy)
The prompt text mentions "All13 expected rows". A rigorous static count of `.ufo/evidence/round-13/expected.json` establishes:
1. `expected_checks` has **exactly 12 keys**:
   `pin_selftest`, `metadata_selftest`, `metadata_old_null`, `metadata_corrected`, `producer_before`, `producer_before_oracle`, `producer_after_oracle`, `producer_after`, `witness_check`, `witness_count`, `pin_live`, `source_census`.
2. `inputs` has **12 + 1 = 13 file entries** (all 13 match working tree bytes at baseline).
3. `verification.json` has **13 check entries**, which includes 3 receipt-only observations (`pin_env_scrub`, `metadata_emit`, `frozen_and_guardrail_unchanged`) not in `expected_checks`.
4. `verification-verdict.json` lists 15 names, omitting `producer_before` and inventing `baseline_final_count` (which exists in no raw receipt).

**Resolution:** The disposition ledger must enumerate **exactly 12 rows** corresponding 1-to-1 to `expected.json#/expected_checks`. In `dispositions-before.json`, all 12 are `effective`. In `dispositions.json`, 11 are `effective` and 1 (`producer_before`) is `superseded`. No 13th row is fabricated.

---

## 3. Bounded Data-Walk of the `producer_before` Row

### Stage 1: The Expectation (`expected.json`)
```json
"producer_before": {
  "exit": 1,
  "contains": "summary preserves top-level exposed declaration kind"
}
```
- Declared intent: Run the historical producer before the fix, expect exit code 1, and expect stdout to contain the assertion identifier `summary preserves top-level exposed declaration kind`.
- Prerequisite: All 13 input digests in `expected.json["inputs"]` must match disk before predicate evaluation.

### Stage 2: The Raw Execution Receipt (`verification.json`)
The receipt contains:
```json
{
  "name": "producer_before",
  "argv": ["python3", ".ufo/evidence/round-13/producer-before.py", "selftest"],
  "started_at": "2026-10-20T04:59:26.753309+00:00",
  "exit": 1,
  "expected_exit": 1,
  "exit_matches": true,
  "stdout": "  check extract_spec picks the census heredoc        ok\n  ... [checks 1-34 pass] ...\n  check mutant digest mismatch refuses               ok\n",
  "stderr": "Traceback (most recent call last):\n  File \".../producer-before.py\", line 1633, in <module>\n    sys.exit(main())\n  File \".../producer-before.py\", line 1478, in cmd_selftest\n    \"runner\": {\"sha256\": sha256_file(RUNNER)},\n  File \".../producer-before.py\", line 218, in sha256_file\n    with open(path, \"rb\") as fh:\nFileNotFoundError: [Errno 2] No such file or directory: '.../.ufo/evidence/tools/mutate-and-run.sh'\n"
}
```
- **Evaluation under `dispositions-before.json` (where state is `effective`):**
  - Exit evaluation: Observed `exit == 1`, expected `1` -> Matches.
  - Predicate evaluation: `"summary preserves top-level exposed declaration kind" in check["stdout"]` -> **FAILS**.
  - Root cause of failure: The script was relocated to `.ufo/evidence/round-13/producer-before.py`. At lines 93–95, `REPO = Path(__file__).resolve().parent.parent` resolved to `.ufo/evidence` rather than the lane root, attempting to read `RUNNER` at `.ufo/evidence/tools/mutate-and-run.sh`. The process crashed at check 35 with unhandled `FileNotFoundError`, exiting with Python's default exception exit code 1. Check 39 was never executed.
  - **Result:** Gate exits `1` with finding `EDS-PREDICATE-FAILED` on row `producer_before`.
  - **Calibration value:** This proves the negative control. It demonstrates that the old unresolved expectation fails and that `exit_matches: true` alone is rejected as mechanism proof.

### Stage 3: Replacement Oracle Checks (`producer-oracle-repair.json`)
`producer-oracle.py` (SHA-256: `d5ae0bd4...`) isolates the source and runner into a temporary `tools/` directory, restoring the valid path layout without modifying historical source bytes.
1. Check `producer_before_oracle`:
   - Evaluates historical source `.ufo/evidence/round-13/producer-before.py` (SHA-256: `592c5c3d...`).
   - Reaches check 39 (lines 1542–1544): `qsummary["declaration"]["kind"] == "declared-witness mapping (not a blind preregistration)"`.
   - Because line 787 reads `declaration.get("declared", {}).get("kind")` (which is `None`), check 39 evaluates to `False`.
   - Output: `check summary preserves top-level exposed declaration kind FAIL\nWITNESS_SELFTEST: 40/41 pass\nVERDICT: FAIL\n`.
   - Exit code: `1`.
   - Matches original `expected_checks.producer_before_oracle` (`exit: 1`, `contains: "... kind FAIL"`).
2. Check `producer_after_oracle`:
   - Evaluates delivered source `tools/bash-witness-study.py` (SHA-256: `49e9e5e2...`).
   - Line 787 correctly reads `declaration.get("kind")`. Check 39 evaluates to `True`.
   - Output: `check summary preserves top-level exposed declaration kind ok\nWITNESS_SELFTEST: 41/41 pass\nVERDICT: PASS\n`.
   - Exit code: `0`.
   - Matches original `expected_checks.producer_after_oracle` (`exit: 0`, `contains: "WITNESS_SELFTEST: 41/41 pass"`).

### Stage 4: After-Disposition Evaluation (`dispositions.json`)
Row `producer_before` transitions from `effective` to `superseded`:
```json
{
  "name": "producer_before",
  "state": "superseded",
  "receipt": ".ufo/evidence/round-13/verification.json",
  "check": "producer_before",
  "reason": "path-layout FileNotFoundError before target assertion; replaced by oracle pair verifying root cause",
  "superseded_by": [
    "producer_before_oracle",
    "producer_after_oracle"
  ]
}
```
- Gate evaluation:
  1. Locates raw check `verification.json#/checks/producer_before`.
  2. Confirms raw check exit is 1, but its stdout lacks the assertion needle (verifying it is indeed an unresolved raw observation).
  3. Verifies `reason` is non-empty.
  4. Verifies `superseded_by` contains valid keys that are both `effective` in `dispositions.json`.
  5. Verifies both `producer_before_oracle` and `producer_after_oracle` satisfy their own original expectations in `expected.json`.
  6. **Result:** Row `producer_before` is reconciled as `superseded_valid`. Gate exits `0` (clean).

---

## 4. Synthesis: Resolving Cross-Proposal Contradictions

By examining peer reports (`Supersession`, `DropCritic`, `EffectiveRows`, `ExitOnlyCritic`, `BaselineCritic`, `RegistryContract`), four significant contradictions emerge:

| Contradiction / Conflict | Proposal A (Naive / Spec-literal) | Proposal B (Over-defensive / Sibling divergent) | Proposed Non-Obvious Move (Unified Synthesis) |
|---|---|---|---|
| **1. Row Schema Consistency** | Spec suggests superseded rows drop pointers: `name/state/reason/superseded_by`. | `Supersession.md` (F2) proposes new fields `raw_receipt` and `raw_check`. | **Uniform Row Pointer Tuple:** Every row (effective and superseded) retains `(name, state, receipt, check)`. Superseded rows *add* `reason` and `superseded_by`. This preserves exact JSON diff symmetry between `dispositions-before.json` and `dispositions.json` (differing only in `state` and the added supersession fields). |
| **2. Supersession Authority Guard** | Gate only checks if `superseded_by` replacements pass. | `DropCritic` (D5) / `Supersession` (F3) warn an author could supersede passing checks to mask regressions. | **Bi-Directional Predicate Validation:** The Gate evaluates the retained raw receipt check and asserts that it **FAILS** its original expectation. If the raw check passes, supersession is rejected (`EDS-SUPERSEDED-RAW-PASSED`). Supersession is valid *only* when the raw observation was genuinely defective/unresolved. |
| **3. Receipt Tamper Boundary** | Gate verifies only `expected.json["inputs"]`. | `ReceiptProvenance` / `BaselineCritic` note `verification.json` and `producer-oracle-repair.json` are NOT in `expected.json["inputs"]`. | **Dual-Tier Digest Anchoring:** `dispositions.json`'s top-level `inputs` map explicitly pins `expected.json`, `verification.json`, and `producer-oracle-repair.json`. Gate checks: Tier 1 = verify `dispositions.json["inputs"]` against disk; Tier 2 = verify `expected.json["inputs"]` against disk; Tier 3 = verify all row `receipt` paths belong to the verified `dispositions.json["inputs"]`. |
| **4. Cardinality Alignment** | Spec refers to "All13 expected rows". | `EffectiveRows` notes `expected_checks` has 12 keys, while `inputs` has 13 files. | **Strict 1-to-1 Bijection:** Gate asserts `set(row["name"] for row in rows) == set(expected.json["expected_checks"].keys())` (exactly 12). Rejects unknown, duplicate, or missing rows. Explicitly documents that 13 refers to input files, not expectations. |

---

## 5. Minimal Complete Design Specification

### A. Disposition Schema (`evidence-dispositions-v1`)

```json
{
  "schema": "evidence-dispositions-v1",
  "expected_file": ".ufo/evidence/round-13/expected.json",
  "inputs": {
    ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
    ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
    ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d"
  },
  "rows": [
    {
      "name": "producer_before",
      "state": "superseded",
      "receipt": ".ufo/evidence/round-13/verification.json",
      "check": "producer_before",
      "reason": "path-layout FileNotFoundError before target assertion; replaced by oracle pair verifying root cause",
      "superseded_by": [
        "producer_before_oracle",
        "producer_after_oracle"
      ]
    },
    {
      "name": "producer_before_oracle",
      "state": "effective",
      "receipt": ".ufo/evidence/round-13/producer-oracle-repair.json",
      "check": "producer_before_oracle"
    },
    {
      "name": "producer_after_oracle",
      "state": "effective",
      "receipt": ".ufo/evidence/round-13/producer-oracle-repair.json",
      "check": "producer_after_oracle"
    }
  ]
}
```

### B. Gate Execution Pipeline (`tools/evidence-disposition.py`)

1. **CLI Interface:**
   - `python3 tools/evidence-disposition.py --root LANE_ROOT --dispositions FILE --json`
   - `python3 tools/evidence-disposition.py --selftest`
   - Exit codes:
     - `0`: All expectations accounted for, effective checks pass, superseded checks verified and replaced.
     - `1`: Semantic expectation failure (e.g. `dispositions-before.json` failing on `producer_before`).
     - `2`: Could-not-evaluate (bad input, missing file, SHA-256 mismatch, cycle, path escape).
     - `64`: Usage error.
2. **Evaluation Order:**
   - Step 1: Validate CLI arguments and lane root containment (`realpath`).
   - Step 2: Parse `dispositions.json` with duplicate-key rejection hook.
   - Step 3: Verify all files in `dispositions.json["inputs"]` match disk SHA-256 (Tier 1).
   - Step 4: Parse `expected.json`; verify all 13 files in `expected.json["inputs"]` match disk SHA-256 (Tier 2).
   - Step 5: Check row cardinality: `len(rows) == 12` and `set(rows) == set(expected_checks)`.
   - Step 6: Parse receipt files (`verification.json`, `producer-oracle-repair.json`).
   - Step 7: For every `effective` row:
     - Recompute `check.exit == expected.exit`.
     - Evaluate `contains` on `check.stdout` only (never stderr).
     - Evaluate structured JSON fields (`pin_live`, `metadata_old_null`, `metadata_corrected`).
     - If any fail -> record finding and mark exit 1.
   - Step 8: For every `superseded` row (`producer_before`):
     - Confirm raw check exists in `receipt`.
     - Confirm raw check **fails** original `expected_checks` predicate (bi-directional guard).
     - Confirm `reason` is non-empty.
     - Confirm `superseded_by` elements are effective rows that passed in Step 7.
     - If raw check passed or replacements failed -> record finding and mark exit 1.
   - Step 9: Emit stable JSON report with finding IDs.

### C. Stable Finding IDs (`EDS-*`)
- `EDS-CLEAN` (exit 0)
- `EDS-PREDICATE-FAILED` (exit 1: expectation predicate failed on effective row)
- `EDS-SUPERSEDED-RAW-PASSED` (exit 1: attempted to supersede a check that already passes)
- `EDS-REPLACEMENT-FAILED` (exit 1: replacement check failed its expectation)
- `EDS-ROW-COUNT` (exit 1: row count != 12 or set mismatch)
- `EDS-UNMAPPED-ROW` (exit 1: row not in expected_checks)
- `EDS-DIGEST-MISMATCH` (exit 2: file on disk does not match pinned SHA-256)
- `EDS-SCHEMA-INVALID` (exit 2: missing keys, invalid types, duplicate keys)
- `EDS-PATH-ESCAPED` (exit 2: path traverses outside root or symlink detected)
- `EDS-CYCLE-DETECTED` (exit 2: replacement points to another superseded row)

---

## 6. Second-Order Effects Across Surfaces

1. **Runtime Surface:**
   The gate is strictly analytical over recorded bytes. It NEVER executes `receipt.argv`. This eliminates environment leakage, working directory sensitivity, and execution timeout hazards.
2. **Contract Surface:**
   The 12-row bijection maintains absolute accountability. No stale check can be silently dropped; every check must be either proven effective or explicitly superseded with audited replacements.
3. **Substrate Surface:**
   Frozen round-12 and round-13 evidence files (`.ufo/evidence/round-12/*`, `.ufo/evidence/round-13/*`, `tools/mutate-and-run.sh`, `SHONEN.md`) remain byte-identical.
4. **Verification Surface:**
   Distinguishes the negative control (`dispositions-before.json` exiting 1 on `contains`) from the positive reconciliation (`dispositions.json` exiting 0). This delivers honest red-before/green-after proof for the reconciliation capability claim C1.

---

## 7. Concrete Risks and Mitigations

| Risk | Severity | Root Cause | Mitigation |
|---|---|---|---|
| **1. Traceback Echo False-Pass** | High | `contains` searched over combined `stdout + stderr`. A traceback echoing the Python source line would match the needle. | Search `contains` exclusively in `check.stdout`. Stderr is strictly diagnostic. |
| **2. Passing-Check Supersession** | High | Author marks a failing check as superseded by an unrelated passing check. | Gate enforces that raw receipt check must fail the original predicate, and at least one replacement satisfies the target assertion. |
| **3. Sibling HEAD Drift** | Medium | Concurrent running siblings (tsukuroi, mado) modify working trees. | Gate does not query Git or inspect live sibling worktrees; it reads only local pinned round-13 receipts. |
| **4. Pinned Input Invalidation** | Medium | Edits to live `tools/*.py` would cause Tier 2 input hash checks to fail (exit 2). | Expected fail-closed behavior. Live tools must not be modified during round 14. Gate implementation lives in new file `tools/evidence-disposition.py`. |
| **5. Subprocess PATH Hijack in Selftest** | Low | Selftest invokes `python3` via ambient PATH. | Selftest uses `sys.executable` with `-I` (isolated mode) to invoke its own script path. |

---

## 8. Checks L1 Should Run (Deferred to Integration)

After Gate and DispositionSpec land their files:

1. **Isolated Selftest:**
   ```sh
   python3 tools/evidence-disposition.py --selftest
   ```
   *Expected:* Exit 0, `SELFTEST: PASS` with stable `EDS-*` finding IDs exercised across isolated fixtures.
2. **Negative Control Verification (`dispositions-before.json`):**
   ```sh
   python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions-before.json --json
   ```
   *Expected:* Exit 1, finding `EDS-PREDICATE-FAILED` on row `producer_before` (exit matches 1, `contains` fails). All other 11 rows effective and pass.
3. **Reconciled Verification (`dispositions.json`):**
   ```sh
   python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions.json --json
   ```
   *Expected:* Exit 0, 12 rows evaluated (11 effective passing, 1 superseded reconciled by `producer_before_oracle` and `producer_after_oracle`).
4. **File Difference Inspection:**
   ```sh
   diff -u .ufo/evidence/round-14/dispositions-before.json .ufo/evidence/round-14/dispositions.json
   ```
   *Expected:* Only `producer_before` row differs (state `effective` -> `superseded`, plus `reason` and `superseded_by`).
5. **Historical Integrity Audit:**
   ```sh
   git diff --quiet d6809df7775338f000e44c8a916067b8866867fb -- .ufo/evidence/round-12 .ufo/evidence/round-13 tools/mutate-and-run.sh SHONEN.md
   ```
   *Expected:* Exit 0 (zero modifications to historical evidence).
