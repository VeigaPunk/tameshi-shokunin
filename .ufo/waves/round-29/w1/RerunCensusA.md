# RerunCensusA — SOURCES census re-run at 9f3084b and at base 367ec0f

Seat: `TameshiR29.RerunCensusA` (executor, leaf). Wave: tameshi-r29-w1.
Repo under test: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only; no git write command was run there).
Report path: `.ufo/waves/round-29/w1/RerunCensusA.md`.
Census script: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`.
Date of run: 2026-10-22 (local clock of the host running the probes).

## 1. Verdict

1. **The SOURCES census FAILS at 9f3084b and PASSES at base 367ec0f.** The single
   new error is `E11` on row `S024`: the row's `used-by` cell names
   `corpus/knowledge/survivor-fixture-minimization.md`, and that file does not
   exist in the tree at 9f3084b. Exit code 1 at 9f3084b, exit code 0 at 367ec0f.
2. **The diff of `corpus/SOURCES.md` between the two revisions touches exactly one
   row and exactly two cells of that row**: `status` (`queued` → `mined`) and
   `used-by` (`—` → `corpus/knowledge/survivor-fixture-minimization.md`). All
   nine other cells of the S024 row are byte-identical, and no other line of the
   file differs (352 lines on both sides, 1 differing line). The confirmation
   requested ("only the S024 status and used-by cells changed") holds.
3. **Yes, the census checks that a used-by path exists.** Check `E11` is emitted by
   `usedby_findings()` (`scripts/sources-census.sh:538-570`); the existence test is
   `[ ! -e "$dir/$path" ]` (`:566`), resolved relative to the lane root that holds
   the registry. The check is armed only for rows whose `status` is `mined`
   (`:559`); a `queued` row with the same `used-by` text is not flagged.
4. **The entry lands after 9f3084b — the pointer lands at 9f3084b, the file it
   names does not exist yet at 9f3084b and does not exist in any later commit of
   any ref of the lane repo as of this run.** `git rev-list --all --objects` over
   the lane repo finds no object named
   `corpus/knowledge/survivor-fixture-minimization.md`. The `used-by` cell at
   9f3084b is therefore a forward reference to the C2 deliverable
   (`corpus/knowledge/survivor-fixture-minimization.md`), which the round has not
   yet produced.
5. **The committed receipt `.ufo/evidence/round-29/census-start.stdout` /
   `.exit` does not reproduce at the commit that carries it.** It records exit 0
   and a `tameshi ok` line; re-running the same validate mode at 9f3084b gives
   exit 1 with the E11 finding. File mtimes show the receipt was captured at
   22:09:28 and `corpus/SOURCES.md` was edited at 22:11:40, so the receipt
   describes the pre-edit working tree and was committed together with the edit
   it predates.

Smallest safe correction (not applied by this seat, no production file touched):
the lane turns green again the moment `corpus/knowledge/survivor-fixture-minimization.md`
is committed — proven by control §5 below, where creating that one file at 9f3084b
turns the failing run into exit 0 with no other change. That file is exactly the
C2 deliverable named in the contract, so the fix belongs to the C2 build item, not
to a SOURCES.md edit. Secondarily, the stale receipt should be regenerated or
labelled as pre-edit so it does not read as a clean-lane receipt for a tree that
is red.

## 2. Exact commands and observed output

### 2.1 Census at 9f3084b (the requested run)

```
W2=$(mktemp -d); cp /home/vgpnk/Projects/shokunin/shokunin.conf $W2/;
ln -s /home/vgpnk/Projects/shokunin/scripts $W2/scripts;
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W2/tameshi-shokunin;
git -C $W2/tameshi-shokunin checkout -q --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5;
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root $W2 tameshi
```

Observed output (exit 1):

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	E11	S024 missing used-by corpus/knowledge/survivor-fixture-minimization.md
EXIT=1
```

Note the absence of a `tameshi ok <path>` line: the script emits `ok` only when
the lane has no E-finding (`scripts/sources-census.sh:741-748`).

### 2.2 Census at base 367ec0f (same recipe, second mirror)

Observed output (exit 0):

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	ok	/tmp/censusB-julR/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

The seven W04 warnings are identical at both revisions; they are pre-existing and
do not affect lane status ("warnings do not affect clean lanes", script header
lines 32-33).

### 2.3 Reproducibility

Two further fresh mirrors at 9f3084b (two more `mktemp -d` + clone + checkout +
validate) produced byte-identical output and `EXIT=1`. The result is not
mirror-path dependent.

### 2.4 Diff of corpus/SOURCES.md between the two revisions

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff \
    367ec0f1d79cb9b67d724f2962e7554a0841b1fc 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 \
    -- corpus/SOURCES.md
```

```
corpus/SOURCES.md | 2 +-
1 file changed, 1 insertions(+), 1 deletions(-)
```

`git diff --numstat` for the same pair and path: `1	1	corpus/SOURCES.md`.

The one changed line, base then 9f3084b:

```
| S024 | Reducing Failure-Inducing Inputs (The Fuzzing Book, Zeller et al.) — https://www.fuzzingbook.org/html/Reducer.html | book | B | delta-debugging reducer practice | §Delta Debugging (fetched 2026-10-19) | a runnable delta-debugging reducer: a Runner returns FAIL only on the precise error, and the input is cut to the minimum that still reproduces it | queued | 2026-10-19 | 365d | — |
| S024 | Reducing Failure-Inducing Inputs (The Fuzzing Book, Zeller et al.) — https://www.fuzzingbook.org/html/Reducer.html | book | B | delta-debugging reducer practice | §Delta Debugging (fetched 2026-10-19) | a runnable delta-debugging reducer: a Runner returns FAIL only on the precise error, and the input is cut to the minimum that still reproduces it | mined | 2026-10-19 | 365d | corpus/knowledge/survivor-fixture-minimization.md |
```

Cell-by-cell comparison of the 11 parsed cells of the S024 row:

| # | column | base 367ec0f | 9f3084b | verdict |
|---|---|---|---|---|
| 0 | id | S024 | S024 | same |
| 1 | source | Reducing Failure-Inducing Inputs … Reducer.html | (identical) | same |
| 2 | kind | book | book | same |
| 3 | tier | B | B | same |
| 4 | scope | delta-debugging reducer practice | (identical) | same |
| 5 | anchor | §Delta Debugging (fetched 2026-10-19) | (identical) | same |
| 6 | teaches | a runnable delta-debugging reducer: a Runner returns FAIL … | (identical) | same |
| 7 | status | queued | mined | **CHANGED** |
| 8 | opened | 2026-10-19 | 2026-10-19 | same |
| 9 | recheck | 365d | 365d | same |
| 10 | used-by | — | corpus/knowledge/survivor-fixture-minimization.md | **CHANGED** |

Whole-file scan of the two blobs: `total differing lines: 1 [35]`, `len a,b: 352 352`.
The S024 row is the only line that differs anywhere in `corpus/SOURCES.md`.

For completeness, the full revision-to-revision diff of the lane repo also carries
`corpus/QUALITY.md` (+34), `corpus/README.md` (+18) and the
`.ufo/evidence/round-29/` contract, counters and S024 HTML snapshot. Those are
outside the `corpus/SOURCES.md` diff asked about here.

### 2.5 Does the census check that a used-by path exists?

Yes. `usedby_findings()` (`scripts/sources-census.sh:538-570`) walks the
`## Registry` table, skips any row whose `status` is not `mined` (`:559`), splits
the `used-by` cell on commas, skips `—`, and for each remaining path runs
`[ ! -e "$dir/$path" ]` (`:566`), printing
`lane  E11  <id> missing used-by <path>`. `usedby_findings` is invoked only in
`validate` mode (`:720-723`).

The consequence for this revision: at base 367ec0f the S024 row is `queued`, so
the E11 branch is not armed for it; at 9f3084b the same row is `mined` and names
a path, so the branch arms and fires.

### 2.6 When does the named entry land?

```
git cat-file -e 9f3084bc60ad56aac01e4556ef4c7653df2f65e5:corpus/knowledge/survivor-fixture-minimization.md
  → fatal: path 'corpus/knowledge/survivor-fixture-minimization.md' does not exist in '9f3084bc…'
git cat-file -e 367ec0f1d79cb9b67d724f2962e7554a0841b1fc:corpus/knowledge/survivor-fixture-minimization.md
  → fatal: … does not exist in '367ec0f…'
git rev-list --all --objects | grep 'survivor-fixture-minimization'
  → (no match; no such object exists in any commit of any ref of the lane repo)
ls corpus/knowledge/survivor-fixture-minimization.md   # lane working tree
  → No such file or directory
```

So: the `used-by` pointer lands **at** 9f3084b (the cell is written in that
commit), while the entry file it points to lands **after** 9f3084b and has not
landed at all yet — not at base, not at 9f3084b, not at the current lane head
`09e4f273dd54edea382ea03f098eecb3628331c3`.

For completeness, the same census re-run at the current lane head
`09e4f27…` also fails identically:

```
tameshi	E11	S024 missing used-by corpus/knowledge/survivor-fixture-minimization.md
EXIT=1
```

i.e. the round has not yet closed the gap between the pointer and the file.

## 3. Controls

**Control A — the file is the sole cause.** At 9f3084b, with nothing changed but
the creation of `corpus/knowledge/survivor-fixture-minimization.md` (one
placeholder line), the same validate run returns:

```
tameshi	W04	S047 … (7 warnings, unchanged)
tameshi	ok	/tmp/censusC-8UVC/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

The E11 finding disappears and the `ok` line returns. No other finding is
masked or introduced. E11 is the only error at 9f3084b.

**Control B — the same edit applied to the base fails the same way.** At base
367ec0f, changing only the S024 row's `status` to `mined` and its `used-by` to
`corpus/knowledge/survivor-fixture-minimization.md` (the exact 9f3084b edit)
produces `E11 S024 missing used-by corpus/knowledge/survivor-fixture-minimization.md`
and exit 1. (The patch also swept two further rows, S044 and S045, which share
the same `queued|2026-10-19|365d|—` cell text, so those two appear as E11 too in
that control; this is an artifact of the mechanical patch and not of the
repository. The base tree itself contains no `survivor-fixture-minimization`
string in any `used-by` cell — verified by grep over the base blob, zero
matches.) This control shows the regression is caused by the edit, not by
anything else in the round.

**Control C — census mode is unaffected.** `sources-census.sh census --root $W2
tameshi` at 9f3084b exits 0 and reports `tameshi rows 89`, `status.mined 62`,
`status.queued 21`, `status.rejected 6`. The E11 finding is validate-only by
construction (`:720-723`), so the E-codes view and the census view of the same
tree disagree; only `validate` reflects the dangling `used-by` pointer.

**Control D — receipt staleness.** The committed receipt was captured against the
pre-edit working tree:

```
stat -c '%y %n' .ufo/evidence/round-29/census-start.stdout corpus/SOURCES.md
  2026-10-22 22:09:28 .ufo/evidence/round-29/census-start.stdout
  2026-10-22 22:11:40 corpus/SOURCES.md
diff <(git show 9f3084b:.ufo/evidence/round-29/census-start.stdout) .ufo/evidence/round-29/census-start.stdout
  → IDENTICAL to 9f3084b receipt
```

and the receipt content is exactly the exit-0 shape observed at base in §2.2
(same seven W04 lines plus `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`,
with `census-start.exit` = `0`). Re-running the same validate mode on the
committed tree gives exit 1. The receipt is therefore not a receipt for the tree
it ships with.

## 4. Coverage note for the round

The S024 row is one of the "widely read input edits" that the contract requires
to land in the same commit as the contract freeze, ahead of the cold reads.
At 9f3084b the row a reader sees says `status = mined` and
`used-by = corpus/knowledge/survivor-fixture-minimization.md`, while the file
named there is absent from the tree. Any cold read of `corpus/SOURCES.md` at
that revision therefore observes a mined source whose cited entry does not yet
exist in the repository — which is exactly what the census's E11 check flags.
This is consistent with the C2 claim's design (the `used-by` cell names the C2
deliverable that the round is meant to produce), but it means the SOURCES.md
edit cannot be evaluated as clean until the C2 build lands.

## 5. Files changed

Only this report:
`.ufo/waves/round-29/w1/RerunCensusA.md`.

No production file was edited. No `git` write command and no `jj` command was run
in `/home/vgpnk/Projects/shokunin`, in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`,
or in any clone; all git invocations against the lane repo were read-only with
`GIT_OPTIONAL_LOCKS=0`. All code ran in throwaway `/tmp` mirrors
(`/tmp/censusA-*`, `/tmp/censusB-*`, `/tmp/censusC-*`, `/tmp/censusD-*`,
`/tmp/censusH-*`, `/tmp/censusR*`), each with `GIT_DIR`, `GIT_WORK_TREE` and
`GIT_INDEX_FILE` unset; the symlinked `scripts` directory was the only shared
substrate and the script is read-only. No process was left running.

## 6. Installs and updates

None. No package was installed or updated; the census script's only dependencies
(bash, coreutils, gawk) were already present and are the script's declared
requirements.

## 7. Risks and blockers

- **Risk (blocker for a green lane at the landed head):** the lane's own
  `corpus/SOURCES.md` registry is red at 9f3084b and at the current head
  `09e4f27` under `sources-census.sh validate`, with the E11 finding on S024.
  Owner: the C2 build item, which must commit
  `corpus/knowledge/survivor-fixture-minimization.md`.
- **Risk (evidence integrity):** `.ufo/evidence/round-29/census-start.stdout` and
  `.exit` are committed at 9f3084b and read as a clean-lane receipt, but they
  were captured before the S024 edit that the same commit introduces. Anyone
  citing them as the census result at 9f3084b would be citing a result that does
  not reproduce. Owner: L1 (receipt regeneration or relabelling).
- **Blocker:** none for this item. The named entry file does not yet exist
  anywhere in the lane repo; it cannot be observed from here whether it will land
  before the round closes.

## 8. Out of scope

No fix was applied. No SOURCES.md cell was rewritten, no entry file was created,
no receipt was regenerated, and no gate was run in the lane repo itself. The
C2/C1 counters were not invoked by this seat.
