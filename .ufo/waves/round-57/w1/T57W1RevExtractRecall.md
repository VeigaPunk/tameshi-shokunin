# T57W1RevExtractRecall: independent recall of the round-57 routed-defect extractor

Read-only seat. Counted the routed items of the seven spot-check files by eye, without the extractor, then compared with the extractor's staged output (`T57W1ExecExtract/stage/.ufo/evidence/round-57/c1/defects.json`, 51 entries). No lane file edited. Lane base `5e3569969b532310d2b8a3d130901757a3df356b`; all files read from the lane tree.

## Verdict

- Recall 51/51, precision 51/51 on the routed-heading set. Set difference is empty both ways (receipt `receipts/id-set-diff.txt`: `mine=51 ext=51 uniq_mine=51`, both differences empty).
- Per-round counts match: r50 4, r51 8, r52 6, r53 9, r54 10, r55 7, r56 7 (= extractor `per_round`).
- Line spans agree for all 51 entries (checked against grep line numbers and the staged `line`/`end` fields).
- Every outside-heading defect the closure routes maps to an extractor item. No recall loss.
- Twelve outside-heading defects are not routed by the closure. They correctly sit outside the set; listed in §3b for the L1's record.
- Four findings for the L1 (§4): an id-rule collision that forces the extractor's reading in round 51, a lane-label namespace clash inside round 51, a wrong cross-reference in round 52, and the R54.5 fold (agreed).
- Not run: the extractor's selftest and the frozen counters (not in this seat's item). Nothing here is a counter verdict.

## 1. Independent count, by eye

| file | routed heading (line) | item lines | count |
|---|---|---|---|
| round-50 | `## Routed defects for the lane next round` (96) | 98, 99, 100, 101 | 4 |
| round-51 | `## Routed defects for the lane next round` (124) | 126 (labelled R51.1), 127-133 (unlabelled) | 8 |
| round-52 | `## Routed defects (lane must fix next round)` (81) | 83-88 (all labelled) | 6 |
| round-53 | `## Routed defects (lane must fix next round)` (76) | 78-86 (all labelled) | 9 |
| round-54 | `## Routed defects (lane owns the fix; ...)` (105) | 107-108, 110, 112, 114, 116, 118, 120, 122, 124 | 9 |
| round-54 | `## Routed defects - one new this pass` (231) | 233-239 (R54.10) | 1 |
| round-55 | `## Routed defects (lane owns the fix; ...)` (116) | 118, 123, 127, 131, 134, 138, 143 | 7 |
| round-56 | `## 6. Verdict and routing` (122), list 130-136 | 130-136 | 7 |

Total 51.

Excluded under those headings, correctly:
- r54 L241-245 `**R54.5 extended.**` folds into R54.5 (same finding, labelled R54.5). Counted separately it would give 52; I agree with the fold.
- r54 L247 `R54.1-R54.9 as filed above ...` is not bold-led, not an item.
- Operator notes r50 L103 and r51 L135 (`Operator note:`), which the extractor also excludes.

## 2. Set difference

- mine minus extractor: empty. extractor minus mine: empty.
- Receipts: `receipts/id-set-diff.txt`, `receipts/staged-ids.txt`.
- Line spans: all 51 agree with the staged `line`/`end` fields (examples: R51.1 126-126, R54.1 107-108, R54.10 233-239, R55.3 127-130, R56.7 136-136).

## 3. Outside the extractor's set

### 3a. Outside-heading defects the closure routes (each has a carrier item, so no recall loss)

| source | defect | routing | carrier |
|---|---|---|---|
| r51 L31 | kagi drift-pins verdict-word grep, not routed to kagi | routed | R51.5 (L130) |
| r51 L32 | `## Gate` lists admits only | routed | R51.6 (L131) |
| r51 L34 (part) | C3 counter missing mutation attack | routed | R51.4 (L129) |
| r52 L18 | 4 untracked round files | routed | R52.4 (L86) |
| r52 L20, L24 (a)-(d) | SHONEN one-line, false "not committed", no Landed changes, vocabulary | routed | R52.6 (L88) |
| r52 L24 (e) | no LOG.md round-52 entry | routed | R52.2 (L84) |
| r52 L46 | over-count review (Corr12) | routed | R52.3 (L85) |
| r53 L28 (a) | SCORECARD past-tense pointers | routed | R53.2 (L79) |
| r53 L28 (b) | SCORECARD `total=6` quote | routed | R53.1 (L78) |
| r53 L28 (c) | no CONTROLS_B receipt | routed | R53.3 (L80) |
| r53 L28 (d) | C2 receipt rev unanchored | routed | R53.4 (L81) |
| r53 L28 (e) | stale verify-freeze receipt | routed | R53.5 (L82) |
| r53 L41 | frozen C1 counter rekey arm dead | routed | R53.1 (L78) |
| r53 L66 | S275 page locator | routed | R53.8 (L85) |
| r54 L26 | 3 untracked seat files | routed | R54.6 (L118) |
| r54 L29, L159 | 26.3 % attack share | routed | R54.9 (L124) |
| r54 L91, L213 (count part) | "84" staged entries vs 81 | routed (count) | R54.9 (L124) |
| r55 L35 | 7 + post-filing uncommitted files | routed | R55.6 (L138), R55.7 (L143) |
| r55 L73, L79, L114 | green C2 receipts at other revs; quoted total=0 | routed | R55.1 (L118), R55.2 (L123) |
| r55 L85 | calibration harm 64/64 -> 46/64 | routed | R55.3 (L127) |
| r56 L26 (D-CF1) | "no byte changed after C0" phrasing | routed | R56.7 (L136) |
| r56 L28 (D-CF3) | registry lacks gate row | routed | R56.6 (L135) |
| r56 L71 | arm-5 provenance gap | routed | R56.5 (L134) |
| r56 L75 (D-C2a) | SKILL `RECEIPT_REV_MISMATCH` cell false | routed | R56.2 (L131) |
| r56 L76, L77 (D-C2b, D-C2c) | recheck 14/14; not indexed | routed | R56.3 (L132) |
| r56 L93 | freshness: stale page-local anchors | routed | R56.1 (L130) |

### 3b. Outside-heading items the closure does NOT route (not in the set; flagged)

- N1. r50 L44: five R40.x cross-codes missing (T50Cross40 wrote no json). Disclosed, not routed.
- N2. r51 L33: deciding run on freeze `84aa673a` (FROZEN_UNCHANGED=0; amendment 2 widened no-harm). Closure: "a judgement call rather than a breach". Not routed. Its harm half is covered in text by R51.1, not as a separate route.
- N3. r51 L34: 95 literal `@P@` placeholders, 41 seat files under `@P@...` names, one misrooted copy, three dead w2 seats. Closure: "All four defects are lane-disclosed". Not routed (only the C3 mutation-attack half sits under R51.4).
- N4. r52 L24 (f): start census "133 rows" not printed in `census-start.stdout`. Not routed.
- N5. r52 L24 (g): `T52W3CritAdmission.md` says "16/19 readers" against 18 committed JSONs. Not routed.
- N6. r54 L22: report author timestamp precedes the cited tip. Closure: "pass (timestamp oddity noted)". Not routed.
- N7. r54 L30: no `w1-results.json` / `w2-results.json` in lane or fleet ("record gap (noted)"). Not routed.
- N8. r54 L91, L213: the delta-debugging entry is described as "refused on capacity" and "Planned (round 55)" re-adoption, but the closure's own finding is that it is already adopted at base (`79f44b5`). Closure marks "disagree". Only the 84/81 count is routed (R54.9). The wording fix is not routed.
- N9. r54 L147-148 and the erratum: fleet MANIFEST `rounds[874]` pointer correction. Closure-side record, not a lane defect.
- N10. r55 L34: wave shape 141 seats over the 64-128 band by 13. Closure Step-1 marks "pass as reported". Not routed.
- N11. r56 L27 (D-CF2): two seats named report files they never wrote to the lane. "No claim rests on them." Not routed.
- N12. r56 L52 and L126: six re-bound headings carry 13 gap-minor findings, bound unrepaired. SHONEN box 3 cites them. Not routed.

Excluded by design and by the extractor alike: operator notes (r50 L103, r51 L135, r53 L90, r55 L152-153, r56 L126, L138).

Disclaimed as not lane defects (no route owed): r54 Erratum L178-182 (first C2 attempt under `/tmp` read the scratch placement, not the lane); r55 L96 S280 colon-spacing notation ("locatable, not misquoted").

## 4. Findings for the L1

- F1. Round-51 id rule. The brief's literal rule (unlabelled n = position among unlabelled items) collides: item 1 is labelled `R51.1`, and items 2-8 would also get `R51.1`-`R51.7`. The extractor's rule (position among all items) is the only collision-free reading and matches the file's order. I agree with it. The brief should record this as the ruling.
- F2. Round-51 label namespace clash. The closure cites the lane's own labels inside its routed items: item 2 (closure position R51.2) reads "(R51.2/R51.3)" for the lane's stale-SKILL and runner-pointer defects (L127). Item 3 text (closure position R51.3) says "The lane disclosed this as R51.2" for the `wrong_expectations` defect (L89). So "R51.2" names two lane defects in the same file. Recommendation: the ledger keys rows by file + line span + closure item, not by bare id text alone.
- F3. Cross-reference slip, round 52. L46 says "See routed defect R52.4". The over-count review is R52.3 (L85). R52.4 is uncommitted round work (L86). A reader following L46 lands on the wrong item. Both ids exist, so the extractor set is unaffected.
- F4. R54.5 fold. Agreed: "**R54.5 extended.**" is the same finding, labelled R54.5; no separate id.

## 5. Sweep (commands and output)

Receipts under `.ufo/waves/round-57/w1/T57W1RevExtractRecall-receipts/`:
- `routing-mentions.txt`: `grep -n -i -E 'rout|for the lane|lane (must|owns|next)|R5[0-6]\.[0-9]+'` over the seven files (100 lines). Every routing mention outside a routed heading was read against §3a/§3b.
- `outside-candidates.txt`: grep for the N-list phrases; used to locate lines.
- `staged-ids.txt`: `jq -r '.defects[] | "\(.id)\t\(.line)-\(.end)"'` over the staged `defects.json` (51 rows).
- `id-set-diff.txt`: `comm -23` / `comm -13` over the two sorted id lists: both empty.

Headings were located by `grep -n '^##'` on each file, and item starts by `grep -n -E '^(\*\*R[0-9]+\.[0-9]+|[0-9]+\. \*\*)'`. These grep outputs were used only to confirm line numbers; the counts in §1 were made by reading.

## Tooling and scratch

- No tool installed or upgraded. Used pre-existing `grep`, `jq`, `comm`, `sort`, `cut`, `tee`, `wc`.
- Scratch note: my first sort/comm attempt wrote to `$TMPDIR/...` with `TMPDIR` unset, which resolved to `/mine.txt`; the redirect failed (EACCES) and nothing was written there. The second command wrote three 51-line id files under `${TMPDIR:-/tmp}` (`mine.txt`, `mine2.txt`, `ext.txt`); they are removed in the final step below. The receipt commands use `HYAKU_SCRATCH`.
- Nothing edited under `corpus/`, `tools/`, `.ufo/evidence/`, or any frozen round path.
