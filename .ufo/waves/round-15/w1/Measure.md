# Measure — round-15 C1 structural counter

Owner: `TameshiR15.Measure` (leaf). Scope written: `.ufo/evidence/round-15/measure.py`
(only). Report written here. No other file touched; no commit.

## Axes named

- **calibration** — make C1's before→after delta countable from committed bytes.
- **operability** — one command, one JSON document, no execution of what it measures.
- **history integrity** — make round-12..14 byte preservation a printed fact.
- **boundedness** — structural counts only; never dressed as a gate or selftest run.

## What was implemented

`.ufo/evidence/round-15/measure.py` is a stdlib-only, read-only counter over
committed blobs at `--rev REV`. It uses only `git rev-parse`, `git show` and
`git ls-tree` (`-C <lane root>`), never the worktree, never the context tool,
never a selftest, never a sibling gate. `--baseline` (default
`a9cf4da78f2514c7bedd91a850a88590009d7df0`, the round-15 claim baseline in
`.ufo/evidence/round-15/claims.json`) selects the revision whose historical
bytes must be preserved. Invalid resolution exits 2 with a
`could-not-evaluate` line; success prints one JSON object and exits 0.

### JSON fields (emitted, `indent=2`, `sort_keys=True`)

| Group | Fields | Structural meaning |
|---|---|---|
| identity | `revision`, `requested_revision`, `baseline_revision`, `scope` | resolved commit plus the no-execution caveat |
| active gate | `context_capture_present`, `context_capture_sha256`, `context_registry_rows`, `context_registry_kinds`, `context_historical_registry_rows`, `context_historical_registry_kinds`, `context_gate_kind_rows`, `context_probe_kind_rows`, `context_gate_active_classification` | `tools/context-capture.py` exists and a SKILL registry row whose `Kind` cell is `gate` names it; no active-path `probe` row exists |
| standalone selftest | `context_registry_selftest_command`, `context_selftest_flag_mentions`, `context_selftest_pass_marker`, `context_selftest_case_mentions`, `context_selftest_self_invocation_lines`, `context_standalone_selftest_present` | `--selftest` CLI mention and `SELFTEST: PASS` marker in the tool blob; self-invocation lines counted as informational evidence |
| exit-64 classes | `context_64_classes`, `context64_registry_could_not_evaluate`, `context_tool_64_class_lines`, `context_tool_64_samples`, `context64_tool_could_not_evaluate`, `context64_explicit_class`, and the same `disposition64_*` family, plus `explicit64_classes_declared` | each tool's registry verdict cell (and/or tool exit map) maps `64` to `could-not-evaluate` in the same clause |
| sources | `source_rows`, `source_malformed`, `source_tiers`, `source_statuses`, `sources_sha256` | current SOURCES registry counts and histograms; malformed rows counted, never silently dropped |
| runner | `runner_recorded_cases`, `recorded_cases` (round-14-compatible alias), `runner_cases_six`, `runner_sha256`, `runner_sha256_matches_round14_published`, `frozen_summary_sha256`, `frozen_summary_sha256_matches_round14_published` | six recorded cases and the two published round-14 digests (`75ed934d…`, `acc01268…`) still match |
| SHONEN | `shonen_marks_total`, `shonen_states`, `shonen_scored_boxes`, `shonen_excluded_boxes`, `shonen_restrained_boxes_excluding3`, `calibration_restraint_score` | fixed adjudication: boxes `(1,2,4)` counted, box `3` excluded; score is `2 × restrained` |
| history | `historical_script_sha256`, `historical_receipt_sha256`, `historical_digests` (script, receipt, frozen summary, runner), `historical_evidence` | sha256 of the round-14 script/receipt plus per-path preserved-at-baseline booleans and a blob-identity comparison of every path under `.ufo/evidence/round-12|13|14` |

`historical_evidence.all_baseline_bytes_preserved` is `1` only when every
baseline-reported historical blob has the identical committed object at
`--rev`; additions under historical dirs are listed separately, never folded
into preservation. At baseline `a9cf4da` the historical tree has 599 paths and
`tools/context-capture.py` is absent (`git cat-file -e` exit 128, read-only
check).

## Behavior at the two revisions (expected semantics, not executed here)

- Before (`--rev a9cf4da…`): `context_capture_present 0`,
  `context_gate_active_classification 0`, `context_standalone_selftest_present 0`,
  `explicit64_classes_declared 0`, `runner_recorded_cases 6`,
  `calibration_restraint_score 6`, `all_baseline_bytes_preserved 1`.
  `source_rows` should be 48, the round-14 closure's independently remeasured
  delivered value; this counter was not run to confirm it here.
- After (delivered round-15 revision): the same six-case / restraint / history
  invariants must still print, while
  `context_capture_present 1`, `context_gate_active_classification 1`,
  `context_standalone_selftest_present 1`, and
  `explicit64_classes_declared 2` become the C1 structural delta.

These are structural predicates. They do not prove the selftest runs, that its
literal expected exits/findings fire, or that the gate passes; only the L1
single execution of the tool and its retained receipt can.

## Evidence retained

- File: `.ufo/evidence/round-15/measure.py` (13 KB, executable; written this wave).
- Read-only baseline facts established without running the counter:
  `git cat-file -e a9cf4da…:tools/context-capture.py` → exit 128 (absent);
  `git ls-tree -r --name-only a9cf4da… -- .ufo/evidence/round-12 .ufo/evidence/round-13 .ufo/evidence/round-14`
  → 599 paths.
- Published round-14 digests used as constants are the values re-read from
  `corpus/lessons/round-14-verifier-spotcheck.md` and independently confirmed by
  `sha256sum` over the current committed runner and frozen summary.
- No gate, selftest, sibling instrument or build/lint/test was executed by this
  seat. No package was installed.

## Exact bounded recommendations

1. **Registry seat:** register the active row with `Kind = gate`, an entry cell
   naming `tools/context-capture.py`, a self-test cell containing `--selftest`,
   and a verdict cell stating `64 could-not-evaluate (usage)` for both the
   context tool row and the `evidence-disposition.py` row. The counter reads
   the registry row's entry and verdict cells literally; a row that still names
   only `.ufo/evidence/round-14/capture-context.py` will not count as the
   active gate.
2. **ContextGate seat:** keep the lane convention `--selftest` plus the
   `SELFTEST: PASS` marker, and retain literal expected exit/finding pairs in
   the selftest. If a different pass marker is used, rely on
   `context_selftest_flag_mentions` / `context_selftest_case_mentions` rather
   than `context_standalone_selftest_present`; the appropriate fix is to keep
   the existing convention, not to weaken the counter.
3. **L1:** run exactly twice after the wave lands:
   `python3 .ufo/evidence/round-15/measure.py --rev a9cf4da78f2514c7bedd91a850a88590009d7df0`
   and the same with `--rev <delivered>`. Record both JSON documents; the
   before→after pair is the C1 structural receipt. Run the tool's own
   `--selftest` once separately — the counter never stands in for it.
4. **L1:** if the delivered baseline differs from `claims.json`, pass
   `--baseline <rev>`; do not edit the default constant post hoc without
   saying so in the report.

## Risks / limits

- Predicates depend on the literal vocabulary chosen by the registry/tool
  seats (`gate`, `64 could-not-evaluate`, `--selftest`, `SELFTEST: PASS`).
  Raw counts and samples are printed alongside every boolean so a wording
  miss is visible rather than silently false.
- `source_rows` requires the 11-cell SOURCES row shape; deviations land in
  `source_malformed`.
- The historical comparison is over committed blobs only; worktree state is
  deliberately unmeasured.
- Static counts are not runtime proof and create no admission credit.

## Blockers

None. No implementation-critical detail required a message to L1.
