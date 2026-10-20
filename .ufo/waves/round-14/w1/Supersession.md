# Round 14 — Supersession graph semantics audit (W1 / Supersession)

Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin. Baseline d6809df7775338f000e44c8a916067b8866867fb.

## Status

- **Contract-only** for the gate and disposition files. `tools/evidence-disposition.py` does not exist in the working tree; `.ufo/evidence/round-14/dispositions*.json` do not exist. Only `.ufo/evidence/round-14/claims.json` is present (untracked).
- Frozen round-13 inputs were read (read-only). No checks, selftests, or gates were executed. No files other than this report were written. Tool installs/updates: none.
- Read-only observations below are from parsing committed-frozen JSON and SHA-256 of files already on disk.

## Observed facts (frozen round-13 evidence)

| Fact | Observation | Source |
|---|---|---|
| expected_checks cardinality | **12** keys: pin_selftest, metadata_selftest, metadata_old_null, metadata_corrected, producer_before, producer_before_oracle, producer_after_oracle, producer_after, witness_check, witness_count, pin_live, source_census | `.ufo/evidence/round-13/expected.json` |
| expected.inputs cardinality | 13 entries; all 13 match the current working tree (mismatches = []) | same, recomputed read-only |
| Raw `producer_before` | exit 1 (= expected exit 1); stdout (1938 chars) **does not contain** `summary preserves top-level exposed declaration kind`; stderr is `FileNotFoundError ... .ufo/evidence/tools/mutate-and-run.sh` | `.ufo/evidence/round-13/verification.json`, check `producer_before` |
| Raw check names in verification.json | 13 names, no duplicates; contains **no** `producer_before_oracle` / `producer_after_oracle` | same |
| Repair receipt names | `producer_before_oracle` (exit 1, stdout ends `kind FAIL`, `WITNESS_SELFTEST: 40/41 pass`) and `producer_after_oracle` (exit 0, `WITNESS_SELFTEST: 41/41 pass`); no other checks | `.ufo/evidence/round-13/producer-oracle-repair.json` |
| Repair `supersedes` field | free-text prose string, not structured | same |
| pin_live stdout | parses as JSON; top-level `result_reuse`=`not_established`; `legs` length 6 (changed 3 / unchanged 3); status tally lives under key `counts`, not `statuses` | `verification.json`, check `pin_live` |
| metadata_old_null / metadata_corrected stdout | parse as JSON; top-level `id`/`reason` present (`metadata_inconsistent`/`normalized_kind_null`; `metadata_consistent`/`ok`) | same |
| Replacement invocation | `producer-oracle.py` copies `--source` into a temp `tools/` layout and runs its selftest; it is **not** the raw argv (`producer-before.py selftest` from the lane root) | `producer-oracle.py` |

## Findings (by severity)

### F1 — HIGH: row-count contract is wrong in the assignment
The spec says "All13 expected rows effective except producer_before superseded". `expected.json` has **12** `expected_checks`; 13 is the `inputs` count. A gate that enforces exactly-once enumeration against 13, or a DispositionSpec that emits 13 rows, either fails or invents an unknown row.
**Change:** 12 rows: 11 effective + `producer_before` superseded. Assert `set(rows.name) == set(expected_checks)` with no duplicates.

### F2 — HIGH: superseded schema has nowhere to retain the observed raw receipt/check
Spec schema for superseded rows is `name/state/reason/superseded_by`. The requirement "superseded producer_before must retain observed raw receipt/check" has no field, so it is unenforceable as written.
**Change:** add explicit `raw_receipt` (path, pinned in `inputs`) and `raw_check` (name) to the superseded row. The gate then verifies: the raw check name occurs exactly once in that receipt; `exit == expected.exit`; and `contains` is absent from `stdout` (see F3).

### F3 — HIGH: no guard against superseding a row that already passes
Nothing in the spec prevents a superseded row whose raw observation satisfies its original expectation. That would let a passing row be relabeled and silently dropped.
**Change:** for superseded rows, require the raw observation to **fail** its original predicate (exit or contains/id/reason/rows/statuses/result_reuse mismatch). If it passes, emit a finding (exit 1) — supersession is unnecessary.

### F4 — MEDIUM: replacement is a different invocation; gate proves only passing, not equivalence
`producer_before_oracle` runs a relocated copy of the source (`tools/` layout in a temp dir). It proves the red-before mechanism on that layout; it does not prove the original raw command. The gate can verify that both replacements pass their original expectations, but not equivalence.
**Change:** the `reason` text must state this explicitly (relocated-fixture replacement; raw crash retained; raw argv not re-proven). Do not let the gate or closure present "exit_matches alone" as mechanism proof (round-13 routed item 1).

### F5 — MEDIUM: structured-predicate mapping is undefined and will fail pin_live
Expected uses `rows` and `statuses`; stdout has `legs` (list) and `counts` (object). Without a declared mapping, `pin_live` fails with "missing key".
**Change:** declare the mapping in the gate: `rows` → `len(stdout.legs)`; `statuses` → `stdout.counts` compared as an exact dict; `result_reuse` → top-level `stdout.result_reuse`; `id`/`reason` → top-level of parsed stdout JSON. Apply `contains` to `stdout` only, never stderr. Parse failure on a structured predicate → finding (exit 1) if stdout is present but not JSON; exit 2 only for missing/unreadable receipt.

### F6 — MEDIUM: cycle/chain guard must be explicit, not implied
Requiring both replacements to be effective prevents a chain only if the gate checks it. The spec does not state the check.
**Change:** for each superseded row: `superseded_by` is a non-empty list, no duplicates, no self-reference, every target exists in rows with `state == effective`, and the set equals exactly `{producer_before_oracle, producer_after_oracle}`. Any target superseded → finding (cycle/chain). Unknown target → exit 2 or finding per a fixed table; pick one and state it.

### F7 — MEDIUM: receipt binding must be per-row, not a global name search
Names are disjoint across the two receipts today (`producer_after` only in verification.json; `producer_before_oracle` / `producer_after_oracle` only in the repair receipt), but a global search would silently accept a same-named check in the wrong receipt if one were added.
**Change:** every effective row carries an explicit `receipt` path; lookup is restricted to that receipt's `checks` and must be unique there.

### F8 — MEDIUM: never trust self-reported `exit_matches`
Both receipts contain `exit_matches` booleans. They are derived by the producing tool, not by the gate.
**Change:** recompute `exit == expected.exit` in the gate. Do not read `exit_matches`.

### F9 — LOW: `supersedes` prose in producer-oracle-repair.json is not machine-usable
**Change:** the gate must not parse it. The link lives only in the dispositions row (`superseded_by` + `raw_receipt`/`raw_check`).

### F10 — LOW / info: input pins are fail-closed, and that must be documented
All 13 expected inputs currently match the working tree. Any later edit to `tools/*.py` or `tools/mutate-and-run.sh` makes the frozen expectation set exit 2 (could-not-evaluate), which is the intended tamper signal. Document that round-13 dispositions become non-reproducible after a runner change.

### F11 — INFO: `pin_env_scrub` has argv identical to `pin_live`
It is not an expected row, so the gate must not enumerate it. The GIT_DIR-poisoning claim belongs to ReceiptHarness, not to the disposition ledger.

## Minimal implementation guard (recommended)

1. Strict schema: unknown keys in dispositions → exit 2. `schema == evidence-dispositions-v1`.
2. Rows: `set(names) == set(expected_checks)`, no duplicates, no unknown names.
3. Before any predicate: recompute sha256 for `expected_file`, every receipt in `inputs`, and every `expected.inputs` entry. Mismatch/missing → exit 2.
4. Effective row: receipt is explicit and in `inputs`; unique `checks[name]` in that receipt; recompute exit; `contains` on stdout; structured predicates per F5 mapping; never execute argv.
5. Superseded row: non-empty `reason`; `raw_receipt`/`raw_check` pinned and unique; raw exit == expected exit and raw stdout lacks the expected marker (raw must **fail**, F3); `superseded_by` exact-set + all effective (F6); both replacements pass their original expectations.
6. Output: stable finding IDs (one fixed table), per-expectation disposition, mismatch details; exit 0 clean / 1 semantic failure / 2 could-not-evaluate / 64 usage.

## Checks for L1 to run (not run by this seat)

- `python3 tools/evidence-disposition.py --selftest` (exit 0; stable IDs for each negative fixture).
- `python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions-before.json --json` → expect **exit 1**, finding for `producer_before` contains mismatch.
- Same with `dispositions.json` → expect **exit 0**; diff of the two files must be only the `producer_before` row (state, reason, superseded_by, raw_*).
- Negative mutants (each must fail with the expected exit/ID): unknown superseded target; self-loop; superseded target that is itself superseded; raw that passes its expectation; replacement that fails; missing receipt digest; tampered `verification.json` (exit 2); dropped row (exit 1); 13th unknown row (exit 1).
- `git diff --quiet 546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50 -- .ufo/evidence/round-13 tools/mutate-and-run.sh SHONEN.md` → clean (historical bytes preserved).

## Residual risk / gaps

- Gate and DispositionSpec outputs are not yet on disk; every claim above about them is contract-level.
- Supersession validates passing replacements, not equivalence to the raw command (F4).
- Structured-predicate mapping (F5) is my proposal; the spec does not define it.
