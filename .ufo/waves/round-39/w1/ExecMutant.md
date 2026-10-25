# ExecMutant — round-39 w1 (mutant kill: census FLAG_GATE)

Scoped to the assigned mutant. No lane file edited; scratch only.

## Finding

Removing the FLAG_GATE early return in `tools/write-path-census.py` so the no-flag path
writes makes `--selftest` **exit 1** (killed), on the exact committed bytes.

- Gate under test: `tools/write-path-census.py:79-80`
  ```
      if not update:
          return False  # FLAG_GATE
  ```
- Detector that fires: `tools/write-path-census.py:100-101`
  `if wrote or not unchanged: failed.append('no-flag path wrote or changed the expected file')`
- Fixture root: `tools/write-path-census.py:93` `tempfile.TemporaryDirectory(prefix='write-path-census-')`

## Commands and retained output

Setup (byte-identical copy; sha256 == contract pin `bc8c660c…7edc62`):

```
mkdir -p /tmp/tameshi-r39-ExecMutant
cp tools/write-path-census.py /tmp/tameshi-r39-ExecMutant/pristine.py
cp tools/write-path-census.py /tmp/tameshi-r39-ExecMutant/mutant_del.py
```

M1 — early return deleted (lines 79-80 replaced by a comment):

```
$ diff -u pristine.py mutant_del.py
@@ -76,8 +76,7 @@
 def update_expected(path, value, update):
     """Write an expected-value file only when update is true."""
-    if not update:
-        return False  # FLAG_GATE
+    # FLAG_GATE early return removed: no-flag path falls through to the write
     with open(path, 'w', encoding='utf-8') as fh:
         fh.write(value)
     return True

$ python3 mutant_del.py --selftest
WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=0 noflag_unchanged=0
FAIL no-flag path wrote or changed the expected file
mutant_del_rc=1
```

M2 — the measure-style substitution (`return False  # FLAG_GATE` → `update = True  # FLAG_GATE`,
i.e. `census/measure.py`'s own mutation), independent reproduction:

```
$ python3 mutant_measure.py --selftest
WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=0 noflag_unchanged=0
FAIL no-flag path wrote or changed the expected file
mutant_measure_rc=1
```

Controls (same scratch dir):

```
$ python3 pristine.py --selftest
WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1
pristine_rc=0
```
Second run of both M1 and pristine reproduced rc=1 / rc=0 (`mutant_del_rc_2=1`, `pristine_rc_2=0`).

Do-nothing control (base rev, unmodified measurement):

```
$ python3 .ufo/evidence/round-39/census/measure.py --lane . --rev 50aadd1bbd94e43cd3fcfb81459414394db2dc35
C2_R39: tool_absent=1 gates=0/21 planted_unflagged=0 planted_flagged=0 planted_scratch=0 fixture_wrote=0 mutant_killed=0 rev=50aadd1… C2_R39_PASS=false
base_measure_rc=1
```

Observed context only (parent judges; not a decision here): at HEAD `233077f` the same counter prints
`tool_absent=0 tool_sha_ok=1 gates=21/21 live_write_sites=99 live_unflagged=0 planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 mutant_killed=1 C2_R39_PASS=true`, rc=0.

## Extra sensitivity probes (depth)

M3 — polarity inverted (`if not update:` → `if update:`, so the no-flag path writes and the flagged
path does not): rc=1, **both** fixture arms fire:

```
WRITE_CENSUS_SELFTEST: ... fixture_wrote=0 noflag_unchanged=0
FAIL no-flag path wrote or changed the expected file
FAIL update flag did not write the expected file
m3_rc=1
```

M4 — M1 plus `if wrote or not unchanged:` → `if False:`: **survives**, rc=0
(`WRITE_CENSUS_SELFTEST: ... fixture_wrote=1 noflag_unchanged=1`, `m4_rc=0`).
Two measured facts follow, stated as risk, not as a predicate edit:

1. The kill rests on a single assertion (`write-path-census.py:100-101`). A mutant that both drops
   the gate and neutralises that arm passes `--selftest` with rc=0.
2. `fixture_wrote` (`write-path-census.py:107`) is derived from the failure strings, not from an
   independent observation of the file, so it reports `1` in M4 while the fixture is broken. In M1
   it flips to `0` only because the same failure text is present.

Write surface check: no-flag write targets `<TemporaryDirectory>/case.expected` only.
`TMPDIR=/tmp/tameshi-r39-ExecMutant/tmpwatch python3 mutant_del.py --selftest` → rc=1 and
`find tmpwatch -mindepth 1` is empty (fixture cleaned up, nothing written outside scratch).
The mutant is killed on behaviour, not on a crash (it prints the fixture line and the FAIL line).

## Files changed

- `/tmp/tameshi-r39-ExecMutant/{pristine,mutant_del,mutant_measure,m3_flip,m4_blind}.py` (scratch).
- `.ufo/waves/round-39/w1/ExecMutant.md` (this report).
- Lane tree otherwise untouched: `git status --porcelain` shows only the pre-existing
  `M corpus/QUALITY.md` and round-39 dispatch/`w1/` entries. No pacman/tool installs. LSP not
  exercised (no symbol work was needed for this assignment).

## Risks / blockers

- Residual mutant survival described in M4 above; the selftest is not mutant-equivalent to
  "the no-flag path never writes" — it is sensitive to exactly one arm.
- No blocker: `--selftest` returns 1 on the assigned mutant.
