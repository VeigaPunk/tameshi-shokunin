# ReconEnvironment — Round 15 Wave 1 Scout Report

## 1. Axes & Posture (Godspeed)

- **Axes:**
  - **Calibration ($C_1$):** Mechanical verifiability of context receipts; exact environment delta verification; non-vacuous positive control proving injection observability; strict discrimination between baseline and poisoned runs.
  - **Operability / Quality:** Fail-closed safety; zero secret leakage (shape-only, ambient environment never dumped, only stripped key names tracked); hermetic repeatability without foreign repo mutation.
- **Posture:** Scout inspection only. Zero verification/gate/selftest execution. Pure read-only source analysis of historical artifacts and bounded recommendation generation.

---

## 2. Line Locations in Historical `capture-context.py`

File: `.ufo/evidence/round-14/capture-context.py` (sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`):

### A. Bounded Injected `GIT_DIR` Field
1. **Declaration of Injected Environment & Poison Path (`lines 60–67`):**
   ```python
   INJECTED_ENV = {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}
   POISON_PATH = INJECTED_ENV["GIT_DIR"]
   CONTROL_ENV_ADDITIONS = {
       "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_CONFIG_GLOBAL": os.devnull,
       "GIT_OPTIONAL_LOCKS": "0",
       "GIT_TERMINAL_PROMPT": "0",
   }
   ```
2. **Positive Control Proving Injection Observability (`lines 394–413`):**
   ```python
   def positive_control_block(git_path, base_env):
       control_env = dict(base_env)
       control_env.update(CONTROL_ENV_ADDITIONS)
       injected_env = dict(control_env)
       injected_env.update(INJECTED_ENV)
       argv = [git_path, "-C", LANE_ROOT, "rev-parse", "--git-dir"]
       baseline = run_bounded(argv, LANE_ROOT, control_env, CONTROL_TIMEOUT_S)
       injected = run_bounded(argv, LANE_ROOT, injected_env, CONTROL_TIMEOUT_S)
       baseline_ok = baseline["exit"] == 0 and baseline["stdout"].strip() != ""
       reflects = (POISON_PATH in injected["stdout"]
                   or POISON_PATH in injected["stderr"]
                   or injected["exit"] != baseline["exit"])
       return {"argv": argv, "baseline": baseline, "injected": injected,
               "baseline_ok": baseline_ok, "injected_reflects_poison": reflects,
               "effective": baseline_ok and injected["exit"] != 0 and reflects,
               "env_additions": dict(CONTROL_ENV_ADDITIONS),
               "env_delta": {"baseline": [], "injected": sorted(INJECTED_ENV)}}
   ```
3. **Poison Path Pre-condition Check (`lines 469–473`):**
   ```python
   environment["poison_path_exists"] = os.path.lexists(POISON_PATH)
   if environment["poison_path_exists"]:
       raise InvalidContext("poison_path_exists",
                            "injected GIT_DIR target exists: " + POISON_PATH)
   ```
4. **Exact Environment Delta Derivation & Verification (`lines 524–536`):**
   ```python
   base_env = safe_env()
   injected_env = dict(base_env)
   injected_env.update(INJECTED_ENV)
   changed = {key for key, value in base_env.items()
              if key in injected_env and injected_env[key] != value}
   delta = sorted((set(base_env) ^ set(injected_env)) | changed)
   actual_injected = {key: injected_env[key] for key in delta}
   environment.update({
       "env_delta_keys": delta, "injected_env": actual_injected,
       "env_delta_matches_declared": delta == sorted(INJECTED_ENV)
       and actual_injected == INJECTED_ENV,
       "baseline_has_GIT_DIR": "GIT_DIR" in base_env,
   })
   ```
5. **Decide Predicates for Environment & Control Integrity (`lines 564–571`):**
   ```python
   if environment.get("env_delta_matches_declared") is not True:
       reasons.append("environment delta is not exactly the declared GIT_DIR injection")
   if environment.get("baseline_has_GIT_DIR") is not False:
       reasons.append("baseline still carries GIT_DIR")
   if control.get("effective") is not True:
       reasons.append("git poison positive control is ineffective")
   ```

### B. No Secret Capture (Secret Prevention & Shape-Only Rules)
1. **Contract Stated in Header Docstring (`line 31`):**
   ```python
   # Dependencies: python3 (stdlib), git. No credentials are read.
   ```
2. **Scrubbing Ambient `GIT_*` Without Reading Values (`lines 184–188`):**
   ```python
   def safe_env():
       env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
       env["LC_ALL"] = "C"
       return env
   ```
3. **Receipt Initialization with Non-Dump Assertion (`lines 421–428`):**
   ```python
   "environment": {
       "baseline_policy": "ambient with every GIT_* key removed, plus LC_ALL=C",
       "injected_policy": "baseline plus exactly the keys in injected_env",
       "injected_env": None, "env_delta_keys": None,
       "env_delta_matches_declared": None, "baseline_has_GIT_DIR": None,
       "ambient_git_keys_removed": [], "poison_path": POISON_PATH,
       "poison_path_exists": None, "ambient_env_dumped": False,
   },
   ```
4. **Recording Key Names Only — Never Values (`lines 466–468`):**
   ```python
   removed = sorted(key for key in os.environ if key.startswith("GIT_"))
   environment = receipt["environment"]
   environment["ambient_git_keys_removed"] = removed
   ```
5. **Restricted Subprocess Run Capture (`lines 208–210` & `lines 542–546`):**
   `run_bounded` captures only `argv`, `cwd`, `exit`, `stdout`, `stderr`. The environment dictionary (`env`) passed to child processes is **never** serialized into `receipt["runs"]["baseline"]` or `receipt["runs"]["injected"]`.
   `receipt["runs"]["env_delta"]` contains only key lists: `{"baseline": [], "injected": delta}`.

---

## 3. Key Locations in Retained `context-receipt.json`

File: `.ufo/evidence/round-14/context-receipt.json`:

1. **`environment` Object (`lines 14–29`):**
   - `"baseline_policy": "ambient with every GIT_* key removed, plus LC_ALL=C"` (`line 15`)
   - `"injected_policy": "baseline plus exactly the keys in injected_env"` (`line 16`)
   - `"injected_env": {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}` (`lines 17–19`): Strictly bounded to the single declared key.
   - `"env_delta_keys": ["GIT_DIR"]` (`lines 20–22`): Explicit 1-element list.
   - `"env_delta_matches_declared": true` (`line 23`)
   - `"baseline_has_GIT_DIR": false` (`line 24`): Confirms clean baseline.
   - `"ambient_git_keys_removed": []` (`line 25`): Key names only; empty list in ambient run.
   - `"poison_path": "/nonexistent/tameshi-round14-poison"` (`line 26`)
   - `"poison_path_exists": false` (`line 27`): Pre-condition satisfied.
   - `"ambient_env_dumped": false` (`line 28`): Explicit invariant confirmation.

2. **`runs.env_delta` (`lines 64–69`):**
   ```json
   "env_delta": {
     "baseline": [],
     "injected": [
       "GIT_DIR"
     ]
   }
   ```

3. **Subprocess Invocations in `runs` (`lines 70–98`):**
   - Both `baseline` and `injected` blocks record only `{argv, cwd, exit, stdout, stderr}`.
   - No environment variables, tokens, paths, or user variables are stored.

4. **`positive_control` Invariant Fields (`lines 117–164`):**
   - Baseline command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse --git-dir` -> exit 0, stdout `".git\n"` (`lines 121–134`).
   - Injected command: exit 128, stderr `"fatal: not a git repository: '/nonexistent/tameshi-round14-poison'\n"` (`lines 136–148`).
   - Control outcome keys: `"baseline_ok": true`, `"injected_reflects_poison": true`, `"effective": true` (`lines 149–152`).
   - Static control environment additions: `"GIT_CONFIG_NOSYSTEM": "1"`, `"GIT_CONFIG_GLOBAL": "/dev/null"`, `"GIT_OPTIONAL_LOCKS": "0"`, `"GIT_TERMINAL_PROMPT": "0"` (`lines 154–159`).

---

## 4. Observable versus Inferred Behavior

| Dimension | Observable Behavior (Mechanically Verified) | Inferred Behavior (Unwarranted Claims to Reject) |
|---|---|---|
| **Environment Delta** | Exactly one variable (`GIT_DIR`) differs between baseline and injected probe executions (`env_delta_keys == ["GIT_DIR"]`). | Broad environment isolation. Immunity to `GIT_DIR` does not imply immunity to `PATH`, `PYTHONPATH`, `LD_PRELOAD`, or shell options. |
| **Injection Delivery** | Direct positive control under identical injected environment causes `git rev-parse --git-dir` to exit 128 and report the exact poison path. | Universal git toolchain behavior. Proven only for `git rev-parse` and the pin probe's internal `git_env()`. |
| **Baseline Cleanliness** | Baseline environment explicitly checked: `baseline_has_GIT_DIR == false`, ambient `GIT_*` keys dropped. | Historical baseline cleanliness. Round 14's receipt does not retroactively prove that round 13 ran with clean environment. |
| **Probe Determinism** | Excluding top-level `observed_at`, baseline and injected probe outputs are byte-identical (`equal: true`, identical comparable sha256). | Suite or mutant determinism. Probe determinism does not establish mutation runner determinism. |
| **Secret Prevention** | Receipt records `"ambient_env_dumped": false`, dumps zero ambient env mappings, and stores only stripped key names. | Total absence of process inspection. Only subprocess env serialization is constrained. |
| **Result Reuse** | Explicitly declared: `"result_reuse": "not_established"` with reason: "content observation + static mapping do not establish environment, dependency, fixture or suite identity". | Safe test result reuse. Identical output under `GIT_DIR` poison cannot justify skipping regression runs. |

---

## 5. Supported Failure Cases in Source Code

The source code of `capture-context.py` supports multiple discriminative failure paths:

### Primary Failure Case: Ineffective Positive Control (`control["effective"] is False` -> Exit 1)
- **Source Mechanism (`capture-context.py:394–413, 570–571`):**
  The positive control asserts three conditions:
  1. `baseline_ok`: baseline exit is 0 and stdout is non-empty (`.git\n`).
  2. `injected["exit"] != 0`: injected run fails.
  3. `reflects`: injected stdout/stderr contains `POISON_PATH` or exits differently from baseline.
  If the injection is swallowed (e.g., if a subshell unsets `GIT_DIR` or falls back to system git config), `effective` evaluates to `False`.
- **Decision & Output (`lines 570–579`):**
  `decide()` appends `"git poison positive control is ineffective"`.
  Returns `("mismatch", 1, reasons)`.
  The receipt records `"status": "mismatch"`, `"exit": 1`.

### Sibling Failure Case: Poison Target Collision (`poison_path_exists` -> Exit 2)
- **Source Mechanism (`capture-context.py:469–473`):**
  `os.path.lexists(POISON_PATH)` is evaluated before executing any subprocess.
  If an attacker or leftover test fixture creates `/nonexistent/tameshi-round14-poison`, an `InvalidContext("poison_path_exists", ...)` exception is raised.
- **Handling (`lines 617–627`):**
  Caught in `main()`, sets `status = "invalid_input"`, `exit = 2`.
  Emits `CONTEXT: INVALID (kind=poison_path_exists ... exit=2)`.

### Sibling Failure Case: Environment Delta Violation (`env_delta_matches_declared` -> Exit 1)
- **Source Mechanism (`capture-context.py:527–534, 564–565`):**
  Computes symmetric difference plus value modifications between `base_env` and `injected_env`.
  If any ambient or helper variable leaks into `injected_env` (e.g. `len(delta) != 1` or `delta != ["GIT_DIR"]`), `env_delta_matches_declared` evaluates to `False`.
  `decide()` appends `"environment delta is not exactly the declared GIT_DIR injection"`, exiting 1.

---

## 6. Bounded Recommendations for Round 15 Promotion

1. **Preserve Historical Artifacts Byte-Identical:**
   Maintain `.ufo/evidence/round-14/capture-context.py` and `.ufo/evidence/round-14/context-receipt.json` without modification.
2. **Promote to Maintained `tools/context-capture.py`:**
   Implement `tools/context-capture.py` as an active tool that retains the identical bounded `GIT_DIR` injection contract (`{"GIT_DIR": "/nonexistent/tameshi-round14-poison"}` or round-15 equivalent) and identical secret prevention invariants (`ambient_env_dumped: False`, only key names recorded).
3. **Hermetic Standalone `--selftest`:**
   Incorporate standalone `--selftest` in `tools/context-capture.py` using `tempfile.TemporaryDirectory()`. The selftest must run isolated synthetic fixtures validating:
   - Exit 0: Clean valid receipt reconciliation.
   - Exit 1: Mismatch cases (including ineffective positive control and env delta mismatch).
   - Exit 2: Could-not-evaluate cases (missing inputs, poison path collision, invalid JSON).
   - Exit 64: CLI usage errors (`usage error, no receipt`).
4. **No Ambient Leaks:**
   Strictly forbid serializing `os.environ` or any ambient credentials into the receipt. Retain `safe_env()` and key-name-only logging for stripped variables.
5. **No Verification Execution by Scout:**
   No checks or gates were executed in this scout inspection; all observations are verified directly from committed source and receipt bytes.
