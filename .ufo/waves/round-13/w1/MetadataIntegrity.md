# MetadataIntegrity — round 13 w1 (read-only review, advisory)

Scope: digest coverage and integrity-before-comparison for the new companion metadata gate (C2 calibration repair of null `declaration.kind`). Frozen round-12 bytes preserved check. No checks, tests, builds, or sibling gates were run. No implementation edits.

## Implementation state observed

- `tools/metadata.py`: absent. `.ufo/evidence/round-13/witness-metadata.json`: absent. `git status --porcelain` shows only `?? .ufo/waves/round-13/`. Nothing has landed yet; findings below are design-stage anchors for the owning executor (`MetadataRepair`, per `.ufo/waves/round-13/w1/swarm-registry.json`).
- Baseline HEAD `546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50`. `git diff --quiet 9df9212 -- .ufo/evidence/round-12 tools/bash-witness-study.py tools/mutate-and-run.sh` is clean (no diff output).

## Frozen anchors (read-only sha256 observed now; match the round-12 manifest and commit 9df9212 blobs)

| File | sha256 | Observed in |
|---|---|---|
| `.ufo/evidence/round-12/BashWitness/summary.json` | `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9` | manifest.json:71; git 9df9212 blob |
| `.ufo/evidence/round-12/BashWitness/declaration.json` | `e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901` | manifest.json:35; declaration-before-run.txt:3 |
| `.ufo/evidence/round-12/BashWitness/declared.tsv` | `0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3` | manifest.json:37; summary.json:14; declaration.json:10 |
| `.ufo/evidence/round-12/BashWitness/manifest.json` | `273ffc39308a6c55bdb1c8f7a86bac9f95886ec470773c99b4d1e2db5b25e1cf` | NOT listed in any manifest; git 9df9212 blob only |
| `tools/bash-witness-study.py` (producer) | `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a` | summary.json:10 (tool.sha256); selftest.sha256.txt:1 |
| `.ufo/evidence/round-12/BashWitness/pristine.sh` | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` | manifest.json:38; declaration.json:20 |
| `.ufo/evidence/round-12/BashWitness/bash-surface-census.spec` | `d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741` | manifest.json:4; declaration.json:27 |
| `tools/mutate-and-run.sh` (runner) | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` | declaration.json:44; declaration-before-run.txt:6 |

## Findings (ordered by severity)

1. **Null kind is silently authoritative in current verification (`check` reports CLEAN).** Producer: `tools/bash-witness-study.py:787` reads `declaration.get("declared", {}).get("kind")`, but `kind` is top-level in `declaration.json:6` (written at `bash-witness-study.py:875`). Result: `summary.json:15` `"kind": null`. `cmd_check` (`:1118-1215`) and `cmd_count` (`:1041-1115`) never compare `summary.declaration.kind` or `summary.declaration.disclosure` to `declaration.json`, so the null passes both. The companion gate MUST compare these two fields only after digest verification and MUST treat a null/absent normalized kind as a named failure, not a pass.

2. **Anchor gap: the summary digest is rooted only in an unanchored manifest.** `summary.json` is trusted via `manifest.json:71`; `manifest.json` (`273ffc39…`) is not pinned by `declaration-before-run.txt` (pins only declared.tsv, declaration.json, pristine.sh, spec, runner), nor by `declaration-hash.txt` (pins only `pristine.sh`), nor by itself (`manifest_files` excludes it). Only git commit 9df9212 anchors it. The companion gate MUST carry literal expected digests for `summary.json`, `declaration.json`, `declared.tsv`, and `manifest.json` in code (not read from the files it verifies, and not copied from a runtime-written file). Pinning `manifest.json` closes the chain.

3. **Producer identity not pinned in the companion path.** `tools/bash-witness-study.py` is not in the manifest; its digest appears only as `summary.json:10` (`249d9dcd…`) and matches the working tree now. The spec forbids editing it (writable paths: `tools/metadata.py`, `.ufo/evidence/round-13/witness-metadata.json`). If anyone edits `:787` in that file, the current tool sha no longer equals `summary.tool.sha256`; the companion must record the summary's tool sha as the producer identity of the frozen bytes and must NOT claim the current tool produced them. Any regenerated summary would be a new artifact, not a repair of the frozen one.

4. **Companion output location is outside the round-12 manifest walk.** `.ufo/evidence/round-13/witness-metadata.json` is not covered by `cmd_check`'s `UNLISTED`/manifest logic (`:1182-1206`). The new file needs its own pinned digest (external to itself) and its inputs must be read with `Path` containment (no `..`, no symlink escape), matching the `UNSAFE` pattern at `:1188-1195`.

5. **Pattern to reuse (correct today, must be kept).** `verify_declared_digest` (`:510-519`) fails with `Fail("TAMPER …")` before any comparison; `cmd_count` calls it first (`:1044`). Malformed JSON raises `Cannot` (`:500-507`, `:1051-1054`). The companion should keep this taxonomy: digest mismatch → Fail (exit 1, named TAMPER); missing/unreadable/malformed → Cannot (exit 2, could-not-evaluate); never a silent null. Required ordering: (a) hash all anchored inputs against literals → Fail on mismatch; (b) parse JSON → Cannot on error; (c) only then derive normalized kind from top-level `kind` plus equality of `disclosure`; (d) never read `summary.declaration.kind` as authority.

6. **Frozen-bytes preservation.** Nothing in the design may write under `.ufo/evidence/round-12/`. `write_json` (`:765-768`) is only reached from `declare`/`run`/`rerun` paths; the companion must not import or invoke them. `summary.json` must not be rewritten; `count`/`check` remain unchanged.

## Exact checks for L1 to run after landing (not executed by this seat)

1. `sha256sum` each anchor in the table above; each must equal its literal. Confirm literals in `tools/metadata.py` equal the table.
2. `git diff --quiet 9df9212 -- .ufo/evidence/round-12 tools/bash-witness-study.py tools/mutate-and-run.sh` → exit 0; `git status --porcelain -- .ufo/evidence/round-12 tools/bash-witness-study.py` → empty.
3. Companion selftest plus negative mutants, each must exit nonzero with a named reason and emit no normalized kind: (a) one byte flipped in a copy of `summary.json`; (b) `declaration.json` with top-level `kind` removed; (c) `declaration.json` with `declared.kind` injected but top-level kind absent; (d) malformed JSON in a copy of `summary.json`; (e) missing `declared.tsv`; (f) `disclosure` mismatch between summary and declaration; (g) path containing `..` or symlink target; (h) manifest.json byte flip.
4. Positive: companion output on the frozen evidence reports kind = top-level `kind` string `declared-witness mapping (not a blind preregistration)` and keeps prior exposure (disclosure text) — not blind.
5. Existing probe, unchanged: `python3 tools/bash-witness-study.py check` and `python3 tools/bash-witness-study.py count` must still exit 0 with the same CLEAN/counts as round-12 closure (declared.tsv sha `0def0d3…`, 96 files covered, 95 manifest entries; killed_on_witness=8, survived=2, total=10).
6. After all runs: re-hash the anchor table; `git status --porcelain` shows only `tools/metadata.py`, `.ufo/evidence/round-13/witness-metadata.json`, and round-13 report paths.

## Residual risk / verification gaps

- No implementation exists yet; this review cannot confirm digest coverage of the new gate code. Re-review after landing is required.
- `check` does not validate `summary.status`'s consistency with `kind`; that is a C2 scope item, not in this seat's scope.
- No tool installs or updates were performed by this seat (RULES.md recorded: none).
