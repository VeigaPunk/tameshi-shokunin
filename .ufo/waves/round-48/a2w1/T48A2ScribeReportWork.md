# T48A2ScribeReportWork — report-fidelity seat (round 48, a2w1)

Axes: calibration (record fidelity) and freshness (whether the report's pointers resolve at the revision the report
describes). Deliverable: `.ufo/waves/round-48/a2w1/T48A2ScribeReportWork.draft.md` (the `## Work performed` and
`## Landed changes` sections only; the L1 writes the report). No claim verdict was produced here and none was rerun:
the two counters were not invoked by this seat.

## What the draft states

Both claims are named with their axes in the opening — C1 calibration (lowest non-retired axis, monitor 6) at
`.ufo/evidence/round-48/contract.json:82-95` and C2 freshness (the sourced claim) at `contract.json:96-125` — followed
by 13 work-item bullets, each with a path:line or commit pointer:

- pre-registration `e73389c0` (contract, census start exit 0) and pre-data amendments 1-3 `f1cfaad3`
  (`contract.json:9-26`);
- the counter freeze `7552984` with both counter sha256s (`freeze-2.json:12-24`), selftests 76/76 and 43/43
  (`selftest/*.stdout`), the two control harnesses, `deciding-run.sh`, no-harm 8 of 8 and cold-read 60 at base;
- amendments 4-10 as the wave-1 attack's product (`contract.json:27-68`), with the two reversals it caused
  (`w1/T48RevenEnvDiff.md`, `w1/T48RevenRegression.md`);
- wave 1's 32-seat dispatch, crash, and the 24 seat reports it left (`spec-w1.json`, `w1/`);
- the salvage commit `15b1521` marked as the orchestrator's, not a landing (`LOG.md:2361`);
- the C1 `--emit` observation at the salvage tip, 55 minutes, exit 1, `total=22 unparsed=22` as the before datum, and
  its `fleet_drift=1` explained by the counter's cleanliness pathspec (`calibration/measure.py:376-380`) with the cause
  marked `[INFERENCE]`;
- C2's CTL_F/G/H receipt (`control/c2-controls.stdout`, F=0 G=0 H=2, meta naming the revisions) and the C2 records
  (rows at `corpus/SOURCES.md:140-143`, snapshots/receipts, Gate lines at `corpus/lessons/round-48.md:19-24`, entries
  re-pointed);
- the mistake/criterion/falsifier chain (`lessons/round-48.md:350-361`, QUALITY 96-97, `pointer-check` red + selftest);
- the `a2w1` dispatch at `17cc5ce` with its role split, and a time-stamped snapshot of how many seats had reported;
- a pending bullet listing what does not exist yet, and a hygiene bullet.

`## Landed changes` ties every change to the round's LOG entries (`LOG.md:2348-2357`, `LOG.md:2359-2368`) and to a
commit: `e73389c0`, `f1cfaad3`, `7552984`, `5054532`, `c7586b9a`, `17cc5ce`; `15b1521` is marked **not a landing** and
`41c1bc0` (the fleet-level `considerthese/2026-10-26.md` reflection) is marked **outside the round's claims**; the
receipts-only commit is a `<PENDING>` placeholder. All eight 40-hex hashes were checked with
`git rev-parse --verify <h>^{commit}` in the lane (8/8 present).

## Verification I did run

- 40-hex hashes in the draft: 8/8 resolve (`git -C tameshi-shokunin rev-parse --verify --quiet <h>^{commit}`).
- Every path:line pointer in the draft: re-read against the tree; six citations were corrected during the work
  (`contract.json` amendment range 30-71 → 27-68, amendments 1-3 8-29 → 9-26; `LOG.md` "attempt 1 scored none" and the
  `c1-controls` naming 2366/2367 → 2364; the attempt-2 LOG section 2359-2370 → 2359-2368; QUALITY 95's falsifier
  1424 → 1418 and criterion 97's range 1426-1440 → 1428-1434; `corpus/QUALITY.md:1380-1440` → 1380-1434).
- Absence claims: `ls .ufo/evidence/round-48/after` → No such file or directory;
  `git cat-file -e c7586b9a:.ufo/evidence/round-48/control/c1-controls.stdout` → does not exist (exit 128);
  `git status --porcelain` in the lane → only `?? .ufo/waves/round-48/a2w1/` and `?? .ufo/waves/round-48/a2w1.ready.dispatched` (the orchestrator's dispatch marker, created after the content revision).
- One read-only probe of the round's own new criterion (not a claim counter, not a verdict):
  `python3 .ufo/evidence/round-48/quality/pointer-check.py --lane LANE --rev c7586b9a --file corpus/QUALITY.md --start "## Criteria appended — round 48"`
  → `checked=11 missing=2`, exit 1 (`control/c1-controls.stdout`, `quality/c94-96-falsifiers.stdout`).

## Findings

### F1 — the C2 lesson cites the wrong `SOURCES.md` lines for S267 and S268 (content record, fixable)

`corpus/lessons/round-48.md:62` states "Row change: `corpus/SOURCES.md:140` appends S267" and
`corpus/lessons/round-48.md:84` states "`:141` appends S268". At the content revision those lines hold S265 and S266;
S267 is at `corpus/SOURCES.md:142` and S268 at `:143`.

Command that shows it:

```
grep -n '^| S26[5-8] |' corpus/SOURCES.md
# 140:| S265 …  141:| S266 …  142:| S267 …  143:| S268 …
```

Impact: the C2 counter reads the rows by id, not by line, so `C2_R48_PASS` is unaffected; the lesson's pointer is
wrong, and a reader following it lands on the S026 supersession instead of S093's. This is a `reference-drift` of the
class the lesson's own `## Mistakes` table names. Remedy is an appended erratum (the round's convention: records are
never rewritten), and the draft therefore cites `:142`/`:143`, not the lesson's numbers.

### F2 — QUALITY 97 does not yet hold at the revision that lands the QUALITY block (pending, not a defect until the receipts commit)

At `c7586b9a` the QUALITY round-48 block cites 11 lane paths, of which two do not exist:
`.ufo/evidence/round-48/control/c1-controls.stdout` (criterion 95's falsifier, `corpus/QUALITY.md:1418`) and
`.ufo/evidence/round-48/quality/c94-96-falsifiers.stdout` (criterion 94's, `corpus/QUALITY.md:1398`). Criterion 97
tests pointers at the round's *landing tip*, so this is satisfied if the pending receipts-only commit carries both
files; it is violated if the report claims criterion 97 verified at `c7586b9a`. Related: `quality/falsifiers.sh:32-35`
exits `CRITERION-95-FALSIFIER-VACUOUS` while the first file is absent, and CTL_A-E have been designed and scripted
(`control/run-controls.py`) but never receipted, although the freeze plan, `LOG.md:2364` and `corpus/QUALITY.md:1418`
all name their receipt. The draft records this as pending rather than as a control result.

### F3 — pointer-check resolves bare evidence sub-paths to round 48, so the lesson's round-47 shorthand reads as missing (checker scope, disclosure for the L1)

`quality/pointer-check.py:22-24,32-34` maps a bare `after/`, `before/`, `control/`, `selftest/`, `quality/`,
`calibration/` or `freshness/` prefix to `.ufo/evidence/round-48/`. The lesson writes round-47 receipts in that shorthand
(`corpus/lessons/round-48.md:110,117` `before/c1-at-freeze.stdout`; `:153` `after/c1.stdout`; `:161,182`
`control/emit-observed-pre-freeze.out`), so a landing-tip run over the lesson prints 7 `MISSING` lines of which only two
are the pending round-48 receipts:

```
python3 .ufo/evidence/round-48/quality/pointer-check.py --lane LANE --rev c7586b9a --file corpus/lessons/round-48.md --start '# Round 48 lesson'
# POINTERS: checked=46 missing=7 skipped=2
# 4 = round-47 shorthand (before/c1-at-freeze.stdout, after/c1.stdout, after/c1.exit, control/emit-observed-pre-freeze.out),
#     each PRESENT at its full .ufo/evidence/round-47/ path (git cat-file -e c7586b9a:<full path> → 0)
# 1 = .ufo/evidence/round-47/selftest, cited for holding 0 files and absent from the tree (git ls-tree -r … | wc -l → 0)
# 2 = the pending round-48 receipts of F2
```

Reading those 7 as defects would misreport; reading them as 0 would hide F2. The draft keeps the count out of the
claims and the L1 should state it this way if the lesson block is cited at all.

### F4 — hygiene, no action

No tool installed or upgraded (pacman paused host-wide; nothing needed). No lane file outside the wave report
directory was written by this seat; the only untracked paths in the lane are the wave directory `.ufo/waves/round-48/a2w1/` and the orchestrator's `a2w1.ready.dispatched` marker. Scratch
`/fast/scratch/hyaku/tameshi-r48/T48A2ScribeReportWork` was created for the probe and removed; the draft live on disk
is the deliverable. Out of scope and untouched: the deciding run, both counters' scoring, `corpus/`, `tools/`,
`SCORECARD.md`, the fleet repo and sibling lanes.

## Limits

- The draft's `<PENDING>` marks are the L1's to fill from `after/` and from the CTL_A-E receipt; nothing in the draft
  states an after value, a verdict or a seat count that had not landed at 2026-10-26T10:46 -03 (38 of 64 `a2w1`
  reports present then, wave in flight).
- The C1 `fleet_drift=1` cause is marked `[INFERENCE]` because the working tree during the 09:27-10:22 emit cannot be
  observed now; what is observed is the FLEET lines (`lane_clean=1` at point 1, `0` at points 2-4) and the pathspec in
  `calibration/measure.py:376-380`.
- F1's impact on C2 is bounded by reading the counter, not by running it: the counter selects a superseding row by its `teaches` cell prefix
  (`freshness/measure.py:213-227`), not by file line, so a lesson line number cannot move `refreshed`.
