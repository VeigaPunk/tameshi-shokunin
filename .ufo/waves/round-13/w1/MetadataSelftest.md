# MetadataSelftest — read-only review, revision 2 (tameshi-r13-w1)

Scope: landed `tools/witness-metadata.py`, its `SELFTEST_CASES`, the producer fix in `tools/bash-witness-study.py`, and the landed companion `.ufo/evidence/round-13/witness-metadata.json`. Read-only; no check, selftest, emit, or hash was executed. Tooling: none installed or updated.

## Verified by reading

- **Case table.** `SELFTEST_CASES` (`tools/witness-metadata.py:624-800`) has 25 literal rows. Each red row reaches its named branch before any earlier failing check:
  - old-null → `normalized_kind_null` (:533-535), after the digest and expected-record checks pass.
  - corrected green → `ok`, exit 0 (:592-598).
  - wrong kind `declared-witness mapping` → `normalized_kind_mismatch` (:538-539); `blind preregistration` → same reason (substring-free literal compare).
  - absent disclosure → `disclosure_missing` (:544-545).
  - tamper-summary / tamper-rerun → `*_digest_mismatch` (:409, :481), mapped to `snapshot_tampered` by the `endswith("_digest_mismatch")` rule (:257-260).
  - tamper-declared-with-wrong-kind → `declared_digest_mismatch` (:403-409). Digests are checked before the companion kind comparison (:538), so integrity precedes comparison.
  - malformed JSON / duplicate key → `companion_json_invalid` exit 2 (:294-302); `_DuplicateKey` is a ValueError subclass and is caught there.
  - missing input → `input_missing` (:333); path escape → `path_rejected` (:316); extra input / missing or unpinned digest → exit 2 `snapshot_tampered` via `SNAPSHOT_TAMPER_REASONS` (:244-251).
- **Isolation.** Fixtures are built under `tempfile.mkdtemp()` (:932), copy pinned inputs from `LANE_ROOT` read-only (:803-812), run the CLI with `--lane-root` pointing at the fixture (:940-952), and are removed in `finally` (:983-984). A post-run hash of the frozen inputs (:986-1003) fails with `FROZEN_MUTATED`.
- **Producer.** `tools/bash-witness-study.py:787` now reads `declaration.get("kind")` (top-level, as in `declaration.json:6`). The regression at `:1538-1544` asserts the literal string. The frozen `summary.json:15` null is not rewritten: the pinned digests in the tool (`:68-84`, `:125-127`) match `manifest.json` lines 71, 35, 37 and 67 (text comparison only).
- **Companion file.** `.ufo/evidence/round-13/witness-metadata.json` matches `build_companion()` field by field (text comparison), including the disclosure string and `frozen_bytes_rewritten: false`.

## Concrete findings

1. **Unkilled branches (medium).** The 25 rows do not exercise these checks. A mutation of any of them would pass selftest:
   - `:363-366` schema / generated_for mismatch
   - `:373-374` expected exit type or value
   - `:395` companion path mismatch
   - `:417-418` summary tool sha (producer identity)
   - `:431` declaration runner sha
   - `:440-441` historical runner checked_live
   - `:456-457` covered-scope value/field
   - `:468-471` uncovered-scope integrity/disposition
   - `:541-542` kind_source
   - `:551-557` disclosure_mismatch digest, disclosure_source
   - `:580-583` frozen_bytes_rewritten and measured_claim flags
   - `:512-517`, `:522-525` summary/declaration disclosure and binding mismatches
2. **No on-disk assertion (medium).** No selftest row or check compares the landed `witness-metadata.json` to `--emit` output, and no check runs `--check` default against the live lane from selftest. L1 must run both (see checks).
3. **Self-referential fixtures (low, residual risk).** `_prepare_fixture` builds every companion from `build_companion()` (:827). The green fixture therefore equals the checker's own construction. Independent anchors are the frozen digests (`:68-84`) and the literal case table; the disclosure digest `ec6e5…b0f0` (`:98-100`) is unverified until hashed (check 5).
4. **Catch-all masking (low).** `main` maps any non-`Failure` exception to `input_unavailable`, exit 2, reason `unexpected_exception` (`:1074-1081`). No case expects that reason, so a defect would show only as a reason mismatch on the case that hits it. Decide whether to keep it, and cover it if kept.
5. **Symlink gap on companion path (low).** `companion_path.is_file()` and `read` at `:358-360` follow symlinks; pinned inputs are checked at `:320-345`. Read-only and inside the lane, so low severity.
6. **Subprocess timeout (low).** `subprocess.run(..., timeout=60)` at `:940-952` has no `TimeoutExpired` handler; a hang would raise in the selftest rather than report a FAIL row.
7. **Producer identity is historical.** The companion records `checked_live: false` (`:166`, `:176`). A reader must not treat the gate as validating the current `bash-witness-study.py` (which changed).

## Checks L1 should run (not executed here)

1. `python3 tools/witness-metadata.py --selftest; echo exit=$?` — expect 25 `SELFTEST_CASE … OK` rows, `SELFTEST: PASS 25/25`, exit 0.
2. `python3 tools/witness-metadata.py --check --json; echo exit=$?` — expect `metadata_consistent`, `reason":"ok"`, exit 0.
3. `python3 tools/witness-metadata.py --emit | diff - .ufo/evidence/round-13/witness-metadata.json; echo exit=$?` — expect empty diff, exit 0.
4. `sha256sum` of `.ufo/evidence/round-12/BashWitness/{summary.json,declaration.json,declared.tsv}` and `rerun-20261020T035435Z/summary.json`; compare to `manifest.json` lines 71, 35, 37, 67.
5. Hash `EXPECTED_DISCLOSURE` (`tools/witness-metadata.py:89-97`, utf-8) and compare to `ec6e5be711945a84e1148819a12d7897386c319a2544b8b0829b4bd74af9b2f0`.
6. `python3 tools/bash-witness-study.py --selftest; echo exit=$?` — expect the `summary preserves top-level exposed declaration kind` check to pass. Do not rewrite `selftest.sha256.txt`.
7. `git status --porcelain -- .ufo/evidence/round-12 tools/bash-witness-study.py` — round-12 frozen directory expected unchanged; the producer edit is the only tool change.

## Verification gaps

- No check was run; all findings are from source reading at the anchors above.
- Coverage findings (1-2) are measured by reading the case table, not by mutation testing.
- The disclosure digest (3, check 5) is unverified.
