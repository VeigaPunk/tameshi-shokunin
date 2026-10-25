# CritC1Loop — round-44 w1 findings

Seat: critic, calibration axis. Read-only scratch probes; no lane changes.

## Load-bearing class probes

- The freeze is round 43 and therefore cannot itself contain `**Planned (round 45):**`; the scratch mirror required a minimal Round 44 fixture to exercise the newest-block parser.
- In the Round 44 scratch mirror, removing `**Planned (round 45):**` produced `m12=1`; restoring it produced `m12=0`.
- In a separate mirror with the newest standing `sources-registry` command changed to the column-zero pattern, m13 produced `m13=1`.

The checks are load-bearing on their intended fixture; the control confirms m12/m13 detect these exact missing requirements. This probe does not establish that arbitrary prose cannot spoof the fields beyond the counter's own parser contract.
