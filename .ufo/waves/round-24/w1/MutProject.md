# MutProject — round24 project() mutation probe

## Verdict

The requested detectors killed five of these nine one-point mutants; four survived both detectors. The public selftest killed M01/M02/M03/M05/M06. The frozen K7–K10 slice killed M01/M02/M03 only. M04 (characters instead of UTF-8 bytes), M07 (schema check removed), M08 (requirement-name type check removed), and M09 (stream type check removed) survived both. No baseline failure or inconclusive result occurred. These are bounded coverage findings, not observed failures of the pristine implementation: all six additional counterexample witnesses behaved as expected on pristine and every restored state.

## Axes and scope

- Discrimination: explicit FAIL lines and the specific frozen predicate that changes.
- Independent-trigger coverage: external versus non-hermetic flags; schema versus other shape checks; UTF-8 bytes versus character count.
- Isolation and reversibility: one changed source line at a time, serial mutation/restore, exact SHA-256 restoration before the next mutant.
- Evidence fidelity: actual stdout/stderr/return codes retained; no inference of promotion, producer authentication, historical R17-CMD-BIND closure, or numeric score uplift.

Only the private checkout was mutated. The only write in the production lane is this assigned report. No source integration, registry battery, replay --run, gates, sibling runtime, subagent dispatch, or mutating Git command in the production lane was performed. There were no tool installs or upgrades; the existing Python was `Python 3.14.8`.

## Checkout and immutable identities

Executed from `/tmp`:

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/TameshiR24-2-MutProject-r24 && git -C /tmp/TameshiR24-2-MutProject-r24 checkout -q --detach c8c5b88c8e961a929cdc351b95a7074c76958909
```

Observed exit 0 with empty stdout/stderr. Subsequent process commands used cwd `/tmp/TameshiR24-2-MutProject-r24` (the frozen ruler's nested CLI commands used fixture directories beneath that checkout).

```text
git rev-parse HEAD
c8c5b88c8e961a929cdc351b95a7074c76958909
sha256sum tools/registry-replay.py .ufo/evidence/round-24/measure.py
9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714  tools/registry-replay.py
0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64  .ufo/evidence/round-24/measure.py
python3 --version
Python 3.14.8
```

`P` below means the complete pristine project-file hash `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714`.

## Same bounded detectors in every state

Nineteen states were exercised: pristine, then each of nine isolated mutants and its immediate byte-restored state. Each state ran the same three subprocess commands concurrently; states were strictly serial. All subprocesses had a 120-second outer timeout, `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`, and `TMPDIR=/tmp/TameshiR24-2-MutProject-r24`. No timeout or detector-process error occurred. Every captured subprocess stderr was empty, including the witness wrapper, which explicitly records exceptions as data.

1. `python3 -B tools/registry-replay.py --selftest`.
2. `python3 -B -c RULER_CODE`, where the exact inline code is below. It imports the unchanged frozen ruler and calls its `replay_rows`, preserving the frozen synthetic fixtures and discrimination logic at `.ufo/evidence/round-24/measure.py:139-201`. It records actual CLI I/O without changing return values. The helper also executes K11 internally, but only K7–K10 are selected and reported here; K1–K6 and the full aggregate ruler were not run. Exit 1 from this wrapper means at least one selected frozen predicate stopped discriminating, not an infrastructure error.
3. `python3 -B -c WITNESS_CODE`, reproduced below: additional fixed direct `project()` witnesses. These are not the requested detectors and do not turn a requested-detector survivor into a killed mutant. The wrapper's process exit is always 0 after recording its data; its `exit` fields are the actual values returned by `project()`. `bundle_present` means a returned bundle object, not publication to disk.

All selftest/ruler temporary artifacts were created under the private checkout and removed by their existing TemporaryDirectory scopes. The extra witnesses use in-memory observations and do not publish files.

### Exact RULER_CODE

```python
import importlib.util, json, pathlib, sys, tempfile
root = pathlib.Path.cwd()
spec = importlib.util.spec_from_file_location('round24_ruler', root / '.ufo/evidence/round-24/measure.py')
measure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(measure)
observed = []
frozen_run = measure.run
def record_run(argv, cwd, timeout=600):
    result = frozen_run(argv, cwd, timeout)
    if '--project' in argv:
        observed.append(dict(case=pathlib.Path(argv[argv.index('--project') + 1]).stem,
                             exit=result['exit'], stdout=result['stdout'], stderr=result['stderr']))
    return result
measure.run = record_run
with tempfile.TemporaryDirectory(prefix='mutproject-ruler-', dir=root) as tmp:
    rows = [row for row in measure.replay_rows(root, pathlib.Path(tmp)) if row['id'] in ('K7', 'K8', 'K9', 'K10')]
print(json.dumps(dict(rows=rows, cli_outputs=observed), sort_keys=True))
raise SystemExit(0 if all(row['discriminated'] for row in rows) else 1)
```

### Exact WITNESS_CODE

```python
import copy, importlib.util, json, pathlib
root = pathlib.Path.cwd()
spec = importlib.util.spec_from_file_location('registry_replay', root / 'tools/registry-replay.py')
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)
clean = {'schema': 'registry-replay-observations-v1', 'revision': 'a' * 40, 'cwd': '/fixture/clone',
         'rows': [{'requirement': {'name': 'one', 'argv': ['gate'], 'expect': {'exit': 0}},
                   'external': False, 'argv': ['gate'], 'cwd': '/fixture/clone', 'revision': 'a' * 40,
                   'runner_result': {'got': 0, 'held': True, 'stdout': 'OK', 'stderr': ''}}]}
cases = []
wrong_schema = copy.deepcopy(clean); wrong_schema['schema'] = 'other'
cases.append(('wrong-schema-full-shape', wrong_schema, 8))
wrong_name = copy.deepcopy(clean); wrong_name['rows'][0]['requirement']['name'] = 7
cases.append(('non-string-requirement-name', wrong_name, 8))
wrong_stream = copy.deepcopy(clean); wrong_stream['rows'][0]['runner_result']['stdout'] = None
cases.append(('non-string-stdout', wrong_stream, 8))
multibyte = copy.deepcopy(clean); multibyte['rows'][0]['runner_result']['stdout'] = 'é' * 5
cases.append(('utf8-ten-bytes-limit-eight', multibyte, 8))
external = copy.deepcopy(clean); external['rows'][0]['external'] = True
cases.append(('external-only', external, 8))
nonhermetic = copy.deepcopy(clean); nonhermetic['rows'][0]['runner_result']['non_hermetic_argv'] = ['/live']
cases.append(('non-hermetic-only', nonhermetic, 8))
rows = []
for name, obs, bound in cases:
    try:
        code, report, bundle = replay.project(obs, bound)
        rows.append(dict(case=name, exit=code, report=report, bundle_present=bundle is not None))
    except Exception as exc:
        rows.append(dict(case=name, exception=type(exc).__name__, message=str(exc)))
print(json.dumps(rows, sort_keys=True))
```
## Per-mutant result matrix

`T/F` below are the four actual `discriminated` values in K7, K8, K9, K10 order. A mutant is killed by the requested pair if either requested detector rejects it with a healthy pristine/restored control.

| Mutant | Single changed location | Selftest actual | Frozen K7–K10 actual | Requested-pair verdict |
|---|---|---|---|---|
| M01 held-disabled | `tools/registry-replay.py:89` | exit 1, 8/10 pass; FAIL: not-held, held-missing | exit 1; F/T/T/T | **KILLED** |
| M02 cleanup-disabled | `tools/registry-replay.py:86` | exit 1, 9/10 pass; FAIL: cleanup | exit 1; T/F/T/T | **KILLED** |
| M03 stream-bound-disabled | `tools/registry-replay.py:96` | exit 1, 9/10 pass; FAIL: stream | exit 1; T/T/F/T | **KILLED** |
| M04 stream-characters-not-bytes | `tools/registry-replay.py:96` | exit 0, 10/10 pass | exit 0; T/T/T/T | **SURVIVED** |
| M05 external-disjunct-deleted | `tools/registry-replay.py:99` | exit 1, 9/10 pass; FAIL: external | exit 0; T/T/T/T | **KILLED** |
| M06 nonhermetic-disjunct-deleted | `tools/registry-replay.py:99` | exit 1, 9/10 pass; FAIL: non-hermetic | exit 0; T/T/T/T | **KILLED** |
| M07 schema-check-disabled | `tools/registry-replay.py:74` | exit 0, 10/10 pass | exit 0; T/T/T/T | **SURVIVED** |
| M08 name-type-check-disabled | `tools/registry-replay.py:83` | exit 0, 10/10 pass | exit 0; T/T/T/T | **SURVIVED** |
| M09 stream-type-check-disabled | `tools/registry-replay.py:94` | exit 0, 10/10 pass | exit 0; T/T/T/T | **SURVIVED** |

## Concrete coverage findings and smallest safe correction

1. **UTF-8 byte accounting survives both detectors (M04).** At `tools/registry-replay.py:96`, replacing encoded-byte length with character length leaves selftest at 10/10 and all four frozen rows discriminating. The fixed witness with `stdout = "é" * 5` and `max_bytes = 8` returns `(1, STREAM_LIMIT, no bundle)` on pristine/restored, but `(0, [], bundle present)` on M04. Existing selftest stream cases at `tools/registry-replay.py:202-203` and frozen K9 at `.ufo/evidence/round-24/measure.py:175` use ASCII only. Smallest safe correction: add a multibyte over-limit case to the public selftest (and, if desired, a separate companion calibration probe), retaining the existing byte implementation.

2. **Invalid-input cases do not isolate the checked predicates (M07/M08/M09).** The sole selftest invalid fixture at `tools/registry-replay.py:206` is `{'schema': 'other'}`: it also lacks rows/revision/cwd, so removing just schema validation still returns INVALID_OBSERVATIONS for another reason. A complete wrong-schema observation is accepted by M07; a complete observation with requirement name `7` is accepted by M08; a complete observation with null stdout raises `AttributeError: 'NoneType' object has no attribute 'encode'` under M09 instead of returning INVALID_OBSERVATIONS/2. All three mutants still pass the public selftest and K7–K10. Smallest safe correction: add three independent, otherwise-valid malformed fixtures to the public selftest, asserting code 2, INVALID_OBSERVATIONS, and no bundle. Pristine already meets these checks; no production guard change is indicated by these probes.

3. **K10's combined flags mask loss of either cause (M05/M06).** Frozen K10 sets both `external=True` and nonempty `non_hermetic_argv` at `.ufo/evidence/round-24/measure.py:181`. Deleting either disjunct in `tools/registry-replay.py:99` still leaves K10 discriminating. The public selftest correctly kills each loss separately (`CASE external FAIL` / `CASE non-hermetic FAIL`, 9/10). The additional single-flag witnesses show the incorrect `live_dependent=[]`, `revision_pinned=1` versus pristine/restored `['one']`, `0`. Smallest safe correction: preserve the existing independent selftest cases and use separate single-flag companion probes when making broader calibration claims. Do not rewrite the frozen round24 ruler or expand its contract silently.

The complete held, cleanup and stream-bound deletions are already covered: M01 causes K7 to publish a bundle; M03 causes K9 to publish a bundle; M02 still refuses via RUNNER_NOT_HELD, but its missing RUNNER_CLEANUP_FAILED is correctly caught by K8. This probe does not establish exhaustive mutation adequacy or a shipped defect in pristine project().

## Restoration evidence

Every mutation was reversed through a surgical one-line edit before the next state. The initial pristine run is the control for M01; each immediate restored run is also the next mutant's fresh pristine-byte control. Before/after here refer to bytes before mutation, mutant bytes throughout the detector run, and restored bytes throughout the repeated detector run. No two mutants overlapped.

| Mutant | Before control | Before SHA | Mutant SHA-256 | After restore SHA | Restored requested detectors | Same six restored witness outputs as pristine | Ruler SHA unchanged |
|---|---|---|---|---|---|---|---|
| M01 | `pristine` | P | `7f8b0b2bee998d05b23e1325a889e8a7a51aabf3062e11550a063290b455b892` | P (exact) | selftest exit 0 / 10/10; K7–K10 exit 0, T/T/T/T | true | true |
| M02 | `M01-restored` | P | `2c157c6fda4ebea172e4c2c156412a91b66e92b648ba10e9370729ace41debaa` | P (exact) | selftest exit 0 / 10/10; K7–K10 exit 0, T/T/T/T | true | true |
| M03 | `M02-restored` | P | `89ab44db1ab5756177ae8466e7a6d840ed798b981716d3adcba0cdf4ee2b405a` | P (exact) | selftest exit 0 / 10/10; K7–K10 exit 0, T/T/T/T | true | true |
| M04 | `M03-restored` | P | `bb23d25db8b320a1b5615521aff911b76a2d67e135d9e174d0c01761670d4dce` | P (exact) | selftest exit 0 / 10/10; K7–K10 exit 0, T/T/T/T | true | true |
| M05 | `M04-restored` | P | `7cdcfe66c45b540ab876973c8aa9706ec7222cfee8fab83446ce551f6abee9d6` | P (exact) | selftest exit 0 / 10/10; K7–K10 exit 0, T/T/T/T | true | true |
| M06 | `M05-restored` | P | `c90a48a79c2347f2a8f97dd6028f09390c62319c2ceb5aff42216d24fe0e5e2e` | P (exact) | selftest exit 0 / 10/10; K7–K10 exit 0, T/T/T/T | true | true |
| M07 | `M06-restored` | P | `6502563e72ac6bcce26b5282aa7347c93be403043e5cb4333715dbcbdfc494e0` | P (exact) | selftest exit 0 / 10/10; K7–K10 exit 0, T/T/T/T | true | true |
| M08 | `M07-restored` | P | `fb20816780a176392ea96b577a903dbce12018144f61f03d5deee0d0b5e6ee68` | P (exact) | selftest exit 0 / 10/10; K7–K10 exit 0, T/T/T/T | true | true |
| M09 | `M08-restored` | P | `c1de1f4a66bc75ac242fb9dc90bf47f6ba217b5eae279fc7248af3b2dea9ac9c` | P (exact) | selftest exit 0 / 10/10; K7–K10 exit 0, T/T/T/T | true | true |

The final `M09-restored` run recorded project-file SHA-256 `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714` both before and after its detectors. The frozen ruler hash remained `0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64` in all nineteen states. No mutant bytes remain.

## Actual detector outputs

The JSON sections below show decoded frozen-ruler row values from each wrapper's actual stdout (not a new measurement). The complete public selftest stdout is retained per mutant. Every requested-detector stderr was the empty string. Pristine/restored witnesses and changed mutant witnesses are included separately; exceptions are observations, never counted as requested-detector kills.

### Pristine control (also the observed behavior of all restored controls)

Selftest exit 0, stdout:

```text
CASE clean PASS
CASE not-held PASS
CASE cleanup PASS
CASE held-missing PASS
CASE stream PASS
CASE stream-at-limit PASS
CASE external PASS
CASE non-hermetic PASS
CASE invalid PASS
CASE plan-realpath PASS
REGISTRY_REPLAY_SELFTEST: 10/10 pass
```

Frozen-ruler wrapper exit 0; selected rows:

```json
[
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_NOT_HELD"
    ],
    "id": "K7",
    "name": "runner-not-held-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_CLEANUP_FAILED"
    ],
    "id": "K8",
    "name": "runner-cleanup-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "STREAM_LIMIT"
    ],
    "id": "K9",
    "name": "stream-limit-refused"
  },
  {
    "discriminated": true,
    "exit": 0,
    "id": "K10",
    "name": "live-dependent-listed",
    "report": {
      "bundle_sha256": "5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245",
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 1048576,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

Fixed project() witnesses, wrapper exit 0:

```json
[
  {
    "bundle_present": false,
    "case": "wrong-schema-full-shape",
    "exit": 2,
    "report": {
      "finding_ids": [
        "INVALID_OBSERVATIONS"
      ]
    }
  },
  {
    "bundle_present": false,
    "case": "non-string-requirement-name",
    "exit": 2,
    "report": {
      "finding_ids": [
        "INVALID_OBSERVATIONS"
      ]
    }
  },
  {
    "bundle_present": false,
    "case": "non-string-stdout",
    "exit": 2,
    "report": {
      "finding_ids": [
        "INVALID_OBSERVATIONS"
      ]
    }
  },
  {
    "bundle_present": false,
    "case": "utf8-ten-bytes-limit-eight",
    "exit": 1,
    "report": {
      "bundle_sha256": null,
      "finding_ids": [
        "STREAM_LIMIT"
      ],
      "live_dependent": [],
      "max_stream_bytes": 8,
      "refused_rows": [
        "one"
      ],
      "revision_pinned": 1,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  },
  {
    "bundle_present": true,
    "case": "external-only",
    "exit": 0,
    "report": {
      "bundle_sha256": null,
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 8,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  },
  {
    "bundle_present": true,
    "case": "non-hermetic-only",
    "exit": 0,
    "report": {
      "bundle_sha256": null,
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 8,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

### M01 — KILLED

Location: `tools/registry-replay.py:89`. Expected detector: Selftest not-held/held-missing and frozen K7 reject the weakening.

```diff
- elif result.get('held') is not True:
+ elif False:
```

Selftest exit 1; actual stdout:

```text
CASE clean PASS
CASE not-held FAIL
CASE cleanup PASS
CASE held-missing FAIL
CASE stream PASS
CASE stream-at-limit PASS
CASE external PASS
CASE non-hermetic PASS
CASE invalid PASS
CASE plan-realpath PASS
REGISTRY_REPLAY_SELFTEST: 8/10 pass
```

Frozen-ruler wrapper exit 1; actual selected rows:

```json
[
  {
    "bundle_written": true,
    "control_ok": true,
    "discriminated": false,
    "exit": 0,
    "finding_ids": [],
    "id": "K7",
    "name": "runner-not-held-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_CLEANUP_FAILED"
    ],
    "id": "K8",
    "name": "runner-cleanup-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "STREAM_LIMIT"
    ],
    "id": "K9",
    "name": "stream-limit-refused"
  },
  {
    "discriminated": true,
    "exit": 0,
    "id": "K10",
    "name": "live-dependent-listed",
    "report": {
      "bundle_sha256": "5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245",
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 1048576,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

All six fixed witness outputs were identical to pristine. The requested-detector output above establishes this mutant's verdict.

### M02 — KILLED

Location: `tools/registry-replay.py:86`. Expected detector: Selftest cleanup and frozen K8 require the cleanup-specific finding, not merely refusal.

```diff
- if result.get('cleanup_error'):
+ if False:
```

Selftest exit 1; actual stdout:

```text
CASE clean PASS
CASE not-held PASS
CASE cleanup FAIL
CASE held-missing PASS
CASE stream PASS
CASE stream-at-limit PASS
CASE external PASS
CASE non-hermetic PASS
CASE invalid PASS
CASE plan-realpath PASS
REGISTRY_REPLAY_SELFTEST: 9/10 pass
```

Frozen-ruler wrapper exit 1; actual selected rows:

```json
[
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_NOT_HELD"
    ],
    "id": "K7",
    "name": "runner-not-held-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": false,
    "exit": 1,
    "finding_ids": [
      "RUNNER_NOT_HELD"
    ],
    "id": "K8",
    "name": "runner-cleanup-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "STREAM_LIMIT"
    ],
    "id": "K9",
    "name": "stream-limit-refused"
  },
  {
    "discriminated": true,
    "exit": 0,
    "id": "K10",
    "name": "live-dependent-listed",
    "report": {
      "bundle_sha256": "5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245",
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 1048576,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

All six fixed witness outputs were identical to pristine. The requested-detector output above establishes this mutant's verdict.

### M03 — KILLED

Location: `tools/registry-replay.py:96`. Expected detector: Selftest stream and frozen K9 reject oversized retained streams.

```diff
- if len(text.encode('utf-8', 'surrogateescape')) > max_bytes:
+ if False:
```

Selftest exit 1; actual stdout:

```text
CASE clean PASS
CASE not-held PASS
CASE cleanup PASS
CASE held-missing PASS
CASE stream FAIL
CASE stream-at-limit PASS
CASE external PASS
CASE non-hermetic PASS
CASE invalid PASS
CASE plan-realpath PASS
REGISTRY_REPLAY_SELFTEST: 9/10 pass
```

Frozen-ruler wrapper exit 1; actual selected rows:

```json
[
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_NOT_HELD"
    ],
    "id": "K7",
    "name": "runner-not-held-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_CLEANUP_FAILED"
    ],
    "id": "K8",
    "name": "runner-cleanup-refused"
  },
  {
    "bundle_written": true,
    "control_ok": true,
    "discriminated": false,
    "exit": 0,
    "finding_ids": [],
    "id": "K9",
    "name": "stream-limit-refused"
  },
  {
    "discriminated": true,
    "exit": 0,
    "id": "K10",
    "name": "live-dependent-listed",
    "report": {
      "bundle_sha256": "5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245",
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 1048576,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

Fixed witness outputs that changed from pristine (the other witnesses were identical):

```json
[
  {
    "bundle_present": true,
    "case": "utf8-ten-bytes-limit-eight",
    "exit": 0,
    "report": {
      "bundle_sha256": null,
      "finding_ids": [],
      "live_dependent": [],
      "max_stream_bytes": 8,
      "refused_rows": [],
      "revision_pinned": 1,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

### M04 — SURVIVED

Location: `tools/registry-replay.py:96`. Expected detector: A byte-bound detector should distinguish ten UTF-8 bytes from five characters at an eight-byte limit.

```diff
- if len(text.encode('utf-8', 'surrogateescape')) > max_bytes:
+ if len(text) > max_bytes:
```

Selftest exit 0; actual stdout:

```text
CASE clean PASS
CASE not-held PASS
CASE cleanup PASS
CASE held-missing PASS
CASE stream PASS
CASE stream-at-limit PASS
CASE external PASS
CASE non-hermetic PASS
CASE invalid PASS
CASE plan-realpath PASS
REGISTRY_REPLAY_SELFTEST: 10/10 pass
```

Frozen-ruler wrapper exit 0; actual selected rows:

```json
[
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_NOT_HELD"
    ],
    "id": "K7",
    "name": "runner-not-held-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_CLEANUP_FAILED"
    ],
    "id": "K8",
    "name": "runner-cleanup-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "STREAM_LIMIT"
    ],
    "id": "K9",
    "name": "stream-limit-refused"
  },
  {
    "discriminated": true,
    "exit": 0,
    "id": "K10",
    "name": "live-dependent-listed",
    "report": {
      "bundle_sha256": "5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245",
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 1048576,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

Fixed witness outputs that changed from pristine (the other witnesses were identical):

```json
[
  {
    "bundle_present": true,
    "case": "utf8-ten-bytes-limit-eight",
    "exit": 0,
    "report": {
      "bundle_sha256": null,
      "finding_ids": [],
      "live_dependent": [],
      "max_stream_bytes": 8,
      "refused_rows": [],
      "revision_pinned": 1,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

### M05 — KILLED

Location: `tools/registry-replay.py:99`. Expected detector: An external-only row must stay live-dependent; selftest external should fail.

```diff
- if row.get('external') is True or result.get('non_hermetic_argv'):
+ if result.get('non_hermetic_argv'):
```

Selftest exit 1; actual stdout:

```text
CASE clean PASS
CASE not-held PASS
CASE cleanup PASS
CASE held-missing PASS
CASE stream PASS
CASE stream-at-limit PASS
CASE external FAIL
CASE non-hermetic PASS
CASE invalid PASS
CASE plan-realpath PASS
REGISTRY_REPLAY_SELFTEST: 9/10 pass
```

Frozen-ruler wrapper exit 0; actual selected rows:

```json
[
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_NOT_HELD"
    ],
    "id": "K7",
    "name": "runner-not-held-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_CLEANUP_FAILED"
    ],
    "id": "K8",
    "name": "runner-cleanup-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "STREAM_LIMIT"
    ],
    "id": "K9",
    "name": "stream-limit-refused"
  },
  {
    "discriminated": true,
    "exit": 0,
    "id": "K10",
    "name": "live-dependent-listed",
    "report": {
      "bundle_sha256": "5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245",
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 1048576,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

Fixed witness outputs that changed from pristine (the other witnesses were identical):

```json
[
  {
    "bundle_present": true,
    "case": "external-only",
    "exit": 0,
    "report": {
      "bundle_sha256": null,
      "finding_ids": [],
      "live_dependent": [],
      "max_stream_bytes": 8,
      "refused_rows": [],
      "revision_pinned": 1,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

### M06 — KILLED

Location: `tools/registry-replay.py:99`. Expected detector: A non-hermetic-only row must stay live-dependent; selftest non-hermetic should fail.

```diff
- if row.get('external') is True or result.get('non_hermetic_argv'):
+ if row.get('external') is True:
```

Selftest exit 1; actual stdout:

```text
CASE clean PASS
CASE not-held PASS
CASE cleanup PASS
CASE held-missing PASS
CASE stream PASS
CASE stream-at-limit PASS
CASE external PASS
CASE non-hermetic FAIL
CASE invalid PASS
CASE plan-realpath PASS
REGISTRY_REPLAY_SELFTEST: 9/10 pass
```

Frozen-ruler wrapper exit 0; actual selected rows:

```json
[
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_NOT_HELD"
    ],
    "id": "K7",
    "name": "runner-not-held-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_CLEANUP_FAILED"
    ],
    "id": "K8",
    "name": "runner-cleanup-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "STREAM_LIMIT"
    ],
    "id": "K9",
    "name": "stream-limit-refused"
  },
  {
    "discriminated": true,
    "exit": 0,
    "id": "K10",
    "name": "live-dependent-listed",
    "report": {
      "bundle_sha256": "5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245",
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 1048576,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

Fixed witness outputs that changed from pristine (the other witnesses were identical):

```json
[
  {
    "bundle_present": true,
    "case": "non-hermetic-only",
    "exit": 0,
    "report": {
      "bundle_sha256": null,
      "finding_ids": [],
      "live_dependent": [],
      "max_stream_bytes": 8,
      "refused_rows": [],
      "revision_pinned": 1,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

### M07 — SURVIVED

Location: `tools/registry-replay.py:74`. Expected detector: A complete observation object with only its schema changed must return INVALID_OBSERVATIONS/2.

```diff
- if (not isinstance(observations, dict) or observations.get('schema') != OBS_SCHEMA
+ if (not isinstance(observations, dict) or False
```

Selftest exit 0; actual stdout:

```text
CASE clean PASS
CASE not-held PASS
CASE cleanup PASS
CASE held-missing PASS
CASE stream PASS
CASE stream-at-limit PASS
CASE external PASS
CASE non-hermetic PASS
CASE invalid PASS
CASE plan-realpath PASS
REGISTRY_REPLAY_SELFTEST: 10/10 pass
```

Frozen-ruler wrapper exit 0; actual selected rows:

```json
[
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_NOT_HELD"
    ],
    "id": "K7",
    "name": "runner-not-held-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_CLEANUP_FAILED"
    ],
    "id": "K8",
    "name": "runner-cleanup-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "STREAM_LIMIT"
    ],
    "id": "K9",
    "name": "stream-limit-refused"
  },
  {
    "discriminated": true,
    "exit": 0,
    "id": "K10",
    "name": "live-dependent-listed",
    "report": {
      "bundle_sha256": "5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245",
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 1048576,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

Fixed witness outputs that changed from pristine (the other witnesses were identical):

```json
[
  {
    "bundle_present": true,
    "case": "wrong-schema-full-shape",
    "exit": 0,
    "report": {
      "bundle_sha256": null,
      "finding_ids": [],
      "live_dependent": [],
      "max_stream_bytes": 8,
      "refused_rows": [],
      "revision_pinned": 1,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

### M08 — SURVIVED

Location: `tools/registry-replay.py:83`. Expected detector: A numeric requirement name must return INVALID_OBSERVATIONS/2.

```diff
- if not isinstance(result, dict) or not isinstance(requirement, dict) or not isinstance(requirement.get('name'), str):
+ if not isinstance(result, dict) or not isinstance(requirement, dict) or False:
```

Selftest exit 0; actual stdout:

```text
CASE clean PASS
CASE not-held PASS
CASE cleanup PASS
CASE held-missing PASS
CASE stream PASS
CASE stream-at-limit PASS
CASE external PASS
CASE non-hermetic PASS
CASE invalid PASS
CASE plan-realpath PASS
REGISTRY_REPLAY_SELFTEST: 10/10 pass
```

Frozen-ruler wrapper exit 0; actual selected rows:

```json
[
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_NOT_HELD"
    ],
    "id": "K7",
    "name": "runner-not-held-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_CLEANUP_FAILED"
    ],
    "id": "K8",
    "name": "runner-cleanup-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "STREAM_LIMIT"
    ],
    "id": "K9",
    "name": "stream-limit-refused"
  },
  {
    "discriminated": true,
    "exit": 0,
    "id": "K10",
    "name": "live-dependent-listed",
    "report": {
      "bundle_sha256": "5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245",
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 1048576,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

Fixed witness outputs that changed from pristine (the other witnesses were identical):

```json
[
  {
    "bundle_present": true,
    "case": "non-string-requirement-name",
    "exit": 0,
    "report": {
      "bundle_sha256": null,
      "finding_ids": [],
      "live_dependent": [],
      "max_stream_bytes": 8,
      "refused_rows": [],
      "revision_pinned": 1,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

### M09 — SURVIVED

Location: `tools/registry-replay.py:94`. Expected detector: A null stdout must return INVALID_OBSERVATIONS/2 rather than raising AttributeError.

```diff
- if not isinstance(text, str):
+ if False:
```

Selftest exit 0; actual stdout:

```text
CASE clean PASS
CASE not-held PASS
CASE cleanup PASS
CASE held-missing PASS
CASE stream PASS
CASE stream-at-limit PASS
CASE external PASS
CASE non-hermetic PASS
CASE invalid PASS
CASE plan-realpath PASS
REGISTRY_REPLAY_SELFTEST: 10/10 pass
```

Frozen-ruler wrapper exit 0; actual selected rows:

```json
[
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_NOT_HELD"
    ],
    "id": "K7",
    "name": "runner-not-held-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "RUNNER_CLEANUP_FAILED"
    ],
    "id": "K8",
    "name": "runner-cleanup-refused"
  },
  {
    "bundle_written": false,
    "control_ok": true,
    "discriminated": true,
    "exit": 1,
    "finding_ids": [
      "STREAM_LIMIT"
    ],
    "id": "K9",
    "name": "stream-limit-refused"
  },
  {
    "discriminated": true,
    "exit": 0,
    "id": "K10",
    "name": "live-dependent-listed",
    "report": {
      "bundle_sha256": "5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245",
      "finding_ids": [],
      "live_dependent": [
        "one"
      ],
      "max_stream_bytes": 1048576,
      "refused_rows": [],
      "revision_pinned": 0,
      "rows": 1,
      "schema": "registry-replay-report-v1"
    }
  }
]
```

Fixed witness outputs that changed from pristine (the other witnesses were identical):

```json
[
  {
    "case": "non-string-stdout",
    "exception": "AttributeError",
    "message": "'NoneType' object has no attribute 'encode'"
  }
]
```
