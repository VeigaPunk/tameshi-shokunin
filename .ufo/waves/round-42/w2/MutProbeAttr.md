# MutProbeAttr — round 42 wave 2: attr-class mutant probes of write-path-census-v4

Seat: L1Tameshi42.MutProbeAttr (mutation-tester). Access date 2026-10-25. Tool under attack:
`tools/write-path-census-v4.py` at a21845f (sha256 `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5`,
identical to the working-tree file). I wrote these mutants without seeing MutantAuthor's `mutants.json` (which does
not exist at a21845f). All counter runs below are `--probe-mutant` against **a21845f (pre-run revision)**.

## Findings

1. **All four attr-class mutants SURVIVE the frozen C2 oracle.** The unmutated copy also survives, so the baseline
   is clean and these are real survivors, not inconclusive results.
2. **Each mutant also passes the tool's own selftest** (`python3 -I <mutant> --selftest` →
   `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0` for all four). Neither battery checks the attr-binding rules at
   `tools/write-path-census-v4.py:17-20` or `:207-209` beyond the single-class, Name-free shape.
3. **Each survivor is a battery gap with a one-site fixture that kills it.** Each fixture below fails only its own
   mutant. The unmutated tool and the other three mutants pass it. I judged this with the counter's own
   `run_tool` + `check_site`, wanting
   `expected=1 scratch=0 explicit_out=0 unflagged=1` (finding 5).
4. **The lane corpus can't catch them either.** Over all 26 `tools/*.py` at a21845f, M1b, M2 and M3 change no site.
   M1 changes only the `resolved` text at `tools/context-capture.py:1667,1682,1685`: `self.counter`, which has
   `self.counter += 1` at :1632, now resolves to `0`. No bit changes there and the `mkdtemp` needle is still present.
   So the full deciding run's `live_*` and `live_unflagged_v4` fields don't detect any of the four.

## Mutants (exact single find/replace on a copy of v4 at a21845f; each `find` occurs once)

| id | point | find → replace | mutant sha256 |
|---|---|---|---|
| M1 `attr_drop_augassign_collect` | `:125-126` | delete `elif isinstance(sub, ast.AugAssign):` / `targets, value = [sub.target], sub` | `faece6b1…c1b3` |
| M1b `attr_drop_augassign_filter` | `:132` | `if len(vals) == 1 and not isinstance(list(vals.values())[0], ast.AugAssign)}` → `if len(vals) == 1}` | `504c5a72…7a26` |
| M2 `attr_every_class` | `:118-119` | `for method in self.methods.values():` → iterate the methods of every `ClassDef` in the module (module tree stashed in `_TREE` at `classify_source`) | `cb5bc432…1bdd2` |
| M3 `attr_caller_env` | `:208` | `_resolve(ctx.cls.attrs[node.attr], {}, text, ctx, depth + 1)` → `..., env, ...` | `73bc1510…cc3cc` |

## PROBE lines

Command (one per mutant, `<file>` = the mutant copy under `/tmp/tameshi-r42w2-MutProbeAttr-work/`):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a21845f523b75adbd3e3f7a62af91294db224ad9 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f --probe-mutant <file>
```

| file | output (exit 0) |
|---|---|
| pristine.py (baseline) | `PROBE outcome=survived detail=` |
| M1_attr_drop_augassign_collect.py | `PROBE outcome=survived detail=` |
| M1b_attr_drop_augassign_filter.py | `PROBE outcome=survived detail=` |
| M2_attr_every_class.py | `PROBE outcome=survived detail=` |
| M3_attr_caller_env.py | `PROBE outcome=survived detail=` |

Each was followed by `C2_R42_CONTROL: probe_outcome=survived rev=a21845f523b75adbd3e3f7a62af91294db224ad9 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f`.

## Killer fixtures (battery gaps)

All four want `{'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True}`, needle None.

**K1_attr_augassign_rebase** kills M1. The contract at `:19-20` says "any augmented assignment" leaves the
attribute unresolved. This is F03's shape with an AugAssign in place of the second plain assignment.

```python
import os
import tempfile


class H:
    def __init__(self):
        self.root = tempfile.mkdtemp()

    def rebase(self):
        self.root += '/../../golden'

    def run(self):
        with open(os.path.join(self.root, 'expected.json'), 'w') as handle:
            handle.write('{}')
```

**K1b_attr_augassign_only** kills M1b. The only `self.` write is an AugAssign. Under M1b the AugAssign node itself
becomes the binding, and its source text supplies the `tempfile` marker.

```python
import os
import tempfile


class H:
    root = 'golden'

    def nest(self):
        self.root += os.sep + tempfile.gettempprefix()

    def run(self):
        with open(os.path.join(self.root, 'expected.json'), 'w') as handle:
            handle.write('{}')
```

**K2_attr_other_class** kills M2. `:17` limits attribute binding to the enclosing class. `Repo` never assigns
`self.root`, so a sibling class's `mkdtemp` must not leak into it.

```python
import os
import tempfile

import fixturebase


class Scratch:
    def __init__(self):
        self.root = tempfile.mkdtemp()


class Repo(fixturebase.Base):
    def run(self):
        with open(os.path.join(self.root, 'expected.json'), 'w') as handle:
            handle.write('{}')
```

**K3_attr_param_shadowed_local** kills M3. The attribute's expression `root` is `__init__`'s parameter, and the
writing method has an unrelated local `root = tempfile.mkdtemp()`. Resolving in the caller's environment binds the
wrong scope.

```python
import os
import tempfile


class H:
    def __init__(self, root):
        self.root = root

    def run(self):
        root = tempfile.mkdtemp()
        with open(os.path.join(self.root, 'expected.json'), 'w') as handle:
            handle.write('{}')
```

## Kill matrix (counter's `run_tool` + `check_site`, via `python3 judge.py`)

| fixture | pristine | M1 | M1b | M2 | M3 |
|---|---|---|---|---|---|
| K1 | ok | **FAIL scratch=1 want 0** | ok | ok | ok |
| K1b | ok | ok | **FAIL scratch=1 want 0** | ok | ok |
| K2 | ok | ok | ok | **FAIL scratch=1 want 0** | ok |
| K3 | ok | ok | ok | ok | **FAIL scratch=1 want 0** |

On the unmutated tool every fixture gave `scratch=0 unflagged=1`; each killing cell gave `scratch=1 unflagged=0`. For
example, K3 under M3 resolved to `"os.path.join(self.root, 'expected.json')tempfile.mkdtemp()se…"`. All four mutants
fail open: an unflagged expected-value write is reported as scratch, which is the false negative that the
v4 docstring at `:38-40` warns against.

## Lane corpus check (tool runs only, no counter, files from `git show a21845f:tools/*.py`)

`files=26 pristine_unflagged=0`. Files with any changed site:

- M1: `tools/context-capture.py`, only the `resolved` text at lines 1667, 1682 and 1685;
- M1b: none;
- M2: none;
- M3: none.

## Mutation hygiene and restoration

- The lane checkout was never written except for this report. `tools/write-path-census-v4.py` sha256 is unchanged
  (`784de4c0…e122fe5`, which equals `git show a21845f:tools/write-path-census-v4.py | sha256sum`). Mutants lived
  only in the copies under `/tmp/tameshi-r42w2-MutProbeAttr-work/`, which is deleted before return.
- Tooling: no installs or upgrades.

## Verdict

BROKEN: the C2 battery doesn't constrain attr binding. Four attr-class mutants (dropping the AugAssign collection,
dropping the AugAssign filter, collecting attributes from every class, resolving with the caller env) survive both
`--probe-mutant` and the tool's selftest. Fixtures K1, K1b, K2 and K3 kill exactly one each.
