# BashDenominator — Pinned Target Denominator & Failing-Label Grammar Analysis

**Seat:** `BashDenominator` (Scout)  
**Round:** Tameshi Round 12, Wave 1  
**Target:** `kagi-shokunin/corpus/surface-census.sh` @ commit `fecee8743e52eb8fb5fbb40782934cb619a1a96e`  
**Blob SHA-256:** `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`  
**Owned Paths:**
- `.ufo/evidence/round-12/BashDenominator/cases.tsv`
- `.ufo/evidence/round-12/BashDenominator/parser.py`
- `.ufo/waves/round-12/w1/BashDenominator.md`

**Strict Quarantine Notice:** In accordance with task constraints, this analysis inspects only the pinned target source code and its selftest execution. Historical mutant outcomes (B1–B10 kill/survive classifications, surviving mutant identities, or prior defect failure logs) were neither inspected nor transmitted.

---

## 1. Axes & Posture (Godspeed)

- **Calibration ($C_1$):** Establishing an exact, deterministic suite denominator (16 cases) and formalizing exit-code semantics ensures that baseline runs and mutant executions are evaluated without count drift, false clean reports, or ambiguous runs.
- **Depth ($C_2$):** Deriving the grammar of failing labels and defining safe parsing specifications enables `BashWitness` to implement a rigorous declared-witness split (`killed-on-witness` vs `accidental` vs `survived`) without regex flakiness, false-positive kills, or outcome bias.

---

## 2. Pinned Target Identity & Execution Model

The target artifact is pinned in `corpus/SOURCES.md` (S033), `SKILL.md:601-606`, and `tools/mutate-and-run.sh:544-545`:
- **Repository:** `kagi-shokunin` (worktree at `/home/vgpnk/Projects/shokunin/kagi-shokunin`)
- **Relative Path:** `corpus/surface-census.sh`
- **Revision:** `fecee8743e52eb8fb5fbb40782934cb619a1a96e`
- **Blob SHA-256:** `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`
- **File Metrics:** 44,212 bytes, 887 lines (886 newlines, final line unterminated), file mode `100755`.

### Execution Requirements & Invocation Doctrine
- **Command:** `bash corpus/surface-census.sh --selftest` (or when running mutants: `bash "$MUTANT" --selftest`).
- **Filesystem Isolation:** The `selftest()` function allocates a dedicated temporary scratch tree (`R="$(mktemp -d)"; trap 'rm -rf "$SELFTEST_R"' EXIT`) and constructs a sandboxed environment (`$R/host`, `$R/census.tsv`, `$R/shapes.tsv`, `$R/baseline.tsv`).
- **Invocation Constraint:** The script executes subshell verifications via `bash "${BASH_SOURCE[0]}" verify ...`. Consequently, **it must be invoked as a valid filesystem file path**, never piped through standard input (e.g. `cat script.sh | bash` unbinds `BASH_SOURCE[0]` under `set -u`, causing immediate exit 1).

---

## 3. Denominator Grammar & Enumeration

The selftest suite defines and runs an exact, fixed set of **16 test cases**:
- **Case Counter:** Initialized as `local cases=0 failures=0` at `surface-census.sh:695`.
- **Sequential Indexing:** Cases increment strictly sequentially: `cases=$((cases + 1))`. Output labels use a two-digit zero-padded index `%02d` (`01` through `16`).
- **Suite Composition:**
  - Cases `01`–`14`: Surfaces and shapes verification (hermetic scratch tree).
  - Cases `15`–`16`: Handler write-side verb verification (`verbs-sandboxed` and `verbs-break-injection`).
- **Substrate Abstention:**
  - Cases `15` and `16` test whether `$THE_JANITOR_BIN` (`the-janitor`) exists on `PATH`.
  - When the handler binary is not installed, cases 15 and 16 emit `skip-case` with token `substrate-absent (handler not on PATH)`.
  - Crucially, skipped cases increment the case counter `cases` but **do not increment `failures`**.
  - Therefore, the total denominator is **always 16**, regardless of whether the substrate is present or absent.

### Summary Line Grammar
At the conclusion of `selftest()`, exactly one summary line is printed to stdout:
1. **All Passed / Skipped (`failures == 0`):**
   ```text
   SELFTEST: PASS (16 cases)
   ```
   Process exits with code **0**.
2. **One or More Failed (`failures > 0`):**
   ```text
   SELFTEST: FAIL (<failures>/16 cases)
   ```
   where `<failures>` is an integer in $[1, 16]$. Process exits with code **1**.

---

## 4. Case Output Grammar & Label Syntax

Every executed test case outputs a single summary line to stdout with one of three prefixes:

### 1. Passing Case: `ok-case`
- Format: `ok-case  %02d %-34s exit=%s %s\n`
- Notice: `ok-case` is followed by **two spaces** to align the two-digit index with `bad-case`.
- Example:
  ```text
  ok-case  01 clean                              exit=0 SURFACE OK
  ok-case  02 mode-drift                         exit=1 SURFACE DIVERGED
  ```

### 2. Failing Case: `bad-case` (Failing Label)
The script exhibits **two distinct syntactic variants** of `bad-case` lines depending on the test harness path:
- **Variant A (Helper `run_case` — Cases 01–09, 11–13):**
  `bad-case %02d %-34s want exit=%s token=%s got exit=%s\n`
  Example:
  ```text
  bad-case 01 clean                              want exit=0 token=SURFACE OK got exit=1
  ```
- **Variant B (Manual Harness Assertions — Cases 10, 14, 15, 16):**
  `bad-case %02d %-34s exit=%s\n`
  Example:
  ```text
  bad-case 10 sqlite-unavailable                 exit=2
  bad-case 14 fused-shape-row                    exit=1
  ```
- **Diagnostic Block Indentation:**
  For cases 01–15, when a case fails, the captured subshell stdout/stderr is emitted indented with four spaces and a pipe delimiter:
  ```text
      | <subshell diagnostic line>
  ```
  (Case 16 does not pipe diagnostic lines).

### 3. Skipped Case: `skip-case`
- Format: `skip-case %02d %-34s %s\n`
- Example:
  ```text
  skip-case 15 verbs-sandboxed                    substrate-absent (handler not on PATH)
  skip-case 16 verbs-break-injection              substrate-absent (handler not on PATH)
  ```

---

## 5. Complete 16-Case Catalog

The following table documents all 16 test cases defined in `corpus/surface-census.sh`:

| Index | Case Label Name (`name`) | Category | Pristine Status | Expected Exit | Assertion Target / Bad-Case Grammar Variant |
|:-----:|:-------------------------|:---------|:---------------:|:-------------:|:--------------------------------------------|
| `01`  | `clean` | surfaces | `ok-case` | 0 | Variant A: `want exit=0 token=SURFACE OK` |
| `02`  | `mode-drift` | surfaces | `ok-case` | 1 | Variant A: `want exit=1 token=SURFACE DIVERGED` |
| `03`  | `asset-gone` | surfaces | `ok-case` | 1 | Variant A: `want exit=1 token=SURFACE GONE` |
| `04`  | `runtime-absent` | surfaces | `ok-case` | 0 | Variant A: `want exit=0 token=SHAPE ABSENT` |
| `05`  | `undeclared-file` | surfaces | `ok-case` | 1 | Variant A: `want exit=1 token=SURFACE UNLISTED` |
| `06`  | `crosscheck-disagree` | surfaces | `ok-case` | 1 | Variant A: `want exit=1 token=SURFACE CROSSCHECK` |
| `07`  | `symlink-swap` | surfaces | `ok-case` | 1 | Variant A: `want exit=1 token=SURFACE LINK` |
| `08`  | `sqlite-magic` | shapes | `ok-case` | 1 | Variant A: `want exit=1 token=SHAPE SHAPE` |
| `09`  | `sqlite-magic-prefix-only` | shapes | `ok-case` | 1 | Variant A: `want exit=1 token=SHAPE SHAPE` |
| `10`  | `sqlite-unavailable` | shapes | `ok-case` | 1 | Variant B: `exit=<rc>` (checks `SHAPE UNVERIFIED`, `unverified=3`) |
| `11`  | `required-table-gone` | shapes | `ok-case` | 1 | Variant A: `want exit=1 token=missing tables` |
| `12`  | `row-floor` | shapes | `ok-case` | 1 | Variant A: `want exit=1 token=rows part 0` |
| `13`  | `malformed-row` | surfaces | `ok-case` | 2 | Variant A: `want exit=2 token=bad kind` |
| `14`  | `fused-shape-row` | shapes | `ok-case` | 2 | Variant B: `exit=<rc>` (checks `too many fields`) |
| `15`  | `verbs-sandboxed` | verbs | `skip-case`* | 0 | Variant B: `exit=<rc>` (*skipped if `$THE_JANITOR_BIN` absent) |
| `16`  | `verbs-break-injection` | verbs | `skip-case`* | 1 | Variant B: `exit=<rc>` (*skipped if `$THE_JANITOR_BIN` absent) |

*On standard execution hosts without `the-janitor`, pristine execution yields 14 `ok-case` and 2 `skip-case`, with `SELFTEST: PASS (16 cases)` and exit code 0.

---

## 6. Safe Parsing Requirements for `BashWitness`

To guarantee that `BashWitness` attributes kills accurately and resists parser vulnerabilities, the following rules MUST be enforced in `tools/bash-witness-study.py`:

### R1. Polymorphic `bad-case` Grammar Handling
A regex that expects `want exit=` will fail on cases 10, 14, 15, and 16. The parser MUST match on the common case prefix:
```python
CASE_RE = re.compile(
    r"^(?P<status>ok-case|bad-case|skip-case)\s+(?P<idx>\d{2})\s+(?P<name>[a-z0-9-]+)\s*(?P<rest>.*)$"
)
```
The failing test case label is extracted directly from the named group `(?P<name>[a-z0-9-]+)`.

### R2. Strict Line-Anchoring Against Indented Diagnostic Bleed
Subshell stdout/stderr from failing runs is printed with prefix `    | `.
- **Rule:** Never use unanchored substring matching (e.g. `if "bad-case" in line:`).
- **Rule:** Explicitly ignore lines matching `^\s*\|` or lines beginning with whitespace before checking for case status tokens.

### R3. Strict Denominator Verification
The suite count must hold on every evaluated run:
- Summary line must match `^SELFTEST:\s+(PASS|FAIL)\s+\((?:(\d+)/)?(\d+)\s+cases\)$`.
- The reported total must equal **16**.
- The number of parsed case lines (`len(ok) + len(bad) + len(skip)`) must equal **16**.
- If total $\neq 16$, the run MUST be classified as `inconclusive` / `count-violated`, not killed or survived.

### R4. Failure Count Parity
- On `SELFTEST: PASS`: parsed `bad-case` count must be 0, and exit code must be 0.
- On `SELFTEST: FAIL`: parsed `bad-case` count must exactly match the `<failures>` integer reported in the summary line, and exit code must be 1.
- Any mismatch between parsed `bad-case` count and summary `<failures>` indicates output truncation or stream corruption.

### R5. Exit Code Semantics
- Exit code 0: clean pass (`failures == 0`).
- Exit code 1: suite failure (`failures >= 1`).
- Any exit code $>1$ (e.g., 2, 126, 127) or exit code 1 lacking the summary line indicates an abnormal shell abort (syntax error, unhandled trap, unbound variable under `set -u`). Such runs must NOT be classified as killed; they are `inconclusive` / `aborted`.

### R6. Canonical Witness Declaration Representation
When pre-registering witness cases:
- Use either the unique lowercase case name (e.g. `mode-drift`, `sqlite-unavailable`) or composite format `02:mode-drift`.
- Match against the set of parsed `bad_case` names.
- Classification rules:
  - If $\text{failing\_cases} \cap \text{declared\_witness} \neq \emptyset \implies \mathbf{killed\text{-}on\text{-}witness}$.
  - If $\text{failing\_cases} \cap \text{declared\_witness} == \emptyset \text{ and } |\text{failing\_cases}| > 0 \implies \mathbf{accidental}$.
  - If $|\text{failing\_cases}| == 0 \text{ and exit} == 0 \implies \mathbf{survived}$.

### R7. Unreached Arms & Substrate Transparency
Cases 15 and 16 (`verbs-sandboxed`, `verbs-break-injection`) cannot fire in environments where `the-janitor` is absent. If any defect targets logic solely exercised by these verbs, it cannot be killed on its witness in a substrate-absent run. `BashWitness` must disclose this unreached arm boundary when declaring witnesses.

---

## 7. Retained Evidence & Test Verification

A reference parser implementing all R1–R7 rules and an exhaustive TSV table have been authored and verified under `.ufo/evidence/round-12/BashDenominator/`:
1. `cases.tsv` (SHA-256 `b3198bb43b94fc1a919f868a75eafba0596c65968560878802ef4176ab144922`):
   Formal declaration table of all 16 cases, classifications, exit criteria, and tokens.
2. `parser.py` (SHA-256 `b73793c158878f896030de622505a48989d2a726abeffe829898176dc8469a96`):
   Production-ready reference parsing module tested against live selftest runs and simulated error fixtures. Live selftest execution returned:
   ```text
   Valid: True
   Verdict: PASS
   Cases: 16
   Failing labels: []
   ```
## 8. Tooling Directive Compliance

No packages were installed or upgraded during this task. System python3, bash, and git were used exclusively.
