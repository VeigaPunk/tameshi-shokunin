# T58W2Read17 — gap-minor

C0: `8063d0a551fc5b3cb5a2d397da7353af53444534`
Section: SKILL.md:2007–2146; SHA-256 `eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06`.

## Findings by severity

### Minor — env-diff clone entry omits fleet-root prerequisite

`python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /fast/scratch/hyaku/tameshi-r58/T58W2Read17/tameshi-f5.json` from the detached C0 clone exited 1:

```text
ENVDIFF: classified=0/9 out=/fast/scratch/hyaku/tameshi-r58/T58W2Read17/tameshi-f5.json
```

All nine receipt surfaces report `PIN_UNREADABLE`. Adding `--fleet-root /home/vgpnk/Projects/shokunin` exits 0 with `ENVDIFF: classified=9/9`. Document this live-read prerequisite, rather than presenting clone-default execution as portable. This is a reader-operability gap, not a falsification of the retained historical F5 result. Full outputs: `T58W2Read17-receipts/command-08.json`, `command-19.json`, and `env-default.json`.

## Sweep and residual risks

- Axes: calibration, runnable command accuracy, pointer integrity, non-mutation.
- LSP unavailable: read xd://lsp returned No such tool; text/source checks are fallback, not semantic reference proof.
- Every assigned section line (2007–2146) read at C0; base-to-C0 SKILL.md diff is empty. Dependency drift, not a newly changed paragraph.
- All seven documented selftests passed: 9/9, 8/8, 13/13, 12/12, 8/8 plus 16/16, 44/44, 10/10.
- Default route-mix returns 1 because live provider concentration is 34/71; the section explicitly predicts live route drift. Not a finding.
- C1 returned killed=18 survived=0 total=18; C2 returned classified=9/9. C2 is retained-metadata checking with live fleet reads, not fresh execution authenticity.
- Wrong-count and source-read expected-red controls returned TOTAL_MISMATCH and ARGV_MISMATCH as documented.
- All 24 extracted full-path pointers resolve; three frozen C1/C2 instrument/population files exactly match 33d03b7. Registry successors and pinned bundle digests match the text.
- Round24 observations project successfully: 43 rows, revision_pinned=41, two live_dependent. Attempted round23 observations return INVALID_OBSERVATIONS because this is a different observation format; no documentation promised cross-format compatibility, so not a finding.
- Historical round23 isolation and round24 write-scope claims are explicitly superseded by corrections in this same section; do not count preserved historical text as current unqualified claims.
- Not exercised: registry-replay --run against the entire live-linked registry, because the section itself warns it can write live siblings and lane writes are forbidden by this assignment. Selftest, plan, and projection exercised; no --run safety pass claimed.
- No tools installed. Scratch removed before delivery.

All 20 executed command argv, cwd, exit, stdout and stderr records are retained in the adjacent JSON and receipt directory. Pointer/frozen/registry checks are in `static-checks.json`. No admission or authenticity verdict is implied.
