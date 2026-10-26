# T47HardCoverEntry — C2 (coverage) selftest additions

Seat `T47HardCoverEntry`, group `coverage`, deliverable
`.ufo/waves/round-47/w1/T47HardCoverEntry.addition.py` (one top-level `extra_T47HardCoverEntry()`,
helpers `_xT47HardCoverEntry_*`). It adds four cases that call the round-46 hardened counter's
`entry_ok()` **directly** with in-memory fixtures (a `rows` dict plus an entry text — no git repo,
no network, no subprocess), which is the stub form the author brief sanctions for code the round-46
`selftest()` does not reach.

Lane writes: this report and the addition file only. Scratch: `/tmp/tameshi-r47-T47HardCoverEntry/`.

## Result — 5 of 8 assigned mutants killed

| pool id | case that kills it | input that separates original from mutant | FAIL line observed (mutant run) |
|---|---|---|---|
| `entry_ok:cmp:0` (`<`→`<=`, 3-line trio minimum) | `T47HE_three_line_entry_ok` | entry with **exactly 3** lines: `source: S256 — upstream` / `verified-at: 2026-10-25` / `recheck: 365d — upstream says "the test order is undefined…"`. Pristine: `len(lines) < 3` false → `(True, 'ok')`; mutant `3 <= 3` true → `(False, 'no provenance trio')` | `FAIL T47HE_three_line_entry_ok want=(True, 'ok') got=(False, 'no provenance trio')` |
| `entry_ok:int:0` (`3`→`4`, same line) | `T47HE_three_line_entry_ok` | same 3-line entry. Pristine `3 < 3` false → `(True, 'ok')`; mutant `3 < 4` true → `(False, 'no provenance trio')` | `FAIL T47HE_three_line_entry_ok want=(True, 'ok') got=(False, 'no provenance trio')` |
| `entry_ok:int:3` (`6`→`7`, window floor) | `T47HE_six_token_quote_ok` | entry (4 lines) whose only quote is exactly 6 tokens (`t1 t2 t3 t4 t5 t6`), located in the snapshot `Upstream note: "t1 … t6" ends here.`. Pristine `6 <= 6` → `(True, 'ok')`; mutant `7 <= 6` false → `(False, 'no located quote')` | `FAIL T47HE_six_token_quote_ok want=(True, 'ok') got=(False, 'no located quote')` |
| `entry_ok:int:4` (`25`→`26`, window ceiling) | `T47HE_twenty_six_token_quote_refused` | entry (4 lines) whose only quote is exactly 26 tokens (`u1 … u26`), located in the snapshot. Pristine `26 > 25` → `(False, 'no located quote')`; mutant `26 <= 26` → `(True, 'ok')` | `FAIL T47HE_twenty_six_token_quote_refused want=(False, 'no located quote') got=(True, 'ok')` |
| `entry_ok:int:7` (`q.group(2)`→`q.group(3)`, fallback arm) | `T47HE_curly_quote_fallback_ok` | entry (4 lines) whose quote is the **curly** form `“the test order is undefined…”`, so `q.group(1)` is `None` and the fallback arm is evaluated. Pristine → `(True, 'ok')`; mutant evaluates `q.group(3)` → `IndexError: no such group` (caught and reported as a named failure) | `FAIL T47HE_curly_quote_fallback_ok want=(True, 'ok') raised IndexError` |

Each killed mutant produces **exactly one** named `FAIL ` line: every non-minimum case carries a
4th blank provenance line, so only `T47HE_three_line_entry_ok` sits on the `len(lines)` boundary.
No case fails for any neutral mutant, and no case fails for every mutant (no source/AST/length pin;
the assertion is the value `entry_ok` returns for a concrete input).

## The three remaining ids are structural non-kills (`crashed`, baseline `crashed`)

`entry_ok:bool:3` (`or`→`and`, line 109), `entry_ok:int:2` (`m.group(1)`→`m.group(2)`, line 101) and
`entry_ok:int:6` (`q.group(1)`→`q.group(2)`, line 109) make `entry_ok` **raise for any ordinary
entry** (`AttributeError: 'NoneType' object has no attribute 'replace'` / `IndexError: no such
group`). The raise happens inside the round-46 `selftest()`'s own case loop, before any `extra_*()`
is invoked, so no addition can print a name for them:

* round-46 `selftest()` line 174 `line = build(reg, ents, readme)`; nested `build()` line 163
  `return out.stdout.strip().splitlines()[-1]` → the **inner** counter subprocess crashed in
  `entry_ok` for case `T1_two_entries_pass`, printed nothing on stdout, and `[-1]` on an empty list
  raises `IndexError` in the **outer** process. The outer process aborts with a bare traceback: it
  prints no `PASS`/`FAIL` line at all, so the pool classes it `crashed`, not `killed`.
* the assembler appends the `extra_*()` calls **after** that case loop (immediately before the
  tally print), so `extra_T47HardCoverEntry()` is dead code under these three mutants — including
  its `try/except Exception` wrapper, which never runs.
* they are *not* behaviourally equivalent: the same fixtures my cases use do separate them
  (`E1`..`E4` raise `AttributeError` under `bool:3`/`int:6`, `IndexError` under `int:2` when called
  directly on the mutated module). Evidence: the direct-call probe below prints
  `RAISED AttributeError` / `RAISED IndexError` for every one of the four fixtures; the pool still
  reports `crashed`.

Measured sweep on the assembled counter (scratch, `/tmp/tameshi-r47-T47HardCoverEntry/h.py`,
each of the three mutants): `rc=1`, `stdout_lines=0`, `named_FAIL=0`,
stderr tail `IndexError: list index out of range` at `return out.stdout.strip().splitlines()[-1]`.

### Remedy (demonstrated in scratch, **not applied** — outside seat bounds)

The round-46 file and its `selftest()` are not a seat's to edit (`pool` excludes `selftest` from
mutation, and the assembler leaves it untouched), so this is a recommendation for the L1. In
`.ufo/evidence/round-46/hardening/coverage-counter.py`, nested `build()` of `selftest()`:

```python
            out = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm'],
                                 capture_output=True, text=True)
            _lines = out.stdout.strip().splitlines()
            return _lines[-1] if _lines else ''
```

Verified on a scratch copy (`/tmp/tameshi-r47-T47HardCoverEntry/h_patched.py`): `PRISTINE pass`, and
the three mutants become named kills — `rc=1`, 18 / 18 / 17 `FAIL ` lines, first line
`FAIL T1_two_entries_pass want='C2_R45_PASS=true' got=`. The case loop then runs to completion
and the tally prints, i.e. the counter becomes *operable* under those mutants instead of aborting
(this is what C2 is meant to buy). It moves no pool address: `selftest` is excluded, and no rule
function changes.

## Verification (commands, exit codes)

All from `/home/vgpnk/Projects/shokunin/tameshi-shokunin` unless noted.

| # | command | exit | result |
|---|---|---|---|
| 1 | `mkdir -p /tmp/tameshi-r47-T47HardCoverEntry` | 0 | scratch root |
| 2 | inline probe: `pool.run_selftest(coverage-counter.py)` + `pool.judge` for the 8 ids | 0 | `PRISTINE pass`; 5 `survived`, 3 `crashed` (crash tail = `build()` `IndexError`) — matches `.ufo/evidence/round-47/before/base-coverage.txt` lines 37/45/52/53/54/55/58/59 |
| 3 | inline probe: `entry_ok` against pristine + all 8 mutants on the 4 fixtures | 0 | pristine `(True,'ok') (True,'ok') (False,'no located quote') (True,'ok')`; separations as in the table; the trio raises |
| 4 | `python3 .ufo/evidence/round-47/hardening/assemble.py --group coverage --add …/T47HardCoverEntry.addition.py --out /tmp/tameshi-r47-T47HardCoverEntry/h.py` | 0 | `wrote … (1 additions)` |
| 5 | `python3 /tmp/tameshi-r47-T47HardCoverEntry/h.py --selftest` | 0 | 20 round-46/46b cases + my 4 all `PASS`; `C2_R45_SELFTEST: cases=24 failed=0`; `VERDICT: PASS` |
| 6 | `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardCoverEntry/h.py --group coverage --ids entry_ok:cmp:0,entry_ok:int:0,entry_ok:bool:3,entry_ok:int:2,entry_ok:int:3,entry_ok:int:4,entry_ok:int:6,entry_ok:int:7` | 0 | `PRISTINE pass`; `killed` cmp:0, int:0, int:3, int:4, int:7; `crashed` bool:3, int:2, int:6 |
| 7 | `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardCoverEntry/h.py --group coverage` (whole group, 86) | 0 | 4 `NEUTRAL … survived` (`Tree.ls:commute:0`, `Tree.read:commute:0`, `measure:commute:0`, `measure:commute:1`); MUT: 69 `killed`, 8 `crashed`, 5 `survived` |
| 8 | baseline diff (`before/base-coverage.txt` vs run 7) | 0 | base `{killed: 64, survived: 14, crashed: 8}` → new `{killed: 69, survived: 9, crashed: 8}`; **regressions: none**; new kills exactly my five ids; new crashes not in base: none |
| 9 | per-mutant `FAIL ` capture (5 mutants, `--selftest` on each mutated copy) | 0 | one named line each, quoted in the table above |
| 10 | scratch remedy check on `h_patched.py` (pristine + trio) | 0 | `PRISTINE pass`; trio 18/18/17 named FAILs, `rc=1` |

No network, no git/jj command in the lane, no package writes, no tool installs (nothing needed), and
no reads of credential/OAuth material.

## Risks / notes for the L1

* **Attribution** is 1 case ↔ 1 mutant for the four window/fallback ids; `cmp:0` and `int:0` share
  the 3-line case because both mutations sit on the same `len(lines) < 3` expression and only an
  exactly-3-line entry can separate either.
* **The trio is the coverage group's structural debt**, not a seat gap: coverage's C2 ceiling with
  additions alone is 69/82 non-neutral (base 64). The two-line `build()` change above would take it
  to 72/82 and is the only route I found that does not fake a kill (I explicitly rejected an
  import-time probe printed before the crash: it would leave the counter crashing, i.e. not
  operable, and would fire outside `selftest()`).
* Name isolation: case names start `T47HE_`, helpers `_xT47HardCoverEntry_` (both outside the pool's
  `^(selftest|main|extra_\w+|_x\w+)$` mutation set), function `extra_T47HardCoverEntry` — no
  collision with other seats' additions; the assembler accepts the file together with the others.
* The cases use only `fold()`/`entry_ok()` globals and their own fixtures; they add no files, no
  git, no subprocess, and they run in well under a second.
