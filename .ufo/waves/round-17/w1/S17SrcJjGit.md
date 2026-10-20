# S17 — jj Git compatibility: HEAD vs the working-copy commit and the branch tip

Seat `TameshiR17.S17SrcJjGit`, wave 1, round 17. Question: how does Git `HEAD`
relate to jj's working-copy commit `@` / its parent `@-` in a colocated
workspace, and what does that teach this round's C2 jj fixes (branch tip, not
HEAD)? Source opened live 2026-10-20. No edits outside this report.

## 1. Source opened (live, 2026-10-20)

| URL | Result | Location used |
|---|---|---|
| `https://jj-vcs.github.io/jj/latest/git-compatibility/` | **301** → `http://docs.jj-vcs.dev/latest/git-compatibility/` | redirect record only; the canonical host is `docs.jj-vcs.dev` |
| `https://docs.jj-vcs.dev/latest/git-compatibility/` | 200, `text/html; charset=UTF-8` | §Colocated Jujutsu/Git workspaces; §Converting a workspace into a colocated workspace; §Supported features; §Branches; §Format mapping details |
| `https://docs.jj-vcs.dev/v0.46.0/git-compatibility/` | 200; same HEAD sentence byte-for-byte | version pin for the quotes |
| `https://docs.jj-vcs.dev/latest/working-copy/` | 200 | §Introduction (`@` is the working-copy commit), §Stale working copy (three steps; `@` per operation) |
| `https://docs.jj-vcs.dev/latest/git-comparison/` | 200 | §Overview: detached HEAD is "the normal state in Jujutsu"; "No current branch" |
| `https://docs.jj-vcs.dev/latest/bookmarks/` | 200 | §Introduction: "no concept of an active/current/checked-out bookmark"; bookmarks move manually or on rewrite |
| `https://docs.jj-vcs.dev/latest/github/` | 200 | §Working in a Git colocated workspaces: "Git will be in a detached HEAD state"; push `@-` because "the working-copy commit itself is empty" |
| `https://docs.jj-vcs.dev/latest/colocation/` and `.../latest/colocated/` | **404** | there is no separate colocation page; colocation is the §Colocated section of git-compatibility |

Version pin: `https://docs.jj-vcs.dev/versions.json` lists `v0.46.0` with
alias `latest` (prerelease and v0.45.1 … v0.41.0 also listed). The docs site
exposes no commit pin, so the row anchors on `v0.46.0`; the same sentence is
present at v0.32.0, v0.33.0, v0.36.0 and v0.46.0 (checked).

### Quotes (verbatim, located, ≤25 words)

**Primary (row anchor), 12 words** — §Converting a workspace into a colocated
workspace, final comment line of the `jj git colocation enable` manual recipe:

> Convince jj to update .git/HEAD to point to the working-copy commit's parent

**Supporting, 13 words** — §Colocated Jujutsu/Git workspaces, ¶2:

> `jj` commands will usually put the Git repo in a "detached HEAD" state

**Supporting, 20 words** — github page, §Working in a Git colocated workspaces:

> After doing `jj git init`, which colocates the `.jj` and `.git` directories, Git will be in a detached HEAD state

The first quote is the one that names the relation: `.git/HEAD` is set to the
**parent** of the working-copy commit, i.e. `@-`, not `@` and not a branch.
The second and third fix the state as detached. git-comparison adds that
detached HEAD is "the normal state in Jujutsu (there's actually no way -- yet,
at least -- to have an active branch/bookmark)", and bookmarks has "There is
currently no concept of an active/current/checked-out bookmark."

## 2. SOURCES.md row draft

Shape: `corpus/SOURCES.md` header (11 columns; cells contain no `|`). Id is
`S0xx` because the L1 assigns ids; the header at tip says "Next unused id:
S058", and no existing row covers jj (grep for `jujutsu|git compatibility|\bjj\b`
over `corpus/SOURCES.md`: none). Status is `queued`, not `mined`, until a
round-17 knowledge/lesson entry cites it; `used-by` is then filled with that
path (row rule: `mined` = cited by ≥1 path).

| S0xx | Git compatibility (Jujutsu docs) — https://docs.jj-vcs.dev/latest/git-compatibility/ | docs | A | colocated jj/git workspaces: what Git HEAD points at, detached HEAD, and why a Git-side revision read is not the branch tip | §Colocated Jujutsu/Git workspaces ¶2 and §Converting a workspace into a colocated workspace, recipe comment, at https://docs.jj-vcs.dev/v0.46.0/git-compatibility/ (alias latest; same sentence at v0.32.0-v0.46.0), fetched 2026-10-20 | in a colocated workspace jj leaves Git detached at the working-copy commit's parent (`@-`), so `git rev-parse HEAD` is neither `@` nor the bookmark tip; read the branch ref or pass an explicit revision | queued | 2026-10-20 | 180d | — |

Row mechanics checked on the extracted line (commands in §4): `awk -F'|'`
gives NF=13 (11 columns), and the id cell is the only `S0xx`.

## 3. What it teaches this round

1. **"Branch tip" must be a branch ref, never HEAD.** In a colocated
   workspace jj leaves `.git/HEAD` at `@-`. So for
   `tools/pin-disposition.py` (C2, item: replace the HEAD-based observation at
   :317-341) the only correct tip is `refs/heads/<branch>` (attached HEAD →
   its branch; detached → `refs/remotes/origin/HEAD`'s branch, else
   `refs/heads/master`, else `refs/heads/main`). HEAD belongs in an
   informational field (`head_differs_from_branch`) and must never stand in
   for the tip. The source also explains why this is structural, not a bug:
   jj has no "current bookmark", so Git's current branch has nothing to track.
2. **The live lane today is the coincidence case.** `HEAD == refs/heads/master
   == @- == 98bea7da…` while `@ == 890ac9e1…`. A field-by-field live
   comparison of old vs new `pin-disposition.py` therefore cannot demonstrate
   divergence (`head_differs_from_branch` is false right now); only the
   assignment's fixture — detached HEAD one commit ahead of master with
   different file bytes — exercises it. This is the same "sha-only agreement"
   class as M01/V03.
3. **Repo identity is a separate guard, and jj makes it sharper.** A
   non-repo path under the fleet root resolves to the fleet super-repo:
   `git -C /home/vgpnk/Projects/shokunin/reports rev-parse --show-toplevel` →
   `/home/vgpnk/Projects/shokunin`, HEAD `db3b5a8…`. So `mutate-and-run.sh`
   must prove `rev-parse --show-toplevel == realpath(repo)` before any
   `git -C "$repo"` read (the `repo_foreign` pattern already in
   `pin-disposition.py`). And in a jj-managed sibling, even a correct HEAD
   read yields `@-`, so pins must come from explicit 40-hex revs
   (`git show <rev>:<path>`), as the regression ledger already does.
4. **For C1's input rule**, the same lesson applies: `measure.py --rev REV`
   reads blobs at an explicit rev; if a seat or tool substitutes "current" or
   HEAD, the recorded sha256 can silently describe `@-` instead of the
   measured rev. Explicit rev in, blob digest out.
5. **A lesser consequence, recorded not relied on:** under jj, `git log -1`
   shows `@-`, so any "commits since X" count done through HEAD omits the
   working-copy commit (`@` here is empty — same tree as HEAD — but jj only
   guarantees that for a fresh working copy).

## 4. Observed evidence (commands, exits, key lines)

All lane reads are read-only; no `jj` command was executed (lane contract),
and no test was run.

| Observation | Command | Result |
|---|---|---|
| Lane is colocated | `ls -d .jj`; `cat .jj/repo/store/git_target` | `.jj` present; `../../../.git` |
| HEAD is detached | `cat .git/HEAD`; `git symbolic-ref -q HEAD; echo exit=$?` | raw sha `98bea7da5801f4bc58e4187690ee1687c8a5061f`; `exit=1`; `git rev-parse --abbrev-ref HEAD` = `HEAD` |
| Branch ref | `git rev-parse master`; `git for-each-ref refs/heads` | `98bea7da…`; `refs/heads/master 98bea7da…` |
| `@` is a child of HEAD | `git rev-list --all --parents \| awk '$2=="98bea7da…"'` | `890ac9e1e03d4742200930d4f7a41658365ecb8b 98bea7da…` |
| `@` is jj-kept and empty | `git cat-file -p 890ac9e1`; `git diff --quiet HEAD 890ac9e1; echo $?`; `git rev-parse HEAD^{tree} 890ac9e1^{tree}` | `parent 98bea7da…`, `change-id tpwwpz…`; `diff_exit=0`; both trees `4e9f7450…` |
| Tip came from jj | `git reflog show refs/heads/master` | `98bea7d refs/heads/master@{0} export from jj` |
| Colocation timing | `stat .jj .jj/repo/store .jj/working_copy` | `.jj` 2026-10-20 11:50:14; working_copy 12:06:03 |
| Round 16 saw the opposite state | `corpus/lessons/round-16-verifier-spotcheck.md:30` | hyaku `jj-lane.sh state` recorded `head=attached` at 11:48, i.e. before `.jj` existed at 11:50 |
| Fleet super-repo borrow | `git -C /home/vgpnk/Projects/shokunin/reports rev-parse --show-toplevel; … rev-parse HEAD` | `/home/vgpnk/Projects/shokunin`; `db3b5a8bd5e79353349b62a5fb155ea22cbf799e` |
| Redirect | `curl -sSI jj-vcs.github.io/jj/latest/git-compatibility/` | `301 redirect=http://docs.jj-vcs.dev/latest/git-compatibility/` |
| Version pin | `curl docs.jj-vcs.dev/versions.json` | `v0.46.0` with `"aliases": ["latest"]` |
| Quote word counts | `python3` `len(q.split())` | primary 12, supporting 13 |
| Row shape | `awk -F'\|'` on the extracted row | `NF=13` |

## 5. Inference and remaining unknowns

- **[OBSERVED]** `890ac9e1` has parent `98bea7da`, is in `refs/jj/keep`, and is
  tree-identical to HEAD. **[INFERENCE]** that this commit is `@` and
  `98bea7da` is `@-`; no `jj log` was run to print them. The graph relation
  plus jj's keep ref and the docs' description make this the only consistent
  reading.
- **[INFERENCE]** jj maintains `.git/HEAD` at `@-` across snapshots, not only
  at `jj git colocation enable`: supported by the recipe comment, the github
  page ("`jj commit` updates the HEAD of the Git repository"), and the live
  parent relation. Not verified for rewrite/conflict cases; the row's
  teaching does not depend on those.
- The docs expose no commit pin; the anchor names `v0.46.0` and records
  earlier versions where the sentence was checked. Page prose is served as
  `latest`, so `recheck 180d` is a cadence, not a guarantee.
- Not run, by contract: any `jj` invocation; any lane selftest or live gate.
  This seat answers the source question only.

## Tooling

No installs or upgrades.

**Verdict: built** — source opened live 2026-10-20 (v0.46.0), quote and
location recorded, row drafted in contract shape, and the teaching tied to the
lane's observed `HEAD == @-` state and the C2 branch-tip/identity fixes.
