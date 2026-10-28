# T56W1RevBaseC1 — independent base cold-read re-derivation (wave 1, milestone: independent base re-derivation)

Seat: `T56W1RevBaseC1` (reviewer). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base: `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`. Floor: `0a2010acd1e92e4e332774050825e21bcfc7e079`.
Item: re-derive the base cold-read state **without** the round-56 counter, re-derive the standing row's
defect at `d33053f7`, and confirm the frozen base receipt reproduces.

Nothing in the lane was edited. Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W1RevBaseC1`.
Machine-readable result: `T56W1RevBaseC1.json`; receipts: `T56W1RevBaseC1-receipts/`.

## 1. Commands actually run (all read-only; no mutating git)

| # | Command | Exit |
|---|---|---|
| A | `python3 .ufo/evidence/round-21/coldread/measure.py --repo <lane> --rev 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 --explain` | 0 |
| B | same as A **without** `--explain` (determinism check) | 0 |
| C | `bash .ufo/evidence/round-48/quality/coldread-precheck.sh <lane> 0a2010acd1e92e4e332774050825e21bcfc7e079 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` | **1** (RED, expected at base) |
| D | `python3 .ufo/evidence/round-21/coldread/measure.py --repo <lane> --rev d33053f7552d --explain` | 0 |
| E | `python3 .ufo/evidence/round-21/coldread/measure.py --repo <lane> --rev 0a2010acd1e92e4e332774050825e21bcfc7e079` | 0 |
| F | `python3 .ufo/evidence/round-56/c1/measure.py --lane <lane> --rev 981c5e8b20a2… --work <empty scratch dir> --explain` (receipt reproduction only) | 1 |
| G | `git -C <lane> rev-parse --verify 0a2010ac…^{commit}`; `git merge-base --is-ancestor d33053f7552d 981c5e8b20a2` | 0 |
| H | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (fleet root) | 0 |

A, C, D, E are the frozen *instruments of record* (round-21 selector, round-48 precheck) — no round-56
counter is involved in any number below except row F, which exists only to diff against the frozen receipt.

## 2. Base state re-derived (independent of the round-56 counter)

Precheck (command C, `receipts/precheck-base.stdout`), final line:

```
COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=981c5e8b20a2 cand_credited=46 lost=18 RED
```

Monitor (command A, `receipts/monitor-base.summary.json`):

- `coldread.sections_covered = 46`, `sections_total = 64` → **credited/total = 46/64**
- `calibration_restraint_score = 6` → **score = 6**
- `coldread.box3_full_page = false` → **box3 = False**
- `shonen = {boxes: 4, marks: ["~","~","~","~"], asserted: 4, checked: 0, untouched: 0,
  box3_marked: true, box3_ledger_link: true, box3_points: false}`
- `sources.rows = 140` (the monitor's own census of `corpus/SOURCES.md`), `depth_score = 10`,
  `recorded_cases = 10`, `ledger_guardrail.lists_agree = true`; `bash scripts/sources-census.sh validate
  --root /home/vgpnk/Projects/shokunin tameshi` exits **0** (W01/W04 advisory lines only)

Determinism (command B): identical — covered 46, score 6, box3 false, 18 uncovered. `--explain` is a
presentation flag, not a measurement input, so the arm-2 number in the frozen receipt is not an
`--explain` artifact.

Floor sanity (command E): `0a2010acd1e9` reads **64/64, score 8, box3 true**, 0 uncovered. So the
precheck's `floor_credited=64` is the monitor's own full-page floor, and base is 18 sections below it.

**Result: base = 46/64 credited, score 6, box3 False, 18 lost headings.** The contract's before-state is
reproduced exactly.

## 3. The 18 lost headings vs the frozen list

`set(monitor.coldread.uncovered_headings) == set(lost-headings-at-base.json)` → **True**
(18 vs 18, `monitor_only = []`, `frozen_only = []`). The **order** differs: the frozen file is sorted,
the monitor reports SKILL.md document order — a list-equality check would report a false mismatch, so
C1's arm must compare as sets (it does: it iterates the frozen list).

The precheck's own 18 `LOST` headings also equal the frozen set exactly (`precheck LOST count 18,
set==frozen True`). All three sources agree.

Per-heading reason strings and drift (derived from the base ledger + base blobs with the round-21
selector's ignore set — `.ufo/evidence/round-21/coldread/ledger.json`, `SKILL.md`, round-17 ledger — and
reconciled **heading by heading** against the monitor's own `reason` field: **18/18 MATCH**):

| # | Heading | SKILL.md lines | section sha256 | ledger entries | reason |
|---|---|---|---|---|---|
| 1 | `## Context gate classification and explicit exit classes — round 15` | 1639–1705 | `132cfb9ef1aa…` | 20 | input-drift: `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/context-capture.py`, `tools/evidence-disposition.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`, `tools/registry.json`, `tools/trace-inputs.py` |
| 2 | `## Effective expectation reconciliation — round 14` | 1593–1626 | `6110606ea4a9…` | 1 | input-drift: `corpus/SOURCES.md`, `tools/context-capture.py` |
| 3 | `## Live-tree re-pin and entry-command monitor — round 17` | 1844–1875 | `6395900104ed…` | 1 | input-drift: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |
| 4 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | 146–260 | `77d88c022646…` | 1 | input-drift: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |
| 5 | `## Pin disposition and provenance correction — round 13` | 1546–1576 | `1fa3130bc6d4…` | 1 | input-drift: `corpus/SOURCES.md` |
| 6 | `## Repeated controls and gate registry — round 12` | 1508–1527 | `3a78cbfcef65…` | 1 | input-drift: `corpus/SOURCES.md`, `tools/repeat-control.py` |
| 7 | `## Standing rules` | 17–44 | `acfb671afd76…` | **0** | **`no-ledger-entry`** (the only non-drift reason) |
| 8 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | 936–949 | `430dd86f25b6…` | 2 | input-drift: `corpus/SOURCES.md` |
| 9 | `## The operator's runbook and the six-leg regression (round 10, measured)` | 1299–1307 | `636e850f885c…` | 2 | input-drift: `tools/registry.json` |
| 10 | `### Gate/probe registry` | 1528–1545 | `99285e24a71a…` | 2 | input-drift: `tools/bash-witness-study.py`, `tools/repeat-control.py` |
| 11 | `### Round-13 gate/probe registry` | 1577–1592 | `896722c49418…` | 2 | input-drift: `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/pin-disposition.py` |
| 12 | `### Round-15 gate/probe registry` | 1706–1736 | `78edbb693cdd…` | 1 | input-drift: `tools/context-capture.py` |
| 13 | `### Round-17 gate/probe registry — re-pin and monitor` | 1876–1884 | `309f83283e75…` | 1 | input-drift: `corpus/SOURCES.md`, `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |
| 14 | `### Round-18 gate/probe registry — routed-defect closure` | 1955–1967 | `661f63518af6…` | 1 | input-drift: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/registry-check.py`, `tools/registry.json` |
| 15 | `### Round-21 gate/probe registry — finite environment differential` | 1994–2133 | `eccd3ec82207…` | 3 | input-drift: `.ufo/evidence/round-15/verify.py`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/env-diff.py`, `tools/registry-check.py`, `tools/registry.json` |
| 16 | `### Round-26 gate/probe registry — report interop` | 2162–2201 | `cc23587b353f…` | 1 | input-drift: `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |
| 17 | `### The service's limits — what tameshi refuses to mutation-test` | 1269–1298 | `7e240e714c6e…` | 1 | input-drift: `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |
| 18 | `### Triggers T1–T3 and the re-pin rule` | 1087–1109 | `2350210704ef…` | 3 | input-drift: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/service-limits.md`, `tools/bash-witness-study.py`, `tools/context-capture.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |

Every heading lives in `SKILL.md` (SKILL.md blob sha256 at base is in `T56W1RevBaseC1.json`; 64 sections
total). Full per-entry detail — each entry's `read_rev`, `traces`, `verdict`, `class`,
`wrong_expectations`, `blocking_gaps`, `commands_executed_count`, every pinned input with its pinned sha
and the base sha it failed against — is in `T56W1RevBaseC1.json` and
`receipts/lost-headings-drift-map.json`.

Drift census across the 18 headings (entry-level counts, from `driftmap.json`):

```
corpus/SOURCES.md 36   tools/registry.json 30   tools/context-capture.py 30
tools/bash-witness-study.py 20   tools/evidence-disposition.py 20   tools/pin-disposition.py 19
tools/mutate-and-run.sh 14   tools/registry-check.py 12   tools/repeat-control.py 11
corpus/QUALITY.md 9   tools/trace-inputs.py 6   tools/env-diff.py 2
corpus/knowledge/service-limits.md 1   .ufo/evidence/round-15/verify.py 1
```

17 of 18 headings (44 ledger entries) fail on `input-drift` — but that is only the **first** failure
`entry_reason` reports. Their verdicts are `gap-minor`/`verified-record` (so no verdict veto) and their
sections still match the ledger by `sha256`; the trace gate was never reached in the monitor's own
reason string. Re-checked directly by calling the frozen `trace_reason()` on all 44 entries:
**44/44 also fail the trace gate**, every one with `trace-input-unrecorded:<p>` (no other trace failure
kind), on 10 distinct paths:

```
.ufo/evidence/round-12/BashWitness/declaration.json 14   .gitignore 13
.ufo/evidence/round-14/context-receipt.json 4   .ufo/evidence/round-13/expected.json 3
.ufo/evidence/round-15/verify.py 3   .ufo/evidence/round-18/final/before.stdout 2
corpus/knowledge/closeout-r11.md 2   .ufo/evidence/round-15/verification-3.json 1
.ufo/evidence/round-12/BashWitness/bash-surface-census.spec 1   .ufo/evidence/round-17/measure.py 1
```

Each of those paths appears in a receipt's `inputs` map but not in the entry's `inputs`, so re-pinning
the entry's inputs at C0 **without** covering them leaves the entry uncreditable (C1's arm 3 requires
`entry_reason(...) is None`). Only `## Standing rules` fails on `no-ledger-entry`: it has **no ledger
entry at all** at base.

## 4. The standing row's defect, re-derived

Row at base `SCORECARD.md:2579` (table headed `### Standing axis table — re-stated at round 54 (base
d33053f7)`), verbatim score cell and commit:

```
| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; 8 is that monitor's
ceiling (two points per restrained, evidence-linked `[~]` box) — at base the **floor** reads 57/64
credited, which is the round-53 honest stop this round repairs | `d33053f7` | 53 |
```

Measured at the commit the row names (command D, `receipts/monitor-d33053f7.summary.json`):

- `calibration_restraint_score = 6` — **the row asserts 8, the monitor reads 6**
- `sections_covered = 57`, `sections_total = 64`, `box3_full_page = false`
- `shonen.marks = ["~","~","~","~"]`, `box3_marked = true`, `box3_ledger_link = true`,
  `box3_points = false`

So the row is wrong on exactly one number and the mechanism is visible: the score formula is
`2·(count of ~ among boxes 1/2/4) + 2·box3_points = 6 + 0`; `box3_points` needs
`box3_full_page`, and 57/64 is not a full page. **8 is unreachable at `d33053f7`.** The row's own
sub-claim — "at base the floor reads 57/64 credited" — is true (measured 57), which is why the defect
survived review: the credited count is honest and only the score cell over-states the monitor.

`d33053f7552db4bd290c99a36979760f544c41ad` resolves and is an ancestor of base (command G). The
row's own last-change cell says round 53. The monitor reaches 8 only at a full page — at the floor
`0a2010ac` (command E: 64/64, score 8, box3 true) and nowhere below it — so the row's `8` is a floor
reading carried onto a 57/64 commit; that the cell was never re-measured at `d33053f7` is
`[INFERENCE]` from the measurement itself (the monitor at that commit reads 6).

## 5. The frozen base receipt reproduces

Command F against an empty work dir produced (verbatim, `receipts/c1-rerun.stdout`):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=981c5e8b20a2 cand_credited=46 lost=18 RED
EXPLAIN arm2-monitor covered=46 score=6 box3=False
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/18
EXPLAIN arm6-restate row_score=8 row_commit=d33053f7552d score_at_row=6 evidence='round-21 cold-read monitor `calibration_restraint_score`; 8 ' round='53'
C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false
```

`diff -u .ufo/evidence/round-56/before/c1.stdout <rerun>` → **empty, exit 0**; both files sha256
`6789d9b004c82ecb8f17536e46bfac2c9c779c8d60e9ebe32ee86c2cb4629b0b`. The output names no work-dir path,
so the diff is byte-identical without any path normalisation. Every arm-1/2/6 number in the receipt is
independently reproduced by commands A/C/D above, and arms 3/4 (no rekey dir, no committed reader
report) follow from `git ls-tree` showing neither at base.

## 6. Findings

**F1 (High — the C0 obligation this seat confirms; instrument-side, not fixable by me).** The standing
calibration row at `SCORECARD.md:2579` states 8 at `d33053f7`, where the frozen round-21 monitor reads 6
(57/64, box3 false). C0 must restate the score to the measured value at the commit the row names.
Mechanism and both readings above (§4). Round 55's R55.3 residue is real and still present at base.

**F2 (High — wave-2 hazard, must be in the L1's C0 plan).** 17 of the 18 lost headings fail on
`input-drift`, and the drifting paths are exactly the files C0 must edit for C2: `corpus/SOURCES.md`
(36 entry-level drifts), `tools/registry.json` (30), `corpus/QUALITY.md` (9),
`corpus/knowledge/service-limits.md` (1). A re-keyed entry that pins the *base* bytes of those files will
be stale at the REV the moment C0 lands. Each re-keyed entry for these 17 headings must pin the **C0**
bytes of `corpus/SOURCES.md`, `corpus/QUALITY.md`, `tools/registry.json`,
`corpus/knowledge/receipt-revision-binding.md` (new), and the other 10 drifting tools, and carry
`read_rev = C0` with `traces` under `rekey-r56-<c0>/`.

**F3 (High — same hazard, one heading).** `## Standing rules` (SKILL.md 17–44, sha
`acfb671afd76…`) has **no ledger entry** at base (`no-ledger-entry`). It is also the one heading whose
text C0 must change, so its section sha256 changes: any entry keyed to the old sha is orphaned by
construction, and the monitor matches entries by section `sha256` only (round-18 `coldread()` `by_sha`).
C0 needs a *new* entry keyed to the post-edit sha, with `read_rev = C0`, `traces` under
`rekey-r56-<c0>/`, `wrong_expectations = 0`, `blocking_gaps = 0`, and a verdict in
`{executed-ok, gap-minor, verified-record}`.

**F4 (High — second-order defect behind the drift; the re-key must cover it).** The 44 entries of the
17 drifted headings fail on `input-drift` only because `entry_reason` returns the **first** failure; the
trace gate is never evaluated in the reported reason. Called directly, `trace_reason()` fails on
**44/44** entries with `trace-input-unrecorded:<p>` (10 distinct paths, §3), i.e. every receipt records
at least one input the entry does not pin. Consequence for wave 2: a re-key that only re-pins the base
drifting paths still leaves all 44 entries uncreditable, and C1's arm 3 (`entry_reason(...) is None`)
stays false. A re-keyed entry's `inputs` must be a **superset** of every key its receipts record (with
equal sha256), or the fresh receipts must record exactly the pinned set. This is latent at base because
input drift masks it — the monitor's reason string cannot distinguish the two.

**F5 (Medium — constraint on the restated row's shape).** The frozen C1 counter's arm 6
(`.ufo/evidence/round-56/c1/measure.py:255-280`) accepts only the **last** 5-cell line whose first cell
is exactly `calibration` and whose second cell is all digits; it then takes the **first resolvable hex
token** in cell 4 as the measured commit and requires `'round-21' in cell 3` and `\b56\b` in cell 5. So
the restated row must: stay a 5-cell `|` row with the axis name bare, put the commit first in the
evidence/measured cell, keep the literal `round-21`, and set the last-change round to `56`. A row that
puts the commit in a different cell, or appends round `56` anywhere else, fails arm 6 for a formatting
reason rather than a measurement one.

**F6 (Low — precision note for C0's wording).** The row's floor observation (57/64 at `d33053f7`) is
true and should survive the restatement; only the score cell and the "8 is that monitor's ceiling"
framing need replacing. Deleting the 57/64 observation would drop the one honest number in the row.

**F7 (Info — set vs list).** `lost-headings-at-base.json` is sorted; `uncovered_headings` is document
order. Set equality holds (18/18), list equality does not. Any consumer comparing lists reports a false
regression; C1's arm 3 iterates the frozen list, which is correct.

## 7. Verification gaps / residual risk

- Not run by me (out of item): the C2 counter, gate fuzz/mutants, controls/deciding/no-harm dry runs,
  the round-56 freeze discipline. Other seats own those. The census was run (command H, exit 0).
- I did not measure the 18 headings at any post-C0 revision — no such revision exists yet; wave 2's
  reader reports and the re-key are the remaining falsifier.
- The monitor's `external_inputs` include live fleet paths outside the lane (`/home/vgpnk/Projects/
  shokunin/*`, `~/.omp/agent/config.yml`, `kimi-shokunin/...`). They are recorded, not verified against
  REV; a change to any of them between PIN and REV does not show up in `sections_covered`. This is a
  pre-existing property of the round-21 selector, unchanged this round, and it is a reason to keep the
  re-key's pinned inputs lane-relative.
- No tool was installed or upgraded for this seat; nothing to record.

## 8. Receipt index

```
receipts/precheck-base.stdout             command C, 18 LOST lines + COLDREAD_PRECHECK line
receipts/monitor-base.summary.json        command A (--explain), trimmed to the measured fields
receipts/monitor-base-noexplain.summary.json  command B (determinism)
receipts/monitor-d33053f7.summary.json    command D (the row's named commit)
receipts/monitor-floor.summary.json       command E (floor 64/64 score 8 box3 true)
receipts/c1-rerun.stdout                  command F, byte-identical to before/c1.stdout
receipts/receipt-diff.txt                 diff + sha256 of both receipts
receipts/lost-headings-drift-map.json     per-heading section sha, pinned inputs, drifted inputs, reasons
receipts/trace-gate-census.txt            frozen trace_reason() over all 44 entries: 44/44 trace-input-unrecorded
receipts/census-validate.stdout           sources-census validate, exit 0 (advisory W01/W04 lines only)
```
