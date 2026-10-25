# CritWaveAccounting — wave accounting (calibration)

Seat `L1Tameshi43.CritWaveAccounting` (critic). Item: count seats declared, seats with
a committed report, roles used, and any duplicated item text under
`.ufo/waves/round-43/`, and name every seat with no report. Read-only on the lane; the
only write is this file. No installs (system `python3` and `git`; `pacman` not run).

The lane kept moving during measurement; every count below names the rev it was taken
from. Committed counts verified at `HEAD = 6b83a11` (2026-10-25 08:10:15 -0300).

## 0. The three declaration artifacts agree — the disagreement is elsewhere

For each wave, three artifacts should carry the same seat set: `spec-w*.json`
(`items`), `dispatch-w*.json` (`taskCall.tasks`, plus `counts`), and
`<wave>/swarm-registry.json` (`members`). Measured:

| fact | wave 1 | wave 2 |
|---|---|---|
| `spec.items` | 34 | 34 |
| `dispatch.taskCall.tasks` | 34 | 34 |
| `dispatch.counts` | `spawn 34, resume 0, total 34` | `spawn 34, resume 0, total 34` |
| `registry.members` | 34 | 34 |
| spec names = registry keys = dispatch names | yes | yes |
| registry `item` == spec `item` | 34/34 | 34/34 |
| registry `role` == spec `role` | 34/34 | 34/34 |
| `agentId` on members | `null` ×34 | `null` ×34 |
| `updatedAt` | `== createdAt` | `== createdAt` |
| unique `Report:` paths / unique names | 34/34, correct `w1/` dir | 34/34, correct `w2/` dir |

The `spec` template is `{{item}}`-substituted verbatim into every dispatch task
(all 68 tasks are `template.replace('{{item}', item)` + lane-bounds/Judged-on/Report
trailer); the `Judged on:` axis equals `axes[0]` for 68/68.

Two structural facts follow. First, **the registry is a plan, not a ledger**: `agentId`
is null for all 68 members and `updatedAt` was never bumped, so the registry can only
evidence *declared* seats — spawn/return/death can only be evidenced by report files.
Second, `dispatch-w*.stderr` is 0 bytes for both waves, so the dispatch call did not
report an error.

## 1. The counts (for the wave-accounting sentence)

- **Seats declared:** 34 wave-1 + 34 wave-2 = **68** (band 32–64 per wave, round ≤128 —
  in policy).
- **Seats with a committed report** at `HEAD = 6b83a11`: **wave 1 = 32 of 34**;
  **wave 2 = 0 of 34**. The records commit `c5335c7` holds 32 `.md` files under `w1/`.
- **Seats with a report on disk:** wave 1 = **34/34** (every declared name has a file,
  smallest 6132 B, no placeholders, no identical contents, no orphans). Wave 2 =
  **20/34 at ~08:10 -0300** and growing — state the time.
- **Seats with no report:** none in wave 1. The two wave-1 seats **without a committed
  report** are **`CritC1Overfit`** and **`RevC1Counter`** — both files exist on disk but
  are untracked at `6b83a11`. Wave 2: 14 seats have no report yet (in flight).
- **Roles used:** wave 1 = 9 (scout 8, reviewer 7, critic 5, executor 4,
  mutation-tester 3, scribe 3, sentinel 2, connector 1, revenger 1). Wave 2 = 7
  (reviewer 16, mutation-tester 6, critic 5, executor 2, sentinel 2, scout 2,
  simplifier 1). Union across the round = **10**. Attack-role share
  (reviewer+critic+mutation-tester): wave 1 = 15/34 (44%), wave 2 = 27/34 (79%) — both
  well over the ≥25% attack rule. `simplifier` appears only in wave 2; `scribe`,
  `connector`, `revenger` only in wave 1.
- **Duplicated item text:** **none**. All 68 item strings are byte-distinct within each
  wave, across waves, and against all 85 round-42 spec items (exact and fuzzy ≥0.60).
  No name or `Report:` path is shared. Near-duplicates (same artifact, re-run): wave-2
  `ScoutCensusDrift` re-runs wave-1 `ExecCensus`'s census command (Jaccard 0.38), and
  five wave-2 seats re-attack a wave-1 seat's instrument (`RevC2Classes2`←`RevC2Classes`,
  `RevC3Tool2`←`RevC3Tool`, `RevC3Counter2`←`RevC3Counter`, `RevC1Predicate`←`RevC1Counter`,
  `MutC1LiveGate`/`MutC1GateRemoved`←`MutC1F11`'s counter). These are intentional
  re-verification, not duplicated assignments — but the report should count wave 2 as
  34 attack seats of which 5–6 re-run wave-1 targets, not 34 fresh coverage seats.

**Suggested sentence** (drop-in, with the caveats the LOG defers here):

> Wave shape: default two v1 waves (policy v1, band 32–64). 34 declared seats in wave 1
> (9 roles, 15 attack) and 34 in wave 2 (7 roles, 27 attack), 68 total, every seat name
> and report path unique and item text unduplicated. Wave 1 has 34 reports on disk but
> 32 committed — `CritC1Overfit` and `RevC1Counter` landed after the records commit
> `c5335c7` and are still untracked, and 9 of the 32 committed reports have since been
> revised; wave 2 has 0 committed reports at measurement (in flight). No dead seat is
> recorded. The two waves overlapped: the wave-2 registry was created while wave-1
> seats were still writing.

## 2. Findings that would falsify a naive sentence

### F1 — "the records commit carries every wave-1 seat report" is false (committed bytes)

`c5335c7` (`round-43: records — … receipts and wave-1 seat reports`) contains 32 `.md`
files under `w1/`, not 34. Absent: `CritC1Overfit.md`, `RevC1Counter.md` — both now on
disk untracked, with `Seat:` headers matching their registry names, so they are genuine
seat reports that landed late. Reproduce:

    $ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree --name-only \
        c5335c7 .ufo/waves/round-43/w1/ | grep -c '\.md$'     # → 32
    $ git -C … status --porcelain .ufo/waves/round-43/w1 | grep -c '^??'   # → 2

A report sentence saying "34 wave-1 seat reports committed" or "every wave-1 seat
report" overstates the committed record by 2.

### F2 — the committed wave-1 record and the measured wave-1 record have diverged

9 of the 32 committed `w1/*.md` are dirty at `6b83a11`
(`CritC2Vacuous, CritC3Maps, MutC3Selftest, RevC2Classes, RevC3Tool, RevProvenance,
RevReportDraft, ScribeLessonGate, ScribeQuality`; `git diff --stat` ≈ 800+/550- line
churn). These are the seats' own post-commit revisions — e.g. `CritC3Maps` now carries
a three-rev substrate table. So "the wave-1 record" is rev-dependent: at `c5335c7` it
is 32 reports in an older form; at `6b83a11` it is still 32 committed plus 9 divergent
working copies plus 2 untracked. The accounting sentence must pin the rev or say both
numbers. (`git status` under `.ufo/waves/round-43/w1/` reproduces this.)

### F3 — wave 2 was dispatched before wave 1 returned

`w2/swarm-registry.json` `createdAt = 2026-10-25T11:03:27.139Z` (08:03:27 -0300).
Eight wave-1 report mtimes fall **after** it (`stat -c %y`):
`RevC1Counter` 08:05:35, `RevC2Classes` 08:05:42, `RevC3Tool` 08:05:51,
`ScribeQuality` 08:06:20, `MutC3Selftest` 08:06:51, `RevReportDraft` 08:06:58,
`CritC1Overfit` 08:06:59, `RevProvenance` 08:07:05. Two are still uncommitted. The
addendum's default shape requires wave 2 "dispatched after wave 1 returns"
(`scripts/hyaku/lane-addendum.md:50-52`), and `LOG.md:2250` says "wave 2 fresh
attackers after wave 1 returns". The bytes show a ≥3-minute overlap. The sentence must
not repeat "after wave 1 returns"; say "dispatched while wave-1 stragglers were still
writing" or name the gap. Caveat: mtimes are filesystem evidence, not committed bytes —
but the two `??` reports are committed-byte-visible.

### F4 — three different "freeze" identities are asserted; the contract disagrees with the assignment and the records

- `contract.json::amendments` now has **14** entries; `frozen_before` declares the
  freeze of record `114ffacd…` (reached through A6/A7).
- The wave-2 dispatch context (my own assignment) names freeze `3aee2c0` and "A1–A9".
- `SCORECARD.md:2053` and `LOG.md:2222` say "frozen at `17f6ef0`".
- `SCORECARD.md:2055` says "amendments A1–A3 are pre-data"; `LOG.md:2224` says "A1–A3
  pre-data; A4 the guard repair from a wave-1 mutation-tester". The contract's own
  `when` fields say A1–A3 "before any seat ran", **A4–A11 "during wave 1"**, and
  **A12–A14 "during wave 2"** (`bb36f80` 08:07:08, `f551ca6` 08:09:07, `6b83a11`
  08:10:15 -0300 — three freezes landed while wave-2 seats were already writing). The
  committed records under-report amendments by 10 (LOG) / 11 (SCORECARD), and each
  seat's "the freeze" refers to different bytes per wave and per phase.
  (RevLog43/RevSC43/RevAmendments own the cells; this is the wave-shape facet.)

### F5 — no dead seats, but the evidence trail cannot prove it

Every declared name has a report on disk in wave 1 (34/34), so "no dead seat" is
consistent with the record; because the registry never binds an `agentId`, a death
would surface only as a missing report — none is missing in wave 1. Wave 2 is in
flight: a "no dead seats" claim about wave 2 would be premature.

## 3. Impacted axes and the smallest safe correction

- **Axis impacted: calibration.** The wave-accounting sentence is a counting sentence;
  `32 committed / 34 declared` vs "all 34" is the difference between a true and a
  false record claim. Depth/operability are only touched through their seats' rev
  provenance (F3/F4), which other seats own.
- **Smallest safe correction:** in the report, state the counts as "34 declared per
  wave (68 total), 32/34 wave-1 reports committed at `c5335c7`
  (`CritC1Overfit`, `RevC1Counter` late, untracked), 0/34 wave-2 committed at
  measurement, no duplicated item text, 10 roles; wave-2 dispatched while wave-1
  stragglers wrote" — and do not reuse the LOG's "after wave 1 returns" wording.

## Reproduce

```bash
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
# declared seats (all three artifacts agree):
python3 -c "import json;[print(w, len(json.load(open(f'.ufo/waves/round-43/{w}/swarm-registry.json'))['members'])) for w in ('w1','w2')]"
python3 -c "import json;[print(w, len(json.load(open(f'.ufo/waves/round-43/spec-{w}.json'))['items']), len(json.load(open(f'.ufo/waves/round-43/dispatch-{w}.json'))['taskCall']['tasks'])) for w in ('w1','w2')]"
# committed reports:
git ls-tree --name-only c5335c7 .ufo/waves/round-43/w1/ | grep -c '\.md$'   # 32
git ls-files .ufo/waves/round-43/w1/*.md | wc -l                           # 32
git ls-files .ufo/waves/round-43/w2/*.md | wc -l                           # 0
git status --porcelain .ufo/waves/round-43/w1/                             # 9 M + 2 ??
# seats absent from the records commit:
comm -13 <(git ls-tree --name-only c5335c7 .ufo/waves/round-43/w1/ | xargs -n1 basename | sed 's/\.md$//' | sort) \
         <(python3 -c "import json;print('\n'.join(sorted(i['name'] for i in json.load(open('.ufo/waves/round-43/spec-w1.json'))['items'])))")
# → CritC1Overfit, RevC1Counter
# duplicated item text (should print 0):
python3 -c "import json,collections;c=collections.Counter(i['item'] for w in ('w1','w2') for i in json.load(open(f'.ufo/waves/round-43/spec-{w}.json'))['items']);print(sum(1 for v in c.values() if v>1))"
# wave-2 dispatch timestamp vs late wave-1 writes:
python3 -c "import json;print(json.load(open('.ufo/waves/round-43/w2/swarm-registry.json'))['createdAt'])"
stat -c '%y %n' .ufo/waves/round-43/w1/*.md | sort
```
