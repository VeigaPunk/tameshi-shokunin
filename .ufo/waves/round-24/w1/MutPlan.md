# MutPlan — round24 `plan()` mutation probe

## Verdict

**Two mutants killed; one survived both assigned detectors; none inconclusive.**

- **M1 — drop repository realpath: KILLED** by `--selftest` and frozen ruler K11.
- **M2 — drop sibling-output realpath: SURVIVED** `--selftest` and frozen ruler K11. A separate, baseline-controlled symlink-sibling fixture exposed the behavioral defect; it does not change the survival classification against the assigned detectors.
- **M3 — include the current lane among siblings: KILLED** by `--selftest` and frozen ruler K11.

All three edits were applied separately in a private clone and restored byte-for-byte. This is a calibration/coverage finding, not an implementation change, producer authentication, promotion, historical R17-CMD-BIND closure, full-ruler verdict, or numeric score uplift.

## Axes and scope

- **Calibration:** distinguish detected mutants from surviving mutants; no kills without passing pristine and restored controls.
- **Coverage:** challenge canonical repository identity, canonical sibling identity, and exclusion of self.
- **Operability:** run the same bounded public-CLI detectors in each state and retain exact restoration hashes.

Target revision: `c8c5b88c8e961a929cdc351b95a7074c76958909`.
Private clone / command cwd: `/tmp/TameshiR24-2-MutPlan-r24`.
Observed interpreter: `Python 3.14.8`. No tool installs or upgrades.
No production files were edited, no tests ran in the production checkout, and no subagents or other orchestration runtime were invoked. The only production write is this report.

### Relevant source evidence

- `tools/registry-replay.py:63-69`: `plan()` canonicalizes the repository, derives its fleet root, canonicalizes sibling outputs, and excludes the current realpath.
- `tools/registry-replay.py:227-240`: the public selftest builds two ordinary sibling directories and a fleet alias; it does not build a symlink sibling. Its predicate checks fleet root and siblings (not `repo` directly).
- `.ufo/evidence/round-24/measure.py:185-200`: K11 likewise builds ordinary sibling directories, then a fleet alias and `..` input; its predicate checks canonical fleet root, canonical repository, and the expected siblings list.
- `.ufo/evidence/round-24/contract.json:56-57,61-64`: K11 is `fleet-root-realpath`; synthetic predicates are bounded evidence, not a general mutation-adequacy guarantee.

## Commands and expected detectors

Clone command executed from `/tmp`, exit 0, no stdout/stderr:

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/TameshiR24-2-MutPlan-r24 && git -C /tmp/TameshiR24-2-MutPlan-r24 checkout -q --detach c8c5b88c8e961a929cdc351b95a7074c76958909
```

Read-only identity command executed in that clone:

```sh
git rev-parse HEAD && sha256sum tools/registry-replay.py .ufo/evidence/round-24/measure.py && python3 --version
```

Observed output:

```text
c8c5b88c8e961a929cdc351b95a7074c76958909
9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714  tools/registry-replay.py
0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64  .ufo/evidence/round-24/measure.py
Python 3.14.8
```

At every phase, the selftest, K11 adapter, supplemental counterexample, and `sha256sum` command ran concurrently, with cwd fixed to the private clone, `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`, and `TMPDIR` set to the private clone. Each top-level detector had a 180-second bound; all completed normally. The selftest's own subprocesses and supplemental public-CLI subprocess each have 30-second bounds. The unchanged ruler helper retains its own 600-second per-command limit, inside the adapter's outer bound.

- `python3 tools/registry-replay.py --selftest`: a kill requires pristine/restored exit 0, mutant exit 1, and explicit `CASE plan-realpath FAIL`.
- K11 adapter below: invokes **the unchanged frozen `replay_rows()` helper**, prints its K11 row, and maps `discriminated` to adapter exit 0/1. Thus a kill is a passing pristine/restored K11 predicate and failing mutant predicate. All `--plan` child exits observed here were 0; adapter failures represent bad plan values, not CLI crashes.
- Calling `replay_rows()` also exercises its bounded K7–K10 synthetic project fixtures, but this report claims only the selected K11 result. It does not call the ruler's `main()`, K1–K6, the registry battery, or an actual replay.

Exact K11 adapter command (cwd as above):

```sh
python3 -c 'import importlib.util, json, sys, tempfile
from pathlib import Path
repo = Path.cwd()
spec = importlib.util.spec_from_file_location("frozen_r24", repo / ".ufo/evidence/round-24/measure.py")
ruler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ruler)
with tempfile.TemporaryDirectory(prefix="mutplan-k11-", dir=repo) as tmp:
    row = next(row for row in ruler.replay_rows(repo, Path(tmp)) if row["id"] == "K11")
    print(json.dumps(row, sort_keys=True))
    raise SystemExit(0 if row["discriminated"] else 1)
'
```

## Mutants and result matrix

Only the indicated behavior-bearing expression changed in each mutant; all other code and the frozen ruler remained unchanged.

| Mutant | Source change | Expected detector | Selftest observed | K11 observed | Verdict |
|---|---|---|---|---|---|
| M1 | line 65: `real = os.path.realpath(repo)` → `real = repo` | Alias/`..` fixture must reject lexical repository/fleet identity | exit 1; `CASE plan-realpath FAIL`; `9/10 pass` | adapter exit 1; CLI exit 0; `discriminated: false` | **KILLED by both** |
| M2 | line 67: `sorted(os.path.realpath(p) for p ...` → `sorted(str(p) for p ...` | Canonical sibling-output assertion should detect a symlink sibling | exit 0; all cases pass; `10/10 pass` | adapter exit 0; CLI exit 0; `discriminated: true` | **SURVIVED both** |
| M3 | line 68: `if p.is_dir() and os.path.realpath(p) != real` → `if p.is_dir()` | Siblings list must omit the current lane | exit 1; `CASE plan-realpath FAIL`; `9/10 pass` | adapter exit 1; CLI exit 0; `discriminated: false` | **KILLED by both** |

M2 deliberately retains `str(p)` so output stays a JSON-serializable path string. Removing the conversion and returning `Path` objects would create an unrelated serialization failure rather than isolate sibling realpath normalization. The realpath-based self-exclusion filter was unchanged in M2.

### Every phase, including controls

`pristine` is M1's baseline; `M1_restored` is also M2's immediate pristine baseline; `M2_restored` is also M3's immediate pristine baseline. Each mutation is therefore bracketed by successful pristine/restored runs of the same detectors.

| Phase | Selftest exit / terminal output | K11 adapter exit / predicate | Supplemental symlink-sibling exit / predicate |
|---|---|---|---|
| `pristine` | 0 / `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | 0 / `true` | 0 / `true` |
| `M1_drop_repo_realpath` | 1 / `REGISTRY_REPLAY_SELFTEST: 9/10 pass` | 1 / `false` | 0 / `true` |
| `M1_restored` | 0 / `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | 0 / `true` | 0 / `true` |
| `M2_drop_sibling_realpath` | 0 / `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | 0 / `true` | 1 / `false` |
| `M2_restored` | 0 / `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | 0 / `true` | 0 / `true` |
| `M3_include_self` | 1 / `REGISTRY_REPLAY_SELFTEST: 9/10 pass` | 1 / `false` | 1 / `false` |
| `M3_restored` | 0 / `REGISTRY_REPLAY_SELFTEST: 10/10 pass` | 0 / `true` | 0 / `true` |

All captured top-level stderr streams were empty. Supplemental public-CLI stderr was also empty in every phase.

## Concrete counterexample for the survivor

The supplemental fixture creates:

```text
<fixture>/fleet/lane-shokunin/                         # repository
<fixture>/canonical/peer-shokunin/                    # actual peer
<fixture>/fleet/peer-shokunin -> ../canonical/peer-shokunin
```

It invokes `tools/registry-replay.py --plan --repo <fixture>/fleet/lane-shokunin --json` and compares the complete plan against canonical expected values. Pristine and restored bytes return the canonical target in `siblings`; M2 returns the symlink spelling in `siblings`. Neither existing detector constructs this distinction: with ordinary peer directories, `str(p)` and `os.path.realpath(p)` are equal.

Exact supplemental command, run with the same environment/cwd in every phase:

```sh
python3 -c 'import json, os, subprocess, sys, tempfile
from pathlib import Path
repo = Path.cwd()
with tempfile.TemporaryDirectory(prefix="mutplan-symlink-", dir=repo) as tmp:
    root = Path(tmp)
    fleet = root / "fleet"
    lane = fleet / "lane-shokunin"
    lane.mkdir(parents=True)
    target = root / "canonical" / "peer-shokunin"
    target.mkdir(parents=True)
    (fleet / "peer-shokunin").symlink_to(target, target_is_directory=True)
    argv = [sys.executable, str(repo / "tools/registry-replay.py"), "--plan", "--repo", str(lane), "--json"]
    result = subprocess.run(argv, cwd=repo, capture_output=True, text=True, timeout=30)
    expected = {"repo": os.path.realpath(lane), "fleet_root": os.path.realpath(fleet), "siblings": [os.path.realpath(target)]}
    try:
        actual = json.loads(result.stdout)
    except ValueError:
        actual = None
    passed = result.returncode == 0 and actual == expected
    print(json.dumps({"probe": "symlink-sibling", "argv": argv, "cli_exit": result.returncode, "cli_stdout": result.stdout, "cli_stderr": result.stderr, "expected": expected, "pass": passed}, sort_keys=True))
    raise SystemExit(0 if passed else 1)
'
```

### Actual survivor counterexample outputs

**M1_restored — helper exit 0**

```json
{"argv": ["/usr/bin/python3", "/tmp/TameshiR24-2-MutPlan-r24/tools/registry-replay.py", "--plan", "--repo", "/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-t94o821r/fleet/lane-shokunin", "--json"], "cli_exit": 0, "cli_stderr": "", "cli_stdout": "{\"fleet_root\": \"/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-t94o821r/fleet\", \"repo\": \"/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-t94o821r/fleet/lane-shokunin\", \"siblings\": [\"/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-t94o821r/canonical/peer-shokunin\"]}\n", "expected": {"fleet_root": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-t94o821r/fleet", "repo": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-t94o821r/fleet/lane-shokunin", "siblings": ["/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-t94o821r/canonical/peer-shokunin"]}, "pass": true, "probe": "symlink-sibling"}
```

**M2_drop_sibling_realpath — helper exit 1**

```json
{"argv": ["/usr/bin/python3", "/tmp/TameshiR24-2-MutPlan-r24/tools/registry-replay.py", "--plan", "--repo", "/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-6a44a85j/fleet/lane-shokunin", "--json"], "cli_exit": 0, "cli_stderr": "", "cli_stdout": "{\"fleet_root\": \"/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-6a44a85j/fleet\", \"repo\": \"/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-6a44a85j/fleet/lane-shokunin\", \"siblings\": [\"/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-6a44a85j/fleet/peer-shokunin\"]}\n", "expected": {"fleet_root": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-6a44a85j/fleet", "repo": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-6a44a85j/fleet/lane-shokunin", "siblings": ["/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-6a44a85j/canonical/peer-shokunin"]}, "pass": false, "probe": "symlink-sibling"}
```

**M2_restored — helper exit 0**

```json
{"argv": ["/usr/bin/python3", "/tmp/TameshiR24-2-MutPlan-r24/tools/registry-replay.py", "--plan", "--repo", "/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-u75j62w1/fleet/lane-shokunin", "--json"], "cli_exit": 0, "cli_stderr": "", "cli_stdout": "{\"fleet_root\": \"/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-u75j62w1/fleet\", \"repo\": \"/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-u75j62w1/fleet/lane-shokunin\", \"siblings\": [\"/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-u75j62w1/canonical/peer-shokunin\"]}\n", "expected": {"fleet_root": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-u75j62w1/fleet", "repo": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-u75j62w1/fleet/lane-shokunin", "siblings": ["/tmp/TameshiR24-2-MutPlan-r24/mutplan-symlink-u75j62w1/canonical/peer-shokunin"]}, "pass": true, "probe": "symlink-sibling"}
```

This establishes a test-coverage gap, **not** a defect in pristine `plan()`: the unmodified implementation produced the correct canonical sibling identity in the supplemental baseline and restoration runs.

## Restoration evidence

The `sha256sum tools/registry-replay.py .ufo/evidence/round-24/measure.py` command ran in every phase. The unchanged ruler SHA-256 was always `0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64`.

| Phase | `tools/registry-replay.py` SHA-256 |
|---|---|
| `pristine` | `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714` |
| `M1_drop_repo_realpath` | `722ac77724a0ac04e61ca4cbaf57180dd76909d26a1725c120e49c1d1d3c7a3d` |
| `M1_restored` | `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714` |
| `M2_drop_sibling_realpath` | `fec7c609b109abf1990502d704418d4614f4c449c50c3f76676275c521bd9a4a` |
| `M2_restored` | `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714` |
| `M3_include_self` | `1825a7dc1039ed97007a0c57723da710f64352d0c91b9984f5190ba0b2d5acec` |
| `M3_restored` | `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714` |

Each restored target hash exactly equals the original target hash. Every restored selftest was `10/10 pass` with exit 0, and every restored K11 and supplemental predicate passed. No mutation remains in the clone.

## Actual assigned-detector transcripts

The following are captured stdout, not inferred outcomes. Exit codes appear in the headings. The K11 JSON is the exact row returned by the frozen ruler helper; its `exit` field is the public `--plan` child status, not the adapter status.

### pristine

`selftest` — exit 0

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

`ruler_K11` — exit 0

```text
{"discriminated": true, "exit": 0, "id": "K11", "name": "fleet-root-realpath", "plan": {"fleet_root": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-z2_8ep71/replay/fleet", "repo": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-z2_8ep71/replay/fleet/lane-shokunin", "siblings": ["/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-z2_8ep71/replay/fleet/other-shokunin"]}}
```

### M1_drop_repo_realpath

`selftest` — exit 1

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
CASE plan-realpath FAIL
REGISTRY_REPLAY_SELFTEST: 9/10 pass
```

`ruler_K11` — exit 1

```text
{"discriminated": false, "exit": 0, "id": "K11", "name": "fleet-root-realpath", "plan": {"fleet_root": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-1v6b7fwz/replay/alias/other-shokunin/..", "repo": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-1v6b7fwz/replay/alias/other-shokunin/../lane-shokunin", "siblings": ["/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-1v6b7fwz/replay/fleet/lane-shokunin", "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-1v6b7fwz/replay/fleet/other-shokunin"]}}
```

### M1_restored

`selftest` — exit 0

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

`ruler_K11` — exit 0

```text
{"discriminated": true, "exit": 0, "id": "K11", "name": "fleet-root-realpath", "plan": {"fleet_root": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-xnfkybfy/replay/fleet", "repo": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-xnfkybfy/replay/fleet/lane-shokunin", "siblings": ["/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-xnfkybfy/replay/fleet/other-shokunin"]}}
```

### M2_drop_sibling_realpath

`selftest` — exit 0

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

`ruler_K11` — exit 0

```text
{"discriminated": true, "exit": 0, "id": "K11", "name": "fleet-root-realpath", "plan": {"fleet_root": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-6zrlkm18/replay/fleet", "repo": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-6zrlkm18/replay/fleet/lane-shokunin", "siblings": ["/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-6zrlkm18/replay/fleet/other-shokunin"]}}
```

### M2_restored

`selftest` — exit 0

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

`ruler_K11` — exit 0

```text
{"discriminated": true, "exit": 0, "id": "K11", "name": "fleet-root-realpath", "plan": {"fleet_root": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-6h7lopyc/replay/fleet", "repo": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-6h7lopyc/replay/fleet/lane-shokunin", "siblings": ["/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-6h7lopyc/replay/fleet/other-shokunin"]}}
```

### M3_include_self

`selftest` — exit 1

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
CASE plan-realpath FAIL
REGISTRY_REPLAY_SELFTEST: 9/10 pass
```

`ruler_K11` — exit 1

```text
{"discriminated": false, "exit": 0, "id": "K11", "name": "fleet-root-realpath", "plan": {"fleet_root": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-ry2j5hzm/replay/fleet", "repo": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-ry2j5hzm/replay/fleet/lane-shokunin", "siblings": ["/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-ry2j5hzm/replay/fleet/lane-shokunin", "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-ry2j5hzm/replay/fleet/other-shokunin"]}}
```

### M3_restored

`selftest` — exit 0

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

`ruler_K11` — exit 0

```text
{"discriminated": true, "exit": 0, "id": "K11", "name": "fleet-root-realpath", "plan": {"fleet_root": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-v649qafz/replay/fleet", "repo": "/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-v649qafz/replay/fleet/lane-shokunin", "siblings": ["/tmp/TameshiR24-2-MutPlan-r24/mutplan-k11-v649qafz/replay/fleet/other-shokunin"]}}
```

## Smallest safe correction

Add one **non-frozen public selftest case** whose sibling is a symlink to a directory outside the fleet spelling, and assert that the returned sibling string equals that target's realpath. Keep the existing alias/`..` and self-exclusion assertions. That fixture is sufficient to distinguish the surviving M2 mutation without changing production behavior or weakening the contract.

Do not rewrite the frozen K11 ruler to retroactively improve this result. Carry the coverage finding into a future explicitly versioned detector if broader sibling-identity coverage is claimed. No correction was applied in this report-only lane.
