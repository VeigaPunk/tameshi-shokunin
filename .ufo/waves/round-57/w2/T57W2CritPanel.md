# T57W2CritPanel — attack on the blind-panel arm (C1, calibration)

Seat: critic (leaf, read-only, no edits). Scope: the amended counter's panel code (`.ufo/evidence/round-57/c1/measure.py` L359-373, constants L70-75, cli L402-411), the contract's C1 text, LEARNING.md, and the wave-1 triage rows. I did not read `T57W2Panel*`. Receipts: `T57W2CritPanel-receipts/` (sweep-commands.txt lists every command).

## Verdict

The panel arm does not show what the contract needs it to show. It compares one self-reported ledger field (`status_at_base`) with a panel file that sits in the same tree, and it forgives 5 disagreements. Four concrete consequences, each reproduced:

1. **A ledger can pass by copying the panel.** Every row whose `status_at_base` git does not force (24 of 51 triaged rows: 22 open, 2 declined, plus any post-base fix) is free to take whatever value the panel file shows. Nothing orders the ledger commit before the panel commit.
2. **The allowance forgives exactly the under-claims it should catch.** Relabelling five pre-base fixes to `open` (planned) against a truthful panel gives `panel_disagree=5, panel_over=0`: the arm passes. Relabelling all 27 pre-base fixes against an all-open panel gives `panel_over=0` (only the 2 declined rows disagree).
3. **The arm is the only check on under-claims and it is blind to them below the allowance.** The `open` rule (L274) requires only that the id appears in the newest Planned paragraph plus keyed evidence that resolves at REV. An item fixed at base passes that rule.
4. **The amended counter is not selftest-clean and the panel arm has no selftest case.** As shipped, `--selftest` prints `C1_R57_SELFTEST: 11/45 pass`; no selftest case sets `panel_pin` (grep finds no `panel` after the selftest start at L447), and `PANEL_SHA256` is still `PIN_PENDING_SET_BY_L1_AFTER_THE_BLIND_PANEL`.

Recommendation: do not let `panel_allowed=5` stand. See "Proposed changes" and "cannot_see wording".

## What the arm actually checks (code facts)

- L369: `dis = [id for each defect if ledger_row.status_at_base != verdicts[id]]`; L370: `panel_over = max(0, len(dis) - 5)`.
- `status_at_base` is checked only for: membership in {fixed, open, declined} (L206-209); "may not be `fixed` when status is not `fixed`" (L209); and, for status `fixed` only, `(sab == 'fixed') == is_ancestor(commit, BASE)` (L238, `fixed_bad`).
- Consequence: for every pre-base fix the value is forced by git (`fixed` iff the commit is an ancestor of BASE). For `open` and `declined` rows, and for post-base fixes, `status_at_base` may be `open` or `declined` with no check against the tree.
- The panel arm never reads the REV `status` field. A row's REV status rests on the mechanical arms only (keyed excerpt resolves at REV, fixed commit touches a keyed path with the excerpt new at routing, `open` id in the planned paragraph, declined reason >= 40 chars).
- `cli()` defaults `panel_pin` to the placeholder (L411), so every `cli` selftest case also depends on a panel file that the fixture never writes.

## Triage facts that bound every panel answer (wave-1 rows, read-only)

- 51 rows: 27 `fixed`, 22 `open`, 2 `declined` (R54.4, R55.7). All 27 fix commits are ancestors of BASE `5e35699` (checked with `git merge-base --is-ancestor`).
- So the wave-1 triage implies `status_at_base` = `fixed` for 27 (forced by git), `open` for 22, `declined` for 2 (free between open/declined only in the arm's eyes).
- Post-base fixes in the triage: **0**. The contract's this-round floor is 6 (`thisround_short=6` on the triage as it stands). Every panel scenario below therefore tests only the 27 forced rows and the 24 free rows.
- C0 (`ca75c26`) changed 6 of the 56 distinct triage evidence paths (`SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/receipt-revision-binding.md`, `tools/registry.json`). A panel that reads the working tree instead of a BASE clone would read C0's edits as "at base".
- Item texts carry routing-time status words in 16 of 51 items (e.g. R50.3 "still read `open`"; R50.4 "Carried (lane-acknowledged)"; R55.3 "still says 8"). The panel is therefore not blind to the lane's own status claims unless its prompt says so.

## Scenario sweep (counter arithmetic, run in a scratch clone at BASE)

Method: `drive.py` / `variants2.py` build a scratch clone at BASE, commit `corpus/routed-defects.json` (49 base rows + the new rows), the frozen `defects.json`, a Planned paragraph for round 58 naming every open id, and a `panel.json`, then call `measure()` from the lane's file with `panel_pin` = sha256 of that panel and `panel_allowed=5`, `this_round_floor=0` (the this-round arm is reported separately). Non-panel faults are the row faults of the honest triage ledger under the amended counter (evidence_bad 5, key_miss 10, fixed_bad 8).

| ledger | panel | panel disagreements | panel_over | arm result | non-panel faults |
|---|---|---|---|---|---|
| honest (= triage at base) | truth (= ancestry) | 0 | 0 | pass | 23 |
| honest | answers like wave-1 triage (REV status) | 0 | 0 | pass | 23 |
| honest | all `open` | 29 | 24 | **fail** | 23 |
| honest | all `fixed` | 24 | 19 | **fail** | 23 |
| relabel 5 pre-base fixes to open, planned | truth | 5 | 0 | **pass** | 23 |
| relabel all 27 pre-base fixes to open, planned | truth | 27 | 22 | fail | 15 |
| relabel all 27 pre-base fixes to open, planned | all `open` | 2 | 0 | **pass** | 15 |
| relabel all 51 to open, planned | all `open` | 0 | 0 | **pass** | 15 |
| relabel the 8 rows fixed-not-new to open | truth | 8 | 3 | fail | 15 |
| relabel 5 of those 8 to open | truth | 5 | 0 | **pass** | 18 (fixed_bad 8 -> 3) |
| relabel the 8 to open | all `open` | 21 | 16 | fail | 15 |

Reading the table:
- Against a truthful panel the arm bites only when more than 5 rows are relabelled. Five hidden under-claims pass, and relabelling the rows the `fixed` rule rejects (`fixed-not-new`: R51.3, R53.6, R53.7, R54.7, R54.9, R54.10, R55.1, R55.3) clears `fixed_bad` from 8 to 3 while the open rule accepts them. The incentive is real: an `open` row escapes the fixed-rule checks.
- Against an all-open panel, the lane passes by relabelling its fixes to open. The remaining non-panel faults (15: evidence_bad 5, key_miss 10) are triage defects that wave-2 repair can clear. An all-open panel plus all-open ledger reaches `panel_over=0` with zero disagreements.
- The 5 is exactly the number of under-claims that pass: it equals the relabel-5 case and the fixed-not-new-5 case.

Post-base fixes (arithmetic from L369-370, not run): with an honest ledger (status_at_base `open` for a post-base fix) and a panel that answers REV status, each post-base fix is one disagreement. The this-round floor is 6. A panel wrong on 5 of 6 floor fixes passes the arm. The arm cannot tell a panel that reads BASE from one that reads REV on the very rows the this-round floor counts.

## Q1. Is the panel independent?

No, not in the sense the lane needs. LEARNING.md (L45-46): "A subagent the lane dispatched is still the lane." PROTOCOL.md § Promotion gates says the same. Dispatched panel seats buy:
- fresh context (they can be kept from the ledger rows and triage `verdict_basis`, if the prompt says so);
- decorrelated reading errors, if they run on a clone at BASE, not on the working tree (6 of 56 triage evidence paths changed at C0).

They do not buy an outside check, a discernment result, or an answer about REV. The panel is a second lane reading of BASE.

## Q2. Can a ledger author pass by copying the panel after it is committed?

Yes, for every row whose `status_at_base` git does not force. The panel file is pinned, but the pin fixes the panel's bytes, not the ledger's dependence on them. The counter reads the ledger and the panel both at REV, and nothing requires the ledger's `status_at_base` to be committed before the panel. L1 authors both `panel.json` and the ledger, so the pin is a hash of the L1's own copy. For the 27 forced rows, copying buys nothing (the value is git-forced). For the 24 free rows it buys full agreement at zero cost.

Required to stop it: commit order. The ledger's `status_at_base` values must be committed at commit A; the panel must be produced from a BASE clone with no ledger visibility and committed at P, with A an ancestor of P and P touching only the panel file; the counter must require ledger `status_at_base` at REV to equal its value at A.

## Q3. What extra evidence shows `status` rests on the tree, not the panel?

The panel shows neither. Needed, per status:
- `fixed`: already mechanical (excerpt new at routing, touched by the commit, and absent at the first parent). Semantic support is not checked (the contract says so).
- `open`: a REV witness that the routed defect still stands. Today the keyed evidence only has to resolve at REV and carry a key. The `open` rule accepts evidence that shows the fixed state (e.g. a keyed `mined` row). Candidate witness: a literal from the item's own text that the open evidence must reproduce at REV (45 of 51 item texts carry a backticked literal; not verified that each literal discriminates).
- `declined`: a reason of 40 characters is the only check. Declined rows need either a pre-registered decision commit or a witness; neither exists. R54.4 and R55.7 have no commit.

## Q4. Is `panel_allowed=5` (about 10 percent of 51) defensible?

No. It is a constant without a calibration. The panel's error rate on semantic base-state questions is not measured (no known-answer control), and the table shows 5 is exactly the number of hidden under-claims the arm forgives. The allowance also exceeds the this-round margin (floor 6, so a panel wrong on 5 floor rows passes). A defensible value is 0 for every row the counter credits (post-base fixes, and any row whose status changes between BASE and REV); forced rows need no panel. For the remaining free rows, report the disagreement count as a measurement, not a pass/fail gate, until a known-answer control gives a rate.

## Q5. Panels that guess, or that copy the wave-1 triage

- All `open`: fails on the 27 forced rows (panel_over 24 on the honest ledger). It passes only with a ledger that relabels its fixes (table row 7), which is the attack.
- All `fixed`: fails (panel_over 19). It also cannot pass any ledger that is honest about post-base fixes.
- Wave-1 triage answers (REV status): 0 disagreements today, because the triage has no post-base fixes. The arm therefore scores a copied triage as perfectly as a blind re-derivation. The score is uninformative on this data.

## Other defects found while attacking the panel (for the L1)

- **Selftest 11/45 as shipped** (`selftest.stdout`). Causes I checked: the good fixture rows lack `status_at_base` (now `base_status_bad`), and the fixed-rule fixture commit message does not name R50.1 while the defect has no `text` (`fixed-not-new`). With `status_at_base` added and R50.1 set base-consistent, selftest is 29/45 (`selftest_patched2.stdout`; the patched copy is `measure-selftest-patched-for-diagnosis.py`). The amendment that introduced the panel arm and the whole-token key rule was not re-run through the selftest. The wave-1 45/45 receipt predates the amendment.
- **No panel selftest case.** The arm is live only if the L1 pins it correctly; nothing in the counter tests it.
- **Contract stale.** `contract.json` has no `amendments` key, but measure.py says the floors were replaced by "contract amendments[0]". The C1 target text still says "fixed >= 20, declined <= 14". The counter says `FIXED_FLOOR=0`, `DECLINED_CAP=999`. The kill_rule says floors are not lowered after scoring; the amendment should be recorded in the contract before scoring is cited.
- **This-round floor unmet by triage.** 0 post-base fixes against a floor of 6.

## Proposed changes (for the L1; not applied, I edit nothing)

1. Commit order: ledger `status_at_base` at commit A; panel produced from a BASE clone with no ledger visibility, committed at P, A an ancestor of P; counter requires REV ledger `status_at_base` == value at A.
2. Drop the 5-allowance. Panel allowance 0 for post-base-fix rows; forced rows take no panel input; free rows report the disagreement count without a pass gate until a known-answer control measures the panel.
3. Panel input: a BASE clone (verified with `rev-parse`), item id, file list and frozen text; state in the prompt that status words in the text describe routing time.
4. `open` witness: a REV-side literal from the item text, reproduced in the cited lines.
5. Add panel selftest cases: a panel that matches passes, a panel one off fails at allowance 0, a ledger whose `status_at_base` disagrees with the panel at P fails, and a ledger committed after P is refused.
6. Record the floor amendment in `contract.json` before scoring.

## Proposed exact wording for the contract's C1 `cannot_see`

Replace the existing panel sentence with:

"the blind panel shows only that the ledger's `status_at_base` field agrees with the panel's verdicts at the panel commit, for the seats' readings of a BASE clone. It does not show that any status is right: (i) the panel is lane-dispatched (LEARNING.md: a subagent the lane dispatched is still the lane), so it is a second lane reading, not an outside or discernment check; (ii) `status_at_base` is a self-report, forced by commit ancestry only for pre-base fixes; for open and declined rows and for post-base fixes the counter does not check it against the tree, so agreement there shows the ledger matches the panel, not the tree; (iii) the panel's error rate on semantic base-state questions is unmeasured (no known-answer control), so the allowance is a constant, not a calibration; (iv) the panel never reads the REV status: a row's REV status rests only on the mechanical arms (keyed excerpt presence, commit ancestry, planned id, reason length), and an under-claimed fix (status `open` for an item fixed at base) is detected by the panel alone, and is forgiven up to the allowance; (v) the item text carries routing-time status words in 16 of 51 items, so the panel is not blind to the lane's own claims unless its prompt says otherwise."

## Commands run (sweep; full list in `T57W2CritPanel-receipts/sweep-commands.txt`)

- `python3 .ufo/evidence/round-57/c1/measure.py --selftest --work $S/w` -> `C1_R57_SELFTEST: 11/45 pass` (selftest.stdout).
- Patched diagnosis copy: `status_at_base` added to fixture rows, selftest -> `29/45` (selftest_patched2.stdout).
- `drive.py` (scratch clone at BASE, 10 variants) -> drive.stdout; `variants2.py` -> variants2.stdout; `faults.py` (per-row faults of the honest triage) -> faults.stdout.
- `git -C <lane> diff --name-only 5e356996 ca75c267` (c0_changed.txt); `git merge-base --is-ancestor` for the 27 fix commits (read-only).
- Greps: `panel` in measure.py (L359-411, none at or after L447); `status_at_base` checks L206-238; `open-unplanned` L274; contract `amendments` key absent.

## Tools

No tools installed or upgraded. Python 3 standard library only. Scratch under `$HYAKU_SCRATCH/tameshi-r57/T57W2CritPanel`, removed on exit; the lane and fleet repo were not mutated (only read-only git and one scratch clone).
