# T58W2Read15 — verified-record

Heading: `### Round-17 gate/probe registry — re-pin and monitor`
C0: `8063d0a551fc5b3cb5a2d397da7353af53444534`
Section: lines 1889–1897, SHA256 `309f83283e7518eb00cf7ce4296daf4bf5e80843ff2b3046755eb55d3ba8fb8c` (frozen round-18 sectionize). Identical section digest at lane base.

## Findings
None in the assigned section. Recommendation only; no admission claimed.

## Executed sweep
Full argv, stdout, stderr and exit values are retained in the adjacent JSON and `T58W2Read15-receipts/command-*.json`.

| Check | Observed output | Exit |
|---|---|---|
| round-18 disposition manifest | `status: clean` | 0 |
| disposition selftest | `SELFTEST: PASS (66/66)` | 0 |
| nonexistent round-17 registry tag | `selects no registry row` | 2 |
| registry selftest | `SELFTEST: PASS (51 cases)` | 0 |
| mutation selftest | `MUTATE_SELFTEST: 107/107 pass`, `VERDICT: PASS` | 0 |
| mutation regression, caller-owned workdir | `REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)` | 0 |
| documented live-fleet pin probe | JSON observations, `result_reuse: not_established` | 0 |
| pin selftest | `SELFTEST: PASS (19/19)` | 0 |
| historical round-17 disposition manifest | `expected_input_digest_mismatch` | 2 |
| full registry at C0 | reviewer timeout at 300 seconds, no captured output | unverified |
| pin selftest with unusable TMPDIR | named `could-not-evaluate` error, no traceback | 2 |
| registry C0, valid new-r17 tag | `REGISTRY_CHECK: held=3/3 superseded=2` | 0 |

## Residual risk / verification gaps
The full registry run did not finish within the imposed limit; no full-monitor pass or saturation claim is made. Scoped replay and selftests do not establish every active row. The live pin probe's sibling states are not pinned to C0. LSP is not mounted (`xd://lsp`: No such tool); supporting code reads are textual only. Referenced round-13/round-16 verdict maps and manifest paths resolved.

Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2Read15` was removed; only processes whose /proc cwd was within it were terminated after the timed-out monitor. No lane source edits or tool installs.

## Self-evaluation
Accuracy 4 (full monitor incomplete, disclosed); completeness 4 (every command variant exercised, full monitor incomplete); clarity 4 (raw receipts are verbose); actionability 4 (explicit monitor gap); conciseness 4 (table plus raw machine evidence). Overall 4.0. Improvement: let an isolated full registry replay finish before claiming full-monitor coverage. The user should agree with the disclosed limits.
