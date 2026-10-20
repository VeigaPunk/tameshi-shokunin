# RunnerMappings — Independent Tabulation & Extraction Trap Analysis

**Seat:** `TameshiR14.RunnerMappings` (Scout)  
**Round:** Tameshi Round 14, Wave 1  
**Target:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh`  
**Target Digest:** SHA-256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`  
**Target Version:** `mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)` (line 158)  
**Manifest Baseline:** `.ufo/evidence/round-13/pin-manifest.json` (`schema: pin-manifest-v1`)  
**Report Output Path:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-14/w1/RunnerMappings.md`  
**Tool Installs / Upgrades:** None (zero external packages or system modifications).

---

## 1. Axes & Posture (Godspeed)

1. **Calibration ($C_1$):** Establish an exact, non-ambiguous, byte-grounded tabulation of all six mutation legs in `tools/mutate-and-run.sh` (target path, repo, relative path, commit pin, blob pin, defect spec, test suite command, and expectation table). This ensures that `ReceiptHarness` (`capture-context.py`) captures verifiable value equality against `pin-manifest.json` rather than superficial variable existence.
2. **Depth ($C_2$):** Systematically uncover and categorize structural extraction traps in `tools/mutate-and-run.sh`—including non-uniform variable suffix naming, multi-leg commit reuse, line continuations, indirection through variables, and selftest mock-call collisions—so the automated harness does not fail or produce false positives.
3. **Non-interference & Leaf Discipline:** Zero target executions, zero modification of historical evidence or runner source code. No subagent delegation. Mid-flight checks are deferred strictly to L1 integration.

---

## 2. Independent Tabulation of the Six Mutation Legs

All facts below are extracted directly from `tools/mutate-and-run.sh` without execution. The six recorded legs appear in executable code in `run_regression()` (lines 1112–1140) and correspond to constants declared at lines 542–559.

### Master Leg Mapping Table

| Leg # | Canonical Leg Name | Fleet-Relative Path (`rel`) | Repo (`${rel%%/*}`) | Path in Repo (`${rel#*/}`) | Pin Variable (`PIN_*`) | Pinned Blob SHA-256 (64-hex) | Rev Variable (`REV_*`) | Pinned Commit (`REV_*`, 40-hex) | Suite Command (`suite`) | Expectation Table (`TABLE_*`) | Defect Tally (K/S/Total) | Kill Rate |
|:---:|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---:|:---:|
| 1 | `js-kimi-census` | `kumitate-shokunin/scripts/kimi-census.mjs` | `kumitate-shokunin` | `scripts/kimi-census.mjs` | `PIN_JS` (line 542) | `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426` | `REV_JS` (line 543) | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `node "$MUTANT" --selftest` | `TABLE_JS` (line 554) | 8K / 2S / 10 | 80% |
| 2 | `bash-surface-census` | `kagi-shokunin/corpus/surface-census.sh` | `kagi-shokunin` | `corpus/surface-census.sh` | `PIN_BASH` (line 544) | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` | `REV_BASH` (line 545) | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `bash "$MUTANT" --selftest` | `TABLE_BASH` (line 555) | 8K / 2S / 10 | 80% |
| 3 | `bash-tsukuroi-census` | `tsukuroi-shokunin/tools/tsukuroi-census.sh` | `tsukuroi-shokunin` | `tools/tsukuroi-census.sh` | `PIN_TSUKUROI` (line 546) | `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5` | `REV_TSUKUROI` (line 547) | `165307fe4746a8807b02ec4a7d7ecac0368454a6` | `bash "$MUTANT" --selftest` | `TABLE_TSUKUROI` (line 556) | 6K / 4S / 10 | 60% |
| 4 | `bash-mado-verify` | `mado-shokunin/tools/mado-verify.sh` | `mado-shokunin` | `tools/mado-verify.sh` | `PIN_MADO` (line 548) | `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` | `REV_MADO` (line 549) | `eead56b20ad2b28299ae4fa623d52a99b44c743c` | `bash "$MUTANT" --selftest` | `TABLE_MADO` (line 557) | 4K / 6S / 10 | 40% |
| 5 | `bash-checklist-run` | `kagi-shokunin/corpus/checklist-run.sh` | `kagi-shokunin` | `corpus/checklist-run.sh` | `PIN_CHECKLIST` (line 550) | `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` | `REV_CHECKLIST` (line 551) | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `bash "$MUTANT" --selftest` | `TABLE_CHECKLIST` (line 558) | 7K / 8S / 15 | 47% |
| 6 | `js-claims-check` | `kumitate-shokunin/scripts/claims-check.mjs` | `kumitate-shokunin` | `scripts/claims-check.mjs` | `PIN_CLAIMS` (line 552) | `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` | `REV_CLAIMS` (line 553) | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `node "$MUTANT" --selftest` | `TABLE_CLAIMS` (line 559) | 7K / 3S / 10 | 70% |

---

## 3. Callsite Structure & Invocation Geometry

### Definition of `regression_case_git` (lines 1061–1072)

```bash
1061: regression_case_git() {
1062:   # <name> <fleet-relative-target> <pin> <rev> <spec> <suite> <recorded-table>
1063:   #   <case-workdir>
...
1068:   local name=$1 rel=$2 pin=$3 rev=$4 spec=$5 suite=$6 table=$7 cwd=$8
1069:   local repo="$FLEET_ROOT/${rel%%/*}" path="${rel#*/}"
1070:   regression_case "$name" "$FLEET_ROOT/$rel" "$pin" "$spec" "$suite" "$table" "$cwd" \
1071:     "$repo" "$rev" "$path" 0 0
1072: }
```

Key characteristics:
1. **Positional Argument Ordering:**
   - `$1` = `name` (canonical leg identifier)
   - `$2` = `rel` (fleet-relative path, e.g. `'kumitate-shokunin/scripts/kimi-census.mjs'`)
   - `$3` = `pin` (dereferenced variable expansion `"$PIN_*"`)
   - `$4` = `rev` (dereferenced variable expansion `"$REV_*"`)
   - `$5` = `spec` (path to defect spec file, `"$specs/<name>.spec"`)
   - `$6` = `suite` (suite command string, e.g. `'node "$MUTANT" --selftest'`)
   - `$7` = `table` (verdict table variable expansion `"$TABLE_*"`)
   - `$8` = `cwd` (per-case working directory, `"$root/<name>"`)
2. **Path Decomposition:**
   - Repo directory: `repo="$FLEET_ROOT/${rel%%/*}"` (extracts head component up to first `/`)
   - Repo-relative path: `path="${rel#*/}"` (extracts tail component after first `/`)
3. **Exact Tolerance Arm:**
   - The final two arguments to `regression_case` are `0 0`, enforcing zero kill-rate delta (`ktol=0`) and zero verdict flips (`ftol=0`).

### Six Actual Invocations in `run_regression()` (lines 1112–1141)

```bash
1112:   regression_case_git js-kimi-census \
1113:     'kumitate-shokunin/scripts/kimi-census.mjs' "$PIN_JS" "$REV_JS" \
1114:     "$specs/js-kimi-census.spec" 'node "$MUTANT" --selftest' "$TABLE_JS" \
1115:     "$root/js-kimi-census"
1116:   st_js=$?
1117:   regression_case_git bash-surface-census \
1118:     'kagi-shokunin/corpus/surface-census.sh' "$PIN_BASH" "$REV_BASH" \
1119:     "$specs/bash-surface-census.spec" 'bash "$MUTANT" --selftest' "$TABLE_BASH" \
1120:     "$root/bash-surface-census"
1121:   st_kagi=$?
1122:   regression_case_git bash-tsukuroi-census \
1123:     'tsukuroi-shokunin/tools/tsukuroi-census.sh' "$PIN_TSUKUROI" "$REV_TSUKUROI" \
1124:     "$specs/bash-tsukuroi-census.spec" 'bash "$MUTANT" --selftest' "$TABLE_TSUKUROI" \
1125:     "$root/bash-tsukuroi-census"
1126:   st_tsu=$?
1127:   regression_case_git bash-mado-verify \
1128:     'mado-shokunin/tools/mado-verify.sh' "$PIN_MADO" "$REV_MADO" \
1129:     "$specs/bash-mado-verify.spec" 'bash "$MUTANT" --selftest' "$TABLE_MADO" \
1130:     "$root/bash-mado-verify"
1131:   st_mado=$?
1132:   regression_case_git bash-checklist-run \
1133:     'kagi-shokunin/corpus/checklist-run.sh' "$PIN_CHECKLIST" "$REV_CHECKLIST" \
1134:     "$specs/bash-checklist-run.spec" 'bash "$MUTANT" --selftest' "$TABLE_CHECKLIST" \
1135:     "$root/bash-checklist-run"
1136:   st_checklist=$?
1137:   regression_case_git js-claims-check \
1138:     'kumitate-shokunin/scripts/claims-check.mjs' "$PIN_CLAIMS" "$REV_CLAIMS" \
1139:     "$specs/js-claims-check.spec" 'node "$MUTANT" --selftest' "$TABLE_CLAIMS" \
1140:     "$root/js-claims-check"
1141:   st_claims=$?
```

---

## 4. Potential Extraction Traps for `ReceiptHarness`

When `ReceiptHarness` (`capture-context.py`) extracts runner tables, constants, and call mappings, it faces specific syntactic and architectural hazards. Failure to account for these will produce extraction errors or false mismatch flags.

### Trap 1: Variable Suffix Asymmetry (Non-uniform Naming)
- **Observed Fact:**
  - Leg 1 (`js-kimi-census`) uses suffix `_JS` (`PIN_JS`, `REV_JS`, `TABLE_JS`), NOT `_KIMI` or `_KIMI_CENSUS`.
  - Leg 2 (`bash-surface-census`) uses suffix `_BASH` (`PIN_BASH`, `REV_BASH`, `TABLE_BASH`), NOT `_SURFACE`.
  - Leg 3 (`bash-tsukuroi-census`) uses suffix `_TSUKUROI`.
  - Leg 4 (`bash-mado-verify`) uses suffix `_MADO`.
  - Leg 5 (`bash-checklist-run`) uses suffix `_CHECKLIST`.
  - Leg 6 (`js-claims-check`) uses suffix `_CLAIMS`.
- **Extraction Risk:** If `capture-context.py` attempts to construct variable names algorithmically from leg identifiers (e.g. `f"PIN_{leg.replace('-', '_').upper()}"`), it will fail to find variables for 4 of the 6 legs (`js-kimi-census`, `bash-surface-census`, `bash-checklist-run`, `js-claims-check`).
- **Remedy for ReceiptHarness:** Parse the actual variable token passed in the `regression_case_git` call (e.g. regex capture group on `"\$PIN_(\w+)"`), or maintain an explicit canonical variable table mapping each leg to its exact constant name.

### Trap 2: Reused Revisions Across Distinct Legs (Collision Hazard)
- **Observed Fact:**
  - Leg 1 (`js-kimi-census`) and Leg 6 (`js-claims-check`) share the exact same commit hash: `175de6ba2e9e904010411b19cab27e0af9aad3d4`.
  - Leg 2 (`bash-surface-census`) and Leg 5 (`bash-checklist-run`) share the exact same commit hash: `fecee8743e52eb8fb5fbb40782934cb619a1a96e`.
- **Extraction Risk:** A dictionary keyed by revision hash (e.g. `revisions[rev] = leg`) will overwrite earlier legs and report only 4 unique revisions instead of 6 valid leg entries.
- **Remedy for ReceiptHarness:** Always key mappings by canonical `leg` name, never by revision hash.

### Trap 3: Fleet-Relative Path Splitting vs. Manifest Schema
- **Observed Fact:**
  - In `mutate-and-run.sh`, the second argument is a combined fleet-relative path, e.g. `'kumitate-shokunin/scripts/kimi-census.mjs'`.
  - In `pin-manifest.json`, the repository and repo-relative path are split into distinct fields: `"repo": "kumitate-shokunin"` and `"path": "scripts/kimi-census.mjs"`.
- **Extraction Risk:** A naive equality check `call_arg_path == manifest["path"]` will fail for all six legs because of the repo prefix.
- **Remedy for ReceiptHarness:** Split the runner call argument on the first `/` (`rel.split('/', 1)`), yielding `repo` and `path`, or verify `call_arg_rel == f"{manifest['repo']}/{manifest['path']}"`.

### Trap 4: Multi-line Command Formatting & Backslash Continuations
- **Observed Fact:** Every call to `regression_case_git` is broken across 4 lines using trailing backslashes `\`.
- **Extraction Risk:** Line-by-line regexes (e.g. matching `^regression_case_git\s+(\S+)\s+(\S+)...`) will fail to match any arguments past the first line.
- **Remedy for ReceiptHarness:** Pre-process the script by joining lines ending in `\` (or run regex in multiline mode with `re.DOTALL` across whitespace).

### Trap 5: Argument Indirection (Variable Expansions vs Literals)
- **Observed Fact:** The invocations pass `"$PIN_JS"`, `"$REV_JS"`, and `"$TABLE_JS"` rather than literal hex strings.
- **Extraction Risk:** If the extractor expects the 64-character hash in the invocation line, it will only extract the string literal `"$PIN_JS"`.
- **Remedy for ReceiptHarness:** The extractor must parse in two passes:
  1. Parse constant definitions (lines 542–559) into a dictionary `constants = {"PIN_JS": "...", ...}`.
  2. Parse the invocations (lines 1112–1140) to extract variable names, then dereference them via `constants[var_name]`.
  3. Validate that the dereferenced values match `pin-manifest.json`.

### Trap 6: Selftest Mock Calls (False Positive Collisions)
- **Observed Fact:** In `tools/mutate-and-run.sh` under `selftest()` (lines 1455–1550), `regression_case_git` is called 6 additional times against mock test fixtures:
  - Line 1455: `regression_case_git fixture-git fakerepo/target.sh "$s_before" "$grev" ...`
  - Line 1465: `regression_case_git fixture-git fakerepo/target.sh "$s_before" "$grev" ...`
  - Line 1472: `regression_case_git fixture-git fakerepo/target.sh ...`
  - Line 1480: `regression_case_git fixture-git fakerepo/target.sh "$s_before" ...`
  - Line 1520: `regression_case_git fixture-exec fakerepo/exec.sh "$exec_sha" "$grev_exec" ...`
  - Line 1547: `regression_case_git fixture-noexec fakerepo/noexec.sh "$noexec_sha" "$grev_noexec" ...`
- **Extraction Risk:** An un-scoped search for all `regression_case_git` invocations across the file will find 12 calls instead of 6, including `fixture-git`, `fixture-exec`, and `fixture-noexec`.
- **Remedy for ReceiptHarness:** Scope extraction strictly to the body of `run_regression()` (between line 1074 and line 1176), or filter calls by the 6 known canonical leg names.

### Trap 7: Docstring / Comment Tables vs Executable Code
- **Observed Fact:**
  - Header comment lines 84–89 provide an informal summary table of legs and kill-rates.
  - Lines 524–536 contain markdown anchors in comments.
  - Line 1103 contains a format string in a `printf` call.
- **Extraction Risk:** Extracting from comments yields documentation that lacks PINs, REVs, and exact invocations.
- **Remedy for ReceiptHarness:** Ensure regexes ignore lines beginning with `#` and target executable assignment statements and function calls only.

### Trap 8: Mode Handling Discrepancy (Exec Bit Mirroring)
- **Observed Fact:** `regression_case` (lines 941–957) checks `git ls-tree` and runs `chmod +x "$dst"` if mode is `100755` (vital for `bash-checklist-run` which re-execs `$SELF`). However, `pin-manifest.json` does NOT store file modes (only blob sha256), and `pin-disposition.py` places mode under `not_compared`.
- **Extraction Risk:** Comparing runner behavior to manifest expectations may mistakenly flag missing mode verification.
- **Remedy for ReceiptHarness:** Record mode handling as an internal runner property; do not assert mode equality against `pin-manifest-v1`.

### Trap 9: Value Verification vs Presence Check
- **Observed Fact:** Merely asserting that `PIN_JS` is defined in the script does not prove that its value equals the manifest's `expected_sha256`.
- **Extraction Risk:** A broken runner defining placeholder or stale pins could pass a presence-only check.
- **Remedy for ReceiptHarness:** `capture-context.py` must compute explicit boolean assertions:
  - `pin_sha256_matches: runner_constants[pin_var] == manifest_leg["expected_sha256"]`
  - `rev_commit_matches: runner_constants[rev_var] == manifest_leg["pinned_commit"]`
  - `path_matches: runner_rel_path == f"{manifest_leg['repo']}/{manifest_leg['path']}"`

---

## 5. Value Agreement with `pin-manifest.json`

Cross-checking the independently tabulated runner values against `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json`:

1. **`js-kimi-census`:**
   - Manifest: `repo="kumitate-shokunin"`, `path="scripts/kimi-census.mjs"`, `pinned_commit="175de6ba2e9e904010411b19cab27e0af9aad3d4"`, `expected_sha256="83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426"`
   - Runner: `rel="kumitate-shokunin/scripts/kimi-census.mjs"`, `REV_JS="175de6ba2e9e904010411b19cab27e0af9aad3d4"`, `PIN_JS="83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426"`
   - **Verdict:** Bit-exact agreement.

2. **`bash-surface-census`:**
   - Manifest: `repo="kagi-shokunin"`, `path="corpus/surface-census.sh"`, `pinned_commit="fecee8743e52eb8fb5fbb40782934cb619a1a96e"`, `expected_sha256="275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f"`
   - Runner: `rel="kagi-shokunin/corpus/surface-census.sh"`, `REV_BASH="fecee8743e52eb8fb5fbb40782934cb619a1a96e"`, `PIN_BASH="275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f"`
   - **Verdict:** Bit-exact agreement.

3. **`bash-tsukuroi-census`:**
   - Manifest: `repo="tsukuroi-shokunin"`, `path="tools/tsukuroi-census.sh"`, `pinned_commit="165307fe4746a8807b02ec4a7d7ecac0368454a6"`, `expected_sha256="084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5"`
   - Runner: `rel="tsukuroi-shokunin/tools/tsukuroi-census.sh"`, `REV_TSUKUROI="165307fe4746a8807b02ec4a7d7ecac0368454a6"`, `PIN_TSUKUROI="084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5"`
   - **Verdict:** Bit-exact agreement.

4. **`bash-mado-verify`:**
   - Manifest: `repo="mado-shokunin"`, `path="tools/mado-verify.sh"`, `pinned_commit="eead56b20ad2b28299ae4fa623d52a99b44c743c"`, `expected_sha256="d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13"`
   - Runner: `rel="mado-shokunin/tools/mado-verify.sh"`, `REV_MADO="eead56b20ad2b28299ae4fa623d52a99b44c743c"`, `PIN_MADO="d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13"`
   - **Verdict:** Bit-exact agreement.

5. **`bash-checklist-run`:**
   - Manifest: `repo="kagi-shokunin"`, `path="corpus/checklist-run.sh"`, `pinned_commit="fecee8743e52eb8fb5fbb40782934cb619a1a96e"`, `expected_sha256="7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf"`
   - Runner: `rel="kagi-shokunin/corpus/checklist-run.sh"`, `REV_CHECKLIST="fecee8743e52eb8fb5fbb40782934cb619a1a96e"`, `PIN_CHECKLIST="7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf"`
   - **Verdict:** Bit-exact agreement.

6. **`js-claims-check`:**
   - Manifest: `repo="kumitate-shokunin"`, `path="scripts/claims-check.mjs"`, `pinned_commit="175de6ba2e9e904010411b19cab27e0af9aad3d4"`, `expected_sha256="e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b"`
   - Runner: `rel="kumitate-shokunin/scripts/claims-check.mjs"`, `REV_CLAIMS="175de6ba2e9e904010411b19cab27e0af9aad3d4"`, `PIN_CLAIMS="e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b"`
   - **Verdict:** Bit-exact agreement.

---

## 6. Concrete Changes, Risks & Checks L1 Should Run

### Concrete Deliverables by this Seat
- Produced comprehensive independent tabulation and trap analysis in `.ufo/waves/round-14/w1/RunnerMappings.md`.
- No modifications made to `tools/mutate-and-run.sh` or historical evidence.

### Residual Risks for Wave 1
1. **ReceiptHarness Regex Fragility:** If `capture-context.py` implements regex without normalization of multi-line continuation or variable lookup, extraction of runner calls will fail.
2. **Ambient vs Injected Environment:** When `capture-context.py` executes `pin-disposition.py` with `GIT_DIR` poisoned to `/nonexistent/tameshi-round14-poison`, `os.environ` must explicitly retain necessary path variables (`PATH`, `HOME`) while injecting `GIT_DIR`. If ambient environment is completely dumped, `git` binary resolution may fail.

### Recommended Checks for L1 Integration
L1 should execute the following checks during integrated verification:

1. **Runner Digest Verification:**
   ```sh
   sha256sum tools/mutate-and-run.sh
   # Expected: 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
   ```
2. **ReceiptHarness Script Execution:**
   ```sh
   python3 .ufo/evidence/round-14/capture-context.py
   # Expected: exit 0, generates .ufo/evidence/round-14/context-receipt.json
   ```
3. **Context Receipt Mapping Validation:**
   ```python
   import json
   with open('.ufo/evidence/round-14/context-receipt.json') as f:
       data = json.load(f)
   # Assert all 6 runner leg mappings report true
   assert len(data.get("legs", [])) == 6
   for leg in data["legs"]:
       assert leg["mapping_matches"] is True
       assert leg["pin_matches"] is True
       assert leg["rev_matches"] is True
   ```
4. **Environment Poisoning Receipt Invariance:**
   ```python
   # Verify baseline vs injected outputs are identical minus timestamp
   assert data["baseline"]["exit_code"] == data["injected"]["exit_code"] == 0
   assert data["injected_env"] == {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}
   assert data["baseline"]["comparable_digest"] == data["injected"]["comparable_digest"]
   ```
