# T55W1ExecCells — C2 registry cells applied

seat: T55W1ExecCells (executor, round-55 wave 1)
item: seven `scratch_root` cell rewords in `tools/registry.json`, measured with the frozen round-55 C2 counter
base (and patch parent): `631cd6455e58dce969310b4c0466c3383d9f5108`
patched rev in scratch clone: `427cab4cd28a2f365f07307e7305aa1999067b53`
scratch: `/fast/scratch/hyaku/tameshi-r55/T55W1ExecCells` (clone at `.../clone`; cleared after the run — the patch is preserved in `registry-cells.patch`, which applies cleanly at the base)
production files touched: **none.** The lane worktree was only read; the seven edits live in the scratch clone and are delivered as a diff below.

## 1. Result line

| arm | base `631cd64` | patched `427cab4` |
|---|---|---|
| grammar | 6/8 | 6/8 (unchanged — repeat-control / context-capture are the stream seat's item) |
| lazy | 5/5 | 5/5 |
| empty | 13/13 | 13/13 |
| usable | 13/13 | 13/13 |
| tmp_mkdirs | 0 | 0 |
| **docs** | **0/7** | **7/7** |
| note | 0/8 | 0/8 (unchanged — the note is another seat's item) |
| skill | 0/1 | 0/1 (unchanged — `SKILL.md` is another seat's item) |
| **total** | **18** | **11** |

Base line, byte-identical to `.ufo/evidence/round-55/before/c2.stdout`:

```
C2_R55: rev=631cd6455e58 grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18 C2_R55_PASS=false
```

Patched line:

```
C2_R55: rev=427cab4cd28a grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=0/8 skill=0/1 total=11 C2_R55_PASS=false
```

The two EXPLAIN lines that moved, base vs patched:

```
EXPLAIN docs                                      0/7 FAIL     (base)
EXPLAIN docs                                      7/7 ok       (patched)
```

## 2. Commands (both receipts, exact)

Base (before any edit, at the frozen rev):

```sh
S=/fast/scratch/hyaku/tameshi-r55/T55W1ExecCells
cd "$S/clone"                      # git clone --shared of the lane, detached at 631cd64
export TMPDIR=$S/tmp
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/c2/measure.py \
  --lane "$S/clone" --rev 631cd6455e58dce969310b4c0466c3383d9f5108 \
  --work "$S/work-base" --explain
```

Patched (after the seven edits were committed in the clone as `427cab4`):

```sh
S=/fast/scratch/hyaku/tameshi-r55/T55W1ExecCells
cd "$S/clone"
export TMPDIR=$S/tmp
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/c2/measure.py \
  --lane "$S/clone" --rev "$(git rev-parse HEAD)" \
  --work "$S/work-patched" --explain
```

Counter return code is 1 in both cases (`C2_R55_PASS=false` — the round is not closed by this seat; note and skill arms plus the grammar arm remain). Receipts:

- `T55W1ExecCells-receipts/c2-base.stdout`, `c2-base.stderr` (empty), `c2-base.rc`, `c2-base-receipts.json`
- `T55W1ExecCells-receipts/c2-patched.stdout`, `c2-patched.stderr` (empty), `c2-patched.rc`, `c2-patched-receipts.json`

Base `bad` map (from `c2-base-receipts.json`) names exactly the five defects and nothing else:

```json
{"context-capture --selftest": "grammar rc=2 stderr=[]",
 "docs": "0/7",
 "note": "0/8",
 "repeat-control --selftest": "grammar rc=2 stderr=[\"repeat-control: setup: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<work>/no-such-tmpdir' (could-not-evaluate)\"]",
 "skill": "0/1"}
```

Patched `bad` map: the same minus `docs`.

Registry gate (rc 0 so the reword does not break it), run in the patched clone at `427cab4` with a usable `TMPDIR` and a clean tree:

```sh
cd /fast/scratch/hyaku/tameshi-r55/T55W1ExecCells/clone   # HEAD 427cab4, status --porcelain empty
TMPDIR=/fast/scratch/hyaku/tameshi-r55/T55W1ExecCells/tmp python3 tools/registry-check.py --selftest
```

```
rc=0
SELFTEST_CASE live-root-warning PASS (exit=0)
SELFTEST: PASS (51 cases)
```

Receipts: `registry-check-selftest-patched.stdout` (51 `SELFTEST_CASE` lines, all PASS), `.stderr` (empty), `.rc` (`rc=0`).

## 3. The reword

Each of the seven cells now carries, in one string:

1. the grammar with the row's own tool name — `` `repeat-control.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)` `` — plus "nothing on stdout and no RuntimeError/Traceback token on either stream";
2. the empty and usable arms, unchanged in substance from round 54 (`TMPDIR=""` ⇒ unset, platform default; a usable TMPDIR holds every `mkdtemp`, nothing under `/tmp`);
3. the eight allocating modes, with the labels the counter invokes them by: `env-diff --selftest, env-diff --contract, repeat-control --selftest, registry-check --selftest, bash-witness-study selftest, pin-disposition --selftest, evidence-disposition --selftest, context-capture --selftest`;
4. the honest class statement: "an operator-visible line grammar, not a shared Python type";
5. a pointer to `(round 55, corpus/knowledge/scratch-root-contract.md)` instead of round 54.

Diff hunks (committed in the scratch clone; full untruncated diff in `T55W1ExecCells-receipts/patch.diff`, 7 insertions / 7 deletions, one path):

```diff
diff --git a/tools/registry.json b/tools/registry.json
index 3f77bfc..4eedf3e 100644
--- a/tools/registry.json
+++ b/tools/registry.json
@@ -44 +44 @@
-      "scratch_root": "TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback); TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp (round 54, corpus/knowledge/scratch-root-contract.md)",
+      "scratch_root": "One stderr line, exit 2: `repeat-control.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)`, nothing on stdout and no RuntimeError/Traceback token on either stream; TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp (round 55, corpus/knowledge/scratch-root-contract.md). The eight allocating modes that print this line: env-diff --selftest, env-diff --contract, repeat-control --selftest, registry-check --selftest, bash-witness-study selftest, pin-disposition --selftest, evidence-disposition --selftest, context-capture --selftest. The class is an operator-visible line grammar, not a shared Python type.",
```

The other six hunks are the same single-line replacement at these registry lines, differing only in the tool name inside the grammar (see `patch.diff`):

| registry line | row | tool named in the cell |
|---|---|---|
| 87 | `bash-witness-selftest` | `bash-witness-study.py` |
| 135 | `pin-disposition-selftest` | `pin-disposition.py` |
| 333 | `evidence-disposition-selftest` | `evidence-disposition.py` |
| 424 | `context-capture-selftest` | `context-capture.py` |
| 620 | `registry-check-selftest` | `registry-check.py` |
| 862 | `env-diff-selftest` | `env-diff.py` (one-line `argv`, so the hunk context is `"argv": ["python3", "tools/env-diff.py", "--selftest"],`) |

## 4. Sweeps (each with its command's output)

`T55W1ExecCells-receipts/registry-sweep.stdout`:

- `git diff --name-status 631cd64 427cab4` ⇒ `M\tools/registry.json` only. No row added, removed or reordered; no other tracked path touched.
- Sorted row names base vs patched ⇒ identical, `ROW_NAMES_IDENTICAL count=56` (the no-harm `registry-row-names-unchanged` monitor's predicate holds on this patch).
- Re-implementation of the counter's docs predicate at `427cab4` ⇒ `cells=7 r55_marker=7 r54_predicate=7`: all seven cells carry `could-not-evaluate: cannot create clone scratch under the scratch root`, and all seven still satisfy round 54's predicate (`TMPDIR`, `empty`, `could-not-evaluate`), so the older counter's docs arm would also still read 7/7 at this rev.
- `git grep -c "TMPDIR set but unusable" 427cab4 -- tools corpus SKILL.md SCORECARD.md` ⇒ no matches: the old sentence survives only where it is historical testimony (`.ufo/evidence/**` receipts), not in the documents the round keeps current.
- Strict eight-mode check the frozen counter does **not** perform — every cell must contain all eight labels as the counter invokes them ⇒ `cells_naming_all_eight=7/7`, each row `modes=8/8 ok` (same receipt). The docs arm's marker match alone would have passed without this.

A finding without a command is not a finding; two non-findings are recorded as such: the docs arm moved exactly by 7 (`total` 18 → 11 with every other arm constant, both runs to the same `--work` discipline), and `registry-check --selftest` is rc 0 with the patched file.

## 5. Incidents (reported, not repaired)

1. **Seat scratch was wiped mid-run at 13:54** (`/fast/scratch/hyaku/tameshi-r55/T55W1ExecCells/receipts`, `clone`, `tmp` disappeared; `work-base/tmp-usable` was left behind). The first base counter run was in flight and its `usable` arm consequently read `12/13` (`usable:registry-check --selftest rc=1 expected=0` — its scratch root vanished under it). That receipt no longer exists; I did not treat it as a property of the rev. The unchanged counter re-run at the same rev read `usable=13/13 … total=18`, identical to the frozen `before/c2.stdout`. All receipts cited here were written afterwards to the durable wave receipts dir.
2. **Isolation of that failure** — a fresh clone at `631cd64` on branch `r55-rev`, with the counter's fixture contract materialized exactly as the counter writes it, ran `registry-check --selftest` rc 0 / 51 cases at a usable `TMPDIR` (`diag-registry-selftest-with-contract.stdout`). So no genuine usable-arm failure exists at the freeze rev, and none exists at the patched rev (13/13 in `c2-patched.stdout`).

## 6. Integration note for the L1

Apply the seven single-line replacements above to the lane's `tools/registry.json` (or cherry-pick `427cab4`'s hunk, 7 ins / 7 del). A portable copy of the commit is in `T55W1ExecCells-receipts/registry-cells.patch` (`git format-patch -1 427cab4`, 80 lines); `git apply --check` against a pristine `631cd64` worktree prints `APPLIES_CLEANLY_AT_631cd64` (`patch-applies.stdout`), so `git am` in the lane picks it up unchanged. Two observations about the lane worktree at the time I ran, which I did not touch:

- `tools/registry.json` already carried an uncommitted **whole-file reformat** (its diff is `3f77bfc..8d5b691` over all 1028 → 1277 lines, not a 7-line patch). The cells in that draft say `Allocating modes: selftest.` (`env-diff`: `selftest, --contract`) — they carry the marker (so the docs arm would read 7/7) but they name only the per-row modes, not the eight allocating modes this round's item 2 requires. If that draft is the integration target, the cells need the eight-mode sentence added; the table in §3 gives the exact wording I verified.
- Nothing else in the lane was written by this seat.

## 7. Risks / cannot see

- The frozen counter's docs arm matches the marker substring only; a cell can carry the marker and still misname a mode. The eight-mode list here is verified by an independent strict check (`cells_naming_all_eight=7/7`, §4), not by the frozen counter — the counter cannot see a wrong mode name, and the lane's integration must re-run that check (or keep this wording) to hold the claim.
- Cell wording is deliberately per-tool in the grammar, so the seven strings are not byte-identical; a caller that parses the cell by prefix will see seven different prefixes. The counter does not care, and the honest claim is that the grammar is a line grammar, not a shared type.
- The scratch cleanup of §5 recurred once; a run that is reaped mid-flight can read a false usable-arm miss. Any arm that fails on a single mode while every other arm is clean should be re-run before it is believed.

## 8. Tooling

No installs or upgrades were needed in this seat; `python3`, `git`, `strace` were already present and adequate. `pacman` was not touched (host-wide pause).
