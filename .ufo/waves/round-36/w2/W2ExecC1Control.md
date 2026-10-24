# C1 do-nothing control rerun

## Attack
Re-ran C1's cold-read monitor at content commit `e423c41ba253357ab8c8513f0376dad9d38ab248`, the parent of refresh commit `b455001e2589b3f4f471d94a3de7e5e549b9f54c`. This is the do-nothing control; no ledger refresh is present at the tested revision.

## Commands and retained evidence

Resolved the commit chain with this read-only command:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log -n 15 --format='%H %P %s'
```

The log identifies `b455001e2589b3f4f471d94a3de7e5e549b9f54c` as the refresh commit with parent `e423c41ba253357ab8c8513f0376dad9d38ab248`.

Ran and captured the requested monitor command:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control && python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev e423c41ba253357ab8c8513f0376dad9d38ab248 > /fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.stdout 2> /fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.stderr; status=$?; printf 'EXIT=%s\n' "$status" > /fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.exit; printf 'EXIT=%s\n' "$status"; wc -c /fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.stdout /fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.stderr
```

Observed exit `0`; captured stdout is 247191 bytes and stderr is empty. The captured JSON reports `calibration_restraint_score: 6`, `coldread.sections_covered: 60`, and `coldread.sections_total: 64`. Captures are retained at:

- `/fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.stdout`
- `/fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.stderr`
- `/fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.exit` (`EXIT=0`)

Compared the captured stdout and exit receipt to the committed control receipt, and hashed both stdout files:

```sh
if cmp -s /fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.stdout /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/control/monitor-at-e423c41b.stdout; then printf 'STDOUT_BYTE_IDENTICAL\n'; else printf 'STDOUT_BYTE_DIFFERENT\n'; fi; if cmp -s /fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.exit /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/control/monitor-at-e423c41b.exit; then printf 'EXIT_BYTE_IDENTICAL\n'; else printf 'EXIT_BYTE_DIFFERENT\n'; fi; sha256sum /fast/scratch/hyaku/tameshi-r36-seats/W2ExecC1Control/monitor-at-e423c41b.stdout /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/control/monitor-at-e423c41b.stdout
```

Observed `STDOUT_BYTE_IDENTICAL` and `EXIT_BYTE_IDENTICAL`. Both stdout SHA-256 values are `b49c84b1599369e4ee61cd87367e73734768cd509cd298af6e78d3023458a44c`. The committed receipts are `.ufo/evidence/round-36/control/monitor-at-e423c41b.stdout` and `.ufo/evidence/round-36/control/monitor-at-e423c41b.exit` (`EXIT=0`).

## Verdict
**VERDICT: AGREE** — rerun at the content commit prints score 6 and coverage 60/64; captured stdout and exit status agree byte-for-byte with the committed control receipt.

## Risks / blockers
None observed. This report covers only the assigned C1 control rerun.
