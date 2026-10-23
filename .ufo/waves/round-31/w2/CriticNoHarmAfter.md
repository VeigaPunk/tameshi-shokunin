# CriticNoHarmAfter

**Verdict: calibration is harmed at the requested content revision; the other five axes show no introduced harm in the inspected cheap-check surfaces. Restoration after wave 2 is not established by this review.** This is a scoped counterexample report, not an admission or round judgment.

Seat: CriticNoHarmAfter. Base: `36c1d3933f680125aeefc447f07db0f03004901a`. Content revision: `2da841bd9913a2037d2bf612793382e572c9d205`. All line citations below refer to committed content at that revision unless explicitly labelled otherwise.

## Verdict per axis

| Axis | What this round touched | Could a standing number drop? | Scoped verdict |
|---|---|---|---|
| calibration | Appended replacement capability/axis tables, corrected the JudgeC1 provenance description, added QUALITY 66–71 and evidence instruments; changed widely read corpus inputs and one SKILL recipe line | **Yes, observed:** strict coverage 64/64 → 55/64, restraint 8 → 6, box3 mismatch 0 → 1, despite unchanged four `[~]` marks. The replacement table says 8 | **Harmed at this revision.** Known intermediate drift is still real; future reads cannot be credited in advance |
| coverage | Added the executable-self-assessment knowledge entry and its index row; added mined S095/S096 and extended S055's used-by | Registry rows increase 92 → 94; no existing coverage scalar is pinned in the standing axis tables. F1–F10 status is expressly unchanged | **Unchanged on existing coverage commitments.** New knowledge is not an invented numerical coverage gain |
| depth | Re-stated the existing nine-case count; no runner/leg edit | Command D remains `recorded_cases=9 depth_score=9` at both revisions | **Unchanged** |
| operability | Added round evidence utilities and safer seat instructions; re-stated existing tool commands and dependencies | No production tool bytes change. A runtime replay count can nevertheless vary: the committed addendum records one existing 9-case/8-passed regression observation. No full runtime certification follows from an empty diff | **Unchanged by the reviewed production-code delta; inherited runtime risk remains**, not a newly repaired capability |
| freshness | Recorded the S055 re-open and new external-source anchors; added dated entry headers and stale-row guidance | No standing freshness scalar exists. Cold-read applicability does drop, but its explicit numerical consequence here is calibration. Census cleanliness does not establish that external teaching is true or newly verified by this seat | **Unchanged on the existing unpinned freshness rubric; source truth not independently rechecked here** |
| adjacency | Cited kumitate's prior art as read-only and distinguished its proxy from tameshi's command-output comparison | No adjacency scalar is pinned; PROVINCE is byte-identical and no sibling product code is changed | **Unchanged**, with the existing ownership boundary retained |

## Evidence

### 1. Isolated execution and actual change surface

Commands ran with cwd `/fast/scratch/hyaku/tameshi-r31-seats/CriticNoHarmAfter/c`, except clone creation and the initial source-repo read-only diff, which ran from this seat's own parent directory. Clone creation/check-out completed with no output and exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 180 git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CriticNoHarmAfter/c
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CriticNoHarmAfter/c checkout -q --detach 2da841bd9913a2037d2bf612793382e572c9d205
```

The requested read-only command was:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat 36c1d3933f680125aeefc447f07db0f03004901a 2da841bd9913a2037d2bf612793382e572c9d205
```

Observed total: `68 files changed, 12496 insertions(+), 2 deletions(-)`. Of these, six are the non-evidence content files: SCORECARD +59 lines, SKILL one-line replacement, QUALITY +98, corpus README +8, SOURCES +15/-1, and the new 84-line knowledge entry. The SKILL change is important: `SKILL.md:1886` adds the seat-owned regression workdir/process discipline. It is not just a corpus-only change.

Actual registry additions are **S095 and S096**, with **S097 the next unused id**, not a third new source row (`corpus/SOURCES.md:104-105,368-377`). The new index row retains all F1–F10 statuses (`corpus/README.md:458-464`). The entry explicitly labels the SCORECARD rule a local inference, not a rule established by the language-documentation sources (`corpus/knowledge/executable-self-assessment.md:31-39`).

### 2. Strongest counterexample: unchanged marks do not preserve calibration credit

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE PYTHONDONTWRITEBYTECODE=1 timeout 150 python3 .ufo/evidence/round-27/c1-measure.py --repo /fast/scratch/hyaku/tameshi-r31-seats/CriticNoHarmAfter/c --rev 36c1d3933f680125aeefc447f07db0f03004901a
```

Observed, exit 0:

```text
C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=36c1d3933f680125aeefc447f07db0f03004901a
```

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE PYTHONDONTWRITEBYTECODE=1 timeout 150 python3 .ufo/evidence/round-27/c1-measure.py --repo /fast/scratch/hyaku/tameshi-r31-seats/CriticNoHarmAfter/c --rev 2da841bd9913a2037d2bf612793382e572c9d205
```

Observed, exit 1:

```text
C1_MONITOR: covered=55/64 restraint=6 box3_mismatch=1 depth_score=9 rev=2da841bd9913a2037d2bf612793382e572c9d205
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ## Pin disposition and provenance correction — round 13
  uncovered: ### Round-13 gate/probe registry
  uncovered: ## Live-tree re-pin and entry-command monitor — round 17
  uncovered: ## Input-keyed cold-read credit — round 17
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ## Ninth recorded case — round 26
```

The wrapper refuses overrides/non-strict results and returns success only for complete coverage, restraint 8 and no mismatch (`.ufo/evidence/round-27/c1-measure.py:35-54`). The underlying formula requires full-page credit for box 3 (`.ufo/evidence/round-18/measure.py:679-683`); matching `[~]` characters alone are insufficient. The recipe itself warns that an unchanged section can lose credit when an input changes (`SKILL.md:1873-1876`).

The new standing row quotes calibration 8 (`SCORECARD.md:1537`), while the directly observed strict monitor gives 6. [INFERENCE] That frozen calibration statement therefore cannot agree at this content revision: the C1 statement invokes this same strict selector (`.ufo/evidence/round-31/c1-measure.py:62-64`). This seat did not run or fabricate a full twelve-statement C1 result.

The new saturation prose also says both owned axes are at or above 8 (`SCORECARD.md:1530-1532`). That is premature as a statement about this content revision. The existing saturation threshold and window are policy, not observed restoration (`SCORECARD.md:257-262`). Do not use the prospective value to waive current repair work.

### 3. Depth, SHONEN and unchanged implementation boundaries

Command D, run once with each literal revision substituted for REV:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git show 2da841bd9913a2037d2bf612793382e572c9d205:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git show 36c1d3933f680125aeefc447f07db0f03004901a:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

Both printed `recorded_cases=9 depth_score=9`, exit 0. The rule is `SCORECARD.md:72-73`; its nine existing case rows are `tools/mutate-and-run.sh:87-95`. No tenth case is claimed (`.ufo/evidence/round-31/contract.json:41-43`).

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git show 2da841bd9913a2037d2bf612793382e572c9d205:SHONEN.md | python3 -c 'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); print("boxes="+str(len(m))+" checked="+str(m.count("x"))+" asserted="+str(m.count("~"))+" untouched="+str(m.count(" "))+" asserted_mark_upper_bound="+str(min(8,2*m.count("~"))))'
```

Observed `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8`, exit 0. All four marks remain lane assertions (`SHONEN.md:5-12`); no new independent authority follows. The JudgeC1 provenance correction is explicit (`SCORECARD.md:1497-1501`; `corpus/QUALITY.md:752-760`).

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff --stat 36c1d3933f680125aeefc447f07db0f03004901a 2da841bd9913a2037d2bf612793382e572c9d205 -- tools/
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff --raw 36c1d3933f680125aeefc447f07db0f03004901a 2da841bd9913a2037d2bf612793382e572c9d205 -- tools/ SHONEN.md PROVINCE.md .ufo/evidence/round-21/coldread/ledger.json .ufo/evidence/round-21/coldread/measure.py .ufo/evidence/round-18/measure.py
```

Both had empty output, exit 0. A read-only committed-blob comparison additionally observed that base SCORECARD, QUALITY and corpus README are byte prefixes, and SHONEN, PROVINCE and the cold-read ledger are byte-identical. The ledger remains unchanged at 2,493,363 bytes: it does not yet contain this wave's restoration.

The unchanged implementation is not a substitute for current runnable receipts. The inherited replay variability is disclosed in `.ufo/evidence/round-31/contract-addendum-1.json:27`; the interop row explicitly discloses a missing-module SETUP rather than claiming runnable success (`SCORECARD.md:1526`). Neither was re-run here. The method/product ownership boundary is unchanged (`PROVINCE.md:14-17,44-47`); the new entry cites, rather than absorbs, kumitate's prior art (`corpus/knowledge/executable-self-assessment.md:36-39`).

### 4. Census

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 60 bash .ufo/evidence/kaika-round-1/sources-census-v2.sh
```

Observed exit 0, rows 94, malformed 0, tiers `A=85 B=7 C=2`, statuses `mined=66 queued=22 rejected=6`, no duplicate ids, no enum/tier-inflation violations, no missing mined used-by paths, no B2 id-or-path failures, and `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`. The B1 informational no-id-cite list still contains 25 entries; it is not a failing census assertion. The retained base output is rows 92 (`.ufo/evidence/round-31/before/c1-at-base.stdout:1`).

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 60 bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate /fast/scratch/hyaku/tameshi-r31-seats/CriticNoHarmAfter/c --today 2026-10-23
```

Observed exit 0, eight W04 warnings for S047, S048, S075, S076, S077, S078, S081 and S092, followed by:

```text
c	ok	/fast/scratch/hyaku/tameshi-r31-seats/CriticNoHarmAfter/c/corpus/SOURCES.md
```

These are the same eight warning ids in the committed baseline (`.ufo/evidence/round-31/before/census-start.stdout:1-9`), not new failures. The external maintained validator was read-only, targeting this clone; it is not asserted to be part of the pinned lane commit. `sha256sum /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` printed `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` for that script. Its documented structural checks do not verify source truth (`scripts/sources-census.sh:24-37`, fleet root).

## Smallest safe correction

Keep the frozen content revision and historical bytes intact. Complete the assigned fresh reads of all nine uncovered sections at that content revision, preserve failing reads honestly, and append only applicable bound entries and their trace receipts. Then measure a **new committed revision** carrying the ledger append with the unchanged strict monitor and frozen C1 counter, and append the actual results and measured hash. The intended restoration is not an observed result here.

Do not fix this by changing SHONEN marks, redefining coverage, weakening the monitor/binding, calling a dispatched seat independent, or awarding saturation from prospective values. Later success cannot make the fixed content revision itself have complete credit. If the final delivered revision still observes restraint 6, cleaner standing rows in exchange for lost calibration are a trade for the canonical Rust judge, not evidence of no harm. This seat makes no admission decision.

Tools installed or updated: none. Only the assigned report and this seat's scratch directory were written. No selftests, regression replay, full C1 counter, binding run, or live external-source reopening was performed by this seat. All started commands completed; no process was killed or left running.
