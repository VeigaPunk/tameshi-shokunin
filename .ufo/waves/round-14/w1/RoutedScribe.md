# RoutedScribe — round-13 routed defects 1–5: disposition checklist

Lane: tameshi-shokunin (round 14, wave w1). Author seat: TameshiR14.RoutedScribe (leaf, read-only).
Source under review: `corpus/lessons/round-13-verifier-spotcheck.md` (`## Routed defects and residuals`, items 1–5, lines 175–183).
Scope of this report: a checklist and evidence pointers only. No file other than this report was written. No gate, selftest, runner, build, or verification was executed. Tools installed/updated: none.

Status key: **open** = no change in the tree that discharges the item; **planned** = round-14 artifact named in the assignment but not present when this report was written.

Presence check at write time: `tools/` tracks only `bash-witness-study.py`, `mutate-and-run.sh`, `pin-disposition.py`, `repeat-control.py`, `witness-metadata.py` (no `evidence-disposition.py`). `.ufo/evidence/round-14/` holds only `claims.json`. `.ufo/waves/round-14/w1/` held only `swarm-registry.json` before this file.

## Checklist

| # | Routed defect (lesson wording, condensed) | Owner (round-14 roster) | Status | Evidence pointers (verified by read) | Required next action |
|---|---|---|---|---|---|
| 1 | `expected.json` `expected_checks.producer_before` asks the relocated raw command to contain the kind assertion; that raw run crashed before the assertion. Supersession is valid but a naive reader sees a mismatch. | DispositionSpec (writes `dispositions-before.json`, `dispositions.json`); Gate (`tools/evidence-disposition.py` semantics); Supersession seat per roster | **planned** (gate and dispositions not present) | `.ufo/evidence/round-13/expected.json` `expected_checks.producer_before` (exit 1, contains `summary preserves top-level exposed declaration kind`) and `producer_before_oracle` (exit 1, contains `… kind FAIL`). `.ufo/evidence/round-13/verification.json` check `producer_before` (exit 1, `exit_matches: true`, stderr is a Python traceback under `producer-before.py`). `.ufo/evidence/round-13/producer-oracle-repair.json` line 3 `"supersedes": "verification.json producer_before: path-layout crash is NOT red-before evidence"`; checks `producer_before_oracle` (line 8, `exit_matches` line 22) and `producer_after_oracle` (exit_matches line 39). `.ufo/evidence/round-13/verification-verdict.json` line 70 `excluded_initial_failure`. | New evidence (round 14) only: `producer_before` row state `superseded` with reason and `superseded_by` = [`producer_before_oracle`, `producer_after_oracle`]; both replacements effective and passing their original expectations. Original raw receipt/check retained, not edited. Do not treat `exit_matches` alone as mechanism proof. |
| 2 | GIT_DIR-poisoning claim has identical argv and no injected-env field; equality of retained JSON does not show the setup; manifest-versus-runner mapping not retained as a receipt. | ReceiptHarness (owns only `.ufo/evidence/round-14/capture-context.py`; L1 runs it); Gate for the env predicate | **planned** (harness not present) | `.ufo/evidence/round-13/verification.json` check `pin_env_scrub` (line ~155): argv identical to `pin_live`; no env field; not listed in `expected.json` `expected_checks`. `corpus/lessons/round-13.md:120` ("Injecting GIT_DIR did not change probe data…") is the only prose record of the injection. Static scrub: `tools/pin-disposition.py:197-211` (`git_env()` drops every `GIT_*`, then sets config/lock/prompt controls); selftest env at `:649-662`. Runner pins: `tools/mutate-and-run.sh:540-553` (`PIN_*`/`REV_*`); leg calls `:1113-1138`. Manifest: `.ufo/evidence/round-13/pin-manifest.json`. | Round-14 `context-receipt.json` (new file) must retain argv, cwd, `injected_env` = `{GIT_DIR: "/nonexistent/tameshi-round14-poison"}` (named variable only, no ambient env dump), baseline and injected outputs with exit codes, comparable JSON minus `observed_at`, source and manifest digests, and explicit six-leg mapping booleans (PIN_/REV_/leg call). The frozen `pin_env_scrub` row is not rewritten and is not counted as retrospective repair of the omitted round-13 setup. |
| 3 | `knowledge §6` is a pre-integration, deferred-at-write account; report, lesson and README carry final receipts. Future readers may take §6 as present absence. | EmpiricalBacklink | **open** | `corpus/knowledge/incremental-pin-disposition.md:251` heading "6. Empirical section — the round-13 receipt (deferred, contents not claimed)"; lines 253–259 say no `pin-dispositions.json` existed when written. That file now exists at `.ufo/evidence/round-13/pin-dispositions.json`. Corroborating index: `corpus/README.md:152` already indexes the receipt. Header line 1–7 cites S003/S041/S047/S048; S048 is the newest correction. The S003 180d versus combined 90d cadence is a deliberate stricter entry recheck, not a violation (lesson item 3). | Append (do not rewrite) a dated errata/backlink block under §6 pointing to `pin-dispositions.json` and the lesson. Prefer S048 wording for future guidance; keep S041/S047 history visible. |
| 4 | Operator/protocol: renderer still appends relative `Report:` trailers; closed-validated payload not fixed; append helper is not the full canonical frozen closure checker. | Operator layer (outside tameshi); not fixable in-lane | **open** (recurs) | `corpus/lessons/round-13.md:76-80` (renderer appended relative trailers; mitigated by absolute paths in context, not fixed). `.ufo/waves/round-13/w1/CorrectionCritic.md:12` (32/32 relative in round-13 `dispatch.json`) and `:54-55`. Round-14 recurrence: `.ufo/waves/round-14/dispatch.json` contains relative `Report: write your scoped findings to .ufo/waves/round-14/w1/<Name>.md` lines (e.g. `DispositionSpec.md`, `AdmissionCritic.md`). Helper: `scripts/hyaku/append-closure.py` (fleet root; serializes/validates, not the full canonical checker). | Record recurrence; do not claim fixed. Each seat's own absolute report path is in its assignment and is the authoritative destination. Operator correction belongs to the renderer owner, not to this lane. |
| 5 | Carried debt: full SKILL cold-read/box3, legacy provenance headers, F1 interop, successor mutation sweeps (kimi/tsukuroi/mado), runbook corrections; SHONEN boxes not independently checkable. | Lane backlog; FreshnessIntake for sweep intake; no SHONEN edits this round | **open** | `SHONEN.md` lines 5, 7, 9, 11 are `[~]` (four boxes). `corpus/README.md:84` F7 "open" for per-leg reuse classification; `corpus/README.md:78` F1 partly held; `corpus/README.md:152-159` states the F7 advance and that successor sweeps and provenance headers remain open. Lesson item 5 names the same debt. | No action this round. Carry forward to a future round as explicit debt. Do not mark any SHONEN box, run successor sweeps, or claim promotion. |

## Discrepancies to resolve before Gate/DispositionSpec finalize

1. **Row count.** The assignment says "All13 expected rows". `.ufo/evidence/round-13/expected.json` `expected_checks` enumerates **12** keys: `metadata_corrected, metadata_old_null, metadata_selftest, pin_live, pin_selftest, producer_after, producer_after_oracle, producer_before, producer_before_oracle, source_census, witness_check, witness_count`. The **13** in the assignment matches the count of `inputs` (13 entries), not of expected checks. The disposition file should enumerate 12 expected rows exactly once: 11 effective and `producer_before` superseded in the after file. Do not invent a 13th row.
2. **Unexpected check.** `verification.json` has 13 checks, including `pin_env_scrub`, `metadata_emit`, and `frozen_and_guardrail_unchanged` (none is an `expected_checks` key). `pin_env_scrub` has the same argv as `pin_live`. `verification-verdict.json` lists 15 matched names, adding `baseline_final_count`, which appears in no expected or verification check. The Gate must not add any of these as expected rows; they are receipt-only observations.
3. **Mtime ordering [INFERENCE].** `expected.json` mtime is 02:00, after `verification.json` at 01:59. Mtime is not evidence; the Gate must verify `expected.json` by `inputs` SHA-256 digests (the lesson reports 13 inputs, 0 mismatches) rather than by timestamps.

## Changes proposed for round-14 (new artifacts only; no historical rewrite)

- `tools/evidence-disposition.py` (Gate): stdlib CLI, `--root LANE --dispositions FILE --json`, `--selftest` using isolated fixtures, exit codes 0/1/2/64, stable finding IDs. Schema `evidence-dispositions-v1`.
- `.ufo/evidence/round-14/dispositions-before.json` and `.ufo/evidence/round-14/dispositions.json` (DispositionSpec): identical except `producer_before` state `effective` → `superseded`, with reason and replacement list.
- `.ufo/evidence/round-14/capture-context.py` and `context-receipt.json` (ReceiptHarness): L1 executes; the frozen expectation check and the context receipt stay separate.
- Empirical backlink block appended under `corpus/knowledge/incremental-pin-disposition.md` §6 (EmpiricalBacklink).
- Operator item 4: no in-lane change; recurrence recorded only.

Files not to touch: `corpus/lessons/round-13-verifier-spotcheck.md`, all of `.ufo/evidence/round-12` and `.ufo/evidence/round-13`, `tools/mutate-and-run.sh`, `SHONEN.md`, and the shared `LOG.md`, `SKILL.md`, `SOURCES.md`, `SCORECARD.md`, `QUALITY.md`, `README.md`.

## Risks

- Writing a 13-row disposition file to match the assignment text would fabricate a row; the Gate would then fail semantic expectations or be satisfied by an invented receipt. Use 12.
- `producer_before` supersession is valid only with both `producer_before_oracle` and `producer_after_oracle` effective and passing. A dispositions file that supersedes without the replacements must be rejected.
- The GIT_DIR claim rests on code scrubbing (`git_env()`) plus the lesson's prose. Neither is an executed receipt until ReceiptHarness runs at L1. Do not state poisoning as proven before that.
- Relative `Report:` trailers recur in round-14 `dispatch.json`; any seat that writes to a relative path lands in the fleet root. Each seat's absolute assignment path is authoritative.
- Carried debt (item 5) must not be converted into a promotion claim or SHONEN edit.

## Checks L1 should run (not run by this seat)

1. `python3 tools/evidence-disposition.py --selftest` (exit 0; stable finding IDs printed).
2. `python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions.json --json` (exit 0; expect 12 expected rows, 1 superseded).
3. `python3 .ufo/evidence/round-14/capture-context.py` (L1 only; exit 0; writes `context-receipt.json`).
4. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (fleet path; expect exit 0 with the known W04 duplicate-URL warnings for S047/S048).
5. `git diff --quiet 546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50 -- .ufo/evidence/round-12 tools/mutate-and-run.sh SHONEN.md` (exit 0 = frozen bytes unchanged).
6. `git diff --quiet d6809df7775338f000e44c8a916067b8866867fb -- .ufo/evidence/round-13 corpus/lessons/round-13-verifier-spotcheck.md` (exit 0 = historical round-13 bytes unchanged).

## Not established

- No runtime behavior of any gate, selftest, runner, or harness was observed by this seat.
- No independent-verifier claim is made; this report is a single-seat reading of committed bytes.
- The GIT_DIR injection's observed effect is taken from the lesson's prose; it is not reproduced here.
