# RGMatrix — §13 projection → pinned-blob cross-check (C1 pre-registration source)

Seat: TameshiR16.RGMatrix. Scope: `corpus/knowledge/arm-class-matrix.md` §13 (13.1–13.7)
projections that predict a mutant outcome for `scripts/round-gate.mjs`, checked against
`kumitate-shokunin` rev `364f1d5954158ef8844bca4a5fef57b05d2f2ca5`, sha256
`f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`.
Static only: no mutant was cut, no gate mode was executed, no `--selftest` was run.

## Verdict

**Every specific line anchor and range endpoint in §13 still resolves to the construct the
matrix describes on the pinned blob.** No line drift, no moved anchors, no changed literals. The
projection's *line addresses* are safe to pre-register from.

Four load-bearing **semantic** defects change implied predictions and must be repaired before
the sweep is pre-registered:

- **D1 — the arm-coverage map is incomplete.** §13.6 ("arms no fixture statically reaches")
  omits five arms that no fixture reaches: `:401` (SCORECARD.md missing), `:425` (LOG.md
  missing), `:436` (git-log failure), `:477` (close-mode report outside `--main-repo`), and
  the main-external citation branch `:377-378`. Mutants there are predicted **survive** and
  are absent from the matrix.
- **D2 — §13.1 line 354 is false.** `REPORT_UNTRACKED` is *not* "the only multi-arm kind
  (5 arms) with every arm statically covered": `:477` is unreached, and
  `SCORECARD_PLAN_MISSING` has two emission sites (`:409`, `:415`) with *both* reached
  (r11, r12).
- **D3 — §13.2 line 370 is false.** The fail-closed detail tail is not "unread except fcE's
  `exit 128` probe": rt3 (`:1436`) asserts the `NO_FILED_REPORTS` tail substring
  `filed=1 round-<N>/kumitate.md`. A mutant of that detail template is **killed**, not
  survived.
- **D4 — §13.6 #4's causal clause is false.** `parseArgs` runs at `:630`, *before* the
  selftest dispatch at `:635`; the nested run's `KUMITATE_LANE='not-a-lane'` therefore does
  reach env-lane validation (`:275-280`) and passes only because hyphens are allowed. A
  single edit that *narrows* the env regex (rejects `not-a-lane`) is killed by the
  hermeticity check (`:1396`); deleting/weakening the check survives.

## Evidence

Pin and identity (read-only):

```
$ git -C kumitate-shokunin show 364f1d5...:scripts/round-gate.mjs > /tmp/.../blob.mjs
exit=0
$ sha256sum blob.mjs
f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  blob.mjs
$ wc -l blob.mjs   → 1511
$ git -C kumitate-shokunin hash-object scripts/round-gate.mjs
1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3
$ git -C kumitate-shokunin rev-parse 364f1d5...:scripts/round-gate.mjs
1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3
```

Blob is identical at the C1 pin and in the current kumitate worktree (line numbers stable
across the `175de6ba` read-time HEAD recorded in §13.10 and the `364f1d5` C1 pin).

Mechanical counts (`blob.mjs`):

```
grep -c "check('"                     → 60   (matches §13.10 #2)
failClosed( sites                     → 527,531,536,644,647,652,683 calls; :656 re-emit;
                                        460,471,488 are `failClosed:` object literals
add('<KIND>' sites                    → 22; per kind: REPORT_UNTRACKED 5, COMMIT_MISSING 2,
                                        LOG_ENTRY_MISSING 2, SCORECARD_ROW_MISSING 2,
                                        SCORECARD_PLAN_MISSING 2, other 9 kinds 1 each
parseVerdict( call sites              → 879,891,900,979,1010,1051,1059,1131,1297,1311 (10)
observed set writes                   → :860 only (inside parseFindings)
durationMs reads                      → :1254 (key), :1263 (typeof only)
citations.mainProbeable reads         → :331/:387 (assignment); no test read
citations.unresolved/notAncestor      → internal :375/:382/:393/:394 only
```

Fixture byte arithmetic (templates re-implemented in Python from `:780-789`; ASCII, so
`Buffer.byteLength == len`):

```
fxThin(5)                 25 B      fxMentions(10,'round-1') 1059 B (smallest non-thin)
fxMentions(1,'round-10') 1119 B     fxBigReport(5)           1579 B
fxNoShonen(5)            1536 B     fxMismatch(5)            1959 B
lowshonen                2061 B     fxHeadingless(5)         2100 B
```

So §13.4's `[26, 1059]` interval is exact: at 1059 the r8 report stays non-thin; at 1060 it
becomes thin and r8's exact kind list fails; at 26 the 25 B thin report stays thin; at 25 it
stops being thin and r4 fails.

Fixture-set facts used for coverage calls (`:760-856`): `fxLaneRepo` always writes
`SCORECARD.md` and `LOG.md` (`opts.scorecard ?? fxScorecard(...)`, `opts.log ?? default`);
`fxCloseFixture` always writes the report under `<main>/.ufo/reports/round-N/lane.md`;
no fixture passes `scorecard:null`/`log:null`; no fixture resolves a cited token in the
`--main-repo` repo (r22 = unresolved, r23 = lane, r24/derived = origin).

## Projection table — §13.1–13.7

`m` = line in `corpus/knowledge/arm-class-matrix.md`. `t` = line(s) in the pinned blob now.
"holds" = does the cited blob line still hold the code/claim the matrix describes.

### §13.1 enum family and coverage table

| # | Projection | m | t | holds | Implied prediction |
|---|---|---|---|---|---|
| P1 | 14/14 kinds have ≥1 text-mode fixture; meta-check is a coarse net | 325 | 171-176, 342-352, 393-551, 1487-1493 | yes | Mutant that stops a *single-arm* kind firing is killed (meta-check + exact kind list). Mutant in one arm of a multi-arm kind may survive if another fixture still fires that kind. |
| P2 | 6/7 fail-closed tokens hand-asserted; 1 token + 2 call-site species uncovered | 326 | 527,531,536,644,647,652,683; 460,471,488 | yes | SURVIVE: `INTERNAL_ERROR` (:683), tracked `REPORTS_DIR_MISSING` (:527), main-repo `UPSTREAM_MISSING` (:488). |
| P3 | exit map 0/1/2/64, 4/4 exercised | 327 | 584-593, 615-618, 629-683 | yes | Kill for exit-code changes on exercised paths (0: r1; 1: r3/r7; 2: fcA-F/jFc/rt3/rt5; 64: u1-u5/rt4). |
| P4 | 4/4 modes; selftest-wins pinned indirectly; `--selftest --json` unpinned | 328 | 635, 48 | yes | SURVIVE for a mutant of selftest-vs-json precedence (no fixture combines them). |
| P5 | all flags exercised; `UFO_SRC` set-value branch uncovered | 329 | 162-163 | yes | SURVIVE for mutants of the non-empty `UFO_SRC` branch (fixtures force `''` at :1347/:1354/:1369). |
| P6 | JSON top-level key set + check shape pinned; nested citations partly unread | 330 | 1254-1262 | yes | Kill for key-set/check-shape mutants; survive for nested `citations` field mutants. |
| P7 | REPORT_MISSING `:342`, r3 pins exit 1, checks=5, exact list | 337 | 342; 898-902 | yes | KILL. |
| P8 | REPORT_THIN `:345`, r4 pins `(bytes=25)` and two-space format | 338 | 345; 908-920 | yes | KILL (constant mutation excluded — see P34). |
| P9 | REPORT_HEADINGS `:347`, r6 pins `headings=0` + SHONEN warning | 339 | 347; 925-929 | yes | KILL. |
| P10 | REPORT_ROUND_MISMATCH `:348-349`, r7/r8/r9 pin both directions | 340 | 348-350; 934-953 | yes | KILL; regex mutations in both directions are discriminated. |
| P11 | REPORT_SHONEN_MISSING `:351-352`, r6/r19/r20/r21 | 341 | 351-353; 925,1048-1070 | yes | KILL (case-insensitive and strict promotion pinned). |
| P12 | COMMIT_CITED_UNRESOLVED `:393`, r22 pins detail token | 342 | 393; 1073-1082 | yes | KILL. |
| P13 | COMMIT_CITED_NOT_ANCESTOR `:394`, r23 pins 7-hex prefix + 40-hex sha | 343 | 394; 1097-1104 | yes | KILL. |
| P14 | SCORECARD_ROW_MISSING arms `:401`,`:404`; r10/r10b | 344 | 401,404; 958-971 | **partial** | `:404` KILL (r10/r10b). `:401` SURVIVE — no fixture ever omits SCORECARD.md (`fxLaneRepo` :761). |
| P15 | SCORECARD_PLAN_MISSING arms `:409`,`:415`; r11/r12/r12b/r13/r14 | 345 | 409,415; 974-1015 | yes | BOTH arms reached (r11→:409, r12→:415): KILL for either arm; r12 also pins `/later/` in the detail (:990). |
| P16 | LOG_ENTRY_MISSING arms `:425`,`:428`; r15 | 346 | 425,428-430; 1018-1023 | **partial** | `:428` KILL. `:425` SURVIVE — LOG.md is always written (:762). |
| P17 | COMMIT_MISSING arms `:436`,`:441`; r16/r17/r18 | 347 | 436,441-443; 1026-1043 | **partial** | `:441` KILL. `:436` (git-log-failure arm) SURVIVE — no fixture corrupts a repo. |
| P18 | TREE_DIRTY `:451`, r26 pins entries=6/first-5-only | 348 | 451-453; 1141-1149 | yes | KILL. |
| P19 | UNPUSHED `:465`, r27 pins `ahead=1` exact | 349 | 465; 1156-1161 | yes | KILL. |
| P20 | REPORT_UNTRACKED 5 arms `:477,:481,:495,:547,:551` | 350 | 477,481,495,547,551; 1166-1183,1420-1431,1460-1467 | **partial** | `:481` KILL (r28), `:495` KILL (r29), `:551` KILL (rt2), `:547` KILL (rt6). `:477` (close-mode outside) SURVIVE — every close fixture puts reports inside main. |
| P21 | "REPORT_UNTRACKED is the only multi-arm kind (5 arms) with every arm statically covered" | 352-354 | 477,481,495,547,551; 409,415 | **no** | False twice: `:477` unreached; `SCORECARD_PLAN_MISSING` is multi-arm with both arms reached. Do not derive "all REPORT_UNTRACKED arms kill" from this line. |

### §13.2 verdict paths

| # | Projection | m | t | holds | Implied prediction |
|---|---|---|---|---|---|
| P22 | `parseVerdict` full-line anchored; all 10 call sites assert `v !== null`; fields read individually | 359-362 | 862-868; 879,891,900,979,1010,1051,1059,1131,1297,1311; 882,901,1134 | yes | KILL for any change to the audit/close verdict line shape or field values. |
| P23 | tracked verdict inline full-line regexes; rt8 prefix-matches only | 366-367 | 1411,1426,1481 | yes | KILL for tracked verdict-shape mutants (rt1/rt2 anchored); rt8 alone would not catch a suffix append. |
| P24 | FAIL-CLOSED token-only; "detail tail unread except fcE exit 128" | 368-371 | 1188,1193,1198,1206,1212,1218,1435,1450; **1436** | **partial (clause false)** | Token mutants at covered sites KILL. Detail tails of fcA-F SURVIVE. But `NO_FILED_REPORTS` detail (`:537-538`) is pinned by rt3 `:1436`: a mutant of `filed=1 round-<N>/…` is KILLED. |
| P25 | selftest shape + `VERDICT: PASS` equality; counts unread | 373-374 | 1399-1400 | yes | Shape mutant KILL; count-value mutant SURVIVE. |
| P26 | JSON top-level key set by equality + check shape | 375-376 | 1254-1262 | yes | KILL for key/shape mutants. |

### §13.3 fail-closed arms

| # | Projection | m | t | holds | Implied prediction |
|---|---|---|---|---|---|
| P27 | 7 tokens over 10 literal sites + `:656` re-emit | 378-380 | 460,471,488,527,531,536,644,647,652,683; 656 | yes (wording: 460/471/488 are object-literal arms, not `failClosed()` calls) | Count and addresses are exact; no prediction change. |
| P28 | Token/site table (REPORTS_DIR_MISSING, NOT_A_GIT_WORKTREE, NO_CLOSED_ROUND, NO_FILED_REPORTS, UPSTREAM_MISSING, MAIN_REPO_NOT_GIT, INTERNAL_ERROR) | 384-390 | 527/647, 644, 652, 536, 460/488, 471/531, 683 | yes | Covered token-site mutations KILL (fcA-F, jFc, rt3, rt5); uncovered species SURVIVE (see P2). |
| P29 | INTERNAL_ERROR token / catch block can change with no fixture moving | 392-393 | 641-684, 683 | yes | SURVIVE. |
| P30 | meta-check structurally blind to fail-closed family | 397-399 | 617 vs 857-860 | yes | A new fail-closed token/detail is invisible to the meta-check; token text at hand-asserted sites can still be killed by fc regexes. |
| P31 | fcE probe cannot distinguish UPSTREAM_MISSING sites; stderr `:615` unread | 400-402 | 1212, 460, 488, 615 | yes | Coordinated site swap SURVIVE (see P50); stderr mutant SURVIVE. |

### §13.4 counts and floors

| # | Projection | m | t | holds | Implied prediction |
|---|---|---|---|---|---|
| P32 | exact counts checks=10/5/13, checked=2/excludedRound=5; kinds compared by `JSON.stringify` | 404-407 | 882,901,1134,1414,1472-1473; 869-872 | yes | KILL for count/list membership/order/multiplicity mutants. |
| P33 | meta-check one-sided (`missing.length===0`); `observed.size` only in unasserted detail; observed⊆enum; stray kind unnoticed | 408-412 | 1489,1491-1492; 342-551 | yes | Stray-kind mutant SURVIVES only where no fixture's exact list observes the path; on covered paths the exact list kills it. |
| P34 | `REPORT_MIN_BYTES` floor interval **[26,1059]** | 412-417 | 167, 345, 913 | yes (arithmetic verified: 25 B / 1059 B, min non-thin 1059) | SURVIVE for any single-edit constant in [26,1059] except 1024; KILL at ≤25 or ≥1060. |
| P35 | `HISTORY_LIMIT=1000`: cap boundary uncovered | 417-418 | 168, 434 | yes (narrowly) | SURVIVE for cap-width changes with n≥1 (fixtures have ≤2 commits; `-n 1` still sees body-marker HEAD). Caveat: `HISTORY_LIMIT→0` makes `git log -n 0` return nothing and r18/r1 fail → KILL. |

### §13.5 reported-unread

| # | Projection | m | t | holds | Implied prediction |
|---|---|---|---|---|---|
| P36 | FAIL-CLOSED detail tails + stderr `:615` unread (fcA-F; fcE also exit 128) | 422-423 | 615, 1188-1220 | yes for fcA-F scope | SURVIVE for fcA-F path/detail remainders and the stderr line. (Global version is false — see P24/rt3.) |
| P37 | selftest counts never asserted | 424-425 | 1399-1400 | yes | SURVIVE. |
| P38 | `durationMs` value unread (typeof only) | 426 | 1263 | yes | SURVIVE (also tracked/fail-closed bodies :569/:613). |
| P39 | JSON `citations.mainProbeable`/`unresolved`/`notAncestor` unread | 427-430 | 331,375,382,387; reads only 1264,1122,1350,1357,1374-1376 | yes | SURVIVE for those fields' writers. |
| P40 | Text details mostly kind-level; exact pins only where §13.1 quotes them | 431-432 | 912,928,990,1081,1101,1146,1160,1169,1180,1428,1436,1464 | **partial** | SURVIVE for r3 path, r7 message, r10/r15 paths, and most other details. KILL additionally for r12 `/later/` (:990), r29 exact `unpushed:` (:1180), rt2 exact `ls-files:` (:1428), rt6 prefix (:1464) — none quoted in §13.1. |

### §13.6 unreached arms (as listed)

| # | Projection | m | t | holds | Implied prediction |
|---|---|---|---|---|---|
| P41 | INTERNAL_ERROR zero fixture | 437-438 | 683 | yes | SURVIVE. |
| P42 | tracked REPORTS_DIR_MISSING `:527` token covered only via main site | 439 | 527, 647 | yes | SURVIVE. |
| P43 | main-repo UPSTREAM_MISSING `:488` — no close fixture pairs lane upstream with main lacking one | 440-441 | 460, 471, 488; close fixtures 1128-1216 | yes | SURVIVE. |
| P44 | env-lane invalid `:277-279`, `--round` non-safe-int `:256`, dirValue flag-like `:246`; nested lane "never reaches parseArgs' env validation because --selftest wins (:635)" | 442-446 | 277-279, 256, 246; **630**, 635 | **partial (causal clause false)** | `:256` and `:246` SURVIVE (no fixture). Env lane: deleting/weakening the check SURVIVES; narrowing the regex so `not-a-lane` is rejected is KILLED by the nested hermeticity run (:1392-1404) — parseArgs validates env before selftest dispatch. |
| P45 | UFO_SRC set-value branch `:162-163` uncovered | 447-449 | 162-163; 1347,1354,1369; 294-296 | yes | SURVIVE. |
| P46 | `--help`/`-h` unknown flags, u1 pins only `--bogus` | 450-451 | 125-126, 273, 1223 | yes | SURVIVE. |
| P47 | `--selftest` wins over `--json`, no combined fixture | 451-452 | 48, 635, 1392-1395 | yes | SURVIVE. |
| P48 | flag>env precedence discriminated for reports-dir/lane (r45) but not main-repo | 452-453 | 1304-1316 | yes | SURVIVE for main-repo precedence mutant (no cited tokens in r45 audit). |
| P49 | citationTokens range form `..`/`...` has no fixture | 454-456 | 315-324; 106-107; 1074,1091,1113 | yes | SURVIVE for the range-split branch (all fixture citations single tokens). |

### §13.7 coordinated edits

| # | Projection | m | t | holds | Implied prediction |
|---|---|---|---|---|---|
| P50 | coordinated rename across kind literal+enum+fixture stays green; prose inventories parsed by nothing; severity pinned at :981/:1053; UPSTREAM_MISSING site swap invisible | 458-464 | 66-98,115-117; 981,1053; 460,488 | yes (coordinated, not single-edit) | SURVIVE for coordinated edits; single-edit severity change from `warning` is KILLED by r11/r19. |

## Unregistered gaps (must be added to the pre-registration)

These arms are reached by no fixture but appear nowhere in §13.6:

| # | Arm | t | Why unreached | Implied prediction |
|---|---|---|---|---|
| U1 | SCORECARD.md-missing arm | 400-401 | `fxLaneRepo` always writes SCORECARD.md (:761); no fixture passes `scorecard:null` | SURVIVE |
| U2 | LOG.md-missing arm | 424-425 | `fxLaneRepo` always writes LOG.md (:762); no fixture passes `log:null` | SURVIVE |
| U3 | git-log-failure arm | 435-436 | all fixtures initialize valid repos with commits | SURVIVE |
| U4 | close-mode report-outside-main arm | 475-477 | every close fixture's reports dir is inside `<main>` (fxCloseFixture :813-814); fcF returns at `:471` before `:476` | SURVIVE |
| U5 | main-repo-external citation branch | 377-378 | no fixture's cited token resolves in `--main-repo` (r22 unresolved, r23 lane, r24/derived origin) | SURVIVE; concrete single-edit candidate: `probe('main', t)` → `probe('origin', t)` at `:377` passes r22/r24/rn/rl/rnone (origin branch yields the same observable) |

## Supplementary — §13.8/§13.10 anchors (outside requested 13.1–13.7, verified because C1 cites them)

| # | Projection | m | t | holds | Implied prediction |
|---|---|---|---|---|---|
| S1 | round-name regex pinned both directions | 466-468 | 348; 942,950 | yes | KILL. |
| S2 | plan window three-sided (r12/r12b/r13) | 467-468 | 987,996,1002 | yes | KILL. |
| S3 | strict promotion (r14, r20) | 468 | 1009,1058 | yes | KILL. |
| S4 | tracked blindfold (rt8) | 468 | 1478-1481 | yes | KILL for tracked output changes; `--repo` ignored. |
| S5 | hermeticity under polluted env + bogus dirs | 468-469 | 1381-1404 | yes | KILL for any selftest dependence on env/dirs. |
| S6 | 40-hex citation boundary | 469 | 1101 | yes | KILL. |

§13.10 pins also hold: `grep -c "check('"` = 60; `wc -l` = 1511; `INTERNAL_ERROR` only at
`:117` (doc) and `:683`; the interval arithmetic is exact (25 B / 1059 B / min non-thin 1059).

## Bounded recommendations

1. **Repair D2 and D4 in the matrix before the pre-registration is filed** (two-line edits at
   m:354 and m:445-446), and add U1–U5 to §13.6; otherwise the ledger leg would pre-register
   five survive-cases as kills or omit them entirely.
2. **Do not generalize "14/14 kind coverage" to arm coverage.** For the 10-mutant sweep,
   classify each mutant by *arm reachability* (tables above), not by kind.
3. **Sweep candidate classes** (all predictions are from the table, not new claims):
   - survives: t:401, 425, 436, 477, 377 (probe swap), 527, 488, 683, 615,
     537-538 trailing text only, 162-163 set branch, 246, 256, 277-279 (deletion/weakening),
     315-324 range split, 168 value 1..1000, 167 value in [26,1059].
   - kills: t:342, 345, 347, 348, 352, 393, 394, 404, 409, 415, 428, 441, 451, 465, 481,
     495, 547, 551, 862-868, 869-872, 882/901/1134, 1254-1262, 1436 (NO_FILED_REPORTS
     detail), 1440-1442 (usage), 1481.
4. **`NO_FILED_REPORTS` detail** (t:537-538) is not a free survive: rt3 pins
   `filed=1 round-<N>/kumitate.md`. If it is chosen as the survive candidate, mutate only the
   trailing `(the highest round is excluded …)` text.
5. **Matrix hygiene** (not mine to edit): `## Errata (round 5)` is glued onto the last line
   of §13.10 item 3 (m:497 ends `… (§13.4).## Errata (round 5) …`) with no newline; any
   machine section-boundary parser will mis-slice §13. Note for the record only.

## Opened paths

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/arm-class-matrix.md`
  (lines 298-497 §13, 494-508 errata boundary only)
- `/tmp/tameshi-r16-RGMatrix-3092/round-gate.mjs`, `blob.mjs` (git-show materialization)
- `/tmp/tameshi-r16-RGMatrix-3092/{sec13.md,cited-lines.txt,cited-compact.txt}` (scratch)
- `kumitate-shokunin` via read-only `git show`/`hash-object`/`rev-parse` only; no writes,
  no checkout.

Tooling: nothing installed or upgraded. Verification executed: `git show` (exit 0),
`sha256sum` (match), `wc -l`, `grep`/`awk` counts, `git hash-object`, Python byte arithmetic.
Not executed: `node round-gate.mjs --selftest` (60/60 unverified by me, per wave-1 constraint)
and any mutant (L1's sweep).
