# AuditMistake — round-15 w2 static audit: QUALITY17 link and old-vs-repaired `--selftest` evidence

Seat: `TameshiR15.AuditMistake` (leaf; no subagent dispatch). Static review only. Nothing was executed: no gate, no `--selftest`, no `--check`, no probe, no `measure.py`, no temp copy of the historical script.

Read-only operations used: `git status --short`, file reads, `sha256sum` on four files, and Python `json.load` key/value inspection of two retained receipts and `.ufo/waves/round-15/spec2.json`. Tool installs or updates: none.

Read revision: lane HEAD `a9cf4da78f2514c7bedd91a850a88590009d7df0` plus the uncommitted round-15 tree (`M` LOG.md, SKILL.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md; `??` .ufo/evidence/round-15/, .ufo/waves/round-15/, corpus/lessons/round-15.md, tools/context-capture.py).

Digests observed (sha256 of bytes read; not behaviour):
- `tools/context-capture.py` = `a2e8cfa2e5c04274bb6999e9a0a751974fb3042291338b7dbd65353f436b2ef5` (2116 lines). `.ufo/waves/round-15/w1/ContextGate.md:22–24` recorded `0ed784e0…` for the same tool at write time, so the file changed after that wave-1 review. The delta is not characterised here. This audit covers the bytes above; any L1 record must hash the bytes it executes.
- `.ufo/evidence/round-14/capture-context.py` = `7313e9a2…7d89` (equals `FROZEN_TOOL_SHA256`, tools/context-capture.py:140–142).
- `.ufo/evidence/round-14/context-receipt.json` = `05cb55b8…9c1a` (equals `FROZEN_RECEIPT_SHA256`, :137–139).
- `.ufo/evidence/round-14/context-missing-env.json` = `1ee9d09b…a208`.

## Axes

1. Calibration classification: is the gate-versus-probe and exit-class mistake linked and registered (QUALITY17)?
2. Evidence retention: is the unsupported old `--selftest` retained beside the repaired same-command result?
3. Selftest literal pins: do the expected exits and finding IDs match the code paths (static trace only)?
4. Hermeticity and historical integrity: bounded agreement.

## F1 — QUALITY17 lesson link: bounded agreement, three low residuals

Read: corpus/QUALITY.md:75–84; corpus/lessons/round-15.md:46–52; corpus/lessons/round-14-verifier-spotcheck.md:160; corpus/README.md:199–203; LOG.md:925–946; corpus/SOURCES.md:60 (S051); SKILL.md:1609–1691.

- QUALITY17 (QUALITY.md:81–84) cites `lessons/round-15.md` (gate-misclassification, exit-class-ambiguity) and the round-14 lesson's Routed defects5. Both targets exist. Round-14 lesson line 160 is Routed defect 5. round-15.md is present but untracked.
- Reciprocal links agree: round-15.md:50–51 names QUALITY17; LOG.md:936–938; README:199–200; S051 row points to round-15.md.
- Residual (low): round-15.md:50 "captured-by" says "QUALITY2 lacked explicit instrument classification". QUALITY.md:3–4 (QUALITY2) is "every claim carries a source". No instrument-classification criterion existed before QUALITY17. The association is loose, not a broken link.
- Residual (low): "PROTOCOL.md §Gate standard" (round-15.md:Gate, SKILL.md:1614) resolves to the fleet-root file `/home/vgpnk/Projects/shokunin/PROTOCOL.md:375–397`, which is outside the lane. The path is not lane-relative. Clauses match: Verdict 380–384, Self-test 385–389, Two evidences 390–397.
- Residual (low): the link resolves only in the working tree until L1 commits `corpus/lessons/round-15.md` and `corpus/QUALITY.md`.

## F2 — Old unsupported `--selftest` versus repaired same-command evidence: evidence absent; expectations source-derived

Source expectations (not observed):
- Old: `python3 .ufo/evidence/round-14/capture-context.py --selftest`. Historical `main()` (capture-context.py:605–613) returns 64 for any argv other than `-h`/`--help`. It writes `unexpected argument(s): --selftest` and USAGE to stderr and writes no receipt. `[INFERENCE]` until observed.
- Repaired: `python3 tools/context-capture.py --selftest`. `run_selftest` (:2005–2017) runs the harness. `finish()` (:1700–1725) prints `SELFTEST: PASS (N/N)` and returns 0. Any failed case returns 1. A setup exception returns 2. `--selftest --json` returns 64 (`parse_argv` :2069–2072; case `usage-selftest-extra` :2002).

Retained receipts present in `.ufo/evidence/round-15/` now: `claims.json`, `integration-decisions.json`, `measure.py`, `sources-before.json`. Absent: selftest stdout/stderr/exit, old-invocation stdout/stderr/exit, check receipts, `verification.json`.

Status: **missing, pending L1.** Planned by `.ufo/waves/round-15/spec2.json` items[31].prompt ("retain expected64 old unsupported and0 new") and w1 `ContextGate`/`TempScope` E5–E8, E12. Not a defect.

No round-15 document asserts an observed `SELFTEST: PASS`. Checked: round-15.md, SKILL.md:1609–1691, LOG.md:925–946. SKILL.md:1680 names the command only.

Hazard for L1 (plan text, not implementation): spec2 items[31] says "exact CLI --snapshot/--check schema as implemented". The implemented CLI has no `--snapshot`. `parse_argv` (:2023–2080) rejects it as an unknown argument, so `python3 tools/context-capture.py --snapshot DIR` exits 64 `usage_error`. `snapshot` appears only in the `snapshot_tampered` ID (:80, :1329–1331, :1910). The tampered case maps to `--check --receipt COPY --expected PIN` with a wrong `receipt_sha256`, which returns `snapshot_tampered` exit 2 (:1323–1333). L1 should be told so that a 64 is not misread as a failed snapshot gate.

## F3 — Explicit exit classes: `--check` surface satisfied; `--selftest` surface undeclared (bounded gap)

- `--check` exits 0/1/2/64 are declared in USAGE (:266–270), the docstring exit map (:88–97), and SKILL.md:1680 (`64 usage_error`). This satisfies the exit-class-ambiguity fix for `--check`.
- `--selftest` exits are not declared. The harness returns 1 on any failed case (:1719–1723) and 2 on setup error (:2008–2014). USAGE and docstring describe only `--check` exits. SKILL.md:1680 self-test column names only the command.
- Counterexample: `--selftest` exit 1 (`SELFTEST: FAIL`) has no declared class. Under PROTOCOL.md:380–382, an undeclared nonzero code reads as could-not-evaluate. That conflicts with the meaning of 1 (failed) the harness itself uses. QUALITY17 requires "explicitly classify every nonzero exit".
- Severity: documentation and registry only; status-neutral. Route to the registry owner. Not an implementation-critical defect.
- Optional, not required by QUALITY17: the selftest pass count `N` is computed, not pinned (`claims`/w1 E18 expected a pinned N).

## F4 — Selftest literal pins: bounded static agreement, not executed

Static trace of 38 harness records (31 `check_case`, 5 `usage_case`, 2 hermetic) against `recompute_*` (:805–1105), validators (:459–805), and `run_check` (:1298–1344). For each record the first finding or stage gives the pinned ID and exit.

| Case(s) | Pinned | Trace |
|---|---|---|
| clean | context_consistent / 0 | fixture (:1388–1569) passes every validator and recompute; expected `findings == []` |
| missing-injected-env, null-injected-env | missing_injected_environment / 1 | `recompute_environment` :807–815; `receipt_verdict_mismatch` follows (fixture status `ok`); `expected_ids` accepts both |
| comparison-raw-mismatch, comparison-observed-at-lie | comparison_mismatch / 1 | `recompute_comparison` :947–978 |
| payload-digest-lie | comparison_tool_digest_mismatch / 1 | payload check :933–944 runs before `recompute_sources` |
| probe-source-lie, runner-source-lie | probe/runner_source_digest_mismatch / 1 | :1019–1035 |
| control-ineffective, control-flag-lie | positive_control_ineffective / 1 | :985–1014 |
| mapping-check-lie, mapping-order-lie | mapping_mismatch / 1 | :1069–1101 |
| mapping-constant-swap | mapping_mismatch / 1 | all recorded fields agree with raw, so the `elif all_match is False` branch (:1102–1105) produces the finding |
| truthy-matches-declared, truthy-all-match, bool-exit, exclusions-widened, comparison-container | receipt_structure_invalid / 2 | `require_bool`/`require_int` reject non-bool/non-int (:387–402); `exclusions != ["observed_at"]` (:574–577) |
| duplicate-key, malformed-json, non-object-json, invalid-utf8 | receipt_json_invalid / 2 | :317–327; `validate_top` :460–462 |
| receipt-missing, expected-missing, expected-invalid, expected-digest-invalid | receipt_missing / expected_missing / expected_invalid / 2 | :1212–1216; :1186–1209 (`expected_invalid` wraps inner) |
| snapshot-tampered | snapshot_tampered / 2 | :1323–1333 |
| expected-verdict-mismatch | expected_verdict_mismatch / 1 | `apply_expected` :1265–1286 |
| stored-verdict-lie | receipt_verdict_mismatch / 1 | `verify_recorded_verdict` :1108–1129 |
| retained-invalid-input | receipt_records_invalid_input / 2 | :1152–1161 |
| baseline-unusable | baseline_unusable / 2 | `validate_baseline_document` :765–796 via :882–889 |
| usage-no-args, usage-receipt-without-expected, usage-expected-without-receipt, usage-unknown-flag, usage-selftest-extra | usage_error / 64 | `parse_argv` :2023–2080; `main` :2086–2093 prints `id=usage_error` |
| hermetic-no-lane-path, hermetic-temp-only | — | :1700–1716 |

Retained frozen receipt, field-shape check (read-only, not a `decide()` replay): 19 top-level keys match `RECEIPT_KEYS`; 10 environment keys match `ENVIRONMENT_KEYS`; `injected_env == {"GIT_DIR": POISON}`; `env_delta_keys == ["GIT_DIR"]`; probe and runner `sha256 == declared`; probe document `tool_sha256 == 297253…`; `payload_tool_sha256_matches_disk` recorded True; six mapping legs have all five checks True and `all_match` True; `runner_leg_order == manifest_leg_order`; `positive_control.effective` True; `env_additions == CONTROL_ENV_ADDITIONS`. `context-missing-env.json` has no `environment.injected_env` key, so `missing_injected_environment` is the expected primary finding. `observed_at` values match `OBSERVED_AT`.

Counterexample search: no pinned literal disagrees with the traced first finding or stage. Not checked: the exact `SELFTEST` output and exit codes, which require L1.

## F5 — Hermeticity and historical integrity: bounded agreement; wave-1 concerns resolved in current source

- `run_check` reads only the named receipt and expected pin (`read_regular` :330–349). It has no write call (:1298–1344). Selftest writes only under `tempfile.mkdtemp` (:1581) and removes the root in `finally` (:2016–2017).
- `DEFAULT_LANE_ROOT = dirname(dirname(SELF))` (:123) uses two `dirname` calls. The wave-1 concern (`AttackTamper`, `AttackUnavailable`, `ClaimEvidence` E2: four `dirname` calls resolve to `/home/vgpnk/Projects`) is resolved in current bytes.
- Historical bytes: `git status` shows no changes under `.ufo/evidence/round-12..14`. `capture-context.py` still hashes `7313e9a2…`. Frozen receipt still hashes `05cb55b8…`.
- `OUTPUT_REL` overwrite concern (wave-1 `AttackUnavailable` item 5): check mode writes nothing, so it cannot overwrite the round-14 receipt.

## F6 — Missing evidence: honest current status (all pending L1, none proven defective)

1. Repaired `python3 tools/context-capture.py --selftest`: stdout, stderr, exit. Expected 0 and `SELFTEST: PASS (N/N)` by static reading. Not observed.
2. Old `capture-context.py --selftest` run from a temp copy of the historical bytes: stdout, stderr, exit. Expected 64 by static reading. Not observed.
3. Same-command pairing: items 1 and 2 retained side by side with the same argv shape (QUALITY17).
4. Round-15 frozen check and expected pin: `--check` clean (0), `context-missing-env.json` pinned to `missing_injected_environment`/1, a tampered copy to `snapshot_tampered`/2, and `--check` with bad argv to `usage_error`/64. Not observed.
5. Round-15 receipts and `verification.json`. Not observed.
6. Round-14 receipt hash before and after L1 (`05cb55b8…`). Not observed.
7. Selftest `--selftest` exit classes (1 and 2) declared in the registry or docstring (F3). Missing as a declaration.

## Messages

No message sent to `TameshiR15`. No implementation-critical defect was found: the selftest pins trace consistently (F4), and the frozen replay shape agrees with the validators (F4). The F2 hazard (`--snapshot` in spec2 items[31]) is a plan-text issue for the main agent, and the F3 gap is a registry/documentation item. Both are reported here for routing.

## Recommended L1 checks (named, not executed here)

1. `sha256sum tools/context-capture.py .ufo/evidence/round-14/context-receipt.json .ufo/evidence/round-14/capture-context.py` before and after the run.
2. Old invocation: copy historical bytes to a temp path with the same argv shape as the repaired run (`--selftest`), and retain stdout, stderr and exit. Expect 64 and no receipt.
3. Repaired: `python3 tools/context-capture.py --selftest`, and again with `GIT_DIR` poisoned. Retain stdout and exit. Expect 0 and `SELFTEST: PASS`.
4. Replace every `--snapshot` reference with `--check --receipt FILE --expected FILE`.
5. Declare `--selftest` exit 1 and exit 2 in the registry row or docstring (F3).
6. Re-hash the final `tools/context-capture.py` bytes, since they differ from the `0ed784e0…` recorded at ContextGate write time.

Status summary: QUALITY17 link **bounded agreement** (F1). Old-vs-repaired retention **missing, pending L1** (F2, F6). `--check` exit classes **agreement** (F3). `--selftest` exit classes **gap, documentation only** (F3). Selftest pins **bounded static agreement, not executed** (F4). Historical integrity and hermeticity **bounded agreement** (F5).
