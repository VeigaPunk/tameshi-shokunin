# PinSchema — round-13 manifest completeness and input validation review

Supersedes the prior review. Reviewed revision: baseline HEAD `546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50`; tool and manifest are uncommitted.

Current artifacts:
- `tools/pin-disposition.py` sha256 `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11`
- `.ufo/evidence/round-13/pin-manifest.json` sha256 `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6`

Scope: read-only. No checks, selftests or tests were run. No implementation was edited.

## Verified

- Manifest pins match `tools/mutate-and-run.sh:542-553`. Repo/path match `:84-89` and `:1112-1140`.
- Leg-set validation (exact six, no duplicate, no unknown), repo/path equality, 40-hex commit, 64-hex digest, duplicate JSON key rejection, exit 2 on invalid input.
- Pinned, HEAD and worktree kept separate. Unchanged requires verified pin plus byte equality. HEAD never substitutes for worktree.
- `result_reuse` is literal `not_established` on every row.
- Repo identity proves its own toplevel; worktree file is lstat/O_NOFOLLOW, contained in repo.
- Added selftest arm `pinned-blob-mismatch` (`pin-disposition.py:1035-1048`, reason at `:307-308`) present: valid-format wrong digest → exit 0, pinned.status=mismatch, content unavailable.

## Status of prior findings

1. **Pins not checked against runner at run time** — accepted as residual per L1 ruling. Manifest is the configured pin authority; main cross-checks manifest against the unchanged runner and records the runner sha.
2. **Git error classed as absent** (`:284-285`, `:326-329`) — residual, documented by PinProbe. Content stays unavailable; reason precision only.
3. **Selftest gaps** — mismatch arm closed. Worktree symlink and outside-repo arms remain uncovered (low, not required by spec).
4. **Missing individual leg exits 0 unavailable** — accepted per L1 ruling.

## Checks L1 should run (not executed here)

- `python3 tools/pin-disposition.py --selftest` → exit 0, `SELFTEST: PASS`; confirm `pinned-blob-mismatch` case line is PASS.
- `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → exit 0; six legs; all `result_reuse` = `not_established`.
- `sha256sum` both files against the digests above to detect a stale review.
- Main: confirm the manifest-vs-runner cross-check and record the runner sha (`75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` at review time, per manifest `derived_from`).

## Residual risk

- Behavior is unverified (no execution).
- Mode/exec-bit not compared (`NOT_COMPARED`, by design).
- Tooling: no installs or updates by this seat.
