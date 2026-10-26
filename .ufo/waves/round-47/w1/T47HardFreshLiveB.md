# T47HardFreshLiveB — freshness selftest addition (round 47, wave 1)

Seat: `T47HardFreshLiveB` · group `freshness` · judged axis: operability (C2)
Deliverable: `.ufo/waves/round-47/w1/T47HardFreshLiveB.addition.py` (the only file I wrote in the lane)
Scratch: `/tmp/tameshi-r47-T47HardFreshLiveB/` · Counter hardened: `.ufo/evidence/round-46/hardening/freshness-counter.py` (read-only, unmodified)

## What the addition does

`extra_T47HardFreshLiveB()` adds six cases that drive `live()` — the only rule function the
round-46 selftest never calls. Every case reuses one scratch git lane built with the round-46
helpers (`_xHardMeasure_git`), and one stub `curl` placed first on `PATH`; no case touches the
network and no case reads the counter's own bytes (no hash/AST/length pin).

Fixture lane (`git init -q -b m`, toplevel asserted `== realpath(scratch)`, one commit with
`-c user.name=t -c user.email=t@t`, `GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`), 11-cell registry rows:

| entry | verdict | in population | stub `curl` | page vs quote |
|---|---|---|---|---|
| S001 | holds | yes (mined) | exit 0, writes page | quote PRESENT |
| S002 | holds | yes (mined) | exit 0, writes page | quote ABSENT |
| S003 | holds | no (row is `queued`) | exit 0, writes page | quote present |
| S004 | drifted | yes (mined) | exit 0, writes page | quote present |
| S005 | holds | yes (mined) | exit 1, writes page | quote present |

Stub behaviour is selected by URL suffix (`/present`, `/absent`, `/error`); env `T47FSLB_MODE=nofile`
makes every call exit 0 while writing no target (the unreadable-download input). The stub always
writes `CURL_STUB_STDOUT_MARKER` to its stdout, so a non-capturing call is observable.

Pristine `live()` output for the fixture (`--selftest`, all six PASS):

```
LIVE S001 present
LIVE S002 absent
LIVE S005 absent
C1_R45_LIVE: present=1 absent=2 rev=m
```

## Per mutant: case, separating input, helper output

`python3 pool.py --try h.py --group freshness --ids ...` → `PRISTINE pass`, each id `killed`.
`FAIL` line below is the first named case the pool records (full `FAIL` sets from `fails.py`).

### live:cmp:1 — `verdict != 'holds'` → `==` (line 307)
Case `T47FSLB01_live_holds_verdict_gate`, assertion `lines == ['LIVE S001 present','LIVE S002 absent','LIVE S005 absent']`.
Input that separates: S004 is `drifted` and in the population. Original skips it; the mutant inverts
the gate, skips the three `holds` rows and measures the drifted one.
```
FAIL T47FSLB01_live_holds_verdict_gate ['LIVE S004 present'] {'present': '1', 'absent': '0', 'rev': 'm'}
```
(co-failing cases: 02, 03, 04, 06 — the mutant prints no line for any `holds` row)

### live:cmp:2 — `id not in pop` → `in` (line 307)
Case `T47FSLB02_live_population_gate`, assertion `lines == want and 'LIVE S003' not in out`.
Input that separates: S003 carries `holds` but its registry row is `queued`, so it is not in
`population()`. Original skips it; the mutant measures exactly that row and skips every registered one.
```
FAIL T47FSLB02_live_population_gate ['LIVE S003 present'] {'present': '1', 'absent': '0', 'rev': 'm'}
```
(first recorded FAIL is 01 with the same detail; 02..04, 06 co-fail)

### live:int:2 — `res.returncode == 0` → `== 1` (line 313)
Case `T47FSLB03_live_returncode_gate`, assertion `'LIVE S001 present'` and `'LIVE S005 absent'` plus
summary `present=1 absent=2`.
Input that separates: S001's curl exits 0 with the page on disk → original reads it (`present`);
S005's curl writes the same page but exits 1 → original refuses to read the target (`absent`). The
mutant swaps both: S001 is never read and S005's on-disk page is read.
```
FAIL T47FSLB03_live_returncode_gate ['LIVE S001 absent', 'LIVE S002 absent', 'LIVE S005 present'] {'present': '1', 'absent': '2', 'rev': 'm'}
```
Note the mutant keeps `present=1 absent=2`, so only the per-id lines separate it — the case asserts them.

### live:const:1 — `capture_output=True` → `False` (line 311)
Case `T47FSLB05_live_captures_child_stdout`. Input that separates: the stub's own stdout. The case
runs `live()` from a child interpreter (`spec_from_file_location` on the counter under test, same
fixture, same stub PATH) and captures that child's stdout: with `capture_output=True` curl's marker
stays in the PIPE the call created; with `False` the child inherits stdout and the marker escapes.
```
FAIL T47FSLB05_live_captures_child_stdout rc=0 marker=True live=True
```
Isolation: this is the only case that fails for this mutant, and it fails for no other mutant.

### live:cmp:3 — `fold(quote) in extract(...)` → `not in` (line 315)
Case `T47FSLB04_live_quote_presence`, assertion `lines == want`.
Input that separates: S001's page contains the quote (original: present) and S002's page does not
(original: absent); the mutant flips both.
```
FAIL T47FSLB04_live_quote_presence ['LIVE S001 absent', 'LIVE S002 present', 'LIVE S005 absent'] {'present': '1', 'absent': '2', 'rev': 'm'}
```
Again `present=1 absent=2` is unchanged by the mutant, so the per-id lines carry the separation.

### live:const:2 — except-branch `present = False` → `True` (line 317)
Case `T47FSLB06_live_unreadable_is_absent`, `T47FSLB_MODE=nofile`: every curl exits 0 but writes no
target, so `open(target,'rb')` raises inside the `try`. Input that separates: that unreadable
download. Original reports `absent` for all three rows; the mutant reports `present` for all three.
```
FAIL T47FSLB06_live_unreadable_is_absent ['LIVE S001 present', 'LIVE S002 present', 'LIVE S005 present'] {'present': '3', 'absent': '0', 'rev': 'm'}
```
Isolation: this is the only case that fails for this mutant, and it fails for no other of the six.

## Group sweep (whole `freshness` group, no `--ids`)

`.ufo/evidence/round-47/hardening/pool.json` group `freshness`: 111 mutants (101 real + 10 neutral).
Baseline `.ufo/evidence/round-47/before/base-freshness.txt` read directly: 58 killed, 39 real
survived, 4 crashed, 10 neutral survived.

With this addition (`sweep2.txt`): `PRISTINE pass`; 70 killed; 27 real survived; 4 crashed
(`parse_rows:int:1`, `parse_rows:int:8`, `review_sets:bool:1`, `review_sets:not:2` — the same four as
the baseline, unchanged); 10/10 neutral `survived`; every baseline `killed` mutant still killed
(empty set difference). Verdict changes vs baseline, exactly 12:

```
live:bool:0 killed    live:bool:1 killed    live:cmp:0 killed    live:cmp:1 killed
live:cmp:2 killed     live:cmp:3 killed     live:const:0 killed  live:const:1 killed
live:const:2 killed   live:int:0 killed     live:int:2 killed    live:not:0 killed
```

Six are my assignment. The other six (`live:bool:0/1`, `live:cmp:0`, `live:const:0`, `live:int:0`,
`live:not:0`) are the live() sibling seat's mutants that the same fixture also separates — reported
here rather than suppressed; no conflict, the pool counts the assembled counter. `live:int:1`
(`return 0` → `1`) remains `survived`: `live()`'s return value is not part of any printed line, so no
behavioural input in this fixture separates it (that mutant is the sibling's, and this file does not
claim it).

## Commands run (all absolute-path, lane left read-only)

| # | command | exit |
|---|---|---|
| 1 | `mkdir -p /tmp/tameshi-r47-T47HardFreshLiveB` | 0 |
| 2 | `python3 .ufo/evidence/round-47/hardening/pool.py --enumerate .ufo/evidence/round-46/hardening/freshness-counter.py` | 0 |
| 3 | `python3 .ufo/evidence/round-47/hardening/assemble.py --group freshness --add .ufo/waves/round-47/w1/T47HardFreshLiveB.addition.py --out /tmp/tameshi-r47-T47HardFreshLiveB/h.py` | 0 |
| 4 | `python3 -m py_compile /tmp/tameshi-r47-T47HardFreshLiveB/h.py` (pre-edit build) | 0 |
| 5 | `python3 /tmp/tameshi-r47-T47HardFreshLiveB/h.py --selftest` (final build) | 0 — `C1_R45_SELFTEST: cases=40 failed=0`, `VERDICT: PASS` |
| 6 | `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/.../h.py --group freshness --ids live:cmp:1,live:cmp:2,live:int:2,live:const:1,live:cmp:3,live:const:2` | 0 — `PRISTINE pass` + 6× `killed` |
| 7 | `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/.../h.py --group freshness` | 0 — sweep above (131 s) |
| 8 | `python3 /tmp/.../failine.py /tmp/.../h.py <ids>` (first FAIL line per mutant) | 0 |
| 9 | `python3 /tmp/.../fails.py /tmp/.../h.py <ids>` (all FAIL lines per mutant) | 0 |

Post-edit re-verification after loosening the `T47FSLB05` sanity conjunct from
`'LIVE S001 present' in child_out` to `'LIVE ' in child_out` (so the case isolates `live:const:1`
instead of also failing on the four gate mutants): commands 3, 5, 6, 7, 8, 9 were all re-run; same
six kills, same sweep totals.

## Bounds / hygiene

- Wrote only the deliverable addition file and this report in the lane; no git/jj command in the
  lane, no `add/commit/stash/checkout/push`, no mutation of the frozen counter, pool, contract or
  evidence directories.
- All scratch under `/tmp/tameshi-r47-T47HardFreshLiveB/`; fixture lanes and stub bin dirs live under
  `tempfile.mkdtemp()` and are removed in the case's `finally`. `PYTHONDONTWRITEBYTECODE=1` is set
  while the fixture is live, so no `__pycache__` is produced for the counter under test.
- `live()` is called in-process (with `sys.stdout` parked in a `StringIO`) except for the
  `live:const:1` probe, which needs a fresh stdout fd and therefore runs in a child interpreter.
  The environment is snapshotted before the first case and restored in `finally`
  (`GIT_*` stripped, `GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`, stub dir prepended to `PATH`).
- Tooling: nothing installed or upgraded (host pacman transactions are paused; no `uv`/`npx` need),
  nothing to record.
- Risk: the fixture depends on `git` ≥ 2.28 (`init -b`) and on `sys.executable` being usable as a
  script interpreter for the stub and the child probe — both are already assumed by the round-46
  additions (`_xHardMeasure_build`, `_xHardMeasure_run`).
