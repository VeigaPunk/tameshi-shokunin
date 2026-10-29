# T57W1ScribeItemsR51x5to8 — ledger rows R51.5-8 (round 57, wave 1)

Scope: triage of the four routed items R51.5-R51.8 of `corpus/lessons/round-51-verifier-spotcheck.md` (`## Routed defects for the lane next round`, items 5-8) against lane base `5e3569969b532310d2b8a3d130901757a3df356b`. Routed-at commit (adds the spot-check): `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`. No lane file was edited. Rows, staged content and receipts are under `.ufo/waves/round-57/w1/T57W1ScribeItemsR51x5to8*`.

## Rows

| id | status | fix class | why |
|---|---|---|---|
| R51.5 kagi cross-domain routing | open | fixable-cheap (report-side) | Only a round-52 seat draft exists; its suggested fix was rejected in review; no fleet report carries the kagi line (rounds 52-56) |
| R51.6 `## Gate` lists rejected candidates | open | fixable-cheap (staged) | `## Gate` (lines 5-12) holds admits and touched rows only |
| R51.7 ledger cell supersession note | fixed | none needed | `bcba892` (round 52) appends the supersession section; ancestor of base, not of `ef19d8e` |
| R51.8 freeze-stamped control receipts | open | fixable-costly | round-56 `deciding-run.sh:99-100` still dates receipts by `git log -1` last-touch; no `FREEZE=` header anywhere |

Row objects (schema exact, plus `keys`, `verdict_basis`, `fix_class`, `fix_note` in `rows.json`):
- R51.7 `commit`: `bcba8924894216268afc4171f06eb8c28e912b46`. Evidence `corpus/knowledge/fleet-kill-rate-ledger.md:439` and `:441`.
- Open rows cite: R51.5 `corpus/knowledge/mutation-case-kagi-drift-pins.md:222`, `:201`, `corpus/lessons/round-52.md:15`; R51.6 `corpus/lessons/round-51.md:7`, `:62`, `:28`; R51.8 `.ufo/evidence/round-56/deciding-run.sh:99-100`, `corpus/lessons/round-51.md:88`.
- Keys per id are in `rows.json`; each id has 4 keys, and each excerpt has a key or the path suffix matches one.

## Verification

- Every excerpt was resolved with the round-50 counter's own functions (`norm`, `show`, `check_evidence`, `measure`, imported unmodified from `.ufo/evidence/round-50/c1/measure.py`, sha256 `ceee320c…ae29`, byte-equal to the lane file). Receipts: `T57W1ScribeItemsR51x5to8-receipts/excerpt-resolution.txt`.
- Fixture ledger runs (scratch clone, four rows, floors zeroed): scenario A (rows as above) gives `total=3`, all `open_unplanned`. The R51.7 fixed row passes. Scenario D (staged patch landed as a fixture commit, R51.6 re-cited to `:14`/`:16`, R51.8 still at `:88`) gives `evidence_bad R51.8`, because the patch moves round-51.md:88 to :93. Scenario D2 (R51.8 re-cited to :93) gives `total=2`, all `open_unplanned`. Scenario E (a newest `**Planned (round 57):**` paragraph naming R51.5, R51.6 and R51.8) gives `total=0` only with an R5x-aware planned regex. Receipts: `measure-scenarios.txt`.

## Counter finding for the L1 (round-57 C1 inherits this)

`.ufo/evidence/round-50/c1/measure.py:111` reads `planned_ids` with `r'\bR4\d\.\d+\b'`. An `open` row for any R5x id therefore counts `open_unplanned` whatever the SCORECARD says. The round-57 counter needs `R[45]\d` (or equivalent) in that regex, and round-57 SCORECARD needs a newest `**Planned (round 57):**` paragraph naming each open id. Without both, R51.5, R51.6 and R51.8 cannot pass as `open`. I did not edit the counter; this is a finding only.

## Staged patch: R51.6 (`fixable-cheap`)

- `stage/corpus/lessons/round-51.md`: the full new file (base bytes + 5 lines after line 12: a `Candidates rejected` block with three bullets). Diff: `R51.6-round-51-candidates.diff-u.patch` (outside `stage/` on purpose, so the copy step does not put a `.patch` into the lane).
- Bullets: (1) hermetic `round21-measure --selftest` not attempted, because the frozen tools-scope amendment does not allow it (C3 section); (2) attempt-2 `SKILL.md` draft discarded (Attempt 3, salvage disposition); (3) attempt-2 probe verdicts superseded, non-deciding (Attempt 3, salvage disposition). Each reason is quoted from the lesson's own text.
- Cold-read: `corpus/lessons/round-51.md` is not an input (`grep -c` on the round-21 ledger = 0 for the exact path). No anchored cite to round-51.md lines exists in the lane (`git grep`). Landing it moves :88 to :93; R51.8's evidence must be re-cited in the same change.
- When landed, R51.6 becomes `fixed` with the landing commit and lines `14-14`, `16-16` (verified in scenario D2 with the fixture commit).

## R51.5 (`fixable-cheap`, report-side)

The lane has no report. The fix is one cross-domain line in the round-57 report (fleet side): kagi `corpus/drift-pins.sh` @ `e64e81b8` (blob `c138d34c…`), `:400` and `:403` unanchored verdict grep, `:158` path-printing DRIFT line, with the knowledge entry as the pointer. The round-52 report is an honest stop with no kagi line, and rounds 53-56 have none either (grep count 0 on each fleet report; existence checked). Do not edit kagi.

## R51.8 (`fixable-costly`)

Fix: bind each control receipt to a `FREEZE=<sha>` header and have the deciding gate check that header. This changes the round-57 controls output, which is a frozen instrument, so it needs a counter amendment and a re-score after the freeze. It also rewrites QUALITY criterion 99 (`corpus/QUALITY.md:1446`), and `corpus/QUALITY.md` is a 71-entry cold-read input. Not done.

## Not verified / limits

- The round-57 counter and its instruments are not in the lane at base; I checked only the round-50 counter's logic, which the round-57 counter inherits.
- No cold-read monitor run: I changed no pinned byte in the lane. The staged R51.6 file is outside the ledger inputs (checked by exact-path grep). The L1 should re-run the monitor when it lands the patch.
- Fleet-side report content is cited only as absence (grep); it is not lane evidence.

## Tools

Nothing installed or upgraded. `git` and `python3` only. No pacman, no uv, no npm.

## Scratch

`$HYAKU_SCRATCH/tameshi-r57/T57W1ScribeItemsR51x5to8` (shared clone, scratch copies) removed after the run.
