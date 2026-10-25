# m7 assignment-mask escape probe

Axis: calibration.

Imported `.ufo/evidence/round-44/calibration/measure.py` and called `m7_citations` independently for each form with an empty registry fixture (so any unmasked S-id is unknown). Command used: `python3 -c '... importlib.util.spec_from_file_location ...; m.m7_citations({"r": form}, {}) ...'` (scratch directory: `/tmp/tameshi-r44-CritM7Escapes-/`).

| Form | Result | Covered by documented “S-id bound to an assignment” scope? |
|---|---|---|
| `safe_floor=S256` | masked; no hit | Yes |
| `safe_floor = S256` | masked; no hit | Yes |
| `safe_floor= S256` | masked; no hit | Yes |
| `SAFE_FLOOR:S256` | flagged (`r unknown S256`) | No; colon is not assignment syntax |
| `safe_floor(S256)` | flagged (`r unknown S256`) | No; call-like parentheses do not bind via `=` |
| `` `safe_floor=S256` `` | masked; no hit | Yes; backticks do not alter assignment binding |
| `safe_floor==S256` | flagged (`r unknown S256`) | No; equality is not assignment |
| `x=staged:S153` | masked; no hit | No for assignment-mask scope; it is masked by the separate `staged:S###` package-token rule |

The three flagged forms outside the documented assignment scope are intentional per the stated rule, not escapes against valid assignments. `x=staged:S153` is also intentionally masked under a different documented class. No flagged probe form was found in an actual receipt/record: searching the lane for the exact forms found only ordinary examples of `safe_floor=S256`; these are assignment-bound and masked. The real SCORECARD historical C3 field is `safe_floor=S256` (contract identifies the old false alarm), and is therefore covered by the fix.

Evidence: counter regex `.ufo/evidence/round-44/calibration/measure.py:89`; application of ASSIGN_ID and residual ID scan at lines 101-114; documented m7 scope in `.ufo/evidence/round-44/contract.json:29`; real historical field cited in contract lines 21,23. No tool install/update.