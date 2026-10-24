# C1 before-measurement spotcheck

## Attack
Attacked C1's calibration baseline at revision `796e08b888849308d0c4d5e932e56833600a139f` using the requested cold-read measurement command from `/fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorBefore/`.

## Commands and retained evidence
- Prepared scratch: `mkdir -p /fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorBefore`
- Ran the requested command directly once:
  `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 796e08b888849308d0c4d5e932e56833600a139f`
- Replayed that same command to retain stdout, stderr, and process exit status:
  `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 796e08b888849308d0c4d5e932e56833600a139f > /fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorBefore/monitor-at-796e08b.stdout 2> /fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorBefore/monitor-at-796e08b.stderr; status=$?; printf '%s\n' "$status" > /fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorBefore/monitor-at-796e08b.exit; printf 'exit=%s\n' "$status"; wc -c /fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorBefore/monitor-at-796e08b.stdout /fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorBefore/monitor-at-796e08b.stderr`
- Compared captured stdout byte-for-byte with the committed receipt using:
  `if cmp -s /fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorBefore/monitor-at-796e08b.stdout /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/after/monitor-at-796e08b.stdout; then printf 'BYTE_IDENTICAL\n'; else printf 'BYTE_DIFFERENT\n'; fi`

Captured run: exit status `0`; stdout `247100` bytes; stderr `0` bytes. Captured stdout is byte-identical to `.ufo/evidence/round-36/after/monitor-at-796e08b.stdout`. Both files report `calibration_restraint_score: 6` and `sections_covered: 60` (`sections_total: 64`). The output and exit status are retained under `/fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorBefore/` as `monitor-at-796e08b.stdout`, `monitor-at-796e08b.stderr`, and `monitor-at-796e08b.exit`.

## Verdict
VERDICT: AGREE — C1 before-measurement receipt agrees byte-for-byte; score is 6 and coverage is 60/64 at the specified revision.

## Risks / blockers
The first direct run's tool display was truncated and did not expose an explicit exit status, so the identical command was replayed once with stdout/exit capture. The captured replay exited 0 and is the byte-compared evidence. No other blockers.