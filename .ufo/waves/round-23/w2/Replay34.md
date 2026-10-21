No field-level false acceptance shows up for `receipt-window-selftest` in the shipped artifacts. The row's name, argv and expected exit/stdout bind exactly to the baseline source, and the retained receipt satisfies them. Two weaknesses remain. First, the replay step drops the runner's cleanup-failure verdict, so a structural false acceptance is possible, though it didn't happen for this row. Second, this row's whole stdout can be reproduced from source alone, so the receipt content doesn't prove the command ran. I wrote no file: this wave forbids writes, including `.ufo/waves/round-23/w2/Replay34.md`, so L1 should persist these findings.

**What is actually present on disk**
- **Baseline source:** `registry-baseline.json` is byte-identical to `tools/registry.json` at `28cae179` (sha256 `ebd2e69a…`, matching `registry_sha256`). The row is active row 33 of 43, with source `SKILL.md@c51eb32:1949`.
- **Frozen requirement:** argv `["python3","tools/receipt-window.py","--selftest"]`, expected exit `0`, and stdout must contain `RECEIPT_WINDOW_SELFTEST: 20/20 pass`. `requirements.json`, the bundle's requirement row 33 and the registry row are equal, and the whole requirement list matches.
- **Receipt fields:** name and argv match exactly, exit is `0`, stderr is empty, and stdout is 1226 bytes. The stdout ends with the required token, and the receipt stdout equals the runner's retained stdout.
- **Bundle integrity:** the bundle hash `3d6c99b7…` matches `expected.json` and is the version committed at `336565fc`. `replay-gate-A.json` shows exit 0 with no findings, using `command-binding.py` hash `d533dc1e…`, which is unchanged at `336565fc`.
- **Same code at every revision:** `tools/receipt-window.py` has the same git blob (`ebb70e49`) at the base, the bundle revision (`496d212`), the frozen delivered revision (`336565fc`) and the `SKILL.md` source revision.
- **Runner hash:** `runner_sha256` `cba16646…` equals `registry-check.py` at `496d212`. Compared with the base, the only change in that file is the stream-retention option, so the pass/fail logic is unchanged.
- **No historical retrofill:** nothing in round-20, round-22 or the historical `receipt-window-selftest.json` changed between base and `336565fc`. The round-21 ledger only gained lines, all labeled "not recipe execution … or required-command coverage". Source reads are not counted as execution.

**What is inferred, not proven**
- **Execution itself:** the clone directory `/tmp/tameshi-r23-replay-naxu6fzi` no longer exists. The 0.077-second run time, the timing window and the cwd were all recorded by the same `replay.py` run.
- **The digest pin:** `expected.json` was written by that same process (`replay.py` lines 72–75). It catches later tampering, but it is not an independent commitment from the caller. I don't count producer self-attestation as authentication.
- **"Full output, not tails":** for this row it adds nothing. The 1226-byte stdout is under the 4096-byte tail limit, so the full stream and the tail are identical.

**Structural false acceptance (not realized for this row)**
- In `registry-check.py` `run_row`, a row only passes if cleanup succeeded (`held = got == expected_exit and not missing and cleanup_ok`).
- `replay.py` builds each receipt from only `got`, `stdout` and `stderr`. It drops `held` and `cleanup_error`.
- It also writes `bundle.json` and `expected.json` before checking `held`, and only returns 1 afterwards.
- So if a row's child processes survived cleanup but exit and output matched, the runner would fail it, yet `command-binding.py` would report it clean. Here `held` is true and there is no `cleanup_error` key, so this didn't happen.

**Adversarial change (concrete)**
- I rebuilt this row's stdout byte-for-byte from the `selftest()` source without running anything. It equals the retained stdout. The output is fixed and needs no repo files or other lanes.
- A forged receipt with that stdout, exit 0, the frozen argv, and any canonical absolute cwd and 40-character revision copied into the bundle's top-level fields would come back clean once `expected.json` is recomputed.
- This works because `cwd` and `revision` are only compared with the bundle's own declarations, and nothing external pins them to `336565fc` or a real checkout.
- This matches the gate's documented scope, which disclaims checking who produced the receipt. It is a tradeoff for the judge, not a fixable defect in the gate.
- A smaller, already-documented gap: the `stdout_contains` check is a plain substring test and exit is a separately declared field. That is the same behavior as the baseline runner, so it is not a regression.

**Smallest safe correction:** make `replay.py` refuse to write `bundle.json` and `expected.json` unless every row passed (`held is True` with no `cleanup_error`). Or carry `held` and the cleanup state into the receipt and fail on them in `evaluate()`. Optionally, add the revision to `expected.json` so it is pinned by something outside the bundle.

**Axes affected:**
- Argv and expected-result binding hold.
- Execution evidence is inferred only.
- Provenance is self-attested.
- Historical evidence is preserved.
- The historical R17-CMD-BIND item is not claimed closed.

I installed no tools and ran no registry command or test suite.
