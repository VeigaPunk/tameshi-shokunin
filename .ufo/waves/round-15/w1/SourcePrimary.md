# Primary source reading — Python subprocess environment and CLI invocation

## Finding and cited source identity

Canonical primary documentation was opened live this round on 2026-10-20 to locate `subprocess.run` environment semantics and actual CLI execution support for the round-15 C1 calibration capability:

- **Source URL:** `https://docs.python.org/3/library/subprocess.html`
- **Access date:** 2026-10-20
- **Documented version / revision:** Python 3.15.0 documentation (`subprocess — Subprocess management — Python 3.15.0 documentation`)
- **Run environment quote (19 words):**
  > “If env is not None, it must be a mapping that defines the environment variables for the new process”
  *(Location: Section “Using the `subprocess` Module”, `subprocess.run` parameter description, paragraph on `env`)*
- **Child interpreter CLI launch quote (24 words):**
  > “passing sys.executable is the recommended way to launch the current Python interpreter again, and use the -m command-line format to launch an installed module.”
  *(Location: Section “Popen Constructor”, `executable` and `args` search-order warning)*
- **Process execution and return codes quote (19 words):**
  > “The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.”
  *(Location: Section “`subprocess` — Subprocess management”, opening overview)*
- **Program argument sequence quote (22 words):**
  > “args is required for all calls and should be a sequence of program arguments or else a single string or path-like object.”
  *(Location: Section “Frequently Used Arguments”, `args` description)*

## Observed facts vs inferences vs gaps

### Observed facts (from primary documentation)
1. **Explicit child environment mapping:** `subprocess.run(..., env=...)` accepts an explicit mapping defining the child process's environment variables. Supplying `env` replaces default process environment inheritance rather than merely documenting an intention.
2. **Actual CLI invocation interface:** `subprocess` does **not** provide a module-level command-line utility (there is no `python -m subprocess` CLI entrypoint, and no Command-Line Interface section in `subprocess.html`).
3. **Execution of external CLI commands:** `subprocess` is designed to spawn and manage external child processes. When re-invoking the Python runtime to execute a script CLI, the documentation explicitly specifies `sys.executable` as the reliable multi-platform entrypoint.
4. **Execution parameters and return codes:** `run()` waits for process completion, captures `returncode`, `stdout`, and `stderr`, and handles tokenized argument sequences without shell-interpolation risks when `shell=False`.

### Inferences
1. For the round-15 context gate `--selftest`, executing the tool's public CLI entrypoint via `subprocess.run([sys.executable, str(script_path), ...], env=isolated_env)` strictly satisfies the outside verifier's routed requirement (testing actual CLI subprocess exits and finding IDs on isolated synthetic fixtures, avoiding in-process function call shortcuts).
2. Supplying an explicit isolated dictionary for `env` in synthetic selftest runs guarantees that the test exercises behavior under controlled child environments rather than unmeasured parent process environment leakage.

### Gaps and non-claims (anti-inference bounds)
1. **No historical inference:** The existence and documentation of `subprocess.run(..., env=...)` does not prove what environment variables were active during uninstrumented historical runs in round 13 or earlier. Prospective evidence stands solely on its own recorded run.
2. **No broad environment independence:** An isolated override of a single variable (such as `GIT_DIR`) in prospective testing demonstrates behavior under that specific override only; it does not prove independence from `PATH`, `HOME`, runtime versions, or unmeasured environment variables.
3. **No author authentication:** Pinned expected digests or exit codes do not authenticate authors or prove provenance beyond matching the recorded bytes.

## Grounding for C1 calibration capability

C1 calibration capability in round 15 addresses routed defect 5 from the outside verifier spot-check (`corpus/lessons/round-14-verifier-spotcheck.md:154-162`):
- The maintained context capture tool (`tools/context-capture.py`) must be classified as a **gate**, not a probe, because its persisted source/mapping comparisons emit mismatch verdicts and process exit 1.
- The gate must provide a standalone isolated `--selftest` that exercises the actual public CLI via `subprocess`, asserting literal expected exit codes (0 clean, 1 mismatch, 2 unavailable, 64 usage) and stable finding tokens.
- S049 and primary documentation ground only prospective explicit child environment mapping and subprocess invocation; they do not establish historical setup or broader environment independence claims.
- `corpus/SOURCES.md` remains unmodified by this seat per contract (`Do not edit SOURCES`).

## Exact bounded recommendations for ContextGate (`tools/context-capture.py`)

1. **Selftest via actual CLI subprocess:**
   In `tools/context-capture.py`, implement `--selftest` using `subprocess.run([sys.executable, sys.argv[0], ...], env=isolated_env, capture_output=True, text=True)` against synthetic temporary fixture trees. Assert literal exit codes and stable finding strings on stdout/stderr. Do not call internal helper functions or `decide()` in lieu of CLI subprocess invocation.
2. **Explicit environment mapping:**
   In prospective context capture runs, pass explicit child environment dictionaries where external commands are called, and record the explicit `injected_env`, `argv`, and `cwd` directly in the receipt (`.ufo/evidence/round-15/context-receipt.json`).
3. **Complete exit classification:**
   Expose the explicit exit lattice:
   - `0`: bounded declared comparison, positive control, and mappings agree.
   - `1`: evaluated mismatch, failed control, or false mapping.
   - `2`: cannot evaluate (missing, unreadable, or invalid input/digest/receipt).
   - `64`: usage error (invalid/unexpected CLI arguments; classified as could-not-evaluate, no receipt).
4. **Historical byte preservation:**
   Keep `.ufo/evidence/round-14/capture-context.py` and round-14 receipts completely byte-identical. Normal prospective context capture in round 15 writes only to round-15 paths.

## Method, tool status, and confidence

- **Confidence:** High. Supported by primary documentation fetched directly from `https://docs.python.org/3/library/subprocess.html` on 2026-10-20, cross-referenced with `corpus/lessons/round-14-verifier-spotcheck.md` and historical round-14 context artifacts.
- **LSP device availability:** Unavailable (`read xd://lsp` returned `No such tool`). Text inspection and web fetch tools served as the literal fallback, not semantic proof.
- **Execution bounds:** Leaf scout seat. No verification execution, builds, linters, or tests were executed. No packages were installed or modified. SOURCES was not edited.
