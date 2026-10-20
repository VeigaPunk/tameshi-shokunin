# Wave 2 — FalsifyUsage (critic, static review only)

Seat: `TameshiR15.FalsifyUsage`. Static review only: nothing was executed and no selftest, check, or build was run. No tools were installed or updated.

## Source read

- `tools/context-capture.py` (snapshot tag `472A`): lines 1-118 (docstring, exit map, stable IDs), 252-292 (`USAGE`, `UsageError`, `CouldNotEvaluate`), 317-350 (`parse_json_strict`, `read_regular`), 1186-1217 (`validate_expected`, `load_expected`), 1222-1346 (`make_result`, `emit`, `apply_expected`, `result_from_exception`, `run_check`), 1572-1726 (`SELFTEST_ENV`, `SelftestHarness`), 1990-2116 (usage cases, `run_selftest`, `parse_argv`, `main`).
- `corpus/lessons/round-14-verifier-spotcheck.md`: lines 154-162 (Routed defects; item 5 requires an explicit 64-to-could-not-evaluate mapping and a standalone self-invocation with literal exit/ID pairs).

## Counterexample: a missing option value is swallowed when the next token is a flag, so the run exits 2 instead of 64

`parse_argv` (lines 2050-2064) treats any non-empty next token as the option value, including a known flag. It only checks `index + 1 >= len(argv)` and `not value`. The tool's own intent is that a missing value is a usage error (line 2052, `UsageError(argument + " needs a value")`). That intent is enforced only when the option is the last token.

Hand trace (static, not executed) of `context-capture.py --check --expected E --receipt --json`:

1. idx0 `--check` sets `mode=check`.
2. idx1 `--expected` sets `expected="E"` (idx moves to 3).
3. idx3 `--receipt`: `value=argv[4]="--json"`, which is non-empty. So `receipt="--json"` and idx moves to 5. `--json` is consumed as a path, so `as_json` stays `False`.
4. Line 2073: both values are set, so no `UsageError`. `main` calls `run_check` in explicit mode.
5. `load_expected("E")` (line 1313) runs:
   - If `E` is absent, it raises `CouldNotEvaluate("expected_missing")`. `main` (2101-2105) catches it and the run exits **2** with id **`expected_missing`**.
   - If `E` is a valid pin, `read_regular("--json", …)` (1318) reads a file literally named `--json` from the cwd. When that file is absent, the run exits **2** with id **`receipt_missing`**, and the output is text even though the caller asked for `--json`.

The mirror form `--check --receipt --json --expected E` reaches `receipt="--json"` in the same way.

Expected under the tool's own contract: `usage_error` / **64** ("--receipt needs a value"). Observed by trace: a could-not-evaluate result with exit 2 under a non-usage ID, or a different exit if a file named `--json` happens to exist. That file would still be stopped by the digest pin, so this is not a live-capture breach.

Selftest gap: the five usage cases (lines 1996-2002) are `[]`, receipt-without-expected, expected-without-receipt, `--check --bogus`, and `--selftest --json`. None of them covers a missing option value, either as the final token or followed by a flag. So the "needs a value" branch and this swallow path are not pinned by a literal exit/ID pair.

Impacted axes:
- C1 exit-class mapping: 64 is reserved for "usage / could-not-evaluate invocation", but an invocation defect falls into the exit-2 receipt/expected classes.
- Stable-ID determinism: the reported ID depends on the filesystem (`expected_missing` vs `receipt_missing`).
- `--json` output contract: the flag is silently dropped.

This is a fixable defect, not a tradeoff.

## Smallest safe correction

1. In `parse_argv`, after reading `value`, raise `UsageError(argument + " needs a value")` when `value` is one of the known tokens: `--check`, `--selftest`, `--json`, `--receipt`, `--expected`, `-h`, `--help`. A path that genuinely starts with `--` can still be passed as `./--x`.
2. Add usage cases that assert literal 64 plus `id=usage_error`:
   - `["--check", "--expected", "expected.json", "--receipt", "--json"]`
   - `["--check", "--receipt"]` (final-token missing value, which pins the existing branch)

No other semantics change.

## Checked and agreed (static only)

- **Unknown flag → 64:** `--check --bogus` reaches line 2066, then `main` (2088-2093) returns 64 and writes `CONTEXT: USAGE_ERROR (id=usage_error exit=64)` to stderr. The selftest pins this (2001, 1684-1691).
- **Help:** `-h` and `--help` give 0 only as the sole argument. Combined with anything else (for example `--check -h`), they are unknown arguments and give 64.
- **No accidental live capture on usage paths:**
  - Every `UsageError` returns before `run_check` (2088-2093), so nothing is read or written.
  - The tool never executes the probe or git.
  - Selftest subprocesses run with `-I`, `cwd` set to a temp case dir, and a fixed `SELFTEST_ENV`. Every check case passes explicit `--receipt`/`--expected`, so frozen mode is never entered.
  - If the pairing guard regressed into frozen mode, the 64 assertion would catch it.
- **Bounded observation (not a separate defect):** the `hermetic-no-lane-path` check (1701-1707) looks for the absolute `DEFAULT_LANE_ROOT` in subprocess output. A frozen-mode run only prints the relative `FROZEN_RECEIPT_REL`, so that check alone would not detect a frozen-mode live read. The protection against that comes only from the exit/ID assertions.
- **Usage-error output format:** usage errors are reported as text on stderr even when `--json` is given. Usage is decided before JSON mode is honoured, and the ID still appears on stderr. This is a tradeoff, not a defect.
