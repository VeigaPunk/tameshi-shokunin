# ScoutJjBounds — routed item 5 (jj seat bounds), round 26 wave 1

## Verdict

Yes, this wave's context closes the wording gap. Round-25 wave context only banned
"git/jj write commands ... any mutating jj" in the lane and said "never touch the fleet repo"
without naming `jj`; a seat could read that as permitting `jj log` at the fleet root. The
round-26 wave-1 context (materialized at `.ufo/waves/round-26/spec-w1.json`, context lines 14-16)
names `jj log`, `jj st`, the fleet root, the lane and clones, and gives the reason. That is the
fix round-25.md:83 prescribes. Two residuals are noted at the end: enforcement is still
instruction-only, and the stated absolute ("any jj command snapshots") is slightly stronger than
the documentation ("snapshots ... at the beginning of every command" unless
`--ignore-working-copy`).

## Observed facts (all commands read-only; no `jj` command run anywhere)

### 1. `.jj` exists at the fleet root and is colocated with `.git`

```
$ ls -d /home/vgpnk/Projects/shokunin/.jj
/home/vgpnk/Projects/shokunin/.jj            # exit 0
$ ls -la /home/vgpnk/Projects/shokunin/.jj
.gitignore  repo/  working_copy/             # .jj/.gitignore contains "/*"
$ cat .jj/repo/store/git_target
../../../.git
$ GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin rev-parse --git-dir
.git                                          # same working copy => colocated
```

`.jj/repo` was created 2026-10-22 00:49:49, before round 25's `spec.json` (written 05:19:29).
The lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.jj` also exists (`ls -d`, exit 0).

### 2. The last jj operation at the fleet root was a `jj log`, during round-25 wave 1

Read as ordinary files under `.jj/repo/op_store/`:

- 25 operation records; `op_heads/heads/` holds one head, `cd619a73...`, mtime
  2026-10-22 05:21:22. `.jj/working_copy/{checkout,tree_state}` and
  `.jj/repo/index/{segments,op_links}` were written at the same second.
- Three op records stamped 05:21:22 (`6cfde235...`, `87db3f16...`, head `cd619a73...`) embed
  the argument string `jj log --no-graph -n 6`. The head record also contains
  `import git refs`.
- No fleet-root op record contains `jj st`.

Round-25 `spec.json` was created 05:19:29 and its `w1/` directory was active from 05:19; the
05:21 snapshot therefore falls inside round-25 wave 1, matching round-25.md:83:
"seat ReReplay14 ran `jj log` at the fleet root; its report says a working-copy reset and git
import were printed". Op records carry no seat identity (strings `plazir27*`, `vgpnk2` only), so
the seat attribution still rests on that record, not on my reading.

Documented basis, opened this session (2026-10-22):
- https://docs.jj-vcs.dev/latest/cli-reference/ — "By default, Jujutsu snapshots the working copy
  at the beginning of every command." and "`--ignore-working-copy` — Don't snapshot the working
  copy".
- https://docs.jj-vcs.dev/latest/git-compatibility/ — "Jujutsu will import and export from and to
  the Git repo on every `jj` command automatically." (colocated section).
- https://docs.jj-vcs.dev/latest/changelog/ — "In colocated repos, any files that jj considers
  added in the working copy will now show up in `git diff` (as if you had run
  `git add --intent-to-add` on them)."

So `jj log` does create an operation (snapshot plus git import) even though it changes no source
file: the fleet root carries that operation today.

### 3. Fleet `git status` and untracked files naming round 25/26

```
$ GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin status --porcelain
 A .scratch/goal-20261022-hyaku-12h.md
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kengaku.report-baseline
 A .ufo/state/kotoba.report-baseline
 A .ufo/state/kotodama.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 A .ufo/state/revenger.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 A scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
 A write
```

- Untracked (`??`) count: 0, also with `--untracked-files=all`.
- **No untracked file names tameshi, round 25 or round 26.** The only path naming tameshi is the
  tracked `.ufo/state/tameshi.report-baseline` (modified).
- The six ` A` entries are intent-to-add: `git ls-files --stage` shows the empty blob
  `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` for each, and `git ls-files --debug` shows zeroed
  stat data and `flags: 20004000`. Their names (`write`, hyaku goal, three `report-baseline`
  files, one `__pycache__` file) do not mention either round. Contents: `write` is
  `agent://U100N079H334f935b`; the goal file is the hyaku 12-hour contract; each baseline is
  `<pid> e3b0c44298fc...` (the empty-report hash).
- This set matches the changelog's description of jj's colocated index behaviour, so it is
  consistent with the routed defect. It is not dated proof: index stat data is zeroed, file
  mtimes span 2026-10-21 14:54 to 2026-10-22 07:32, and earlier jj activity clusters exist at
  00:49-00:53, 01:01, 01:30-01:32 and 01:36. The entries cannot be attributed to one seat from
  bytes alone.

### 4. Bound texts compared

- Round-25 `spec.json`, context line 13: "never run git/jj write commands
  (add/commit/checkout/reset/stash/push/fetch, any mutating jj) in
  /home/.../tameshi-shokunin; never touch the fleet repo /home/.../shokunin, sibling lanes,
  lane jj state or the lane Git index. Read-only git with GIT_OPTIONAL_LOCKS=0 is fine."
  `jj log` is not a write command; the fleet clause does not name jj. Gap.
- Round-25 spotcheck lines 204-205 name it: "Seat bounds: ReReplay14 ran `jj log` at the fleet
  root, and ReOutputComplete ran `jj st` in the lane. Wave contexts must name `jj` beside git."
- Round-26 `spec-w1.json`, context lines 14-16: "Never run ANY `jj` command anywhere — not
  `jj log`, not `jj st`, not at the fleet root ..., not in .../tameshi-shokunin, not in a clone:
  any jj command snapshots a colocated working copy (round-25 seats did this; it is a routed
  defect)." Gap closed. Note the file is `spec-w1.json`; there is no `round-26/spec.json`.

## Inference (labelled)

- The 05:21:22 op is the trace of a seat's read-only `jj log --no-graph -n 6`, so the harm is
  reachable exactly as the lesson says: a command a seat believes is observational wrote an
  operation, imported git refs and refreshed the working copy. [supported by op-store strings and
  the two jj doc quotes above; seat identity is inference]
- Because the prohibition is context text only, nothing prevents a recurrence; the fleet jj
  operation store is the obvious read-only tripwire (head mtime or op count) if Main wants
  detection rather than instruction. [inference, not implemented — out of this item's scope]

## Remaining unknowns

- Which seat ran the 05:21 fleet `jj log`: op records carry no seat name.
- Whether the lane `jj st` by ReOutputComplete happened as recorded: lane `.jj` state was out of
  bounds for this scout ("never touch lane jj state"), so it is unverified here.
- Installed jj version: the binary is `/home/vgpnk/.local/bin/jj` (31,077,192 bytes,
  2026-10-03 18:33); its version was not read because that needs a `jj` invocation. Docs cited
  are the "latest" pages, not necessarily the installed build.
- Whether some intent-to-add entries predate round 25; the index stores no usable stat data.

## Smallest safe correction

Keep the round-26 context wording; it implements the prescribed fix. The one calibration nit is
the absolute "any jj command snapshots a colocated working copy": the documentation says the
snapshot is default behaviour, cancelled by `--ignore-working-copy`, and a command run outside a
repo (for example `jj --version`) snapshots nothing. If the L1 wants the stated reason to match
the source, say "every jj command snapshots by default". No production file was edited by this
scout; no tool was installed or upgraded.
