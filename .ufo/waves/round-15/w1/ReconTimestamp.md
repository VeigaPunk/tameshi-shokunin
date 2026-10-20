# ReconTimestamp — Round 15 Wave 1 Scout Report

**Seat**: `TameshiR15.ReconTimestamp` (scout, leaf)  
**Role**: UFO-FSD scout — resolve one unknown from source evidence  
**Target**: Historical `capture-context.py` and retained `context-receipt.json` audit for ONLY `observed_at` volatile exclusion  
**Checks run**: None mid-flight (static inspection and analysis of committed bytes only; no gate, selftest, or tool execution)  
**Tool installs/updates**: None  

---

## 1. Godspeed Axes & Frontier Orientation

1. **Axes (from `SCORECARD.md` & `AXES.md`):**
   - **depth** (baseline **6** / 10; six recorded mutation cases in `tools/mutate-and-run.sh:84-89`)
   - **calibration** (baseline **6** / 8; C1 capability acquisition, lowest tied axis with depth; scalar 6 unchanged)
   - **coverage** (unpinned; F7 prerequisite open)
   - **operability** (runner regression and selftests intact)
   - **freshness** (unpinned; owner-readiness intake refusal maintained)
   - **adjacency** (strict boundary; sibling gates read-only, never absorbed)

2. **Frontier direction:**
   - Round 15 C1 calibration capability promotes `capture-context.py` to active gate `tools/context-capture.py` resolving outside round-14 routed defect 5 (proper gate classification, explicit exit 64 mapping, and standalone hermetic `--selftest` with literal expected exits and stable finding IDs).
   - Historical evidence under `.ufo/evidence/round-12..14/` remains strictly immutable.
   - This seat isolates and audits the volatile exclusion mechanism for `observed_at` to ground specification fixtures (`SpecTimestamp`) and review criteria (`ReviewTimestamp`).

---

## 2. Line and Key Citations

### 2.1 Historical Source: `tameshi-shokunin/.ufo/evidence/round-14/capture-context.py`

- **Line 6–8** (`Docstring contract`):  
  `"The emitted JSON documents are compared after removing ONLY the top-level observed_at. Any inequality is a mismatch; there is no retry and no A-B-A."`  
  Grounds the explicit design contract: volatility normalization is restricted strictly to a single top-level key.
- **Line 119–122** (`USAGE string`):  
  `"compare the pin probe's two observations minus the top-level observed_at, map the runner's six legs to the manifest, and write .ufo/evidence/round-14/context-receipt.json."`
- **Line 138–139** (`utc_now()`):  
  ```python
  def utc_now():
      return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  ```
  Generates ISO 8601 UTC second-precision timestamp for the receipt itself.
- **Line 357** (`comparison_block()` baseline validation):  
  ```python
  or "observed_at" not in base):
  ```
  Requires that the baseline probe output carries top-level `"observed_at"`. If missing, raises `InvalidContext("probe_baseline_unusable", "baseline probe run is not a six-leg ok pin-disposition-v1 document")`, routed to exit 2 (`status: invalid_input`) on lines 617–628.
- **Line 364–366** (`comparison_block()` receipt dictionary init):  
  ```python
  result = {
      "exclusions": ["observed_at"],
      "normalization": "top-level observed_at removed; canonical JSON compared",
      "observed_at": {"baseline": base.get("observed_at"), "injected": None},
      ...
  }
  ```
- **Line 376** (`comparison_block()` injected timestamp capture):  
  ```python
  result["observed_at"]["injected"] = injected.get("observed_at")
  ```
  Retains the injected timestamp for observable provenance rather than discarding it.
- **Line 377–380** (`comparison_block()` injected presence check):  
  ```python
  if "observed_at" not in injected:
      result["error"] = "injected document has no top-level observed_at"
      return result
  ```
  Missing `"observed_at"` in the injected document does not raise an exception; it populates `result["error"]` and leaves `result["equal"] = False`.
- **Line 384–386** (`comparison_block()` shallow copy and pop):  
  ```python
  base_cmp, inj_cmp = dict(base), dict(injected)
  base_cmp.pop("observed_at")
  inj_cmp.pop("observed_at")
  ```
  Operates on shallow dictionary copies. Deletes strictly the top-level key `"observed_at"`.
- **Line 387–391** (`comparison_block()` canonical dump and digest):  
  ```python
  base_text = json.dumps(base_cmp, sort_keys=True, separators=(",", ":"))
  inj_text = json.dumps(inj_cmp, sort_keys=True, separators=(",", ":"))
  result["baseline_comparable_sha256"] = sha256_bytes(base_text.encode())
  result["injected_comparable_sha256"] = sha256_bytes(inj_text.encode())
  result["equal"] = base_text == inj_text
  ```
- **Line 418** (`base_receipt()` initialization):  
  `"observed_at": utc_now(),` stamps top-level receipt generation time.
- **Line 560–563** (`decide()` mismatch check):  
  ```python
  if comparison.get("equal") is not True:
      reasons.append("injected observation differs from baseline after "
                     "excluding observed_at: {}".format(
                         comparison.get("error") or "normalized JSON mismatch"))
  ```
  Yields `("mismatch", 1, reasons)`, routing failure to exit 1.

---

### 2.2 Retained Evidence: `tameshi-shokunin/.ufo/evidence/round-14/context-receipt.json`

- **Line 5** (`top-level receipt key`):  
  `"observed_at": "2026-10-20T06:35:01Z"`
- **Line 83** (`embedded baseline stdout payload`):  
  `"observed_at": "2026-10-20T06:35:01Z"`
- **Line 97** (`embedded injected stdout payload`):  
  `"observed_at": "2026-10-20T06:35:01Z"`
- **Lines 99–116** (`comparison` block):  
  ```json
  "comparison": {
    "exclusions": [
      "observed_at"
    ],
    "normalization": "top-level observed_at removed; canonical JSON compared",
    "observed_at": {
      "baseline": "2026-10-20T06:35:01Z",
      "injected": "2026-10-20T06:35:01Z"
    },
    "raw_stdout_equal": true,
    "baseline_comparable_sha256": "22e79150fb56beb74902b1c9056e930db9bd76321488a39e7e82f3bc1d1261f9",
    "injected_comparable_sha256": "22e79150fb56beb74902b1c9056e930db9bd76321488a39e7e82f3bc1d1261f9",
    "payload_tool_sha256_matches_disk": true,
    "equal": true,
    "error": null
  }
  ```

---

## 3. Observable versus Inferred Behavior

### 3.1 Observable Behavior (Mechanically Proven by Source & Receipt Bytes)

1. **Exclusion Scope is Strictly Singular and Top-Level**:  
   Only the key `"observed_at"` is popped via `base_cmp.pop("observed_at")` and `inj_cmp.pop("observed_at")`. No nested dictionary keys, leg-level fields, status fields, commit hashes, or counts are altered or removed.
2. **Provenance Non-Suppression**:  
   The excluded timestamps are retained in the receipt structure (`comparison.observed_at.baseline` and `comparison.observed_at.injected`). The exclusion is purely operational for serialization comparison, not an erasure of provenance.
3. **Asymmetric Handling of Missing Key**:  
   - If the baseline probe output omits `"observed_at"`, it triggers `InvalidContext("probe_baseline_unusable", ...)`, returning exit code **2** (`could-not-evaluate` / `invalid_input`).  
   - If the injected probe output omits `"observed_at"`, it sets `comparison.error = "injected document has no top-level observed_at"` and returns `equal: False`, which `decide()` handles as a comparison failure, returning exit code **1** (`mismatch`).
4. **Canonical Form Comparison**:  
   Normalization sorts keys (`sort_keys=True`) and removes whitespace (`separators=(",", ":")`), producing SHA-256 digests `baseline_comparable_sha256` and `injected_comparable_sha256`. Equality holds if and only if those digests match.
5. **Historical Timing Coincidence**:  
   In round 14's retained receipt, both probe executions finished within the same second (`06:35:01Z`), resulting in `raw_stdout_equal: true`. The normalization code path was executed, but both raw and normalized documents were byte-identical in that specific historical run.

### 3.2 Inferred Behavior (Unenforced Assumptions & Non-Claims to Reject)

1. **Unenforced Timestamp Semantics & Monotonicity**:  
   The harness does not validate that `"observed_at"` is a valid ISO 8601 string, non-empty, or that `injected.observed_at >= baseline.observed_at`. Any JSON value (an empty string, integer, or invalid date) satisfies the presence check. Inferring that `"observed_at"` is validated for format or timeline monotonicity is false.
2. **Unearned Atomicity Claim**:  
   Excluding `observed_at` normalizes wall-clock variance between sequential probe executions; it does **not** prove atomic multi-repo inspection. If worktree bytes or commits change between runs, leg content will differ, correctly causing a mismatch.
3. **Unearned Environment Scrub Claim**:  
   Stripping `observed_at` and observing equality under `GIT_DIR` injection does **not** establish environment independence for unmeasured variables (`PATH`, toolchain, locales, or global configs). The receipt explicitly lists `not_compared` items.

---

## 4. Failure Cases Supported by Source Logic

### Primary Failure Case: Injected Probe Output Lacks `observed_at`
- **Mechanism**: The injected probe outputs a syntactically valid JSON document matching `pin-disposition-v1` schema and six legs, but omits the top-level `"observed_at"` property.
- **Source Path**: `capture-context.py:377–380`:
  ```python
  if "observed_at" not in injected:
      result["error"] = "injected document has no top-level observed_at"
      return result
  ```
- **Observable Verdict & Exit Code**:
  - `result["equal"]` remains `False`.
  - `decide()` triggers `reasons.append("injected observation differs from baseline after excluding observed_at: injected document has no top-level observed_at")`.
  - Final status: `"mismatch"`.
  - Exit code: **1**.
  - Stable finding ID / reason: `"mismatch"` with detail `"injected document has no top-level observed_at"`.

### Alternate Failure Case: Baseline Probe Output Lacks `observed_at`
- **Mechanism**: The baseline probe output omits `"observed_at"`.
- **Source Path**: `capture-context.py:357–361`:
  ```python
  or "observed_at" not in base):
      raise InvalidContext(
          "probe_baseline_unusable",
          "baseline probe run is not a six-leg ok pin-disposition-v1 document",
      )
  ```
- **Observable Verdict & Exit Code**:
  - Trapped by `main()` lines 617–628.
  - Final status: `"invalid_input"`.
  - Exit code: **2**.
  - Reason token: `"probe_baseline_unusable"`.

### Tertiary Failure Case: Unstripped Volatile Field Divergence
- **Mechanism**: If a probe mutant or updated tool emits an additional unstripped volatile field (e.g. `pid`, `duration_ms`, or per-leg `probed_at`), `base_cmp` and `inj_cmp` retain that field.
- **Source Path**: `capture-context.py:385–391`.
- **Observable Verdict & Exit Code**:
  - `base_text != inj_text` -> `result["equal"] = False`, `result["error"] = None`.
  - `decide()` appends `"injected observation differs from baseline after excluding observed_at: normalized JSON mismatch"`.
  - Final status: `"mismatch"`.
  - Exit code: **1**.

---

## 5. Bounded Recommendations

1. **For `ContextGate` (`tools/context-capture.py`)**:
   - **Preserve exact exclusion boundary**: Continue excluding ONLY `observed_at` from the root dictionary. Do not broaden the exclusion list or strip nested keys.
   - **Retain original timestamp provenance**: Maintain `comparison.observed_at.baseline` and `comparison.observed_at.injected` in the receipt.
   - **Hermetic `--selftest` coverage**:
     - Provide a test fixture where baseline and injected JSON strings differ *only* in `observed_at` (e.g., `2026-10-20T06:35:01Z` vs `2026-10-20T06:35:02Z`), confirming that normalized comparison evaluates to `equal: true` and exit 0.
     - Provide a test fixture where injected JSON omits `observed_at`, verifying exit 1 and the exact stable finding token `"injected document has no top-level observed_at"`.
2. **For `SpecTimestamp`**:
   - Pin the synthetic fixture to assert literal exit code **1** for missing injected timestamp and exit code **2** for missing baseline timestamp.
3. **For `ReviewTimestamp`**:
   - Reject any claim that `observed_at` exclusion validates ISO 8601 formatting, enforces clock monotonicity, or establishes multi-repo atomic snapshots.
