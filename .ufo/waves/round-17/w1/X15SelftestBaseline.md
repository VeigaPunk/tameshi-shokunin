# X15SelftestBaseline — no-harm baseline at 98bea7d

## Scope
Ran every registered lane selftest plus `mutate-and-run.sh --regression` in a
fleet-mirror clone of `tameshi-shokunin` at
`98bea7da5801f4bc58e4187690ee1687c8a5061f` (clone HEAD verified with
`git rev-parse HEAD`). Sibling `*-shokunin` repos were symlinked beside the
clone so `mutate-and-run.sh` could resolve `FLEET_ROOT`. No lane file outside
the two owned paths was written; all runs are hermetic (mkdtemp fixtures).

## Results

| run | tool | exit | pass | elapsed_s | tool sha256 |
|-----|------|------|------|-----------|-------------|
| mutate-and-run --selftest | tools/mutate-and-run.sh | 0 | 83/83 | 5.325 | 0673d2e5…8118aa |
| mutate-and-run --regression | tools/mutate-and-run.sh | 0 | 7/7 cases | 121.431 | 0673d2e5…8118aa |
| bash-witness-study selftest | tools/bash-witness-study.py | 0 | 41/41 | 0.058 | 49e9e5e2…50ad80 |
| context-capture --selftest | tools/context-capture.py | 0 | 49/49 | 1.479 | c4a1d165…601726 |
| evidence-disposition --selftest | tools/evidence-disposition.py | 0 | 34/34 | 1.069 | 1609a9df…d42d2d95 |
| pin-disposition --selftest | tools/pin-disposition.py | 0 | 18/18 | 0.852 | 29725397…f14f11 |
| repeat-control --selftest | tools/repeat-control.py | 0 | 29/29 | 0.808 | 296fe566…cbc25 |
| witness-metadata --selftest | tools/witness-metadata.py | 0 | 39/39 | 1.505 | df339068…0bed4 |
| round-16 measure --selftest | .ufo/evidence/round-16/measure.py | 0 | 38/38 | 0.905 | 03b67f58…ffbb |
| round-16 assemble --selftest | .ufo/evidence/round-16/coldread/assemble.py | 0 | 38/38 | 0.039 | 9ee9264a…a156 |
| round-16 reattribute --selftest | .ufo/evidence/round-16/attribution/reattribute.py | 0 | 8/8 new-rule | 0.032 | eaf564e4…015c1 |
| round-15 verify --rev 7650fe4d | .ufo/evidence/round-15/verify.py | 0 | 44/44 | 2.052 | 7e4519d9…2522 |

**Totals: 12/12 runs exit 0; 428/428 sub-checks pass; ~135.6 s cumulative.**

## Evidence
- Key lines: `MUTATE_SELFTEST: 83/83 pass / VERDICT: PASS`;
  `REGRESSION: PASS (cases=7 passed=7; ledger legs exact)`;
  `WITNESS_SELFTEST: 41/41 pass / VERDICT: PASS`;
  `SELFTEST: PASS (49/49)`; `SELFTEST: PASS (34/34)`;
  `SELFTEST: PASS (18/18)`; `SELFTEST: PASS (29 cases)`;
  `SELFTEST: PASS 39/39`; `MEASURE_SELFTEST: 38/38 pass`;
  `SELFTEST: all checks passed` (38 `[ok]`, 0 `[not ok]`);
  `SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)`;
  verify.py: 44 `: PASS` lines, 0 `: FAIL`, exit 0.
- The 5 literal `FAIL` tokens in reattribute stdout are the intended
  old-rule-fails assertions, not failures (stated in its PASS line).
- Full sha256 values, per-run argv/exit/elapsed and summary lines:
  `.ufo/evidence/round-17/noharm-baseline-98bea7d.json`.
- Tool sha256 are blob-content hashes re-verified against the pinned rev via
  `git show 98bea7d:<path> | sha256sum` (all 11 matched).

## Risks / notes
- Runs were executed concurrently; elapsed values reflect wall time under a
  parallel batch, not isolated timing. `--regression` dominated (121 s).
- `--regression` workdir `/tmp/tameshi-r4-2-regression.Xgm5t3` was removed on
  PASS as designed.
- No tool installs were needed; nothing installed.
- Scratch clone at `/tmp/tameshi-r17w1-X15SelftestBaseline-*/` left in /tmp
  (ephemeral; not a lane path).

Verdict: holds — every lane selftest and the regression leg passes at 98bea7d.
