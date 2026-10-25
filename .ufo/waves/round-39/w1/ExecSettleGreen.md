# ExecSettleGreen — settlement green fixture

Seat: ExecSettleGreen (leaf). Milestone: Settlement green. Round 39, wave 1.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at HEAD `233077f88d7a8d142eff329202a120457a5d5258`
(`round-39: freeze C1 guard counter and C2 write-path census before data`).
No file in the live lane was edited except this report. No git/jj/index/state mutation. No pacman.

## Verdict line

```text
WAVE_PARENT: verdict=SETTLED detail=parent exit >= last seat terminal
```

Exit code `0`.

## Exact command and input

Receipt used (retained at `/tmp/tameshi-r39-ExecSettleGreen/green.json`):

```json
{"parent_exit_unix":30,"seats":[{"name":"a","terminal_unix":20},{"name":"b","terminal_unix":25}]}
```

Command (run from `/tmp/tameshi-r39-ExecSettleGreen`):

```text
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/wave-parent-settle.py --receipt green.json
```

Full retained log: `/tmp/tameshi-r39-ExecSettleGreen/run.log`.

## Why this is the frozen fixture

- `.ufo/evidence/round-39/contract.json:43` — `"green_fixture": "parent_exit_unix=30, seat terminals 20 and 25 → SETTLED"`.
- `.ufo/evidence/round-39/contract.json:41` — predicate: `SETTLED iff every seat has a terminal timestamp and parent_exit_unix >= max(terminal_unix)`.
- `tools/wave-parent-settle.py:16-33` implements exactly that: all terminals must be `int` (line 24-26), `last = max(terminals)` (line 30), `if parent_exit < last: UNSETTLED` (line 31), else `SETTLED` (line 33).
- Tool blob at HEAD: sha256 `0c4fd7a4217d9b0d908588911989b091114fb749f21fc96f4130145974c31323`. The tool does not exist at base rev `50aadd1bbd94e43cd3fcfb81459414394db2dc35` (`git rev-parse 50aadd1...:tools/wave-parent-settle.py` → fatal: path exists on disk, but not in base rev), so this classification is a HEAD-rev statement.

## Discriminating controls (same tool, same run log)

| receipt | parent_exit_unix | terminals | observed verdict | exit |
|---|---|---|---|---|
| `green.json` | 30 | 20, 25 | `SETTLED` | 0 |
| `red.json` | 10 | 20 | `UNSETTLED detail=parent exited before last seat terminal` | 1 |
| `missing-terminal.json` | 30 | none for seat a | `UNSETTLED detail=seat a has no terminal` | 1 |
| `--selftest` | — | — | `WAVE_PARENT_SELFTEST: 3/3 pass` | 0 |

Boundary probes, also retained in `/tmp/tameshi-r39-ExecSettleGreen/`:

- `eq.json` (parent 25, terminals 20/25) → `SETTLED`, exit 0. Confirms the `>=` boundary from contract.json:41.
- `one_before.json` (parent 24, terminals 20/25) → `UNSETTLED`, exit 1. One second earlier flips the verdict, so the green result is not a constant.
- `reordered.json` (seats listed 25 then 20, parent 30) → `SETTLED`, exit 0. Seat order does not affect `max`.

## Falsification attempt against the frozen predicate

No falsifier found. The green fixture classifies `SETTLED`; the red fixture and the
missing-terminal fixture classify `UNSETTLED`; the equality boundary is `SETTLED` and one
unit below it is `UNSETTLED`. The verdict line above is reproduced verbatim from
`/tmp/tameshi-r39-ExecSettleGreen/run.log`.

Residual edge, reported not fixed (outside the assigned fixture): `classify()` uses
`isinstance(x, int)`, and in Python `bool` is an `int` subclass, so a JSON receipt with
`"parent_exit_unix": true` and `terminal_unix: 1` would classify `SETTLED`. This does not
touch the frozen green/red fixtures and no predicate text was rewritten.

## Files changed

- `.ufo/waves/round-39/w1/ExecSettleGreen.md` (this report).
- Scratch only: `/tmp/tameshi-r39-ExecSettleGreen/{green,red,missing-terminal,eq,one_before,reordered}.json`, `run.log`.

## Risks / blockers

None blocking. Settlement classification of the assigned receipt is SETTLED at HEAD
`233077f88d7a8d142eff329202a120457a5d5258`.
