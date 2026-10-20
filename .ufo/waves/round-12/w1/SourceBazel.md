# SourceBazel — S028 Test Encyclopedia Evaluation Report

- **Seat**: `SourceBazel` (scout, leaf member — no subagent dispatch)
- **Wave**: `tameshi-r12-w1`
- **Target**: S028 (`https://bazel.build/reference/test-encyclopedia`), sections §Role of the test runner and §Initial conditions
- **Assigned Question**: Evaluate whether exact output equality is a lane policy or source requirement; return located quote/access date and scope; no registry edits.

---

## 1. Executive Verdict

**Exact output equality is strictly a lane policy, NOT a source requirement of S028.**

- **S028 Source Requirement**: Bazel's normative specification establishes that test pass/fail outcome is determined exclusively by process termination status (exit code 0 = pass, non-zero = fail). Standard streams (`stdout` and `stderr`) are uninspected write sinks; S028 explicitly mandates that output content has *no significance* to the test runner. S028 imposes zero requirement for byte-for-byte stream equality across runs.
- **Tameshi Lane Policy**: Tameshi's Round 12 C1 calibration gate (`tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`) mandates $N \ge 3$ repeated runs with identical exit code, identical `stdout` bytes, and identical `stderr` bytes (`controls_match` exit 0; any disagreement yields `controls_mismatch` exit 1). This is a lane-internal calibration discipline to catch un-isolated or nondeterministic harness behavior prior to mutation analysis.

---

## 2. Source Metadata & Access

- **Source ID**: `S028`
- **Title**: *Test encyclopedia* (Bazel)
- **URL**: `https://bazel.build/reference/test-encyclopedia`
- **Access Date**: `2026-10-20` (Observed host access: `2026-10-20T02:15:01Z`; prior registration in round 1 recorded `2026-10-19`)
- **Document Digests**:
  - HTML body SHA-256: `30992fd116d331f8935aa26797c124dfaf7e05cf9a21921ed0d6427c1920f0e1`
  - Markdown alternate SHA-256 (`test-encyclopedia.md`): `f139999d707935244f73c26ca1bf8f1b7253dbf9722327e11a978be51fbca429`

---

## 3. Located Quotes from S028

### A. Section: Role of the test runner (`#role-test-runner`)

> "From the point of view of the test runner, each test is a program which can be invoked with `execve()`. There may be other ways to execute tests; for example, an IDE might allow the execution of Java tests in-process. However, the result of running the test as a standalone process must be considered authoritative. **If a test process runs to completion and terminates normally with an exit code of zero, the test has passed. Any other result is considered a test failure. In particular, writing any of the strings `PASS` or `FAIL` to stdout has no significance to the test runner.**"

> "If the main process of a test exits, but some of its children are still running, the test runner should consider the run complete and count it as a success or failure based on the exit code observed from the main process. The test runner may kill any stray processes. Tests should not leak processes in this fashion."

### B. Section: Initial conditions (`#initial-conditions`)

> "When executing a test, the test runner must establish certain initial conditions.
> The test runner must invoke each test with the path to the test executable in `argv[0]`. This path must be relative and beneath the test's current directory (which is in the runfiles tree, see below). The test runner should not pass any other arguments to a test unless the user explicitly requests it."

> "**File descriptor 0 (`stdin`) shall be open for reading, but what it is attached to is unspecified. Tests must not read from it. File descriptors 1 (`stdout`) and 2 (`stderr`) shall be open for writing, but what they are attached to is unspecified. It could be a terminal, a pipe, a regular file, or anything else to which characters can be written.** They may share an entry in the open file table (meaning that they cannot seek independently). Tests should not inherit any other open file descriptors."

> Initial environment block mandates:
> - `LANG`: *unset* (required)
> - `LANGUAGE`: *unset* (required)
> - `LC_ALL`: *unset* (required)
> - `LC_CTYPE`: *unset* or `C.UTF-8` (required)
> - `TZ`: `UTC` (required)
> - `TEST_TMPDIR`: absolute path to a private writable directory (required)
> - `TEST_SRCDIR`: absolute path to the base of the runfiles tree (required)
> - `TEST_PREMATURE_EXIT_FILE`: absolute path to a private file in a writable directory (used for catching calls to `exit()`) (optional)
> - `BAZEL_TEST`: Signifies test executable is being driven by `bazel test` (required)

### C. Section: Purpose of tests (`#purpose-of-tests`)

> "Therefore the outcome of a test must depend only on:
> * source files on which the test has a declared dependency
> * products of the build system on which the test has a declared dependency
> * resources whose behavior is guaranteed by the test runner to remain constant
> Currently, such behavior is not enforced. However, test runners reserve the right to add such enforcement in the future."

---

## 4. Evaluation: Lane Policy vs. Source Requirement

| Dimension | S028 Specification (External Source) | Tameshi Round 12 C1 (`tools/repeat-control.py`) (Lane Policy) |
|---|---|---|
| **Pass/Fail Decision Basis** | Standalone process exit code: `exit == 0` is PASS; any other exit or killed process is FAIL. | Matching exit code AND matching `stdout` bytes AND matching `stderr` bytes across all $N \ge 3$ runs. |
| **Treatment of `stdout`/`stderr`** | Non-normative stream sinks. Destination is unspecified (file, pipe, terminal). Strings written to stdout explicitly have "no significance to the test runner". | Normative gating data. Captured verbatim without byte normalization; any diff across repeated runs triggers `controls_mismatch` (exit 1). |
| **Output Determinism Requirement** | **None.** Output byte equality across runs is neither defined nor required. | **Mandatory.** Zero byte-level deviation allowed across $N \ge 3$ runs. |
| **Failure Classification** | Process exits non-zero, exceeds timeout/resource limits, leaves `TEST_PREMATURE_EXIT_FILE`, or receives killer signal. | Run-to-run output/exit disagreement (`controls_mismatch` exit 1); non-zero baseline (`baseline_nonzero` exit 2); binary unavailable (`command_unavailable` exit 2). |
| **Hermeticity Meaning** | Outcome (exit 0 vs non-zero) depends only on declared source dependencies and runner constants. | Calibration precondition: Repeated execution of the unmodified control must yield bitwise-reproducible stdout, stderr, and exit code. |

**Conclusion**: Exact byte-for-byte stream output equality is an internal **lane policy** authored for Tameshi's C1 calibration gate. It cannot be attributed to S028 as an external specification requirement.

---

## 5. Scope of S028

The scope of S028 (*Bazel Test Encyclopedia*) is to formally define the execution contract between the test runner infrastructure and an automated test target invoked as an OS subprocess (`execve`):
1. **Runner Responsibilities**: Set argv[0], prepare clean initial environment variables (`LANG` unset, `TZ=UTC`, `$TEST_TMPDIR`), manage runfiles symlink tree, monitor timeouts and process limits, reap stray processes, and map exit 0 to PASS.
2. **Test Responsibilities**: Do not read from stdin; write files only to `$TEST_TMPDIR` or `$TEST_UNDECLARED_OUTPUTS_DIR`; do not mutate the runfiles tree; exit 0 on success.
3. **Explicit Non-Scope**:
   - S028 does **not** evaluate stdout/stderr streams to determine verdicts or test validity.
   - S028 does **not** specify test caching conditions based on stdout/stderr checksums.
   - S028 does **not** govern mutation testing or calibration gates.

---

## 6. Risks and Invalidation Hazards

1. **Risk of False Citation (Attribution Overclaim)**:
   - *Hazard*: Citing S028 as the justification or authority for failing tests due to mismatched `stdout`/`stderr` bytes would be invalid. S028 explicitly repudiates using stdout for verdicts: *"writing any of the strings PASS or FAIL to stdout has no significance to the test runner"*.
   - *Mitigation*: The round 12 knowledge note (`repeated-control-precondition.md`) and scorecard must explicitly declare exact output equality as a lane policy, distinguishing it from S028's exit-code-only contract.

2. **Risk of Rejecting Benignly Nondeterministic Tools**:
   - *Hazard*: Because lane policy enforces exact stdout/stderr byte matching, test runners or scripts that report execution wall-clock time (e.g. `pytest`, `cargo test`, `jest`, or bash gates emitting timestamps or elapsed seconds) will fail C1 with `controls_mismatch` (exit 1) despite being fully compliant with S028 hermeticity.
   - *Mitigation*: Command wrappers under C1 test must strip or suppress benign time/pid outputs, or the runner invocation must be calibrated accordingly.

3. **Risk of Conflating Determinism with Flakiness Fixes**:
   - *Hazard*: Observing $N=3$ identical runs does not prove a test is deterministic or immune to flakiness.
   - *Mitigation*: Enforce the wave contract: matching controls confirm repeatable baseline observation under pristine conditions, but *"no flakiness cured or determinism proven"*.

---

## 7. Owned Paths & Integrity

- **Report Path**: `.ufo/waves/round-12/w1/SourceBazel.md` (this report)
- **Evidence Path**: `.ufo/evidence/round-12/SourceBazel/source-excerpt.txt`
- **Registry Edits**: **None**. `corpus/SOURCES.md` was inspected and verified; no edits were made by this seat (preserving the "no registry edits" contract).
- **Tooling / Installs**: None. System tools (`curl`, `sha256sum`, python3) sufficed.
