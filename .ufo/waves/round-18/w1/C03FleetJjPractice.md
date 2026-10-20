# C03FleetJjPractice — fleet HEAD vs branch tip, against contract D

Round 18 wave 1, connector seat. Read-only. No sibling file edited. No tool installed.
Scratch: `/tmp/tameshi-r18w1-C03FleetJjPractice-w177T3` (jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5).
Labels: **[OBS]** command output from this seat; **[DOC]** a cited report's own quoted output; **[INFER]** reading.

Axes used: rule fidelity (what the fleet actually resolved), contract match (D vs that rule), staleness (sibling sentences that still describe v1).

## Verdict

partial

Contract D's comparison target matches the fleet rule. The only procedure D names (`jj git init --colocate`) does not produce the `HEAD !=` branch-tip state D's selftest needs, and "resolved" is not pinned to v2 `cmd_state`, so a copy of the still-cited v1 ladder would leave P08 open.

## 1. Agreed resolution rule

The rule that survived helper v2 (fleet `14df5b933128bc04495b7b646672956db3d7ac03`, 2026-10-20T13:05:01-03:00, ancestor of fleet HEAD `ae12f330697d09bcf7fa7df7552e1c48a6443950`; those four doctrine files are porcelain-clean) is:

The lane tip is the commit at `refs/heads/<branch>`. Git HEAD is not that tip. `@{u}`, `--abbrev-ref HEAD`, and `branch --show-current` are not branch sources. A cited hash is an ancestor of the branch ref. Push/landed is a separate check (`ahead=0` and `git ls-remote origin refs/heads/<branch>`), not a substitute for the local tip.

| where | what it binds |
|---|---|
| `scripts/hyaku/lane-addendum.md:173-177` | After the first helper commit, HEAD is detached. Read the tip with `jj-lane.sh state` (`local=`) or `git rev-parse <branch>`. Record measured revisions as the branch tip, never bare `HEAD`. |
| `scripts/hyaku/inline.sh:33-34` and `:37` | `lane_tip` is `state`'s `local=` field. Never read `@{u}` or HEAD for lane state. |
| `scripts/hyaku/closure-prompt.md:22-26` and `:54` | `merge-base --is-ancestor <hash> <branch>`. Confirm the push with `ls-remote origin refs/heads/<branch>`. |
| `scripts/hyaku/jj-lane.sh:113-126` | `detect_branch`: attached `refs/heads/*` only (anything else, including `refs/jj/*`, is ignored), else `refs/remotes/origin/HEAD`. No master/main/first-branch fallback inside this function. |
| `scripts/hyaku/jj-lane.sh:155-175` | `state`: `lane.branch`, else `detect_branch`, else the single name among `master` and `main` if exactly one exists. `local` is `rev-parse --verify refs/heads/$branch` and must match `^[0-9a-f]{40}$` or the command exits 1. `ahead`/`behind` are branch-vs-branch. HEAD is only `attached`/`detached`. |
| `scripts/hyaku/jj-lane.sh:454-456` and `:610-615` | "Git tracks it" means present in `refs/heads/$branch:<path>`. The bookmark moves only after the new commit's parent is that tip. |
| `.ufo/waves/hyaku/PHASE2.md:76-80` | Lane tips are recorded from `refs/heads/<branch>` because colocated HEAD detaches and `@{u}` is unusable. |
| tameshi `corpus/lessons/round-17-verifier-spotcheck.md:437-439` | R17-JJ-GUARDS: G2/G3 still compare to HEAD. Repair against the resolved branch tip. Equality at one closure is not every jj state. |

v1 (`67a3123:53-65`, **[OBS]** `git show 67a3123:scripts/hyaku/jj-lane.sh`) was a different function: `symbolic-ref -q --short HEAD`, then `origin/HEAD`, then `master`, then `main`, then the first `refs/heads/` name, and `print_state` printed `local=-` when the ref was absent. That function is not the current rule. Lines 53-65 of the live file are `usage()` help text (**[OBS]** `sed` of the clean worktree).

## 2. What HEAD actually is (jj 0.45.1)

**[DOC]** `JjDocHeadAttachment.md:13-23` and **[OBS]** this seat, scratch `…-w177T3`, exit 0. Two fresh `git init -b master` repos, one commit, `jj git init --colocate` from inside the repo (a `jj -R <git-repo> git init` does not create the repo; that attempt is discarded).

| step | HEAD | `refs/heads/master` | trees | ancestry |
|---|---|---|---|---|
| after `jj git init --colocate` | attached `refs/heads/master`, `5d0d02438ddfe98772f442f11aeb484713cc6746` | same | same | mutual ancestors (rc 0 / 0) |
| repo A, then `jj new -m n1` | detached `7cad1d65d2faaf55cc7252614ad2ec5a50e0a49b` (jj: `@-`, empty) | still `5d0d024…` | `HEAD^{tree}` = `master^{tree}` = `08585692ce06452da6f82ae66b90d98b55536fca` | `HEAD` ancestor of master rc=1; master ancestor of `HEAD` rc=0 |
| repo B, edit `a.txt`, `jj commit -m divergence -- a.txt`, no bookmark move | detached `4ae747a4452482d6397194e924e05bde64bba9d3` (jj: `@-`, description `divergence`) | still `5d0d024…` | `HEAD:a.txt` = worktree `61780798228d17af2d34fce4cfbdf35556832472`; `master:a.txt` = `78981922613b2afb6025042ff6bd878ac1994e85` | `HEAD` ancestor of master rc=1 |
| repo B, `jj bookmark set master -r @-` | still detached, `4ae747a4…` | now `4ae747a4…` | equal | — |

So:

- Colocation init leaves HEAD attached at the branch tip. It does not create the divergence.
- `jj new` moves HEAD to the previous working-copy commit. Commit ids diverge. Trees do not. A G2 byte check cannot see it.
- `jj commit` of a content change, before `bookmark set`, puts HEAD at the new `@-`. Live bytes match `HEAD:` and differ from `refs/heads/<branch>:`. The new commit is an ancestor of HEAD and not of the branch. This is the G2 and G3 split.
- After the bookmark moves, HEAD equals the branch tip and stays detached.

Live tameshi is that last state, not the window. **[OBS]** `git -C tameshi-shokunin rev-parse HEAD` and `rev-parse refs/heads/master` both `183f87b899e6cae46be98d251cbc87fb5118f6ca`; `symbolic-ref -q HEAD` rc=1; `git config --get lane.branch` = `master`. A probe of this checkout cannot show P08 open.

`JjAuditGameDev3d.md:121-131` and `:166-175` (HEAD after `jj new` is an empty commit, not an ancestor of `main`, and equals `main` only after `bookmark set`) match repo A/B. They are the same graph as `JjDocHeadAttachment.md` F2/F3, not a second rule.

## 3. Contract D against that rule

D says G2 (live bytes committed) and G3 (rev is an ancestor) compare to the resolved branch tip `refs/heads/<branch>`, never bare HEAD; selftests for G3 tag-object refusal, G5 symlink-mode refusal, and a colocated fixture (`jj git init --colocate` in `/tmp`; HEAD != branch tip) that fails on the HEAD-based code; v1/v2 schemas and exits unchanged.

At dispatch tip `183f87b` (equals `refs/heads/master`; porcelain clean for the two tools) the code is still HEAD-based:

- G3 `tools/evidence-disposition.py:441-455` — `merge-base --is-ancestor` against `HEAD`.
- G2 `tools/evidence-disposition.py:510-540` — `tree_entry(lane, "HEAD", path)` and the finding text names `HEAD:`.

That is the debt R17-JJ-GUARDS names. Pointing both at `refs/heads/<branch>` matches §1. It also matches the helper's own "in the branch tip commit" test (`jj-lane.sh:454-456`). On repo B, HEAD-based G2 accepts the live bytes (they equal `HEAD:a.txt`) and branch-based G2 raises `historical_input_uncommitted`. HEAD-based G3 accepts rev `4ae747a4…`; branch-based G3 rejects it. That is P08's open/closed split.

What matches, without stretching D:

- Local `refs/heads/<branch>`, not the remote. Landed/pushed stays `ahead=0` plus `ls-remote` (`closure-prompt.md:24-26`, `:54`; `PHASE2.md:101`). G2/G3 are "committed on the branch tip", which is the local ref. `JjAuditAudio.md:119` adds `refs/remotes/origin/main` for a landed citation. That extra check is a different invariant. D is right to leave it out.
- Schemas and the exit map stay put. Absent branch ref should be the existing could-not-evaluate exit 2, which is how `state` already refuses a non-40-hex ref (`jj-lane.sh:171-172`) rather than inventing a new exit.
- Tag-object and symlink-mode selftests are R17-GUARD-COVERAGE (`round-17-verifier-spotcheck.md:428-432`), carried in the same tool. G3's peel-must-equal-the-input is `evidence-disposition.py:443-448`. G5's mode set is `:544-555` (`100644`/`100755` only). They do not implement the jj rule and they do not falsify a HEAD read.

What does not match:

1. **Fixture command.** The only command D names leaves HEAD attached and equal to the tip (**[OBS]** repo A). The selftest then cannot fail on HEAD-based code. The divergence D asserts is a later `jj commit` of content with the bookmark left unmoved (repo B). `jj new` alone splits ids and not trees, so it falsifies G3 only when the rev is that empty HEAD commit, and it leaves G2 green for both implementations.
2. **Which resolver "resolved" means.** v2 order is `lane.branch`, then `detect_branch()` at `jj-lane.sh:113-126`, then unique `master` xor `main` (`:162-167`), then a 40-hex `refs/heads/$branch` or an error. The v1 ladder still described by siblings (§4) and still implemented by `tools/pin-disposition.py:324-371` (including "first local branch", and a raw-HEAD `commit` when no branch exists at `:379-381` and `:405`) is not that order. `symbolic-ref --short` on an attached `refs/jj/root` is the bug v2 closed (`JjAuditClosurePrompt.md:85-89`, `JjAuditInlineSh.md` F8: `branch=jj/root`, `refs/heads/master` absent, `ahead=0`). Copying pin-disposition into G2/G3 reopens P08 on the no-branch path.

`closure-prompt.md:14` and `:68` still say "lane HEAD". The value `inline.sh:146` writes is `lane_tip` (`local=`). The label is the old word; the bytes are the branch tip. Fleet-owned wording, not a second rule.

## 4. Stale sibling statements

Routed. Not edited.

| statement | why it is stale | owner |
|---|---|---|
| `kaidoku-shokunin/.ufo/waves/round-18/w1/ConnFleetJjPractice.md:103-106` | Calls `jj-lane.sh:53-65` the live `detect_branch` and lists master, main, and the first local branch. Those lines are `usage()`. The live function is `:113-126` and stops after `origin/HEAD`. | kaidoku |
| same file `:7-14` and `:86-90` | Says no sibling has migrated a live pin, that tameshi `pin-disposition.py:318` is still the tip read, and that `.ufo/waves/round-17/` is untracked. At `183f87b` the tip read is `refs/heads/<branch>^{commit}` (`pin-disposition.py:415`); `:392` reads `HEAD^{commit}` only to set `head_differs_from_branch`. The spot-check commit is that rev. Already named at `corpus/lessons/round-17-verifier-spotcheck.md:456-458`. | kaidoku |
| `.ufo/waves/hyaku/jj-w1/reports/JjAuditAudio.md:50` | "HEAD … may lag the branch" between `jj commit` and bookmark set. The same report's sandbox (`:109-114`) and repo B show the opposite direction: HEAD is the new commit, the branch ref is the old tip. | audio (historical audit) |
| `.ufo/waves/hyaku/jj-w1/reports/JjAuditKumitate.md:158` and `:198` | Prescribes the v1 ladder (`symbolic-ref --short` → `origin/HEAD` → master/main → first local branch) as the fix. v2 rejected that ladder. The diagnosis is still live: `kumitate-shokunin/scripts/round-gate.mjs:373` is still `merge-base --is-ancestor` against `HEAD`, and `:456` is still `@{u}..HEAD`. | kumitate |
| `.ufo/waves/hyaku/jj-w1/reports/JjAuditSouji.md:186` | Describes `jj-lane.sh:56` as `--short` plus a first-local-branch fallback, and treats a missing ref as non-load-bearing. v2 `state` exits 1 on a non-40-hex ref (`:171-172`). | souji / fleet |
| `.ufo/waves/hyaku/jj-w1/reports/JjTrialKaidoku.md:79` | "HEAD detaches after the first jj mutation … at the branch tip." Detach is true. Tip equality is the post-bookmark state (repo B's last step), not the post-commit window. | kaidoku |
| `.ufo/waves/hyaku/jj-w1/reports/JjTrialGameDev2d.md:122` | Calls `git rev-parse HEAD` in `run-reps.sh` safe under colocation. The agreed rule says that read is not the lane tip. | game-dev-2d |

In-lane, same trap, already routed as R17-CITATIONS: `tools/pin-disposition.py:43-46` and `:325-330` still cite `:53-65` and implement the v1 ladder plus the HEAD fallback. Do not copy it into `evidence-disposition.py`. The ER-jj2 line-anchor note is under `.ufo/waves/round-18/staged/` and is not on `183f87b`.

`JjAuditChousa.md:330-331` equates `@-` with the branch tip "in the measured post-commit state". That equality is repo B after `bookmark set`, not after `jj commit`. Treat the sentence as that measurement, not as the rule.

## 5. One move

Build the contract D selftest as repo B, and resolve the branch the way v2 `state` does.

After `jj git init --colocate`, change a tracked file, `jj commit` it, and assert before any `jj bookmark set`. G2 and G3 must use `refs/heads/<branch>`, with `<branch>` from `lane.branch`, else `detect_branch()` (`jj-lane.sh:113-126`), else unique `master` xor `main`. The tip must be 40 hex. A missing or non-hash ref is could-not-evaluate (exit 2), never `HEAD`. The HEAD-based mutant (today's `:450` and `:518`) fails that fixture: G2 accepts bytes that differ from the branch blob, and G3 accepts the unbookmarked commit. Keep the tag-object and symlink-mode cases; they do not replace this one.

## 6. Risks

1. A fixture that stops at colocate, or that bookmarks before the assert, has HEAD == tip (repo A; repo B last step; live tameshi). HEAD-based code passes. The selftest goes green without closing P08.
2. A `jj new`-only fixture splits commit ids and not trees. G2 stays green on the mutant.
3. Copying `pin-disposition.py`'s no-branch HEAD fallback, or the v1 `--short` ladder in §4, accepts an off-tip HEAD or a `refs/jj/root` name. That is P08 still open, with a new selftest that does not notice.
4. Running the fixture against the live lane, or cloning the live detached worktree (`JjAuditGameDev3d.md:149-155`), does not construct the window. The fixture has to be a fresh `/tmp` repo.
5. `git status` without `--no-optional-locks` rewrites a colocated index (`JjAuditGameDev3d.md:139-146`). G2/G3 as specified use `ls-tree` / `merge-base`, not `status`. Adding a status call to the fixture would mutate the index the test is reading.

## 7. Verification the L1 can run

1. Replay repo B in `/tmp` (commands in §2). Expect detached HEAD ≠ `refs/heads/master`, distinct `a.txt` blobs, `merge-base --is-ancestor HEAD refs/heads/master` rc=1, and equality only after `bookmark set`.
2. On the new selftest, the unpatched `183f87b` tool follows HEAD (P08 open). After the G2/G3 retarget, the same fixture is closed, and deleting the retarget makes the selftest fail.
3. A repo with no `refs/heads/*` and detached HEAD exits 2 and does not read `HEAD`.
4. `jj new` with no content change stays green for G2 under both the old and the new code. If a G2 assertion is attached to that shape, the assertion is wrong.
5. Tag-object and symlink-mode removals fail their own cases and are reported separately from P08.

Tool installs: none.
