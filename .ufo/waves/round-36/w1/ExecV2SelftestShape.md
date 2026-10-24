# Round 36 W1 — v2 before-mode self-test

Attacked: C2 depth surface, by running the frozen `c1-measure-v2.py` before-mode arm at the assigned round-35 base revision. No production artifacts were edited.

Exact command run (work path was created empty under the assigned scratch root):

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r36-seats/ExecV2SelftestShape/work && python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/c1/c1-measure-v2.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 51d3f08073be65d3475cf0286042fc0dbe4c4a7d --work /fast/scratch/hyaku/tameshi-r36-seats/ExecV2SelftestShape/work --before; rc=$?; printf 'COMMAND_EXIT=%s\n' "$rc"
```

Retained command output:

```text
C1_R36V2: mode=before tool_present=0 runner_sha_ok=1 rev=51d3f08073be65d3475cf0286042fc0dbe4c4a7d C1_R36V2_PASS=false
COMMAND_EXIT=1
```

Verdict: PASS — the before arm printed `mode=before` and `C1_R36V2_PASS=false`, and the process exited 1, as assigned.

Risks/blockers: none observed for this scoped run.
