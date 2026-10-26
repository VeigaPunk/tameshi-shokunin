# Round 50 lesson

L1 TameshiR50 (hyaku run 9, attempt 1). Two claims on distinct axes, pre-registered before any seat with both counters, the
frozen 49-item defect set, the controls harnesses, the no-harm monitors and the deciding script
(`.ufo/evidence/round-50/contract.json`, freeze `cdbf24c07f9be3a991997c25b1f1d4bb375014ae`, `amendments: []`); controls and
both counter selftests scored at freeze bytes and committed at `f87910fe` before wave 1. C1 calibration: the lane's
disposition of the 49 items its round-40..49 closures routed becomes one ledger, `corpus/routed-defects.json`, with at least
five items closed this round. C2 coverage (sourced, capability): the F6 move, `tools/shrink-case.py`, a 1-minimal shrinker of
a gate's killing case with its cost in guard runs. Frontier step: row S271, S022 and S024 re-read, the mistakes below, sourced
claim C2. Assimilation: theme F6 from `merge/tameshi/` (one entry admitted with edits, the staged row refused as-is and
re-grounded, one entry deferred). considerthese: `considerthese/2026-10-26.md` proposal 3 implemented as C1 (section below).

## Gate

Rows opened this round (contract v1 rule 1: URL, access date, located quote of at most 25 words). Snapshot and fetch receipt:
`.ufo/waves/round-50/w1/T50ScribeRows.src/` (`fetch-receipt.json`), corroborated by two independent fetches with the same
sha256 (`.ufo/waves/round-50/w1/T50ExecSrcZeller/`, `.ufo/waves/round-50/w1/T50ScribePkgDD.src/`).

- **S271** — Zeller & Hildebrandt, "Simplifying and Isolating Failure-Inducing Input", IEEE TSE 28(2), February 2002,
  DOI 10.1109/32.988498 — `https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf`, accessed 2026-10-26,
  HTTP 200, 247,738 B, sha256 `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`. The carrier is a university
  course mirror (the DOI resolves to IEEE Xplore, which served no article bytes: `T50ExecSrcZeller.md:19-25`); the running
  head "IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002" and the title block identify it. Tier A.
  The mirror is paginated 1-17 with no journal folios, so the anchor names sections, Definition 10, Propositions 11-12 and
  Figs. 11-12, never printed pages (the row draft's "printed p. 183" was an inference from an offset and was removed before
  the append). Quote (21 words), §I Introduction, reading-order extract: "It stops when a minimal test case is reached, where
  removing any single input entity would cause the failure to disappear." Second quote (16 words), §I: "After 57 tests, the
  original 896-line HTML input is reduced to the minimal failing test case". Recheck cell `730d`; the re-verify condition
  stripped from it: fetch the URL, `pdftotext` in default reading order (the `-layout` mode hyphen-folds "simplifies"), and
  expect one hit each for `removing any single input entity`, `After 57 tests`, `139 automated test runs`.

Rows touched old → new (logged here as contract v1 asks):
- **S022** status `queued` → `mined`; used-by `—` → `corpus/knowledge/fixture-shrinking-pilot.md` (the pilot quotes its
  abstract; re-fetched 2026-10-26, HTTP 200, 115,315 B, sha256 `fa3036a3…`, anchor and teaches cell still present,
  `.ufo/waves/round-50/w1/T50ScribeSrcHeld.md`; quote, 25 words: "significantly mitigates the impact of the test-case
  validity problem, by ensuring that any reduced test case is one that could in principle have been generated").
- **S024** used-by `corpus/knowledge/survivor-fixture-minimization.md` → that entry plus
  `corpus/knowledge/fixture-shrinking-pilot.md` and `corpus/knowledge/delta-debugging-minimization-contract.md` (re-fetched
  2026-10-26, byte-identical to the round-29 snapshot, sha256 `3abede35…`).
- Registry notes: one appended round-50 line and "Next unused id: S272"; the Zeller lead bullet and the old stop note stay
  as written.

### Assimilation (theme F6, `/home/vgpnk/Projects/shokuknow/merge/tameshi/`, read-only)

Id collision check in scratch (`.ufo/waves/round-50/w1/T50ExecIdGuard/`): `reg-ids` 130 (S001-S270), `staged-ids` 103,
`collisions` 8 (S153-S160, all known since rounds 45-47); none on S167. Guard proof: a scratch registry with an indented
`  | S167 |` row yields 9 collisions where the column-zero pattern misses it. The guard (`tools/staged-id-guard.py --json`)
agrees: `collision_count=8`, `next_free=safe_floor=S271`. Renumber map: staged S167 → **S271**, by document (the URL and DOI
are the evidence; S167 collides with nothing and is not reused, and S175 by arithmetic is refused). Quarantine slice: 17
tameshi rows, all S105-S143; S167 is not one of them by id, but its document appears at
`absent-defect-register.md:219` as `payload-absent`; hand-checked this round: the span is verbatim in the reading-order
extract and missing only from the `-layout` extract, a two-column fold false positive, not a fabrication.

- **Admit — `delta-debugging-minimization-contract.md`**, with the edits of `.ufo/waves/round-50/w1/T50ScribePkgDD.md`
  `## Required edits` (source re-pointed to S271 with a committed snapshot; page locators replaced by section/definition
  anchors; the recheck command replaced by one that can see the text; the witness direction corrected — a removal that
  loses the failure; the B5 sentence replaced by the round-29 record; the dangling `CANNOT-ANSWER.md` dropped; a coverage
  delta against the held S024 restatement). Landed at `corpus/knowledge/delta-debugging-minimization-contract.md`.
- **Reject — the staged S167 row as written**, and the entry's cost claim. The row's anchor "p. 183-184" does not resolve on
  the carrier (no folios, 17 pages for an 18-page range) and its recheck (`curl … | grep -c 'minimal test case'`) returns 0
  on the compressed PDF; the document is adopted only as the re-grounded S271. The entry's sentence that the 896-line
  reduction cost "139 automated test runs" is refused under QUALITY 2: the source gives 57 for that reduction (§I; §IV-B
  Fig. 12), and 139 is the Abstract's two-reduction total, 82 + 57. Flip: none needed; the corrected statement is in the
  admitted entry.
- **Defer — `r7-ieice-mutant-abstraction-authority.md`** (`.ufo/waves/round-50/w1/T50ScribePkgIeice.md`): the report is
  verified verbatim, but it reduces the mutant set, not a fixture, so it would be filed on the wrong side of F6. Flip: admit
  as "survivor-side review cost, F6-adjacent, does not move F6", tier A only inside its own numbers.

## C1 — what the dispositions found

Ten disposer seats (`.ufo/waves/round-50/w1/T50Disp4{0..9}.rows.json`) and ten independent cross-coders
(`T50Cross4{0..9}.json`; T50Cross40 wrote its codes into its returned output only, no json file) judged the 49 items against
the tree at base. Disposer and cross-coder agreed on 30 of the 44 items both coded; the L1 resolved the 14 disagreements
item by item (`.ufo/evidence/round-50/integrate/agreement.json`, `overrides.json`, each override with its reason). The
ledger lands 31 fixed, 7 open, 11 declined; 8 of the fixed items are closed by this round's commits (R40.2, R40.3, R45.2,
R46.4, R47.2, R49.1, R49.2, R49.4). The revenger's walk (`T50RevengerRecur.md`) finds the long tail is not lapsed fixes but
items never given one: never acknowledged (R40.2, R40.3), re-classified as disclosed or operator-owned, or left out of a
Planned paragraph (R49.1). Three classes came back after a QUALITY criterion (monitor-false-red after 88; standing rows
after 92; pointers after 72/73/81/97); one came back with no criterion at all (receipt not committed: round 45 → fixed 46 →
round 47), which R45.2 and R47.2 close this round with committed receipts
(`.ufo/evidence/round-50/routed/receipts/MANIFEST.md`).

Attacks before the data, disclosed, not used to re-score (`T50CritC1Contract.md`, `T50RevControls.md`, `T50MutC1Counter.md`):
- A fabricated commit plus ledger passes the frozen C1 counter in a scratch clone (`fixed=49 fixed_this_round=49 total=0`,
  F1), and opposite dispositions of one tree both pass (F2): the counter checks that evidence exists, is keyed, is new and is
  not an acknowledgement; it cannot check that a status is true. The after-base floor is therefore not evidence that any fix
  is genuine; the per-row wave-2 attacks and the closure sample are.
- R40.2 and R41.7 had no keyed line in any allowed path at base, so no ledger could pass until round-50 prose named them
  (`T50RevControls.md` H2); this lesson's corrections name both, which is also what makes them fabricable.
- The contract prose says CTL_FAB reached `fixed=38`; the receipt says `fixed=40 evidence_bad=2` (two terms false, not one).
  The receipt is the record.
- The frozen selftest kills 11 of 29 single-edit mutants of the C1 counter; a 43-case extended selftest kills 29 of 29
  (`T50MutC1Counter/`).

## C2 — what the attacks found

The shrinker (`T50ExecShrinker.md`: ddmin to a single-unit fixpoint with a verdict cache, 12 public mutants 100 → 24 units in
188 runs, every run matching the logged invocations) was built blind to the hidden panel. The frozen C2 counter is weaker than
its predicate reads, and the round discloses it (`T50CritC2Contract.md`, `T50SentinelShrink.md`, `T50ExecLogger.md`,
`T50MutC2Counter.md`):
- the shrinker runs in a directory beside the counter's own judge copies and can rewrite them, which makes `kills` and
  `minimal` tautologies (sentinel F1, critical, shown with a paired control);
- the run log lives in the shrinker's directory, so `runs == logged` holds for an honest shrinker and also for one that
  strips the logger or pads the log (critic F1, sentinel F2); a lookup table keyed by the mutant's hash passes 12 of 20 with
  zero runs (critic F2);
- a FIFO or a lone surrogate in the output can hang or crash the deciding run (sentinel F3, F4);
- the frozen selftest kills 14 of 28 single-edit mutants; the survivors cluster on map-bearing cases and on records pins.
The round's shrinker does none of these: wave 2 reviews its source for writes outside its TMPDIR, any read of a guard copy it
was not handed, and any table of answers, and re-counts its guard runs from outside its own directory. The C2 verdict rests on
that review as well as on the counter.

## Mistakes

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| 1 | verification-blindspot: both round-49 frozen counters' `--selftest` exercised only pure helpers, so the pins, floors and totals that print the claim label were certified by nothing | `.ufo/waves/round-49/w1/T49MutC1Counter.md` (14 of 28 survive; the selftest never calls `measure()`), `.ufo/waves/round-49/w1/T49MutC2Counter.md` (9 of 15); `.ufo/evidence/round-50/quality/reach-r49.stdout` (`calls_measure=0 FAIL` twice) | QUALITY 17 (`corpus/QUALITY.md:77-83`: helper-only controls are not a standalone selftest) — written for gates, never applied to the lane's own claim counters | QUALITY criterion 101 (selftest reaches `measure()`; mutation probe disclosed); both round-50 counters build fixture repos and call `measure()` (`.ufo/evidence/round-50/control/c1-selftest.stdout` 25/25, `c2-selftest.stdout` 9/9). Shown able to fail: `selftest-reach.py` exits 1 on round 49's counters and 0 on round 50's (`reach-r49.*`, `reach-r50.*`). Reach is not enough: the round-50 selftests still kill only 11/29 and 14/28 (`T50MutC1Counter.md`, `T50MutC2Counter.md`), which the criterion makes a stated number |
| 2 | misclassification: the round-49 generator printed a setup fault as a finding (an unreadable guard gave `VIOLATION` and exit 1, where its docstring says exit 2) | `corpus/lessons/round-49-verifier-spotcheck.md:122` (R49.1); `.ufo/waves/round-50/w1/T50ScribeMistake.receipts.txt` probe P11 | QUALITY 17 (classify every nonzero exit) | `tools/pbt-staged-id.py` error paths fixed with four new selftest cases that fail on the base bytes (`T50ExecGenFix/red-before.stdout` `cases=35 failed=4`, `green-after.stdout` `failed=0`); the capability line is byte-equal (no-harm monitor `r49-generator-capability`) |
| 3 | instrument-design (found this round, not fixed): both round-50 frozen counters admit forgeries a mechanical check cannot see — a fabricated ledger passes C1, and a shrinker can rewrite C2's judge copies and its own run log | `T50CritC1Contract.md` F1-F2, `T50SentinelShrink.md` F1-F2, `T50CritC2Contract.md` F1-F2 | none | not fixed: the counters are frozen. Routed to round 51 as successor counters (judge from bytes the shrinker never saw, run log outside its reach, output read with a type and size check; per-row disposition attested by a seat other than the ledger's author). This round's defence is the wave-2 per-row and per-source review, named in the report |

## Corrections to earlier records

- **R40.2 — the round-40 wave grant, cited durably.** The round-40 report cited the transient seat-ledger line in
  `~/.local/state/shokunin-hyaku/wave-slots`, which the release path deletes. The durable record of that wave is
  `.ufo/waves/round-40/settlement-receipt.json` (sha256 `659e39bb7fba6d381ee3af27daec8b74a6542d861b8b4666b4d46d4ad44f89a3`):
  64 registry members, 64 seat exits, 64 reports present. The round-40 report is a closed fleet file and is not rewritten.
- **R40.3 — the round-40 id lists, pasted as the closure asked.** `reg-ids` (105 ids, sha256
  `b11c94133a35ce8c2c13bb30c04dc545290e53c40710cfd09c4b0a3d94126e91`): S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020 S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060 S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096 S097 S099 S100 S101 S102 S103 S104 S105 S106 S107 S108. `staged-ids` (2 ids, sha256
  `d77a652a2dbc36459dc74a10e8daa7f2e47cc713db0d02fc10d7f48dbb129fce`): S132 S152. Collisions: none. Source:
  `.ufo/waves/round-40/assimilation/reg-ids`, `staged-ids`.
- **R40.4 — the S152 quote is 13 tokens, not "11 words".** `corpus/lessons/round-40.md:14` labels the quote "drawbacks such
  as fragility and lack of context can lead to false positives" as 11 words; it is 13 whitespace tokens and 13 letter/digit
  words (`T50ScribeCorrections.md`, C1-R50-2). The same slip stands in `corpus/knowledge/r6-snapshot-practice-corpus.md:10`.
- **R46.4** — the S259 quote's fold is stated in the round-46 lesson itself, in an appended block
  (`corpus/lessons/round-46.md`, `## Correction — appended in round 50`).
- **R41.7 (declined)** — the round-41 note block at `corpus/SOURCES.md:436-437` (round-41 numbering) splits a bullet list
  across a blank line; it renders as two lists and has no parse impact. Reflowing it would edit a closed registry note for no
  gain, so the item is declined, not fixed.

## considerthese

`considerthese/2026-10-26.md` (operator reflection, 2026-10-26), proposal 3, "Recurring-defect tracker for closures"
(`considerthese/2026-10-26.md:80-82`), was mined in round 49 as a one-round tally — the nine spot-checks of rounds 40-48
carry 44 status-neutral defects in 26 classes, 10 classes recur in a later round and carry 24 of the 44 rows, four of them
after a QUALITY criterion had been written for them (`corpus/lessons/round-49.md:130-140`) — and is implemented this round as
C1's ledger, `corpus/routed-defects.json` (`.ufo/evidence/round-50/contract.json:27`), scored by
`.ufo/evidence/round-50/c1/measure.py` (label `C1_R50_PASS`).

What the ledger does that the proposal asked for. It makes the lane's disposition of every routed defect a checkable record:
one row for each of the 49 items the ten spot-checks of rounds 40-49 routed (`.ufo/evidence/round-50/c1/defects.json`), with a
status the tree must support — `fixed` needs a full commit after the item's routing commit, a keyed excerpt absent from that
path at `routed_at`, and no acknowledgement word on the cited lines; `open` needs the id in the newest `**Planned (round`
paragraph of `SCORECARD.md`; `declined` needs a reason of at least 40 characters (`measure.py:13-25`) — and every evidence
excerpt must resolve at its cited 1-based lines, outside the spot-checks, the ledger and this round's C1 instrument, with the
ten spot-check files byte-unchanged. It also forces work in the round that opens it: `fixed >= 20`, `declined <= 12`, and at
least 5 fixes landed by commits after base (`contract.json:30-34`), which is what a ledger fabricated from history alone
cannot meet (`contract.json:35`, control `CTL_FAB`). So "a routed defect is not a closed defect" becomes a predicate instead
of a note, the half of the proposal that says the disposition must be visible.

What it does not do. It is per item, not per class: the row schema carries no class field (`contract.json:27`), so it neither
tallies a defect class nor counts a recurrence across rounds — the proposal's central question, "check whether a defect
already routed to a criterion shows up again", is not answered by the ledger. It carries no gate: the proposal's
"a recurrence means the fix did not stick and should become a gate, not another note" has no counterpart, because nothing in
the instrument reads two rounds at once. Its population also differs from the proposal's: 49 routed items, not the 44
status-neutral conformance defects the round-49 tally counted (`corpus/lessons/round-49.md:134`). And it cannot see semantic
support — a keyed excerpt that is new since routing but does not actually resolve the defect passes the counter
(`contract.json:35`); wave-2 seats attack that per row and the closure samples it. The recurrence half therefore stays open,
and the round-49 note already named what it needs: a criterion with a falsifier over the spot-checks
(`corpus/lessons/round-49.md:140`). The next step is a class field plus a recurrence clause whose falsifier is a class fixed
in round N that reappears in round N+k, not a second prose ledger.

## Limits named

- Calibration stays 8: that is the round-21 monitor's ceiling (two points per restrained `[~]` box). C1 moves the surface
  (routed-defect dispositions), not the score.
- The ledger's statuses are the L1's after resolving two independent codings; the counter does not judge them true.
- F6 is held for the method on killing cases, one gate, line-level units; the round-29 B5 survivor stays masked.
