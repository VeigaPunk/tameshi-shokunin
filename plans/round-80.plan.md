# tameshi round 80 — plan (frozen before any wave data)

Lane: tameshi-shokunin. Base: `dd2b9e2c44df680174a829901829fe86a2185185`
(branch `master` = `origin/master`; the round-79 non-author closure and its
spot-check commit). Round 80 (attempt 1), hyaku run 15.

Round shape: **one v1 wave, 13 seats** (policy
`/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`, band 8–16;
attack seats by the policy's named set = reviewer 2 + critic 1 +
mutation-tester 1 = 4 = 30.8 %). Roles: executor 4, scribe 1, scout 2,
reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1. `labrat` is
a frozen-topology seat the validator rejects; the canonical §3 planner seat is
held by the L1 and a bounded planning data-walk rides a scout item.

Saturation state at round start (`SCORECARD.md`): scored axes depth 10,
calibration 8, freshness 9 — all at or above saturation line 8. Round 79
entered a capability (`receipt-bytes binding sweep`), so the stagnation window
(N = 2) is NOT full and the nudge does not fire: the lowest-axis obligation
binds and **C1 works calibration, the lowest scored axis (8)**.

Three claims on distinct axes, causally separable: C1 lands only in
`tools/registry-figure-bind.py`, `tools/registry-figure-bind.json`, the
`SKILL.md` round-80 registry section, the refreshed `tools/registry.json`
tokens and its receipts; C2 lands only inside `tools/selfstate-freshness.py`,
`tools/wave-reconcile.py`, their two mutant specs and their battery receipts;
C3 lands only inside `tools/receipt-bytes-bind.py` and its receipts. C1's
counter RUNS the instruments (it reads their stdout), which is disclosure, not
coupling: no row of C1 reads C2's or C3's receipts, and no counter executes
another claim's *instrument as its subject*.

Design-phase disclosure (pre-data, this plan's own commit): the L1 built all
three candidates and ran their counters before this plan was frozen. The
candidate bytes are committed here under `.ufo/evidence/round-80/design/`
(`design/SHA256SUMS`) and the lane's `tools/` currently holds the same bytes,
uncommitted until the landing commit. The predicates below are frozen against
those measurements; the wave's seats re-derive and attack them and never edit
the lane.

## R80-C1 — calibration: the registry home's printed figures equal the live figures

**What the lane got wrong (round-79 non-author closure defect 5).** SKILL.md's
latest registry section (`### Gate/probe registry — round 76`) still read
`WAVE_RECONCILE_SELFTEST: 19/19 pass` / "7 defects" (tool: 23/23 / 12) and
`SELFSTATE_SELFTEST: 11/11 pass` over "20 rows" (tool: 14/14 over 22), and the
round-79 capability `receipt-bytes binding sweep` had no registry row in
SKILL.md or `tools/registry.json` at all. A stale self-description is
overreach in the lane's own assessment of what it holds.

**Before (measured at base `dd2b9e2c`, design instrument over the declared
7-row manifest).** `REGISTRY_BIND: rows=7 match=0 stale=5 absent=2 error=0
unexpected=7`, exit 1 (`.ufo/evidence/round-80/design/c1-before-sweep.txt`):
five stale rows (SKILL.md and `registry.json` for wave-record reconciliation
19/19→23/23 and self-state freshness 11/11→14/14, plus the registry's sweep
row `rows=20 match=18`→`rows=22 match=20`) and two absent rows (no
`receipt-bytes binding sweep` row on either surface). The do-nothing control
is this base reading: appending nothing to either surface cannot reach the
after-state, and a counter that ignored a surface would report fewer rows
than 7 (the manifest is the declared population).

**After.**
- `tools/registry-figure-bind.py` (new): a declared manifest of 7 rows over
  two surfaces (`doc` = the LAST markdown row of a name in a doc; `registry-json`
  = a `rows[]` entry of `tools/registry.json`); the manifest `figure` regex
  must match exactly once in the declared row and once in the live
  instrument's stdout; a row measures `match`, `stale`, `absent` or `error`,
  and `expect` (`match`|`stale`) is declared per row so a standing red arm
  MEASURES its divergence every sweep.
- `SKILL.md` gains `### Gate/probe registry — round 80` with the three rows
  (wave-record reconciliation and self-state freshness refreshed, the new
  `registry-figure-bind` row and a `receipt-bytes binding sweep` row), and
  `tools/registry.json` gains/refreshes the same figures (including
  `registry-figure-bind-selftest`, `receipt-bytes-selftest`,
  `receipt-bytes-tree`).
- A selfstate capability row `registry-bind-selftest` binds the new
  capability's figure in `tools/selfstate-freshness.json`.

**Counting commands (pasteable; after-state at the records rev):**

```sh
python3 -I -X utf8 tools/registry-figure-bind.py --selftest | tail -1
python3 -I -X utf8 tools/registry-figure-bind.py --repo . | tail -1
```

**Kill rule (frozen).** C1 fails if (i) the base sweep is not
`rows=7 match=0 stale=5 absent=2 error=0 unexpected=7` exit 1; (ii) the landed
sweep is not `REGISTRY_BIND: rows=7 match=7 stale=0 absent=0 error=0
unexpected=0` exit 0; (iii) `--selftest` is not `11/11 pass` exit 0; (iv) an
injected stale row (a scratch manifest row carrying the base 19/19 token
against the live 24/24 instrument) is not measured `stale` — the counter is
shown able to fail; (v) any row's instrument exits non-zero at the landed
sweep (an `error` row is never a match); or (vi) the declared population in
`tools/registry-figure-bind.json` is not exactly 7 rows.

## R80-C2 — coverage: the four survivors the round-79 wave named become fixture coverage

**Named survivors (round-79 wave; each measured, none fixed then).**
`ss-bom-strip` (scout `T79W1SC2` S1: the BOM guard deleted, survived 14/14),
`ss-cache-key-drops-argv` (S4: the row cache key loses argv, survived 14/14),
`python-utf8-dropped` (mutation-tester `T79W1M1`: the python tuple loses
`-X utf8`, survived), and `wr-record-unknown-root-check-removed` (S W7: the
`_record_span` unknown-root guard deleted, survived 23/23).

**Before (measured at base `dd2b9e2c`; do-nothing control = the base tool
bytes scored by the new defects).**
`.ufo/evidence/round-80/control/selfstate-freshness-base-r80.py` (sha256
`ca8acdd9fc64…`, 14 arms) + the 3-defect control spec:
`MUTATE: DONE (target=selfstate-control-r80 defects=3 killed=0 survived=3
inconclusive=0 kill-rate=0%)`, `CONTROL: GREEN`, restore byte-identical
(`c2-control-selfstate.txt`). `.ufo/evidence/round-80/control/wave-reconcile-base-r80.py`
(sha256 `d9336fcd8b17…`, 23 arms) + the 1-defect control spec:
`defects=1 killed=0 survived=1`, `CONTROL: GREEN`, byte-identical restore
(`c2-control-wave.txt`). A round that adds no arm cannot reach the after-state.

**After.**
- selfstate arms 15–17 (real CLI against git fixtures): arm15 measures BOTH
  decode refusals (a BOM doc → `bom-present`, a non-UTF-8 doc → `not-utf8`);
  arm16 runs two rows on one path/rev with different argv; arm17 runs an
  instrument that prints `sys.flags.utf8_mode` under an explicit UTF-8 locale.
  `SELFTEST_ARMS` 14 → 17.
- wave-reconcile arm24 refuses a row whose `record.root` is undeclared, by
  name (`unknown-root:`), and fails (not crashes) when the guard is deleted.
  `SELFTEST_ARMS` 23 → 24.
- the two specs carry the new defects (`tools/selfstate-freshness-mutants.spec`
  4 defects, `tools/wave-reconcile-mutants.spec` 13).

**Kill matrix (frozen; measured on the design candidates, pristine 17/17 and
24/24):**

| mutant | dies on |
|---|---|
| `ss-bom-strip` | arm15 only |
| `ss-cache-key-drops-argv` | arm16 only |
| `python-utf8-dropped` | arm17 only |
| `python-isolation-dropped` | arm14 only (unchanged) |
| `record-unknown-root-check-removed` | arm24 only |
| wave-reconcile defects 1–12 | their round-79 arms, unchanged |

**Counting commands (pasteable; after-state at the landing rev):**

```sh
python3 -I -X utf8 tools/selfstate-freshness.py --selftest | tail -1
python3 -I -X utf8 tools/wave-reconcile.py --selftest | tail -1
bash tools/mutate-and-run.sh --target tools/selfstate-freshness.py \
  --defects tools/selfstate-freshness-mutants.spec \
  --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir "$WORK/ss" \
  --label selfstate-arms-r80
bash tools/mutate-and-run.sh --target tools/wave-reconcile.py \
  --defects tools/wave-reconcile-mutants.spec \
  --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir "$WORK/wr" \
  --label wave-reconcile-arms-r80
```

**Kill rule (frozen).** C2 fails if (i) the two control batteries are not
`defects=3 killed=0 survived=3` and `defects=1 killed=0 survived=1` with
`CONTROL: GREEN` and byte-identical restore; (ii) the landed selftests are not
`SELFSTATE_SELFTEST: 17/17 pass` and `WAVE_RECONCILE_SELFTEST: 24/24 pass`,
exit 0; (iii) the landed batteries are not `defects=4 killed=4 survived=0` and
`defects=13 killed=13 survived=0` with `CONTROL: GREEN` and byte-identical
restore; (iv) any defect's FAIL set differs from the frozen matrix; or (v) any
base arm changes its outcome between the base bytes and the landed bytes
(the no-harm monitors below).

## R80-C3 — operability: the receipt population covers the declared tree, design class included

**What the lane could not do (round-79 non-author closure defects 1 and 4).**
The whole-tree sweep read `receipts=22` while the tree carried 29 files with a
complete declared header: seven round-79 design receipts carry
`# design_base:` / `# design_tool:` / `# design_tool_sha256:` /
`# measured_bytes: worktree (uncommitted at design_base)`, and the instrument
recognised only the measured triple, so the class it targets (a sha that
exists in no blob) swept clean by being outside the population.

**Before (measured at base `dd2b9e2c`, base instrument over `.ufo/evidence`).**
`RECEIPT_BIND: receipts=22 bound=14 corrected=8 unbound=0` exit 0, no `design`
field (`c3-before-sweep.txt`, instrument sha256 `8d9f9d76d472…`). The
do-nothing control is this reading: adding no recognition cannot see the seven
design receipts.

**After.**
- `tools/receipt-bytes-bind.py` recognises the design block as its own
  declared class and measures it: `design` when `design_base` resolves,
  `unbound` (`design-base-unresolvable`) when it does not; a design block
  without the uncommitted marker is a setup refusal (`design-marker-absent`),
  a file carrying both blocks is refused (`receipt-header-mixed`), and a
  design tool path outside the repo is refused. `SELFTEST_ARMS` 10 → 13.
- the sweep reports `design=D` in its summary and counts it separately.
- a standing `receipt-bytes-tree` registry row runs the whole-tree sweep.

**Counting commands (pasteable; after-state at the records rev):**

```sh
python3 -I -X utf8 tools/receipt-bytes-bind.py --selftest | tail -1
python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . --root .ufo/evidence | tail -1
```

**Kill rule (frozen).** C3 fails if (i) the base sweep is not
`receipts=22 bound=14 corrected=8 unbound=0` without a `design` field; (ii)
the landed sweep is not `RECEIPT_BIND: receipts=29 bound=14 corrected=8
design=7 unbound=0` exit 0; (iii) `--selftest` is not `13/13 pass` exit 0;
(iv) a design block without the marker is not refused with
`design-marker-absent`; (v) an unresolvable `design_base` is not `unbound`
with `detail=design-base-unresolvable`; or (vi) a mixed measured+design
header is accepted.

## No-harm monitors

- C2: the base and landed selftest arm lines diff to exactly the appended
  arms (selfstate `14a15,16,17`; wave-reconcile `23a24`), every base arm
  outcome identical.
- C3: the measured-block arms 1–10 keep their outcomes (the base selftest is
  re-run on the landed bytes and the ten printed lines diff empty).
- Standing sweeps at the records tip: `WAVE_RECONCILE: rows=6 met=6
  unexpected=0`; `SELFSTATE: rows=23 match=21 stale=2 unexpected=0`
  (the base 22 rows identical plus the new `registry-bind-selftest` row);
  `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 107/107 pass`
  unchanged.

## Sources

C2 opens **S308** (PEP 540, UTF-8 Mode: the `-X utf8` ground for arm17, and
why the arm must pin a UTF-8 locale — the POSIX locale enables the mode). C3
re-opens **S289** (git-cat-file: the `blob <rev>:<path>` binding the measured
block still rests on). The round appends the round-79 routed rejected row
**S309** (`docs.python.org/3/library/sys.html`, refused as the `-I` ground)
with its reason and flip. Snapshots and located quotes land under
`.ufo/evidence/round-80/sources/` and in the round lesson's `## Gate`.

## coldread_forecast (criterion 110/115)

Planned monitored edits: `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`,
`corpus/SOURCES.md`, `SKILL.md`, `tools/registry.json`,
`tools/selfstate-freshness.json`, `tools/selfstate-freshness.py`,
`tools/wave-reconcile.py`, `tools/receipt-bytes-bind.py`,
`tools/registry-figure-bind.py`, `tools/registry-figure-bind.json`.

```
python3 -I -X utf8 tools/rekey-cost.py --edit SCORECARD.md --edit LOG.md \
  --edit corpus/QUALITY.md --edit corpus/SOURCES.md --edit SKILL.md \
  --edit tools/registry.json --edit tools/selfstate-freshness.json \
  --edit tools/selfstate-freshness.py --edit tools/wave-reconcile.py \
  --edit tools/receipt-bytes-bind.py --edit tools/registry-figure-bind.py \
  --edit tools/registry-figure-bind.json
→ REKEY_COST sections=65 planned=12 at_risk=17 predicted_lost=17
```

Receipt `.ufo/evidence/round-80/design/rekey-cost-full-r80.txt`. The forecast's
`predicted_lost=17` is priced into this round: one end-of-round rekey batch
covers the monitor's measured uncredited set at the pre-rekey tip.

## Admission

Every claim is judged on the counter, kill rule and predicate above. A claim
that misses is an honest stop, never a narrowed target. The round is admitted
only if every claim verifies and no axis is harmed.
