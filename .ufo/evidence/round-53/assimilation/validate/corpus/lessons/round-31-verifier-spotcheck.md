# Round 31 — verifier spot-check (tameshi)

author: hyaku closure (non-author integrator, @m_opus)

Scope: tameshi round 31 (L1 `TameshiR31`, attempt 1). Base `36c1d3933f680125aeefc447f07db0f03004901a`,
head `08125328f87df92d3f25d0034ee792253ecbcbd9`; measurement revision `83c001a5`, last SCORECARD commit
`67c0e013`. Fleet report `.ufo/reports/round-31/tameshi.md` at fleet commit
`1e2bdd275b1aaa4361ccdefb2e5dbfdd6c19e1e5`.

Driver digest (copied from `.ufo/watchdog.log`):
`2026-10-23T05:50:40-03:00 launch tameshi round=31 pgid=800710 driver=hyaku-inline attempt=1`;
`2026-10-23T07:14:27-03:00 complete tameshi round=31; hyaku-inline attempt=1`.

Re-check method: closure re-measurements over committed bytes (`git show`, `git diff`, `git log`, python
over `git show`, `sha256sum`, `curl`), plus five read-only closure seats (CloseT31Conform, CloseT31Counter,
CloseT31Size, CloseT31Sources, CloseT31NoHarm; none died). The lane's gates, counters and selftests
(`c1-measure.py`, `round-27/c1-measure.py`, command D, `tools/*`, `dead-seat-check.py`,
`bind-select-v5.py`) were **not executed** here (§Gate standard, closure consequence): their committed
receipts were evidence-verified, and the facts behind them were re-measured directly where plain commands
reach them.

## Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-31/tameshi.md` | `tameshi-shokunin 1e2bdd275b1a…` (07:14:04-03:00), one commit | pass |
| SHONEN heading, one line per box | report `## SHONEN` vs `grep -c '^- \[.\]' SHONEN.md` | 4 lines, all `[~]` with pointers; SHONEN.md has 4 boxes, same order; `git diff --stat 36c1d393 08125328 -- SHONEN.md` empty | pass |
| Cited commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` × 9 (36c1d393, c111dab5, ce1d7a64, 87eb64eb, 2da841bd, 3351738a, 83c001a5, 67c0e013, 08125328) | all exit 0; `git log 36c1d393..08125328` = the 8 round commits, all authored `tameshi-shokunin <tameshi@shokunin.local>` | pass |
| Pushed | `scripts/hyaku/jj-lane.sh state tameshi-shokunin` | `branch=master local=remote=08125328… ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| Leftovers | `git status --porcelain` | empty | pass |
| Late writes | `find tameshi-shokunin \( -name .git -o -name .jj \) -prune -o -newermt '2026-10-23T07:13:00-03:00'` | only the three `after/` final receipts (mtime 07:13:20), all tracked and committed in `08125328` (07:13:24) | pass |
| Prompt carries the template contract | python replica of `render_prompt()` (`scripts/shokunin-watchdog.sh:172-191`, template `templates/round-prompt.md`, `shokunin.conf:55` axes) vs `.ufo/prompts/tameshi-round-31.md` | rendered 8385 B is a byte-exact prefix; `## 6.` hyaku addendum starts at offset 8385; worktree equals committed `28e0d19` (05:50:38) | pass |
| Fleet-root misroot | `git -C /home/vgpnk/Projects/shokunin status --porcelain`; `ls .ufo/waves/round-31` (fleet) | no tameshi round-31 file; fleet `.ufo/waves/round-31` absent | pass |
| Marker report? | — | no; 8 landed commits with checkable work | status ok |

Conformance defects (status-neutral): none in step 1. Evidence gaps: no round-31 receipt for the base monitor
reading the report states ("base covered 64/64, restraint 8"; the round-30 closure verified 64/64 restraint 8
at `65b6e84f`), and `after/commandD-at-final.stdout` has no `.exit` file.

## Claim C1 — calibration (measured): verified

Frozen object: `git show {c111dab5,08125328}:.ufo/evidence/round-31/c1-measure.py | sha256sum` →
`657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584` at both, equal to `contract.json`
`counter_sha256`; `git diff --stat c111dab5 08125328 -- c1-measure.py contract.json` empty. Freeze precedes
every seat: `c111dab5` 09:01:22Z, child dispatch record `ce1d7a64` 09:04:17Z, wave-1 registry created
09:04:11.865Z (`w1/swarm-registry.json:4`), first seat receipt 09:05:40Z (`w1/SrcRustdoc.md:14`)
(CloseT31Counter).

Re-measured (plain python over `git show REV:SCORECARD.md`, CloseT31Size):

| Statement (base → head line) | Base claimed / observed | Head claimed / observed | Base row kind |
|---|---|---|---|
| sources-registry (240 → 1514) | 0,44 / 0,92 | 0,94 / 0,94 | dated literal |
| mutation sweep runner (241 → 1515) | 80,80,0 / 106,106,0 | 106,106,0 / 106,106,0 | dated; round-17 line 633 "95/95" stale current |
| six-leg regression ledger (242 → 1516) | PASS,6,6,0 / PASS,9,9,0 | PASS,9,9,0 / PASS,9,9,0 | dated; round-17 line 634 "cases=7" stale current |
| repeated pristine-control gate (243 → 1517) | PASS,29,0 / same | PASS,29,0 / same | match |
| six-leg content-disposition probe (244 → 1518) | 18,18,0 / 19,19,0 | 19,19,0 / 19,19,0 | dated; already superseded by 19/19 at 634 |
| exposed witness provenance correction (245 → 1519) | 39,39,0 / same | same | match |
| effective expectation reconciliation (246 → 1520) | 34,34,0 / 66,66,0 | 66,66,0 / 66,66,0 | dated; round-17 line 635 "56/56" stale current |
| retained invocation-context gate (247 → 1521) | 0,49,49 / same | same | match |
| hermetic env-differential probe (248 → 1522) | 9,9 / same | same | match |
| callback-authoritative wave accounting (249 → 1523) | 8,8 / same | same | match |
| depth (66 → 1536) | 6 / 9 | 9 / 9 | round-1 baseline |
| calibration (67 → 1537) | 0 / 8 | 8 / 8 | round-1 baseline |

- Claimed values: the independent extraction equals every `claimed=` in `before/c1-at-base.stdout:1-12`,
  `after/c1-at-83c001a5.stdout:1-12` and `after/c1-at-final.stdout:1-12` (zero disagreements); the rows
  selected at `83c001a5` and `67c0e013` are identical.
- Append-only: committed bytes, `head[:len(base)] == base` → True (118152 B → 127356 B, zero CR bytes);
  `git diff --stat 36c1d393 08125328 -- SCORECARD.md` → `73 insertions(+)`, no deletion;
  `git diff --name-only 67c0e013 08125328 -- SCORECARD.md` empty, and `git diff --stat 36c1d393 08125328 --
  tools/` empty, so the `67c0e013` reading carries to the head.
- Observed values: evidence-verified from the counter's committed receipts (base exit 1 `mismatches=7`;
  `83c001a5` and `67c0e013` exit 0 `statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1
  C1_R31_PASS=true`). Plainly re-measured: sources-registry 94 rows (`git show 67c0e013:corpus/SOURCES.md |
  grep -c '^| S[0-9]'` → 94; base 92) and census exit 0 (closure run below). Corroborated by independent
  older committed receipts with tools unchanged: `.ufo/waves/round-30/res/SampleBoundReads.md:92,97,111-112`
  (regression PASS cases=9 passed=9; 106/106), `.ufo/evidence/round-30/attempt3/evidence-disposition-selftest.txt:2-6`
  (66/66), `.ufo/waves/round-30/wC/SelftestsNoHarmHead.md:51-65` (49/49, 9/9, 19/19, 29 cases, 39/39),
  `.ufo/evidence/round-22/final/verification.json:39-40` (8/8); depth 9 and calibration 8 from
  `after/commandD-at-final.stdout` and `after/c1monitor-at-final.stdout:1`.

### §9 rulings on the two controls that met the counter

- **Receipt-copy route (CtlLabelShortcut static shape, CtlReceiptCopy V2): does not make C1 unverifiable.**
  The claimed property is agreement between a standing row and its command at REV, not who ran the command;
  `contract.json` `controls_before_data` names this route at `c111dab5`, before data. The counter re-executes
  every command at REV (`c1-measure.py:142,204`), so a stale copy fails (CtlReceiptCopy V1: 1 mismatch, PASS
  false, `w1/CtlReceiptCopy.md:90-105`), and a do-nothing round stays at 7 mismatches (`w1/CtlDoNothing.md:43-46`).
  The target is not reachable without making the rows true.
- **`| Axis | Score |` header (CtlWrongHeader C): a §9 predicate-identity defect, but it does not make C1
  unverifiable.** The code selects axis tables with `len(header) > 1 and header[1].startswith('Score')`
  (`c1-measure.py:116`); the contract surface says `| Axis | Score (0-10) |` tables. The plan sentence and the
  code condition differ, and the control shows the difference is real (loose 9/8 vs strict 6/0 on its
  sandbox, `w1/CtlWrongHeader.md:248,282-285`). It is not a skip of the claimed work: the passing control
  holds correct values. Both declared forms were frozen before data, so the closure judged C1 under the
  stricter one, the contract text. At `67c0e013` both axis tables use the exact header (`SCORECARD.md:64,1534`);
  strict and loose selection pick the same 12 rows, and strict selection over the committed observed tuples
  gives base 7 → after 0 (CloseT31Counter). The result does not depend on the looseness. Dissent recorded:
  CloseT31Counter ruled this control makes C1 "unverifiable under §9's predicate-identity requirement" while
  finding the 7 → 0 reading uncontradicted. This closure does not adopt that ruling, because the claim
  verifies under both frozen readings, and §9's voiding clause covers rules changed after data, which did not
  happen. The defect is routed (item 1 below) and was disclosed by the lane before data (lesson Mistake 5).
- Minor: the counter's append-only test is decoded-text `startswith` (`c1-measure.py:201`), not the byte prefix
  the predicate names. The closure byte check above holds, so it is harmless here; routed.
- MutCounter fixture gaps M07 (observe at base instead of REV) and M08 (exit forced to zero)
  (`w1/MutCounter.md:42-43`) are absent from the frozen counter (sha above). The after receipts record every
  command exit 0. [INFERENCE] Neither would change the recorded after tuples.

### Size of the gain (critics weighed)

The 7 → 0 reading is reproduced, but it is not seven repaired current misassessments. Three were stale
*current* counts in the round-17 supersession line (95/95, `cases=7`, 56/56, `SCORECARD.md:632-636` at base).
Four were dated literals: the fleet-round-1 sources count, the 18/18 that line 634 had already superseded, and
the round-1 depth/calibration baseline, whose current values 9 and 8 already appeared at 1308/1453/1475-1478.
The real gain is one consolidated, revision-named, command-checked current statement per standing row, with
three stale current counts corrected. It is a modest calibration move with no capability or score change
(calibration 8 → 8, depth 9 → 9). The report's own Gate rejects the "seven calibration errors" reading with this
decomposition, so the reported claim is not oversized.

## No harm (owned axes depth, calibration; others spot-read)

- Cold-read ledger `.ufo/evidence/round-21/coldread/ledger.json` (python over `git show`, CloseT31NoHarm): entries
  456 / 456 / 480 / 480 at base / `2da841bd` / `83c001a5` / head; `head[:456] == base` as data; non-entry keys
  equal; 24 new entries all `read_rev=2da841bd`, verdicts gap-minor 14, verified-record 8, executed-ok 2;
  equal to `coldread/append-receipt-w2.json`.
- Binding v5: sha256 `8760ddc9…1338` at head equals `contract-addendum-1.json`; added in `87eb64e`, unchanged to
  head; ancestry `87eb64e` (06:37:05) → `3351738` (wave-2 dispatch, 06:37:45) → `83c001a5` (data) holds. The
  addendum touches the no-harm instrument only, and the C1 counter sha is unchanged.
- Monitor receipts (evidence-verified): `after/c1monitor-at-83c001a5.stdout` and `after/c1monitor-at-final.stdout`
  `covered=64/64 restraint=8 box3_mismatch=0 depth_score=9`, exit 0; command D `recorded_cases=9 depth_score=9`.
  `git diff --stat 36c1d393 08125328 -- .ufo/evidence/round-27/ .ufo/evidence/round-21/coldread/measure.py
  .ufo/evidence/round-18/ tools/` is empty, so the monitor chain and every tool are unchanged.
- `SKILL.md`: one recipe line at `:1886` (per-seat `--workdir`, cwd check before kill). `corpus/QUALITY.md`: 98
  insertions, 0 deletions (criteria 66-71 plus errata). `corpus/SOURCES.md`: S055 `used-by` widened, S095/S096
  appended, round-31 note appended.
- Dead seat: CtlBindV5Fresh (wave 2, mutation-tester) died with `cyber_policy`. Its task text is not reused by
  any other wave-2 item (Jaccard < 0.3 against every item; dispatch `resume=0`). `dead-seat-check-w2.txt`
  flagged=0, exit 0. The round-30 FLAG (ConnectorOverlap) was confirmed from committed receipts only.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 verified: claimed rows and append-only re-measured, observed tuples evidence-verified and corroborated; gain is modest (see size) |
| depth | unchanged | command D 9 → 9 (receipt); `tools/` unchanged |
| coverage | unchanged | no claim; the new entry is lane ground the README row calls "not F1–F10, not held core", not a frontier move |
| freshness | unchanged | no claim; S055 re-opened (live page now 3.15.1) |
| operability | unchanged | `tools/` unchanged; per-leg tally check and 8 guard survivors re-deferred |
| adjacency | unchanged | tsukuroi SIGPIPE race reported, not absorbed (`w2/RegressionFlake.md`) |

Re-measured here: claimed values of all 12 statements (base, `83c001a5`, `67c0e013`), the byte prefix, counter
and binding hashes, freeze and dispatch ordering, ledger append, SOURCES rows 92 → 94, the census, source
digests and quotes. Evidence-verified only: the counter's observed tuples and PASS lines, monitor readings,
command D, selftest tallies, control receipts and binding-v5 receipts.

## Discernment spot-check (LEARNING.md)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S095 Go testable examples | admit (mined, 180d) | `curl -sL https://go.dev/blog/examples` (closure seat, 2026-10-23): 40059 B, sha256 `1a40ae77…958178` | agree | digest equals the pin; quote at HTML line 517 (inside 514-517), 11 words ≤ 25; `&rsquo;` rendered ASCII, as the lesson discloses |
| S096 rustdoc documentation tests | admit (mined, on-release) | `curl -sL https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html`: 51137 B, sha256 `95572c73…4de3cb7` | agree | digest equals the pin; quote at lines 181-182 verbatim (modulo `<code>` markup), 22 words |
| S055 doctest (re-opened) | admit as re-open, no new id | `curl -sL https://docs.python.org/3/library/doctest.html`: 216574 B, sha256 `cc245e8c…629ba21` (pin `369dcc17…cc46`) | agree | byte count equal; the footer reads `Last updated on Oct 23, 2026 (09:57 UTC)` (line 2205), so the page was rebuilt after the pin. The quoted bullet is intact (18 words). [INFERENCE] digest drift is the rebuild stamp only |
| SrcDoctest draft row (same URL as S055) | reject | `git show 08125328:corpus/SOURCES.md \| grep -c 'docs.python.org/3/library/doctest.html'` → 1; `w1/SrcDoctest.md` proposes `\| S095 \| doctest … <same URL>` | agree | a second row without `supersedes` would duplicate S055 (census E04) |
| SrcRustdoc id S095 | reject | `w1/SrcRustdoc.md` draft row `\| S095 \| Documentation tests …`; head S095 = Go (line 104), S096 = rustdoc (line 105) | agree | id collision. (The seat's report title says S097, but its draft row says S095; the lesson rejects the row as submitted.) |
| Binding v4 | reject before data | `ctl/bind-v5-real-r30.stdout` (63 assembled, 63 kept), `bind-v5-new-shapes.stdout` (9 shapes killed), `bind-v5-old-shapes.stdout`/`bind-v5-old-controls.stdout` (all `v4_kept: 0`); ancestry `87eb64e` → `3351738` | agree | v4 kept 63/63 forged entries (CtlBindV4New); v5 was re-scored before any wave-2 seat |

New SOURCES rows S095 and S096 (`corpus/SOURCES.md` lines 104-105 at head) and S055 (line 64): 11 columns each,
equal to the header; status, recheck and used-by match the lesson table (`round-31.md:37-41`);
`corpus/knowledge/executable-self-assessment.md` exists and cites all three.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ eight `W04` duplicate-URL warnings (S047, S048, S075, S076, S077, S078, S081, S092) and
`tameshi ok …/corpus/SOURCES.md`, exit 0 (byte-equal to `before/census-start.stdout` and
`after/census-end.stdout`).

## Trend verdicts

- **expansion: unprovable-but-better.** One new admitted entry (`corpus/knowledge/executable-self-assessment.md`)
  cites mined rows S055/S095/S096 and has a README row (`corpus/README.md:462`). That row and the SCORECARD
  block both say it is not a frontier move, and kumitate holds adjacent prior art, so net new uncovered ground
  is not shown.
- **quality: improved.** Three stale current self-assessment counts and four dated rows are superseded by one
  appended, revision-named statement per row that agrees with its command. The nine drifted sections
  re-verified through 24 fresh bound cold reads (64/64, restraint 8), and no admitted entry failed its re-check.
- **discernment: improved.** The spot-check agrees with the gate on three admits and three rejects. The
  header-selector gap the controls exposed became lesson Mistake 5 with a routed fix.

## SHONEN (operator note)

All four boxes stay `[~]`. Boxes 2 (end-to-end task: nine-leg regression PASS observed at `67c0e013`) and
3 (instructions executable: monitor 64/64 with transcript-bound fresh readers) look checkable by a non-author
from committed evidence. Promotion is operator-owned, so nothing is marked here.

## Routed defects (lane fixes next round)

1. Predicate identity: `c1-measure.py:116` accepts any second header cell starting `Score`, but the contract
   says `Score (0–10)`. The next contract quotes each selector's exact code condition, and one control per
   selector clause runs before freeze (lesson Mistake 5; not a retro-fix of C1).
2. The append-only test in `c1-measure.py:201` compares decoded text, but the predicate says byte prefix.
   Align code and text in the next counter.
3. Runner per-leg tally check and the 8 MutateHead guard survivors, now deferred twice (rounds 30 → 31 → 32).
   Land them or retire the route with a stated reason.
4. Evidence gaps: commit a base monitor receipt whenever the report states a base reading; give command D an
   `.exit` file.
5. Already routed by the lane, kept on the queue: MutCounter M07/M08 fixtures; dead-seat-check threshold and
   three survivors (M04, M05, M12); binding v5 FA-1..FA-3 and false rejects; `spec-w2.json` context naming v4
   (Mistake 7); SKILL sentence "processes it started"; QUALITY 69/71 errata; `mte-interop.py` SETUP on this host.
6. S055: the live page is now Python 3.15.1 with a new digest at equal length. On the next re-open, refresh the
   anchor and digest, or record the pinned bytes.
