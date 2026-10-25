# ExecCommandD — Command D (axis: depth)

Seat: executor (leaf). Lane untouched; read-only `git show` only. No tool installs were
needed or performed. Work dir: `/tmp/tameshi-r40-ExecCommandD/`.

## Command and output

Exact command from `SCORECARD.md:72-73` (the file's only Command D definition), run from the
lane root:

```sh
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

with `REV=5641ed84c8dc148c34c8dd83f062279ddf06b4af`:

```
recorded_cases=9 depth_score=9
exit=0
```

**recorded_cases=9 · depth_score=9.** Matches the frozen `contract.json:10` value
`"depth_score": 9` and the live depth row `SCORECARD.md:1536` (which predicts
`recorded_cases=9 depth_score=9`).

## The nine counted rows (grounding the count)

At REV, `tools/mutate-and-run.sh:87-95` — exactly the nine lines the regex matches:

| line | row | target | recorded |
|---|---|---|---|
| 87 | `js-kimi-census` | `kumitate-shokunin/scripts/kimi-census.mjs` | 8/10 (80 %) |
| 88 | `bash-surface-census` | `kagi-shokunin/corpus/surface-census.sh` | 8/10 (80 %) |
| 89 | `bash-tsukuroi-census` | `tsukuroi-shokunin/tools/tsukuroi-census.sh` | 6/10 (60 %) |
| 90 | `bash-mado-verify` | `mado-shokunin/tools/mado-verify.sh` | 4/10 (40 %) |
| 91 | `bash-checklist-run` | `kagi-shokunin/corpus/checklist-run.sh` | 7/15 (47 %) |
| 92 | `js-claims-check` | `kumitate-shokunin/scripts/claims-check.mjs` | 7/10 (70 %) |
| 93 | `js-round-gate` | `kumitate-shokunin/scripts/round-gate.mjs` | 5/10 (50 %) |
| 94 | `js-sources-check` | `kumitate-shokunin/scripts/sources-check.mjs` | 5/10 (50 %) |
| 95 | `js-cite-check` | `kumitate-shokunin/scripts/cite-check.mjs` | 5/10 (50 %) |

The runner's executable registry agrees, so the 9 is not comment-only drift:

- nine `regression_case_git` invocations: `tools/mutate-and-run.sh:1386, 1391, 1396, 1401, 1406, 1411, 1416, 1421, 1426` at REV;
- `local nlegs=9 npass=0 nfail=0 nsetup=0 st` at `:1432`;
- `REGRESSION_EXPECT` prints the same nine names at `:1374`;
- no tenth leg name appears anywhere in the 2080-line file.

## Falsification attempts (all negative — predicate holds)

1. **Over-count?** `git show REV:tools/mutate-and-run.sh | grep -nE '^#   (js|bash)-'` returns
   exactly the nine lines above; no indented example/spec-block line outside the ledger block
   matches the regex. Count is not inflated by prose.
2. **Under-count?** The regex requires `NN/NN`; the `7/15` row is included, and every leg has a
   matching `regression_case_git` call plus an `nlegs` tally of 9. No recorded case exists that
   the regex misses.
3. **Base-vs-rev invariance — the depth move is zero.** `tools/mutate-and-run.sh` is
   byte-identical at base and REV:
   - base `304e3355…` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
   - REV `5641ed84…` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
   - `git diff --stat 304e3355 5641ed84 -- tools/mutate-and-run.sh` → empty
   - Command D at base also prints `recorded_cases=9 depth_score=9`.

   So round 40 **holds** depth at 9; it adds no ledger leg. Any claim of a depth increment from
   Command D this round is refuted by the empty base→rev diff.
4. **Anchor check.** The live depth row (`SCORECARD.md:1536`) cites `:87-95`, which is exactly
   where the nine rows sit at REV. The older pre-round baseline row (`SCORECARD.md:66`) cites
   `:84-89`, which at REV spans only the `--regression` prose header plus rows 87-89 — that row
   is explicitly historical and Command D does not read it; the score is unaffected.

## Verdict

Command D reproduces the frozen depth scalar exactly: **recorded_cases=9, depth_score=9**,
exit 0. No falsification found. Retained evidence: command + output above, row listing at
`:87-95`, registry calls at `:1386-1429`, `nlegs=9` at `:1432`, identical runner sha at both revs.

Notes: C1 and C2 counters were **not** run in default mode (that run belongs to the L1). No lane
file, index, or jj state was written.
