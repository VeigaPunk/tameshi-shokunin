# T57W1RevCensus — round-57 census conformance and scratch hygiene

Item: verify census conformance at round start, then scratch directive observation.
Lane base and HEAD: `5e3569969b532310d2b8a3d130901757a3df356b` (lane HEAD unchanged; `git status` shows only the untracked round-57 evidence and wave directories).

## 1. Re-run and comparison

Commands (`S` is my scratch, removed at end):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census   --root /home/vgpnk/Projects/shokunin tameshi
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/clone/corpus/SOURCES.md   # clone checked out detached at 5e35695
```

- Re-run validate exit: 0. Round-start `census-before.exit`: `CENSUS_BEFORE_EXIT=0`. Match.
- Re-run validate stdout is byte-identical to `census-before.stdout` (17 lines). `diff` empty.
- `corpus/SOURCES.md` sha256 `6c2096d8…a6d3` equals the base blob (`git show 5e35695:corpus/SOURCES.md`). The registry is unchanged since base.
- Base clone (5e35695) validate: exit 0. Findings identical to the lane run except the final `ok` line's path, which names the clone instead of the lane.
- Census mode: `rows 142`; tier A 127, B 12, C 3, invalid 0; status mined 114, queued 21, rejected 7, invalid 0; missing 0. Matches the round-start fact of 142 rows.

Receipts: `T57W1RevCensus-receipts/` (`validate-rerun.stdout`, `census-rerun.stdout`, `validate-base-clone.stdout`, `census-before.*`).

## 2. Findings by class

| class | count | ids |
|---|---|---|
| E01–E12 | 0 | none |
| W01 | 1 | S101 (tier C mined, used-by non-—; documented in `## Id allocation`, round 34) |
| W02 | 0 | — |
| W03 | 0 | — |
| W04 | 15 | S047, S048, S075, S076, S077, S078, S081, S092, S104, S160, S265, S266, S267, S268, S274 (duplicate URL across scopes; warnings do not affect status) |

No warning class is new relative to round start. The round-44 note already expects the S160 W04.

## 3. Id contiguity S001–S282

Sweep (`awk` over registry rows at lines 8–159, 13 fields each; `sort | uniq -d`; `comm -23` against `seq 1 282`):

- 142 table rows, 142 unique ids, **0 duplicates**, all rows NF = 13, all ids match `S[0-9]{3,}`, file order is strictly ascending, **0 ids beyond S282**.
- **140 gaps** in S001–S282. Classified (`T57W1RevCensus-receipts/gap-classification.tsv`):

| gap class | ids | documented in SOURCES.md `## Id allocation`? |
|---|---|---|
| retired | S038, S039 (2) | yes: "S038–S039 allocated, never written, retired" |
| unused | S098 (1) | yes: "S098 is not used: seat SrcBashCase could not open" |
| staged reserved | S161–S255 (95) | yes: "staged ids S161–S255 stay reserved by document for the package" (from round 45 onward) |
| **undocumented in registry** | **S109–S131 (23), S133–S151 (19) = 42** | **no.** Mentions appear only in lessons `round-38.md`, `round-39.md`, `round-40.md` (and their verifier spot-checks) as staged-scout ids, refused or "present-but-not-appended". Round-40 lesson line 73 says nine present-but-not-appended and seven refused. The registry's own id-allocation log never names this range. |

Judgement: the 42 undocumented gaps are not errors under the census contract (E03 checks only duplicates; no gap rule exists). They are a documentation gap in the registry's own allocation record. The gaps are the staged scout package's ids (S105–S200 range in round-38 lesson line 60) that were never rowed. Renumbering them would violate "never renumbered", so the fix is a one-line allocation note in a later round (not this wave, because any byte change to SOURCES.md drops cold-read credit per the wave brief).

Next unused id documented: S283 (round-56 note). Consistent with the table (max S282 = REFUSED SLSA row, documented in the round-56 allocation note).

## 4. Scratch directive: `/fast/scratch/hyaku/tameshi-r57/`

Observed at ~21:08 local, with wave-1 seats still running (roster lists them as sub, running):

- **Not empty.** 37 top-level entries. Seat trees range from 0 B to 2.3 GB (`T57W1MutGate` 2.3G, `T57W1LabratFloor` 1.9G, `T57W1ExecFreezeBind` 1.2G, `T57W1ExecForecast` 776M, `L1-exp` 770M, plus roughly 20 seats at ~381 MB each, consistent with a `git clone --shared` working tree of the lane). Also `controls/`.
- **Second observation, 21:09:39:** 39 top-level entries (count rising while peers still write). Still not empty; the wave-1 end state is unmet.
- Empty seat dirs present (`T57W1RevInherited`, `T57W1ScoutSourceA`, `T57W1ScribeItemsR51x1to4`, `T57W1ScribeRecords`, …).
- The directive's precondition ("after every seat of wave 1 is done") is **not yet met**: many seats are still running. The end-state check cannot be scored yet. I did not delete any other seat's tree.
- Fleet-root `/fast/scratch/hyaku/` also holds non-tameshi files (`.c2crit-scorecard.md`, `.gate-sources.md`, `base-scorecard.md`, `c1.json`, `base-repeat-control.py`) outside `tameshi-r57/`. Recorded, not touched.
- My own tree: `T57W1RevCensus/` (381 MB, of which 381 MB is the clone worktree). Removed at end of item.

Recommended for L1 after wave 1 completes: re-run `ls -A /fast/scratch/hyaku/tameshi-r57/ | wc -l` and expect 0. Seats that leave a `clone/` worktree behind will fail that check.

## 5. Tools

None installed or upgraded. All checks used the existing `sources-census.sh`, `awk`, `comm`, `sort`, `seq`, `diff`, `git show`, `sha256sum`.

## 6. Gaps in this check

- The round-start receipt is `validate` output, not `census` output; I re-ran both modes and the census receipt (rows 142) is recorded only from this seat's re-run.
- I did not verify that the 42 undocumented ids correspond exactly to the staged scout package; I verified the lesson-file mentions and the round-40 accounting. A full staged-package cross-check would need `.ufo/waves/round-38…40` staged id files, which were outside this item.
