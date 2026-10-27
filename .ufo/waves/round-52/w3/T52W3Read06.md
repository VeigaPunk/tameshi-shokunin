## Findings

- F1: “N=8 since round 18, N=9 since round 26, N=10 since round 51.” **SKILL.md:976** — stale as a current count: CAND1 `tools/mutate-and-run.sh` runs ten embedded legs and its `--selftest` also checks `calls=10 specs=10 nlegs=10` (`tools/mutate-and-run.sh:2013-2015`; `.ufo/waves/round-52/w2/T52W2Fix06.selftest.out:83-95`). The dated milestones are accurate, but the unqualified present-tense count of current legs is superseded by round 52's ten-leg state. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | sed -n '976p'; git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:tools/mutate-and-run.sh | sed -n '1500,1550p;2013,2018p'`

- F2: “`MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 at `cf41efaa…`” **SKILL.md:1003-1004** — the command's 67/67 output and 0 exit are dated historical evidence at the old tool revision; however, the round-52 parenthetical's precise claim that “the same command prints `MUTATE_SELFTEST: 107/107 pass`” is not supported by the cited selftest receipt: it shows `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`, but does not record the command, exit status, or tool sha. The section's assertion of the same command's rc 0 at tool sha `977de470…` therefore overstates what the cited receipt establishes. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:.ufo/waves/round-52/w2/T52W2Fix06.selftest.out; git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:tools/mutate-and-run.sh | sed -n '2121,2132p'`

## Holds

1. `REGRESSION_TOOL`, `REGRESSION_DATE`, `REGRESSION_BAND`, `REGRESSION_EXPECT`, per-leg `REGRESSION_PIN`, `REGRESSION_SWEEP`, `REGRESSION_TABLE`, `REGRESSION_CASE`, differing-row `REGRESSION_DEFECT`, `REGRESSION_WORKDIR`, and closing `REGRESSION: PASS|FAIL|SETUP` are the documented record fields. Checked CAND1 runner header `tools/mutate-and-run.sh:144-157`.
2. PASS's exact-ledger criteria (case band and table match, zero flips; closing case count) hold for current runner; `run_regression` uses exact per-leg tolerance and emits the stated PASS format. Checked `tools/mutate-and-run.sh:133-143, 1540-1541`; the current ten-leg count is finding F1.
3. Historical T7-1 measured instance: four legs, `match=10/10`, flips 0, closing `cases=4 passed=4`, rc 0 is corroborated by `reports/r7-aud-t7.md:43-56` and is explicitly dated in the section.
4. FAIL row format and out-of-band case format are implemented; `ABSENT` is emitted on either unmatched recorded/measured row. Checked `tools/mutate-and-run.sh:1353-1372, 1391-1401`.
5. SETUP distinctions and environment remedy are consistent with runner setup refusal and exit map. Checked `tools/mutate-and-run.sh:139-143, 1276-1280`.
6. Ledger PASS is explicitly limited to pinned-table reproduction, not today's gate effectiveness; rate/pin scoping is stated in `corpus/knowledge/fleet-kill-rate-ledger.md:13-14, 21-39`.
7. Round-7 plan supports the sibling-claim attestation discipline and no-edit boundary: replay read-only or name missing part; `plans/round-7.plan.md:11-15`.
8. Selftest's historical 67/67 claim is an accurately dated T7-1 fact, and round-52 selftest's specific arms (git-materialized replay, drifted tree, setup paths, flipped entry) are represented in CAND1 tool code and round-52 receipt. Checked `tools/mutate-and-run.sh:167-176, 2013-2021`; `.ufo/waves/round-52/w2/T52W2Fix06.selftest.out:53-82`.

## Summary

- Findings: 2 (current regression-leg count; round-52 selftest receipt does not establish the cited command/rc/tool sha).
- Holds checked: 8.
