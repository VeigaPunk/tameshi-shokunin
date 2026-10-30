# T58W1ExecInstr — instrument selftests and diff audit

Freeze selected from the lane history command (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format='%H %s' -8`): `e2c2e654ff4c764d554810eabc849370052743d7`, `round-58: freeze (5/5) ...`. A shared scratch clone was detached at that commit.

## Executed checks

- `python3 -I .ufo/evidence/round-58/c1/measure.py --selftest --work <scratch>` — **C1_R58_SELFTEST: 110/110 pass** (exit 0).
- `python3 -I .ufo/evidence/round-58/c2/measure.py --selftest --work <scratch>` — **C2_R58_SELFTEST: 23/23 pass** (exit 0). This includes the strict element-equality and exact exit-2-code cases.
- `bash -n .ufo/evidence/round-58/controls.sh .ufo/evidence/round-58/no-harm.sh .ufo/evidence/round-58/deciding-run.sh` — silent (exit 0).

## Diff audit

Ran `diff -u .ufo/evidence/round-57/c1/measure.py .ufo/evidence/round-58/c1/measure.py` and the corresponding command for `c2/measure.py`; both returned 1, as expected for differences.

C1 differences: round labels/output strings, BASE re-pin to `2a32aa8228d5f86a85c81a923a3148bf792a9538`, defects/panel paths and defects digest, hard exclusions, corresponding fixture setup and assertions. A9 provenance lookup changes from round-57 w2/w3 seat/results to round-58 w1 seat/results. The changed provenance wave location is a behavioral topology change in service of this round's w1 panel; no other behavioral change was observed in the complete textual diff.

C2 differences: round labels/output strings and mutants path re-pin; `row_named_codes` now accepts only stdout_contains elements exactly equal to a gate code, and exit-2 rows must include exact `RECEIPT_REV_UNRESOLVABLE`; three strictness selftest cases were added, with fixture paths/prefix updated to round 58. No other behavioral change was observed in the complete textual diff.

Scratch clone/work directory removed. No tools installed or updated.