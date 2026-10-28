# T55W1Simplifier — two-tool grammar fix vs one shared `tools/scratch_root.py`

**Verdict: keep the per-tool definitions. Do not create `tools/scratch_root.py`.**
The round's fix is the *handler*, not the helper: the seven helpers already compute the same
rule correctly at base (2 byte-identical variants, differing only in one docstring sentence),
while the defect R55 measures came from three tools that raised a bare `RuntimeError` into a
generic handler. A shared module does not touch that handler and cannot be imported in four of
the six ways this lane runs a tool — one of which is another member of the seven.

Nothing in the lane was edited by this seat. Every mutation below is a `git clone --shared`
fixture under `/fast/scratch/hyaku/tameshi-r55/T55W1Simplifier/` (removed at the end). Receipts:
`.ufo/waves/round-55/w1/T55W1Simplifier-receipts/` (scripts and their transcripts named per
claim).

The lane moved while this seat ran: the seat opened at `631cd645` (counter freeze), the C0
integration landed at `9cf0146`, and the freeze's amendment 8 landed at `133b2ce`. Findings are
stated against the revision they were measured at, and the counter was audited in **both** byte
states (`c2-measure.frozen.py`, sha256 `36ca47d3…`, and `c2-measure.amd8.py`, sha256 `0458f632…`).

---

## 1. What is actually duplicated (measured, not counted by eye)

`receipts/dup-ledger.py` → `receipts/dup-ledger.out`, run at base `0a2010ac` and at lane HEAD
`133b2ce`:

| unit | base `0a2010ac` | lane HEAD `133b2ce` (C0 landed) |
|---|---|---|
| `strict_scratch_root()` body | **88 lines, 7 copies, 2 distinct bodies** (`b161cc82` 13 lines: env-diff, bash-witness-study, pin-disposition, evidence-disposition; `80194a6d` 12 lines: repeat-control, registry-check, context-capture) | 88 lines, 7 copies, 2 distinct bodies (same split; the 12-line group's sha moved to `ba67d7f8` — docstring only) |
| raise token | **2** (`raise ScratchRootUnusable(` ×4, `raise RuntimeError(` ×3) | **1** (`ScratchRootUnusable` ×7) |
| `class ScratchRootUnusable` | 4 copies, 8 lines, 1 variant, **absent in 3** (repeat-control, registry-check, context-capture) | 7 copies, 14 lines, **3 variants** (`631d5a8c` ×4, `c1e93c4b` ×1, `ea2ecd8c` ×2) |
| seven tool files | 11,955 lines | 11,996 lines |

So the real duplication is 88 lines of helper (0.7 % of the seven files), and the round's fix
**traded divergence for copies**: the class token converged from 2 to 1 (good), while the class
block went from 4 copies/1 variant to 7 copies/3 variants (a 6-line addition, three docstrings to
keep in step). That is the correct trade for a two-line type marker, but it is the honest ledger, and
it is the opposite of what "dedupe the class" would buy.

## 2. The divergence that actually caused the R55 defect is the handler

At base, all three 12-line helpers computed the *same correct* rule; the failure was downstream:

```
repeat-control   setup_failure(f"{type(exc).__name__}: {exc}")   → "setup: RuntimeError: …"   stdout verdict + exit 2
context-capture  except Exception → "SELFTEST: FAIL (setup error: RuntimeError: …)" on STDOUT  exit 2
registry-check   --rev clone failure → "REGISTRY_CHECK: could-not-evaluate (…)" on STDOUT      exit 2
```

Three tools, three different prefix/stream/exit shapes — exactly the four prefixes, two streams and
two exit constants round 54 measured (`T54W1Simplify01.md` §2). A shared helper module addresses
none of them: the arm has to stay per tool regardless, because its prefix, stream and exit code are
the tool's own contract.

## 3. The case *for* one module, stated at its strongest

- 88 helper lines + 14 class lines replaceable by one 22-line module and seven one-line imports:
  measured net at lane HEAD `133b2ce` is **−52 lines** (`8 files changed, 36 insertions(+), 88
  deletions(-)`, `receipts/module-costs.txt` §5) — a 0.43 % shrink, and after this round the
  helper exists in *seven* copies rather than two variants of one, so the drift surface grows.
- One rule, one place: the round-54 docstring sentence ("an empty TMPDIR is unset") is already
  missing from three of the seven copies at base. A module deletes that question.
- The class would be declared once instead of 7 times; the three new declarations C0 added (6 code
  lines + docstrings) would not exist.

That is a genuine, bounded win. It is bought with the five breakages below, and it does not deliver
the round's claim on its own: converting the **base** tree to the module and changing nothing else
leaves the frozen grammar at `grammar=6/9` — byte-identical to the base score
(`receipts/real-arms.txt`, "shared-module option" block). The module is grammar-neutral; the handler
arm is the whole fix.

## 4. The case against — five measured breakages, one of them a frozen instrument

1. **The round's own frozen no-harm monitor goes RED.** `no-harm.sh` `tools-scope` allow-lists
   exactly eight paths (`M:` of the seven tools plus `registry.json`); an added file falls to `*)
   s=RED`. Running the frozen lines verbatim on the module fixture (`receipts/module-costs.txt` §4):
   ```
   NOHARM tools-scope [M:tools/bash-witness-study.py … A:tools/scratch_root.py ] RED
   ```
   `no-harm.sh` is in `contract.json`'s `frozen_paths`; this round may not amend it. The option is
   therefore not merely costlier — it is incompatible with the round's deciding instrument.
2. **`env-diff` — one of the seven — cannot measure a converted python tool.** Its surface model is
   one git blob: `read_surface()` returns `git show rev:path` bytes and `execute()` writes them as
   the single file `/tmp/w/target.sh` inside bwrap. Measured (`receipts/module-costs.txt` §6):
   ```
   surface py-surface classification unavailable clean_exit 1
   stderr_tail 'Traceback … from scratch_root import … ModuleNotFoundError: No module named 'scratch_root''
   ```
   The lane's environment-sensitivity instrument silently degrades to `unavailable` for a class of
   surfaces it used to classify.
3. **`python3 -I` drops the script directory from `sys.path`.** rc=1, `ModuleNotFoundError`
   (`receipts/module-costs.txt` §2). The lane documents `python3 -I` for three tools and its
   no-harm monitors invoke two tools that way.
4. **Subset copies die at import.** Round 17 staged 3 of 33 `tools/` entries, round 18 staged 4 of
   33. A converted tool copied alone gives `rc=1` + a traceback (`receipts/module-costs.txt` §1) —
   i.e. it reintroduces exactly the defect class (R53.6) this lineage removed.
5. **A write into the lane on every invocation.** 6 of 7 converted tools leave
   `tools/__pycache__/scratch_root.cpython-314.pyc` even when they only print usage
   (`receipts/pycache.txt`); only context-capture is immune, because it sets
   `sys.dont_write_bytecode`. Nothing in the lane removes `tools/__pycache__`, and `registry-check`
   only masks it for its *children* by exporting `PYTHONDONTWRITEBYTECODE`.

Round 54's fourth cost still holds at this base and I re-verified the anchors: each tool hashes only
itself (`env-diff.py:252 instrument_sha256 = digest(Path(__file__).read_bytes())`,
`evidence-disposition.py:230`/`pin-disposition.py:192 tool_sha256()` over `SELF`, and
`registry-replay.py:164` loads a runner by path with `spec_from_file_location`, which does not put
the file's directory on `sys.path`). A sibling helper's bytes would sit outside every one of those
pins.

One further argument, from this round's own contract: deliverable 3 requires the note to say the
class is "an operator-visible line grammar, **not a shared Python type**". Building the shared type
while the note denies one would make the frozen document false.

## 5. Decision

**Minimal, per tool.** Add the class where it is missing, raise it from the helper, and catch it
before the generic handler. Demonstrated in a scratch clone at rev `1cebefd`: 20 insertions,
2 deletions across two files, and with the frozen counter's own table:
`grammar=8/9` (only `registry-check --rev`, which the base tree also fails, is red), `lazy=5/5`
(`receipts/real-arms.txt`).

The shape that landed as C0 (`9cf0146`) is the same decision extended to a third tool — correctly:
the amended counter's ninth allocating mode, `registry-check --rev`, is a genuine allocating path
whose base line was `REGISTRY_CHECK: could-not-evaluate (…)` **on stdout** with a parenthesis
instead of the class colon, i.e. unfixable by the grammar without touching that tool. Real receipt on
lane HEAD: `grammar=9/9`, one stderr line each (`receipts/grammar-lane-head.txt`).

One reading the L1 should state rather than leave implicit: `repeat-control` still writes
`REPEAT_CONTROL: setup_error` to stdout alongside the stderr class line
(`receipts/grammar-lane-head.txt`). The frozen counter permits it (it only forbids the grammar line
on stdout and any `RuntimeError`/`Traceback` token). The seat brief says "stdout carries no setup
error". Both readings are defensible — the tool's contract is "every exit carries one
`REPEAT_CONTROL: <id>` line" — but the round's report must say which one it means, because the
counter cannot tell them apart.

## 6. Interface sketch — **not built**, and not recommended this round

Kept for the record so a later round does not have to re-derive it:

```python
# tools/scratch_root.py   (preconditions: no-harm tools-scope amended; see §4)
class ScratchRootUnusable(RuntimeError): ...      # the type token only
def strict_scratch_root() -> str: ...             # TMPDIR when usable, else gettempdir()
def class_line(tool: str, exc: BaseException) -> str:
    """'<tool>: could-not-evaluate: <exc>' — the operator line, stderr, exit 2."""
```

It becomes warranted only when **all** of these hold: (a) a round amends the `tools-scope`
monitor's allow-list; (b) `env-diff` gains a multi-file surface model (or the lane stops pinning
python tools as single blobs); (c) every invocation path either keeps the script directory on
`sys.path` or the tools carry an explicit `sys.path` bootstrap; (d) a `tools/__pycache__` policy
exists. Until then the module buys −52 lines and costs the lane its single-file execution model.

## 7. C2 counter dead-arm audit

Method: load the frozen counter, replace **only** the two subprocess executors (`run`, `trace`)
with a scripted responder, and call the frozen `main()` unmodified — every predicate, denominator,
`total` term and the verdict are the counter's own code (`receipts/arm-matrix.py`,
`receipts/arm-matrix.out` for the pre-amendment bytes, `receipts/arm-matrix.amd8.out` for the
current ones). A scenario the counter rejects while every observation is perfect is a counter
defect. Doc arms additionally ran against three purpose-broken fixture revisions
(`receipts/doc-arms.txt`).

| # | perturbation | pre-amd8 | amd8 | reading |
|---|---|---|---|---|
| S0 | all observations perfect, conforming docs | **total=1, PASS=false, bad={}** | total=0, PASS=true | pre-amd8 the **target was unreachable**; amd8 fixes it |
| S1 | grammar line, exit 3 | 8/9 | 8/9 | live |
| S2 | grammar line on stdout | 8/9 | 8/9 | live |
| S3 | grammar line + `Traceback` | 8/9 | 8/9 | live |
| S4 | grammar line + `RuntimeError` | 8/9 | 8/9 | live |
| S5 | grammar line printed **twice** | — | **9/9, PASS** | lenient |
| S6 | grammar line + a stray second stderr line | — | **9/9, PASS** | lenient |
| S7 | a lazy mode allocates (rc 2) | 4/5 | 4/5 | live |
| S8 | `strict_scratch_root` treats `""` as unusable | 12/13 | 12/13 | live |
| S9 | usable-arm regression (rc 1) | 12/13 | 12/13 | live |
| S10 | one `/tmp` mkdir in the census | tmp_mkdirs=8 | tmp_mkdirs=8 | live |
| S11 | strace log missing | total unchanged | **total=0, PASS=false** | accounting gap |
| B-docs | one registry cell loses the marker | — | docs 6/7 | live |
| B-note | one mode name dropped from the note | — | note 8/9 | live |
| B-skill | SKILL.md loses the marker | — | skill 0/1 | live |

**No arm is dead** — each of the seven can be driven red by a concrete input. Four findings survive
the audit, all in the *frozen* instrument, so they are reported and not repaired:

1. **`total` can print 0 while the verdict is false (S11).** `bad["strace:<mode>"]` is set when the
   tracer log is missing, but `tmp_total` only sums keys starting `tmp_mkdirs:` and no term includes
   the `strace:` class; the verdict still reads `not bad`. Verdict-safe, number-unsafe: the round's
   prose target "`total=0`" is not by itself a pass.
2. **"One line" is not what the grammar arm enforces (S5, S6).** The predicate is `rc == 2 and any(
   GRAMMAR.match(line) for line in stderr)` plus two token bans; a duplicate class line, or a class
   line followed by any other diagnostic, is scored conformant. The seven tools do print exactly one
   line today (`stderr=1` for all nine modes in `receipts/grammar-lane-head.txt`), so the claim holds
   of the *tools* — it just is not the counter's predicate, and the round's report should not say the
   counter proves it.
3. **The grammar's `'<value>'` is unsatisfiable for a value containing `'`.** The tools print the
   path with `%r`, which switches to double quotes exactly then. Real execution, frozen regex
   (`receipts/apostrophe-real.txt`):
   ```
   TMPDIR="/tmp/it's here-missing"  rc=2
     stderr: pin-disposition.py: could-not-evaluate: … directory: "/tmp/it's here-missing" (could-not-evaluate)
     frozen GRAMMAR matches: [False]
   ```
   A conforming tool is scored FAIL for an apostrophe in `TMPDIR`. The same line with a plain path
   matches `[True]`.
4. **`note` is a substring count.** `note_names = [m for m in allocating if m[0] in note_txt]` over
   whitespace-collapsed text: a note that names a mode in a sentence saying it is *not* supported
   scores the same as one that lists it as conforming. With amendment 6 the denominator is now
   `len(allocating) = 9`, so the note must name `registry-check --rev` too — deliverable 3's "eight
   allocating modes" is one short of what the current counter measures.

## 8. Bounds and hygiene

- No lane production file, counter, contract, freeze, no-harm or deciding-run script was modified.
  `tools/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**` were read only.
- All mutation happened in `git clone --shared` fixtures under
  `/fast/scratch/hyaku/tameshi-r55/T55W1Simplifier/`, each with `git rev-parse --show-toplevel`
  asserted equal to the fixture directory before any commit. No `jj`, no lane checkout, no push.
  The scratch tree is removed at the end of the seat, so every fixture revision cited above is
  preserved as a diff in `receipts/fixtures.diff` (sha256 `ede827bc…`, seven sections):
  `1cebefd` the two-tool fix, `caf02b6` the shared module at base, `4d6f548` the shared module at
  lane HEAD, `06bead3` the conforming-docs fixture, `084fd94`/`d94b4f2`/`af0a6d9` its three
  single-defect mutants.
- Sources census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  → `tameshi ok …/corpus/SOURCES.md`, exit 0 (W04 duplicate-url warnings only).
- Tooling: nothing installed or upgraded (pacman paused host-wide; no `uv`/`npx`/binary needed).
- The scratch tree is removed at the end of the seat; the receipts under
  `.ufo/waves/round-55/w1/T55W1Simplifier-receipts/` are the only artifacts.
