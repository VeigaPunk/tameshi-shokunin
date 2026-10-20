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
