# RerunRunnerGuard — mutate-and-run.sh rerun + external GIT_DIR canary (R17 wave 2, falsify)

Seat: `TameshiR17.RerunRunnerGuard-2`. Target: `tools/mutate-and-run.sh` at
`eb7838b16490ca7ba17ea3242ade76a61f744af2` (tool sha256
`fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a`; the runner
change itself entered at `2a22ade` — 165 changed lines, +146/-19; `eb7838b` only touches
`tools/evidence-disposition.py`). Clone: `/tmp/tameshi-r17w2-RerunRunnerGuard-u9btEL/fleet/tameshi-shokunin`,
fleet-mirror symlinks to the sibling repos, detached at the landing rev.

## A. `--selftest` — PASS 95/95, exit 0

```
cd $C && bash tools/mutate-and-run.sh --selftest
MUTATE_SELFTEST: 95/95 pass
VERDICT: PASS
EXIT=0
```
(computed count, not hardcoded: `tools/mutate-and-run.sh:1832`, `:1834`.)
Positive arms observed include `repo-identity guard: …` (5 PASS), `GIT_* scrub: …`
(7 PASS), `leg-count agreement: calls=7 specs=7 nlegs=7 (want 7)`, and all seven
`embedded leg <name>: spec and recorded table agree` PASS lines.

## B. `--regression` — PASS cases=7, exit 0

```
bash tools/mutate-and-run.sh --regression   # 183.5 s
REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact); …
REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)
EXIT=0
```
Every baseline row held exactly, 0 flips, `kill-rate` equal to the recorded value:
`js-kimi-census 10/10 … 8/10`, `bash-surface-census 8/10`, `bash-tsukuroi-census 6/10`,
`bash-mado-verify 4/10`, `bash-checklist-run 15/15 … 7/15`, `js-claims-check 7/10`,
`js-round-gate 5/10` (`REGRESSION_TABLE` lines; band/expect printed at
`tools/mutate-and-run.sh:1234-1236`, verdict at `:1303`). Pins materialized from each
sibling's object store at the recorded rev; the symlinked fleet-mirror paths were
accepted by the `realpath` guard (`tools/mutate-and-run.sh:1050-1055`).

## C. Command D (SCORECARD.md:73) — 7

```
REV=eb7838b16490ca7ba17ea3242ade76a61f744af2
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(…)); …'
recorded_cases=7 depth_score=7
EXIT=0
```
The seven matched lines are the ledger at `tools/mutate-and-run.sh:85-91`. Counting-rule
consistency check: the same command over the SCORECARD depth row's measured commit
`284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` yields `baseline_recorded_cases=6`, matching
`SCORECARD.md:66` depth 6; the r16 seventh leg accounts for 6 -> 7 at the landing rev.

## D. External canary: `GIT_DIR` exported while running the selftest from the clone

Canary repo base-committed in /tmp (1 commit), `.git` exported on the invocation:

```
GIT_DIR=$CANARY/.git bash tools/mutate-and-run.sh --selftest      # exit 0, 95/95, VERDICT: PASS
GIT_DIR=$CANARY/.git GIT_WORK_TREE=$CANARY GIT_INDEX_FILE=$CANARY/.git/index bash tools/mutate-and-run.sh --selftest
                                                                  # exit 0, 95/95, VERDICT: PASS
GIT_DIR=$CLONE/.git bash tools/mutate-and-run.sh --selftest       # exact R04 shape; exit 0, 95/95
```

Canary measurements before/after (prefix-only export, so the measuring shell is clean):
`head=82ecd263… / 82ecd263…`, `refs=refs/heads/master 82ecd263…` identical, `refcount=1`,
`index_sha=d2eeb8ce…` identical, `status=` empty, `commits=1` both sides — **HEAD did not
move**. Stronger probe on a second canary: the full `.git` tree digest
(`find . -type f | sha256sum`) was `f91c8e211a7b89b5f9972d945cfa57404b256e2761907108f32385b2925dd00b`
before and after the run (`GITDIR_IDENTICAL`). The clone itself in the R04 shape:
`HEAD` `eb7838b1…`/`eb7838b1…`, index `0a11608a…`/`0a11608a…`, status empty both sides.

## E. Read-side at full leg scale — regression under exported `GIT_DIR`

```
GIT_DIR=$CANARY/.git bash tools/mutate-and-run.sh --regression   # exit 0
REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)
```
Canary `.git` digest identical and canary HEAD `99f85fcc…` unchanged; all seven
materializations still read the pinned sibling blobs (pins and tables as in B). This is the
same code path as the selftest's `fixture-env-read` arm but at real-leg scale.

## F. Negative control (the canary probe is live, and the arms are not vacuous)

The clone's script was copied to /tmp and only the scrub dispatch was replaced by
`git "$@"` (one hunk, `git_clean` at `tools/mutate-and-run.sh:257-268`):

```
bash mutate-noscrub.sh --selftest  (no outer export)   -> 89/95, VERDICT: FAIL
  FAIL … canary HEAD unchanged / canary refs unchanged / canary index/worktree unchanged /
       fixture wrote its own history / rev-addressed reads … / env-independent read …
GIT_DIR=$CANARY2/.git bash mutate-noscrub.sh --selftest -> 90/95, VERDICT: FAIL
  canary2 HEAD 151153bf… -> 5870be10…, refs moved
  FAIL repo-identity guard … (2), fixture wrote its own history, rev-addressed reads … (2)
```
With the scrub removed the external canary HEAD/refs **do** move, and the selftest fails in
both invocation shapes; with the shipped code they do not. Note (honest mechanism): under
an outer-exported `GIT_DIR` the four internal canary arms compare through the same
redirected env (their reads go to the outer canary), so removal is caught there by the
fixture-history and rev-read arms; without the outer export all four canary arms fail. Either
way the gate reports FAIL, so the 95/95 green is not vacuous.

## G. Code review of the guard

- Every git *invocation* goes through `git_clean`; the only direct invocations are the two
  lines inside it (`tools/mutate-and-run.sh:264,266`). The remaining `git` tokens are
  `command -v git` presence checks (`:1038`, `:1216-1217`) and prose. The unset list is
  derived per call from `env` (`sed` at `:262`), so *all* `GIT_*` names are covered, not a
  hand list.
- Repo-identity guard (`:1043-1055`): refuses before any rev-addressed read when
  `realpath(repo) != realpath(--show-toplevel)`, and the selftest's refuse/accept arms
  (`:1686-1719`) prove both directions; the read-side arm (`:1751-1763`) proves a leaked
  `GIT_DIR` cannot reroute `git show`.
- Diff review (2a22ade): scrub applied to every materialization step, fixture history
  consolidated into `fixture_commit` (identity via `-c`, `commit.gpgsign=false`), no removal
  of the pin/restore checks; no behavioral regression seen.

## Findings (none blocking)

- minor/doc — `VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'`
  (`tools/mutate-and-run.sh:164`) is stale after r16/r17 and is unused (never printed; the
  provenance line uses the sha256 at `:484`). Dead metadata only.
- minor/doc — the `--selftest` description says "four fixture specs" (`:138-139`) while five
  are created (`:1378,1388,1395,1402,1644`), and the description (`:138-160`) does not name
  the r17 canary/repo-identity arms (they are documented inline at `:1686-1763`).
- residual risk — the scrub covers the tool's own git calls, not arbitrary `--suite`
  commands, which inherit the caller's environment (the suite contract exports only
  MUTANT/TARGET/PRISTINE/WORKDIR/DEFECT_ID); a caller-exported `GIT_DIR` could still steer a
  *suite's* own git use. No ledger suite runs git, so no current effect.
- residual risk — `git_clean` resolves `env`/`git` through PATH / shell function lookup; an
  adversarial caller could shadow them, out of scope of the R04 accident and of the claim.

## Verdict

**Holds** — attacked the wave-1 runner guard at the landing rev: selftest 95/95 (exit 0),
regression PASS cases=7 with every baseline row exact (exit 0), SCORECARD command D = 7,
and an external canary with `GIT_DIR` exported shows the canary HEAD/refs/index/.git tree
and the clone byte-identical before/after (also under the exact R04 shape and at full
regression scale); with the scrub removed the same probe moves the canary and the selftest
fails (89/95 or 90/95), so the guard is both effective and tested. No tool installs were
needed. Scratch only under `/tmp/tameshi-r17w2-RerunRunnerGuard-u9btEL`; no `jj`, no git
writes outside /tmp.
