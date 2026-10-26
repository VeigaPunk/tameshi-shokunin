# Attempt-1 wave w1 seat inventory (round 48)

Source: `.ufo/waves/round-48/w1-dispatch.json` (32 spawn members; identical to `w1/swarm-registry.json`, createdAt 2026-10-26T08:39:27Z, agentId all null). Files under `.ufo/waves/round-48/w1`; mtimes are local (-03) on 2026-10-26. A seat is `report` if `<Seat>.md` exists, `deliverable-only` if only other `<Seat>.*` files exist, `no output` if none.

| Seat | Role | Class | Files (bytes, mtime) |
|---|---|---|---|
| T48ExecC1Counter | executor | deliverable-only | `T48ExecC1Counter.measure.py` (48727 B, 05:51:12) |
| T48ExecC2Counter | executor | report | `T48ExecC2Counter.controls.py` (11633 B, 05:49:11)<br>`T48ExecC2Counter.md` (15129 B, 05:53:08)<br>`T48ExecC2Counter.measure.py` (38473 B, 05:50:40) |
| T48ExecObs1 | executor | no output | — |
| T48ExecObs2 | executor | report | `T48ExecObs2.emit.exit` (2 B, 07:19:42)<br>`T48ExecObs2.emit.stderr` (0 B, 07:19:42)<br>`T48ExecObs2.emit.stdout` (19894 B, 07:19:42)<br>`T48ExecObs2.md` (11878 B, 07:20:39) |
| T48ExecObs3 | executor | no output | — |
| T48ExecC1Controls | executor | deliverable-only | `T48ExecC1Controls.run-controls.py` (19129 B, 05:51:18) |
| T48ExecFetchS026 | executor | report | `T48ExecFetchS026.md` (8931 B, 05:42:53) |
| T48ExecFetchS048 | executor | report | `T48ExecFetchS048.md` (8946 B, 05:41:58) |
| T48ExecFetchS093 | executor | report | `T48ExecFetchS093.md` (13981 B, 05:43:48) |
| T48ExecFetchS108 | executor | report | `T48ExecFetchS108.md` (8963 B, 05:42:54) |
| T48ExecSelftestReceipts | executor | report | `T48ExecSelftestReceipts.md` (16742 B, 05:50:14) |
| T48RevenRegression | revenger | report | `T48RevenRegression.md` (17187 B, 06:52:38) |
| T48RevenEnvDiff | revenger | report | `T48RevenEnvDiff.md` (14612 B, 05:47:54) |
| T48CritLoad | critic | report | `T48CritLoad.md` (13482 B, 06:56:15) |
| T48CritC1Design | critic | report | `T48CritC1Design.md` (25854 B, 05:52:19) |
| T48CritC2Design | critic | no output | — |
| T48CritMistakeFix | critic | no output | — |
| T48RevC1Predicate | reviewer | no output | — |
| T48RevC2Predicate | reviewer | no output | — |
| T48RevSpotcheckRouting | reviewer | report | `T48RevSpotcheckRouting.md` (17243 B, 05:52:45) |
| T48MutC1Core | mutation-tester | no output | — |
| T48SentinelTmp | sentinel | report | `T48SentinelTmp.md` (18164 B, 06:01:11) |
| T48ScribeRowsA | scribe | report | `T48ScribeRowsA.md` (6901 B, 05:52:46)<br>`T48ScribeRowsA.rows.md` (20440 B, 05:51:23) |
| T48ScribeRowsB | scribe | deliverable-only | `T48ScribeRowsB.rows.md` (23785 B, 06:03:07) |
| T48ScribeMistakes | scribe | report | `T48ScribeMistakes.draft.md` (11239 B, 05:50:39)<br>`T48ScribeMistakes.md` (8339 B, 05:51:21) |
| T48ScribeLessonCorrection | scribe | report | `T48ScribeLessonCorrection.draft.md` (14861 B, 05:53:54)<br>`T48ScribeLessonCorrection.md` (9870 B, 05:53:54) |
| T48ScoutHeldUses | scout | report | `T48ScoutHeldUses.md` (12474 B, 05:47:15) |
| T48ScoutConsiderthese | scout | report | `T48ScoutConsiderthese.md` (8253 B, 05:48:32) |
| T48ScoutPackage | scout | report | `T48ScoutPackage.md` (9501 B, 05:47:55) |
| T48ScoutCarried | scout | report | `T48ScoutCarried.md` (10480 B, 05:47:59) |
| T48ConnSiblings | connector | report | `T48ConnSiblings.md` (13243 B, 05:47:20) |
| T48ConnCorpus | connector | report | `T48ConnCorpus.md` (10771 B, 05:47:35) |

Counts: {'deliverable-only': 3, 'report': 22, 'no output': 7} (total 32).

Shared (non-seat) entries in `w1/`: `selftest/` (15 run receipts + `falsifiers.baselane.sh`, 05:42-05:48), `sources/` (S026/S048/S093/S108 snapshots + receipts, 05:41-05:42), `swarm-registry.json` (46860 B, 05:39, mode 600).

Note: `T48ExecObs2.md` (07:20) and `T48CritLoad.md`/`T48RevenRegression.md` (06:5x) are the latest writes; last mtime in `w1/` is 07:20:39. Obs2's `.emit.*` trio is a receipt set, not an extra seat.

## Leftover scratch /fast/scratch/hyaku/tameshi-r48/T48*

No directory matches an attempt-1 seat name (none of the 32 names above). All 27 `T48*` dirs belong to attempt-2 (`T48A2*`) or wave-2 (`T48W2*`) seats, listed below (`du -sh` at inventory time, live seats still running; nothing deleted).

| Dir | du -sh |
|---|---|
| T48A2CritC1Emit | 308M |
| T48A2CritC2Design | 462M |
| T48A2CritLessonCorrections | 0 |
| T48A2ExecC1Selftest | 155M |
| T48A2ExecC1SerialA | 2.4G |
| T48A2ExecC1SerialB | 2.4G |
| T48A2ExecC1SerialD | 2.4G |
| T48A2ExecC2ControlsReplay | 761M |
| T48A2ExecLiveStability | 6.5M |
| T48A2ExecSixLegReplay | 18M |
| T48A2MutC1Fleet | 7.1M |
| T48A2MutFalsifiers | 154M |
| T48A2RevDecidingScript | 0 |
| T48A2RevenSigpipePair | 5.9M |
| T48A2RevenSixLegHistory | 2.0M |
| T48A2RevSalvage | 0 |
| T48A2RevShonen | 0 |
| T48A2RevSpotcheckR47 | 0 |
| T48A2ScribeReportSources | 4.0K |
| T48A2ScribeShonen | 252K |
| T48A2SentinelFixtures | 800M |
| T48W2CritC1Controls | 4.9G |
| T48W2ExecC1ProbeB | 2.5G |
| T48W2ExecC1ProbeD | 203M |
| T48W2MutC1CounterA | 11M |
| T48W2MutC1CounterB | 104K |
