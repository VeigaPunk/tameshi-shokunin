# Round 30 — verifier spot-check (tameshi)

author: hyaku closure (non-author integrator, @m_opus)

Scope: tameshi round 30 (L1 `TameshiR30A3`, attempt 3; attempts `TameshiR30` and `TameshiR30A2` died with
the orchestrator at 05:25:25Z and 06:19:06Z). Base `9ed6db840dc97a0a5f4758b6b5f60cee83a61645`, head
`8abf67c05cc31b46cba6dc7d892dcdcab0714889`. Fleet report `.ufo/reports/round-30/tameshi.md` at fleet
commit `3ed950636d69c5690069643460701b4917b6c7ac`.

Driver digest (copied from `.ufo/watchdog.log`):
`2026-10-23T01:45:23-03:00 launch tameshi round=30 pgid=2450711 driver=hyaku-inline attempt=1`;
`2026-10-23T02:26:38-03:00 lane-dead-no-report tameshi round=30; retry same round (attempt 1: L1 died with the orchestrator process exit at 05:25:25Z)`;
`2026-10-23T02:26:39-03:00 launch tameshi round=30 pgid=2558324 driver=hyaku-inline attempt=2`;
`2026-10-23T03:40:27-03:00 lane-dead-no-report tameshi round=30; retry same round (attempt 2: L1 died with the orchestrator process (omp SIGSEGV) at 06:19:06Z)`;
`2026-10-23T03:40:29-03:00 launch tameshi round=30 pgid=3137686 driver=hyaku-inline attempt=3`;
`2026-10-23T05:25:19-03:00 complete tameshi round=30; hyaku-inline attempt=3`.

Re-check method: closure re-measurements over committed bytes (`git show`, `git diff`, python over
`git show`, sha256sum, curl), plus four read-only closure seats (CloseBindRestore, CloseC1Judge,
CloseSpotSources, CloseBreaches; none died). The lane's gates and selftests (`tools/mutate-and-run.sh
--regression`/`--selftest`, `c1-measure-v4.py`, `round-27/c1-measure.py`, command D) were **not executed**
here (§Gate standard, closure consequence); their committed receipts were evidence-verified, and the
ledger, binding and source facts behind them were re-measured directly.

## Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-30/tameshi.md` | `tameshi-shokunin 3ed950636d69…` (05:24:52-03:00), one commit | pass |
| SHONEN heading, one line per box | read report `## SHONEN` | 4 lines, all `[~]` with pointers | pass |
| Cited commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` × 14 (9ed6db84, dcdf2d08, e59728df, 8a8d2540, f09d3425, 713dee6a, bb681566, 07ed440a, 9207f226, a2fa6c92, 4df5107f, 65b6e84f, 957c5ddb, 8abf67c0) | all hold; `git log 9ed6db84..8abf67c0` lists exactly the 13 round commits, all authored `tameshi-shokunin` | pass |
| Pushed | `scripts/hyaku/jj-lane.sh state tameshi-shokunin` | `branch=master local=remote=8abf67c0… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git ls-remote origin refs/heads/master` → `8abf67c0…` | pass |
| Leftovers | `git status --porcelain` | empty | pass |
| Late writes after report | `find tameshi-shokunin -newermt '2026-10-23T05:24:00-03:00' -type f -not -path './.git/*' -not -path './.jj/*'` | empty; last lane commit `8abf67c0` at 05:24:03-03:00, before the report commit | pass |
| Prompt carries the template contract | render `templates/round-prompt.md` with `render_prompt()`'s substitutions (lane `tameshi`, round 30, conf axes `depth + calibration (verification-fixture craft)`) and compare with `.ufo/prompts/tameshi-round-30.md` | rendered 140 lines are a byte-exact prefix of the prompt (`startswith` True); hyaku addendum §6 begins at L141; worktree prompt equals committed `1fad9bc`; no L2 route map is quoted, so no `MISSION.md` bucket comparison applies | pass |
| Fleet-root misroot | `ls /home/vgpnk/Projects/shokunin/.ufo/waves/round-30`; `git -C /home/vgpnk/Projects/shokunin status --porcelain --ignored`; grep for `ColdA01` over fleet `.ufo/` | path absent; no ColdA01 file, tracked, untracked or ignored; `git log --all --diff-filter=A -- '*ColdA01*'` empty (CloseBreaches). Untracked fleet-root files (`write`, `s395.txt`, `*.html`, `bm.json`, `AGENTS.md`) all have mtimes on or before 2026-10-22 20:37 -03:00, before round 30's first launch | pass |
| Marker report? | — | no; 13 landed commits with checkable work | status ok |

Conformance defects (status-neutral):
- The report's Gate and the SCORECARD row call JudgeC1 a "named non-author judge"/"named non-author seat".
  JudgeC1 was dispatched by the L1 and is still the lane (LEARNING.md §Discernment: "A subagent the lane
  dispatched is still the lane"; AXES.md: "a dispatched subagent does not count"). The C1 ruling below is
  therefore this closure's own; JudgeC1's report is supporting evidence only.
- The lesson cites the S094 paragraph of the knowledge entry as `:60-62`; the paragraph is line 60 only
  (61 blank, 62 `## Limits`) (CloseSpotSources).

## Claim C1 — operability (exploratory): `unprovable-but-better` (ruled by this closure)

Judged object: `bb681566`; `git diff bb681566 8abf67c0 -- tools/mutate-and-run.sh` is empty, blob
sha256 `a7d3f2dd…2eb9` at both (CloseC1Judge), so the head carries it unchanged.

Code read (`git show 8abf67c0:tools/mutate-and-run.sh`):
- Guard `:1456-1460`: `if (( npass + nfail + nsetup != nlegs ))` → `REGRESSION: SETUP (case-tally mismatch:
  cases=%s counted=%s)`, exit 2. `nlegs` is the literal `local nlegs=9` (`:1432`), matching the nine
  `st_*=$?` assignments (`:1390-1430`); `counted` is the loop sum (`:1433-1439`). Two independent sources,
  not a tautology; on the pristine nine-operand loop the sum is always 9, so the guard cannot fire on a
  legitimate run.
- Harness (`git diff 9ed6db84 bb681566 -- tools/mutate-and-run.sh`, selftest hunk `@@ -1975`): awk extracts
  the real tally block from `$SELF`, takes leg names from the `st_*=$?` assignments (not from the loop),
  writes `tally(){ local st_*=S …; <block> }` and runs it under `bash`. It checks exact first line and exit
  for all-pass, one FAIL/SETUP status at each of 9 positions, four mixed vectors, and a guard stress that
  deletes the loop's last operand and requires `cases=9 counted=8`, exit 2. This executes the block; it does
  not model it.

Committed evidence (evidence-verified, not re-run; CloseC1Judge path:line):
- Base false PASS on the dropped-leg mutant: `.ufo/waves/round-29/w1/MutateLegSum.md:104,108,112`
  (`REGRESSION: PASS (cases=9 passed=8; …)`, exit 0); at head with the guard disabled the same:
  `wC/RegressionReplayHead.md:172`.
- Head refusal and detector: `wC/JudgeC1.md:22` (mutant selftest `98/106`, `VERDICT: FAIL, EXIT=1`);
  pristine head selftest `106/106` (`JudgeC1.md:14`, `SelftestsNoHarmHead.md:97`); base selftest `97/97`
  (`SelftestsNoHarmHead.md:49,95`). 106 = 97 + 9 new cases; on the mutant 8 of the 9 new cases fail.
- Supporting counter: `v4/head.stdout:59-61` `refused_drops=9/9 … C1_R30_PASS=true` vs `v4/base.stdout:47-48`
  `refused_drops=0/9 … false`; `RerunC1Head.md:8` reproduces head.stdout at `bb681566`. Not the verdict:
  CtlS2SymEval also meets v4.
- Declaration before content: `git merge-base --is-ancestor 713dee6a bb681566` → 0 (713dee6a 03:08:50-03:00,
  bb681566 03:11:04-03:00).

Ruling: **`unprovable-but-better`**. Reasons: the named defect (a dropped tally leg printing a false PASS,
round-29 routed item 7) is now refused at run time and caught by the selftest, with committed before/after
outputs; the guard has no false-alarm path by construction; the harness runs the real block. Why not a
countable verdict: four counter versions were met by controls before data and the last one cannot separate
running the block from modelling it; the runtime check is sum-only (a duplicate-one/drop-one miscount still
prints PASS and is caught only by the selftest); MutateHead leaves 8 real selftest survivors (T08, H03, H04,
H05, N01, N02, N03, N05), routed by id at `corpus/lessons/round-30.md:207-211`. Better than base, not complete.

## Calibration no-harm restoration (owned axis): verified real, not a re-scoring

Plain re-measurement of `.ufo/evidence/round-21/coldread/ledger.json` (python over `git show`):

```
entries base 393  9207f226 393  4df5107f 456  head 456
prefix_equal True            # head entries[:393] == base entries (as data)
nonentry_equal True          # every non-entry key equal; 4df5107f == head
new entries read_rev: {'bb681566b18211adf8ae9c28df91e17678e3f545': 63}
new verdicts: gap-minor 35, verified-record 22, executed-ok 6
new-entry input sha256 vs blobs: 832 inputs, 0 mismatch at bb681566;
  1 mismatch at head = entry 58's own input ledger.json (self-reference; the append changes it)
$ git diff --numstat 9ed6db84 8abf67c0 -- .ufo/evidence/round-21/coldread/ledger.json
3924	0
```

The append is equal as data, not as a byte prefix (the JSON tail is re-serialised at byte 2247478,
`}` → `},`); `append-receipt-wC.json` claims only data equality, which holds (CloseBindRestore).

- Monitor unchanged: `git diff --stat 9ed6db84 8abf67c0 -- .ufo/evidence/round-27/` is empty; its chain
  `round-21/coldread/measure.py` and `round-18/measure.py` are blob-identical (CloseBindRestore). The monitor
  reads SKILL sections, entry fields (`start`, `skill_sha256`, `heading`, `inputs`, `read_rev`, `traces`) and
  committed trace receipts; it never reads the `binding` field or a binding script. A binding change cannot
  re-score existing entries; the 64/64 comes from 63 new entries read at `bb681566`.
- Binding v3 frozen before data: added in `9207f226` (`git log --diff-filter=A`), sha256 `6f3a66bb…8b44` at
  head equals the hash recorded in `attempt3/bind-controls.txt:2`; `git diff --stat 9207f226 8abf67c0 --
  coldread/bind-select-v3.py` empty; ancestry `9207f226` → `a2fa6c92` (dispatch 04:14:15-03:00) → `4df5107f`
  (data 04:52:47-03:00) holds. v2 (`bind-select.py`, sha256 `1a48a519…3384`, last changed `07ed440a`) is
  not used for the wave-C assembly.
- Controls (`attempt3/bind-controls.txt:3-14`): v2 do-nothing `kept 32` exit 0 (rejected before data);
  v3 do-nothing, prompt-only, prose-mention, no-result `kept 0` exit 1; real r29 `kept 31`; forged `kept 30`.
- Forged-shape exposure: CtlBindV3 lists five shapes v3 still keeps (names in another tool's intent, error
  result, shell comment, result before call, reused call id). The post-data audit (`audit-bound-wC.py`)
  requires a `bash` call naming `trace-inputs.py --out <trace>`, a later non-error result with the same id
  and a trace `rev` equal to `read_rev`, which kills all five; `audit-bound-wC.out` ends `AUDIT:
  traces_ok=211 traces_fail=0`. Independent sample by CloseBindRestore (entries 0/21/42/62 → ColdA01,
  ColdA08, ColdB04, ColdB11): bound transcripts exist under `~/.omp/agent/sessions/`, size and sha256 match
  the binding, every cited trace maps to a real `bash` call with a later non-error result.
- Monitor receipts (evidence-verified): `head/c1monitor-at-bb681566.stdout` `covered=33/64 restraint=6
  box3_mismatch=1` exit 1; `head/c1monitor-at-4df5107f.stdout` and `head/c1monitor-at-65b6e84f.stdout`
  `covered=64/64 restraint=8 box3_mismatch=0` exit 0; `monitor-at-base.stdout` 64/64 restraint 8.
  `res/RerunMonitorHead.md` reproduces base, `bb681566` and `957c5ddb`.

## Other axes

- Depth (owned): `head/depth-shonen-at-65b6e84f.stdout` `recorded_cases=9 depth_score=9`, equal to base
  (evidence-verified). SCORECARD diff (`git diff 9ed6db84 8abf67c0 -- SCORECARD.md`): one appended
  18-line Round 30 block, no other change; calibration 8 → 8, depth 9 → 9.
- Operability no-harm (evidence-verified): nine-leg `REGRESSION: PASS (cases=9 passed=9 …)` exit 0 at
  `bb681566` (`RegressionReplayHead.md:112-114`); every `tools/*.py` selftest has equal exit at base and
  `bb681566` (SelftestsNoHarmHead); `attempt3/evidence-disposition-selftest.txt:2-6` 66/66 at both.
- Coverage, freshness, adjacency: no change claimed; nothing found harmed.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | unprovable-but-better | C1 ruling above (this closure, non-author) |
| calibration | unchanged | monitor 64/64 restraint 8 at base and `65b6e84f`; restoration re-measured real |
| depth | unchanged | command D 9 → 9 (receipt) |
| coverage | unchanged | no claim; README row is core ground |
| freshness | unchanged | no claim; S092–S094 re-opened with equal digests |
| adjacency | unchanged | no claim; ConnectorOverlap no sibling overlap |

Re-measured here: ledger append, entry input hashes, binding script hashes and ordering, monitor/binding
file identity, SOURCES row count 89 → 92 (`git show <rev>:corpus/SOURCES.md | grep -c '^| S[0-9]'`),
census, source digests and quotes. Evidence-verified only: monitor readings, command D, runner selftest
tallies, nine-leg replay, v4 counter receipts.

## Discernment spot-check (LEARNING.md)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S093 bwrap.xml v0.13.1 | admit | `curl https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml` (closure, 2026-10-23): sha256 `2cb77df2…be1da`, 33289 B | agree | digest equals the row pin; bwrap.xml:159 quote located verbatim, 13 words (≤25); tag commit `362936ae…` equals the row (CloseSpotSources) |
| S094 arXiv:1411.2664v3 | admit | `curl https://arxiv.org/pdf/1411.2664v3` + `pdftotext` (CloseSpotSources): sha256 `6e9532a9…0d697`, 322643 B | agree | digest equals pin; §1 printed page 2 sentence located verbatim, 17 words |
| S092 bazel remote caching | admit (`queued`) | `curl https://bazel.build/remote/caching.md` (CloseSpotSources): sha256 `266915c5…768a5b`, 16210 B | agree | digest equals pin; line 345 quote, 9 words |
| Knowledge entry "cleared environment" | reject (erratum E1) | bwrap.xml:233-235 (closure re-open): `--clearenv` unsets all variables "except for PWD and any that are subsequently set by --setenv"; `c1-measure-v4.py:321-326` then sets PATH/HOME/LANG/TMPDIR | agree | "cleared" overstates; E1 (`regression-tally-completeness.md:72`) states the exact scope |
| Knowledge entry S094 paragraph | reject (erratum E2) | arXiv:1411.2664v3 §1 | agree | §1 describes a leaderboard holdout overfitting after returned scores; "defeats allowlists" and the control-round extension are the entry's inference; E2 (`:73`) says so |
| Binding v2 | reject | `attempt3/bind-controls.txt:5` (committed receipt; not re-run) | agree | a do-nothing transcript keeps 32/32 under v2; v3 keeps 0/32 |

New SOURCES rows S092, S093, S094 (`corpus/SOURCES.md` L101-L103): 11 columns each; kinds docs/docs/paper,
tier A, status queued/mined; anchors line-level with digests; quotes ≤25 words as above.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ eight `W04` duplicate-URL warnings (S047, S048, S075, S076, S077, S078, S081, S092) and
`tameshi ok …/corpus/SOURCES.md`, exit 0.

## Disclosed breaches, weighed

- **Dead-seat overlap (Mistake 4): harmless, process lapse.** `spec-wA.json` vs `spec-wC.json`
  (CloseBreaches): dead wA `RegressionReplay`/`SelftestsNoHarm` measured `f09d3425` + `witness/fix.diff`;
  wC `RegressionReplayHead`/`SelftestsNoHarmHead` measure the landed `bb681566` and are the unspawned
  attempt-2 wave-B items (no seat transcript), not a dead seat's task. Only `ConnectorOverlap` reuses a dead
  seat's name (9 dead names vs 38 wC names); its scan adds the landed diff and the binding surface. Distinct
  measured objects; the missed pre-dispatch dead-list diff is the defect, already booked.
- **ColdA01 containment (Mistake 5): defect, harm contained.** The two killed processes belonged to
  ColdA09's replay workdir `/tmp/tameshi-r4-2-regression.1e5R9E` (`TameshiR30A3.ColdA01.jsonl:174-175`,
  07:32:43Z). ColdA09 claimed no receipt from that replay (`wC/ColdA09.md`, section 26); section 26 is
  covered by ColdB09's complete nine-leg PASS (`wC/ColdB09.md:34`); the no-harm PASS is RegressionReplayHead's
  own `--workdir` run. ColdA09's report attributes both deaths to its own timeout, which misses the
  07:32:43Z kill. The misrooted report has no fleet copy (conformance table).
- **Untrusted leftovers:** none of the ten paths in `attempt3/inherited-removed.txt` is cited by the report
  or lesson; no commit ever added them (CloseBreaches).

## Trend verdicts

- **expansion: unprovable-but-better.** New entry `corpus/knowledge/regression-tally-completeness.md` cites
  mined rows S087/S093/S094 and has a README row, and binding v3 plus the audit are new instruments. The
  README row itself says "Core ground …, not a frontier move", so net new uncovered ground is not shown;
  the lane's `improved` is not adopted. Not harmed: the two overreaching sentences are marked by E1/E2.
- **quality: improved.** The 31 sections drifted by `bb681566` re-verify through 63 fresh entries (none
  failing, inputs hash-equal to `bb681566`), credit back to 64/64; entry overreach marked by errata.
- **discernment: improved.** The spot-check agrees with the gate on three admits and three rejects.

## SHONEN (operator note)

All four boxes stay `[~]`. Boxes 2 (end-to-end task: nine-leg replay receipt) and 3 (instructions
executable: monitor 64/64 with transcript-bound fresh readers) look checkable by a non-author from
committed evidence; promotion is operator-owned, so nothing is marked here.

## Routed defects (lane fixes next round)

1. SCORECARD row and report Gate call JudgeC1 "non-author"; append an erratum naming this closure as the
   non-author C1 reviewer (append-only; do not edit the round-30 block).
2. Cold-read recipe: pass `--workdir` under the seat's own scratch on every `--regression` run, and require
   the cwd check before any kill (Mistake 5 fix); record the ColdA09 kill in ColdA09's section-26 note.
3. Pre-dispatch dead-seat diff (Mistake 4 fix) as a committed check, not prose.
4. Binding v4 from the audit conditions; runtime tally check beyond the sum (per-leg presence), and the
   8 MutateHead survivors (already routed to round 31).
5. Lesson cite `:60-62` → `:60`; stale `Next unused id: S092.` in SOURCES (already routed).
6. Unowned dead workdir `/tmp/tameshi-r4-2-regression.j0FKnk` (~07:25Z, clone
   `tameshi-registry-check-i272er4j`) matches no wave-C transcript: identify its owner in round 31.
