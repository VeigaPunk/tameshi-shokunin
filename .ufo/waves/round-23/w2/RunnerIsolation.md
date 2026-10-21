**Axes reviewed:** clone/read-only isolation, full-stream handling, receipt-command execution.

### Findings

**High — `--rev` is not isolated from live sibling worktrees.**  
**Exploit path:** A registered row uses a relative path such as `../<sibling>-shokunin/...` to write outside the clone.  
**Evidence:** `tools/registry-check.py:773–782` symlinks live sibling directories into the temporary fleet; `:676–684` runs rows with the clone as `cwd`. The `:632–645` guard checks only absolute argv tokens under the live fleet root, so it does not catch relative traversal through those symlinks. `replay.py:51–60` recreates the same live-sibling symlinks. The selftest’s non-hermetic case covers an absolute live-fleet token (`registry-check.py:1695–1719`), not this path.  
**Impact:** A row can mutate a real sibling despite running under `--rev`; deleting the temporary clone does not undo those writes. `registry-C` reports 46/46 holds at revision `336565…`, but that result does not establish sibling isolation.  
**Smallest remediation:** Run rows in an OS-enforced sandbox with the target and siblings mounted read-only; do not expose live sibling directories as writable symlinks.

**Medium — Replay writes into the target when `--out` points there.**  
**Exploit path:** Invoke replay with an output directory inside the target repository.  
**Evidence:** `replay.py:42`, `:73–81` creates the output directory and writes `bundle.json`, `expected.json`, and `observations.json`. The recorded `replay-command-A.json` passes `--out` under the target’s `.ufo/evidence/round-23/replay` directory. This contradicts the script’s “No live lane or sibling writes” docstring (`replay.py:7`).  
**Impact:** The replay harness itself changes the target, irrespective of row behavior. This is an explicit output path, so the issue is the unqualified read-only guarantee.  
**Smallest remediation:** Reject output paths beneath the target/fleet when claiming read-only execution, or explicitly scope that guarantee to row execution and designate the output write as an exception.

**Medium — Full-stream capture is opt-in for reporting, but unbounded in memory and persisted unredacted during replay.**  
**Exploit path:** A row emits very large output or prints sensitive data; replay opts into retaining it.  
**Evidence:** `run_row` defaults `retain_streams=False` (`registry-check.py:648–649`), but `communicate()` captures complete streams before the tail is produced (`:693`, `:717–726`). `replay.py:60` passes `retain_streams=True` and writes complete stdout/stderr into both observations and the bundle (`:66–81`). The replay observation receipt contains separate complete `stdout`/`stderr` fields and tail fields.  
**Impact:** Excessive output can exhaust memory/disk; secrets printed by a command can enter persisted evidence. No secret is established by the inspected examples.  
**Smallest remediation:** Enforce stream-size limits, scan required tokens incrementally, and avoid persisting raw streams or redact them before export.

### Gate execution check

**No finding:** `command-binding.py` validates the receipt’s argv, cwd, revision, exit, and stdout fields; it does not dispatch receipt argv. Its selftest subprocess invokes the gate itself on temporary fixtures. The recorded source-read gate is rejected with `ARGV_MISMATCH`, while the replay gate is clean. Those gate receipts are stamped `496d212…`; `registry-C` is stamped `336565…`, so the gate receipts are not same-revision execution evidence.

Static review only; no attack, build, or test was run. I did not write the requested report file because the governing assignment forbids all file writes; these findings are for L1 to persist.
