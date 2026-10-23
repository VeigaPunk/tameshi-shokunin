# RegistryNoHarm — gate/probe registry no-harm check, 9f3084b against base 367ec0f

Seat: `TameshiR29.RegistryNoHarm` (executor, leaf). Wave: tameshi-r29-w1.
Target revision: `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`. Base revision:
`367ec0f1d79cb9b67d724f2962e7554a0841b1fc`. Both resolved with
`git rev-parse <rev>^{commit}` inside the mirror clone and matching the strings
above.
Fleet mirror: `/tmp/RegistryNoHarm-Hq79/fleet` — one symlink per real
`*-shokunin` sibling plus a `git clone --no-hardlinks` of tameshi-shokunin
checked out detached at the target revision (`R=/tmp/RegistryNoHarm-Hq79/fleet/tameshi-shokunin`).
Run date: 2026-10-22 (host clock). All code ran inside `/tmp`; nothing ran in the
lane repo itself.

## 1. Verdict

**One row changed result between base and target, and it broke: `sources-census`
held at base (`got=0`) and differs at target (`got=1`). The registry itself is
unchanged — `tools/registry.json` is byte-identical at both revisions (sha256
`c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c`, 56 rows, 49
active, 7 superseded) — so the break is caused by a data edit in the target
commit, not by a registry edit.**

- Target `9f3084b`: `REGISTRY_CHECK: held=47/49 superseded=7`, process exit **1**.
- Base `367ec0f`: `REGISTRY_CHECK: held=48/49 superseded=7`, process exit **1**.
- Row-by-row diff of the two human reports is exactly two lines: the
  `sources-census` ROW line and the summary line. All 55 other rows (48 held
  active rows, 7 superseded rows) are character-identical.
- `verify-round15` is not held at either revision (`expect=0 got=1`). It is
  **not** a rev-caused difference; it fails identically at both revs because it
  delegates its last sub-check to the **live** fleet census at an absolute path
  (`/home/vgpnk/Projects/shokunin`), whose working tree currently carries the
  same dangling S024 pointer. See §3.2.

Cause of the one real difference: the target commit changes
`corpus/SOURCES.md` row S024 from `status=queued, used-by=—` to
`status=mined, used-by=corpus/knowledge/survivor-fixture-minimization.md`, and
**that entry file does not exist in the tree at 9f3084b** (nor in any object of
any ref of the lane repo). The `sources-census` registry row runs
`bash .ufo/evidence/kaika-round-1/sources-census-v2.sh`, whose part A
("mined used-by missing") and part B2 ("id-or-path cite") both fire on the
dangling path, so the row exits 1 against an expected 0.

Smallest safe correction (not applied here; no production file touched): commit
`corpus/knowledge/survivor-fixture-minimization.md` with a `source:` line citing
S024 — which is exactly the C2/F6 deliverable named in
`.ufo/evidence/round-29/contract.json` and in the row's own `used-by` cell. The
`used-by` cell should not be reverted: C2's predicate requires S024 to be
`mined` with that entry path in `used-by`, so the fix belongs to the C2 build
item, not to a SOURCES.md edit. Proven by control §4.1 and §4.2.

## 2. Commands and summary lines

Mirror setup (verbatim, one shell):

```
W=$(mktemp -d /tmp/RegistryNoHarm-XXXX); mkdir $W/fleet
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do
  b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b
done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
R=$W/fleet/tameshi-shokunin
```

`--help` shows the flags as given in the assignment (`--root`, `--rev`,
`--registry`, `--only`, `--tag`, `--json`, `--selftest`), so the prescribed
invocation was used unchanged.

Target:

```
cd $R && timeout 1800 python3 tools/registry-check.py --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
```

process exit `1`; summary line:

```
REGISTRY_CHECK: held=47/49 superseded=7
```

Base:

```
cd $R && timeout 1800 python3 tools/registry-check.py --rev 367ec0f1d79cb9b67d724f2962e7554a0841b1fc
```

process exit `1`; summary line:

```
REGISTRY_CHECK: held=48/49 superseded=7
```

Each full run took ~357 s of wall time (two concurrent runs); no row reported
`timeout`, `unavailable` or `non-hermetic`. Both runs used the clone's own
`tools/registry.json` at the graded revision, which is byte-identical at both
revs.

Row-by-row diff of the two reports:

```
diff out-base.txt out-target.txt
26c26
< ROW sources-census expect=0 got=0 held
---
> ROW sources-census expect=0 got=1 differs
57c57
< REGISTRY_CHECK: held=48/49 superseded=7
---
> REGISTRY_CHECK: held=47/49 superseded=7
```

## 3. Every row that is not held

### 3.1 Target 9f3084b — not held

```
ROW sources-census expect=0 got=1 differs
ROW verify-round15 expect=0 got=1 differs
```

Single-row confirmation with its own process exit (`--only`):

```
$ python3 tools/registry-check.py --rev 9f3084bc... --only sources-census
ROW sources-census expect=0 got=1 differs
REGISTRY_CHECK: held=0/1 superseded=0
process exit 1        (reproduced twice, identical)

$ python3 tools/registry-check.py --rev 9f3084bc... --only verify-round15
ROW verify-round15 expect=0 got=1 differs
REGISTRY_CHECK: held=0/1 superseded=0
process exit 1
```

Superseded rows are printed without a held/differs token and are excluded from
the held count; their `got` values are identical at both revs:

```
ROW evidence-disposition-round17 superseded expect=0 got=2
ROW evidence-disposition-round17-before superseded expect=1 got=2
ROW evidence-disposition-round14-superseded expect=0 got=2
ROW trace-inputs-round17-selftest superseded expect=0 got=0
ROW command-binding-selftest superseded expect=0 got=0
ROW command-binding-frozen-clean superseded expect=0 got=0
ROW command-binding-source-read-red superseded expect=1 got=1
```

The three `got=2` superseded rows are `could-not-evaluate` on rows whose
disposition files were retired in rounds 18/24; they are pre-existing, identical
at both revs, and do not enter the held fraction.

### 3.2 Base 367ec0f — not held

```
ROW verify-round15 expect=0 got=1 differs
```

```
$ python3 tools/registry-check.py --rev 367ec0f... --only verify-round15
ROW verify-round15 expect=0 got=1 differs
REGISTRY_CHECK: held=0/1 superseded=0
process exit 1
```

Same seven superseded `got` values as §3.1.

## 4. Row-by-row comparison and why the difference occurs

| row | base got | target got | verdict |
|---|---|---|---|
| `sources-census` | 0 held | **1 differs** | **result differs** |
| `verify-round15` | 1 differs | 1 differs | same result, not held in both |
| other 47 active rows | as expected | same | identical |
| 7 superseded rows | see §3.1 | same | identical |

Only the first line differs.

### 4.1 Why `sources-census` differs

Tree diff between the revisions (`git diff --name-status 367ec0f 9f3084b`):
only `.ufo/evidence/round-29/*` additions plus `corpus/QUALITY.md`,
`corpus/README.md`, `corpus/SOURCES.md`. `tools/` is untouched, so the row's
argv, expectation and the census script are identical at both revs (the script
blob hashes to `b9b754713c9c359823e85106e0177e6678bd95b567d1c897fd7f3464945a2bc3`
at both revs).

The one data edit that matters, `corpus/SOURCES.md`:

```
-| S024 | … | queued | 2026-10-19 | 365d | — |
+| S024 | … | mined  | 2026-10-19 | 365d | corpus/knowledge/survivor-fixture-minimization.md |
```

The entry that cell names is absent, at target and everywhere else:

```
$ git -C $R cat-file -e 9f3084bc...:corpus/knowledge/survivor-fixture-minimization.md
fatal: path 'corpus/knowledge/survivor-fixture-minimization.md' does not exist in '9f3084bc…'
$ git -C $R rev-list --all --objects | grep -c survivor-fixture-minimization
0
```

Running the census script directly at the target checkout gives exit 1 with the
two findings:

```
$ cd $R && bash .ufo/evidence/kaika-round-1/sources-census-v2.sh
…
== A mined used-by missing (must print nothing)
missing: corpus/knowledge/survivor-fixture-minimization.md
…
== B2 id-or-path cite (must print nothing)
no-id-or-path-cite: S024 corpus/knowledge/survivor-fixture-minimization.md (Reducer.html)
== VERDICT
SOURCES_CENSUS: VIOLATIONS
exit 1
```

and at the base checkout, exit 0 with `SOURCES_CENSUS: CLEAN (contract v1 + H4
id-or-path)` (the same script, same command, S024 still `queued` there so the
mined-used-by arm is not armed). Registry-check's captured tail at target:

```
== A mined used-by missing (must print nothing)
missing: corpus/knowledge/survivor-fixture-minimization.md
no-id-or-path-cite: S024 corpus/knowledge/survivor-fixture-minimization.md (Reducer.html)
== VERDICT
SOURCES_CENSUS: VIOLATIONS
```

This reproduces the finding already filed by the sibling seat
`.ufo/waves/round-29/w1/RerunCensusA.md`, from the registry side: the round-29
`SOURCES.md` edit is a forward pointer to the C2 deliverable, and the registry's
own census row is red until that deliverable lands.

### 4.2 Why `verify-round15` is not held at **both** revs (not a rev difference)

`tools/registry.json` marks this row `"external": true`. Its last sub-check runs
the census gate at an absolute live path, not at the graded clone
(`.ufo/evidence/round-15/verify.py:834-836`):

```
census_argv = [CENSUS_TOOL, "validate", "--root",
               "/home/vgpnk/Projects/shokunin", "tameshi"]
```

`CENSUS_TOOL` is `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
(`verify.py:105`). The live lane working tree currently carries the same
dangling S024 pointer, so the census sub-check fails whatever `--rev` is graded:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --root /home/vgpnk/Projects/shokunin tameshi
tameshi	W04	S047 … (7 pre-existing W04 warnings)
tameshi	E11	S024 missing used-by corpus/knowledge/survivor-fixture-minimization.md
exit 1
```

The captured tails at base and target are identical in the failing lines:

```
measure-historical-preserved: PASS all_baseline_bytes_preserved=1 changed=[]
sources-census: FAIL exit=1 (expected 0)
sources-census-ok-line: FAIL ok line absent
```

So `verify-round15` is a genuine second detector of the same defect, through the
live fleet root. Every other sub-check of that row passes at both revs. It will
turn green when the live lane tree contains the C2 entry file; it is not a
registry defect and not a base→target regression.

## 5. Controls

### 5.1 The missing entry file is the sole cause of the `sources-census` break

At 9f3084b, in a throwaway clone, adding one file
`corpus/knowledge/survivor-fixture-minimization.md` (two lines: a heading and
`source: S024`) and nothing else:

```
$ cd /tmp/RegistryNoHarm-Hq79/fixsim && python3 tools/registry-check.py --root . --only sources-census
ROW sources-census expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
process exit 0
```

Committed variant, graded through the same `--rev` path the assignment uses:

```
$ git add corpus/knowledge/survivor-fixture-minimization.md && git commit -m 'control: add C2 entry stub'
$ python3 tools/registry-check.py --rev HEAD --only sources-census
ROW sources-census expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
process exit 0
```

Direct census on the same tree returns `SOURCES_CENSUS: CLEAN (contract v1 + H4
id-or-path)` and exit 0. No other finding appears or disappears.

### 5.2 The live-root census failure in §4.2 is the same cause

Pointing the fleetside census at a root whose `tameshi-shokunin` is a clone
**with** the entry file returns `tameshi	ok	…/corpus/SOURCES.md` and exit 0
(`/tmp/RegistryNoHarm-Hq79/fleetcheck`), while the same command against a root
whose clone is at **base** (no entry file, S024 `queued`) also returns exit 0
(`/tmp/RegistryNoHarm-Hq79/fleetbase`). The failure in §4.2 therefore tracks the
`mined` + dangling-`used-by` state of the live lane tree, not the census tool and
not `--rev`.

### 5.3 Everything else is unaffected

The registry file itself is unchanged (`sha256 c1b75366…` at both revs, verified
with `git show <rev>:tools/registry.json | sha256sum`), `tools/` has no diff
between the revs, and 55 of 56 printed row lines are character-identical across
the two runs. The two corpus prose additions (`corpus/QUALITY.md` 55-57,
`corpus/README.md` Round 29) are read by no registry row.

## 6. Files changed

Only this report: `.ufo/waves/round-29/w1/RegistryNoHarm.md`.

No production file was created or edited. No `git add`/`commit`/`checkout`/
`reset`/`stash`/`push`/`fetch`/`pull` was run in
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`, in `/home/vgpnk/Projects/shokunin`,
or in any sibling lane. The single `git commit` in §5.1 was run inside the
throwaway clone `/tmp/RegistryNoHarm-Hq79/fixsim`, which is not a lane and holds
no lane state. Every read of the lane repo used `GIT_OPTIONAL_LOCKS=0`. No `jj`
command was run anywhere. All executing code ran under `/tmp` with `GIT_DIR`,
`GIT_WORK_TREE` and `GIT_INDEX_FILE` unset. No process started by this seat is
still running.

## 7. Installs and updates

None. No package was installed or upgraded; the probes needed only `python3`,
`git`, `bash`, `gawk` and `uv`, all already present.

## 8. Risks and blockers

- **Blocker for a green registry at the target rev:** `sources-census` is red at
  9f3084b because `corpus/SOURCES.md` S024 is `mined` with `used-by` pointing at
  `corpus/knowledge/survivor-fixture-minimization.md`, which exists in no commit
  of the lane repo. Owner: the C2/F6 build item; committing that entry file is
  the whole fix (§5.1).
- **Same defect, second detection path (environmental):** `verify-round15` is
  red at both revs because its census sub-check targets the live fleet root at a
  hardcoded absolute path (`verify.py:834-836`). It will clear when the live
  lane tree gains the C2 entry file; it is not a base→target regression and does
  not indicate a registry defect. Recorded so no one reads it as harm from the
  9f3084b commit.
- **Observation, out of this item's scope:** the three superseded
  `evidence-disposition-*` rows print `got=2` (could-not-evaluate) at both revs.
  They are excluded from the held fraction by the tool's own contract, so they
  are not a break; noted only so the 49-row denominator is not mistaken for a
  clean 49.
- No blocker for this item. The verdict is measured, reproducible (the
  `--only sources-census` run was repeated twice with identical output), and
  covered by a passing control.
