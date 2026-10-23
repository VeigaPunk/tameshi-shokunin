# ReviewControls — audit of pre-freeze control discipline, round 29

**Verdict: PARTIAL PASS.** The two-stage discipline was largely executed — both v1
counters were attacked by controls, both claims were re-designed and re-frozen, and v2
controls were scored, all before the wave-1 dispatch — but it ends in one hard
violation: wave-1 data was dispatched while the last control seat (CriticC2v2) was
still unresolved and presumed dead, and its report, which proved the C2 v2 target
unreachable on this host, landed after dispatch. The rule "controls built and scored
before any data seat" was not enforced as a gate on dispatch. Two recording gaps
accompany it: the CtlC2Shortcut refusal-hold appears in no pre-data artifact
(asymmetric with CtlC1Shortcut, which is recorded in both amendments), and the control
wave itself has no dispatch/registry receipt, so seat lifecycle events — refusals,
"taken as dead" — exist only as post-mortem narration in the lesson.

## Timeline (all times -0300, commit times from `git log --format='%h %cI %s'`, file times from `stat -c %y`)

| Time | Event |
|---|---|
| 22:12:16 | `9f3084b` freezes contract + v1 counters + all widely read input edits (S024, README, QUALITY 55-57) |
| 22:17:36 | `ctl/CtlC2Cheap.md` (C2-K1..K5, all no-meet) |
| 22:19:39 | `ctl/CtlC1Cheap.md` (C1-K1..K4, all no-meet; K4 gained monitor-only credit, binding check rejected it) |
| 22:21:28 | `6ab11a6`: `contract-amendment-1.json` re-freezes C2 as v2 — control CriticC2Design met v1 three ways |
| 22:21:53 | `ctl/CriticC1Design.md` file settles |
| 22:21:58 | `ctl/CriticC2Design.md` file settles — ~30 s *after* the commit citing it |
| 22:25:58 | `ctl/CtlC2v2Port.md` (seven controls against C2 v2, all no-meet) |
| 22:26:42 | `ctl/C1v2-rescore.txt` (L1 re-scores K2-K4 under c1-measure-v2, all false) |
| 22:26:47 | `09e4f27`: `contract-amendment-2.json` re-freezes C1 as v2 + ctl receipts + `make-spec-w1.py` |
| 22:26:57 | `spec-w1.json`, `dispatch-w1.json`, `dispatch-w1.stderr` written; registry `updatedAt` identical |
| 22:27:45 | `task-adapter-w1.json` — the 49-seat wave-1 task call |
| **22:33:57** | **`ctl/CriticC2v2.md` lands — 6m12s after the dispatch record; seat had been "taken as dead"** |
| 22:49:35 | `9bb699a` (jj-side chain): `corpus/lessons/round-29.md` names both shortcut holds and Mistake 1 |
| 22:50:31 | `bc2058a`: 22 bound cold-read entries appended — **and CriticC2v2.md is committed inside this data commit** |
| 23:46:49 | `7a45f7b` (E): F6 fixture landed; C2 measured `kill_original=0 … C2_F6_V2_PASS=false`, honest stop |

## Question 1 — was every counter re-frozen before data?

Yes, on the clock. C2 v2 in `contract-amendment-1.json` (`6ab11a6`, 22:21:28), C1 v2 in
`contract-amendment-2.json` (`09e4f27`, 22:26:47); the wave-1 dispatch record is
22:26:57–22:27:45 and the first data commit `bc2058a` is 22:50:31. Both amendments
self-declare `made_before_data: true, data_seats_run_before_amendment: 0`, consistent
with the timeline. The control→redesign loop ran twice for C2 (v1 met by
CriticC2Design three ways → v2; v2 attacked by CtlC2v2Port's seven controls, none met)
and twice for C1 (v1 attacked by CtlC1Cheap K1-K4, none met, but CriticC1Design found
the counter's executable identity unpinned → v2; K2-K4 re-scored under v2 by the L1,
all false — `ctl/C1v2-rescore.txt`).

## Question 2 — which control reports existed before the wave-1 dispatch?

Six of the seven files in `.ufo/waves/round-29/ctl/`: CtlC2Cheap (22:17:36),
CtlC1Cheap (22:19:39), CriticC1Design (22:21:53), CriticC2Design (22:21:58),
CtlC2v2Port (22:25:58), C1v2-rescore (22:26:42). The seventh, **CriticC2v2.md
(22:33:57), did not** — it postdates `task-adapter-w1.json` (22:27:45) and
`dispatch-w1.json` (22:26:57). It is committed in `bc2058a` (`git show --stat bc2058a`
lists it), i.e. the control receipt rides inside the cold-read data commit.

## Question 3 — CriticC2v2's report relative to dispatch; did the L1 act before data?

The report is a pre-data design review of the *re-frozen* C2 v2 counter (seat's own
header: "Frozen B: 6ab11a62…"). Its Q5 proves the full pinned original cannot kill B5
on this host: all three pinned census exec rows declare mode 755
(`kagi corpus/surface-census.tsv:22,30-31`), B5 removes only the access-bit check, so
the exact-mode check rejects any file that could produce the required divergence —
matching the final `kill_original=0` MISS. It landed 6 minutes after dispatch, while
the data seats ran. The L1 did **not** act on it before data: no amendment-3 exists,
BuildF6A/BuildF6B proceeded and produced the predicted outcome, and the report was
committed inside the data commit `bc2058a` itself. Per the lesson (Mistake 1,
`corpus/lessons/round-29.md:79-92`), the seat had ended "without a final message" and
was taken as dead; the dispatch went out without a last check of the report path.
Acting after 22:33 was anyway constrained — data seats had scored, so re-amending the
predicate would have collided with the frozen-rule clause — which is exactly why the
gate belongs *at dispatch time*, not after.

## Question 4 — are the two safety-refusal seats recorded as holds?

Partially, and asymmetrically.

- **CtlC1Shortcut: yes, pre-data.** Named as a provider-safety-refusal hold in both
  `contract-amendment-1.json` (`c1_unchanged` field) and `contract-amendment-2.json`
  (`bound` field), committed 22:21/22:26 — before dispatch.
- **CtlC2Shortcut: no pre-data record.** `grep -c CtlC2Shortcut` returns 0 in both
  amendments; nothing under `.ufo/waves/round-29/` names it. Its first record is
  `corpus/lessons/round-29.md:46` (22:49:35 chain commit; LOG.md's "two control seats
  refused by a provider safety filter (holds)" lands at E, 23:46:49). The contract's
  required class `shortcut keyed on ids or labels`
  (`contract.json` `controls_required_before_data`) was therefore never scored for
  either claim: both shortcut seats refused, the refusals were accepted as holds
  rather than retried or substituted, and the contract defines no hold path. For C1
  this is the most load-bearing class — the binding check is syntactic and an
  L1-forged report-plus-registry-member is precisely a keyed-on-ids shortcut;
  amendment-2's `bound` field honestly discloses exactly this. Neither refused seat
  left a report file, so the "error text in the report" the lesson cites lives only in
  the (absent here) fleet report.

## Secondary observations

- `6ab11a6` (22:21:28) cites CriticC2Design's three meets, but `CriticC2Design.md`'s
  mtime is 22:21:58 — the amendment was committed ~30 s before the report file
  settled. Harmless ordering jitter, same failure shape as the CriticC2v2 miss at
  smaller stakes.
- No dispatch/registry receipt exists for the control wave at all: no
  `dispatch-ctl*.json`, and `w1/swarm-registry.json` members are the 49 wave-1 seats
  only. The "8 seats in two calls" composition is evidenced only by the lesson and the
  report files; refused/presumed-dead seats leave no mechanism trace.
- Residual risk: the shortcut class is untested on both counters, and C1 v2's
  disclosure admits the binding check cannot distinguish a forged L1 report. A future
  round could still meet the predicate by that route; the bound is disclosed, not
  closed.

## Smallest safe process fix

1. **Gate dispatch on control-seat settlement.** The wave-spec generator
   (`make-spec-w1.py` pattern) must refuse to emit a data wave while any control seat
   lacks a report file *and* a terminal-status line; keep a tiny
   `.ufo/waves/round-N/ctl/status.json` ({seat, spawned_at, report_path, status:
   ok|refused|dead, error}) that the generator checks. This is exactly the lesson's
   own Mistake-1 fix — "report file at its path or recorded dead with its error text
   after a final check" — made mechanical instead of narrative.
2. **Reachability witness at freeze time.** For any claim whose predicate conjoins a
   physical kill/fixture condition, the freeze commit carries one hand-built PASS
   instance (or a documented impossibility proof → don't make the claim). CriticC2v2
   Q5's mode-755 masking was discoverable in minutes; it cost a whole build sub-wave
   and the claim.
3. **Symmetric hold records.** Each amendment records every control seat against the
   claim it amends, including refusals with their error text — CtlC2Shortcut's
   omission from amendment-1 is the template violation this closes.

Verification performed: commit times and file stats via read-only `git log`/`git show
--stat`/`git status`/`stat` in the lane (no writes made except this report); seat
lists extracted from `spec-w1.json`, `task-adapter-w1.json`, and
`w1/swarm-registry.json`; hold records grepped across the lane and fleet
`.ufo/reports/round-29/` (no tameshi report present there). No tools installed or
updated; no processes started.
