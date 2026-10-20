# MetadataSchema — round-13 read-only surgical review
Scope: companion metadata kind normalization against frozen top-level `kind` and `disclosure`. No implementation edits, no checks or gates executed, no sibling execution. Read-only `git status`/`git log` and file reads only. No tools installed or updated.

## State observed (2026-10-20)

- `tools/witness-metadata.py` — absent. `.ufo/evidence/round-13/` — absent. The MetadataRepair implementation has not landed; there is nothing to review yet beyond the frozen inputs and the producer defect.
- Message delivered to executor `TameshiR13.MetadataRepair` (write tool confirmed delivery; the id is taken from the spec item name and is not in the visible roster).

## Frozen anchors (read-only, not modified)

| Item | Anchor | Value |
|---|---|---|
| Top-level kind | `.ufo/evidence/round-12/BashWitness/declaration.json` line 6 | `"declared-witness mapping (not a blind preregistration)"` |
| Top-level disclosure | same file line 7 | `declared-witness mapping, not a blind preregistration: before declaring, the author had seen recorded aggregate outcomes of this leg …` |
| Nested declared block | same file lines 8-15 | `path`, `sha256`, `rows`, `none_rows` only — **no `kind` key** |
| Nested null (historical) | `.ufo/evidence/round-12/BashWitness/summary.json` line 15 | `"kind": null` |
| Summary disclosure | `summary.json` line 16 | same disclosure text as declaration.json |
| declaration.json sha256 | computed | `e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901` (matches `declaration-before-run.txt` line 3) |
| summary.json sha256 | computed | `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9` |
| declared.tsv sha256 | computed | `0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3` (matches declaration.json `declared.sha256`) |

## Root cause of the null (producer defect)

- `tools/bash-witness-study.py:787`: `"kind": declaration.get("declared", {}).get("kind"),` reads the **nested** `declared` object.
- The writer `tools/bash-witness-study.py:875` puts `kind` at the **top level** of `declaration`, and `:877-882` builds `declared` without `kind`.
- So the producer looks at a key that never exists and emits `null` by construction. The defect is a wrong-path read, not a missing value in the frozen data. The intended value is the top-level `kind` (and its `disclosure`), per `corpus/lessons/round-12-verifier-spotcheck.md:146` ("nested `declaration.kind=null` metadata defect").
- `summary.json:16` copies the disclosure correctly from top level (`declaration.get("disclosure")`, line 788), so only `kind` is mis-read.

## Findings for the companion metadata gate (MetadataRepair)

1. **Normalized kind must equal the frozen top-level kind byte-for-byte.** Expected value: `declared-witness mapping (not a blind preregistration)`. Do not introduce a shortened label, enum, or new vocabulary (e.g. `declared-witness-mapping`, `prior-exposed`). That would be an invented kind. Severity: high if violated.
2. **Never upgrade wording toward blind.** The normalized kind must retain `not a blind preregistration`. Any normalization that drops the parenthetical, or maps to a term containing `blind`/`preregistered` without `not`, is a prior-exposure misrepresentation. Severity: high.
3. **Disclosure is a required input, not optional.** Companion `--check` must fail if the top-level `disclosure` is absent, empty, non-string, or not byte-equal to the frozen text. Falling back to "no disclosure" or to a default string is a defect. Expected: exit 1 `metadata_inconsistent` on wrong or absent disclosure; exit 2 when the input cannot be read or parsed.
4. **Do not read the nested path for kind.** The companion normalizer must read top-level `kind`. Reading `declared.kind` again reproduces the original null and must be red in selftest. Severity: high.
5. **Original null is historical fact.** `summary.json` must remain byte-identical (sha256 above). The companion must record the nested null as an observed prior value, not overwrite it and not treat it as authoritative. Companion-only output; no write to `round-12/`.
6. **Anchor digests.** The companion must pin sha256 of summary.json and declaration.json (and declared.tsv per the frozen declaration reference). Missing or mismatched digest → exit 2 `snapshot_tampered`, not a pass.
7. **Selftest arms L1 should expect (not run here):** old null red (nested-path read reproduces `null`), corrected companion green (top-level kind equals frozen literal), tampered declaration (digest mismatch → exit 2), wrong kind string (→ exit 1), absent disclosure (→ exit 1), malformed JSON (→ exit 2).

## Exact checks L1 should run (not executed here)

- `sha256sum .ufo/evidence/round-12/BashWitness/summary.json .ufo/evidence/round-12/BashWitness/declaration.json .ufo/evidence/round-12/BashWitness/declared.tsv` — compare to the table above; all three must be unchanged.
- `git diff --stat -- .ufo/evidence/round-12 tools/bash-witness-study.py` — expect no frozen round-12 change from this round.
- `python3 tools/witness-metadata.py --selftest` (once landed) — expect the literal IDs and exits from MetadataRepair's spec.
- `python3 tools/witness-metadata.py --check` against the live companion — expect exit 0 `metadata_consistent` only if kind equals the frozen top-level string byte-for-byte.
- Grep the companion for the literal normalized value `declared-witness mapping (not a blind preregistration)` and confirm no alternate kind vocabulary is introduced.

## Residual risk / verification gaps

- The implementation is not present, so no code-level finding is possible yet; this report covers the input contract and the producer defect only.
- Delivery to `TameshiR13.MetadataRepair` is unconfirmed (id not in the visible roster).
- Tooling: none installed or updated.

## Post-landing review (read-only, 2026-10-20)

Source reviewed: `tools/witness-metadata.py` (1088 lines; read in full: literals 58-128, builder 141-227, loaders 283-345, core check 353-598, selftest table 624-800, fixtures 825-903, runner 906-1010, CLI 1047-1084); `.ufo/evidence/round-13/witness-metadata.json` (74 lines); producer diff `git diff -- tools/bash-witness-study.py` (`:787` changed, cmd_selftest regression at ~`:1538-1544`). No check, selftest, or gate was run.

### Kind / disclosure / digests (verified, no defect)

- Frozen digests recomputed now, all match the pins at `witness-metadata.py:68-84` and the companion `frozen_declaration`: summary.json `acc01268cb5f…47b9`, declaration.json `e8d2024ad13e…0901`, declared.tsv `0def0d3b370…41e6fd`, rerun summary `6726421fde88…a5f0` (`:125-127`).
- Companion `declaration.kind` = `declared-witness mapping (not a blind preregistration)`, byte-equal to frozen `declaration.json:6`; enforced twice: against frozen top-level at `:494`, against companion literal at `:538`. No invented label.
- `EXPECTED_DISCLOSURE` (`:89-97`) is byte-equal to frozen `declaration.json#/disclosure`; sha256 `ec6e5be711945a84e1148819a12d7897386c319a2544b8b0829b4bd74af9b2f0` matches `:98-100`. Summary disclosure equals it (`:512`).
- `blind: false` / `prior_exposure: true` enforced (`:559-566`). Original nested null preserved as historical (`:568-578`, companion `original_nested`).
- Rerun summary: nested kind null, disclosure equal to literal, declared sha `0def0d3b…`; the residual null is named and integrity-anchored (`:122-127`, `:473-491`), not silently authoritative.
- Frozen bytes untouched: summary/declaration/declared/rerun hashes above equal the pins; `git status` shows no `M` under `.ufo/evidence/round-12/`.

### Producer fix (Main)

- `tools/bash-witness-study.py:787` now reads `declaration.get("kind")` (top-level), replacing the nested read. The old value was `declaration.get("declared",{}).get("kind")`, which is always null (the writer at `:875` does not put kind under `declared`). Fix is minimal and matches the frozen top-level field.
- Live producer sha is now `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`; the companion pins `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a` (`:110-113`), which is the historical producer in frozen `summary.json` `tool.sha256` and in the rerun summary. `checked_live: false` keeps the gate green; the companion note must say the live producer was repaired afterward, or a reviewer will read the pin as current.
- The added producer regression (`check("summary preserves top-level exposed declaration kind", …)`) feeds a literal kind into the fixture; it checks pass-through, not normalization against frozen declarations. Acceptable as producer-local.

### Concrete findings (ordered by severity)

1. **Medium — confounded selftest arm.** `tamper-declared-with-wrong-kind-red` (`witness-metadata.py:883-884` sets companion kind to `blind preregistration`; `:894-897` appends to declared.tsv). Expected `declared_digest_mismatch`. The digest check at `:409` fires before the kind check at `:538`, so the wrong-kind arm is never exercised. The case name claims a kind arm it cannot observe. Owner: MetadataRepair. Fix: drop the kind mutation from that fixture, or rename it `tamper-declared-red`.
2. **Low-medium — TOCTOU between integrity and parse.** Bytes are hashed at `:405` and the file is parsed again at `:412-413` (summary, declaration) and `:477`/`:482` (rerun). A file swapped between hash and parse passes integrity on the old bytes and parses the new ones. Fix: parse from the bytes already verified (`json.loads` on the hashed buffer) rather than re-reading the path.
3. **Low — companion path not lstat-checked.** `main()` (`:1056-1062`) accepts an absolute `--companion` outside the lane, and `run_check` uses `companion_path.is_file()` (`:358`), which follows symlinks. Read-only, verdict-only, so no write exposure, but it is inconsistent with the input-path rule at `:336-337`. Fix: lstat/symlink-reject the companion path, or document that `--companion` is an explicit operator input.
4. **Low — unreachable branch.** `:502-503` (`source_disclosure_digest_mismatch`) cannot fire once `:500` equality holds and the literal sha is correct. Harmless; keep as a guard or delete.
5. **Design note (not a defect).** `companion != build_companion()` (`:588`) makes the companion a pure function of the tool literals. Real anchors are the frozen digests at `:68-84` checked against bytes at `:399-409`; the literals are the authority and their review belongs in LOG. Companion adds no independent evidence beyond that.
6. **Hygiene — untracked artifact.** `tools/__pycache__/witness-metadata.cpython-314.pyc` (created 01:51) is untracked and `git check-ignore` reports it is not ignored. Remove before admission or add an ignore rule. Not removed by this review.

### Exact checks for L1 to run (not run here)

- `sha256sum .ufo/evidence/round-12/BashWitness/{summary.json,declaration.json,declared.tsv} .ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json` — compare to `witness-metadata.py:68-84,125-127`.
- `python3 tools/witness-metadata.py --selftest` — expect `SELFTEST: PASS 25/25`; confirm the `tamper-declared-with-wrong-kind-red` line after finding 1 is fixed.
- `python3 tools/witness-metadata.py --check --json` — expect `"id": "metadata_consistent"`, exit 0.
- `python3 tools/witness-metadata.py --emit | diff - .ufo/evidence/round-13/witness-metadata.json` — expect no diff except trailing newline/indent; confirms companion equals the pinned constants.
- `python3 tools/bash-witness-study.py --selftest` (producer regression, Main-owned) — expect the new `summary preserves top-level exposed declaration kind` check to pass.
- `git diff --stat -- .ufo/evidence/round-12 tools/bash-witness-study.py` — expect `.ufo/evidence/round-12` unchanged; producer diff limited to `:787` and the selftest block.
- `git check-ignore -v tools/__pycache__` — must be ignored or the directory removed.

### Residual risk / gaps

- No runtime evidence: none of the above was executed by this review.
- Tooling: none installed or updated.
