# Round-43 m7 first-hit: byte-level cause

Axes: calibration (assigned); depth/investigative completeness; reproducibility. The cause is a regex mismatch between prose phrase `safe floor` and field key `safe_floor`.

## Evidence chain

- Base commit `506e99c7b73c85711f066895984d501fcf7539cd` SCORECARD line 2091 (from `git show <base>:SCORECARD.md`) is:
  `C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=24 selftest_failed=0 staged_rows=103 live_collisions=7 live_collisions_agree=1 live_held=3 live_held_agree=1 live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1 safe_map_admitted=1 map_dedupe_live=1 held_refused=1 safe_floor=S256 staged_sha256=020fbeaa… naive_agree=1 substitute=0 rev=3c4003f6… C3_R43_PASS=true`
- Exact token bytes: `safe_floor=S256` = `73 61 66 65 5f 66 6c 6f 6f 72 3d 53 32 35 36` (underscore is byte `5f`; spaces are `20`). Full line byte dump was captured from the commit in `/tmp/tameshi-r44-RevCause/scratch/scorecard-base.md`.
- Round-43 code `.ufo/evidence/round-43/calibration/measure.py:73-81` declares `safe floor` in `MASK_IDS` / `VALUE_ID_AFTER`; `safe floor` has a literal space, not `_`. The loop at lines 451-458 skips the `safe-floor` entry (and skips the phrase-only entry), then applies `VALUE_ID_AFTER`; thus neither expression removes `S256` from `safe_floor=S256`. Applied to the exact line, the old mask leaves it unchanged and `ID_RE` yields `[S256]`. With the empty registry map used to isolate this line, old m7 reports `[SCORECARD.md#round-43 unknown S256]`.
- Round-44 code `.ufo/evidence/round-44/calibration/measure.py:89, 101-110` adds `ASSIGN_ID = re.compile(r\b[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*?S\d{3,}?)` and masks the matched ID. The same exact line is therefore masked; it produces no ID and m7 is `[]` against the same empty map. This assignment-form match accepts `_` in the key.
- Counter outputs on the allowed base revision (both executable scripts imported from their specified committed versions):
  - Round 43, `--rev 506e99c7b73c85711f066895984d501fcf7539cd --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685`: `C2_R43: self_pin=1 classes=7 m6=0 m7=1 m8=0 m10=0 m11=0 m12=0 m13=0 total=1 records=4 sources_rows=114 standing=114 receipts=17 revisions=4 m13_probe=standing=7_column0=113_valid=114 rev=506e99c7b73c85711f066895984d501fcf7539cd freeze=6b83a11c61f0fad1074ec1f2a4c38a2fd7034685 C2_R43_PASS=false first=m7:SCORECARD.md#round-43_unknown_S256`
  - Round 44, same `--rev`, `--freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e`: `C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=1 m13=0 total=1 records=4 sources_rows=114 standing=114 receipts=17 revisions=4 m13_probe=standing=7_column0=113_valid=114 rev=506e99c7b73c85711f066895984d501fcf7539cd freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=false first=m12:newest_block_is_round_43,_the_contract_round_is_44`
  - The round-44 `m12` hit is expected for this diagnostic invocation: the requested base revisions newest SCORECARD block is round 43, whereas that counters frozen contract round is 44. It does not alter the demonstrated m7=0 for the inherited block.

## Regex byte diff

The old value-after regex is `(?:staged:|next unused id|safe floor|register:)[^\\n]{0,30}?\\bS\\d{3,}\\b`. The new mask adds the separate assignment regex above; `VALUE_ID_AFTER` itself is unchanged. Unified source diff (old→new): the unchanged `VALUE_ID_AFTER` definition moves from line 81 to 85; added at new line 89 is `ASSIGN_ID = re.compile(r\b[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*?S\d{3,}?)`; added at new line 109 is application of that mask. Byte-level distinguishing addition is `5c 62 ...` (regex `\\b` word boundary), identifier class `[a-zA-Z_]` (underscore explicitly included), assignment `\\s*=\\s*`, then optional quote and `S\\d{3,}`. The old regex requires literal `safe floor`; it cannot match underscore in `safe_floor`.

## Conclusion and confidence

Observed cause with high confidence: the round-43 m7 first-hit was `S256` from the exact `safe_floor=S256` SCORECARD receipt field. The old phrase-based mask did not match that field spelling; assignment masking in round 44 removes the assigned S-id. No tooling installed.
