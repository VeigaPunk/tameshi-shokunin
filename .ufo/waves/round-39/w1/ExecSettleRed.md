# ExecSettleRed — round-39 w1 finding

Milestone: Settlement red · Judged on: depth · Leaf seat, no dispatch.

## Requested verdicts — both as the contract's `settlement` section declares

Command 1 (cwd = lane root):

```
$ python3 tools/wave-parent-settle.py --selftest
WAVE_PARENT_SELFTEST: 3/3 pass
SELFTEST_EXIT=0
```

Command 2 — red receipt `{"parent_exit_unix":10,"seats":[{"name":"a","terminal_unix":20}]}`
(`/tmp/tameshi-r39-ExecSettleRed/red.json`, `tools/wave-parent-settle.py --receipt`):

```
$ python3 tools/wave-parent-settle.py --receipt /tmp/tameshi-r39-ExecSettleRed/red.json
WAVE_PARENT: verdict=UNSETTLED detail=parent exited before last seat terminal
RED_EXIT=1
```

`UNSETTLED` is reached by the **early-exit** rule (`:31-32`), not by the missing-terminal
rule (`:27-28`) — the detail string pins which branch fired. This matches
`.ufo/evidence/round-39/contract.json` `settlement.red_fixture` exactly.
Both requested verdicts are correct. The findings below are outside those two fixtures.

## Depth: the selftest does not pin the predicate's own boundary

All mutants are copies under `/tmp/tameshi-r39-ExecSettleRed/`; the live checkout is
byte-untouched.

| Mutant | Edit | `--selftest` | Verdict on a boundary receipt |
|---|---|---|---|
| M1 | drop `parent_exit < last` branch | `2/3 pass`, exit 1, `FAIL red` | killed |
| M3 | `if parent_exit <= last and False` | `2/3 pass`, exit 1, `FAIL red` | killed |
| M2 | drop terminal guard | traceback `TypeError` at `:31` | killed by crash, no labeled FAIL |
| **M7** | `:31` `<` → `<=` | **`3/3 pass`, exit 0** | **survives** |
| **M4** | `:21` `isinstance(parent_exit,int)` → `parent_exit is None` | **`3/3 pass`, exit 0** | **survives** |
| **M5** | `:27` `isinstance(terminal,int)` → `terminal is None` | **`3/3 pass`, exit 0** | **survives** |

M7 is the sharp one. The contract predicate is `parent_exit_unix >= max(terminal_unix)`,
i.e. equality is SETTLED. M7 inverts that boundary and the selftest still reports 3/3:

```
$ python3 /tmp/tameshi-r39-ExecSettleRed/m7_strict_ge.py --selftest
WAVE_PARENT_SELFTEST: 3/3 pass          # exit 0
$ python3 /tmp/tameshi-r39-ExecSettleRed/m7_strict_ge.py --receipt .../equal.json   # parent 25, terminals 20 & 25
WAVE_PARENT: verdict=UNSETTLED detail=parent exited before last seat terminal        # exit 1
$ python3 tools/wave-parent-settle.py --receipt .../equal.json                       # live control
WAVE_PARENT: verdict=SETTLED detail=parent exit >= last seat terminal                # exit 0
```

Cause: `selftest` cases at `:37-48` are red (10<20), green (30 vs 20,25) and
missing-terminal. None exercises `parent_exit == max(terminal)`, so `:31` has no
equality case; none supplies a non-int `parent_exit`, so `:21` is unpinned; the
missing-terminal case at `:48` uses an *absent* key, so `:27`'s type intent is
unpinned. Three of six mutants survive a 3/3 pass.

## Depth: type guard accepts booleans, and malformed receipts masquerade as UNSETTLED

`isinstance(x, int)` is True for `bool` in Python, so a seat with no timestamp but a
JSON `true` settles:

```
$ printf '{"parent_exit_unix":30,"seats":[{"name":"a","terminal_unix":true}]}' > /tmp/.../boolterm.json
$ python3 tools/wave-parent-settle.py --receipt /tmp/.../boolterm.json
WAVE_PARENT: verdict=SETTLED detail=parent exit >= last seat terminal     # exit 0
```
Symmetrically `parent_exit_unix:true` with `terminal_unix:0` → `SETTLED`. Criterion 78
(`corpus/QUALITY.md:931-941`) requires "every seat has a terminal timestamp"; `true` is
not a timestamp, yet `:21`/`:27` accept it.

Malformed input collides with the documented exit codes (`:9` reserves 2 for usage):

```
$ python3 tools/wave-parent-settle.py --receipt /tmp/.../array.json    # top-level list
AttributeError: 'list' object has no attribute 'get'   at :17          # exit 1
$ python3 tools/wave-parent-settle.py --receipt /tmp/.../nope.json     # missing file
FileNotFoundError                                                       # exit 1
$ python3 tools/wave-parent-settle.py --receipt /tmp/.../scalar_seat.json  # seats:[1]
AttributeError: 'int' object has no attribute 'get'   at :25           # exit 1
$ python3 tools/wave-parent-settle.py                                   # no args
NOARGS_EXIT=2
```
Exit 1 is the tool's own UNSETTLED code, so a caller keying only on exit status reads a
corrupt receipt as a genuine early parent exit. `--receipt` never validates the
top-level object or `seats[]` element shape (`:17`, `:25`).

Also `:21` reports `parent_exit_unix missing` for a *present* float (`30.5`), so the
detail string misstates the cause.

## Depth: the receipt shape has no producer anywhere in the lane

The lane's real dispatch record `.ufo/waves/round-39/dispatch-w1.json` carries
`registry.members` (64 entries: `agent`, `agentId`, `role`, `name`, `path`, `reportDir`,
`task`, …), `counts{spawn:64}`, and **no** top-level `parent_exit_unix` and no `seats`
list. Fed directly to the tool:

```
$ python3 tools/wave-parent-settle.py --receipt .ufo/waves/round-39/dispatch-w1.json
WAVE_PARENT: verdict=UNSETTLED detail=no seats      # exit 1
```

`grep -rn "parent_exit_unix\|terminal_unix"` over the lane returns only the tool itself,
`corpus/QUALITY.md:940`, `contract.json`, and the round-39 spec/dispatch task strings.
No tool or dispatch step writes a settlement receipt (`tools/registry-check.py`,
`tools/wave-accounting.py`, `tools/receipt-*.py` have no terminal/parent concept —
`grep -n "terminal\|parent_exit" tools/*.py` hits only `wave-parent-settle.py` and
unrelated `selftest_terminal` uses in `bash-witness-study.py`). Both fixtures are
hand-written; on the lane's actual record the tool cannot express a verdict at all.

`git cat-file -e 50aadd1bbd94e43cd3fcfb81459414394db2dc35:tools/wave-parent-settle.py`
→ fatal, exit 128: the tool does not exist at the frozen lane base rev, it lands at
HEAD `233077f` ("round-39: freeze C1 guard counter and C2 write-path census before data").
So settlement has no base-rev control run; only the tool's own selftest can be measured
at base, and it is absent there.

## Consequence for the milestone

The two assigned verdicts hold: selftest 3/3 exit 0, red receipt UNSETTLED exit 1, and
the red verdict is reached by the branch criterion 78 names. What does not hold is
criterion 78's "falsifier that must fail": the failing selftest it promises is real for
M1/M3 (2/3, exit 1) but absent for a `<=` at `:31`, which flips the contract's equality
boundary to UNSETTLED and still prints `3/3 pass`. An admission rule that trusts a bare
`3/3` cannot distinguish that mutant from the committed tool.

## Bounds / hygiene

- No edit to the live lane checkout; every mutant and receipt is under
  `/tmp/tameshi-r39-ExecSettleRed/`. Lane jj/Git index, `.git`, `.ufo/state`,
  domain trees and `considerthese/` untouched.
- No package installs or updates this run; no pacman transaction attempted.
- No subagents, background jobs, or variant dispatch.

## Risks

- Exit-code-only callers will read a malformed receipt as UNSETTLED (exit 1).
- `terminal_unix: true` / `parent_exit_unix: true` settle a seat that recorded no
  timestamp.
- Feeding the real dispatch record yields `no seats`, which is indistinguishable in
  shape from a legitimate empty dispatch.
