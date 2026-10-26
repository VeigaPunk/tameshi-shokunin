# T48A2ScoutDeadSeats — attempt-1 wave w1 inventory

Table: .ufo/waves/round-48/a2w1/T48A2ScoutDeadSeats.table.md

Findings (observed with os.listdir/stat on w1/ against w1-dispatch.json members; no w1-results.json exists):
- 32 seats dispatched; w1-dispatch.json and w1/swarm-registry.json have the same 32 members, all agentId null.
- report (<Seat>.md present): 22. deliverable-only: 3 (T48ExecC1Counter, T48ExecC1Controls, T48ScribeRowsB). no output: 7 (T48ExecObs1, T48ExecObs3, T48CritC2Design, T48CritMistakeFix, T48RevC1Predicate, T48RevC2Predicate, T48MutC1Core).
- Only T48ExecObs2 landed an emit set (.emit.stdout/.stderr/.exit + .md); Obs1 and Obs3 produced nothing. T48MutC1Core's promised cases.md is absent.
- Last write in w1/ is 07:20:39 (-03, T48ExecObs2.md). Most seats landed 05:41-06:03; late ones 06:52 (RevenRegression), 06:56 (CritLoad), 07:19-07:20 (Obs2).
- Classification is by file presence only; contents were not judged. T48ScribeRowsB / ExecC1Counter / ExecC1Controls have deliverables but no report .md, so any results claims from them are unreported.
- Leftover scratch: no /fast/scratch/hyaku/tameshi-r48/T48* dir carries an attempt-1 seat name; the 27 T48* dirs present are all T48A2*/T48W2* (live a2/w2 seats), sizes in the table. Nothing deleted. Several are multi-GB (C1SerialA/B/D 2.4G each, W2CritC1Controls 4.8G).
- Tools installed: none. My own scratch: none created.
