# tameshi round 78 — plan (frozen before any wave data)

Lane: tameshi-shokunin. Base: `5bcb13ea7cc08bb0b594fcd0c2bb770cb8fe64a0`
(branch `master` = `origin/master`, clean tree — the round-77 non-author closure
verdict commit). Round 78 (attempt 1), hyaku run 15.

Round shape: **one v1 wave, 12 seats** (policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16; attack seats by the policy's
named set = reviewer 2 + critic 1 + mutation-tester 1 = 4 = 33.3 %). `labrat` is
a frozen-topology seat the validator rejects; the canonical §3 planner seat is
held by the L1, and a bounded planning data-walk rides the scout item.

Saturation state at round start (SCORECARD.md): scored axes depth 10,
calibration 8, freshness 9 — all at or above the saturation line 8. Rounds 75,
76 and 77 entered no capability row, so the stagnation window (N = 2) is full
and the nudge is **ACTIVE**: round 78 is the capability round (AXES.md §The
stagnation nudge). C1 is therefore a capability acquisition; C2 works coverage,
a verdict-only axis, so the lowest-axis obligation is not waived — it is met by
the capability ground the nudge directs.

Two claims on distinct axes, causally separable: C1 lands only inside
`tools/selfstate-freshness.py`, `tools/selfstate-freshness.json` and the
`SCORECARD.md` capability row it demonstrates; C2 lands only inside
`tools/wave-reconcile.py`, `tools/wave-reconcile-mutants.spec` and their
battery receipts. Neither counter runs the other's instrument: C1's sweep
executes the rows' pinned instruments (the bash row runs
`tools/mutate-and-run.sh`, not `wave-reconcile.py`), C2's battery executes
`tools/wave-reconcile.py --selftest` (never the selfstate sweep).

Design-phase disclosure (pre-data, this plan's own commit): the L1 built both
candidates and ran their counters before this plan was frozen. The candidate
bytes, both controls, the base-state receipts and the landed battery are
committed under `.ufo/evidence/round-78/` in the same commit as this plan
(`design/` holds the exact candidate bytes and `design/SHA256SUMS`). The lane's
`tools/` files currently hold the same bytes, uncommitted until the landing
commit. The predicates below are frozen against those measurements; the wave's
seats re-derive and attack them and never edit the lane.

## R78-C1 — operability, capability acquisition: a non-Python instrument can carry a live freshness row

**What the lane could not do (round-77 carry).** `tools/selfstate-freshness.py`
executed every instrument as `['python3', '-I', '-X', 'utf8', dest] + argv`
(`tools/selfstate-freshness.py` at base, the `GitInstrumentRunner.__call__`
body), so the lane's bash mutation runner could never be a live row — the
round-77 lesson recorded the gap ("a bash instrument cannot become a live row")
and criterion 127 requires a frozen tuple table for a widened runner.

**Before (measured at base `5bcb13ea`).**
- Base sweep, base manifest: `SELFSTATE: rows=20 match=18 stale=2 unexpected=0`,
  exit 0 (`.ufo/evidence/round-78/c1-base-sweep.txt`).
- Do-nothing control (the cheapest control that skips the claimed work: the
  BASE runner bytes plus the NEW manifest row): `SELFSTATE error=setup
  figure-absent:mutation-runner-selftest`, exit 2, no summary
  (`.ufo/evidence/round-78/c1-control-bash-row-on-base-runner.txt`). A round
  that adds only the row cannot reach the after-state.

**After.**
- A frozen interpreter tuple table binds a row's `instrument.interpreter` to its
  runner: `python -> ('python3', '-I', '-X', 'utf8')` (the base default,
  unchanged) and `bash -> ('bash',)`; an undeclared interpreter defaults to
  python; any other name is a setup refusal (`interpreter-unknown:<id>:<name>`)
  before any row effect.
- One live row `mutation-runner-selftest` binds the `mutation sweep runner`
  capability row's printed figure `MUTATE_SELFTEST: \d+/\d+ pass` to
  `tools/mutate-and-run.sh --selftest` at the base revision, interpreter
  `bash`.
- The capability demonstrates: the live sweep executes the bash instrument and
  prints `SELFSTATE_ROW mutation-runner-selftest … measured=match ok`,
  `SELFSTATE: rows=21 match=19 stale=2 unexpected=0`, exit 0.
- `SELFSTATE_SELFTEST: 13/13 pass` exit 0, with arm 12 (unknown interpreter
  refused) and arm 13 (a `bash` row executed from extracted bytes through the
  tuple table by the real CLI against a git fixture).

Counting commands (pasteable; after-state at the landing rev):

```sh
python3 -I -X utf8 tools/selfstate-freshness.py --selftest | tail -1
python3 -I -X utf8 tools/selfstate-freshness.py --repo . \
  --doc-rev 5bcb13ea7cc08bb0b594fcd0c2bb770cb8fe64a0 | tail -2
```

**Kill rule (frozen).** C1 fails if (i) the base sweep with the base manifest is
not `rows=20 match=18 stale=2 unexpected=0` exit 0, or the do-nothing control is
not exit 2 with `figure-absent:mutation-runner-selftest`; (ii) the landed sweep
is not `rows=21 match=19 stale=2 unexpected=0` exit 0 with the bash row
`measured=match`; (iii) `--selftest` is not `13/13` exit 0; (iv) any of the base
20 rows changes its measured state (the no-harm monitor below); (v) the
interpreter table admits a name other than `python`/`bash`, or a row without a
declared interpreter does not run under the python tuple; or (vi) the capability
row does not enter `SCORECARD.md`'s `## Capabilities` table in this round with
the sweep evidence pointer.

## R78-C2 — coverage: the two round-77 survivors become fixture coverage

**Named survivors (round-77 wave, `corpus/lessons/round-77.md` §Wave findings).**
`git-listing-uses-head` (`GitReader.listing` resolves `HEAD` instead of the
row's rev) and `arm20-cleanup-removed` (the arm20 fixture cleanup is deleted:
suite green, one leaked `wave-reconcile-git-*` dir per run) both survived the
round-77 suite 20/20 because the fixture was one commit deep (HEAD == rev) and
no arm had a leftover post-condition.

**Before (measured at base `5bcb13ea`).**
`python3 -I -X utf8 <base tools/wave-reconcile.py> --selftest` →
`WAVE_RECONCILE_SELFTEST: 20/20 pass` exit 0
(`.ufo/evidence/round-78/c2-base-selftest.txt`). The do-nothing control is the
round-78 10-defect spec run against BASE bytes: `MUTATE: DONE
(target=wave-reconcile-base-control-r78 defects=10 killed=8 survived=2
inconclusive=0 kill-rate=80%)`, the two survivors being exactly
`git-listing-uses-head` and `arm20-cleanup-removed`, `CONTROL: GREEN`, restore
byte-identical (`sha256 67d3a4cc2e75…`)
(`.ufo/evidence/round-78/c2-base-control-battery.txt`).

**After.**
- arm20 gains a leftover post-condition: the arm scans the scratch parent for
  `wave-reconcile-git-*` entries before and after the fixture and returns
  `leak:<n>` instead of `meet` when a fixture survives its cleanup.
- arm21 builds a TWO-commit fixture (rev1 carries the record and
  `wave/one.md`; rev2 = HEAD adds `wave/two.md`) and measures the row at rev1:
  the pinned listing is one top-level report → `meet`; a reader resolving HEAD
  sees two → `drift`. `SELFTEST_ARMS` 20 → 21.
- `tools/wave-reconcile-mutants.spec` gains the two defects (10 total; the
  first eight blocks byte-identical to base).
- Landed battery: `CONTROL: GREEN`, `MUTATE_RESTORE: OK` byte-identical,
  `MUTATE: DONE (target=wave-reconcile-arms-r78 defects=10 killed=10
  survived=0 inconclusive=0 kill-rate=100%)`; landed selftest `21/21 pass`
  exit 0.

Counting commands (pasteable; after-state at the landing rev):

```sh
python3 -I -X utf8 tools/wave-reconcile.py --selftest | tail -1
bash tools/mutate-and-run.sh --target tools/wave-reconcile.py \
  --defects tools/wave-reconcile-mutants.spec \
  --suite 'python3 -I -X utf8 "$MUTANT" --selftest' \
  --workdir "$HYAKU_SCRATCH/tameshi-r78/l1/battery" --label wave-reconcile-arms-r78
```

**Kill matrix (frozen; measured on the design-phase candidate, pristine 21/21):**

| mutant | dies on |
|---|---|
| `m2-delimited-tautology` | arm13 + arm16 (unchanged) |
| `span-rule-removed` | arm14 + arm17 + arm18 (unchanged) |
| `seat-reports-any-depth` | arm15 + arm20 (unchanged) |
| `mc-record-bound` | arm16 (unchanged) |
| `roles-bypass` | arm17 (unchanged) |
| `attack-bypass` | arm18 (unchanged) |
| `adv-seatreports-require-printed-bypass` | arm19 only (unchanged) |
| `git-listing-recursion-removed` | arm20 + **arm21** (NEW intrinsic collateral: a non-recursive listing of the two-commit fixture also drifts, disclosed) |
| `git-listing-uses-head` | **arm21 only** (new) |
| `arm20-cleanup-removed` | **arm20 only** (new) |

**Kill rule (frozen).** C2 fails if (i) the base control is not
`killed=8 survived=2` with exactly those two survivors and `CONTROL: GREEN`;
(ii) the landed selftest is not `21/21` exit 0; (iii) the landed battery is not
`defects=10 killed=10 survived=0` with `CONTROL: GREEN` and byte-identical
restore; (iv) any defect's kill set differs from the frozen matrix, or
`git-listing-recursion-removed` fails any arm other than the disclosed
arm20 + arm21; (v) any base arm 1–20 changes its outcome between base bytes and
landed bytes (the no-harm monitor below); or (vi) the landed bytes change any
counter other than the selftest arm count and the spec defect count (the
standing six-row wave sweep and the 20-row selfstate sweep stay out of scope
except as the C1 monitor).

## No-harm monitors

- `diff <(grep -E 'SELFTEST arm(1[0-9]|[1-9])-' base) <(… landed)` → empty
  (arms 1–19 byte-identical; arm20 keeps its `meet`).
- Base 20 selfstate rows: `diff` of the `SELFSTATE_ROW` lines, base sweep vs
  landed sweep minus the new row → empty.
- `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 107/107 pass`
  before and after (the C1 row's instrument is unchanged: pinned at base).
- No other tool's counter is read by either claim.

## Sources

C1 rests on **S306** (GNU Bash manual, *Invoking Bash*, opened this round); C2
rests on **S091** (gitrevisions, re-opened this round for the HEAD ground, a
different ground than its round-20 short-hex-pin scope). Both snapshots and
their located quotes land under `.ufo/evidence/round-78/sources/` and in the
round lesson's `## Gate`.

## Admission

Every claim is judged on the counter, kill rule and predicate above. A claim
that misses is an honest stop, never a narrowed target. The round is admitted
only if both claims verify and no axis is harmed.
