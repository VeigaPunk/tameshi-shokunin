# T51W2ExecTool07 — independent audit of the C3 registry row for `tools/mte-interop.py`

Seat T51W2ExecTool07, round 51 wave 2 (falsify). Candidate
`6d8c11e378aa90b12650808e1b79270742935f15`; base `9962033fd7a75aa2f2847e979dd687a5d28505a1`.

Row audited: **SKILL.md:2148**, name cell `mte report interop`, data row 07 of the canonical
section `#### Gate/probe registry — round 51` (heading SKILL.md:2138; 30 data rows at
SKILL.md:2142-2171). Read-only on the lane; every run in
`git clone --shared --no-checkout` at CAND under
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool07/clone`, `TMPDIR=$S/tmp`, stdin `/dev/null`.
Raw receipts: `.ufo/waves/round-51/w2/@P@ExecTool07/` (numbered files, indexed in §11).

## Verdict on operability

**The row is operably true at CAND and the frozen C3 counter covers it.** The row's exact
backticked self-test exits 0 with a real finding id on the last stdout line, the usage probe exits
a code the verdict map declares, both vendored pins are load-bearing and their digests match the
committed bytes, the tool is a genuine gate (it fails), and the row's write-scope claim that the
lane is read-only holds under every run I made.

**Four row-level defects are measured below, plus two cross-surface findings.** None of them makes
the C3 predicate fail for this row, and three of the four sit on things the C3 counter never reads.
Ranked by what matters for the round's own claims:

1. **The verdict map does not cover the tool's crash path** (§6, material): an uncaught exception
   exits **1**, which the row maps to `failed`, although nothing was graded. The sibling row for
   `tools/registry-replay.py` in the same table (SKILL.md:2155) discloses exactly this
   ("an uncaught traceback also exits 1"); row 2148 does not.
2. **The write-scope cell omits one TMPDIR tree** (§5, minor): the tool creates a bare
   `tameshi-mte-<rand>` node_modules staging tree (`tools/mte-interop.py:199`) that the cell's
   list does not name.
3. **The pinned-values cell mis-attributes `REGRESSION_TABLE` counts** (§7, minor): those counts
   are emitted at run time and arrive over stdout, not embedded in the pinned runner file.
4. **The Self-test cell overstates negative-control coverage** (§1, minor): 14 of the 17 checks
   are negative controls, 2 are positive controls and 1 is a location assertion.

The two cross-surface items are the lane-wide `--help` → exit 0 convention (§6, shared by sibling
rows, so not counted against this row) and the stale `mte-interop-check` needle in
`tools/registry.json` (§8, pre-existing at base, outside the C3 predicate).

**This is not row 16.** The known clone-context blocker belongs to row 16 of the table
(SKILL.md:2157, `tools/round21-measure.py`), not to this row; §4 measures it to confirm the
attribution.

## 1. The row's own commands, exits, last lines and wall times (the item's required receipt)

Executed from the fresh `--shared` clone at CAND, `TMPDIR=$S/tmp`, stdin `/dev/null`:

| run | argv | exit | last stdout line | wall |
|---|---|---|---|---|
| row self-test | `python3 tools/mte-interop.py --selftest` | **0** | `MTE_SELFTEST: 17/17 pass` | **0.18 s** |
| usage probe | `python3 tools/mte-interop.py --r51-no-such-flag` | **64** | *(stdout empty)* stderr `mte-interop.py: error: one of the arguments --check --selftest is required` | **0.04 s** |

Both are three orders of magnitude inside the counter's 900 s / 60 s limits. The self-test is
stable: three consecutive runs each printed `MTE_SELFTEST: 17/17 pass` (receipt 01, and the
stability loop). It is also independent of the interpreter's `jsonschema` version and of the
`uv` wrapper the row's *entry* command uses: `uv run --no-project --with jsonschema==4.25.1 …
--selftest` → exit 0 `17/17 pass`, and the same under `jsonschema==4.20.0` → exit 0 `17/17 pass`.

The printed tally is exact. `tools/mte-interop.py:405-421` holds 16 case rows of which
**14 expect `want=False`** (negative controls) and **2 expect `want=True`** (`conforming`,
`emitter-inconclusive-to-runtimeerror`), plus one `emitter-locations` case (tool:429) — 17 checks,
matching the printed `17/17`.

**Minor wording defect (finding 4 of 4).** The row's Self-test cell calls the 17 *"the committed
negative controls"*, but only 14 of the 17 are negative controls: two are positive controls (they
assert that a conforming report is **accepted**) and one is a location assertion, not a control at
all. The denominator and the pass count are right; the label overstates negative-control coverage.
I verified by walking the `cases` list with `ast` and reading each entry's `want` flag; the 14/2
split is also visible in the tool's own output (receipt 01), which prints
`CASE conforming PASS` and `CASE emitter-inconclusive-to-runtimeerror PASS` alongside the fourteen
`want=False` cases.

## 2. The frozen C3 counter accepts this row

I replayed the frozen counter's own row logic against the row rather than reasoning about it.
`measure.py` was imported from `.ufo/evidence/round-51/c3/measure.py`; its sha256
`a3abbd3b7888432919a999b1de357d4b71fa7262d55ae2f5ff97be4dddb3fd3a` equals the `freeze.json` pin,
so the bytes I exercised are the frozen bytes:

```
MATCH_ROW_LINE 2148
ROW_REASON None
SPEC_ARGV  ['python3', 'tools/mte-interop.py', '--selftest']
SPEC_USAGE ['python3', 'tools/mte-interop.py', '--r51-no-such-flag']
RUN_ROW_WHY None
RUN_ROW_LAST 'MTE_SELFTEST: 17/17 pass'
```

`row_reason()` returning `None` means every one of the counter's structural checks passes for this
row: kind is `gate`, the entry cell names `tools/mte-interop.py`, the verdict map carries both `0`
and `1` as tokens, the self-test cell holds exactly one backticked command whose argv is
`python3 tools/mte-interop.py --selftest` with no shell metacharacters, every backticked pinned
path exists at CAND, the write scope is non-empty, and the owner is `tameshi`. `run_row()` then
confirms the two behavioural halves: the self-test exits 0 from the clone and its finding id
`MTE_SELFTEST:` is in the row's Self-test cell, and the usage probe's 64 is declared in the verdict
map. Receipts: `rowcheck.py` (reusable), `14-…`, and §7.

I also ran the **whole** frozen counter at CAND (receipt 25). It names my row covered and puts the
round's single miss on row 16:

```
C3_TOOL tools/mte-interop.py: covered line 2148 selftest exit=0 last=MTE_SELFTEST: 17/17 pass
C3_TOOL tools/round21-measure.py: MISSING (line 2157 selftest-exit=1 last=)
C3_R51: rev=6d8c11e378aa90b12650808e1b79270742935f15 tools=30 rows=32 covered=29 missing=1 \
        deleted=0 selftest_fail_rows=2 total=1 C3_R51_PASS=false
```

`selftest_fail_rows=2` is the counter's own accounting for the two row evaluations that failed
inside `run_row` (both belong to `round21-measure`); my row contributes neither. So
`C3_R51_PASS=false` at CAND is the **already-disclosed** round-21-measure clone-context blocker,
not any defect of row 2148 — which is exactly what §4 verifies independently.

## 3. The tool is a real gate, not a probe

PROTOCOL §Gate standard: "A tool that cannot fail is a **probe**, and is registered as one." I
could make this gate fail four different ways, so `kind: gate` is truthful:

| experiment | exit | last stdout line |
|---|---|---|
| synthetic kept-regression workdir, all ten legs conforming | **0** | `MTE_INTEROP: PASS legs_conforming=10/10` |
| same workdir with one leg's recorded verdict flipped | **1** | `MTE_INTEROP: FAIL legs_conforming=0/10` |
| `judge()` neutered (`failed = []` always) → selftest | **1** | `MTE_SELFTEST: 3/17 pass` |
| nine-leg workdir (`bash-drift-pins` removed) | **2** | `MTE_INTEROP: SETUP (leg set … differs from the ten ledger legs …)` |

Receipts 03 (clean), 04 (flipped), 05 (neutered judge), 16 (nine legs). The gate's own `--check`
path is therefore not vacuous: it distinguishes a conforming leg set from a mutated one and refuses
a leg set that is not the ten the runner records.

Against the **real** fleet the gate is green at CAND and the entry command is green:
`uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root
/home/vgpnk/Projects/shokunin` → exit **0**, `MTE_INTEROP: PASS legs_conforming=10/10`, wall
**182.78 s** (receipt 10; repeated run exit 0 in receipt 18/09).

## 4. This is not row 16 — the clone-context blocker belongs elsewhere

The task asks me to include row 16's known clone-context failure if my tool is it. It is not.
Row 16 of the table is SKILL.md:2157, `tools/round21-measure.py`. Its self-test from a fresh
clone of the lane fails exactly as disclosed, because its fixture expects sibling fleet repos:

```
$ python3 tools/round21-measure.py --selftest          # from the CAND clone
exit=1
subprocess.CalledProcessError: Command '['git', '-C', '.../clone/kumitate-shokunin', 'show',
  '175de6ba…:scripts/kimi-census.mjs']' returned non-zero exit status 128
```

Receipt 15. `tools/mte-interop.py --selftest` needs no sibling repo, no fleet root and no network:
it runs green from the same clone (§1). So the C3 blocker on this row is zero, and the row is
covered by the counter.

## 5. Write scope — one TMPDIR tree is undeclared (mismatch, minor)

The row's write-scope cell reads:

> caller-chosen `--workdir`/`--emit` DIR plus isolated TMPDIR trees `tameshi-mte-selftest-*`,
> `tameshi-mte-fleet-*`, `tameshi-mte-regression-*`; lane read-only

I instrumented `tempfile` (a `sitecustomize.py` hook on `mkdtemp`/`TemporaryDirectory`) and
recorded every tree the tool actually creates (receipt 14):

```
mkdtemp prefix='tameshi-mte-selftest-'  -> …/tameshi-mte-selftest-ufy7jh1r     tool:386  (declared)
TemporaryDirectory prefix='tameshi-mte-' -> …/tameshi-mte-od34x82j              tool:199  (UNDECLARED)
```

`tools/mte-interop.py:199` stages the extracted npm `node_modules` for the official metrics
library in a bare `tameshi-mte-` tree. It is created by **both** `--selftest` and `--check`
(the metrics computation is on the selftest path too), it matches none of the three globs the cell
lists, and it is the tree that holds the extracted `mutation-testing-metrics` package. The live
`--check` path additionally creates `tameshi-mte-fleet-*` (tool:276, the staged fleet) and
`tameshi-mte-regression-*` (tool:309, the kept regression workdir) — both declared.

The **lane read-only** half of the cell holds: after every run, including three live
`--check --fleet-root /home/vgpnk/Projects/shokunin` runs against the real fleet, the clone's
`git status --porcelain` is empty (receipts 09/10/18 show the runs; the clone tree was re-checked
afterwards and is clean), and the fleet-side `git status` diff before/after my window contains
only *other* lanes' concurrent round-48/53/54 work — the runner materialises each leg from the
sibling repo's git object store (`git show <rev>:<path>`, runner:1276) and never writes a sibling
tree. The tool's own writes stay inside TMPDIR and the caller-named `--workdir`/`--emit` dirs:
`tools/mte-interop.py:280` copies the runner into the staged fleet, `:288` writes
`regression.stdout` into the workdir, `:338-342` writes the `--emit` artefacts, `:386-392` the
selftest fixture.

**Severity: minor.** The tree is inside TMPDIR and is removed with the process, so nothing escapes
the declared scope; the cell is an incomplete enumeration, not a wrong one.

## 6. Verdict map — the crash path is undeclared (mismatch, material)

The row's verdict map is:

> 0 clean; 1 failed; 2 could-not-evaluate (setup); 64 could-not-evaluate (usage)

I enumerated every exit-producing site in the tool (`return` at 299/324/347/357/398/430/444, plus
`Parser.error` → `exit(64)` at 447-450). The map covers 0, 1, 2 and 64 correctly — but the tool
has a fifth outcome that the map does not name: **an uncaught exception**. Python exits **1** for
an unhandled exception, so a crash is indistinguishable by exit code from a graded failure, and it
is the code the row maps to `failed`.

Two reachable crash paths, both from the gate's own `--check` mode:

| crash | exit | stdout | stderr |
|---|---|---|---|
| `<leg>/sweep.log` unreadable (`tool:331` `sweep_log.read_text()` is outside the `try` at 296-323) | **1** | stops mid-leg list, **no** `MTE_INTEROP:` verdict line at all | `PermissionError: [Errno 13] …` traceback |
| `--emit DIR` not writable (`tool:338` `out.mkdir(parents=True)` is outside the `try` at 296-323) | **1** | stops mid-leg list, **no** `MTE_INTEROP:` verdict line | `PermissionError: [Errno 13] …` traceback |

Receipts 08 (both stdout and stderr). In both cases the last stdout line is a `MTE_LEG … CONFORMS`
line — a reader that keys on the verdict line sees no verdict at all, and a reader that keys on the
exit code sees `failed`.

PROTOCOL §Gate standard requires that "every other code a gate exits (2, 3, 64, …) is declared in
its registry entry and mapped onto clean | failed | could-not-evaluate, and an undeclared nonzero
code reads as could-not-evaluate". Here the code is *declared*, but its **meaning** is wrong for
this path: `1` means `failed` in the row, yet on this path nothing was failed — the gate could not
evaluate. The lane already knows this shape: the sibling row for `tools/registry-replay.py` in the
same table (SKILL.md:2155) says "… an uncaught traceback also exits 1" inside its `1 failed` cell.
Row 2148 omits the equivalent clause. A one-clause fix restores the map's truth.

Note this is a **documentation defect in the row, not a C3 predicate failure**: the frozen counter
checks only that the verdict map contains `0` and `1` and that the usage probe's code is declared
(`measure.py` `row_reason()`/`run_row()`), so it cannot see this.

Two smaller notes on the same cell:

* `--help` exits **0** (argparse's default) — a request that graded nothing returns the `clean`
  code. This is a lane-wide argparse convention, not specific to this row
  (`tools/golden-verdict.py`, `tools/pin-disposition.py`, `tools/shrink-case.py` behave the same,
  receipts 17 and the equivalent probes), so I do not count it against this row.
* `2 could-not-evaluate (setup)` is accurate for the setup conditions I could reach: missing
  `jsonschema` (exit 2, "No module named 'jsonschema'"), missing `node` (exit 2, "node not found"),
  vendor-tarball integrity mismatch (exit 2), leg-set mismatch (exit 2), and `regression exit 2`
  (exit 2). Receipts 20/21/06/E2/16.

## 7. Pinned values — load-bearing, digests match, with one scoping nuance

The row's pinned-values cell names `tools/mutate-and-run.sh` (for its embedded `TABLE_*` recorded
per-defect verdicts and `REGRESSION_TABLE` counts) and the two vendored tarballs (for their
`npm dist.integrity` sha512 literals in the tool).

* **The two vendor pins are load-bearing for the row's own self-test.** Appending one byte to
  `tools/vendor/mutation-testing-report-schema-3.9.0.tgz` in a scratch copy turns the self-test
  into exit 2, `MTE_SELFTEST: SETUP (mutation-testing-report-schema-3.9.0.tgz integrity mismatch)`
  (receipt 06); the same for `mutation-testing-metrics-3.9.0.tgz` → exit 2, `SETUP (… integrity
  mismatch)` (receipt E2 / verify_log). `tools/mte-interop.py:176-182` recomputes the digest and
  refuses on mismatch.
* **The digests in the row's cell are true of the committed bytes.** I recomputed
  `base64(sha256… )` of each committed blob at CAND and compared it with the literals at
  `tools/mte-interop.py:64` and `:66` — both match exactly (verify_log E4).
* **Scoping nuance (disclosure, not a defect):** the runner pin is load-bearing for the **check**
  path but **not** for the **self-test** path. Changing `TABLE_DRIFTPINS` in a scratch copy of
  `tools/mutate-and-run.sh` leaves `--selftest` at `17/17 pass` exit 0, while `--check` over the
  same workdir flips to exit 1 `MTE_INTEROP: FAIL legs_conforming=9/10` (receipt 07). The row's
  cell does not claim the self-test depends on the runner — its Self-test cell names the tool and
  the finding id only — so the cell is accurate; I record the asymmetry because a reader could
  otherwise assume the selftest exercises the pinned runner.
* **A third, smaller wording imprecision (minor, disclosure).** The cell says the runner carries
  "embedded `TABLE_*` recorded per-defect verdicts **and `REGRESSION_TABLE` counts**". The
  `TABLE_*` half is exact: `tools/mte-interop.py:228-235` reads them out of the runner file's
  `TABLE_\w+='…'` literals (`tools/mutate-and-run.sh:634-643`), and that is what the `per_mutant`
  check compares against. The `REGRESSION_TABLE` counts are **not** embedded in the runner file —
  the runner *emits* those lines at run time (`tools/mutate-and-run.sh:1392`), and the tool parses
  them from the regression **stdout** (`tools/mte-interop.py:313-314`,
  `TABLE.finditer(stdout)`). `git show CAND:tools/mutate-and-run.sh | grep -E "REGRESSION_TABLE
  (js|bash)-"` matches nothing: no leg's `REGRESSION_TABLE` line is a file literal. What the
  runner file *does* embed is the expected-count panel (`tools/mutate-and-run.sh:2038-2047`, e.g.
  `'bash-drift-pins:bash-drift-pins.spec:TABLE_DRIFTPINS:10:2'`), which is a different thing
  again. So the cell's parenthetical attributes to the pinned file a value that in fact arrives
  over stdout at run time. The pinned *path* is still correct and load-bearing for the check path
  (receipt 07), so the C3 predicate is unaffected; the wording is what is off.

### Pinned-value summary

| pinned path (row's cell) | exists at CAND | load-bearing for the row's **self-test** | load-bearing for the row's **entry command** | cell wording |
|---|---|---|---|---|
| `tools/mutate-and-run.sh` | yes | no (receipt 07) | yes — `TABLE_*` verdicts drive `per_mutant` (receipt 07) | partly off: `REGRESSION_TABLE` counts arrive over stdout, not from the file |
| `tools/vendor/mutation-testing-report-schema-3.9.0.tgz` | yes | yes — exit 2 `integrity mismatch` (receipt 06) | yes | accurate |
| `tools/vendor/mutation-testing-metrics-3.9.0.tgz` | yes | yes — exit 2 `integrity mismatch` (verify_log E2) | yes | accurate |

## 8. Cross-surface staleness found next door (not the C3 predicate, but the same tool)

`tools/registry.json` (byte-identical base → CAND) still carries an active row for this same tool
whose expectation the candidate tool can no longer satisfy:

```
tools/registry.json:1011-1019
"name": "mte-interop-check", "kind": "gate",
"argv": ["uv","run","--no-project","--with","jsonschema==4.25.1","python3","tools/mte-interop.py","--check"],
"expect": {"exit": 0, "stdout_contains": ["MTE_INTEROP: PASS legs_conforming=9/9"]}
```

At CAND the tool prints `MTE_INTEROP: PASS legs_conforming=**10/10**` (ten legs:
`tools/mte-interop.py:78` adds `bash-drift-pins`/`TABLE_DRIFTPINS`, and the tool's own error text
says "the ten ledger legs", `tool:318`). Replaying the lane's own monitor:

```
$ python3 tools/registry-check.py --rev 6d8c11e3… --only mte-interop-check --json
"expect": 0, "got": 2, "held": false,
"stdout_missing": ["MTE_INTEROP: PASS legs_conforming=9/9"],
"stdout_tail": "MTE_WORKDIR: … \nMTE_INTEROP: SETUP (regression exit 2)\n"
REGISTRY_CHECK: held=0/1 superseded=0        (exit 1)
```

Receipts 11 (candidate) and 12 (base). The **same row also differs at base**, with the same
missing needle and the same `regression exit 2` — so the `9/9` needle was already stale before
round 51 and the tenth leg did not introduce it. The CAND tool additionally changed the sibling
`mte-interop-selftest` row's world: `tools/registry-check.py --root . --only mte-interop-selftest`
→ `ROW mte-interop-selftest expect=0 got=0 held` (receipt 13), i.e. the selftest registry row is
green. The round-26 registry row at SKILL.md:2136 likewise still says "the nine ledger legs" and
"`mte-interop-check` (9/9)".

This is outside the frozen C3 predicate (which reads only the SKILL.md round-51 table), but it is
the same tool and the same registry-home topic, so it is worth the L1's attention: the ten-leg
change propagated into `tools/mte-interop.py` and into `tools/mutate-and-run.sh` but **not** into
`tools/registry.json` nor into the older SKILL.md:2136 row.

## 9. What I did not do

I did not write to the lane, to any sibling repo, or to any fixture outside my own scratch; I did
not modify `tools/mte-interop.py`, `tools/mutate-and-run.sh`, `tools/registry.json` or SKILL.md;
and I did not attempt to repair the row — the two mismatches in §5 and §6 are reported as
findings, not fixed. The only files this seat wrote are this report and the raw receipts under
`.ufo/waves/round-51/w2/@P@ExecTool07/`.

Scratch was confined to `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool07/` with an explicit
`TMPDIR` under it; the two `/tmp/tameshi-mte-*` trees the tool left behind (one failed run kept
its workdir) were removed, and the lane's clone stayed clean throughout.

## 10. Recommendation

The row stands for C3 purposes: the counter accepts it, the self-test is green and stable, the
gate really fails, and the pins bite. Two edits would make it fully true, both inside the cell the
row already owns:

1. In the Verdict map cell, extend the `1 failed` class with the crash clause the sibling
   `registry-replay` row already carries (e.g. "1 failed (an uncaught exception also exits 1)").
2. In the Write scope cell, name the fourth TMPDIR tree the tool creates — the bare `tameshi-mte-*`
   node_modules staging tree at `tools/mte-interop.py:199`.

Neither is required for `C3_R51_PASS`; both are required for the registry row to be *accurate*,
which is what the round-51 registry section claims to deliver.

## 11. Raw receipts index

All under `.ufo/waves/round-51/w2/@P@ExecTool07/`:

| file | content |
|---|---|
| `01-selftest.stdout` / `.stderr` | row self-test, CAND clone, exit 0, `MTE_SELFTEST: 17/17 pass` |
| `02-usage.stdout` / `.stderr` | usage probe `--r51-no-such-flag`, exit 64 |
| `03-gate-synthetic-clean.stdout` | synthetic 10-leg workdir → exit 0 `PASS legs_conforming=10/10` |
| `04-gate-synthetic-flip.stdout` | one leg's recorded verdict flipped → exit 1 `FAIL legs_conforming=0/10` |
| `05-mutant-neutered-judge.stdout` | `judge()` neutered → selftest exit 1 `3/17 pass` |
| `06-tampered-vendor-tarball.stdout` | schema tarball tampered → selftest exit 2 integrity mismatch |
| `07-tampered-runner-check.stdout` | `TABLE_DRIFTPINS` tampered → check exit 1 `FAIL legs_conforming=9/10` |
| `08-unreadable-sweep-log.stdout` / `.stderr` | unreadable `sweep.log` → exit 1, no verdict line, traceback |
| `09-live-check-fleet-root.stdout` | live `--check --fleet-root <fleet>` at CAND → exit 0 `PASS 10/10` |
| `10-entry-command-uv.stdout` | the row's literal entry command → exit 0 `PASS 10/10`, wall 182.78 s |
| `11-registry-check-mte-row-candidate.json` | `registry-check --rev CAND --only mte-interop-check` → differs |
| `12-registry-check-mte-row-base.json` | same at base → also differs (pre-existing) |
| `13-registry-check-selftest-row.out` | `registry-check --root . --only mte-interop-selftest` → held |
| `14-tmpdir-tree-inventory.log` | instrumented `tempfile` inventory of the tool's TMPDIR trees |
| `15-row16-round21-selftest-clone-context.stdout` | row 16 (`round21-measure.py`) clone-context failure |
| `16-nine-leg-workdir-rejected.stdout` | nine-leg workdir → exit 2, "differs from the ten ledger legs" |
| `17-help-exit0.stdout` | `--help` exits 0 |
| `18-live-check-second-run.stdout` | second live run → exit 0 `PASS 10/10` |
| `19-base-live-check.stdout` | live `--check` at base → exit 2 `SETUP (regression exit 2)` |
| `20-node-absent-selftest.stdout` | node removed from PATH → selftest exit 2 `SETUP (node not found)` |
| `21-jsonschema-absent-selftest.stdout` | `python3 -S` → selftest exit 2 `SETUP (No module named 'jsonschema')` |
| `22-live-check-third-run.stdout` | third live `--check` run → exit 0 `PASS 10/10` |
| `23-verification-log.txt` | condensed item-by-item verification log (A–I) |
| `24-tampered-metrics-tarball.stdout` | metrics tarball tampered → selftest exit 2 integrity mismatch |
| `25-c3-counter-full-run.txt` | whole frozen C3 counter at CAND: this row covered, row 16 missing, `total=1` |
| `26-emit-unwritable.stdout` / `.stderr` | `--emit DIR` not writable → exit 1, no verdict line, `PermissionError` traceback |
| `27-entry-command-uv-timed.stdout` | the row's literal entry command, timed → exit 0, wall 182.78 s |
| `rowcheck.py` | reusable replay of the frozen counter's `row_reason()`/`run_row()` on this row |
| `mkworkdir.py` | builder for the synthetic kept-regression workdirs used in §3 |
