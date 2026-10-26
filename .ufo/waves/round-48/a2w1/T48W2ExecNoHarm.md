# T48W2ExecNoHarm — round-48 no-harm monitors at CONTENT (attempt 2, a2w1)

Seat: executor, leaf. Item: run the round-48 no-harm monitors at CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17`
in a scratch clone, run the deciding run's `COLDREAD_SECTIONS_CREDITED` command (base 60), compare with
`.ufo/evidence/round-48/before/no-harm-at-base.stdout`, and check that the round-45 freshness counter still prints
`population=73 fresh=71`.

What this attacks: the claim that the content revision is harm-free — that the eight frozen monitors, the cold-read
credited-section count and the round-45 freshness floor are all unchanged at the revision the deciding run will score.

Verdict: **8/8 no-harm monitors ok, no RED — but the cold-read gate is RED at CONTENT: 57 credited sections against
a required 60.** Secondary disclosure: the deciding run's step-0 `FROZEN_UNCHANGED` check is also 0 at CONTENT.

## Method

Scratch: `S=/fast/scratch/hyaku/tameshi-r48/T48W2ExecNoHarm`; `git clone -q --shared` of the lane into `$S/clone`,
`git -C $S/clone checkout --detach c7586b9a…`; `TMPDIR=$S`; scratch removed at the end. The lane checkout was
read-only throughout (no writes, no git/jj mutation). `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh
status` before the pass: `/fast/scratch/hyaku` 23% used, 621.4G free — no ENOSPC. No tool installed or upgraded.

Commands (cwd = `$S/clone`; the script is the frozen one — `git diff --quiet 755298415f8c c7586b9a… --
.ufo/evidence/round-48/no-harm.sh` → identical):

```
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/no-harm.sh "$S/clone" c7586b9a10effc63b4bd327f976edc094c1bdc17
python3 .ufo/evidence/round-21/coldread/measure.py --repo "$S/clone" --rev <rev> \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print(sum(1 for s in d["coldread"]["sections"] if s["credited"]))'
python3 .ufo/evidence/round-45/freshness/measure.py --lane "$S/clone" --rev <rev>
```

## The eight monitors: identical to base except the registry count

Observed at CONTENT (receipt `receipts/no-harm-at-content.stdout`, script exit 0, stderr empty, 33 s):

```
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread score=6 box3_full_page=False ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-124 128 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
```

Against `before/no-harm-at-base.stdout` (same eight lines, `registry-rows-not-below-124 124 ok`): seven lines are
byte-identical; the only movement is the registry count 124 → 128 (the four C2 rows S265-S268), still above the
floor of 124. No RED line, `NOHARM_OK_COUNT=8` would hold.

## F1 (RED, finding) — cold-read credited sections are 57 at CONTENT, the deciding run needs 60

Command output (`receipts/coldread-sections-across-revs.txt`):

```
473336d9d789f6081195e7376d17836a24666bc3 (base)      sections=60
755298415f8c (counter freeze, freeze-2)                sections=60
c7586b9a10effc63b4bd327f976edc094c1bdc17 (content)     sections=57
17cc5ce141868454d05bf75ef5cd230e35f0cdf4 (lane HEAD)  sections=57
```

`COLDREAD_SECTIONS_CREDITED=57 (base 60)`; `.ufo/evidence/round-48/deciding-run.sh:31`
(`[ "$sections" -ge 60 ] || rc=1`) therefore sets `rc=1`, and `.ufo/evidence/round-48/deciding-run.sh:33`
prints `DECIDING_RUN_EXIT=1`. The base measurement (60) is reproduced in the same clone, so the clone and the
selector are faithful and the drop is a property of CONTENT, not of my scratch tree.

Three sections lost credit (`receipts/coldread-section-diff-base-vs-content.txt`; 64 sections at both revisions,
60 → 57 credited, none newly credited):

| section start | heading | crediting ledger entries at base | at content |
|---|---|---|---|
| 1479 | `## Repeated controls and gate registry — round 12` | 1 of 17 | 0 of 17 |
| 1517 | `## Pin disposition and provenance correction — round 13` | 1 of 20 | 0 of 20 |
| 1563 | `## Effective expectation reconciliation — round 14` | 1 of 15 | 0 of 15 |

Credit rule: `.ufo/evidence/round-18/measure.py:625-641` credits a section when at least one matching ledger entry
has `entry_reason(...) is None` and no entry is stale; `.ufo/evidence/round-18/measure.py:330-350` (`input_failures`)
reports `input-drift:<path>` when the sha256 of the file at REV differs from the sha recorded in the entry's
`inputs`. Each of the three sections had exactly one surviving crediting entry, and that entry pins one of the two
knowledge files content re-anchored (`receipts/crediting-entry-input-drift.txt`):

- 1479 → `corpus/knowledge/repeated-control-precondition.md`, recorded `1339460070d6`; base and freeze-2
  `1339460070d6`, CONTENT `e56f5876fa5a`; content reason of the crediting entry is exactly
  `input-drift:corpus/knowledge/repeated-control-precondition.md`.
- 1517 and 1563 → `corpus/knowledge/incremental-pin-disposition.md`, recorded `0cc873009784`; base and freeze-2
  `0cc873009784`, CONTENT `966a8065ea8e`; content reason of both crediting entries is exactly
  `input-drift:corpus/knowledge/incremental-pin-disposition.md`.

The two drifting files are exactly the C2 re-anchoring edits — `git diff -U0 755298415f8c c7586b9a… --
corpus/knowledge/incremental-pin-disposition.md corpus/knowledge/repeated-control-precondition.md` shows one
`@@ -1,2 +1,2 @@` hunk each: line 1 (`source:`, now citing S265/S267/S268) and line 2 (`verified-at: 2026-10-26`).
The append of S265-S268 to `corpus/SOURCES.md` is not what breaks these three sections (it drifts only entries that
already failed at base); the re-pointed knowledge files are.

Why this cannot be repaired inside the frozen frame: the round-21 ledger that pins those shas is
`.ufo/evidence/round-21`, and `.ufo/evidence/round-48/deciding-run.sh:21` lists `.ufo/evidence/round-21` inside the
`FROZEN` set whose `git diff --quiet "$FREEZE" "$REV"` must hold. A ledger re-pin committed after the counter
freeze `755298415f8c` would flip `FROZEN_UNCHANGED` to 0 (also `rc=1`); a re-pin before it is already past. The
gate as frozen is therefore unsatisfiable at this content revision — the L1 must re-cut content without those two
knowledge re-anchors or record a documented miss; neither is mine to choose.

## F2 (disclosed, outside the eight monitors) — step-0 `FROZEN_UNCHANGED` is 0 at CONTENT

Measured while locating the sections gate (`receipts/frozen-set-check.txt`):

```
git diff --quiet 755298415f8c c7586b9a10effc63b4bd327f976edc094c1bdc17 -- <deciding-run.sh:21 FROZEN set>
exit=1   => deciding-run.sh:22 prints FROZEN_UNCHANGED=0 and sets rc=1
.ufo/evidence/round-48/control/c2-controls.{exit,meta,stderr,stdout}  4 files, +21 lines
```

`git ls-tree -r 755298415f8c .ufo/evidence/round-48/control/` holds only `c2-controls.py` and `run-controls.py`;
`git log --diff-filter=A -- .ufo/evidence/round-48/control/c2-controls.stdout` attributes the four receipts to
`c7586b9` (content). `$E/control` is inside the `FROZEN` set, so the content commit's control receipts are frozen-set
drift. Not one of my eight monitors and not my item to fix — reported because it is measured at CONTENT and gates
the same deciding invocation as F1.

## Round-45 freshness: still `population=73 fresh=71`, and why re-anchoring cannot move it

Observed (`receipts/r45-freshness-at-content.stdout` vs `…-at-base.stdout`); the two stdout files are identical
except the `rev=` token:

```
C1_R45: self_pin=1 population=73 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0
        disputed=2 fresh=71 score=9 target=50 rev=<rev> C1_R45_PASS=true
DISPUTED S048
DISPUTED S093
```

Why the C2 re-anchoring leaves it untouched — the counter never reads a citing knowledge entry:

1. Population is `corpus/SOURCES.md` at REV only (`.ufo/evidence/round-45/freshness/measure.py:222,279,301`),
   filtered by `status == 'mined'`, `int(id[1:]) <= MAX_ID` (=160, line 47) and an http(s) URL in the source cell.
   S265-S268 are `mined` with URLs but their ids exceed 160, and `git diff -U0 473336d… c7586b9a… -- corpus/SOURCES.md`
   contains no changed line matching `| S0xx |`/`| S1xx |` (only the four appended `| S265…S268 |` rows) → 73 either way.
2. `fresh` grades those population ids against `.ufo/evidence/round-45/freshness/ledger.json` (73 entries, max id
   S160, none ≥ S200), the snapshot blobs and `reviews.json` (73 reviews, disputes exactly S048 and S093) — all at
   REV, and content touched no path under `.ufo/evidence/round-45/` or its snapshots
   (`git diff --name-only 473336d… c7586b9a… | grep -E 'round-45|snapshots'` → empty). So verified=73, disputed=2,
   fresh=71.
3. The knowledge files are not an input: the counter's only file reads are `corpus/SOURCES.md`, its own
   `ledger.json`/`reviews.json`, `.ufo/waves/round-45/w2-results.json` and review reports under
   `.ufo/waves/round-45/` (lines 56-59, 206). Its content-word overlap test compares the quote against the *row's*
   scope+anchor+teaches cells, not the citing entry. Re-pointing `S026→S265`, `S048→S266`, `S093→S267`, `S108→S268`
   in `corpus/knowledge/*.md` changes no graded quantity, and S026/S048/S093/S108 stay in the population with their
   round-45 verdicts (S048/S093 still disputed).

## Summary

- Eight frozen no-harm monitors at CONTENT: 8/8 ok, no RED; registry 124 → 128 (floor 124).
- F1 RED: `COLDREAD_SECTIONS_CREDITED=57` < 60 → `deciding-run.sh:31` sets `rc=1`; cause is the C2 re-anchoring of
  `corpus/knowledge/incremental-pin-disposition.md` and `corpus/knowledge/repeated-control-precondition.md`, which
  are pinned inputs of the only crediting ledger entries for sections 1479/1517/1563; `.ufo/evidence/round-21` is
  frozen, so no in-frame re-pin exists.
- F2 disclosed: `FROZEN_UNCHANGED=0` at CONTENT from the `c2-controls.*` receipts committed in `c7586b9`.
- Round-45 freshness unchanged: `population=73 fresh=71 C1_R45_PASS=true`, disputed S048/S093.

Receipts in this directory: `receipts/no-harm-at-content.stdout`, `receipts/coldread-sections-across-revs.txt`,
`receipts/coldread-section-diff-base-vs-content.txt`, `receipts/crediting-entry-input-drift.txt`,
`receipts/frozen-set-check.txt`, `receipts/r45-freshness-at-base.stdout`,
`receipts/r45-freshness-at-content.stdout`. Scratch dir `/fast/scratch/hyaku/tameshi-r48/T48W2ExecNoHarm` removed
after the receipts were copied. No build, lint, test or formatter was run (wave in flight); nothing under `corpus/`,
`tools/` or `SCORECARD.md` was written; the lane worktree, index and jj state were untouched.
