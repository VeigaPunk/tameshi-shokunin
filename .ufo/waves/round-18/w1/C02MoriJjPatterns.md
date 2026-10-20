# C02 — mori jj-colocated fixtures for tameshi P08

Axes: depth (a fixture that actually splits G2 and G3), calibration (branch naming and which ref is compared), operability monitored (sandbox isolation; unscored).

No tools installed.

## What mori builds

The divergence mori measures is a `jj commit` that does not move the bookmark. `jj git init --colocate` is only the setup step.

Sequence in `case_jj_commit_no_bookmark` (`mori-shokunin/tools/mori-round17-jj-regressions.py:617-630`):

1. Plain `git init -b master` plus one commit (`git_init` at `:210-215`, lane seed commit in `build_sandbox` at `:382-384`).
2. `jj git init --colocate <absolute repo>` run from the case directory, outside the repo (`jj_colocate` at `:267-274`).
3. Append bytes to a tracked file and `jj commit`. No `bookmark set`.
4. Expect `HEAD_BRANCH_MISMATCH` and no progress credit. The paired helper case (`:598-614`) is the same commit plus `bookmark set <branch> -r @-`, after which progress is credited.

Isolation that P08 should copy (`:26-36`, `:166-199`, `:249-255`): every git call is `git -C <sandbox>` with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset; `GIT_CEILING_DIRECTORIES` is the case parent; `HOME`, `XDG_*`, `JJ_CONFIG`, `GIT_CONFIG_GLOBAL` point inside the case; non-init jj calls are `jj -R <sandbox>` only after `<sandbox>/.jj` exists; no remote is created.

Recorded gate result, not just the script. `mori-shokunin/.ufo/waves/round-17/evidence/jj-after/run-manifest.json`:

- `jj-commit-no-bookmark` (`:851-970`) status match, lane `head=6e2e721c87818bd4e1b34eb0683a11f773c80092`, `branch=0cbec284382d2f8f147ee1aebd6ae7bb1885961c`.
- `jj-helper-commit` (`:749-840`) status match, lane `head=branch=db30f02fbd12b78dd2fb0c480ebc3d5b62d7d1cc`.

Production reading rule (`mori-shokunin/tools/mori-census.sh:2099-2104`, `:2175-2182`, `:2303-2309`; knowledge `corpus/knowledge/jj-branch-anchor-r17.md:9-19`): `jj commit` moves the working-copy parent, which is git HEAD, and the bookmark moves only in a later command. Rows 6 and 9 read `refs/heads/<branch>`. The name comes from an attached `symbolic-ref HEAD`, else `refs/remotes/origin/HEAD`, else the unique one of `refs/heads/master` and `refs/heads/main` (`lane_branch_probe` at `:2110-2138`). That third arm is `jj-lane.sh` `cmd_state` (`scripts/hyaku/jj-lane.sh:162-166`), not `detect_branch()` (`:115-126`), which returns failure after the origin arm.

`HEAD_BRANCH_MISMATCH` is only the failed ancestor test `merge-base --is-ancestor HEAD refs/heads/<branch>` (`mori-census.sh:2141-2171`; knowledge `:23-24`). Exit 0, including HEAD behind the tip (`case_git_detached_behind` at `mori-round17-jj-regressions.py:560-568`), emits no finding. Grading still uses the branch ref. If no name resolves, the census keeps literal `HEAD` (`:2181-2182`, `:2304-2309`; case `git-fallback-head` at `:679-691`). The knowledge note says that fallback is not a branch-identity proof (`jj-branch-anchor-r17.md:18-19`).

## Replay on jj 0.45.1

Scratch `/tmp/tameshi-r18w1-C02MoriJjPatterns-ZEKqlh` (removed from the lane; not a lane git write). `jj` `/home/vgpnk/.local/bin/jj` `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`. `git version 2.56.0`. Commands run with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_COMMON_DIR` unset. Operator `~/.config/jj` mtime stayed `2026-10-19 18:29:58` (stat only).

`python3 probe.py` exit 0. Same user config shape as mori (`name`/`email` only).

| step | symbolic-ref HEAD | git HEAD | refs/heads/master | trees | ancestry |
|---|---|---|---|---|---|
| after `git commit` | rc 0 `refs/heads/master` | `8bfe659a…` | `8bfe659a…` | equal | each is ancestor of the other |
| after `jj git init --colocate` rc 0 | rc 0, still attached | `8bfe659a…` | `8bfe659a…` | equal | same |
| after `jj commit` of `base\noff-bookmark\n`, no bookmark move, rc 0 | rc 1 | `19c34b9d…` | `8bfe659a…` | differ | HEAD ancestor of master rc 1; master ancestor of HEAD rc 0 |
| after second `jj commit` restoring `base\n`, rc 0 | rc 1 | `9a2104da…` | `8bfe659a…` | equal again | middle `19c34b9d…` ancestor of HEAD rc 0, of master rc 1 |
| after `bookmark set master -r @-`, rc 0 | rc 1 (still detached) | `9a2104da…` | `9a2104da…` | equal | aligned |

jj ids at the first diverging step: `@` = `2a86d8a9…` (empty), `@-` = `19c34b9d…` = git HEAD, bookmark still `8bfe659a…`. Git HEAD is `@-`, the working-copy parent. The empty `@` commit is not git HEAD. Live `tools/seed.txt` sha256 `3fe85c24056376b176725988bfdd5cdad987a3ab368ed34eff2eb85e07617592` matched `HEAD:tools/seed.txt` and differed from `refs/heads/master:tools/seed.txt` (`f34848ca…`, bytes `base\n`).

After the restoring commit, path bytes at git HEAD and at master were both `base\n` while the commit ids still differed. Middle blob stayed the off-bookmark bytes.

`jj bookmark set master -r <older>` without a flag: exit 1, `Refusing to move bookmark backwards or sideways: master`, refs unchanged. With `--allow-backwards`: exit 0, git HEAD stayed `9a2104da…` (`@-`), master moved to `8bfe659a…`, trees stayed equal.

At the detached step, `rev-parse --absolute-git-dir` was `<repo>/.git` (a directory), `--show-toplevel` was the repo, `--is-shallow-repository` was `false`. `symbolic-ref HEAD` rc 1, `symbolic-ref refs/remotes/origin/HEAD` rc 1, `show-ref --verify refs/heads/master` rc 0, `refs/heads/main` rc 1.

## Disagreement with the planned branch-tip resolution

Contract D's comparison target agrees with mori: G2 and G3 should read `refs/heads/<branch>`, and current tameshi code still reads HEAD (`tools/evidence-disposition.py:44-48`, `:441-454`, call order G3 then G1/G2 at `:1528-1532`). Three planned details do not survive this fixture.

1. Naming `<branch>` with `detect_branch()` alone fails here. The function (`scripts/hyaku/jj-lane.sh:115-126`) stops after attached HEAD and `origin/HEAD`. This fixture is detached and has no origin, so that function returns failure. Round-cache ER-jj2 (`tameshi-shokunin/.ufo/waves/round-18/staged/corpus/knowledge/fleet-kill-rate-ledger.md:422`) describes exactly those two arms. The name `master` comes from mori's third arm. `tools/pin-disposition.py:324-371` would also return `master` here, and then falls back to raw HEAD when no local branch exists (`:375-381`). Mori falls back to HEAD when master and main are missing or both exist (`mori-census.sh:2136-2138`). Contract D and `SKILL.md:1033` (unresolvable branch is SETUP rc 2) both refuse that fallback. Copying either fallback makes the verdict follow HEAD on the unresolved-name input, which is P08's open condition.

2. `jj git init --colocate` does not make git HEAD differ from the branch tip on jj 0.45.1. HEAD stays a symbolic ref to `refs/heads/master`. Inequality starts at `jj commit` without `bookmark set`. A plain `jj bookmark set` while `@-` stays is refused unless `--allow-backwards` is passed, and the move measured here kept the trees equal, so G2's path-byte check does not split.

3. Commit-id inequality is not a G2 split and is not a G3 split. G3 runs before G2 (`evidence-disposition.py:1528-1532`).
   - One content commit, historical rev = master, pin = master's blob, live bytes = git HEAD's blob: master is an ancestor of both, so G3 agrees. G2 against HEAD accepts (`live` equals `HEAD:path`, `:536-540`); G2 against the tip raises `historical_input_uncommitted`. [INFERENCE from those lines plus the measured blobs; evidence-disposition was not executed.]
   - Restoring the bytes in a second unbookmarked commit makes `HEAD^{tree}` equal the master tree, so G2 agrees. The middle commit is an ancestor of git HEAD and not of master, so G3 against HEAD accepts and G3 against the tip raises `historical_input_unavailable`. [INFERENCE, same limit.]
   - A selftest that only asserts `HEAD != refs/heads/master` stays green for a G3-reverted tool on the first shape, and stays green for a G2-reverted tool on the second shape.

Mori's ancestor finding is the wrong predicate for the comparison. In the first diverging step, master is an ancestor of HEAD and the mismatch still fires, because the tested direction is HEAD-ancestor-of-branch. Behind-HEAD (`case_git_detached_behind`) is silent and the census still reads the branch. G2/G3 have to use the tip on every input, including when that ancestor check exits 0.

## Proposed move

Build P08 as one /tmp colocated repo using mori's no-bookmark sequence and the unique master/main name (detached HEAD, no origin). Keep two historical revs in that repo:

- After the first content-changing `jj commit`, waive with rev = `refs/heads/master` and pin = that blob, live bytes equal to git HEAD. Closed means exit 2 `historical_input_uncommitted`. This fails HEAD-based G2.
- After a second `jj commit` that restores the path bytes, waive with rev = the middle commit. Closed means exit 2 `historical_input_unavailable`. This fails HEAD-based G3 while path bytes at HEAD and at master match.

Assert in the fixture, before running the tool: `symbolic-ref HEAD` rc 1, unique `refs/heads/master`, git HEAD equals `jj log -r @-`, git HEAD differs from `@`, and the two blob relations above. Do not treat colocate-only, a refused `bookmark set`, or mori's HEAD fallback as the closed condition.

## Risks

- The second commit is tree-equal to master, so a probe that only checks commit ids looks diverged and does not exercise G2.
- `--allow-backwards` can manufacture the same commit split with equal trees. It is not the failure window mori recorded.
- `pin-disposition.py`'s first-hit `master` then `main` then any other branch disagrees with mori's unique-or-unresolved rule when both `master` and `main` exist. Not exercised here.
- Mori's positive check that `HOME/.config/jj` exists (`mori-round17-jj-regressions.py:804-811`) was false on this jj when `JJ_CONFIG` is a file (`redirected jj config exists=False`). Hermeticity evidence is the unchanged operator mtime, not that directory.
- G4's non-shallow `<root>/.git` check matches this sandbox (`absolute-git-dir` and `shallow=false` measured). That does not show a full dispositions document exits 0 or 2.

## Verification

- Read mori gate, census probe, knowledge note, jj-lane `detect_branch` / `cmd_state`, tameshi `evidence-disposition.py` G2/G3 and call order, `pin-disposition.py` `detect_branch`, lesson §7 item 5 (`corpus/lessons/round-17-verifier-spotcheck.md:437-439`), staged ER-jj2.
- `python3 /tmp/tameshi-r18w1-C02MoriJjPatterns-ZEKqlh/probe.py` exit 0 (jj 0.45.1, git 2.56.0).
- Plain `bookmark set` backwards exit 1; `--allow-backwards` exit 0 with HEAD left on `@-`.
- Resolver and G4-shaped `rev-parse` probes exit 0 as tabulated above.
- evidence-disposition itself was not run. Exit-2 finding ids are [INFERENCE].

Verdict: partial — mori's unbookmarked `jj commit` is the P08 divergence; colocate-only, `detect_branch()` alone, and a bare commit-id check do not close G2 and G3.
