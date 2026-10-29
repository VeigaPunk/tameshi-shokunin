# T57W1ConnectorCross — cross-claim pattern finder (round 57, wave 1)

Seat: T57W1ConnectorCross (leaf connector, no subagents). Lane base `5e3569969b532310d2b8a3d130901757a3df356b`. No lane file was edited; no tool was installed; the only writes are this report, its `.json`, and `T57W1ConnectorCross-receipts/`.

## Inputs

- Routed items, rounds 50-56: `T57W1ExecExtract/stage/.ufo/evidence/round-57/c1/defects.json` (51 items; per-round 4/8/6/9/10/7/7; the extractor's own selftest PASS and its R51 id-rule deviation are recorded in `T57W1ExecExtract.md`). Item texts are the extractor's 600-char excerpts.
- Ledger: `corpus/routed-defects.json` (49 rows, rounds 40-49).
- Round 56: `corpus/lessons/round-56.md` `## Mistakes`; `corpus/lessons/round-56-verifier-spotcheck.md` §1-§6 (the C2 defects D-C2a/b/c, the routed R56.1-R56.7).
- Criteria: `corpus/QUALITY.md`, criteria 1-107, located by `grep` and dated by the `## Criteria appended` block that contains each one (`T57W1ConnectorCross-receipts/criteria-dating.txt`).

Caveat on the ledger: the 49 rows carry a disposition, a note and an evidence pointer, not the original spot-check text. The defect class of each fixed or open ledger row is therefore inferred from its note and evidence, and is marked `[INFERENCE]` in the JSON. The ten declined rows state their reason directly.

## (a) Recurring defect classes, counts over the 100 routed items

Ledger = the 49 rows of rounds 40-49. New = the 51 items of rounds 50-56. Class is assigned by the defect's shape, one class per item.

| # | class | ledger | new | total | items (new unless marked L) |
|---|---|---:|---:|---:|---|
| 1 | record-receipt mismatch: a number, count, digest, quote or pointer in a record disagrees with the artifact it names | 6 | 15 | 21 | L: R40.1, R40.4, R44.1, R47.1, R47.3, R48.5; R51.3, R52.3, R53.4, R53.5, R53.7, R54.2, R54.3, R54.4, R54.5, R54.7, R54.9, R54.10, R55.2, R55.4, R56.4 |
| 2 | claim ahead of receipt: a verdict, control result or "committed/run" statement with no receipt at the named revision | 2 | 7 | 9 | L: R41.2, R41.4; R53.2, R53.3, R54.1, R55.1, R55.3, R56.2, R56.7 |
| 3 | uncommitted or untracked round work | 4 | 4 | 8 | L: R43.2, R45.2, R47.2, R48.3; R52.4, R53.9, R54.6, R55.6 |
| 4 | stale standing statement or cell (not updated after its subject moved) | 6 | 6 | 12 | L: R41.5, R43.3, R46.4, R47.4, R49.3, R49.4; R50.1, R50.3, R51.2, R51.7, R54.8, R56.3 |
| 5 | missing or unsatisfied registry, index or log row | 1 | 3 | 4 | L: R41.6; R50.2, R52.2, R56.6 |
| 6 | citation anchor or digest drift (line anchor or unpinned digest into a moving file) | 3 | 2 | 5 | L: R40.2, R40.3, R46.1; R53.8, R56.1 |
| 7 | instrument defect (counter, gate or script wrong, dead, unmapped or unsafe) | 8 | 6 | 14 | L: R41.1, R41.3, R42.1, R43.1, R46.3, R48.2, R49.1, R49.2; R51.1, R51.4, R52.5, R53.1, R53.6, R55.5 |
| 8 | control unproven, or control provenance unpinned | 1 | 2 | 3 | L: R40.5; R51.8, R56.5 |
| 9 | routed item carried open | 6 | 1 | 7 | L: R45.1, R45.4, R46.2, R47.5, R48.4, R49.5; R50.4 |
| 10 | declined observation, not a defect | 10 | 0 | 10 | L: R41.7, R42.2, R42.3, R42.4, R44.2, R45.3, R46.5, R47.7, R48.6, R49.6 |
| 11 | report, routing or attribution contract | 2 | 5 | 7 | L: R47.6, R48.1; R51.5, R51.6, R52.1, R52.6, R55.7 |
| | total | 49 | 51 | 100 | |

Class 10 holds the ten items the ledger records as declined (observation, operator-owned promotion, cosmetic). They are counted, but they are not defects, so they are excluded from the none-count in (b)-(c).

## (b) The criterion that should have caught each class

Timing key (computed by `T57W1ConnectorCross-receipts/tally.py`): **pre** = a criterion naming the shape was in force before the item's round; **post** = the criterion landed after the item; **same** = it landed from the item's own round; **none** = no criterion names the shape.

| class | criteria that name the shape | pre / post / same / none | items with none |
|---|---|---|---|
| 1 record-receipt mismatch | 62 (a value in no committed receipt is not reported), 39 (a claim names one effective receipt with digests), 71 (a standing row that quotes output names its revision), 97 (pointers resolve at the landing revision), 23, 38, 51, 87, 100 | 18 / 2 / 0 / 1 | R40.1 |
| 2 claim ahead of receipt | 62, 2 (every claim carries a measured anchor), 40 (a historical calibration receipt is not a current monitor), 81, 103, 106 (a control is scored at the revision it certifies) | 7 / 1 / 1 / 0 | — |
| 3 uncommitted work | 8 (a verification report lands in the repo), 9 (evidence is in the repo before the commit that cites it), 99 (control receipts committed before the deciding run) | 7 / 1 / 0 / 0 | — |
| 4 stale standing statement | 71 (a standing statement goes stale with its subject), 35 (an erratum is appended and dated), 26, 10, 94 (a refusal cites its decisive criterion), 103 | 9 / 2 / 0 / 1 | R41.5 |
| 5 missing registry/log row | 103 (a tool change lands with its registered gate row), 5 (a rejection is kept) | 1 / 1 / 0 / 2 | R41.6, R52.2 |
| 6 citation anchor or digest drift | 34 (anchor by symbol, not line, into a moving file), 79 (a located quote needs a committed snapshot) | 5 / 0 / 0 / 0 | — |
| 7 instrument defect | 17 (classify every nonzero exit), 29 (a guard is covered only if its removal changes a verdict), 24 (run the registered entry command before editing an instrument), 101 (a counter's selftest reaches the deciding code), 105 (a counter arm is proven on a positive control), 106 (the gate compares the receipt's `rev=`), 99 | 7 / 4 / 1 / 2 | R51.4, R52.5 |
| 8 control unproven | 105, 99, 11 (a repeated control names its sample) | 2 / 1 / 0 / 0 | — |
| 9 routed item open | 48 (a routed gap is not repaired until a frozen predicate fails at base), 50 (a claim citing routed items freezes a ledger) | 7 / 0 / 0 / 0 | — |
| 10 declined observation | 5 (a rejection is kept), 1 (a marked opinion is allowed) | not a defect | — |
| 11 report/routing/attribution | 53 (cold-read again after an edit), 36 (a stray write is preserved and routed), 5 | 5 / 0 / 0 / 2 | R51.5, R52.6 |

Notes on the table:

- R52.5 is recorded as `none` with a contrary rule. The item says `tools/registry-check.py:766` hard-codes `/tmp`. At base that line reads `TMPDIR` (`T57W1ConnectorCross-receipts/registry-check-base-lines.txt`: `766: t = _os.environ.get("TMPDIR")`, `772: return tempfile.gettempdir()`), and `tempfile.gettempdir()` is the fallback only when `TMPDIR` is unset. Criterion 9 reads "Scratch stays in `/tmp`", which is the opposite of the lane's TMPDIR rule (see flag 2 below).
- Declined items under class 10 and the one open ledger row under class 9 are counted as dispositions, not as failures to catch.

## (c) The three classes with the most `none`

| rank | class | none | share of class | why it has no criterion |
|---|---|---:|---:|---|
| 1 | 5 missing or unsatisfied registry/log row | 2 of 4 | 50 % | R41.6 (staged SOURCES ids collided, unrenumbered) and R52.2 (LOG round entry missing) have no QUALITY rule. Criterion 7 covers only the coverage-map row of a knowledge file, and criterion 72 covers only the LOG entries that name a file. |
| 2 | 11 report, routing or attribution contract | 2 of 7 | 29 % | R51.5 (cross-domain routing owed to kagi) and R52.6 (report-contract repairs) live in the PROTOCOL report contract, not in QUALITY. |
| 3 | 7 instrument defect | 2 of 14 | 14 % | R51.4 (`round21-measure.py --selftest` not hermetic) has no rule on selftest hermeticity. R52.5 is covered only by criterion 9, which endorses `/tmp`. |

Classes 1 (1 of 21) and 4 (1 of 12) each have one `none` (R40.1 and R41.5). The count of `none` is small overall: 8 of the 90 non-declined items. The ranking by count ties at two (5, 7, 11); it is ordered here by share.

## Cross-claim pattern: C1 and C2 fail the same way

The pattern is one shared shape: a record asserts a value, verdict or pointer, and the receipt it names does not carry it, or the record is absent until something consumes it. The four points below are each grounded in a receipt named in the Receipts list.

**P1. A record is created only when a claim consumes it, so its gap accumulates.** The ledger holds rows for rounds 40-49 and none for rounds 50-56, although the spot-checks for those rounds hold 51 routed items. Criterion 50 requires a frozen ledger only for a claim that cites routed items, and no claim cited rounds 50-56 before this round's C1. C1 and the ledger are the same gap: a receipt exists, and the record that should index it does not.

**P2. Counters measure presence, not agreement.** The round-56 spot-check states that C2's docs arm "counts presence of codes, not their truth" (§2, D-C2a). R56.2 is the consequence: a SKILL cell names `RECEIPT_REV_MISMATCH` where the gate emits `RECEIPT_REV_CONTENT_DRIFT`, and the counter passed. The same shape is in class 1 and class 2 (30 of 100 items together): R54.3 quotes `total=14` where the receipt prints 13; R55.2 quotes `total=0` where `c2-integrated.out:44` prints `total=1`; R55.3 leaves the calibration row at 8 while the monitor reads 6. The check that would fail in each case is "the value in the record equals the value in the receipt it names". None of the frozen counters performs that comparison for prose values.

**P3. Pointers to moving or unverified targets.** R54.3 cites `SCORECARD.md:2584`. At base that line is a different row. The correction is an appended erratum at `SCORECARD.md:2650` ("Old: `total=14` … Corrected: `total=13`"), which satisfies criterion 35. The old line-number pointer is what criterion 34 forbids for a moving file. R56.1 is the same class for SKILL page-local ranges (57 of 61 stale, per the round-56 lesson). R56.4 is the digest version: 13 of 18 `external_inputs` labels are not the sha256 of the C0 path.

**P4. Rules are in force; enforcement is not.** 68 of the 90 non-declined items had a criterion in force before their round that names the item's shape (table (b), timing `pre`), and only 8 had none. More criteria are therefore not the lever. The lever is a mechanical check that binds a record to its receipt. The mechanical checks that exist were added late: criterion 99 (round 49), the deciding-run refusal, and criteria 106 and 107 (round 54 and round 56). R55.5 shows the gap at its sharpest: criterion 106, appended in round 54, already requires that a gate compare the receipt's `rev=` with the revision it decides. The round-55 `deciding-run.sh` still did not, and the defect was found at closure.

**Mapping the round-56 mistakes onto the same pattern.** The four round-56 mistake rows are four versions of P1-P3:

- *landing* (before-receipts cited while untracked): class 3 (R53.9, R54.6, R55.6 are the same class in earlier rounds, and R52.4 before them). Criteria 8 and 9 name it; both existed before round 52.
- *citation drift* (SKILL page-local anchors): class 6, R56.1, under criterion 34, which existed since round 18 and was violated in round 56.
- *sourced quotation* (the false S282 quote): class 1. Criterion 91 (a located quote is compared byte-exact; round 47) and criterion 79 (a located quote needs a committed snapshot) both predate round 56, and the S282 sentence still reached the source row unchecked until the L1 re-opened the source.
- *claim sizing* (the C2 do-nothing control that reaches its target through stub controls or a rewritten `rev=`): class 8, R56.5. Criteria 99, 105 and 106 cover the scoring and positive control, but no criterion requires a producer-provenance check on the receipt. That is the one shape in this sample that no criterion names (R56.5's second half), and it is what the round-56 spot-check's `cannot_see` row already records.

## Flags for the L1 (verifiable, each with its receipt)

1. **R52.5 is stale at base.** `tools/registry-check.py:766` reads `TMPDIR` and the docstring at :762-764 records the round-53 change. The residual is the `tempfile.gettempdir()` fallback at :772 for an unset `TMPDIR`. The C1 ledger row for R52.5 should record "fixed at base (round 53)" with those lines, not "open". Receipt: `registry-check-base-lines.txt`.
2. **Criterion 9 conflicts with the TMPDIR rule.** It reads "Scratch stays in `/tmp`", while the seat spec and the R52.5 and R53.6 items require TMPDIR. A ledger row should not map a `/tmp` item to criterion 9. Receipt: `grep-criteria-keywords.txt` (`QUALITY.md:24`).
3. **R54.3 pointer.** The ledger row should cite `SCORECARD.md:2650` (the erratum) and name criterion 34 for the old line anchor. Receipt: `spot-verify-3.txt`, `criteria-dating.txt`.
4. **R55.2 path.** The receipt is `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out:44` (`total=1 C2_R55_PASS=false`), not an `.ufo/evidence/` path. Receipt: `spot-verify-3.txt`.
5. **R56.3 index part still open at base.** `grep -c receipt-revision-binding corpus/README.md` prints `0` (receipt `spot-verify-2.txt`), which confirms D-C2c.

## Limits

- The criterion for each item is the seat's judgement of shape match. The JSON lists the criterion for each of the 100 items, so a second reader can check each one. A wrong match would change the `none` count only for items whose shape is loose: R41.5, R52.6, R51.5 and R40.1 are the ones I would check first.
- Fixed and open ledger rows are classified from their notes (`[INFERENCE]`); the original R40-R49 spot-check text was not re-read here.
- Criterion dates come from the `## Criteria appended` block that contains each criterion. Criteria 51 and 53 sit in blocks whose headers name another round; their own text names round 26 and round 27, and I used the text.
- One grep in the sweep (`rekey-dir-count|ls-tree` in `round-50/c1/measure.py`) returned nothing: that file is not the round-53 counter the note concerned. It is not used in any conclusion.

## Sweep and receipts

Commands and output are in `T57W1ConnectorCross-receipts/`:

- `grep-criteria-keywords.txt`: keyword greps over QUALITY (uncommitted/untracked/clean tree; TMPDIR, /tmp, tempfile; hermetic, LOG.md, producer, cross-domain).
- `criteria-dating.txt`: criterion header lines, the criteria cited, the SCORECARD anchor move (2584 vs 2650).
- `spot-verify.txt`, `spot-verify-2.txt`, `spot-verify-3.txt`, `registry-check-base-lines.txt`: the registry-check.py TMPDIR lines at base and working tree; the README index count; the R54.3 and R55.2 totals against their receipts.
- `tally.py` and `tally.json`: the classification, the counts in (a) and (b), and the none list in (c). Run as `python3 tally.py`; it asserts 100 items, 49 ledger, and the per-round counts 4/8/6/9/10/7/7.
- `tally-summary.txt`: the per-class summary printed by the tally.

Installed: nothing. Scratch: `$HYAKU_SCRATCH/tameshi-r57/T57W1ConnectorCross`, removed on exit.
