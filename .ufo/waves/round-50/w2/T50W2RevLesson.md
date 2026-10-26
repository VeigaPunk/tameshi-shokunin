# T50W2RevLesson — review of `corpus/lessons/round-50.md` at 80ea77e99e239982ab0b93e416645ef2359725d3

Seat: T50W2RevLesson (reviewer, leaf) · Lane: tameshi-shokunin · Revision read: `80ea77e9`
(content revision). Every pointer below was checked against the file it names at that revision.
No file was modified; scratch `/fast/scratch/hyaku/tameshi-r50/T50W2RevLesson` deleted before
yield. No tool installed (nothing needed; pacman untouched).

## Method

- Lesson numbered: `git -C <lane> show 80ea77e9:corpus/lessons/round-50.md | nl -ba`.
- Evidence read at REV via `git show 80ea77e9:<path>`; wave-1/receipt files read from the lane
  checkout (working tree == REV for `SCORECARD.md`, verified `cmp`).
- Counts re-derived with `python3` over the JSON artifacts; quotes re-located in the committed
  snapshot texts under `.ufo/waves/round-50/w1/T50ScribeRows.src/`,
  `T50ExecSrcZeller/`, `T50ScribePkgDD.src/` (three independent fetches, identical sha256).

## Statement checks that hold (no finding)

| lesson line(s) | statement | evidence (command that shows it) |
|---|---|---|
| 3-6 | freeze `cdbf24c0`, `amendments: []`, controls + selftests committed at `f87910fe` before wave 1 | `git cat-file -t cdbf24c0`; `git merge-base --is-ancestor cdbf24c0 80ea77e9`; `git show --stat f87910fe` (21 control/selftest receipts) |
| 15-17 | snapshot receipt + two corroborating fetches, same sha256 | `sha256sum` of the three PDFs → all `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`, 247,738 B, HTTP 200 (`fetch-receipt.json`) |
| 19-30 | S271 extra: DOI, URL, accessed 2026-10-26, sha256, running head, 17 pages, no folios, quotes 21/16 words, recheck `730d` | row at `corpus/SOURCES.md:146`; `pdfinfo` Pages=17; `grep -c 'removing any single input entity'` =1 (reading-order line 69), `grep -c 'After 57 tests'` =1 (line 89); folio text `183/184` count 0 (`s167-source-check.txt`) |
| 32-41 | S022 queued→mined + used-by, S024 used-by gains, registry notes: one appended round-50 line + `Next unused id: S272`, Zeller lead and stop note stay | `git diff e3729de..80ea77e9 -- corpus/SOURCES.md` (exactly those 7 line changes) |
| 45-52 | reg-ids 130 (S001-S270), staged-ids 103, collisions 8 S153-S160, none on S167; indented row proof 9 vs column0 8; S167'd in quarantine (17 rows, all S105-S143); document at `absent-defect-register.md:219` (`payload-absent`) | `T50ExecIdGuard/reg-ids` (130 lines), `staged-ids` (103), `collisions` (8), `guard-run.json`, `proof/guard-proof.json` vs `proof/guard-proof-column0.json`, `quarantine-slice` (17 lines), staged row at `merge/tameshi/SOURCES.append.md:21` |
| 54-67 | admit/reject/defer triage matches the package text and receipts | `T50ScribePkgDD.md` `## Required edits` (14 edits) implemented in `corpus/knowledge/delta-debugging-minimization-contract.md` (source S271, §/Definition anchors, tr-normalized recheck, B5 round-29 record, no CANNOT-ANSWER, coverage delta vs S024); `T50ScribePkgIeice.md` verdict `defer`; staged S167 anchor `p. 183-184` and `grep -c 'minimal test case'` recheck confirmed in package row |
| 71-81 | 10 disposers + 9 cross json files (T50Cross40 none); 30/44 agree, 14 disagreements, overrides + resolutions cover all 14; ledger 31 fixed/7 open/11 declined; 8 fixed by this round's commits (R40.2, R40.3, R45.2, R46.4, R47.2, R49.1, R49.2, R49.4) | `T50Disp4{0..9}.rows.json`; `T50Cross41..49.json`; `integrate/agreement.json` (44 both-coded, 30 agree, 14 both-coded disagreements); `overrides.json` (9) ∪ `resolutions.json` (10) cover the 14; `corpus/routed-defects.json` counts; ledger rows for the 8 show post-base commits |
| 83-93 | fabricated-commit pass (F1: `fixed=49 fixed_this_round=49 total=0`), underclaim pass (F2), R40.2/R41.7 unsatisfiable at base until prose names them (H2), CTL_FAB prose 38 vs receipt `fixed=40 evidence_bad=2`, C1 selftest 11/29, ext 43-case 29/29 | `T50CritC1Contract.md` F1-F2; `T50RevControls.md` H2/M1; `control/c1-CTL_FAB.stdout`; `T50MutC1Counter/results.json` + `ext_run.log` (killed=11/29, survivors=18 all killed by ext) |
| 97-110 | shrinker ddmin-to-fixpoint + verdict cache; 12 public mutants 100→24 units in 188 runs, every run == logged; C2 counter weaknesses F1-F4 + 12/20 zero-run lookup; C2 selftest 14/28, survivors cluster map-bearing + records pins | `T50ExecShrinker.public-runs.json` (sums: units_before=100, units_after=24, runs=188); `counter-probe.log`; `T50SentinelShrink.md` F1-F4; `T50CritC2Contract.md` F1/F2; `T50MutC2Counter.md` (14 killed/14 survived; m04/m07 map-less fixtures, m18/m19 records pins) |
| 114-118 | Mistake rows: 1) r49 counters' selftests never reached `measure()` (T49MutC1 14/28 survive; T49MutC2 9/15; `reach-r49.stdout` `calls_measure=0 FAIL` twice; QUALITY 17 at `QUALITY.md:77-83`; QUALITY criterion 101 at `:1526`; both r50 counters build fixture repos and call `measure()`); 2) R49.1 exit-1/2 misclassification at `round-49-verifier-spotcheck.md:122`, probe P11, red-before `cases=35 failed=4`, green-after `failed=0`, capability line byte-equal, no-harm monitor `r49-generator-capability`; 3) successor counters + wave-2 review | `reach-r49.stdout` files=2 failed=2; `reach-r50.stdout` `calls_measure=2 ok` / `calls_measure=1 ok`; `T50ExecGenFix/red-before.stdout`, `green-after.stdout`, `base/green-capability.stdout` (identical last line); `.ufo/evidence/round-50/no-harm.sh` |
| 122-137 | Corrections: R40.2 settlement receipt sha256 `659e39bb…` 64/64/64; R40.3 reg-ids 105 / staged-ids 2 sha256 pins and S132 S152; R40.4 13 tokens vs "11 words"; R46.4 appended correction block; R41.7 declined with reason | `sha256sum` of `.ufo/waves/round-40/settlement-receipt.json`, `assimilation/reg-ids`, `staged-ids` (all match); `round-40.md:14`; `r6-snapshot-practice-corpus.md:10`; `round-46.md:136-147`; ledger R41.7 declined, reason ≥40 chars |
| 141-169 | considerthese proposal 3 at `considerthese/2026-10-26.md:80-82`; round-49 tally 44/26/10/24/four at `round-49.md:130-140`; `contract.json:27,30-34,35`; `measure.py:13-25`; open items in newest `**Planned (round 51)**` paragraph = exactly the 7 ledger-open ids | `considerthese/2026-10-26.md:80-82`; `round-49.md:133-141`; `nl -ba contract.json`; `measure.py` head; `SCORECARD.md` tail |
| 171-176 | Limits named (calibration stays 8; statuses L1-owned; F6 held for one gate, line-level units; B5 stays masked) | consistent with `contract.json`, `corpus/README.md` round-50 F6 block, `survivor-fixture-minimization.md:53,57` |

Also verified: all ten `round-4{0..9}-verifier-spotcheck.md` files byte-unchanged base→REV
(`git show … | sha256sum`, 10/10 SAME); `defects.json` 49 items R40.1..R49.6, sha256
`6a953e6e…` matches the frozen counter pin; `SCORECARD.md` working tree == REV.

## Findings

### F1 — MEDIUM: S271's row quote cell is a 31-word non-verbatim paraphrase, not the located quote the Gate presents

- Where: `corpus/SOURCES.md:146`, cell 7 of the S271 row
  (`python3 -c` split on `|`): "a failing test case is 1-minimal when removing any single change
  makes the failure disappear, ddmin returns such a case, and the reduction is itself a cost
  measured in test runs" — **31 whitespace tokens** (32 `\w+` tokens).
- Not located in the snapshot: `grep -c -i 'a failing test case is 1-minimal'` = 0,
  `grep -c -i 'ddmin returns such a case'` = 0; only the fragment `removing any single change`
  occurs (1 hit). The *located* quotes (lesson lines 26-28: "It stops when a minimal test case is
  reached, where removing any single input entity would cause the failure to disappear." 21 words;
  "After 57 tests, …" 16 words) both occur exactly once in the reading-order extract (lines 69/89).
- Contract position: CORPUS.md contract v1 rule 1 binds the lesson Gate (URL, access date, ≤25-word
  quote with location grounding teaches) — the Gate complies (21/16 words, both ≤25, both located).
  No Gate violation. But the row itself is a claim (rule 1) and its quote cell is what later
  freshness/recheck sweeps and readers read as the located quote; it neither matches the Gate's
  quotes nor the ≤25-word cap, and it differs materially from the source text (e.g. "ddmin returns
  such a case" appears nowhere in the paper).
- Precedent note: many existing rows have >25-token quote cells (S258 44, S267 54, S269 31,
  S270 26, S022 28; S024 exactly 25), so this is a systemic style, but S271 is this round's new
  row and should not propagate it.
- Exact fix: set the S271 quote cell to the located verbatim sentence from §I
  ("It stops when a minimal test case is reached, where removing any single input entity would cause
  the failure to disappear." — 21 words, line 69 of `delta-debugging.reading-order.txt`), or to a
  shorter verbatim ≤25-word span of it, keeping it identical to the Gate quote.

### F2 — LOW: the lesson's recheck description omits the whitespace normalization its own condition uses

- Where: `corpus/lessons/round-50.md:29-30` — "expect one hit each for `removing any single input
  entity`, `After 57 tests`, `139 automated test runs`".
- Observed: in both committed reading-order extracts
  (`T50ScribePkgDD.src/delta-debugging.reading-order.txt` and `T50ScribeRows.src/zeller-hildebrandt-tse2002.txt`)
  the literal `139 automated test runs` yields **0** hits because the line wraps after "test"
  ("…required 139 automated test\nruns, or 35 minutes…"). The operational condition stored in the
  row's knowledge entry (`corpus/knowledge/delta-debugging-minimization-contract.md`, recheck line)
  prefixes `tr -s ' \n' ' '`, under which the phrase hits once.
- Exact fix: phrase the condition as "expect one hit each after whitespace collapse
  (`tr -s ' \n' ' '`)" (the two other phrases hit as literal, counts 1 each).

### F3 — LOW: off-by-one pointer to `round-49.md:140` for the falsifier-over-spot-checks sentence

- Where: lesson lines 167-168 — "…a criterion with a falsifier over the spot-checks
  (`corpus/lessons/round-49.md:140`)".
- Observed: the sentence "a recurrence criterion is left for a round that can give it a falsifier
  over all nine spot-checks" is line 141 of `round-49.md`; line 140 is "fail, not another note.
  This round commits its counters' selftest receipts (…)". The e140 pointer is on the preceding
  sentence in the same paragraph.
- Exact fix: change the citation to `round-49.md:141`. (The adjacent citation `:134` for "44
  status-neutral conformance defects" is correct.)

### F4 — INFO: T50Cross40 has no json file; the lesson's parenthetical ("wrote its codes into its returned output only") is not independently verifiable from the lane

- `T50Cross41.json`..`T50Cross49.json` exist; `T50Cross40.json` does not (matching the lesson).
  The "returned output only" explanation cannot be checked against any committed artifact — a note,
  not a defect; the 30/44 + 14 resolutions nonetheless reconcile (F1 of the verified table).

## Gate compliance (CORPUS.md contract v1)

- Rule 1 (URL / access date / ≤25-word located quote with location for every new row): S271
  satisfies it in the lesson Gate — URL, accessed 2026-10-26, 21- and 16-word quotes with §I
  locations, both verbatim-hit once, both grounding the teaches cell. Non-author re-open confirmed
  by the two independent fetches with identical sha256.
- Rule 2 (append-only; status/recheck/used-by changes logged old→new): the only in-place changes
  base→REV are S022 status+used-by, S024 used-by, the registry-note append and the "Next unused id"
  line — all logged in `## Gate` (lines 32-41). S271 is a new row, not an edit. No unlogged change
  found in `git diff e3729de..80ea77e9 -- corpus/SOURCES.md`.
- Every number the Gate prints for S271 (HTTP 200, 247,738 B, sha256, 17 pages, 21/16 words,
  `730d`) reproduces from the receipts.

## Summary

- All count claims check out: 49/30-of-44/14/31-7-11/8 this-round fixes (ids correct), 11/29 +
  43-case 29/29, 14/28 + survivor clustering, 130/103/8, 17 quarantine rows (all S105-S143), 247,738 B,
  21/16/25-word quotes, 100→24 units in 188 runs, 64/64/64, 105/2 sha pins, 13 tokens, 44/26/10/24/four.
- Every pointer resolves at the named file:line (the only off-by-one is `round-49.md:141` vs `:140`, F3).
- Every "what counters/seats found" claim matches the receipts, including the disclosed CTL_FAB
  prose-vs-receipt deviation (38 vs 40/evidence_bad=2) and the F1/F2/H2 blind spots.
- Gate meets CORPUS.md contract v1 rule 1; row transitions are logged old→new (rule 2).
- One substantive edit recommended: S271's SOURCES row quote cell (31-word paraphrase, not located)
  should be replaced by the Gate's located 21-word verbatim quote (F1); plus two wording fixes (F2, F3).
- No false, stale, or unlocatable claim found beyond F1-F3; the lesson is accurate about its own scope
  and about what the counter can and cannot certify.
