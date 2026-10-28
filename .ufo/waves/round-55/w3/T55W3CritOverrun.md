# T55W3CritOverrun — the seat overrun (wave 3, critic)

Seat `T55W3CritOverrun`. Object attacked: the round's dispatch shape — 75 + 34 + 32 = 141 seats,
three waves — and the claim that the third wave was the right call. No lane file, frozen file or
spec was edited. Every number below is a command in `T55W3CritOverrun-receipts/` (`r1`..`r7`,
`.out` beside each script).

## Verdict

**The overrun is a real breach of the binding round contract, and it is the lesser defect — but only
as a reported breach.** Three readings had to be separated, and one of them refuted my first reading:

1. *Per-wave policy bands were honoured.* w1 75 in 64–128, w2 34 and w3 32 in 32–64 each (r1). No
   validator refused any wave: the config's `waveMinLanes`/`waveMaxLanes` bound one wave's width
   (`ufo-mission-result.mjs:2656-2658`, `ufo-swarm-wave.mjs:16-18`), which is why a three-wave round
   can validate cleanly.
2. *The round cap was not.* The addendum's round contract is the operator rule, and run 11 keeps it
   binding: "every other run-10/9/8/7 rule, including the 64–128 seat band, the 256 hard ceiling, the
   ≥25 % attack share … stays binding" (`lane-addendum.md:3-6`); "**Round size: 64–128 seats in
   total, every round** … Shape per §2: one v2 wave of 64–128, or two v1 waves (32–64 each) summing
   to 64–128, residual call included" (`:77-79`); §2 item 2 sanctions exactly those two shapes plus
   "one ordinary `task` call of ≤8 reviewer/critic seats, counted in the round total (≤128)"
   (`:196-212`). 141 exceeds 128 by 13, and v2 + v1 + v1 is neither sanctioned shape.
3. *The breach is invisible to tooling and therefore disclosure-controlled.* That is the round's
   actual exposure: nothing in the dispatch path can catch it, so the report is the only control.

Against the alternatives, the overrun is the cheaper defect: the RED floor is a failed deciding run
(46/64 credited, score 6 — r3), re-keying fewer than 18 sections is arithmetically impossible
(46 + k < 64 for every k < 18), a reader-only wave is 18 seats against a 32-seat floor, and the
≤8-seat residual call cannot carry 18 sections. The conforming continuation left *after* wave 1 had
already run at 75 was **127 seats (wave 2 = 34 + 18 readers) with all 14 wave-3 attack seats
dropped** — the round spent 13 seats over the cap to keep those 14.

The right call was for the *readers*, not for the *count*. The count was avoidable at plan time:
sizing wave 1 at the v2 floor (64) instead of 75 leaves a 128-seat two-wave round that carries all 18
readers and 12 of the 14 attacks (r2). The root cause is a 17-section planning miss: wave 2's brief
still said "One SKILL.md section drifted" and read 3 seats on `## Standing rules`; wave 3's brief,
written three minutes later, says 18 sections (r4). A credit measure at a candidate revision would
have priced the re-key before the wave that had to carry it was sized.

## The strongest counterexample I could run

The item's own alternatives are *smaller* than the alternative that actually matters. The tightest
counterexample is not "no readers" but "readers inside the cap":

```
wave 1 (already dispatched, v2 band 64-128):            75
wave 2 (v1 band 32-64): 34 attack + 18 readers =       52   -> round total 127 <= 128, two waves
wave 3: 0 seats (a <=8-seat residual call cannot hold the 14 attacks: 127 + 8 = 135 > 128)
cost: all 14 wave-3 attack seats dropped
```
Versus the plan-time version, which keeps 12 of them:
```
wave 1: 64 (v2 floor)   wave 2: 34 + 18 readers + 12 attacks = 64   total 128, two v1/v2 waves
cost: 11 wave-1 seats + 2 attack seats = the 13-seat overrun, moved to plan time
```
So the overrun is exactly the 13 seats the round refused to cut — not an accident of packing. What
those 13 seats buy is measurable: 14 distinct attack items (highest content-word Jaccard against any
wave-2 attack item 0.250 — r5), 10 of them on objects that did not exist before this round (the
re-key binder, the 18 reader deliverables, the seat overrun, SHONEN at C0, the deciding artefacts).
The round's own amendments 5–9 are the yield precedent: seats, not the L1, found those counter holes.

Priced against the claims:

| option | seats | conforms | cost to the claims |
|---|---|---|---|
| A RED floor, no re-key | 109 (75+34) | total ✔, shape ✘ | credited **46/64, score 6**; `NOHARM coldread-floor` RED on both terms; the deciding gate (`deciding-run.sh:63,70-71`) fails → no green verdict (r3) |
| B re-key k < 18 sections | +k | ✘ | 46 + k < 64 for every k < 18 → floor still RED; not a reachable state |
| C reader-only wave (18) | 127 | total ✔, wave below the 32 floor ✘ | refused by the validator; if forced, the 14 attacks are lost |
| D ≤8-seat residual call (sanctioned form) | 117 | total ✔, shape ✘ | at most 8 of 18 sections read → ≥10 stay uncredited → RED floor |
| E plan-time 64 + 64 | 128 | ✔ both v1/v2 shapes and the cap | 13 seats of coverage dropped at sizing time; needs the credit measure before wave 1 |
| **F actual** | **141** | ✘ +13, third wave | all 18 readers + all 14 attacks |

## Receipts

**R1 — band accounting** (`python3 r1_band_accounting.py LANE`):

```
w1       75  64..128    in band (per-swarm maxLanes=256, hardCeiling=256)
w2       34  32..64     in band (per-swarm maxLanes=256, hardCeiling=256)
w3       32  32..64     in band (per-swarm maxLanes=256, hardCeiling=256)
round total 141 seats; per-L1 round budget maxLanes=256 -> within
BAND_COMPLIANT=true ROUND_TOTAL=141 ROUND_BUDGET=256
```
Verdict: every wave validated; the 256 figure is the validator ceiling, not the round rule.

**R2 — alternative shapes off the specs** (`python3 r2_alt_shapes.py LANE`):

```
w3 composition: 18 re-key readers + 14 attack seats = 32 (the v1 wave floor)
lost headings that force a reader: 18; w3 reader count: 18 -> one reader per lost section
[B] 18 < 32 -> refused, so 32 is the minimum legal standalone reader wave;
    the extra 14 attack seats are what the floor costs, not padding.
[C] wave 2 capacity 64; 34 + 18 readers = 52 (fits); plus w3's 14 attacks = 66 -> over by 2
    to shape-conform: wave 2 = 64, drop 2 attack seat(s), total = 139 seats, 2 waves
DELTA vs dispatched: +1 wave; dispatched carries 2 more attack seats than [C].
```
Verdict: the reader set is minimal (18 = the lost set exactly); the wave is the minimum legal size;
the inline 64-seat fold (C) still exceeds the 128 round cap at 139, so only E conforms (r2's [C] is
the *wave-band* counterexample, not the cap-conforming one).

**R3 — what the RED floor would have cost** (`python3 r3_red_cost.py LANE`, frozen round-21 measure
at C0, no re-key entries):

```
at C0, with no re-key entries: credited=46/64 score=6
missing=18 reasons={"input-drift": 17, "no-ledger-entry": 1}
pre-registered floor (no-harm.sh): score>=8 and credited>=64
deciding gate (deciding-run.sh): coldread-precheck exit 0 or rc=1
NO_REKEY_MONITOR=RED
```
Verdict: the "disclosed miss" is not a monitor note; it is a failed deciding run on the round's
lowest axis (calibration), which is the axis the round exists to move.

**R4 — was the third wave assembled or copied?** (`python3 r4_brief_staleness.py LANE`):

```
C0 commit       2026-10-28 14:16:39 -0300
w2-dispatch.json 2026-10-28 14:18:16.206562490
w3-dispatch.json 2026-10-28 14:21:42.309548534
-> C0 precedes wave-2 dispatch: readers were dispatchable inside wave 2.
freeze.json at the revision w3's brief names (133b2ce): 8 amendments
w3 brief says: 7 amendments (stale by 1 at the revision it names)
w3 brief reader-discipline line: ['# Reader discipline (only the three reader seats)']
w3 brief heading the discipline names: ['Read `## Standing rules` AT 9cf0146b94ddba12d454ebf7288ce6e5']
w3 brief reader JSON path occurrences of /w2/: 4  of /w3/: 0
w3 items that are readers: 18
```
Verdict: wave 3's brief is wave 2's brief with one paragraph appended (20 context lines unchanged;
the diff adds only the "# Why this wave exists" block and rewords line 1). It therefore tells 18
readers it is "the three reader seats", names one section, routes every JSON to `round-55/w2/`, and
carries wave 2's amendment count against wave 3's freeze commit. None of that is fatal — each reader
item names its own section and the binder searches both directories — but it is the overrun's real
non-seat price and belongs in the record.

**R5 — padding and calibration** (`python3 r5_padding_and_totals.py LANE`):

```
w1 28/75 = 37.3%   w2 24/34 = 70.6%   w3 10/32 = 31.2%   (policy floor 25%)
highest content-word Jaccard, w3 attack vs any w2 attack: 0.250 (T55W3RevW2 ~ T55W2RevWaveArtifacts)
r45 81  r46 72  r47 72  r48 96  r49 88  r50 85  r51 124  r52 100 (3 waves)  r53 91  r54 123  r55 141
```
Verdict: no wave is padding by the ≥25 % rule, no wave-3 attack duplicates a wave-2 item, and 141 is
the highest round total in eleven rounds (previous high 124) — the outlier is the total, not a wave.

**R6 — can the wave's product be cashed?** (`python3 .ufo/evidence/round-55/integrate/binder.py
LANE 9cf0146b 9cf0146b <scratch>/out`):

```
Traceback (most recent call last):
  File ".../round-55/integrate/binder.py", line 54, in <module>
    RES[item['heading']] = int(item['n'])
KeyError: 'n'
```
Verdict: the committed pair is inconsistent. `.ufo/evidence/round-55/integrate/resolutions.json`
holds 21 items keyed `id/from/finding/decision/evidence` (wave-1 adjudications, no `heading`, no
`n`); round 54's file was keyed `findings/heading/kind/n/reader/routed`. Until the input is
converted (or the binder made tolerant), the 18 readers cannot be bound at all — the third wave is
necessary but not sufficient, which is a blast-radius fact for the overrun argument, not a reason to
have skipped the readers.

**R7 — where the readers actually wrote** (`python3 r7_reader_coverage.py LANE`, 17:52Z snapshot):

```
reader JSONs per directory: {'w2': 11, 'w3': 5} total 16
distinct headings read: 15 of 18 lost
finding-bearing: 11 of 16 files
cand == C0 for every file: True
```
Verdict: 11 of 16 re-key reader files sit in the **wave-2** directory because the brief's path says
so (R4). The binder's `WAVE_DIRS` covers both, so the bind survives; but the wave-3 record must name
the placement, and any audit scoped to `w3/T55W3R*.json` will see 5 of 16.

## Impacted axes

- **Calibration (primary, the round's lowest axis).** The round's record would otherwise claim a
  conforming dispatch; the frozen contract's own `shape` line already describes a v2 wave plus a
  32–64 v1 wave, which is itself not one of §2's two shapes — so the record needs one honest
  sentence about shape, not three.
- **Operability / cost (secondary).** +13 seats against a 1056 runner ceiling and a 256 validator
  ceiling, dispatched as 75/34/32 — no concurrency risk, but the cap exists to bound exactly this
  kind of drift, so the breach is a cost signal even when harmless in practice.

## The exact sentence the report should carry

> Round total 141 seats in three waves (75 under policy v2 at band 64–128, then 34 and 32 under
> policy v1 at band 32–64 each): **this is a reported shape-conformance defect** — the round
> contract sanctions one v2 wave or two v1 waves summing to ≤128 plus a ≤8-seat residual call, so the
> total exceeds the 128 cap by 13 and the third wave is not one of the two sanctioned shapes — and it
> is the lesser defect, because the 18 sections the content edits drift are exactly the 18 the credit
> measure lists uncredited at C0 (credited 46/64, score 6), 18 is below the 32-seat wave floor and
> the residual call is capped at 8, and the conforming continuation left by a 75-seat wave 1 was 127
> seats with all 14 wave-3 attack seats dropped; every wave passed its own policy band, so no
> validator refused it.

Short form for the report header, same facts:

> 141 seats in three waves (75/34/32), +13 over the 64–128 round cap and outside the two sanctioned
> shapes — a reported shape-conformance defect, taken because the 18-section re-key cannot travel in
> a ≤8-seat residual call and the alternatives were a failed cold-read floor (46/64, score 6) or
> losing all 14 wave-3 attack seats.

## Smallest safe correction

1. **One sentence in the report and the LOG entry**, the text above (round-28 kagi, `:207-209`, is
   the fleet idiom: name the shape defect, the total, the reason). No frozen file is edited —
   `contract.json`'s `shape` stays as frozen and the report carries the deviation beside it.
2. **Name the reader placement.** Record that 11 of the 16 re-key reader JSONs landed in
   `.ufo/waves/round-55/w2/` because the wave-3 brief carries wave 2's reader-discipline line
   verbatim, and that the binder's `WAVE_DIRS` searches both directories (R4, R7). Any
   reader-deliverable audit must scan both.
3. **Unblock the cash-out before the deciding run.** Convert
   `.ufo/evidence/round-55/integrate/resolutions.json` to the binder's `{heading, n, …}` schema (or
   teach `binder.py` to skip items without `heading`), or `binder.py` raises `KeyError: 'n'` at line
   54 and the re-key binds nothing (R6). This is the one correction that changes the round's verdict;
   the overrun itself needs no seat re-run, no production edit and no frozen-file change.
4. Record the brief's two stale cells as dispatch-record facts rather than editing the spec: "7
   amendments" at a commit carrying 8 (R4), and a reader-discipline paragraph describing 3 readers on
   one section when 18 read 18.

## Artifacts opened

`spec-w1.json`, `spec-w2.json`, `spec-w3.json`, `w1-dispatch.json`, `w2-dispatch.json`,
`w3-dispatch.json`, `w2/swarm-registry.json`, `w3/swarm-registry.json` (head),
`.ufo/evidence/round-55/{contract,freeze}.json`, `c1/lost-headings-at-c0.json`,
`c1/measure.py` (read), `c2/measure.py` (read), `no-harm.sh`, `deciding-run.sh`,
`integrate/binder.py`, `integrate/resolutions.json`, the 16 `w2|w3/T55W3R*.json` reader files,
`w2/T55W2Read0{1,2,3}.json`; `scripts/hyaku/lane-addendum.md`, `scripts/hyaku/ufo-wave-policy{,v2}.json`,
`scripts/hyaku/ufo-mission-result.mjs`, `scripts/hyaku/ufo-swarm-wave.mjs`;
`.ufo/reports/round-{18,28,45}/*.md` (precedent), `.ufo/waves/round-44..54` dispatch files (totals);
lane `LOG.md` (round-55 entry), `corpus/QUALITY.md` (criteria 23/33/53/93 lines),
`corpus/lessons/round-55.md` (grep), `.ufo/evidence/round-18/measure.py` (read only).

Tool installs this seat: none. No package manager, no binary, no network fetch.
