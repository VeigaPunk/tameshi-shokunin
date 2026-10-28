# T55W2RevToolDiffs — attack on the three round-55 tool diffs

Seat: `T55W2RevToolDiffs` (wave 2, falsify; L1 TameshiR55). Milestone: attack the three tool diffs.
Axis under judgement: **operability** (C2). Base `0a2010acd1e92e4e332774050825e21bcfc7e079`, content commit
C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

## 0. Axes named (godspeed)

1. **Handler coverage** — every path that can reach `strict_scratch_root()` in each tool.
2. **Exit-class invariance** — does the diff move an exit code for anything except the refusal, and does the
   refusal keep `2` under every stream state.
3. **Stream contract** — what lands on stdout vs stderr, per mode, versus the tool's documented interface.
4. **Doc/byte fidelity** — the new note section, the seven registry cells and the counter's `docs` arm versus the
   bytes the tools actually emit.
5. **Machine-consumer contract** — `--json` callers of `registry-check`, stdout readers of `repeat-control`.

## 1. What I attacked, and how

All runs are read-only against two `git clone --shared` copies in scratch (no lane write, no lane mutation):

```
S=/fast/scratch/hyaku/tameshi-r55/T55W2RevToolDiffs
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
git clone -q --shared --no-checkout $L $S/clone-c0   && git -C $S/clone-c0 checkout -q -B w2c0 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
git clone -q --shared --no-checkout $L $S/clone-base && git -C $S/clone-base checkout -q -B w2base 0a2010acd1e92e4e332774050825e21bcfc7e079
```

Arm driver (kept as a receipt): `receipts/run-arms.sh`, run as

```
bash receipts/run-arms.sh $S/clone-c0 c0      #  → receipts/c0.arms.txt
bash receipts/run-arms.sh $S/clone-base base  #  → receipts/base.arms.txt
python3 receipts/pairs.py base c0 > receipts/pairs.txt
```

In this report `receipts/` means `.ufo/waves/round-55/w2/T55W2RevToolDiffs-receipts/`. Each arm runs one
documented mode with `TMPDIR=/nonexistent/x` or `TMPDIR=$S/tmp-ok`, storing `<arm>.rc`, `<arm>.stdout`,
`<arm>.stderr` under `receipts/<rev>/`. The full table is `receipts/pairs.txt`; the diff-relevant rows are
reproduced below (rc / stdout bytes).

| mode | TMPDIR | base rc / stdout | C0 rc / stdout |
|---|---|---|---|
| `repeat-control --selftest` | `/nonexistent/x` | 2 / 28 B (`REPEAT_CONTROL: setup_error`) | 2 / 28 B (same) |
| `repeat-control --snapshot …` | `/nonexistent/x` | 0 / 294 B | 0 / 294 B |
| `repeat-control --runs 3 --out … -- /bin/true` | `/nonexistent/x` | 0 / 437 B | 0 / 437 B |
| `repeat-control --help` | `/nonexistent/x` | 0 / 140 B | 0 / 140 B |
| `context-capture --selftest` | `/nonexistent/x` | 2 / 168 B (`SELFTEST: FAIL (setup error: RuntimeError: …)`) | 2 / 0 B |
| `context-capture --check --json` | `/nonexistent/x` | 0 / 626 B | 0 / 626 B |
| `context-capture` (no args) | `/nonexistent/x` | 64 / 0 B | 64 / 0 B |
| `registry-check --selftest` | `/nonexistent/x` | 2 / 0 B, stderr grammar | 2 / 0 B, stderr grammar (identical) |
| `registry-check --rev HEAD` | `/nonexistent/x` | 2 / 161 B (`REGISTRY_CHECK: could-not-evaluate (…)`) | 2 / 0 B |
| `registry-check --rev HEAD --json` | `/nonexistent/x` | 2 / 342 B (JSON report, `rev_resolved`) | 2 / 0 B |
| `registry-check --rev HEAD --only repeat-control-selftest --json` | `$S/tmp-ok` | — | 0 / JSON, `rev_resolved=9cf0146…` |
| `registry-check --root . --only repeat-control-selftest --json` (live) | `/nonexistent/x` | 1 / 1025 B | 1 / 1020 B |
| same, live | `$S/tmp-ok` | 0 / 3739 B | 0 / 3734 B |

The base-vs-C0 deltas are exactly the three hunks: repeat-control's stderr class, context-capture's
stdout→stderr move, registry-check `--rev`'s stdout→stderr move. The registry-check selftest hunk produced no
delta at all (finding F6).

## 2. Findings

### F1 (medium) — the refusal line is still written unguarded; a refusing stream yields exit `1`

The SKILL standing rule this round edited says the arm is "exit 2 … never a traceback, never exit 1"
(`SKILL.md:35-37`), and the note repeats it (`corpus/knowledge/scratch-root-contract.md:35-37`: "never 1 (a
verdict of \"differs\"/\"failed\") and never a traceback"). The handlers write the line with a bare
`sys.stderr.write` / `print(..., file=sys.stderr)`:

- `tools/context-capture.py:2217-2221`
- `tools/registry-check.py:1851-1853` and `:1935-1939`

A stream that exists but refuses bytes (`/dev/full`, ENOSPC) raises `OSError` inside the handler, the exception
escapes `main`, and CPython exits 1 — a verdict-class exit in both tools' vocabularies. Full receipt:
`receipts/devfull-matrix.txt`.

```
stream-state matrix (TMPDIR=/nonexistent/x):
                             base  C0     base  C0
                             stderr=/dev/full  stdout=/dev/full
context-capture --selftest     2     1     1     2
registry-check  --rev HEAD     2     1     1     2
registry-check  --selftest     1     1     —     —
repeat-control  --selftest     2     2     2     2
```

strace (`receipts/c0/cc-devfull.strace`) shows the mechanism for the C0 stderr case: the grammar write fails
`= -1 ENOSPC (No space left on device)`, the traceback writes fail, the interpreter reports `lost sys.stderr`,
`+++ exited with 1 +++`. Under `stderr=/dev/full` C0 context-capture also leaves stdout at 0 bytes
(`receipts/c0/context-capture-stderr-devfull.stdout`), so the operator gets **no line at all and exit 1**.

The honest reading of the base/C0 pair: the defect is not new — it moved. At base context-capture's line went to
stdout (stdout-full → 1) and now goes to stderr (stderr-full → 1); registry-check `--rev` did the same. C0's own
comment claims "the exception type never is [operator-visible] … never a traceback", but a refused stream still
turns the class into a traceback and exit 1. `repeat-control` is the only one of the three that is correct:
`emit_err` (`tools/repeat-control.py:183-187`) catches `(OSError, ValueError)` → `rc=2` under either stream.
`registry-check --selftest` under `stderr=/dev/full` is `rc=1` at base too — the new selftest branch copies the
pre-existing unguarded print.

Verdict: the round's "never exit 1" claim is not met for these two tools under stream refusal, and the diff did
not close it, it relocated it. Fix: route the line through a guarded emitter (repeat-control's `emit_err` shape)
in both tools, including the pre-existing `RuntimeError` branches. The grammar line cannot be delivered when the
stream refuses; the requirement that survives is the exit class.

### F2 (medium) — `registry-check --rev` loses its stdout report for the refusal; `--json` now returns empty stdout

`tools/registry-check.py:52-54` documents exit 2 for "could-not-evaluate (registry unreadable/invalid, root or
rev missing, **clone failure**, …)" and `:74-76` documents "`--json` machine report on stdout". Every other
could-not-evaluate cause in the same mode still emits that report; the new scratch branch returns before the
report is built.

```
$ cd $S/clone-base && TMPDIR=/nonexistent/x python3 tools/registry-check.py --rev HEAD --json
{ "error": "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/x' (could-not-evaluate)", "rev": "HEAD", "rev_resolved": "0a2010ac…", … }        # 342 B, rc=2
$ cd $S/clone-c0  && TMPDIR=/nonexistent/x python3 tools/registry-check.py --rev HEAD --json
# 0 bytes on stdout, rc=2
$ cd $S/clone-c0 && TMPDIR=/nonexistent/x python3 tools/registry-check.py --rev HEAD
# 0 bytes on stdout, rc=2   (base: "REGISTRY_CHECK: could-not-evaluate (…)", 161 B)
$ cd $S/clone-c0 && TMPDIR=/nonexistent/x python3 tools/registry-check.py --rev deadbeefdeadbeef --json
{ "error": "rev 'deadbeefdeadbeef' unavailable in …", … }        # still JSON
$ cd $S/clone-c0 && TMPDIR=/nonexistent/x python3 tools/registry-check.py --root /nonexistent --json
{ "error": "root_unavailable: /nonexistent", … }                  # still JSON
```

Verdict: the `--json` machine contract now depends on *why* the run could not be evaluated; a caller of the
documented mode gets a parseable report for a bad rev or a missing root and nothing at all for an unusable
scratch root. The C2 grammar arm checks only rc, stderr grammar and the absence of `RuntimeError`/`Traceback`
(`.ufo/evidence/round-55/c2/measure.py:198-205`), so it cannot see the loss. Fix: emit the same report (with
`error`) **and** the stderr grammar line; or amend the docstring as part of the same edit.

### F3 (medium) — the registry cells quote a tool token two of the three tools never emit; `docs=7/7` is marker-only

`tools/registry.json` cells begin `One stderr line, exit 2, could-not-evaluate: "<tool>.py: could-not-evaluate: …"`.
Actual first lines at C0:

```
repeat-control  → repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: …   (cell says repeat-control.py:)
registry-check  → registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: …   (cell says registry-check.py:)
context-capture → context-capture.py: …                                                                        (cell matches)
```

Measured the other four for context (same command shape, `2>&1 >/dev/null | sed -n 1p`):

```
bash-witness-study.py → WITNESS_STUDY: could-not-evaluate: …            (cell says bash-witness-study.py:)
pin-disposition.py    → pin-disposition.py: could-not-evaluate: …        (matches)
evidence-disposition.py → evidence-disposition.py: could-not-evaluate: … (matches)
env-diff.py           → ENVDIFF_SETUP: could-not-evaluate: …            (cell says env-diff.py:)
```

So 4 of 7 cells quote a byte shape the tool never prints, and the `docs` arm passes them because it matches a
substring (`MARKER`, `measure.py:46`) rather than the emitted line (`measure.py:248`). The counter's own
`cannot_see` only concedes "whether a caller parses the grammar by prefix or by the whole line"
(`.ufo/evidence/round-55/contract.json` C2.cannot_see) — but the cell is not a parsing question, it is a false
quotation. In-scope cells: `repeat-control-selftest`, `registry-check-selftest`.

Verdict: `docs=7/7` is a saturation claim about a marker, not about the documented line. Fix: quote the emitted
prefix (or use `<tool>:` as the note does) and make the arm compare the whole grammar against a live run.

### F4 (low-medium, pre-existing) — the run path turns a child's scratch refusal into exit 1 `differs`

Assignment question "the run path": `registry-check` live mode runs registry rows in the caller's environment, so
the row's child inherits the unusable `TMPDIR`, refuses with exit 2, and registry-check grades that as a
**verdict**:

```
$ cd $S/clone-c0 && TMPDIR=/nonexistent/x python3 tools/registry-check.py --root . --only repeat-control-selftest --json
rc=1   stdout: {"exit": 1, "held": 0, …}
       stderr: ROW repeat-control-selftest expect=0 got=2 differs
               REGISTRY_CHECK: held=0/1 superseded=0
$ cd $S/clone-c0 && TMPDIR=$S/tmp-ok python3 tools/registry-check.py --root . --only repeat-control-selftest --json
rc=0   … ROW repeat-control-selftest expect=0 got=0 held
```

The same pair exists at base (`receipts/base/rcg-live-only-unusable{.rc,.stdout,.stderr}`), so C0 did not
introduce it; but it is the documented run path, it contradicts the note's "never 1 (a verdict of
\"differs\")", and neither the counter's lazy list nor its blind-spot paragraph names it. Fix option: when a row
exits 2 and its stderr carries the frozen grammar, classify the run as could-not-evaluate (exit 2) rather than
`differs`; or document the live path as out of the class.

### F5 (low) — repeat-control still prints a class line on stdout, so the note's new sentence is false

The new note section (`corpus/knowledge/scratch-root-contract.md:99-102`, added by C0) says "the grammar is
matched on stderr, so a caller that parses stdout sees nothing." At C0:

```
$ TMPDIR=/nonexistent/x python3 tools/repeat-control.py --selftest
stdout: REPEAT_CONTROL: setup_error      (28 B)
stderr: repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: …
rc=2
$ TMPDIR=/nonexistent/x python3 tools/context-capture.py --selftest   → stdout 0 B
$ TMPDIR=/nonexistent/x python3 tools/registry-check.py --rev HEAD    → stdout 0 B
```

`setup_error` is a could-not-evaluate-family id in repeat-control's own table
(`tools/repeat-control.py:40-47`), so no false verdict is produced; but a stdout parser sees a class and it is
not `could-not-evaluate`, and the three tools are not uniform on stdout (one line vs empty). The
`could_not_evaluate` helper (`tools/repeat-control.py:228-235`) deliberately re-uses `setup_error`. Verdict:
the note sentence overstates; either emit `REPEAT_CONTROL: could-not-evaluate` (new id, same exit 2) or reword
the note to "a caller that parses stdout sees no grammar line".

### F6 (low) — the registry-check selftest hunk is behaviourally dead

Base and C0 are byte-identical for the arm the hunk targets: the pre-existing `except RuntimeError` already
printed `registry-check: could-not-evaluate: {exc}` to stderr and returned 2, and `ScratchRootUnusable`
subclasses `RuntimeError`, so the new earlier branch prints the same line and returns the same code.

```
diff receipts/base/rcg-selftest-unusable.stderr receipts/c0/rcg-selftest-unusable.stderr   # no output
cat receipts/{base,c0}/rcg-selftest-unusable.rc                                            # 2 and 2
```

Verdict: redundant branch added next to the handler that already did the job. Not harmful, but it is dead
weight in the exact handler the round is about, and it hides that the *reason* this tool already passed at base
(the base receipt has `grammar registry-check --selftest … ok`) was the generic branch.

### F7 (low, pre-existing formatter; the new byte-shape claim is what breaks) — a value containing `'` breaks the frozen grammar

The note (`:75`) and the cells freeze `TMPDIR is not a usable directory: '<value>'`, but the helper formats the
value with `%r`, which switches to double quotes when the value contains a single quote:

```
$ TMPDIR="/nonexistent/it's" python3 tools/repeat-control.py --selftest 2>&1 >/dev/null | sed -n 1p
repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: "/nonexistent/it's" (could-not-evaluate)
GRAMMAR_MATCH= False   (same for context-capture.py and registry-check)
```

The frozen `GRAMMAR` (`c2/measure.py:47-49`) requires `'.+'`, so the class line is not matched for such a
value. The counter's fixture never contains a quote, so the arm passes. Verdict: the byte shape in the note and
cells is not universal; document the exception or emit a quote-independent form.

## 3. The assignment's three questions, answered

1. **Does the new handler cover every path that can raise the scratch refusal?**
   - `repeat-control`: allocation only at `selftest()`'s `mkdtemp` (`tools/repeat-control.py:629`); `--snapshot`,
     run mode and `--help` allocate nothing (verified rc 0/0/0 under both TMPDIRs). The handler
     (`:925-926`) sits in `main`, ahead of the generic `except Exception` (`:927`); the mkdtemp is outside
     `selftest()`'s own `except Exception` (`:715`, `:893`), proven by the grammar escaping to `main`.
     **Covered.**
   - `context-capture`: allocation only in `SelftestHarness.__init__` (`:1642`), reachable only from
     `run_selftest`; handler at `:2217`, ahead of `:2222`. `--check`/`--help`/no-args never allocate.
     **Covered** (except F1's stream case).
   - `registry-check`: allocations at `:784` (`clone_lane_at_rev`, reached only from `--rev`) and `:935`
     (`selftest`); handlers at `:1851` and `:1935`, both ahead of the `RuntimeError` branches. `clone_lane_at_rev`'s
     `except OSError` (`:785`) does not catch the new `RuntimeError` subclass, so the refusal propagates as
     intended. **Covered** for the allocating modes; **not covered** for the live run path (F4).
2. **Does any change alter an exit code other than the scratch refusal?** No. Every measured exit code is
   unchanged base→C0 for normal streams (pair table, `receipts/pairs.txt`). Under a *refused* stream the refusal
   still exits 1 at both revisions (F1): context-capture and `registry-check --rev` moved that failure from the
   stdout side to the stderr side; `registry-check --selftest` and `repeat-control` are unchanged (1 and 2
   respectively).
3. **Is the exception ever swallowed by a broader handler that prints the raw type?** No in the three diffs.
   Each new handler precedes the broader one, and the observed lines carry no `RuntimeError` token. Latent: if a
   non-selftest mode of `context-capture` ever allocates scratch, `main`'s `except Exception`
   (`:2322-2327`) would print `internal_error: ScratchRootUnusable: …` into the JSON result — unreachable today
   because the only `mkdtemp` is the selftest harness.

## 4. Verdict

Wave 1's three hunks do what the counter measures — the three base grammar failures
(`repeat-control --selftest`, `context-capture --selftest`, `registry-check --rev`) now emit the stderr grammar
and exit 2 — and they leave every other measured exit code alone. They do not close the operability axis:
the refusal line itself is still unguarded (F1: whichever stream carries it, a refusing stream yields exit 1;
C0 moved the flaw from stdout to stderr), the `--json` report is dropped on one
could-not-evaluate cause while kept on the others (F2), the cells that document the line quote tokens two of the
three tools do not print (F3), the documented run path still yields exit 1 for the same environment fact (F4),
and the new note sentence about stdout is contradicted by repeat-control's own output (F5). The
registry-check selftest hunk is dead code (F6), and the frozen byte shape is not universal (F7).

## 5. Residual risk and verification gaps

- **Not run: the full `registry-check --rev` usable arm.** The registry has 49 active rows with 7 260 s of
  registered timeouts, so the success path was exercised with `--only repeat-control-selftest` (rc 0, JSON
  report, `rev_resolved=9cf0146b…`). The diff only adds a handler ahead of the clone, and the `--only` pair
  shows the success path is not perturbed, but the full 49-row run is unmeasured here.
- **Not run: the frozen C2 counter.** `.ufo/evidence/round-55/before/c2.stdout` was read as the base receipt;
  the C0-side counter run belongs to the wave's counter seats. F3's `docs=7/7` claim is therefore inferred from
  the counter source (`MARKER`-only) plus the measured first lines, not from a counter run.
- **Latent, unmeasured:** `OSError` from `mkdtemp` on a *usable* TMPDIR (ENOSPC) is a different failure than
  the refusal: repeat-control prints `setup: OSError:`, context-capture falls into the old stdout
  `SELFTEST: FAIL` branch, and `registry-check --selftest` lets `OSError` escape `main` entirely (it catches
  only `RuntimeError`) → traceback, exit 1. Pre-existing, untouched by the diff, outside the frozen grammar.
- **Not measured:** `TMPDIR` pointing at a file or a symlink-to-dir (same `isdir`/`access` branch as the
  nonexistent path, so no new class is expected).
- Registry cells for the other four tools were measured only by running their selftests at C0; no
  registry/counter cross-check was run for them.
- No tool installs or upgrades were made (recorded per the operator rule: none).

## 6. Artifacts opened

Lane at `0a2010ac…` and `9cf0146b…` (via the two shared clones): `tools/repeat-control.py`,
`tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `SKILL.md` (`## Standing rules`),
`corpus/knowledge/scratch-root-contract.md`, `.ufo/evidence/round-55/contract.json`,
`.ufo/evidence/round-55/c2/measure.py`, `.ufo/evidence/round-55/before/c2.stdout`. No frozen file, lane
production file or wave spec was modified.

Receipts under `.ufo/waves/round-55/w2/T55W2RevToolDiffs-receipts/`:

| path | what |
|---|---|
| `run-arms.sh` | the arm driver (modes × TMPDIR × revision) |
| `c0.arms.txt`, `base.arms.txt` | the driver's console output, both revisions |
| `pairs.py`, `pairs.txt` | rc / stdout-bytes / first-line table rendered from the captures |
| `c0/`, `base/` | `<arm>.rc`, `<arm>.stdout`, `<arm>.stderr` per arm |
| `devfull-matrix.txt` | stream-state matrix (stderr-full / stdout-full) for all three tools, both revisions |
| `c0/cc-devfull.strace` | ENOSPC write trace behind F1 |
| `c0/*-quoted-value.stderr` | `TMPDIR="/nonexistent/it's"` lines behind F7 |
| `c0/rcg-rev-only-usable.*` | the `--rev --only` usable pair |
| `c0/rcg-rev-devfull.stdout`, `c0/*-stderrclosed.stdout` | stream-state captures |
