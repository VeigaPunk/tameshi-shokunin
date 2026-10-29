# T57W2RepairR553xR554 — repair ledger rows R55.3 and R55.4 (round 57, wave 2, C1 calibration)

Seat: `T57W2RepairR553xR554` (leaf, no subagents). Lane `tameshi-shokunin` at master `06e9849`; base `5e35699`; scratch only, no lane mutation, no git mutation in the lane, no tools installed.

## Outcome

| id | status (kept) | status_at_base (kept) | repair | counter result |
|---|---|---|---|---|
| R55.4 | open | open | REPAIRED: evidence replaced by one admissible committed lane line | no EXPLAIN fault line |
| R55.3 | fixed | fixed | commit provenance corrected `2f5512a8` → `8c20d5c`; evidence kept | **UNREPAIRABLE** under the amended counter: `fixed-not-new` remains |

Plus one loud finding (status is NOT changed, see F1): the calibration monitor reads **6** at lane HEAD `06e9849` (46/64 credited, 18 headings lost), against **8** at base. The defect shape of R55.3 (monitor below the row's 8) is back at HEAD.

## R55.4 — repaired

Old evidence: two `.ufo/waves/round-56/...` paths whose names do not end in a key → `soft-excluded-path` (EXPLAIN lines, both). Not weakened; removed.

New evidence (one item, a committed lane file that is not a spot-check, the ledger, or a round-57 instrument/control/contract/freeze):

- path `.ufo/evidence/round-55/control/controls-a.stdout`, lines `5-6`, excerpt `CTL CTL_SKIP_c2 C2_R55: rev=13bb9e5d92df grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/9 skill=1/1 total=4 C2_R55_PASS=false CONTROLS_A: 5/5 as pre-registered`
- Keys matched as whole tokens: `CTL_SKIP_c2`, `CONTROLS_A`, `controls-a.stdout` (path suffix). `still running` is not in the excerpt; not needed.
- The item's claim is supported: the committed control stdout already reads `CTL_SKIP_c2 … total=4 C2_R55_PASS=false` and `CONTROLS_A: 5/5 as pre-registered`, so "still running at filing" is stale.
- `status` stays `open`; the counter's planned arm passes in the dry run because `dry-c1.sh` appends the open ids of rows 50-100 to a `**Planned (round 58)**` paragraph. The L1 must list R55.4 in the real round-58 Planned paragraph.

Sweep for R55.4 (command, output summarised): `git grep -n -i -E 'CTL_SKIP_c2|CONTROLS_A|controls-a\.stdout|still running' HEAD` — the hit set includes `.ufo/evidence/round-55/control/controls-a.stdout:5` and `:6` (exact lines quoted above), `.ufo/evidence/round-54/control/controls-a.stdout:6` (different round, different verdict), and the round-56 control file. The round-55 file was chosen because it is the one the item cites (`4c04c1d3`, 14:51:26) and is not a frozen spot-check.

## R55.3 — unrepairable as `fixed`

What the existing row got wrong: `commit: 2f5512a8` does not introduce the excerpt. `git show 2f5512a8:SCORECARD.md` does not contain it (checked with whitespace-normalised substring match: `False`); the row text (lowercase `round-21`) is introduced by `8c20d5c` (round-56: correct scorecard evidence predicates): absent at its parent `2f5512a8`, present at `8c20d5c`, touches only `SCORECARD.md`, ancestor of base, not an ancestor of `routed_at` `fa48c06c`. So the commit field is corrected to `8c20d5c`. This does not make the row pass.

Why it still fails: `fixed-not-new` requires either (a) the commit message names `R55.3` (regex `(?<![\w.])R55\.3(?!\d)`), or (b) the evidence path is named in the item text (path or basename substring). Sweep (`.ufo/waves/round-57/w2/T57W2RepairR553xR554-receipts/sweep-R55.3.txt`):

- `2f5512a8`: message names R55.3: 0; touches `SCORECARD.md` and 5 `.ufo/waves/round-56/integration/*` files.
- `8c20d5c`: message names R55.3: 0; touches `SCORECARD.md`.
- History-wide `git log --all --grep` for `R55.3` (whole token): 0 commits.
- Commits in `fa48c06c..HEAD` whose message names R55.3: none.
- Item text (`defects.json` R55.3, `text`; no `extended_text` field): contains neither `SCORECARD.md` nor `SCORECARD`-as-path nor any file basename. Only `SCORECARD` as a word.

No commit exists that satisfies the names-id or item-text arm, and I did not manufacture one (no commit in lane, no weakened key, no path-basename substring trick). Therefore R55.3 is reported `unrepairable` under the amended counter. Route for the L1 (not done here): a post-base round-57 commit that names `R55.3` in its message and itself introduces a new keyed excerpt (the restated calibration row, with the monitor value it reads at its own revision) would satisfy the arm. That is a content decision for the L1, not a repair of this row.

## F1 — finding: calibration monitor regressed at lane HEAD (status not changed)

Command (scratch clones, detached):
`python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev <rev>`

| revision | calibration_restraint_score | sections_covered | box3_full_page | uncovered_headings |
|---|---|---|---|---|
| base `5e35699` | 8 | 64/64 | true | 0 |
| HEAD `06e9849` | **6** | **46/64** | **false** | **18** |

The 18 uncovered headings are the round-56 re-key set (`## Standing rules`, `## Mutation-sweep recipe …`, `## The leg ledger …`, `### Triggers T1–T3 …`, `### The service's limits …`, `## The operator's runbook …`, `### The map …`, `## Repeated controls and gate registry …`, `### Gate/probe registry`, `## Pin disposition …`, `### Round-13 gate/probe registry`, `## Effective expectation reconciliation …`, `## Context gate classification …`, and further). Receipt: `.ufo/waves/round-57/w2/T57W2RepairR553xR554-receipts/cold-read-monitor.txt`.

Cause (observed, not fully traced): `git diff 5e35699 HEAD -- SKILL.md` shows the round-57 C0 content edits (`ca75c26`) to the receipt-revision rows and the `receipt-revision gate` registry row, inside the sections that the round-56 re-key bound. This matches the NO-HARM note (C0 uncredited headings to re-bind in wave 3).

Consequence: `SCORECARD.md:2718` (calibration row, value 8) is false at HEAD: the monitor reads 6. R55.3's `fixed` is proven at base only.

Status decision: I did NOT change `status` for R55.3. The counter forbids `status_at_base == fixed` with `status != fixed` (`base_status_bad`), and base monitor evidence (8/64) proves the base status correct. So flipping `status` would require flipping `status_at_base` too, which is contradicted by the base proof. The HEAD regression must be routed by the L1 as a new item for the wave-3 re-bind, not by editing this row.

## Dry runs (scratch ledger, `dry-c1.sh 80`, `LEDGER=$S/ledger.json`)

Before (L1 `dry-c1-explain.txt`, ledger working tree):

```
EXPLAIN fixed-not-new R55.3
EXPLAIN evidence-bad R55.4 soft-excluded-path .ufo/waves/round-56/w3/T56W3ScribeRecords.md
EXPLAIN evidence-bad R55.4 soft-excluded-path .ufo/waves/round-56/w1/T56W1RevRound55Dispositions.md
C1_R57: self=63a88c257490 rev=629cbec94707 rows=51/51 agree=31/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=21 C1_R57_PASS=false
```

After (patched ledger, my rows):

```
EXPLAIN fixed-not-new R55.1
EXPLAIN fixed-not-new R55.3
EXPLAIN evidence-bad R55.6 soft-excluded-path .ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/base.json
EXPLAIN evidence-bad R55.6 soft-excluded-path .ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/cand.json
EXPLAIN evidence-bad R55.6 soft-excluded-path .ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/rekey.json
EXPLAIN evidence-bad R55.6 soft-excluded-path .ufo/waves/round-55/w2/T55W2ScoutColdread-receipts/inputs.json
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=3 key_miss=8 fixed_bad=8 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=b35edd478eb7 rows=51/51 agree=32/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=20 C1_R57_PASS=false
```

Result: R55.4 no longer in any EXPLAIN line; R55.3 still `fixed-not-new` (unrepairable, above). `agree` 31/51 → 32/51, `total` 21 → 20. Remaining R55.1 / R55.6 / key-miss / panel-pin faults are other items and the pin, not in this seat's scope. `panel_pin=1` is the pending panel pin (`PIN_PENDING…`), unchanged by this seat.

Blind panel: I did not read `.ufo/evidence/round-57/c1/panel.json` (blind arm; reading it would tune `status_at_base`). Nothing here was tuned to it.

## Deliverables

- Rows (full replacement, all fields): `.ufo/waves/round-57/w2/T57W2RepairR553xR554/rows.json` (list of two objects; R55.3 carries the corrected commit and the unrepairable note).
- Machine-readable: `.ufo/waves/round-57/w2/T57W2RepairR553xR554.json`.
- Receipts: `.ufo/waves/round-57/w2/T57W2RepairR553xR554-receipts/` — `dry-run-patched.txt`, `ledger-patched.json` (scratch-patched full ledger, not installed), `cold-read-monitor.txt`, `sweep-R55.3.txt`.
- Lane `corpus/routed-defects.json` untouched by this seat (still the L1's working-tree edit set; `git status` shows only the L1's `M`).

## Commands run (summary)

- `git -C <lane> log/show/grep/diff-tree` over `fa48c06c..HEAD`, `2f5512a8`, `8c20d5c`, `c1dd23b3`, `06e9849`, `ca75c26`, `5e35699`: provenance and sweep (outputs in receipts above).
- `git clone --shared` scratch clones of HEAD and base; `measure.py` of round-21 monitor at base and HEAD (two runs each, JSON captured).
- `patch-ledger.py` → `$S/ledger.json`; `LEDGER=$S/ledger.json bash dry-c1.sh 80`.

## Tooling

None installed or upgraded.

## Checks for the L1

1. Install `rows.json` as the replacement for R55.3 and R55.4 only after deciding R55.3's residual: the counter cannot pass it; the candidate route is a post-base round-57 restatement commit naming `R55.3` (content decision).
2. Route F1 (monitor 6 at HEAD) to wave 3 re-bind (the 18 headings); do not restate the calibration row to 8 at HEAD until the monitor reads 8 at the deciding revision.
3. R55.4 needs a round-58 `**Planned**` line naming it in the real SCORECARD (dry run appends it automatically; the real tree does not).
