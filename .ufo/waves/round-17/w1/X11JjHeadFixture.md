# X11JjHeadFixture — jj head-vs-branch fixture (round 17, wave 1)

Verdict: **built** — red-before confirmed on the committed tool (fixture exit 1).

## Files changed

- `.ufo/evidence/round-17/jj/head-vs-branch.sh` (new, executable, 8315 bytes)

No other files written; no lane tools touched (new path, written directly per wave rules).

## What the script does

`head-vs-branch.sh <pin-disposition.py path>`:

1. `mktemp -d /tmp/tameshi-r17-jj-head-XXXXXX`, `trap rm -rf EXIT` → self-cleaning.
2. Builds `$SCRATCH/fleet/kagi-shokunin` as a git repo on branch `master`;
   commits v1 bytes to `corpus/surface-census.sh` (commit `MASTER_TIP`).
3. Emulates jj's `@-` snapshot per JjAuditTameshi.md §2.3 (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditTameshi.md`):
   `checkout --detach master`, write v2 bytes, commit → detached `HEAD` one
   commit ahead of `master` (`master..HEAD = 1`, `symbolic-ref HEAD` fails),
   v2 present only in the detached commit and the worktree. Real `jj` exists on
   the host (0.45.1, `~/.local/bin/jj`) but plain git reproduces the identical
   observable state, so the script stays hermetic — noted in script comments.
4. Writes a `pin-manifest-v1` manifest pinning `MASTER_TIP` + v1 sha256 for
   `bash-surface-census`; the other five recorded legs are present
   (pinned_commit = 40 zeros → `repo_missing`/`pinned_commit_missing` rows)
   because `read_manifest` rejects manifests that omit a leg
   (tools/pin-disposition.py `missing` check; run_mode still exits 0).
5. Runs `python3 $TOOL --manifest $M --root $FLEET`; extracts the leg's
   `head.commit`/`head.blob_sha256`/`pinned`/`worktree` fields and prints them.
6. Exit: `0` head.commit == master tip; `1` == detached commit; `2` setup,
   tool non-zero, or unmatched commit.

## Red-before run (committed tool @ 98bea7d)

Command:
```
T=$(mktemp -d); git -C tameshi-shokunin show 98bea7d...:tools/pin-disposition.py > $T/pin-disposition.py
.ufo/evidence/round-17/jj/head-vs-branch.sh $T/pin-disposition.py
```

Output (exits: tool 0, fixture 1):
```
FIXTURE master_tip=1267494c0649a104d117545fbef18211606ac476
FIXTURE head_detached=ea064feca1aea98b90fe2aff6320cd0f5aac48d0 (master..HEAD = 1, detached)
FIXTURE v1_sha256=78e89b5b…  pinned at master tip
FIXTURE v2_sha256=a0b7c69a…  only in detached HEAD + worktree
OBSERVED head.commit=ea064feca1aea98b90fe2aff6320cd0f5aac48d0 head.status=present
         head.blob_sha256=a0b7c69aba8e5de8daf156e19dc4763edb3fa8bb5898a5de2e3d0fc423b52078
OBSERVED pinned.commit=1267494c…  worktree.sha256=a0b7c69a…
VERDICT: head observation used detached HEAD (…v2 bytes) — jj @- snapshot reported as repo head
FIXTURE_EXIT=1
```

The committed tool's `head_observation` resolves `HEAD^{commit}` verbatim
(tools/pin-disposition.py `rev-parse ... "HEAD^{commit}"`), so on a jj-worked
lane it reports unpushed working-copy snapshot bytes (v2) as the repo's
"current" head, while `pinned` correctly reads the master-tip commit. This is
exactly the §2.3 hazard; a branch-safe fix would resolve
`refs/heads/master^{commit}` (audit §1.2 recommends it).

## Green-path note

Exit-0 arm is a literal `head.commit == $MASTER_TIP` compare; it cannot fire on
the committed tool (red is the point of the fixture). It fires for any tool
revision that resolves the branch ref instead of bare `HEAD` — the fixture
needs no change to grade post-fix tools. [INFERENCE: untested against a fixed
tool since none exists in this wave.]

## Evidence retained

- Fixture output above (full run shown verbatim in session transcript).
- `ls /tmp/tameshi-r17-jj-head-*` after the run: no scratch dirs remain →
  self-cleaning verified.
- No installs (git, python3, sha256sum, bash all host-provided; jj 0.45.1
  present but unused).

## Risks / blockers

- None blocking. Minor: manifest pins zero-commit placeholders for 5 legs, so
  `counts.unavailable` in the tool's JSON includes expected noise — the verdict
  only reads the exercised leg's `head` fields.
- The script emulates rather than invokes jj; if a future jj changes what it
  exports to git HEAD, this fixture tracks §2.3's documented state, not live jj.

## Follow-up 2

Requested repairs (w2/RerunPinBranch.md finding 1, w2/QualityCriteriaReview.md
§"every runner scrubs GIT_*"): the wave-1 script claimed `GIT_*` hermeticity
but only *set* five pins — an inherited `GIT_DIR` redirected every fixture
`git -C` so both setup commits landed in the victim repo before `SETUP-FAIL`.
Fixed in `.ufo/evidence/round-17/jj/head-vs-branch.sh` (rewritten, now 10411
bytes):

1. **GIT_* scrub**: after mktemp/trap, a `while read` loop over `env` output
   unsets every inherited `GIT_*` variable *before* any fixture git call; only
   the deliberate pins (`GIT_CONFIG_NOSYSTEM`, `GIT_CONFIG_GLOBAL=/dev/null`,
   `GIT_TERMINAL_PROMPT`, author/committer identity) are then re-exported.
2. **Scratch-containment assert**: `assert_gitdir_under_scratch` checks
   `realpath(git rev-parse --absolute-git-dir)` is under `realpath($SCRATCH)`
   after `git init` and again after the detached commit; escape → exit 2.
3. **Tightened verdict** (RerunPinBranch finding 2, opportunistic): exit 0 now
   requires `head.commit == master_tip` **and** `head.blob_sha256 == v1_sha`;
   exit 1 fires on the detached commit *or* the v2 blob — a mixed tool that
   names the branch tip but hashes HEAD's blob now goes red. `head.branch`
   (landed tools) is printed, null on the old tool.

### Runs (all in /tmp, lane untouched)

Tools extracted by `git show <rev>:tools/pin-disposition.py`:
old `98bea7d` sha256 `297253971d…`, landed `eb7838b` sha256 `331529eada…`.

- **Committed tool** → **exit 1** (red, still):
  `head.commit=a6f335eaf…` (the detached snapshot commit),
  `head.blob_sha256=a0b7c69a…` (v2 bytes), `head.branch=null`.
- **Landed tool (eb7838b)** → **exit 0** (green):
  `head.commit=f2cc247c…` = master tip, `head.blob_sha256=78e89b5b…` (v1),
  `head.branch=master`; `worktree.sha256` still reports the v2 worktree bytes.
- **Canary proof**: canary repo in /tmp (`HEAD=0bcca321…`),
  `env GIT_DIR=$CANARY/.git GIT_WORK_TREE=… GIT_INDEX_FILE=… GIT_OBJECT_DIRECTORY=…
  head-vs-branch.sh pin-new.py` → **exit 0**, canary HEAD unchanged
  (`0bcca321…`), `git fsck --strict` silent, canary object store holds only its
  own 3 objects (`git cat-file -t <fixture SHA>` → could not get object info).
  Note: the clean and canary fixture runs produced identical commit SHAs
  (`f2cc247c…`) — fixed identity + fixed messages + identical trees + the two
  runs landing in the same second make fixture commits deterministic; it is a
  coincidence artifact, not object reuse (canary has no fixture objects).

### Final script sha256

`33bdaeaebd9f6f358f512f7fd12807b08b7cc3697d70e2cc5c1deccb086058d3`
(`.ufo/evidence/round-17/jj/head-vs-branch.sh`, 10411 bytes)

Verdict: **built** — scrub verified by canary, red/green split on old/new tool
retained and tightened.
