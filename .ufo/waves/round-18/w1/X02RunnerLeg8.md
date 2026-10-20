# X02RunnerLeg8 — round 18 leg 8 integration

## Files changed

- `.ufo/waves/round-18/staged/tools/mutate-and-run.sh` — staged from committed
  `git show 183f87b899e6cae46be98d251cbc87fb5118f6ca:tools/mutate-and-run.sh`;
  adds the eighth ledger row, pin/revision, embedded `js-sources-check.spec`
  integration fixture, spec existence check, `REGRESSION_EXPECT` entry, pinned
  `regression_case_git` call, case tally, and selftest list/tuple agreement.
  The leg runs `node "$MUTANT" --selftest` against kumitate
  `scripts/sources-check.mjs` at `0acb7752d19058b953ebbeba253b1e35f6548de5`.
  Its header row uses the requested `0/10 (PLACEHOLDER)` so command D's format
  regex matches it.
- `.ufo/waves/round-18/staged/LEG8-INTEGRATION.md` — exact list of every
  remaining L1 replacement point.
- `.ufo/waves/round-18/w1/X02RunnerLeg8.md` — this report.

The committed target pin was confirmed by `git show ... | sha256sum` as
`6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`; `git
ls-tree` reports mode `100755`. The staged script is executable.

## Evidence

All selftest and regression commands ran in the `/tmp` fleet-mirror clone
`/tmp/tameshi-r18w1-X02RunnerLeg8-9lpK4u/fleet/tameshi-shokunin`, with
`GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, and `GIT_COMMON_DIR` unset and
working directory inside that clone. No lane or sibling Git worktree was used
for test writes.

1. **Before — committed baseline:**
   `(cd "$CLONE" && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR bash tools/mutate-and-run.sh --selftest)`
   exited **0**. Receipt:
   `/tmp/tameshi-r18w1-X02RunnerLeg8-9lpK4u/selftest-before.txt:96-97`:
   `MUTATE_SELFTEST: 95/95 pass`; `VERDICT: PASS`.

2. **After — staged runner and dummy spec:**
   The same command exited **0**. Receipt:
   `/tmp/tameshi-r18w1-X02RunnerLeg8-9lpK4u/selftest-after-fixed.txt:83-97`:
   `PASS embedded leg specs: eight files written`,
   `PASS leg-count agreement: calls=8 specs=8 nlegs=8 (want 8)`,
   `PASS leg-count agreement: selftest leg tuples=8 (want 8)`,
   `PASS embedded leg js-sources-check: spec and recorded table agree`, and
   `MUTATE_SELFTEST: 96/96 pass`; `VERDICT: PASS`.

3. **Regression:**
   `(cd "$CLONE" && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR bash tools/mutate-and-run.sh --regression --keep)`
   exited **0**. Receipt:
   `/tmp/tameshi-r18w1-X02RunnerLeg8-9lpK4u/regression-fixed.txt:40-45`:
   - `REGRESSION_PIN js-sources-check` identifies rev
     `0acb7752d19058b953ebbeba253b1e35f6548de5`, mode `100755`, and the expected
     SHA-256.
   - `REGRESSION_SWEEP js-sources-check: MUTATE: DONE (target=js-sources-check defects=2 killed=2 survived=0 inconclusive=0 kill-rate=100%)`
   - `REGRESSION_TABLE js-sources-check: match=2/2 recorded-killed=2 measured-killed=2 survived=0 inconclusive=0 flips=0`
   - `REGRESSION_CASE js-sources-check: PASS ... defects=2`
   - `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`

   The first dummy regression attempt exited 2 because its second `@old` string
   occurred twice (`APPLY FAIL id=R18D2 ... old-string-count=2 expected=1`,
   `/tmp/tameshi-r4-2-regression.p545BJ/js-sources-check/sweep.log:5-6`). The
   placeholder was corrected to a unique legacy-identity assertion and the
   final selftest/regression above passed. This was a dummy-fixture setup issue,
   not an unresolved target failure.

4. **Leg-count red-before:**
   In the temporary clone only, removed the `js-sources-check` tuple and ran the
   selftest command above. It exited **1**. Receipt:
   `/tmp/tameshi-r18w1-X02RunnerLeg8-9lpK4u/legcount-redbefore.txt:83-97`:
   `PASS leg-count agreement: calls=8 specs=8 nlegs=8 (want 8)`,
   `FAIL leg-count agreement: selftest leg tuples=7 (want 8)`, and
   `MUTATE_SELFTEST: 94/95 pass`; `VERDICT: FAIL`. The staged file retains the
   tuple.

5. **Header ledger regex:**
   `functions.grep` with
   `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+` against the staged runner returned
   exactly eight rows at lines 86–93; the eighth is the `js-sources-check`
   `0/10` placeholder.

## L1 replacements, risks, blockers

The staged code is intentionally not the final measured round-18 case. L1 must
replace the temporary spec/table and selftest tuple counts, change the header
`0/10` to the measured kill-rate, and update the temporary/pending provenance
comments. `.ufo/waves/round-18/staged/LEG8-INTEGRATION.md` lists each exact line
range. No other blocker; no tools were installed.

Verdict: built
