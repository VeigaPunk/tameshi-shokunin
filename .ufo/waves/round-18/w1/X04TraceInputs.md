# X04 — Trace Inputs Promotion

## Axes

- **Depth:** promoted the trace collector and added focused synthetic assertions for the surviving mutation gaps.
- **Calibration:** verified the pristine selftest and each exact round-17 survivor mutant independently.
- **Operability:** monitored; no environment or external-system changes.

## Implementation

Created `tools/trace-inputs.py` from `.ufo/evidence/round-17/coldread/trace-inputs.py` without changing the historical copy. The source bytes matched SHA-256 `521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070`; the promoted file is `fb1d81f67551fb04e9e447cbc706ef5cc9cfd5208169004184b24ab15f3f2636` (755 mode, matching the source's executable mode).

Diff summary against the round-17 copy: only the module docstring path (`tools/trace-inputs.py`, line 2) and selftest additions: O_RDWR exclusion (`tools/trace-inputs.py:818-820`), a parseable trace with an opened input but no successful root exec (`:852-872`), and checking the actual child cache-prefix environment against its receipt/private path (`:925-930`). Existing `execve-script-input` coverage remains at `:888-889` and asserts `run.sh` is recorded in `inputs`. CLI, schema, and receipt-producing implementation are unchanged. The source copy still hashes to `521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070`.

## Retained evidence

Tests ran from `/tmp/tameshi-r18w1-X04TraceInputs-6IeGGh/fleet/tameshi-shokunin`, checked out at `183f87b899e6cae46be98d251cbc87fb5118f6ca`, with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, and `GIT_COMMON_DIR` unset. The unmutated candidate was copied into this isolated clone.

- Pristine: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR TMPDIR=/tmp/tameshi-r18w1-X04TraceInputs-6IeGGh python3 tools/trace-inputs.py --selftest` — **exit 0**, `SELFTEST: 30/30` (round-17 27 plus 3 new assertions).
- M01 exact survivor (round-17 report, `WRITE_FLAGS_RE`: delete `RDWR|`): the `/tmp` copy used `WRITE_FLAGS_RE = re.compile(r"\bO_(?:WRONLY|CREAT|TRUNC|APPEND|TMPFILE)\b")`. `python3 tools/trace-inputs-m01.py --selftest` — **exit 1**, `FAIL rdwr-open-excluded`, `SELFTEST: 29/30`.
- M03 exact survivor (round-17 report, `scrubbed_env`): replaced `env["PYTHONPYCACHEPREFIX"] = cache` with `env["PYTHONPYCACHEPREFIX"] = "."` in a separate `/tmp` copy. `python3 tools/trace-inputs-m03.py --selftest` — **exit 1**, `FAIL pycache-prefix-private`, `SELFTEST: 29/30`.
- M04 exact survivor (round-17 report, root-exec guard): replaced `if tracer.first_pid is None or tracer.first_pid not in tracer.exec_ok:` with `if tracer.first_pid is None:` in a separate `/tmp` copy. `python3 tools/trace-inputs-m04.py --selftest` — **exit 1**, `FAIL root-exec-required`, `SELFTEST: 29/30`. The fixture's fake strace emits a parseable successful `openat` line but no `execve`, isolating this guard.

All three mutant selftests used the same four-variable `env -u` prefix, `TMPDIR=/tmp/tameshi-r18w1-X04TraceInputs-6IeGGh`, and clone cwd. No tools were installed.

## Risks and blockers

None known. The missing-root-exec assertion intentionally uses synthetic strace output; it tests the trace validation contract without relying on a real missing-command trace, which the round-17 report showed may be empty.

Verdict: built