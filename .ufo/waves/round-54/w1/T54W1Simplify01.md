# T54W1Simplify01 — the four copies of `ScratchRootUnusable`

**Verdict: the duplication is warranted. Keep the four copies; do not create a shared
`tools/scratch_root.py`.**

The premise "a five-line class and a three-line mapping" overstates what is there: the class is
**two code lines** (a `class` line and its one-line docstring), inserted as a four-line block with its
two PEP-8 blank lines — the C0 hunk reads `+5` only because it also carries the helper's new docstring
sentence — and the mapping is three lines that no two tools can share because each carries its own
prefix, stream and exit constant. What is genuinely duplicated across the seven tools is the
12–13-line `strict_scratch_root()` helper, 88 lines in total — and that duplication cannot be removed
without breaking the property that makes the tools runnable as copies. So the class is not the
abstraction to attack; it is the smallest correct unit of a pattern whose larger unit is load-bearing.

Nothing in the lane was edited. Every mutation below happened in `git clone --shared` copies under
`/fast/scratch/hyaku/tameshi-r54/T54W1Simplify01/` (removed at the end of the seat). Receipts:
`.ufo/waves/round-54/w1/T54W1Simplify01-receipts/` (`measure.sh`, `measure.out`, `fix1/`, `fix2/`).

---

## 1. What is actually duplicated (measured, not counted by eye)

`measure.out` §2 extracts every `strict_scratch_root` body and every `ScratchRootUnusable` class and
call site by AST at the lane tip.

| unit | copies | size | identical? |
|---|---|---|---|
| `strict_scratch_root()` helper | 7 | 12 lines (×3) or 13 lines (×4) = **88 lines** | **2 distinct bodies**: `sha 80194a6dde3ff6bd` (context-capture, registry-check, repeat-control) and `sha b161cc8238791e59` (env-diff, evidence-disposition, pin-disposition, bash-witness-study) |
| `class ScratchRootUnusable(RuntimeError)` | 4 | 2 code lines each = **8 lines** | byte-identical, docstring included |
| `except ScratchRootUnusable` arm | 4 at C0, **5 at the tip** | 3 lines each = 15 lines | bodies differ; env-diff's two arms are **byte-identical** |

The whole difference between the two helper variants is one docstring sentence and one token:

```
-    fallback to /tmp, preserving CR47 semantics), else the platform default."""
+    fallback to /tmp, preserving CR47 semantics), else the platform default.
+    An empty TMPDIR is unset (round 54, corpus/knowledge/scratch-root-contract.md)."""
...
-            raise RuntimeError(
+            raise ScratchRootUnusable(
```

Every file has **exactly one** raiser (AST, `measure.out` §2/§7): the raise lives inside
`strict_scratch_root` and nowhere else. So each arm's catch set is exactly one call — that is the
property that makes the class a *type token* rather than decoration, and the property a bare
`RuntimeError` cannot preserve.

Arm texts, which is why the arm cannot be shared:

| file | arm prints | exit |
|---|---|---|
| env-diff.py:234 and :263 | `ENVDIFF_SETUP: could-not-evaluate: %s` → stderr | `2` |
| evidence-disposition.py:3231 | `evidence-disposition.py: could-not-evaluate: {}` → stderr | `2` |
| pin-disposition.py:1399 | `pin-disposition.py: could-not-evaluate: {}` → stderr | `2` |
| bash-witness-study.py:1788 | `WITNESS_STUDY: could-not-evaluate: {exc}` → stderr | `EXIT_CANNOT` |

Four prefixes, two stream APIs, two exit constants: a shared arm would need all four threaded
through a helper to replace fifteen lines with five one-line calls — more code, and a new import in
every file (§2).

## 2. Why one helper is the wrong answer — grounded in how the tools are invoked

The seven selftest rows in `tools/registry.json` all invoke a path, never a module:

```
['python3', 'tools/env-diff.py', '--selftest']        ['python3', 'tools/context-capture.py', '--selftest']
['python3', 'tools/registry-check.py', '--selftest']  ['python3', 'tools/repeat-control.py', '--selftest']
['python3', 'tools/evidence-disposition.py', '--selftest']  ['python3', 'tools/pin-disposition.py', '--selftest']
['python3', 'tools/bash-witness-study.py', 'selftest']
```

That makes `sys.path[0]` the tools directory, so a sibling import *would* resolve in a whole-directory
copy. It fails everywhere else, and the lane uses everywhere else:

1. **There is no shared-module precedent to follow.** AST over all 29 `tools/*.py`: **zero** local or
   relative imports (`measure.out` §3). Every tool is one file plus the standard library. A
   `tools/scratch_root.py` would be the first, and the first thing a copy can silently lose.
2. **Subset copies are the demonstrated practice.** Round-17 staged `3` of `33` `tools/` entries and
   round-18 staged `4` of `33` (`measure.out` §3). Reproduction `fix1/`: a file that imports a
   sibling, copied alone, dies at import —
   ```
   Traceback (most recent call last):
     File ".../fix1/subset/consumer.py", line 2, in <module>
       from scratch_root import ScratchRootUnusable
   ModuleNotFoundError: No module named 'scratch_root'
   rc=1
   ```
   That is exit 1 with a traceback: precisely the defect (R53.6) round 54 exists to remove, reintroduced
   by the deduplication that was supposed to be free.
3. **By-path loading resolves the import from the wrong revision.** `tools/registry-replay.py:163-166`
   loads `clone/tools/registry-check.py` with `importlib.util.spec_from_file_location(...)` +
   `exec_module`, and `spec_from_file_location` does **not** add the file's directory to `sys.path`;
   `sys.path[0]` stays the lane's live `tools/`. Reproduction `fix2/`: executing revision A's runner
   while `sys.path[0]` points at revision B prints
   ```
   runner saw helper: revB-helper
   ```
   A replay pinned at revision A would run revision B's helper and report nothing.
4. **The helper would escape every instrument hash.** Each of the four pins itself only:
   `report["instrument_sha256"] = digest(Path(__file__).read_bytes())` (env-diff.py:252),
   `tool_sha256()` over `SELF = os.path.realpath(__file__)` (evidence-disposition.py:136/230,
   pin-disposition.py:110/192), `"sha256": sha256_file(Path(__file__).resolve())`
   (bash-witness-study.py:811). A sibling module's bytes would be covered by none of them, and
   `registry-replay` hashes only the runner file it loads (`runner_sha` at :163).

Cost of the rejected option, for the record: one 13-line module plus seven one-line imports replaces
88 lines of helper, 8 lines of class and ~9 lines of arm — a net **≈85 lines deleted** out of
**11,955** lines across the seven tools (0.7%). That is the deletion "one helper" makes possible, and
it buys three measured breakages in §2.1–§2.4. Not kept.

## 3. Why not a bare `RuntimeError` in the four (the cheaper-looking deletion)

Measured A/B on one set-but-unusable `TMPDIR` (`measure.out` §1):

| tool | base `d33053f` (raise `RuntimeError`) | C0 `59c3810` (class + arm) |
|---|---|---|
| env-diff | rc=1, 18 lines, **traceback** | rc=2, 1 line |
| evidence-disposition | rc=1, 13 lines, **traceback** | rc=2, 1 line |
| pin-disposition | rc=1, 13 lines, **traceback** | rc=2, 1 line |
| bash-witness-study | rc=1, 14 lines, **traceback** | rc=2, 1 line |
| context-capture | rc=2, 1 line (generic `except Exception`) | unchanged |
| registry-check | rc=2, 1 line (generic `except RuntimeError`) | unchanged |
| repeat-control | rc=2, 2 lines (generic setup path) | unchanged |

So the class is not needed for *three* tools — they already reach exit 2 through a broad catch — and
it is exactly what the *four* needed. The question is only whether the four could catch
`RuntimeError` instead of the subclass. That deletes 8 lines and can be measured against a fabricated
interior bug (`measure.out` §5):

- typed arm, bug raised inside `selftest()` → `rc=1 traceback=1`, last line
  `RuntimeError: injected interior bug: jj status failed` — loud, and no claim about the environment;
- `except RuntimeError as exc`, same bug → `rc=2 traceback=0`, last line
  `evidence-disposition.py: could-not-evaluate: injected interior bug: jj status failed` — a
  **could-not-evaluate verdict about a TMPDIR that is perfectly usable**. The typed arm is the only
  thing that keeps that line from being printed.

The same ragged edge already exists where the class is absent: context-capture (one of the three)
under an injected crash prints `SELFTEST: FAIL (setup error: RuntimeError: injected interior bug:
fixture case crashed)` and exits **2**. A verdict word, from a tool that has no class. That is the
shape the four were right to avoid.

## 4. Why the existing per-file exit-2 types cannot absorb it (the "reuse, don't subclass" option)

Each of the four already has an exit-2 authority, but none of them fits, so `ScratchRootUnusable` is
not a second convention — it is the only member of its own:

- evidence-disposition's `CouldNotEvaluate.__init__(self, finding_id, detail)` needs a finding id and
  `emit_could_not_evaluate` serialises `{"id": exc.finding_id, "error": {"kind": ..., "message": ...}}`;
  raising it from the helper would demand an invented id and change the one-line shape to a JSON payload.
- bash-witness-study's `Cannot` prints `WITNESS_STUDY: CANNOT-EVALUATE (%s)`, so reusing it produces
  `WITNESS_STUDY: CANNOT-EVALUATE (cannot create clone scratch ... '/nonexistent/nope' (could-not-evaluate))`
  — nested parenthesis and a different prefix from the other six lines.
- pin-disposition's `InvalidInput` feeds a usage-code grammar (`invalid_input("invalid_usage", ...)`), a
  different register from an environmental refusal.
- env-diff has no could-not-evaluate type at all: its non-selftest catch is
  `except (OSError, ValueError, KeyError, TypeError)`, which the class deliberately sits outside.

The strongest deletion candidate the sweep found and the reason it is refused: **5 lines** — delete
bash-witness-study's class and arm and let the helper raise `Cannot` (`measure.out` §2 shows the
only raiser is the helper). It passes every C2 arm, but it breaks the one-line shape that the seven
`scratch_root` registry cells document
(`TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback)`): the
uniform prefix is the whole point of a *single declared class* across seven tools, and the cell text is
what the operability claim is written against. Refused: it improves the line count and harms the
uniform-shape axis that the seven cells declare.

## 5. Minimal change, and the deletion it makes possible

**Minimal change: none.** The class stays at 2 lines × 4 and the arm at 3 lines × its catch site;
both are the floor, and every route below the floor costs more than it saves:

| option | lines deleted | measured cost |
|---|---|---|
| one `tools/scratch_root.py` | ≈85 net | import breakage in subset copies (rc=1 + traceback), cross-revision mixing under `exec_module`, helper outside all instrument hashes |
| bare `RuntimeError` in the four | 8 | a false `could-not-evaluate` line for any interior bug (measured §3) |
| reuse `Cannot` in bash-witness-study | 5 | the uniform one-line shape that the seven registry cells document |
| extract a 2-statement `_scratch_root_exit(exc)` inside env-diff (its two arms are byte-identical) | 0 — a 5-line helper replaces six lines with two calls, so net **+1** | none; it renames three lines without removing one |
| move env-diff's selftest branch inside its outer `try` to drop the inner arm | **4** (272 → 268 lines; measured 273 → 269 with one injected line) | measured in `measure.out` §10: a genuine `ValueError` inside `selftest()` goes from `rc=1 traceback=1` to `rc=2` printing `ENVDIFF_SETUP: injected selftest ValueError` — the laundering harm of §3, in the opposite direction |

The minimal change that is *a deletion* is therefore the four-line arm merge in §10, and it is refused
on measured evidence: it turns a genuine `selftest()` failure into an `ENVDIFF_SETUP` line with
exit 2. The larger deletion the one-module option promises — ≈85 lines, §2 — is refused on three
measured breakages. So the recommendation is a NO-OP on both the class and the arms. The tools are 29
single-file programs run by path from `registry.json` argv, copied into wave staging that has taken
subsets (3/33 and 4/33), loaded by path by `registry-replay` and `shrink-case`, and self-hashed
per file; an 8-line type declaration is the cheapest possible way to keep one exit class across that,
and both of its lines are load-bearing: the type fixes the catch set, the docstring tells the next
reader what exit class the file intends.

## 6. Observations outside the deletion decision (each with a receipt, none acted on)

1. **env-diff's run path did leak the class at C0 — and is already fixed at the tip.** At
   `59c3810`, `strict_scratch_root` is reached from `execute()` on the run path (AST: line 80); the
   only other non-selftest allocation site among the seven is registry-check's `clone_lane_at_rev`
   (line 780), which maps it through its own `RuntimeError` path, so **env-diff was the sole
   class-bearer whose non-selftest site had no arm**. A set-but-unusable `TMPDIR` there produced
   `rc=1 traceback=1` ending
   `ScratchRootUnusable: cannot create clone scratch ... '/nonexistent/nope-r54' (could-not-evaluate)`
   (`measure.out` §7b). The lane moved while this seat ran; tip `99c3bc8` closed exactly that with a
   three-line arm (`git diff 59c38109bf11 99c3bc8 -- tools/env-diff.py`), and §9a at the tip now reads
   `rc=2 traceback=0 lines=1`. My earlier reading of the frozen commit stands; the defect is not open.
2. **The lane's own registry runner does not consume the class.** Under an unusable `TMPDIR`,
   `python3 tools/registry-check.py --root . --only env-diff-selftest` prints
   `ROW env-diff-selftest expect=0 got=2 differs` and exits 1 (`measure.out` §8a), because `run_row`
   sets `held = got == expected_exit` and has no exit-2 branch. The contract note says a set-but-unusable
   `TMPDIR` is "could-not-evaluate (2), never 1 (a verdict of "differs"/"failed")"
   (`corpus/knowledge/scratch-root-contract.md:36`). Two consumers, two answers: the C2 counter reads
   the tool's stderr and calls it conformant; the registry runner reads the exit code and calls it a
   discrepancy. Naming this is in scope for the *duplication* question because it is the only payoff
   the class has beyond the counter, and today it is unclaimed.
3. **The C2 counter's arm-1 predicate is a substring test**, so a line that opens with a verdict word
   still passes: context-capture at C0 prints `SELFTEST: FAIL (setup error: RuntimeError: cannot
   create clone scratch ...'/nonexistent/nope' (could-not-evaluate))` and is counted 7/7 conformant
   (`measure.out` §1, C0 half). The cell text for that row claims "could-not-evaluate" and the line does
   contain it, so the counter is not wrong — it is coarse, and it is coarse in exactly the place where
   the missing class (that tool is one of the three) shows.

## 7. Bounds and hygiene

- No lane file, counter, contract, freeze, ledger or wave spec was touched; `git status` in the lane
  shows only the pre-existing untracked `.ufo/` artifacts of other seats. `tools/registry.json` and all
  lane files were read only.
- Census re-run at the end of the seat: `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → `tameshi ok .../corpus/SOURCES.md`, exit 0
  (`measure.out` §6).
- Fixtures that write: `fix1/` (a `scratch_root.py` **fixture for the rejected option**, not lane code)
  and `fix2/`; both are copies inside this seat's receipts directory. Scratch tree
  `/fast/scratch/hyaku/tameshi-r54/T54W1Simplify01/` removed at the end of the seat; the fixtures
  that remain in the receipts tree are the only artifacts.
- Tooling: nothing installed, nothing upgraded (pacman transactions are paused host-wide and no
  `uv`/`npx`/binary was needed).
