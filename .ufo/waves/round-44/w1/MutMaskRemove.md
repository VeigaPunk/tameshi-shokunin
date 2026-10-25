# MutMaskRemove — round-44 w1 mutation probe (red-before receipt)

Seat: L1Tameshi44.MutMaskRemove (mutation tester). Lane: tameshi-shokunin.

## Mutant
Copied the round-44 counter to scratch `/tmp/tameshi-r44-MutMaskRemove-/measure.py` and removed
ONLY the `ASSIGN_ID.sub(...)` line in `m7_citations` (originally measure.py:109):
`masked = ASSIGN_ID.sub(lambda m: re.sub(r'S\d{3,}', ' ', m.group(0)), masked)`.
`diff -u` against the lane copy shows exactly this one line removed (nothing else changed).

## Detector
`python3 /tmp/tameshi-r44-MutMaskRemove-/measure.py --selftest`

## Output (verbatim)
```
C2_R44_SELFTEST: cases=16 failed=2
FAIL T6_safe_floor_value_not_citation ['r unknown S256']
FAIL T6_assign_with_spaces_masked ['r unknown S256']
VERDICT: FAIL
selftest_exit=1
```

## Verdict
KILLED. failed=2 matches the contract's do_nothing_control expectation exactly:
`T6_safe_floor_value_not_citation` and `T6_assign_with_spaces_masked` fail with
`['r unknown S256']`; exit code 1. This is the red-before receipt for the
ASSIGN_ID mask fix.

## Evidence
- Pristine lane copy sha256: `c0c6199fd6172df69326834eaad4884a27427fdd84cf79404dd5b1f44bd9c0d6`
  (equals contract `counter_sha256`).
- Mutated scratch sha256: `aabebebaf1dac5293367624a7eb6ee6f524f30452774f036a4d3207b07dbbdef`.
- Diff (lane vs scratch) removes only line 109 (`ASSIGN_ID.sub(...)`).
- Lane checkout untouched (read-only; no git/jj mutations). Scratch is disposable per item.

## Notes
- The contract-referenced receipt `.ufo/evidence/round-44/control/mask-removed.selftest.stdout`
  does not yet exist in the tree; this report carries the verbatim selftest output (cases/failed/exit)
  that receipt would contain.
- No tools installed; no pacman/uv/npx actions needed.
