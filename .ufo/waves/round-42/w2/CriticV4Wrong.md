# CriticV4Wrong — false negatives in write-path-census-v4 (round 42, wave 2)

Attacked: `tools/write-path-census-v4.py` at lane HEAD `a21845f523b75adbd3e3f7a62af91294db224ad9`
(sha256 `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5`); v3 baseline
`tools/write-path-census-v3.py` (sha256 `095924a7…0279`). No counter was run. Selftest:
`python3 tools/write-path-census-v4.py --selftest` → `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0`.

Method: 29 small fixtures, each with one `# TARGET` expected-value write. Each was scored with
`python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v4.py --file <F>.py --json`
(and v3 `--file <F>.py`), then **executed** in a sandbox cwd with `TMPDIR` pointed at a private
`_tmp/`; "lands" below is the file the run actually created outside `_tmp/` (a repo-relative path).
No fixture passes an update flag. Harness: `/tmp/tameshi-r42w2-CriticV4Wrong-fx/run.py` (deleted
before return as required; key fixture sources are reproduced at the end).

## Findings

**Result: 28 of 29 hidden.** 23 are new in v4 (v3 reported `unflagged=1`), 5 are inherited from
v3, and 1 survived. In every hidden case v4 sets `unflagged=0` through `scratch=1` or
`explicit_out=1` (or `flagged=1` in E1), even though the run wrote the expected file into the
repo tree.

### v4 regressions, ranked by realism (realism ranking is [INFERENCE])

| # | Fixture | v4 verdict (target line) | v3 | Lands | v4 mechanism (path:line) |
|---|---|---|---|---|---|
| 1 | C1 `--out` with `default="tests/golden"` | L7 `explicit_out=1 unflagged=0`, resolved ends `argparse --out` | unflagged=1 | `tests/golden/expected.json` | `Module` (v4:84-99) and `_out_flag` (v4:282-286) never inspect `default=` |
| 2 | A3 `self.root = root or tempfile.mkdtemp()`, caller `Regen("tests/fixtures")` | L10 `scratch=1` | unflagged=1 | `tests/fixtures/case1.expected` | BoolOp falls to v4:215 `return '', trace`; attr fold (v4:207-209) puts the `tempfile` text in the trace; the substring test (v4:373) passes |
| 2b | A4 same with IfExp `Path(root) if root is not None else Path(tempfile.mkdtemp())` | L10 `scratch=1` | unflagged=1 | `tests/fixtures/case1.expected` | same |
| 3 | C8 `if not dest_dir: dest_dir = "tests/golden"` inside `emit`, called only as `emit("{}", ns.out)` (`--out` default None) | L8 `explicit_out=1` | unflagged=1 | `tests/golden/expected.json` | nested `if` body walked on a copied env (v4:430); the fallback never reaches the write's env, so `_param_args` (v4:227-257) applies |
| 3b | C2 `if ns.out is None: ns.out = "tests/golden"` | L9 `explicit_out=1` | unflagged=1 | `tests/golden/expected.json` | attribute stores on the namespace are never checked |
| 4 | C7 writer `emit(blob, dest_dir)` with an in-module `emit(.., ns.out)`; a sibling module does `from lib import emit; emit("{}", "tests/golden")` | lib L6 `explicit_out=1`; caller file `{"sites": []}` | unflagged=1 | `tests/golden/expected.json` | "every in-module call" (v4:26-29, 241) is vacuously true for an importable public function, so a repo-wide census hides the write in both files |
| 5 | B1 subclass `__init__` rebinds `self.root = "tests/cases"` after `super().__init__()` | L10 `scratch=1` | unflagged=1 | `tests/cases/c1/expected.json` | `ClassInfo` (v4:111-132) reads one class body only |
| 5b | B2 subclass overrides `case_dir` (template method) | L13 `scratch=1` | unflagged=1 | `tests/cases/c1/expected.json` | `method_return` (v4:134-146) folds the base's method only |
| 6 | B8 `out_dir()` = `if self.keep: return "tests/golden"` / `return self.tmp`; `Runner(keep=True)` | L16 `scratch=1` | unflagged=1 | `tests/golden/a.expected` | v4:138 counts only top-level `Return`s, so a method with two returns folds to the unconditional one |
| 7 | B6 class attr `root = "tests/snapshots"`; `self.root = tempfile.mkdtemp()` only in an optional `isolate()` that is never called | L12 `scratch=1` | unflagged=1 | `tests/snapshots/a.snapshot` | class-body assignments are not collected (v4:118-130 walks methods only) |
| 8 | D3 promote a scratch output into golden: `golden = os.path.join("tests/golden", os.path.basename(produced))`, `produced` under `mkdtemp()` | L9 `scratch=1` | **scratch=0 unflagged=1** | `tests/golden/report.expected` | depth raised 4 to 8 (v3:43 → v4:71); the trace now reaches a `mkdtemp` five hops up through a basename argument, and a whole-trace substring decides scratch |
| 9 | C3 `ap.set_defaults(output_dir="tests/golden")` | L8 `explicit_out=1` | unflagged=1 | `tests/golden/expected.json` | as #1 |
| 10 | C12 sub-parser: `build --out`, `refresh --golden-dir dest="out" default="tests/golden"`; run `refresh` | L11 `explicit_out=1` | unflagged=1 | `tests/golden/expected.json` | `out_dests` maps dest→flag module-wide (v4:99); a non-output option sharing the dest is not detected |
| 11 | C6 `functools.partial(emit, dest_dir="tests/golden")` | L8 `explicit_out=1` | unflagged=1 | `tests/golden/expected.json` | only `Name(...)` calls are collected (v4:414) |
| 11b | C4 `HANDLERS = {"emit": emit}; HANDLERS["emit"]("{}", "tests/golden")` | L7 `explicit_out=1` | unflagged=1 | `tests/golden/expected.json` | same |
| 11c | C5 `getattr(sys.modules[__name__], "emit")("{}", "tests/golden")` | L7 `explicit_out=1` | unflagged=1 | `tests/golden/expected.json` | same |
| 12 | B3 external `r.root = "tests/golden"` after `Runner()` | L10 `scratch=1` | unflagged=1 | `tests/golden/expected.json` | non-`self` stores ignored (v4:128) |
| 13 | B4 same class, second binding `self.root, self.dirty = "tests/golden", False` | L14 `scratch=1` | unflagged=1 | `tests/golden/expected.json` | only `Attribute` targets count (v4:128); Tuple targets are skipped, so the "two distinct expressions → unresolved" guard never fires |
| 13b | B5 `setattr(self, "root", "tests/golden")` in `__init__` | L12 `scratch=1` | unflagged=1 | `tests/golden/expected.json` | same guard bypassed |
| 14 | C9 mirror loop `for out_dir in (out_dir, "tests/golden"):` | L7 `explicit_out=1` | unflagged=1 | `tests/golden/expected.json` | `_bind` (v4:342-353) has no `For` / Tuple binding, so the parameter path applies |
| 15 | C11 `if not sys.argv[1:]: ns = argparse.Namespace(out="tests/golden")` | L10 `explicit_out=1` | unflagged=1 | `tests/golden/expected.json` | as #3 |
| 16 | B7 nested class defined inside an `Outer` method assigns `self.root = tempfile.mkdtemp()`; `Outer.root = "tests/golden"` | L15 `scratch=1` | unflagged=1 | `tests/golden/expected.txt` | `ast.walk(method)` (v4:119) descends into the nested class, and the inner `self` is credited to `Outer` |
| 17 | C10 `Path(ns.out) / GOLDEN` with an absolute `GOLDEN = Path(__file__).resolve().parent/"tests"/"golden"/"expected.json"` | L9 `explicit_out=1` | unflagged=1 | `tests/golden/expected.json` | `_out_flag` follows only the left operand (v4:294-295); an absolute right operand discards it |

### Inherited from v3 (still v4 false negatives, not regressions)

- A2: `NamedTemporaryFile(dir=SNAP.parent)`, then `os.replace(fh.name, SNAP)`. v4 L11 reports
  `scratch=1`, v3 `scratch=1`, and the run lands `tests/snapshots/report.snapshot`. Both
  `os.replace` arguments share one trace (v4:331-333, 360-375), so the scratch source taints the
  repo destination.
- A5: `out_dir = out_dir or tempfile.mkdtemp()` with caller `dump("c1", "tests/data")`. v4 L7
  reports `scratch=1`, and the run lands `tests/data/c1.expected`.
- D1: a repo directory `tests/golden/tmpl/`. v4 L3 reports `scratch=1`, because `'/tmp'` is a
  substring of `/tmpl` (v4:59, 373-375).
- D2: `dest = ns.scratch_dir or "tests/golden"`. v4 L8 reports `scratch=1` because the identifier
  contains `scratch`. The run without the flag lands `tests/golden/expected.json`.
- E1: an unrelated `--update-index` option. v4 L7 reports `flagged=1`, because `--update\b`
  matches file-wide (v4:66, 437). The write lands `tests/golden/expected.json`.

### Survived

- A1: `fd, tmp = tempfile.mkstemp(dir="tests/golden"); ...; os.replace(tmp, GOLDEN)`. v4 L12
  correctly reports `unflagged=1`: the tuple target leaves `tmp` unbound, so no scratch text
  enters the trace.
- Live lane verdicts. Every expected site v4 clears in tracked `tools/*.py` at `a21845f` was
  checked: `context-capture.py:1682/1685`, `golden-verdict.py:52-56`, `registry-replay.py:123`,
  `repeat-control.py:811/820` and `wave-accounting.py:165`.
  - `SelftestHarness` (`context-capture.py:1622`) is never subclassed or rebound; its only use is
    `:2196`.
  - `registry-replay.py` requires `--out` (`:274`, `:285`) and never reassigns `args.out`.
  - Today's `live_unflagged_v4=0` is therefore not falsified on the live files. The generality
    the records claim is.

### Records the fixtures contradict

- `corpus/knowledge/r42-attribute-and-outflag-destinations.md:36-37` says that with two or more
  distinct expressions an attribute is "never read as scratch". B4 and B5 each bind `self.root`
  twice in the same class, and both come back `scratch=1`.
- Lines 70-73 of the same entry say that "class attributes, inheritance, conditional
  assignment, containers, … sub-parsers, calls into other modules and calls through a variable
  stay unresolved."
  - Each of these is instead positively resolved to safe: B6, B1/B2, C8/C11/B5, C4, C12, C7 and
    C4/C5/C6.
  - The disclaimer "an unresolved destination is not proven safe" never triggers, because v4
    does not leave these unresolved. It clears them with `unflagged=0`.
- Line 76 of the entry says "explicit_out says the operator names the destination." In C1, C2
  and C3 the operator names nothing: the repo destination is hard-coded as an argparse default,
  a `set_defaults` value, or a `None` fallback. No disclaimer covers this.

## Axes impacted

- Depth (C2). The resolver fails open: every unmodelled shape becomes "safe" instead of
  "unresolved".
- No-harm. The D3 regression comes from the depth raise alone.
- Record accuracy. The knowledge entry's "never" and "stay unresolved" claims are contradicted.

## Smallest safe correction (fail closed; each item kills the listed fixtures)

1. **Attribute binding (v4:111-132).** Leave an attribute unresolved when any of these holds:
   the class has a base; the module defines a subclass of it; any `setattr` or `__dict__` use
   exists; any Tuple, Starred, For or With target writes `self.<attr>`; a class-body assignment
   of the same name exists; or any non-`self` `<x>.<attr> =` store exists in the module. Stop
   `ast.walk` at nested `ClassDef`/`FunctionDef`. Kills B1, B3, B4, B5, B6 and B7.
2. **Method fold (v4:138).** Count every `Return` in the method body, excluding nested defs.
   Skip the fold when the module has a subclass that overrides the method. Kills B2 and B8.
3. **Scratch test (v4:373-375).** Decide scratch from the destination root only (the first
   `join` argument or the left operand of `/`), not the whole trace. Require every branch of a
   BoolOp or IfExp to be scratch. Match markers as path components (`/tmp/`) or calls
   (`tempfile.*`, `mkdtemp(`), not substrings. Kills A2, A3, A4, A5, D1, D2 and D3.
4. **Output flag (v4:84-99, 227-309).** Reject `explicit_out` in any of these cases:
   - the option has a non-`None` `default=`, or a `set_defaults` entry for that dest;
   - any non-output option shares the dest;
   - `<ns>.<dest>` is stored to, or `<ns>` is rebound anywhere in the scope;
   - the parameter is stored to anywhere in the function (including nested blocks and `for`
     targets);
   - the function name appears in any Load context other than `call.func`;
   - the function is public, so another module may import it.

   Follow `/` and `join` past the root only through relative constants. Kills C1-C12.

Add the 23 regression fixtures above to `SELFTEST` (or the frozen battery's successor) so these
shapes are pinned.

## Reproduction (key fixtures; each scored with the v4 `--json` command above)

```python
# C1 (L7 explicit_out=1; lands tests/golden/expected.json)
import argparse
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument("--out", default="tests/golden")
ns = ap.parse_args()
(Path(ns.out) / "expected.json").write_text("{}")
```

```python
# A3 (scratch=1; lands tests/fixtures/case1.expected)
import os, tempfile
class Regen:
    def __init__(self, root=None):
        self.root = root or tempfile.mkdtemp()
    def write(self, name, text):
        with open(os.path.join(self.root, name + ".expected"), "w") as fh:
            fh.write(text)
Regen("tests/fixtures").write("case1", "x")
```

```python
# B4 (scratch=1 despite two self.root bindings; lands tests/golden/expected.json)
import os, tempfile
class Runner:
    def __init__(self):
        self.root = tempfile.mkdtemp(); self.dirty = True
    def use_repo(self):
        self.root, self.dirty = "tests/golden", False
    def emit(self, text):
        with open(os.path.join(self.root, "expected.json"), "w") as fh:
            fh.write(text)
r = Runner(); r.use_repo(); r.emit("{}")
```

```python
# B8 (scratch=1; lands tests/golden/a.expected)
import os, tempfile
class Runner:
    def __init__(self, keep=False):
        self.keep = keep; self.tmp = tempfile.mkdtemp()
    def out_dir(self):
        if self.keep:
            return "tests/golden"
        return self.tmp
    def save(self, name):
        with open(os.path.join(self.out_dir(), name + ".expected"), "w") as fh:
            fh.write("x")
Runner(keep=True).save("a")
```

```python
# C8 (explicit_out=1; run without --out lands tests/golden/expected.json)
import argparse, os
def emit(blob, dest_dir):
    if not dest_dir:
        dest_dir = "tests/golden"
    with open(os.path.join(dest_dir, "expected.json"), "w") as fh:
        fh.write(blob)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out")
    ns = ap.parse_args(); emit("{}", ns.out)
main()
```

```python
# D3 (v4 scratch=1, v3 unflagged=1; lands tests/golden/report.expected)
import os, tempfile
work = tempfile.mkdtemp()
produced = os.path.join(work, "report.expected")
with open(produced, "w") as fh:
    fh.write("x")
golden = os.path.join("tests/golden", os.path.basename(produced))
with open(golden, "w") as fh:
    fh.write(open(produced).read())
```

Tooling: none installed or updated. Lane writes: this report only.

BROKEN: v4's attribute binding, method-return fold, output-flag trace and depth-8 trace clear 23 repo-landing expected-value writes as `scratch`/`explicit_out` that v3 reported as unflagged, contradicting the knowledge entry's "never read as scratch" and "stay unresolved" claims. The live-lane verdicts still hold.
