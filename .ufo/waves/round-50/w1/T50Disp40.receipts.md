# T50Disp40 receipts — C1 disposer, round-40 spot-check

Round 50, lane `tameshi-shokunin`, base `e3729de862f73ae080d98fcf522a7081ce16e40a`.
Scratch root `/fast/scratch/hyaku/tameshi-r50/T50Disp40/` (removed before yield; no /tmp receipt stands).
Tooling: nothing installed. `python3` and `git` sufficed; the pacman pause was not exercised.

## 1. Self-check on a scratch clone (only my five rows)

```
$ git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /fast/scratch/hyaku/tameshi-r50/T50Disp40/lane
$ git -C <clone> rev-parse --show-toplevel
/fast/scratch/hyaku/tameshi-r50/T50Disp40/lane
$ git -C <clone> log --oneline -1
4afb060 round-50: SCORECARD pre-registration section and the standing axis table restated with round-49 values (routed R49.4); no-harm at base
# corpus/routed-defects.json written from T50Disp40.rows.json (R40.1..R40.5 only), then:
$ git -C <clone> -c user.name=T50Disp40 -c user.email=t50disp40@scratch.local \
    commit -q -m 'scratch: T50Disp40 round-40 rows only (final)'
13b2ab7662c0446750659d4b2b3fed1cd638f29d
$ TMPDIR=/fast/scratch/hyaku/tameshi-r50/T50Disp40 \
  python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-50/c1/measure.py \
    --lane <clone> --rev HEAD --explain
EXPLAIN open-unplanned R40.2
EXPLAIN open-unplanned R40.3
EXPLAIN missing R41.1
... (R41.1..R49.6 missing: 44 lines, other seats' rounds)
EXPLAIN missing R49.6
C1_R50: self=ceee320c9ad8 rev=13b2ab7662c0446750659d4b2b3fed1cd638f29d defects=49 rows=5 fixed=2 open=2 declined=1 fixed_this_round=0 missing=44 extra=0 duplicate=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=2 declined_bad=0 fixed_short=18 declined_over=0 this_round_short=5 total=69 C1_R50_PASS=false
exit 1
```

No `evidence_bad`, `key_miss`, `fixed_bad`, `duplicate`, `extra`, `spotcheck_changed` or `defects_pin`
line names a round-40 row: every excerpt resolved at its cited lines, both `fixed` rows passed the
freshness/ack scan, and no row was rejected. The only round-40 EXPLAIN lines are the two
`open-unplanned` lines explained in the report (§2): the newest `**Planned (round 50)` paragraph
(`SCORECARD.md:2410`) is the L1's to write and does not yet name R40.2 or R40.3. `missing` lines are
the 44 items of rounds 41–49 that this seat does not own; `fixed_short`/`this_round_short` are fleet
floors, not round-40 findings (both round-40 fixes predate base `e3729de8`, so they cannot count
toward the `fixed_after_base_min=5` floor).

An earlier iteration of the same run marked R40.5 `open` (`total=70`, `open_unplanned=3`); it was
reclassified to `declined` after the tree probes in §2 showed the can-fail successor already exists.
Both transcripts were observed; only the final one is reproduced.

## 2. Tree probes behind each verdict (run at base unless stated)

```
$ git -C LANE merge-base --is-ancestor a3d6c690bcbf8914551d4f4e8e1612784c1c2046 e3729de8...   # exit 0
$ git -C LANE merge-base --is-ancestor b37ce974b6efb8c465626d7346149549a3300a4b a3d6c690...   # exit 1
$ git -C LANE merge-base --is-ancestor b37ce974b6efb8c465626d7346149549a3300a4b e3729de8...   # exit 0
$ git -C LANE log --format='%H %ad %s' -S'counts one adopted, six refused, ten present-but-not-appended' \
    e3729de8 -- corpus/lessons/round-41.md
b37ce974b6efb8c465626d7346149549a3300a4b Sun Oct 25 03:39:24 2026 -0300 round-41: C1 records reconciliation + C2 write-path-census-v3 ...
$ git -C LANE log --format='%H %ad %s' -S'a quote labelled "11 words" that has 13 tokens' \
    e3729de8 -- corpus/lessons/round-41.md
b37ce974b6efb8c465626d7346149549a3300a4b Sun Oct 25 03:39:24 2026 -0300 round-41: C1 records reconciliation + C2 write-path-census-v3 ...

$ git show e3729de8:corpus/lessons/round-41.md | sed -n '51,58p'
### Correction — the round-40 quarantine summary

The round-40 closure's routed defect 1 stands: that lesson's closing sentence says seven
refused and nine present-but-not-appended, while the verdict table in the same file
counts one adopted, six refused, ten present-but-not-appended. The table is the record;
the summary sentence is the drift. This appended correction is the fix the closure asked
for ("append a correction in the round-41 lesson — do not rewrite the closed round-40
file in place"). The round-40 file is unchanged.
$ git show e3729de8:corpus/lessons/round-41.md | sed -n '75p'
| count-label-drift | ... | the round-40 closure's routed defect 4 (a quote labelled "11 words" that has 13 tokens) — the same class, one round later, caught by re-counting instead of trusting the label | ... |

# R40.1 numeric truth: the round-40 quarantine table itself
$ awk '/^### Quarantine/{f=1;next} f&&/^\| S[0-9]/{print}' corpus/lessons/round-40.md | wc -l
17
# verdict recount (case-folded): Adopted 1 (S132); refuse 6 (S109, S131, S137, S140, S141, S143);
# present rows 11 minus the adopted one = 10 present-but-not-appended (S118 misbound counts present).
# The three prose-class rows the table marks "the prose class is stale": S113, S123, S134.

# R40.4 numeric truth
$ printf '%s' 'drawbacks such as fragility and lack of context can lead to false positives' | wc -w
13
$ git show e3729de8:corpus/lessons/round-40.md | sed -n '14p'
- Quote (11 words), English abstract: "drawbacks such as fragility and lack of context can lead to false positives".

# R40.2: the report still cites the transient pointer, and no errata replaces it
$ git show e3729de8:.ufo/waves/round-40/w1/dispatch-outcome.md | sed -n '12,16p'
The grant is recorded in the seat ledger as `1792889233 64 tameshi round-40-w1`
(`~/.local/state/shokunin-hyaku/wave-slots`), taken at 2026-10-24T21:47:13-03:00,
immediately before the wave was dispatched. It was released only after the
settlement classification below (`released lane=tameshi wave=round-40-w1`,
exit 0).
$ git log --format='%H %ad %s' -3 -- .ufo/waves/round-40/w1/dispatch-outcome.md
46781274ea882274892dc1dbe81a07b7aee40e25 Sat Oct 24 22:32:17 2026 -0300 round-40: deciding receipts, 64-seat settled wave, S108 pin, quarantine verdicts
   # last touch predates routed_at a3d6c690; nothing appended since
$ grep -rn "wave-slots" LOG.md SCORECARD.md   # no output
$ grep -rln "wave-slots" . --include=*.md | grep -v spotcheck
./.ufo/waves/round-40/w1/dispatch-outcome.md
./.ufo/waves/round-41/w1/CriticR40Discharge.md
# the durable artefact exists and is committed (base):
$ git show e3729de8:.ufo/waves/round-40/settlement-receipt.json | sed -n '277,279p'
  "registry_members": 64,
  "seat_exits": 64,
  "reports_present": 64,

# R40.3: no pasted id list
$ git show e3729de8:.ufo/waves/round-40/w1/dispatch-outcome.md | grep -c 'S1[0-9][0-9]'
0
$ git show e3729de8:.ufo/waves/round-40/assimilation/reg-ids | wc -l
105
$ git show e3729de8:.ufo/waves/round-40/assimilation/staged-ids | wc -l
2
$ grep -rn "reg-ids\|staged-ids" .ufo/reports  # no output (no round report pastes them)

# R40.5: the vacuous regex is still the only depth guard at the round-38 contract path,
# and no post-routing record names its retirement
$ for f in $(git ls-tree -r --name-only e3729de8 .ufo/evidence | grep contract.json); do
    n=$(git show e3729de8:$f | grep -c depth_command_d); [ "$n" != "0" ] && echo "$f $n"; done
.ufo/evidence/round-38/contract.json 1
.ufo/evidence/round-39/contract.json 2
$ git show e3729de8:.ufo/evidence/round-39/contract.json | sed -n '12p'
      "summary": "The round-39 depth no-harm guard agrees with canonical SCORECARD command D on the live runner and on a ledger-stripped copy. The round-38 regex ^\\s*leg remains a vacuous control (0 hits) and is not rewritten.",
$ git grep -n "depth guard" e3729de8 -- ':!corpus/lessons/*spotcheck*'
# only pre-round-40 wave files (round-17/18/30/36/39); no round-41+ retirement record
$ grep -n "depth" corpus/QUALITY.md
# criteria mention neither a depth guard nor its retirement
```

## 3. Digests of the artefacts the rows cite (base)

```
659e39bb7fba6d381ee3af27daec8b74a6542d861b8b4666b4d46d4ad44f89a3  .ufo/waves/round-40/settlement-receipt.json
b11c94133a35ce8c2c13bb30c04dc545290e53c40710cfd09c4b0a3d94126e91  .ufo/waves/round-40/assimilation/reg-ids
d77a652a2dbc36459dc74a10e8daa7f2e47cc713db0d02fc10d7f48dbb129fce  .ufo/waves/round-40/assimilation/staged-ids
a50e118d9608d9b55e2bf9bbb52391c3c1b079072728b301507403076e21d5fd  .ufo/waves/round-40/w1/dispatch-outcome.md
d4aa77b826b50e92ad598159a2f539ff6bc939da96e81f05f2b415e660717051  corpus/lessons/round-40-verifier-spotcheck.md (equals the defect set's pin)
```
