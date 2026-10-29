# T57W1ScribeQuality — QUALITY criteria draft (round 57, wave 1)

Lane base `5e3569969b532310d2b8a3d130901757a3df356b`. Item: draft up to three append-only `corpus/QUALITY.md` criteria, each with its lesson and a falsifier. Staged only; no lane file edited.

## Deliverables

- Staged diff: `.ufo/waves/round-57/w1/T57W1ScribeQuality/stage/corpus/QUALITY.diff` (`diff -u` against base bytes; 32 lines; appends one header and criteria 108–110 after line 1705; `git apply --check -R` passes against the candidate).
- Receipts: `.ufo/waves/round-57/w1/T57W1ScribeQuality-receipts/` (listed in §4).
- Machine-readable: `.ufo/waves/round-57/w1/T57W1ScribeQuality.json`.

Numbering: the base maximum is criterion 107 (last `### Criterion` heading in `corpus/QUALITY.md` at base is `### Criterion 107`), so the drafts are 108, 109, 110 under `## Criteria appended — round 57 (2026-10-28)`.

## 1. The three criteria

| # | Title (short) | Axis it protects | Lesson / motivation | Falsifier (run at base unless stated) |
|---|---|---|---|---|
| 108 | Every routed item of a closure has one ledger row in the next round; a row's past-tense receipt resolves | calibration | `corpus/lessons/round-56-verifier-spotcheck.md` §6; `considerthese/2026-10-28.md` proposal 1 | Ledger parsed at base: `rows 49 rows_r50_56 0`; `git ls-tree --name-only BASE .ufo/evidence/round-53/after/` prints nothing, while SCORECARD and LOG cite that path |
| 109 | A gate with a selftest has an executed `kind: gate` registry row that pins its exit map | operability | round-56 closure §1 D-CF3 and §6 R56.6 | Registry parsed at base: `gate-rows-naming-gate 0`; the only row naming `tools/receipt-revision-gate.py` is `receipt-revision-gate-selftest` (kind `selftest`, `expect.exit` 0, 19/19 line and eleven CASE lines, no exit 2/3 class) |
| 110 | A planned edit to a monitored file is priced in cold-read credit before the first content edit; a miss is named | calibration | `corpus/lessons/round-52-verifier-spotcheck.md` (rejected-harmed, credited 64 → 45, 19 lost); `considerthese/2026-10-28.md` proposal 3 | Round-52 contract top-level keys have no `coldread_forecast` (`False`); its `coldread_note` prices three sections and says the SKILL.md edits "drop the sections they touch" with no count; the two-line QUALITY append measured `lost=6` |

Overlap, stated so the L1 can weigh it:
- 108 vs criterion 97: 97 checks pointers in SCORECARD, LOG, QUALITY and lesson blocks. The ledger is not in that list, so 108 adds it. 108 also adds the within-one-round coverage rule, which 97 does not state.
- 110 vs criterion 98: 98 prechecks the content revision after drafting. 110 adds the forecast before the first content edit and the named-miss rule. The falsifier uses 98's script unchanged.
- 109 vs criteria 103 and 107: 103 binds a tool's output to its row and SKILL statements; 107 binds a receipt's `rev=`. Neither pins a gate's exit map to an executed row, which is what R56.6 asked for.

What the criteria do not claim: they are text. No counter in this wave is scored against them. The round-57 C1 and C2 counters are other seats' work.

## 2. Measured evidence

### 2a. Cold-read drop of the drafted diff (no-harm, the item's central cost)

Measured with the frozen monitor path `.ufo/evidence/round-48/quality/coldread-precheck.sh LANE BASE CAND` in a scratch clone (`git clone --shared`, detached at base; candidate = base plus the staged block, committed with fixture identity in the scratch clone only).

- Floor (base `5e356996`): `floor_credited=64`, score 8 at base (`coldread-base-5e356996.json`, `calibration_restraint_score: 8`, 64 of 64 sections credited).
- Candidate `36a4dff3`: `COLDREAD_PRECHECK floor=5e3569969b53 floor_credited=64 cand=36a4dff3c603 cand_credited=58 lost=6 RED`, exit 1 (`precheck-stage-diff.txt`).
- The six lost headings: `## Live-tree re-pin and entry-command monitor — round 17`; `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`; `## Standing rules`; `### Round-18 gate/probe registry — routed-defect closure`; `### Round-21 gate/probe registry — finite environment differential`; `### Triggers T1–T3 and the re-pin rule`.
- Sensitivity check: a two-line append to QUALITY alone (candidate `d584b9e5`, scratch) also gives `cand_credited=58 lost=6 RED` with the same six headings (`precheck-quality-2line.txt`). The loss therefore follows the pinned file being edited, not the number of lines added. This is the datum criterion 110 asks a forecast to state.

Consequence for the L1: the staged diff, as it stands, makes 64 → 58. The six headings must be re-keyed with fresh readers at the content-final commit C0, as the round contract's `no_harm` already plans. I did not reduce the criteria to avoid this cost; the cost is the item's measured outcome.

### 2b. Base facts behind the criteria (each re-derived this round)

- Ledger at base: `rows 49`, ids `R40`–`R49` only, `rows_r50_56 0`.
- `.ufo/evidence/round-53/after/` at base: `git ls-tree --name-only` prints nothing (`exit=0`). `LOG.md:2490`, `SCORECARD.md:2507, 2526, 2543` and `corpus/lessons/round-53-verifier-spotcheck.md:28, 79` cite it.
- Registry at base: 57 rows, kinds `selftest` 31, `gate` 22, `probe` 4. Gate-kind rows naming `receipt-revision-gate.py`: 0. The only row naming the gate is `receipt-revision-gate-selftest`, `expect.exit` 0.
- Round-52 contract (`.ufo/evidence/round-52/contract.json`) top-level keys: `schema, round, lane, l1, date, base, axes_at_base, claims, separability, no_harm, controls, deciding, frontier_step, amendments`. No `coldread_forecast`.
- Round-52 closure (`corpus/lessons/round-52-verifier-spotcheck.md`, verdict line): `rejected-harmed`; `COLDREAD_PRECHECK ... cand_credited=45 lost=19 RED`.
- Round-57 contract (lane working tree; absent at base): its keys do not include a `coldread_forecast`. Criterion 110 therefore applies to round 57 only if the L1 adds that key before the first content edit. That is a requirement on the L1, not a claim that round 57 meets 110.

## 3. Checks not run

- No counter was run against the criteria; they are drafts. Their falsifiers were run as stated in §2b.
- The `round-57/c1` and `round-57/c2` counters were not run (not my item; not in my stage).
- `scripts/sources-census.sh` and the registry check were not run (no SOURCES, registry or tool bytes changed by this seat).
- Lesson pointers: criterion 110 cites a lesson at base, not `corpus/lessons/round-57.md`. Criteria 108 and 109 cite round-56 lesson sections that exist at base. None of my criteria cites a round-57 lesson heading that does not yet exist.

## 4. Receipts (`.ufo/waves/round-57/w1/T57W1ScribeQuality-receipts/`)

- `falsifiers-108-110.txt`: the exact base-side commands for 108 and 109, the round-52 contract keys check, with their output.
- `round53-after-citations.txt`: `git grep` of `round-53/after` at base (SCORECARD, LOG, round-53 spot-check) and the empty `ls-tree`.
- `coldread-base-5e356996.json`: monitor output at base (score 8, 64/64 credited).
- `precheck-stage-diff.txt`: precheck of the staged diff (`lost=6 RED`).
- `precheck-quality-2line.txt`: precheck of the two-line QUALITY append (`lost=6 RED`).

Criteria 108 and 110 cite receipt paths under this directory. For criterion 97 to hold at the landing tip, the L1 must commit these five files with the QUALITY block. Until they are committed, the citations are pending (the same situation criterion 107's erratum describes).

## 5. Tools

No tool was installed or upgraded. Every command used the existing `python3`, `git` and the lane's own `coldread-precheck.sh`.

## 6. Handoff to L1

1. Copy `stage/corpus/QUALITY.diff` into the lane with `patch -p1` (or equivalent) at the content-final commit, and commit the receipts with it.
2. Re-run `coldread-precheck.sh` at the final commit; the expected result is the measured `lost=6` unless other staged content changes the set. Re-key the six headings in §2a with fresh readers at C0.
3. Add a `coldread_forecast` key to the round-57 contract before the first content edit (criterion 110), using the measured per-file values (QUALITY append: 6 headings).
4. Do not reflow or reformat any section above the criteria block; the block only appends.
