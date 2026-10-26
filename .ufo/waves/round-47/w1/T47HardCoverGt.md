# T47HardCoverGt — coverage group selftest addition (round 47, C2 operability)

Seat: `T47HardCoverGt` · group `coverage` · deliverable
`.ufo/waves/round-47/w1/T47HardCoverGt.addition.py` (one `extra_T47HardCoverGt()` + `_xT47HardCoverGt_*`
helpers) · counter hardened: `.ufo/evidence/round-46/hardening/coverage-counter.py` · pool
`.ufo/evidence/round-47/hardening/pool.json` · scratch `/tmp/tameshi-r47-T47HardCoverGt/`.

**Result: all 4 assigned mutants killed.** Full `coverage` group sweep with my addition alone:
**74 killed / 8 survived / 0 crashed of 82 real mutants, 4/4 neutral `survived`; baseline was
64 killed / 10 survived / 8 crashed.** No mutant that was killed at the baseline lost its kill.

## Why a crash guard is part of this deliverable (measured, not assumed)

All four assigned mutants make a counter run die inside `gt_rows`. The round-46 suite reaches that
path only through its inline case `T1_two_entries_pass`, which parses the child's stdout as
`out.stdout.strip().splitlines()[-1]` (coverage-counter.py:163). When the child dies the parent
raises and the process exits on a bare traceback, so the pool scores `crashed`, never `killed`
(reproduced before writing anything, on the assembled file with no additions):

```
=== Tree.read:const:0  rc 1  STDOUT: ''
STDERR: ... File "c.py", line 174, in selftest
           line = build(reg, ents, readme)
        File "c.py", line 163, in build
           return out.stdout.strip().splitlines()[-1]
        IndexError: list index out of range
```
(same traceback for `gt_rows:int:3`, `gt_rows:const:0`, `gt_rows:int:6`)

Extras are inserted after the inline case loop, so no `extra_*` can run unless that exception is
held. The addition therefore replaces the module-level `selftest` name with a thin wrapper
(`_xT47HardCoverGt_frozen_selftest` keeps the original) that catches the exception, runs the probes,
and returns 1. It prints **no** FAIL line itself: if the probes pass, nothing is printed and the run
stays an unlabelled crash, exactly as without the addition (no blanket `crash -> kill`
conversion). Rule code, pool addresses and `main()` are untouched; `measure()` mode is untouched.

## The cases and the input that separates each mutant

Probes build a committed scratch lane (`tempfile`, `git -C d`, toplevel assertion, identity only via
`-c user.name=t -c user.email=t@t`) holding two snapshot files, `corpus/SOURCES.md`,
`corpus/knowledge/{a,b}.md`, `corpus/README.md` and the running counter's own bytes at `SELF_PATH`.
`Tree(d, 'm')` + `gt_rows(...)` are called in process; the full-counter case runs the file as
`--lane d --rev m`. Every probe call is inside `try/except Exception` -> `FAIL <case> raised
<ExcName>`.

| pool id | site in the round-46 counter | case(s) that name it | separating input | helper output line |
|---|---|---|---|---|
| `Tree.read:const:0` | `def read(self, path, binary=False)` (default flipped to `True`) | `G01`, `G02`, `G03` (primary), `G04`, `G05` | two mined googletest rows whose anchors name existing snapshots: the registry must arrive as text, so `ROW_RE.match` gets `str` | `FAIL G01_gt_rows_reads_two_rows raised TypeError: cannot use a string pattern on a bytes-like object` |
| `gt_rows:int:3` | `data = tree.read(snap.group(0), binary=True)` (`group(0)` -> `group(1)`) | `G01`, `G02`, `G03` (primary), `G04`, `G05` | same lane; `SNAP_RE` has no capture group, so group 1 has no value | `FAIL G02_gt_rows_snapshot_bytes_folded raised IndexError: no such group` |
| `gt_rows:const:0` | same line, `binary=True` -> `False` | `G01`, `G02`, `G03` (primary), `G04`, `G05` | same lane; the snapshot must be hashed as bytes (pristine: `rows['S256']['text'] == fold(snapshot)` and `used == {a.md, b.md}`) | `FAIL G02_gt_rows_snapshot_bytes_folded raised TypeError: Strings must be encoded before hashing` |
| `gt_rows:int:6` | `if not url or not GT_RE.match(url.group(0)):` (`group(0)` -> `group(1)`) | `G01`, `G02`, `G03` (primary), `G04`, `G05` | a row whose source cell carries an `https://…` URL (`URL_RE` has no capture group) | `FAIL G01_gt_rows_reads_two_rows raised IndexError: no such group` |

Both `group(0)` mutants raise the same `IndexError`; they are distinguished by site, not by message,
and each is separately killed because the mutation is applied one site at a time.

Pristine lines for the same cases (all in the assembled run):

```
PASS G01_gt_rows_reads_two_rows row_ids=S256,S257
PASS G02_gt_rows_snapshot_bytes_folded text='Remember that the test order is undefine' used=corpus/knowledge/a.md,corpus/knowledge/b.md
PASS G03_gt_rows_mismatched_digest_dropped row_ids=-
PASS G04_measure_valid_fixture_passes exit=0 C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
PASS G05_measure_single_row_completes exit=1 C2_R45: self_pin=1 rows=1 entries=2 indexed=2 row_ids=S256 rev=m C2_R45_PASS=false
```

Each mutated run prints **five** named FAIL lines (three in-process `raised …`, two end-to-end
`exit=1`), exit code 1. `G04`/`G05` assert the end-to-end verdict (`exit=0` + `rows=2` +
`C2_R45_PASS=true`; `exit=1` + `rows=1` + `C2_R45_PASS=false`), so a counter that dies or reports a
different verdict on the same lane is a named failure rather than a crash.

## Full-group sweep (my addition alone, no `--ids`)

`pool.py --try /tmp/tameshi-r47-T47HardCoverGt/h.py --group coverage` -> 86 MUT + 4 NEUTRAL lines:
**killed=74, MUT survived=8, crashed=0, timeout=0**; `NEUTRAL Tree.read:commute:0`,
`Tree.ls:commute:0`, `measure:commute:0`, `measure:commute:1` — all `survived`.

Baseline `.ufo/evidence/round-47/before/base-coverage.txt`: killed=64, survived=10 (MUT), crashed=8.
Transitions (all one-way, no kill regressed):

| mutant | baseline | with this addition | failing case |
|---|---|---|---|
| `Tree.read:const:0`, `gt_rows:int:3`, `gt_rows:const:0`, `gt_rows:int:6` | crashed | killed | `G01`/`G02`/`G03` (assigned) |
| `entry_ok:bool:3`, `entry_ok:int:2`, `entry_ok:int:6` | crashed | killed | `G04`, `G05` (`exit=1`, no verdict line) |
| `measure:const:0` | crashed | killed | `G04`, `G05` |
| `measure:int:0` (`return 0 if passed` -> `1`) | survived | killed | `G04` (`exit=1` on a fixture that must pass) |
| `measure:int:1` (`else 1` -> `else 2`) | survived | killed | `G05` (`exit=2` where 1 is the frozen failure code) |

The six unassigned kills are honest separations on my own fixtures (the counter returns a different
value or dies on the same input), but **they overlap `.ufo/waves/round-47/w1/T47HardCoverEntry.addition.py`
and `.ufo/waves/round-47/w1/T47HardCoverMeasure.addition.py`'s subject matter**; the L1 should score
those two seats on their own pages, not on this overlap.

## Commands run (all absolute paths, scratch only)

| command | exit |
|---|---|
| `python3 .ufo/evidence/round-47/hardening/pool.py --enumerate .ufo/evidence/round-46/hardening/coverage-counter.py` (site check) | 0 |
| `python3 .ufo/evidence/round-47/hardening/assemble.py --group coverage --add .ufo/waves/round-47/w1/T47HardCoverGt.addition.py --out /tmp/tameshi-r47-T47HardCoverGt/h.py` | 0 |
| `python3 /tmp/tameshi-r47-T47HardCoverGt/h.py --selftest` -> 25 cases, 0 failed, `VERDICT: PASS` | 0 |
| `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardCoverGt/h.py --group coverage --ids Tree.read:const:0,gt_rows:int:3,gt_rows:const:0,gt_rows:int:6` -> `PRISTINE pass` + 4x `killed` | 0 |
| `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardCoverGt/h.py --group coverage` (full sweep, output `/tmp/tameshi-r47-T47HardCoverGt/sweep.txt`) | 0 |
| `python3 .ufo/evidence/round-47/hardening/assemble.py --group coverage --add T47HardCoverEntry.addition.py --add T47HardCoverMeasure.addition.py --add T47HardCoverGt.addition.py --out /tmp/tameshi-r47-T47HardCoverGt/all.py` | 0 |
| `python3 /tmp/tameshi-r47-T47HardCoverGt/all.py --selftest` -> 35 cases, 0 failed, `VERDICT: PASS` | 0 |
| `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardCoverGt/all.py --group coverage --ids <the four ids>` -> `PRISTINE pass` + 4x `killed` | 0 |

Composition check: with the Entry and Measure seats' additions assembled together, the counter still
prints `VERDICT: PASS` (35 cases) and my four mutants stay killed; each seat's `extra_*` is called
once by the frozen tally (my cases are counted once: 25 cases alone, 35 with the two siblings).

## Risks / notes for the L1

1. The module-level `selftest` wrapper is the only mechanism that lets an addition report these
   mutants at all; it is silent unless one of my probes fails, so it does not by itself relabel
   unrelated crashes (verified: with the probes removed from consideration, `entry_ok:*` crashes are
   relabelled only because `G04`/`G05` genuinely observe the dead child). If the L1 prefers a
   counter-level fix (making the inline `build` total), the wrapper become redundant but the probes
   still kill the four assigned ids.
2. Wrapper chaining: if another addition also redefines `selftest`, the last block to execute captures
   the previous wrapper, so either order composes; my probes print nothing on success.
3. No edits outside the deliverable and this report; no git/jj writes in the lane; all scratch under
   `/tmp/tameshi-r47-T47HardCoverGt/`. No tool installs were needed (nothing added; pacman untouched).
