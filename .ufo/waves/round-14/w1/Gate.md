# Gate — expectation disposition checker (round 14, w1)

Seat: `TameshiR14.Gate` (leaf executor). Owned path: `tools/evidence-disposition.py`.
No other lane, evidence, shared, or sibling file was written or edited.

## Delivered

`tools/evidence-disposition.py` (new, stdlib only, ~1950 lines incl. selftest).

CLI:

```text
evidence-disposition.py --root LANE --dispositions FILE [--json]
evidence-disposition.py --selftest
```

Exit map: `0` clean, `1` failed semantic expectation, `2` could-not-evaluate
(bad/missing/tampered/path-invalid input, invalid schema/type, unexpected
exception), `64` usage. Usage errors go to stderr; no JSON contract is claimed
for exit 64.

### Accepted dispositions document

Shape `evidence-dispositions-v1` with `expected_file`, `inputs`, `rows`.

- Effective row keys are exactly `{name,state="effective",receipt,check}`.
  `check` MUST equal `name`; a same-shaped check under another name
  (e.g. `pin_live -> pin_env_scrub`) yields `effective_check_name_mismatch`
  (exit 1).
- Superseded row keys are exactly
  `{name,state="superseded",reason,raw_receipt,raw_check,superseded_by}`.
  `raw_receipt`/`raw_check` are required; the raw observation is re-evaluated
  against the frozen expectation and must genuinely mismatch.
- Only `producer_before` may be superseded. Its replacements must be exactly
  `producer_before_oracle` and `producer_after_oracle`; both must be effective,
  `check == name`, bind `producer-oracle-repair.json`, and pass their original
  expectations. Extra replacements, self-targeting, chains, cycles, missing
  rows, unknown rows, and duplicate row names are findings.
- The oracle receipt must declare `supersedes` starting
  `verification.json producer_before`, and its `oracle_sha256` must equal
  `expected.inputs[".ufo/evidence/round-13/producer-oracle.py"]`.

`receipt`/`raw_receipt` are lane-relative canonical paths that must match an
`inputs` key and live beside `expected_file`. `inputs` must pin the expected
file plus `verification.json` and `producer-oracle-repair.json`. Every declared
pin is hashed first; `expected.inputs` (13 historical entries) is verified in
full before any predicate. Receipt-only checks are reported under
`informational.receipt_only_checks` and never become expectations.

### Predicate semantics

Only the original expected fields are enforced: `exit`, `contains`, `id`,
`reason`, `rows`, `statuses`, `result_reuse`.

- `exit` is recomputed from the receipt `check.exit` integer; bool is rejected.
  Receipt `expected_exit`/`exit_matches` are never read or trusted.
- `contains` is a literal substring of `check.stdout` only (never stderr).
- `id`/`reason` are exact top-level fields of one JSON object parsed from
  `check.stdout`; non-JSON yields `expected_stdout_not_json`.
- `rows` compares the expected count against top-level `rows` (int or list
  length), `counts.legs`, and `len(legs)`; all present sources must agree.
- `statuses` compares the expected histogram against top-level `statuses`,
  `counts`, and the per-leg `content_status` histogram; absent statuses count
  as zero.
- `result_reuse` compares the top-level value and every per-leg value.

`evaluate_expectation` aggregates all occurrences of one predicate ID into a
single finding per expectation, so finding IDs are unique per
(`id`, expectation).

### Output schema (JSON)

```json
{
  "schema": "evidence-disposition-result-v1",
  "tool": "evidence-disposition.py r14 (...)",
  "tool_sha256": "<self sha256>",
  "status": "clean | failed | could_not_evaluate",
  "exit": 0,
  "root": "<abs lane>",
  "dispositions": "<path as given>",
  "expected_file": ".ufo/evidence/round-13/expected.json",
  "counts": {"expected_checks": 12, "effective": 11, "superseded": 1,
             "passed": 11, "failed": 0, "findings": 0},
  "rows": [
    {"name": "...", "state": "effective", "receipt": "...", "check": "...",
     "expected_exit": 0, "observed_exit": 0, "outcome": "pass",
     "mismatches": []},
    {"name": "producer_before", "state": "superseded", "reason": "...",
     "raw_receipt": ".../verification.json", "raw_check": "producer_before",
     "raw_retained": true, "raw_expectation_failed": true,
     "raw_mismatches": ["expected_contains_missing"],
     "replacements": ["producer_before_oracle", "producer_after_oracle"],
     "outcome": "superseded", "mismatches": []}
  ],
  "findings": [{"id": "<stable id>", "expectation": "<name|null>", "detail": "..."}],
  "informational": {"receipt_only_checks": [{"receipt": "...", "check": "..."}]},
  "inputs_verified": ["..."],
  "expected_inputs_verified": ["..."]
}
```

Rows are emitted in `expected_checks` order; findings are sorted by
`(id, expectation, detail)`. Text mode prints one summary line, one `ROW` line
per expectation, and one `FINDING` line per finding. Exit-2 documents carry
`id`, `error.kind`, `error.message`, and one finding under the same stable ID.

Stable finding-ID families:

- Could-not-evaluate: `dispositions_missing`, `dispositions_unreadable`,
  `dispositions_json_invalid`, `schema_mismatch`, `dispositions_field_invalid`,
  `row_invalid`, `path_rejected`, `receipt_out_of_scope`, `input_unpinned`,
  `input_missing`, `input_unreadable`, `input_digest_mismatch`,
  `expected_file_missing`, `expected_json_invalid`,
  `expected_structure_invalid`, `expectation_invalid`,
  `expected_input_missing`, `expected_input_unreadable`,
  `expected_input_digest_mismatch`, `receipt_json_invalid`,
  `receipt_structure_invalid`, `receipt_check_invalid`,
  `receipt_check_duplicate`, `receipt_check_ambiguous`, `root_unavailable`,
  `internal_error`.
- Semantic: `row_missing`, `row_duplicate`, `row_unknown`,
  `effective_check_name_mismatch`, `receipt_check_missing`,
  `expected_exit_mismatch`, `expected_contains_missing`,
  `expected_stdout_not_json`, `expected_id_mismatch`,
  `expected_reason_mismatch`, `expected_rows_mismatch`,
  `expected_statuses_mismatch`, `expected_result_reuse_mismatch`,
  `supersession_not_permitted`, `superseded_reason_missing`,
  `superseded_raw_binding_mismatch`, `superseded_raw_missing`,
  `supersession_unwarranted`, `superseded_by_invalid`,
  `superseded_by_unknown`, `superseded_target_not_effective`,
  `superseded_required_replacement_missing`,
  `superseded_replacement_not_allowed`, `superseded_replacement_failed`,
  `superseded_cycle`, `superseded_oracle_binding_missing`.

### Safety properties implemented

- Every declared pin and expected input is read once through `O_NOFOLLOW`,
  `lstat`/`fstat` dev+ino compared, hashed, and parsed from the same cached
  bytes; no re-read between digest and predicate.
- Canonical lane-relative paths only: absolute, `..`, `.`, `\\`, NUL, `//`,
  trailing separators, non-canonical forms, symlink components, non-regular
  files, and paths resolving outside the lane are rejected.
- Strict JSON: UTF-8, duplicate keys rejected, `NaN`/`Infinity` rejected,
  top-level object required.
- Strict types: bool is not an exit in either expected or receipt; `statuses`
  values and `rows` must be non-negative ints; unknown expectation fields are
  rejected rather than silently ignored.
- Receipt argv is never read, validated for execution, or executed. The only
  `subprocess.run` calls are the selftest invoking this CLI and the two usage
  checks. A fixture receipt contains `sh -c "touch <marker>"`; the selftest
  asserts the marker is absent.
- Unexpected exceptions map to `internal_error` exit 2, never exit 1.

## Historical data read (static, no gate run)

Read directly from the lane before and after coding:

- `.ufo/evidence/round-13/expected.json`: **12** `expected_checks` keys,
  **13** `inputs` entries. All 13 input paths currently exist.
- `.ufo/evidence/round-13/verification.json`: 13 checks; all check `exit`
  values are ints and all `stdout`/`stderr` values are strings.
- `.ufo/evidence/round-13/producer-oracle-repair.json`: 2 checks, both typed as
  above; `supersedes` starts `verification.json producer_before`;
  `oracle_sha256` equals the `producer-oracle.py` digest in `expected.inputs`.
- Static predicate checks against the retained stdout:
  `pin_selftest` contains `SELFTEST: PASS (18/18)`; `metadata_selftest`
  contains `SELFTEST: PASS 39/39`; `producer_after` contains
  `WITNESS_SELFTEST: 41/41 pass`; `witness_check` contains
  `WITNESS_CHECK: CLEAN`; `witness_count` contains `witness_classified=10`.
  `metadata_old_null` is exit 1 with JSON `id=metadata_inconsistent`,
  `reason=normalized_kind_null`; `metadata_corrected` is exit 0 with
  `id=metadata_consistent`. `pin_live` is exit 0 with
  `counts={legs:6,unchanged:3,changed:3,unavailable:0}`,
  `len(legs)=6`, per-leg content_status changed3/unchanged3, and
  `not_established` on the top level and every leg.
  `producer_before` stdout does **not** contain
  `summary preserves top-level exposed declaration kind` (the path-layout
  crash happened first); both oracle rows contain their expected markers.
- `dispositions-before.json` and `dispositions.json` as landed by
  DispositionSpec: 12 rows each; before = 12 effective; after = 11 effective +
  `producer_before` superseded with `raw_receipt` verification.json,
  `raw_check` producer_before, and the two oracle replacements. All effective
  rows have `check == name`; all receipt/raw_receipt values are lane-relative
  and match the three `inputs` keys. This matches the parser's required shape.

## Selftest (defined, not executed by this seat)

`--selftest` builds only isolated fixtures under
`/tmp/tameshi-r14-evidence-disposition-selftest.*` and invokes this CLI via
`subprocess`; it never reads the real lane, historical evidence, sibling gates,
or receipt argv. The fixture expected set has 7 checks (dynamic enumeration, not
12/13), and each case asserts a literal exit code and exact finding-ID set.

34 cases are defined:

1. clean superseded (exit 0, no findings; informational receipt-only check)
2. unsuperseded crash mismatch (`expected_contains_missing`)
3. missing/drop row (`row_missing`)
4. unknown row (`row_unknown`)
5. duplicate row name (`row_duplicate`)
6. effective check identity (`effective_check_name_mismatch`)
7. cross-receipt ambiguous check (`receipt_check_ambiguous`)
8. self/cycle replacement (`superseded_cycle`,
   `superseded_replacement_not_allowed`, `superseded_target_not_effective`)
9. missing required replacement (`superseded_by_unknown`,
   `superseded_replacement_not_allowed`,
   `superseded_required_replacement_missing`)
10. replacement fails (`expected_contains_missing`,
    `superseded_replacement_failed`)
11. superseded reason empty (`superseded_reason_missing`)
12. raw check absent (`superseded_raw_missing`)
13. raw binding wrong (`superseded_raw_binding_mismatch`)
14. raw observation passes (`supersession_unwarranted`)
15. non-producer_before supersession (`supersession_not_permitted`)
16. oracle binding wrong (`superseded_oracle_binding_missing`)
17. exit-only false positive (`expected_contains_missing`)
18. id-only false positive (`expected_id_mismatch`)
19. rows/statuses/result_reuse mismatch (three IDs)
20. effective exit mismatch (`expected_exit_mismatch`)
21. receipt tamper (`input_digest_mismatch`)
22. expected input tamper (`expected_input_digest_mismatch`)
23. expected file missing (`expected_file_missing`)
24. receipt file missing (`input_missing`)
25. unpinned receipt (`input_unpinned`)
26. bool receipt exit (`receipt_check_invalid`)
27. bool expected exit (`expectation_invalid`)
28. duplicate receipt check (`receipt_check_duplicate`)
29. malformed dispositions JSON (`dispositions_json_invalid`)
30. duplicate JSON key (`dispositions_json_invalid`)
31. receipt path escape (`path_rejected`)
32. usage: no arguments (exit 64)
33. usage: `--selftest --json` (exit 64)
34. receipt argv never executed (marker absent)

No selftest, gate, or historical receipt was executed by this seat. The tally
is therefore **unobserved**; L1 owns the run and the tally. The expected design
tally is 34/34, but this report does not claim it as observed evidence.

## Checks L1 should run after all owners land

From `/home/vgpnk/Projects/shokunin/tameshi-shokunin`:

```sh
python3 tools/evidence-disposition.py --selftest
# expect exit 0 and a SELFTEST: PASS line; record the actual tally

python3 tools/evidence-disposition.py \
  --root /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --dispositions .ufo/evidence/round-14/dispositions-before.json --json
# expect exit 1; finding expected_contains_missing on producer_before;
# 12 effective, 11 passed, 1 failed, 0 superseded

python3 tools/evidence-disposition.py \
  --root /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --dispositions .ufo/evidence/round-14/dispositions.json --json
# expect exit 0 clean; 12 expected, 11 effective, 1 superseded,
# 11 passed, 0 failed, 0 findings; producer_before record has
# raw_retained=true, raw_expectation_failed=true,
# raw_mismatches=["expected_contains_missing"]; informational lists
# pin_env_scrub, metadata_emit, frozen_and_guardrail_unchanged
```

Also useful: confirm `inputs_verified` has 3 entries and
`expected_inputs_verified` has 13, and that exit-2 tamper behavior is limited to
the pinned bytes (`input_digest_mismatch`) before any predicate.

## Risks and limits

1. **Pins are configured authority, not authentication.** A dispositions file
   can pin a rewritten receipt and pass. L1/HistoricalIntegrity should compare
   the three pins against baseline/historical bytes. This seat made no
   authentication or preregistration claim.
2. **The 13 original `expected.inputs` digests are enforced in full.** Any
   round-14 edit to those historical tools/evidence files makes the gate exit 2
   by design. This seat changed none of them; only the new tool was added.
3. **Supersession policy is deliberately specific, not a framework.** Only
   `producer_before` may be superseded, only by the two named oracle rows, and
   only with the round-13 sibling receipt/oracle binding. That is the routed
   round-14 policy, not a general supersession engine.
4. **No verification was executed.** Correctness claims here rest on code review
   and static reads of the historical JSON. The selftest tally and the two real
   dispositions exits are predictions for L1 to observe.
5. `--dispositions` is resolved relative to the caller's cwd; `--root` is
   resolved to an absolute lane. No LSP operation was used (a single new stdlib
   file did not require symbol lookup/refactor); no LSP availability probe was
   made. No tools were installed or updated.
