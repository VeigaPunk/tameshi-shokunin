# CriticC2Zero — depth axis, milestone "Constant zero"

## Finding: why a census tool that always prints unflagged=0 fails planted_unflagged=1

The predicate (`.ufo/evidence/round-39/contract.json:24`) requires the committed
tool's `--selftest` to report `planted_unflagged=1`. The planted control string is
in the pinned tool itself:

- `tools/write-path-census.py:58` — `PLANTED['unflagged'] = 'open("case.expected", "w")\n'`

That line is an expected-value write (`EXPECTED_RE` matches `case.expected`,
`tools/write-path-census.py:51-53`) with no update flag (`FLAG_RE` miss, line 55)
and no scratch path (`SCRATCH_RE` miss, line 54), so an honest
`classify_text` (lines 64-74) must count it as 1 unflagged write. The selftest
hard-codes the expectation `expect = {'unflagged': 1, ...}` at line 89 and prints
`planted_unflagged=<got>` at line 109.

A classifier that returns `unflagged=0` unconditionally misclassifies the planted
string → selftest prints `planted_unflagged=0` → `measure.py:126`
(`fields.get('planted_unflagged') == '1'`) is false → `planted_ok` false →
`C2_R39_PASS=false`. This is exactly the contract's pre-declared kill
(`contract.json:28`: "A classifier that always reports 0 fails planted_unflagged").

## Evidence (executed)

1. Constant-zero mutant (scratch copy, `return write_sites, 0` at line 74):
   ```
   WRITE_CENSUS_SELFTEST: planted_unflagged=0 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1
   FAIL planted unflagged: want unflagged=1 got 0
   rc=1
   ```
2. Pinned tool selftest (working-tree blob sha256 `bc8c660c…` == contract pin
   `contract.json:30`): `planted_unflagged=1 … fixture_wrote=1`, rc=0.
3. Control: `python3 .ufo/evidence/round-39/census/measure.py --lane … --rev 50aadd1bbd94e43cd3fcfb81459414394db2dc35`
   → `tool_absent=1 gates=0/21 … C2_R39_PASS=false` (rc=1), matching the frozen
   `before` field.
4. `measure.py --rev HEAD` → `tool_sha_ok=1 gates=21/21 planted_unflagged=1 …
   mutant_killed=1 C2_R39_PASS=true` (rc=0).

## Counterexample attempt — none survives

Strongest attack: a constant-zero classifier that *hardcodes* `planted_unflagged=1`
in its selftest output. It clears `planted_ok` but cannot match the
`tool_sha256` pin (`contract.json:30`, enforced `measure.py:83-84,133`), so
`tool_sha_ok=0` still yields `C2_R39_PASS=false`. The sha pin binds the exact
bytes; `live_unflagged` is reported-only per the kill rule (`contract.json:29`),
so honest classification of the planted string is the only path through.
No falsification of the frozen predicate found.

## Impacted axes

Depth only. The constant-zero kill chain is real and verified end-to-end;
the predicate stands. No correction needed — claim supported.

## Smallest safe correction

None.
