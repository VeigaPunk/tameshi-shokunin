# MetadataRepair — round 13 (C2 companion metadata)

Status: implementation landed; no checks executed by this seat (per contract).
Score delta **0/0** — this metadata repair is not a depth or calibration move
(`measure.py` never reads the companion; no SHONEN, runner, or scored ledger
was touched).

## Axes

| Axis | Move | Harm check |
|---|---|---|
| depth | unchanged — no new recorded leg, no kill-rate/7th-case claim | none |
| calibration | unchanged (0/0) — null defect repaired as provenance metadata only, no promotion | none |
| coverage | unchanged — no new province/surface | none |
| operability | local improvement — new bounded fail-closed gate + companion | none; frozen bytes read-only |
| freshness | unchanged — rerun null named and integrity-checked, still uncorrected | none |
| adjacency | unchanged — sibling gates/runner never executed or edited | none |

## Files

- `tools/witness-metadata.py` (new, 1290 lines) — sha256
  `df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4`.
- `.ufo/evidence/round-13/witness-metadata.json` (new companion) — sha256
  `463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d`.

Nothing under `.ufo/evidence/round-12/` was written; all round-12 reads are
read-only. `tools/bash-witness-study.py` and `tools/mutate-and-run.sh` were
not edited (L1 owns the producer root fix). Tool installs/updates: none.

## Root cause being repaired (not rewritten)

`tools/bash-witness-study.py:787` writes
`declaration.kind = declaration.get("declared", {}).get("kind")`; the explicit
frozen kind is top-level at `.ufo/evidence/round-12/BashWitness/declaration.json:6`.
The frozen `summary.json` therefore records `declaration.kind = null`. The
companion adds normalized metadata only and preserves that null as a historical
fact.

## Companion schema (pinned literals, no invented kind)

- `expected`: `{"id": "metadata_consistent", "exit": 0}`.
- `frozen_declaration` map pins the three files the checker reads, and the tool
  pins the same literals (`tools/witness-metadata.py:68-86`), so the companion
  is not self-certifying:
  - `summary.json` `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9`
  - `declaration.json` `e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901`
  - `declared.tsv` `0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3`
- `producer`: historical producer identity `tools/bash-witness-study.py`
  `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a`,
  source `summary.json#/tool`, `checked_live: false`. The gate never live-hashes
  the producer or runner, so C2 does not depend on C1's tool bytes.
- `historical_runner`: `tools/mutate-and-run.sh`
  `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`,
  source `declaration.json#/inputs/runner`, `checked_live: false`.
- `declaration.kind`: exact frozen top-level string
  `declared-witness mapping (not a blind preregistration)`; never a shortened
  label, enum, or null-as-blind fallback.
- `declaration.disclosure`: byte-equal to frozen disclosure; pinned sha256
  `ec6e5be711945a84e1148819a12d7897386c319a2544b8b0829b4bd74af9b2f0`;
  `prior_exposure: true`, `blind: false`.
- `original_nested`: `source: summary.json#/declaration/kind`,
  `value: null`, `state: historical-null-preserved`, plus a note that the null
  is not authority.
- `scope`: covers canonical `summary.json` (sha above); explicitly names the
  second frozen null at `rerun-20261020T035435Z/summary.json`
  (`6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0`) as
  `named-residual-uncorrected` / `sha256-anchored-and-reverified`. It remains
  outside normalized scope; the gate hashes that file and asserts null kind,
  byte-equal disclosure, and the declared.tsv binding so the claim is not
  literal-only.
- `frozen_bytes_rewritten: false`, `measured_claim_unchanged: true`.

## Gate behavior (`--check`, default live-read inside lane)

Order is integrity-first, then semantics; no writes.

1. Companion must be a regular file (symlinks rejected via `lstat`) and is
   loaded with strict JSON (UTF-8, duplicate keys rejected, NaN/Infinity
   rejected, top-level object required).
2. **All four pinned files are resolved, hashed and cached before any exit-1
   comparison**: `summary.json`, `declaration.json`, `declared.tsv`, and the
   rerun summary. Paths are tool literals (not companion-controlled), must be
   relative, contain no `..`, have no symlink components, resolve inside the
   lane root, and be regular files. A tampered byte therefore always wins over
   a companion semantic defect (`0` companion + tampered rerun → exit 2).
3. Companion schema/expected record and digest-map agreement with the tool
   literals; no frozen re-read.
4. Frozen JSON parsed from the exact captured bytes (no TOCTOU re-read):
   producer/runner identities, rerun residual, exact top-level kind,
   byte-equal disclosure, nested null, declared.tsv binding.
5. Companion kind/disclosure/prior-exposure/blind/nested-null semantics.
6. Full canonical equality with `build_companion()`; any unmodeled key or
   rewritten note/value fails `companion_noncanonical`.

Verdicts (one ID + exit; `--json` gives one object):

```text
exit 0  metadata_consistent      reason=ok
exit 1  metadata_inconsistent    e.g. normalized_kind_null, normalized_kind_mismatch,
                                 disclosure_missing, disclosure_mismatch,
                                 blind_upgrade_rejected, prior_exposure_missing,
                                 original_nested_value_missing, original_nested_not_null,
                                 expected_record_missing, scope_uncovered_missing,
                                 schema_mismatch, producer_missing,
                                 runner_identity_mismatch,
                                 frozen_bytes_claim_invalid,
                                 companion_noncanonical
exit 2  snapshot_tampered        *_digest_mismatch, companion_inputs_mismatch,
                                 companion_path_mismatch, companion_digest_invalid,
                                 companion_digest_unpinned
exit 2  input_unavailable        companion_missing, companion_path_rejected,
                                 *_json_invalid, *_json_not_object, input_missing,
                                 path_rejected, lane_root_unavailable,
                                 unexpected_exception
```

Unexpected exceptions are caught and mapped to exit 2; no traceback reaches
the operator. `--selftest` invokes this CLI as a subprocess over isolated
`tempfile.mkdtemp()` fixtures (removed in `finally`); fixture expectations are
literal in `SELFTEST_CASES` (`tools/witness-metadata.py:659`).

Selftest case IDs / expected exits (all persisted in tool):

```text
corrected-companion-green                          metadata_consistent/ok/0
old-null-red                                       metadata_inconsistent/normalized_kind_null/1
expected-record-missing-red                        metadata_inconsistent/expected_record_missing/1
rerun-scope-omitted-red                            metadata_inconsistent/scope_uncovered_missing/1
producer-checked-live-red                          metadata_inconsistent/producer_checked_live_invalid/1
extra-blind-key-red                                metadata_inconsistent/companion_noncanonical/1
tamper-rerun-red                                   snapshot_tampered/rerun_summary_digest_mismatch/2
tamper-plus-companion-defect-red                   snapshot_tampered/rerun_summary_digest_mismatch/2
tamper-declaration-red                             snapshot_tampered/declaration_digest_mismatch/2
symlink-input-red                                  input_unavailable/path_rejected/2
symlink-companion-red                              input_unavailable/companion_path_rejected/2
lane-root-missing-red                              input_unavailable/lane_root_unavailable/2
nan-companion-red                                  input_unavailable/companion_json_invalid/2
non-object-companion-red                           input_unavailable/companion_json_not_object/2
invalid-utf8-companion-red                         input_unavailable/companion_json_invalid/2
wrong-schema-red                                   metadata_inconsistent/schema_mismatch/1
frozen-manifest-not-object-red                     snapshot_tampered/companion_inputs_mismatch/2
companion-path-mismatch-red                        snapshot_tampered/companion_path_mismatch/2
producer-missing-red                               metadata_inconsistent/producer_missing/1
runner-mismatch-red                                metadata_inconsistent/runner_identity_mismatch/1
frozen-flag-rewritten-red                          metadata_inconsistent/frozen_bytes_claim_invalid/1
wrong-kind-short-red                               metadata_inconsistent/normalized_kind_mismatch/1
wrong-kind-blind-red                               metadata_inconsistent/normalized_kind_mismatch/1
absent-disclosure-red                              metadata_inconsistent/disclosure_missing/1
disclosure-mismatch-red                            metadata_inconsistent/disclosure_mismatch/1
blind-upgrade-red                                  metadata_inconsistent/blind_upgrade_rejected/1
prior-exposure-missing-red                         metadata_inconsistent/prior_exposure_missing/1
nested-null-omitted-red                            metadata_inconsistent/original_nested_value_missing/1
nested-null-rewritten-red                          metadata_inconsistent/original_nested_not_null/1
tamper-summary-red                                 snapshot_tampered/summary_digest_mismatch/2
tamper-declared-before-kind-red                    snapshot_tampered/declared_digest_mismatch/2
missing-companion-red                              input_unavailable/companion_missing/2
malformed-json-red                                 input_unavailable/companion_json_invalid/2
duplicate-key-red                                  input_unavailable/companion_json_invalid/2
missing-input-red                                  input_unavailable/input_missing/2
path-escape-red                                    input_unavailable/path_rejected/2
extra-input-red                                    snapshot_tampered/companion_inputs_mismatch/2
missing-digest-red                                 snapshot_tampered/companion_digest_invalid/2
unpinned-digest-red                                snapshot_tampered/companion_digest_unpinned/2
```

The two tamper cases carry a wrong kind too, proving digest-before-compare;
`tamper-plus-companion-defect-red` proves a tampered rerun is reported as
exit 2 even when the companion also has an exit-1 defect.

## Red-before construction (reported, not executed)

Before the companion existed, the default command was red:

```sh
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 tools/witness-metadata.py --check --json
# intended: exit 2, id=input_unavailable, reason=companion_missing
```

Old-null versus kind-only correction, same command shape (old-null companion is
the production companion with `declaration.kind` set to `null`):

```sh
python3 - <<'PY'
import json
src = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/witness-metadata.json"
c = json.load(open(src))
c["declaration"]["kind"] = None
json.dump(c, open("/tmp/witness-metadata-old-null.json", "w"), indent=2)
PY

for c in /tmp/witness-metadata-old-null.json \
         /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/witness-metadata.json; do
  python3 tools/witness-metadata.py --check --companion "$c" --json
  echo "exit=$?"
done
# intended: old-null  exit 1 metadata_inconsistent/normalized_kind_null
#           corrected exit 0 metadata_consistent/ok
```

## Exact checks L1 should run (not run here)

1. `python3 tools/witness-metadata.py --selftest` → 39 `SELFTEST_CASE … OK`
   lines and `SELFTEST: PASS 39/39`, exit 0, no `Traceback` (subprocesses use
   `python -I`; a 60 s timeout marks a case FAIL instead of crashing).
2. The same-command loop above → first exit 1 / `normalized_kind_null`,
   second exit 0 / `metadata_consistent`.
3. `python3 tools/witness-metadata.py --check --json` → exit 0,
   `{"id":"metadata_consistent","reason":"ok",...}`, `inputs_verified` names
   `summary`, `declaration`, `declared`.
4. `python3 tools/witness-metadata.py --emit | cmp - .ufo/evidence/round-13/witness-metadata.json`
   → exit 0, empty output (companion matches canonical builder).
5. Frozen-byte guard (read-only): sha256 of the three pinned round-12 files and
   `rerun-…/summary.json` must still equal the literals above; selftest also
   asserts this before/after fixtures.
6. Negative stdout/exits are emitted by selftest and should be retained by Main
   with the companion digest map above.

## Risks / blockers

- The gate deliberately requires the companion to equal `build_companion()`;
  any future companion edit must update the tool constants in the same change.
  This is the no-invented-kind / no-silent-extra-key boundary, not an accident.
- The producer SHA is a historical identity. L1's planned fix to
  `bash-witness-study.py:787` changes the live producer; the gate intentionally
  does not live-hash it, preserving C1/C2 independence.
- The rerun summary null is digest-anchored and read as a raw historical
  observation, but explicitly **not** normalized or corrected; the canonical
  summary is the only covered null observation.
- An explicit `--companion` outside the lane remains accepted (needed for the
  direct old-null red probe). It is read-only, and the success record names the
  resolved `lane_root` plus `companion_in_lane: false`, so it cannot be
  mistaken for an in-lane verification. Input files are always tool-pinned
  lane-relative paths and are hash-verified before comparison.
- CLI usage errors keep argparse's exit 2, matching the declared registry
  convention; they are not counted as `input_unavailable` receipts.
- Generated `tools/__pycache__/witness-metadata.cpython-314.pyc` (01:51) was
  not produced by this seat's script execution; it is consistent with a
  reviewer importing the module. It was removed; `tools/__pycache__` is now
  absent. Report provenance is unknown beyond that inference.
- No sibling gate, mutation runner, or repeat-control CLI was executed. No
  frozen round-12 bytes were modified.
