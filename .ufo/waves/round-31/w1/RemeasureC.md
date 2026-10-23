# RemeasureC — independent re-measurement of the C1 observed column at base

Seat: `TameshiR31.RemeasureC` (executor, wave 1). Item: re-measure, without the
frozen counter, the values the C1 counter observed at
`36c1d3933f680125aeefc447f07db0f03004901a` and tabulate them against
`.ufo/evidence/round-31/before/c1-at-base.stdout`.

## Verdict

**REPRODUCED — 12 of 12 observed tuples are reproduced independently; 7
mismatches against the committed standing rows are confirmed.** The frozen
before receipt is accurate: `C1_R31: statements=12 mismatches=7 unparsed=0
unobservable=0 append_only=1 … C1_R31_PASS=false`, exit 1. No production file
was changed. The frozen counter (`.ufo/evidence/round-31/c1-measure.py`) was
never executed in this seat; only the twelve underlying commands were run, from
a scratch clone.

## Setup (measured)

- Clone: `/fast/scratch/hyaku/tameshi-r31-seats/RemeasureC/fleet/tameshi-shokunin`,
  `git clone -q --no-hardlinks` from the lane, `checkout -q --detach
  36c1d3933f680125aeefc447f07db0f03004901a`; `git rev-parse HEAD` →
  `36c1d3933f680125aeefc447f07db0f03004901a`.
- Fleet mirror: `/fast/scratch/hyaku/tameshi-r31-seats/RemeasureC/fleet/` with
  every sibling `*-shokunin` exposed as a symlink (read-only use).
- `SCORECARD.md` at base: blob `8c3241309d42365359f69cfde2f6805b10d3b1d1`,
  `sha256 518286e0758c85bf00c5aae6a29c0011cc8ab0284bd328b991b64671d6cea2f0`,
  118152 bytes, 1480 lines; worktree file equals the commit (`git diff --stat`
  empty).
- Command environment: `PYTHONDONTWRITEBYTECODE=1`, `GIT_DIR`/`GIT_WORK_TREE`/
  `GIT_INDEX_FILE` unset; every command wrapped in `timeout 900`.
- Table selection re-derived independently: the only `| Capability |` table is
  at `SCORECARD.md:238` (rows `:240-249`); the only `| Axis | Score (0–10) |`
  table is at `SCORECARD.md:64` (rows `:66-67`). Every later `| Axis | …` table
  has a verdict header (`Round-12 lane verdict`, `Round-16 lane verdict`, …),
  not a `Score…` second cell, so none competes for "last row of the frozen
  table type". My own parser (no import of the counter) reports the same 12
  claimed values the counter's `claimed=` column shows.

## Statement table (base)

`row states` = value read off the last row of its frozen table type.
`observed` = value I measured. `counter` = the value in
`.ufo/evidence/round-31/before/c1-at-base.stdout`.

| # | statement (SCORECARD anchor) | row states | my observed | counter observed | equal? |
|---|---|---|---|---|---|
| 1 | sources-registry (`:240`) | `exit 0, 44 rows` | exit 0; `== A rows` → `92`; `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | `0,92` | yes |
| 2 | mutation sweep runner (`:241`) | `MUTATE_SELFTEST: 80/80 pass`, exit 0 | `MUTATE_SELFTEST: 106/106 pass`, `VERDICT: PASS`, exit 0 | `106,106,0` | yes |
| 3 | six-leg regression ledger (`:242`) | `REGRESSION: PASS (cases=6 passed=6 …)`, exit 0 | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`, exit 0 | `PASS,9,9,0` | yes |
| 4 | repeated pristine-control gate (`:243`) | `PASS (29 cases)`, exit 0 | `SELFTEST: PASS (29 cases)`, exit 0 | `PASS,29,0` | yes |
| 5 | six-leg content-disposition probe (`:244`) | `18/18 PASS0` | `SELFTEST: PASS (19/19)`, exit 0 | `19,19,0` | yes |
| 6 | exposed witness provenance correction (`:245`) | `metadata selftest39/39 PASS0` | `SELFTEST: PASS 39/39`, exit 0 | `39,39,0` | yes |
| 7 | effective expectation reconciliation (`:246`) | `PASS34/34 exit0` | `SELFTEST: PASS (66/66)`, exit 0 | `66,66,0` | yes |
| 8 | retained invocation-context gate (`:247`) | `exit0, copied-source CLI selftest49/49` | exit 0; `selftest-new-full-count: PASS summary SELFTEST: PASS (49/49)` | `0,49,49` | yes |
| 9 | hermetic env-differential probe (`:248`) | `actual9/9` | `ENVDIFF_SELFTEST: 9/9 pass`, exit 0 | `9,9` | yes |
| 10 | callback-authoritative wave accounting (`:249`) | `frozen counter8/8` | `ACCOUNTING_SELFTEST: 8/8 pass`, exit 0 (extra suite `16/16 pass`) | `8,8` | yes |
| 11 | depth (`:66`) | `6` | `recorded_cases=9 depth_score=9`, exit 0 | `9` | yes |
| 12 | calibration (`:67`) | `0` | `calibration_restraint_score: 8`, exit 0 | `8` | yes |

Derived from the table: mismatches are statements 1, 2, 3, 5, 7, 11, 12 —
seven, exactly as the before receipt reports. Matches are 4, 6, 8, 9, 10 —
five. Append-only clause at `REV = base`: base `SCORECARD.md` is trivially a
byte prefix of itself (`base_bytes=118152 identical=True prefix=True`), so
`append_only=1` is correct at base and says nothing about a future revision.

## Exact commands and receipts

Run from the scratch clone root. Full stdout/stderr and exit codes are retained
under `/fast/scratch/hyaku/tameshi-r31-seats/RemeasureC/fleet/obs/` (`<name>.out`,
`<name>.err`, `<name>.exit`).

| # | command | exit | key line | receipt |
|---|---|---|---|---|
| 1 | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` | 0 | `== A rows` / `92`; `SOURCES_CENSUS: CLEAN` | `census.out` |
| 2 | `bash tools/mutate-and-run.sh --selftest` | 0 | `MUTATE_SELFTEST: 106/106 pass` | `mutselftest.out` |
| 3 | `bash tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r31-seats/RemeasureC/regression-wd` | 0 | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` | `regression.out` |
| 4 | `python3 tools/repeat-control.py --selftest` | 0 | `SELFTEST: PASS (29 cases)` | `repeatctl.out` |
| 5 | `python3 tools/pin-disposition.py --selftest` | 0 | `SELFTEST: PASS (19/19)` | `pindisp.out` |
| 6 | `python3 tools/witness-metadata.py --selftest` | 0 | `SELFTEST: PASS 39/39` | `witnessmeta.out` |
| 7 | `python3 tools/evidence-disposition.py --selftest` | 0 | `SELFTEST: PASS (66/66)` | `evdisp.out` |
| 8 | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` | 0 | `selftest-new-full-count: PASS summary SELFTEST: PASS (49/49)` (all listed gates PASS) | `verify.out` |
| 9 | `python3 tools/env-diff.py --selftest` | 0 | `ENVDIFF_SELFTEST: 9/9 pass` (first actual `9/9` per-case) | `envdiff.out` |
| 10 | `python3 tools/wave-accounting.py --selftest` | 0 | `ACCOUNTING_SELFTEST: 8/8 pass` | `waveacct.out` |
| 11 | command D (`SCORECARD.md:72-73`), `REV=36c1d39…` | 0 | `recorded_cases=9 depth_score=9` | `cmdd.out` |
| 12 | `python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev 36c1d3933f680125aeefc447f07db0f03004901a` | 0 | JSON `calibration_restraint_score: 8` (`overrides_used: false`, `trace_gate: strict`, `revision` = base) | `calmon.out` |

Timing: the ten short commands ran concurrently, 44.9 s wall; the selftest and
the six-leg regression ran concurrently, 300.7 s wall. Scratch footprint 158 MB.
No process started by this seat remains (checked every `/proc/*/cwd`; none
points into the seat scratch dir).

## Cross-checks (corroboration, not the frozen counter)

- Command C (`SCORECARD.md:74-75`, `REV=base`) → `boxes=4 checked=0 asserted=4
  untouched=0 asserted_mark_upper_bound=8`, exit 0. The four `[~]` marks are
  `SHONEN.md:5,7,9,11`; the monitor's own `shonen` object agrees
  (`asserted: 4`, `box3_marked: true`, `box3_ledger_link: true`) and credits
  `box3_full_page: true`.
- Round-27 `c1-measure.py` (a second, non-frozen instrument, referenced by the
  contract's `no_harm` field) at base:
  `C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9
  rev=36c1d39…`, exit 0. Two independent tools agree on `8` and `9`.
- Depth has two independent instruments: command D `recorded_cases=9` and
  `--regression` `cases=9` (with `passed=9`).
- Statement 1 is stale on either reading of the row's word "rows":
  `corpus/SOURCES.md` at base holds 92 `S…` rows (A=83, B=7, C=2), which equals
  the census's `== A rows` count of 92. So the frozen counter's A-row reading
  and a plain total-row reading coincide at base and both differ from `44`.
- Statements 5, 7, 11, 12's later round rows (`SCORECARD.md:587-588`,
  `:625-627`) already record different scalars (`depth 6 → 7`, `calibration
  6 → 8`), but those tables' headers are verdict tables, not `| Axis | Score
  (0–10) |`; the frozen statement set is the single baseline table at
  `:64`. They do not participate in the measurement and were not treated as
  claims about the standing rows.

## Smallest safe correction

None is required in production for this item, and none was made. The base state
is confirmed as recorded, so the wave-2 correction has to change the standing
rows, not the counter or the predicate. Measured shape constraint for that
correction (advisory; not implemented here): because the base file must remain a
byte prefix, the corrected statements cannot be produced by editing
`SCORECARD.md:66-67` or `:240-249` in place. The counter takes the last row per
id across tables whose first header cell is `Capability` or whose second header
cell starts with `Score`, and base has exactly one table of each shape, so an
appended table of the same header shape is what supersedes them. That is a
mechanical consequence of the frozen predicate, not a request to amend it.

## Risks and limits

1. One run per command. Repeat-variation of these values is the
   `DeterminismProbe` item, not mine; env-diff's known raw-output-variable case
   affects the round-21 real receipt, not its `9/9` selftest.
2. `verify.py` writes untracked artifacts into the repository it runs in
   (`.ufo/evidence/round-15/attempt-4/`, `verification-4.json`). In my clone
   this is inert; the frozen counter runs it in a disposable clone. Pointing it
   at the lane worktree would dirty that worktree.
3. The six-leg regression ran from the mirror lane clone with sibling repos
   exposed as symlinks under the same fleet directory; `REGRESSION_PIN` lines
   resolved to `fleet/kumitate-shokunin` at the pinned revisions and read them
   read-only. The counter runs the same command from a second mirror clone; the
   outputs agree.
4. The sources-registry comparison is label-sensitive: the frozen counter
   compares the census's `== A rows` line, while the row prose says only
   "rows". They coincide at base (92) and diverge only if A/B/C composition
   changes; the frozen reading governs.
5. No model or scalar verdict is claimed here. `8` and `9` above are the
   monitors' reported field values at base, quoted as observations.

## Scope compliance

No production file edited; no counter execution; no `git add/commit/checkout/
reset/stash/push/fetch/pull` in the lane or fleet repos; no `jj` command
anywhere; no sibling, lane index or lane jj state touched. No tool installed or
upgraded. Files written: this report and files under
`/fast/scratch/hyaku/tameshi-r31-seats/RemeasureC/`.
