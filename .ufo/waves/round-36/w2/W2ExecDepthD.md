# W2ExecDepthD — round 36 final-tip reread

## Attack and verdict

Attacked command D (depth) and the calibration cold-read monitor at final lane tip `fbb01cf46f8437fd1264c1a3acc053c882fa2164`, after the receipt commits. **Verdict: command D is unchanged at 9; calibration reads 8/64 at the final tip, matching the measured refresh commit. No input-drift re-trigger was observed between those commits.**

## Exact runs and retained evidence

Working tree: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

1. Command D from `SCORECARD.md:73`, pinned to final revision `fbb01cf46f8437fd1264c1a3acc053c882fa2164` (exit 0):

   `set -o pipefail; REV=fbb01cf46f8437fd1264c1a3acc053c882fa2164; git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))' > /fast/scratch/hyaku/tameshi-r36-seats/W2ExecDepthD/depthD-at-fbb01cf.stdout 2> /fast/scratch/hyaku/tameshi-r36-seats/W2ExecDepthD/depthD-at-fbb01cf.stderr; printf 'exit=%s\n' "$?"`

   Output: `recorded_cases=9 depth_score=9`. Captured at `/fast/scratch/hyaku/tameshi-r36-seats/W2ExecDepthD/depthD-at-fbb01cf.stdout` (stderr empty). The committed refresh-commit receipt at `b455001e2589b3f4f471d94a3de7e5e549b9f54c` likewise says `recorded_cases=9 depth_score=9` and records the pinned runner SHA-256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (`.ufo/evidence/round-36/after/depthD-at-b455001e.stdout`).

2. Calibration monitor at final revision `fbb01cf46f8437fd1264c1a3acc053c882fa2164` (exit 0):

   `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev fbb01cf46f8437fd1264c1a3acc053c882fa2164 > /fast/scratch/hyaku/tameshi-r36-seats/W2ExecDepthD/monitor-at-fbb01cf.stdout 2> /fast/scratch/hyaku/tameshi-r36-seats/W2ExecDepthD/monitor-at-fbb01cf.stderr; printf 'exit=%s\n' "$?"`

   Output fields: `calibration_restraint_score=8`, `sections_covered=64`, `sections_total=64`, `box3_full_page=true`, `trace_gate=strict`, `depth_score=9`. Captured at `/fast/scratch/hyaku/tameshi-r36-seats/W2ExecDepthD/monitor-at-fbb01cf.stdout` (stderr empty). The recorded refresh-commit monitor at `b455001e2589b3f4f471d94a3de7e5e549b9f54c` also reports restraint 8 and coverage 64/64 (`.ufo/evidence/round-36/after/monitor-at-b455001e.stdout`). The pre-refresh baseline `796e08b888849308d0c4d5e932e56833600a139f` reports 6 and 60/64; the content-only control is documented as 6.

## Input-drift disclosure

`SCORECARD.md:1763-1765` explicitly says post-refresh record-keeping commits that touch the four headings' cited inputs re-trigger the monitor's input-drift rule by design, and that 8 is pinned to the refresh commit. I checked the intervening revisions (`b455001e2589b3f4f471d94a3de7e5e549b9f54c` → final `fbb01cf46f8437fd1264c1a3acc053c882fa2164`): the only changed file under `SKILL.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `corpus/`, and `tools/` is `corpus/lessons/round-36-verifier-spotcheck.md`; it is not in the refreshed headings' cited-input sets in `.ufo/evidence/round-36/coldread/refresh-specs.json`. The post-refresh evidence/receipt commits therefore did not change those cited inputs, and the final-tip rerun remains 8/64 rather than re-triggering to 6. The round-36 lesson `## Holds` covers the deferred `code_view` repair and the L1-author-read scope; the input-drift rule is disclosed in the SCORECARD numeric note.

## Risks and blockers

- The 8-point credit is the declared L1-author input-keyed source-read scope, not independent/blind cold-read or recipe re-execution; see the scope wording in `.ufo/evidence/round-36/coldread/refresh-receipts.json`.
- Future edits to cited inputs can invalidate the refresh credit and must be remeasured. No blocker.
