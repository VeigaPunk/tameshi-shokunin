# C2Tautology — is "official score equals tameshi kill rate" a tautology?

Seat: TameshiR25.C2Tautology (critic, leaf). Target: C2 in `.ufo/evidence/round-25/contract.json` and
`tools/mte-interop.py` at the amended revision (tool sha256 `311448d9…`, equal to
`contract-amendment-1.json` `tool_sha256_now`).

## Verdict

Yes, the score comparison is a tautology. The format-interop capability is real, but the
statement that the official score "equals the tameshi kill rate" (contract.json:23) is true by
construction and cannot fail on ledger data. The score check, the ledger check and the schema
check can each be deleted without changing the C2 counter's output. Only the selftest notices,
and the selftest never runs the emitter's status map. In the contract's live `--fleet-root` mode,
the `FAIL` verdict cannot be reached from ledger data at all: the outcome is either
`PASS 8/8` or `SETUP`.

This is a fixable defect in the wording and the falsifiers, not a reason to reject the
capability. The schema acceptance and the library run against pinned official artifacts are
genuine interop evidence. They should be claimed as a one-time property of the emitter, not as
8 independent confirmations, and not as a score agreement.

## Evidence

### 1. The "tameshi kill rate" is re-derived from the report itself

- The emitter writes `status` and `statusReason` from the same variable in one dict literal:
  `'status': STATUS[verdicts[d['id']]]` and `'statusReason': 'tameshi verdict %s' % verdicts[d['id']]`
  (`tools/mte-interop.py:139-140`).
- `tameshi_counts` computes the "tameshi" side by reading back `statusReason` from that same report
  (`:147-155`). It does not read `results.tsv`, the `REGRESSION_TABLE` measured counts, or the
  sweep's `MUTATE:` line.
- The `TABLE` regex captures `measured-killed`, `survived` and `inconclusive` (`:60-61`), but
  `check` keeps only groups 2 and 3, the recorded total and the recorded killed count (`:262`).
  The independent measured numbers are thrown away.
- The official formula is `mutationScore = (killed+timeout)/(killed+timeout+survived+noCoverage)*100`,
  and RuntimeError counts as invalid
  (`mutation-testing-metrics-3.9.0.tgz:package/src/calculateMetrics.ts:234-253`).
- An exact replay (killed-delta 0 and inconclusive 0, enforced at `tools/mutate-and-run.sh:1239-1244`)
  emits only `Killed` and `Survived`. The official score then reduces algebraically to
  `100·k/(k+s)`, the same expression as `:206`. The comparison tests only that the pinned library
  reads `Killed` as detected and `Survived` as undetected. That is a constant of a pinned,
  sha512-checked artifact, and repeating it on 8 legs adds no further information.

### 2. Live mode cannot produce FAIL from ledger data

`run_regression` raises `Setup` whenever the runner exits non-zero (`tools/mte-interop.py:242-243`).
A judged leg has therefore always passed the exact band. On such a leg:

- The killed count from `results.tsv` equals `recorded-killed`.
- killed + survived equals the recorded total.
- inconclusive is 0.

So the ledger arm (`:211-212`) restates the regression gate. In this mode `MTE_LEG … FAILS` fires
only when the tool's own code or the pinned library regresses.

### 3. Mutants of the check (run on scratch copies under `/tmp/c2taut` only)

**Setup.** I used `--workdir /tmp/c2taut/wd`, assembled from the 6 legs that had finished sweeping
in peers' kept workdirs (`/tmp/tameshi-mte-regression-nd6l_4mb`, `…-c_wgc958`). I copied only
`pristine.target.*`, `spec.copy` and `results.tsv`, and synthesized a `regression.stdout` with exact
`REGRESSION_TABLE` lines. `js-round-gate` and `js-sources-check` were not available. I did not
execute the live `--fleet-root` 8-leg run. Every command was
`uv run -q --no-project --with jsonschema==4.25.1 python3 <copy>/tools/mte-interop.py …`
(scripts: `/tmp/c2taut/run.sh`, `/tmp/c2taut/run2.sh`).

**Baseline.** Unmodified tool: `MTE_INTEROP: PASS legs_conforming=6/6` (exit 0) and
`MTE_SELFTEST: 10/10 pass` (exit 0).

| Mutant or doctored input | `--check` | `--selftest` |
|---|---|---|
| `STATUS['SURVIVED']='NoCoverage'` | PASS 6/6 (exit 0) | 10/10 |
| `STATUS['KILLED']='Timeout'` | FAIL 0/6 (exit 1), on the killed count only; the score still equals | 10/10 |
| `STATUS['INCONCLUSIVE']='Killed'` | PASS 6/6 | 10/10 |
| `STATUS['INCONCLUSIVE']='Timeout'` (Stryker-faithful for exit 124) | PASS 6/6 | 10/10 |
| score arm forced `True` | PASS 6/6 | 9/10; only `timeout-is-not-a-tameshi-kill` fails |
| ledger arm forced `True` | PASS 6/6 | 7/10 |
| schema arm forced `True` | PASS 6/6 | 7/10 |
| balanced flip in `bash-checklist-run/results.tsv` (A1 SURVIVED→KILLED, A2 KILLED→SURVIVED, recorded table unchanged) | `MTE_LEG bash-checklist-run: CONFORMS … official_killed=7 recorded_killed=7`, PASS 6/6 | n/a |
| `js-kimi-census` D1 → INCONCLUSIVE | `FAILS … official_valid=9 recorded_defects=10`, FAIL 5/6 (exit 1) | n/a |

What the table shows:

- **The selftest never runs the emitter.** Every case is a hand-built report (`:298-327`). Any
  change to the `STATUS` map passes the selftest. The `INCONCLUSIVE` entry is exercised nowhere:
  live replays require inconclusive 0, and the selftest hard-codes its statuses.
- **The score arm is uniquely needed by one case only.** That case,
  `timeout-is-not-a-tameshi-kill` (`:313-314, 325`), is a report whose `status` (`Timeout`)
  contradicts its own `statusReason` (`SURVIVED`). The emitter cannot produce it. In
  `status-flipped-vs-verdict`, the ledger arm already catches the flip.
- **The ledger arm compares counts, not identities.** In `--workdir` mode a balanced verdict flip
  conforms, although the regression gate would report `flips=2` and FAIL. In live mode the flip
  never reaches the judge.

### 4. Which parts carry real information

| Part | Live 8/8 information | Notes |
|---|---|---|
| Schema acceptance | One-time and real: the emitter's fixed shape is accepted by the pinned official draft-07 schema. | Per leg it is constant. Positions are ≥1 by construction (`:109-112`), statuses come from a fixed enum-valid map, every field is a string, and duplicate ids are refused earlier (`:128-129`). The validator runs with no `FormatChecker`, so the schema's only `format: uri` is ignored. The schema does not check locations against `source`. |
| Score equality | None beyond "the pinned library treats Killed and Survived as detected and undetected". | Algebraic identity under the 1:1 mapping (§1). |
| Timeout and RuntimeError semantics | None in live mode. | Tameshi INCONCLUSIVE includes suite timeouts (exit 124, `tools/mutate-and-run.sh:539`). Stryker semantics count `Timeout` as detected, and the official formula agrees (`calculateMetrics.ts:234`). Mapping to `RuntimeError` is a chosen convention that keeps tameshi's denominator, not an equivalence. A Stryker-faithful mapping would make the official score differ from tameshi's rate on any leg with a timeout. No live leg can contain one, and neither mapping is tested against the emitter. |
| Ledger counts | In live mode, implied by `REGRESSION: PASS`. | In `--workdir` mode they catch INCONCLUSIVE rows and killed-count drift, but not balanced flips. Of the `STATUS` mutants, the only one any check catches is `KILLED→Timeout`, via `official['killed']`. The node runner already returns `survived` and `totalInvalid` (`:69-70`), but `judge` ignores both, which is why `SURVIVED→NoCoverage` survives. |
| Rounding of ledger percentages | None. The tool never compares a recorded percentage. | The runner rounds half up, `pct=(200k+n)/(2n)` (`tools/mutate-and-run.sh:562`). The ledger records `7/15 = 47 %` (`SKILL.md:1103, 1316`) and the runner prints `kill-rate=47%`, but the official score is `46.666666666666664` (observed baseline line for `bash-checklist-run`). Read against the runner's printed kill rate, "official score equals the tameshi kill rate" is false for that leg; it holds only for the unrounded fraction. On the 6 observed legs the Python and JavaScript evaluation orders are bit-equal, so the `1e-9` tolerance is not load-bearing there. It is load-bearing in the selftest's 2/3 case (`66.66666666666666` vs `66.66666666666667`) and in the INCONCLUSIVE probe (`77.77777777777779` vs `77.77777777777777`). |
| Setup invariants | Real but small: each `@old` is unique in the pristine target, spec defect ids equal the results rows, and each verdict is in the vocabulary. | These are the only data-dependent conditions in live mode, and their failure gives SETUP, not FAIL. |

## Impacted axes

- **Coverage (the axis C2 is judged on).** The capability gain is real: reports are emitted,
  accepted by the official schema and scored by the official library. "legs_conforming=8/8"
  overstates it as 8 independent agreements when it is one property counted eight times.
- **Calibration.** The claim risks provenance overreach: the "tameshi kill rate" is not an
  independent measurement, and the ledger percentage is rounded.

## Smallest safe correction

### Wording (replacement for the C2 statement)

> For each recorded mutation-ledger leg that `tools/mutate-and-run.sh --regression` replays exactly
> (REGRESSION: PASS), `tools/mte-interop.py` emits a mutation-testing-elements report that the pinned
> official schema 3.9.0 accepts and that the pinned official mutation-testing-metrics 3.9.0 library
> scores. Under the emitter's one-to-one mapping (KILLED→Killed, SURVIVED→Survived; an exact replay
> has no INCONCLUSIVE), the official score equals the unrounded killed/(killed+survived)×100 by
> construction. This agreement shows that the library reads those two statuses as detected and
> undetected; it is not an independent re-measurement. The official killed and valid counts equal
> the recorded ledger table, which the regression gate already enforces. The ledger's rounded
> percentages are not compared (bash-checklist-run scores 46.67, recorded as 47 %). INCONCLUSIVE
> maps to RuntimeError by convention, including suite timeouts that Stryker would report as
> Timeout (detected); the selftest exercises this only with hand-built reports.

### Additional falsifiers (each closes a demonstrated gap)

1. **Independent comparator.** Capture `measured-killed`, `survived`, `inconclusive` and `flips`
   from `REGRESSION_TABLE` (extend the regex at `:60-61`). Require:
   - `official.survived == survived`, which kills `SURVIVED→NoCoverage`;
   - `official.totalInvalid == inconclusive`;
   - `flips == 0`.

   This closes the balanced-flip pass in `--workdir` mode. Optionally, compute `tameshi_score`
   from these captured counts instead of from `statusReason`.
2. **An emitter-level negative control in the selftest.** Build a tiny leg directory with one
   `INCONCLUSIVE` row (exit 124), run it through `leg_report`, and assert `status == 'RuntimeError'`
   and `official.totalInvalid == 1`. This kills the `INCONCLUSIVE→Killed` and
   `INCONCLUSIVE→Timeout` mutants, which currently survive both modes.
3. **A rounding falsifier.** Assert that rounding half up the official score equals the integer
   `kill-rate` in the leg's `sweep.log` `MUTATE:` line. Record that strict equality is false for
   `bash-checklist-run`, so the claim is held to the unrounded fraction.

For the judge, the tradeoff is whether "score equals" may count as a C2 acceptance criterion at
all. I recommend reclassifying it as a sanity check and taking schema acceptance plus falsifiers
1 and 2 as the load-bearing evidence.

## Process notes

- No tool installs or upgrades. I used the existing `uv` 0.13.0, node v24.21.0 and python3, with
  jsonschema 4.25.1 resolved ephemerally by `uv run --with`.
- Nothing was written in the lane except this report. I read peers' kept `/tmp` workdirs and did
  not modify them. Scratch copies live under `/tmp/c2taut`.
- No git or jj write commands. One read-only `GIT_OPTIONAL_LOCKS=0 git log` and `git status`.
