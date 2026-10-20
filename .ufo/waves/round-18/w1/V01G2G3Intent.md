# V01G2G3Intent: why evidence-disposition G2/G3 compare with HEAD, and the branch-tip restatement

Seat: TameshiR18.V01G2G3Intent (revenger, round 18 wave 1).

- **Rev studied:** `183f87b899e6cae46be98d251cbc87fb5118f6ca`. `git show 183f87b:tools/evidence-disposition.py | sha256sum` gives `f8f05c7aa601…7e27`.
- **Lane writes:** this report only. Every lane read was read-only: `git show`, `rev-parse`, `log`, `reflog`, `grep`, `config --get`, `status --porcelain`, and `git clone` used as a source.
- **Scratch:** `/tmp/tameshi-r18w1-V01G2G3Intent-*`. Every git and jj write happened there. Every command ran with GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE and GIT_COMMON_DIR unset.
- **Lane state after the work:** HEAD = master = `93d22aa…`. `git status --porcelain --untracked-files=no` prints 0 lines.
- **Tools:** nothing installed or upgraded. I used the host's git 2.56.0, jj 0.45.1-7c41cdeb and python3, and curl for one documentation fetch.

## 1. Answer

- **Why HEAD.** HEAD stands in for "the lane's committed tip". The round-17 commission was branch-relative. The critic K03 rewrote it as HEAD while working in a plain-git clone, where HEAD equals the tip by construction. X01 then implemented K03's text literally. No test ever built a state where HEAD differs from the branch tip.
- **What G2 protects (I2).** A waived instrument's live bytes are exactly its bytes in the lane's committed state. Drift from the pin may come only from committed lane history.
- **What G3 protects (I3).** The declared rev is exactly a commit object, and it lies in the history of that same committed state. So `expected_inputs_historical` states true provenance.
- **The restatement.** Compute one anchor commit A per run and use it in both guards:
  - When a lane binding exists, A is `refs/heads/<lane.branch>`. The binding is the git config key `lane.branch` that `jj-lane.sh` writes; the attached branch is used if there is no binding. HEAD is never consulted.
  - In an unbound, detached, non-jj harness clone, A is the checked-out commit. That commit is admitted only if some branch or remote-tracking ref contains it.
- **Results.** With this restatement, ten fixture states take their intended outcome, and an eleventh (JB) gets the deliberate strict exit 2. The committed selftest still passes 56/56, and the landed round-17 manifests give unchanged results.
- **Falsified alternatives:**
  - "refs/heads/<branch> only", with pin-disposition branch detection: breaks registry-check `--rev` clones (D6, D7).
  - "branch tip, or HEAD if HEAD is on the branch": accepts a worktree older than the declared rev (JG).

## 2. Where "HEAD" came from

1. **The commission was branch-relative.**
   - `.ufo/waves/round-17/dispatch1.json:439` sets C2 as "registered entry commands return their registered outcome **at the branch tip**".
   - X01's task (`:449`) asks for "one 40-hex commit that is an **ancestor of master**".
   - K03's task (`:674`) asks "rev not an **ancestor of master**?".
2. **The critic restated it as HEAD.** K03HistoricalInputsTamper.md:
   - `:62`: "live bytes must equal `HEAD:<path>` (no working-tree drift)".
   - `:63`: "`git log --format=%H <rev>..HEAD -- <path>` must be non-empty".
   - `:64`: "separates 'instrument moved by a **lane commit**' from tampering".
   - `:67`: "`git merge-base --is-ancestor <rev> HEAD` must hold".
   - K03's lab (`:9`) was a "fleet-mirror clone at 98bea7d", which was the dispatch tip of branch master (`dispatch1.json:439`).
   - [INFERENCE] HEAD was a proxy for "master" there, because the two were equal in that clone. Neither k03.md nor x01.md contains any of jj, bookmark, detached, colocat, branch tip or refs/heads (grep: 0 matches).
3. **The builder implemented K03 literally.**
   - X01DispositionV2.md:108-115 compares against "`HEAD:<path>` (`ls-tree HEAD`…)" and runs "`merge-base --is-ancestor <rev> HEAD`".
   - The code at 183f87b does the same: `tools/evidence-disposition.py:441-455` (`… rev, "HEAD"`, "not an ancestor of HEAD") and `:518` (`tree_entry(lane, "HEAD", path)`).
   - The docstring repeats it at `:44-48`, and so does the usage text at `:178-180`.
   - K03's second G2 clause (`git log <rev>..HEAD`) was never implemented: the grep for `"log"|\.\.HEAD|rev-list` in the tool finds 0 matches. §3 shows that clause is implied, provided both guards share one anchor.
4. **No test could tell HEAD from the tip.**
   - Every fixture comes from `_git_init_commit`, which runs `git init -q` and then commits (`:1955-1957`). HEAD is therefore attached to the branch.
   - I re-ran the committed selftest under three re-anchored copies (§4.3). All four graders pass 56/56, so a HEAD→tip anchor mutation survives the suite.
5. **The divergence was flagged and routed, but not fixed.**
   - ReviewDispositionV2Code.md:174-176: "G2 pins `HEAD`, not `refs/heads/<branch>`… branch-tip-blind by construction".
   - The verifier spot-check, `corpus/lessons/round-17-verifier-spotcheck.md`:
     - `:37`: the verifier's own ancestry check used "the branch ref, never detached HEAD".
     - `:286-288`: "latent jj correctness debt. At this closure HEAD=master=30b0ca8".
     - `:437-439`: routes R17-JJ-GUARDS.
   - In the same round the lane moved pin-disposition from `HEAD^{commit}` to the branch tip, citing S061:
     - `corpus/lessons/round-17.md:58`.
     - `corpus/SOURCES.md:70`: "jj leaves Git detached at the working-copy commit's parent, so `git rev-parse HEAD` is not the bookmark tip".
     - The round-17 manifest's reason for `tools/pin-disposition.py`.
   - So round 17 fixed one tool and not this one.
6. **A HEAD-anchored acceptance was recorded without being recognised as off-branch.**
   - w2/RerunOP1.md:4-6 says "checkout detached at the landing rev", and `:86` records A4: "edit `tools/mutate-and-run.sh` and **commit** it (`d1005c9`) → 0 clean".
   - That commit sat on a detached HEAD in a clone, not on master. It was read as by-design ("live==HEAD", `:134-137`). DA4 in §4.2 reproduces this shape.
7. **Why it held at closure.** The live lane's `reflog refs/heads/master` and `reflog HEAD` move in lockstep. Every entry is "export from jj" (16:40:21, 16:22:36, 16:01:32, …). That is the helper's commit path: `jj commit` followed by `bookmark set <b> -r @-` (`scripts/hyaku/jj-lane.sh:596-659`, fleet `14df5b9`, file sha256 `3369dc27…e421`). In that steady state HEAD equals the bookmark.

## 3. What each guard protects

- **I2: G2, `historical_input_uncommitted`** (docstring `:44-46`; K03:61-64).
  - For each waived path P, the live state equals P's state in the lane's committed tree.
  - An uncommitted edit, a symlink, or an uncommitted deletion counts as tampering.
  - A committed deletion is allowed.
- **I3: G3, `historical_input_unavailable`** (`:47-48`; K03:65-67).
  - `rev^{commit}` resolves to exactly `rev`.
  - `rev` is an ancestor of the same committed state.
  - This excludes K03's false-provenance attacks: A1 (dangling commit), A2 (tree id), and off-branch commits.
- **Joint property.** Take anchor A and combine:
  - G1: live ≠ pin.
  - G2: live = A:P.
  - The pin check at `:1533-1544`: rev:P = pin.
  - G3: rev ≤ A.

  Then A:P ≠ rev:P with rev ≤ A, so the pin→live move lies in `rev..A`. That is exactly K03's dropped `git log` clause. **This requires G2 and G3 to use the same anchor.** JG shows a two-anchor rule breaking it.
- **Why HEAD is the wrong anchor under jj.**
  - In a jj colocated workspace, HEAD is jj's `@-`. The jj docs say "jj commands will usually put the Git repo in a 'detached HEAD' state" and give the recipe comment "Convince jj to update .git/HEAD to point to the working-copy commit's parent" (https://docs.jj-vcs.dev/latest/git-compatibility/, fetched 2026-10-20, html sha256 `db9c9a76…`; this is S061).
  - The lane's committed state is the bookmark. `jj-lane.sh:436-440` writes the binding, and `:454-456` says "git tracks it = present in the branch tip commit".
  - HEAD can lag the bookmark:
    - when the bookmark sits on `@`;
    - after the recovery path at `:283-341`, whose `reanchor_wc` leaves a non-empty `@` alone (`:262-275`).
  - HEAD can also run ahead of the bookmark or off it:
    - a seat's `jj commit` (`:581-583`);
    - a raw detached commit (spotcheck:57-70).

## 4. Behavioural evidence

### 4.1 Live lane and clone facts

| Command | Exit | Key output |
|---|---|---|
| `git -C $L rev-parse HEAD refs/heads/master` | 0 | `93d22aa…` / `93d22aa…`. Master moved past the dispatch tip; `183f87b..master` contains only `.ufo/evidence/round-18/*` |
| `git -C $L symbolic-ref -q HEAD` | 1 | detached (jj colocated; `$L/.jj` exists) |
| `git -C $L config --get lane.branch` | 0 | `master` |
| `git clone $L <tmp>`, then `config --get lane.branch` | 1 | the binding is **not cloned**. The clone gets `refs/heads/master=93d22aa`, `origin/HEAD→origin/master` |
| `clone-probe.sh` (jj source with HEAD lagging the bookmark, then `git clone`) | 0 | `clone symref HEAD=detached origin/HEAD=none`; the only ref is `refs/remotes/origin/master`. The clone has **no `refs/heads/master`** |

### 4.2 Fixture matrix

Commands:

```bash
cd /tmp/tameshi-r18w1-V01G2G3Intent-gJPdGU
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR python3 mkmodels.py   # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR python3 driver.py     # exit 0
```

The results are in `/tmp/tameshi-r18w1-V01G2G3Intent-fx-hvupndo6/results.json`.

How the fixtures were built:
- Lanes come from the tool's own `_build_lane`, `_rows` and `_dispositions_v2`, imported from the 183f87b bytes.
- jj fixtures run `jj git init --colocate` and then `git config lane.branch master`, mirroring `jj-lane.sh:439`.
- Clones use registry-check's own `clone_lane_at_rev` (`tools/registry-check.py:426-487`). It runs `git clone -q --no-hardlinks` and then `checkout -q --detach <sha>`. Only its mkdtemp prefix was redirected to my scratch.

The four graders:

| Grader | What it is |
|---|---|
| HEAD | the committed tool |
| T | anchor = `refs/heads/<B>`, with B taken from `lane.branch`, then the attached branch, then origin/HEAD, then master, main, or the first local branch (the pin-disposition / `jj-lane.sh cmd_state` order) |
| G | anchor = the tip, or HEAD when HEAD ≤ tip. With no binding, HEAD |
| R | the §5 restatement |

T, G and R are copies of the 183f87b tool that differ only in `resolve_historical_rev` and `check_historical_waiver`.

| State | Git facts | Intended | HEAD | T | G | R |
|---|---|---|---|---|---|---|
| P0: plain git, attached | HEAD = tip | 0 | 0 | 0 | 0 | 0 |
| J0: jj steady (`jj commit`, bookmark on `@-`) | HEAD = tip | 0 | 0 | 0 | 0 | 0 |
| JA: jj, bookmark on `@`, which holds the move | HEAD < tip | 0 | **2** `uncommitted` "live bytes differ from HEAD:tools/pinned-tool.py" | 0 | 0 | 0 |
| JB: jj, bookmark advanced past a stale worktree; the tip moved P again | HEAD < tip | policy (§6d) | 0 | 2 | 0 | 2 |
| JC: jj, seat `jj commit` parks an edit of P | HEAD ⊄ tip | 2 | **0** | 2 | 2 | 2 |
| JC3: jj, declared rev X on a side line reachable only from HEAD | X not on master | 2 | **0**, payload `{P: X}` (false provenance) | 2 `unavailable` | 2 | 2 |
| LI: jj, HEAD moved to a foreign fixture commit; worktree and bookmark untouched (round-17 incident shape) | HEAD ⊄ tip | 0 | **2** "live path is not present at HEAD" | 0 | 0 | 0 |
| JG: jj, stale worktree c0 < declared rev c1 ≤ tip c2 | HEAD < rev | 2 | 2 | 2 | **0** | 2 |
| D6: registry-check clone at REV; the source tip later moved P | clone master ≠ REV | 0 | 0 | **2** "differ from refs/heads/master" | 0 | 0 |
| D7: registry-check clone taken while the source HEAD lags its bookmark | no `refs/heads/*` in the clone | 0 | 0 | **2** "cannot determine the lane branch" | 0 | 0 |
| DA4: registry-check clone, then a detached commit edits P (RerunOP1 A4 shape) | HEAD unpublished | 2 | **0** | 2 | **0** | 2 "detached HEAD … is on no branch or remote-tracking branch" |

Wrong outcomes per grader:

| Grader | Wrong | States |
|---|---|---|
| HEAD | 5 | JA, JC, JC3, LI, DA4 |
| T | 2 | D6, D7 |
| G | 2 | JG, DA4 |
| R | 0 | JB is the deliberate strict choice |

The G3 divergence also shows directly at function level, in state JA with `resolve_historical_rev(lane, <branch tip>)`. HEAD raises "rev … is not an ancestor of HEAD"; T, G and R accept.

### 4.3 Selftest discrimination

The committed `selftest()` was run in-process for each grader, with only its mkdtemp prefix redirected to my scratch. Each one ends `SELFTEST: PASS (56/56)` with exit 0, 56 PASS lines and 0 FAIL lines:

| Grader | sha256 prefix |
|---|---|
| ed.py | `f8f05c7a…` |
| model_T.py | `0cf88635…` |
| model_G.py | `6d0adfdf…` |
| model_R.py | `1b5bd2ff…` |

Conclusion: none of the 56 cases constrains the anchor. The repair needs new cases.

### 4.4 Control on real data

Setup: a fleet-mirror clone at 183f87b, made with the contract recipe. Clone HEAD = `183f87b`. Clone `refs/heads/master` = `93d22aa`, which already differs from the graded rev today. `lane.branch` is unset in the clone.

Results for HEAD, T, G and R alike:

| Manifest | Exit | Status | Waivers |
|---|---|---|---|
| `.ufo/evidence/round-17/dispositions.json` | 0 | `clean` | `{tools/mutate-and-run.sh, tools/pin-disposition.py: 4acc607d…}` |
| `.ufo/evidence/round-17/dispositions-before.json` | 1 | `failed` with `expected_contains_missing` | same |

The clone's porcelain was empty afterwards. T passes here only because `183f87b..93d22aa` touched no waived tool.

## 5. Exact restatement (model R, as tested)

Compute one anchor A per run and use it in both guards. All git calls go through the existing `git_call`, which uses the G4 environment from `:361-383`. `git config --get` therefore reads only `<root>/.git/config`.

1. **Choose the branch B.** B := `git config --get lane.branch`. If that is empty and `git symbolic-ref -q HEAD` gives `refs/heads/X`, then B := X.
2. **Bound lane.** If B is set:
   - A := `git rev-parse --verify -q --end-of-options refs/heads/<B>^{commit}`, which must be 40-hex. Otherwise exit 2 with `historical_input_unavailable`.
   - HEAD is never read.
3. **jj workspace without a binding.** If B is unset and `<root>/.jj` exists: exit 2 with `historical_input_unavailable` ("jj workspace without a lane.branch binding has no authoritative tip").
4. **Harness clone.** If B is unset and there is no `.jj`, A := `HEAD^{commit}`.
   - This covers registry-check `--rev`, which checks out `--detach <sha>` and verifies HEAD == sha (`registry-check.py:465-486`).
   - A is admitted only if `git for-each-ref --contains A --format=%(refname) refs/heads/ refs/remotes/` lists at least one non-`*/HEAD` ref. Otherwise exit 2.

**G3′:**
- `rev-parse --verify --end-of-options <rev>^{commit}` must equal `rev` (unchanged).
- `git merge-base --is-ancestor --end-of-options <rev> A` must exit 0. Exit 1, or any other exit, gives `historical_input_unavailable` with "rev … is not an ancestor of <label> (<A>)".

**G2′:**
- `ls-tree -z --full-tree A -- <path>` replaces the HEAD lookup at `:518`.
- The same refusals apply. The detail names the anchor label, for example `live bytes differ from refs/heads/master:<path>`.
- A committed deletion is still allowed: the path is absent live and absent at A.
- Finding ids and exits are unchanged.

The anchor function as tested (`model_R.py:489`):

```python
def _v01_anchor(lane):
    branch = _v01_text(git_call(lane, ["config", "--get", "lane.branch"]))
    if not branch:
        ref = _v01_text(git_call(lane, ["symbolic-ref", "-q", "HEAD"]))
        if ref.startswith("refs/heads/"):
            branch = ref[len("refs/heads/"):]
    if branch:
        tip = _v01_commit_of(lane, "refs/heads/" + branch)   # rev-parse --verify -q --end-of-options X^{commit}
        if tip is None:
            raise CouldNotEvaluate("historical_input_unavailable", "lane branch refs/heads/{} does not resolve to a commit".format(branch))
        return "refs/heads/" + branch, tip
    if os.path.lexists(os.path.join(str(lane), ".jj")):
        raise CouldNotEvaluate("historical_input_unavailable", "jj workspace without a lane.branch binding has no authoritative tip")
    head = _v01_commit_of(lane, "HEAD")
    if head is None:
        raise CouldNotEvaluate("historical_input_unavailable", "HEAD does not resolve to a commit")
    proc = git_call(lane, ["for-each-ref", "--contains", head, "--format=%(refname)", "refs/heads/", "refs/remotes/"])
    if not [r for r in _v01_text(proc).splitlines() if r and not r.endswith("/HEAD")]:
        raise CouldNotEvaluate("historical_input_unavailable", "detached HEAD {} is on no branch or remote-tracking branch".format(head))
    return "HEAD", head
```

The docstring at `:44-48` and the usage text at `:178-180` need the same restatement.

## 6. Consequences for contract D, contract A P08 and the registry

a. **Contract D's literal wording needs a carve-out.** It says "compare against `refs/heads/<branch>`, never bare HEAD". Step 4 above is that carve-out for unbound detached clones. Without it, any branch detection that falls through to origin/HEAD, master or main anchors a `--rev` clone on the source lane's master at clone time:
   - **D6 shape:** grading a commit with `registry-check --rev` after a later commit moved a waived path gives a false exit 2. `tools/mutate-and-run.sh` is waived, and C1 moves it this round (leg 8).
   - **D7 shape:** while the live lane's HEAD ≠ master, a `registry-check --rev` clone has no branch at all, so every grade gives exit 2.

   Either way the `evidence-disposition-round18` row would fail the C2 no-harm monitor without any real regression.

b. **jj fixtures must write the binding.** The contract-D selftest and the P08 probe should run `git config lane.branch <b>` after `jj git init --colocate`, as `jj-lane.sh:439` does for every real lane. Otherwise R deliberately refuses (step 3). With the binding, P08 sees the following on the JA, JC and LI shapes:

   | Code | JA | JC | LI |
   |---|---|---|---|
   | HEAD-anchored (183f87b) | 2 | 0 | 2 |
   | Restated (R) | 0 | 2 | 0 |

c. **Cases that discriminate.**
   - Red on the 183f87b code: JA, JC, JC3, LI, DA4.
   - Guards against a branch-only regression: D6, D7. They are red on T.
   - Guard against a two-anchor regression: JG. It is red on G.
   - The existing 56 cases cannot carry this change (§4.3).

d. **JB is a policy choice.** R refuses with exit 2 and names the anchor; this fails safe. G would accept JB, but G also fails JG. I recommend R.

e. **Adjacent gap, not re-verified here.** G2 checks `type == blob` but not the mode (`:531`). ReviewDispositionV2Code.md:128-133 reproduced a symlink→regular pass. G2′ could require `TREE_MODES` (`:458`), as G5 already does (`:543-560`).

## 7. Confidence and limits

- **High confidence, behavioural:**
  - Under jj, HEAD diverges from the tip in both directions, and the HEAD-anchored guards mis-grade both ways (JA, JC, JC3, LI).
  - The clone hazard comes from registry-check's own clone function at 183f87b (D6, D7, DA4).
  - All of this was observed on jj 0.45.1.
- **Medium confidence:** JB's lag was produced by a git-side `update-ref refs/heads/master`, not by running `jj-lane.sh` recovery. [INFERENCE] The git-visible state is the same: HEAD lags, the worktree is stale, and the tool reads only git.
- **[INFERENCE]:** K03's motive (HEAD equal to master in its clone) rests on k03.md:9 and on zero jj/branch-tip terms in K03 and X01.
- **Not run:** the real `jj-lane.sh` recovery or push path; any lane registry row.
- **Scratch artifacts:** the models are analysis artifacts under `/tmp/tameshi-r18w1-V01G2G3Intent-gJPdGU`, not proposed patches. That directory also holds `mkmodels.py` `310a2f60…`, `driver.py` `d943d5fe…`, `clone-probe.sh` `b79606f8…` and the selftest logs `st-*.log`.

Verdict: holds. G2/G3 use HEAD only as an untested stand-in for the lane tip. Anchoring both guards on one commit — `refs/heads/<lane.branch>`, or the harness's published detached HEAD in an unbound non-jj clone — preserves I2 and I3 under jj. A literal "refs/heads/<branch> only" rule falls in registry-check `--rev` clones (D6, D7).
