# Round 35 w2 — ExecSelftest

## Result

**BOUND — one fixture label overstates its behavior.** The selftest catches the `(auto,KEEP)=(0,0)` mutation at `runtime`, but `cfg-gated accept swap (0,0)` does not actually turn a failing verdict into PASS. It only zeros `nfail`; the subsequent tally-completeness guard sees fewer than `nlegs` counted and returns SETUP (exit 2), not PASS. Thus this fixture proves the `(0,0)` configuration is swept and the behavior change is detected, but not that a kill-to-accept mutation under `(0,0)` is detected. Evidence: pinned tool case construction at `tools/tally-audit-v3.py:774-776`; runner tally and count guard at `tools/mutate-and-run.sh:1432-1460`.

**HYGIENE — requested count is stale for these pinned bytes.** The observed output is `TALLY_AUDIT_V3_SELFTEST: 30/30 pass`, not `28/28`. The two additional cases are the A4 real-root kill and comment-accept witnesses at `tools/tally-audit-v3.py:787-790`. All 30 listed cases passed; the six grouped round-35 cases and those two A4 cases are itemized below.

No CRITICAL finding against C1 from this assignment. The A4 real-root gate is killed by the runtime check; its inert-comment counterpart is accepted. No other round-35 case was found to pass for an unintended reason.

## Evidence and method

The source checkout was already at the assigned pin. Exact command and result:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse --verify 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b^{commit} && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD
EXIT=0
7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
```

To respect the no-mutating-git fence, I did not clone or checkout. I used read-only `git archive` of the two pinned inputs in the permitted scratch directory; the selftest reads the adjacent runner from that extracted snapshot:

```text
set -o pipefail && mkdir -p /fast/scratch/hyaku/tameshi-r35-w2/ExecSelftest/pinned && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b tools/tally-audit-v3.py tools/mutate-and-run.sh | tar -x -C /fast/scratch/hyaku/tameshi-r35-w2/ExecSelftest/pinned && sha256sum /fast/scratch/hyaku/tameshi-r35-w2/ExecSelftest/pinned/tools/tally-audit-v3.py /fast/scratch/hyaku/tameshi-r35-w2/ExecSelftest/pinned/tools/mutate-and-run.sh
EXIT=0
ef98fc5367cdb12c71c8b0ddfb5b83835100831f545f6510437dc84014865885  .../tools/tally-audit-v3.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  .../tools/mutate-and-run.sh
```

These hashes match the frozen pins in `.ufo/evidence/round-35/contract.json:7-19`. The test command, run from `/fast/scratch/hyaku/tameshi-r35-w2/ExecSelftest/pinned`, was:

```text
python3 tools/tally-audit-v3.py --selftest
```

Observed wall time: 322.14 seconds. Output ended `TALLY_AUDIT_V3_SELFTEST: 30/30 pass`. Exit is 0: the pinned implementation returns 0 exactly when `passed == len(cases)` (`tools/tally-audit-v3.py:804-821`, `842-844`). The case rows below are the exact observed `CASE` results; the exit in parentheses is the inner audit process exit reported by the selftest, not the outer selftest exit.

## Per-case results

The first six rows are the six grouped round-35 config/stdout and comment-blind cases (`tools/tally-audit-v3.py:774-786`). The final two are the A4 real-root cases (`:787-790`). For kill fixtures, `check='runtime'` makes the selftest require both exit 1 and a `CHECK runtime FAIL` line (`:804-817`); accept fixtures require overall audit exit 0, which means all audit checks passed.

| Case | Observed selftest result | Construction and assertion |
|---|---|---|
| cfg-gated accept swap (0,0) | PASS (exit 1) | Inserts `nfail=0` only for `(0,0)`; requires runtime failure. It is caught, but due to the tally guard it changes FAIL to SETUP rather than PASS (BOUND above). |
| cfg-gated pass mask (1,1) | PASS (exit 1) | Zeros `npass` only for `(1,1)`; an all-zero vector becomes SETUP at the count guard instead of PASS. Requires runtime failure. |
| workdir-branch condition swap | PASS (exit 1) | Replaces the auto/no-keep workdir branch condition with `(0,0)`; the full-stdout oracle exercises the PASS vector and detects the workdir-output/removal change. Requires runtime failure. |
| comment names a leg | PASS (exit 0) | Adds an inert comment naming `st_js`; accepted, as expected for comment-blind structural scans. |
| comment brace in body | PASS (exit 0) | Adds `}` in a shell comment inside the tally body; accepted, as expected when brace scanning uses the comment-blanked code view. |
| comment esac in arm | PASS (exit 0) | Adds `esac` in a shell comment after a case arm; accepted, as expected when case locators use the comment-blanked view. |
| real-root gated mask | PASS (exit 1) | Adds a mask gated on `$auto == 1` and `/tmp/tameshi-r4-2-regression.*`; requires runtime failure. `auto_root()` creates that real prefix and all four configs are run (`:347-369`, `:544-551`). |
| comment names real root | PASS (exit 0) | Adds the real-root string only in a comment; accepted. |

All remaining pinned selftest cases also passed. Their observed inner exits are included here to retain the complete 30-case result:

| Case | Result | Case | Result |
|---|---|---|---|
| pristine | PASS (0) | dup-drop operand | PASS (1) |
| nlegs wrong | PASS (1) | head masked | PASS (1) |
| status 4 passes | PASS (1) | guard undercount only | PASS (1) |
| in-block 7-bit mask | PASS (1) | arm pattern 00 | PASS (1) |
| head overwrite | PASS (1) | printf count swap | PASS (1) |
| majority-gated fail | PASS (1) | keep-conjunct guard | PASS (1) |
| conditional double count | PASS (1) | harness exit-only | PASS (1) |
| harness swallowed | PASS (1) | harness position 8 skipped | PASS (1) |
| harness position 0 skipped | PASS (1) | harness position 1 skipped | PASS (1) |
| aux wrapper loop | PASS (0) | aux pre-count loop | PASS (0) |
| second extraction line | PASS (0) | reversed operands | PASS (0) |

## What I could not break / limits

- The pinned 30-case selftest completed with all cases passing; the six grouped round-35 cases have the expected runtime-fail or overall-pass assertions, except for the inaccurate “accept swap” label described above.
- The A4 root gate is exercised with a real temporary directory using the runner's `/tmp/tameshi-r4-2-regression.` prefix, not a fixed literal (`tools/tally-audit-v3.py:347-369`). The seeded gate is rejected at `runtime`; a comment-only mention is accepted.
- This was a review of the pinned selftest and its constructions, not a new C1 measurement or a broader proof that every possible mutation is covered. I made no changes to the lane or frozen artifacts; no tools were installed.
