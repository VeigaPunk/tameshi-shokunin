# Round 18 C1 mutation case — X01CaseSpec

Axes: **depth** (eighth mutation case), **calibration** (pre-registered predictions), **operability** monitored only.

## Result

Built and ran the eighth `kumitate` mutation case for `scripts/sources-check.mjs`. The pinned source was not modified. The 10 exact-string defects were registered before the first mutant run; the pristine control passed; the sweep produced **5/10 killed (50%)**, with **10/10 predictions matching** and **0 inconclusive**.

## Files written

- `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`
- `.ufo/evidence/round-18/sources-check/predictions.json`
- `.ufo/evidence/round-18/sources-check/suite.txt`
- `.ufo/evidence/round-18/sources-check/control.txt`
- `.ufo/evidence/round-18/sources-check/sweep/sweep.txt`
- `.ufo/waves/round-18/w1/X01CaseSpec.md` (this report)

## Evidence

- **Pinned bytes:** `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs` was materialized at `/tmp/tameshi-r18w1-X01CaseSpec-mPCKzd/sources-check.mjs`; SHA-256 `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`, 897 lines, mode 100755 (`git ls-tree` reported `100755 blob`). The ten `@old` anchors were each checked on the materialized pinned copy and each search returned exactly one occurrence: finding emission line 293, enum line 114, usage return line 492, DRIFT verdict line 483, strict promotion line 434, missing-source fail-closed line 182, row increment line 247, duplicate finding line 251, entry count line 368, and per-file read fail-closed line 356.
- **Runner syntax and method:** in the `/tmp` lane clone at the dispatch revision, `bash tools/mutate-and-run.sh --help` exited 0 and showed the `@defect` / `@old` / `@new` format, count==1 guard, and exit-status oracle. The copied hermetic suite is the round-16 `env -i` form with per-defect private `HOME`/`TMPDIR`, `GIT_CONFIG_NOSYSTEM=1`, and `GIT_CEILING_DIRECTORIES`.
- **Preregistration:** spec SHA-256 `c8d24cb4b6b1a372543764fc27c9d16f65510a29fed1045bedb2863ce2408c91`; suite SHA-256 `6e550d5a2f6a78fc0654c297b80bb042e8482423d80e2e16bab7374227931f7b`. Predictions record five kill-aimed and five hole-aimed defects. The L1 was messaged exactly `C1 predictions ready`; the requested `refs/heads/master:.ufo/evidence/round-18/sources-check/predictions.json` poll resolved after 60 seconds. L1 confirmed commit `93d22aa21a144a0e2833b1be74718d15060f002b` and froze the spec/predictions before the sweep.
- **Pristine control:** the corrected direct control invocation exited 0, stdout SHA-256 `e0880a5a2bed0bba3d1a08583ac9e9d95db8f259d5a563f877b7f27544665e5f` (6,274 bytes), empty stderr, `SOURCES_SELFTEST: 46/46 pass` / `VERDICT: PASS`; retained in `control.txt`. An initial wrapper attempt had an unexported suite variable and therefore executed no selftest (exit 0, empty stdout); it is not counted as the control. The immediately corrected invocation is the recorded run.
- **Sweep:** ran `bash tools/mutate-and-run.sh --target /tmp/tameshi-r18w1-X01CaseSpec-mPCKzd/sources-check.mjs --defects <committed round-18 spec> --suite <committed suite>` from the `/tmp` fleet mirror at `refs/heads/master` commit `93d22aa21a144a0e2833b1be74718d15060f002b`; runner SHA-256 `fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a`, exit 0. Full output is retained in `sweep/sweep.txt`: target/spec/control pins at lines 2–19; all ten measured results at lines 20–109; `MUTATE_RESTORE: OK` at line 110; `MUTATE: DONE (target=sources-check.mjs defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)` at line 112; prediction comparison 10/10 and 5/10 rate at lines 117–131. The target SHA-256 after the sweep matches the pin (`sweep.txt:110,115–116`).

## Risks and blockers

No blocker. The five predicted survivors are sensitivity limits observed by this suite: enum shrinkage, DRIFT verdict spelling, duplicate line location, positive `entriesWithSource` count, and the per-entry read-failure classification. They were not repaired or separately probed; this assignment builds and measures the case only. No tools were installed.

**Verdict: built**
