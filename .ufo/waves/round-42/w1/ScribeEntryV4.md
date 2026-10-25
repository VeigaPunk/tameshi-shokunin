# ScribeEntryV4 — draft r42-attribute-and-outflag-destinations.md (C2 knowledge entry)

Scribe seat (leaf, no dispatch), round 42 wave 1. Access date: 2026-10-25.
Report path (relative to lane repo): `.ufo/waves/round-42/w1/ScribeEntryV4.md`.

## Findings (each with exact source / path:line)

1. **Contract (C2) read** — `.ufo/evidence/round-42/contract.json` `claims.C2`:
   surface = "the F4 write-path census gains two destination edge classes v3 cannot bind:
   instance attributes bound in the enclosing class (through a same-class method whose
   return folds) and destinations rooted at an argparse output option traced through
   every in-module call site; knowledge entry
   corpus/knowledge/r42-attribute-and-outflag-destinations.md; capability instrument
   tools/write-path-census-v4.py". Statement: the three live v3 false positives
   (`tools/context-capture.py:1682`, `:1685`, `tools/registry-replay.py:123`) are
   classified not-unflagged with resolved text naming `mkdtemp` / `--out`, every
   fixture keeps its declared classification, and every declared mutant of the new
   resolution code is killed under the exit-plus-FAIL oracle. `counter`
   `.ufo/evidence/round-42/census/measure.py` sha256 `3c3727ece033263f9e68ca2601012dc0170c6387cee44f3e7c09ee5744890ff2`.

2. **Live false positives (the write sites v3 mis-flags)**:
   - `tools/context-capture.py:1682` — `with open(expected_path, "wb") as handle:` and
     `:1685` — `with open(expected_path, "w", encoding="utf-8") as handle:`. Binding
     chain: `self.root = tempfile.mkdtemp(..., dir="/tmp")` (`:1624`) →
     `directory = self.case_dir(name)` (`:1660`) → `case_dir` returns
     `os.path.join(self.root, ...)` (`:1633`) → `expected_path = os.path.join(directory,
     "expected.json")` (`:1662`). The destination is rooted at an instance attribute
     whose value is a `mkdtemp` return folded through a same-class method's return.
   - `tools/registry-replay.py:123` — `(out / 'bundle.json').write_bytes(raw)` inside
     `publish(code, report, bundle, out)` (`:116`). Binding chain: `--out` declared at
     `:259` (`p.add_argument('--out')`), `a = p.parse_args()` (`:262`),
     `out = Path(args.out)` (`:181`), call sites `publish(code, report, bundle, out)`
     (`:185`) and `publish(code, report, bundle, Path(a.out))` (`:282`). Both
     in-module call sites root `out` at the argparse `--out` dest. This is the
     output-flag class (explicit `--out` directory; not an update-flag hazard).

3. **v3's failure mechanism** — `tools/write-path-census-v3.py:58-100` (`_resolve`):
   for an `Attribute` node the base is resolved ( `:94-96`); `self` is a bare `Name`
   absent from the env, so `self.root` resolves to `root` with no scratch trace →
   `scratch=0` for `:1682/:1685`. For registry-replay `:123`, the update-flag pattern
   (`FLAG_RE`, `:41`) does not include argparse output options and `_resolve` cannot
   fold the argparse Namespace → `explicit_out=0`. Confirmed by control receipts:
   `.ufo/evidence/round-42/control/c2-v3-in-slot.stdout` shows `FAIL F01_attr_scratch
   scratch=0 want 1`, `FAIL F04_outflag explicit_out=0 want 1` and the three live
   site FAILs; `.ufo/evidence/round-42/control/c2-junk.stdout` shows a junk tool fails
   F01-F09 + the three live sites; `.ufo/evidence/round-42/before/c2-at-base.stdout`
   shows `tool_absent=1 live_unflagged_v3=3 C2_R42_PASS=false`.

4. **Fixture contract (the classification lattice)** — `.ufo/evidence/round-42/census/measure.py`:
   `FIXTURES` (`:72-202`) F01-F10, `LIVE` (`:204-211`) with declared bits
   (expected/scratch/explicit_out/unflagged) and resolved-text needles `mkdtemp` /
   `--out`; `oracle` (`:311-317`) exit-plus-FAIL; predicate `:462-465`.
   F01 = attr+scratch (`mkdtemp`), F02 = attr+golden (unflagged), F03 = attr+
   ambiguous rebind (unflagged), F04 = outflag (explicit_out, `--out`), F05 =
   inflag (unflagged), F06 = outflag with mixed callers (unflagged), F07/F08/F09 =
   constant/join/symlink (unflagged), F10 = sys.argv update flag (not unflagged).

5. **S157 source (argparse docs), opened this round** — https://docs.python.org/3/library/argparse.html.
   Verified anchors: `#dest` (HTML line 1490; quotes at lines 1504-1514) and
   `#the-parse-args-method` (line 1645; quote at 1650-1651). Snapshot copy fetched to
   `/tmp/tameshi-r42-ScribeEntryV4-src/argparse.html` sha256
   `3158c439e504752c93f582ddec59483a75c890411c1d3ee3b733125950bf93b7`, 328434 bytes
   (identical digest to ScoutArgparse's capture). Lane-side pin at
   `.ufo/evidence/round-42/sources/argparse.html` is not yet written (read-only seat);
   digest may shift on re-pin due to docs.python.org's footer clock (round-33/40 lesson).

6. **S155 source (PIT outcome vocabulary, adopted this round from staged:S159)** —
   https://pitest.org/quickstart/basic_concepts/ "Run error" definition: "A run error
   means something went wrong when trying to test the mutation." (13 words, page
   lines 192-193). PIT lists Run error as a separate outcome class from Killed; the
   page does not count run errors as kills or as scoring input. The kill oracle's
   runtime-error class (contract C2.kill_oracle) is this PIT "Run error" = Stryker
   RuntimeError: non-zero exit / Traceback / unparseable output is `runtime_error`, not
   killed.

7. **Tooling**: no tools installed or upgraded (curl/sha256sum already present;
   pacman transactions paused; nothing needed).

8. **Could not check**: the deciding-run numerics (placeholders below); the final
   pinned digest of the lane argparse snapshot; the v4 implementation itself
   (`tools/write-path-census-v4.py` does not exist at base — confirmed by
   `ls tools/write-path-census-v4.py` → no such file; `ls` of round-42/census
   contains only `measure.py`).

---

## Draft entry (fenced; L1 lands at `corpus/knowledge/r42-attribute-and-outflag-destinations.md`)

```markdown
source: S153 — ast — Abstract syntax trees (Python 3.15.1 documentation) — https://docs.python.org/3/library/ast.html — snapshot .ufo/evidence/round-41/sources/ast.html sha256 183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317 — opened 2026-10-25 (held)
source: S157 — argparse — Parser for command-line options, arguments and subcommands (Python 3.15.1 documentation) — https://docs.python.org/3/library/argparse.html — snapshot .ufo/evidence/round-42/sources/argparse.html (sha256 <from deciding run>; capture digest 3158c439e504752c93f582ddec59483a75c890411c1d3ee3b733125950bf93b7, 328434 B) — opened 2026-10-25
source: S155 — PIT basic concepts — https://pitest.org/quickstart/basic_concepts/ — §Run error — opened 2026-10-23, verified 2026-10-25 (adopted this round from staged:S159)
verified-at: 2026-10-25
recheck: 180d — re-open the committed argparse and PIT snapshots and re-locate the quotes below in the tag-stripped text
ground: F4 (write-path census / golden-snapshot fixture discipline)

# Two destination classes the live v3 census cannot bind

## What the sources state

- S153 (held; CPython `ast` reference) gives the machinery: a parsed tree exposes
  `Name`, `Assign`, `Call` and `Attribute` nodes, `ast.get_source_segment` recovers a
  node's source, and `iter_child_nodes` / `NodeVisitor` walk the tree. Assignment and
  call stay in one tree — the property a line-oriented matcher lacks.
- S157 (argparse): "For optional argument actions, the value of `dest` is normally
  inferred from the option strings." (15 words, §The add_argument() method, anchor
  `#dest`). Mechanism: "ArgumentParser generates the value of dest by taking the first
  double-dash long option string and stripping away the initial `-` characters." (21
  words, `#dest`). `parse_args` assigns into a Namespace: "Convert argument strings to
  objects and assign them as attributes of the namespace. Return the populated
  namespace." (17 words, anchor `#the-parse-args-method`). So `--out` ⇒ dest `out` ⇒
  attribute `args.out` after `parse_args()`.
- S155 (PIT, adopted): "A run error means something went wrong when trying to test the
  mutation." (13 words). PIT lists Run error as a distinct outcome class alongside
  Killed; the page does not count run errors as kills or as scoring input.

Neither source describes static analysis. They supply what v4's two chains use: for the
attribute class, assignments reachable as `self.<attr>` inside the class; for the
output-flag class, an option string's dest becoming a Namespace attribute; for the
oracle, the run-error outcome class.

## What v4 does

1. **Attribute-bound destinations** (class `attr`): an assignment `self.<attr> =
   <value>` inside the enclosing class enters an attribute environment; a same-class
   method whose body returns an expression over that attribute (e.g. `case_dir`
   returning `os.path.join(self.root, name)`) folds onto the caller's assignment when
   the method is called on `self`; local chaining (`expected_path = os.path.join(
   directory, ...)`) then carries that trace to the write site. The scratch marker
   (`tempfile.mkdtemp`, `/tmp`, ...) becomes visible → `scratch=1`, `unflagged=0`.
   Live effect: `tools/context-capture.py:1682` and `:1685` resolve to text naming
   `mkdtemp`.
2. **Output-flag destinations** (class `outflag`): `add_argument('--out')` records the
   option string; `parse_args()` yields a Namespace whose attribute is the dest
   (`args.out`); every in-module call site that passes a value rooted at `args.out`
   (through `Path(args.out)` or directly) is traced to the write site → `explicit_out=1`
   with `resolved` naming `--out`. If any in-module call site roots the parameter at a
   non-flag value (literal, another flag, or an unknown base), the site is **not**
   tagged `explicit_out` (F06). Live effect: `tools/registry-replay.py:123` resolves
   to `--out` via call sites at `:185` and `:282`.
3. The `resolved` field stays a trace of consulted source segments (the r41 reading
   rule), not a normalized path.

## What v4 does not resolve

- Ambiguous attribute re-binding: an attribute reassigned after its defining assignment
  (F03 `rebase` → `self.root = 'golden'`) is not provably scratch; the site keeps its
  conservative classification (`unflagged=1`). Scratch/explicit_out claims are only
  made on single-source evidence.
- Mixed callers: F06 (`publish(..., Path(args.out))` and `publish(..., Path('golden'))`)
  is not `explicit_out` — the flag class requires every in-module call site to agree.
- Input flags (`--input`, F05) and module-level constants (F07), variable joins (F08),
  symlinks (F09), and `sys.argv` update flags (F10) are unchanged from v3.
- The v3 bounds persist: depth-4 bounded recognizer, not a dataflow analyser; aliases,
  closures over reassigned names, dictionary/list elements, block rebindings, and paths
  computed by non-folding calls are not resolved. Attribute resolution is class-scoped
  (the enclosing class's own methods), not interprocedural beyond the traced chains.

## The kill oracle (exit-plus-FAIL, per contract C2.kill_oracle)

Killed iff every battery run exits 0 with parseable output **and** at least one battery
case differs from its declared classification (a FAIL line names it). Non-zero exit,
Traceback or unparseable output is `runtime_error` — S155's PIT "Run error" / Stryker
RuntimeError, which neither tool counts as a kill. No differing case = survived. Mutant
protocol: `mutants.json` declares >= 3 mutants covering classes `attr`, `method`,
`outflag`, each `find` occurring exactly once in the v4 bytes and each applying exactly
once; each mutant must be `killed`.

## Measured classification (one default-mode deciding run at the measurement revision)

| check | declared | observed |
|---|---|---|
| F01_attr_scratch | scratch=1 unflagged=0 "mkdtemp" | <from deciding run> |
| F02_attr_golden | unflagged=1 | <from deciding run> |
| F03_attr_ambiguous | unflagged=1 | <from deciding run> |
| F04_outflag | explicit_out=1 unflagged=0 "--out" | <from deciding run> |
| F05_inflag | unflagged=1 | <from deciding run> |
| F06_outflag_mixed_callers | unflagged=1 | <from deciding run> |
| F07_module_constant | unflagged=1 | <from deciding run> |
| F08_variable_join | unflagged=1 | <from deciding run> |
| F09_symlink | unflagged=1 | <from deciding run> |
| F10_update_flag | unflagged=0 | <from deciding run> |
| live context-capture.py:1682 | scratch=1 unflagged=0 "mkdtemp" | <from deciding run> |
| live context-capture.py:1685 | scratch=1 unflagged=0 "mkdtemp" | <from deciding run> |
| live registry-replay.py:123 | explicit_out=1 unflagged=0 "--out" | <from deciding run> |
| selftest_exit | 0 | <from deciding run> |
| fixtures_pass | 10/10 | <from deciding run> |
| run_errors | 0 | <from deciding run> |
| live_unflagged_v4 | 0 | <from deciding run> |
| live_tool_errors_v4 | 0 | <from deciding run> |
| mutants (>=3: attr, method, outflag) | all killed | <from deciding run> |
| C2_R42_PASS | true, exit 0 | <from deciding run> |

## What is not claimed

- No universality: two new classes are resolved; the v3 bounded-recognizer caveats
  remain in force and F03/F06 carve the conservative no-claim zones.
- No interprocedural analysis beyond the two traced chains; no taint or dataflow
  guarantee.
- No change to v2/v3 pins; v3 stays at its round-41 sha and this entry does not edit
  tools.
- No claim that the live `tools/*.py` census has no other reporting gap; the only
  measured live sites are the three above.
```

---

Report trailer: every path above is relative to `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
