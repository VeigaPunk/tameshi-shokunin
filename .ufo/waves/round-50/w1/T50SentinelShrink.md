# T50SentinelShrink — C2 interface and counter, hostile-input review

Seat: `T50SentinelShrink` (sentinel, leaf). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at
`4afb060` (base `e3729de8`). Read-only on the lane; every probe ran in
`/fast/scratch/hyaku/tameshi-r50/T50SentinelShrink` against a `git clone --shared` fixture lane
(`tools/shrink-case.py` + F6 records added, toplevel asserted) and the frozen counter imported from a
scratch copy (`sha256 c3da7e59abf279db2ebf165d1a8d8298295ca234cd83b49027b9cb0b1823dfe3`, identical to
`.ufo/evidence/round-50/c2/measure.py`). Host Python 3.14.8. I never decided the claim; none of the
runs below is a verdict.

Every probe drives the **frozen** `measure()` from a scratch copy (`receipts/drive.py`) with a
two-mutant public panel (round-49 `M01`,`M02`, digest passed to `measure()`), an empty hidden panel, and
the frozen generator taken from the real lane (`gen_lane`) so the `gen_pin`/`guard_pin` terms are the
frozen ones. The `MUTANT …`/`C2_R50:` lines quoted below are the counter's own output.

| # | severity | surface |
|---|---|---|
| F1 | Critical | the shrinker can rewrite the counter's judge copies → `C2_R50_PASS=true` with no shrinking |
| F2 | High | the run log `.runs` is shrinker-writable and shrinker-avoidable → the cost term is self-consistency only |
| F3 | High | a FIFO `.runs` or `out.json`, or a symlinked `.runs`, blocks the counter forever (no read timeout; none in the deciding run) |
| F4 | High | a lone surrogate in `out.json` crashes the counter mid-run (uncaught `UnicodeEncodeError`) |
| F5 | Medium | a poisoned `work/frozen-pbt.py` is re-executed unverified; the `N-1` tolerance then hides it |
| F6 | Medium | cost-term type laxity: `runs: false` == `0`, `units_before: 8.0` accepted |
| F7 | Medium | shrinker is unsandboxed with full uid; the deciding run's "clean tree" requirement is a comment |
| F8 | Medium | unbounded `capture_output` and no aggregate time budget |
| F9 | Low | a JSON-array panel raises `AttributeError` instead of counting `panel_invalid` |
| F10 | Low | `instrument()` anchors on the first column-0 `import `; inside a docstring it is inert |
| F11 | Low | `is_subcase` compares content, `units`/`removals` compare terminators |
| F12 | Low | `reduced` is `ua <= ub`, so 19 of 20 mutants may be identity |

---

## F1 — Critical: the shrinker overwrites the counter's own judge, and the counter never re-reads it

`.ufo/evidence/round-50/c2/measure.py:254-258` writes the judge copies of the guards, and `:289`
builds the judge from those paths **after** the shrinker has exited:

```
254: vp, vm = os.path.join(ver, 'pristine.py'), os.path.join(ver, 'mutant.py')
255: with open(vp, 'w', encoding='utf-8') as fh:  fh.write(guard_src)
257: with open(vm, 'w', encoding='utf-8') as fh:  fh.write(msrc)
289: judge = Judge(gen, vp, vm, casedir)
```

The shrinker runs with `cwd=shr` (`measure.py:276-277`), and `ver/` is its sibling
(`ver, shr, casedir = d/ver, d/shr, d/case`, `measure.py:251`), so `../ver/mutant.py` is writable by
the process under test. `kills` and `minimal` are then decided on bytes the shrinker chose — the
two checks that decide whether a case is real — while the shrinker's own report is what the `cost` term tests.

Exploit path (proven): a shrinker that (a) copies the input case, (b) drops one line, (c) writes
`../ver/mutant.py` as a wrapper that emits a setup refusal **only when the three case files equal the
dropped case** and exec's the real pristine guard otherwise, (d) reports `runs: 0`, (e) never invokes a
guard. `kills` and `minimal` become tautologies on the counter's side.

Command (fixture lane rev `b1d71416`):

```
R50_MODE=forge python3 drive.py b1d7141619883f6203b6a9c6fa173730ec955006 forge w-forge
```

```
MUTANT M01 panel=public exit=0 units=8->7 runs=0 logged=0 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
MUTANT M02 panel=public exit=0 units=8->7 runs=0 logged=0 exit0=1 valid=1 subset=1 kills=1 minimal=1 cost=1 reduced=1 OK
C2_R50: … mutants=2 ok=2 units_before=16 units_after=14 … total=0 C2_R50_PASS=true
```

Paired control (identical shrinker, `forge()` call removed — mode `droponly`):

```
MUTANT M01 … kills=0 minimal=0 … FAIL
MUTANT M02 … kills=1 minimal=0 … FAIL
C2_R50: … total=2 C2_R50_PASS=false
```

So the single write to `../ver/mutant.py` is load-bearing: it flips `kills`/`minimal` from 0 to 1 and
the counter from `false` to `true`. Receipts: `receipts/receipt-forge.txt`,
`receipts/receipt-droponly.txt`, shrinker `receipts/shrink-case.py` (`forge()`).

Impact: the claim's `cannot_see` admits only "how the shrinker searches … beyond its logged cost"; it
does not admit "the shrinker rewrites the judge". A deciding run that prints `C2_R50_PASS=true` is
therefore not evidence that any case was shrunk.

Smallest remediation: judge from bytes the shrinker never saw. After `subprocess.run` returns, rewrite
`vp`/`vm` from the in-memory `guard_src`/`msrc` into a fresh directory (and `os.chmod` the parent 0555
while the shrinker runs), or keep a digest of `ver/` taken at write time and refuse on mismatch.

## F2 — High: `.runs` lives in the shrinker's cwd, so the "logged invocations" are not an observation

`measure.py:282-284` counts lines in `shr/.runs`; `sp`/`sm` (`measure.py:266-270`) place the
instrumented guards next to it, and `measure.py:276` hands the shrinker those paths. The three logger
lines (`measure.py:62-64` `INSTRUMENT`) are plain text in a file the shrinker can rewrite, so the
counter can neither force the log nor trust it.

Three variants, all accepted (`cost=1`):

1. **Avoided.** Shrinker strips the three `_r50_os`/`_r50_fh` lines from `--pristine`/`--mutant` and
   runs the de-instrumented copies. 15 real guard subprocesses per mutant, `.runs` absent, reported
   `runs: false`:

   ```
   MUTANT M01 panel=public exit=0 units=8->1 runs=False logged=0 … cost=1 reduced=1 OK
   C2_R50: … total=0 C2_R50_PASS=true
   actual guard subprocesses: 15 ; counter saw logged: ABSENT
   ```

2. **Fabricated.** Shrinker appends 5000 lines to `shr/.runs` and reports `runs: 5000`; the true count
   is 15: `MUTANT M01 … runs=5000 logged=5000 … cost=1 … OK`.

3. **Cooperative control.** Same shrinker using the instrumented copies: `runs=15 logged=15 … cost=1`.
   So on the intended path the accounting is exact and there is **no double count** (each `run_guard`
   is a fresh `sys.executable -I guard`, one import = one line, and `logged` is read at `:282` before
   the judge at `:289` touches the uninstrumented `ver/` copies). The defect is that the counter
   cannot distinguish 1–3.

Commands: `R50_MODE=greedy`, `R50_MODE=inflate`, `R50_MODE=honest` with `drive.py` (receipts
`receipt2-greedy.txt`, `receipt-inflate.txt`, `receipt2-honest.txt`).

Impact: `runs` equals the logged invocations only when the shrinker cooperates, so the claim's "stated
run count equal to the logged guard invocations" is unfalsifiable in both directions.

Smallest remediation: count invocations outside the shrinker's reach — pass an inherited pipe (fd 3)
or a log path in `work/` (not `shr/`) through the instrumented guard's environment, and read it after
the run; refuse if the log is a non-regular file or if `runs < 1`.

## F3 — High: a FIFO `.runs` (or `out.json`) blocks the counter forever

`measure.py:283` opens `shr/.runs` for reading with no `O_NONBLOCK`, no `stat`, no timeout; the whole
`measure()` call sits in `deciding-run.sh:46` with no `timeout` either. After the shrinker exits with
`out.json` written, the counter blocks inside `open()`.

Command (fixture lane rev `35b0bf1b`, mode `fifo`): the shrinker `os.mkfifo()`s `shr/.runs` and exits 0.

```
python3 harness/deadline.py 35b0bf1b600edfeff1a2d6b7af33dc1e24393f85 fifo w-fifo4 12
driver STILL RUNNING after 12s -> killed (counter has no read timeout)
--- receipt (w-fifo4.stdout):  SELFTEST exit=0 last=PROBE_SELFTEST ok
--- .runs: fifo 0 bytes      --- out.json present: yes
```

The same holds for the output file (the try/except at `:285-287` catches `OSError`, not a blocked
`open`); the shrinker exits 0 and leaves `out.json` as a FIFO, `.runs` absent:

```
python3 harness/deadline.py d676264f3bf6bfecc98a33514eb5ee584228eb3a fifoout w-fifoout 10
driver STILL RUNNING after 10s -> killed (counter has no read timeout)
--- receipt: SELFTEST exit=0 last=PROBE_SELFTEST ok   --- out.json: fifo   --- .runs exists: no
```

Related, same line: `.runs` → `/dev/zero` makes the count loop non-terminating
(`receipt-defs.txt`: `subprocess.TimeoutExpired … timed out after 5 seconds` for the exact
`sum(1 for _ in fh)` the counter runs). And because the guard opens `.runs` for append at import
(`measure.py:62-64`), a **symlink** there writes outside the work dir: `.runs` → a file in another repo
appended `p\n`, and `git -C victim status --porcelain` printed ` M notes.txt`
(`receipt-defs.txt`). A shrinker can therefore write into any tree, including the lane, through the
counter's own instrumentation.

Impact: the deciding run can hang before printing any `MUTANT` line; a killed run cannot be re-invoked
(`deciding-run.sh:29` refuses a second `c2.start`), so the kill rule turns a hang into a void round.

Smallest remediation: `st = os.lstat(p)`; require `stat.S_ISREG`; `os.open(p, O_RDONLY|O_NOFOLLOW)` with
a byte cap; wrap the read and both `subprocess.run` calls in a watchdog that kills the process group.

## F4 — High: a lone surrogate in `out.json` crashes the counter

`valid_case` (`measure.py:148-150`) only checks `isinstance(…, str)`. A string such as `"\ud800"`
(legal JSON, `json.load` yields a lone surrogate) reaches `judge.kills` at `measure.py:298`, which calls
`run_guard` → `write_text(..., encoding='utf-8')` in the frozen generator and raises.

```
python3 drive.py 13f42adc… surrogate w-surrogate      # out.json registry = case + "\ud800"
Traceback (most recent call last):
  File ".../measure.py", line 298, in measure
    flags['kills'] = judge.kills(s)
  File ".../measure.py", line 158, in kills
    if self.gen.check(case, self.gen.run_guard(self.mutant, self.casedir, case)) is None:
UnicodeEncodeError: 'utf-8' codec can't encode character '\ud800' in position 498: surrogates not allowed
```

Note `flags['subset']` is already 0 for that case — `kills` is evaluated unconditionally, so the crash
happens even for a case `is_subcase` has rejected. Exit 1, and no `C2_R50:` line is printed
(`receipts/receipt-surrogate.txt`).

Impact: one line of `out.json` voids the deciding run (kill rule: one invocation, no re-run) — and it
is not reported as a counter term, just as a traceback.

Smallest remediation: `case[field].encode('utf-8')` inside `valid_case`, and wrap
`judge.kills`/`removals` in `except (OSError, ValueError, UnicodeError)` → `valid = 0`.

## F5 — Medium: the frozen generator in the work dir is re-executed unverified, and `N-1` hides the damage

`measure.py:259` re-executes `work/frozen-pbt.py` for every mutant; the digest is checked once at
`:194-201` against `git show`. That file sits three levels above the shrinker's cwd, so the shrinker can
rewrite it after the first mutant. A shrinker that also does an honest greedy shrink for mutant 1 and
poisons the generator for mutant 2 gets:

```
MUTANT M01 panel=public … units=8->1 … OK
MUTANT M02 panel=public … units=1->1 … kills=0 minimal=0 … FAIL
C2_R50: … mutants=2 ok=1 … ok_short=0 no_reduction=0 … total=0 C2_R50_PASS=true
--- m01/shr/case.json: {"registry": "POISONED-CASE-BY-SHRINKER\n", "staged": "", "map": null}
```

(`receipts/receipt-poison.txt`, mode `poison`.) The counter prints `true` with the second mutant's
counterexample literally chosen by the shrinker, because `ok_short = max(0, (total-1) - ok)`
(`measure.py:313`) only requires `N-1`.

Impact: the `N-1` margin is pre-registered, so this is not a predicate violation by itself; the defect
is that the margin can be *spent at will* on the single hardest mutant, exactly where the hidden panel
is meant to bite, and the substitution is invisible in the receipt.

Smallest remediation: re-hash `frozen-pbt.py` immediately before each `find_case` (cheap, same
`sha()`), and require `unfound == 0` for every hidden mutant.

## F6 — Medium: cost-term type laxity

`measure.py:300-302`:

```
300: flags['cost'] = (out.get('runs') == logged and isinstance(out.get('runs'), int)
301:                  and out.get('units_before') == ub and out.get('units_after') == ua)
302: flags['reduced'] = ua <= ub
```

`isinstance(True, int)` is `True` and `True == 1`, `False == 0`; `units_before`/`units_after` have no
type test at all, and `8.0 == 8`. Proven in the accepted run of F2 variant 1:
`runs=False logged=0 … cost=1` with `out.json` carrying `False 8.0 1.0`
(`receipts/receipt2-greedy.txt`). `runs` is also never required to be `>= 1`, so "cost in guard runs"
can be 0.

Impact: `true`/`false`/floats satisfy a term whose name is "cost". Low exploit value on its own (the
shrink must still be real), but it is the term that certifies the *stated cost*, and it accepts values
that are not counts.

Smallest remediation: `type(x) is int and x >= 1` for `runs`, `type(x) is int` for the unit counts.

## F7 — Medium: the shrinker runs unsandboxed, and nothing witnesses the lane after it

`measure.py:276-277` gives the shrinker only `cwd` and `TMPDIR`; there is no chroot/seccomp/user
namespace, and no post-run check of the lane. `deciding-run.sh:9` *states* "the working tree must be
clean" but the script contains no `git status` anywhere (grep over the file finds the comment only),
and the monitors (`deciding-run.sh:38`) run **before** C2 (`:46`) and read committed bytes
(`git show`). So a shrinker write into the lane during C2 is invisible in every receipt of the run;
F3's symlink probe shows the write primitive (`git status` → ` M notes.txt`).

Impact: the decided tree can be modified during the deciding run with no witness; the next round's base
inherits it.

Smallest remediation: `[ -z "$(git -C "$LANE" status --porcelain)" ]` before and after the C2 block,
or run the shrinker under `bwrap --ro-bind / / --tmpfs …` (a peer seat is prototyping exactly that).

## F8 — Medium: unbounded capture and no aggregate budget

`measure.py:232` and `:276-277` use `capture_output=True` with no cap, and `:232-234` also decodes the
whole buffer for `[-1][:200]`. A child writing 300 MB raised the parent's `VmHWM` to 633980 kB
(`receipts/receipt-defs2.txt`). Per-mutant budget is `SHRINK_TIMEOUT = 900` (`:59`) and
`find_case` gets 3600 s (`:173`), so 20 mutants can spend ~25 h; nothing aggregates.

Impact: memory/CPU DoS on the deciding host from a shrinker or a `--selftest` run; the wall-clock bound
is 20× the intended one.

Smallest remediation: stream child output to a file under `work/` with a byte cap (or read at most N
bytes and kill), and set one deadline for the whole `measure()`.

## F9 — Low: a JSON-array panel raises `AttributeError`

`measure.py:215`: `if sha(raw) != pin or not isinstance(doc.get('mutants'), list)`. The digest is tested
first, so the crash is only reachable when the panel digest **matches** the pin (not the case at
freeze: `PUBLIC_SHA256`/`HIDDEN_SHA256` are objects). With a matching array panel:

```
RAISED AttributeError: 'list' object has no attribute 'get'      (receipts/receipt-defs2.txt)
```

Impact: a robustness gap, not an exploit; malformed input should be `panel_invalid`, not a traceback.

Smallest remediation: `if sha(raw) != pin or not isinstance(doc, dict) or not isinstance(doc.get('mutants'), list)`.

## F10 — Low: `instrument()` can put the logger inside a docstring

`measure.py:82-87` anchors on the first line *starting* with `import `/`from `:

```
86: if line.startswith('import ') or line.startswith('from '):
87:     return '\n'.join(lines[:i]) + '\n' + (INSTRUMENT % tag) + '\n'.join(lines[i:])
```

No `ast`, no awareness of string state. A guard whose docstring has a column-0 `import os` gets the
logger inserted as docstring text; the guard then runs normally and never creates `.runs`:

```
run rc: 0  stdout: b'body ran\n'   .runs exists: False      (receipts/receipt-defs2.txt)
```

The pinned guard is safe today (first column-0 import is `import argparse` at
`tools/staged-id-guard.py:57`), so this is not a current bypass through the guard; it is a textual
bypass the mechanism admits, and it also breaks on `from __future__ import …` (syntax error).

Smallest remediation: `ast.parse`, insert as the first statement after the module docstring, and assert
at instrument time that the first statement of the instrumented module is the logger.

## F11 — Low: `is_subcase` compares content, `units`/`removals` compare terminators

`measure.py:130-132` uses `s[field].splitlines()` (terminators dropped), `measure.py:105-108` and
`:111-123` use `splitlines(True)`. A case with every line end rewritten `\n` → `\r\n` is byte-unequal
yet accepted as a sub-case, with the same unit count:

```
byte-equal-line-ends: False   is_subcase(s,c): True   units c/s: 2 2      (receipts/receipt-defs.txt)
```

Impact: benign for the pinned guard — `parse_rows` and the oracle both use `text.splitlines()`, so a
`\r` cannot change the verdict; the test is a *content* sub-case, not the "lines kept" of the interface
text, and it is the one place where `splitlines`/`splitlines(True)` disagree.

Smallest remediation: compare `splitlines(True)` in `is_subcase` so the sub-case is terminator-exact.

## F12 — Low: `reduced` is non-strict

`measure.py:302` `flags['reduced'] = ua <= ub`; the only strict requirement is aggregate
(`measure.py:314` `after_sum < before_sum`). The contract's C2 predicate says "for at least 19 of 20
mutants **with a net reduction**". A mutant whose found counterexample is already 1-minimal passes
`valid/subset/kills/minimal/reduced` by identity; one honest shrink anywhere carries the sum.

Impact: a per-mutant requirement in the prose that the counter does not enforce; the observable effect
is confined to already-minimal cases (the generator's cases here are not minimal: 8 → 1 in the greedy
run).

Smallest remediation: `ua < ub`, or restate the aggregate in the contract.

---

## Probes that found no defect (recorded so they are not re-run as suspicions)

- **Run logger double-count**: none on the intended path. Each `run_guard` is a new
  `python3 -I guard`, so one import = one line; `logged` is read (`:282`) before the judge (`:289`)
  runs on the uninstrumented `ver/` copies. Measured 15 logged / 15 executed
  (`receipts/receipt2-honest.txt`). The failure mode is *under*-counting (F2), not double counting.
- **`subsequence()`** (`:125-127`) is correct, including duplicates and the empty case
  (`subsequence(['a','a'], ['a'])` → False, `subsequence([], x)` → True).
- **Non-string map keys**: unreachable across the JSON boundary (`json.loads` yields `str` keys;
  `json.dumps({1:2})` writes `"1"`), and `units`/`removals`/`is_subcase` are key-type agnostic anyway.
- **`out.json` with extra fields**: accepted by design; my probe's `"note": "probe"` was ignored and
  `total=0` (`receipts/receipt2-greedy.txt`). No field-set check, no impact observed.
- **Grandchild holding the captured pipe does not defeat `timeout=`** on CPython 3.14.8:
  `subprocess.run(..., timeout=2, capture_output=True)` returned `TimeoutExpired after 2.0s`
  (`receipts/hang.py`). The effective hang is F3's FIFO/.runs read, not the pipe.
- **Non-UTF-8 `out.json`**: caught as `ValueError` → `out = None` → `valid=0` (`:286-288`). Sound.
- **`--selftest` rc and `records()`**: no hostile input reaches them; the
  `records()` column offsets (`cells[7]`, `cells[8]`, `measure.py:337-338`) match the lane's
  `corpus/SOURCES.md` row shape.

## Evidence index

All under `.ufo/waves/round-50/w1/T50SentinelShrink.receipts/` (cited in this report as `receipts/<name>`): `drive.py` (harness that imports the
frozen counter from a scratch copy), `shrink-case.py` (the probe shrinker, modes
`greedy|honest|inflate|forge|droponly|fifo|fifoout|poison|surrogate`), `probe_defs.py`, `probe_defs2.py`,
`deadline.py`, `hang.py`, `panel.json`, `hidden.json`, and the raw `receipt-*.txt` / `receipt2-*.txt`
outputs quoted above. Scratch (`/fast/scratch/hyaku/tameshi-r50/T50SentinelShrink`) was the only
write target during probing and is deleted.

Tooling: nothing installed; `python3` 3.14.8 was already present, no pacman/uv/npx call was made.

## Summary

1. Critical: the shrinker can overwrite `../ver/mutant.py`, so `kills`/`minimal` become tautologies and `C2_R50_PASS=true` with zero shrinking (F1, paired control fails without the write).
2. High: `.runs` is in the shrinker's cwd — avoided (15 real runs, logged 0), fabricated (5000 fake lines accepted), exact only when the shrinker cooperates; no double count on the intended path (F2).
3. High: a FIFO `.runs`/`out.json` hangs `measure()` forever (no read timeout; `deciding-run.sh` has none either); a symlinked `.runs` writes into any tree; `/dev/zero` never ends (F3).
4. High: a lone surrogate in `out.json` crashes the counter at `judge.kills` before any `C2_R50` line (F4).
5. Medium: `work/frozen-pbt.py` is re-executed per mutant from a shrinker-writable path and the `N-1` margin hides the substituted case (F5); `runs: false`/`8.0` satisfy the cost term (F6); no sandbox and no clean-tree witness (F7); unbounded capture, no aggregate budget (F8).
6. Low: array panel → `AttributeError` (F9); text-anchored instrumentation can be inert (F10); content-vs-terminator sub-case test (F11); `reduced` is non-strict (F12).
7. Cheapest hardening: re-materialise `ver/` after the shrinker exits, move the run log out of its view (fd/pipe), require a regular non-symlink log, add a watchdog, reject non-UTF-8-encodable cases.
