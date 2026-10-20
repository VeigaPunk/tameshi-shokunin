# S06DetectBranchCites — R17-CITATIONS: `jj-lane.sh:<lines>` and `detect_branch`

Base: lane `183f87b899e6cae46be98d251cbc87fb5118f6ca` (master). Fleet helper read at fleet HEAD
`ae12f330697d09bcf7fa7df7552e1c48a6443950`; `git --no-optional-locks status --porcelain -- scripts/hyaku/jj-lane.sh` → empty.

## 1. Ground truth (measured, not inferred)

| Fact | Command | Result |
|---|---|---|
| `detect_branch` is at `:115` | `grep -n '^detect_branch' scripts/hyaku/jj-lane.sh` (live, and `git show <rev>:…` for `5d8a3b5b`, `14df5b9`, `ae12f33`) | `115:detect_branch() { # <dir>` at all four; body ends `}` at `:126` |
| It was at `:53-65` at fleet `67a3123` | `git show 67a3123:scripts/hyaku/jj-lane.sh \| grep -n '^detect_branch'` | `53:` — and `nl` shows `:53` = `detect_branch() {`, `:65` = `}` (exactly 13 lines) |
| The cited range is now usage text | `nl -ba scripts/hyaku/jj-lane.sh \| sed -n '50,66p'` | `:50` `usage() {`; `:53-56` the four CLI usage lines; `:57-60` exit/output help; `:61` `EOF`; `:62` `exit 64`; `:63` `}`; `:64` blank; `:65` `err() { echo "jj-lane: $*" >&2; }` |
| Helper blob shas | `git show <rev>:… \| sha256sum` | `67a3123` → `24790416…`; `5d8a3b5b`, `14df5b9`, `ae12f33` → `3369dc27b4909a9d1c2def774b128fb4a8cb71953ac9b12de4c8519b9024e421` |
| v2 narrowed the function | `sed -n '113,126p' scripts/hyaku/jj-lane.sh` | comment `:113-114` "Branch detection used ONLY by init…"; body = attached `HEAD` → `origin/HEAD` only, `return 1` otherwise. The v1 `master`/`main`/first-local ladder (present at `67a3123:59-64`) is gone |
| Operator route is `state` | `grep -n 'lane\.branch\|lane_branch_git' scripts/hyaku/jj-lane.sh` | `:100` reads `git config lane.branch`; `:439` `init` writes it; `:162` `cmd_state`: `lane_branch_git` first, then `detect_branch`, then a single `master`/`main` (`:163-168`) |

Behavioural proof (synthetic `/tmp` fixture: `git init`, one commit, `git branch -M master`, `git checkout --detach`, **no** `origin/HEAD`):

```
source <(sed -n '74,126p' scripts/hyaku/jj-lane.sh); detect_branch $FIX      -> out=[]      rc=1
source <(git show 67a3123:scripts/hyaku/jj-lane.sh \| sed -n '53,65p'); \
  detect_branch $FIX                                                        -> out=[master] rc=0
git config lane.branch master; lane_branch_git $FIX                         -> out=[master] rc=0
```

Live lane: `jj-lane.sh state /home/vgpnk/Projects/shokunin/tameshi-shokunin` → exit 0,
`state branch=master local=183f87b8… remote=183f87b8… ahead=0 behind=0 head=detached tracked=0 untracked=2`
(`origin/HEAD` is `refs/remotes/origin/master` here, so v2 `detect_branch` also returns `master`; the fixture is where it does not).

Consequence: the range anchor is stale at every site, **and** "`<branch>` per `detect_branch`" is no longer
self-sufficient in the exact state the notes describe (detached HEAD, no `origin/HEAD`): v2 returns nothing
there, while `state` resolves through `lane.branch` (measured above).

## 2. Every active citation (`SKILL.md`, `corpus/`, `tools/`)

`grep -rnE 'jj-lane\.sh:[0-9]+(-[0-9]+)?' SKILL.md corpus tools` → 6 lines; two further sites in
`tools/pin-disposition.py` carry the range on the line after the file name (`(:53-65)`). Full set = 8 sites:

| path:line | Cited text | What it now points at | Standing |
|---|---|---|---|
| `SKILL.md:1028-1029` | "`<branch>` per `detect_branch`, `../scripts/hyaku/jj-lane.sh:53-65`" | `usage()` text (`:53-63`) + blank + `err()` (`:65`); resolver at `:115-126` | stale anchor; `detect_branch` is now init-only and under-resolves in a detached no-`origin/HEAD` lane |
| `corpus/knowledge/verification-patterns-fleet.md:309` | "`detect_branch`, `../scripts/hyaku/jj-lane.sh:53-65`" | same | stale anchor; already staged as `ER-jj2` (B14), verified below |
| `corpus/knowledge/fleet-kill-rate-ledger.md:420` | same | same | same |
| `corpus/knowledge/service-limits.md:279` | same | same | same |
| `corpus/knowledge/incremental-pin-disposition.md:386` | same | same | same |
| `corpus/knowledge/operator-runbook.md:514` (ER-R3) | same | same | same (staged variant with the mechanism record) |
| `tools/pin-disposition.py:42-43` | "the way scripts/hyaku/jj-lane.sh / detect_branch does `(:53-65)`" | same | stale anchor + the described ladder is v1's, not v2's (this tool deliberately mirrors v1) |
| `tools/pin-disposition.py:325` | "Mirror scripts/hyaku/jj-lane.sh detect_branch `(:53-65)`, read-only." | same | stale anchor; mirror target is v1 `67a3123`, faithful to it |

Name-only `detect_branch` references (no line anchor, no correction): `SKILL.md:1028`;
`tools/pin-disposition.py:324` (def) and `:401` (call); `corpus/lessons/round-17.md:58`;
`corpus/lessons/round-17-verifier-spotcheck.md:446-447` (the round-17 routing record — its
"moved to line115 in fleet 5d8a3b5" is accurate; `:447` holds the `53–65` literal).

## 3. Historical citations — inventoried, **not** corrected

Records are append-only and are not re-interpreted, so none of these is edited.
`grep -rlE 'jj-lane\.sh:[0-9]+' .ufo/evidence/round-17` → **0 files** (no citation-form anchor in evidence).
The two `RR2` traces (`traces/RR2/7.json:6`, `15.json:6`) carry `sed -n "53,65p"` inside a recorded command,
i.e. receipt text, not a citation.

`.ufo/waves/round-17` — 23 sites in 11 files (each cited range → what that range is at the current helper):

| Sites | Range | Current content of that range |
|---|---|---|
| `W06RunbookJj.md:15,95` | `:50-52` | `usage() {` + `cat >&2 <<'EOF'` + `usage:` |
| `C01SiblingOverlap.md:78,120` | `:51-81` | `usage()` body through `cmd_state`'s comment |
| `C03JjMap.md:31` | `:53-69` | usage text, `err()`; no resolver |
| `C03JjMap.md:33` | `:152-160` | state section header + `cmd_state` head |
| `C03JjMap.md:34` | `:186` | `classify_push_error()` |
| `C03JjMap.md:78` | `:111` | `}` (end of `lane_id_jj`) |
| `C03JjMap.md:145` | `:200-216` | `push_preflight()` body |
| `C03JjMap.md:151` | `:183-184` | push-recovery comment |
| `JjAndMisroot.md:47` | `:532-534` | the `.ufo` / `.ufo/state` / `.ufo/watchdog.log` "driver runtime is never committed" case |
| `RerunPinBranch.md:93`, `HeadSweepRecheck.md:31`, `CR27.md:49,66`, `CR40.md:14,149`, `RR2.md:28,107,179` | `:53-65` | usage text (the drift these notes already describe) |
| `LessonCarryCheck.md:199` | `:518-521` | auto-track `"none()"` check in `cmd_commit` |
| `R09Skill1033.md:38,112` | `:53-65` | usage text |

Also historical: `.ufo/waves/round-17/staged/tools/pin-disposition.py:43,325` (staged copy of the round-17
tool, same stale anchor) and its untracked `__pycache__` file (not tracked at `183f87b8`:
`git ls-tree -r --name-only 183f87b8 | grep -c __pycache__` → 0).

## 4. Proposed correction wording (append-only; function by name, never lines)

### 4.1 Corpus — already staged by B14ErJjCorrections; independently verified

`head -c <base-bytes> <staged> | cmp - <(git show 183f87b8:<f>)` → identical for all five files
(base/staged bytes: ledger 40058/40636, incremental-pin 27034/27612, service-limits 22311/22889,
verification-patterns 40254/40832, runbook 32249/33515; line counts 420→422, 386→388, 279→281, 309→311, 514→516).
Each append is one blank line + one `ER-jj2`/`ER-R3` block, exact EOF append, nothing else changed.

Accuracy check of the staged text: it names `detect_branch()` and states the v2 ladder correctly
(attached HEAD → `origin/HEAD`), keeps the tip as `refs/heads/<branch>`, and scopes itself to the anchor.
Two optional precision notes for the L1 **before install** (after install it is append-only):
(1) `:53-65` is `usage()` (`:53-63`) plus `err()`'s line (`:65`), so "usage() help text" is close but not literal;
(2) the block does not state that `detect_branch` is init-scoped and returns nothing in a detached lane
without `origin/HEAD` (measured), nor that `state` resolves via `lane.branch`. Not defects for the
"correct only the anchor" scope — no rewrite proposed.

### 4.2 `SKILL.md:1029` — **not staged**; the B14 draft needs one addition

B14's drafted append names `detect_branch()` as the resolver. Measured, that function cannot resolve a
detached lane that has no `origin/HEAD` (rc 1, empty), which is exactly the state the reading rule addresses;
`state` still resolves it. Proposed append after the `current`/`stale`/`drift` table's reading-rule block
(`SKILL.md:1027-1035`), replacing B14's draft:

```markdown
**Round-18 anchor note (append-only).** The `../scripts/hyaku/jj-lane.sh:53-65` anchor in the reading rule
above is stale: that range is the `usage()` help text, not the branch resolver, and the fleet helper has moved
the function since. Cite the helper by function name, never by line: `<branch>` is read from
`../scripts/hyaku/jj-lane.sh state <repo>`, field `branch=` (`lane_branch_git` — git config `lane.branch`,
written by `init` — then `detect_branch`, then a single `master`/`main`); `detect_branch` alone is init-scoped
and returns nothing in a detached lane with no `origin/HEAD` (measured 2026-10-20). The tip is still
`refs/heads/<branch>`; the rule itself is unchanged.
```

(If the L1 prefers a pointer repair over an append: replace only the two-line parenthetical at `:1028-1029`
with "`<branch>` from `../scripts/hyaku/jj-lane.sh state <repo>` field `branch=` — functions cited by name,
never a line range"; the surrounding rule text is unchanged either way.)

### 4.3 `tools/pin-disposition.py` — in-place docstring repair (no code change)

Comment text only; the tool's ladder is a deliberate superset of v1 and its behaviour is unchanged.

Site A, `:42-43`:

```diff
-  head      the lane branch resolved the way scripts/hyaku/jj-lane.sh
-            detect_branch does (:53-65): an attached HEAD wins; a detached
+  head      the lane branch resolved the way scripts/hyaku/jj-lane.sh's
+            `detect_branch` did at fleet `67a3123` (cited by name; v2 moved it
+            and keeps only attached HEAD -> `origin/HEAD`): an attached HEAD wins; a detached
```

Site B, `:325`:

```diff
-    """Mirror scripts/hyaku/jj-lane.sh detect_branch (:53-65), read-only.
+    """Mirror scripts/hyaku/jj-lane.sh `detect_branch` (fleet `67a3123`), read-only.
```

The remaining paragraphs of that docstring already describe the v1 ladder (attached → `origin/HEAD` →
`master` → `main` → first local branch) and stay accurate for this tool.

## 5. Remaining unknowns / handoff

- L1 decision: append at `SKILL.md` (append-only, as drafted above) vs the in-place pointer repair; `SKILL.md`
  is not in the round-18 staged tree (`ls .ufo/waves/round-18/staged/SKILL.md` → not found), so this site is
  unclosed until the L1 installs something.
- `tools/pin-disposition.py` is likewise unstaged; the L1 installs the two docstring edits at a normal wave install.
- Fleet-owner note (out of lane write scope): `scripts/hyaku/jj-lane.sh:113` says detection is "used ONLY by
  init", but `:162` (`cmd_state`) also calls it; harmless because `lane_branch_git` runs first, but the comment
  and the call graph disagree.
- Not run (not this item's check): lane selftests, `mutate-and-run.sh`, registry checks. No tools installed.
- Scratch: `/tmp/tameshi-r18w1-S06DetectBranchCites-*` (fixture + cmp bases); no lane or sibling file edited.

Commands, exits: `grep` inventory → 0; `jj-lane.sh state` → 0; fixture `detect_branch` v2 → 1 (as measured),
v1 → 0; `lane_branch_git` → 0; `cmp` prefix checks → 0 (all five).

Verdict: built — all 8 active citation sites checked against fleet `ae12f33` (function at `:115-126`; `:53-65` is usage text), the four ER-jj `ER-jj2` appends verified prefix-identical, and correction wording proposed for the two un-staged sites (`SKILL.md:1029`, `tools/pin-disposition.py:42-43,325`).
