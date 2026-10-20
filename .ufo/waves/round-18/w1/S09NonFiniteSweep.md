# S09 — non-finite / out-of-range numeric config sweep (round 18, wave 1)

Seat: `TameshiR18.S09NonFiniteSweep` (leaf, advisory). Rev under test:
`183f87b899e6cae46be98d251cbc87fb5118f6ca`. No lane file edited; only this report
written. All execution in a throwaway fleet-mirror clone
`/tmp/tameshi-r18w1-S09NonFiniteSweep-VPJi7M/fleet/tameshi-shokunin` (all `GIT_*`
scrubbed by `env`/shell env; no lane git write).

## Method

Swept every executable in the lane that reads numeric configuration:

- `git grep -n 'type=int|type=float|int(os.environ|float(os.environ' tools/ .ufo/evidence/round-17/`
  → only `tools/bash-witness-study.py:1610,1612` has typed numeric argv; every other
  numeric enters via raw strings (bash) or JSON.
- `git grep -n 'json.loads|parse_constant|json_int|_is_int|require_int'` over
  `tools/*.py` and the round-17 kit, then read each consumer and executed the
  reachable paths against crafted inputs.

Execution probes (in the clone, cwd = clone root):

```
python3 tools/registry-check.py --root . --registry /tmp/reg-s09-{nan,inf,ninf,zero,neg,bigexp,nansleep}.txt --json
bash tools/mutate-and-run.sh --target /tmp/s09-target.c --defects /tmp/s09-spec.txt --suite 'exit 0' --timeout <token>
bash tools/mutate-and-run.sh --regression --timeout <token>
python3 -c '... build_parser().parse_args(["run","--timeout","-5","--tail","-4"])'
```

## Findings (ordered by impact)

### F1 — `tools/registry-check.py` accepts `timeout_s` NaN / +Infinity and crashes mid-sweep, leaving the row's child alive (HIGH; the known C2 item, now measured end-to-end)

- Parse: `json.loads(raw.decode("utf-8"))` at `tools/registry-check.py:281` — no
  `parse_constant`, and `json.loads` also maps the literal `1e400` to `inf`.
- Validation: `tools/registry-check.py:221-228` rejects only
  `isinstance(ts, bool) | not isinstance(ts, (int,float)) | ts <= 0`. NaN compares
  false to `<= 0`; `+Infinity` is > 0. So both pass as "a positive number".
- Consumption: `proc.communicate(timeout=row["timeout_s"])` at
  `tools/registry-check.py:383`.
- Observed (clone, exit codes measured):

| `timeout_s` | exit | observed |
|---|---|---|
| `NaN` | 1 | `ValueError: cannot convert float NaN to integer` (selectors.py:395), uncaught traceback |
| `Infinity` | 1 | `OverflowError: cannot convert float infinity to integer`, uncaught traceback |
| `1e400` | 1 | same `OverflowError` (JSON exponent → inf; no literal needed) |
| `-Infinity` | 2 | `REGISTRY_CHECK: could-not-evaluate (registry invalid: rows[0].timeout_s must be a positive number)` |
| `0`, `-1` | 2 | same validation error |

- Exit-map impact: the documented map (`tools/registry-check.py:49-51`) is
  `0 all held · 1 any differs · 2 could-not-evaluate`. A NaN/Inf registry is
  reported as **"a row differs"**, not could-not-evaluate — the C2 probe P09
  contract ("closed = exit 2 with a validation error naming timeout_s") is
  currently unmet in the worst way (crash + wrong class).
- Child leak: with argv `python3 -c "import time; time.sleep(30)"`, the tool
  exited 1 and `pgrep -af S09CANARY` still listed the child (pid 2437697);
  `start_new_session=True` (`:371`) plus the uncaught exception means `_kill_group`
  never runs. The orphan can keep writing into the graded root.
- Test pinning: **none**. The selftest `row()` helper hardcodes `timeout_s: 30`
  (`:620`); the only other fixtures use `5` (`:971`, `:1060`). There is no case for
  `0`, negative, NaN, Infinity, or `1e400`, so even the existing `ts <= 0` guard is
  unpinned (a `<=`→`<` mutant survives). Contract C's new selftest cases are
  therefore load-bearing, not redundant.

### F2 — `tools/mutate-and-run.sh` non-integer `--timeout`/`--tail` abort with exit 1, colliding with the DEGRADED / FAIL exit (MEDIUM)

- Parse: `need_val` only checks non-empty (`:1851-1852`); values are interpolated
  straight into arithmetic at `:462-463` (run) and `:1211-1212` (`--regression`).
- Observed (clone):

| invocation | exit | line |
|---|---|---|
| `--timeout nan` | **1** | `tools/mutate-and-run.sh: line 462: nan: unbound variable` |
| `--timeout NaN` / `abc` | **1** | same, `line 462` |
| `--regression --timeout nan` | **1** | `line 1211: nan: unbound variable` |
| `--timeout 0` / `-5` / `5x` / `08` | 64 | `--timeout must be a positive integer` (correct) |
| `--timeout +5` | 0 | accepted, runs as 5 |
| `--timeout 0x10` | 0 | accepted, runs as 16 |
| `--tail nan` | **1** | `line 463: nan: unbound variable` |
| `--tail -1` / `0` | 64 | correct |

- Mechanism: a bare alphabetic token is a valid bash arithmetic *identifier*; with
  `set -u` an unbound-variable expansion is fatal, so the `(( … )) || usage_exit`
  guard never runs. Tokens that are arithmetic *syntax errors* (`5x`, `08`) do
  reach `usage_exit` (64), hence the two-class split.
- Impact: exit 1 is documented as `done-with-inconclusive (DEGRADED)` for a run and
  `≥1 case FAIL` for `--regression` (`:78-79`, `:121-122`). A mistyped timeout is
  therefore indistinguishable from a real degraded sweep or a regression failure to
  any wrapper that keys on the exit code. Round-18's own count
  (`--regression` cases=8 PASS) keys on exit 0 vs non-zero, so the misclass would
  not fake a PASS, but it can fake a FAIL/DEGRADED.
- Test pinning: none — every selftest invocation passes a valid timeout
  (`:1418,1433,1448,1454,1460,...`).

### F3 — `tools/bash-witness-study.py` accepts negative/zero `--timeout`/`--tail` at its own boundary (LOW)

- `sp.add_argument("--timeout", type=int, …)` / `--tail` at `:1610-1612`; no range
  check before `run_sweep(...)` (`:946`).
- Measured parser acceptance: `Namespace(mode='run', timeout=-5, tail=-4)` and
  `timeout=0, tail=0` both parse with exit 0.
- Downstream `mutate-and-run.sh` refuses (`64`), and `_execute_sweep` maps any exit
  other than 0/1 to `could-not-evaluate` (`:927-934`), so no silent run occurs.
  The defect is classification/ergonomics: a usage error surfaces as exit 2
  (could-not-evaluate) rather than 64. `type=int` already rejects `nan`/`inf`
  strings (argparse `int()`).
- Test pinning: none for invalid values.

### F4 — `tools/context-capture.py` admits non-finite numbers in documents it calls "strict JSON", and does not range-check `runner_call.line` (LOW)

- `parse_json_strict` (`:335-347`) and `embedded_json` (`:786-788`) call
  `json.loads(..., object_pairs_hook=_no_duplicate_keys)` with **no**
  `parse_constant`, while the error text claims `"is not strict JSON"`. A receipt
  or embedded baseline/injected document containing `NaN`/`Infinity` parses and is
  re-serialized by `canonical_payload` (`json.dumps` emits the non-RFC token
  `NaN`), so the canonical digest is over non-standard JSON. No downstream numeric
  consumer of those documents was found to be weakened (all ints go through
  `require_int`, `:414-421`, which enforces `type is int`), hence LOW.
- `require_int` has no minimum. `scope["line_start"]` is explicitly checked
  `>= 1` (`:702`), but `runner_call.line` (`:763-764`) accepts `0` and negative
  values. The field is declared metadata (compared only for leg/repo/path/pin
  constants at `:1084-1105`), so impact is a receipt that asserts an impossible
  line and still validates — an inconsistency with the adjacent `line_start`
  rule rather than a false pass of a gate.
- Test pinning: `grep -i nan tools/context-capture.py` → no matches; no case
  pins either point.

### F5 — `tools/evidence-disposition.py` non-finite rejection is correct but unpinned (LOW, mutant-bait)

- Both parses use `parse_constant=_reject_constant` (`:221-234`, `:830`), and all
  consumed counts enforce `type is int` plus `< 0`/`>= 0` bounds (`:243-244`,
  `:714-730`, `:797`, `:840-845`, `:953`). NaN therefore cannot enter logic.
- No selftest case exercises a `NaN`/`Infinity` payload (`grep -n 'nan|constant'`
  finds only code, never a `SELFTEST_CASE`). Removing `parse_constant` would
  leave the suite green — a surviving mutant of exactly the R17 class.

## Positive controls (checked, safe)

- `tools/witness-metadata.py` — strict parse with `_reject_constant`
  (`:285-298`) **and** a selftest that feeds `{"schema": NaN}` and expects red
  (`:745`, `:978-981`). Holds, pinned.
- `tools/repeat-control.py` — `--runs` is `re.fullmatch(r"[0-9]+")` + `runs < 3`
  refusal (`:258-262`) → rejects `nan`, negatives, zero; snapshot `runs` and
  `expected_exit` require `int` not bool (`:374-388`). Holds.
- `tools/pin-disposition.py` — manifest `json.loads` at `:590` lacks
  `parse_constant`, but every consumed field is a validated string
  (leg/repo/path/40-hex/64-hex, `:596-660`); no numeric config reaches logic.
  Parse laxity only, no impact found.
- `.ufo/evidence/round-17/measure.py` (ancestor of the round-18 `measure.py`,
  contract F) — ledger/receipt `json.loads` at `:398` and `:556` lack
  `parse_constant`, but every consumed numeric goes through `json_int`
  (`:292-296`: `type is int`, `>= 0`), so NaN → `malformed-entry` (fail-closed).
  Holds by strict int typing; recommend the new copy keep `json_int` and add
  `parse_constant` as defence in depth.
- `tools/mutate-and-run.sh` valid numerics: `0`/negative/trailing-garbage are all
  refused with 64; only identifier-shaped tokens hit F2. `+5` and `0x10` are
  accepted by bash arithmetic as 5/16 — permissive, not unsafe.

## Recommendations (advisory; C2/C3 owners decide)

1. `registry-check.py`: parse with `parse_constant` rejecting `NaN`/`Infinity`/
   `-Infinity` **and** `math.isfinite(ts) and ts > 0` in `registry_errors`, so
   `1e400` is caught too; exit 2 naming the row. Add selftest rows for NaN,
   Infinity, `1e400`, `0`, `-1` (contract C).
2. `mutate-and-run.sh`: before the arithmetic, require
   `[[ "$TIMEOUT_S" =~ ^[0-9]+$ ]] && [[ "$TAIL_N" =~ ^[0-9]+$ ]]` (or an
   explicit `case` numeric guard) and `usage_exit` on failure — never let a token
   reach `(( ))` as an identifier. Add a selftest case asserting exit 64 for
   `--timeout nan` and `--tail nan` in both modes.
3. `bash-witness-study.py`: a custom argparse type that enforces `>= 1` (usage 64)
   so an invalid value is a usage error, not could-not-evaluate.
4. `context-capture.py`: add `parse_constant=_reject_constant` (matching
   evidence-disposition) and give `require_int` a `minimum` (line `>= 1`).
5. `evidence-disposition.py`: add a NaN/Infinity fixture so the existing defence
   is mutation-covered.

## Remaining unknowns

- No committed caller was found that passes a non-integer timeout string to
  `mutate-and-run.sh`; F2 is a CLI misclassification, not an observed lane
  regression.
- The round-18 `measure.py`/`assemble.py`/`defect-probes.py` do not exist at the
  dispatch rev, so contract F's new files could not be audited — only their
  round-17 ancestor.
- Whether the L1 wants F2 fixed inside this wave is a scope call; the report is
  advisory.

Verdict: **falls** — the lane is not uniformly finite-number disciplined: `registry-check` accepts NaN/+Infinity/`1e400` `timeout_s` and crashes mid-sweep (exit 1, orphaned child, no test), and `mutate-and-run.sh` kills itself with exit 1 on identifier-shaped timeout tokens, colliding with its DEGRADED/FAIL exit; all other numeric surfaces (repeat-control, witness-metadata, evidence-disposition, measure.py consumption) hold, with evidence-disposition's defence unpinned.
