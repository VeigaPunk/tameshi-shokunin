# TameshiR15.RuntimeHarness — round-15 w2 report

Scope: wrote `.ufo/evidence/round-15/verify.py` (new, 834 lines) and nothing
else. Not executed; static review only. Report is the only other write.

## What was implemented

`python3 .ufo/evidence/round-15/verify.py --rev REV` runs, in order, recording
every subprocess stdout/stderr/exit into `verification.json` (exit 0 only when
all checks pass; a first-failure receipt is never overwritten — later attempts
write `verification-N.json`):

1. Resolve `--rev`, `BASELINE` (`a9cf4da…7df0`), `PREFIX_REV` (`bca5deb`).
2. Source/content pins: `tools/context-capture.py@REV` must equal
   `c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726` (final
   w2 bytes per TameshiR15.ContextGate); `@bca5deb` must equal
   `0ed784e0…61edc`; the two round-14 receipts must equal
   `05cb55b8…899c1a` (clean) and `1ee9d09b…a208` (missing-env); runner and
   frozen summary equal the published round-14 digests
   (`75ed934d…adc5`, `acc01268…b9`).
3. Integrity: `capture-context.py`, both receipts, `mutate-and-run.sh`,
   `SHONEN.md`, `round-14-verifier-spotcheck.md` byte-equal baseline↔REV;
   `git diff --name-only` over `.ufo/evidence/round-12..14` empty.
4. Frozen inputs: three own round-15 dirs —
   `frozen/context-clean/{receipt,expected}.json`,
   `frozen/context-missing-env/…`, `frozen/mapping-suffix/…` — with
   `tameshi-context-expected-v1` pins. Existing files are digest-verified,
   never silently overwritten.
5. `expected.json` persisted before any gate run: all input/source SHA-256
   and literal expected exit/id pairs.
6. Same-path contrasts at one temp `candidate.py`, identical argv, only file
   bytes differ: `--selftest` on archived probe bytes (expect 64,
   "unexpected argument") vs final bytes (expect 0, `SELFTEST: PASS (n/n)`);
   usage proof `--check --expected <file> --receipt --json` on prefix bytes
   (expect 2 / `receipt_missing`, no `--json` file created) vs final bytes
   (expect 64 / `id=usage_error`).
7. Registered path run: `tools/context-capture.py --check --json` (built-in
   frozen mode) once, asserting `mode=frozen`, receipt path
   `.ufo/evidence/round-14/context-receipt.json`, `digest_matches`.
8. Explicit gate runs at the temp path: clean 0/`context_consistent`,
   missing-env 1/`missing_injected_environment`, tampered scratch copy
   2/`snapshot_tampered` with `verdict_matches_expected=False`
   (honest clean pin deliberately unmatched — integrity refusal precedes
   verdict), `--receipt`-without-`--expected` 64/`usage_error`.
9. Mapping oracle: mutated receipt (leg0 suffix/constants → BASH, stored
   verdict kept clean) under prefix bytes expect 1/`expected_verdict_mismatch`
   (oracle *fails*), under final bytes expect 1/`mapping_mismatch` with
   `verdict_matches_expected=True` (oracle *passes*); discrimination recorded
   as `mapping-oracle-discriminates` (old FAIL → new PASS required).
10. `measure.py --rev BASELINE` → `before.json`, `--rev REV` → `after.json`,
    plus pinned field assertions (before: context tool absent; after:
    `context_capture_sha256` = pin, `context_gate_active_classification=1`,
    `context_standalone_selftest_present=1`, both 64 classes explicit =2,
    runner/summary digests published-matched, cases 6, restraint 6).
11. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
    end receipt → `sources-after.json`, expecting exit 0 + `tameshi\tok` line.

## Source actually read

- `tools/context-capture.py` (final worktree, tag #7746): docstring exit map
  0/1/2/64; `EXPECTED_SCHEMA` exactly-four-key pin; `parse_argv` rejects a
  `KNOWN_ARGUMENTS` flag as an option value (usage_error/64); `emit` JSON shape
  (`schema tameshi-context-gate-result-v1`, `id`, `exit`, `findings`,
  `receipt.{path,sha256,digest_matches}`, `verdict_matches_expected`);
  `apply_expected` behavior; selftest `SELFTEST_CASE`/`SELFTEST: PASS (n/n)`
  output; usage cases at :2180-2190 including the flag-as-value case.
- `git show bca5deb:tools/context-capture.py`: no `KNOWN_ARGUMENTS` symbol —
  the pre-fix parser consumes `--json` as `--receipt`'s value; frozen root is
  `parents[2]` of the script (temp copies can't do frozen mode).
- `.ufo/evidence/round-14/capture-context.py`: bare-arg guard exits 64 with
  "unexpected argument(s)" — the old `--selftest` expectation.
- `clean receipt mapping.legs[0]`: suffix "JS", constants PIN_JS/REV_JS/
  TABLE_JS — the mutation site for the mapping oracle.
- `measure.py` CLI: `--rev` required, `--baseline` default = round-15
  baseline; output field names used in the pinned assertions.
- `corpus/lessons/round-14-verifier-spotcheck.md` Routed defects 5 (gate
  classification, standalone selftest, explicit 64 classes) and published
  digests; `AGENTS.md`; `sources-census.sh` validate contract;
  `.ufo/evidence/round-12/verify-round.py` as runner precedent.

## Defects / risks (bounded)

- `usage-proof-old` asserts on a *copy* of `bca5deb` bytes, not the worktree —
  pre-fix source is not retained post-commit, so this is the only feasible
  same-path form. Recorded as copied-source; never claimed as registered path.
- `mapping-oracle-old` expectation (`expected_verdict_mismatch/1`) is derived
  from reading `bca5deb`'s recompute path (stored `declared_variable_suffix`
  trust at its :716-721, :1045, :1061), not from execution; if it behaves
  differently the check fails and retains the actual output — no false pass.
- `gate-frozen-builtin` reads `tools/context-capture.py` from the worktree and
  pins it to `c4a1d165…`; if L1 commits different bytes than the announced
  final identity, that check correctly fails rather than silently adapting.
- Frozen explicit-mode runs use absolute paths (temp-path `candidate.py` runs
  from `scratch` cwd); relative receipt paths would mis-resolve otherwise.
- `tool_env()` strips `GIT_*` and pins `LC_ALL=C` for all child processes
  including `git` reads inside `git()` — ambient `GIT_DIR` injection cannot
  redirect the lane's own reads (round-14 lesson).
- Nonzero measure runs still write `before.json`/`after.json` (retain all
  receipts); field checks then fail on unparseable/mismatched output.

## Blockers

None. Two parent corrections mid-flight were incorporated: no `--snapshot`
flag exists (explicit `--check --receipt --expected --json` used), and the
final source pin was updated to `c4a1d165…` after the owner's fixes; pre-fix
`bca5deb` retained only as the old-half oracle.

## Tool installs

None.

## Checks for L1

`python3 .ufo/evidence/round-15/verify.py --rev <final-commit>` once, after
committing the final `tools/context-capture.py` (must equal pin
`c4a1d165…601726`). First-attempt artifacts are preserved; the rerun writes
`verification-2.json` plus `attempt-2/{expected,before,after,sources-after}.json`.
Shared immutable inputs: `frozen/{context-clean,context-missing-env,mapping-suffix}/{receipt,expected}.json`.

## Post-run repair (after failed L1 run 0494c244)

L1's initial run failed only `selftest-new`: the copied tool at
`scratch/candidate.py` made its `DEFAULT_LANE_ROOT=/tmp`, which is a prefix
of the selftest's own `mkdtemp` root, tripping `hermetic-no-lane-path`.
Repairs, none executed:

- Temp layout is now `<scratch>/lane/tools/candidate.py` (parents created);
  same path for old and new bytes; tool source unchanged (pin c4a1d165…).
- Attempt-local outputs: first run wrote `verification.json`,
  `expected.json`, `before.json`, `after.json`, `sources-after.json` at the
  round-15 root and is preserved. A rerun computes serial N from existing
  `verification[-N].json`, writes `verification-N.json` at the root and
  `attempt-N/{expected,before,after,sources-after}.json`; the payload names
  `artifact_dir`. Shared `frozen/` inputs stay immutable digest-verified.
- `main` removes the scratch tree in `finally` (the initial run's
  `/tmp/tameshi-r15-verify-4pexcuhm` is L1's to remove).

No production gate, expected IDs, or pin values changed.
