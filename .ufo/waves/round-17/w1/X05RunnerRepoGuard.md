# X05RunnerRepoGuard — repo-identity guard for mutate-and-run.sh (r17w1)

## Scope

Port `tools/pin-disposition.py` `repo_identity` (:235-265) into
`tools/mutate-and-run.sh` `regression_case` (git-materialization block, was
:996-1035) as a staged copy; refuse `git -C "$repo"` reads that would silently
climb to a super-repo; add refuse + accept selftest cases; keep legs 7/7/7.

Hazard evidence (read): `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditTameshi.md`
- §1.1 :43-46 — the four D-class `git -C "$repo"` reads (rev-parse :1000,
  cat-file :1004, show :1009, ls-tree :1018) have no repo-identity guard; a
  lane dir without `.git` resolves in the fleet super-repo.
- §2.2 :133-147 — observed: `git -C lane rev-parse --show-toplevel` returns the
  fleet root for a lane without `.git`; `pin-disposition.py` is the only
  guarded tool and is named "the model for the fix".
- §5 R1 :283-287 — "R1 — mutate-and-run.sh reads `git -C "$repo"` with no
  repo-identity guard … high blast radius: 7 ledger legs."

## Files changed

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-17/staged/tools/mutate-and-run.sh`
  (new staged copy; committed source `tools/mutate-and-run.sh` untouched).
  Diff vs committed rev 98bea7d: **+58/-0**, two hunks:
  1. `regression_case` git arm: after the `command -v git` probe, before the
     first rev-addressed read, a guard computing
     `repo_real=$(realpath "$repo")` and
     `repo_top=$(git -C "$repo" rev-parse --show-toplevel)`; unless
     `realpath "$repo_top" == "$repo_real"` it prints
     `REGRESSION_CASE <name>: SETUP (repo_identity_mismatch: …)` and returns
     2. Empty/failed resolutions fail closed into the same refusal. `realpath`
     (coreutils) is already on the tool's stated dependency list (:159).
  2. `selftest` r7-1 block: new fixture — git super-repo
     `$root/fleet2/super` with `target.sh` committed at **both** the repo root
     and `nogit/` (so `git show rev:target.sh` is satisfied root-relative and
     `git ls-tree rev -- target.sh`, which is CWD-relative, is satisfied at
     `nogit/target.sh`), plus a `nogit/` subdir with no `.git`. Two cases:
     - refuse-arm: `regression_case fixture-nogit … "$super/nogit" "$srev" target.sh 0 0`
       → exit 2, `repo_identity_mismatch` line present;
     - accept-arm: `regression_case fixture-ownrepo … "$grepo" "$grev" target.sh 0 0`
       → exit 0, exact-tolerance PASS line, no mismatch text.

## Evidence

- Baseline (committed rev, fleet-mirror clone
  `/tmp/tameshi-r17w1-X05RunnerRepoGuard-GW29Xt/fleet/tameshi-shokunin`):
  `bash tools/mutate-and-run.sh --selftest` → **83/83, VERDICT: PASS, exit 0**.
- Staged copy: `bash <staged> --selftest` → **88/88, VERDICT: PASS, exit 0**
  (`bash -n` clean). New cases all PASS:
  `no-.git dir inside super-repo refused (exit 2)`,
  `refusal names repo_identity_mismatch`, `a real repo passes (exit 0)`,
  `accepted leg ran at exact tolerance`, `accepted leg emits no mismatch line`.
- Guard-removed mutant (`/tmp/r17-mutant-noguard.sh`: staged minus lines
  1001-1015, the guard block only — selftest text retained):
  `--selftest` → **86/88, VERDICT: FAIL, exit 1**. The two failures are the
  refuse-arm cases; rg17.out shows the hazard live — unguarded, `fixture-nogit`
  materialized `target.sh` from the **super-repo's** object store and
  `REGRESSION_CASE fixture-nogit: PASS`. (First draft committed only
  `super/target.sh`; the mutant then died at `ls-tree`'s CWD-relative pathspec
  as an unrelated SETUP, still exit-2 — fixed by committing `nogit/target.sh`
  too, so the unguarded path now sweeps fully green, a sharper falsifier.)
- `bash <staged> --regression` from the fleet-mirror clone (staged file copied
  in; siblings symlinked, so lane dirs are symlinks — realpath equality is what
  admits them): **REGRESSION: PASS (cases=7 passed=7 …), exit 0**; zero
  `repo_identity_mismatch` lines. All seven legs PASS at exact tolerance.
- Command D (leg-count agreement, unchanged): staged selftest lines
  `PASS leg-count agreement: calls=7 specs=7 nlegs=7 (want 7)` and
  `PASS leg-count agreement: selftest leg tuples=7 (want 7)`; direct counts on
  the staged file: `grep -cE '^  regression_case_git (js|bash)-'` = 7, lent
  tuples = 7, `local nlegs=7`. Header legs block untouched.

## Behavior delta

Only the git-materialization arm of `regression_case` changes: `$repo` must
resolve via `git rev-parse --show-toplevel` to itself (realpath-equal), else
SETUP `repo_identity_mismatch` (exit 2). Fixture-mode calls (no repo arg) and
all sweep semantics are byte-identical. Deviation from the pin-disposition.py
port, deliberate: it also refuses symlinks / non-dirs / basename drift
(repo_symlink, repo_not_directory, repo_outside_root); here those all collapse
to the single stable reason `repo_identity_mismatch` per the assignment —
fail-closed in every case, coarser reason taxonomy.

## Risks / notes

- `realpath` used instead of `readlink -f`; identical semantics, already a
  stated tool dependency.
- Lanes that genuinely lack `.git` (jj-only) now SETUP instead of reading the
  super-repo — that is the intended repair; all four ledger lanes
  (kumitate, kagi, tsukuroi, mado) currently carry `.git`, verified.
- No installs; no `jj`/`git` writes in lane repos; scratch under
  `/tmp/tameshi-r17w1-X05RunnerRepoGuard-GW29Xt` and `/tmp/r17-*` only.

## Verdict

built — guard ported and falsifier-proven; staged file 88/88 selftest PASS, regression PASS cases=7, mutant 86/88 exit 1.

## Follow-up

### F1/F14 repair — GIT_* scrub (N01TraceGitSafety.md; R04ReviewContractB.md §0)

Root cause confirmed live: `GIT_DIR=<canary>/.git bash <committed 98bea7d
mutate-and-run.sh> --selftest` exits 0 with `MUTATE_SELFTEST: 83/83 pass` while the
canary's HEAD moves `c88131d → 8291985` and its status becomes
` D exec.sh / D noexec.sh / D target.sh` — the exact 12:29 lane signature
(N01 F1, R04 §0), reproduced safely against a `/tmp` canary, never the lane.

Staged changes (`staged/tools/mutate-and-run.sh`, sha256 `fb6d86d5…03001a`,
+146/−19 vs 98bea7d):

- `git_clean()` (:257) — every git call goes through
  `env -u <every GIT_* var in the live env> git …`. The unset list is derived from
  `env | sed -n 's/^\(GIT_[A-Za-z0-9_]*\)=.*/\1/p'`, so it scrubs *all* GIT_*
  names (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY,
  GIT_ALTERNATE_OBJECT_DIRECTORIES, GIT_COMMON_DIR, GIT_NAMESPACE, GIT_CONFIG_*,
  GIT_AUTHOR_*, GIT_TRACE*, …), not a hand-copied subset.
- `fixture_commit()` (:275) — the selftest's single fixture-history builder
  (init → add -A or named paths → commit → `rev-parse HEAD`), all through
  `git_clean`; the four inline fixture sequences (`grepo` :1586, `exec`
  :1642, `noexec` :1674, `super` :1701) now call it.
- `regression_case` (:1051-1075) — all five rev-addressed reads (`--show-toplevel`,
  `rev-parse --verify`, `cat-file -e`, `show`, `ls-tree`) now use `git_clean`;
  bare `git` survives only inside `git_clean` and the `command -v git` probes.

New selftest cases (7 assertions, :1724-1764):

- canary arm — base-committed canary repo, its `.git` exported as `GIT_DIR`, the
  exact `fixture_commit` step re-run on a fresh dir: fixture-commit succeeds,
  the fixture gets its own history, canary HEAD / refs / index+worktree unchanged.
- read side — because `--show-toplevel` alone does not catch a leaked `GIT_DIR`
  (observed: it still reports the `-C` worktree, so the r17 guard passes while
  reads land in the canary — N01 F14), the pinned rev exists only in `$grepo`;
  with the scrub the leg PASSes at exact tolerance, without it the read lands in
  the canary and refuses `revision not found` (SETUP 2).

### Commands and exits

| command (cwd) | exit | key output |
|---|---|---|
| `bash <staged> --selftest` | 0 | `MUTATE_SELFTEST: 95/95 pass`, `VERDICT: PASS`; 7 new PASS lines at :73-79 |
| `GIT_DIR=<canary>/.git bash <staged> --selftest` | 0 | `95/95 pass`; canary HEAD `401e6dab…` before **and** after, `status` empty → `CANARY-UNCHANGED` |
| `bash /tmp/r17-mutant-noscrub.sh --selftest` (faithful mutant: `git_clean(){ git "$@"; }`) | 1 | `89/95 pass`; exactly the 6 scrub assertions FAIL (:74-79); fixture dir has no `.git`, canary log gains `selftest-leak` on top of `selftest-canary` |
| `GIT_DIR=<canary3>/.git bash <mutant> --selftest` | 1 | `90/95 pass`; canary HEAD `cede1e8 → 87aa77c` (commits `selftest-canary`, `selftest-superrepo`) → `LEAK-REPRODUCED` |
| `GIT_DIR=<canary2>/.git bash /tmp/mar.sh --selftest` (committed bytes) | 0 | red-before: `83/83 pass` yet canary HEAD moves and status shows the fixture files |
| `bash <staged> --regression` in fleet-mirror clone | 0 | `REGRESSION: PASS (cases=7 passed=7; ledger legs exact…)`, 121.6 s |
| command D on staged | — | `PASS leg-count agreement: calls=7 specs=7 nlegs=7 (want 7)` and `selftest leg tuples=7 (want 7)` — 7/7/7 unchanged |

Lane hygiene: `git -C <lane> rev-parse HEAD` read-only before and after every run
is `98bea7d…`; no lane git write, no `jj`, no installs. Scratch in `/tmp` only
(`/tmp/tameshi-r17w1-X05RunnerRepoGuard-GW29Xt`, `/tmp/r17-*`,
`/tmp/tameshi-r4-2-selftest.*` from the deliberately-kept FAIL scratch).

Method note: the first mutant draft inserted `git "$@"; return 0` at the head of
`git_clean`, which also masked git's exit status and produced one collateral false
failure (`ledger leg missing revision named`). Rebuilt as a faithful
`git_clean(){ git "$@"; }` body replacement; the 89/95 result above is from that
faithful build.

Residual: `bash "$SELF"` sweep sub-invocations still inherit the caller's `GIT_*`
environment (sweep mode makes no git calls; the regression suite commands are the
caller's own). Scrubbing those too would change the documented suite contract.

Follow-up verdict: built — scrub ported with a canary falsifier and a read-side
falsifier; staged 95/95 exit 0 (also 95/95 under an external `GIT_DIR`), faithful
mutant 89/95 exit 1, regression PASS cases=7, legs 7/7/7.
