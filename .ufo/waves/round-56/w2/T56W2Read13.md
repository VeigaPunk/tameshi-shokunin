# T56W2Read13 — cold-read report

Heading: `### Round-17 gate/probe registry — re-pin and monitor`  
Candidate: `c0137451f5b7f22d65f748fc69f1b181f55e1378`  
Section range at C0: `SKILL.md:1889-1897`  
`section_sha256`: `309f83283e7518eb00cf7ce4296daf4bf5e80843ff2b3046755eb55d3ba8fb8c`

## Verdict

**verified-record** — no false statement or failing command found in this section. The section text/hash is identical at base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` (lines 1876-1884) and C0 (line numbers shifted only).

## Verification sweep

Ran the table commands at C0 in a detached scratch clone; repeated the primary evidence-disposition, self-test, pin-disposition, and mutation self-test commands from the lane root where applicable.

- **evidence-disposition:** round-18 dispositions returned exit 0, `status=clean`, `effective=11`, `superseded=1`; round-17 dispositions returned exit 2 (`expected_input_digest_mismatch`); round-18 `dispositions-before.json` returned exit 1 with `status=failed`, `failed=1`, expectation `producer_before`; `--selftest` passed 66/66; no-argument usage returned 64.
- **registry-check:** `--selftest` passed 51 cases; an invalid registry, unknown revision, and unmatched tag each returned 2; unknown-flag usage returned 64; a differing registry run returned 1. The lane-root C0 run reported `REGISTRY_CHECK: held=48/50 superseded=7`.
- **mutate-and-run:** `--selftest` passed 107/107; lane-root `--regression` with usable TMPDIR passed all 10/10 legs (exit 0); a clone with an unresolved/borrowed sibling repository returned SETUP with `repo_identity_mismatch` (exit 2), matching the row's stated SETUP-2 case; no-argument usage returned 64.
- **pin-disposition:** the listed probe returned exit 0 with 6 observations (1 unchanged, 5 changed, 0 unavailable); `--selftest` passed 19/19. With unusable TMPDIR, `--selftest` returned 2 and named the value without a traceback. The normal probe with the same unusable TMPDIR returned 0 because it allocates no scratch.
- The required fleet census command `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exited 0.

Receipts are under `T56W2Read13-receipts/`.

## Notes (not findings in this section)

1. The pin-disposition TMPDIR exit-2 arm applies to the allocating `--selftest` path. The normal probe stays lazy and exits 0 with an unusable TMPDIR; the row's parenthetical points to the self-test, but naming the mode explicitly would prevent over-application.
2. The C0 registry-check result is 48/50 held, exit 1. Active differences are `sources-census` (expect 0, got 1) and `verify-round15` (expect 0, got 1). The same two active rows differ at base (47/49 across 49 active rows), so this is pre-existing tree state, not a false exit-map statement in this section. The lane-internal `sources-census-v2.sh` reports `SOURCES_CENSUS: VIOLATIONS` for S280 (`corpus/knowledge/scratch-root-contract.md` lacks `S280` and `Errors.html`); the separate required fleet census command above passes. `verify-round15` reports `registered-tool-source-pin: FAIL` for `tools/context-capture.py` (worktree/C0 SHA `831b781054d701d7347df62c4044eb274a775967aaf0ce3d49bef4056b111d8d`, pinned `c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726`).
3. The registry-check `clone failed` exit-2 arm was not independently forced; its other listed exit arms were exercised.
