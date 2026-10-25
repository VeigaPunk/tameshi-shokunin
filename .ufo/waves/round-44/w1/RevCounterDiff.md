# RevCounterDiff — round-44 counter delta review (C1 calibration)

Reviewer: L1Tameshi44.RevCounterDiff (leaf; no subagents). Scope: diff of the round-44 counter
against the round-43 counter at base.

- Round-44 counter (working tree): `.ufo/evidence/round-44/calibration/measure.py`, sha256
  `c0c6199fd6172df69326834eaad4884a27427fdd84cf79404dd5b1f44bd9c0d6` — identical to the freeze
  revision `ba01973c73ad7de60e5bd19ae08255a1b7ef917e` (`git show ba01973c...` byte-identical to
  working tree; `git status --porcelain` clean for this file) and matches the contract's
  `counter_sha256`.
- Round-43 counter: `git show 506e99c7b73c85711f066895984d501fcf7539cd:.ufo/evidence/round-43/calibration/measure.py`
  (514 lines) vs round-44 (558 lines).

## Diff summary (10 hunks, all accounted for)

| Hunk | Location (43 -> 44) | Change | Intended? |
|---|---|---|---|
| H1 | docstring line 1 (`@@ -1,5 +1,5 @@`) | Header relabel: "Round-43 C2 counter — record agreement, extended to two new classes" -> "Round-44 C2 counter — record agreement, successor of the round-43 counter" | Yes — (4) label change |
| H2 | docstring `@@ -12,9 +12,13 @@` | m7 prose updated: `staged:S###` / `Next unused id` / assignment-bound S-id (`key=S###`, `safe_floor=S256`) all masked; documents the round-44 fix | Yes — documents (1)/(2) |
| H3 | docstring `@@ -30,13 +34,13 @@` | `C2_R43_PASS` -> `C2_R44_PASS`; counting command path `round-43/` -> `round-44/` | Yes — (4)/(5) |
| H4 | `@@ -54,8 +58,8 @@` | `SELF_REL`, `CONTRACT_REL` -> `.ufo/evidence/round-44/...` | Yes — (5) |
| H5 | `@@ -82,8 +86,35 @@` | Adds `ASSIGN_ID = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*"?S\d{3,}"?')` (line 89) and the new function `m7_citations()` (lines 92-115) | Yes — (1)+(2) |
| H6 | `@@ -378,8 +409,29 @@` | Four new T6 selftest cases: `T6_safe_floor_value_not_citation`, `T6_assign_with_spaces_masked`, `T6_genuine_unknown_still_flagged`, `T6_unmined_flagged`; selftest print label `C2_R43_SELFTEST` -> `C2_R44_SELFTEST` | Yes — (3)/(4) |
| H7 | `@@ -404,7 +456,13 @@` | Pin lookup changed from `contract['claims']['C2']['counter_sha256']` to a loop over `contract['claims']` picking the first claim whose `counter == SELF_REL`, with a refusal if none | Yes — (6) |
| H8 | `@@ -446,21 +504,7 @@` | Inline m7 loop in `main()` replaced by `m7 = m7_citations(record_texts, registry_rows)` | Yes — (2) |
| H9 | `@@ -483,7 +527,7 @@` | Output field `C2_R43:` -> `C2_R44:` | Yes — (4) |
| H10 | `@@ -498,7 +542,7 @@` | `C2_R43_PASS=` -> `C2_R44_PASS=` | Yes — (4) |

**No unintended changes found.** Every hunk maps to exactly one of the six intended changes.

## Behavioral verification

1. **Refactor equivalence (H5/H8).** Old inline m7 used `mined_ids(registry)`; `m7_citations`
   computes `mined = {sid for sid, cells in registry_rows.items() if len(cells) > 7 and cells[7] == 'mined'}`
   from `registry_rows = rows(registry)` (main line 497). `mined_ids` (unchanged, lines 146-152)
   is exactly that predicate, so the mined-set is identical. Mask pipeline order identical
   (MASK_IDS skipping `next-free-phrase`/`safe-floor`, then VALUE_ID_AFTER, VALUE_ID_BEFORE)
   plus the new ASSIGN_ID pass. Hit format identical (`'<name> unknown <sid>'` / `'<name> unmined <sid>'`).
   Only semantic change to m7: assignment-bound S-ids are now masked.
2. **ASSIGN_ID mask (H5).** Regex allows spaces around `=` and an optional quote (`safe_floor=S256`,
   `safe_floor = S256`, `key="S123"`). It cannot match `staged_sha256=020fbeaa…` (value is not
   `S\d{3,}`). Issue `safe_floor=S256` is not caught by the prose `safe floor` masks (underscore),
   so this is the operative round-44 fix.
3. **Selftest (H6).** Round-43 counter `--selftest`: `cases=12 failed=0` PASS. Round-44 counter
   `--selftest`: `cases=16 failed=0` PASS. Exactly +4 cases (T6), all passing; T1–T5 unchanged and
   still green.
4. **Do-nothing control (mask removed).** Simulated the contract's control by executing the round-44
   source with the ASSIGN_ID sub-line removed: `m7_citations(rec_bad, reg)` flips from `[]` to
   `['r unknown S256']`, exactly matching the contract's `do_nothing_control` receipt claim.
5. **Pin discovery (H7).** The round-44 contract carries `counter_sha256` on C1 (`counter == SELF_REL`),
   not on C2; the loop finds it (pin = `c0c6199f...`). Base code would have raised KeyError on the
   round-44 contract; new code refuses cleanly when no claim names the counter. Deterministic: C1
   precedes C2 in the JSON object and only C1 has a `counter` field.

## Residual risk / verification gaps

- **ASSIGN_ID breadth (low).** Any `identifier=S###` token in the records is masked as a value. This
  is the contract's stated grammar ("an S-id bound to an assignment (key=S###) is a field value, not
  a citation"), so it is intended; a prose "cited from source=S777" style utterance would also be
  masked, but no such shape exists in the round-42/43 records reviewed.
- **First-match pin loop (low).** If a future contract has two claims naming the same counter, the
  first (insertion order) wins silently. Not reachable in the round-44 contract.
- **Not measured.** I did not run the full `measure.py --lane ... --rev ... --freeze ...` counting
  runs (that is the L1's deciding measurement); selftest and the mask-removed control are the only
  executions performed. At base, the round-43 counter still prints the C1 `before_state` line
  (m7=1/total=1) per the contract, not re-verified here.

## Tooling

No tools installed or upgraded (no install/update required for this review). Scratch:
`/tmp/tameshi-r44-RevCounterDiff-/` (diff artifacts: `round43_measure_at_base.py`,
`round44_measure_at_freeze.py`, `counter43_vs_44.diff`, `wt_vs_freeze.diff`).
