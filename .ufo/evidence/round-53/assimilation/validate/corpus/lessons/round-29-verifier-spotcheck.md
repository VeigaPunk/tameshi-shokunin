# Round 29 — verifier spot-check (tameshi)

author: hyaku closure (non-author integrator, @m_opus)

Scope: tameshi round 29 (L1 `TameshiR29`, attempt 1, the repair-first round). Base
`367ec0f1d79cb9b67d724f2962e7554a0841b1fc`, head `3c16b3a649181b0dbfa386997de8c573f5bf7c3b`.
Fleet report `.ufo/reports/round-29/tameshi.md` at fleet commit `772f7105c422f8680b408d7d27bbedda952cbf6b`.

Driver digest (copied from `.ufo/watchdog.log`):
`2026-10-22T22:02:58-03:00 launch tameshi round=29 pgid=3655176 driver=hyaku-inline attempt=1`;
`2026-10-23T00:03:44-03:00 complete tameshi round=29; hyaku-inline attempt=1`.

Re-check method: closure re-measurements over committed bytes (`git show`, `git diff`, jq/python, sha256sum,
curl), plus five read-only closure seats (C1SelectionCritic, C1ShortcutCritic, C2TimingReviewer,
ContainmentReviewer, PromptConformanceReviewer). The lane counters `c1-measure-v2.py` and `c2-measure-v2.py`
were **not executed** here (§Gate standard, closure consequence). Their committed receipts were
evidence-verified, and the ledger and fixture facts behind them were re-measured directly.

## Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-29/tameshi.md` | `tameshi-shokunin 772f7105c422…` (00:03:26-03:00), one commit | pass |
| SHONEN heading, one line per box | read report `## SHONEN` | 4 lines, all `[~]` with pointers | pass |
| Cited commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` × 9 (9f3084bc, 6ab11a62, 09e4f273, bc2058a4, 7a45f7b9, 9bb699ad, 6892c3ee, 1a1e8b22, 3c16b3a6) | all hold; all authored `tameshi-shokunin`; `git log 367ec0f1..3c16b3a6` lists exactly these 9 | pass |
| Pushed | `scripts/hyaku/jj-lane.sh state tameshi-shokunin` | `branch=master local=remote=3c16b3a6… ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| Leftovers | `git status --porcelain` | empty | pass |
| Late writes after report | `find tameshi-shokunin -newermt '2026-10-23T00:03:30-03:00' -type f -not -path '*/.git/*' -not -path '*/.jj/*'` | empty. Last lane commit 3c16b3a6 at 00:02:07-03:00 (03:02:07Z), before the 03:03Z freeze and the report commit | pass |
| Prompt carries the template contract | seat PromptConformanceReviewer: rendered `templates/round-prompt.md` diffed against prompt lines 1–140 | exit 0 (byte-identical §1–5); all 5 round-level and 5 child-lane items present; L2 route map matches `MISSION.md`; hyaku addendum §6 at L141; prompt committed `f414a5c` | pass |
| Marker report? | — | no; 9 landed commits with checkable work | status ok |

Conformance defects (status-neutral):
- The report's "Measured commit" column names `6892c3ee`, `1a1e8b22` and `3c16b3a6` for both claims.
  Committed receipts exist only at `bc2058a4` (`c1-at-D.stdout`), `7a45f7b9` (`c1-at-E.stdout`, `c2-at-E.stdout`)
  and `9bb699ad` (`res/RerunC1Head.md`).
- The report's C2 "after" value `quote_located=1` appears in no committed receipt. `c2-at-E.stdout` reads
  `quote_located=0`, and the lesson line it needs landed in `9bb699ad`. C2TimingReviewer found the inputs
  byte-identical across the three head commits (blob hashes for fixtures, counter, entry and lesson),
  so the head value is inferred, not a receipt. The verdict (C2 false) does not depend on it.

## Claim C1 — calibration (monitor repair with seat binding): verified

Frozen counter and contract: `git diff 09e4f273 3c16b3a6 -- .ufo/evidence/round-29/c1-measure-v2.py
.ufo/evidence/round-29/contract-amendment-2.json .ufo/evidence/round-21/coldread/measure.py
.ufo/evidence/round-18/measure.py` is empty (C1SelectionCritic). `09e4f273` (22:26:47-03:00) precedes
`spec-w1.json`/`dispatch-w1.json` (22:26:57) and the first reader report (22:32:27).

Plain re-measurement of the ledger (`.ufo/evidence/round-21/coldread/ledger.json`, python over `git show`):

```
entries base 371  pre-data(09e4f273) 371  head 393
prefix_equal True            # head entries[:371] == base entries
nonentry_equal True          # every non-entry key equal
new entries read_rev: {'9f3084bc': 22}
new headings include '### Round-18 gate/probe registry — routed-defect c…': 2   # the one section uncovered at base
$ git diff --numstat 367ec0f1 3c16b3a6 -- .ufo/evidence/round-21/coldread/ledger.json
1781	0
```

Committed receipts (evidence-verified, not re-run):
- base `367ec0f1` (`ctl/C1v2-rescore.txt`, `res/RerunC1Head.md:74`): `covered=63/64 restraint=6 box3_mismatch=1 appended=0 bound=0`, `C1_R29_V2_PASS=false`.
- `bc2058a4` / `7a45f7b9` / `9bb699ad`: `covered=64/64 restraint=8 box3_mismatch=0 appended=22 bound=22 prefix_equal=1`, `C1_R29_V2_PASS=true`, exit 0.
- `git diff --name-only 7a45f7b9 3c16b3a6` touches no C1 input.

**Selection question: the frozen check applied as written, not a rule chosen after data.**
- The frozen binding (`contract-amendment-2.json`; `c1-measure-v2.py:132-157`) requires each appended
  entry's report to hold a json block with the entry's seat, `read_rev`, start, heading **and verdict**,
  and each seat to be a registry member.
- C1SelectionCritic re-implemented that predicate independently over the committed `assembled-w1.json`
  and `w1/swarm-registry.json`. Result: `kept: 22 dropped: 10 exact_match_receipt: True`, the same
  partition as `coldread/select-receipt-w1.json`.
- The 10 exclusions are assembler-normalized verdicts (report `executed-ok`/`verified-record` with minor
  gaps → entry `gap-minor`) and seat self-labels (`TameshiR29.Read*`). For example Read02A:
  `report_verdict executed-ok`, `entry_verdict gap-minor`.
- Exclusion cannot cherry-pick:
  - All 36 reports carry passing verdicts (`gap-minor` 10, `verified-record` 9, `executed-ok` 17), with
    no blocking gap and no wrong expectation.
  - Appending all 32 gives the same `covered=64/64 restraint=8 box3_mismatch=0`, failing only on
    `bound=22≠32` (`coldread/c1-dry-all32.txt`).
- The selection script `select-bound.py` was written after data, in `bc2058a4`. It reproduces the
  frozen predicate except that it omits `bool(reports)`, which has no effect here.
- The real defect is upstream, Mistake 5: the binding was frozen without testing the assembler's output
  shape, so 10 genuine passing reads went uncredited.

**Shortcut question: the target is shown to be beyond the shortcut by outside evidence, not by the round's controls.**
- Scored against v2: K1 do-nothing, K2 junk, K3 all-false, K4 no-reader (`ctl/C1v2-rescore.txt`), all
  `PASS=false`. Ledger-only and SHONEN-only edits cannot pass, because `restraint==8` needs the pinned
  monitor's `box3_full_page`.
- The contract's required class "shortcut keyed on ids or labels" (`contract.json`
  `controls_required_before_data`) was **never scored**:
  - CtlC1Shortcut and CtlC2Shortcut ended on `cyber_policy` refusals and were accepted as holds without
    a retry or a substitute.
  - The contract defines no hold path.
  - CtlC2Shortcut has no pre-data record at all (`res/ReviewControls.md`).
- The binding check is syntactic, so forged reports plus registry members would satisfy it.
- The closure checked the defence from outside instead. The host session store holds 36
  `TameshiR29.Read*.jsonl` seat transcripts:
  `ls ~/.omp/agent/sessions/-Projects-shokunin/2026-10-23T00-54-50-959Z_01a16640-…/TameshiR29 | grep -c '^TameshiR29\.Read[0-9]*[A-C]\.jsonl$'` → `36`.
- Bound seats Read01A, Read06A and Read10C each have a transcript that ends in their `COLDREAD` line.
  Their committed reports match the ledger entries on seat, `read_rev`, start, heading and verdict
  (C1ShortcutCritic).
- The Read02A transcript (`history://TameshiR29.Read02A`) shows a real traced read, including
  `REGRESSION: PASS (cases=9 passed=9 …)`.
- The 22 bound entries therefore rest on real seat work. The control gap is a discernment defect and is
  routed below. It does not falsify the measurement.

Verdict: **calibration improved.** Restraint 6 → 8 and box3_mismatch 1 → 0 are evidence-verified on
the frozen counter; the ledger append is re-measured.

## Claim C2 — coverage, frontier F6: missed (honest stop), confirmed

- Counter frozen: `git diff --shortstat 6ab11a62 3c16b3a6 -- .ufo/evidence/round-29/c2-measure-v2.py` is
  empty. The sha256 `adc721f9…ada4c` equals `contract-amendment-1.json` `counter_sha256`.
- Before (`c2v2-at-base.stdout`, rev `367ec0f1`): `fixture=absent`, `C2_F6_V2_PASS=false`, exit 1.
- After (`c2-at-E.stdout`, rev `7a45f7b9`): `fixture=present anchored=1 kill_original=0
  units_original=105 units_minimized=105 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=1
  quote_located=0`, PASS false, exit 1. The fixtures, counter and entry blobs are identical through
  `3c16b3a6`.
- Unreachable in principle under the pinned declaration: `grep -c '\texec\t755'` on the anchored
  `census.tsv` (sha256 `4af0dbcc…` = the pinned declaration) gives 3. B5 deletes only the exec-bit arm,
  and the exact-mode check still fires. The BuildF6B 512-mode sweep gives `WINNERS []`, and BuildF6A agrees.
- Timing (Mistake 1): `ctl/CriticC2v2.md`, which states that Q5 is unreachable, is dated 22:33:57-03:00.
  `task-adapter-w1.json` is dated 22:27:45-03:00 and registry `updatedAt` is 01:26:57Z, so the control
  report came 6 min 12 s after wave-1 dispatch.
  - Those are file mtimes cited in the lesson, not committed timestamps. No committed content
    contradicts them.

Verdict: **coverage unchanged** (target missed). The new entry is graded under expansion.

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | improved | C1 above: ledger 371 → 393 (append-only, re-measured). The frozen-counter receipts read `PASS=true` at bc2058a4, 7a45f7b9 and 9bb699ad, with the target verified to rest on real seat work |
| coverage | unchanged | C2 `PASS=false` at the frozen counter, and the target is structurally unreachable |
| depth | unchanged | depth command D `recorded_cases=9 depth_score=9` at base and head (report, CriticNoHarm). The SCORECARD diff asserts 9 → 9 |
| operability | unchanged | no claim; the SCORECARD block says unchanged |
| freshness | unchanged | no claim. The S059 stale anchor is carried and routed (below) |
| adjacency | unchanged | no claim; the ConnectorOverlap findings are report-only |

No-harm: `git diff 367ec0f1 3c16b3a6 -- SCORECARD.md` is +22 lines, append only. C1's row matches
`c1-at-E.stdout`, C2's row reads "none / missed (honest stop)", and no axis score changes without
backing. `git diff --stat 367ec0f1 3c16b3a6 -- . ':!.ufo'` touches LOG, SCORECARD, QUALITY, README,
SOURCES (2 +/−, S024 only) and the new entry and lesson. No harmed axis.

## Discernment spot-check

| Item (lesson `## Gate` / report Gate) | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S024 re-open → `mined` | admit | `curl -sL https://www.fuzzingbook.org/html/Reducer.html \| sha256sum` → `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99` | agree | The bytes are identical to the committed snapshot. Tag-stripped text contains "Its result is 1-minimal, meaning that every character contained is required to produce the error" verbatim (15 words) in the Delta Debugging section, after the MysteryRunner trace |
| S059 supersedes row not written (deferred to r30) | reject (deferral) | `curl -sL https://bazel.build/remote/caching.md \| sha256sum` → `266915c5d73f2cfe7d4ddcd9bb36a78e6037a710a71f2bab7d35b16d67768a5b`; `grep -c 'does not track tools outside a workspace'` → 2 | agree | The live markdown differs from the row's anchor `0d362d11…` and matches ReopenS059. The quoted claim still stands. Writing a SOURCES edit after the content revision would drift the cold-read credit (QUALITY 56), so the deferral is reasoned. It stays a routed debt |
| Cold-read report Read07A | reject (assembler format) | `git show 3c16b3a6:.ufo/waves/round-29/w1/Read07A.md` line 22: `"corpus/lessons/round-13-verifier-spotcheck.md": "6b8d2cafdab33c72"` | agree | The input digest is 16 hex characters, not a sha256; `assemble-w1.out:35` rejects it on exactly that ground |
| 10 passing entries excluded by the binding check (e.g. Read02A) | reject (binding) | `select-receipt-w1.json` `excluded_entries[0]`: `report_verdict executed-ok`, `entry_verdict gap-minor`. The independent re-implementation of the frozen predicate gives the same 22/10 | agree | It is the frozen check applied as written. Exclusion hides no failing read and does not change coverage; the cost is uncredited good reads (Mistake 5) |

SOURCES row re-opened: S024 (the only row touched; rows 89 → 89, none added). The anchor reads "§Delta
Debugging (fetched 2026-10-19)" and the section exists in the live page. The ≤25-word quote carried by
the lesson and the entry (15 words) was located verbatim, see above.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0,
`tameshi ok`, with the 7 W04 warnings S047, S048, S075, S076, S077, S078 and S081. This matches the
report's census end.

## Trend verdicts

- **expansion: improved.** `corpus/knowledge/survivor-fixture-minimization.md` is new ground:
  `git grep -il F6 367ec0f1 -- corpus/knowledge/` returns nothing. It is source-headed on S024, which
  is now `mined` with its quote re-located, and it cites the coverage-map row (README `## Frontier` F6).
  The entry records a measured negative finding (B5 masked by the 755 exec rows) and claims no kill.
- **quality: improved.** Twelve drifted SKILL sections were re-verified by 36 fresh cold reads at
  `9f3084bc`, none failing, and the monitor credit is restored to 64/64. Four sampled entries hold
  (SampleBoundReads). The entry was corrected after review (`6892c3ee`). No admitted entry failed its
  re-check. The stale S059 anchor is marked in the lesson and routed, not left silent.
- **discernment: improved.** The closure agrees with the gate on the admit (S024) and on three rejects
  (S059 deferral, Read07A, binding exclusions). The control wave caught the met C2 v1 and the unpinned
  C1 v1 before data.
  - Offsets, routed below: the required shortcut control class was never scored, and data was
    dispatched before a control report landed (Mistake 1).

## Verdict

C1 verified (calibration improved). C2 missed (honest stop), and no axis was harmed. **Not admitted**:
a declared claim did not verify. Status `ok`.

SHONEN: all four boxes are `[~]`. Box 3 now agrees with the monitor, but its readers are lane-dispatched
seats, so no box is checkable by a non-author from this round's evidence alone. Promotion is
operator-owned.

## Routed defects (lane fixes next round)

1. **Unscored shortcut control class.** CtlC1Shortcut and CtlC2Shortcut were held on `cyber_policy`
   without a retry or substitute, and the contract had no hold path. Before round-30 data, score a
   reworded "keyed on ids or labels" control against the frozen counters. Add a hold rule to the
   contract template: a refused required control blocks the data wave until it is replaced and scored.
2. **Binding is syntactic.** Bind each appended entry to an outside artifact as well, for example the
   seat transcript path in the host session store or the registry's `updatedAt`/agent id. Record that
   artifact in the ledger so a closure can check it without a session search.
3. **Assembler/binding shape mismatch** (Mistake 5). Bind against `effective_verdict` and canonical
   seat names, or make the assembler preserve report verdicts and labels. Test the frozen binding on a
   pilot assembly before the freeze. Add `bool(reports)` to `select-bound.py`. Re-credit the 10
   excluded reads only through a new frozen claim, never retroactively.
4. **Control-before-data ordering** (Mistake 1). The data wave must not dispatch until every control
   report has landed, checked by file presence and not by seat status. Commit timestamps or receipts
   for the ordering instead of relying on mtimes alone.
5. **Containment** (operator: runtime enforcement; lane: seat-prompt clauses):
   - (a) Misroot: Read10C wrote `.ufo/waves/round-29/w1/Read10C.md` at the fleet root. The file was
     untracked and was moved byte-exact (sha256 `fafd4c36…`) into the lane; the fleet path is now
     absent. Add an absolute-lane-path clause and a pre-assembly presence sweep.
   - (b) BuildF6B killed BuildF6A's processes (`w1/BuildF6B.md:350-354`, PID 2758108 and two
     children). Add "never kill a process you did not start; verify `/proc/<pid>/cwd`" to every wave
     context.
   - (c) BuildF6A, cancelled at 02:47Z, kept writing until 03:03Z. Only its own report changed
     (`git diff --stat 1a1e8b22 3c16b3a6`: `BuildF6A.md | 12+ 11-`), and it landed before the freeze.
     The runtime should kill a seat's process group at its deadline.
6. **Receipt gaps.** Commit a counter receipt at every revision a report names as "measured". Correct
   the report's C2 `quote_located=1` / head-commit claims in the round-30 report (an erratum, not a
   rewrite).
7. **Carried items:**
   - The S059 supersedes row is round 30's first SOURCES edit.
   - The runner leg-sum defect (MutateLegSum) is routed to round 30.
   - Mistakes row 1's falsifier rests on uncommitted mtimes; commit the evidence it rests on.
