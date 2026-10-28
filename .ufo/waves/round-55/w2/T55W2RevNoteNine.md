# T55W2RevNoteNine — nine modes vs the code

Seat: T55W2RevNoteNine (wave 2, falsify). Lane `tameshi-shokunin`, attacked at
**C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`** on a `git clone --shared`
(`.ufo/evidence/round-55/c2/measure.py` read at the *frozen* counter
`133b2ce6d4d86d783db38607343c3654350194b8`, amendment 8). No lane file was
edited; every write below is under `.ufo/waves/round-55/w2/`.

Item: does the note's claim that **exactly nine documented modes allocate
scratch** hold against the code, and is there a tenth?

## Working-tree context

The attacked bytes are C0's. While this seat ran, the lane's working tree
acquired uncommitted edits from other wave-2 seats: the note's final paragraph
(the blind-spot sentence at `:99-101`), `tools/registry-check.py` and
`tools/context-capture.py` (stream-refusal handling). None of them touch the
nine-mode section, the five lazy names, or the helper construction, so every
finding below stands against the working tree as well — except that the
in-flight note edit **removes** the blind-spot sentence and leaves the nine-mode
count unqualified, which makes F1 harder to route, not easier. Verdict is
against C0 as the seat spec requires.

## Verdict

**The nine are real, and the count is right for the seven tools' own
allocation — but the note's mode table is not the whole allocating set, and its
own line is not universally parseable.**

* Nine documented modes reach a `strict_scratch_root()` call site, and only
  those nine do. Each is listed below with the call site, the branch that
  reaches it, and the handler that prints the frozen line; all nine measured at
  C0 print the frozen `GRAMMAR` and exit 2 (receipts 01/02).
* The five named lazy modes reach **no** allocation at all — not "allocate
  lazily": their call graphs contain no `strict_scratch_root()` call and no
  `tempfile.*` call, and under a fresh usable `TMPDIR` they issue **0** `mkdir`
  inside it (receipt 03).
* **There is a tenth documented allocating mode: `registry-check --root DIR`
  (the live run, the tool's default mode).** It allocates scratch inside the
  rows it replays, and under an unusable `TMPDIR` it prints a *verdict*
  (`ROW … got=2 differs`, exit 1) instead of the one-line class (receipts
  04/05). This is the same class of miss as the `registry-check --rev` the round
  already found, one branch over: `--rev` allocates itself and was added; live
  run allocates through its children and was not.
* Three smaller defects (below): the frozen grammar cannot match its own line
  for a `TMPDIR` value containing `'`; the note's fifth lazy label
  `pin-disposition --read` is not a mode of the tool; and the frozen counter's
  own docstring still documents **eight** allocating modes.

## The nine (deliverable table)

Allocation sites found by `grep -n strict_scratch_root` over `tools/` (ten call
sites in seven files) and by the branch-scoped AST closure in
`T55W2RevNoteNine-receipts/reach2.py` (output `09-reach.out`), then measured.

| # | mode (as the note names it) | allocation site | how that mode reaches it | guard that prints the line |
|---|---|---|---|---|
| 1 | `env-diff --selftest` | `tools/env-diff.py:80` `TemporaryDirectory(…, dir=strict_scratch_root())` in `execute()` | `selftest()` → `probe()` → `execute()`; also the unconditional `execute(…, bwrap="/nonexistent/tameshi-bwrap")` at `:180` | `:234-236` `except ScratchRootUnusable` → `ENVDIFF_SETUP: could-not-evaluate: …`, rc 2 |
| 2 | `env-diff --contract` | same `:80` | `main()` → `surface_result()` → `probe()` → `execute()` | `:263-265` same handler |
| 3 | `repeat-control --selftest` | `tools/repeat-control.py:629` `mkdtemp(dir=strict_scratch_root())` | `dispatch()` `--selftest` → `selftest()` first statement | `main()` `:925-926` → `could_not_evaluate()` `:229-232`, rc 2 |
| 4 | `registry-check --selftest` | `tools/registry-check.py:934-935` `mkdtemp(dir=strict_scratch_root())` | `main()` `--selftest` → `selftest()` first statement | `:1851-1853`, rc 2 |
| 5 | `registry-check --rev` | `tools/registry-check.py:784` in `clone_lane_at_rev()` | `main()`, branch `if rev is not None:` → `clone_lane_at_rev()` at `:1934` (only caller) | `:1935-1939`, rc 2 |
| 6 | `bash-witness-study selftest` | `tools/bash-witness-study.py:1259-1260` `mkdtemp(dir=strict_scratch_root())` | `main()` handlers map → `cmd_selftest()` first statement | `:1788-1790`, rc `EXIT_CANNOT` |
| 7 | `pin-disposition --selftest` | `tools/pin-disposition.py:725` `mkdtemp(dir=strict_scratch_root())` | `main()` `argv == ["--selftest"]` → `selftest()` first statement | `:1399-1401`, rc 2 |
| 8 | `evidence-disposition --selftest` | `tools/evidence-disposition.py:2370` `mkdtemp(dir=strict_scratch_root())` | `main()` `options["selftest"]` → `selftest()` first statement | `:3231-3233`, rc 2 |
| 9 | `context-capture --selftest` | `tools/context-capture.py:1642-1643` `mkdtemp(dir=strict_scratch_root())` in `SelftestHarness.__init__` | `main()` → `run_selftest()` → `SelftestHarness()` at `:2214` | `run_selftest()` `:2217-2221`, rc 2 |

Measured (receipt `01-nine-modes.out`): every one of the nine, with
`TMPDIR=<nonexistent>`, returns **rc 2**, prints one stderr line that the
*frozen* counter's own `GRAMMAR` object matches (`frozen GRAMMAR.match: True`),
and carries no `RuntimeError`/`Traceback` token. Stdout (receipt
`02-nine-stdout.out`) is empty for eight; `repeat-control --selftest` also emits
`REPEAT_CONTROL: setup_error` on stdout — a class id (`EXIT_BY_ID["setup_error"]
== 2`), not a verdict, so it does not reintroduce the round-54 `SELFTEST: FAIL`
residue.

No tenth *helper* site exists: the ten `strict_scratch_root()` call sites in the
seven tools are exactly the nine above plus `env-diff.py:80`'s second reach
(the same site, reachable from both `env-diff` modes). No other tool defines the
helper (`grep -rn strict_scratch_root tools/` → 7 definitions).

## The five lazy modes: why they cannot reach an allocation

Not "they allocate only on the real path" — each lazy entry function has no
allocation in its call graph at all, and the tool's only helper site is inside
its selftest, which the lazy path never calls.

| mode (as the note names it) | entry function | why the path cannot allocate |
|---|---|---|
| `repeat-control --snapshot` | `snapshot_mode()` `:481` | the tool's only `tempfile` use is `:629` inside `selftest()`; `snapshot_mode` reads `expected.json` + observation files and writes nothing |
| `bash-witness-study count` | `cmd_count()` `:1070` | the tool's only `mkdtemp`s are `:1259`/`:1264` inside `cmd_selftest()`; `count` recomputes from `results.tsv` and the case logs |
| `pin-disposition --read` (**no such flag — see F3**) | `run_mode()` `:686` (the read path, entered by `--manifest/--root`) | only helper site `:725` inside `selftest()`; `run_mode` reads git objects and emits JSON |
| `evidence-disposition --json` (`--json` is a flag of the read mode) | `run_mode()` `:1547` (entered by `--root/--dispositions`) | only helper site `:2370` inside `selftest()`; `run_mode` reads receipts and git blobs |
| `context-capture --check` | `run_check()` `:1359` | only helper site is `SelftestHarness.__init__` `:1642-1643`, constructed only from `run_selftest()` |

Empirical, same conclusion from the other side (receipt `03-lazy-strace.out`):
with a fresh usable `TMPDIR` and `strace -f -e trace=mkdir,mkdirat`, each of the
five issues **`mkdirs-under-TMPDIR=0`**; with an unusable `TMPDIR` each keeps
rc 0 (receipt `01-nine-modes.out`, lazy block). So the lazy claim is sound for
the five *named* invocations — with the naming caveat in F3.

## F1 (high) — the tenth documented allocating mode: `registry-check --root` (live run)

`registry-check.py` documents three modes in its own USAGE (`:117-120`) and
docstring: the live run (`[--root DIR]`, the default), `--rev REV`, and
`--selftest`. `--rev` and `--selftest` call `strict_scratch_root()` themselves
(`:784`, `:935`); the **live run allocates through its rows**: `main()` →
`evaluate()` (`:847`) → `run_row()` (`:648`) → `Popen(row["argv"], cwd=cwd,
env=row_env())` (`:676`), and every row that is one of the seven selftests then
calls `strict_scratch_root()` in the child. No guard exists on that branch — the
live path returns verdicts.

Receipt `05-live-alloc.out` (usable `TMPDIR`, `--only repeat-control-selftest`):
44 `mkdir` calls inside `$TMPDIR/tameshi-r12-repeat-control-selftest.*`, i.e. the
mode's scratch lands in the live `TMPDIR` through the row.

Receipt `04-live-mode.out` (unusable `TMPDIR`, same row):

```
ROW repeat-control-selftest expect=0 got=2 differs
REGISTRY_CHECK: held=0/1 superseded=0
rc=1
```

versus the same row under a usable `TMPDIR`: `expect=0 got=0 held`, `rc=0`.

So the tenth mode takes an **environment fact and prints it as a registry
verdict** (`differs`, exit 1) — the exact class round 53 removed from inside the
tools, relocated one level up, and the frozen counter never measures it (its 14
measured modes are the nine plus the five lazy ones; `--root` live is in
neither). The note's blind-spot sentence (note `:99`) points the wrong way:
*"a documented mode outside the registry and the usage text could still allocate
scratch unmeasured"* — the unmeasured allocating mode is documented **inside**
both the usage text and the registry surface itself.

Fix shape (not applied — this seat does not edit): either give the live branch
the same refusal when any selected row declares `scratch_root` and `TMPDIR` is
set-but-unusable (rc 2, one line), or state in the note and the counter that the
live run inherits the class of its rows and is out of scope — the second is
weaker, because exit 1 is then an unfalsifiable pass-shaped result.

## F2 (medium) — the frozen grammar cannot match its own line for a quoted value

The line is built with `%r` (`tools/*/strict_scratch_root`, e.g.
`repeat-control.py:166-167`, the `%r` at `:167`), which double-quotes a value
that contains a single quote. Receipt `06-quoted-grammar.out`:

```
$ TMPDIR="/tmp/it's-not-a-dir-1920605" python3 tools/repeat-control.py --selftest
rc=2
repeat-control: could-not-evaluate: … TMPDIR is not a usable directory: "/tmp/it's-not-a-dir-1920605" (could-not-evaluate)
    -> frozen GRAMMAR.match: False
```

The behaviour is correct (rc 2, value named, one line); the **frozen counter's
`GRAMMAR`** (`'.+'`) does not match it, so the C2 grammar arm is value-shape
dependent: a legal unusable `TMPDIR` containing `'` turns nine passing modes into
nine arm failures. The note's template (`… directory: '<value>' (could-not-
evaluate)`) is not what the tools emit for such a value, and the note calls the
line "the contract". Either normalise quoting in the seven helpers, or widen the
grammar to `['\"].+['\"]` — both are one-line changes, but the grammar is frozen
in the counter, so this needs an amendment if the line is to stay byte-shaped.

## F3 (medium-low) — the fifth lazy mode does not exist as an invocation

Note `:90-93` names `pin-disposition --read` as a lazy mode; the tool accepts no
`--read` flag (USAGE `:148-150`: `--manifest PATH --root FLEET` or `--selftest`;
`parse_argv()` `:1355` rejects everything else). Receipt `07-pin-read-literal.out`:

```
$ TMPDIR=<unusable> python3 tools/pin-disposition.py --read
rc=2
  "status": "invalid_input",
  "error": {"kind": "invalid_usage", "message": "unknown argument: --read"}
```

Two consequences. (a) A reader following the note literally gets **exit 2** —
the same exit class as could-not-evaluate — with no grammar line, so the lazy
arm cannot be checked as written. (b) The frozen counter's lazy tuple is
labelled `"pin-disposition --read"` (`measure.py:112`) while its argv omits
`--read` (it passes `--manifest … --root …`), so the measured mode and the
reported label differ; the counter would keep passing even if the read path
started allocating, because the label is not the invocation. The name is the
registry row `pin-disposition-read`, not a mode. `evidence-disposition --json`
in the same sentence has the milder form of the problem: `--json` is a flag of
the read mode, not a mode.

## F4 (low) — the frozen counter still documents eight allocating modes

`133b2ce:.ufo/evidence/round-55/c2/measure.py` (frozen) says in its docstring:

```
$ git show 133b2ce:.ufo/evidence/round-55/c2/measure.py | sed -n '18,32p'
  grammar  8 allocating modes (the seven self-tests + `env-diff --contract`):
  …
  * only the self-test was measured, so `env-diff --contract` (the one other
    documented mode that allocates scratch) was outside the contract.
`C2_R55: rev=... grammar=N/8 lazy=N/5 … note=N/8 skill=N/1 total=N …`
```

Amendment 8 fixed
the *totals* (`len(allocating)`, `len(cheap)`) but not the prose, so the frozen
counter and the note disagree on the contract's own count (8 vs 9). The code is
right and the note is right; the frozen document a cold reader reaches first is
stale. Cannot be fixed inside this wave (frozen file) — an amendment-9 candidate
or an explicit "the docstring is superseded by amendment 8" line.

## Residual risk (checked, not defects at C0)

1. **`tools/env-diff.py:186` is the only allocation site in the seven tools with
   no `dir=`** (`tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff-pin.")`),
   so it resolves `TMPDIR` through `tempfile.gettempdir()` — the round-53 silent
   `/tmp` fallback. It is **not reachable** under an unusable `TMPDIR` today
   *only* because `env-diff.py:180` unconditionally calls `execute(…,
   bwrap="/nonexistent/tameshi-bwrap")`, which hits the guard at `:80` first.
   Verified with a `PATH` that has no `bwrap` (receipt `08-bwrap-absent.out`):
   rc 2, frozen grammar, `mkdirs under /tmp: 0`. The ordering is load-bearing
   and undocumented; if `:180` is ever reordered after the pin fixture, the
   selftest silently writes the fixture under `/tmp` and exits 1 with FAIL cases
   — a verdict, not the class.
2. **`registry-check --rev`'s usable path is not exercised anywhere.** Note
   `:82-84` says it "is covered by the tool's own self-test, which exercises the
   same helper" — true of `strict_scratch_root()` (`:935`), false of
   `clone_lane_at_rev()`: the selftest never calls it (`grep -n
   clone_lane_at_rev` → definition `:774` and the single `--rev` caller `:1934`).
   No registry row covers `--rev` either. So a usable-`TMPDIR` regression in the
   clone/fleet-mirror branch would be invisible to C2.
3. `bash-witness-study check` **fails at C0** (`WITNESS_CHECK: DRIFT
   tools/mutate-and-run.sh sha256=977de47… committed=75ed934…`, rc 1, receipt
   `10-unmeasured-modes.out`). Provenance: the runner last changed at round-51
   `6d8c11e`, the manifest is from round-12 `9df9212` — pre-existing, **not** a
   C0 or wave-1 regression. Named so it is not mistaken for one; out of this
   item's scope.

## Coverage of the hunt

Documented modes enumerated from usage text, docstrings, and registry rows —
**20 modes across the seven tools**: `env-diff` 2 (`--contract`, `--selftest`);
`repeat-control` 3 (`--runs/--out`, `--snapshot`, `--selftest`);
`registry-check` 3 (live `--root`, `--rev`, `--selftest`); `bash-witness-study`
6 (`declare`, `run`, `rerun`, `count`, `check`, `selftest`);
`pin-disposition` 2 (read, `--selftest`); `evidence-disposition` 2 (read,
`--selftest`); `context-capture` 2 (`--check`, `--selftest`).

* Nine reach a helper site (table above).
* One more allocates transitively: `registry-check --root` live (F1).
* The remaining ten allocate nothing: the five named lazy modes plus
  `repeat-control --runs/--out`, `bash-witness-study declare`, `run`, `rerun`,
  `check`. Measured for the cheap ones under an unusable `TMPDIR`
  (`10-unmeasured-modes.out`: `--runs` → `controls_match` rc 0; `declare` →
  refusal rc 1; `check` → drift rc 1); `run`/`rerun` are cited statically:
  `run_sweep()` always passes `--workdir` (`bash-witness-study.py:617-635`,
  the flag at `:628`), so the runner takes its `mkdir -p "$WORKDIR"`
  branch (`mutate-and-run.sh:490-495`, `else` at `:493`) and never its
  `mktemp -d` branch (`:491` run mode, `:1432` regression mode).
* Registry rows (19 rows referencing the seven tools) add no mode: every row is
  a selftest, a lazy read/snapshot, or `bash-witness count` — verified with
  `python3 -c "…"` over `tools/registry.json` (all 19 rows printed in receipt
  `11-registry-rows.out`).
  No row covers `registry-check --rev` or `env-diff --contract`.

## Verification gaps

* I did not re-run the frozen C2 counter end to end (other seats own that); the
  nine arms were reproduced mode by mode, and the grammar verdicts use the
  counter's own `GRAMMAR` object imported from the frozen file.
* `bash-witness-study run` / `rerun` were not executed (they run the 10-defect
  sweep into the lane evidence dir); their non-allocation is cited statically
  plus the runner's `--workdir` branch.
* The quoted-value finding (F2) was tested on `repeat-control` only; all seven
  helpers share the identical `%r` construction (`grep` of the seven
  definitions), so the conclusion generalises by construction, not by test.
* F1's full live run (all 49 active rows) was not run; `--only` isolates the
  allocation proof to one row and is sufficient because the row is the
  allocating path.

## Artifacts opened

At C0 (via the scratch clone): `tools/env-diff.py`, `tools/repeat-control.py`,
`tools/registry-check.py`, `tools/bash-witness-study.py`,
`tools/pin-disposition.py`, `tools/evidence-disposition.py`,
`tools/context-capture.py`, `tools/registry.json`, `tools/mutate-and-run.sh`,
`corpus/knowledge/scratch-root-contract.md`; plus
`.ufo/evidence/round-55/c2/measure.py` at C0 **and** at the frozen counter
`133b2ce` (docstring + totals diff), `SCORECARD.md` and `LOG.md` (drift
provenance only). Lane git log for the provenance of the runner drift.

## Receipts

`T55W2RevNoteNine-receipts/` — `probes.sh CLONE WORKDIR` (one command, reruns
everything; every grammar verdict imports the frozen `GRAMMAR`), `reach2.py`
(branch-scoped AST closure), and its outputs:
`00-rev.txt` (clone at C0, clean tree), `01-nine-modes.out` (nine rc 2 + frozen
grammar; five lazy rc 0; literal `--read` rc 2), `02-nine-stdout.out`,
`03-lazy-strace.out` (0 mkdirs), `04-live-mode.out` (differs/rc 1 vs held/rc 0),
`05-live-alloc.out` (44 mkdirs, first two lines), `06-quoted-grammar.out`,
`07-pin-read-literal.out`, `08-bwrap-absent.out`, `09-reach.out`,
`10-unmeasured-modes.out`, `11-registry-rows.out` (the registry row census:
19 rows, 6 modes, no allocating mode the table lacks).

Scratch (`/fast/scratch/hyaku/tameshi-r55/T55W2RevNoteNine`) removed. No lane
production file, frozen file, or wave spec was written; no mutating git command
ran in the lane; the census input set is untouched by this seat.

Report: .ufo/waves/round-55/w2/T55W2RevNoteNine.md
