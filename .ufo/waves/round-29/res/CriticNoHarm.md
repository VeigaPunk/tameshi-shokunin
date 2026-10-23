# CriticNoHarm — round 29

## Verdict first

No counterexample found in the assigned no-harm checks.

| Axis | Base → E → observed newer master | Verdict |
|---|---|---|
| Depth | recorded cases 9 → 9 → 9; score 9 → 9 → 9 | Unchanged; no detected harm. |
| Operability / registry | Eight selected active rows held at every revision, including `sources-census` | No detected harm in the exercised subset; not a full-battery verdict. |
| Source-registry validation | Fleet validation exits 0 at every revision; identical seven W04 warnings | No detected harm; warnings are inherited, not a warning-free result. |
| Protected-surface stability after `9f3084bc` | Empty protected-path diff and no intervening protected-path commits through newer master | No edits after that boundary to any named protected path. |

These are bounded attack results, not admission, promotion, or a verdict on the independent C1/C2 claims.

## Evidence

### Revisions and isolation

- Base: `367ec0f1d79cb9b67d724f2962e7554a0841b1fc`.
- E: `7a45f7b9d6a2542a553276330c8b02ac2e28c7ef`.
- Newer master observed and measured: `9bb699ad2d9f795dff95df85eb967129c54927d6`.
- Boundary: `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`.

Observed lane command, read-only:

```text
timeout 900 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse master
9bb699ad2d9f795dff95df85eb967129c54927d6
```

All Git writes were confined to my clones. Initial clone commands, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset, exited 0:

```sh
timeout 900 git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r29-CriticNoHarm
timeout 900 git -C /fast/scratch/hyaku/tameshi-r29-CriticNoHarm checkout -q --detach 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef
```

Fleet mirror: `/tmp/CriticNoHarm-nDTK/fleet`, with the other twenty `*-shokunin` directories linked read-only and a separate no-hardlinks tameshi clone. The mirror also links the fleet's `shokunin.conf`: the census requires that file even with an explicit lane (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:452-455,517-520`). Newer master was fetched into both own clones before measurement. Measurement subprocesses removed every inherited `GIT_*` variable and set `PYTHONDONTWRITEBYTECODE=1`.

### 1. Depth

Authority: E `SCORECARD.md:66,69-73`; actual ledger rows: E `tools/mutate-and-run.sh:87-95`. The rubric counts documented cases, not freshly replayed mutation kills.

Exact pipeline executed in `/fast/scratch/hyaku/tameshi-r29-CriticNoHarm`, via `timeout 900 bash -o pipefail -c`, with `REV` set separately to each full revision above:

```sh
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

Observed at base, E, and newer master independently; every pipeline exited 0:

```text
recorded_cases=9 depth_score=9
```

### 2. Registry

Source-census row authority: E `tools/registry.json:570-588`; the required stdout marker is at lines 579-580. Other exercised rows are at E `tools/registry.json:5,24,43,440,825,971,981`. Holding requires the expected exit and every registered stdout needle, not merely an exit-0 subprocess (`tools/registry-check.py:30-38`).

Working directory: `/tmp/CriticNoHarm-nDTK/fleet/tameshi-shokunin`. Exact command form, executed once for every combination of the three full revisions and eight row names below:

```sh
timeout 900 python3 tools/registry-check.py --rev REV --only ROW
```

Every outer command exited 0. These exact per-row output lines occurred at each revision:

```text
ROW sources-census expect=0 got=0 held
ROW repeat-control-snapshot-clean expect=0 got=0 held
ROW repeat-control-snapshot-mismatch expect=1 got=1 held
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
ROW command-binding-source-read-red-pinned expect=1 got=1 held
ROW receipt-window-selftest expect=0 got=0 held
ROW repeat-control-selftest expect=0 got=0 held
ROW mutate-and-run-selftest expect=0 got=0 held
```

Each individual invocation ended with:

```text
REGISTRY_CHECK: held=1/1 superseded=0
```

Thus 24 individual registered outcomes held: eight at base, eight at E, eight at newer master. The expected-red snapshot and pinned command-binding row remained red rather than being accidentally made permissive. No full-registry, nine-leg regression, or interop execution is claimed.

### 3. Fleet SOURCES census

Exact command:

```sh
timeout 900 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /tmp/CriticNoHarm-nDTK/fleet tameshi
```

Executed at E; then the own mirror clone was checked out detached at base for comparison and restored; finally it was checked out at newer master and measured there. All checkout commands used `timeout 900 git -C /tmp/CriticNoHarm-nDTK/fleet/tameshi-shokunin checkout -q --detach REV` and exited 0.

At each of base, E, and newer master, validation exited 0 with identical output:

```text
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	ok	/tmp/CriticNoHarm-nDTK/fleet/tameshi-shokunin/corpus/SOURCES.md
```

The validator explicitly permits warnings (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:16-18`) and identifies W04 as same-URL/different-scope, non-failing (`:33`). Consequently these warnings do not falsify the bounded no-harm result, but must not be described as absent.

### 4. Protected paths after the boundary

Exact commands in the own scratch clone, each exit 0 with empty stdout:

```sh
timeout 900 git diff --stat 9f3084bc 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef -- corpus/SOURCES.md corpus/README.md corpus/QUALITY.md SHONEN.md SKILL.md tools/
timeout 900 git diff --stat 9f3084bc 9bb699ad2d9f795dff95df85eb967129c54927d6 -- corpus/SOURCES.md corpus/README.md corpus/QUALITY.md SHONEN.md SKILL.md tools/
timeout 900 git log '--format=%H %s' --name-status 9f3084bc..7a45f7b9d6a2542a553276330c8b02ac2e28c7ef -- corpus/SOURCES.md corpus/README.md corpus/QUALITY.md SHONEN.md SKILL.md tools/
timeout 900 git log '--format=%H %s' --name-status 9f3084bc..9bb699ad2d9f795dff95df85eb967129c54927d6 -- corpus/SOURCES.md corpus/README.md corpus/QUALITY.md SHONEN.md SKILL.md tools/
```

The history query attacks the strongest net-diff loophole: an intermediate edit followed by a revert. It also found nothing. This excludes the boundary commit itself; it does not assert that the protected files were unchanged across the whole base-to-E interval.

Additional observed newer-head scope:

```sh
timeout 900 git diff --stat 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef 9bb699ad2d9f795dff95df85eb967129c54927d6 --
```

Output names six changed files, 189 insertions: `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-29.md`, and three `.ufo/evidence/round-29/{c1-at-E,c2-at-E,census-E}.stdout` receipts. None is a protected path above. The newer-head scope is therefore slightly broader than the context's three accounting documents, without a detected protected-surface regression.

## Smallest safe correction

No implementation correction is supported by these checks. Keep any no-harm statement explicitly bounded to the exercised registry subset, retain the seven inherited W04 warnings, and do not convert the unchanged depth counter into a new depth gain. This review supplies no reason for a canonical judge to reject on these four tested axes; unexercised registry rows remain outside its evidence.

## Tooling and cleanup

No tools installed or upgraded. No model, seat, or `jj` command invoked. All measurement commands completed. Final `timeout 900 fuser -v /fast/scratch/hyaku/tameshi-r29-CriticNoHarm /tmp/CriticNoHarm-nDTK/fleet/tameshi-shokunin` returned exit 1 with no output (no process using either checkout directory). No long-lived job was started. The only lane write is this assigned report.
