# RemeasureA — independent re-measurement of the C1 observed values at base

**Verdict: CALIBRATED, all 12 frozen statements independently reproduce the counter's observed values at base `36c1d3933f680125aeefc447f07db0f03004901a`, exit 0 where the counter saw exit 0.** I did not run the counter. Every value below is my own execution of the same frozen command in my own scratch clone. 0 of 12 values differ from `.ufo/evidence/round-31/before/c1-at-base.stdout`. The base receipt's 7 mismatches are between the committed SCORECARD claims and the observed state, not between the counter and the state.

## Method

- Working dir: `/fast/scratch/hyaku/tameshi-r31-seats/RemeasureA/`.
- Fleet mirror: sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` symlinked into `fleet/`, lane cloned `--no-hardlinks` to `fleet/tameshi-shokunin` and checked out `--detach` at base. Second clone `clone-light` at base for the short selftests, so the mirror stays untouched by them.
- All runs used `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE PYTHONDONTWRITEBYTECODE=1` and `timeout` (900 s short, 1800 s selftest, 2700 s regression).
- I read the frozen counter source at lane commit `c111dab58b0a8d55e991bbd2efe3aad56717b95a` only to learn the 12 frozen commands and their observation regexes, and did not execute it. `git show c111dab...:.ufo/evidence/round-31/c1-measure.py | sha256sum` = `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584`, equal to `contract.json` `counter_sha256`. `git show c111dab...:.ufo/evidence/round-31/coldread/bind-select-v4.py | sha256sum` = `dd8bb39309cb337b4b0e6703657198fc88655ce4b498de2ad3f637e04030b87f`, equal to the contract binding hash. Base commit resolves in the clone (`git cat-file -e` ok).
- Each observation was repeated where a repeat is cheap: the mutation selftest, `evidence-disposition`, `pin-disposition` and the calibration monitor all returned the same value twice (see "Stability" below).

## Table: statement, observed by me, observed by the counter, equal?

Counter column is verbatim from `.ufo/evidence/round-31/before/c1-at-base.stdout` (tuple order per statement, as the counter prints `claimed=… observed=…`).

| statement | observed by me | observed by the counter | equal? |
|---|---|---|---|
| sources-registry | exit 0, 92 rows | exit=0, 0,92 | yes |
| mutation sweep runner | `MUTATE_SELFTEST: 106/106 pass`, exit 0 | 106,106,0 | yes |
| six-leg regression ledger | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`, exit 0 | PASS,9,9,0 | yes |
| repeated pristine-control gate | `SELFTEST: PASS (29 cases)`, exit 0 | PASS,29,0 | yes |
| six-leg content-disposition probe | `SELFTEST: PASS (19/19)`, exit 0 | 19,19,0 | yes |
| exposed witness provenance correction | `SELFTEST: PASS 39/39`, exit 0 | 39,39,0 | yes |
| effective expectation reconciliation | `SELFTEST: PASS (66/66)`, exit 0 | 66,66,0 | yes |
| retained invocation-context gate | `summary SELFTEST: PASS (49/49)`, process exit 0 | 0,49,49 | yes |
| hermetic env-differential probe | `ENVDIFF_SELFTEST: 9/9 pass`, exit 0 | 9,9 | yes |
| callback-authoritative wave accounting | `ACCOUNTING_SELFTEST: 8/8 pass`, exit 0 | 8,8 | yes |
| depth | `recorded_cases=9 depth_score=9`, exit 0 | 9 | yes |
| calibration | `"calibration_restraint_score": 8`, exit 0 | 8 | yes |

Claims at base (last row of each frozen table type in the committed `SCORECARD.md`) versus my observed values give exactly 7 non-equal statements: sources-registry (44 vs 92 rows), mutation sweep runner (80/80 vs 106/106), regression ledger (cases=6 vs 9), content-disposition (18/18 vs 19/19), expectation reconciliation (34/34 vs 66/66), depth (6 vs 9), calibration (0 vs 8). The other 5 equal (pristine-control 29, witness 39/39, invocation-context 0,49,49, env-differential 9/9, wave accounting 8/8). 7 mismatches is the frozen receipt's `mismatches=7`; the base SCORECARD is a byte prefix of itself, so `append_only=1` is trivially consistent.

## Evidence (exact commands and observed lines)

Working dir `/fast/scratch/hyaku/tameshi-r31-seats/RemeasureA/fleet/tameshi-shokunin` (base checkout):

```
bash .ufo/evidence/kaika-round-1/sources-census-v2.sh
  == A rows
  92
  ...
  SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)      exit=0
```

Cross-check by two orthogonal counts of `corpus/SOURCES.md`: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` = 92; `grep -oE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | wc -l` = 92 and `| sort -u | wc -l` = 92. The census script's own duplicate-id check printed nothing. So "92 rows" is a real registry size, not a regex artifact.

```
timeout 1800 bash tools/mutate-and-run.sh --selftest
  MUTATE_SELFTEST: 106/106 pass                            exit=0   (7.7 s)
timeout 2700 bash tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r31-seats/RemeasureA/rg
  REGRESSION_CASE js-kimi-census: PASS ... (all nine legs PASS)
  REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
                                                           exit=0   (298.8 s)
```

The regression ran from the mirror so `FLEET_ROOT=$(dirname $(dirname $(dirname $SELF)))` resolves to `/fast/scratch/hyaku/tameshi-r31-seats/RemeasureA/fleet`; the nine legs materialize their pinned blobs with read-only `git show` and write only into `rg/`. Static leg count in `tools/mutate-and-run.sh` matches: nine `regression_case_git` calls at lines 1386, 1391, 1396, 1401, 1406, 1411, 1416, 1421, 1426 (the remaining five `regression_case_git` hits are selftest fixtures).

Working dir `/fast/scratch/hyaku/tameshi-r31-seats/RemeasureA/clone-light` (base checkout), each under `timeout 900`:

```
python3 tools/repeat-control.py --selftest        -> SELFTEST: PASS (29 cases)        exit=0
python3 tools/pin-disposition.py --selftest       -> SELFTEST: PASS (19/19)           exit=0
python3 tools/witness-metadata.py --selftest      -> SELFTEST: PASS 39/39             exit=0
python3 tools/evidence-disposition.py --selftest  -> SELFTEST: PASS (66/66)           exit=0
python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72
                                                  -> summary SELFTEST: PASS (49/49)   exit=0
python3 tools/env-diff.py --selftest              -> ENVDIFF_SELFTEST: 9/9 pass       exit=0
python3 tools/wave-accounting.py --selftest       -> ACCOUNTING_SELFTEST: 8/8 pass    exit=0
git show 36c1d39...:tools/mutate-and-run.sh | python3 <regex file>
                                                  -> recorded_cases=9 depth_score=9   exit=0
python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone-light> --rev 36c1d39...
                                                  -> "calibration_restraint_score": 8 exit=0
```

The depth count used the identical regex `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+` (multi-line) fed from `git show "$REV:tools/mutate-and-run.sh"`; the only difference from the counter is that the snippet lives in a scratch file instead of `python3 -c`, which cannot change the count.

Raw outputs retained at `/fast/scratch/hyaku/tameshi-r31-seats/RemeasureA/{selftest.out,regression.out,obs/*.stdout,obs/*.stderr}`.

## Stability

- `tools/mutate-and-run.sh --selftest` twice: `106/106 pass` both times.
- `tools/evidence-disposition.py --selftest` twice: `PASS (66/66)` both times.
- `tools/pin-disposition.py --selftest` twice: `PASS (19/19)` both times.
- `coldread/measure.py` twice: `calibration_restraint_score = 8` both times.
- Wall times (selftest 7.7 s vs 1800 s cap; regression 298.8 s vs 2700 s cap) leave large margin, so no timeout confound at base.

## Calibration notes (advisory to the L1, no amendment of the freeze)

1. The counter's observed column is trustworthy at base: an independent implementation path (separate clones, isolated runs, no shared scratch) returned all 12 tuples identically. The counter's 7 mismatches are genuine SCORECARD drift (the largest: census rows 44 to 92; expectation reconciliation 34 to 66).
2. Concurrency: the counter runs all 12 commands at once in one clone; I ran them isolated. Values agreed, so no cross-talk is visible at base. This is evidence about these fixed inputs only, not a general concurrency-safety proof.
3. Binding trap for the wave-2 row rewrite, derived from the frozen counter source: capability rows are keyed by the first cell verbatim (`rows[(kind, cells[0])]`), so the labels must stay exactly `sources-registry`, `mutation sweep runner`, **`six-leg regression ledger`** (do not rename to "nine-leg": the entry would become UNPARSED, since a missing row or a non-matching label is `UNPARSED`, not a mismatch to be repaired later), `repeated pristine-control gate`, `six-leg content-disposition probe`, `exposed witness provenance correction`, `effective expectation reconciliation`, `retained invocation-context gate`, `hermetic env-differential probe`, `callback-authoritative wave accounting`. Axis rows must keep first cells `depth` and `calibration`, and the second cell must be a bare integer that `re.fullmatch(r'\d+')` accepts (`9`, `8`; not `9/10`).
4. Each row's claim regex binds to the row text, so the new rows must state the numbers in the frozen phrasings, for example `exit 0, 92 rows`; `` `MUTATE_SELFTEST: 106/106 pass`, exit 0``; `cases=9 passed=9 ..., exit 0`; `PASS (29 cases), exit 0`; `19/19 PASS0`; `metadata selftest39/39 PASS0`; `PASS66/66 exit0`; `exit0, copied-source CLI selftest49/49`; `actual9/9`; `frozen counter8/8`.
5. Because the counter reads the **last** row of each table type and requires the base SCORECARD to remain a byte prefix, the correct shape is append new rows after the old ones, never edit the old rows.

## Smallest safe correction

None in this seat: I changed no file in any repository. For the round, the smallest safe correction is the one wave 2 already owns, restating the 10 capability rows and the 2 axis rows by append with the values in the table above, keeping the frozen labels and phrasings from note 3 and 4.

## Risks and limits

- I did not and cannot verify behaviour at the future lane revision; this report measures only base.
- The counter's `six-leg regression ledger` name is stale for a tool that now replays nine legs; the value 9 is real, while the label must be preserved because it is the frozen binding key.
- The calibration monitor reads external files outside the lane (hashes appear in its JSON). I recorded only the score; no external content was copied.
- One process concern: the regression run was moved to a harness background job after 60 s and I waited for it; it exited 0, and I killed nothing and started no other process.

## Tooling

No tools installed or upgraded. Used the system `git`, `python3`, `bash`, `timeout`, `grep`, `wc` only.

## Files changed

- `.ufo/waves/round-31/w1/RemeasureA.md` (this report, the only file written outside my scratch dir).
- Scratch only: `/fast/scratch/hyaku/tameshi-r31-seats/RemeasureA/{fleet/,clone-light/,rg/,obs/,selftest.out,regression.out,run-light.sh,depth-count.py}`.
