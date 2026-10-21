# Replay43 — `wave-accounting-wrong-count-entry` (round-23 W2 falsification)

**Agent:** TameshiR23.Replay43  
**Scope:** Single registry row only  
**Tooling installs:** none

## Godspeed axes

| Axis | Result |
|------|--------|
| Frozen argv identity | Match across baseline, requirements, replay |
| Exit + stdout token binding | Exact substring match; held on replay |
| Defect semantics (wrong wave2 counts) | **Not bound** by frozen tokens |
| Execution evidence vs inference | **Present** in replay artifacts |
| Producer authentication | Correctly **not** claimed |

## Frozen contract (baseline `28cae179`)

```json
{
  "argv": [
    "python3",
    "tools/wave-accounting.py",
    "--bundle",
    ".ufo/evidence/round-22/wrong-count-bundle.json",
    "--expected",
    ".ufo/evidence/round-22/wrong-count-expected.json",
    "--json"
  ],
  "expect": {
    "exit": 1,
    "stdout_contains": [
      "TOTAL_MISMATCH",
      "\"completed\": 66",
      "\"dead\": 80"
    ]
  }
}
```

Sources checked (byte-identical for this row): `registry-baseline.json`, `requirements.json` (`source_revision` `28cae179…`), `git show 28cae179:tools/registry.json`.

Fixture intent: `wrong-count-bundle.json` wave2 `claimed` `{completed: 40, dead: 35, seats: 75}` vs observed `{38, 37, 75}` from outcomes.

## Evidence presence (not inferred)

Replay at `496d212…` in clone `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`:

| Field | Location | Value |
|-------|----------|--------|
| Full stdout/stderr | `replay/observations.json` → `rows[]` → `runner_result.stdout` | Complete JSON (not tail-only) |
| Receipt | `replay/bundle.json` → `receipts[]` | Same stdout as observations (`stdout` equality verified) |
| Invocation | `argv`, `cwd`, `revision`, `measurement_interval` | Recorded per row |
| Runner | `observations.json` `runner_sha256` | Pins `tools/registry-check.py` used by `replay.py` |

`replay-command-A.json` line: `wave-accounting-wrong-count-entry 1 True`.  
Observed: `got=1`, `expect=1`, `held=true`, `elapsed_s≈0.084`.

Full stdout (abbreviated structure):

- `finding_ids`: `["TOTAL_MISMATCH"]`
- `findings[0]`: `wave=wave2`, detail `claimed={40,35,75} observed={38,37,75}`
- `total`: `{completed: 66, dead: 80, seats: 146}` (sum of **observed** wave rollups)
- `authority`: declares retained callbacks; **not** provider authentication

`command-binding.py --bundle replay/bundle.json --expected replay/expected.json`: exit **0**, `finding_ids` **[]** (whole bundle clean).

## Static exact binding — confirmed

For this row, `command-binding.py` `evaluate()` confirms exact match on:

- `argv` (no shell normalization)
- `cwd` == bundle `cwd`
- `revision` == bundle `revision`
- `exit` == 1
- All three `stdout_contains` needles present in retained stdout

No reliance on `stdout_tail`, `held` flags, or source-read paths for binding.

## Field-level false acceptance — **yes**

Frozen `stdout_contains` does **not** pin the wave-local wrong-count defect:

1. **`"completed": 66` / `"dead": 80`** match only the top-level `"total"` block. They do **not** appear in the mismatch `detail` (which uses 40/35 vs 38/37). Any exit-1 JSON that still emits the same aggregate `total` literals satisfies these needles regardless of which wave failed or what claimed/observed pair is reported.

2. **`TOTAL_MISMATCH`** is a bare substring needle. It matches inside longer tokens (e.g. `TOTAL_MISMATCH_X` in `finding_ids`) — verified: `'TOTAL_MISMATCH' in 'TOTAL_MISMATCH_X'` is true. Replacing ids with a non-prefix code (`WRONG_CODE`) correctly yields `STDOUT_MISMATCH`.

3. **No needle** requires `"wave": "wave2"`, `claimed={'completed': 40`, or the observed 38/37 pair.

### Concrete adversarial delta (replay bundle semantics)

Using live `command-binding.evaluate()` on a copy of the retained receipt:

| Mutation | `evaluate()` exit | Findings |
|----------|-------------------|----------|
| Change finding `"wave": "wave2"` → `"wave1"` only | **0** | `[]` |
| Tamper detail `claimed` 40/35 → 99/99 | **0** | `[]` |
| Replace all finding ids with `WRONG_CODE` (no `TOTAL_MISMATCH` substring) | **1** | `STDOUT_MISMATCH` |
| Receipt `exit` 0 with same stdout | **1** | `EXIT_MISMATCH` |

**Interpretation:** Registry + command-binding treat this row as “exit 1 + generic mismatch marker + frozen aggregate totals,” not as “wave2 wrong-count fixture fired with the pinned claimed/observed delta.” That is a calibration gap, not an argv/cwd/revision miss.

## Rejected claims

- **Producer authentication:** Tool output and binding doc explicitly disclaim it; no retrofill of producer-checked metadata into replay receipts.
- **Source-read as execution:** `actual-source-read.json` is separate `cat tools/registry.json`; replay row evidence comes from `replay.py` clone execution, not from that read.
- **Historical metadata retrofill:** `measurement_interval` and full streams are attached by the round-23 replay instrument to **new** observations only; not backfilled into round-22 registry tails.

## Calibration verdict

| Question | Answer |
|----------|--------|
| Evidence actually present? | **Yes** — full stdout in `replay/bundle.json` and `replay/observations.json` |
| Static exact argv/expect binding? | **Yes** — matches baseline and passes `command-binding` on retained receipt |
| False acceptance on stdout semantics? | **Yes** — wave/detail semantics and substring `TOTAL_MISMATCH` weakness |
| Recommended tighten (informational only) | Add needles such as `"wave\": \"wave2\""` and/or a literal from the intended `detail` line; or require absence of `"finding_ids\": []"` plus wave-scoped tokens |

**Judged calibration:** Binding layer is honest for structural fields; **outcome tokens over-accept** relative to the row name and fixture intent.
