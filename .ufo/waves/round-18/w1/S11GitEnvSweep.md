# S11 — static sweep: GIT_* scrubbing at every subprocess/git call site

Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` · base rev `183f87b899e6cae46be98d251cbc87fb5118f6ca`
Scope: `tools/*.py`, `tools/*.sh`, `.ufo/evidence/round-1[3-8]/*.py` (plus registry-relevant subdirectory tools and an in-flight annex).
Method: static reading only; no canary was run (X09 owns that). The only execution was a throwaway `/tmp` git-semantics experiment to ground what the declared canary export triad actually measures (below).

Working-tree bytes equal the base rev for every tracked file in scope:

```
$ git -C <lane> diff --stat 183f87b8 -- tools .ufo/evidence/round-13 .ufo/evidence/round-14 .ufo/evidence/round-15 .ufo/evidence/round-16 .ufo/evidence/round-17 .ufo/evidence/round-18
(no output) ; exit 0
$ git -C <lane> status --porcelain -- <same paths>
?? .ufo/evidence/round-18/
?? tools/trace-inputs.py
exit 0
```

So the path:line citations below are valid at the base rev. The two `??` entries are wave-1 construction (contracts B/E/F), not base bytes; they are treated separately in the annex.

Registry rows that X09 will execute (12, all `status: active`):

```
$ git -C <lane> show 183f87b8:tools/registry.json | python3 -c '…kind=="selftest"…'
repeat-control-selftest | python3 tools/repeat-control.py --selftest
bash-witness-selftest | python3 tools/bash-witness-study.py selftest
pin-disposition-selftest | python3 tools/pin-disposition.py --selftest
witness-metadata-selftest | python3 tools/witness-metadata.py --selftest
evidence-disposition-selftest | python3 tools/evidence-disposition.py --selftest
context-capture-selftest | python3 tools/context-capture.py --selftest
mutate-and-run-selftest | bash tools/mutate-and-run.sh --selftest
measure-round16-selftest | python3 .ufo/evidence/round-16/measure.py --selftest
registry-check-selftest | python3 tools/registry-check.py --selftest
measure-round17-selftest | python3 .ufo/evidence/round-17/measure.py --selftest
trace-inputs-round17-selftest | python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest
assemble-round17-selftest | python3 .ufo/evidence/round-17/coldread/assemble.py --selftest
exit 0
```

Definition used for the `scrubbed` column: **yes** = the git child is given an environment with every `GIT_*` name removed (Python `{k:v for … if not k.startswith("GIT_")}` or shell `env -u` per live name); **no** = `env` omitted (inherits) or built from `os.environ` without filtering, even when it adds `GIT_CONFIG_*`; **n/a** = non-git subprocess, or recursive self-invocation whose child does its own scrub.

## A. `tools/` — every subprocess/git call site

| Tool | Call site | What runs | Scrubbed? | Reached by `--selftest` / registry row? |
|---|---|---|---|---|
| `tools/bash-witness-study.py` | :337 | `subprocess.run(["git","-C",kagi,"show",…])`, no `env=` | **no** (inherits GIT_*) | no — `cmd_selftest` :1218-1578 contains no subprocess/git |
| | :604 | `subprocess.run(argv, …, env=sweep_env())`; `sweep_env` :572-576 removes only `SCRUB_ENV` :116-117 (`THE_JANITOR_BIN`, `SQLITE3_BIN`, `CENSUS_BREAK`, `DEEP`, `ONEPASSWORD_BROWSER_SUPPORT`) | **no** (no GIT_* scrub) | no |
| `tools/context-capture.py` | :1647 | harness runs the CLI with `env=SELFTEST_ENV` (:1615-1618: fixed `{PATH, LC_ALL, GIT_DIR=/nonexistent/context-selftest-poison}`) | **yes** (replaces the environment; inherited GIT_* never reaches the child; the poison GIT_DIR is deliberate) | yes — but the CLI executes no git (`:10-12`, grep: only this subprocess call) |
| `tools/evidence-disposition.py` | :389 | `git_call` → `env=git_environment()` :380-383 filters every GIT_* + replace/graft/config overrides | **yes** | yes |
| | :1916 | `_git` → `env=_selftest_git_env()` :1900-1913 filters every GIT_* | **yes** | yes |
| | :1930 | `_git_raw` → `env=_selftest_git_env()` | **yes** | yes |
| | :2102 | `run_cli` runs this tool itself; `env=None` unless `env_extra`, and `env_extra` path is `dict(os.environ)` + extras (:2097-2101) | **no at spawn** | yes — child's own git calls all use `git_environment()` |
| | :2756 | usage-selftest runs this tool itself, no `env=` | **no at spawn** | child scrubs; usage paths do not reach git |
| `tools/pin-disposition.py` | :227 | `git()` → `env=git_env()` :207-220 filters every GIT_* | **yes** | yes |
| | :770 | selftest fixture git → `env` built at :751 from a GIT_*-free copy + identity | **yes** | yes |
| | :931 | `run_cli` runs this tool itself, no `env=` | **no at spawn** | child's git calls use `git_env()` |
| `tools/registry-check.py` | :368 | `run_row` Popen → `env=row_env()` :153-157 (= `git_env()` + `PYTHONDONTWRITEBYTECODE=1`) | **yes** | yes |
| | :411 | `rev-parse` → `env=git_env()` | **yes** | yes |
| | :451 | `git clone` → `env=git_env()` (:441) | **yes** | yes |
| | :465 / :476 | `checkout` and `rev-parse HEAD` → `env=env` (same scrubbed map) | **yes** | yes |
| | :602 | `run_child` (self) → `env=row_env()` + optional extras | **yes** (extras are the deliberate decoy only in the scrub tests) | yes |
| | :651 | selftest `git()` → `env=git_env()` + optional extras | **yes** | yes |
| | :743 | generated row script uses its inherited `env`; that env is the scrubbed `row_env()` from :368 | **yes** (by parent) | yes |
| `tools/repeat-control.py` | :281 | `run_once(command)` — arbitrary user command, no `env=` | **no** | yes (self-test) but no git anywhere in the tool |
| | :612 | `run_child` (self), no `env=` | **no at spawn** | no git |
| | :646 | `bash fixtures/stable.sh`, no `env=` | **no** | fixture uses no git |
| `tools/witness-metadata.py` | :1133 | selftest child `sys.executable -I …`, no `env=` | **no at spawn** | yes; tool contains no git invocation (grep `git` = 0) |
| `tools/mutate-and-run.sh` | :257-268 | `git_clean()`: enumerates every live `GIT_*` name and re-execs `env -u NAME … git` | **yes** | yes |
| | :278, :280, :282, :284, :286 | `fixture_commit` init/add/commit/rev-parse — all `git_clean` | **yes** | yes (its own canary arm :1724-1750 proves it) |
| | :1051, :1057, :1061, :1066, :1075 | `regression_case_git` toplevel/rev/cat-file/show/ls-tree — all `git_clean` | **yes** | `--regression` only |
| | :1643, :1675 | selftest pin reads — `git_clean` | **yes** | yes |
| | :1735-1737, :1742, :1745, :1747, :1749 | canary-arm probes — `git_clean` | **yes** | yes |
| | :302 | `python3 -` spec helper, env inherited | **n/a** (helper never calls git) | yes |
| | :443 | suite run `timeout … bash -c "$SUITE"`, env inherited | **no** | yes, but synthetic fixture suites call no git; the round-gate leg suite (:1278) uses `env -i` without GIT_DIR |
| | :1110, :1417, :1433, :1448, :1454, :1460, … | recursive `bash "$SELF"` invocations, env inherited | **no at spawn** | child re-scrubs every git call via `git_clean` |

Result for `tools/`: all **git** invocations scrub except `bash-witness-study.py:337` and `bash-witness-study.py:604`. Every non-git subprocess that inherits the environment is listed above; the only ones that can carry GIT_* into a git process are the unscrubbed bash-witness sites, the `mutate-and-run.sh` suite invocation (target-dependent), and recursive self-invocations whose child scrubs.

## B. `.ufo/evidence/round-13..17` top-level `*.py`

| Tool | Call site | Scrubbed? | Notes |
|---|---|---|---|
| `round-13/measure.py` | :14 `check_output(git rev-parse)`, :16 `git show` | **no** | read-only verbs; no writes, but an exported GIT_DIR redirects the reads |
| `round-13/producer-before.py` | :337 `git show` (no env), :604 runner via `sweep_env()` | **no / no** | same copy shape as bash-witness: `SCRUB_ENV` :116-117 has no GIT_*; site :337 has no env |
| `round-13/producer-oracle.py` | :19 `subprocess.run([python, bash-witness-study.py, selftest])`, no env | **no at spawn** | child selftest executes no git |
| `round-14/capture-context.py` | :192 `run_bounded(…, env)` | **yes** | `safe_env()` :184-187 filters every GIT_*; baseline run scrubbed; the injected run and positive control add `GIT_DIR=/nonexistent/tameshi-round14-poison` only (:161, :395-409) |
| `round-14/measure.py` | :16 `git show` | **no** | read-only |
| `round-15/measure.py` | :68 `git …` helper | **no** | read-only |
| `round-15/verify.py` | :149-152 `git()` env filter :148; :190 `run_command(…, env=env)` where `env=tool_env()` :369 and `tool_env` :280-284 filters every GIT_* | **yes / yes** | |
| `round-16/measure.py` | :79 `git()` helper, no env; :419 `run(…, env=env)` with `env=dict(os.environ, GIT_CONFIG_NOSYSTEM=1, identity…)` | **no / no** | `--selftest` reaches git through :419→:422 `git_in` and performs `init`/`add`/`commit` (:431-443); the helper at :79 is the only other subprocess creation (used by `blob`/`run_mode`) |
| `round-17/measure.py` | :140 `GIT_ENV` filter; :151-152 `git()` env=GIT_ENV; :871 `base_env` filter; :878-879 `run()` env=run_env; :1453-1454 env=GIT_ENV | **yes** | its :1385-1391 case injects `/nonexistent` GIT_DIR into a child and expects the child's scrub to neutralise it |

## C. Annex — registry-relevant subdirectory tools and wave-1 in-flight files

| Tool | Call site | Scrubbed? | Notes |
|---|---|---|---|
| `round-16/coldread/anchor-check.py` | :41-43 `git show`, no env | **no** | read-only; not a registry row |
| `round-16/coldread/assemble.py` | — | — | no subprocess/git (grep 0) |
| `round-16/attribution/reattribute.py` | — | — | no subprocess/git (grep 0) |
| `round-16/round-gate/survivor-probes/c1059-probe.sh` | :19, :34, :41, :63-81 | **no** | only `GIT_CONFIG_*`/identity exported at :57-60; inherited `GIT_DIR` would redirect the fixture writes |
| `round-17/jj/head-vs-branch.sh` | :74-78 unsets every live `GIT_*`; :83-85 re-exports only controlled config/identity | **yes** | explicit round-17 lesson scrub |
| `round-17/coldread/assemble.py` | :229-233, :277-282, :1016-1021 | **yes** | all `env=_git_env()` :217-224 |
| `round-17/coldread/trace-inputs.py` | :522 `git_run(argv, env)`; callers :529/:537/:544 pass `scrubbed_env()` from :617-618; :633 strace with that env; :746-758 fixture git with `fixture_env`; :565 strace capability probe (`subprocess.call`, no `env=`, runs `/usr/bin/true`, no git) | **yes** (git children); :565 inherits but is not git | :797-798 selftest passes inherited `run_env` to the tool under test; the tool scrubs internally, so no git child inherits |
| `tools/trace-inputs.py` (untracked, not at base) | same shape; :917-923 selftest asserts `GIT_DIR` is removed | **yes** | contract B promotion in flight; X09 at base will not see it |
| `.ufo/evidence/round-18/measure.py`, `coldread/assemble.py` (untracked) | `GIT_ENV`/`_git_env` filters | **yes** | contract F copies in flight |

## D. Comparison with X09GitEnvCanary's expected outcome (not run)

X09's declared harness (read read-only while in flight, `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/git-env-canary.py:222-236`) runs each selftest-row argv in a `/tmp` clone with:

```
GIT_DIR       = <canary>/.git
GIT_WORK_TREE = <canary>
GIT_INDEX_FILE= <canary>/.git/index
```

and fingerprints `<canary>/.git/HEAD`, `refs`, `index`, `objects` (:159-169). Its dispatch text predicts "tools/bash-witness-study.py and any other unscrubbed tool show up".

Static prediction per row:

| Row | Git reached? | Inherited GIT_*? | Predicted canary |
|---|---|---|---|
| repeat-control-selftest | no | no | clean |
| bash-witness-selftest | **no** (selftest contains no subprocess at all; the two unscrubbed sites are `declare/run/rerun`, not `selftest`) | — | **clean** |
| pin-disposition-selftest | yes | no | clean |
| witness-metadata-selftest | no | no | clean |
| evidence-disposition-selftest | yes | no | clean |
| context-capture-selftest | no | fixed env | clean |
| mutate-and-run-selftest | yes | no (`git_clean`) | clean |
| **measure-round16-selftest** | **yes** | **yes** (`os.environ` copy at :412) | **clean, but row exits ∉ {0}**: the fixture `add`/`commit` target the canary's own worktree, so `commit` is `nothing to commit` and the `assert` at :433-434 raises |
| registry-check-selftest | yes | no | clean |
| measure-round17-selftest | yes | no | clean |
| trace-inputs-round17-selftest | yes | no | clean |
| assemble-round17-selftest | yes | no | clean |

So the expected dynamic output is **12 × `CANARY <tool> clean`**, not the dispatch-expected `touched` for bash-witness. The one unscrubbed registry selftest that does reach git cannot move the canary under the exact export triad.

Grounding experiment (throwaway `/tmp`, no lane repo; commands and exit codes):

```
canary: git init + seed commit; export GIT_DIR=<canary>/.git GIT_WORK_TREE=<canary> GIT_INDEX_FILE=<canary>/.git/index
synrepo: write a.txt/b.txt (outside the canary worktree)
git -C synrepo init -q   -> init_rc=0
git -C synrepo add -A    -> add_rc=0
git -C synrepo commit -qm label -> commit_rc=1, stdout "On branch master|nothing to commit, working tree clean"
canary .git/HEAD file hash, refs tree hash, index hash, objects tree hash: HEAD_same=yes refs_same=yes index_same=yes objects_same=yes
```

Sensitivity check, same fixture but exporting **only** `GIT_DIR=<canary>/.git` (no `GIT_WORK_TREE`/`GIT_INDEX_FILE`):

```
init_rc=0 add_rc=0 commit_rc=0 head_moved=yes syn_git=no
```

That is the R17 incident shape: the fixture commit lands on the canary branch and moves its HEAD. `GIT_WORK_TREE`/`GIT_INDEX_FILE` pinned to the canary is what converts the unscrubbed `measure-round16` write path into a no-op against the measured facets. A `clean` verdict therefore does not evidence a scrub; conversely, an omitted or redirected `GIT_WORK_TREE` would make the same tool report `touched`.

## E. Facts, inference, unknowns

Observed (static + the `/tmp` experiment):
- `bash-witness-study.py:337` and `:604` are the only unscrubbed git sites in `tools/*`; `sweep_env()` scrubs five app variables and no GIT_*.
- `bash-witness-study.py --selftest`/`selftest` is hermetic parsing with no subprocess; contract E's two named sites are correct, but neither is exercised by the row X09 runs.
- `round-16/measure.py` is the only registry selftest that spawns git with inherited `GIT_*` (three sites, one path via `--selftest`).
- All other registry selftests either run no git or scrub every git child (`pin-disposition`, `evidence-disposition`, `registry-check`, `round-17 measure`, `round-17 trace-inputs`, `round-17 assemble`, `mutate-and-run` via `git_clean`).
- Historical evidence scripts 13-16 (`measure.py`; `producer-before.py`; `producer-oracle.py`; subdir `anchor-check.py`, `c1059-probe.sh`) remain unscrubbed; round-17's and round-14's are scrubbed.
- `git_clean` in `mutate-and-run.sh` derives the unset list from the live environment, so it covers every GIT_* name, not a fixed three.

[INFERENCE] Under X09's exact triad, `measure-round16-selftest` reaches `git commit` against the canary worktree where nothing changed, raising at `assert`; its row exit is therefore expected nonzero while the canary facets stay identical. I did not run that selftest or X09.

Unresolved/unknown:
- X09's in-flight file may change before it runs; predictions above use its current read-at-time logic.
- X09 may treat a nonzero row exit as `CANNOT-EVALUATE` rather than printing a `CANARY … clean` line; the row is the only failing row either way.
- The canary cannot see read-only redirection (13-16 `measure.py` `git show` under an inherited `GIT_DIR`) because it only fingerprints HEAD/refs/index/objects.
- The canary fingerprints `.git/config`, the worktree, and `index.lock` are excluded by the harness; a reinit/config rewrite is invisible.

Verdict: **partial** — the static sweep confirms contract E's `bash-witness-study.py:337/:604` exposure and finds one more registry selftest with inherited GIT_* (`round-16/measure.py:79/:419`), while all other registry selftests scrub; the declared X09 canary triad is predicted to report all 12 canary verdicts clean (measure-round16 only because `GIT_WORK_TREE` pins a no-op commit, with its row expected to exit nonzero), so the dynamic canary as specified cannot evidence the two real gaps.
