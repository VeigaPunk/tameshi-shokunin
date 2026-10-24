# ExecMonitorAfter — C1 refresh measurement

## Attack
Re-ran the C1 calibration monitor at refresh commit `b455001e2589b3f4f471d94a3de7e5e549b9f54c` (receipt basename `monitor-at-b455001e.stdout`). This was limited to the assigned C1 measurement; C2 was not attacked.

## Commands and retained evidence

Resolved the receipt's abbreviated revision:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse --verify b455001e^{commit}
```

Output: `b455001e2589b3f4f471d94a3de7e5e549b9f54c`.

Executed the requested counting command, capturing stdout, stderr and exit status under scratch:

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev b455001e2589b3f4f471d94a3de7e5e549b9f54c
```

- Stdout: `/fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorAfter/monitor.stdout`
- Stderr: `/fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorAfter/monitor.stderr` (empty)
- Exit receipt: `/fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorAfter/monitor.exit` (`EXIT=0`)
- The captured JSON records `rev_input` and `revision` as `b455001e2589b3f4f471d94a3de7e5e549b9f54c`.

Assertions against that captured JSON passed:

```sh
python3 -c 'import json; d=json.load(open("/fast/scratch/hyaku/tameshi-r36-seats/ExecMonitorAfter/monitor.stdout")); c=d["coldread"]; assert d["calibration_restraint_score"] == 8, d["calibration_restraint_score"]; assert c["sections_covered"] == 64 and c["sections_total"] == 64, (c["sections_covered"], c["sections_total"]); print("ASSERTIONS_PASS: calibration_restraint_score=8; sections_covered=64/64")'
```

Full score line from the captured result: `calibration_restraint_score=8; coldread.sections_covered=64/64 (sections_total=64); depth_score=9`.

An initial local assertion attempt looked for `sections_covered` at the JSON top level and raised `KeyError`; the result nests it under `coldread`. The corrected assertion above passed; the measurement itself exited 0.

## Verdict
**VERDICT: C1 after-measurement PASS** — the refresh revision measured calibration restraint 8 with all 64/64 sections covered.
