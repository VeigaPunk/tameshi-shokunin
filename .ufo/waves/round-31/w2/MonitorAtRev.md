# MonitorAtRev — strict cold-read monitor at 2da84 vs base

VERDICT — CONFIRMED, no missed section. At `2da841bd9913a2037d2bf612793382e572c9d205` (REV) the strict monitor reports
`sections_covered 55 / sections_total 64`, `calibration_restraint_score 6`; at base `36c1d3933f680125aeefc447f07db0f03004901a`
it reports `64 / 64`, `8`. The nine uncovered sections are exactly the nine sections this wave's Cold* readers were given
(three reads each, one per group A, B and C, grouped differently), and no drifted section is missing from the reading set.
Eight sections lost credit because a recorded input file's digest changed at REV (`corpus/README.md`, `corpus/SOURCES.md`,
`corpus/QUALITY.md`); the ninth, `SKILL.md:1855`, lost its ledger entry because the one-line `SKILL.md` edit at line 1886
changed that section's body sha256 — no input file of it changed.

## 1. Measurements

| revision | sections_covered / total | calibration_restraint_score | depth_score | box3_full_page | trace_gate | overrides_used |
|---|---|---|---|---|---|---|
| base `36c1d393` | 64 / 64 | 8 | 9 | true | strict | false |
| REV `2da841bd` | 55 / 64 | 6 | 9 | false | strict | false |

Both runs used `ledger_source: "rev"`, `ledger_committed: true`, and the same ledger blob (`dba8d1e23f5015036524219fcf8278e89fdd2153`) and
measure blobs (`9643f7032ae6fde843464d4ef6bc0c5919518528` for `.ufo/evidence/round-18/measure.py`, `9eb05868558224a1aaec3054de47feaf7219225a`
for `.ufo/evidence/round-21/coldread/measure.py`) at base and REV, so the delta is tree content, not instrument drift.

The score drop is the box-3 rule, not a new restraint judgement: `calibration_restraint_score = 2+2+2 + 2*box3_points` with
`box3_points = box3_marked and box3_link and box3_full_page` (`.ufo/evidence/round-18/measure.py:681-683`). `box3_full_page` is
`sections_covered == sections_total` (`:655`), so the same 55/64 reading removes exactly 2 points (8 → 6). The four `[~]` marks
and the box-3 ledger link are unchanged at both revisions (`shonen.asserted 4`, `box3_marked true`, `box3_ledger_link true`).

## 2. The nine uncovered headings, with the monitor's exact reasons

| start | heading | reason (verbatim from `mon-rev.json`) |
|---|---|---|
| 131 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | `input-drift:corpus/QUALITY.md;input-drift:corpus/README.md;input-drift:corpus/SOURCES.md;input-drift:corpus/QUALITY.md;input-drift:corpus/README.md;input-drift:corpus/SOURCES.md;input-drift:tools/mutate-and-run.sh;input-drift:corpus/README.md;input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh` |
| 375 | `## Restore discipline — before/after identity, not continuous non-write proof` | `input-drift:corpus/README.md;input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh` |
| 1380 | `### The map — where a reader enters, artifact by artifact` | `input-drift:corpus/README.md;input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh` |
| 1517 | `## Pin disposition and provenance correction — round 13` | `input-drift:.ufo/evidence/round-17/coldread/assemble.py;input-drift:.ufo/evidence/round-17/measure.py;input-drift:corpus/knowledge/incremental-pin-disposition.md;input-drift:tools/bash-witness-study.py;input-drift:tools/mutate-and-run.sh;input-drift:corpus/SOURCES.md;input-drift:corpus/SOURCES.md;input-drift:corpus/knowledge/incremental-pin-disposition.md;input-drift:tools/bash-witness-study.py;input-drift:tools/mutate-and-run.sh;input-drift:corpus/SOURCES.md;input-drift:tools/bash-witness-study.py;input-drift:tools/mutate-and-run.sh;input-drift:tools/trace-inputs.py;input-drift:corpus/SOURCES.md;input-drift:tools/mutate-and-run.sh` |
| 1548 | `### Round-13 gate/probe registry` | `input-drift:corpus/SOURCES.md;input-drift:corpus/SOURCES.md;input-drift:tools/bash-witness-study.py;input-drift:tools/mutate-and-run.sh;input-drift:corpus/SOURCES.md;input-drift:tools/bash-witness-study.py;input-drift:tools/mutate-and-run.sh;input-drift:tools/trace-inputs.py;input-drift:corpus/SOURCES.md;input-drift:tools/mutate-and-run.sh` |
| 1814 | `## Live-tree re-pin and entry-command monitor — round 17` | `input-drift:corpus/QUALITY.md;input-drift:corpus/README.md;input-drift:corpus/SOURCES.md;input-drift:tools/mutate-and-run.sh;input-drift:corpus/SOURCES.md;input-drift:corpus/SOURCES.md;input-drift:tools/mutate-and-run.sh` |
| 1855 | `## Input-keyed cold-read credit — round 17` | `no-ledger-entry` |
| 1938 | `### Round-20 gate/probe registry — frozen receipt instruments` | `input-drift:corpus/QUALITY.md;input-drift:corpus/QUALITY.md;input-drift:corpus/SOURCES.md;input-drift:corpus/QUALITY.md;input-drift:corpus/SOURCES.md;input-drift:tools/registry.json` |
| 2104 | `## Ninth recorded case — round 26` | `input-drift:corpus/QUALITY.md;input-drift:corpus/README.md;input-drift:corpus/SOURCES.md;input-drift:corpus/SOURCES.md;input-drift:tools/mutate-and-run.sh` |

At base the same sections are credited: the base run's `coldread.missing` is empty and `coldread.reasons` is `{"credited": 64}`.

## 3. Why each is uncovered

Mechanism: a section is matched to ledger entries by the sha256 of the section's own bytes; an entry credits only when every recorded
input digest verifies at REV (`sha256(git cat-file blob REV:<path>) == recorded`, `.ufo/evidence/round-18/measure.py:330-350`); a
section with no entry for its sha is `no-ledger-entry` (`:614`). The reason string is the `;`-joined union over that section's entries,
so it names both the inputs that changed at REV and older stale records.

Changed recorded inputs, base → REV:

| path | sha256 at base | sha256 at REV |
|---|---|---|
| `corpus/README.md` | `636b716e7891f09cc3eb4a2c47bcf3a5120460c356dcfc07f5d8ba9b63259909` | `0b68064b9d65a93eb8abfbcd86736cff927f827894d643449e413b3aa7212cbd` |
| `corpus/SOURCES.md` | `b830d6fa03699f15bcfaeb7579899d247284b7a85a17e7ddb61a979a451007c7` | `489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741` |
| `corpus/QUALITY.md` | `f7e0dc952e6dc8c06dee59767b065a635920ce1a281cf8d4fa3d9e9420356a7a` | `6cbf9cf7a9117a747be356f7ac5ed8288c8609195205bcca427809b4d96804ac` |

Per section, the recorded input that changed (entry whose inputs were clean at base and fail at REV, plus the single-file revert
result in section 5):

| section | former clean entries at base → REV failure | minimum changed input |
|---|---|---|
| 131 `## Mutation-sweep recipe` | two entries, one failing on README only, one on all three | `corpus/README.md` (sufficient alone) |
| 375 `## Restore discipline` | three entries, each failing on README only | `corpus/README.md` |
| 1380 `### The map` | two entries, each failing on README only | `corpus/README.md` |
| 1517 `## Pin disposition … round 13` | two entries, each failing on SOURCES only | `corpus/SOURCES.md` |
| 1548 `### Round-13 gate/probe registry` | two entries, each failing on SOURCES only | `corpus/SOURCES.md` |
| 1814 `## Live-tree re-pin … round 17` | two entries, each failing on SOURCES only | `corpus/SOURCES.md` |
| 1938 `### Round-20 gate/probe registry` | two entries: one on QUALITY only, one on QUALITY+SOURCES | `corpus/QUALITY.md` (sufficient alone) |
| 2104 `## Ninth recorded case … round 26` | two entries: one on SOURCES only, one on all three | `corpus/SOURCES.md` (sufficient alone) |
| 1855 `## Input-keyed cold-read credit` | none — section identity changed, see below | `SKILL.md` body line 1886 |

The ninth section is not input drift. `git diff -U0 36c1d393 2da841bd -- SKILL.md` is one changed line:
`@@ -1886 +1886 @@ Recipe for one bucket, cold:` — the sentence that now also says "A seat gives every `--regression` a `--workdir`
under its own scratch dir … (round 31; QUALITY 67)". Line 1886 falls inside the section that starts at 1855 and ends at 1896 (next
heading `### Round-17 gate/probe registry — input-keyed credit` at 1897). The section's sha256 therefore changes from
`43a041e711564e5a…` at base (two ledger entries, one credited at base via `read_rev 8eaae28ec4a3`) to `4869ae55bc8ed104…` at REV
(zero entries), giving `no-ledger-entry`. `SKILL.md` is in `IGNORED_INPUTS`, so it is never an input digest; only the section sha
picks it up. 63 of the 64 section body shas are identical between base and REV; 1855 is the only one that changed.

Inherited stale components, not this round's drift: `tools/mutate-and-run.sh` is byte-identical at base and REV
(`a7d3f2dd7d47…` both), yet a round-17-era entry for section 375 records `fb91ef7621f5…`; likewise
`tools/bash-witness-study.py`, `tools/trace-inputs.py`, `corpus/knowledge/incremental-pin-disposition.md`,
`.ufo/evidence/round-17/coldread/{assemble,measure}.py` and `tools/registry.json` are unchanged base→REV but recorded stale by older
entries. They appear in the reason strings because reasons union every entry; only the three corpus files are new drift. Of the six
non-`.ufo` files changed base→REV, `SCORECARD.md` is recorded as an input in two entries (starts 17 and 1155) with no formerly clean
entry newly failing on it, and `corpus/knowledge/executable-self-assessment.md` is new and recorded by no entry, so neither costs a
section.

## 4. Is the drifted set exactly the cold-reader set?

Yes, both directions. The wave-2 spec (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-31/spec-w2.json`) assigns:

| group | item → section starts | distinct sections per group |
|---|---|---|
| A | ColdA01 → 131, 375, 1380; ColdA02 → 1517, 1548, 1814; ColdA03 → 1855, 1938, 2104 | all 9 |
| B | ColdB01 → 375, 1380, 1517; ColdB02 → 1548, 1814, 1855; ColdB03 → 131, 1938, 2104 | all 9 |
| C | ColdC01 → 1380, 1517, 1548; ColdC02 → 1814, 1855, 1938; ColdC03 → 131, 375, 2104 | all 9 |

The union is exactly `{131, 375, 1380, 1517, 1548, 1814, 1855, 1938, 2104}` — the monitor's nine uncovered starts — with each section
read exactly three times, once per group. No section outside the nine is assigned to a Cold item; no drifted section is unassigned.
Missed section: none. The 27 reason strings quoted in the spec prompts also equal the monitor's reasons at REV (re-extracted and
compared programmatically: 27/27 match, 0 mismatch), so no reader was dispatched with a stale reason.

## 5. Falsifier — single-file reverts

In my sandbox clone only, I committed one revision per corpus file with just that file reverted to base (`git checkout <base> -- <file>`;
commits `ba1b3475` README, `ed5d5df9` SOURCES, `bbc3c0fe` QUALITY), then ran the monitor at each:

| synthetic revision | sections covered | uncovered starts |
|---|---|---|
| README reverted `ba1b3475` | 58 / 64 | 1517, 1548, 1814, 1855, 1938, 2104 |
| SOURCES reverted `ed5d5df9` | 59 / 64 | 131, 375, 1380, 1855, 1938 |
| QUALITY reverted `bbc3c0fe` | 56 / 64 | 131, 375, 1380, 1517, 1548, 1814, 1855, 2104 |

This reproduces the causal map above: README alone restores 131, 375, 1380; SOURCES alone restores 1517, 1548, 1814, 2104; QUALITY
alone restores 1938; 1855 never returns. These revisions exist only in `/fast/scratch/hyaku/tameshi-r31-seats/MonitorAtRev/c` and are
not lane revisions.

## 6. Method caveat (exact tool semantics)

The frozen credit algorithm is `.ufo/evidence/round-18/measure.py`, but the round-21 wrapper adds its own ledger path to the ignore
set (`.ufo/evidence/round-21/coldread/measure.py:112`: `module.IGNORED_INPUTS = module.IGNORED_INPUTS | frozenset((LEDGER,))`).
Importing the round-18 module directly (without that patch) reports 56/64 and an extra uncovered section at start 1964
`### Round-21 gate/probe registry — finite environment differential`, because one of that section's entries records
`.ufo/evidence/round-21/coldread/ledger.json` as an input. The cited 55/64 is the wrapper's value and is the one that matches the wave
context and the spec prompts; reproduce with the wrapper command, not with a direct module import.

## 7. Commands and retained evidence

```text
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/MonitorAtRev/c
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/MonitorAtRev/c checkout -q --detach 2da841bd9913a2037d2bf612793382e572c9d205
2da841bd9913a2037d2bf612793382e572c9d205

$ cd /fast/scratch/hyaku/tameshi-r31-seats/MonitorAtRev/c && python3 .ufo/evidence/round-21/coldread/measure.py --repo /fast/scratch/hyaku/tameshi-r31-seats/MonitorAtRev/c --rev 2da841bd9913a2037d2bf612793382e572c9d205 > /fast/scratch/hyaku/tameshi-r31-seats/MonitorAtRev/mon-rev.json
exit 0; revision 2da841bd9913a2037d2bf612793382e572c9d205; sections_covered 55 / 64; calibration_restraint_score 6; depth_score 9; box3_full_page False; trace_gate strict; overrides_used False

$ same command with --rev 36c1d3933f680125aeefc447f07db0f03004901a > mon-base.json
exit 0; sections_covered 64 / 64; calibration_restraint_score 8; depth_score 9; box3_full_page True; uncovered []

$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../c diff --name-only 36c1d393 2da841bd
68 files; the 6 outside .ufo/: SCORECARD.md, SKILL.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md, corpus/knowledge/executable-self-assessment.md

$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../c diff -U0 36c1d393 2da841bd -- SKILL.md
@@ -1886 +1886 @@ Recipe for one bucket, cold:   (one replaced line)

$ sha256sum SKILL.md   # in the clone at REV
2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a
```

Retained under `/fast/scratch/hyaku/tameshi-r31-seats/MonitorAtRev/`: `mon-rev.json`, `mon-base.json`,
`mon-revless-{README,SOURCES,QUALITY}.json`, and the probes `probe.py`, `probe2.py`, `probe3.py`, `probe4.py`, `probe5.py`, `probe6.py`.
No file outside my scratch dir and this report was written; no process was left running; no tool was installed.

## 8. Risks and blockers

- The base reading (64/64, 8) shows the loss is introduced by REV alone; the nine-section reading set is therefore complete, and a
  reader assigned to any of these nine is not reading a section that merely appears in a stale reason string.
- The reason strings overstate new drift: components such as `tools/mutate-and-run.sh` and the round-17 instruments are inherited
  staleness. A planner who reads them as round-31 edits would mis-rank the cause.
- The `no-ledger-entry` case is the only one that cannot regain credit by restoring an input; it needs a fresh ledger entry for the new
  section sha, which the lane's assemble step produces from fresh reads.
- No blockers. The monitor is read-only; the only mutating operations were clonings and synthetic commits in my own scratch clone.

## 9. Smallest safe correction

No production or plan change is indicated. Do not edit the ledger, the three corpus inputs, or the monitor to recover the number:
the nine sections are correctly identified as drifted, and the Cold* assignment already covers each of them three times. The lane's
existing path — fresh reads at REV, then `assemble.py --carry` — is the only correct repair. Whether the score returns to 8 is an
outcome of those reads, not something this measurement can assert [INFERENCE: 64/64 and `box3_full_page true` require all nine new
entries to credit under the strict gate].
