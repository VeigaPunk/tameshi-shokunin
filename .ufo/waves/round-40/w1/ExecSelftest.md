# ExecSelftest — round 40 w1

Seat: leaf, re-run the v2 census selftest. Axis: depth.
Lane HEAD at measurement: `5641ed8` (= contract commit). No counter was run in default mode.
No lane file edited; scratch work in `/tmp/tameshi-r40-ExecSelftest/`.

## 1. Assigned run (exact command)

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v2.py --selftest --fixtures /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-40/census/fixtures.json
```

```
WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0
EXIT=0
```

Same line and EXIT=0 from lane cwd with relative paths, and from `--selftest` with no `--fixtures`
(default resolves to `<lane>/.ufo/evidence/round-40/census/fixtures.json`). No args → usage, `EXIT=2`.

## 2. Pin legs that this seat could check (all match)

```
sha256sum tools/write-path-census-v2.py tools/write-path-census.py .ufo/evidence/round-40/census/fixtures.json
4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b  tools/write-path-census-v2.py
bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62  tools/write-path-census.py
af237473b3966d8b37e24bc9272909178aac4f2d77252045a0e3f9a5b20efa5d  .ufo/evidence/round-40/census/fixtures.json
```

- v2 sha == contract `claims.C1.tool_sha256`; v1 sha == `v1_sha256`. `git diff --stat HEAD -- tools/write-path-census-v2.py tools/write-path-census.py .ufo/evidence/round-40/census/fixtures.json` is empty, so the worktree bytes the counter will `git show` at HEAD are the bytes measured here.
- Base absence (base C1 must stay false): `git cat-file -e 304e3355705640af2879c772fc9a5c2902c61763:tools/write-path-census-v2.py` → `fatal: path 'tools/write-path-census-v2.py' exists on disk, but not in '304e335...'`, exit 128. Tool absent at base.

## 3. Mutation clause of the predicate — confirmed on scratch copies

Copies of the shipped tool under `/tmp/tameshi-r40-ExecSelftest/`, run against the shipped fixtures:

| mutant | output | exit |
|---|---|---|
| `WRITE_RE` line `os\.replace\s*\(` deleted | `... replace_unflagged=0 ...` + `FAIL planted replace_unflagged: want unflagged=1 got 0` | 1 |
| `EXPECTED_RE` alternative `expected\.json` deleted | `... bytes_unflagged=0 ...` + `FAIL planted bytes_unflagged: want unflagged=1 got 0` | 1 |
| shipped tool, fixture `bytes_unflagged` replaced by `print('expected.json')` | `FAIL planted bytes_unflagged: want unflagged=1 got 0` | 1 |

So both deletion mutants are killed and the selftest is not a tautology against a corrupted fixture file.

## 4. Depth finding — the selftest does not bind the cited live `os.replace` shape

The planted case is `"replace_unflagged": "os.replace(tmp, 'case.expected')\n"`. Its `replace_unflagged=1`
is produced by **two** independent pattern classes: the `os\.replace` write form *and* the literal
`'case.expected'` matched by `EXPECTED_RE`. The live line the predicate cites for this leg is
`tools/bash-witness-study.py:778`:

```
778:    os.replace(tmp, path)
```

`path` is a `Path` parameter of `write_json` (line 776-778), no expected-like literal on the line.

Per-line classification, by importing the shipped modules read-only (no corpus totals, no counter):

```
registry-replay.py:123  v2= (1, 1)  v1= (1, 0)
bash-witness-study.py:778  v2= (1, 0)  v1= (0, 0)
```

Consequence, demonstrated: a strictly narrower variant
`r"""|os\.replace\s*\([^)]*expected"""` (`/tmp/tameshi-r40-ExecSelftest/mut_narrow_replace.py`)

```
WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0
EXIT=0
```

still passes the shipped selftest, and on the live line it yields

```
bash-witness-study.py:778 -> (0, 0)
```

That pattern would fail the predicate's corpus leg while the selftest stays green. The selftest therefore
pins the *deletion* of the `os\.replace` alternative, but not the shape that makes the live witness line
count. The predicate itself is **not** falsified: the shipped pattern does hit `:778` (write_sites 1 vs v1's 0),
which is all the leg asks. The caveat for the L1: `replace_unflagged=1` is not evidence that the live
`os.replace` line is counted as *unflagged* — on the live line v2 reports write_sites=1, unflagged=0. The
replace leg is a write-site leg only, so any depth narrative that reads the selftest number as unflagged
coverage of `bash-witness-study.py` overstates it.

## 5. Ancillary measured inconsistency (not a predicate leg)

```
cd <lane> && python3 .ufo/evidence/round-40/census/measure.py --lane . --control
C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0 v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false
EXIT=1
```

The numbers match the contract's v1 expectation (`bytes_unflagged=0`, `replace writes=0`) but the leg
prints PASS=false. In `measure.py` (`control()`):

```
meets = bytes_u == 1 and replace_w >= 1 and v1_classify(planted['replace_unflagged'])[1] == 1
```

i.e. the control passes only if v1 *reaches* the v2 target, while the comment two lines above says
`# The v2 target is both new classes at 1. v1 cannot reach it.` and the frozen predicate says v1 must
score 0/0. The control's pass criterion is inverted relative to its own comment and the contract. This is
not one of the five C1 predicate legs, but `--control` at HEAD can never pass, so the L1 must not read
`C1_R40_CONTROL_PASS=false` as a C1 failure. Harness defect, not a tool defect (the contract forbids me to
rewrite the predicate and I did not edit `measure.py`).

## Files changed

None in the lane. Scratch only: `/tmp/tameshi-r40-ExecSelftest/{mut_no_replace.py,mut_no_expected_json.py,mut_narrow_replace.py,fixtures_broken.json,mut_narrow_json.py}`.

## Risks / limits

- Measured at HEAD `5641ed8` only; base-rev counter behaviour not exercised (that is the L1's deciding run).
- No pacman / install transactions were needed or run.
- Whether the working-tree-vs-HEAD equality holds at the L1's chosen REV is a `git`-time question; at HEAD the check is clean.
