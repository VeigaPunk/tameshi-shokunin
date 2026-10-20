# S02 — No-harm baseline: every lane selftest entry point

Seat: TameshiR18.S02BaselineSelftests · wave 1 · round 18
Question: at pinned rev `183f87b899e6cae46be98d251cbc87fb5118f6ca`, what state do the lane's
selftest/gate entry points report, run with every inherited `GIT_*` removed and cwd inside a
`/tmp` fleet-mirror clone? (Round-18 before-state for all instruments.)

## Method (observed)

- Clone: `/tmp/tameshi-r18w1-S02BaselineSelftests-I8SYG5` — `mkdir $W/fleet`, a symlink per
  `*-shokunin` sibling of the lane, then `git clone` of the lane and `checkout -q 183f87b...`
  in `$W/fleet/tameshi-shokunin`. `git rev-parse HEAD` = `183f87b899e6cae46be98d251cbc87fb5118f6ca`.
- `python3 tools/registry-check.py --list` does **not** exist at this rev:
  `registry-check: unknown argument '--list'`, exit **64** (usage). I used the sanctioned
  alternative: read `tools/registry.json` at the rev (schema `tameshi-entry-registry-v1`,
  sha256 `98bdc23c…e0630`, 29 rows: 28 active / 1 superseded; 12 rows `kind=selftest`).
- Selftests were executed one per process, `cwd` = clone root, `stdin=/dev/null`, environment =
  inherited env with **every** `GIT_*` key removed and `PYTHONDONTWRITEBYTECODE=1` (runner
  `/tmp/s02_run_selftests.py`, stdlib only). Inherited at call time were `GIT_EDITOR`,
  `GIT_PAGER`, `GIT_TERMINAL_PROMPT`; no `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_CONFIG*`
  was set. The regression call was repeated with those three also unset; same result.
- Whole run repeated a second time in a cleaned clone: every exit reproduced (table uses run 1;
  run 2 tallies identical).

## Table A — 12 registered `kind=selftest` rows (direct run, GIT_* scrubbed)

| # | row | command | exit | pass tally (official summary line) | s |
|---|---|---|---|---|---|
| 1 | repeat-control-selftest | `python3 tools/repeat-control.py --selftest` | 0 | `SELFTEST: PASS (29 cases)` | 0.7 |
| 2 | bash-witness-selftest | `python3 tools/bash-witness-study.py selftest` | 0 | `WITNESS_SELFTEST: 41/41 pass` + `VERDICT: PASS` | 0.05 |
| 3 | pin-disposition-selftest | `python3 tools/pin-disposition.py --selftest` | 0 | `SELFTEST: PASS (19/19)` | 0.9 |
| 4 | witness-metadata-selftest | `python3 tools/witness-metadata.py --selftest` | 0 | `SELFTEST: PASS 39/39` | 1.3 |
| 5 | evidence-disposition-selftest | `python3 tools/evidence-disposition.py --selftest` | 0 | `SELFTEST: PASS (56/56)` | 2.0 |
| 6 | context-capture-selftest | `python3 tools/context-capture.py --selftest` | 0 | `SELFTEST: PASS (49/49)` | 1.3 |
| 7 | mutate-and-run-selftest | `bash tools/mutate-and-run.sh --selftest` | 0 | `MUTATE_SELFTEST: 95/95 pass` + `VERDICT: PASS` | 5.5 |
| 8 | measure-round16-selftest | `python3 .ufo/evidence/round-16/measure.py --selftest` | 0 | `MEASURE_SELFTEST: 38/38 pass` | 0.8 |
| 9 | registry-check-selftest | `python3 tools/registry-check.py --selftest` | 0 | `SELFTEST: PASS (34 cases)` (incl. `live-root-warning PASS`) | 3.0 |
| 10 | measure-round17-selftest | `python3 .ufo/evidence/round-17/measure.py --selftest` | 0 | `MEASURE_SELFTEST: 94/94 pass` | 3.4 |
| 11 | trace-inputs-round17-selftest | `python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest` | 0 | `SELFTEST: 27/27` | 1.3 |
| 12 | assemble-round17-selftest | `python3 .ufo/evidence/round-17/coldread/assemble.py --selftest` | 0 | `SELFTEST: all checks passed` (77 `[ok]`, 0 `not ok`) | 0.1 |

All stderr empty. Sum of the 12 rows ≈ 20 s wall.

## Table B — selftest-shaped entries registered under other kinds, plus the named extras

| row | kind | command | exit | tally |
|---|---|---|---|---|
| assemble-round16-selftest | gate | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 | `SELFTEST: all checks passed` |
| reattribute-round16-selftest | probe | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 | `SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)` |
| mutate-and-run-regression | gate | `bash tools/mutate-and-run.sh --regression` | 0 | `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)` (117 s) |

Regression legs all exact, no flips: js-kimi-census, bash-surface-census, bash-tsukuroi-census,
bash-mado-verify, bash-checklist-run, js-claims-check, js-round-gate (7/7 PASS, each
`match=<n>/<n> flips=0`). Note for C1: baseline `cases=7`; the round-18 eighth leg would move this
line to `cases=8`.

## Table C — full registry replay (all 28 active + 1 superseded)

`python3 tools/registry-check.py --root . --json` (live-root mode inside the throwaway clone):

```
REGISTRY_CHECK: held=28/28 superseded=1        exit 0   (139 s wall)
```

The single superseded row behaves as designed and is excluded: `evidence-disposition-round14-superseded`
expect 0, got 2 (`status=superseded`). Every other row matched its registered exit (28/28), including
the three rows that expect exit 1 (`repeat-control-snapshot-mismatch`, `context-capture-missing-env`,
`context-capture-mapping-suffix`, `evidence-disposition-round17-before`). Every needle
(`stdout_contains`) was satisfied — that is what `held` asserts. This is the before-state of the
round's `--rev REV --json` no-harm gate (contract C2): it must still read 28/28 after the wave.

## Hygiene / no-harm observations

- **Selftests are non-writing in the lane tree**: after all 12 selftests + `mutate-and-run --regression`,
  `git status --porcelain` in the clone = 0 lines. Re-run in a cleaned clone: 0 lines again.
- **One active gate writes into the graded root**: `--only verify-round15` creates
  `.ufo/evidence/round-15/attempt-4/` (4 files) and `.ufo/evidence/round-15/verification-4.json`
  at the root. Attributed by isolation: remove both → run only that row → both reappear (exit 0,
  `held=1/1`). `registry-check` itself warns about this in live-root mode
  (`registry-check: warning: live --root mode runs rows in the lane; rows may write into the root`),
  and its selftest covers the warning (`SELFTEST_CASE live-root-warning PASS`). In the round's
  no-harm command (`--rev REV`) the write lands in a throwaway clone, so the live lane is safe;
  a bare `--root .` run against the live tree would dirty it. No lane/sibling repo was touched by
  this seat: every run was in the `/tmp` clone; no `GIT_*` variable pointed at the lane.
- **Tool before-state (sha256 of committed bytes at the rev)** — for diffing after the wave:

```
repeat-control.py       296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25
bash-witness-study.py   49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80
pin-disposition.py      331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c
witness-metadata.py     df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4
evidence-disposition.py f8f05c7aa601cf0b6f0907cc1ead2fc01acaad6a3c19e81888c084a969583e27
context-capture.py      c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726
mutate-and-run.sh       fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a
registry-check.py       0bf9d1d2971c9fe478823754c7b889315585b73361ee3146631f409c4c5a3765
round-16/measure.py     03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb
round-17/measure.py     d25d3d04cb26ca7c20ef7333baaa181c350c6ee912d58f648927fb835b3ce7f3
round-17/trace-inputs.py 521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070
round-17/assemble.py    8bcce2eafe37e5ca11e1a145e4c6c826071eca55917ddb464a1b6da190f6ccd1
registry.json           98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630
```

- `tools/trace-inputs.py` is **absent** at the rev (`git cat-file -e` → exit 128); the registered
  trace selftest therefore runs the round-17 copy, consistent with contract B (promotion is new work,
  and the round-17 copy must stay byte-identical: `521be955…53070`).
- No tool installed or upgraded during this task.

## Gaps

- `--list` (named in the ticket) is not implemented in the rev's `registry-check.py`; usage is the four
  documented selectors. Inventory was taken from `tools/registry.json` as the ticket's alternative allows.
- `assemble.py --selftest` (round 17) prints no numeric case tally; its count above is the literal
  `[ok]` line count (77), which is its own check granularity, not a registry field.

## Verdict

holds — at 183f87b with all `GIT_*` scrubbed, the 12 registered selftests, `mutate-and-run --selftest`
(95/95) and `--regression` (7/7 legs, flips=0) are all green and lane-clean, and the full registry
replays held=28/28 superseded=1; the only root-writing entry observed is gate `verify-round15`.
