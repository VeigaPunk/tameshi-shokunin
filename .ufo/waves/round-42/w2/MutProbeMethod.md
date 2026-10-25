# MutProbeMethod — method-fold mutants of write-path-census-v4 (round 42, wave 2)

Seat: L1Tameshi42.MutProbeMethod (mutation-tester, read-only, scratch under `/tmp/tameshi-r42w2-MutProbeMethod-*`, deleted before return).
Attacked: the v4 method-return fold (`tools/write-path-census-v4.py:134-146` `ClassInfo.method_return`, gate `:195`), and the C2 counter's power to kill defects in it.
Tool under test: `tools/write-path-census-v4.py` at `a21845f523b75adbd3e3f7a62af91294db224ad9` (pre-run). `git show a21845f:tools/write-path-census-v4.py | sha256sum` and the working copy both give `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5`.
Tooling installed/updated: none.

## Findings

1. **Two of the three requested mutants survive the frozen C2 oracle, and so does an extra variant.** Only the empty-environment mutant is killed. The battery (`measure.py:72-211`, fixtures F01-F10 plus three live sites) never calls a method with more than one return. It also never calls a same-named method on a receiver other than `self`.
2. **The v4 selftest does not kill the survivors either.** All three print `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0`. The selftest case `method_two_returns` (`write-path-census-v4.py:510-526`) cannot kill either two-return variant. Its nested `return self.base` is not top-level, so `m1` never sees it. `ast.walk` visits nodes breadth-first, so the top-level `return "fixtures"` still comes first for `m1b`.
3. **Pristine-tool defect (wrong direction):** a method that has a nested `return <golden>` followed by one top-level `return <mkdtemp>` gets `scratch=1 unflagged=0`, even when the call reaches the golden branch. Fixture `X` below shows it. The docstring promises the ambiguous-attribute case is "never read as scratch" (`:17-20`), but the method fold (`:21-23`, `:138`) only counts top-level returns, so it gives no such guarantee. As a result a reachable golden write is hidden. This falls under the docstring's "Control flow … out of scope" disclaimer (`:40-41`). Still, it is a false negative, not a merely unresolved site.

## Probe command (run once per mutant, with a pristine baseline)

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a21845f523b75adbd3e3f7a62af91294db224ad9 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f --probe-mutant /tmp/tameshi-r42w2-MutProbeMethod-<id>/write-path-census-v4.py
```

Each mutant is a single-point replacement of the pristine bytes; every find string occurred exactly once.

| id | mutant (line) | sha256 | PROBE line | verdict |
|---|---|---|---|---|
| base | pristine | `784de4c0…22fe5` | `PROBE outcome=survived detail=` | baseline clean, probe conclusive |
| m1 | two returns, first wins: `:139` `if len(returns) != 1:` becomes `if not returns:` | `5d8a9685…ee5736` | `PROBE outcome=survived detail=` | **survived** |
| m1b | variant: returns collected by `ast.walk(method)` (nested included), first wins, `:138-139` | `3aa9d03e…19b5` | `PROBE outcome=survived detail=` | **survived** |
| m2 | skip method env: `:146` `return returns[0].value, env` becomes `return returns[0].value, {}` | `c2cd78db…eb91b` | `PROBE outcome=killed detail=F01_attr_scratch scratch=0 want 1` | killed |
| m3 | fold any `x.<m>()`: `:195` `_is_self_attr(node.func)` becomes `isinstance(node.func, ast.Attribute)` | `a8dfa40a…04f8` | `PROBE outcome=survived detail=` | **survived** |

Every probe exited 0 with the line `C2_R42_CONTROL: probe_outcome=<same> rev=a21845f523b75adbd3e3f7a62af91294db224ad9 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f`.
Selftest (`python3 -I <copy> --selftest`): base, m1, m1b and m3 print `cases=15 failed=0`. m2 prints `FAIL attr_bound_scratch: scratch=False, want True`, `FAIL attr_bound_scratch: unflagged=True, want False`, `failed=2`.

## Killing fixtures for the survivors

Each fixture was run with `python3 -I <copy> --file <fixture> --json` on the pristine copy and on all four mutants. The bits shown are for the one expected-value site.

**K1, kills m1 and m1b** (the declared spec is "exactly one top-level return"; want `expected=1 scratch=0 explicit_out=0 unflagged=1`):

```python
import os
import tempfile


class H:
    def __init__(self):
        self.root = tempfile.mkdtemp()

    def case_dir(self, name):
        return os.path.join(self.root, name)
        return os.path.join('golden', name)

    def run(self):
        with open(os.path.join(self.case_dir('a'), 'expected.json'), 'w') as handle:
            handle.write('{}')
```

Results at L14: base, m2 and m3 give `scr=0 unfl=1`; m1 and m1b give `scr=1 unfl=0`. Caveat: the second top-level return is dead code, so "first wins" is right at run time. K1 enforces the documented conservative contract, not a reachable write. m1 is behaviorally near-equivalent for top-level returns. The real-world risk lies in m1b and in finding 3.

**K1b, kills m1b with reachable code** (want `unflagged=1`):

```python
import os
import tempfile


class H:
    def __init__(self):
        self.root = tempfile.mkdtemp()

    def case_dir(self, name, fresh):
        if fresh:
            return os.path.join(self.root, name)
        else:
            return os.path.join('golden', name)

    def run(self):
        with open(os.path.join(self.case_dir('a', False), 'expected.json'), 'w') as handle:
            handle.write('{}')
```

Results at L16: base, m1, m2 and m3 give `scr=0 unfl=1`; m1b gives `scr=1 unfl=0`, which hides a golden write.

**K3, kills m3** (a foreign receiver whose method shares a name with a same-class method; want `unflagged=1`):

```python
import os
import tempfile


class H:
    def __init__(self):
        self.root = tempfile.mkdtemp()

    def case_dir(self, name):
        return os.path.join(self.root, name)

    def run(self, peer):
        with open(os.path.join(peer.case_dir('a'), 'expected.json'), 'w') as handle:
            handle.write('{}')
```

Results at L13: base, m1, m1b and m2 give `scr=0 unfl=1`; m3 gives `scr=1 unfl=0`, folding `peer.case_dir` into `self.root = mkdtemp()`.

**X, a pristine-tool false negative (finding 3; no mutant needed)**:

```python
import os
import tempfile


class H:
    def __init__(self):
        self.root = tempfile.mkdtemp()

    def case_dir(self, name, keep):
        if keep:
            return os.path.join('golden', name)
        return os.path.join(self.root, name)

    def run(self):
        with open(os.path.join(self.case_dir('a', True), 'expected.json'), 'w') as handle:
            handle.write('{}')
```

Result at L15: all five copies, pristine included, give `scr=1 unfl=0`. The call takes the `golden` branch, yet the site is cleared as scratch.

## Consequence for C2

The predicate needs one killed mutant of class `method` in `mutants.json` (`measure.py:38-40`, `:455`). A MutantAuthor that picks the env-skip shape (m2) gets a kill from F01. The return-count and receiver gates, however, are not covered by the frozen battery or by the selftest. That is a coverage finding, not a contract change. Adding K1b and K3 to the v4 selftest (or to a successor battery) would kill both survivors.

## Restoration evidence

The lane checkout was never written apart from this report. `sha256sum tools/write-path-census-v4.py` gives `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5` both before and after, the same as the copy at `a21845f`. All mutants and fixtures lived under `/tmp/tameshi-r42w2-MutProbeMethod-{base,m1,m1b,m2,m3,fixtures}` and were removed before return.

Verdict: `BROKEN: the C2 battery and the v4 selftest kill no method-fold mutant except env-skip. Two-return (m1 and m1b) and any-receiver (m3) survive; killing fixtures are K1/K1b and K3. Pristine v4 also clears a reachable golden write as scratch (fixture X).`
