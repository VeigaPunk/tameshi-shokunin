# AttrFix — round-16 wave 1 report

Routed defect 2 repair (append-only re-attribution of round-15 usage-finding rows).
Seat: leaf executor; no delegation used, no messages sent.

## Files changed

- `.ufo/evidence/round-16/attribution/reattribute.py` — new; sha256 `8804ca2dcda2bd9355d2a795ad4bb45be8d0baad7be4b20a7c9bbef757145a81`. Stdlib only (argparse/hashlib/json/re/sys/pathlib).
- `.ufo/evidence/round-16/attribution/correction.json` — new, written by the script create-only; sha256 `344558958d8678215ed39f4fcafb556c06ea8574969f2c0b5501a5faff6aba41`.
- No other lane path written. `.ufo/evidence/round-15/verification-3.json` untouched: sha256 `3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce` before and after (printed on every run). `.ufo/evidence/round-15/verify.py` untouched.
- Scratch: `/tmp/tameshi-r16-AttrFix-dlyIUlCW/` only.

## What it does

1. Reads `verification-3.json`, verifies and prints its sha256.
2. Re-derives `observed_id` for every `kind="command"` check row under two rules:
   - **OLD** — verbatim copy of `verify.py`: `ID_TOKEN_RE = re.compile(r"id=([a-z_]+)")` at `verify.py:138`, applied at `verify.py:196-210` (JSON-last-line `id` when `stdout_is_result_json`, else first `id=` match in stdout then stderr). The receipt does not store `stdout_is_result_json`, so it is reconstructed positionally: `--json` is a flag unless it is the value of `--receipt`/`--expected` (`reattribute.py:_stdout_is_result_json`). This reproduces the recorded `observed_id` on all 14 command rows (`old_rule_fidelity_failures: []`).
   - **NEW** — id inside the last line matching `^[A-Z_]+: [A-Z_]+ \(id=([a-z_]+) exit=(\d+)\)$` on stderr, else stdout; none → null (`reattribute.py:VERDICT_LINE_RE`, `observed_id_new`).
3. Writes `correction.json` naming rows where both ids are concrete and differ — exactly `usage-proof-new` and `gate-usage`, both `context_consistent → usage_error`, each with its terminal `verdict_line` `CONTEXT: USAGE_ERROR (id=usage_error exit=64)`. Rows where one side is null (all `--json` rows: verdict travels in the JSON document, not a text line) are listed under `coverage_changes`, not corrections — they lose nothing the JSON doc did not already carry.

## Executed evidence

- `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` → exit 0. The single fixture is the receipt's `usage-proof-new` row verbatim (raw stderr was retained; no tool replay needed for the fixture). Same fixture, same oracle `observed_id == usage_error`:
  - `old rule: observed_id='context_consistent' oracle -> exit=1 (FAIL)`
  - `new rule: observed_id='usage_error' oracle -> exit=0 (PASS)`
  - `SELFTEST: PASS (old rule fails, new rule passes; same fixture+oracle, rule is the only delta)`
- `python3 .ufo/evidence/round-16/attribution/reattribute.py` → exit 0; `corrections: usage-proof-new context_consistent->usage_error, gate-usage context_consistent->usage_error`; `old rule reproduced every recorded observed_id (14 command rows)`; wrote `correction.json`. Re-run is idempotent (create-only write; identical bytes accepted, differing bytes refused).
- Independent replay (extra check, `/tmp` mirror): `git show 7650fe4db89f3a706aed63d048ac47e02289cc72:tools/context-capture.py` → `/tmp/.../context-capture.py`; both usage argv variants under `env -i PATH=/usr/bin:/bin LC_ALL=C` exited 64, and each emitted stderr **byte-identical** to the retained receipt stderr (`usage-proof-new`: `stderr identical to receipt: True`; `gate-usage`: True), terminal line `CONTEXT: USAGE_ERROR (id=usage_error exit=64)`.

## Root cause (as routed)

`verify.py:552` and `:558` define the usage rows with `expected_id=None` and only `stderr_token="id=usage_error"` (`:631-632`, `:713-717` calls), so the misparsed `observed_id` was recorded but never oracle-compared — receipts stayed green while attribution was wrong. The help text's exit table line `exit 0   clean retained receipt (id=context_consistent)` precedes the verdict on stderr, so first-`id=` grabs it.

## Risks / bounds

- `coverage_changes` (7 rows → null under the line rule) is informational, not a defect: those rows' ids live in the result JSON document. If L1 wants a single corrected-attribution stream for all rows, the new rule should be layered as JSON-first/verdict-line-fallback — flagged, not silently extended.
- `verify.py` itself is intentionally unmodified (routed repair is the append-only correction; a future verifier patch is a separate move).
- `correction.json` pins the receipt by sha256 (`source_receipt.sha256`); if the receipt were ever replaced the linkage breaks by design.

## Recommendations (bounded)

1. L1 may embed `correction.json` by reference in `corpus/lessons/round-16.md ## Mistakes` as the defect-2 repair evidence; the lesson's predicted two rows and both deltas match exactly.
2. If a round-17 verifier rewrite happens, extract ids as: result-JSON `id` → last structured verdict line → null; never scan help text.
3. No further action needed from this seat.

Tool installs/updates: none. No pacman transaction, no sibling-repo write, no credential/db access.
