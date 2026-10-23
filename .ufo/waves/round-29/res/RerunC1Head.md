# RerunC1Head — C1 counter re-run at E, master, lane head, and base

Verdict: C1_R29_V2_PASS=true CONFIRMED. The frozen counter reproduces the reported
PASS at E and at the newer lane head, and reproduces the frozen "before" MISS at
base. Counter bytes, commit-before-dispatch, and ledger append all verified.

Clone: `/fast/scratch/hyaku/tameshi-r29-RerunC1Head` (fresh `--no-hardlinks` clone,
GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset). `master` in the clone is
`7a45f7b9d6a2542a553276330c8b02ac2e28c7ef` (E). The live lane's master has since
advanced to `9bb699ad2d9f795dff95df85eb967129c54927d6`, so it was fetched into the
clone and measured too, per the "measure there too" clause.

## 1. Counter byte identity vs contract

`sha256sum .ufo/evidence/round-29/c1-measure-v2.py` (working tree at E):

```
2ec2f1a02f73ba10136288abc06197cd73cb388c013db80af3a926959ed70491  .ufo/evidence/round-29/c1-measure-v2.py
```

`git show 09e4f273dd54edea382ea03f098eecb3628331c3:.ufo/evidence/round-29/c1-measure-v2.py | sha256sum`:

```
2ec2f1a02f73ba10136288abc06197cd73cb388c013db80af3a926959ed70491  -
```

Matches `counter_sha256` in `.ufo/evidence/round-29/contract-amendment-2.json:14`
(`2ec2f1a02f73ba10136288abc06197cd73cb388c013db80af3a926959ed70491`). The
`MONITOR_SHA` pins at c1-measure-v2.py:43-46 equal the `pinned_monitor_sha256`
block at contract-amendment-2.json:15-18.

## 2. Counter committed before wave-1 dispatch

`git log --format='%H %cI %s' -- .ufo/evidence/round-29/c1-measure-v2.py` (single
entry — created once, never modified):

```
09e4f273dd54edea382ea03f098eecb3628331c3 2026-10-22T22:26:47-03:00 round-29: C1 counter v2 re-frozen before data (pinned monitor chain); control receipts (CriticC1Design, CriticC2Design, CtlC2v2Port, C1v2 re-score); wave-1 generator
```

`git log --format='%H %cI %s' -- .ufo/waves/round-29/dispatch-w1.json`:

```
bc2058a405fadfc1594c4ee764988902c09525ee 2026-10-22T22:50:31-03:00 round-29: wave-1 cold reads (36 seats, 12 sections at 9f3084bc) assembled; 22 bound entries appended (ledger 371 -> 393)...
```

Counter commit 22:26:47 precedes dispatch-record commit 22:50:31 by ~24 min, and
`git merge-base --is-ancestor 09e4f273 bc2058a4` exits 0 (`ANCESTOR_OK`).
dispatch-w1.json itself names the v2 counter and the 09e4f273 freeze in its
taskCall context (dispatch-w1.json:479).

## 3. Counter runs (timeout 900, python3)

At E (`--rev 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef`), exit 0:

```
C1_R29_V2: covered=64/64 restraint=8 box3_mismatch=0 appended=22 bound=22 prefix_equal=1 rev=7a45f7b9d6a2542a553276330c8b02ac2e28c7ef
PREDICATE: C1_R29_V2_PASS=true
```

At clone `master` (same rev), exit 0 — identical output.

At live lane head (`--rev 9bb699ad2d9f795dff95df85eb967129c54927d6`), exit 0:

```
C1_R29_V2: covered=64/64 restraint=8 box3_mismatch=0 appended=22 bound=22 prefix_equal=1 rev=9bb699ad2d9f795dff95df85eb967129c54927d6
PREDICATE: C1_R29_V2_PASS=true
```

At base (`--rev 367ec0f1d79cb9b67d724f2962e7554a0841b1fc`), exit 1:

```
  uncovered: ### Round-18 gate/probe registry — routed-defect closure
C1_R29_V2: covered=63/64 restraint=6 box3_mismatch=1 appended=0 bound=0 prefix_equal=1 rev=367ec0f1d79cb9b67d724f2962e7554a0841b1fc
PREDICATE: C1_R29_V2_PASS=false
```

Base output matches the frozen `before` field (contract-amendment-2.json:21:
covered=63/64 restraint=6 box3_mismatch=1). E output matches the claim's reported
PASS numbers (64/64, 8, 0, 22/22).

## 4. Ledger diff base..E is a pure append

`git diff --numstat 367ec0f1 7a45f7b9 -- .ufo/evidence/round-21/coldread/ledger.json`:

```
1781	0	.ufo/evidence/round-21/coldread/ledger.json
```

`git diff --stat` confirms `1781 insertions(+), 0 deletions`, and the counter's
own `prefix_equal=1` confirms all 371 base entries and every non-entry key are
byte-equivalent as canonical JSON. E..9bb699ad touches only
`.ufo/evidence/round-29/c1-at-E.stdout`, `c2-at-E.stdout`, `census-E.stdout`,
`LOG.md`, `SCORECARD.md`, `corpus/lessons/round-29.md` — no ledger or wave-1
report/registry bytes — so the identical PASS there is expected.

## Residual note

The counter's binding check (c1-measure-v2.py:128-152) is syntactic: it verifies
report paths, JSON-block fields, and registry membership at REV, not authorship.
Contract-amendment-2.json:24 acknowledges this bound; no defect found in scope.

## Tooling

No installs or updates performed; stock python3/git/sha256sum sufficed.

Report: .ufo/waves/round-29/res/RerunC1Head.md
