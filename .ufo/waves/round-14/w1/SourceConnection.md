# SourceConnection — S003 omitted-input limitation, Python env semantics, and contextual evidence receipt

Lane: tameshi-shokunin (round 14, wave w1). Author seat: `TameshiR14.SourceConnection` (leaf, connector).
Scope: Connect S003 omitted-input limitation and Python `env` semantics to the contextual evidence receipt contract (`context-receipt.json` / `capture-context.py`). Rigorously separate source facts, inferences, and actual experiments.
Checks run: none. No gate, selftest, runner, or harness was executed (deferred to L1). Tool installs/updates: none. No files other than this report are modified.

Baseline: `d6809df7775338f000e44c8a916067b8866867fb`; delivered round-13 commit: `7dd16d9bdd15ef64228297e76e3b1bee690efde8`; measured-content commit: `4acc607dfd79f19d508bd50cdd06b77269fccd1d`.

---

## 1. Named axes

- **Calibration (primary):** enforce strict separation between:
  1. *Source facts* (what external documentation and recorded artifacts literally state),
  2. *Inferences* (logical models of why tools behave or how components compose), and
  3. *Actual experiments* (empirically executed, captured runtime events).
  Prevent the fallacy of citing language API specifications or tool limitation documentation as proof that a specific runtime environment scrub was executed.
- **Depth:** trace the connection between upstream mutation testing limitations (StrykerJS S003), standard library process isolation mechanisms (Python `subprocess` `env`), and tameshi's prospective round-14 contextual receipt (`context-receipt.json`).
- **Operability, Freshness, Coverage, Adjacency:** harm none. Read-only connector report. Zero modification to shared lane files, sibling repos, fleet files, or historical evidence.

---

## 2. S003 omitted-input limitation and Python env semantics

### 2.1 Upstream foundation: S003 (StrykerJS incremental mode)
- **Source:** StrykerJS documentation `https://stryker-mutator.io/docs/stryker-js/incremental/` (§*Limitations*, registered as S003 in `corpus/SOURCES.md`).
- **Verbatim limitation:**
  > "Any other changes to your environment are not detected, such as updates to other files, updated (dev) dependencies, changes to environment variables, changes to .snap files, readme files, etc."
  and:
  > "Stryker will not detect any changes you've made in files other than mutated files and test files."
  and:
  > "The dry run remains required; as it discovers tests, mutation coverage per test, and ensures Stryker runs successfully when no mutant is active."
- **Core methodological lesson:** Content hashing of a target file or test file has fundamental, structural blind spots. Environment variables, toolchain binaries, configuration files, and ambient shell state are omitted from file-level content hashes. Therefore, target file byte identity does not guarantee identical runtime behavior, and cannot alone license verdict reuse.

### 2.2 Standard library mechanism: Python subprocess `env` semantics
- **Source:** Python 3 standard library `subprocess` documentation `https://docs.python.org/3/library/subprocess.html` (§*Using the subprocess Module* / §*Popen Constructor*).
- **Verbatim specification:**
  > "these are used instead of the default behavior of inheriting the current process’ environment."
  and:
  > "If specified, env must provide any variables required for the program to execute."
- **Operating system mechanism:** On POSIX platforms, passing an explicit `env` mapping calls `execve`/`execvpe` with the exact provided pointer array, completely bypassing the default inheritance of `environ` from the parent process.
- **Implementation in `pin-disposition.py`:**
  Lines 197–211 define `git_env()`:
  ```python
  def git_env():
      env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
      env.update({
          "GIT_CONFIG_NOSYSTEM": "1",
          "GIT_CONFIG_GLOBAL": os.devnull,
          "GIT_OPTIONAL_LOCKS": "0",
          "GIT_TERMINAL_PROMPT": "0",
          "GIT_NO_LAZY_FETCH": "1",
          "GIT_PAGER": "cat",
          "LC_ALL": "C",
      })
      return env
  ```
  Lines 214–225 pass `env=git_env()` to `subprocess.run(["git", "-C", repo_abs] + args, ...)`.

---

## 3. Tripartite distinction: source fact, inference, and actual experiment

A critical vulnerability identified in round 13's outside review (`corpus/lessons/round-13-verifier-spotcheck.md:180`, routed defect 2) was the blurring of these three categories. To maintain rigorous calibration, every statement regarding environment isolation must be classified into one of the following:

### Category 1: Source Fact
Statements that reflect literal text in documentation or frozen byte sequences in repository artifacts:
- **SF-1 (S003 text):** StrykerJS documentation explicitly declares that changes to environment variables are not detected by its incremental change-detection algorithm (§*Limitations*).
- **SF-2 (Python documentation text):** Python's `subprocess` documentation explicitly states that providing an `env` dictionary replaces the default environment inheritance (§*Popen Constructor*).
- **SF-3 (Static code in repo):** `tools/pin-disposition.py` lines 197–211 contain Python code that iterates over `os.environ` and excludes keys matching `key.startswith("GIT_")`, appending seven fixed `GIT_*` configuration overrides.
- **SF-4 (Frozen round-13 receipt):** `.ufo/evidence/round-13/verification.json` records a check named `pin_env_scrub` with exit code `0`, whose recorded `argv` is identical to `pin_live` (`["python3", "tools/pin-disposition.py", "--manifest", ".ufo/evidence/round-13/pin-manifest.json", "--root", "/home/vgpnk/Projects/shokunin"]`), whose `stdout` is byte-identical to `pin_live`, and which contains **no** `injected_env` field, **no** ambient environment dump, and **no** record of `GIT_DIR` having been set.

### Category 2: Inference
Deductions, models, and arguments derived from source facts:
- **INF-1 (Transfer from S003 to tameshi pin probe):** Because S003 demonstrates that environment variables and external dependencies are undetected by file hashing, tameshi infers that checking the SHA256 of the six mutation targets cannot establish that historical test suite verdicts remain valid. This inference justifies setting `result_reuse: "not_established"` across all six legs in `pin-disposition.py`.
- **INF-2 (Subprocess isolation model):** Because Python's `subprocess.run(env=git_env())` passes an explicit dictionary omitting `GIT_*` to `execve`, any ambient `GIT_DIR` present in `pin-disposition.py`'s parent process will not reach the child `git` processes invoked by `git_run()`.
- **INF-3 (Failure mechanism under Git semantics):** In Git plumbing, if `GIT_DIR` is set to an invalid directory (e.g. `/nonexistent/tameshi-round14-poison`), any `git -C <repo> rev-parse` command fails immediately with exit `128` (`fatal: not a git directory`). Therefore, if `pin-disposition.py` were vulnerable to ambient `GIT_DIR` leakage, running under that poisoned variable would turn leg statuses from `verified`/`present` to `unavailable` (`git_unavailable`).
- **INF-4 (The documentation overclaim fallacy — REJECTED):** *Claiming that SF-2 (Python docs) and SF-3 (static code) prove that round 13 empirically demonstrated resilience to `GIT_DIR` poisoning is an invalid inference.* Code existing in a file does not prove it was executed under specific test conditions, and library documentation does not prove what an ambient caller supplied.

### Category 3: Actual Experiment
Empirically executed, instrumented runtime runs capturing inputs, execution parameters, and outputs:
- **EXP-1 (Historical round-13 execution):** The execution that created `.ufo/evidence/round-13/verification.json` at 2026-10-20T04:59Z. As recorded, `pin_env_scrub` was executed, but the ambient environment was not captured and no injected variable was recorded. This was an uninstrumented rerun, not an auditable poisoning experiment.
- **EXP-2 (Prospective round-14 execution via `capture-context.py`):** The planned execution (to be run by L1) wherein `capture-context.py` executes `pin-disposition.py` twice:
  1. *Baseline run:* executed without injection; captures `argv`, `cwd`, exit code, and stdout JSON.
  2. *Injected run:* executed with explicit `injected_env={"GIT_DIR": "/nonexistent/tameshi-round14-poison"}`; captures `argv`, `cwd`, exit code, and stdout JSON.
  3. *Receipt generation:* records the exact `injected_env` mapping, proves baseline exit == injected exit == 0, and asserts that baseline output equals injected output modulo volatile `observed_at`.

---

## 4. Connection to contextual evidence receipt (`context-receipt.json`)

Connecting S003's principle and Python's semantics directly defines the necessary architecture for round 14's contextual receipt:

```
+-----------------------------------------------------------------------------------+
| S003 Omitted-Input Limitation:                                                    |
| Target content hash DOES NOT detect environment variable changes.                |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| Tameshi Constraint:                                                               |
| Pin probe must prove target observations are invariant under ambient Git poison,  |
| but cannot rely on target hash alone.                                            |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| Python `env` Mechanism:                                                           |
| `git_env()` scrubs `GIT_*` keys and passes explicit mapping via `execve`.         |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| Historical Gap (Round 13 Routed Defect 2):                                        |
| Receipt omitted `injected_env`; scrub was static code, not an auditable receipt.  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| Round 14 Contextual Evidence Receipt (`context-receipt.json`):                    |
| 1. Explicit bounded `injected_env`: `{"GIT_DIR": "/nonexistent/..."}`            |
| 2. Dual execution (baseline vs injected) executed by L1.                          |
| 3. Zero ambient environment dump (no secret leaks).                               |
| 4. Structural equality check excluding only volatile `observed_at`.               |
| 5. Explicit mapping verification against `mutate-and-run.sh` tables.              |
+-----------------------------------------------------------------------------------+
```

### Key architectural requirements for `context-receipt.json`:
1. **No retrospective repair of round 13:**
   The round-13 receipt `.ufo/evidence/round-13/verification.json` must remain byte-identical (Criteria 4, 14). Round 14 does not rewrite historical records to pretend `injected_env` was present; it acknowledges the round-13 receipt gap as an uninstrumented rerun and provides `context-receipt.json` as a new prospective artifact.
2. **Fail-closed poison selection:**
   Using `/nonexistent/tameshi-round14-poison` ensures that if `git_env()` fails to scrub `GIT_DIR`, Git plumbing fails closed immediately. It eliminates ambiguous test states where a valid repository might be accidentally targeted.
3. **Hygiene against credential leakage:**
   Per `PROVINCE.md` and `corpus/QUALITY.md`, `capture-context.py` must never dump the parent `os.environ` (which could contain API keys, tokens, or local paths). The receipt records *only* the specific injected variable key/value and boolean verification flags.
4. **Separation of expectation gate from context harness:**
   `tools/evidence-disposition.py` (Gate for C1) evaluates the 13 historical expectation rows against `verification.json` and `producer-oracle-repair.json`. It does not require `context-receipt.json` to pass. The contextual receipt addresses routed defect 2 prospectively without entangling the historical reconciliation gate.

---

## 5. Concrete changes and risks

### Concrete changes
1. **Register source grounding:** Formally record Python `subprocess` `env` parameter documentation (`https://docs.python.org/3/library/subprocess.html`) as an admitted technical authority for subprocess environment isolation semantics (next open tier-A row S049, if admitted by L1).
2. **Receipt specification in `capture-context.py`:** Ensure ReceiptHarness implements:
   - Explicit `injected_env: {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}`.
   - Separate recording of baseline run and injected run (argv, exit code, outputs).
   - Comparison function that strips volatile `observed_at` and verifies JSON equality.
   - Inclusion of runner constant and leg call verification booleans.
3. **Reporting discipline:** Ensure the final round-14 report clearly distinguishes:
   - S003 limitation and Python docs as *Source Facts*.
   - The isolation argument as *Inference*.
   - The L1 execution of `capture-context.py` as *Actual Experiment*.

### Risks and mitigations
- **Risk 1: Ambient environment leakage.**
  *Mechanism:* Serializing `os.environ` into `context-receipt.json` would leak sensitive environment variables.
  *Mitigation:* EnvSentinel and ReceiptHarness strictly constrain the receipt schema to record only the explicitly injected dictionary `{"GIT_DIR": "..."}`.
- **Risk 2: Retrospective claim inflation.**
  *Mechanism:* Claiming that the round-14 context receipt "fixes" or "proves" that round 13 was clean.
  *Mitigation:* Explicitly label round-13 `pin_env_scrub` as an uninstrumented same-argv rerun in all round-14 documentation. Round 14 provides prospective capability, not historical revisionism.
- **Risk 3: Ineffective poison value.**
  *Mechanism:* Using an ambient directory that happens to be a valid git worktree could allow Git to succeed even if unscrubbed.
  *Mitigation:* The path `/nonexistent/tameshi-round14-poison` is non-existent by definition and guarantees exit `128` on leak.

---

## 6. Checks L1 should run (deferred; not run by this seat)

1. **Verify historical evidence immutability:**
   ```sh
   git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --quiet d6809df7775338f000e44c8a916067b8866867fb -- .ufo/evidence/round-13/
   ```
2. **Audit `capture-context.py` before execution:**
   Confirm that `capture-context.py` does not read or dump ambient environment variables into its output dictionary, and sets `injected_env = {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}`.
3. **Execute `capture-context.py` and inspect `context-receipt.json`:**
   ```sh
   python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-14/capture-context.py
   ```
   Verify that `context-receipt.json`:
   - Contains `injected_env` with the exact poison string.
   - Contains no `PATH`, `HOME`, or ambient credentials.
   - Confirms `baseline.exit == 0` and `injected.exit == 0`.
   - Confirms `comparison.outputs_match_excluding_observed_at == true`.
   - Confirms `mappings.all_six_legs_verified == true`.
4. **Execute `evidence-disposition.py` selftest and check runs:**
   ```sh
   python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/evidence-disposition.py --selftest
   ```

---

## 7. Residual risks and bounds

- **Residual unmeasured inputs (S003 blind spots):** While `GIT_DIR` isolation is verified by this contextual receipt, other unpinned inputs named by S003 (interpreter version, installed dev dependencies, system shared libraries, `TMPDIR`) remain outside the single-file pin probe. These continue to be catalogued under `not_compared` in `pin-disposition.py`.
- **Operating system scope:** Python's `subprocess` `env` mapping on POSIX replaces `environ` cleanly; on Windows, environment inheritance behavior for standard system variables (e.g. `SystemRoot`) differs. The lane operates on Linux (Arch Linux POSIX environment); no cross-platform generalization is claimed.
- **No mid-flight execution:** As a leaf subagent, this seat ran zero executions. All verifications remain deferred to L1.
