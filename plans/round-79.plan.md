# tameshi round 79 — plan (frozen before any wave data)

Lane: tameshi-shokunin. Base: `0cac8e4604e01ff2e2bc0813c745c99d928b5dd5`
(branch `master` = `origin/master`, clean tree — the round-78 non-author
closure verdict commit). Round 79 (attempt 1), hyaku run 15.

Round shape: **one v1 wave, 12 seats** (policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16; attack seats by the policy's
named set = reviewer 2 + critic 1 + mutation-tester 1 = 4 = 33.3 %). `labrat` is
a frozen-topology seat the validator rejects; the canonical §3 planner seat is
held by the L1, and a bounded planning data-walk rides the scout item.

Saturation state at round start (SCORECARD.md): scored axes depth 10,
calibration 8, freshness 9 — all at or above the saturation line 8. Round 78
entered a capability row (`non-Python instrument freshness row`), so the
stagnation window (N = 2) is NOT full and the nudge does not fire: the
lowest-axis obligation binds and **C1 works calibration, the lowest scored
axis (8)**.

Three claims on distinct axes, causally separable: C1 lands only in
`.ufo/evidence/round-78/*` receipts, `tools/receipt-bytes-bind.py` (new) and the
`SCORECARD.md` capability row it demonstrates; C2 lands only inside
`tools/wave-reconcile.py`, `tools/wave-reconcile-mutants.spec` and their
battery receipts; C3 lands only inside `tools/selfstate-freshness.py`,
`tools/selfstate-freshness-mutants.spec` (new) and their battery receipts.
Neither counter executes another claim's instrument: C1's sweep reads receipts
and `git cat-file` blobs (never runs a tool); C2's battery runs the
`wave-reconcile.py` selftest; C3's battery runs the `selfstate-freshness.py`
selftest. Disclosed byte dependency: C1's population includes receipts that
name `tools/wave-reconcile.py` and `tools/selfstate-freshness.py`, so C1 reads
those tools' committed blobs as data.

Design-phase disclosure (pre-data, this plan's own commit): the L1 built all
three candidates and ran their counters before this plan was frozen. The
candidate bytes, the three do-nothing controls, the base-state receipts and the
landed batteries are committed under `.ufo/evidence/round-79/` in the same
commit as this plan (`design/` holds the exact candidate bytes and
`design/SHA256SUMS`). The lane's `tools/` files currently hold the same bytes,
uncommitted until the landing commit; the eight round-78 receipt corrections are
uncommitted until the landing commit too. The predicates below are frozen
against those measurements; the wave's seats re-derive and attack them and
never edit the lane.

## R79-C1 — calibration, capability acquisition: a receipt's recorded tool bytes exist in a revision the receipt names

**What the lane could not do (round-78 closure routed defect 1).** Eight
receipts under `.ufo/evidence/round-78/` record `# measured_rev: 6f532752…` and
a `# tool_sha256:` that does not exist at that revision — the runs graded the
wave-close worktree and the bytes landed at `091d50e4…`. Nothing in the lane
re-derived the pair, so every gate accepted a receipt naming a revision that
does not carry the bytes it certifies (the class criterion 128 names, and the
round-77 §6.1 relapse).

**Before (measured at base `0cac8e46`, candidate instrument over the round-78
receipt population — `--root .ufo/evidence/round-78`, the defect's location, so
the count is stable as later rounds add their own receipts).**
`RECEIPT_BIND: receipts=12 bound=4 corrected=0 unbound=8`, exit 1
(`.ufo/evidence/round-79/c1-base-sweep.txt`); the eight unbound receipts are
exactly `c1-cache-kill`, `c1-landed-selftest`, `c1-landed-sweep`,
`c2-concurrency-prepost`, `c2-landed-battery`, `c2-landed-selftest`,
`standing-sweep-ss-r78`, `standing-sweep-wr-r78`, each `detail=bytes-rev-absent`.
The do-nothing control is the same population with no correction line: it is
this base reading (the cheapest control that skips the claimed work).

**After.**
- `tools/receipt-bytes-bind.py` (new): a declared population — every regular
  file under `--root` carrying exactly one `# measured_rev:`, `# tool:` and
  `# tool_sha256:` header line — measures `bound` (the measured revision's
  committed blob carries the sha), `corrected` (a single append-only
  `# measured_bytes_rev:` names a revision whose blob carries it), or
  `unbound` with a named reason. Exit 0 iff every receipt is bound or
  corrected; setup exit 2 before any row effect on a zero population, a
  duplicate/malformed header, a non-repo root or a non-repo-relative tool path.
- Eight append-only corrections: one `# measured_bytes_rev:
  091d50e47bfea5a38d97671934ae0127ef760edc` line inserted after each receipt's
  `# tool_sha256:` line (the commit that carries the recorded sha; no existing
  byte changes).
- The capability row `receipt-bytes binding sweep` enters `SCORECARD.md`'s
  `## Capabilities` table with the sweep and `10/10` selftest pointers.

**Counting commands (pasteable; after-state at the landing rev):**

```sh
python3 -I -X utf8 tools/receipt-bytes-bind.py --selftest | tail -1
python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . --root .ufo/evidence/round-78 | tail -1
```

**Kill rule (frozen).** C1 fails if (i) the base sweep is not
`receipts=12 bound=4 corrected=0 unbound=8` exit 1 with exactly the eight named
receipts; (ii) the landed sweep is not `receipts=12 bound=4 corrected=8
unbound=0` exit 0; (iii) `--selftest` is not `10/10` exit 0; (iv) any of the
eight receipts changes an existing line between base and landing (the
correction must be one inserted line per receipt, zero deletions, and every
`# tool_sha256:` byte-identical); (v) a correction naming `6f532752…` (the
revision the receipt already names, whose bytes differ) is not `unbound=1` with
`detail=bytes-rev-mismatch` exit 1 (the false-correction control); or (vi) the
capability row does not enter `SCORECARD.md`'s `## Capabilities` table this
round.

## R79-C2 — coverage: the two survivors the round-78 wave named become fixture coverage

**Named survivors (round-78 wave, `corpus/lessons/round-78.md` §Wave findings).**
`w1-leak-scan-empty` — the leftover detector always reports clean
(`return set()`/`None`), surviving 21/21 because a healthy cleanup never leaks,
so no arm ever measured the detector's live branch; `w2-head-guard-removed` —
the pinned fixture's `HEAD != rev` precondition deleted, surviving 21/21
because no arm reached the guard, so a degenerate fixture would be measured
silently.

**Before (measured at base `0cac8e46`).** `WAVE_RECONCILE_SELFTEST: 21/21
pass` exit 0 on the base bytes
(`.ufo/evidence/round-79/c2-base-selftest.txt`). The do-nothing control is the
LANDED tool with the two new arm registrations removed (suite 21/21) scored by
the frozen 12-defect spec: `MUTATE: DONE (target=wave-reconcile-control-r79
defects=12 killed=10 survived=2 inconclusive=0 kill-rate=83%)`, the two
survivors exactly `leak-detector-blind` and `head-guard-removed`, `CONTROL:
GREEN`, restore byte-identical (`sha256 25df7bd78eae…`)
(`.ufo/evidence/round-79/c2-control-battery.txt`, control bytes
`.ufo/evidence/round-79/control/wave-reconcile-no-new-arms.py`). A round that
adds the fixtures without the two arms cannot reach the after-state.

**After.**
- The leftover post-condition is extracted to the module-level `_leftover(path)`
  (`1` when the fixture path exists, else `None`) and arm22 measures BOTH
  branches: a live fixture path must report `1`, the same path after removal
  must report `None`. The arm20/arm21 post-conditions call it.
- The fixture builder is extracted to `_build_listing_fixture(fix, mode,
  second_commit=True)`; the pinned mode refuses a degenerate `HEAD == rev`
  fixture (`git-fixture-head-equals-rev`), and arm23 builds that degenerate
  fixture ON PURPOSE (`second_commit=False`) and measures the refusal.
- `SELFTEST_ARMS` 21 → 23; `tools/wave-reconcile-mutants.spec` 10 → 12 defects
  (the `arm20-cleanup-removed` anchor gains the arm20 cleanup comment line so
  it stays unique after the refactor; the edit it performs is unchanged).

**Kill matrix (frozen; measured on the design-phase candidate, pristine 23/23):**

| mutant | dies on |
|---|---|
| `m2-delimited-tautology` | arm13 + arm16 (unchanged) |
| `span-rule-removed` | arm14 + arm17 + arm18 (unchanged) |
| `seat-reports-any-depth` | arm15 + arm20 (unchanged) |
| `mc-record-bound` | arm16 (unchanged) |
| `roles-bypass` | arm17 (unchanged) |
| `attack-bypass` | arm18 (unchanged) |
| `adv-seatreports-require-printed-bypass` | arm19 only (unchanged) |
| `git-listing-recursion-removed` | arm20 + arm21 (unchanged) |
| `git-listing-uses-head` | arm21 only (unchanged) |
| `arm20-cleanup-removed` | arm20 only (unchanged) |
| `leak-detector-blind` | **arm22 only** (new) |
| `head-guard-removed` | **arm23 only** (new) |

**Counting commands (pasteable; after-state at the landing rev):**

```sh
python3 -I -X utf8 tools/wave-reconcile.py --selftest | tail -1
bash tools/mutate-and-run.sh --target tools/wave-reconcile.py \
  --defects tools/wave-reconcile-mutants.spec \
  --suite 'python3 -I -X utf8 "$MUTANT" --selftest' \
  --workdir "$HYAKU_SCRATCH/tameshi-r79/l1/battery" --label wave-reconcile-arms-r79
```

**Kill rule (frozen).** C2 fails if (i) the do-nothing control is not
`defects=12 killed=10 survived=2` with exactly those two survivors and
`CONTROL: GREEN`; (ii) the landed selftest is not `23/23` exit 0; (iii) the
landed battery is not `defects=12 killed=12 survived=0` with `CONTROL: GREEN`
and byte-identical restore; (iv) any defect's kill set differs from the frozen
matrix; (v) any base arm 1–21 changes its outcome between base bytes and landed
bytes (the no-harm monitor below); or (vi) the first ten defects' kill sets
change at all.

## R79-C3 — operability: the selfstate runner's `-I` is load-bearing

**Named survivor (round-78 wave).** `s3-python-isolation-dropped` — a python
tuple without `-I` survived 13/13 (`T78W1M1`): no fixture distinguished
isolated mode, so every python-defaulted row could silently run without it.

**Before (measured at base `0cac8e46`).** `SELFSTATE_SELFTEST: 13/13 pass`
exit 0 (`c3-base-selftest.txt`). The do-nothing control is the BASE tool bytes
scored by the frozen one-defect spec: `MUTATE: DONE
(target=selfstate-control-r79 defects=1 killed=0 survived=1 inconclusive=0
kill-rate=0%)`, survivor `python-isolation-dropped`, `CONTROL: GREEN`, restore
byte-identical (`sha256 7edecba8b9c6…`)
(`.ufo/evidence/round-79/c3-control-battery.txt`).

**After.**
- arm14 (`ARM14_python_isolation_tuple`) runs the real CLI against a git
  fixture whose python instrument prints `TOY_ISO: 1/1 pass` iff
  `sys.flags.isolated` and `TOY_ISO: 0/1 pass` otherwise; the row's doc figure
  is `1/1`, so the frozen `('python3', '-I', '-X', 'utf8')` tuple measures
  `match` and a tuple without `-I` measures `stale` (arm FAIL).
- `SELFTEST_ARMS` 13 → 14; `tools/selfstate-freshness-mutants.spec` (new, one
  defect) is the standing battery for the isolation mutant.

**Counting commands (pasteable; after-state at the landing rev):**

```sh
python3 -I -X utf8 tools/selfstate-freshness.py --selftest | tail -1
bash tools/mutate-and-run.sh --target tools/selfstate-freshness.py \
  --defects tools/selfstate-freshness-mutants.spec \
  --suite 'python3 -I -X utf8 "$MUTANT" --selftest' \
  --workdir "$HYAKU_SCRATCH/tameshi-r79/l1/battery-ss" --label selfstate-arms-r79
```

**Kill rule (frozen).** C3 fails if (i) the base control is not
`defects=1 killed=0 survived=1` with `CONTROL: GREEN`; (ii) the landed selftest
is not `14/14` exit 0; (iii) the landed battery is not `defects=1 killed=1
survived=0` with byte-identical restore; (iv) the mutant's FAIL set is not
exactly arm14; or (v) any base arm 1–13 changes its outcome between base and
landed bytes.

## No-harm monitors

- C2: `diff` of the `SELFTEST arm1…arm21` lines between `c2-base-selftest.txt`
  and `c2-landed-selftest.txt` → empty.
- C3: `diff` of the `SELFTEST_ARM1…ARM13` lines between `c3-base-selftest.txt`
  and `c3-landed-selftest.txt` → empty.
- Standing sweeps at the landing tip: `WAVE_RECONCILE: rows=6 met=6
  unexpected=0` unchanged; `SELFSTATE: rows=22 match=20 stale=2 unexpected=0`
  (base 21 rows identical; one new row `receipt-bind-selftest` for the C1
  capability figure, added after the landing commit and pinned at it).
- `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 107/107 pass`
  before and after (the runner is unchanged).
- No other tool's counter is read by any claim.

## Sources

C1 re-opens **S289** (git-cat-file documentation, the `blob <rev>:<path>`
binding); C2 re-opens **S305** (git-ls-tree, the `-r` recursion ground); C3
opens **S307** (Python 3.15 `using/cmdline.html`, the `-I` isolated-mode
ground). All three snapshots and their located quotes land under
`.ufo/evidence/round-79/sources/` and in the round lesson's `## Gate`.

## coldread_forecast (criterion 110/115)

Planned monitored edits: `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`,
`corpus/SOURCES.md`, `tools/wave-reconcile.py`,
`tools/wave-reconcile-mutants.spec`, `tools/selfstate-freshness.py`,
`tools/receipt-bytes-bind.py`, `tools/selfstate-freshness.json`. Measured
pre-data with the lane's own forecast instrument:

```
python3 -I -X utf8 tools/rekey-cost.py --edit SCORECARD.md --edit LOG.md \
  --edit corpus/QUALITY.md --edit corpus/SOURCES.md \
  --edit tools/wave-reconcile.py --edit tools/wave-reconcile-mutants.spec \
  --edit tools/selfstate-freshness.py --edit tools/receipt-bytes-bind.py \
  --edit tools/selfstate-freshness.json
→ REKEY_COST sections=65 planned=9 at_risk=14 predicted_lost=14
```

Receipt `.ufo/evidence/round-79/rekey-cost-full-r79.txt`. The forecast's
`predicted_lost=14` is priced into this round: one end-of-round rekey batch
covers the monitor's measured uncredited set at the pre-rekey tip.

## Admission

Every claim is judged on the counter, kill rule and predicate above. A claim
that misses is an honest stop, never a narrowed target. The round is admitted
only if every claim verifies and no axis is harmed.
