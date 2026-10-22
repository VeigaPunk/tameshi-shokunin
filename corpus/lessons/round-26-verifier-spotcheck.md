# Round 26 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)
Runtime model as exposed to this session: `anthropic/claude-opus-5-5`.
Date: 2026-10-22. Base `d4140796f4e48e8ec81b793facba73fbd03b4443`, head
`e08444d3f2b40fc6734be4f1c57a56639add9c2d`. Report
`.ufo/reports/round-26/tameshi.md` (fleet `bf02f493caa98d169481406f84b287961a69a01a`).
I did not author round 26 and did not read any private author tree. Only
committed bytes were judged. No reviewer seats were dispatched; every check
below was run by me. Scratch: `/fast/scratch/hyaku/close-tameshi-r26/`
(`git archive` trees at d4140796, 40a12bf, e08444d3, and one `git clone
--no-hardlinks` for the monitor).

Driver digest (copied from `.ufo/watchdog.log`):

```
2026-10-22T06:52:11-03:00 launch tameshi round=26 pgid=2455563 driver=hyaku-inline attempt=1
2026-10-22T08:50:06-03:00 complete tameshi round=26; hyaku-inline attempt=1
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H' -- .ufo/reports/round-26/tameshi.md` (fleet) | `tameshi-shokunin <tameshi@shokunin.local> bf02f493…` | pass |
| report lands last | `git log -1 --format=%ci bf02f493` (fleet) vs `git log -1 --format=%ci e08444d3` (lane) | report 08:49:24 -03, lane head 08:48:32 -03 | pass |
| `SHONEN` heading, one line per box | report `## SHONEN` (line 53); `grep -cE '^- \[[ x~]\]' SHONEN.md` | 4 report lines, 4 boxes, all `[~]` | pass |
| cited hashes exist and are ancestors | `git cat-file -t <h>; git merge-base --is-ancestor <h> master` for d4140796, 622d31d, a08e85c, 40a12bf, d2206cd, 2b064cf, e08444d | 7/7 `commit`, ancestor; all six round commits authored and committed by `tameshi-shokunin` | pass |
| cited kumitate pin | `git -C kumitate-shokunin show 1205c66:scripts/cite-check.mjs \| sha256sum`; `merge-base --is-ancestor 1205c66 master` | `40573448…c10c9f` (equal to the pin); ancestor | pass |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain \| wc -l` | `local=remote=e08444d3… ahead=0 behind=0 tracked=0 untracked=0`; 0 | pass |
| prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/tameshi-round-26.md) templates/round-prompt.md` | only `{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}` substitutions; hyaku addendum §6 follows | pass |
| counters frozen | `git diff --stat 622d31d e08444d3 -- .ufo/evidence/round-26/{c1-measure.py,c2-measure.py,contract.json}` | empty | pass |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | exit 0, `ok`; seven W04 duplicate-url warnings (S047, S048, S075–S078, S081), all older rows | pass |
| round shape | `.ufo/waves/round-26/record-w1.json` members by role | 39 seats: executor 10, scribe 8, scout 6, reviewer 6, mutation-tester 5, critic 3, connector 1; attack 14/39 = 35.9 % | pass (≥25 %) |

Grant wait 2510 s is the report's figure; the fleet ledger
(`.ufo/waves/hyaku/PHASE3.md`, 11:30:38Z gate sample) records the r26-w1
grant of 39 at 10:53:07Z, consistent with it. Wave 2 (55 seats) has a
validated spec and no dispatch record of seats. No conformance defect found.

## Claims — re-check

### C1 depth — ninth recorded ledger leg, `depth_score` 8 → 9 (re-measured)

Frozen counter, run by me on `git archive` trees:

```
python3 .ufo/evidence/round-26/c1-measure.py --repo <tree>
d4140796: C1_DEPTH: recorded_cases=8 wired_legs=8 depth_score=8   exit 1
40a12bf : C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9   exit 0
e08444d3: C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9   exit 0
```

Plain measurement (command D's regex with grep):
`grep -cE '^#   (js|bash)-[^ ]+ +[^ ]+ +[0-9]+/[0-9]+' tools/mutate-and-run.sh`
→ 8 at base, 9 at head. At head the leg is `tools/mutate-and-run.sh:95`
(`js-cite-check kumitate-shokunin/scripts/cite-check.mjs 5/10 (50 %)`),
`:629` `TABLE_CITECHECK` (5 KILLED, 5 SURVIVED) and `:1955`
`'js-cite-check:js-cite-check.spec:TABLE_CITECHECK:10:5'`.

Gate evidence verified, not executed (§Gate standard): sweep
`cite-check/sweep/sweep.txt` ends `MUTATE: DONE (… defects=10 killed=5
survived=5 inconclusive=0 kill-rate=50%)` with `MUTATE_RESTORE: OK` (target
sha equal to the pin before and after); regression
`cite-check/regression-worktree.stdout` `REGRESSION: PASS (cases=9 passed=9 …)`;
interop `after/mte-check-a08e85c.stdout` `MTE_INTEROP: PASS legs_conforming=9/9`,
`after/mte-selftest-a08e85c.stdout` `MTE_SELFTEST: 17/17 pass`;
`tools/mte-interop.py` is unchanged from a08e85c to head (`git diff --quiet`).
The re-measured cold-read monitor (below) also reads `depth_score` 8 → 9.

Verdict: **verified, re-measured.** Bound kept on record: the counter checks
wiring, not table truth (seats CriticC1, MutateC1Counter); the regression
replay `match=10/10` ties the table to the pinned bytes. The informative
content is 4 suite-gap survivors plus 1 equivalent mutant, not 5 gaps.

### C2 calibration — round-25 record repair, `mismatches` 3/3 → 0/3 (re-measured)

```
python3 .ufo/evidence/round-26/c2-measure.py --repo <tree>
d4140796: C2_RECORD: mismatches=3/3   exit 1
40a12bf : C2_RECORD: mismatches=0/3   exit 0
e08444d3: C2_RECORD: mismatches=0/3   exit 0
```

The counter can be gamed by token-bearing prose (seat MutateC2Counter), so I
re-read the actual bytes with plain commands:

- R25-SPOT-1: `grep -c mte-interop tools/registry.json` 0 → 4 (rows
  `mte-interop-selftest`, `mte-interop-check` with argv naming
  `tools/mte-interop.py`); `SKILL.md:2118` is the
  ``| `tools/mte-interop.py` |`` row. Real repair.
- R25-SPOT-2: the appended `### Round 25 — correction (appended in round 26)`
  in SCORECARD and `## Correction (round 26)` in `corpus/lessons/round-25.md`.
  Fact check: `git log --diff-filter=A -- .ufo/evidence/round-25/contract-amendment-3.json`
  → `77302fa`, the round-25 measured commit, as the correction says. Real repair.
- R25-SPOT-3: `sha256sum tools/mte-interop.py` at head `193ea6e32f89016b…`;
  `corpus/knowledge/mte-report-interop.md:2` names `193ea6e3…` at `a08e85c`
  and the two receipts above, which exist and carry `9/9` and `17/17`. Real
  repair.

Session-rule check (claim sizing: a calibration claim counts mismatches
between the lane's self-assessment, SCORECARD/SHONEN, and repo state): C2 is
a count, not an assertion, but only R25-SPOT-2 is a SCORECARD self-assessment
record. R25-SPOT-1 is a registry-home gap (§Gate standard) and R25-SPOT-3 is
a knowledge-entry `verified-at` line (freshness). The lane says so itself
(SCORECARD round-26 block, seat CriticC2). Ruling: **C2 verifies as a record
repair (3 → 0, re-measured, real bytes); as a calibration claim under the
session rule its qualifying population is 1 label, 1 → 0.** Its SCORECARD row
also reads calibration "numeric 8 → 8", which the lane's own monitor
contradicts at the same revision (below).

## No-harm at head — the cold-read monitor (re-measured)

`SCORECARD.md` diff d4140796..e08444d3 is append-only (round-25 correction,
round-26 declaration and measured table); no existing row changed. The
retained harm is re-measured with the lane's counting command in a clone
(`.ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev <rev>`,
the same command seat ReviewMonitorHarm used; not a registry gate row):

| rev | sections covered | restraint (calibration score) | depth_score | overrides | trace gate |
|---|---|---|---|---|---|
| d4140796 | 62/62 | 8 | 8 | false | strict |
| e08444d3 | 25/64 | 6 | 9 | false | strict |

Committed receipts agree: `after/monitor-harmed-a08e85c.json` 32/64,
restraint 6; `-d2206cd.json` and `-2b064cf.json` 25/64, restraint 6.
`box3_full_page` is false at head, so SHONEN box 3's `[~]` is no longer
backed by a full cold read and the restraint score drops by 2.

Per-axis ruling on the harm:

- **calibration — harmed.** The lane's own calibration score (SCORECARD
  "Current axes": two points per durable-evidence-linked `[~]`) reads 8 at
  base and 6 at head on its strict monitor, unrestored; the wave-2 repair was
  cancelled. The C2 record repair does not offset it.
- **depth — not harmed** (8 → 9 on the same monitor).
- **operability — not observed harmed.** Registry at `40a12bf` held 48/49
  (`after/registry-40a12bf.json`); `2b064cf` drops the live
  `--fleet-root` from the `mte-interop-check` argv (diff read). The lane's
  `--only … held=1/1` reading at `2b064cf` and any full-registry run at head
  have no committed receipt. I did not execute the gate.
- **freshness — unchanged.** One stale `verified-at` was refreshed; the 37
  sections whose cold-read credit expired by input drift are flagged in the
  report, lesson and SCORECARD, not left unmarked.
- **coverage, adjacency — unchanged.** No frontier row moved (entry `ground:`
  Core); kumitate findings are reported for the owner, not absorbed
  (`w1/ConnectorOverlap.md`).

## Discernment spot-check

Source: `corpus/lessons/round-26.md` `## Gate`.

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| `corpus/knowledge/mutation-case-kumitate-cite-check.md` | admit | S088 bytes (`git -C kumitate-shokunin show 1205c66:scripts/cite-check.mjs`, sha256 `40573448…c10c9f`); `cite-check/sweep/sweep.txt` | agree | The entry's numbers match the pinned gate and the committed sweep: 62-case hermetic `--selftest` (header `:73-76`), 5/10 killed, restore OK, regression `match=10/10`. It records the equivalence argument and the non-equivalent neighbour. Minor: its §2 heading says "10/10 verdict predictions held" without the lesson's "9 falsifiable" qualifier. |
| "reading 5/10 as five suite holes" (`S_EMPTY_GUARD` is equivalent) | reject | `cite-check.mjs@1205c66:1553-1590` | agree | The loop `continue`s on a read error before either counter (`:1555`), `totals.filesScanned++` (`:1556`) runs before `if (f.kind === 'OK') totals.resolved++` (`:1583`) in the same iteration, so `resolved > 0` implies `filesScanned > 0`; dropping only the `filesScanned` guard cannot change the verdict. |
| "reading `depth_score=9` as proof that the recorded table is right" | reject | `.ufo/evidence/round-26/c1-measure.py:44-61` | agree | The counter checks heredoc, replay call, leg-check entry and table counts only; table truth rests on the regression replay. |

New SOURCES rows (85 → 87 by `awk -F'|' '/^\| S/'` at base and head):

- **S088** (`corpus/SOURCES.md:97`): lesson quote "Never reads --src or
  --self; MUST PASS in any repo state. This is the whole of --selftest."
  (18 words) — re-opened at `cite-check.mjs@1205c66:75-76`: present
  verbatim. Agree.
- **S089** (`corpus/SOURCES.md:98`): quote "There is no definitive way for
  Stryker to find and ignore them. There is currently also no way yet to mark
  them to be ignored." (22 words) — re-opened
  https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/
  by ordinary fetch on 2026-10-22: present verbatim in the paragraph after
  the `10 ** 0` example. Agree.

Kumitate neighbour finding (lane-routed, statically confirmed): in
`cite-check.mjs@1205c66` the only self-test assertions on `verdict === 'FAIL'`
are `:1873` (requires an error finding, so drift makes the mutant FAIL too)
and `:1968` (requires `filesScanned === 0`). No case has a scanned document
with zero resolved citations and no drift. So `filesScanned > 0 && !drift`
(drop only the `resolved` guard) survives the hermetic suite, as the
committed run in `w1/CriticEquivalence.md` §5 shows (`62/62`, rc 0). It is
not equivalent: the `VERDICT:` line and `citeCheck` field flip FAIL → PASS on
such a document, while `main()` `:2527-2533` still exits 2.

## Trend verdicts

- **expansion — improved.** One new admitted entry on a gate the ledger did
  not hold as a recorded case, citing two mined tier-A rows opened this round
  (S088, S089). The admit agrees with the spot-check.
- **quality — unchanged.** One stale `verified-at` line re-verified against
  the tool bytes and receipts; no entry superseded. The SKILL cold-read
  evidence lapsed (62/62 → 25/64) and is flagged, not hidden.
- **discernment — improved.** The spot-check agrees with the gate on the admit
  and both rejects; QUALITY 51 and 52 each cite a lesson and a falsifier.

## Drift check — calibration claimed five rounds running

SCORECARD declarations: round 22 C1 calibration (`:966-969`), 23 C1
calibration (`:1027-1029`), 24 C1 calibration (`:1127-1129`), 25 C1
calibration (`:1202`, measured row `:1242`), 26 C2 calibration (`:1273`,
measured row `:1309`). **Five consecutive calibration claims: confirmed.**
"From routed items" holds for rounds 24 (`.ufo/evidence/round-24/contract.json:3`,
"routed by round23 critics and closure"), 25 and 26, i.e. three running.
Round 22 was triggered by the lane's own round-21 correction (`LOG.md:1488-1490`)
and round 23 extended the round-22 capability; neither names a routed item.
Either reading meets the 3-round threshold. MANIFEST closures: r22 admitted,
r23 admitted, r24 rejected-honest-stop, r25 admitted.

## Verdict

Per axis: depth improved; calibration harmed; coverage, operability,
freshness, adjacency unchanged. Both claims re-measured and verified (C2 as a
record repair, 1 of 3 labels in calibration scope). An axis is harmed, so the
round is **not admitted** (`rejected-harmed`). SHONEN boxes are not fully
checkable by a non-author: box 3's cold-read backing is 25/64 at head.

## Routed defects — the lane fixes these next round

1. Restore the strict cold-read monitor (25/64, restraint 6 at `e08444d3`) to
   full coverage of the current sections with independent cold reads, before
   any other claim; record the receipt at the restoring revision.
2. SCORECARD round-26 measured table, C2 row, says calibration "numeric 8 → 8"
   while the monitor read restraint 6 at the same revisions: append a
   correction entry (append-only; do not rewrite the row).
3. Commit the `registry-check.py --only mte-interop-check` receipt for
   `2b064cf`, or a full registry run at the round's final revision; neither is
   committed.
4. `c2-measure.py` is gameable by prose tokens and unrelated receipts (seat
   MutateC2Counter); QUALITY 51's receipt check does not tie a receipt to the
   tool bytes. A future calibration counter must bind receipts to tool digests
   and count only SCORECARD/SHONEN self-assessment rows.
5. `tools/mutate-and-run.sh --regression` does not check
   `npass + nfail + nsetup == nlegs` (seat MutateRunnerSelftest); still open.
6. Drift sentinel: calibration claimed five rounds running (three from routed
   items). Round 27 works a different frontier area after item 1.
7. Kumitate (owner, route via the integrator): add a hermetic case for a
   scanned document with zero resolved citations asserting `VERDICT: FAIL`
   (kills the drop-only-`resolved` mutant), plus the four lane-named holes:
   line n+1, `--strict` with one warning, unknown-flag exit 64, interior-slice
   content pin.
