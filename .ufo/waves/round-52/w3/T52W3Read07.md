## Findings
- F1: “`tools/env-diff.py` | probe | `python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /tmp/tameshi-f5.json`” — the `--out` pathname in the purported runnable entry is hard-coded to `/tmp/tameshi-f5.json`, but the round-52 scratch directive explicitly prohibits writing there beyond small files; it is not a valid reusable invocation under the current required workflow. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:SKILL.md | sed -n '1964,2103p'`.
- F2: “`tools/env-diff.py` | probe | ...” write-scope claim “isolated `/tmp/tameshi-r21-envdiff.*`” is stale: CAND1 `tools/env-diff.py` calls `tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff.", dir="/tmp")` (around line 60); the declared scratch rule requires `/fast/scratch/...` and limits writes under `/tmp`. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:tools/env-diff.py | rg -n 'TemporaryDirectory|dir="/tmp"'`.

## Holds
- Checked 6 pointers/statements: Source lesson and knowledge entry exist; `env-diff.py` and the round-21 contract/receipt exist; round21 facade and frozen cold-read probe exist. Their fleet-bound details and paths hold at CAND1. Commands: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:<path>` for each pointer.

## Summary
- Two findings: stale hard-coded `/tmp` output and environment-diff scratch location.
- Section hash recorded in the JSON deliverable.
