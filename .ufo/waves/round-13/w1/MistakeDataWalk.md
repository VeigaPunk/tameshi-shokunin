# MistakeDataWalk — routed `declaration.kind` null

## Reconstructed contract and evidence

- **Last-known-good source invariant:** `cmd_declare` writes `kind` and `disclosure` as top-level members of `declaration.json`; its separate `declared` object contains the `declared.tsv` path/hash, row count, and `none_rows`, not a `kind` (`tools/bash-witness-study.py:870-883`). The intended literal is **`declared-witness mapping (not a blind preregistration)`** (`:875`). The disclosure at `:185-193` and frozen `declaration.json:5-15` explain prior exposure to recorded aggregate/per-defect outcomes and state that no per-defect witness classification existed before the run.
- **Divergence:** `build_summary` routes `summary.declaration.kind` from `declaration.get("declared", {}).get("kind")` (`tools/bash-witness-study.py:771-789`, specifically `:787`), one level too deep. Since the producer's `declared` object has no `kind`, `.get()` returns `None`; JSON serialization produces `null`. The frozen output confirms this at `.ufo/evidence/round-12/BashWitness/summary.json:12-17`: `kind` is null while disclosure is copied correctly from the top level. This is a deterministic producer/schema-path defect, not evidence that the declaration lacked a kind. The earlier report independently records this explanation and that classification was unaffected (`.ufo/waves/round-12/w2/WitnessFinish.md:245-251`).
- **Frozen-evidence boundary:** The old declaration and summary are recorded in `manifest.json` (`.ufo/evidence/round-12/BashWitness/manifest.json:35,71`); observed SHA-256s are declaration `e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901` and summary `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9`. The summary's embedded tool SHA is `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a`, which matches the currently read `tools/bash-witness-study.py`; the manifest also anchors the original bytes. Do not repair by rewriting either historical file or its manifest. The legacy checker treats an added file in this evidence tree as `UNLISTED` (`tools/bash-witness-study.py:811-831,1507-1520`), so keep the round-13 companion at its assigned separate path `.ufo/evidence/round-13/witness-metadata.json` (round-13 `spec.json`, `MetadataRepair` item, lines 13-15).

## Minimal repair and L1 assertions

Create only the new companion. Anchor its input digests to the exact frozen `summary.json` and `declaration.json` bytes above; retain the old summary's nested null as the historical observation, and derive the normalized kind from the declaration's explicit top-level `kind` (not from `declared.tsv` or a guessed label). Carry the top-level disclosure verbatim so the non-blind/prior-exposure qualification remains explicit. This matches round-13's C2 claim: a digest-anchored normalized companion validates the disclosed non-blind kind while the old-null representation fails (`.ufo/evidence/round-13/claims.json:6`).

L1 should run, but this seat did not run:

```sh
python3 tools/witness-metadata.py --selftest
python3 tools/witness-metadata.py --check
```

Expected negative mutation for the selftest/isolated fixture: change **only the companion's normalized declaration `kind` value** from the exact top-level literal above to JSON `null` (the old-null case); leave both frozen inputs and their recorded digests untouched. Assert `--check` returns exit **1**, status **`metadata_inconsistent`**. The unmutated companion must return exit **0**, status **`metadata_consistent`**. A separate source-byte mutation with stale recorded digest must return exit **2**, status **`snapshot_tampered`**; this distinguishes the intended semantic check from mere digest linkage. Do not perform these mutations against the historical `BashWitness` directory.

## Confidence and method

High confidence in the producer path error and intended value: source construction, summary construction, both frozen JSON files, and the historical round-12 note agree. The LSP device is not mounted in this session (`read xd://lsp` reported no such tool); source locations were confirmed by direct file reads, with text search used only for navigation. No checks, builds, or tool installs were performed.
