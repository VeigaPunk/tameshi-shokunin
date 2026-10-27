# T52W3ExecC1Probe — frozen C1 counter at CAND1 (probe, non-deciding)

Seat: executor, axis operability, milestone "C1 probe at CAND1". Nothing in this file decides C1;
the deciding run is the L1's single invocation of `.ufo/evidence/round-52/deciding-run.sh`. Lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`,
probed rev **CAND1 `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`** (lane HEAD at run time was its child
`f1a3246`, the wave-3 spec commit; the probe read CAND1 bytes through `git show`, never the worktree).

## 1. Command, provenance, exit

```
S=/fast/scratch/hyaku/tameshi-r52/T52W3ExecC1Probe; mkdir -p "$S/w"
HYAKU_SCRATCH="$S" TMPDIR="$S" python3 \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-52/c1/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135 --work "$S/w" --explain
```

- exit **0**, wall **636.49 s**, work dir empty on entry (the counter refuses a non-empty one).
- Counter bytes executed: `.ufo/evidence/round-52/c1/measure.py` sha256
  `3edfdb8737c667430f5555076899851ecaa25e4b2e5ccfe4c0603ae3e0bb3ec6` (frozen round-52 C1 counter).
  Same bytes `--selftest` → `C1_SELFTEST: cases=9 failed=0`, exit 0
  (`w3/T52W3ExecC1Probe/selftest.stdout`).
- Registry grader: the counter copies **BASE** `tools/registry-check.py`
  (`.ufo/evidence/round-52/c1/measure.py:103-107`) and runs it `-I` against `--rev CAND1`; the copy
  in the work dir sha256 `cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad`, equal to
  `git -C LANE show ef19d8e1:tools/registry-check.py | sha256sum` **and** to
  `git -C LANE show 7ff81a5b:tools/registry-check.py | sha256sum` — the file is unchanged between base
  and CAND1 (`git diff --stat ef19d8e1 7ff81a5b -- tools/` lists only `tools/registry.json` 4 lines
  and `tools/round21-measure.py` 11 lines).
- C3 counter: digest gate at `measure.py:123` passed — the copy sha256
  `a3abbd3b7888432919a999b1de357d4b71fa7262d55ae2f5ff97be4dddb3fd3a` equals `C3_SHA`
  (`measure.py:27`) and equals
  `git -C LANE show 7ff81a5b:.ufo/evidence/round-51/c3/measure.py | sha256sum`.

## 2. Result (verbatim, last line of `w3/T52W3ExecC1Probe.stdout`)

```
C1_R52: rev=7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135 held=49/49 not_held=0 dropped=0 mte_row=0 c3_covered=30 c3_total=0 r21_cases_missing=0 total=0 C1_R52_PASS=true
```

All five other explain lines, verbatim (`w3/T52W3ExecC1Probe.stdout:1-4`):

```
C1_REGISTRY_CHECK exit=0 summary=49/49 not_held=[]
C1_DROPPED none
C1_MTE_ROW ok legs=10 want='MTE_INTEROP: PASS legs_conforming=10/10' status=active needles=['MTE_INTEROP: PASS legs_conforming=10/10']
C1_R21_CASES missing=none
```

Every unit is zero: R (rows) 0, D (dropped) 0, M (mte row) 0, C (C3) 0, G (case literals) 0, and the
parser's summary-mismatch clause 0 (`measure.py:72-75`).

## 3. Rows not held — **none**

`held=49/49`, 56 row lines total, 7 `superseded` (`w3/T52W3ExecC1Probe/registry-check.stdout:57`,
`REGISTRY_CHECK: held=49/49 superseded=7`). Command that shows the negative directly:

```
grep -v ' held$' w3/T52W3ExecC1Probe/registry-check.stdout    # prints only the 7 superseded rows + the summary
grep -c '^ROW ' w3/T52W3ExecC1Probe/registry-check.stdout     # 56
```

The frozen parser excludes superseded rows by construction
(`.ufo/evidence/round-52/c1/measure.py:72`: `not sup and verdict != 'held'`), and the two rows that
*did* differ from BASE are exactly the repair: BASE
`tools/registry.json:1014` expected `legs_conforming=9/9` while `tools/mte-interop.py:74` already
carried a 10-key `LEG_TABLE` (`git -C LANE show ef19d8e1:tools/mte-interop.py` → BASE legs 10); at
CAND1 the row expects `10/10` and holds (`git diff ef19d8e1 7ff81a5b -- tools/registry.json` shows
that one row's `expect` and `source` lines as the whole change).

Two supporting anchors for the M unit: `tools/mte-interop.py:74-78` at CAND1 still holds 10 leg keys,
and the row is `status=active, kind=gate` with `--check` in argv (`git -C LANE show
7ff81a5b:tools/registry.json` → `rows 56 / active 49`).

Three superseded rows do return `exit=2` (could-not-evaluate) where their declared expects are
0/1/0:

```
ROW evidence-disposition-round17 superseded expect=0 got=2
ROW evidence-disposition-round17-before superseded expect=1 got=2
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
```

Cause (as far as the run shows): their argv point the tool at committed historical inputs
(`--dispositions .ufo/evidence/round-17/dispositions.json`, `…-before.json`,
`.ufo/evidence/round-14/dispositions.json`; `git -C LANE show 7ff81a5b:tools/registry.json`), and the
tool answers `2 could-not-evaluate` — the same historical-input refusal contract amendment 1
records for the control clone. They are `superseded`, excluded by the parser, and cost no unit; I did
not chase the exact refusal text because replaying a superseded row is outside this item.

## 4. C3 MISSING lines — **none**

```
C3_R51: rev=7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135 tools=30 rows=32 covered=30 missing=0 deleted=0 selftest_fail_rows=1 total=0 C3_R51_PASS=true
```

(`w3/T52W3ExecC1Probe/c3.stdout:31`; `grep -n 'MISSING\|DELETED' w3/T52W3ExecC1Probe/c3.stdout` →
no output; `grep -c '^C3_TOOL' …` → 30.) All 30 covered tools sit on `SKILL.md:2142-2171`, one
consecutive row each, every row `selftest exit=0`:

| tool | line | last line observed |
|---|---|---|
| `tools/round21-measure.py` | 2157 | `ROUND21_MEASURE_SELFTEST: 13/13 pass` |
| `tools/mte-interop.py` | 2148 | `MTE_SELFTEST: 17/17 pass` |
| `tools/registry-check.py` | 2154 | `SELFTEST: PASS (51 cases)` |
| `tools/evidence-disposition.py` | 2146 | `SELFTEST: PASS (66/66)` |

(The full 30-row list is `c3.stdout:1-30`.) The round-21 row that was the single MISSING at CAND0 is
green: its Self-test cell at CAND1 carries exactly one backticked span
(`git -C LANE show 7ff81a5b:SKILL.md | sed -n 2157p` → command span plus backtick-free prose
"… its subject counter c2-count.py names in its FLEET literal …"), satisfying the frozen row rule
`.ufo/evidence/round-51/c3/measure.py:125-127`.

`selftest_fail_rows=1` is **not** a missing tool and does not enter `total`
(`.ufo/evidence/round-51/c3/measure.py:232`: `total = missing + len(deleted)`). It is the stale
**duplicate** row at `SKILL.md:1504` (round-12 section):

```
| bash declared-witness study | probe | `python3 tools/bash-witness-study.py count` | … | `python3 tools/bash-witness-study.py selftest` | …
```

The self-test runs, exits 0 and prints `VERDICT: PASS`, but the cell contains no `VERDICT:` token, so
`run_row` returns `finding-id-not-in-row (VERDICT:)`
(`.ufo/evidence/round-51/c3/measure.py:179-180`). The tool is still covered by `SKILL.md:2142`
(`… → VERDICT: is the last line, preceded by WITNESS_SELFTEST: 51/51 pass`), so the failure is noise.
Verified by importing the frozen C3 functions against CAND1 bytes: the only candidate rows outside
the covering block are `SKILL.md:1503` (rejected earlier by `row_reason` as
`pinned-path-missing:mismatch/expected.json` — the pinned cell uses the relative path
`` `mismatch/expected.json` `` where `git ls-tree 7ff81a5b -- .ufo/evidence/round-12/ControlGate`
shows `ControlGate/mismatch/expected.json` exists) and `SKILL.md:1504`. So exactly one row reaches
the run-and-check stage and fails — the round-12 duplicate.

## 5. Scope guards I checked because the probe alone cannot

- **Dropped active rows** (`measure.py:111-117`, `base-active.json` vs the rev's registry):
  `C1_DROPPED none`; CAND1 has 56 rows, 49 active, base list 49.
- **Round-21 case literals** (`measure.py:31-34`, `:132-133`): `C1_R21_CASES missing=none` — all 11
  pinned `check("…")` literals present in `tools/round21-measure.py` at CAND1.
- **The round-21 selftest really is fleet-bound now**, which is what let the C3 row go green from a
  fresh clone: `git diff ef19d8e1 7ff81a5b -- tools/round21-measure.py` replaces
  `ROOT.parent / surface["repo"]` with a `FLEET` literal read out of the subject counter
  (`fleet = Path(re.search(r'^FLEET = Path\("([^"]+)"\)$', …))` at `:77-78`, used by the
  `git -C str(fleet / surface["repo"])` read at `:81`).

## 6. Secondary observations (not claim units)

- The probe ran at CAND1 while the lane HEAD is one commit later (`f1a3246` "wave-3 spec; re-key
  instrument; CAND1 precheck"). If the deciding run uses HEAD instead of CAND1 it is measuring
  different bytes; C1's predicate names REV, so this is only a naming risk for the L1.
- `tools/registry-check.py:766` hard-codes a `/tmp` clone for its fixture trees. After the run
  `ls -d /tmp/tameshi-registry-check-* | wc -l` → 0, so the clone was removed; seven other
  `/tmp/tameshi-*` directories exist but their mtimes (2026-10-26 21:24 … 2026-10-27 02:28) all
  predate this run (03:25-03:31) and are not this seat's. Environment note only — no `/tmp` path is
  cited as evidence anywhere in this report.
- Host dependence stands as the contract declares (`C1.sourced`): `round21-measure-selftest` and the
  C3 `round21-measure` row read the fleet root, so on a host without
  `/home/vgpnk/Projects/shokunin/kumitate-shokunin` they would go red for environmental reasons.
  Both were held here.
- `C1.cannot_see` still applies: the probe shows every row's needle is *satisfied*, not that it is
  *meaningful*. Only the mte needle is independently bound, and it agrees with the 10-key
  `LEG_TABLE`.

## 7. Risks and blockers

- **Non-deciding.** This is one probe run; if the L1's deciding run measures a different rev or a
  dirty worktree it can differ. Nothing here is a verdict on C1.
- No blockers. No tool installs or upgrades were made (none needed); `pacman` was not touched (guard
  honoured). No mutating git/jj command ran in the lane or the fleet repo; the only clone was the
  C3 counter's own shared clone inside the scratch work dir, and `registry-check.py`'s `/tmp` clone.
- Scratch `/fast/scratch/hyaku/tameshi-r52/T52W3ExecC1Probe` is deleted before this seat returns;
  every receipt cited above lives under `.ufo/waves/round-52/w3/`.

## 8. Evidence index (paths under `.ufo/waves/round-52/w3/`)

| file | sha256 |
|---|---|
| `T52W3ExecC1Probe.stdout` (counter stdout + explain, 35 lines) | `702c24e1e0cf400902da71693a63e32e76c85a0556997f2ba8da94d9f77876bd` |
| `T52W3ExecC1Probe/registry-check.stdout` (56 rows, 49 held / 7 superseded) | `a2294843a548f3357185d2855557419f63ab342b1bb65a8cb4e913b0478a56a7` |
| `T52W3ExecC1Probe/c3.stdout` (30/30 covered, missing=0) | `f4958f339c2008d8194f95f68c527e42747a3eb9bcf6c6bce89a5c42190ba3c6` |
| `T52W3ExecC1Probe/selftest.stdout` (9/9, exit 0) | `6942c0e5e63374af26981eb0a3bf5f41ff5d3f9a738576405dba27dce2a45219` |
| `T52W3ExecC1Probe/run.txt` (command, rc, wall, digests) | as written |

## Summary

- Frozen C1 counter at CAND1 `7ff81a5b0a` (exit 0, wall 636.49 s): `held=49/49 not_held=0 dropped=0
  mte_row=0 c3_covered=30 c3_total=0 r21_cases_missing=0 total=0 C1_R52_PASS=true`.
- Rows not held: **none**. 56 rows, 49 active all held against the BASE grader bytes
  (`cba16646…`); 7 superseded excluded by `measure.py:72`, three of which now exit 2
  (evidence-disposition historical inputs) and cost nothing.
- C3 MISSING lines: **none**. `covered=30 missing=0 deleted=0`, rows `SKILL.md:2142-2171`, all
  selftest exit 0; the CAND0 blocker (round-21 row, 3 backticked spans) reads 1 span at CAND1 and is
  covered with `ROUND21_MEASURE_SELFTEST: 13/13 pass`.
- `selftest_fail_rows=1` is the stale round-12 duplicate at `SKILL.md:1504` (`finding-id-not-in-row
  (VERDICT:)`); the tool is covered at `:2142`, so it is not a unit.
- Repair confirmed at CAND1: registry row expects `legs_conforming=10/10` against a 10-key
  `LEG_TABLE` (`tools/mte-interop.py:74`), where BASE expected `9/9` against the same 10 legs.
- Non-deciding probe only; the L1's deciding run owns the claim. No installs, no lane writes outside
  `w3/`, no mutating git/jj command, scratch deleted.
