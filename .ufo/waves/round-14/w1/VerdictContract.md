# VerdictContract — round-14 w1 (contract-only review)

Seat: `TameshiR14.VerdictContract` (reviewer, leaf). Lane: tameshi-shokunin.
Scope: proposed gate exit lattice and stable finding-id contract for `tools/evidence-disposition.py` (Gate) and the `evidence-dispositions-v1` schema, reviewed against the protocol Gate standard.

## Status and basis

- **Contract-only.** `tools/evidence-disposition.py` does not exist at review time (`read` returned not found; `tools/` lists `pin-disposition.py`, `witness-metadata.py`, `bash-witness-study.py`, `repeat-control.py` only). No code was read, and nothing was executed: no gate run, no selftest, no tests, builds, lint, or receipt argv. Findings below judge the retained contract and the retained round-13 evidence bytes.
- **Tooling:** no installs or updates. One `web_search` was used to confirm argparse exit-status behaviour (see H3).
- **Not an independent verification.** This is a leaf reviewer's read of the contract.

Sources read: `AGENTS.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/lessons/round-13-verifier-spotcheck.md`, `.ufo/waves/round-14/spec.json` (context, Interfaces), `.ufo/evidence/round-14/claims.json`, `.ufo/evidence/round-13/expected.json`, `.ufo/evidence/round-13/verification.json`, `.ufo/evidence/round-13/producer-oracle-repair.json`, `corpus/knowledge/repeated-control-precondition.md` §2–3, `corpus/knowledge/gates-survey-kagi.md` (§7 items 1–5), `corpus/knowledge/service-optin-protocol.md` (U4), `tools/witness-metadata.py` (exit map and verdict-id mapping), `tools/repeat-control.py` (last-finding-id; selftest exception path), and the protocol Gate standard at `kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md` lines 388–424.

## Protocol conformance of the proposed lattice

Protocol Gate standard (`PROTOCOL.md:393-419`):
- `0` = clean and `1` = failed fleet-wide. Every other code must be declared in the registry and mapped to `clean | failed | could-not-evaluate`. An undeclared nonzero code reads as could-not-evaluate.
- Self-test must assert both exit and a stable finding-id, with expected values committed in the owning repo and independent of recomputation. A helper-only self-check does not satisfy this.
- A gate whose verdict depends on mutable artifacts ships a run over committed inputs with a committed expected verdict. Its `expected.json` pins every input digest, and an edited input is `snapshot_tampered` (could-not-evaluate), never a compared verdict.
- A verdict names the revision it was measured against (`PROTOCOL.md:406-407`).
- Registry row required: name, `gate|probe`, entry command, verdict map, self-test command and spelling, pinned-value path, write scope, owner (`PROTOCOL.md:411-419`).

The shape 0/1/2/64 is protocol-conformant. The gaps are in what the contract leaves unspecified.

## Findings by severity

### High — must resolve before implementation

**H1. The "All13" row count contradicts the frozen expectation file.** Spec Interfaces say "Enumerate expected_checks exactly once" and "All13 expected rows effective except producer_before superseded". The frozen `.ufo/evidence/round-13/expected.json` `expected_checks` has **12** keys (lines 19–74): pin_selftest, metadata_selftest, metadata_old_null, metadata_corrected, producer_before, producer_before_oracle, producer_after_oracle, producer_after, witness_check, witness_count, pin_live, source_census. The number 13 matches neither the expected keys nor the expected file's inputs (13 entries, lines 5–17). It matches `verification.json` `checks` (13 entries). Consequence: an implementer either invents a 13th row, violating "no unexplained rows", or cannot satisfy the acceptance as written. **Fix:** rows = the 12 `expected_checks` keys, exactly once each; after state = 11 effective + `producer_before` superseded. Do not edit `expected.json`.

**H2. Uncaught exceptions would exit 1.** Python's default for an unhandled exception is exit 1, which the contract defines as "failed semantic expectations". A malformed receipt, a `UnicodeDecodeError` on receipt stdout, or a `KeyError` in a predicate would therefore read as a semantic failure. The sibling precedent exists precisely for this: `repeat-control` declares `setup_error` (could-not-evaluate) so no uncaught exception exits 1 (`corpus/knowledge/repeated-control-precondition.md` §3.1; `tools/repeat-control.py:185-188`, selftest catch-all `:857-861`). **Fix:** a top-level catch-all that maps any unexpected exception to exit 2 with ID `setup_error`, emitting the JSON document when `--json` is set.

**H3. argparse usage errors would exit 2, not 64.** The stdlib `ArgumentParser.error()` prints usage and exits with status 2; a subclass must override `error()` to change this (argparse docs, https://docs.python.org/3/library/argparse.html, cited via `web_search`). Spec requires usage = 64. Without an override, a usage error is indistinguishable from could-not-evaluate by exit code, and only the ID differs. **Fix:** a parser subclass whose `error()` exits 64 with ID `usage_error`. Decide and state `--help` exit (0 is conventional; it is not a verdict).

**H4. The stable finding IDs are never enumerated.** Spec says "Output stable finding IDs" but names none. Protocol requires committed expected finding-ids that the selftest asserts independently. Without a table, the selftest cannot be specified, and the C1 claim ("same command rejects old unresolved row") is not checkable. **Recommended table** (this is a proposal to decide before code, not an observation):

| ID | Exit | Class | Trigger |
|---|---|---|---|
| `disposition_clean` | 0 | clean | all 12 rows dispositioned; effective rows pass; superseded rows satisfy their replacement requirement |
| `expectation_failed` | 1 | failed | an effective row's check violates its original predicate, or a superseded row's replacement does not pass (prefer per-predicate sub-IDs, e.g. `exit_mismatch`, `contains_missing`, `field_mismatch`, so the before-run names the row and predicate) |
| `snapshot_tampered` | 2 | could-not-evaluate | any digest mismatch in `inputs` or original `expected.inputs` (name aligned with `witness-metadata.py` and `repeat-control`) |
| `input_unavailable` | 2 | could-not-evaluate | expected file, receipt, or disposition file missing |
| `input_malformed` | 2 | could-not-evaluate | JSON or schema error, unknown key, wrong type, duplicate JSON key |
| `path_escape` | 2 | could-not-evaluate | absolute path, `..`, symlink, or resolution outside `--root` |
| `receipt_ambiguous` | 2 | could-not-evaluate | duplicate `check` name within one receipt |
| `disposition_ledger_invalid` | 2 | could-not-evaluate | missing, duplicate, or unknown row; replacement not named |
| `superseded_raw_missing` | 2 | could-not-evaluate | superseded row without retained observed raw receipt/check |
| `setup_error` | 2 | could-not-evaluate | any uncaught exception (H2) |
| `usage_error` | 64 | could-not-evaluate | invalid arguments (H3) |

Open decisions the spec must settle: (a) whether a dependency cycle in `superseded_by` is 1 or 2 (recommend 2, since a ledger whose graph cannot be evaluated is unevaluable input); (b) whether `input_malformed` and `path_escape` stay separate IDs (recommend separate, same exit).

**Precedence rule (missing from spec).** Any could-not-evaluate condition short-circuits: report that ID and emit no semantic verdict. Semantic `1` is emitted only after all inputs are digest-verified and the ledger is complete. Spec already says "verify every original expected.inputs digest too before predicates"; make the short-circuit explicit so a tampered input plus a mismatch never yields exit 1.

**H5. The C1 rejection must be classified as exit 1, not 2.** With `dispositions-before.json` (`producer_before` effective), the honest outcome is exit 1 on `producer_before`: the expected contains string `summary preserves top-level exposed declaration kind` is absent from the raw run's stdout, while exit matches 1 and stderr holds a traceback (`verification.json` `producer_before`, lines 81–94). If the implementation routes this through a ledger or input error, it still "rejects" but misclassifies, and the C1 "rejects the old unresolved row" claim is then wrong for the stated reason. **L1 check:** exit exactly 1, and the finding names `producer_before`.

**H6. Structured-predicate field mapping is undefined, and one field name does not exist in the evidence.**
- `pin_live.rows: 6` (expected.json line 63): the pin-disposition JSON carries `counts.legs = 6` (`verification.json` line 150); there is no `rows` key.
- `pin_live.statuses: {unchanged:3, changed:3, unavailable:0}` maps to `counts.{unchanged,changed,unavailable}`, not a `statuses` key. The mapping must be written down.
- `metadata_old_null` `id`/`reason` are top-level JSON keys of a single-line JSON stdout (`verification.json` line 60). `pin_selftest`, `metadata_selftest`, `witness_count` are text lines; `pin_live` is multi-line pretty JSON, so a last-line rule cannot parse it.
- Spec says "using parsed check.stdout" with no parse mode. Each expectation needs a declared parse mode: whole-document JSON, last-non-empty-line (kagi precedent, `gates-survey-kagi.md` §7 item 4; repeat-control `last_finding_id`, `tools/repeat-control.py:559-562`), or raw substring for `contains`.

**Dependency on mutable tools.** The Gate's verdict includes digest checks on `tools/pin-disposition.py`, `tools/witness-metadata.py`, `tools/bash-witness-study.py`, and `tools/mutate-and-run.sh` (expected.json `inputs`). Any later edit to those tools turns the round-13 verdict into `snapshot_tampered` (exit 2). That is consistent with the protocol but must be understood by L1 as a tamper, not a regression.

### Medium

**M1. Receipt-to-row binding is ambiguous.** `receipt` is "receipt files verification.json and producer-oracle-repair.json", but the row field form (path or label) is unspecified. Check locations: `producer_after`, `pin_live`, `witness_count` and the other seven original expected rows are in `verification.json`; only `producer_before_oracle` and `producer_after_oracle` are in `producer-oracle-repair.json`. Three receipt checks are referenced by no expected row: `pin_env_scrub`, `metadata_emit`, `frozen_and_guardrail_unchanged` (`verification.json` lines 154–219). Specify that unreferenced receipt checks are listed as `unreferenced` in output and do not gate. Silent omission risks a reader believing they were judged.

**M2. Receipt self-reported `exit_matches` must not be trusted.** Recompute from `exit` against the expected exit. The digest pin protects the bytes; the gate must still not read a convenience boolean as evidence.

**M3. JSON hazards.** Python `json` keeps the last of duplicate keys silently, so a duplicated `"state"` or `"exit"` key can mask a change. Reject duplicates with `object_pairs_hook`. Python `True == 1`: use a type-strict comparison (`type(x) is int`) for exit and counts, so `exit: true` cannot satisfy `exit: 1`.

**M4. Path containment.** Spec says "relative path" for `expected_file` and `inputs`, but does not forbid absolute paths, `..`, or symlinks. Repeat-control rejects symlinked snapshot inputs (`repeated-control-precondition.md` §3.1). Resolve under `--root` and reject escape with `path_escape`. Also specify whether `--dispositions FILE` resolves against cwd or `--root`.

**M5. Revision naming.** Protocol requires the verdict to name the revision it was measured against (`PROTOCOL.md:406-407`). Spec's output contract does not include it. Add lane HEAD (or an explicit `no-git` marker) plus the digests of the expected file and disposition file to the JSON output.

**M6. Selftest contract is underspecified.** Spec says "Isolated selftest invokes own CLI via subprocess and checks exit plus stable IDs" (good). Missing: selftest exit code (recommend 0 all cases match ID and exit, 1 any mismatch, 2 fixture-build failure); fixtures must be built under a temp root and never default to the live tree; the expected-ID table must be a literal in the script, not derived from the predicate code under test.

**M7. Committed expected verdict for the frozen before/after runs.** Protocol requires a committed expected verdict for a run over a mutable artifact. `dispositions-before.json` should exit 1 with `expectation_failed` on `producer_before`; `dispositions.json` should exit 0 with `disposition_clean`. Neither expectation is committed in the spec. Without a sidecar or in-file expected verdict, the before-run exit 1 is observed but not pinned.

**M8. Registry row missing (protocol debt).** Protocol requires the registry row (`PROTOCOL.md:411-419`). For tameshi the registry home is the lane `SKILL.md`, which this seat must not touch. Until the owner adds it, the 64 and new IDs are "undeclared → could-not-evaluate" by default. Record as owned debt for L1 or the lane owner; it does not block exit behaviour.

**M9. Verdict line.** Emit a final stdout line `EVIDENCE_DISPOSITION: <ID>` in text mode, matching the last-non-empty-line convention (repeat-control `last_finding_id`; kagi §7 item 4), so text-mode callers have the same discriminator as `--json`.

**M10. Read-only guarantee.** Gate must write nothing and must never invoke `pin-disposition.py` or any receipt argv. Verify by tree digest before and after a run (L1 check below).

### Low

**L1. `source_census` is exit-only** (`expected.json` lines 71–73). Exit-flatten risk: the `service-optin-protocol.md` U4 note says an exit-only adjudicator cannot kill that family. Accept as a stated residual, or add a stdout predicate in a new expectation.

**L2. "13" probably conflates counts.** `expected.json` has 13 `inputs` and `verification.json` has 13 `checks`; neither is the expected-row count (12). Correct the spec prose to 12 rows.

**L3. Before/after diff discipline.** `dispositions.json` must differ from `dispositions-before.json` only in `producer_before` state, reason, and `superseded_by`. The gate cannot enforce this (no baseline); L1 enforces it with `diff`.

## Must-have failure paths (selftest and L1 fixtures; design only, not run)

1. Canonical after file → exit 0, `disposition_clean`.
2. Before file (`producer_before` effective) → exit 1, `expectation_failed` on `producer_before`, all other 11 rows pass. Exit must be 1, not 2 (H5).
3. One byte edited in `expected.json` → exit 2, `snapshot_tampered`, before any predicate.
4. One byte edited in `verification.json` → exit 2, `snapshot_tampered`.
5. One byte edited in `producer-oracle-repair.json` → exit 2, `snapshot_tampered`.
6. Missing receipt → exit 2, `input_unavailable`.
7. Duplicate `check` name in a receipt → exit 2, `receipt_ambiguous`.
8. Ledger with 11 rows, or 13 rows with an unknown name → exit 2, `disposition_ledger_invalid`.
9. Duplicate row name → exit 2, `disposition_ledger_invalid`.
10. Superseded `producer_before` without retained raw check → exit 2, `superseded_raw_missing`.
11. `superseded_by` naming only one replacement → exit 2, `disposition_ledger_invalid`.
12. Replacement row effective but failing (e.g. `producer_after_oracle` exit 1) → exit 1, `expectation_failed`.
13. `superseded_by` cycle or pointing to a superseded row → exit 2 (per decision (a)).
14. Receipt `exit: true` against expected 1 → exit 1 with type-strict mismatch, never a pass.
15. Duplicate JSON key in dispositions → exit 2, `input_malformed`.
16. Invalid UTF-8 in receipt stdout → exit 2, not a traceback exit 1 (H2).
17. Absolute path, `..` component, or symlink in `inputs` → exit 2, `path_escape`.
18. Unknown argument → exit 64, `usage_error` (not 2, H3); no arguments → 64.
19. Injected exception in a predicate → exit 2, `setup_error`.
20. Tamper plus mismatch in the same input → exit 2 only (precedence).
21. Receipt `exit_matches` false while exit matches → ignored, verdict follows recomputed exit.
22. Receipt argv pointing at a sentinel-creating command → sentinel absent after run (never executed).
23. Tree digest of the fixture root unchanged after a run (read-only).
24. Finding IDs and JSON key order identical across two runs (stability).

## Checks L1 should run after all seats finish (not run here)

- `python3 tools/evidence-disposition.py --root <LANE> --dispositions .ufo/evidence/round-14/dispositions.json --json; echo $?` → expect 0 and `disposition_clean`.
- Same with `dispositions-before.json` → expect exit 1, `expectation_failed`, `producer_before` named, and not exit 2.
- `python3 tools/evidence-disposition.py --selftest; echo $?` → expect 0; output contains every ID in the table above.
- `python3 tools/evidence-disposition.py --bogus; echo $?` → expect 64.
- Before any gate run and after: sha256 of `.ufo/evidence/round-12/`, `.ufo/evidence/round-13/`, `tools/*` (historical), and `git diff --quiet` of those paths against the stated baselines; old raw evidence must be byte-identical.
- `diff .ufo/evidence/round-14/dispositions-before.json .ufo/evidence/round-14/dispositions.json` → only `producer_before` state, reason, `superseded_by` differ (L3).
- Confirm the four live tool digests in `expected.json` `inputs` still match at check time; if one moved, the expected outcome is `snapshot_tampered`, not a regression.
- Confirm the registry row (M8) is owned and scheduled, or record it as debt.

## Residual risk

- Exit-only expectation `source_census` (L1). Accepted residual unless changed.
- Gate depends on live tool digests for tamper detection; tool edits in later rounds will flip verdicts by design.
- The 13-vs-12 discrepancy (H1) is a spec-prose error, not a frozen-evidence error; the frozen file is internally consistent with 12 expected checks and 15 receipt checks (13 + 2).

## Verified-in-evidence (positive, not run)

- `producer_before_oracle` retained stdout contains `check summary preserves top-level exposed declaration kind FAIL` and `WITNESS_SELFTEST: 40/41 pass`, `VERDICT: FAIL`, exit 1 (`producer-oracle-repair.json` line 20) — satisfies its expected predicate.
- `producer_after_oracle` retained stdout contains `WITNESS_SELFTEST: 41/41 pass`, `VERDICT: PASS`, exit 0 (`producer-oracle-repair.json` line 37) — satisfies its expected predicate.
- `verification.json` contains `SELFTEST: PASS (18/18)` (pin_selftest), `SELFTEST: PASS 39/39` (metadata_selftest), `witness_classified=10` (witness_count), and `"result_reuse": "not_established"` (pin_live). The `metadata_old_null` JSON carries `id: metadata_inconsistent`, `reason: normalized_kind_null`.

Result: the lattice shape is protocol-conformant. Before implementation: fix the row count (H1), require ID table and precedence (H4), resolve argparse and catch-all exits (H2/H3), define predicate parse modes and field mapping (H6), and commit before/after expected verdicts (M7).
