# PredK8 — critic review of frozen predicate K8 `runner-cleanup-refused`

Revision reviewed: c8c5b88c8e961a929cdc351b95a7074c76958909 (HEAD of the lane, read-only).
Mode: static review only. This item says "Attack", not "Run", so I executed no selftest, ruler or mutant. Every claim about what a mutant does is traced from the code, not observed.

## Verdict

**K8 does not discriminate.** It does not pass vacuously. At c8c5b88 it passes for the right reason. The base result in `before.json` is honest.

The defect: K8's only fixture sets `held=False` together with `cleanup_error`. The ruler also checks the finding with `in`, not exact equality. So K8 cannot tell a real `cleanup_error` refusal apart from two plausible weaker implementations:

- W1 relabels every not-held row.
- W2 checks `cleanup_error` only inside the not-held branch.

W2 also survives the tool's own `--selftest`. That leaves the documented rule ("refuses when `held` is not `true` **or** `cleanup_error` is set") with no test for the `cleanup_error`-alone half.

This is a fixable defect in the ruler and the selftest. It is not a tradeoff the judge must reject. The real runner never emits `cleanup_error` with `held=True`, so the gap only shows up when `--project` reads observation files that the runner did not write.

## Counterexamples

**W2 (strongest; survives K8, K7 and the tool selftest).** Replace `tools/registry-replay.py:86-91` with:

```python
if result.get('held') is not True:
    findings.add('RUNNER_CLEANUP_FAILED' if result.get('cleanup_error') else 'RUNNER_NOT_HELD')
    refused.append(name)
```

Traced against `measure.py`:

- control `obs()`: `held=True` → no finding, exit 0, bundle written. `control_ok` stays true.
- K7 `obs(held=False)` → `['RUNNER_NOT_HELD']`, exit 1, no bundle. Discriminated.
- K8 `obs(held=False, cleanup_error='row descendants remain')` → `['RUNNER_CLEANUP_FAILED']`, exit 1, no bundle. Discriminated.
- Tool selftest (`registry-replay.py:199-206`): the `not-held`, `cleanup` and `held-missing` cases all give the exact expected lists. The `REGISTRY_REPLAY_SELFTEST: 10/10 pass` registry row (`tools/registry.json:991-998`) still holds.

The input that separates W2 from c8c5b88 is a row with `runner_result = {got: 0, held: true, stdout: 'OK\n', stderr: '', cleanup_error: 'x'}`:

- c8c5b88 (`:86-88`, cleanup checked first): exit 1, `RUNNER_CLEANUP_FAILED`, no bundle.
- W2: exit 0, bundle published.

Neither the ruler nor the selftest contains this input.

**W1 (survives K8 and K7; killed only by the tool selftest).** Ignore `cleanup_error` entirely and add both `RUNNER_NOT_HELD` and `RUNNER_CLEANUP_FAILED` to any row whose `held` is not `True`. The K8 check at `measure.py:179` (`finding in report.get('finding_ids', [])`) accepts the two-element list, and so does the K7 check. The tool selftest kills W1 because it compares exact lists (`registry-replay.py:219`). `measure.py` never runs that selftest, though, so K8's discrimination depends on a separate registry row, not on K8 itself.

## Evidence

- K8 fixture is `obs(held=False, cleanup_error=...)` with a membership check: `.ufo/evidence/round-24/measure.py:173-180`. No `held=True` cleanup fixture exists. The finding check is membership, not equality.
- Implementation precedence: `tools/registry-replay.py:86-91` checks `cleanup_error` before `held`, so at c8c5b88 K8 passes through the cleanup branch (right reason).
- Selftest `cleanup` case is also `held=False`: `tools/registry-replay.py:200`.
- Runner invariant: `tools/registry-check.py:720` sets `held = got == expected_exit and not missing and cleanup_ok`. The timeout path (`:700-709`) sets `held=False` before adding `cleanup_error`. So on runner-produced observations, W2 behaves the same as c8c5b88; the two differ only on observation files the runner did not write. `--project` accepts any such file (`registry-replay.py:273-284`).
- Documented rule says either condition is enough: `corpus/knowledge/replay-projection-hardening.md:17` ("`held` is not `true` or `cleanup_error` is set"). SKILL.md:2052 lists `RUNNER_CLEANUP_FAILED` as a separate refusal.
- Not vacuous: a missing tool gives `tool-absent` → false (`measure.py:143-144`). An unparseable report becomes `{}`, so the finding check sees an empty list → false (`:163-166`). The control gate needs exit 0, `finding_ids == []` and a written bundle (`:170`), which kills an implementation that always refuses.
- Minor: the ruler only checks for `out/bundle.json` (`:167`). An implementation that wrote `expected.json` or `live-dependent.json` on refusal would still pass. c8c5b88's `publish` writes nothing when `bundle is None` (`registry-replay.py:116-118`).

## Is `before.json` honest?

Yes.

- `git ls-tree 6a1821a… tools/` shows only `command-binding.py` and `registry-check.py`; `registry-replay.py` is absent. So K8 = `tool-absent` = false is the only possible result at base.
- The recorded `instrument_sha256` (`0a7f6daa…daa64`) matches both the frozen ruler (`git show e338f1b:.ufo/evidence/round-24/measure.py | sha256sum`) and the current file.
- e338f1b's only parent is the base 6a1821a.
- The 1/11 count (only K4 discriminated) agrees with the base selftest output in the receipt.

## Impacted axes

- **Calibration/discrimination:** K8 claims "cleanup refused" but only tests "cleanup on a not-held row". That is weaker than its name and weaker than the rule documented in the knowledge entry.
- **Documentation fidelity:** `replay-projection-hardening.md:17` claims an either-condition refusal that has no test.

No regression, no duplicate authority and no identity change in the K8 path.

## Smallest safe correction

The ruler is frozen, so the K8 result for round 24 stands on its own terms. The fixes are:

1. **Tool selftest (production, next integrator):** add a case `('cleanup-held', obs(held=True, cleanup_error='x'), (), 1, ['RUNNER_CLEANUP_FAILED'], False)` and update the registry literal to `11/11`. This kills W2 at the registry level.
2. **Next contract's ruler:** add a K8 fixture `obs(cleanup_error='row descendants remain')` with `held` left `True`. Require exact `finding_ids == ['RUNNER_CLEANUP_FAILED']` for K8, and the same for K7 with `['RUNNER_NOT_HELD']`. This kills W1 and W2 directly.
3. Optionally, require that the refusal writes no files at all under `--out` (`not out.exists()`).

To confirm the traces, a Run-authorised item would apply W2 to a /tmp clone at c8c5b88, then run `measure.py --repo CLONE` (expected: K8 discriminated true) and `python3 tools/registry-replay.py --selftest` (expected: 10/10).

## Tooling

No tools installed or updated.
