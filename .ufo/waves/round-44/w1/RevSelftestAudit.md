# RevSelftestAudit — round-44 selftest vacuity audit (wave 1)

Audit scope: `.ufo/evidence/round-44/calibration/measure.py` (sha256 `c0c6199fd6172df69326834eaad4884a27427fdd84cf79404dd5b1f44bd9c0d6`,
matches the contract pin). Method: copy the counter to `/tmp/tameshi-r44-RevSelftestAudit-A/base.py`, apply one one-line mutation per case (verified by
`difflib` to differ from base in exactly one line), and run `python3 <mutant>.py --selftest` (Python 3.14.8; no tools installed — no pacman/npx/uv
transaction needed). Baseline first: `C2_R44_SELFTEST: cases=16 failed=0` / `VERDICT: PASS`.

## Result: zero vacuity — all 16 cases have a failing one-line mutation

| Case | Rule it proves | One-line mutation (counter line → changed) | Observed |
|---|---|---|---|
| T1_missing_planned_detected | missing `**Planned (round N+1):**` field must flag | L170 `% (round_no + 1)` → `% round_no` | FAIL (expected `['**Planned (round 10):**']`, got `[]`) |
| T1_planned_present_clean | present field with a value is clean | L177 `if not tail:` → `if True:` | FAIL (`['**Planned (round 10):** names nothing']`) |
| T1_prose_only_detected | prose mention of "Planned (round 10)" is not the field, must flag | L173 `if index < 0:` → `if False:` | FAIL (`[]`); collateral: T1_missing_planned_detected also fails |
| T2_indent_probe_load_bearing | indent probe is load-bearing: column-zero counts N-1, census-valid counts N | L210 `lines[index] = '  ' + line` → `lines[index] = line` | FAIL (`column0=2 valid=2`); collateral: T2_census_valid_standing_clean also fails |
| T2_column_zero_standing_detected | column-zero counting command must flag | L228 `elif not any('0,3' in span for span in commands):` → `elif False:` | FAIL (`[]`); collateral: T2_column_zero_plus_prose_detected also fails |
| T2_census_valid_standing_clean | census-valid `^ {0,3}\|` command is clean | L228 → `elif True:` | FAIL (`['standing command is column-zero only']`) |
| T2_column_zero_plus_prose_detected | 0,3-space pattern in prose is not the command, still flags | L228 → `elif not any('0,3' in span for span in commands) and '0,3' not in newest:` | FAIL (`[]`) |
| T3_path_cites_clean | resolving backtick cites (after `:NN`/brace norm) are clean | L267 `if token in tree_paths:` → `if False:` | FAIL (`['r:corpus/SOURCES.md', 'r:tools/x.py']`) |
| T3_path_cites_detected | unresolved cite must flag | L272 `hits.append(...)` → `pass` | FAIL (`[]`) |
| T4_mined_parse | `mined_ids` reads the status cell (index 7) | L149 `status = cells[7] if len(cells) > 7 else ''` → `status = cells[6]` | FAIL (`set()` vs `{'S001','S002'}`) |
| T4_id_regex | `ID_RE` matches S### but not S99 | L75 `\bS\d{3,}\b` → `\bS\d{2,}\b` | FAIL (`['S001','S99']` vs `['S001']`) |
| T5_count_claim | `row_count_claim` parses "N rows at round M" | L191 "rows at round" → "row at round" | FAIL (`None None`) |
| T6_safe_floor_value_not_citation | `safe_floor=S256` (assignment-bound S-id) is a value, not a citation | L109 ASSIGN_ID mask line removed → `pass` | FAIL `['r unknown S256']` (see output below); collateral: T6_assign_with_spaces_masked also fails |
| T6_assign_with_spaces_masked | `safe_floor = S256` (spaces around `=`) is masked | L89 `\s*=\s*` → `=` | FAIL `['r unknown S256']` |
| T6_genuine_unknown_still_flagged | genuine unknown S-id must still flag as unknown | L111 `if sid not in registry_rows:` → `if False:` (unknown branch deadened) | FAIL `['r unmined S777']` (see output below) |
| T6_unmined_flagged | unmined (queued) row cite must flag | L113 `elif sid not in mined:` → `elif False:` | FAIL (`[]` vs `['r unmined S001']`) |

Required mutations, command output (run in `/tmp/tameshi-r44-RevSelftestAudit-A/`):

```
$ python3 T6_safe_floor_value_not_citation.py --selftest    # ASSIGN_ID mask line (L109) removed
C2_R44_SELFTEST: cases=16 failed=2
FAIL T6_safe_floor_value_not_citation ['r unknown S256']
FAIL T6_assign_with_spaces_masked ['r unknown S256']
VERDICT: FAIL

$ python3 T6_genuine_unknown_still_flagged.py --selftest    # unknown branch (L111) deadened
C2_R44_SELFTEST: cases=16 failed=1
FAIL T6_genuine_unknown_still_flagged ['r unmined S777']
VERDICT: FAIL
```

The first matches the contract's `do_nothing_control` receipt (`mask-removed.selftest.stdout`: ASSIGN_ID mask line removed → `['r unknown S256']`).

## Collateral failures (mutations that break a sibling case too)

All collateral failures are the complementary half of the same rule and are documented above: deadening the missing-field branch also deadens prose detection
(T1), disabling the indent breaks the census-clean case (T2), disabling column-zero flagging also affects the prose-0,3 case (T2), and removing the
ASSIGN_ID mask also lets the spaced-assign form through (T6). No mutation caused a *different* rule's case to fail beyond its direct dual.

## Verification gaps

- Only the 16 named `case(...)` entries were exercised; the `main()` measurement path (self_pin/classes/total, freeze pinning) is not covered by
  `--selftest` — out of scope for this item.
- Mutations were applied to a scratch copy, not to the committed counter (lane read-only); the committed counter is untouched and still `.self-tests PASS.

## Tooling

No tools installed. `python3` 3.14.8 (system) was used; no pacman/npx/uv transaction was needed.
