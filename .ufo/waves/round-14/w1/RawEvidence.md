# Round 14 w1 — RawEvidence: historical round-13 evidence inventory and parser contract

Lane: tameshi-shokunin. Seat: `TameshiR14.RawEvidence` (leaf, read-only scout).
Files inspected:
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/expected.json`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/verification.json`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/producer-oracle-repair.json`
- Supplementary: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/verification-verdict.json`

Checks run mid-flight: **none** (zero executions of gates, runners, probes, or python scripts; only static file reads and JSON structural analysis). Tool installs/updates: **none**.

---

## 1. Cardinality audit: Expected count is 12, not 13

### Root Cause of the "13" Ambiguity
The round-14 wave prompt and `spec.json` mention *"All13 expected rows effective except producer_before superseded in after."* This conflates three distinct counts:
1. `expected.json` **`inputs` map** has **13 entries** (the 13 measured input digests verified in the round-13 closure note).
2. `verification.json` **`checks` array** has **13 check objects** (10 matching `expected_checks` + 3 unmapped checks).
3. `expected.json` **`expected_checks` map** has **exactly 12 keys**.

Across all receipts (`verification.json` and `producer-oracle-repair.json`), there are **15 total check executions**.

### Dispositions Row Partition
`dispositions.json` must map the 12 keys of `expected_checks` into:
- **11 effective rows**: `pin_selftest`, `metadata_selftest`, `metadata_old_null`, `metadata_corrected`, `producer_before_oracle`, `producer_after_oracle`, `producer_after`, `witness_check`, `witness_count`, `pin_live`, `source_census`.
- **1 superseded row**: `producer_before` (superseded by `producer_before_oracle` and `producer_after_oracle`).
- **Total: 12 rows**. Fabricating a 13th row to satisfy literal prompt wording would invent an unbacked expectation.

---

## 2. Complete Inventory of `expected.json` (12 expected_checks)

Top-level metadata:
- `schema`: `"tameshi-round13-evidence-v1"`
- `baseline`: `"546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50"`
- `inputs`: 13 digest-pinned paths (`round-12` inputs, 4 tools, manifest, companions, producer, oracle).
- `expected_checks`: 12 keys.

| Key | Expected Fields & Types | Target Receipt File | Receipt Check Name |
|---|---|---|---|
| `pin_selftest` | `exit`: 0 (`int`), `contains`: `"SELFTEST: PASS (18/18)"` (`str`) | `verification.json` | `pin_selftest` |
| `metadata_selftest` | `exit`: 0 (`int`), `contains`: `"SELFTEST: PASS 39/39"` (`str`) | `verification.json` | `metadata_selftest` |
| `metadata_old_null` | `exit`: 1 (`int`), `id`: `"metadata_inconsistent"` (`str`), `reason`: `"normalized_kind_null"` (`str`) | `verification.json` | `metadata_old_null` |
| `metadata_corrected` | `exit`: 0 (`int`), `id`: `"metadata_consistent"` (`str`) | `verification.json` | `metadata_corrected` |
| `producer_before` | `exit`: 1 (`int`), `contains`: `"summary preserves top-level exposed declaration kind"` (`str`) | `verification.json` | `producer_before` (stale/superseded) |
| `producer_before_oracle` | `exit`: 1 (`int`), `contains`: `"summary preserves top-level exposed declaration kind FAIL"` (`str`) | `producer-oracle-repair.json` | `producer_before_oracle` |
| `producer_after_oracle` | `exit`: 0 (`int`), `contains`: `"WITNESS_SELFTEST: 41/41 pass"` (`str`) | `producer-oracle-repair.json` | `producer_after_oracle` |
| `producer_after` | `exit`: 0 (`int`), `contains`: `"WITNESS_SELFTEST: 41/41 pass"` (`str`) | `verification.json` | `producer_after` |
| `witness_check` | `exit`: 0 (`int`), `contains`: `"WITNESS_CHECK: CLEAN"` (`str`) | `verification.json` | `witness_check` |
| `witness_count` | `exit`: 0 (`int`), `contains`: `"witness_classified=10"` (`str`) | `verification.json` | `witness_count` |
| `pin_live` | `exit`: 0 (`int`), `rows`: 6 (`int`), `result_reuse`: `"not_established"` (`str`), `statuses`: `{"changed": 3, "unavailable": 0, "unchanged": 3}` (`dict[str, int]`) | `verification.json` | `pin_live` |
| `source_census` | `exit`: 0 (`int`) | `verification.json` | `source_census` |

Field taxonomy in `expected_checks`:
- `exit`: present in all 12 keys (100%).
- `contains`: present in 8 keys (`pin_selftest`, `metadata_selftest`, `producer_before`, `producer_before_oracle`, `producer_after_oracle`, `producer_after`, `witness_check`, `witness_count`).
- `id`: present in 2 keys (`metadata_old_null`, `metadata_corrected`).
- `reason`: present in 1 key (`metadata_old_null`).
- `rows`: present in 1 key (`pin_live`).
- `statuses`: present in 1 key (`pin_live`).
- `result_reuse`: present in 1 key (`pin_live`).

---

## 3. Receipt Inventory & Coverage Gap Analysis

### 3.1. `verification.json` (13 checks)
Schema: `"tameshi-round13-verification-v1"`.
Check records have uniform shape: `name` (`str`), `argv` (`list[str]`), `started_at` (`str`), `exit` (`int`), `expected_exit` (`int`), `exit_matches` (`bool`), `stdout` (`str`), `stderr` (`str`).

Checks mapping:
- **10 map to `expected_checks`**: `pin_selftest`, `metadata_selftest`, `metadata_old_null`, `metadata_corrected`, `producer_before`, `producer_after`, `witness_check`, `witness_count`, `pin_live`, `source_census`.
- **3 unmapped checks**:
  1. `pin_env_scrub`: identical argv to `pin_live`; exit 0; stdout byte-identical to `pin_live`.
  2. `metadata_emit`: runs `tools/witness-metadata.py --emit`; exit 0; outputs companion JSON.
  3. `frozen_and_guardrail_unchanged`: runs `git diff --quiet 546b371...`; exit 0.

### 3.2. `producer-oracle-repair.json` (2 checks)
Schema: `"tameshi-round13-producer-oracle-repair-v1"`.
- `producer_before_oracle`: exit 1, expected_exit 1; stdout contains regression assertion FAIL; final line `WITNESS_SELFTEST: 40/41 pass`, `VERDICT: FAIL`.
- `producer_after_oracle`: exit 0, expected_exit 0; stdout contains regression assertion ok; final line `WITNESS_SELFTEST: 41/41 pass`, `VERDICT: PASS`.
Both map to `expected_checks`.

### 3.3. Phantom verdict checks
In `verification-verdict.json`, check list contains `baseline_final_count` (`matched: true`).
**Critical finding:** `baseline_final_count` exists in **neither** `verification.json` **nor** `producer-oracle-repair.json`. It is an unbacked verdict claim and must not be accepted by the gate as a valid check.

---

## 4. Unsupported Fields and Parser Requirements

### 4.1. Receipts do not carry structured predicate keys as top-level dict keys
A naive checker inspecting `check["id"]`, `check["rows"]`, or `check["statuses"]` will crash with `KeyError` or fail:
1. **`id` and `reason`** live inside `metadata_old_null.stdout` and `metadata_corrected.stdout` as JSON strings:
   - `metadata_old_null.stdout`: `{"companion": "...", "detail": "", "exit": 1, "id": "metadata_inconsistent", "reason": "normalized_kind_null"}`
   - `metadata_corrected.stdout`: `{"companion": "...", ..., "exit": 0, "id": "metadata_consistent", ..., "reason": "ok"}`
   - **Parser requirement**: Gate must parse `check["stdout"]` with `json.loads()` and extract `stdout_json.get("id")` and `stdout_json.get("reason")`.
2. **`rows`, `statuses`, and `result_reuse`** live inside `pin_live.stdout` as a JSON string:
   - Top-level `pin_live.stdout` keys: `schema`, `tool`, `tool_sha256`, `status`, `observed_at`, `manifest`, `root`, `result_reuse`, `result_reuse_reason`, `not_compared`, `counts`, `legs`.
   - `rows`: must be checked against `len(stdout_json.get("legs", []))` or `stdout_json.get("counts", {}).get("legs")` (both equal 6).
   - `statuses`: in `stdout_json["counts"]`, keys are `{"unchanged": 3, "changed": 3, "unavailable": 0, "legs": 6}`. Parser must verify `counts["changed"] == 3`, `counts["unchanged"] == 3`, `counts["unavailable"] == 0` (or derive counts from `legs[].content_status`).
   - `result_reuse`: top-level `stdout_json.get("result_reuse") == "not_established"` (and optionally each leg's `result_reuse`).
   - **Parser requirement**: Gate must parse `pin_live.stdout` with `json.loads()` and navigate to `counts` and `legs`.

### 4.2. Exact Predicate Parsing Rules
- **Exit code**:
  - Must compare `check["exit"] == expected["exit"]`.
  - Type strictness: `type(check["exit"]) is int and not isinstance(check["exit"], bool)`. In Python, `isinstance(True, int)` is `True` and `True == 1`, which could yield false-positive passes on exit 1 if boolean values leak in.
- **`contains` substring match**:
  - Substring check: `expected["contains"] in check["stdout"]`.
  - Must NOT match against `stderr`.
- **Receipt `exit_matches` boolean**:
  - Gate must **ignore** `check.get("exit_matches")`. It is self-attested by the historical runner and masks mechanism failures (such as `producer_before`).
- **Unsupported fields in expected checks**:
  - The gate must fail-closed if any key in `expected_checks[name]` is outside the set `{"exit", "contains", "id", "reason", "rows", "statuses", "result_reuse"}`.

### 4.3. The `producer_before` Stale Failure Mechanism
In `verification.json`:
- `exit`: 1 (matches expected exit 1; `exit_matches`: true).
- `stderr`: contains `FileNotFoundError: ... '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/tools/mutate-and-run.sh'`.
- `stdout`: cuts off after `check mutant digest mismatch refuses ok`. Does **NOT** contain `"summary preserves top-level exposed declaration kind"`.
- **Result**: `producer_before` is a path-layout crash before reaching the assertion.
- When evaluated as an effective row against `expected.json`, `producer_before` **FAILS** the `contains` check!
- This gives the exact red/green discriminator required for the round-14 reconciliation:
  - `dispositions-before.json` (where `producer_before` is effective) fails with exit 1 and finding `expected_contains_mismatch`.
  - `dispositions.json` (where `producer_before` is superseded by `producer_before_oracle` and `producer_after_oracle`) passes with exit 0.

---

## 5. Advisory to Gate (`tools/evidence-disposition.py`) and Spec (`dispositions.json`)

### Advice to Gate (`tools/evidence-disposition.py`)
1. **Universe of expectations**: Anchor strictly on `expected.json["expected_checks"]` (12 entries). Enforce that `dispositions.json` contains exactly 1 row per expected check (total 12).
2. **Supersession semantics**:
   - For superseded rows, enforce `state == "superseded"`, non-empty `reason`, and `superseded_by` containing valid effective check names (`["producer_before_oracle", "producer_after_oracle"]`).
   - Gate must verify that every replacement named in `superseded_by` is itself an effective row that passes its own expectation.
   - Retain the raw superseded check record in the disposition and verify that it matches raw receipt bytes.
3. **Receipt checking without execution**:
   - Verify input digests (all 13 inputs from `expected.json` + `verification.json` + `producer-oracle-repair.json`) before executing predicates.
   - Do NOT run receipt `argv`.
4. **Receipt check coverage classification**:
   - 11 checks: matched effective.
   - 1 check (`producer_before`): matched superseded.
   - 3 checks (`pin_env_scrub`, `metadata_emit`, `frozen_and_guardrail_unchanged`): classify as `unmapped_receipt_check`, ensuring they are neither treated as expected checks nor silently dropped.
   - Reject `baseline_final_count` as an unknown/unbacked check name.
5. **Exit codes and stable finding IDs**:
   - Exit 0: all dispositions match.
   - Exit 1: semantic failure (e.g., `predicate_mismatch`, `superseded_replacement_failed`, `missing_expected_row`, `unexpected_disposition_row`).
   - Exit 2: evaluation blocked (e.g., `input_digest_mismatch`, `receipt_missing`, `json_malformed`, `path_traversal`).
   - Exit 64: usage error.

### Advice to DispositionSpec (`dispositions-before.json` & `dispositions.json`)
1. **Cardinality**: Explicitly state **12 expected rows** (11 effective + 1 superseded). Explain in the report why prompt's "All13" is a historical conflation of 13 inputs / 13 verification checks.
2. **Schema structure**:
   ```json
   {
     "schema": "evidence-dispositions-v1",
     "expected_file": ".ufo/evidence/round-13/expected.json",
     "inputs": {
       ".ufo/evidence/round-13/expected.json": "b771...",
       ".ufo/evidence/round-13/verification.json": "0d58...",
       ".ufo/evidence/round-13/producer-oracle-repair.json": "0a45..."
     },
     "rows": [ ... 12 rows ... ]
   }
   ```
3. **`dispositions-before.json`**:
   - All 12 rows set `state: "effective"`.
   - `producer_before` points to `receipt: ".ufo/evidence/round-13/verification.json"` and `check: "producer_before"`.
   - When run against the gate, this file must fail on `producer_before` (`contains` missing).
4. **`dispositions.json`**:
   - 11 rows `state: "effective"`.
   - `producer_before` set `state: "superseded"`, `reason: "path-layout FileNotFoundError before target assertion"`, `superseded_by: ["producer_before_oracle", "producer_after_oracle"]`, `raw_receipt: ".ufo/evidence/round-13/verification.json"`, `raw_check: "producer_before"`.
   - When run against the gate, this file must pass with exit 0.

---

## 6. Concrete Changes, Risks, and Checks for L1

### Concrete Changes
- Dispositions file must define 12 rows corresponding to the 12 keys of `expected_checks`.
- Gate must parse JSON in stdout for `id`, `reason`, `rows`, `statuses`, `result_reuse`.
- Gate must treat `contains` as a strict substring check on `stdout` and ignore self-reported `exit_matches: true`.

### Residual Risks
1. **Over-filtering / Schema Mismatch**: If Gate assumes receipt checks contain top-level `id` or `statuses`, all structured checks will fail.
2. **Input Coverage Gap**: `verification.json`'s `measured_input_sha256` only pinned 12 of the 13 inputs (omitted `producer-oracle.py`). `dispositions.json` must pin `expected.json` and both receipts.
3. **Phantom Verdict Name**: If Gate looks at `verification-verdict.json`, it will encounter `baseline_final_count`, which does not exist in any receipt. Gate should evaluate against receipts directly.

### Checks L1 Should Run (Deferred to Integration Phase)
1. **Digest verification of evidence inputs**:
   ```sh
   python3 -c "import hashlib, json; exp = json.load(open('.ufo/evidence/round-13/expected.json')); print('mismatches:', [p for p,h in exp['inputs'].items() if hashlib.sha256(open(p,'rb').read()).hexdigest() != h])"
   ```
   Must return `mismatches: []`.
2. **Gate selftest**:
   ```sh
   python3 tools/evidence-disposition.py --selftest
   ```
   Must exit 0 with all isolated fixture test cases passing.
3. **Gate evaluation of before-state (Negative Control)**:
   ```sh
   python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions-before.json --json
   ```
   Must exit 1, reporting failure on `producer_before`.
4. **Gate evaluation of after-state (Target Capability)**:
   ```sh
   python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions.json --json
   ```
   Must exit 0 with all 12 expectations satisfied (11 effective, 1 superseded).
5. **Guardrail check**:
   ```sh
   git diff --quiet d6809df7775338f000e44c8a916067b8866867fb -- .ufo/evidence/round-12 .ufo/evidence/round-13 tools/mutate-and-run.sh
   ```
   Must exit 0, confirming historical evidence is byte-identical.
