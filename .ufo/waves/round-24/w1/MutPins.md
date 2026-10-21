# MutPins — round 24 W1

## Verdict

**All six assigned variants were detected by the combined bounded detectors, but not by the same detector.** Dropping a digest needle or reactivating the unpinned predecessor is killed by the corresponding K5/K6 predicate and **survives `registry-check.py --only` on unchanged bundles**. Changing one digest hex digit is killed directly by `--only` (`held=false`, process exit 1). For the digit mutants the ruler's internal pristine control fails, so its substitution experiment is **inconclusive**, not a substitution kill.

The delivered pinned revision itself had valid controls: K5 and K6 each reported `control=true`, `substituted=false`, `discriminated=true`. Each mutant was applied alone, restored exactly, and followed by the same detectors. All six restoration runs returned to that result. This is a scoped mutation-probe finding, not round acceptance, producer authentication, promotion, historical R17-CMD-BIND closure, or a numeric score uplift.

## Axes and scope

- **Calibration:** distinguish a genuine substitution kill, a direct stdout-pin mismatch, and a failed internal baseline.
- **Pin sensitivity:** loss, one-hex-digit corruption, and rollback to the superseded unpinned row, independently for both bundles.
- **Isolation / reversibility:** only `tools/registry.json` in the private clone was edited; original bytes were restored after every mutation. No sibling dispatch, no other runtime, no production edit, no registry battery, and no full eleven-predicate ruler run.

Revision: `c8c5b88c8e961a929cdc351b95a7074c76958909` (observed `git rev-parse HEAD`). Private clone: `/tmp/TameshiR24-2.MutPins-r24`. Outside that scratch clone and the ruler's temporary private workcopies, the only write is this assigned report. Tool installs/updates: **none**.

## Commands and detector contract

Bootstrap (exit 0, empty stdout/stderr):

```sh
GIT_OPTIONAL_LOCKS=0 git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/TameshiR24-2.MutPins-r24 && GIT_OPTIONAL_LOCKS=0 git -C /tmp/TameshiR24-2.MutPins-r24 checkout -q --detach c8c5b88c8e961a929cdc351b95a7074c76958909
```

All detector subprocesses used `cwd=/tmp/TameshiR24-2.MutPins-r24`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`, and a 150-second outer timeout. No timeout occurred. At each stage, hashes, K5/K6, and the four independent `--only` commands ran concurrently; mutation/restoration waited for them all to finish. The restored run of the preceding variant is also the pristine run immediately preceding the next variant.

For each NAME below, execute exactly:

```sh
python3 -B tools/registry-check.py --root /tmp/TameshiR24-2.MutPins-r24 --only NAME --json
```

Names executed at every stage:

```text
command-binding-frozen-clean-pinned
command-binding-source-read-red-pinned
command-binding-frozen-clean
command-binding-source-read-red
```

K5/K6 were run by `python3 -B -c` with the following **exact** argument body, importing and calling the frozen, unmodified `pin_rows` implementation. The aggregate exit below belongs to this explicit two-predicate wrapper, not the unrun eleven-predicate CLI:

```python
import importlib.util, json, tempfile
from pathlib import Path
repo = Path.cwd()
spec = importlib.util.spec_from_file_location("r24_measure", repo / ".ufo/evidence/round-24/measure.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
with tempfile.TemporaryDirectory(prefix="MutPins-K56-") as tmp:
    rows = m.pin_rows(repo, Path(tmp))
print(json.dumps({"rows": rows}, sort_keys=True, indent=2))
raise SystemExit(0 if all(row["discriminated"] for row in rows) else 1)
```

The ruler creates private copies and performs its own bundle/expected-file substitutions there; their temporary directories are removed on context exit. It does not substitute bundle bytes in the manually mutated clone. All K5/K6 wrapper stderr was empty.

Every direct `--only` invocation emitted this same warning on stderr, appropriately referring to the private scratch root, followed by its ROW/REGISTRY_CHECK lines recorded below:

```text
registry-check: warning: live --root mode runs rows in the lane; rows may write into the root (use --rev to grade a throwaway clone)
```

## Expected detector and observed result

K5/K6 derive active rows from the bundle path, require every original bundle control to hold, then require at least one row to fail on self-consistent substitution (`.ufo/evidence/round-24/measure.py:92-135`). K5 replaces the replay bundle with the pre-existing correct-command bundle and recomputes its expected-file hash; K6 appends a newline to the first receipt's stdout and recomputes its expected-file hash (`measure.py:107-116`). Thus a bare bundle/expected-file hash check is insufficient; the additional literal registry pin is behavior-bearing.

`registry-check.py` implements the declared row: it searches the configured literal stdout needles and combines that result with exit and cleanup status (`tools/registry-check.py:648-652,717-720`). It is not independently authenticating the registry contract. The original pins are `tools/registry.json:974,984`; the superseded predecessor expectations are `tools/registry.json:939-958`.

In the table, C/S/D are the target predicate's actual `control`, `substituted`, and `discriminated` booleans. The unaffected predicate stayed `true/false/true` for every single-row mutant.

| Mutant | Direct selected row: exit / held | Target C / S / D | K5/K6 wrapper exit | Verdict |
|---|---|---|---|---|
| `drop-token-clean` | 0 / true | true / true / false | 1 | Killed by K5; survives direct --only |
| `drop-token-red` | 0 / true | true / true / false | 1 | Killed by K6; survives direct --only |
| `one-hex-digit-clean` | 1 / false | false / false / false | 1 | Killed by direct --only; K5 substitution test internally inconclusive |
| `one-hex-digit-red` | 1 / false | false / false / false | 1 | Killed by direct --only; K6 substitution test internally inconclusive |
| `reactivate-superseded-clean` | 0 / true | true / true / false | 1 | Killed by K5; survives direct --only |
| `reactivate-superseded-red` | 0 / true | true / true / false | 1 | Killed by K6; survives direct --only |

### Minimal mutation definitions

- **drop-token-clean:** Remove only the literal `bundle_sha256` stdout needle at `tools/registry.json:974`.
- **drop-token-red:** Remove only the literal `bundle_sha256` stdout needle at `tools/registry.json:984`.
- **one-hex-digit-clean:** Change the first digest hex digit `3` to `4` at `tools/registry.json:974`; do not change bundle or expected bytes.
- **one-hex-digit-red:** Change the first digest hex digit `d` to `e` at `tools/registry.json:984`; do not change bundle or expected bytes.
- **reactivate-superseded-clean:** Reactivate `command-binding-frozen-clean` and supersede its pinned successor, reversing `superseded_by` to the old row. Only status/edge metadata changes (pristine lines 944-945 and 976).
- **reactivate-superseded-red:** Reactivate `command-binding-source-read-red` and supersede its pinned successor, reversing `superseded_by` to the old row. Only status/edge metadata changes (pristine lines 955-956 and 986).

Reactivation uses valid inverse supersession edges rather than leaving a dangling/non-active successor, so it tests rollback behavior, not a registry-schema error (`tools/registry-check.py:277-298`). Both the newly active predecessor and the now-superseded pinned successor were explicitly run with `--only`.

### Concrete counterexample / boundary

Remove just the digest needle at `tools/registry.json:974`. On the unchanged replay bundle, direct `--only command-binding-frozen-clean-pinned` still prints `ROW command-binding-frozen-clean-pinned expect=0 got=0 held` and exits 0. The frozen K5 substitution then also holds, so K5 reports `control=true`, `substituted=true`, `discriminated=false`. The red row behaves analogously. Rollback to the old active row produces the same loss of substitution sensitivity. This is a coverage finding for **`--only` used alone**, not evidence that fixed pinned rows accept the frozen substitutions.

The digit variants are different: the unchanged command still produces its correct exit and actual hash, but the monitor reports the deliberately wrong literal in `stdout_missing` and exits 1. Their K5/K6 internal `control=false` is explicitly not counted as a successful substitution kill.

## Actual detector output by stage

The following records preserve the parsed K5/K6 stdout JSON, direct command exits and observed ROW/trailer lines. All direct stdout JSON also carried the actual registry digest shown in the hash table. A superseded row's `held=0/0 superseded=1` trailer is exclusion from active totals, not a claim that it was an active passing row; its per-row JSON `held` remained true here.

### pristine

K5/K6 wrapper exit: `0`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": true,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": true,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### drop-token-clean

K5/K6 wrapper exit: `1`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": false,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": true
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": true,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### restored-after-drop-token-clean

K5/K6 wrapper exit: `0`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": true,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": true,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### drop-token-red

K5/K6 wrapper exit: `1`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": true,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": false,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": true
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### restored-after-drop-token-red

K5/K6 wrapper exit: `0`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": true,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": true,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### one-hex-digit-clean

K5/K6 wrapper exit: `1`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": false
      },
      "discriminated": false,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": true,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=1
ROW command-binding-frozen-clean-pinned expect=0 got=0 differs
REGISTRY_CHECK: held=0/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### restored-after-one-hex-digit-clean

K5/K6 wrapper exit: `0`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": true,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": true,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### one-hex-digit-red

K5/K6 wrapper exit: `1`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": true,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": false
      },
      "discriminated": false,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=1
ROW command-binding-source-read-red-pinned expect=1 got=1 differs
REGISTRY_CHECK: held=0/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### restored-after-one-hex-digit-red

K5/K6 wrapper exit: `0`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": true,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": true,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### reactivate-superseded-clean

K5/K6 wrapper exit: `1`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean": true
      },
      "discriminated": false,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean"
      ],
      "substituted": {
        "command-binding-frozen-clean": true
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": true,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### restored-after-reactivate-superseded-clean

K5/K6 wrapper exit: `0`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": true,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": true,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### reactivate-superseded-red

K5/K6 wrapper exit: `1`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": true,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red": true
      },
      "discriminated": false,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red"
      ],
      "substituted": {
        "command-binding-source-read-red": true
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
```

### restored-after-reactivate-superseded-red

K5/K6 wrapper exit: `0`. Actual parsed stdout:

```json
{
  "rows": [
    {
      "control": {
        "command-binding-frozen-clean-pinned": true
      },
      "discriminated": true,
      "id": "K5",
      "name": "frozen-clean-substitution",
      "rows": [
        "command-binding-frozen-clean-pinned"
      ],
      "substituted": {
        "command-binding-frozen-clean-pinned": false
      }
    },
    {
      "control": {
        "command-binding-source-read-red-pinned": true
      },
      "discriminated": true,
      "id": "K6",
      "name": "source-read-red-substitution",
      "rows": [
        "command-binding-source-read-red-pinned"
      ],
      "substituted": {
        "command-binding-source-read-red-pinned": false
      }
    }
  ]
}
```

Direct checks (process exit then exact post-warning stderr lines):

```text
--only command-binding-frozen-clean-pinned: exit=0
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-source-read-red-pinned: exit=0
ROW command-binding-source-read-red-pinned expect=1 got=1 held
REGISTRY_CHECK: held=1/1 superseded=0
--only command-binding-frozen-clean: exit=0
ROW command-binding-frozen-clean superseded expect=0 got=0
REGISTRY_CHECK: held=0/0 superseded=1
--only command-binding-source-read-red: exit=0
ROW command-binding-source-read-red superseded expect=1 got=1
REGISTRY_CHECK: held=0/0 superseded=1
```

### Command stdout and digit-mismatch evidence

On all thirteen stages the command payloads themselves were unchanged. The pinned clean/red rows' `stdout_tail` values were:

```json
{"bundle_sha256": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}
{"bundle_sha256": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf", "exit": 1, "finding_ids": ["ARGV_MISMATCH"], "schema": "command-binding-report-v1"}
```

The two deliberately wrong expected tokens were reported exactly as follows:

`one-hex-digit-clean`:

```json
{
  "name": "command-binding-frozen-clean-pinned",
  "expect": 0,
  "got": 0,
  "held": false,
  "stdout_missing": [
    "\"bundle_sha256\": \"4d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9\""
  ],
  "stdout_tail": "{\"bundle_sha256\": \"3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9\", \"exit\": 0, \"finding_ids\": [], \"schema\": \"command-binding-report-v1\"}\n"
}
```

`one-hex-digit-red`:

```json
{
  "name": "command-binding-source-read-red-pinned",
  "expect": 1,
  "got": 1,
  "held": false,
  "stdout_missing": [
    "\"bundle_sha256\": \"eb620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf\""
  ],
  "stdout_tail": "{\"bundle_sha256\": \"db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf\", \"exit\": 1, \"finding_ids\": [\"ARGV_MISMATCH\"], \"schema\": \"command-binding-report-v1\"}\n"
}
```

## Before / mutant / restored hashes

`sha256sum` ran on the eight paths below at every stage (exit 0, empty stderr). Before and all six exact restorations of `tools/registry.json`:

```text
a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f  tools/registry.json
```

| Stage | Actual tools/registry.json SHA-256 |
|---|---|
| `pristine` | `a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f` |
| `drop-token-clean` | `5a5523658b6b678f6d039c59e0696e63faf2ded8a5c4b87ef3de5b02f8834f01` |
| `restored-after-drop-token-clean` | `a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f` |
| `drop-token-red` | `b7852384d13c08bf95a4187714ba658619532bbb7472544fea0ec44b883487ff` |
| `restored-after-drop-token-red` | `a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f` |
| `one-hex-digit-clean` | `57ada54864ee23eb702e8a72b8d0345993fa09cccf2189c24130f65467ff3a4b` |
| `restored-after-one-hex-digit-clean` | `a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f` |
| `one-hex-digit-red` | `93fd01082acc8c3652f8fc0d749499118dc69de40ab7819b48b9ae1b49ccf80b` |
| `restored-after-one-hex-digit-red` | `a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f` |
| `reactivate-superseded-clean` | `387664ac288db05a64bc8e5abaa1c651a001471557bc618a066060dd51d0b920` |
| `restored-after-reactivate-superseded-clean` | `a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f` |
| `reactivate-superseded-red` | `11d415ad8756bdbc0253aa9fbd2da6ee70a378e4be5ae28b0e8cfc39cbea69d5` |
| `restored-after-reactivate-superseded-red` | `a8f255f1c88fa32d75059c52a75229322796bfba7316798ba092ee18b10c8a0f` |

All eight observed file hashes match pristine on **each** of the six restoration stages. The other seven files remained at the following hashes on every stage, including all six mutants:

```text
0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64  .ufo/evidence/round-24/measure.py
cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad  tools/registry-check.py
9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d  tools/command-binding.py
3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9  .ufo/evidence/round-23/replay/bundle.json
0831c9c820488dc9d9096c90aade44217b6b615501fae7810e6fce414cb2a0a1  .ufo/evidence/round-23/replay/expected.json
db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf  .ufo/evidence/round-23/source-read-bundle.json
70f357e354c4badb22f974070ccf37dfda512103c3cf3ab93297a3ea27cb5dc8  .ufo/evidence/round-23/source-read-expected.json
```

No production hashes or sibling state were changed by this probe. No mutating git command ran in production; cloning/checking out occurred only in the assigned private `/tmp` clone. No helper script or scaffold file was created. Temporary ruler workcopies were context-managed and removed; the private clone remains restored at the assigned revision for inspection.

## Smallest safe correction

Keep both pinned successors active and preserve their exact digest stdout needles. Treat `--only` as row compliance, not a detector of removal/rollback of the row's own contract; retain K5/K6 beside it when asserting the named substitution protection. No production change is proposed from this probe, and no stronger authentication or score claim follows from it. This separation is already consistent with `.ufo/evidence/round-24/contract.json:61-64` (named substitutions only; changing a row and bundle can choose a new contract).
