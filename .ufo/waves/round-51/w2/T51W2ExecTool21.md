# T51W2ExecTool21 — C3 registry row audit: `tools/tally-audit.py`

**Seat:** T51W2ExecTool21 (executor, axis operability, milestone C3 row falsification)
**Lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
**Base:** `9962033fd7a75aa2f2847e979dd687a5d28505a1` · **Candidate audited:** `6d8c11e378aa90b12650808e1b79270742935f15`
**Row audited:** `SKILL.md:2162`, canonical section heading `#### Gate/probe registry — round 51` at `SKILL.md:2138`
**Method:** read-only on lane/fleet/sibling repos; `git clone --shared --no-checkout` at CAND in scratch `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool21/clone`; explicit `TMPDIR`; `stdin=/dev/null`; no fixture git operation (no commit was needed), so no `rev-parse --show-toplevel` race. No source or row was modified. No tool installed (none needed).
**Raw receipts:** `.ufo/waves/round-51/w2/T51W2ExecTool21/` (mirrored at `@P@ExecTool21/`).

---

## 0. Verdict in one line

**The row is runnable and truthful in its kind, entry, self-test, pinned-value, write-scope and owner cells; its verdict map is falsified in one clause:** `64 could-not-evaluate (runner usage error surfaced through --then-regression)` does not describe the tool — a runner usage error surfaces as **2**, and the shipped runner never makes the tool exit 64 at all. The frozen C3 predicate still accepts the row (usage probe exits 2, which the map declares), so this is a registry-accuracy defect of exactly the kind the contract's C3 `cannot_see` names, disclosed here rather than concealed. C3_PASS is not killed by this row.

Measured from the clone at CAND: self-test `exit 0`, last line `TALLY_AUDIT_SELFTEST: 11/11 pass`, **13.69 s**; usage probe `--r51-no-such-flag` `exit 2`, stdout empty, stderr last line `tally-audit.py: error: unrecognized arguments: --r51-no-such-flag`, **0.03 s**; default entry (audit the runner beside the tool) `exit 0`, last line `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)`, **1.27 s**.

---

## 1. Row under test (candidate bytes)

`SKILL.md:2162`:

```
| tally audit undercount guard | gate | `python3 tools/tally-audit.py` audits the runner `tools/mutate-and-run.sh` beside it; `--runner PATH`, `--then-regression --workdir DIR` accepted | 0 clean; 1 failed; 2 could-not-evaluate (cannot audit, usage, or regression SETUP); 64 could-not-evaluate (runner usage error surfaced through --then-regression) | `python3 tools/tally-audit.py --selftest` → TALLY_AUDIT_SELFTEST: 11/11 pass | `tools/tally-audit.py` REF_BLOCK reference tally block and leg-name panel are literals in the tool; audited `tools/mutate-and-run.sh` read-only | TMPDIR scratch dirs with prefix tally-audit, removed on exit; --then-regression hands its workdir to the runner | tameshi |
```

Only one row in the whole SKILL names this tool (checked by importing the C3 counter's own row parser: `rows naming tools/tally-audit.py: [(2162, 'tally audit undercount guard')]`), so there is no competing older row.

Environment: `Python 3.14.8`, `GNU bash 5.3.20(1)`, `git 2.56.0`; clone HEAD `6d8c11e3…`; audited runner `sha256 977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda` (matches the sha named in the tool's own REF_BLOCK comment, `tools/tally-audit.py:47`, "runner at sha256 977de470…0bda (round 51, lines 1510-1548)").

---

## 2. Required runs (clone at CAND, scratch TMPDIR, stdin /dev/null)

| # | command (exactly as row / predicate) | exit | last stdout line | wall |
|---|---|---|---|---|
| 1 | `python3 tools/tally-audit.py --selftest` | **0** | `TALLY_AUDIT_SELFTEST: 11/11 pass` | 13690 ms |
| 2 | `python3 tools/tally-audit.py --r51-no-such-flag` | **2** | (no stdout) stderr last: `tally-audit.py: error: unrecognized arguments: --r51-no-such-flag` | 30 ms |
| 3 | `python3 tools/tally-audit.py` (default entry) | **0** | `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)` | 1270 ms |

Run 1 prints 11 `CASE … PASS (exit N)` lines, all PASS, then the marker. All 11 case exits match their seeds (`pristine`/`reversed operands` 0, the nine fault cases 1) — `tools/tally-audit.py:399-437`.

Run 3 details, showing the gate is live at CAND (the tenth C2 leg was wired into the panel, per amendment 2):

```
CHECK static PASS legs=10 operands=10 nlegs=10
CHECK runtime PASS vectors=358 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=29/29
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
```

Run 2's `2` is a token in the row's verdict map (`2 could-not-evaluate (cannot audit, usage, or regression SETUP)`), which is what the counter checks. The row's declared `2` is therefore exact: argparse usage errors, `CannotAudit` and regression SETUP all return 2 (`tools/tally-audit.py:452-453`, `:390-392`).

---

## 3. Field-by-field verification against source

| Cell | Row claim | Source evidence at CAND | Verdict |
|---|---|---|---|
| Name / kind | "tally audit undercount guard", `gate` | The tool computes a verdict and **fails** on a real tally defect: scratch copy of the runner with `nlegs=9` → `TALLY_AUDIT: FAIL`, exit 1, `CHECK static FAIL`/`runtime FAIL`/`harness FAIL` (probe P1). A tool that cannot fail would be a probe (PROTOCOL §Gate standard, fleet `PROTOCOL.md:375`); this one can. | **TRUE** |
| Entry command | `python3 tools/tally-audit.py` audits `tools/mutate-and-run.sh` beside it; `--runner`, `--then-regression --workdir` accepted | Default runner is `os.path.join(HERE, 'mutate-and-run.sh')` with `HERE = dirname(abspath(__file__))` (`tools/tally-audit.py:42,442`); flags declared at `:443-445`. Default run 3 audits the beside-it runner and passes. Workdir handoff observed: shim runner logging `$*` prints `ARGV: --regression --workdir /fast/scratch/.../mut/wd` on stderr; tool exit 0 (probe P5). | **TRUE** |
| Verdict map `0` | clean | `audit()` returns 0 iff all three CHECKs pass (`:371-378`); selftest returns 0 iff 11/11 (`:437`). Run 1 and run 3 exit 0. | **TRUE** |
| Verdict map `1` | failed | `audit()` returns 1 when any CHECK fails (`:378`); selftest returns 1 on a failed case (`:437`). Probes P1/P2 exit 1. | **TRUE** |
| Verdict map `2` | could-not-evaluate (cannot audit, usage, or regression SETUP) | `CannotAudit`/`OSError`/… → `TALLY_AUDIT: SETUP`, 2 (`:452-453`); argparse usage → 2 (run 2); regression SETUP (`:390-392`) → 2 (probe P3). `/dev/null` as `--runner` → `TALLY_AUDIT: SETUP (run_regression() not found)`, 2 (probe P6). | **TRUE** |
| Verdict map `64` | "could-not-evaluate (runner usage error surfaced through --then-regression)" | **Falsified — see §4 F1.** A runner usage error prints no `REGRESSION:` line, so `then_regression` takes the SETUP branch and returns **2** (`:390-392`), not 64. 64 is reachable only when the runner prints a `REGRESSION:` line *and* exits 64 (`:394`), which the shipped runner never does: its four REGRESSION print sites exit 1, 2, 2, 0 (`tools/mutate-and-run.sh:1523,1529,1538,1548`). Its usage path exits 64 at `tools/mutate-and-run.sh:247-250` — but through this tool that path is absorbed as 2. | **FALSE (cause + reachability)** |
| Self-test cell | exactly one backticked command `python3 tools/tally-audit.py --selftest`; marker `TALLY_AUDIT_SELFTEST: 11/11 pass` | Command is one backtick pair, no shell metacharacters; runs 11 cases and exits 0 (run 1). The marker is emitted only at `:436`, after the case loop, and appears **0 times** in `--help` output — it is a real finding id, not author-chosen help text; a failure changes the count and exit (`:436-437`). | **TRUE** |
| Pinned values | `tools/tally-audit.py` REF_BLOCK reference tally block and leg-name panel are literals; audited `tools/mutate-and-run.sh` read-only | Both named paths exist at CAND. `REF_BLOCK` (`:49-88`) and `REF_NAMES` (`:89-90`) are literals, and they decide the verdict: a scratch tool copy whose REF_BLOCK says `nlegs=11` makes the harness reject the reference block → `CHECK harness FAIL`, exit 1 (probe P2). The runner is only read (`open(...,'r')`, `:359`, and an awk extraction of the runner in a bash subprocess); its digest is unchanged after every run. | **TRUE** |
| Write scope | TMPDIR scratch dirs with prefix `tally-audit`, removed on exit; `--then-regression` hands its workdir to the runner | `tempfile.mkdtemp(prefix='tally-audit.')` / `prefix='tally-audit-selftest.'`, `shutil.rmtree` in `finally` (`:364,372,419,435`). After the runs, every scratch `TMPDIR` directory is empty (`find` → 0 entries) and `/tmp/tally-audit*` is absent; clone `git status --porcelain` is empty; the runner sha256 is unchanged (read-only claim true). Workdir handoff observed in P5. The `$TMPDIR/h.XXXXXX` harness subdirs live inside the `tally-audit.*` tree and are removed with it. | **TRUE** |
| Owner | tameshi | literal | **TRUE** |

Conformance summary: 7 of 8 cells verified true against source; the verdict-map cell is half-true (`0/1/2` exact, `64` falsified).

---

## 4. Findings

### F1 (the falsification): the verdict map's `64` clause is wrong on cause and cannot occur with the shipped runner

Row text: `64 could-not-evaluate (runner usage error surfaced through --then-regression)`.

`then_regression()` (`tools/tally-audit.py:381-394`) runs `bash RUNNER --regression [--workdir DIR]`, then looks for `^REGRESSION: (PASS|FAIL|SETUP) \(cases=(\d+)` in **stdout**. If the line is missing or the case count differs from the legs found, it prints `TALLY_AUDIT_REGRESSION: SETUP (REGRESSION line missing or cases != N legs found)` and returns **2** (`:390-392`). Only when the line is present does it return the runner's exit code (`:394`).

The runner's usage errors take `usage_exit()`, which prints usage to stderr and `exit 64` **before** any `REGRESSION:` line is printed (`tools/mutate-and-run.sh:247-250`; the REGRESSION print sites are `:1523,1529,1538,1548` and exit 1/2/2/0). Measured on the shipped runner bytes at CAND: `bash tools/mutate-and-run.sh --regression --workdir` → exit **64**, stdout **0 bytes** (0 `REGRESSION:` lines), stderr first `mutate-and-run: --workdir needs a value`, last `1 done-with-inconclusive · 2 setup/refusal · 64 usage.` (receipt `usage-runner.out/.err/.rc`). Fed through `--then-regression` this is exactly the missing-line case (receipt `usage-runner.*`); empirical proof, on a scratch runner that exits 64 on `--regression` with no REGRESSION line (probe P3):

```
CHECK static PASS legs=10 operands=10 nlegs=10
CHECK runtime PASS vectors=358 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=29/29
TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)
TALLY_AUDIT_REGRESSION: SETUP (REGRESSION line missing or cases != 10 legs found)
exit 2
```

So "runner usage error surfaced through --then-regression" is exactly the branch that returns 2 — the row already maps that situation under `2` ("regression SETUP") and then contradicts itself with the 64 clause. 64 is reachable only in the unnatural case where a runner prints a REGRESSION line and *then* exits 64 (probe P4: `TALLY_AUDIT_REGRESSION: PASS (cases=10 legs=10 exit=64)`, exit 64). With the shipped runner the tool's code space is exactly `{0,1,2}`.

Impact:
- **C3 predicate: none.** The usage probe exits 2; 2 is declared. The counter's own `row_reason`/`run_row` accept the row (§5). C3_PASS is not harmed by this row.
- **Registry accuracy: defect.** PROTOCOL §Gate standard (fleet `PROTOCOL.md:375`, Verdict bullet) requires every other code a gate exits to be declared and mapped; this entry additionally states a cause for 64 that the code does not implement. A reader who believes the row would infer that a runner usage error surfaces as 64 and mis-grade a manual `--then-regression` run as an undeclared code instead of SETUP. The honest entry is either to drop the 64 clause or to say "64 only if the runner prints a REGRESSION line and exits 64 (not the shipped runner)". **Not repaired** (seat bounds: advisory only).
- The sibling row for `tools/tally-audit-v2.py` handles the analogous case correctly ("a timed-out then-regression reports 124 and folds to 2"), which is the convention this row departs from.

### No other row-field mismatch found

- Kind `gate` is defensible under PROTOCOL's definition (reads a surface, compares against repo-persisted expected values, returns a verdict, and fails — P1).
- The self-test is green in the clone with scratch TMPDIR in 13.69 s and the last line is byte-equal to the row's recorded marker.
- The pinned literals are load-bearing (P2), both named pinned paths exist, and the audited runner is read-only (digest and clone status unchanged).
- Write scope is accurate and clean on exit.

---

## 5. Counter cross-check (what the frozen C3 predicate sees)

Imported `.ufo/evidence/round-51/c3/measure.py` read-only and applied its own `row_reason()` and `run_row()` to this row against the clone (receipt `counter-crosscheck.txt`):

```
rows naming tools/tally-audit.py: [(2162, 'tally audit undercount guard')]
row_reason: None
selftest argv: ['python3', 'tools/tally-audit.py', '--selftest']
usage argv: ['python3', 'tools/tally-audit.py', '--r51-no-such-flag']
verdict map cell: 0 clean; 1 failed; 2 could-not-evaluate (cannot audit, usage, or regression SETUP); 64 could-not-evaluate (runner usage error surfaced through --then-regression)
run_row: None | last: TALLY_AUDIT_SELFTEST: 11/11 pass
=> COVERED
```

So the row is covered by the counter; F1 is invisible to it, as the contract's C3 `cannot_see` already predicted ("that the verdict map names every code the tool can exit with…"). This is disclosed, not concealed.

---

## 6. Other falsification probes (scratch copies; lane untouched)

| Probe | Fixture (exact mutation) | Result |
|---|---|---|
| P1 | runner copy, unique real tally declaration (`runner:1510`) `local nlegs=10 …` → `=9` | exit 1; `CHECK static FAIL legs=10 operands=10 nlegs=9; nlegs=9 but 10 legs assigned`; `CHECK runtime FAIL … mismatched=358`; `CHECK harness FAIL`; `TALLY_AUDIT: FAIL` — the gate truly fails |
| P2 | tool copy, `REF_BLOCK` first line (`tool:49`) `nlegs=10` → `nlegs=11` | exit 1; `CHECK static PASS`, `CHECK runtime PASS`, `CHECK harness FAIL harness rejects or cannot run the reference block ((9, 8))` — the pinned literal really affects expected behavior |
| P3 | runner shim: `--regression` → `exit 64` (no REGRESSION line) | audit PASS, then `TALLY_AUDIT_REGRESSION: SETUP …`, exit **2** — refutes the row's 64 cause |
| P4 | runner shim: `--regression` → print `REGRESSION: PASS (cases=10 …)`, `exit 64` | exit **64**, `TALLY_AUDIT_REGRESSION: PASS (cases=10 legs=10 exit=64)` — the only 64 path |
| P5 | runner shim: `--regression` → print `ARGV: $*` to stderr, print `REGRESSION: PASS (cases=10 …)`, exit 0; invoked `--then-regression --workdir mut/wd` | exit 0; stderr `ARGV: --regression --workdir /fast/scratch/…/mut/wd` — workdir handoff true |
| P6 | `--runner /dev/null` | exit 2; `TALLY_AUDIT: SETUP (run_regression() not found)` — cannot-audit mapping true |

Fixtures are exactly described in `fixtures.txt` and are one-line copies of the CAND blobs; they were deleted with the scratch root.

---

## 7. Known blockers that do **not** apply

This is not the known row16-style clone-context failure (`tools/round21-measure.py`, whose `--selftest` expects sibling fleet repos and exits 1). `tools/tally-audit.py --selftest` reads only the runner beside it in the clone, uses no fleet sibling, and is green in 13.69 s. C3's known blocker is not hit by this row.

## 8. Risks / disclosure

1. **F1** is a documentation-accuracy defect in a registry cell that the frozen predicate cannot test (it only requires the probe's own exit code to be a token). If the L1 closes C3 without repairing it, the round notes should record that the `64` clause was falsified by wave 2.
2. `then_regression()` propagates the runner's exit code whenever a REGRESSION line is present (`:394`), so with a non-shipped `--runner` the tool's true code space is `{0,1,2} ∪ {runner exit}`; the row declares only 64 of those and for the wrong cause. With the shipped runner only `{0,1,2}` occur — the row's `0/1/2` mappings are complete and exact.
3. Operability is otherwise intact: the row's self-test is a real 11-case gate over the runner's tally block, not a probe, and reproduces in a clone with no side effects (clean TMPDIR, clean clone, unchanged runner digest).

## 9. Artifacts

`.ufo/waves/round-51/w2/T51W2ExecTool21/` (mirrored under `@P@ExecTool21/`):
`selftest.out`, `selftest.err`, `usage.out`, `usage.err`, `audit.out`, `audit.err`, `probe-nlegs9.out/.err/.rc`, `probe-refblock.out`, `probe-usage64.out/.err`, `probe-pass64.out`, `probe-workdir.out/.err`, `probe-cannot-audit.out/.err`, `usage-runner.out` (shipped runner usage run: 0 bytes), `usage-runner.err`, `usage-runner.rc` (64), `counter-crosscheck.txt`, `fixtures.txt`, `timings.txt`, `commands.txt`, `environment.txt`, `row-text-line2162.txt`.

Nothing was installed or updated. Scratch root deleted before yield.
