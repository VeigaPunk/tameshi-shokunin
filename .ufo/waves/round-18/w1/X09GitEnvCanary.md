# Round 18 wave 1 — Git environment canary

Axes: depth (measure every registered selftest), calibration (attribute changes only to the injected canary repository); operability monitored.

## Method and evidence

Implemented `.ufo/evidence/round-18/git-env-canary.py`. It resolves the requested commit, clones it detached into a `/tmp` fleet-mirror, reads that clone's `tools/registry.json`, and runs each row identified as a selftest (registry `kind: selftest`, `--selftest` argv, or final `selftest` argv). Each run gets a separate throwaway Git repository, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` aimed only at that canary. Before/after fingerprints cover HEAD, refs/packed-refs, index/index.lock, and objects.

Command at the assigned base:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/git-env-canary.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 183f87b899e6cae46be98d251cbc87fb5118f6ca
```

Tool exit: **0** (complete report; no row timed out). Key output: `REV 183f87b899e6cae46be98d251cbc87fb5118f6ca`, `SELFTEST_ROWS 14`, `TOUCHED_TOOLS none`.

## Per-row command, exit, and canary verdict

| Registry row | Command | Exit | Canary |
|---|---|---:|---|
| repeat-control-selftest | `python3 tools/repeat-control.py --selftest` | 0 | clean |
| bash-witness-selftest | `python3 tools/bash-witness-study.py selftest` | 0 | clean |
| pin-disposition-selftest | `python3 tools/pin-disposition.py --selftest` | 0 | clean |
| witness-metadata-selftest | `python3 tools/witness-metadata.py --selftest` | 0 | clean |
| evidence-disposition-selftest | `python3 tools/evidence-disposition.py --selftest` | 0 | clean |
| context-capture-selftest | `python3 tools/context-capture.py --selftest` | 0 | clean |
| mutate-and-run-selftest | `bash tools/mutate-and-run.sh --selftest` | 0 | clean |
| measure-round16-selftest | `python3 .ufo/evidence/round-16/measure.py --selftest` | 1 | clean |
| assemble-round16-selftest | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 | clean |
| reattribute-round16-selftest | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 | clean |
| registry-check-selftest | `python3 tools/registry-check.py --selftest` | 0 | clean |
| measure-round17-selftest | `python3 .ufo/evidence/round-17/measure.py --selftest` | 0 | clean |
| trace-inputs-round17-selftest | `python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest` | 0 | clean |
| assemble-round17-selftest | `python3 .ufo/evidence/round-17/coldread/assemble.py --selftest` | 0 | clean |

**Touched tools:** none. No canary HEAD, refs, index, or object-database changes were observed.

## Deviations and risks

- The expected `tools/bash-witness-study.py` hit was **not observed**: its registered `selftest` row exited 0 and its canary remained clean. At the pinned source, `cmd_selftest` is at `tools/bash-witness-study.py:1218`; the Git materializer is separate at `:332-344`, outside that selftest path. Thus this result measures the registered selftest path and does not demonstrate that the tool's other modes scrub inherited Git environment.
- `measure-round16-selftest` exited 1 while its canary remained clean. Its captured child output was not retained by the probe; this report records the measured exit without assigning a cause.

**partial** — probe and all 14 canary observations completed at the requested base, but the expected Bash-witness touch was absent and one selftest returned nonzero.
