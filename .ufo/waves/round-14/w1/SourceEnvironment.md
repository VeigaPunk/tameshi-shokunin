# SourceEnvironment — environment documentation and explicit provenance

Lane: tameshi-shokunin (round 14, wave w1). Author seat: `TameshiR14.SourceEnvironment` (leaf, read-only research scout).
Scope: source verification of Python `subprocess` section `env` and StrykerJS `incremental` section `Limitations`. Analysis of explicit injected environment provenance versus documentation overclaims for round-14 capability C1.
Checks run: none. No gate, selftest, runner, or harness was executed. Tool installs/updates: none. No files other than this report are modified.

---

## 1. Named axes

- **Calibration (primary):** separate library API specifications from empirical execution facts. Ensure environment resilience claims rest on auditable, reproducible runtime receipts rather than citing library documentation as proof that runtime scrubbing occurred.
- **Depth:** articulate exact source locations, exact bounded quotes (<= 25 words), precise scopes, and the failure modes of conflating specification guarantees with historical execution records.
- **Operability, Freshness, Coverage, Adjacency:** harm none. Read-only scout report; no product or sibling code modified.

---

## 2. Located source citations

### Source A: Python `subprocess` — `env` parameter specification

- **Canonical URL:** `https://docs.python.org/3/library/subprocess.html`
- **Access date:** 2026-10-20
- **Section:** `env` (located in §*Using the subprocess Module* under `subprocess.run` and §*Popen Constructor* under `class subprocess.Popen`)
- **Exact quote (14 words, <= 25 words):**
  > "these are used instead of the default behavior of inheriting the current process’ environment."
- **Companion exact quote from `Popen` Note (13 words, <= 25 words):**
  > "If specified, env must provide any variables required for the program to execute."
- **Scope and authority:**
  - *Kind/Tier:* Standard library official technical documentation (Tier A docs).
  - *What it teaches (O):* When the `env` parameter is not `None`, Python passes the supplied mapping to the underlying operating system process creation call (`execvpe` on POSIX / `CreateProcess` on Windows) instead of inheriting the parent process's `os.environ`. The caller must explicitly supply all necessary variables required for execution.
  - *What it does NOT prove (bound):* The documentation defines the mechanism available to callers; it does **not** prove what environment variables were set, inherited, or scrubbed in any particular execution of a script. It does not prove that an ambient caller did not leak variables before Python startup, nor does it prove that a specific historical execution actually ran with poisoned inputs.

### Source B: StrykerJS — `incremental` mode limitations

- **Canonical URL:** `https://stryker-mutator.io/docs/stryker-js/incremental/` (registered in `corpus/SOURCES.md` as S003)
- **Access date:** 2026-10-20
- **Section:** `Limitations` (§*Limitations*, bullet 4)
- **Exact quote (22 words, <= 25 words):**
  > "Any other changes to your environment are not detected, such as updates to other files, updated (dev) dependencies, changes to environment variables,"
- **Opening sentence exact quote (9 words, <= 25 words):**
  > "Any other changes to your environment are not detected"
- **Scope and authority:**
  - *Kind/Tier:* Upstream mutation testing tool official documentation (Tier A docs; S003).
  - *What it teaches (O):* Incremental analysis tools that compare code and test hashes have fundamental blind spots: they cannot detect changes to external environment variables, dependencies, or unmonitored files. Therefore, target content equality alone does not establish identical execution behavior.
  - *Relevance to tameshi:* S003 validates why tameshi's pin probe deliberately marks `result_reuse: not_established` even when target content matches byte-for-byte. Environment variables are an unmonitored dimension in content hashing.

---

## 3. Provenance analysis: explicit injection vs documentation overclaim

### The defect in historical round 13 evidence (routed defect 2)
In round 13, `pin-disposition.py` implemented `git_env()` (`tools/pin-disposition.py:197-211`), which strips ambient `GIT_*` keys and sets `GIT_CONFIG_NOSYSTEM="1"`, `GIT_CONFIG_GLOBAL="/dev/null"`, etc. The round-13 verification receipt (`.ufo/evidence/round-13/verification.json`) contained a check named `pin_env_scrub`.

However, as identified in `corpus/lessons/round-13-verifier-spotcheck.md:180` (routed defect 2):
1. The recorded `argv` for `pin_env_scrub` was identical to `pin_live` (`["python3", "tools/pin-disposition.py", "--manifest", ".ufo/evidence/round-13/pin-manifest.json", "--root", "/home/vgpnk/Projects/shokunin"]`).
2. There was **no** `injected_env` field recorded in the receipt.
3. The check stdout was identical to `pin_live` (modulo `observed_at`).
4. While the static code of `git_env()` was visible in the repo, the *runtime setup* of the claimed `GIT_DIR` poisoning experiment was omitted from the receipt.

### The documentation overclaim trap
It is tempting to claim:
> *"The Python documentation states that `env` overrides inheritance, and `git_env()` scrubs `GIT_*`, so the documentation and code prove that `GIT_DIR` poisoning was scrubbed at runtime."*

This claim is **invalid** under `corpus/QUALITY.md` (Criteria 2, 3, 14):
1. **Conflation of specification and execution:** Documentation describes how `subprocess.run(..., env=...)` behaves when called. It is not an empirical record of an execution event.
2. **Unobserved variable presence:** The receipt did not record that `GIT_DIR` was ever injected into the parent process or passed into `pin-disposition.py`.
3. **No negative counterexample or baseline comparison:** Without recording both the injected variable value and comparing baseline vs injected execution in the receipt, an outside auditor cannot distinguish an executed poisoning experiment from an unexecuted or inert run.

### The requirement for round-14 explicit provenance
To satisfy the calibration bar without rewriting round-13 historical bytes:
1. **Prospective receipt, not retrospective rewriting:** Round 13's `pin_env_scrub` remains a frozen historical observation with an acknowledged provenance gap. Round 14 creates a new, distinct receipt via `.ufo/evidence/round-14/capture-context.py` yielding `context-receipt.json`.
2. **Explicit bounded injection:** The harness must explicitly define and record:
   ```python
   injected_env = {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}
   ```
   Setting `GIT_DIR` to a nonexistent path is a fail-closed poison: if Git honors the ambient `GIT_DIR`, it aborts immediately with `fatal: not a git directory`. If `git_env()` successfully scrubs it, Git discovers the target repo normally.
3. **No ambient environment dumping:** The receipt must record ONLY the explicitly injected variable (`injected_env`), never `os.environ` (which would leak credentials, SSH tokens, user paths, and violate environment hygiene).
4. **Structured delta verification:** The receipt records `argv`, `cwd`, `injected_env`, baseline exit and output, injected exit and output, and asserts byte equality of the probe output minus volatile fields (`observed_at`).

---

## 4. Concrete changes and risks

### Proposed changes
1. **Document sources:** Register Python `subprocess` §`env` as a formal reference for subprocess environment mapping contracts. (If added to `corpus/SOURCES.md`, S049 is the next available ID; S003 is already mined in row S003).
2. **Receipt contract in `capture-context.py`:** Support `TameshiR14.ReceiptHarness` in implementing:
   - Explicit `injected_env: {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}`.
   - Dual-run execution (baseline vs injected) executed by L1.
   - Output comparison verifying that probe data is invariant under `GIT_DIR` poisoning while excluding non-semantic dynamic timestamps (`observed_at`).
   - Logging runner/manifest mappings directly into `context-receipt.json`.
3. **Evidence isolation:** Ensure `tools/evidence-disposition.py` does not require the prospective `context-receipt.json` to validate the historical round-13 expectations. The disposition gate validates the frozen round-13 rows; the context receipt provides round-14 contextual provenance.

### Risks
- **Overclaiming documentation authority:** Treating library doc quotes as a substitute for execution receipts. *Mitigation:* Explicitly label docs as mechanism specifications and receipts as empirical observations.
- **Ambient environment leaks:** Accidentally serializing parent process `os.environ` into `context-receipt.json`. *Mitigation:* EnvSentinel and ReceiptHarness must whitelist only the explicit `injected_env` keys.
- **Retrospective historical alteration:** Modifying round-13 files to add `injected_env`. *Mitigation:* Historical files remain strictly read-only; new receipts live exclusively in `.ufo/evidence/round-14/`.
- **Ineffective poison value:** If `GIT_DIR` is set to an existing git directory (e.g. `.` or `/tmp`), git might succeed for reasons other than scrubbing. *Mitigation:* Use `/nonexistent/tameshi-round14-poison` to guarantee that any leak produces an immediate fatal git error.

---

## 5. Checks L1 should run (not run by this seat)

1. Verify `corpus/SOURCES.md` format and census if new rows are added:
   ```sh
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
   ```
2. Verify that historical evidence files are untouched:
   ```sh
   git diff --quiet d6809df7775338f000e44c8a916067b8866867fb -- .ufo/evidence/round-13/
   ```
3. Run `capture-context.py` once implemented by ReceiptHarness:
   ```sh
   python3 .ufo/evidence/round-14/capture-context.py
   ```
4. Verify `context-receipt.json` schema and containment:
   - Contains exact `injected_env` mapping `{"GIT_DIR": "/nonexistent/tameshi-round14-poison"}`.
   - Contains NO ambient environment variables (no `PATH`, `HOME`, `USER`, tokens, etc.).
   - Records both baseline and injected exit codes as 0.
   - Records output comparison matching across baseline and injected runs (excluding `observed_at`).
