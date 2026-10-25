# ReviewV4Entry — round 42 wave 2 (FALSIFY)

Attacked: `corpus/knowledge/r42-attribute-and-outflag-destinations.md` (as landed at
`a21845f`) against `tools/write-path-census-v4.py` behavior. Axis: depth. Method: v4 run
directly (`python3 tools/write-path-census-v4.py --file F --json`) on 32 small probe files
under `/tmp/tameshi-r42w2-ReviewV4Entry-probes/` (deleted before return; every falsifying
source is inlined below). No counter run in default mode; no lane edits besides this file.
Runtime of each falsifying probe was cross-checked with plain Python where the claim is
about what the destination really is. Accessed 2026-10-25.

## Findings — false sentences (by severity)

### F1 (high) — "What is not claimed", bullet 1: 7 of the 11 listed shapes do NOT "stay unresolved"; v4 resolves them, mostly to a *safe* class

Entry `:70-73`: "Aliases, closures over reassigned names, attribute reassignment outside `self`, class
attributes, inheritance, conditional assignment, containers, `parse_known_args`, sub-parsers,
calls into other modules and calls through a variable stay unresolved."

| shape | probe (expected-value site result) | holds? |
|---|---|---|
| aliases | p20 `me = self; open(join(me.base,"expected.json"),"w")` → `scratch=0 explicit_out=0 unflagged=1` | holds |
| closures over reassigned names | p29 → `scratch=1 unflagged=0`; runtime dest is `tests/fixtures` | **FALSE** |
| attribute reassignment outside `self` | p12, p24 → `explicit_out=1 unflagged=0` | **FALSE** |
| class attributes | p07 → `unflagged=1` (holds); p08 → `scratch=1` (class attr ignored) | **FALSE** (p08) |
| inheritance | p06, p11 → `unflagged=1` (holds); p05 → `scratch=1` | **FALSE** (p05) |
| conditional assignment | p09, p08 → `scratch=1` | **FALSE** |
| containers | p22 → `scratch=1` | **FALSE** |
| `parse_known_args` | p14 (tuple unpack), p15 (`[0]`) → `explicit_out=0 unflagged=1` | holds |
| sub-parsers | p16 → `explicit_out=1` | **FALSE** (resolved, not unresolved) |
| calls into other modules | p21 → `scratch=1` | **FALSE** |
| calls through a variable | p17, p18 → `explicit_out=1` (see F3) | **FALSE** |

Probe sources (each run as `python3 tools/write-path-census-v4.py --file pNN.py --json`):

```python
# p29 closure over reassigned name -> scratch=1 unflagged=0 (runtime: tests/fixtures)
import os, tempfile
def make():
    d = tempfile.mkdtemp()
    def w():
        with open(os.path.join(d, "expected.json"), "w") as fh:
            fh.write("y")
    d = "tests/fixtures"
    return w
```
```python
# p12 attribute reassignment outside self -> explicit_out=1 unflagged=0
import argparse, os
ap = argparse.ArgumentParser()
ap.add_argument("--out")
ns = ap.parse_args()
ns.out = "tests/fixtures"
with open(os.path.join(ns.out, "expected.json"), "w") as fh:
    fh.write("y")
```
```python
# p24 parser b never declares --out; nb.out hard-set -> explicit_out=1 unflagged=0
import argparse, os
a = argparse.ArgumentParser(); a.add_argument("--out")
b = argparse.ArgumentParser(); b.add_argument("--src")
nb = b.parse_args(["--src", "x"])
nb.out = "tests/fixtures"
with open(os.path.join(nb.out, "expected.json"), "w") as fh:
    fh.write("y")
```
```python
# p08 class attribute + conditional self assignment -> scratch=1 unflagged=0
import os, tempfile
class R:
    root = "tests/fixtures"
    def __init__(self, fast):
        if fast:
            self.root = tempfile.mkdtemp()
    def go(self):
        with open(os.path.join(self.root, "expected.json"), "w") as fh:
            fh.write("y")
```
```python
# p05 inheritance: subclass overrides root -> parent site still scratch=1
import os, tempfile
class Base:
    def __init__(self):
        self.root = tempfile.mkdtemp()
    def go(self):
        with open(os.path.join(self.root, "expected.json"), "w") as fh:
            fh.write("y")
class Child(Base):
    def __init__(self):
        self.root = "tests/fixtures"
```
```python
# p09 conditional assignment -> scratch=1 (pre-if binding wins; if-body env is a copy)
import os, tempfile, sys
d = tempfile.mkdtemp()
if len(sys.argv) > 1:
    d = "tests/fixtures"
with open(os.path.join(d, "expected.json"), "w") as fh:
    fh.write("y")
```
```python
# p22 container: whole dict text lands in the trace -> scratch=1 though key "b" is a repo dir
import os, tempfile
dirs = {"a": tempfile.mkdtemp(), "b": "tests/fixtures"}
with open(os.path.join(dirs["b"], "expected.json"), "w") as fh:
    fh.write("y")
```
```python
# p21 other-module call: identifier text "scratch_root" matches a SCRATCH_MARKER -> scratch=1
import os, helpers
with open(os.path.join(helpers.scratch_root(), "expected.json"), "w") as fh:
    fh.write("y")
```
```python
# p16 sub-parser option -> explicit_out=1 (resolved, contrary to "stay unresolved")
import argparse, os
ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd")
w = sub.add_parser("write"); w.add_argument("--out")
ns = ap.parse_args()
with open(os.path.join(ns.out, "expected.json"), "w") as fh:
    fh.write("y")
```

Mechanisms (path:line): conditional/closure — `_walk_stmts` binds top-level statements and
recurses with `dict(env)` copies (`tools/write-path-census-v4.py:420,430`), so the pre-branch
or pre-def binding survives; class attributes and inheritance — `ClassInfo` sees only
`self.<attr>` assignments inside the class's own methods (`:115-132`); attribute reassignment
outside `self` — `_out_flag` keys only on `<name>.<dest>` + any `parse_args` call, never on
later stores (`:282-286`, `:264-265`), and `Module.out_dests` is module-global, not per
parser (`:99`); containers/other modules — `scratch` matches markers in the raw source
*trace*, including identifier text (`:373-375`, `:200-205`, `:212-214`).

The bullet's next sentence "An unresolved destination is not proven safe" is undercut in
practice: v4 classifies p04, p21, p22 and p29 as `scratch` (the safe class), not unresolved.

### F2 (high) — Step 1 guarantee "leave it unresolved, so it is never read as scratch" is false; "every `self.<attr> = <expr>` … is collected" is incomplete

Entry `:35-37`. Probes:

```python
# p04 two distinct plain assignments, neither scratch -> scratch=1 unflagged=0
import os
class R:
    def __init__(self):
        self.scratch = "fixtures"
    def reset(self):
        self.scratch = "tests/golden_dir"
    def go(self):
        with open(os.path.join(self.scratch, "expected.json"), "w") as fh:
            fh.write("y")
```
```python
# p01 tuple-target rebinding not collected -> attr resolves to mkdtemp -> scratch=1
import os, tempfile
class R:
    def __init__(self):
        self.base = tempfile.mkdtemp()
    def reset(self):
        self.base, other = "fixtures", 1
    def go(self):
        with open(os.path.join(self.base, "expected.json"), "w") as fh:
            fh.write("y")
```

Same `scratch=1` result for p02 (`setattr(self, "base", "fixtures")`), p03
(`for self.base in ("fixtures", "tests"):`), p05 (subclass override), p08 (class attr).
p04 is the sentence's own scenario (two distinct expressions) and is still read as scratch,
because the unresolved attribute's *name* is in the trace and matches `'scratch'`
(`:58-65`, `:373`). p01/p03: `ClassInfo` collects only `Assign`/`AnnAssign`/`AugAssign` whose
target is directly `self.<attr>` (`:121-130`). Tuple, for-loop, `with … as self.x` and
`setattr` rebindings are skipped, so the "two or more distinct" check never fires.
Held: p25 (augmented assignment) → `unflagged=1`; selftest `attr_two_assignments` holds.

### F3 (high) — Step 3 "A single call with any other argument (a constant, an `--input` value) keeps the site unflagged" is false

Entry `:43-46`. Probes, all → `explicit_out=1 unflagged=0`:

```python
# p17 constant passed through a call via a variable
import argparse, os
def emit(blob, dest_dir):
    with open(os.path.join(dest_dir, "expected.json"), "w") as fh:
        fh.write(blob)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out")
    ns = ap.parse_args()
    emit("{}", ns.out)
    f = emit
    f("{}", "tests/fixtures")
```
- p18: `emit(ns.out)` plus `list(map(emit, ["tests/fixtures"]))`.
- p23b: `def emit(blob, dest_dir, extra=None)`, calls `emit("{}", ns.out)` and
  `emit(*["{}", "tests/fixtures"], ns.out)`. At runtime `dest_dir == "tests/fixtures"`
  (confirmed with `python3 -c`); v4 reads `call.args[1]` = `ns.out` because it only rejects a
  `Starred` at the parameter's own index (`:247-250`).
- p19: a nested `def inner(dest_dir)` inside module-level `emit(blob, dest_dir)` is called
  as `inner("tests/fixtures")`. v4 maps the inner parameter to the outer function's call
  sites, because `ctx.func` is only set for top-level defs (`:424-426`, `:234-239`). This also
  falsifies the precondition "its root is a parameter of a module-level function".

Cause: call sites are collected only where `node.func` is a bare `Name` in `module.funcs`
(`:414-415`). Indirect calls are dropped, not treated as "any other argument". Held: p26
(keyword-only argument), selftest `output_param_one_constant_caller`.

### F4 (medium) — "`explicit_out` says the operator names the destination" (`:76`) is false

All → `explicit_out=1 unflagged=0`:
- p13 `ap.add_argument("--out", default="tests/fixtures")`. With no `--out` given,
  `parse_args([]).out == "tests/fixtures"` (runtime-confirmed), so the operator named nothing.
- p28 `ns = ap.parse_args(["--out", "tests/fixtures"])`: a hard-coded argv list
  (runtime → `tests/fixtures`). `_parse_args_ns` accepts any `.parse_args(...)` call,
  whatever its arguments (`:264-265`).
- p12 and p24 above: the destination is overwritten in code.

### F5 (low) — Records claim: "The round-42 records carry the renamed-identifier falsifier that separates the two (`corpus/lessons/round-42.md`)" overstates

Entry `:81-82`. The cited lesson only promises it: `corpus/lessons/round-42.md:157-159`
says the separation "is shown outside the predicate, by a renamed-identifier battery run in
wave 2". `SCORECARD.md:2017` says the falsifier "runs" outside the predicate. The harness
itself is in a wave-1 report (`.ufo/waves/round-42/w1/CriticFixtureOverfit.md:58-74`), which
was run only against v3 and the two cheat copies (v4 was absent: `:78`). Its files live in
uncommitted `/tmp/tameshi-r42-CriticFixtureOverfit-r1/`. I ran it against the landed v4 for
this review:

```
$ cd /tmp && python3 /tmp/tameshi-r42-CriticFixtureOverfit-r1/renamed_falsify.py \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v4.py
R01_attr_scratch_renamed ok … R06_inflag_renamed ok
SUMMARY 6/6
```
(harness sha256 `cab9ccf0…902f`, cases `f91a43c7…9ef5`, both matching the w1 report). So the
substance holds: v4 is a resolver and passes 6/6 renamed cases. But the records do not
"carry" the falsifier or its v4 result; the cited file defers it to wave 2.

### F6 (low) — "text mode keeps v3's line format" is only half true

The per-site line is byte-identical (v3 `tools/write-path-census-v3.py:327-337` vs v4
`:677-687`). But v4 drops v3's trailing totals line (v3 `:339`). For
`--file tools/registry-replay.py`, v3 prints 2 lines and v4 prints 1. No in-lane consumer
breaks: the counter's text mode parses only site lines (`measure.py:213`). Text mode also
never shows `explicit_out`, so the only text-mode cue for `unflagged=0` on
`registry-replay.py:123` is the `argparse --out` suffix.

### Secondary — source-quote metadata in "What the sources state" (outside the two assigned sections)

- `:20-21` "(14 words)": the quoted sentence pair is **17** words (`echo "$q" | wc -w` → 17;
  scout's own count is 17, `.ufo/waves/round-42/w1/ScoutArgparse.md:24`).
- `:15-17` "Lines 1513–1514": in the raw snapshot, "Any" ends line **1512**, so the span is
  1512–1514. Count is 20 by `wc -w` (18 without the `-`/`_` tokens), not 19.
- `:60-61` Stryker quote "is not represented in your mutation score" is **7** words, not 8.
- Snapshot sha256 matches (`3158c439…93b7`). The quotes at raw lines 1504–1505 and 1650–1651
  are present.

## What survived the attack

- **Live-site table: SURVIVES.** `tools/context-capture.py:1682`/`:1685` are the two
  `open(expected_path, …)` writes. `:1624-1625` is `self.root = tempfile.mkdtemp(…, dir="/tmp")`
  and `:1631-1635` is `case_dir`. `tools/registry-replay.py:123` writes `out / 'expected.json'`,
  `:181`/`:185` and `:282` are the only two `publish(` calls, and `--out` is at `:259`.
  v3 gives `unflagged=1` on all three. v4 gives `scratch=1 unflagged=0` with `mkdtemp` in
  `resolved` at 1682/1685, and `unflagged=0` with `resolved` ending `argparse --out` at 123:
  `python3 tools/write-path-census-v{3,4}.py --file tools/{context-capture,registry-replay}.py`.
  Imprecision only: the base at 1682/1685 is `directory`, which is bound to
  `self.case_dir(name)` at `:1660`. And `:181`'s `args` is a parameter of `run_replay`, so
  the chain needs `:287 run_replay(a)` and `:262 a = p.parse_args()`, which the table omits.
- **"Resolution depth rises from four to eight; the context-capture chain needs six":
  SURVIVES.** v3 `MAX_DEPTH = 4` (`v3:43`), v4 `= 8` (`v4:71`), and both use the same
  `depth > MAX_DEPTH` test. Ablation with copies `sed 's/^MAX_DEPTH = 8/MAX_DEPTH = k/'`:
  1682/1685 flip to `scratch=1` first at k=6. registry-replay:123 needs k=7 (not claimed).
- **Step 2 (method-return fold) is literally accurate** (`:134-146`). But it resolves
  methods with *nested* conditional returns to the top-level one. p10 (`if keep: return
  "tests/fixtures"` / `return self.base`) → `scratch=1`. That is the same conditional gap as F1.
- **Step 3 dest derivation matches S157.** It uses the first double-dash long option with
  leading `-` stripped and internal `-`→`_`, or a constant `dest=` (`:92-99`). p27
  `-o/--out-dir` → `ns.out_dir` → `explicit_out=1`.
- **`--json` prints every write site with v3's record fields plus `explicit_out`**
  (`:378-385`). v3 has no `--json` at all.
- **`flagged` stays file-global:** p30 has the flag string only inside a help constant and
  still gets `flagged=1 unflagged=0` (`:437`).
- **`registry-replay.py --out tests/` would overwrite `expected.json`:** confirmed by `:123`.
- **Lane-wide unflagged = 0:** v4 `--json` over all 26 `git ls-files 'tools/*.py'` →
  `files 26 unflagged 0`, no parse errors.
- **Held "unresolved" shapes:** aliases (p20), plain class attribute (p07), inherited
  attribute read (p06), inherited method (p11), `parse_known_args` (p14, p15), and
  augmented-only attribute (p25). All give `unflagged=1`.
- `--selftest` → `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0`.

## Residual risk / gaps

- I did not run any counter (`measure.py`), in any mode.
- The scratch-marker-on-identifier behavior (F1 p21, F2 p04) is inherited from v3's trace
  heuristic. The entry's own guarantees still state it cannot happen.
- No tools installed or upgraded. `tools/__pycache__/write-path-census-v4.cpython-314.pyc`
  (mtime 09:46:48 UTC, gitignored by `.gitignore:4`) was not produced by this seat: every run
  here executed v4 as `__main__`, which writes no bytecode for itself.

BROKEN: the entry's scope disclaimers and guarantees — 7 of 11 "stay unresolved" shapes are resolved (mostly to scratch/explicit_out), Step 1's "never read as scratch", Step 3's "a single other call keeps the site unflagged", and "explicit_out says the operator names the destination" are each falsified by a runnable probe; the live-site table, depth claim and lane-wide count survive.
