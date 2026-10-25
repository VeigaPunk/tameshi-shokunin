# CriticParentExit — parent exit before last seat terminal is UNSETTLED

Milestone: CriticParentExit. Axis: calibration. Scratch: `/tmp/tameshi-r40-CriticParentExit/`.
Live checkout read-only; no lane file modified. Tool bytes hashed this run:
`sha256(tools/wave-parent-settle.py) = 0c4fd7a4217d9b0d908588911989b091114fb749f21fc96f4130145974c31323`
(identical to the round-39 review bytes — the defects noted there are still live).

## Finding: the claim holds — with two demonstrated false-SETTLED holes and one provenance gap

### 1. The headline rule is implemented and fires

`tools/wave-parent-settle.py:30-33`:

```python
last = max(terminals)
if parent_exit < last:
    return 'UNSETTLED', 'parent exited before last seat terminal'
return 'SETTLED', 'parent exit >= last seat terminal'
```

plus the fail-closed guards at `:19-22` (no seats / missing `parent_exit_unix`) and
`:27-28` (seat without int `terminal_unix`). Observed this run:

```
$ python3 tools/wave-parent-settle.py --selftest
WAVE_PARENT_SELFTEST: 3/3 pass                                        # rc 0
$ python3 tools/wave-parent-settle.py --receipt red.json        # {"parent_exit_unix":10,"seats":[{"name":"a","terminal_unix":20}]}
WAVE_PARENT: verdict=UNSETTLED detail=parent exited before last seat terminal   # rc 1
$ python3 tools/wave-parent-settle.py --receipt .ufo/waves/round-39/settlement-receipt.json
WAVE_PARENT: verdict=SETTLED detail=parent exit >= last seat terminal           # rc 0
```

This matches the frozen r39 predicate in `.ufo/evidence/round-39/contract.json:41`
("SETTLED iff every seat has a terminal timestamp and parent_exit_unix >= max(terminal_unix)")
and the round-38 failure shape the docstring cites (`:4-6`).

### 2. Boundary: `parent_exit == last` → SETTLED (per spec, but coarse)

`equal.json` `{"parent_exit_unix":25, terminal 25}` → `SETTLED`, rc 0. The predicate
says "before" ⇒ equality is contractually SETTLED. Calibration caveat, not a defect:
at 1-second `*_unix` granularity a parent that exits in the *same* second as the last
terminal is indistinguishable from one that exits after; the tool resolves the tie
toward SETTLED. If the judge wants strict-outlived semantics the fix is `<=` at `:31`
plus sub-second timestamps — flagging, not rewriting.

### 3. False-SETTLED counterexamples (demonstrated, fixable)

`bool` subclasses `int`, so `isinstance(x, int)` at `:21` and `:27` admits JSON `true`/`false`:

```
$ python3 tools/wave-parent-settle.py --receipt boolterm.json
  # {"parent_exit_unix":30,"seats":[{"name":"dead","terminal_unix":false}]}
WAVE_PARENT: verdict=SETTLED ...   # a seat with terminal `false` counts as terminated
$ python3 tools/wave-parent-settle.py --receipt boolparent.json
  # {"parent_exit_unix":true,"seats":[{"name":"a","terminal_unix":0}]}
WAVE_PARENT: verdict=SETTLED ...
```

Smallest safe correction: `type(x) is int` (or `not isinstance(x, bool)`) at `:21` and `:27`.
Round-39 seats (ExecSettleRed.md:62-64, MT15) reported the same hole; never patched —
the file sha is unchanged.

### 4. Malformed receipts crash with rc 1 — indistinguishable from UNSETTLED

```
$ python3 tools/wave-parent-settle.py --receipt scalar_seat.json   # {"seats":[1]}
AttributeError: 'int' object has no attribute 'get'   (:25)        # rc 1, no WAVE_PARENT line
$ python3 tools/wave-parent-settle.py --receipt toplist.json       # [1,2]
AttributeError: 'list' object has no attribute 'get'   (:17)       # rc 1
$ python3 tools/wave-parent-settle.py --receipt floatparent.json   # parent_exit_unix:30.5
WAVE_PARENT: verdict=UNSETTLED detail=parent_exit_unix missing     # rc 1 — value present, detail misstates
```

Any caller keying on exit code reads a crash as a legitimate UNSETTLED — false provenance
on the negative side too. Correction: `isinstance(receipt, dict)` and `isinstance(seat, dict)`
guards that return `'UNSETTLED', 'malformed receipt'` explicitly.

### 5. Provenance gap: nothing produces the receipt schema

No lane tool writes `parent_exit_unix`/`terminal_unix` — `grep` over the lane hits only the
tool itself, `corpus/QUALITY.md:940`, the r39 contract/spec strings, and the hand-assembled
`.ufo/waves/round-39/settlement-receipt.json`. Feeding the real r40 dispatch record:

```
$ python3 tools/wave-parent-settle.py --receipt .ufo/waves/round-40/dispatch-w1.json
WAVE_PARENT: verdict=UNSETTLED detail=no seats      # rc 1 — shape collision with a legit empty dispatch
```

So every verdict attests only to what a self-reported receipt *claims*. A dead seat that was
respawned and left a terminal under the same name is invisible to the classifier — which is
consistent with "do not replace a dead seat" (and the docstring's own `:7` disclaimer) but
means UNSETTLED/SETTLED proves receipt content, not observed parent/seat lifetimes.

## Bottom line

Predicate faithfully implemented at `:31-32`; red shape → UNSETTLED as claimed (rc 1,
selftest 3/3). Two defects the canonical judge should weigh: (a) `bool` terminals/exits
produce false-SETTLED (`:21`,`:27` — fix: `type(x) is int`); (b) malformed receipts exit 1
via traceback, aliasing crash to UNSETTLED (`:17`,`:25` — fix: dict guards returning a named
UNSETTLED detail). Tradeoff to note: `==` boundary and self-reported provenance are per-spec,
not defects to repair here.
