# ReviewSnapshotPins — round-15 C1 frozen pins, expected-pin schema, input-hash binding, authentication wording

Seat: `TameshiR15.ReviewSnapshotPins` (reviewer, leaf). Author-side advisory only; not admission authority.
Read revision: working tree at review time; `tools/context-capture.py` as shown with tag `#472A`.
Execution: **none**. No gate, selftest, probe, runner, git or sibling command was run. Reads were `read`/`grep`/`glob` only. No `sha256` was recomputed on disk; literal digests below are compared as text against the source and retained citations.
Tool installs/updates: none. No credential, agent DB or auth file was touched.

## Source read (exact)

- `AGENTS.md` (whole).
- `corpus/lessons/round-14-verifier-spotcheck.md` lines 82–100 and 154–162 (C1 limits; Routed defect 5).
- `tools/context-capture.py`: lines 1–119 (header contract, modes, stable IDs, exit map, bounded-scope paragraph); 145–250 (pinned constants, key sets); 295–460 (hashing, strict JSON, `read_regular`, coercion helpers); 459–563 (`validate_top`, `validate_environment`, `validate_runs`); 804–853 (`recompute_environment`, `recompute_runs`); 1017–1036 (`recompute_sources`, probe and runner only); 1185–1348 (`validate_expected`, `load_expected`, `make_result`, `apply_expected`, `result_from_exception`, `run_check`); 1578–1728 (`SelftestHarness`, `check_case`, `usage_case`, `finish`); 1879–2005 (snapshot, expected-pin and usage selftest cases); 2020–2116 (`parse_argv`, `main`).
- Targeted greps over the tool for `manifest`, `expected_r13`, `authenticat|tamper|integrity|authority`, `expected_verdict_mismatch`, `receipt_sha256`, `1ee9d09b`.
- `SKILL.md` lines 1601–1692 (historical gate row 1602; classification section 1609–1675; round-15 registry 1677–1681; authenticity wording 1683–1691).
- `.ufo/evidence/**/*context*` glob and a grep for `tameshi-context-expected-v1` across `.ufo`, `corpus`, `tools`.
- Not read in full: `tools/context-capture.py` 120–144, 1349–1577 (fixture builder) and 1728–1877 (selftest bodies), except by grep hit. Findings below do not depend on those ranges.

## Verified agreement (bounded to static reading)

1. **Expected-pin schema is strict.** `validate_expected` (1186–1209) requires exactly the four keys, the literal schema, a lowercase 64-hex digest (`HEX64` at 177; `require_hex` fullmatch 423–428), a stable-ID regex match (179, 1203) and `exit` as a non-bool int in {0,1,2} (`require_int` 394–402, `type(value) is not int`, so `True` is rejected).
2. **Duplicate keys rejected** for both the expected pin and the receipt (`_no_duplicate_keys` 308–314; `parse_json_strict` 317–327).
3. **Digest precedes semantics, from one read.** `run_check` reads `raw` once (1316–1323), compares `sha256_bytes(raw)` to `expected["receipt_sha256"]` (1323–1324) and only then parses the same `raw` (1334–1336). No TOCTOU between digest and parse. A mismatch returns `snapshot_tampered`/2 (1325–1333).
4. **Frozen literals are consistent with retained citations.** `FROZEN_RECEIPT_SHA256` = `05cb55b8…9c1a` (137–139), `FROZEN_TOOL_SHA256` = `7313e9a2…7d89` (140–142), id `context_consistent`, exit 0 (143–144). These match the round-14 lesson (its line 96 and 104 citations of the clean receipt), the round-14 receipts' `tool_sha256` field, and SKILL 1680. Not recomputed on disk in this pass.
5. **Frozen tool-declaration check exists.** `check_receipt` 1175–1179 compares the receipt's `tool_sha256` to `FROZEN_TOOL_SHA256` in frozen mode only.
6. **Frozen mode reads only the pinned path** under `DEFAULT_LANE_ROOT` (1299–1308); explicit mode reads only `--receipt` and `--expected` (1310–1313).
7. **Snapshot-tamper and expected-pin selftest cases are literal.** `snapshot-tampered` (1906–1913), `expected-invalid` (1919–1926), `expected-digest-invalid` (1982–1989), `expected-missing` (1915–1917), `expected-verdict-mismatch` (1928–1936). `check_case` (1611–1673) requires literal exit code, `id`, and absence of `Traceback`.
8. **Authenticity disclaimers exist in the registry.** SKILL 1619–1620 ("adds no … author authentication"), 1604–1605 and 1683–1686 ("configured authority, not cryptographic proof of author authenticity"); the round-15 lesson rejects "source authentication" (`corpus/lessons/round-15.md` lines 39–41).

## Findings

### F1 — Medium. Pinned expected verdict is not enforced for could-not-evaluate results; exit contradicts the documented ID map

- Code: `apply_expected` (1265–1286). If `result["exit"] == 0` on mismatch, it becomes `expected_verdict_mismatch`/exit 1 (1277–1282). Otherwise it only appends a finding (1283–1285) and **keeps the original id and exit**.
- Doc contract: `expected_verdict_mismatch exit 1` (tool docstring line 74); SKILL 1680 "1 failed stable finding ID".
- Concrete static counterexample (exit 2 branch): `--check --receipt R --expected E` with R not valid JSON and E = `{"schema":"tameshi-context-expected-v1","receipt_sha256":sha256(R),"id":"context_consistent","exit":0}`. Path: `run_check` 1334–1339 → `result_from_exception` 1289–1295 → `apply_expected` 1265–1285. Result: `exit 2`, `id receipt_json_invalid`, `findings` contains `expected_verdict_mismatch`, `verdict_matches_expected false`. Documented contract says `expected_verdict_mismatch` ⇒ exit 1. The same holds for `snapshot_tampered`/2 on an expected pin of another id, and for any exit-2 recompute.
- Coverage: the only selftest for `expected_verdict_mismatch` (1928–1936) uses a clean (exit 0) receipt, so the exit-2 branch is never exercised. No selftest asserts a literal exit for it.
- Not a false clean (exit stays nonzero). It is a stable-ID/exit inconsistency and an untested branch in the "literal expected exit/finding pairs" requirement.

### F2 — Medium (claim wording). "The digest pin is the integrity authority" overstates explicit mode; frozen anchors share the editable file

- Tool docstring 99–100: "the digest pin is the integrity authority". It contains no coordinated-edit bound. The same docstring says the tool's `tool_sha256` is "not treated as authentication" (100), but that is the only disclaimer.
- Explicit mode: the digest and the expected id/exit both come from caller-supplied files (`load_expected` 1313; compare 1323–1324). Counterexample: rewrite R to R′ and write E′ = `{sha(R′), id:X, exit:Y}` for whatever X/Y R′ produces. `run_check` returns `verdict_matches_expected true`, exit Y. No independent anchor exists.
- Frozen mode: `FROZEN_RECEIPT_SHA256`, `FROZEN_TOOL_SHA256`, `FROZEN_EXPECTED_ID/EXIT` (137–144) are literals in the same file as the logic. Coordinated edit of the tool constants and the receipt passes with exit 0. `tool_sha256()` (300–305, reported 1227) is only reported and never compared to any pinned value.
- SKILL 1664–1665 ("an edited snapshot is integrity failure") is true only against **non-coordinated** edits; the coordinated case is not stated there. SKILL 1683–1686 does disclaim authenticity, so the registry is compliant; the docstring at 99–100 and the SKILL 1664 wording are not.
- Recommended wording (no code change required for this finding): docstring 99–100 and SKILL 1664–1665 should say "detects non-coordinated byte edits; does not detect coordinated rewrite of the receipt and its pin, including edits to the tool's own frozen constants."

### F3 — Medium. Frozen input hashes are bound only transitively; manifest and expected digests are shape-checked, never compared

- Recomputed: `recompute_sources` (1017–1035) checks `probe.sha256 == declared_sha256` and `runner.sha256 == manifest_declared_sha256`, plus literal `True` flags. Nothing else.
- Shape-only: `sources.manifest.sha256` and `sources.expected_r13.sha256` are validated by `validate_sources` (622–642) as 64-hex and never read again. grep finds no other reference.
- No constant binds probe, runner, manifest or expected-r13 digests. The only anchor is `FROZEN_RECEIPT_SHA256` (137–139), which transitively covers them. Counterexample (explicit mode): set `sources.manifest.sha256` and `sources.expected_r13.sha256` to any 64-hex values, recompute the expected digest, run `--check --receipt R --expected E` → `context_consistent`/0.
- The docstring (50–52) claims only probe and runner recomputation, so this is not an overclaim in the tool. It is a coverage gap relative to the round-14 lesson's "frozen input hash" framing; the lesson's routed item 5 asks for registry/selftest correction, not new hashing.
- Selftest fixtures (1351–1353, 1475–1479) build manifest and expected bytes but never assert on them.

### F4 — Low. Negative fixture listed as a pinned value, but no committed expected pin exists

- SKILL 1653–1659 describes `context-missing-env.json` (sha256 `1ee9d09b…2aa208`) as "the discriminating counterpart: passed with a caller-committed expected pin … `missing_injected_environment`, exit 1". SKILL 1680 lists the same digest under "Pinned values".
- Evidence: glob `.ufo/evidence/**/*context*` returns only `round-14/{context-missing-env.json, context-receipt.json, capture-context.py}`. Grep for `tameshi-context-expected-v1` finds the tool and round-15 wave reports only. No committed expected JSON for the negative fixture exists, and the tool contains no `1ee9d09b` constant.
- The only retained counterpart is round-14 `guardrails.json` `context_setup_missing_field` (inline helper, per w1 AttackClean line 15), which is not this gate.
- Recommendation: either commit the expected pin under the round-15 evidence path and treat its gate run as L1-only, or reword SKILL 1680 "pinned values" to "referenced fixture, not pinned".

### F5 — Low (observation). `read_regular` stat-then-open follows symlinks

- `read_regular` (330–349) uses `os.stat` (follows symlinks) and then `open`. Digest and parse use the bytes from that single `open`, so a symlink target swap cannot change digested bytes; a FIFO or swapped path can at most block or be read as the target. Symlink containment belongs to the SecureSymlinkScope review. Noted only so the pin does not claim path identity.

### F6 — Observation. Exit 64 cannot be pinned

- `validate_expected` allows exit {0,1,2} only (1206). Usage has no receipt, so no pin is needed and this is consistent with SKILL 1666. Recorded as bounded, not a defect.

## Counterexamples summary (static, not executed)

| # | Claim tested | Counterexample | Outcome |
|---|---|---|---|
| F1 | expected pin ⇒ exit per ID map | invalid-JSON receipt with pin `context_consistent`/0 | exit 2 with `expected_verdict_mismatch` finding (doc says exit 1) |
| F2 | digest pin is integrity authority | coordinated rewrite of R and E; or of tool constants and R | exit = pinned verdict; no detection |
| F3 | frozen input hashes verified | edit manifest and expected-r13 digests and re-pin | `context_consistent`/0 |
| F4 | negative counterpart pinned | no committed expected file | counterpart is documentation-only |

## Bounded agreement

Within the static read set above, the expected-pin schema (strict keys, lowercase digest, id regex, exit ∈ {0,1,2}, duplicate-key rejection), the single-read digest-then-parse ordering, and the frozen literals' text agreement with the retained round-14 citations hold. This is agreement with the text, not with the on-disk bytes, and it is not a prediction of any run result.

## Routing

- F1 is implementation-critical for the "literal expected exit/finding pairs" contract: messaged to `TameshiR15`.
- F2, F3 and F4 are wording or coverage items for the registry owner; recorded here, not messaged.

## Checks for L1 (after all seats return; not run by this seat)

1. `python3 tools/context-capture.py --selftest`, and confirm whether any case pins `expected_verdict_mismatch` with exit 2 (expected: none, per F1).
2. Construct an invalid-JSON receipt with a matching `receipt_sha256` and `context_consistent`/0 pin; confirm exit code and whether `expected_verdict_mismatch` is listed (F1).
3. Compare the on-disk sha256 of `tools/context-capture.py`'s frozen targets with the literals at 137–144 (not done here).
