# S20JjLaneState — read-only jj/git state of lane `tameshi`

Seat `S20JjLaneState`, round-17 wave 1. Observation window **2026-10-20 12:16–12:26 -03:00**.
All reads; no `jj` write, no git write, no lane file written except this report. Nothing was
installed or upgraded for this seat. Lane tip at dispatch and throughout: `98bea7da5801f4bc58e4187690ee1687c8a5061f`.

Renderer for any jj read: `jj` **0.45.1** (`~/.local/bin/jj`), git **2.56.0**, jj remote
`origin https://github.com/VeigaPunk/tameshi-shokunin.git`.

## Facts table

| # | Fact | Command | Observed | Exit |
|---|---|---|---|---|
| 1 | Lane state line (first observation, before 12:21) | `scripts/hyaku/jj-lane.sh state <lane>` | `state branch=master local=98bea7da… remote=98bea7da… ahead=0 behind=0 head=detached tracked=0 untracked=3` | 0 |
| 2 | Lane state line (12:24:11, after sibling writes) | same | `… tracked=2 untracked=5` | 0 |
| 3 | Git HEAD is detached | `git -C <lane> symbolic-ref -q HEAD` | *no output* | **1** |
| 4 | `--abbrev-ref` prints the literal string `HEAD` | `git -C <lane> rev-parse --abbrev-ref HEAD` | `HEAD` | 0 |
| 5 | No upstream | `git -C <lane> rev-parse @{u}` | `fatal: HEAD does not point to a branch` | **128** |
| 6 | `.git/HEAD` is an object id (detached), not a ref | `cat .git/HEAD`; `stat` | `98bea7da5801f4bc58e4187690ee1687c8a5061f`, mtime `12:06:01.625` | 0 |
| 7 | Index clean; no staged entries | `git diff --cached --name-only \| wc -l` | `0` (`.git/index` mtime `12:06:08`) | 0 |
| 8 | Branch local = remote = HEAD commit | `git rev-parse refs/heads/master refs/remotes/origin/master HEAD`; `git ls-remote origin refs/heads/master` | all `98bea7da5801…` | 0 |
| 9 | jj working copy | `jj --ignore-working-copy -R <lane> status` | `Working copy (@): tpwwpzrl 890ac9e1 (empty)`; `(@-): lqnopzwy 98bea7da master` | 0 |
| 10 | Repo-level jj config | `jj --ignore-working-copy -R <lane> config list --repo` | `revset-aliases."trunk()" = "master@origin"`; **`snapshot.auto-track = "none()"`**; `user.name = "tameshi-shokunin"`; `user.email = "tameshi@shokunin.local"` (exactly 4 keys) | 0 |
| 11 | Repo config lives **outside** the repo | `jj --ignore-working-copy -R <lane> config path --repo` | `/home/vgpnk/.config/jj/repos/900fa08b5e426ae84a97/config.toml` (mtime `12:07:32`) | 0 |
| 12 | max-new-file-size is default | `jj … config get snapshot.max-new-file-size` | `1MiB` (unset) | 0 |
| 13 | `immutable_heads()` is the builtin only | `jj … config get 'revset-aliases."immutable_heads()"'` | `builtin_immutable_heads()` — the pilot's `\| ::bookmarks()` alias is **absent** | 0 |
| 14 | `.gitignore` **at HEAD** | `git -C <lane> show HEAD:.gitignore` | one line: `.ufo/interactive-sessions/` (27 B) | 0 |
| 15 | `.gitignore` **in worktree** | `cat -A`; `stat` | 3 lines / 57 B: `.ufo/interactive-sessions/`, `.ufo/state/`, `.ufo/watchdog.log`; mtime **`2026-10-20 12:21:34.984487734`**; `git diff` = `+2` lines; status ` M .gitignore` | 0 |
| 16 | Lane `.ufo/state/` and `.ufo/watchdog.log` | `ls -d .ufo/state`; `ls .ufo/watchdog.log` | **absent** (exit 2 each) | 2 |
| 17 | Fleet-root driver runtime | `ls -la /home/vgpnk/Projects/shokunin/.ufo/` | `.ufo/state/` exists; `.ufo/watchdog.log` 34 821 B | 0 |
| 18 | Ignore status flipped during the seat | `git check-ignore -v --no-index .ufo/state/x .ufo/watchdog.log` | before 12:21: no match, exit 1; after: `.gitignore:2:.ufo/state/`, `.gitignore:3:.ufo/watchdog.log` | 0/1 |
| 19 | `.jj` is invisible to git | `git check-ignore -v --no-index .jj/repo/config-id` | `.jj/.gitignore:1:/*` (jj's own 3-byte ignore file) | 0 |
| 20 | jj op log = 10 ops; `.jj` was **re-created at 11:50:14** | `ls -t .jj/repo/op_store/operations` + `strings` | oldest 4 ops at `11:50:14`: `add workspace 'default'`, `import git refs`, `import git head`, `track remote bookmark master@origin` → a fresh `jj git init --colocate` (the 2026-10-19 20:39 op generation is gone) | 0 |
| 21 | Tip commit was **made by jj** | ops at `12:06:01–03` | `track paths` → `snapshot working copy` → `edit commit metadata for a25a30b` → `commit 63a13c6` → `point bookmark master to 98bea7da` → `jj git push --remote origin --bookmark master` | 0 |
| 22 | Tip identity | `git log -1 --format='%an <%ae> / %cn <%ce>' 98bea7da` | `protocol-shokunin <protocol@shokunin.local>` for **both**; committer date `2026-10-20 12:06:01 -0300`; 1 file, 245 insertions | 0 |
| 23 | jj keep refs contaminate `--all` walks | `git for-each-ref refs/jj/keep \| wc -l`; `git log --all --oneline`; `git rev-list --all --count` | **17** keep refs; `--all` = **64** commits and includes `63a13c6` with an **empty subject** | 0 |
| 24 | `63a13c6` is a header-only duplicate of the tip | `git cat-file -p` on both | same tree `4e9f745`, same parent `017a2b0`, same author/committer, same `change-id lqnopzwy…`; 277 B vs 351 B — only the message is missing | 0 |
| 25 | Lane docs say nothing about jj | `grep -ci 'jj' SKILL.md README.md`; `grep -ci jujutsu` | `0` / `0` (LOG.md's only "pushed" hit is a report line, LOG.md:1029) | 0/1 |
| 26 | Report-hash convention lives fleet-side | `grep -n pushed scripts/hyaku/{lane-addendum,closure-prompt}.md` | `lane-addendum.md:127`, `closure-prompt.md:53` — cite `landed <hash>` (older helper prints `pushed <hash>`), never `committed` | 0 |
| 27 | Live `pin-disposition.py` still resolves **HEAD** | `sed -n '315,320p' tools/pin-disposition.py` | `head_observation()` → `rev-parse --verify --quiet --end-of-options HEAD^{commit}` | 0 |
| 28 | Live `mutate-and-run.sh` has no repo-identity guard | `grep -n 'rev-parse --show-toplevel\|realpath\|GIT_CEILING' tools/mutate-and-run.sh` | only a sandbox `GIT_CEILING_DIRECTORIES` at :1222; the `git -C "$repo"` leg materialization at :1001–:1019 has no toplevel check | 0/1 |
| 29 | No round-17 staged instruments yet | `ls .ufo/waves/round-17/`; `find …/staged` | `staged/` **absent** at 12:24 (spec/dispatch/spawn/assignments present) | 2 |

Live-tree change during the seat (not mine; four sibling reports S03/S05/S06/S08/S09 note it too):
` M .gitignore` **and** ` M .ufo/evidence/round-16/round-gate/runner-sha256.txt` share the byte-identical
mtime `12:21:34.984487734` (one operation touched both); new untracked `?? .ufo/evidence/round-15/attempt-4/`
and `?? .ufo/evidence/round-15/verification-4.json` also appeared between facts 1 and 2.

## JjTrialTameshi.md recommendations vs current state

Source: `.ufo/waves/hyaku/jj-w1/reports/JjTrialTameshi.md` §Recommendations (per-lane). Verifier
header claim (`.ufo/evidence/round-17/…`) reads the same report.

| # | Recommendation | Status now | Evidence |
|---|---|---|---|
| R1 | Keep `snapshot.auto-track="none()"` | **Applied / holds** | fact 10; 5 untracked paths stayed `??` and `jj status` stayed clean across all reads |
| R2 | Add `.ufo/state/` and `.ufo/watchdog.log` to `.gitignore` | **Worktree-only — not landed** | facts 14/15/18: present since 12:21:34, absent from HEAD `98bea7da`; `staged/` does not exist yet |
| R3 | "Lane tooling needs no changes" | **Superseded — not applied** | JjAuditTameshi R1/R2 (repo-identity guard, branch-tip instead of HEAD) contradict it; live bytes still HEAD-based (facts 27/28); round-17 C2 claims these as "jj fixes", staged for post-wave install |
| R4 | Report convention: cite the pushed hash, never `committed` | **Applied fleet-side** | `lane-addendum.md:127`, `closure-prompt.md:53`; helper prints `pushed <hash>` (the addendum calls that the older helper). No lane file restates it (fact 25) |
| R5 | No per-lane jj config beyond what `init` sets | **Holds** | fact 10: exactly trunk alias + identity + auto-track; no `max-new-file-size` change (fact 12) |

## Remaining jj recommendations not yet applied

1. **Land the `.gitignore` fix.** The two lines exist only in the worktree (mtime 12:21:34); the
   branch tip and origin still carry the 1-line file. Action: one pathspec-limited
   `jj-lane.sh commit <lane> --as <id> -m … -- .gitignore`.
2. **Install the two jj-safety tool fixes** (round-17 C2, `JjAuditTameshi` R1/R2): branch-tip
   resolution in `tools/pin-disposition.py` (today `HEAD^{commit}`, fact 27) and a repo-identity
   guard in `tools/mutate-and-run.sh` (today none on the live `git -C` leg, fact 28). Not staged
   as of 12:24.
3. *(Adjacent, JjRevengerLaneJjState rec 4 — not in JjTrialTameshi)* `immutable_heads()` is the
   plain builtin: the pilot's `builtin_immutable_heads() | ::bookmarks()` alias did not survive the
   11:50 clean re-init. Builtin = `trunk() | tags() | untracked_remote_bookmarks() | untracked_remote_tags()`
   (`jj help -k revsets`), and `trunk() = master@origin`, so pushed master history and the `cursor/*`
   remote bookmarks remain immutable. Residual: any *local* non-trunk bookmark would not be
   protected. [INFERENCE] Low risk for this lane, whose only bookmark is `master`; re-setting the
   alias is a lane decision, and JjTrialTameshi R5 argues against adding config.
4. *(Adjacent, revenger rec 6)* Exclude `refs/jj/keep` from global commit walks. Now demonstrated
   concretely: `git log --all` returns 64 commits, including header-only object `63a13c6` whose
   subject is empty (facts 23/24). Any census/hash enumeration must use explicit branch refs or
   filter `refs/jj/keep`.
5. *(Adjacent, revenger rec 5)* Dirty-index guard at commit time: the helper does not reject a
   non-empty `git diff --cached`. Index was clean all seat (fact 7); no live defect.
6. *(Adjacent, revenger rec 7)* Diagnostic divergence line in `init`: moot — the lane is past init
   and `state` agrees with the jj view (`master`, `master@git`, `master@origin` all `98bea7da`).

## Interpretation

- The lane is **healthy and in the post-trial regime**: `.jj` was freshly re-colocated at
  11:50:14, `auto-track=none()`, one empty working-copy commit on top of the branch tip, and the
  current tip (`98bea7da`) was itself produced by the jj helper path at 12:06 (round-16 spot-check,
  `protocol` identity), so the git history carries a jj `change-id` header and the git reflog
  records `HEAD@{0}: export from jj`.
- Detached HEAD is the expected jj invariant (JjDocHeadAttachment: `jj commit` detaches at `@-` and
  never re-attaches). Here HEAD = `@-` = branch tip, and `@` is empty, so the classic `JjAuditTameshi`
  R2 hazard (HEAD ahead of the bookmark) is **not active now** — but it is one snapshot away, which
  is why the branch-tip fix in item 2 matters.
- The `state` helper line is a *worktree* line, not a commit-readiness verdict: `tracked`/`untracked`
  counted `0/3` at 12:16 and `2/5` at 12:24 purely from sibling writes; `local/remote/ahead/behind`
  stayed `98bea7da/98bea7da/0/0` throughout and `ls-remote` confirmed origin.

## Residual unknowns

- Who wrote `.gitignore` (+`runner-sha256.txt`) at 12:21:34 is not observable from git/jj (no
  worktree-level provenance); sibling reports attribute it to "other seats". I did not write it.
- The empty-message object `63a13c6` mechanism (same tree/parent/identity/change-id, missing message)
  is an internal jj write artifact; I observed the artifact, not the code path. [INFERENCE] It is
  the pre-describe commit object that jj keeps for the op log, retained via `refs/jj/keep`.
- `~/.config/jj/repos/` holds two additional stale entries with the `tameshi-shokunin` identity, one
  with `auto-track = "all()"` (mtime 11:17:16, a sandbox path from the jj trial). They do not affect
  the live lane (live path resolves to `900fa08b…`, fact 11); their path hashes were not mapped.

## Commands used (verbatim, lane root = `<lane>`)

```
scripts/hyaku/jj-lane.sh state <lane>
git -C <lane> symbolic-ref -q HEAD ; echo $?          # 1
git -C <lane> rev-parse --abbrev-ref HEAD             # HEAD
git -C <lane> rev-parse '@{u}'                        # fatal: HEAD does not point to a branch (128)
git -C <lane> rev-parse HEAD refs/heads/master refs/remotes/origin/master
git -C <lane> ls-remote origin refs/heads/master
git -C <lane> log -1 --format='%an <%ae> / %cn <%ce>' 98bea7da
git -C <lane> cat-file -p 98bea7da ; git -C <lane> cat-file -p 63a13c6
git -C <lane> for-each-ref refs/jj/keep | wc -l       # 17
git -C <lane> log --all --oneline                     # 64, includes empty-subject 63a13c6
git -C <lane> show HEAD:.gitignore ; cat -A <lane>/.gitignore ; git -C <lane> diff -- .gitignore
git -C <lane> check-ignore -v --no-index .ufo/state/x .ufo/watchdog.log .jj/repo/config-id
jj --ignore-working-copy -R <lane> status
jj --ignore-working-copy -R <lane> config list --repo
jj --ignore-working-copy -R <lane> config path --repo
jj --ignore-working-copy -R <lane> config get snapshot.max-new-file-size
jj --ignore-working-copy -R <lane> config get 'revset-aliases."immutable_heads()"'
jj --ignore-working-copy -R <lane> help -k revsets | grep -A6 builtin_immutable_heads
ls -t <lane>/.jj/repo/op_store/operations ; strings <op-file>
ls -d <lane>/.ufo/state <lane>/.ufo/watchdog.log
grep -ci 'jj' <lane>/SKILL.md <lane>/README.md
sed -n '315,320p' <lane>/tools/pin-disposition.py
```

**Verdict: partial** — every JjTrialTameshi keeper holds (auto-track `none()`, init-only config,
pushed-hash convention fleet-side) except the `.gitignore` fix, which is worktree-only and unlanded,
and the "tooling needs no changes" rec, which the round-17 jj fixes supersede and which is not yet
in live bytes.
