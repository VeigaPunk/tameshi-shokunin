# T47ExecDeadCode — dead-code debt list for `tools/` (considerthese 2026-10-25, idea 3)

Seat: leaf executor. Item: mine idea 3 of `considerthese/2026-10-25.md` — keep a list of unreachable code
in `tools/` so it is deleted instead of permanently absorbed by the round-43 classification rule.

Scope respected: read-only on the lane. Two writes only — the scanner
`.ufo/waves/round-47/w1/T47ExecDeadCode.scan.py` and this report. No edit to `tools/`, no git/jj mutation,
no counter run, no tool installed (nothing needed; `ast` + stdlib only, pacman paused and unused).
Scratch: `/tmp/tameshi-r47-T47ExecDeadCode/`.

Deliverable: `.ufo/waves/round-47/w1/T47ExecDeadCode.scan.py` — stdlib `ast`, 315 lines,
sha256 `64826c3d2e4f3b68fdd280e2486e9b44569bad27ac6858cef3cc096e6cc35353`.
Exit code: `0` clean, `1` findings present, `2` missing root. It is a debt list, not a verdict instrument.

## Command and result on the lane tree

Run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`:

```
python3 .ufo/waves/round-47/w1/T47ExecDeadCode.scan.py
```

```
[after-terminator] 0 finding(s)

[constant-test] 0 finding(s)

[unreferenced] 2 finding(s)
  tools/tally-audit-v2.py:135   def brace_depth_at(text, offset):  # function never referenced in-file, never imported
  tools/tally-audit-v3.py:234   def brace_depth_at(text, offset):  # function never referenced in-file, never imported

scanned_files=51 findings=2 after-terminator=0 constant-test=0 unreferenced=2 parse_errors=0
caveats: non-docstring name strings and explicit imports count as references, so CLI argv dispatch and selftest helpers are not reported; a whole-module import of a scanned file keeps its top-level functions live.
```

Exit `1` (findings present). Roots cover `tools/` (27 files) and `.ufo/evidence/round-44..47` (1 + 4 + 13 + 6),
51 files total, 0 parse errors.

Counts per class:

| class | findings | files hit |
|---|---|---|
| after-terminator | 0 | — |
| constant-test | 0 | — |
| unreferenced | 2 | `tools/tally-audit-v2.py`, `tools/tally-audit-v3.py` |

## Debt list (the two standing items)

| # | file:line | class | excerpt | verdict |
|---|---|---|---|---|
| 1 | `tools/tally-audit-v2.py:135-143` | unreferenced | `def brace_depth_at(text, offset):` | dead helper; safe to delete |
| 2 | `tools/tally-audit-v3.py:234-242` | unreferenced | `def brace_depth_at(text, offset):` | dead helper; same body, duplicated |

Verified not referenced anywhere in the lane, not only by the scanner:

```
$ grep -rn "brace_depth_at" --include='*' . | grep -v __pycache__ | grep -v '^./.git/'
./tools/tally-audit-v2.py:135:def brace_depth_at(text, offset):
./tools/tally-audit-v3.py:234:def brace_depth_at(text, offset):
./.ufo/waves/round-35/w2/AttackPerIndexParse.md:58   (report prose, not code)
... (round-35 wave prose only)
```

Only the two `def` lines in code; every other hit is a round-35 wave report *about* this function. No
`getattr`/`globals()`/string dispatch path exists in either tool (`grep` for the name finds nothing else).

This is exactly the debt idea 3 predicts, and it is older than round 47: round 35 already filed it as
HYGIENE-1 — "`brace_depth_at()` is dead code" (`.ufo/waves/round-35/w2/AttackPerIndexParse.md:58,260`,
`.ufo/waves/round-35/w2/ConnectorCommentBlind.md:125,162`, `.ufo/waves/round-35/w2/ScoutTailRegion.md:42,123`).
Twelve rounds later it is still standing, and it now exists twice (v2 `:135`, v3 `:234`, v3 having shifted
from the `:215-224` span the round-35 seat cited) because the v3 rewrite copied the dead helper along with the
live ones. That is the growth mode the idea asks to flag: the classification rule absorbs it, the tool copies
it, nobody deletes it.

## How the scanner would FAIL — planted cases (non-vacuity)

A scanner never shown to flag a planted case is vacuous. Fixture
`/tmp/tameshi-r47-T47ExecDeadCode/fixture/` holds one example of each class plus live controls
(a function called in-file, a function reachable only via a string dispatch table, a function imported by
another file):

```
python3 .ufo/waves/round-47/w1/T47ExecDeadCode.scan.py /tmp/tameshi-r47-T47ExecDeadCode/fixture
```

```
[after-terminator] 4 finding(s)
  fixture/planted.py  :6     print('AFTER_RETURN_DEAD')  # unreachable after return at line 5
  fixture/planted.py  :11    print('AFTER_RAISE_DEAD')  # unreachable after raise at line 10
  fixture/planted.py  :18    print('AFTER_CONTINUE_DEAD')  # unreachable after continue at line 17
  fixture/planted.py  :25    print('AFTER_BREAK_DEAD')  # unreachable after break at line 24

[constant-test] 3 finding(s)
  fixture/planted.py  :29    if False:  # if guarded by a constant-false test
  fixture/planted.py  :31    if 0:  # if guarded by a constant-false test
  fixture/planted.py  :33    while False:  # while guarded by a constant-false test

[unreferenced] 6 finding(s)
  fixture/importing.py:4     def wrapper():  # function never referenced in-file, never imported
  fixture/planted.py  :9     def after_raise():  # function never referenced in-file, never imported
  fixture/planted.py  :14    def after_continue(items):  # function never referenced in-file, never imported
  fixture/planted.py  :22    def after_break(items):  # function never referenced in-file, never imported
  fixture/planted.py  :28    def constant_if():  # function never referenced in-file, never imported
  fixture/planted.py  :37    def never_called():  # function never referenced in-file, never imported

scanned_files=3 findings=13 after-terminator=4 constant-test=3 unreferenced=6 parse_errors=0
```

Live controls behaved: `after_return`, `live_caller`, `cmd_alpha` (`COMMANDS = {'alpha': 'cmd_alpha'}` — a
name string), `shared` (imported by `importing.py` via `from control import shared`) and `uses_shared` were
all *not* listed. One false-positive shape is visible in the fixture output: `importing.py:wrapper` is flagged
because that fixture file never calls it — correct per the class definition (in-file references + imports), and
exactly why the class is labelled advisory.

Block coverage was proved separately, because the class-1 rule is only as good as the block walker. Fixture
`/tmp/tameshi-r47-T47ExecDeadCode/blocks/blocks.py` puts a terminator-then-statement into an `async for` body,
an `except` handler, a `finally`, a `try … else`, a `match` case, a class method body and a `with` body, plus
`elif False`:

```
[after-terminator] 7 finding(s)
  blocks/blocks.py:9     print('AFTER_ASYNC_BREAK_DEAD')  # unreachable after break at line 8
  blocks/blocks.py:17    print('AFTER_HANDLER_RAISE_DEAD')  # unreachable after raise at line 16
  blocks/blocks.py:25    print('AFTER_FINALLY_RETURN_DEAD')  # unreachable after return at line 24
  blocks/blocks.py:35    print('AFTER_TRY_ELSE_RAISE_DEAD')  # unreachable after raise at line 34
  blocks/blocks.py:42    print('AFTER_MATCH_CASE_RETURN_DEAD')  # unreachable after return at line 41
  blocks/blocks.py:50    print('AFTER_CLASS_METHOD_RETURN_DEAD')  # unreachable after return at line 49
  blocks/blocks.py:63    print('AFTER_WITH_RETURN_DEAD')  # unreachable after return at line 62

[constant-test] 1 finding(s)
  blocks/blocks.py:56    elif False:  # if guarded by a constant-false test
```

(An earlier revision reported the handler and match-case rows twice — `ExceptHandler.body`/`match_case.body`
were yielded both from the parent and from the node itself. The duplicate was removed and re-proved by this
fixture; 7 distinct sites, not 9.)

Real-data non-vacuity: scanning every evidence round (`... .ufo/evidence`, 150 files — outside the declared
roots, ad-hoc only) reproduces dead code that human seats had already named, at their exact lines:

```
[unreferenced] 4 finding(s)
  .ufo/evidence/round-12/BytesReview/probe.py:51    def naive_bash(a, b):
  .ufo/evidence/round-33/c2/c2-measure.py    :43    def parse_row(line):
  .ufo/evidence/round-35/c1/c1-measure.py    :266   def load_copies(directory):
  .ufo/evidence/round-36/c1/c1-measure-v2.py :283   def load_copies(directory):
scanned_files=150 findings=4 after-terminator=0 constant-test=0 unreferenced=4 parse_errors=0
```

`load_copies` at `round-35/c1/c1-measure.py:266` is the identical file:line a round-36 seat recorded as
"dead code" (`.ufo/waves/round-36/w2/W2RevengerV1Docstring.md:58`). So the scanner's positive class fires on
independently adjudicated real dead code, not only on my synthetic corpus.

## The one known case named by the 2026-10-25 file — found, with a location correction

Idea 3 cites round 43's `dead_code_only` survivor as "a second return after an unconditional return in the F12
fixture path of `tools/write-path-census-v3.py`". Extracted programmatically from the round-43 counter's
`FIXTURES['F12_method_two_returns']` (`ast` read of
`.ufo/evidence/round-43/mutants/measure.py:236-243`) into
`/tmp/tameshi-r47-T47ExecDeadCode/known/F12_method_two_returns.py`, the scanner finds it:

```
[after-terminator] 1 finding(s)
  /tmp/tameshi-r47-T47ExecDeadCode/known/F12_method_two_returns.py:8     return os.path.join('golden', 'expected.json')  # unreachable after return at line 7
scanned_files=1 findings=2 after-terminator=1 constant-test=0 unreferenced=1 parse_errors=0
```

(the second row there, `def run(self)` unreferenced, is correct for a 13-line fixture with no caller).

Correction worth recording before anyone acts on the debt list: **that second `return` is not code in
`tools/write-path-census-v3.py`.** It is a string constant inside round-43's counter, written to a scratch
directory at measurement time and used as *input* to the tool. An independent AST check of the tool:

```
python3 - <<'EOF'  # walk every ordered block of tools/write-path-census-v3.py, report terminator-then-statement
[...]
EOF
→ (no output)
```

and a whole-tree grep finds the fixture body only in `.ufo/evidence/round-43/mutants/measure.py`. Consequences:
`tools/write-path-census-v3.py` has zero class-1 debt, and the round-43 `dead_code_only` label was a property
of the *fixture*, not of the tool. Nothing in `tools/` should be deleted in the name of that survivor; the
mutable thing the label protects is the classification rule's wording, which is not this seat's item.

A committed scan root cannot see the fixture either (it is a string, and round 43 is outside the declared
roots); extracting the string was the only way to cross-check it, which is why the extraction is shown above
rather than a scan of the round-43 tree.

## False-positive audit of the two real findings

- `brace_depth_at` in v2/v3: name appears only at its `def` in code, never as `Name`, `Attribute`, string
  token, or import in any scanned file; repo-wide grep confirms. The body is self-contained arithmetic over
  `text[:offset]` with no callers, so deletion cannot change behaviour.
- No other class-3 hit exists, so no audit is needed for the rest.
- Classes 1 and 2 are empty in the real tree. Corroborated independently by a plain-regex pass over the same
  roots for `(return|raise|continue|break)` followed by a more-indented statement on the next line and for
  `if|while (False|0):` — zero hits, matching the scanner.

## Measured masking (why the empty classes are not an artefact of the reference rule)

Class 3 deliberately errs toward under-reporting; each masking channel was measured, not assumed:

1. **Docstring prose.** String tokens count as references only outside docstrings (otherwise the word "run" in
   a docstring would mask `def run`). Removing docstrings from the token set added **0** findings over the 51
   in-scope files — the exclusion changes no verdict here.
2. **Whole-module imports.** Exactly one pair of scanned files is linked by `import X`:
   `.ufo/evidence/round-45/control/run-controls.py` does `sys.path.insert(...); import measure as m1` against
   `.ufo/evidence/round-47/calibration/measure.py`. Re-scanning `round-47/calibration` alone (which removes the
   masking) still yields `unreferenced=0`, so no dead function is hidden behind it.
3. **Explicit from-imports between scanned files: 0**, so no name is kept alive by a cross-file import.
4. **Dunder methods and decorator-registered handlers** are treated as live by construction (the interpreter
   and the decorator reference them, not a name). This is a known blind spot, by design.
5. **CLI/selftest name strings** (`COMMANDS = {'alpha': 'cmd_alpha'}`, argv dispatch tables) are treated as
   references; without that, every argv helper would be reported dead. The planted fixture proves the rule
   both ways (`cmd_alpha` suppressed, `never_called` reported).

## Adjacent standing dead weight, outside the three requested classes (measured, not scanned)

The round-45 simplification seat proposed six deletions in the round-45 counters and applied none (frozen
provenance). Checked at the freeze commit, four of them are still present verbatim:

```
.ufo/evidence/round-45/coverage/measure.py:23:import json          # unused import
.ufo/evidence/round-45/coverage/measure.py:145:    results = []    # assigned, never used
.ufo/evidence/round-45/coverage/measure.py:30:sys.dont_write_bytecode = True   # no-op
.ufo/evidence/round-45/freshness/measure.py:55:sys.dont_write_bytecode = True   # no-op
```

The scanner intentionally does not count these — unused imports, dead bindings and no-op assignments are dead
*weight*, not unreachable statements — but they belong on the same debt list, and the round-45 report is the
existing record of them (`.ufo/waves/round-45/w2/SimplCounters.md`, D1–D4). Their relevance to idea 3: the
round-45 proposal was routed to round 46 and closed without deletion, which is the same absorption failure as
`brace_depth_at` surviving round 35.

## Limits of the delivered list

- The class-3 predicate is syntactic. A function reached only via `importlib`, `runpy`, a subprocess
  `python tools/x.py --flag`, an entry-point table in `setup`/`pyproject`, or a decorator registration is kept
  live only if a non-docstring string or import names it. Deleting any reported item still wants the one-line
  grep shown above; both current items pass it.
- Class 1 follows the literal rule "statement after an unconditional terminator in the same block". It does
  not model `while True:` bodies (no `break` is unreachable if the loop never ends, but a `return`-then-code
  shape there is still reported correctly), nor dead code made unreachable by a constant condition — that is
  class 2 only for `False`/`0`/`not True`, not for general constant folding (`if 1 == 2:` is not flagged).
- The default roots are the five declared paths. Round-43-era fixture strings and pre-round-44 evidence are
  visible only via an explicit root argument, as the ad-hoc runs above show.
- Findings are advisory rows, never a gate on the lane: the scanner exits `1` when it finds anything, so a
  future CI use would need the count, not the exit code.

## Files changed by this seat

- `.ufo/waves/round-47/w1/T47ExecDeadCode.scan.py` — new scanner (deliverable).
- `.ufo/waves/round-47/w1/T47ExecDeadCode.md` — this report.

Nothing else in the lane was written; `tools/` was not touched, and `brace_depth_at` is left in place for the
owner of a tools-change round to delete (both copies) together with the round-45 dead weight above.
