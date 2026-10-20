# S08HeadComparisons — bare-`HEAD` sweep of lane tools

Seat: TameshiR18.S08HeadComparisons (leaf, scout). Base rev: `183f87b899e6cae46be98d251cbc87fb5118f6ca`.
Scope: `tools/*` and the registered `.ufo/evidence/round-1[3-7]/*.py` entry points.
No tool installs. Scratch only under `/tmp/tameshi-r18w1-S08HeadComparisons-*`; the only lane write is this file.

## Method

- Exhaustive grep for the token `HEAD` over `tools/*.py tools/*.sh .ufo/evidence/round-1[3-7]/*.py .ufo/evidence/round-1[3-7]/*/*.py` and for the indirect forms (`rev-parse HEAD`, `HEAD^{commit}`, `HEAD^{tree}`, `merge-base --is-ancestor … HEAD`, `ls-tree HEAD`, `.git/HEAD`); every hit read in context.
- Registry coverage read from `tools/registry.json` and demonstrated by running one row under `strace -f -e trace=execve` in a `/tmp` fleet-mirror clone at the base rev.
- S061 behaviour reproduced in a `/tmp` `jj git init --colocate` fixture (writes only in `/tmp`), including a `tools/trace-inputs.py` receipt against the colocated tree.

## Live lane state (observed, 2026-10-20)

```
$ git -C <lane> symbolic-ref -q HEAD          # exit 1 -> detached (jj colocated, .jj present)
$ git -C <lane> rev-parse HEAD                # 183f87b899e6cae46be98d251cbc87fb5118f6ca
$ git -C <lane> for-each-ref refs/heads       # refs/heads/master 183f87b899e6…  (== HEAD at dispatch)
$ jj --ignore-working-copy log -r '@|@-|master' -T 'commit_id.short() ++ " " ++ bookmarks ++ " " ++ description.first_line()'
c25c2c061ecc            <- @  (working copy, no bookmark)
183f87b899e6 master    <- @- (git HEAD points here)
```

At dispatch `HEAD == master` because `@` is an empty working-copy commit on top of the tip. That equality is incidental: S061 (`corpus/lessons/round-17.md:35`, "Convince jj to update .git/HEAD to point to the working-copy commit's parent"; restated `w2/ReopenS061.md:37`) means git `HEAD` is `@-`, so as soon as a bookmark moves to `@` (or the lane sits on an unbookmarked working-copy commit), `HEAD != branch tip`.

## Findings

`should be tip` = under jj colocation should read `refs/heads/<branch>` (S061 / contract D), not bare `HEAD`.

| # | Site | Role of `HEAD` | should be tip | Registry row exercising it |
|---|------|----------------|---------------|----------------------------|
| 1 | `tools/evidence-disposition.py:450` | G3: `git merge-base --is-ancestor --end-of-options <rev> HEAD` | **yes** (contract D) | `evidence-disposition-round17` (active) and `-round17-before` (active); proven by strace below |
| 2 | `tools/evidence-disposition.py:518` | G2: `tree_entry(lane, "HEAD", path)` → `git ls-tree -z --full-tree HEAD -- <path>` (`tree_entry` at :461-471) | **yes** (contract D) | same two active rows; proven by strace |
| 3 | `tools/trace-inputs.py:537-538` (new wave-1 promotion; at first read byte-identical to `.ufo/evidence/round-17/coldread/trace-inputs.py:537-538`, sha256 `521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070`; a sibling edited it during this sweep — final check sha256 `fb1d81f67551fb04e9e447cbc706ef5cc9cfd5208169004184b24ab15f3f2636`, same HEAD read at `:537-538`, selftest rev assertion moved `:882 → :908`) | `repo_filter`: receipt `"rev"` = `git rev-parse --verify HEAD` of `--root` | **yes when `--root` is the lane** (today only latent: 0/780 round-17 receipts used the live lane; all rooted in `/tmp` clones). For live-lane traces the matching tree is jj `@`, not `HEAD` either — see fixture | `trace-inputs-round17-selftest` is `--selftest` only; its rev assertion runs on an attached-HEAD synthetic repo (`tools/trace-inputs.py:908` at final check). **No row exercises the production live-lane path** |
| 4 | `.ufo/evidence/round-17/coldread/assemble.py:946` | `resolve_expected_page`: last-resort `for rev in list(revs) + ["HEAD"]` (production caller :1860) | **yes**: the page is evidence for a report keyed by `read_rev`; the fallback must be the lane tip, not `@-` | `assemble-round17-selftest` is `--selftest` only; production fallback not row-exercised. Round-18 `assemble.py` inherits this per contract F |
| 5 | `tools/registry.json:427-436` (literal at :433) | Row `measure-round16-rev` (active, kind `probe`) runs `python3 .ufo/evidence/round-16/measure.py --rev HEAD --repo .` | **yes**: the row encodes lane state as bare `HEAD`; `measure.py` itself has no production `HEAD` read (only the selftest commit helper at `round-16/measure.py:435`) | this *is* the registry row; today `HEAD == master`, so benign; after a bookmark move it measures `@-` |

### Registry coverage, observed

```
W=$(mktemp -d …); fleet-mirror clone at 183f87b; cd clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  strace -f -e trace=execve -o exec.log python3 tools/evidence-disposition.py \
  --root . --dispositions .ufo/evidence/round-17/dispositions.json --json
exit=0   counts={'effective': 11, 'expected_checks': 12, 'failed': 0, 'findings': 0, 'passed': 11, 'superseded': 1}
```

strace of that single active row:

- 13 `execve` lines carrying `["git","-C",…,"merge-base","--is-ancestor","--end-of-options","4acc607dfd79f19d508bd50cdd06b772…","HEAD"]` — G3 (the 13 are the PATH-shim wrapper fan-out of the same calls: 13 `ls-tree` lines per waived path below, not 13 distinct checks).
- `["git","-C",…,"ls-tree","-z","--full-tree","HEAD","--","tools/mutate-and-run.sh"]` ×13 and the same for `["…","--","tools/pin-disposition.py"]` ×13 — G2, once per `historical_inputs` entry.
- 39 occurrences of the literal `"HEAD"` argv token in total; 0 `"HEAD:"` (G2 uses `ls-tree`, not `cat-file`).

`evidence-disposition-round17-before` uses `.ufo/evidence/round-17/dispositions-before.json`, which carries the same two `historical_inputs`, so it exercises G3+G2 too. `evidence-disposition-round14-superseded` (superseded) carries `historical_inputs: []`, so **that** row never reaches G2/G3.

Execution-context note: `registry-check.py --rev REV` runs rows with cwd in a `/tmp` clone detached at REV (`clone_lane_at_rev`, `tools/registry-check.py:427-487`), where `HEAD == REV`; the rows prove the code path is exercised, but the S061 harm needs a direct/live-lane run (or any run whose `HEAD` is jj's `@-`).

## Falsifier: jj colocation breaks G3 and G2 predicates

`/tmp` fixture (all writes in `/tmp`): `git init -b master`, one empty commit, `jj git init --colocate`, write `f.txt`, `jj describe`, then `jj bookmark set master -r @`.

```
HEAD before bookmark move : 11a7cfed354e69d8f4576ea12d10d588e0f3181b   (== @- == base)
@                         : 8ae494f6478425a2b6fe09e0ab0a0b9e0eaecfcc   ("wc change")
master after move         : 8ae494f6478425a2b6fe09e0ab0a0b9e0eaecfcc   (== @)
HEAD after move           : 11a7cfed354e69d8f4576ea12d10d588e0f3181b   (unchanged)
git merge-base --is-ancestor $(git rev-parse refs/heads/master) HEAD   -> exit 1
git merge-base --is-ancestor $(git rev-parse HEAD) $(git rev-parse refs/heads/master) -> exit 0
git ls-tree HEAD -- f.txt            -> (empty)
git ls-tree refs/heads/master -- f.txt -> 100644 blob b8f99f5b… f.txt
sha256(worktree f.txt) = 4c7a03f2… == sha256(master:f.txt)
```

Consequence for the two contracted sites — predicates observed, tool verdicts [INFERENCE]:

- G3 at `:450` would call the **current branch tip** `historical_input_unavailable` (the tip is `@`, a child of `HEAD`, so it is not an ancestor of `HEAD`).
- G2 at `:518` would call bytes that **are committed at the branch tip** `historical_input_uncommitted` (present at `master`, absent at `HEAD`).

The same fixture with `tools/trace-inputs.py`:

```
python3 tools/trace-inputs.py --root $J --out $J/receipt.json --cwd $J -- cat f.txt
exit=0
receipt rev      = 11a7cfed…            (git HEAD = @-)
receipt inputs   = {"f.txt": "4c7a03f2…"}
receipt untracked= {}
git ls-files --cached -- f.txt -> f.txt   (jj keeps the index at @)
```

So a live-lane receipt under colocation can record `rev` = a commit in which none of the recorded `inputs` exists: the docstring claim "tracked at HEAD (`ls-files --cached`)" (`tools/trace-inputs.py:19`) is index membership, and under colocation index = `@` while `HEAD` = `@-`. `assemble.load_trace_receipt` then requires a seat report's `read_rev` to equal that `HEAD` value (`assemble.py:456`, `trace-rev-mismatch`), pinning the report to `@-` rather than the lane tip. Round-17 practice sidesteps this (all 780 receipts root in `/tmp` clones, 16 distinct revs, 0 live-lane roots).

## Further instances to route (do not fix)

- **R1 — `tools/trace-inputs.py:537-538`** (and the round-17 copy it was promoted from, contract B): resolve the branch tip for lane roots instead of `HEAD`; if a live-lane trace is to remain supported, the rev that matches the bytes is jj `@`, which no current receipt field expresses. Selftest `trace-inputs.py:882` asserts `rev == head_sha` on an attached-HEAD fixture, so contract B's "byte-for-byte behaviour" needs an explicit L1 decision.
- **R2 — `.ufo/evidence/round-17/coldread/assemble.py:946`**: `+ ["HEAD"]` fallback; use the branch tip or fail with `page-not-at-read_rev` when the page is absent at every observed rev. Round-18 `assemble.py` inherits the line (contract F).
- **R3 — `tools/registry.json:433`**: repin `measure-round16-rev` to `refs/heads/master` or an exact 40-hex sha; the row currently passes only because `@-` happens to equal the bookmark tip.
- **R4 (caveat, no action)** — `tools/registry-check.py:477`: not lane state (it asserts the ephemeral clone's `--detach <sha>` checkout), so leave it. But callers that pass `--rev HEAD` resolve `@-` and clone at it; whether a clone materializes an unbookmarked `@-` is reachable-from-fetched-refs dependent, [INFERENCE], untested. No current row runs `registry-check --rev`.

## Covered, not instances (no change)

- `tools/pin-disposition.py:392` — raw `HEAD^{commit}` is used only to compute `head_differs_from_branch`; `commit` is the resolved `refs/heads/<branch>` tip (`:405-427`), exactly the S061 pattern. Registry row `pin-disposition-read` (active) exercises it; `head_differs_from_branch` is otherwise asserted only by the selftest (`:1310`).
- `tools/registry-check.py:656` `head_of()` — selftest canary only (`:710-711`, `:723`); `:413` `resolve_rev` resolves the caller's explicit rev.
- `tools/mutate-and-run.sh:286`, `:1742`, `:1745` — fixture commit helper and GIT_* canary selftest; production materializes pins through explicit revs (`:1051-1075`).
- `tools/context-capture.py:1447` — `rev-parse --git-dir` only; no HEAD read.
- `tools/bash-witness-study.py:338` — `git show <40-hex REV_BASH>:<path>`; rev comes from pins, never HEAD.
- `tools/witness-metadata.py`, `tools/repeat-control.py` — no git subprocess.
- Selftest-only HEAD reads (synthetic repos / expected values): `evidence-disposition.py:1937,2008,2019,2030`; `pin-disposition.py:808-835,1288-1292`; `registry-check.py:656`; `round-16/measure.py:435`; `round-17/measure.py:894,1379-1383` (the latter deliberately tests `--rev HEAD` on an attached fixture); `round-17/coldread/assemble.py:1078,1084,1519,1526,1547`; `round-17/coldread/trace-inputs.py:768` (and its `tools/trace-inputs.py` twin).
- Other registered entry points use explicit revs only: `round-15/verify.py` (`--rev` required at `:317`; rev resolve at `:163`), `round-15/measure.py:186` (`required=True`), `round-16/measure.py:640-643` (`--rev` required), `round-17/measure.py:1486-1487` (`--rev` required), `round-13/measure.py:14` (explicit rev), `round-14/capture-context.py:400` (`--git-dir`), `round-16/attribution/reattribute.py` and `round-16/coldread/assemble.py` (zero `git` references at all).

## Remaining unknowns

- Whether any round-18 seat will trace the live lane rather than a `/tmp` clone; round-17 evidence says no (0/780), so R1 is latent, not active.
- For live-lane traces, whether the L1 wants receipt `rev` = bookmark tip or jj `@`; the v1 receipt schema has one `rev` field and cannot express both.
- Clone materialization of an unbookmarked `@-` rev in `registry-check.py:477` (would need a contrived fixture to falsify).
- Rounds 13/14/15/16 non-registered scripts were checked opportunistically; none read bare HEAD.

## Verdict

G2/G3 confirmed as the only live-lane HEAD-state defects exercised by active rows, with three further instances routed (trace-inputs receipt `rev`, assemble HEAD fallback, registry row `measure-round16-rev`) and the rest either deliberate divergence detection or fixture/ephemeral HEAD reads — built.
