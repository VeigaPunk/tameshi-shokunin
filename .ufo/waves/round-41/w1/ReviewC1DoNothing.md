# ReviewC1DoNothing — C1 do-nothing falsification (round 41, w1)

## Verdict

**A do-nothing path cannot reach `total=0`.** Both live mismatches are load-bearing and
independent: restoring the standing-row count alone leaves `m9=1`, restoring the round-40
correction alone leaves `m6=1`, and neither class is reachable by any edit to the other
classes. Measured four-way matrix below. The two record edits are also *sufficient*:
the records as landed score `m6=0 m7=0 m8=0 m9=0 total=0`.

One blocker is **not** about the do-nothing path: the counter's bytes changed three times
after the freeze and the contract pin is one edit behind the live file (finding F1).

Counter bytes used for every line below:
`/tmp/tameshi-r41-reviewc1nothing-livebin/measure.py`, sha256
`9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd`
(the live `.ufo/evidence/round-41/calibration/measure.py` at snapshot 03:44–03:45 -03).
The base and freeze lines were re-measured under **all four** counter versions
(`f00917dd…4cb0c2`, `5ccb42d8…f08553`, `8bc9b422…ce11c`, `9aaa99ac…92cd`) and are
identical each time — `records=0` makes m7/m8 vacuous and the m6/m9 inputs are the same
at those revisions.

## The three lines

```text
1) $ python3 .ufo/evidence/round-41/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046
MISMATCH m6 SCORECARD standing row says 103 rows, SOURCES.md has 107
MISMATCH m9 round-40 quarantine summary says (1, 7, 9), its table counts (1, 6, 10) (no round-41 correction)
C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=0 sources_rows=107 rev=a3d6c690bcbf8914551d4f4e8e1612784c1c2046 C1_R41_PASS=false      (exit 1)

2) $ … --rev d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937
MISMATCH m6 SCORECARD standing row says 103 rows, SOURCES.md has 107
MISMATCH m9 round-40 quarantine summary says (1, 7, 9), its table counts (1, 6, 10) (no round-41 correction)
C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=0 sources_rows=107 rev=d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937 C1_R41_PASS=false      (exit 1)

3) $ … --lane /tmp/tameshi-r41-reviewc1nothing-strict --rev work      # round-41 records copied, m6 and m9 edits stripped
MISMATCH m6 SCORECARD standing row says 103 rows, SOURCES.md has 109
MISMATCH m9 round-40 quarantine summary says (1, 7, 9), its table counts (1, 6, 10) (no round-41 correction)
C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=3 sources_rows=109 rev=work C1_R41_PASS=false      (exit 1)
```

`records=0` at lines 1–2 is correct, not a counter fault: at both revisions
`corpus/lessons/round-41.md` is absent and neither `SCORECARD.md` nor `LOG.md` has its
round-41 section, so m7/m8 have no audit surface and count 0 by the counter's own
declared rule. Line 3 has `records=3` (lesson + `## Round 41` + `## 2026-10-25`).

Positive control (records as landed, both edits present):

```text
$ … --lane /tmp/tameshi-r41-reviewc1nothing-finalfixed --rev work
C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 rev=work C1_R41_PASS=true      (exit 0)
```

## Independence matrix (`--rev work`, fresh snapshots of the lane)

| m6 edit | m9 edit | line | total |
|---|---|---|---|
| no | no | `m6=1 m7=0 m8=0 m9=1 … total=2` | 2 |
| no | yes | `m6=1 m7=0 m8=0 m9=0 … total=1` | 1 |
| yes | no | `m6=0 m7=0 m8=0 m9=1 … total=1` | 1 |
| yes | yes | `m6=0 m7=0 m8=0 m9=0 … total=0` | 0 |

Each edit removes exactly its own class and no other; neither can substitute for the other.

## Structural evidence (path:line)

- m6 reads the **last** `| sources-registry |` row in the whole file —
  `.ufo/evidence/round-41/calibration/measure.py:216-222` (`standing[-1]`, regex
  `(\d+) rows`). The `## Round 41` section (`SCORECARD.md:1895`) contains no standing row,
  so only `SCORECARD.md:1851` can move this field. It now reads `109 rows at round 41`
  (restated from 103), which is why the landed tree scores m6=0.
- m9 flattens whitespace, reads the round-40 table, and accepts any round-41 lesson
  correction that states the table's own counts —
  `measure.py:244-262`; the expected words are now derived from the table
  (`:253-258`), not hardcoded.
- m6/m9 are the only two classes that can fire without a round-41 record; the counter
  cannot reach 0 at the base or freeze revision for that reason alone.

## Findings

**F1 — BLOCKER: the counter's pin does not match the counter's bytes.** The contract pin
moved three times after the freeze commit, and the live file is now a fourth version:

| step | sha256 | recorded |
|---|---|---|
| freeze `d4ee4e6` | `f00917dd…4cb0c2` | `contract.json` original |
| A1 (`cells[9]`→`cells[8]`) | `5ccb42d8…f08553` | amendment A1 |
| A4 (`os.path.exists`, `rstrip('/')` in work mode) | `8bc9b422…ce11c` | amendment A4, **current `claims.C1.counter_sha256`** |
| live file at 03:44–03:45 | `9aaa99ac…92cd` | **no amendment** — the change is the m9 block at `measure.py:250-258` (expected words derived from the table instead of `'six refused'`/`'ten present'`) |

A deciding run executed now would score bytes the contract does not pin, and A5 is missing
for the m9 rewrite. Either the drift stops and the contract is re-pinned (with A5), or the
pin must be treated as unverifiable. `.ufo/evidence/round-41/calibration/measure.py` and
both census files were already dirty in `git status` when this seat measured.

**F2 — the m6 target moved under the round.** `SOURCES.md` holds 107 rows at base and at
freeze but **109** in the working tree (`S153`, `S154` appended by this wave; statuses
81 mined / 22 queued / 6 rejected). The dispatch item for seat `ScribeScorecard`
(`.ufo/waves/round-41/w1/swarm-registry.json`, `members.ScribeScorecard.item`) still says
"the standing sources-registry row restated to **107 rows**". Following that literally
leaves `m6=1` (107≠109). The landed row says 109, which is the correct number; the
instruction should be corrected so the next editor does not revert it.

**F3 — m8 at the deciding revision needs the evidence committed.** The round-41 lesson
cites three paths that do not exist at the freeze and are still untracked:
`.ufo/evidence/round-41/sources/ast.html`, `.ufo/evidence/round-41/sources/pathlib.html`,
`corpus/knowledge/r41-variable-destination-writes.md`. `--rev work` passes them
(`measure.py:111-118`, `os.path.exists`); a rev-mode deciding run at a commit that omits
them scores `m8=3`. They must be in the measured commit.

**F4 — earlier counter defects were real and are now fixed in the bytes, not in the rule.**
Confirmed by reproduction against the pinned freeze counter `f00917dd…` before its edits:

- m7 read the `opened` column: a scratch lesson citing exactly one *mined* id (`S153`,
  registry status `mined`) scored `m7=1 … status=2026-10-25 total=1 C1_R41_PASS=false`;
  the same tree scores `total=0` under `cells[8]`. So under the freeze counter the C1
  predicate was reachable only by citing zero ids. Recorded as A1.
- m8 in work mode used `os.path.isfile`, so an existing directory was "unresolvable":
  a record citing `.ufo/waves/round-41/` scored `m8=2` even though the directory exists
  (rev mode's `git cat-file -e` accepts a tree). Fixed by A4.
- The lesson's staged-id range originally spelled a bare `S255`, which m7 read as a
  registry id (it is a staged-package id). Rephrased by A3; my four-line budget for this
  seat does not regress it.

None of these change the verdict: with the frozen rule text (m6, m7, m8, m9 all zero) and
the current counts, the do-nothing path is closed.

## Reproduce (the /tmp trees are convenience copies, not the evidence)

The lines above are the evidence; every recipe below is deterministic and was run.

Counter bytes are reconstructible from the freeze blob
`git show d4ee4e63…:.ufo/evidence/round-41/calibration/measure.py` (sha `f00917dd…4cb0c2`):

- `5ccb42d8…f08553`: `cells[9]` → `cells[8]` (`registry()`, line 137).
- `8bc9b422…ce11c`: also `os.path.isfile` → `os.path.exists` in `resolves()` line 113, and
  `.rstrip('/')` after the `:N-M` strip in `path_tokens()`.
- `9aaa99ac…92cd` (measured): also `measure.py:250-258`, expected refusal/presence words
  derived from the round-40 table (`want_refused`, `want_present`) instead of the literals
  `'six refused'` / `'ten present'`.

`strict` tree (line 3): `rsync -a --exclude=.git --exclude=.jj` the lane to
`/tmp/tameshi-r41-reviewc1nothing-strict`, then two text edits in the copy —
(1) the last `| sources-registry |` row `109 rows at round 41` → `103 rows at round 35`;
(2) delete the block from `### Correction — the round-40 quarantine summary` up to (not
including) `## Mistakes`. Nothing else differs from the landed tree.

F4 repro A (m7 column): a tree whose round-41 lesson cites exactly one registry id, `S153`
(registry status `mined`), with the standing row at 109 and the correction present →
`f00917dd` prints `MISMATCH m7 S153 cited but status=2026-10-25`, `total=1`, exit 1;
`cells[8]` prints `m6=0 m7=0 m8=0 m9=0 total=0 C1_R41_PASS=true`, exit 0.

F4 repro B (m8 directory): the same tree with a backticked `.ufo/waves/round-41/` and
`.ufo/waves/round-41/w1/` in its SCORECARD section → `f00917dd` `--rev work` prints
`MISMATCH m8 .ufo/waves/round-41/ cited but does not resolve at work` and the `w1/` line,
`total=2`; the A4 bytes print neither.

## Constraints honored

- No default-mode run at any revision other than the base and freeze revisions, and one
  `--rev work` per scratch tree; never against the tip as a measurement.
- No writes to the lane checkout, `.git`, `.jj`, `.ufo/state`, contract, counters, or any
  sibling lane. Every edit was made inside `/tmp/tameshi-r41-reviewc1nothing-*`.
- Contract read at start (`counter_sha256 f00917dd…`) and again at the end; the difference
  is reported as F1, never edited.
- No tool installed or upgraded (nothing needed); no packages touched.

Report: .ufo/waves/round-41/w1/ReviewC1DoNothing.md
