I found no false acceptance on the `defect-probes-selftest` row: its argv and expected result are bound exactly, statically, at row index 30 in every file. The one field-level gap is that the bundle receipt leaves out the runner's `held` and `cleanup_ok` result, so the gate could accept a run the runner rejected. That gap is not triggered by this row's evidence.

I did not write `.ufo/waves/round-23/w2/Replay31.md`. The wave instructions forbid all file writes, including report files, so L1 should save these findings. I didn't install anything, and I didn't run the original registry command, any suite, build or test. Everything below comes from file reads, `git show`, `jq` and `sha256sum`.

**What is bound and present (checked, not inferred)**
- **Baseline source:** `tools/registry.json` at base `28cae17` is byte-identical to `registry-baseline.json` (sha256 `ebd2e69a…`), which matches `requirements.json`'s `registry_sha256`. The baseline row has argv `["python3", ".ufo/evidence/round-18/defect-probes.py", "--selftest"]`, expects exit 0 with `stdout_contains ["SELFTEST: PASS"]`, and has status `active`. It is unchanged at `336565f`, which adds only the three `command-binding-*` rows.
- **Frozen requirements:** `requirements.json` and the bundle hold the same requirement object, and the whole requirements arrays are equal. Each file has exactly one row with this name.
- **New invocation metadata:** the observation row has the same argv, cwd `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`, and revision `496d212`. Its measurement interval runs from 14:44:52.910 to 14:44:52.996 UTC, which is inside the replay's 14:42:22–14:44:58 window and before commit `8f66b5d` (14:46:12). The runner's `elapsed_s` of 0.085 matches. `replay-command-A.json` shows `defect-probes-selftest 0 True` and `REPLAY: 43 / 43`.
- **Full output, not tails:** the bundle receipt stdout (516 bytes) and the observation's full stdout have the same sha256, `aa7dd3a4…`. Stderr is empty. All six `SELFTEST_CASE … PASS` lines are present, followed by `SELFTEST: PASS (6 cases)`. The tail equals the full stream for this row. An independent run at `336565f` (`registry-C`) produced the same stdout digest.
- **Gate result:** `bundle.json` sha256 is `3d6c99b7…`, matching `expected.json`. `replay-gate-A` reports exit 0 with no findings. `command-binding.py` has the same digest, `d533dc1e…`, at `496d212`, at `336565f` and on disk.
- **Executed script:** `defect-probes.py` is byte-identical (`99297d96…`) at `28cae17`, `496d212` and `336565f`. The change in revision did not change what ran.
- **No retrofill:** `git diff 28cae17 336565f` changes nothing under `round-18` or earlier rounds; only the three registry rows are added. The full streams are new from `retain_streams=True` in `registry-check.py@496d212`. They are not projected back into historical observations.

**Field-level gap: runner result dropped**
- In `replay.py`, the bundle receipt copies only `got`, `stdout` and `stderr`.
- `registry-check.run_row` sets `held = got == expected_exit and not missing and cleanup_ok`. The `held`, `cleanup_error` and `stdout_missing` fields are not carried into the receipt, and `command-binding.py` never checks them.
- A row with exit 0, the token present and leftover child processes would be `held=false` in the runner but CLEAN in the gate.
- For this row `held=true` and there is no `cleanup_error`; across all 43 rows nothing is non-held. So this is latent, not an actual false acceptance.
- **Smallest safe correction:** either have the bundle drop or flag any receipt whose `runner_result.held` is not true, or add a required `cleanup_ok` receipt field that the gate checks.

**Things that are inferred or not authenticated**
- **Receipt argv is the declaration, not the observed process.** `replay.py` writes `'argv': list(row['argv'])`. Reading `run_row` statically, it runs `Popen(row["argv"])` on the same list, so the binding holds by code. But the gate's argv equality is true by construction for bundles from this producer. It catches hand-edited bundles, not a producer that ran something else. This is the disclaimed producer-authentication limit, a tradeoff rather than a fixable defect.
- **Cwd can no longer be checked.** `/tmp/tameshi-r23-replay-naxu6fzi` is gone (`test -e` fails). The receipt cwd and the bundle cwd are written from the same variable.
- **Environment is not recorded.** The `python3` version and the `row_env()` contents are not in the receipt.
- **`runner_sha256` hashes the wrong copy.** It hashes the working-tree `tools/registry-check.py`, not the clone's copy that actually ran. Both are `cba16646…`, so no impact now.
- **The gate trusts the bundle's own requirements.** It never compares them to `requirements.json` or `registry_sha256`. Only `replay.py` does that check before producing. A bundle that drops this row from both requirements and receipts, with a recomputed `expected.json`, would come out CLEAN. That is by design, because `expected.json` is the caller-trusted commitment.

**Adversarial change that would still pass**
`expect` pins only the substring `SELFTEST: PASS`, not the case count. If `selftest()` lost five of its six `record(...)` calls, or recorded none, it would print `SELFTEST: PASS (1 cases)` or `(0 cases)` and exit 0. Both the registry runner and the gate would accept it.
- This is a weakness in the frozen baseline contract, not a gate defect. The frozen contract must not change this round.
- **Correction for a future contract:** pin `SELFTEST: PASS (6 cases)`, or a per-case token set.

**Impacted axes:** calibration through receipt semantics (the dropped runner result) and contract strength (the weak needle). Historical R17-CMD-BIND is not claimed closed.
