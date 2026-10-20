# SpecUsage — exit-64 usage class: exact pair and hermetic fixture recipe

Seat: `TameshiR15.SpecUsage` (leaf, advisory). Scope: draft this report only.
No source edit, no gate/selftest execution, no sibling execution, no registry
edit. All claims below are read from committed bytes and are bounded to that
read; nothing here is an executed result.

Evidence read:

- `.ufo/evidence/round-14/capture-context.py`, 647 lines, SHA256
  `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`
  (historical bytes; this seat did not modify them).
- `.ufo/evidence/round-14/context-receipt.json`: retained `status=ok`,
  `exit=0`, `invocation.argv=[".ufo/evidence/round-14/capture-context.py"]`.
- `SKILL.md:1602` current registry row for this harness (0/1/2 only, no
  selftest; exit64 absent).
- `tools/evidence-disposition.py` existing selftest/usage convention
  (`UsageError` :147, `selftest` :1510, usage rows :1829-1836,
  `SELFTEST_CASE` :1521/:1524, `parse_argv` :1863, `--selftest takes no other
  arguments` :1913, `main` :1927, final `SELFTEST: PASS` :1856).

## 1. What the historical source actually supports

The exit map is explicit (`capture-context.py:26-29`):

> `64 usage error, no receipt.`

The 64 branch is `main` at lines 605-613:

```python
def main(argv):
    if argv:
        if len(argv) == 1 and argv[0] in ("-h", "--help"):
            sys.stdout.write(USAGE)
            return 0
        sys.stderr.write("capture-context.py: unexpected argument(s): {}\n".format(
            " ".join(argv)))
        sys.stderr.write(USAGE)
        return 64
```

`USAGE` begins `usage: capture-context.py` (`:117`) and its own last line is
`exit 0 equal; exit 1 mismatch; exit 2 could-not-evaluate; exit 64 usage.`
(`:123`).

Observed consequences, all from code order rather than execution:

1. Exit **64 is supported** and exact. The branch returns before
   `base_receipt()` (`:614`), before any input read and before
   `write_receipt()`; therefore **no receipt and no temp dotfile can be
   written on this path**. The docstring line and code agree.
2. The stable diagnostic token is literal:
   `unexpected argument(s): <argv joined with single spaces>`, written to
   **stderr**, immediately followed by the whole `USAGE` text (also stderr).
   Stdout is empty on this path.
3. The **only** non-64 argv accepted by the historical CLI is exactly one
   token, `-h` or `--help`; that path writes `USAGE` to **stdout** and returns
   **0**. Any other argv (including `--help` plus one more token) is 64.
4. A **zero-argument invocation is not usage**. It falls through to
   `receipt = base_receipt()` and the full capture (`:614+`). A fixture that
   invokes `[python3, TOOL]` and expects 64 would instead start a real capture
   and write a receipt. This is the single biggest trap when copying the
   sibling gate's usage rows (see §5.1).
5. This class has **no production finding ID** in the historical tool: 64
   emits no JSON, no `kind`, and no `reasons`. Only the stderr text and the
   exit code are observable. Do not invent a finding taxonomy for it.

## 2. Exact expected exit/finding pairs

Literal rows; `TOOL` is the maintained `tools/context-capture.py` (or a
byte-identical copy, §3). "Writes" means any filesystem write outside the
fixture tree.

| Selftest case (proposed literal label) | argv after `TOOL` | exit | stdout | stderr literal | writes |
|---|---|---:|---|---|---|
| `usage-unexpected-argument` | `--bogus-flag` | **64** | empty | contains `unexpected argument(s): --bogus-flag` and `usage: ` | none |
| `usage-unexpected-argument-echo` | `--bogus-flag extra` | **64** | empty | contains `unexpected argument(s): --bogus-flag extra` | none |
| `usage-help-plus-extra` | `--help --bogus` | **64** | empty | contains `unexpected argument(s): --help --bogus` | none |
| `usage-help` (boundary) | `--help` (and `-h`) | **0** | starts `usage: ` | empty | none |
| `usage-selftest-extra` (only if `--selftest` exists) | `--selftest --bogus` | **64** | empty | contains `unexpected argument(s): --selftest --bogus` | none |

Provenance of each row:

- Rows 1-4 are historical behavior (`:605-613`), including the multi-token
  join and the exactly-one-token help rule. Row 3 is the sharp discriminator
  for `len(argv) == 1`.
- Row 5 is **convention-derived, not historical**: `capture-context.py` has no
  `--selftest`; the sibling gate declares `--selftest takes no other
  arguments` and exits 64 (`tools/evidence-disposition.py:1913`, usage row
  `:1831`). Adopt it only because the promoted CLI must expose `--selftest`;
  if the promoted parser deliberately ignores trailing tokens after
  `--selftest`, drop the row rather than assert an unobserved behavior.

No row asserts a "finding ID", because none exists on this path. The literal
finding pair is `(exit=64, stderr contains "unexpected argument(s): <exact
argv echo>")`.

## 3. Isolated fixture recipe for the 64 class

Requirements met: actual public CLI subprocess, synthetic fixture only,
byte-identical tool copy, no live lane reads, no network, no writes outside a
temp root, literal expected exit and token.

### 3.1 Placement (containment is structural)

Create the fixture at:

```text
<tmp>/r/lane/tools/context-capture.py
```

with `tmp = tempfile.mkdtemp(prefix="tameshi-r15-usage-")`.

Directory-derivation check for that exact placement:

| `dirname^n(SELF)` | value | contained |
|---|---|---|
| 1 | `<tmp>/r/lane/tools` | yes |
| 2 | `<tmp>/r/lane` | yes — correct `LANE_ROOT` for a tool under `tools/` |
| 3 | `<tmp>/r` | yes |
| 4 | `<tmp>` | yes — historical `LANE_ROOT` formula; any mistaken receipt write still lands under `<tmp>` |
| 5 | parent of `<tmp>` | not used by any tools-relative derivation |

So the fixture stays hermetic even if the implementation regresses past the
argv check and writes a receipt: both the correct and the historical root
formulas resolve inside `<tmp>`. Do **not** run the maintained tool in place
from this fixture: `SELF`/`LANE_ROOT` are resolved with
`os.path.realpath(__file__)` at import (`:46-48`), which would touch the real
lane path, and a regression could write the round-15 receipt into the real
lane.

### 3.2 Exact steps (stdlib; adapt into `--selftest`)

```python
tmp = tempfile.mkdtemp(prefix="tameshi-r15-usage-")
lane = pathlib.Path(tmp, "r", "lane")
copy = lane / "tools" / "context-capture.py"
copy.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SELF, copy)                     # SELF = maintained tool path
assert hashlib.sha256(copy.read_bytes()).digest() == hashlib.sha256(
    pathlib.Path(SELF).read_bytes()).digest()

before = {p.relative_to(tmp) for p in pathlib.Path(tmp).rglob("*")}

env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
env.update({"LC_ALL": "C", "PYTHONDONTWRITEBYTECODE": "1"})

proc = subprocess.run(
    [sys.executable, "-B", str(copy), "--bogus-flag"],
    cwd=str(lane), env=env, stdin=subprocess.DEVNULL,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
)

err = proc.stderr.decode("utf-8")
after = {p.relative_to(tmp) for p in pathlib.Path(tmp).rglob("*")}

ok = (
    proc.returncode == 64
    and proc.stdout == b""
    and "unexpected argument(s): --bogus-flag" in err
    and "usage: " in err
    and before == after                          # no receipt, no .tmp dotfile, no __pycache__
)
```

Notes, each bounded:

- `timeout=30` mirrors the historical `CONTROL_TIMEOUT_S`; the usage branch
  returns immediately.
- `-B` plus `PYTHONDONTWRITEBYTECODE=1` keeps the main-script import from
  creating `__pycache__`; the before/after set equality would catch it anyway.
- `GIT_*` stripping mirrors `safe_env()` (`:170-173`). The usage branch reads
  no environment, but a uniform child environment makes a regression that
  reaches `evaluate()` fail on the missing synthetic inputs (exit 2) rather
  than on ambient state.
- `before == after` is the literal "no receipt" assertion from the exit map.
  It covers the receipt path, the `mkstemp` dotfile from `write_receipt`
  (`:559-573`), and any mistaken directory creation.
- Copy-hash equality is a precondition record, not a claim about production
  behavior; it proves the subprocess ran the maintained bytes.
- The same recipe, with the argv tails from §2, yields the other four rows.
  Cleanup: `tempfile.TemporaryDirectory` or explicit `rmtree`; nothing outside
  the temp root was touched.

## 4. Stable finding and selftest labels

- Production-stable observable: `exit 64` plus literal
  `unexpected argument(s): <space-joined argv>` on stderr, `usage: ` echo
  following, stdout empty, no receipt. This is the pair the fixture must pin.
- Suggested selftest label (new, hyphenated, matching
  `usage-no-arguments` / `usage-selftest-extra` at
  `tools/evidence-disposition.py:1830-1831`): `usage-unexpected-argument`.
  Reuse the existing selftest output convention rather than inventing one:
  `SELFTEST_CASE <name> PASS (<detail>)` (`:1521`), `FAIL` (`:1524`), final
  `SELFTEST: PASS (n/n)` (`:1856`).
- Improvement over the sibling's usage rows: those assert only
  `returncode == 64` (`:1829-1836`). For C1's literal exit/finding requirement,
  this class should assert exit **and** the stderr echo **and** zero writes.
  That is three assertions on one existing behavior, not a new validation
  framework.
- The program-name prefix is not part of the stable pair. Historical text is
  `capture-context.py: unexpected argument(s): ...`; a promoted tool named
  `context-capture.py` may use the new basename. Assert the name-independent
  substring `unexpected argument(s): --bogus-flag` (and `usage: `), not the
  whole first line, unless the implementation deliberately freezes the
  historical prefix. Do not assert both name variants as if both existed.

## 5. Implementation-critical notes for ContextGate

### 5.1 Do not copy the sibling's zero-argument usage row

`tools/evidence-disposition.py` legitimately uses `[sys.executable, SELF]` as
its `usage-no-arguments` row because that CLI requires `--root` and
`--dispositions` (`:1928-1941`). `capture-context.py` is the opposite:
zero arguments is the valid capture mode (`:605-614`). Running `[SELF]` inside
a context selftest would execute the production capture against live lane
inputs and write the round-15 receipt. The context usage rows must all pass an
explicit invalid token (or the single help token) and a temp cwd.

### 5.2 Do not let a stock parser turn this into exit 2 or a new token

`argparse`'s default error path prints `error: unrecognized arguments: ...`
and exits **2**. Exit 2 is this tool's could-not-evaluate class and writes an
`invalid_input` receipt (`:617-628`), so an argparse default would silently
merge the two classes and erase the 64 row. The existing repository pattern is
a hand-rolled parser raising `UsageError` and returning 64
(`tools/evidence-disposition.py:147,1863-1941`); either follow that pattern or
override the parser's exit status to 64 and emit the historical
`unexpected argument(s): ` token.

### 5.3 Root derivation must change for the new location

The historical script sits four levels below the lane root
(`.ufo/evidence/round-14/capture-context.py`, `:47`). A tool at
`<lane>/tools/context-capture.py` must use:

```python
LANE_ROOT = os.path.dirname(os.path.dirname(SELF))   # dirname^2, not ^4
FLEET_ROOT = os.path.dirname(LANE_ROOT)
```

Copying `dirname^4` verbatim yields `LANE_ROOT=/home/vgpnk/Projects` for the
real path, i.e. reads and writes outside the lane. This is independent of the
64 fixture (which never resolves roots) but is required for normal capture and
for the fixture's containment argument in §3.1.

### 5.4 Keep 64 distinct from 2

- 2 = could-not-evaluate: writes a receipt with `status=invalid_input`,
  `exit=2`, and a `kind` (`:617-628`).
- 64 = usage error: writes no receipt at all (docstring `:29`, code order
  `:605-614`).

A fixture cannot distinguish the classes if the promoted tool starts emitting a
receipt on usage errors, and a registry cannot either. Preserve the absence.

### 5.5 Registry classification (Registry owns the edit; advisory only)

The active row (`SKILL.md:1602`) declares only 0/1/2 and says "no standalone
selftest". The round-14 routed defect 5 requires the 64 path to be declared
and requires a standalone isolated selftest. Suggested verdict-map text for
the context gate, keeping the source literals while adding the gate-standard
umbrella:

> 0 clean; 1 failed/mismatch; 2 could-not-evaluate; 64 could-not-evaluate
> (usage error, no receipt)

and for the disposition gate's existing `64 usage` token, the same
`64 could-not-evaluate (usage)` umbrella. The parenthetical keeps the
observable distinction: 64 has no receipt, 2 does. This seat does not edit
`SKILL.md`.

## 6. Non-claims and bounds

- Nothing in §2-§4 was executed; no claim that `tools/context-capture.py`
  exists, compiles, or passes. The report answers only what the historical
  bytes support and what a hermetic fixture must assert.
- No claim about exit 0/1/2 fixtures (other Spec seats own clean, mismatch,
  control, mapping, unavailable, tamper, JSON, types, timestamp,
  environment, names, source pins, reuse). No broad validation feature is
  proposed: the 64 row is one subprocess, one exit compare, three string/set
  compares.
- Historical bytes and the round-14 receipt are untouched;
  `7313e9a2...` remains the read digest.
