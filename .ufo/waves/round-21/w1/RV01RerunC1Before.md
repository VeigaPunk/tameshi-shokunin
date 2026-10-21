done

# C1 rerun result

## Findings
- Both requested revisions measured **0 killed / 18 survived / 0 inconclusive** (18 total). Every row has `anchor_count: 1`; all four pristine controls exited 0; every mutant selftest exited 0 without timeout. All 18 ordered mutant IDs and verdicts match `c1-before.json`.
- **Agreement:** the rerun at `08175c62d661fddf052ed10abc91313dec8eb77d` agrees with the frozen baseline receipt (`killed: 0`, `survived: 18`, `inconclusive: 0`). The independent run at `33d03b716d3edcf1d8656d46d6df61801d232c52` gives the same counts and row verdicts. No count disagreement observed.
- The ruler's nonzero exit is expected: its documented exit is 0 only when every mutant is killed, and 1 when a complete measurement contains any non-kill. Neither run was a setup failure or inconclusive measurement.

## Exact commands and results
1. `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 08175c62d661fddf052ed10abc91313dec8eb77d --json`
   - Exit: **1**.
   - JSON stdout: `/tmp/tameshi-r21-RV01RerunC1Before/out-08175c62.json` (12,241 bytes; SHA-256 `ab8450d4f950cd3a788477c98c9fb5cb9ab91dc8c1baf889c039c481171775be`). Receipt fields: `killed=0 survived=18 inconclusive=0 total=18`.
   - Observed stderr summary: `C1: killed=0 survived=18 inconclusive=0 total=18 rev=08175c62d661fddf052ed10abc91313dec8eb77d`.
2. `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 33d03b716d3edcf1d8656d46d6df61801d232c52 --json`
   - Exit: **1**.
   - JSON stdout: `/tmp/tameshi-r21-RV01RerunC1Before/out-33d03b71.json` (12,242 bytes; SHA-256 `13982b9b3a8d4c300f6d2ba5539a2a86e5b95a60056de43fc30a9310a359598d`). Receipt fields: `killed=0 survived=18 inconclusive=0 total=18`.
   - Observed stderr summary: `C1: killed=0 survived=18 inconclusive=0 total=18 rev=33d03b716d3edcf1d8656d46d6df61801d232c52`.

For each run, the stderr row reports were all `SURVIVED`: `MB03`–`MB12` (`tools/bash-witness-study.py`), `D02`, `D11`, `D12` (`tools/evidence-disposition.py`), `R02`, `R05`, `R07` (`tools/registry-check.py`), and `T04`, `T12` (`tools/trace-inputs.py`). The JSON stdout files above are the retained full receipts.

## Provenance, differences, and gaps
- Both commits resolved successfully. Current ruler SHA-256 `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396` and spec SHA-256 `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c` match the receipt and `c1-before.json`; all four tool blob digests also match the baseline receipt. The ruler uses private temporary clones; its clone and selftest paths scrub `GIT_*` variables. No lane tree files were changed except this report. No tools were installed or updated.
- The receipt is not byte-identical to the earlier `c1-before.json`: run durations differ, and the same-revision rerun has different `registry-check.py` stdout digests for the pristine control and rows R02/R05/R07. Those recorded selftests still exit 0 with `SELFTEST: PASS (48 cases)` and the rows still survive. I did not determine the cause of those digest differences; they do not alter the requested count comparison.
- Baseline evidence: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-before.json` (SHA-256 `7614cd394c0059d4cfe3cb4ffe17aa9c4151e3595be48d2d167763f032aa45ce`). Stderr was observed in the command results; it was not separately saved as a scratch file.