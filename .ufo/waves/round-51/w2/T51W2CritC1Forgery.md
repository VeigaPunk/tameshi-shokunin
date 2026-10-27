# T51W2CritC1Forgery — C1 counter attack

Axes: calibration (C1 claim); depth and operability (counter weakness is actionable). This is a counter-forgery report, not a new C1 verdict.

## Baseline

Isolated shared clone at `/fast/scratch/hyaku/tameshi-r51/T51W2CritC1Forgery/clone`, checked out at CAND `6d8c11e378aa90b12650808e1b79270742935f15`. Boundary command was `git -C .../clone rev-parse --show-toplevel`; it returned the clone path before checkout. Pristine command:

```sh
python3 .ufo/evidence/round-51/c1/measure.py --lane /fast/scratch/hyaku/tameshi-r51/T51W2CritC1Forgery/clone --rev HEAD --explain
```

Observed exit 0, ten `FRONTIER Fk: ok`, `frontier_bad=0 readme_prefix=1 sources_rows=133 status_conflicts=0 usedby_missing=0 total=0 C1_R51_PASS=true`.

## Findings

Each probe changed exactly one condition in the cloned counter, ran it against the pristine candidate, and restored the counter. All six printed `total=0 C1_R51_PASS=true` (exit 0):

- **F1 — status mismatch ignored.** Replaced `if word != want['status'].lower():` with `if False:`. Counter mutation: a README status/round disagreement no longer contributes to `fbad`. Evidence: `measure.py:119-127`; invocation/output above and probe label `ignore status mismatches`.
- **F2 — unsupported pointer accepted.** Replaced `if not ok_ptr:` with a no-op condition. Counter mutation: a missing/unsupported citation no longer contributes to `fbad`. Evidence: `measure.py:128-141`; probe label `ignore pointer validation`.
- **F3 — duplicate table rows accepted.** Replaced `if len(mine) != 1:` with `if len(mine) == 0:`. Counter mutation: multiple rows for an expected ID bypass the uniqueness check. Evidence: `measure.py:105-111`; probe label `accept duplicate rows`.
- **F4 — queued/used-by contradiction ignored.** Replaced `if status == 'queued' and paths:` with `if False:`. Counter mutation disables this registry contradiction count. Evidence: `measure.py:147-163`; probe label `ignore source status conflict`.
- **F5 — missing mined used-by path ignored.** Replaced `if not exists(lane, rev, p):` with `if False:`. Counter mutation disables the missing-path finding. Evidence: `measure.py:164-168`; probe label `ignore missing used-by paths`.
- **F6 — non-prefix README accepted.** Replaced `total = fbad + conflicts + missing + (1 - prefix)` with `total = fbad + conflicts + missing`. Counter mutation drops the append-only invariant from scoring. Evidence: `measure.py:179-195`; probe label `ignore append-only prefix`.

Exact probe driver was a Python `- <<'PY'` script in the scratch clone: it loaded `orig=counter.read_text()`, replaced one exact `a` with `b` per mutation, ran `["python3", str(counter), "--lane", str(p), "--rev", "HEAD", "--explain"]` with `cwd=p`, printed return code/label/summary, then restored `orig`. All replacement anchors were present. It did **not** commit mutations or alter lane files.

## Calibration / limitation

These demonstrate six single-clause weakened counters yielding a false pass on CAND, but are not the stronger differential claimed by “pristine rejects, mutant passes”: the pristine candidate itself correctly passes each unperturbed predicate. I did not claim empirical wrong-table/pointer/SOURCES fixtures were rejected by pristine and accepted by the corresponding mutated counter. The exact fixture-level differential remains unproven here. The measured result is still material: the counter's implementation has independent single-clause blind spots if the corresponding bad data reaches the deciding revision.

Smallest safe correction: retain the frozen counter bytes as an authenticated deciding-run input (or pin and verify its digest in the runner), so the tested implementation cannot be silently weakened; add targeted negative controls for each predicate—wrong status, unsupported pointer, duplicate ID row, queued-with-used-by, missing mined path, and rewritten README—and require pristine rejection before accepting its positive control. Counter provenance is not established merely by a self-consistent `C1_R51_PASS` receipt.
