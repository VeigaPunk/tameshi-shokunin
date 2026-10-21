done

# SC11 — `registry-check.py` R02/R05/R07 fixture recon

## Evidence scope

Target is frozen revision `33d03b716d3edcf1d8656d46d6df61801d232c52`, `tools/registry-check.py` (1,920 lines; extracted-file SHA-256 `33d0d17c140a6b9662c023a3a8cfa67065e17fb8c73af20d7c8055005565aeb6`). The mutant definitions are R02, R05, and R07 in `.ufo/evidence/round-21/c1-mutants.json`. Findings below use direct source reads at the frozen revision; no test or selftest was run.

## Observed semantics

- **Timeout validation / R02:** `registry_errors()` rejects booleans and non-numeric values, then requires a finite `0 < timeout_s <= MAX_TIMEOUT_S` (`tools/registry-check.py:238-256`; cap is 86,400 seconds at `:104-106`). Invalid values become registry errors (`:369-372`, `:832-846`) and human output is `REGISTRY_CHECK: could-not-evaluate (...)` (`:884-888`). R02 changes the lower bound to `0 <= timeout_s`, so literal zero reaches execution.
- **Baseline children / R05:** `_direct_child_identities()` snapshots `(pid, starttime)` pairs whose parent is the checker before a row starts (`:456-465`); `run_row()` captures this set before `Popen` (`:674-676`). `_row_identity_is_owned()` walks current ancestry, rejects PID reuse, accepts the row leader only with its matching start time, and when ancestry reaches the checker returns whether the current child identity is *not* in that pre-row baseline (`:468-489`). This excludes pre-existing checker children from row cleanup while allowing newly adopted row descendants. R05 replaces that membership decision with unconditional `True`.
- **In-row signal scope / R07:** `_signal_row_processes()` supplies a callback that recomputes row ownership for each candidate (`:527-538`). `_signal_process_identity()` checks both the saved start time and that callback before opening a pidfd and again after opening it, immediately before signaling (`:503-524`). R07 removes the scope predicate from both guards; a same-start-time process that has moved out of row ancestry can then be signaled.
- **Observable failure output:** one active row with a failed expectation yields `ROW <name> expect=<exit> got=<...> differs` and a `REGISTRY_CHECK: held=...` summary (`:884-905`); `evaluate()` returns 1 when active rows do not all hold (`:869-881`). The selftest records a case as `SELFTEST_CASE ... FAIL (...)` and ends with `SELFTEST: FAIL (...)` (`:919-926`, `:1778-1782`).

## Existing selftest scaffolding to reuse

- `selftest()` owns one `/tmp` scratch directory and defines `record`, `run_child`, `write_registry`, `row`, and `check_lines` (`:912-972`). Use these rather than a new fixture framework.
- The invalid-timeout loop already builds raw JSON by replacing the helper row's default `timeout_s: 30`, runs the checker as a child, and asserts exit 2 plus diagnostic fragments (`:1500-1525`). Add zero there for R02.
- Timeout/cleanup integration examples are `timeout-kills-group` and `run_escape_case()` for setsid/setpgid pipe-holding descendants (`:1129-1215`), plus `normal-exit-kills-double-fork` (`:1218-1272`). These exercise cleanup end-to-end but do not isolate the baseline-membership or signal-scope predicates.
- The closest deterministic helper-level fixture is `pidfd-revalidates-starttime` (`:1566-1589`): it monkeypatches pidfd open/send/close, injects `read_stat`, restores globals in `finally`, and asserts a rejected signal. Reuse this pattern for R05/R07; add each result through `record()`.

## Exact discriminating recipes and predicted mutant failures

These are proposed fixture additions, not executed observations. Predicted outputs are **[INFERENCE]** from the cited implementation and existing formatting.

### R02 — zero is not a valid timeout

1. In the invalid-timeout tuple at `:1500-1509`, add `("timeout-zero", "0", "finite positive number")`.
2. Change that loop's row command at `:1510` to a guaranteed long-running process, e.g. `row(case, "import time; time.sleep(2)", 0)`. Keep the existing JSON replacement (`:1511-1518`) and `run_child`/`record` assertion (`:1519-1525`). The long sleep avoids making the mutant's `timeout=0` result depend on a short child winning the scheduling race.
3. With the intended guard, the child should exit 2 with the diagnostic containing `rows[0] ('timeout-zero').timeout_s must be a finite positive number <= 86400`, so the new case records `SELFTEST_CASE timeout-zero PASS (exit=2)`.
4. Under R02, zero passes validation and the sleeping row immediately times out; its captured checker output should contain:

   ```text
   ROW timeout-zero expect=0 got=timeout differs
   REGISTRY_CHECK: held=0/1 superseded=0
   ```

   The outer selftest should therefore print `SELFTEST_CASE timeout-zero FAIL (exit=1)` and end with `SELFTEST: FAIL (1 of N cases: timeout-zero)`. The nested row lines are captured by `run_child`; the selftest's direct failure line is the `SELFTEST_CASE` line.

### R05 — pre-existing checker child must remain out of row ownership

Add a deterministic helper-level test alongside the existing pidfd helper case (`:1566-1589`): temporarily replace `_read_proc_stat` with a lookup that returns `(os.getpid(), 4242, "S")` for synthetic PID `987654`; call `_row_identity_is_owned(987654, 4242, 987655, 77, frozenset({(987654, 4242)}))`; restore `_read_proc_stat` in `finally`. The synthetic process is an unchanged, pre-existing direct child of the checker, so the baseline implementation must return false. Record `not owned`, with detail `owned={owned}`.

Expected under R05: `_row_identity_is_owned()` returns true at the altered branch, giving the exact case line `SELFTEST_CASE baseline-child-excluded FAIL (owned=True)` and a final `SELFTEST: FAIL (1 of N cases: baseline-child-excluded)`. This directly isolates the branch at `:486-487` without creating or signaling a real process.

### R07 — recheck ancestry after pidfd acquisition

Add a helper-level case beside `pidfd-revalidates-starttime` (`:1566-1589`). Use matching injected `read_stat=lambda _pid: (os.getpid(), 4242, "S")`; replace `os.pidfd_open` with a stub returning `999999`, `signal.pidfd_send_signal` with a collector, and `os.close` with a no-op, restoring all three in `finally` as the existing test does. Supply a callback that returns `True` on its first call and `False` on its second. Call `_signal_process_identity(987654, 4242, signal.SIGKILL, in_row_scope, read_stat=...)`. Record success only if the helper returns false, the callback was called twice, and the signal collector is empty (e.g. detail `scope_rejected={not accepted} scope_checks={len(scope_calls)} signals={len(fake_signals)}`).

The baseline enters the first guard, opens the fake pidfd, then rejects when the second scope check returns false. Under R07 both guards omit the callback: it returns true, sends once, and never calls the scope callback. Expected exact mutant line for the proposed detail is `SELFTEST_CASE pidfd-revalidates-row-scope FAIL (scope_rejected=False scope_checks=0 signals=1)`, followed by `SELFTEST: FAIL (1 of N cases: pidfd-revalidates-row-scope)`.

## Commands, checks, gaps

- Source extraction: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 33d03b716d3edcf1d8656d46d6df61801d232c52:tools/registry-check.py > /tmp/tameshi-r21-SC11ReconRegistry-x/registry-check.py` — exit 0. `wc -l` reported 1,920; `sha256sum` reported the digest above. `git status --porcelain -- tools/registry-check.py` produced no output (target path unchanged).
- `read xd://lsp` returned `No such tool: xd://lsp`; no LSP definition/reference result is available. The source findings are direct line reads, not grep presented as semantic proof.
- `python3 tools/registry-check.py --selftest` was **not run**; no checks were exercised by this read-only recon. No tools were installed or updated.
- Disagreements/defects: none found in the inspected source. Remaining limitation: the three predicted failure outputs are fixture design expectations, not observed test output.
