# Replay42 — `wave-accounting-selftest` (R23 W2 falsification)

**Seat:** TameshiR23.Replay42  
**Revision under test:** `496d212bc46789cdf8cafab72978bdb7f4182963` (replay instrument)  
**Frozen registry digest:** `requirements.json` ↔ `registry-baseline.json` verified  
**Tooling installs:** none

## Axes

| Axis | Question |
|------|----------|
| Command identity | Does frozen argv match baseline registry and replay invocation? |
| Outcome binding | Do exit and `stdout_contains` match receipt vs requirement? |
| Evidence presence | Is full stdout retained in replay artifacts, or inferred from tails/source-read? |
| Gate semantics | Can `command-binding.py` accept outcomes that did not run the selftest body? |
| Provenance | Are source-read / historical metadata treated as execution? (must reject) |

## Frozen contract (baseline)

From `registry-baseline.json` / `requirements.json` (identical slice):

- **name:** `wave-accounting-selftest`
- **argv:** `["python3", "tools/wave-accounting.py", "--selftest"]`
- **expect:** `exit: 0`, `stdout_contains`: `ACCOUNTING_SELFTEST: 8/8 pass`, `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass`, `FINDING: SELFTEST_PASS`
- **source anchor:** `SKILL.md@66a25abf9a07f99df6f8584044a83a21349706a1:1997`

`git show 496d212:tools/registry.json` row matches the baseline slice byte-for-byte on `name` / `argv` / `expect`.

## Actual retained invocation (replay)

**Producer:** `.ufo/evidence/round-23/replay.py` at `replay-command-A.json` (exit 0), line `wave-accounting-selftest 0 True`, `REPLAY: 43 / 43`.

**Receipt** (`replay/bundle.json`):

| Field | Value |
|-------|--------|
| argv | `["python3", "tools/wave-accounting.py", "--selftest"]` |
| cwd | `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin` (= bundle `cwd`) |
| revision | `496d212bc46789cdf8cafab72978bdb7f4182963` |
| exit | `0` |
| stdout length | **1112** bytes (complete, not a tail fragment) |
| stderr | empty |

**Observations** (`replay/observations.json`): same argv/cwd/revision; `runner_result.held === true`, `got === 0`, `expect === 0`; `stdout` **equals** `stdout_tail` (1112 bytes). Capture note: *complete decoded stdout/stderr*.

Full stdout (present on disk, verified by extraction):

- 8× `ACCOUNTING_CASE … ok`
- `ACCOUNTING_SELFTEST: 8/8 pass`
- 16× `ACCOUNTING_EXTRA_CASE … ok`
- `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass`
- `FINDING: SELFTEST_PASS`

**Replay gate on bundle:** `replay-gate-A.json` exit 0, `finding_ids: []` for digest-pinned `replay/bundle.json`.

## Static binding audit (`command-binding.py`)

Row-local `evaluate()` over the live receipt vs requirement: **no findings** (argv, cwd, revision, exit, all three stdout needles).

Cross-artifact: `bundle.json` receipt stdout **byte-identical** to `observations.json` `runner_result.stdout`.

## Field-level false acceptance (actual evidence)

**Not found** on the retained replay row. Frozen argv/expect, receipt fields, and full stdout align; `held` is consistent with `registry-check.run_row` semantics (exit + substring needles + cleanup).

## Concrete adversarial delta (gate semantics, not replay tamper)

`command-binding.py` checks only **literal** `stdout_contains` needles on the receipt stdout (stderr ignored for tokens). A tampered bundle could replace the 1112-byte stdout with **91 bytes**:

```text
ACCOUNTING_SELFTEST: 8/8 pass
ACCOUNTING_EXTRA_SELFTEST: 16/16 pass
FINDING: SELFTEST_PASS
```

With matching argv/cwd/revision/exit 0, `evaluate()` returns `(0, [])` — **no** `ACCOUNTING_CASE` / `ACCOUNTING_EXTRA_CASE` lines required. This matches the tool docstring: it validates retained declarations, **not** producer authenticity or selftest case coverage.

The **observed** replay receipt is materially stronger (24 case lines + summaries); the gap is between gate minimum and semantic selftest completion.

Secondary adversarial (monitoring): `registry-check` stores `stdout_tail` as the last `TAIL_BYTES` for default reports. For this row the replay instrument sets full `stdout` and tail equals full output; a **hypothetical** long stdout could drop early needles from tail-only review while still passing substring checks on full stream — not triggered here.

## Source-read / producer authentication (rejected)

- `source-read-gate-A.json`: exit **1**, `finding_ids: ["ARGV_MISMATCH"]` on `source-read-bundle.json` — source-read bundle is **not** a valid command receipt substitute.
- `actual-source-read.json` stdout is embedded **registry JSON text** (includes the `wave-accounting-selftest` row definition), not subprocess output from `tools/wave-accounting.py --selftest`. Must not credit as command execution or retrofill invocation metadata.
- Tool output authority string (`wave-accounting` gate JSON): *not provider authentication* — do not treat as producer attestation.

## Calibration verdict

| Claim | Result |
|-------|--------|
| Static exact binding (frozen ↔ baseline ↔ receipt) | **Confirmed** |
| Execution evidence actually present vs inferred | **Present** in `replay/bundle.json` + `replay/observations.json` (full stdout) |
| False acceptance on retained replay row | **None** |
| Adversarial delta for C1 gate | **91-byte forged stdout** satisfies `command-binding` without running selftest cases; actual receipt exceeds that minimum |

**Row status:** Replay-backed binding for `wave-accounting-selftest` is **calibrated** for argv/expect/receipt integrity; falsification target is the **intentional** shallow stdout token check, not a mismatch in the delivered replay artifacts.
