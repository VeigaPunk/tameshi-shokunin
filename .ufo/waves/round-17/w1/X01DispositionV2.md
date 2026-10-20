# X01DispositionV2 — interface contract A (evidence-dispositions-v2)

## Files changed
- `.ufo/waves/round-17/staged/tools/evidence-disposition.py` (new staged copy of
  `tools/evidence-disposition.py` @ `98bea7da`, v1 code untouched, v2 added)

## Implementation notes (staged tool)
- `SCHEMA_V2 = "evidence-dispositions-v2"`; v1 branch and all v1 finding ids are
  byte-identical in behaviour. Unknown schema → `schema_mismatch` (exit 2).
- v2 adds `supersedes` (required; must be a canonical lane-relative path pinned
  in `inputs` — else `input_unpinned`) and `historical_inputs` (required object,
  may be `{}`). Entry shape `{path: {"rev": <40-hex>, "reason": <non-empty>}}`;
  malformed entries → `dispositions_field_invalid`.
- `historical_input_forbidden` (exit 2): key not under `tools/`, checked during
  manifest validation before any hashing.
- `historical_input_unknown` (exit 2): key not in `expected.json inputs`,
  checked after expected is parsed and before any git call.
- Repo-identity guard before every blob read: `git -C <root> rev-parse
  --show-toplevel`, realpath compare vs `realpath(--root)`; failure →
  `historical_input_unavailable`. Guard only runs when `historical_inputs`
  is non-empty, so a v2 manifest without historical keys needs no repo.
- Blob read: `git -C <root> cat-file blob --end-of-options <rev>:<path>`
  (rev pinned to 40-hex, path canonicalised `tools/*` — no option injection;
  `--end-of-options` verified working on host git 2.56.0). Nonzero exit →
  `historical_input_unavailable`. Digest mismatch vs the expected pin →
  `expected_input_digest_mismatch` (same id as live drift; contract wording).
- Non-historical `expected.inputs` keep live-tree `safe_file`/`read_regular`
  integrity-first verification; dispositions `inputs` (incl. `supersedes`) are
  all live-verified.
- Payload (v2 runs only): adds `supersedes` and
  `expected_inputs_historical` {path: rev}. v1 payloads unchanged.

## Acceptance evidence
- Selftest, committed tool @ `98bea7da`:
  `python3 <committed> --selftest` → `SELFTEST: PASS (34/34)`, exit 0.
- Selftest, staged tool:
  `python3 <staged> --selftest` → `SELFTEST: PASS (46/46)`, exit 0.
  New cases (all PASS):
  `v2-clean-historical` (0), `v2-historical-digest-mismatch` (2,
  `expected_input_digest_mismatch`), `v2-historical-unknown` (2,
  `historical_input_unknown`), `v2-historical-forbidden` (2,
  `historical_input_forbidden`), `v2-historical-unavailable-rev` (2,
  `historical_input_unavailable`), `v2-historical-unavailable-object` (2,
  `historical_input_unavailable`), `v2-identity-guard` (nested root inside a
  foreign super-repo → 2 `historical_input_unavailable`),
  `v1-extra-keys-tolerated` (0 — v1 ignores extra top-level keys),
  `v2-live-mismatch-nonhistorical-tool` (2, `expected_input_digest_mismatch`),
  `v2-live-mismatch-nonhistorical-fixture` (2, same),
  `v2-supersedes-unpinned` (2, `input_unpinned`),
  `v2-supersedes-missing` (2, `dispositions_field_invalid`).
  All required Target cases are present; `v1` behaviour unchanged is pinned by
  the 34 inherited cases plus `v1-extra-keys-tolerated`.
- Live /tmp-manifest run (real lane):
  `python3 <staged> --root /home/vgpnk/Projects/shokunin/tameshi-shokunin
   --dispositions /tmp/tameshi-r17w1-X01DispositionV2-e6XRwD/v2-manifest.json
   --json` → exit 0, `status=clean`,
  counts `{expected_checks:12, effective:11, superseded:1, passed:11,
  failed:0, findings:0}`; `supersedes=.ufo/evidence/round-14/dispositions.json`;
  `expected_inputs_historical` = all four `tools/*` keys →
  `4acc607dfd79f19d508bd50cdd06b77269fccd1d`.
  Manifest = round-14 v1 manifest (rows verbatim) + `supersedes` +
  `historical_inputs` on every `tools/*` entry of round-13 expected.inputs;
  each blob digest at `4acc607` verified equal to the expected pin
  (`git cat-file blob --end-of-options <rev>:<path> | sha256` — asserted in
  the builder script).
- v1 round-14 command unchanged under staged tool:
  `--root LANE --dispositions .ufo/evidence/round-14/dispositions.json --json`
  → exit 2, `id=expected_input_digest_mismatch`, message
  `tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…`.
  The committed tool at the same command yields the identical exit/id/message,
  confirming the staged change introduces no v1 regression.

## Findings for L1 (advisory, not in my write set)
- `tools/mutate-and-run.sh` is the only expected-input that drifted live vs
  the round-13 pin (live `0673d2e5…`, pin `75ed934d…`); the other three
  `tools/*` inputs still match live. The v2 manifest at round-13 rev `4acc607`
  restores a clean gate.
- The committed round-14 `dispositions-before.json` is schema v1 with
  `producer_before` effective. For the appended round-17
  `dispositions-before.json` to yield **exit 1** (contract: "1 failed,
  producer_before unresolved") it must itself be v2 with `historical_inputs`
  covering `tools/mutate-and-run.sh` — otherwise the live drift yields exit 2
  before predicates run. It must also carry `supersedes` (required in v2);
  `supersedes: .ufo/evidence/round-14/dispositions-before.json` is the natural
  value.
- Contract wording "v1 fields plus `supersedes` and `historical_inputs`" was
  read literally: both keys are required on v2 manifests. If L1 intends
  optional `historical_inputs`, relax one line in `run_mode`.

## Risks / blockers
- None blocking. `git` must be available in PATH for v2 historical reads
  (host git 2.56.0 observed); `--end-of-options` supported since git 2.36.

No tool installs were needed.

## Follow-up — hardening per K03 G1–G7 and R03 F1–F3

Same write scope: only `staged/tools/evidence-disposition.py` (now 2860 lines) and
this report. No git writes in the lane; no lane files outside these two touched.

### What changed (staged tool only; v1 paths untouched)
- **F1 / ordering:** `historical_inputs` keys are classified (prefix, shape,
  membership in `expected.inputs`) before any live read of those paths; the
  expected-inputs loop dispatches per key, so a waived path is never opened
  through `safe_file`/`read_regular`.
- **G1 `historical_input_unneeded`:** a waived path whose live bytes still equal
  the expected pin exits 2.
- **G2 `historical_input_uncommitted`:** live bytes of a waived path must equal
  `HEAD:<path>` (`ls-tree HEAD`, blob compare); uncommitted worktree edit,
  symlink, or deletion-while-HEAD-has-it exits 2. A committed deletion is
  allowed. G2 takes precedence over F1's "deleted/symlinked must not break a
  waived path" parenthetical — that live state is uncommitted tampering.
- **G3 `historical_input_unavailable`:** `rev-parse --verify <rev>^{commit}` must
  return exactly `rev` (rejects tree/blob/HEAD/branch/abbrev/uppercase) and
  `merge-base --is-ancestor <rev> HEAD` must hold.
- **G4 hermetic git:** every git call runs with all inherited `GIT_*` removed
  plus `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE=/dev/null`,
  `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`; `--absolute-git-dir`
  must be `realpath(root)/.git`, `--show-toplevel` must be `realpath(root)`, and
  shallow repositories are refused. Replace refs are neutralised (not refused).
- **G5:** `ls-tree` entry must be mode `100644`/`100755` type `blob`; bytes read
  as bytes (`capture_output`, never `text=True`).
- **G6:** text mode prints `HISTORICAL <path> rev=<rev> sha256=<sha>` per
  waiver; JSON keeps `expected_inputs_historical` and adds `historical_text`.
- **G7 `supersedes_mismatch`:** the superseded document must be schema v1 with
  this document's `expected_file` and `rows`, and its `inputs` must be pinned
  identically here.
- **R03 F7:** the invalid-schema detail string was reverted to the exact r14
  text (`dispositions schema must be 'evidence-dispositions-v1'`) so a v1
  consumer sees no change.

### Commands / exits
- Staged selftest: `python3 <staged> --selftest` → **`SELFTEST: PASS (56/56)`**,
  exit 0 (56 `SELFTEST_CASE` lines). Committed baseline tool → PASS (34/34).
  New cases: `v2-historical-unneeded` (2 `historical_input_unneeded`),
  `v2-historical-uncommitted` (2 `historical_input_uncommitted`),
  `v2-historical-dangling` (2 `historical_input_unavailable`),
  `v2-historical-tree-id` (2 `historical_input_unavailable`),
  `v2-historical-replace-ref` (0, replace ref present),
  `v2-gitdir-env` (0 with `GIT_DIR`/`GIT_WORK_TREE` exported to a foreign
  repo), `v2-shallow-repo` (2 `historical_input_unavailable`),
  `v2-blob-bytes-crlf` (0, raw CRLF blob bytes),
  `v2-committed-deletion` (0), `v2-supersedes-rows-mismatch` (2
  `supersedes_mismatch`); earlier v2/v1 cases retained.
- Mutant discrimination (each /tmp copy of the staged tool, `--selftest`), each
  red set is exactly the targeted case:
  `no-env` (drop `GIT_ENV_OVERRIDES`) → `v2-historical-replace-ref`;
  `text-blob` (`text=True` blob read) → `v2-blob-bytes-crlf`;
  `no-g1` → `v2-historical-unneeded`; `no-g2` → `v2-historical-uncommitted`;
  `no-ancestry` → `v2-historical-dangling`.
- Live lane, `--root /home/vgpnk/Projects/shokunin/tameshi-shokunin`:
  - `/tmp` manifest waiving **only** `tools/mutate-and-run.sh` at
    `4acc607dfd79f19d508bd50cdd06b77269fccd1d`, superseding
    `.ufo/evidence/round-14/dispositions.json` → **exit 0**, `clean`,
    11 effective + 1 superseded, findings 0; text mode printed
    `HISTORICAL tools/mutate-and-run.sh rev=4acc607… sha256=75ed934d…`.
  - before counterpart (same waiver, supersedes the round-14 before-manifest,
    `producer_before` effective) → **exit 1**, `failed`,
    ids `['expected_contains_missing']`, 11 passed / 1 failed.
  - L1's actual `.ufo/evidence/round-17/dispositions{,-before}.json` (blanket
    4-tool waiver) → **exit 2 `historical_input_unneeded`**:
    `tools/bash-witness-study.py: live bytes still equal the expected pin`.
    **L1 must narrow `historical_inputs` to `tools/mutate-and-run.sh`** (and
    update the manifest reasons) or the integrated gate is red by G1.
  - v1 round-14 manifest at tip → exit 2 `expected_input_digest_mismatch`
    (`tools/mutate-and-run.sh` observed `0673d2e5…` expects `75ed934d…`),
    identical to the committed tool.
- v1 differential (committed vs staged tool, text mode): clean tree at
  `0c6e36d0` (round-14 manifest; all 13 expected inputs match) → both exit 0,
  stdout byte-equal; tampered `verification.json` → both exit 2, stdout
  byte-equal; invalid schema → both exit 2, stdout byte-equal; v1 JSON equal
  after dropping `tool`/`tool_sha256`, no extra keys on v1 runs.

### Residual notes
- `v2-gitdir-env` asserts **0 clean** (environment scrubbing neutralises the
  foreign `GIT_DIR`), not a refusal; K03's A5 expected 2, which is what an
  unscrubbed implementation returns. Scrubbing is the stronger fix.
- G7 makes `supersedes` a checked lineage, so the L1 before-manifest must
  supersede `.ufo/evidence/round-14/dispositions-before.json` (rows copied
  verbatim), not the after-manifest.
- Blocker for integration (not for this build): the two live round-17 manifests
  are rejected by G1 until narrowed to the single moved runner.
