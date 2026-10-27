source: S157 — argparse — Parser for command-line options, arguments and subcommands (Python 3.15.1 documentation) — https://docs.python.org/3/library/argparse.html — §dest (`#dest`) and §The parse_args() method — snapshot .ufo/evidence/round-42/sources/python-argparse.html sha256 3158c439e504752c93f582ddec59483a75c890411c1d3ee3b733125950bf93b7 — opened 2026-10-25
source: S153 — ast — Abstract syntax trees (Python 3.15.1 documentation) — https://docs.python.org/3/library/ast.html — snapshot .ufo/evidence/round-41/sources/ast.html — opened 2026-10-25 (round 41)
source: S001 — Mutant states and metrics (Stryker Mutator docs) — https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ — §Mutant states, Runtime error — snapshot .ufo/evidence/round-42/sources/stryker-mutant-states.html sha256 ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11 — re-opened 2026-10-25
source: S158 — DetectionStatus.java (PIT source, hcoles/pitest@f7fe5adf) — snapshot .ufo/evidence/round-42/sources/pit-DetectionStatus.java — opened 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-open the committed argparse snapshot and re-locate the §dest quotes below in the tag-stripped text
ground: F4 (golden / snapshot fixture discipline) — write-path half

# An attribute or an output flag can carry a write destination that a line-local census misreads

## What the sources state

- S157, §dest, snapshot lines 1504–1505: "For optional argument actions, the value of
  dest is normally inferred from the option strings." (15 words). Lines 1512–1514: "Any
  internal - characters will be converted to _ characters to make sure the string is a
  valid attribute name." (20 words). So `add_argument('--out-dir')` puts the value at
  `ns.out_dir`, and the destination of a write rooted at `ns.out_dir` is whatever the
  operator passed on the command line **when the option has no default** (S157 §default,
  snapshot lines 1209–1211: "The default keyword argument of add_argument() specifies what
  value should be used if the command-line argument is not present." — 18 words;
  `set_defaults()` supplies the same).
- S157, §The parse_args() method, lines 1650–1651: "Convert argument strings to objects
  and assign them as attributes of the namespace. Return the populated namespace."
  (17 words). That is the binding the tool checks for: the namespace must come from a
  `parse_args(...)` call before an attribute read counts as an option value.
- S153 (held since round 41) supplies the syntax tree the tool walks.

## The three live misreads (v3) and what v4 does

| site | v3 | why | v4 |
|---|---|---|---|
| `tools/context-capture.py:1682`, `:1685` | `unflagged=1` | the base is `self.case_dir(name)`; v3 cannot see that `case_dir` returns `os.path.join(self.root, …)` or that `self.root = tempfile.mkdtemp(…, dir="/tmp")` (`:1624`, `:1631-1635`) | `scratch=1`, `unflagged=0`; resolved text carries `mkdtemp` |
| `tools/registry-replay.py:123` | `unflagged=1` | `out` is a parameter of `publish`; both in-module calls pass `out = Path(args.out)` (`:181`, `:185`) or `Path(a.out)` (`:282`), and `--out` is declared at `:259` | `explicit_out=1`, `unflagged=0`; resolved text ends `argparse --out` |

v4 (`tools/write-path-census-v4.py`) adds three bounded steps to v3's walk:

1. **Attribute binding.** Every `self.<attr> = <expr>` in any method of the enclosing
   class is collected. An attribute with exactly one distinct plain assignment resolves to
   it. Two or more distinct expressions, or any augmented assignment, leave it unresolved,
   so it is never read as scratch — for the plain-assignment shapes the collector sees.
   Tuple targets, starred targets, `for self.x in …`, `with … as self.x`, walrus and
   `setattr(self, …)` are not collected, so a second binding through any of those shapes
   does not make the attribute ambiguous.
2. **Method-return fold.** `self.<m>(…)` for a same-class method with exactly one
   top-level `return <expr>` resolves to that expression, evaluated in the method's own
   top-level assignments. Nested returns are ignored, so a method whose reachable branch
   returns a golden path but also carries a top-level `return` of a scratch path is folded
   to the scratch path.
3. **Output-flag trace.** For `--out`, `--output`, `--out-dir` and `--output-dir`, the
   dest is derived as S157 states, or taken from `dest=`. A destination is `explicit_out`
   when its root resolves to `<ns>.<dest>` with `<ns>` bound to a `parse_args(...)` result.
   It is also `explicit_out` when its root is a parameter of a module-level function and
   every in-module call passes, at that position, an expression that does. A single
   call with any other argument (a constant, an `--input` value) keeps the site unflagged.
   `default=`, `const=` and `set_defaults()` values are **not** checked: an option with a
   default still labels the destination `explicit_out` although the write then lands in the
   default path without the operator naming it.

Resolution depth rises from four to eight hops: the context-capture chain needs six.
`--json` prints every write site with `explicit_out` beside v3's fields; text mode keeps
v3's per-site line format (without v3's totals line).

## The kill oracle used to test it

The round-42 counter (`.ufo/evidence/round-42/census/measure.py`) mutates v4 and runs a
ten-fixture battery plus the three live sites out of process. A mutant is `killed` only
when every run completes with parseable output and at least one case differs from its
declared classification. A crash, a Traceback or unparseable output is `runtime_error`,
and a run with no differing case is `survived`. This matches the lane's own verdict rule:
a crash before the summary is Inconclusive, not a kill (`SKILL.md:208-209`). It also
matches Stryker, whose Runtime error state "is not represented in your mutation score"
(S001, snapshot line 26, 8 words). PIT scores the same class as detected (S158,
`RUN_ERROR(true)`, line 63), so the oracle follows Stryker and the lane, not PIT.
`corpus/knowledge/pit-outcome-vocabulary.md` records that divergence. The counter's own
docstring cites PIT and Stryker together for this rule; that citation is half wrong and
is corrected in the round-42 contract's post-freeze amendments (the counter bytes are
pinned and are not edited).

## What is not claimed

- Not a dataflow analyser. The bounded steps above are not sound: the wave-2 attack seats
  found v4 clearing repo-landing expected-value writes as `scratch`/`explicit_out` in 23
  constructed shapes (CriticV4Wrong) and more in the reviewer's and critics' probes
  (ReviewV4Entry, ReviewV4Source, CriticSourced, MutProbeMethod). Known false-negative
  classes (each hides a real expected-value write):
  - parameter shadowing: a function parameter does not shadow a module-level binding, so
    `def emit(ns): … ns.out …` after a module-level `ns = ap.parse_args()` borrows the
    global namespace;
  - nested functions and loops: `_bind` does not bind `for` targets or nested-function
    parameters, so a loop or inner function that assigns a golden path inside a flagged
    function still reads as explicit;
  - starred-argument misalignment: `emit(*pair, ns.out)` shifts positions, so the wrong
    parameter is traced;
  - non-plain attribute rebinds: tuple/starred targets, `setattr(self, …)`, class-body
    assignments, subclass rebinding and template-method overrides evade the ambiguity rule
    and read as scratch;
  - `default=` / `set_defaults` on an output option (label `explicit_out` although the
    operator never named the destination);
  - calls through variables, `functools.partial`, `getattr`, dicts, sub-parsers sharing a
    dest, and `os.path.join` with an absolute later component;
  - the whole-resolved-text substring test: `/tmp` inside `tmpl` or an identifier such as
    `scratch_root` flips `scratch`;
  - two-destination writes (`os.replace` over two `--out` paths) never count as
    `explicit_out`.
- `flagged` stays file-global, as in v3: an update-flag string anywhere in the file
  marks every site flagged, and a short `--update` option flags the whole file.
- `explicit_out` says the operator *can* name the destination; because of the `default=`
  gap it does not prove the write lands where the operator chose.
- The counter's frozen battery cannot tell a resolver from a tool that special-cases the
  battery's names and line numbers. The wave-1 critic built one (a v3 copy with literal
  tables) that passes every fixture and live check. The round-42 records carry the
  renamed-identifier falsifier that separates the two (`corpus/lessons/round-42.md`).
- No new open write path is claimed in this lane's tools; with v4 the lane's tracked
  `tools/` Python files (26) census 0 unflagged sites, and that count is the only live
  claim the frozen counter makes.

## Adjacency

A wave-1 connector scan of the sibling lanes found no tool that resolves `self.<attr>`
or argparse output destinations in a write census
(`.ufo/waves/round-42/w1/ConnectorSibling.md`). The round-41 prior art (kotodama's
assignment-folding tools) stays cited, not absorbed.
