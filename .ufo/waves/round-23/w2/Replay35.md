The `receipt-measure-selftest` row is statically exact-bound, but the gate can falsely accept it. If the requirement and receipt are edited together, `tools/command-binding.py` still reports clean, because it never compares the bundle against the frozen `requirements.json` or a pinned revision. I didn't write `.ufo/waves/round-23/w2/Replay35.md`, because this wave forbids all file writes, including the Report trailer. These findings are the report. I didn't run the registry command, any suite, or the gate. I only did read-only JSON and SHA-256 comparisons and read Git loose objects with Python. I installed nothing.

**The row's data is exactly bound (checked against retained bytes)**
- **Argv and expect:** `["python3","tools/receipt-measure.py","--selftest"]`, exit `0`, stdout token `RECEIPT_MEASURE_SELFTEST: 10/10 pass`. This is identical in the baseline registry (row 38, `status=active`), `requirements.json` (row 34), `bundle.json` (requirement and receipt 34) and `observations.json` (row 34). The bundle's 43 requirements equal the frozen ones exactly. The registry digest `ebd2e69a…` matches.
- **Baseline source:** `SKILL.md@c51eb32f:1950` gives this argv and "0 clean". The `10/10 pass` token comes from the registry author, not from that source line.
- **Output:** the bundle stdout (985 characters) equals the full observation stdout. It contains the token once, has no `FAIL` lines and no replacement characters, and stderr is empty. Exit is `0`, `held` is `true`, and there is no `cleanup_error`.
- **Same tool at every revision:** the `tools/receipt-measure.py` blob `41b4fdb1` (SHA-256 `a67bffa9…`) is identical at 28cae179, 496d212b and 336565fc, and in the live tree. The `RECEIPT_MEASURE_RUNNER_SHA256` line in stdout matches it.
- **Revision lineage:** 496d212b is the grandparent of the frozen 336565fc: 336565fc → 8f66b5d9 → 496d212b → 15ae6029 → 28cae179.

**What is actually evidenced versus inferred**
- **Present:** retained bytes for argv, the cwd string, the revision string, exit, full stdout/stderr and timing. Row timing is 14:44:54.75 to 14:44:55.72, inside the run window, and consistent with the 0.968 s elapsed.
- **Inferred from code only:**
  - That the process really ran in `/tmp/tameshi-r23-replay-naxu6fzi/...` at 496d212b. That temporary clone has been deleted, and `replay.py` sets both fields from its own variables.
  - That this stdout came from that process. That would need producer authentication, which isn't established and is rejected for this audit.
- **No historical retrofill:** the runner fields appear only on the new replay rows.
- **Not closed:** historical R17-CMD-BIND.

**False acceptance (impacts calibration and identity)**
`evaluate()` (lines 99–112) only compares each receipt to the bundle's own `requirements`, `cwd` and `revision`. The only outside input is `expected.json`, which pins the bundle's SHA-256. But `replay.py` (line 74) writes `expected.json` in the same run that writes the bundle. The only check against the frozen contract is `replay.py` line 40, which runs on the producer side.

So the gate does not verify the frozen contract itself:
- `bundle.requirements[34].expect.stdout_contains` is never compared with the frozen requirements.
- `bundle.revision` is never compared with the frozen revision. It is 496d212b, which is neither the base 28cae179 nor the frozen 336565fc, and the gate still reports clean.
- The `cwd` and `revision` checks only compare producer fields with other producer fields.

**Adversarial edit (worked out from the code, not run)**
1. In requirement 34, set `stdout_contains` to `["RECEIPT_MEASURE_SELFTEST"]`.
2. In receipt 34, set stdout to `RECEIPT_MEASURE_SELFTEST: 9/10 pass\n` and keep `exit: 0`.
3. Optionally set `revision` to `15ae6029…` (a real 40-hex revision) in the bundle and in every receipt.
4. Recompute `expected.json`.

The gate would return exit 0 with no findings. No case in the contract's population catches this.

**Other issues**
- **Wrong runner digest:** `observations.runner_sha256` and `instrument_sha256` hash the live repo's `tools/registry-check.py`, not the clone's copy that actually ran. They agree here only because both are blob `08ac9cd1`.
- **Constant printed like a measurement:** `ROUND20_MEASURE_INSTRUMENT_SHA256` prints the hardcoded `FROZEN_MEASURE_SHA` and measures nothing.
- **Cleanup status dropped:** the bundle drops `cleanup_ok`/`cleanup_error`, so the gate can't see cleanup failures.
- **Full output adds nothing here:** for this row the stored tail equals the full stdout.

**Smallest safe fix**
- Have L1 pass the gate a frozen requirements digest and an expected revision before the replay runs.
- Have the gate check that the bundle's requirement bytes and `bundle.revision` match those inputs.
- Have L1 own `expected.json`, not `replay.py`.
- In `replay.py`, hash the clone's `tools/registry-check.py`.
