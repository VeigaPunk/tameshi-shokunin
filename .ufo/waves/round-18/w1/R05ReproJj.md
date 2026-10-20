# R05 — P08 jj-colocated HEAD falsifier

Axes: **falsification strength**, **fixture fidelity**, and **no-harm**. The test used only a `/tmp` repository; the lane and helper source were read-only.

## Source and fixture

Read `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh` (no execution in the lane). Its commit path checks that `@-` is the branch tip or re-anchors an empty working copy (`:580-594`), commits the named paths (`:596-606`), then moves the branch bookmark to that commit (`:658-659`). In an analogous colocated fixture, that normal commit/bookmark sequence initially left Git `HEAD` and `refs/heads/master` equal at `35373f8980a055a2642b4bd3bc3ec5db2feb9089`. I then used `jj new d1e83cbe34ee99476ced531b1f596b18f19ed80f` to move the colocated working copy onto the older base without moving `master`, and committed a side history. This produced the required distinct Git HEAD and branch tip. This distinction matters: the helper's straight-line commit/bookmark sequence alone did not create the mismatch in this fixture.

Created `/tmp/tameshi-r18w1-R05ReproJj-azGixW/colocated` from a Git repo, then ran `jj git init --colocate .` (exit 0; `Initialized repo in "."`). The checker was copied from the lane clone checked out at `183f87b899e6cae46be98d251cbc87fb5118f6ca`; the clone's `git rev-parse HEAD` was exactly that revision. Fixture commits were made with local fixture identity and with inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, and `GIT_COMMON_DIR` unset.

The final side-history candidate `D=3d647f2642727482d28c7aef58766edebd0d8ece` contains the original `tools/side-marker.txt` bytes (`side anchor\n`); the HEAD-only commit changes those bytes to `head-only marker bytes\n`. The branch tip has no `tools/side-marker.txt` entry.

## Exact final state

Commands, from the fixture directory:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR git rev-parse HEAD
0fa9629c39872f36f1dcca857c3f66180f781c41

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR git rev-parse refs/heads/master
35373f8980a055a2642b4bd3bc3ec5db2feb9089

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR git merge-base --is-ancestor D HEAD
exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR git merge-base --is-ancestor D refs/heads/master
exit 1
```

`jj log --ignore-working-copy --no-graph -n 8` (exit 0) showed, from newest to oldest: the empty working-copy commit `c3553615`; `0fa9629c` (`head-only marker revision`); `dbd7df67` (`head-only instrument move`); `3d647f26` (`side historical anchor with pinned tool bytes`); then the distinct `master` bookmark at `35373f89` (`helper commit subject change`), followed by base `d1e83cbe`. `git status --short` was empty after removing Python's generated fixture `__pycache__`.

## G2/G3 outcome

Using the permitted direct-function route, imported the copied dispatch-version `tools/evidence-disposition.py` and called `resolve_historical_rev(lane, D)`, `check_historical_waiver(lane, "tools/side-marker.txt", sha256(b"side anchor\\n"))`, and `historical_blob(lane, D, ...)`. The Python command exited 0 and printed:

```text
G3_RESOLVE_HISTORICAL_REV=PASS
G2_CHECK_HISTORICAL_WAIVER=PASS
HISTORICAL_BLOB_PIN_MATCH=True
G3_BRANCH_TIP_ANCESTOR_EXIT=1
G2_BRANCH_TIP_TREE_ENTRY=None
```

This is the behavioral split: the dispatch implementation's G3 runs `git merge-base --is-ancestor <rev> HEAD` (`tools/evidence-disposition.py:441-455`), so the candidate passes although it is not an ancestor of `refs/heads/master`. G2 reads `HEAD:<path>` (`:510-540`), so it accepts bytes committed only on that HEAD history even though the branch tip has no entry. The branch-tip comparison rejects both cases. This falsifies P08's required branch-tip behavior at the dispatch revision.

Verification used the allowed G2/G3 direct-function route rather than constructing full receipt/manifest inputs; no full CLI run or selftest is claimed. No tools were installed or updated.

**Verdict: falls — dispatch G2/G3 follow Git HEAD rather than `refs/heads/master` in a jj-colocated mismatch fixture.**
