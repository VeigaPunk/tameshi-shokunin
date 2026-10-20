# ReconNames — equal-valued REV variable name mismatch reconnaissance

## Finding and relevant axes

Historical `capture-context.py` and retained `context-receipt.json` enforce variable name identity in addition to commit hash equality for runner-to-manifest mapping. Because two distinct pairs of legs share identical commit hashes across the runner's six legs, comparing resolved commit values alone would allow misbound variables to pass undetected. The historical source discriminates name mismatches statically via regex parsing of `tools/mutate-and-run.sh` without executing the runner.

Relevant axes:
- **Calibration (primary):** verified discernment between equal-valued variable bindings; calibration capability preserved without scalar inflation (6→6).
- **Operability:** explicit contract for the promoted `tools/context-capture.py` gate, preserving the exit classification (`0` ok, `1` mismatch, `2` invalid/could-not-evaluate, `64` usage).
- **Depth / Coverage / Freshness / Adjacency (bounds):** zero new mutation cases or target depth claims; no unapproved successor sweep; sibling trees read-only; no execution of sibling gates or runner mid-flight.

---

## Evidence chain: lines and keys

### 1. Equal-valued REV constants in `tools/mutate-and-run.sh`
In `tools/mutate-and-run.sh:542-555`, six git revision constants are declared:
- **Pair 1 (`kagi-shokunin`):**
  - Line 545: `REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e` (bound to leg `bash-surface-census`, line 1118)
  - Line 551: `REV_CHECKLIST=fecee8743e52eb8fb5fbb40782934cb619a1a96e` (bound to leg `bash-checklist-run`, line 1133)
  - `REV_BASH == REV_CHECKLIST`
- **Pair 2 (`kumitate-shokunin`):**
  - Line 543: `REV_JS=175de6ba2e9e904010411b19cab27e0af9aad3d4` (bound to leg `js-kimi-census`, line 1113)
  - Line 553: `REV_CLAIMS=175de6ba2e9e904010411b19cab27e0af9aad3d4` (bound to leg `js-claims-check`, line 1138)
  - `REV_JS == REV_CLAIMS`

### 2. Name-checking logic in `.ufo/evidence/round-14/capture-context.py`
- **Lines 71-81 (`EXPECTED_SUFFIX` table):**
  Explicitly documents the rationale:
  `# REV_BASH == REV_CHECKLIST and REV_JS == REV_CLAIMS, so the intended variable`
  `# NAME per leg is checked, not only the resolved value.`
  Maps each of the six legs to its expected suffix: `"JS"`, `"BASH"`, `"TSUKUROI"`, `"MADO"`, `"CHECKLIST"`, `"CLAIMS"`.
- **Lines 89-106 (Regex parsing):**
  - Line 90: `REV_CONST_RE = re.compile(r"^(REV_[A-Z0-9_]+)=([0-9a-f]{40})$", re.MULTILINE)`
  - Lines 93-101: `CALL_RE` captures `"\\$REV_(?P<rev>[A-Z0-9_]+)"` into `rev_suffix`.
  - Lines 104-106: `RUN_REGRESSION_RE` captures the body of `run_regression()`.
- **Lines 109-115 (`CHECKS` definition):**
  Includes `rev_name_and_value_match_manifest` and `constant_names_match_leg`.
- **Lines 214-258 (`parse_runner_mapping`):**
  Extracts `pins`, `revs`, and `calls`. Validates that exactly 6 unique `PIN_` and 6 unique `REV_` constants exist in the runner text (`:247-249`).
- **Lines 259-338 (`mapping_block`):**
  - Line 273: `rev_name = "REV_" + call["rev_suffix"]`
  - Line 276: `rev_value = parsed["revs"].get(rev_name)`
  - Lines 286-289:
    ```python
    checks["rev_name_and_value_match_manifest"] = (
        suffix is not None and rev_name == "REV_" + suffix
        and rev_value == manifest["pinned_commit"]
    )
    ```
  - Lines 290-294:
    ```python
    checks["constant_names_match_leg"] = (
        suffix is not None
        and call["pin_suffix"] == call["rev_suffix"] == call["table_suffix"] == suffix
    )
    ```
  - Line 312: `"match": all(checks.values())`
  - Lines 320-323: On check failure, appends failed check names to `reasons`:
    `"leg {}: {}".format(row["leg"], ", ".join(failed))`
  - Line 335: `"all_match": set_equal and order_equal and all(row["match"] for row in rows)`
- **Lines 553-580 (`decide`):**
  - Lines 576-577: `if not mapping.get("all_match"): reasons.extend(mapping.get("reasons") or ["runner mapping mismatch"])`
  - Lines 578-579: `if reasons: return "mismatch", 1, reasons`
  - Emits exit code `1` and status `"mismatch"`.

### 3. Retained evidence in `.ufo/evidence/round-14/context-receipt.json`
- **Mapping block keys (`:191-414`):**
  - Schema: `"runner-leg-mapping-v1"` (`:193`)
  - Target: `"tools/mutate-and-run.sh"` (`:194`)
  - Parsed summary: `header_rows: 6, pin_constants: 6, rev_constants: 6, leg_calls: 6` (`:195-200`)
  - Declared suffix table: `"declared_variable_table"` (`:331` in generator, present in receipt)
- **Per-leg keys (`:209-410`):**
  For both equal-valued legs:
  - `bash-surface-census` (`:240-273`):
    - `declared_variable_suffix`: `"BASH"`
    - `runner_call.rev_constant`: `"REV_BASH"`
    - `rev_value`: `"fecee8743e52eb8fb5fbb40782934cb619a1a96e"`
    - `checks.rev_name_and_value_match_manifest`: `true` (`:267`)
    - `checks.constant_names_match_leg`: `true` (`:270`)
    - `match`: `true` (`:272`)
  - `bash-checklist-run` (`:342-375`):
    - `declared_variable_suffix`: `"CHECKLIST"`
    - `runner_call.rev_constant`: `"REV_CHECKLIST"`
    - `rev_value`: `"fecee8743e52eb8fb5fbb40782934cb619a1a96e"`
    - `checks.rev_name_and_value_match_manifest`: `true` (`:369`)
    - `checks.constant_names_match_leg`: `true` (`:371`)
    - `match`: `true` (`:373`)
- **Aggregate receipt verdict (`:411-423`):**
  - `"all_match": true` (`:411`)
  - `"reasons": []` (`:412`)
  - `"status": "ok"` (`:421`)
  - `"exit": 0` (`:422`)

---

## Observable versus inferred behavior

### Observable facts (what source text and retained receipt demonstrate)
1. **Static AST/regex text matching:** `capture-context.py` only reads `tools/mutate-and-run.sh` as text. It searches for regex patterns inside `run_regression()`.
2. **Dual-constraint enforcement:** To achieve `all_match=true`, the runner call must satisfy:
   - Value constraint: `rev_value == manifest["pinned_commit"]`
   - Name constraint: `rev_name == "REV_" + suffix`
   - Co-occurrence constraint: `call["pin_suffix"] == call["rev_suffix"] == call["table_suffix"] == suffix`
3. **Discriminator action:** When a swapped variable name is encountered (e.g. `$REV_CHECKLIST` in `bash-surface-census`), the value constraint is satisfied, but both the name constraint and co-occurrence constraint evaluate to `false`.
4. **Deterministic exit:** A mapping mismatch triggers `all_match=false`, appending the failure to `reasons`, which directly causes `decide()` to return `("mismatch", 1, reasons)`. The process exits with code `1`.

### Inferred behavior (what source does NOT demonstrate and must NOT be claimed)
1. **No dynamic execution of the runner:** `capture-context.py` never executes `mutate-and-run.sh` (`"The runner is never run"`, `:13`). It does not observe whether bash executes or fails.
2. **No runtime divergence:** Because `REV_BASH` and `REV_CHECKLIST` expand to the exact same 40-hex commit hash, dynamic bash execution of `git show "$REV_BASH":...` versus `git show "$REV_CHECKLIST":...` would produce byte-identical git objects. The discriminator detects semantic/provenance misbinding, not dynamic git failure.
3. **No claim of variable interchangeability:** One must not infer that equal values make variable names fungible; the contract requires strict leg-to-manifest variable provenance.
4. **No broader suite claims:** Static verification of constant names does not prove mutation kill rates, test execution, or environment independence.

---

## Supported failure case

### Description
In `tools/mutate-and-run.sh`, inside `run_regression()`, substitute the call parameter for leg `bash-surface-census` from `"$REV_BASH"` to `"$REV_CHECKLIST"`:

```bash
# Line 1118 mutated:
regression_case_git bash-surface-census \
  'kagi-shokunin/corpus/surface-census.sh' "$PIN_BASH" "$REV_CHECKLIST" \
  "$specs/bash-surface-census.spec" 'bash "$MUTANT" --selftest' "$TABLE_BASH" \
  "$root/bash-surface-census"
```

### Trace through `capture-context.py`
1. `CALL_RE` parses the line: `pin_suffix="BASH"`, `rev_suffix="CHECKLIST"`, `table_suffix="BASH"`.
2. `parsed["revs"]` contains `"REV_CHECKLIST": "fecee8743e52eb8fb5fbb40782934cb619a1a96e"`.
3. In `mapping_block()`:
   - `suffix = EXPECTED_SUFFIX["bash-surface-census"] = "BASH"`.
   - `rev_name = "REV_CHECKLIST"`.
   - `rev_value = "fecee8743e52eb8fb5fbb40782934cb619a1a96e"`.
   - `manifest["pinned_commit"] = "fecee8743e52eb8fb5fbb40782934cb619a1a96e"`.
   - Value equality holds: `rev_value == manifest["pinned_commit"]` is `True`.
   - Name equality fails: `rev_name == "REV_" + suffix` (`"REV_CHECKLIST" == "REV_BASH"`) is `False`.
   - Co-occurrence fails: `call["pin_suffix"] == call["rev_suffix"]` (`"BASH" == "CHECKLIST"`) is `False`.
   - Consequently:
     - `checks["rev_name_and_value_match_manifest"] = False`
     - `checks["constant_names_match_leg"] = False`
     - `row["match"] = False`
     - `reasons.append("leg bash-surface-census: rev_name_and_value_match_manifest, constant_names_match_leg")`
     - `all_match = False`
4. In `decide()`:
   - `mapping.get("all_match")` is `False`.
   - `decide()` returns `("mismatch", 1, ["leg bash-surface-census: rev_name_and_value_match_manifest, constant_names_match_leg"])`.
5. In `main()`:
   - `receipt` is written with `"status": "mismatch"`, `"exit": 1`.
   - Process exits with code `1`.

### Historical corroboration
This failure case was recorded as an exercised guardrail check in `.ufo/evidence/round-14/guardrails.json:36-48`:
- Check name: `runner_variable_swap_discriminator`
- Execution: mutated `tools/mutate-and-run.sh` replacing `"$REV_BASH"` with `"$REV_CHECKLIST"`, ran `mapping_block()`, and asserted `not out["all_match"] and not row["checks"]["constant_names_match_leg"]`.
- Output: `runner_variable_swap_rejected: equal REV values do not hide wrong binding`.

---

## Bounded recommendations for active `tools/context-capture.py`

1. **Preserve dual name and value matching:**
   In promoting the historical script to `tools/context-capture.py`, retain both `rev_name_and_value_match_manifest` and `constant_names_match_leg`. Do not simplify to value-only comparison.
2. **Incorporate into standalone hermetic `--selftest`:**
   Implement an isolated synthetic fixture test exercising this exact case:
   - Construct a synthetic runner fixture with equal-valued `REV_BASH` and `REV_CHECKLIST` where `"$REV_CHECKLIST"` is mistakenly bound to the `bash-surface-census` call.
   - Run the public CLI against the synthetic tree.
   - Assert exit code `1`, status `"mismatch"`, and finding reason citing the mapping failure.
3. **Maintain strict exit classification:**
   - Exit `0`: matching context, effective poison control, and clean six-leg mapping.
   - Exit `1`: mismatch (including mapping failure or volatile exclusion inequality).
   - Exit `2`: could-not-evaluate (missing input, malformed JSON, poison path already present).
   - Exit `64`: usage error (unexpected CLI arguments; no receipt written).
4. **Historical integrity:**
   Do not modify or rerun round-14 historical evidence (`.ufo/evidence/round-14/*`). All prospective captures belong under round-15 paths.

---

## Method and confidence

- **Confidence:** High. All citations are taken directly from committed historical artifacts (`.ufo/evidence/round-14/capture-context.py`, `.ufo/evidence/round-14/context-receipt.json`, `.ufo/evidence/round-14/guardrails.json`, and `tools/mutate-and-run.sh`).
- **Tool execution disclosure:** In conformance with the target contract, **no verification execution** was run (no Python scripts, no bash runner, no git commits, no gates).
- **LSP status:** LSP navigation was unavailable (`xd://lsp` not mounted); analysis performed via direct file reading.
- **Tools installed/updated:** None.
