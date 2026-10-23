# RerunCensus — SOURCES census re-run and append-only diff check

Seat: `RerunCensus`. Item: frontier step — run the SOURCES census at `bb681566b18211adf8ae9c28df91e17678e3f545` and at base `9ed6db840dc97a0a5f4758b6b5f60cee83a61645`, then confirm the `corpus/SOURCES.md` diff shape and used-by existence. Wall clock about 5 minutes, inside the 45-minute cold-read-class box (this item runs no cold read).

## Verdict

**Pass on all three assigned confirmations.**

1. `sources-census.sh validate --root <mirror> tameshi` exits 0 and prints `tameshi	ok	…/corpus/SOURCES.md` at both revisions. The two outputs are identical except for one line: the target adds `W04 S092 duplicate url bazel.build/remote/caching across scopes`. No E-code (data defect) at either revision.
2. The `corpus/SOURCES.md` diff between the revisions changes exactly one shared line, the `used-by` cell of S087 (line 96 in both), appends rows S092–S094 directly after S091 (lines 101–103), and appends a 9-line round-30 note block at the end (lines 356–364). No other line of the file differs.
3. Every `used-by` path of a mined row exists at `bb681566b18211adf8ae9c28df91e17678e3f545`: the census emits no E11, and an independent row parse finds 64 mined rows carrying 104 distinct used-by paths, 0 missing. Both paths on S087’s changed cell exist, and `corpus/knowledge/regression-tally-completeness.md` is tracked at HEAD.

Two recorded observations, neither a failure of the assigned checks: a stale `- Next unused id: S092.` line now sits beside the new `- Next unused id: S095.` line (append-only convention, stated at SOURCES.md:353 and :267, so expected, but the round-30 note does not name the stale line); and one non-reproducible output anomaly on my first base-revision invocation, recorded under "Observed anomaly" and filed to `xd://report_issue`.

## Setup

Both mirrors were built exactly as assigned. `shokunin.conf` was copied in, `scripts` symlinked, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset for every git call.

```
W2=/fast/scratch/hyaku/tameshi-r30a2-seats/RerunCensus/m
mkdir -p $W2; cp /home/vgpnk/Projects/shokunin/shokunin.conf $W2/
ln -sfn /home/vgpnk/Projects/shokunin/scripts $W2/scripts
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin $W2/tameshi-shokunin
git -C $W2/tameshi-shokunin checkout -q --detach bb681566b18211adf8ae9c28df91e17678e3f545
git -C $W2/tameshi-shokunin rev-parse HEAD
```
Observed: `bb681566b18211adf8ae9c28df91e17678e3f545`; `git status --porcelain` empty. The base mirror `/fast/scratch/hyaku/tameshi-r30a2-seats/RerunCensus/base` was built the same way and observed at `9ed6db840dc97a0a5f4758b6b5f60cee83a61645`, also clean.

Instrument identity: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`. Relevant behaviour: row parsing and W04 at `scripts/sources-census.sh:574-660` (W04 emission at `:645`), used-by existence check at `usedby_findings()` `:538` with the E11 print at `:567`.

## Census runs and observed output

Target revision:

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root $W2 tameshi
```
Observed, `EXIT=0`, 9 lines (repeated three times, byte-identical, sha256 prefix `3ce914b26878449b`):

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	ok	/fast/scratch/hyaku/tameshi-r30a2-seats/RerunCensus/m/tameshi-shokunin/corpus/SOURCES.md
```

Base revision (`$W3=/fast/scratch/hyaku/tameshi-r30a2-seats/RerunCensus/base`, same command, `--root $W3`):

Observed, `EXIT=0`, 8 lines (three repeats, byte-identical, sha256 prefix `a066eefcdf580632`):

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	ok	/fast/scratch/hyaku/tameshi-r30a2-seats/RerunCensus/base/tameshi-shokunin/corpus/SOURCES.md
```

Modulo the root path, `diff` of the two outputs is exactly:

```
7a8
> tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
```

The S092 warning is expected: S092 reuses S059’s URL under a different scope and its teaches begins `supersedes S059`, which suppresses E04 but not the cross-scope W04 at `scripts/sources-census.sh:645`. Warnings do not change exit status (`:33`).

Supplementary totals (`sources-census.sh census --root … tameshi`), read-only, not part of the assigned command:

| metric | base | target |
|---|---|---|
| rows | 89 | 92 |
| tier.A / B / C | 80 / 7 / 2 | 83 / 7 / 2 |
| status.mined / queued / rejected | 62 / 21 / 6 | 64 / 22 / 6 |
| FLEET.missing | 0 | 0 |

## Diff confirmation

Command, read-only, run in the lane repo with `GIT_OPTIONAL_LOCKS=0`:

```
GIT_OPTIONAL_LOCKS=0 git diff 9ed6db840dc97a0a5f4758b6b5f60cee83a61645 \
  bb681566b18211adf8ae9c28df91e17678e3f545 -- corpus/SOURCES.md
```
Observed hunks: `@@ -96 +96 @@` (one line replaced), `@@ -100,0 +101,3 @@` (three rows added), `@@ -352,0 +356,9 @@` (nine note lines added); stat `13 insertions(+), 1 deletion(-)`. No other hunk exists, so no other line of the file changed.

Independent cell-level check (Python, reading both worktrees): 89 base rows, 92 target rows; ids only in target `S092, S093, S094`; ids only in base none; exactly one shared row differs, `S087` at line 96 in both files, 11 cells each, and the only differing column is the used-by cell (index 10):

- base: `corpus/knowledge/mte-report-interop.md`
- target: `corpus/knowledge/mte-report-interop.md, corpus/knowledge/regression-tally-completeness.md`

That matches the round-30 note at `corpus/SOURCES.md:357-363` word for word, including "status and recheck unchanged". Lines 1–95 and 97–100 are byte-identical between the revisions.

Append placement: the base registry’s last row is S091 at line 100; the target has S092 at 101, S093 at 102, S094 at 103 — inside the `## Registry` table (the parser places all 92 rows in the Registry section), followed by the blank line and the next section. The note block is the file tail: base ended at line 352 (`- Next unused id: S092.`, 352 lines total); target has 364 lines, the added block being lines 356–364, from `Round 30: S092 supersedes S059's anchor …` through `- Next unused id: S095.`.

## Used-by existence at the content revision

The census’s own check (`usedby_findings`, mined rows only, `[ ! -e "$dir/$path" ]` at `scripts/sources-census.sh:566-568`) printed no E11 at the target revision, which is already the assigned confirmation. An independent parse of the same file agrees:

- 64 mined rows; 104 used-by paths (cells split on commas, `—` skipped); 0 missing at the target worktree root.
- S087: both `corpus/knowledge/mte-report-interop.md` and `corpus/knowledge/regression-tally-completeness.md` exist.
- S092 is `queued` with used-by `—` (anchor-only supersede), so it is correctly outside the mined-row check.
- S093 and S094 are `mined`, each with `corpus/knowledge/regression-tally-completeness.md`, which exists.
- `git ls-tree -r HEAD -- corpus/knowledge/` lists both `regression-tally-completeness.md` and `mte-report-interop.md`, so the paths are tracked at the content revision, not merely present in my checkout.

## Observations (recorded, not failures)

1. Stale id pointer, by design. Target `corpus/SOURCES.md:355` still reads `- Next unused id: S092.` while S092–S094 now exist, and the new line at `:364` says `- Next unused id: S095.`. The append-only convention for these stale lines is explicit at `:267` (round 18) and `:353` (round 28: "The stale `Next unused id: S090` line above stays append-only"), so this is the established pattern, not an accidental edit. It is an id-collision hazard only for a reader who stops at the first matching line; the round-30 note does not repeat the round-28 sentence for S092.
2. Observed anomaly on my first base-revision invocation. That first run printed the eight-line output including `S092 duplicate url bazel.build/remote/caching`, i.e. exactly the target output modulo root path, although the base worktree’s `corpus/SOURCES.md` at that moment had 89 rows, 0 occurrences of `S092`, sha256 `804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca`, and mtime 04:14:40 -03:00 (the checkout that produced it). Three immediate repeats, and every later run, are byte-identical and omit the S092 line (`a066eefcdf580632`), while the target is stable at `3ce914b26878449b`. I cannot make the base file produce that line, and the two commands were issued in the same parallel batch as the target census, so I read it as crossed or duplicated output delivery rather than census behaviour. It is filed to `xd://report_issue`. The base output quoted above is from the deterministic repeats, not from that first invocation.

## Risks and limits

- One host, one `gawk`/bash, two mirrors; behaviour on another host is unmeasured.
- The census check is path existence only (`-e`), not content or intent. A used-by path that exists but does not actually cite the row would pass here and is outside this item.
- The W04 count difference is a warning-level consequence of the intended S092 supersede, not a new defect; I make no claim about whether W04 should distinguish supersedes rows beyond the code I read at `:645`.
- The anomaly in observation 2 is a single unreproduced event; my repeat evidence bounds it to delivery, but I did not capture process ids for those two batched commands, so the mechanism is attributed, not proven.
- Base and target runs used the default `--today` (2026-10-23); date-dependent codes E08/E09 were silent at both revisions.

## Environment, custody, cleanup

- No tools installed or upgraded; no pacman, no `jj`, no git write command. All git was read-only with `GIT_OPTIONAL_LOCKS=0`; clones used `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`.
- Nothing was written under the lane repo except this report; no production file was edited; both worktrees remain clean.
- Scratch is confined to `/fast/scratch/hyaku/tameshi-r30a2-seats/RerunCensus/{m,base}` (clones plus copied conf and `scripts` symlink). No background processes were started and none remain; nothing was killed. `/fast` had 221G free before the clones.
- I did not open `/fast/scratch/hyaku/tameshi-r30a3/` or `/fast/scratch/hyaku/tameshi-r30a2/`.

## Smallest safe correction

None required for the three assigned confirmations; the census is green at both revisions and the diff is exactly the declared shape.

Optional, content owner’s call and not applied here: extend the round-30 note at `corpus/SOURCES.md:357-363` with the same sentence round 28 used for S090 — that the `- Next unused id: S092.` line at `:355` stays append-only — so the two live id lines are not ambiguous to a cold reader.
