# SelftestsNoHarmHead — no-harm selftest replay (verification-fixture craft)

## Verdict

**No harm to selftest operability.** At content revision `bb681566b18211adf8ae9c28df91e17678e3f545` and at base `9ed6db840dc97a0a5f4758b6b5f60cee83a61645`, every selftest I could execute exits identically, and the runner's own `--selftest` is green on both sides. The only behavioral delta is the intended one: `tools/mutate-and-run.sh --selftest` grows from **97/97 pass** to **106/106 pass** (exit 0 both), and the diff is additions only — the nine new PASS lines are the round-30 tally-harness cases. No pre-existing case turned red, disappeared, or changed order.

One cell is **not exercised** and one tool has no `--selftest` interface; both are documented below with causes. Two cells are nonzero on **both** revisions for environment reasons unrelated to the change (`mte-interop` without `jsonschema`, `round21-measure` without the five-lane fleet layout) and both go green at both revisions in the intended environment.

Seat: `SelftestsNoHarmHead`. Axis reviewed: operability. No judgment of C1, no promotion, no numeric-score claim.

## Scope and method

Executed read-only commands, all Git context variables unset (`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`), with `GIT_OPTIONAL_LOCKS=0` on the lane reads. Nothing was run inside `/home/vgpnk/Projects/shokunin/tameshi-shokunin` itself.

```sh
mkdir -p /fast/scratch/hyaku/noharm-wC/rev-base /fast/scratch/hyaku/noharm-wC/rev-target
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 \
  git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  rev-base/tameshi-shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 \
  git -C rev-base/tameshi-shokunin checkout -q --detach 9ed6db840dc97a0a5f4758b6b5f60cee83a61645
# rev-parse HEAD -> 9ed6db840dc97a0a5f4758b6b5f60cee83a61645

# same for rev-target/tameshi-shokunin, detached at
# bb681566b18211adf8ae9c28df91e17678e3f545
```

Each clone is named `tameshi-shokunin` inside a per-revision parent so that tools which resolve a sibling lane under the clone's parent (see `round21-measure` below) see a fleet-shaped layout. An earlier run in plain `base/` and `target/` directories produced the same results for every other tool.

Per revision, from the clone root:

```sh
timeout 600 bash tools/mutate-and-run.sh --selftest
for t in <each tools/*.py that accepts --selftest>; do
  timeout 600 python3 tools/$t.py --selftest
done
```

Environment: `python3 3.14.8`, `GNU bash 5.3.20(1)-release`, `uv 0.13.0`. `jj` exists at `/home/vgpnk/.local/bin/jj` and was **not invoked by this seat** (see the lane bound in Limits).

The set of `--selftest` acceptors was established from source, not assumed: of the 17 `tools/*.py` files, 16 parse `--selftest`; `tools/bash-witness-study.py` exposes a `selftest` **subcommand** instead (`tools/bash-witness-study.py:1750`) and rejects `--selftest` with exit 64 (`bash-witness-study.py: error: the following arguments are required: mode`). It is reported as a supplemental row.

## Table — literal commands

Base = `9ed6db840dc97a0a5f4758b6b5f60cee83a61645`; target = `bb681566b18211adf8ae9c28df91e17678e3f545`. "Summary line" is the tool's own selftest summary (the last non-empty line unless noted).

| Tool | base exit | target exit | base summary | target summary |
|---|---|---|---|---|
| `tools/mutate-and-run.sh --selftest` | 0 | 0 | `MUTATE_SELFTEST: 97/97 pass` + `VERDICT: PASS` | `MUTATE_SELFTEST: 106/106 pass` + `VERDICT: PASS` |
| `tools/command-binding.py` | 0 | 0 | `COMMAND_BINDING_SELFTEST: 44/44 pass` | same |
| `tools/context-capture.py` | 0 | 0 | `SELFTEST: PASS (49/49)` | same |
| `tools/env-diff.py` | 0 | 0 | `ENVDIFF_SELFTEST: 9/9 pass` | same |
| `tools/evidence-disposition.py` | not run | not run | lane bound forbids `jj`; selftest requires it (see Differences 4) | same |
| `tools/mte-interop.py` | 2 | 2 | `MTE_SELFTEST: SETUP (No module named 'jsonschema')` | same |
| `tools/pin-disposition.py` | 0 | 0 | `SELFTEST: PASS (19/19)` | same |
| `tools/receipt-measure.py` | 0 | 0 | `RECEIPT_MEASURE_SELFTEST: 10/10 pass` | same |
| `tools/receipt-window.py` | 0 | 0 | `RECEIPT_WINDOW_SELFTEST: 20/20 pass` | same |
| `tools/registry-check.py` | 0 | 0 | `SELFTEST: PASS (51 cases)` | same (timing floats differ, see Differences 2) |
| `tools/registry-replay.py` | 0 | 0 | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | same |
| `tools/repeat-control.py` | 0 | 0 | `SELFTEST: PASS (29 cases)` | same |
| `tools/round21-measure.py` | 1 | 1 | traceback: `git -C .../rev-base/kumitate-shokunin show 175de6ba...:scripts/kimi-census.mjs` → exit 128 (see Differences 3) | same, `rev-target` path |
| `tools/trace-inputs.py` | 0 | 0 | `SELFTEST: 30/30` | same |
| `tools/wave-accounting.py` | 0 | 0 | `FINDING: SELFTEST_PASS` | same |
| `tools/wave-route-mix.py` | 0 | 0 | `ROUTEMIX_SELFTEST: 8/8 pass` | same |
| `tools/witness-metadata.py` | 0 | 0 | `SELFTEST: PASS 39/39` | same |

Full logs: `/fast/scratch/hyaku/noharm-wC/logs2/{base,target}-<tool>.log`; runner logs `logs2/{base,target}-runner.log`.

## Supplemental cells (same commands, intended environment)

| Tool / invocation | base exit | target exit | summary |
|---|---|---|---|
| `python3 tools/round21-measure.py --selftest`, both clones given read-only sibling links to `kagi-`, `kumitate-`, `mado-`, `tsukuroi-shokunin` | 0 | 0 | `ROUND21_MEASURE_SELFTEST: 13/13 pass` |
| `timeout 600 uv run --no-project --with jsonschema==4.25.1 -- python3 tools/mte-interop.py --selftest` | 0 | 0 | `MTE_SELFTEST: 17/17 pass` |
| `timeout 600 python3 tools/bash-witness-study.py selftest` (no `--selftest` interface) | 0 | 0 | `WITNESS_SELFTEST: 51/51 pass` + `VERDICT: PASS`; logs byte-identical after normalizing the clone path |

## Differences and causes

### 1. `mutate-and-run.sh --selftest`: 97 → 106 cases, exit 0 on both

Observed diff of the two runner logs (`diff` after normalizing the clone path) is **additions only**, plus the summary line:

```text
94a95,103
> PASS tally harness: block extracted, leg status names=9 (want 9)
> PASS tally harness: all nine legs pass -> PASS passed=9, exit 0
> PASS tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (9/9)
> PASS tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (9/9)
> PASS tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
> PASS tally harness: statuses 2 2 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
> PASS tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
> PASS tally harness: statuses 3 0 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
> PASS tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2
98c107
< MUTATE_SELFTEST: 97/97 pass
---
> MUTATE_SELFTEST: 106/106 pass
```

Both logs contain 0 `FAIL` lines (base 97 `PASS`, target 106 `PASS`).

Cause: the round-30 block added at `tools/mutate-and-run.sh:1989-2040` extracts `run_regression`'s tally block out of the file (:1994) and runs it under fixed leg statuses through `tally_line`; `:2038-2039` drops one operand from the loop and asserts the new completeness guard refuses. That is 24 `tally_line` assertions — 23 vectors (1 all-pass, 9 single-FAIL positions, 9 single-SETUP positions, 4 mixed/unknown vectors) plus 1 guard stress — surfaced as 9 `st` cases. The commit message names "23 vectors + guard stress"; the observed 24 invocations match. The guard itself is the 9-line addition at `tools/mutate-and-run.sh:1453-1461` (`REGRESSION: SETUP (case-tally mismatch: cases=... counted=...)`). Hunk headers in the revision diff: `@@ -1448,6 +1450,15 @@` and `@@ -1975,6 +1986,59 @@`. This is the intended change; it adds coverage and removes nothing.

### 2. `registry-check.py`: timing floats only

The only log difference after path normalization is in two already-PASS lines:

```text
-SELFTEST_CASE timeout-kills-setsid-pipe PASS (exit=1 elapsed=1.426s survivor=False marker=False)
-SELFTEST_CASE timeout-kills-setpgid-pipe PASS (exit=1 elapsed=1.402s survivor=False marker=False)
+SELFTEST_CASE timeout-kills-setsid-pipe PASS (exit=1 elapsed=1.391s survivor=False marker=False)
+SELFTEST_CASE timeout-kills-setpgid-pipe PASS (exit=1 elapsed=1.417s survivor=False marker=False)
```

All 51 cases pass at both revisions, exit 0 both. Cause: wall-clock nondeterminism in the timeout cases, not revision content. Recorded as a named difference because the bytes differ; no behavioral consequence.

### 3. `round21-measure.py` in a bare clone layout: exit 1 at both

Bare layout (clone plus no siblings) fails at both revisions, identically:

```text
subprocess.CalledProcessError: Command '['git', '-C', '/fast/scratch/hyaku/noharm-wC/rev-base/kumitate-shokunin', 'show', '175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs']' returned non-zero exit status 128.
```

Cause: `tools/round21-measure.py:74` resolves each pinned surface blob as `str(ROOT.parent / surface["repo"])`; the round-21 contract's surfaces span five lanes (`kagi-shokunin`, `kumitate-shokunin`, `mado-shokunin`, `tameshi-shokunin`, `tsukuroi-shokunin`), while a bare clone has only `tameshi-shokunin` beside it. With read-only symlinks to the four other lane repos in the per-revision parent, both revisions pass `13/13` (supplemental table). Cause is layout, not the change.

### 4. `evidence-disposition.py --selftest`: not executed (lane bound)

The selftest requires `jj` for its isolated colocated-repository cases: `tools/evidence-disposition.py:121` ("Selftest also requires `jj` for its isolated colocated-repository cases") and the child invocation at `tools/evidence-disposition.py:2041` (`["jj"] + list(argv)`). This seat's lane bound says: never run ANY `jj` command anywhere. I therefore did not run this selftest. `tools/evidence-disposition.py` is byte-identical at both revisions (identity evidence below), so it cannot produce a base/target difference; that is `[INFERENCE]` from file identity, not an executed result. The parent can fill this cell from a seat not under the `jj` ban.

### 5. `bash-witness-study.py`: no `--selftest` interface

`python3 tools/bash-witness-study.py --selftest` exits 64 with `bash-witness-study.py: error: the following arguments are required: mode`; the tool's selftest is the `selftest` subcommand (`tools/bash-witness-study.py:1750`). Run in that form it passes 51/51 at both revisions with byte-identical logs after path normalization (supplemental table). This is an interface mismatch in the task wording, not a difference between revisions.

### 6. Everything else: no difference

For all 15 executed `--selftest` Python tools, base and target exit codes match and the logs are byte-identical after normalizing the clone path (the `registry-check` timing floats in item 2 are the sole exception). No unnecessary work was manufactured: all 17 `tools/*.py` are byte-identical across the two revisions, so a behavioral difference could only have come from repository content or environment, and none appeared.

## Identity evidence for the comparison

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat \
  9ed6db840dc97a0a5f4758b6b5f60cee83a61645 \
  bb681566b18211adf8ae9c28df91e17678e3f545 -- tools/
```

Observed:

```text
 tools/mutate-and-run.sh | 66 ++++++++++++++++++++++++++++++++++++++++++++++++-
 1 file changed, 65 insertions(+), 1 deletion(-)
```

Path-keyed sha256 comparison of every Python tool across the two clones:

```sh
for r in rev-base rev-target; do
  (cd /fast/scratch/hyaku/noharm-wC/$r/tameshi-shokunin && \
   sha256sum tools/*.py | awk '{print $2, $1}' | sort) > /tmp/h-$r.txt
done
join /tmp/h-rev-base.txt /tmp/h-rev-target.txt | \
  awk '$2!=$3{print "DIFF",$0} END{print "compared",NR}'
```

Observed: `compared 17`, with no `DIFF` line. The runner itself differs, as expected:

```text
fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de  rev-base/.../tools/mutate-and-run.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  rev-target/.../tools/mutate-and-run.sh
```

Both clones reported zero entries from `git status --porcelain` after all runs.

## Why this is an operability no-harm result

- Both revisions: runner `--selftest` exit 0; every executed Python selftest exit 0 except two environment cells that are nonzero and identical on both sides.
- The only semantic change in selftest output is the addition of 9 PASS cases exercising the new `--regression` tally guard; no existing case regressed.
- The nine real regression legs were **not** replayed (`--selftest` does not run them); this report makes no claim about `--regression` kill rates or universal behavioral equivalence.

## Limits and risks

- `evidence-disposition.py --selftest` is unexercised here because of the `jj` lane bound; file identity is the only basis for saying it cannot differ across revisions.
- `mte-interop` and `round21-measure` are nonzero under the literal command in this host/layout (missing system `jsonschema`; missing sibling lanes). These are pre-existing environment properties present at both revisions, not regressions, and both go green in the intended environment.
- The `registry-check` elapsed-time floats show that two PASS lines are not byte-stable run to run; do not use those lines as byte-identity evidence.
- Scratch evidence is ephemeral: `/fast/scratch/hyaku/noharm-wC/` (two clones, `logs2/`). Nothing was committed.

## Smallest safe correction

None to production bytes — the no-harm verdict needs no edit. If the L1 wants every cell green or exercised under the literal command set, the smallest additions are environmental, not code: (a) run `evidence-disposition.py --selftest` from a seat outside the `jj` ban; (b) make `jsonschema` importable by the `python3` that runs `mte-interop.py` (or accept the documented `SETUP`); (c) run `round21-measure.py --selftest` in a fleet root holding the other four lane checkouts (the supplemental run shows 13/13 at both revisions).

## Compliance and cleanup

- Wrote only this report under the lane; no production file edited; no Git write in the lane or fleet; no `jj` command run anywhere; no seat spawned; no model passed.
- All runs were synchronous inside `/fast/scratch/hyaku/noharm-wC`; no process or service started by this seat remains. Other `mutate-and-run.sh` processes visible during the run belong to other seats' cold-read harnesses (`/tmp/Cold*`) and were not touched.
- Tools installed or updated: none. `uv run --no-project --with jsonschema==4.25.1` used an ephemeral environment (uv 0.13.0, package `jsonschema 4.25.1` acquired into the uv cache) solely to exercise `mte-interop.py --selftest`; no host package was installed or upgraded.
