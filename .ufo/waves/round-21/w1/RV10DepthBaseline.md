# RV10 Depth no-harm baseline @ 33d03b716d3edcf1d8656d46d6df61801d232c52

**Verdict: done.** Both depth no-harm monitors hold at the frozen base: command D reports `recorded_cases=8 depth_score=8` (expected 8), and `tools/mutate-and-run.sh --regression` reports `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`, exit 0.

## Findings

1. **Depth axis (SCORECARD.md:73 command D)** — `recorded_cases=8 depth_score=8`, exit 0, 0.018 s. Matches the context expectation (recorded_cases=8) and SCORECARD's depth rule (one point per recorded ledger case, cap 10). The 8 recorded cases are the eight `#   js-*|bash-*` ledger rows in `tools/mutate-and-run.sh` (legs 1–8, r18 state).
2. **Regression gate** — `bash tools/mutate-and-run.sh --regression` in a scratch clone detached at 33d03b716d3edcf1d8656d46d6df61801d232c52: **exit 0, PASS, cases=8 passed=8**, wall time 125.4 s. Every leg reproduced its recorded table exactly (flips=0, inconclusive=0, killed-delta=0, defects = recorded count; controls green and MUTATE_RESTORE: OK are implied by the exact-band PASS — no leg printed FAIL/SETUP). stderr empty (0 lines).
3. **First regression attempt was a SETUP refusal, not a measurement** (exit 2, `repo_identity_mismatch ... toplevel=unresolved`, cases=8 passed=0 cannot-verify=8): I had cloned only tameshi-shokunin without the sanctioned sibling symlinks. Fixed by creating the bounds-prescribed read-only symlinks `/tmp/tameshi-r21-RV10DepthBaseline-x/fleet/<sibling> -> /home/vgpnk/Projects/shokunin/<sibling>` for the other 20 fleet repos; the r17 identity guard explicitly accepts symlinked fleet paths (realpath equality, `mutate-and-run.sh:1112-1119`). Attempt-1 outputs preserved as evidence; its kept workdir is `/tmp/tameshi-r4-2-regression.ETlnvG` (SETUP keeps workdir per contract); the PASS run removed its own workdir.
4. No harm: the lane working tree was only read (`git show`, file reads); sibling repos were only read via their git object stores (`git show <rev>:<path>`); the clone is at `/tmp/tameshi-r21-RV10DepthBaseline-x/fleet/tameshi-shokunin` (HEAD = 33d03b716d3edcf1d8656d46d6df61801d232c52, verified by `rev-parse`). GIT_* scrubbed from the regression run's environment. No tools installed (none needed).

## Exact commands, exits, durations

| # | Command (cwd unless noted) | Exit | Duration | Result |
|---|---|---|---|---|
| 1 | `git show 33d03b7…:tools/mutate-and-run.sh \| python3 -c '<SCORECARD.md:74 one-liner>'` (lane repo, read-only) | 0 | 0.018 s | `recorded_cases=8 depth_score=8` |
| 2 | `git clone -q --no-hardlinks <lane> /tmp/tameshi-r21-RV10DepthBaseline-x/fleet/tameshi-shokunin && git -C <clone> checkout -q --detach 33d03b7… && git -C <clone> rev-parse HEAD` | 0 | — | `33d03b716d3edcf1d8656d46d6df61801d232c52` |
| 3 | `bash tools/mutate-and-run.sh --regression` (clone; no sibling symlinks yet) | 2 | <0.05 s | `REGRESSION: SETUP (cases=8 passed=0 cannot-verify=8)` — refusal, kept as evidence |
| 4 | symlink 20 fleet siblings into clone `fleet/`, then `bash tools/mutate-and-run.sh --regression` (clone, GIT_* scrubbed) | 0 | 125.4 s | `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)` |

Note on (1): the very first invocation of command D printed a corrupted duration because the tool session was busy and the clock straddled a queue wait; it was re-run cleanly (row 1 above, canonical). The `recorded_cases=8 depth_score=8` output was identical in both runs.

## Per-leg results (attempt 4, all PASS)

| Leg | Repo @ rev (pinned target sha256, mode) | defects | killed | survived | kill-rate | flips |
|---|---|---|---|---|---|---|
| js-kimi-census | kumitate @ 175de6ba… (83016d45…, 100644) | 10 | 8 | 2 | 80% | 0 |
| bash-surface-census | kagi @ fecee874… (275d8294…, 100755) | 10 | 8 | 2 | 80% | 0 |
| bash-tsukuroi-census | tsukuroi @ 165307fe… (084951be…, 100755) | 10 | 6 | 4 | 60% | 0 |
| bash-mado-verify | mado @ eead56b2… (d7edaab4…, 100755) | 10 | 4 | 6 | 40% | 0 |
| bash-checklist-run | kagi @ fecee874… (7e5ec98b…, 100755) | 15 | 7 | 8 | 47% | 0 |
| js-claims-check | kumitate @ 175de6ba… (e9a21b44…, 100755) | 10 | 7 | 3 | 70% | 0 |
| js-round-gate | kumitate @ 364f1d59… (f890e277…, 100755) | 10 | 5 | 5 | 50% | 0 |
| js-sources-check | kumitate @ 0acb7752… (6a293a72…, 100755) | 10 | 5 | 5 | 50% | 0 |

Runner pin: `tools/mutate-and-run.sh` sha256 `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` (r10-2 as committed at the frozen base); REGRESSION_DATE 2026-10-21T12:12:15Z.

## Evidence paths

- `.ufo/waves/round-21/w1/depth/command-D.txt` — command D capture (sha256 `dde8df2e…`)
- `.ufo/waves/round-21/w1/depth/regression.out` — full PASS ledger, 46 lines (sha256 `4fbaf0e1…`)
- `.ufo/waves/round-21/w1/depth/regression.err` — empty (sha256 `e3b0c442…`, the empty-string hash)
- `.ufo/waves/round-21/w1/depth/regression-attempt1-setup.out` / `.err` — attempt-3 SETUP refusal (sha256 `a6d1f1dc…` / empty)
- Clone: `/tmp/tameshi-r21-RV10DepthBaseline-x/fleet/tameshi-shokunin` @ 33d03b716d3edcf1d8656d46d6df61801d232c52

## Residual risk and verification gaps

- None observed for the two monitors. Per-leg durations were not separately captured (legs' `duration-ms` live inside per-leg evidence dirs, removed on PASS); total wall time 125.4 s is recorded. This does not affect the pass/fail evidence.
- Calibration/other no-harm monitors are other seats' items; not run here.
