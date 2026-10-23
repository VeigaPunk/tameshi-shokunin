# ReviewContractTrail

## Verdict

All four requested **historical ordering checks are satisfied**. This is an audit of committed objects and ancestry, not a C1 result, an admission decision, or approval to replace a binding.

Axis: **calibration**. The relevant risks are false freeze provenance, receipts landed after data, and conflating a later instrument revision with the original freeze.

| Check | Finding | Hashes and recorded committer times |
|---|---|---|
| 1. Counter, contract and predicate before any SCORECARD row change | Satisfied | Freeze `c111dab58b0a8d55e991bbd2efe3aad56717b95a`, `2026-10-23T06:01:22-03:00`; first and only SCORECARD change in the requested range: `2da841bd9913a2037d2bf612793382e572c9d205`, `2026-10-23T06:37:13-03:00`. |
| 2. Every wave-1 report committed before content | Satisfied | All 32 Markdown reports, plus their registry, were added in `87eb64eb2b4840168d669f9125b2df28982108d5`, `2026-10-23T06:37:05-03:00`. That commit is the content commit's immediate parent, eight seconds earlier by its recorded timestamp. The complete w1 tree is identical at both commits. |
| 3. v4 frozen at c111dab5; v5 committed before this wave's dispatch record | Satisfied, chronology only | v4 added at `c111dab58b0a8d55e991bbd2efe3aad56717b95a`, `06:01:22-03:00`; v5 added at `87eb64eb2b4840168d669f9125b2df28982108d5`, `06:37:05-03:00`; dispatch record added at `3351738ad2e84efc30a680d97828be12adc96d88`, `06:37:45-03:00`, all on 2026-10-23. |
| 4. Counter blob unchanged from freeze to content | Satisfied | Both revisions resolve the counter to Git blob `f478a0b52976264711a0b9235a260143b55a6329`; the requested diff-stat command printed nothing. |

## Evidence

All shell commands below ran with working directory `/fast/scratch/hyaku/tameshi-r31-seats/ReviewContractTrail/`. The lane was read-only. Times below are recorded metadata; ancestry, rather than timestamps alone, establishes commit ordering.

### Requested history commands

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format='%h %cI %s' 36c1d3933f680125aeefc447f07db0f03004901a..2da841bd9913a2037d2bf612793382e572c9d205
```

Observed output:

```text
2da841b 2026-10-23T06:37:13-03:00 round-31: content revision — SCORECARD standing rows re-stated (C1 data), S095-S096 + S055 re-open, knowledge entry, README row, QUALITY 66-71, SKILL recipe workdir rule
87eb64e 2026-10-23T06:37:05-03:00 round-31: wave-1 control receipts, binding v5 (redesigned before data), dead-seat check, wave-2 generator
ce1d7a6 2026-10-23T06:04:17-03:00 round-31: wave-1 spec and dispatch record (pre-data controls + build)
c111dab 2026-10-23T06:01:22-03:00 round-31: freeze C1 counter, binding v4, contract, base receipts
```

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format='%h %cI %s' 36c1d3933f680125aeefc447f07db0f03004901a..87eb64eb2b4840168d669f9125b2df28982108d5
```

Observed output:

```text
87eb64e 2026-10-23T06:37:05-03:00 round-31: wave-1 control receipts, binding v5 (redesigned before data), dead-seat check, wave-2 generator
ce1d7a6 2026-10-23T06:04:17-03:00 round-31: wave-1 spec and dispatch record (pre-data controls + build)
c111dab 2026-10-23T06:01:22-03:00 round-31: freeze C1 counter, binding v4, contract, base receipts
```

### Ancestry, including the dispatch record

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --reverse --format='%H %cI parents=%P %s' 36c1d3933f680125aeefc447f07db0f03004901a..3351738ad2e84efc30a680d97828be12adc96d88
```

Observed output:

```text
c111dab58b0a8d55e991bbd2efe3aad56717b95a 2026-10-23T06:01:22-03:00 parents=36c1d3933f680125aeefc447f07db0f03004901a round-31: freeze C1 counter, binding v4, contract, base receipts
ce1d7a6454b1d6c929eb5f160e203c6d7093d633 2026-10-23T06:04:17-03:00 parents=c111dab58b0a8d55e991bbd2efe3aad56717b95a round-31: wave-1 spec and dispatch record (pre-data controls + build)
87eb64eb2b4840168d669f9125b2df28982108d5 2026-10-23T06:37:05-03:00 parents=ce1d7a6454b1d6c929eb5f160e203c6d7093d633 round-31: wave-1 control receipts, binding v5 (redesigned before data), dead-seat check, wave-2 generator
2da841bd9913a2037d2bf612793382e572c9d205 2026-10-23T06:37:13-03:00 parents=87eb64eb2b4840168d669f9125b2df28982108d5 round-31: content revision — SCORECARD standing rows re-stated (C1 data), S095-S096 + S055 re-open, knowledge entry, README row, QUALITY 66-71, SKILL recipe workdir rule
3351738ad2e84efc30a680d97828be12adc96d88 2026-10-23T06:37:45-03:00 parents=2da841bd9913a2037d2bf612793382e572c9d205 round-31: wave-2 spec, dispatch record, content monitor, pre-dispatch overlap check
```

### Check 1: actual file history, not commit subjects alone

Locations: `.ufo/evidence/round-31/contract.json:14-18` contains the predicate and counter identity; `:25-26` contains the target and immutable-freeze rule. `.ufo/evidence/round-31/c1-measure.py:4-20` states the same predicate; `:196-224` implements row comparison and the prefix condition. The appended standing tables are at `SCORECARD.md:1512-1537`.

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --reverse --format='%H %cI %s' --name-status 36c1d3933f680125aeefc447f07db0f03004901a..2da841bd9913a2037d2bf612793382e572c9d205 -- SCORECARD.md
```

Observed output:

```text
2da841bd9913a2037d2bf612793382e572c9d205 2026-10-23T06:37:13-03:00 round-31: content revision — SCORECARD standing rows re-stated (C1 data), S095-S096 + S055 re-open, knowledge entry, README row, QUALITY 66-71, SKILL recipe workdir rule

M	SCORECARD.md
```

The frozen contract was also read directly with:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c111dab5:.ufo/evidence/round-31/contract.json
```

Observed predicate in that committed object:

```text
"predicate": "C1 passes at REV iff, for each of the 12 frozen statements, the last row of its frozen table type in the committed SCORECARD.md at REV states values equal to the values its frozen command prints when run at REV, and the base SCORECARD.md is a byte prefix of REV's SCORECARD.md."
```

### Checks 2 and 3: additions and complete receipt inventory

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --reverse --format='%H %cI %s' --name-status 36c1d3933f680125aeefc447f07db0f03004901a..HEAD -- .ufo/waves/round-31/w1/ .ufo/waves/round-31/dispatch-w2.json .ufo/evidence/round-31/coldread/bind-select-v4.py .ufo/evidence/round-31/coldread/bind-select-v5.py .ufo/evidence/round-31/contract.json .ufo/evidence/round-31/c1-measure.py
```

Observed: `c111dab58b0a8d55e991bbd2efe3aad56717b95a` added the counter, v4 and contract; `87eb64eb2b4840168d669f9125b2df28982108d5` added v5 and every w1 path listed below; `3351738ad2e84efc30a680d97828be12adc96d88` added `dispatch-w2.json`. No other changes to those paths appeared in this history read.

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 87eb64eb2b4840168d669f9125b2df28982108d5 -- .ufo/waves/round-31/w1/
```

Observed output:

```text
.ufo/waves/round-31/w1/BuildDeadSeatCheck.md
.ufo/waves/round-31/w1/ConnectorOverlap.md
.ufo/waves/round-31/w1/CriticC1.md
.ufo/waves/round-31/w1/CriticNoHarm.md
.ufo/waves/round-31/w1/CtlBindV4New.md
.ufo/waves/round-31/w1/CtlBindV4Old.md
.ufo/waves/round-31/w1/CtlDoNothing.md
.ufo/waves/round-31/w1/CtlHiddenRows.md
.ufo/waves/round-31/w1/CtlJunkRows.md
.ufo/waves/round-31/w1/CtlLabelShortcut.md
.ufo/waves/round-31/w1/CtlReceiptCopy.md
.ufo/waves/round-31/w1/CtlRewriteInPlace.md
.ufo/waves/round-31/w1/CtlRowsDeleted.md
.ufo/waves/round-31/w1/CtlWrongHeader.md
.ufo/waves/round-31/w1/DeterminismProbe.md
.ufo/waves/round-31/w1/MutCounter.md
.ufo/waves/round-31/w1/RemeasureA.md
.ufo/waves/round-31/w1/RemeasureB.md
.ufo/waves/round-31/w1/RemeasureC.md
.ufo/waves/round-31/w1/RevengerStrayTmp.md
.ufo/waves/round-31/w1/ReviewBindV4.md
.ufo/waves/round-31/w1/ReviewCounter.md
.ufo/waves/round-31/w1/ReviewRoutedR30.md
.ufo/waves/round-31/w1/ScoutFrontier.md
.ufo/waves/round-31/w1/ScoutStatements.md
.ufo/waves/round-31/w1/ScribeEntry.md
.ufo/waves/round-31/w1/ScribeMistakes31.md
.ufo/waves/round-31/w1/ScribeQuality.md
.ufo/waves/round-31/w1/SentinelCounter.md
.ufo/waves/round-31/w1/SrcDoctest.md
.ufo/waves/round-31/w1/SrcGoExamples.md
.ufo/waves/round-31/w1/SrcRustdoc.md
.ufo/waves/round-31/w1/swarm-registry.json
```

This covers every w1 Markdown report, not only reports whose names begin with `Ctl`. The w1 registry identifies the wave at `.ufo/waves/round-31/w1/swarm-registry.json:2-6`.

The frozen v4 declaration is at `.ufo/evidence/round-31/contract.json:49-54`. The later addendum explicitly proposes superseding v4 with v5 at `.ufo/evidence/round-31/contract-addendum-1.json:4-13`; it is not evidence that v5 was the original frozen instrument.

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c111dab5:.ufo/evidence/round-31/coldread/bind-select-v4.py | sha256sum
```

Observed:

```text
dd8bb39309cb337b4b0e6703657198fc88655ce4b498de2ad3f637e04030b87f  -
```

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 87eb64eb2b4840168d669f9125b2df28982108d5:.ufo/evidence/round-31/coldread/bind-select-v5.py | sha256sum
```

Observed:

```text
8760ddc9014af73a20dc95627528b845af75c9539c780fa509fba2c9b2e61338  -
```

The w2 registry's `createdAt` is `2026-10-23T09:37:38.498Z` (`.ufo/waves/round-31/w2/swarm-registry.json:4-5`), also later than the v5 commit's `09:37:05Z`. This is a record timestamp, not an independently observed runtime dispatch time: the registry has null agent IDs, and `dispatch-w2.json:324-326,489-490` records a task-call payload and directions to issue it.

### Check 4 and byte-identity cross-checks

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat c111dab5 2da841bd9913a2037d2bf612793382e572c9d205 -- .ufo/evidence/round-31/c1-measure.py
```

Observed: **no output**.

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse c111dab5:.ufo/evidence/round-31/c1-measure.py 2da841bd9913a2037d2bf612793382e572c9d205:.ufo/evidence/round-31/c1-measure.py c111dab5:.ufo/evidence/round-31/contract.json 2da841bd9913a2037d2bf612793382e572c9d205:.ufo/evidence/round-31/contract.json c111dab5:.ufo/evidence/round-31/coldread/bind-select-v4.py 2da841bd9913a2037d2bf612793382e572c9d205:.ufo/evidence/round-31/coldread/bind-select-v4.py 87eb64eb2b4840168d669f9125b2df28982108d5:.ufo/evidence/round-31/coldread/bind-select-v5.py 3351738ad2e84efc30a680d97828be12adc96d88:.ufo/evidence/round-31/coldread/bind-select-v5.py 87eb64eb2b4840168d669f9125b2df28982108d5:.ufo/waves/round-31/w1 2da841bd9913a2037d2bf612793382e572c9d205:.ufo/waves/round-31/w1
```

Observed output, in the command's argument order:

```text
f478a0b52976264711a0b9235a260143b55a6329
f478a0b52976264711a0b9235a260143b55a6329
6a05a1d20cd05b27b576eaba0df765dbce3568df
6a05a1d20cd05b27b576eaba0df765dbce3568df
1970d16aca8d37d0396bc30a5d198b8a7886c83c
1970d16aca8d37d0396bc30a5d198b8a7886c83c
290a5800fbcf48cfdd478f9ea2fab5cf97999c45
290a5800fbcf48cfdd478f9ea2fab5cf97999c45
0915585a9945481e119d733dd238de9cc43bbd84
0915585a9945481e119d733dd238de9cc43bbd84
```

These pairs establish counter and contract identity from freeze to content, v4 identity over the same interval, v5 identity from its commit to the dispatch-record commit, and complete w1 tree identity from controls to content.

## Counterexample and limits

The strongest scoped falsifier was an earlier SCORECARD edit or a receipt added only with the content, concealed by reassuring commit subjects. The path history and complete w1 tree identity rule that out in the audited chain.

There is a real limit to a broader provenance claim: v5 is a distinct later instrument. The frozen contract at `contract.json:49-54` and the dispatched context at `dispatch-w2.json:325` still name v4; the addendum at `contract-addendum-1.json:5-13` names a v5 replacement. All four chronological checks can therefore hold without establishing that a v5-only no-harm result satisfies the canonical v4 assignment. This report does not resolve that authority question or grant a new one.

## Smallest safe correction

No chronological repair or history rewrite is needed. In the round's closure, retain the precise distinction: **C1 and v4 froze at c111dab5; v5 was a later pre-content, pre-dispatch-record redesign**. Apply the canonical assignment's v4 binding to its claimed evidence, and label any v5 result separately unless an authoritative instruction changes that requirement. Do not describe this audit as proving either an unchanged no-harm instrument or actual runtime dispatch timing.

No production edits, gates, selftests, counter executions, alternate runtimes, subagent dispatches, installs, or upgrades were performed. All shell commands completed; no process was left running.
