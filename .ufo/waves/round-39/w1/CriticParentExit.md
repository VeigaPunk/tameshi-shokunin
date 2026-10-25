# CriticParentExit — round-39 w1 finding

Milestone: Parent exit · Judged on: depth

## Question

Would a parent exit before seat terminals be SETTLED or UNSETTLED under
`tools/wave-parent-settle.py`, given the round-38 dispatch-outcome.md shape?

## Finding: UNSETTLED

A parent process exiting before the last seat terminal is classified **UNSETTLED**.
Two independent rules in `tools/wave-parent-settle.py` each reach that verdict on the
round-38 record:

1. **Early-exit rule** — `tools/wave-parent-settle.py:31-32`:
   ```python
   if parent_exit < last:
       return 'UNSETTLED', 'parent exited before last seat terminal'
   ```
   The docstring at `tools/wave-parent-settle.py:4-6` names this exact shape:
   "A parent that exits while seats are still running is UNSETTLED (the round-38
   failure shape)." Round-38 dispatch-outcome.md:44-45 records exactly that:
   "the dispatcher session's parent process exited while the 65 asynchronous seat
   jobs were still running (`DISPATCHER_EXIT=0`)".

2. **Missing-terminal rule** — `tools/wave-parent-settle.py:27-28`:
   ```python
   if not isinstance(terminal, int):
       return 'UNSETTLED', 'seat %s has no terminal' % name
   ```
   Round-38 dispatch-outcome.md:46-48: "the remaining 64 jobs left no terminal
   record at all" — 64 of 65 seats have no `terminal_unix`, so classification hits
   UNSETTLED before even comparing timestamps.

## Evidence (commands run, scratch only — live checkout untouched)

```
$ python3 tools/wave-parent-settle.py --selftest
WAVE_PARENT_SELFTEST: 3/3 pass                      # exit 0; 'red' case (parent_exit 10 < terminal 20) wants UNSETTLED

$ python3 tools/wave-parent-settle.py --receipt /tmp/tameshi-r39-CriticParentExit/early-exit.json
WAVE_PARENT: verdict=UNSETTLED detail=parent exited before last seat terminal   # exit 1

$ python3 tools/wave-parent-settle.py --receipt /tmp/tameshi-r39-CriticParentExit/r38-shape.json
WAVE_PARENT: verdict=UNSETTLED detail=seat Seat64NoTerminal has no terminal     # exit 1
```

Receipt JSONs were written under `/tmp/tameshi-r39-CriticParentExit/` per lane
bounds; no lane or fleet files were modified.

## Cited rule (one line)

`tools/wave-parent-settle.py:31-32` — `parent_exit < last` ⇒ UNSETTLED
("parent exited before last seat terminal"); SETTLED requires `parent_exit >= max(seat.terminal_unix)`
(`:33`, `:30`) **and** every seat carrying an int `terminal_unix` (`:27-28`).

## Consequence for the milestone

The round-38 outcome is doubly UNSETTLED — the parent exited before seat terminals
AND 64/65 seats never recorded a terminal. Any admission rule that requires the
parent to outlive its seats rejects this dispatch; the tool's own docstring cites
round-38 as the canonical failure shape.
