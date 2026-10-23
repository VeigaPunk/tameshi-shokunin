# CONTROL CtlK2Junk (round 30, C1 pre-data control K2 "junk")

CONTROL CtlK2Junk: meets=false C1_R30_PASS=false

- C1_R30 summary line: `C1_R30: rev=71fe7f08e0316df18e9817bdafa2a00e897331c3 pristine_selftest=0 harness=19/19 refused_drops=0/9 killed=13/13 equiv_pass=0/4 heldout_killed=12/12 heldout_equiv=0/4`
- `PREDICATE: C1_R30_PASS=false`
- exit code: **1** (predicate false; no counter error — exit 2 was not reached)
- counter: `python3 .ufo/evidence/round-30/c1-measure-v2.py --repo CLONE --rev 71fe7f08e0316df18e9817bdafa2a00e897331c3`
  - counter file sha256 verified unchanged before the run: `5ed4e663ff16556d0bfef68a9fc1e3cf820ab8bc2b620169e800da914f0c8719` (matches contract-amendment-1.json).
- sandbox: `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK2Junk/clone`, detached at lane tip `e59728df5ebb053c9810049c05fd4e9d59d82dee`, control committed as `71fe7f08e0316df18e9817bdafa2a00e897331c3`.
- evidence: `.ufo/evidence/round-30/ctl/CtlK2Junk.diff`, `.ufo/evidence/round-30/ctl/CtlK2Junk.stdout` (counter stdout + final `exit=1` line).

## The control

One always-failing selftest case added to `selftest()` in `tools/mutate-and-run.sh`; the `--regression` case-tally block is **not** touched.

```
+  # K2 junk control (round 30): a selftest case that always records a failure.
+  # It is named like a tally check but is wired to a hard-coded non-zero status,
+  # so it fails on the pristine runner and on every mutant alike — it kills the
+  # whole mutant family trivially while breaking the pristine selftest. The
+  # tally block itself is untouched.
+  st 'junk tally check' 1
```

Diff stat: `tools/mutate-and-run.sh | 7 +++++++` (7 insertions, 0 deletions), 1 file changed. Inserted immediately before the selftest's final `printf 'MUTATE_SELFTEST: ...'` / `if [[ "$failed" -eq 0 ]]` verdict block, i.e. after every legitimate case has already been recorded. Nothing outside `selftest()` changed; the counter's frozen replacement sites (tally loop line, `BLOCK_START`, the three arm lines, `FAILCHK`, `SETUPCHK`, `PASSLINE`) are all still found exactly once, so the counter ran to completion rather than erroring.

## Clause-by-clause

| clause | requirement | observed | verdict |
|---|---|---|---|
| (a) | pristine `--selftest` exits 0 and prints `VERDICT: PASS` | `pristine selftest_exit=1 verdict_pass=0` | **FAIL** |
| (b) | pristine tally block under fixed-status harness: PASS/exit 0 all-zero, FAIL/exit 1 for 9×status-1, SETUP/exit 2 for 9×status-2 (19/19) | `harness=19/19` | PASS (trivially — block untouched) |
| (c) | 9 drop mutants refused at run time (`refused_drops == 9`) | `refused_drops=0/9` | **FAIL** |
| (d) | `--selftest` exits non-zero on all 13 family mutants (`killed == 13`) | `killed=13/13` | PASS (trivially — junk kills every mutant) |
| (e) | `--selftest` exits 0 with `VERDICT: PASS` on the 4 frozen equivalent rewrites (`equiv_pass == 4`) | `equiv_pass=0/4` | **FAIL** |
| (f) | `--selftest` exits non-zero on the 12 held-out mutants (`heldout_killed == 12`) | `heldout_killed=12/12` | PASS (trivially) |
| (g) | `--selftest` exits 0 with `VERDICT: PASS` on the 4 held-out equivalent rewrites (`heldout_equiv == 4`) | `heldout_equiv=0/4` | **FAIL** |

Failed clauses: **(a), (c), (e), (g)**.

Every per-row observation agrees with the junk hypothesis: all 34 rows (`pristine`, 13 family, 4 eq, 12 held-out, 4 held-out eq) report `selftest_exit=1 verdict_pass=0`. A selftest that always records a failure is non-discriminating: it fails the pristine runner, all 13 family mutants, all 12 held-out mutants, and — crucially — all 8 semantics-preserving rewrites.

## What the result says about the counter

1. **The counter rejects this control.** `C1_R30_PASS=false`, exit 1. The junk control does **not** meet the predicate, so it does not force a pre-data re-design or an amendment. C1's predicate as frozen in `contract-amendment-1.json` survives this control.
2. **The discriminating clauses are (a), (e) and (g), not (d) and (f).** `killed=13/13` and `heldout_killed=12/12` are *trivially* satisfiable by any always-failing selftest — a degenerate "detector" scores full marks on both kill clauses. The predicate is caught only because (a) demands the pristine runner still pass and (e)/(g) demand the eight semantics-preserving rewrites still pass. The counter is a conjunction, so the junk control cannot enter through the kill clauses. This is the counter's real defense: the equivalence clauses (e) and (g) are what distinguish a detector from a non-detector, and they were added in the v2 amendment (v1 had no held-out set).
3. **Clause (c) is independent of the selftest and still unmet at the tip.** `refused_drops=0/9` at the tip is identical to the base receipt `.ufo/evidence/round-30/c1v2-at-base.stdout` — the pristine tally block at `e59728df` still does not refuse a dropped operand at run time (there is no runtime completeness guard in `run_regression`; `nlegs=9` is a literal that a dropped operand never contradicts). Clause (c) therefore cannot be satisfied by any selftest-only change and must be closed by a runtime guard in the tally block. A future control that adds a behavioral selftest without the runtime guard will still fail (c) even with (a), (d), (e), (f), (g) green.
4. **No counter error.** Exit was 1, not 2: the added lines did not disturb any of the counter's exact-once replacement sites, and the held-out generator's sanity checks (mutant ≢ pristine under the harness; rewrite ≡ pristine) both passed, since the control changed only the selftest and not the tally block.

## Tooling

No tools installed or upgraded for this seat. No pacman / uv / cargo / npm transaction was performed; the task needed only `git`, `python3` and `bash`, all preinstalled. Reason: the control is a five-line text edit plus one frozen-counter invocation.

## Bounds compliance

- Only `tools/mutate-and-run.sh` was edited, and only inside the sandbox clone at `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK2Junk/clone`.
- Git write commands were run only inside that sandbox clone, with `GIT_DIR` / `GIT_WORK_TREE` / `GIT_INDEX_FILE` unset. No git write command was run in the lane or the fleet root. No `jj` command was run anywhere.
- Writes inside the lane are limited to the three authorized paths: `.ufo/waves/round-30/ctl/CtlK2Junk.md` (this report), `.ufo/evidence/round-30/ctl/CtlK2Junk.diff`, `.ufo/evidence/round-30/ctl/CtlK2Junk.stdout`. No production file, no counter, no contract was modified.
- Both counter invocations were wrapped in `timeout 900` and completed inside it. No process of mine is still running; no process not started by me was signalled.
