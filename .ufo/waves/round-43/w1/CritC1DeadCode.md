# CritC1DeadCode — attack on the `method_fold_several_returns` dead-code judgment

Seat: L1Tameshi43.CritC1DeadCode (critic, depth). Item: try to construct a *reachable*
two-top-level-return input that makes pristine and mutant disagree; if none exists, state the
structural argument. Bounds honoured: lane read-only apart from `/tmp/tameshi-r43-CritC1DeadCode-w1`
and this report; no measurement run (only the allowed control `--probe-mutant` at the freeze rev);
no installs, no pacman.

## Verdict

**The `dead_code_only` classification stands. No reachable-input difference exists, and the
structural argument is a compile-time fact, not a convention:** the divergent branch requires
`len(returns) >= 2` over `method.body` direct children
(`tools/write-path-census-v4.py:138-139`), and a function-body statement list is executed
linearly, so any second top-level `Return` is preceded by a `Return` that already transferred
control. CPython does not even emit bytecode for the remainder of that block.

That is the *only* possible trigger, so the mutant's divergence set is exactly the set of inputs
whose folding method carries dead statements — which is what `D_dead_code_only` declares. The
classification is not merely survivable: it is provable. It is also **not** `equivalent`
(`E`): F12 does differ, so `dead_code_only=1, equivalent=0` is the right tally.

## Reproduction and identity (bytes)

```
$ git show 17f6ef0…:tools/write-path-census-v4.py > pristine.py
784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5  pristine.py
     # == contract.json frozen_tools["tools/write-path-census-v4.py"] and tool_sha256
$ # apply mutants.json entry verbatim; count(find)==1, count(replace)==0 for all six mutants
method_fold_several_returns 1 0
mutant sha b455639c2f7c7ddb53546d52a916a0863601e417c1693e698f4e54349d8979d5 (len 25983, base 25984)
$ diff pristine.py mutant.py
10c10
<         if len(returns) != 1:
---
>         if len(returns) < 1:
```

Only the `returns >= 2` case changes (0 returns: both bail; 1 return: both fold identically).

## Evidence 1 — 17 constructed inputs, pristine vs mutant JSON

Harness (`harness.py`) mirrors the tool's own count
(`[s for s in method.body if isinstance(s, ast.Return) and s.value is not None]`) and copies the
counter's `unreachable_statements()` verbatim. Each row: tool-level top-level returns per method,
the counter's dead-block detector, then `--json` fingerprint comparison.

Reachable-shaped idioms (every way a fixture author writes "two returns, both reachable"):

| candidate | top-level returns | dead blocks | JSON |
|---|---|---|---|
| A01 if/else returns | `destination [11]` | `[]` | same |
| A02 if/elif/else returns | `[]` | `[]` | same |
| A03 try/finally + tail return | `destination [10]` | `[]` | same |
| A04 try/except/else/finally | `[]` | `[]` | same |
| A05 for/while returns + tail | `destination [10]` | `[]` | same |
| A06 with-return + tail | `destination [8]` | `[]` | same |
| A07 match/case returns | `[]` | `[]` | same |
| A08 nested def, dead return inside it | `destination [11]`, `inner [9,10]` | `['module.body[1].body[0].body[0][1]']` | same |
| A09 raise-guard then return | `destination [8]` | `[]` | same |
| A10 conditional early return | `destination [8]` | `[]` | same |
| C01 single top-level return (control) | `destination [6]` | `[]` | same |
| C02 `while True:` + tail return | `destination [8]` | `[]` (detector misses it) | same |

Dead-shaped variants (all differing; each carries the trigger block):

| candidate | top-level returns | dead blocks | JSON |
|---|---|---|---|
| B01 `return a; return b` one-liner | `destination [6, 6]` | `['module.body[1].body[0][0]']` | **DIFF** |
| B02 F12 clone | `destination [7, 8]` | same | **DIFF** |
| B03 `raise` then two returns | `destination [7, 8]` | same | **DIFF** |
| B04 `return a` then `if True: return b` | `destination [6]` | `['module.body[1].body[0][0]']` | same |
| B05 conditional + two top-level | `destination [8, 9]` | same | **DIFF** |
| B06 async method, two returns | `destination [6, 7]` | same | **DIFF** |
| B07 raise, assign, two returns | `destination [8, 9]` | same | **DIFF** |

```
violations (>=2 top-level returns but no dead block): 0
diff cases: B01,B02,B03,B05,B06,B07
diff cases with empty dead_blocks: []
```

B04 is the sharp negative control: a file *with* an unreachable statement after a `return` whose
return sits nesting-deep (`if`) has count 1 and does **not** differ. Divergence tracks the
top-level count, not the presence of dead code — so the mutant's behavioural surface is exactly
the top-level-multi-return block, i.e. exactly the dead block.

## Evidence 2 — the structural argument

Let `B = [s_0 … s_{n-1}]` be a `FunctionDef.body` list (what line 138 iterates). Python executes
`B` as an ordered sequence; reaching `s_j` implies every `s_i` (`i < j`) was executed in order.
Executing a `Return` transfers control out of the frame. No statement form in a flat body list can
skip a statement and resume at a later one: `if`/`match`/`for`/`while`/`try`/`with` are all
compound nodes, so a `return` under any of them is not in `B` (it is in that node's own `body`,
`orelse`, `handlers` or `finalbody`). Hence for consecutive `Return` nodes at indices `i < j` in
`B`, `s_j` is unreachable for every input — `len(returns) >= 2` implies a statement after an
unconditional `return` in the same block, which is exactly `D`'s predicate.

Corollary that also closes the counter's `unreachable_statements()` "same block" wording gap
(`measure.py:377`, file-scoped): any differing input necessarily has ≥2 top-level returns in the
folding method's body list, so the detector's hit necessarily lies **in the trigger's own block**.
The implementation is file-scoped but provably cannot mislabel *this* mutant. And B04 shows the
marker alone is insufficient (dead code with no divergence → same JSON), so the label is applied
only to genuine differentials.

## Evidence 3 — compiler and runtime proof, not just syntax

```
lines executed in destination() over 3 calls: [4, 5]
dead return line (6) executed: False

--- dis of a 2-top-level-return body ---
  2  LOAD_SMALL_INT 1 / STORE_FAST first
  3  LOAD_FAST_BORROW first / RETURN_VALUE
jump targets: set()
instructions: RESUME, LOAD_SMALL_INT, STORE_FAST, LOAD_FAST_BORROW, RETURN_VALUE
```

The second `return` is not merely skipped at runtime — CPython emits **no instructions at all**
for statements after a top-level `RETURN_VALUE`, and there is no jump target into them. There is
no bytecode-level back door (no `goto`, no jump table) that a source fixture could use.

## Evidence 4 — the counter's fixture-only differential misses nothing live

`differential()` (`measure.py:448`) iterates only `FIXTURES`; the K oracle battery covers the three
`LIVE` sites but the differential never inspects the 26/27 `tools/*.py` files. I closed that gap
myself at both permitted revs:

```
== rev 487b8f0d tool files 26
   files with 2+ top-level returns or any diff: 0
== rev 17f6ef0c tool files 27
   files with 2+ top-level returns or any diff: 0
```

No live file has a method with ≥2 top-level returns, and pristine vs mutant JSON is identical on
every one. So no live-site differential is being hidden.

## Evidence 5 — declared fixtures under the counter's own detector, and the allowed control

```
F12 unreachable_statements: ['module.body[1].body[0][1]']     # fires, in the trigger block
F11 unreachable_statements: []                                 # kill fixture is reachable
F12 top-level return lines: destination [7, 8]
$ measure.py --rev 17f6ef0… --freeze 17f6ef0… --probe-mutant /tmp/…/mutant.py
C1_R43_PROBE: verdict=killed failures=1 errors=0 first=['F12_method_two_returns expected=1 want 0']
```

F12 differential (pristine → mutant), the whole mechanism visible in one line:

```
pristine: {"expected": false, "unflagged": false, "resolved": "self.destination()", ...}
mutant:   {"expected": true,  "unflagged": true,
           "resolved": "os.path.join('tmp', 'expected.json')tmp'tmp'expected.json'expected.json'", ...}
```

So the mutant is behaviourally live (two classification bits flip) — the classification is
`dead_code_only`, not `equivalent` — and the flip is caused solely by folding `returns[0]` of a
method whose second top-level `return` the compiler deletes.

## Findings

1. **No defect in the judgment.** `dead_code_only` is correct for
   `method_fold_several_returns`, and it is *structurally* forced, not merely the best of the
   fixtures tried: `>=2` top-level returns ⇒ a deleted statement in the same block.
2. **Coverage note (non-blocking, do not edit the frozen tool this round):** the tool's own
   selftest has no case that reaches the guard. `tools/write-path-census-v4.py:510`
   (`method_two_returns`) is an `if fast: return …` + tail `return`, i.e. count 1 — the guard is
   not exercised. Both tools pass `--selftest`: `cases=15 failed=0` for pristine *and* for the
   mutant. The guard's only coverage is F12, external to the tool. Smallest safe correction, when
   the tool may be touched again: add one selftest case with two top-level `return`s, or rename
   `method_two_returns` so it does not claim coverage it lacks. No action this round.
3. **`D`'s "same block" wording vs the file-scoped detector** is a latent gap in general but
   provably inert for this mutant (Evidence 2 corollary) — no correction required.
4. **`unreachable_statements()` under-detects** control-flow-unreachable tails (C02:
   `while True:` + tail `return` is unreachable but the detector returns `[]`). Direction is
   conservative (labels a case `reachable`) and cannot bite here because C02's count is 1, so it
   never differs.

## Impacted axes

- **depth** — the survivor-resolution rule survives the strongest reachable counterexample
  attempt; `kill_fixture_reachable=1` / `dead_arg_ok=1` are the defensible readings.
- calibration / operability — untouched by this seat.

## Worktree state observed during this seat (not mine, not a C1 finding)

Nothing in this seat wrote outside `/tmp/tameshi-r43-CritC1DeadCode-w1` (now deleted) and this
report. While the seat ran, other seats' writes appeared in the lane worktree:

```
$ sha256sum tools/write-path-census-v4.py tools/staged-id-guard.py
784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5  tools/write-path-census-v4.py   # == freeze
efa5f129cba312c26c1fc453e6cd7f783efafeecccfac791e8c03d3d290f9b3c  tools/staged-id-guard.py        # != freeze 8140945a…
 M .ufo/evidence/round-43/calibration/measure.py
 M LOG.md  M SCORECARD.md  M corpus/QUALITY.md  M corpus/README.md  M corpus/SOURCES.md
```

C1 is insulated: every C1 read (`tool_raw`, `muts_raw`, `contract_raw`, `self_raw`, staged
`tools/`) is `git show REV:path`, so uncommitted worktree edits do not enter the C1 battery —
my pristine copy taken from `17f6ef0…` still hashes to the frozen `784de4c0…`. Two live hazards
for other seats, flagged without investigating them: (a) the C2 counter reads its **running**
file (`measure.py` main: `running = sha(open(__file__))`) and zeros `self_pin` if it differs from
`counter_sha256` — a worktree edit of `calibration/measure.py` at measurement time would force
`C2_R43_PASS=false`; (b) `tools/staged-id-guard.py` in the worktree no longer matches
`frozen_tools`, which is C3's seat to reconcile before its deciding run.

## Commands run

- `git show 17f6ef0…:tools/write-path-census-v4.py` (hash check), mutant reconstruction from
  `.ufo/evidence/round-42/census/mutants.json`, `diff` (10c10).
- `python3 -I pristine.py --selftest` / `python3 -I mutant.py --selftest` → `cases=15 failed=0` both.
- `python3 harness.py` (17 candidates), `python3 livescan.py` (base + freeze tool corpus),
  `python3 proof.py` (settrace + `dis`).
- Control only: `python3 .ufo/evidence/round-43/mutants/measure.py --lane … --rev 17f6ef0… --freeze 17f6ef0… --probe-mutant /tmp/…/mutant.py`
  → `verdict=killed failures=1`. No measurement run was performed; the deciding run is L1's.
