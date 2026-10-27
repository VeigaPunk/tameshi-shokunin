# T51W2ExecTool09 — C3 registry row audit: `tools/pbt-staged-id.py`

Round 51 wave 2, lane `tameshi-shokunin`, base `9962033f`, candidate `6d8c11e378aa90b12650808e1b79270742935f15`.
Axis: operability. Milestone: C3 row falsification. Scope: **one row**, read-only on the lane; no source,
row or counter was modified. Every measurement below is from a `git clone --shared` of the lane at CAND
(`rev-parse --show-toplevel` = the scratch clone, verified), `TMPDIR` under the seat scratch, stdin `/dev/null`.
All bytes cited are `git show 6d8c11e…:<path>`, never the lane worktree. (During this seat the lane worktree
gained concurrent sibling edits — `M SKILL.md` at the `tally audit v3` row `:2162` and `M tools/tally-audit-v3.py`,
mtime 23:07-23:08 — which do not touch `:2150` and cannot reach my measurements because they ran against the
detached CAND clone.)

**Bottom line.** The row is **counter-conformant and substantially truthful**, and this row is **not** the
known round-21/row-16 clone-context failure (that belongs to `tools/round21-measure.py`, table row 16 /
`tools-base.json` index 16; my tool is index 9 / table row 9). I found **six falsifications**, none of which
flips the frozen predicate but three of which make a row claim that a re-running reader can contradict:

| id | severity | one line |
|---|---|---|
| F1 | **material** | the row pins `cases=35`, but the tally is environment-conditional: **34 as root**, **33 without `/dev/full`** (measured). |
| F2 | **material** | the row's self-test command omits `-I`, which the tool's own frozen interface (`:35-38`) and the round-49 counter both require; with an ambient `PYTHONPATH` the counter's own `run_row` returns `selftest-exit=1` for this row (measured). |
| F3 | **material** | the row's `1 failed (violation)` under-describes exit 1: a **hanging guard (124)** and a **crashing guard** also exit 1 and print `VIOLATION` — an environment fault is minted as a contract violation (measured, 60 s). |
| F4 | disclosure | `Pinned values: none` is true of the self-test, but the **entry** command's verdict depends on `tools/staged-id-guard.py`, whose digest the row never pins (it exists only in `.ufo/evidence/round-49/c2/panel.json`, and matches the CAND blob exactly). |
| F5 | disclosure | a green self-test is **partial** coverage: it never invokes the graded surface at all, and 1 of my 4 real mutants of the classifier survives it (measured). |
| F6 | none | my row is **not** row16's clone-context blocker; the self-test is green in a fresh clone *and* in an empty dir containing only the tool. |

---

## 0. The row under audit

`SKILL.md:2150`, inside `#### Gate/probe registry — round 51` (heading `SKILL.md:2138`, table header `:2140`);
32 data rows in the registry sections the counter scans, 30 in the round-51 section; this row is **row 9**.

```
| pbt staged-id generator | gate | `python3 tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 1 --cases 400 --dump OUT.jsonl` | 0 clean; 1 failed (violation); 2 could-not-evaluate (usage or setup) | `python3 tools/pbt-staged-id.py --selftest` → PBT_STAGED_ID_SELFTEST: cases=35 failed=0 | none — expected answers are oracle code literals in check() and the selftest; the graded surface is tools/staged-id-guard.py named by --guard | caller-chosen --dump path plus an isolated TMPDIR work root (pbt-staged-id-); selftest scratch under TMPDIR | tameshi |
```

Counter predicate (`C3` frozen at `.ufo/evidence/round-51/c3/measure.py:1-30`) for an 8-cell row: kind
`gate|probe`; entry naming `tools/T`; verdict map holding `0` **and** `1` as tokens; exactly one backticked
self-test command of argv `python3 [-I] tools/T ...selftest...` with no shell metacharacters; pinned cell
non-empty and either `none…` or every backticked path existing at REV; non-empty write scope; owner
`tameshi`; the self-test exiting 0 from a fresh clone with its **first whitespace token of the last stdout
line** present in the cell; and the usage probe (`--r51-no-such-flag`) exiting with a code that appears as a
token in the verdict map.

Reused the counter's **own** predicate functions rather than re-implementing them
(`counter-row-reason.txt`, `counter-run-row.txt`):

```
registry sections rows total: 32
rows whose ENTRY cell names the tool: [(2150, 'pbt staged-id generator')]
row_reason line 2150 -> None   spec: (['python3','tools/pbt-staged-id.py','--selftest'],
                                      ['python3','tools/pbt-staged-id.py','--r51-no-such-flag'], ...)
run_row -> (None, 'PBT_STAGED_ID_SELFTEST: cases=35 failed=0')
```

So the frozen predicate covers this row. Everything below is the independent audit the predicate does not
perform (`C3.cannot_see`: kind, write scope, pinned-value description, verdict-map completeness).

---

## 1. The row's own two commands — measured, 3 repeats each

Fixture: `git clone --shared` of the lane at CAND, `--detach 6d8c11e`, `TMPDIR=$S/tmp`, stdin `/dev/null`.

**Self-test** — `python3 tools/pbt-staged-id.py --selftest` (the row's exact backticked command):

| repeat | exit | wall | last stdout line | stderr bytes |
|---|---|---|---|---|
| 1 | **0** | 48 ms | `PBT_STAGED_ID_SELFTEST: cases=35 failed=0` | 0 |
| 2 | **0** | 50 ms | `PBT_STAGED_ID_SELFTEST: cases=35 failed=0` | 0 |
| 3 | **0** | 47 ms | `PBT_STAGED_ID_SELFTEST: cases=35 failed=0` | 0 |

35 `CASE … PASS` lines + 1 tally line = 36 stdout lines. **The row's stated literal matches the measured
last line byte for byte** in this environment (`selftest.stdout`, `selftest-repeat{1,2,3}.stdout`).

**Usage probe** — `python3 tools/pbt-staged-id.py --r51-no-such-flag`:

| repeat | exit | wall | last stderr line |
|---|---|---|---|
| 1–3 | **2** | 46 / 44 / 44 ms | `pbt-staged-id.py: error: unrecognized arguments: --r51-no-such-flag` |

Exit 2 is a token of the row's verdict map ("`2` could-not-evaluate (usage or setup)") — declared, as
PROTOCOL §Gate standard requires (`/home/vgpnk/Projects/shokunin/PROTOCOL.md:375-424`, "Verdict" bullet).

**Entry command** — `python3 tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 1 --cases 400 --dump OUT.jsonl`:

exit **0**, wall **17.2 s**, dump **400** JSONL lines, stderr empty, last line
`PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=246,indent_4_plus=31,id_4_plus_digits=31,collision=201,no_collision=62,held=48,unmapped=31,cascade=41,refusal=62,url_form_variant=30,map=106,map_inadmissible=31`
(`entry.stdout`). All twelve frozen classes ≥ `CLASS_MIN=20` → **no `SHORT` markers** (min observed 30).
Same seed twice → byte-identical dumps and identical `CLASS` lines (determinism claim at `:44` holds).
Round-49's own parameters (seed 4949, 400 cases) also exit 0 with `violations=0`.

---

## 2. Row fields against source

### 2.1 `Kind: gate` — TRUE (it genuinely fails)

PROTOCOL: "A tool that cannot fail is a probe, and is registered as one." Measured exit **1** with a
`VIOLATION` body in four independent ways:

* a stub guard returning a wrong answer → `VIOLATION index=0 exit 0, oracle expects 1`, exit 1;
* three real mutants of the graded surface taken verbatim from the committed round-49 panel
  (`.ufo/evidence/round-49/c2/panel.json`; each `old` occurs exactly once in the current blob):
  * `M01 row-indent-4` → exit 1, `VIOLATION index=18 field next_free: guard 'S012', oracle 'S002'`
  * `M04 www-kept` → exit 1, `VIOLATION index=59 field held: guard {}, oracle {'S018': 'S018'}`
  * `M05 slash-kept` → exit 1, `VIOLATION index=7 field held: guard {}, oracle {'S015': 'S015'}`

`gate` is the right classification (`probe-mutants.txt`).

### 2.2 Exit codes — the code **set** {0,1,2} is complete and correctly classed; the **meaning** of 1 is broader than the row states (F3)

Codes the tool can return, enumerated from source and confirmed by execution: `main` returns
`selftest()`→{0,1} (`:1093`), `_setup_error()`→2 (`:892-894`), `run()`→{0,1} (`:875`);
argparse's own error path exits **2**; `--help` exits 0. There is no 3, 64 or 124 exit path. So the row's
map covers every code (PROTOCOL "every other code a gate exits … is declared" — satisfied).

But exit 1 carries three distinct causes, and only one is a contract violation:

| cause | measured | tool exit | printed class |
|---|---|---|---|
| the guard's answer disagrees with the oracle | yes | 1 | `VIOLATION index=… field/exit …` |
| the **guard hangs** past `GUARD_TIMEOUT=60` (`:788` returns `{'exit':124}`) | yes, 60 s | **1** | `VIOLATION index=0 exit 124, oracle expects 1` |
| the guard is not valid Python / exits 3 | yes | **1** | `VIOLATION index=0 stdout is not one JSON object` / `VIOLATION … exit 3, oracle expects 1` |

The tool's own docstring assigns exit 2 to "setup problem (bad arguments, unreadable guard, unwritable dump
or case file, unusable work directory)" (`:40-42`) and its own comment claims "a broken environment is setup
(exit 2), never a violation with a made-up counterexample" (`:1019-1020`) — the timeout and crash paths
contradict that claim. **Consequence for the row:** `1 failed (violation)` is code-accurate
(PROTOCOL's class `failed` is right) but its parenthetical gloss asserts that exit 1 means *the graded
surface violated its contract*; a hung or non-Python guard also exits 1, so a reader who sees a red row
cannot tell a real interop defect from an infrastructure fault (`probe-exit-classes.txt`).

All setup/usage probes exit **2** as declared: missing guard, missing `--guard/--seed/--cases/--dump`,
unwritable dump (`/dev/full`), `--cases 0`, `--cases -3`, non-integer `--seed`, `--guard /tmp`,
`--dump /tmp`, unknown flag. `--help` exits 0.

### 2.3 `Pinned values: none …` — truthful for the self-test, incomplete for the entry command (F4)

The cell reads `none — expected answers are oracle code literals in check() and the selftest; the graded
surface is tools/staged-id-guard.py named by --guard`. Verified:

* **Self-test path really is self-contained.** Copied *only* `tools/pbt-staged-id.py` into an otherwise empty
  directory and ran `--selftest`: exit 0, `cases=35 failed=0`. It reads no lane file, resolves no expected
  values from disk, and its expected answers are literals inside `check()`/`oracle_case()`/`selftest()`.
  So `none` is honest for the graded surface of the **self-test**.
* **But the entry command's verdict depends on a mutable lane file whose digest the row does not pin.**
  `tools/staged-id-guard.py` at CAND is `sha256 03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`
  — exactly the `target_sha256` in `.ufo/evidence/round-49/c2/panel.json` and `GUARD_SHA` in
  `.ufo/evidence/round-49/c2/measure.py:45`. That pin lives in round-49 evidence and is **not cited by this
  row**, so the row declares `none` while its entry verdict is not reproducible against an edited guard.
  The counter cannot catch this: `measure.py:row_reason` skips *all* pinned-path checks when the cell starts
  with `none`. This is the §Gate standard "Drift pins"/"Two evidences" surface, disclosed not falsified —
  the objective evidence does exist, the row just does not point at it.

### 2.4 `Write scope` — TRUE

Row: *caller-chosen `--dump` path plus an isolated TMPDIR work root (`pbt-staged-id-`); selftest scratch under TMPDIR.*

* work root: `workspace()` → `tempfile.mkdtemp(prefix='pbt-staged-id-')` (`:807`), honors `TMPDIR`, removed
  in `finally` (`:817-818`) — after 400-case entry run, 60 s timeout run, mutant runs and every selftest,
  `$TMPDIR` residue count = **0**;
* `--dump` is written to the caller's absolute path (`os.path.abspath`, `:1114`), 400 lines;
* selftest scratch: `tempfile.mkdtemp(prefix='pbt-selftest-')` (`:1028`) under `TMPDIR`, removed in
  `finally` (`:1090`); it then rebinds `tempfile.tempdir` to a private subdir (`:1029-1031`) so its own leak
  check looks at the private tree;
* **no lane writes**: `git -C clone status --porcelain` empty after every run (checked after the entry run,
  after the mutant runs and after the repeated selftest runs); no `__pycache__` under `tools/`.

Two non-persistent, out-of-TMPDIR writes the cell does not mention (harmless, disclosed for precision): the
`dump-write-failure-is-setup` case opens `/dev/full` for writing (`:1076-1078`) and the work-root-removal
case attempts `makedirs` under `/proc/self/…` (`:1064`). Neither creates a file that survives.

### 2.5 Last-line marker — a real computed diagnostic, not author-chosen help text

`print('PBT_STAGED_ID_SELFTEST: cases=%d failed=%d' % (len(cases), failed))` at `:1092`; `failed` is
`sum(1 for _, ok in cases if not ok)` at `:1091`. This is a genuine tally of executed assertions, and it is
**not** constant: it changes when assertions fail. Mutation evidence (`probe-selftest-nonvacuity.txt`):

| scratch mutation of the tool | selftest result | reading |
|---|---|---|
| `normalise_document` keeps `www.` | exit 1, `cases=35 failed=2`, first `CASE held-form-insensitive FAIL` | caught |
| oracle returns 0 for refused analysis | exit 1, `cases=35 failed=2`, first `CASE unmapped-refused FAIL` | caught |
| classifier never adds `indent_4_plus` | **exit 0, `cases=35 failed=0`** | **survives** |
| comment-only edit (equivalence control) | exit 0, `cases=35 failed=0` | equivalent |

So the marker discriminates real regressions — but F1 below shows its *number* is not a stable pinned value,
and the surviving classifier mutant shows the self-test does not assert the twelve-class distribution at all.

---

## 3. Falsifications

### F1 (material) — the pinned `cases=35` is environment-conditional: 34 as root, 33 without `/dev/full`

`skip()` at `:1021-1022` prints `CASE <name> SKIP <why>` but **does not append to `cases`**, so
`len(cases)` at `:1092` shrinks silently while the tally still reads `failed=0`. Two skip paths exist:

* `:1038-1039` — `if os.geteuid() == 0: skip('unreadable-guard-is-setup', 'uid 0 can read a mode-000 file')`
* `:1071-1072` — `if not os.path.exists('/dev/full'): skip('dump-write-failure-is-setup', …)`

Measured:

| environment | last stdout line | exit |
|---|---|---|
| uid 1000, `/dev/full` present (this host) | `PBT_STAGED_ID_SELFTEST: cases=35 failed=0` | 0 |
| **uid 0** (`unshare -r`), `/dev/full` present | **`PBT_STAGED_ID_SELFTEST: cases=34 failed=0`** | 0 |
| uid 0 *and* `/dev/full` absent (`unshare -rm` + tmpfs on `/dev`) | **`PBT_STAGED_ID_SELFTEST: cases=33 failed=0`** | 0 |

Receipts `selftest.stdout` (1199 B, 35 `CASE` lines) vs `selftest-as-root.stdout` (1230 B, one
`CASE unreadable-guard-is-setup SKIP uid 0 can read a mode-000 file`, tally `cases=34`).

**Does this break C3?** No. `measure.py:run_row` compares only `last.split()[0]` =
`PBT_STAGED_ID_SELFTEST:` against the cell, so the count is never checked and the row is covered in all
three environments. **Does it falsify the row?** Yes, as stated: the cell asserts a specific expected output
`… cases=35 failed=0`, and a reader who re-runs as root (a routine CI identity) gets `cases=34 failed=0` and
must conclude the row is stale. The stable thing here is the finding id, not the number — the row should
either state the tally without the count or name the two conditions. Not repaired by me (no row edits).

### F2 (material) — the row's commands omit `-I`, which the tool's frozen interface requires; the omission demonstrably flips this row to MISSING

* The tool's own frozen interface, docstring `:35-38`:
  `python3 -I pbt-staged-id.py --guard GUARD --seed INT --cases N --dump FILE` / `python3 -I pbt-staged-id.py --selftest`.
* The round-49 C2 counter invokes it with isolation: `[sys.executable, '-I', gen, …]`
  (`.ufo/evidence/round-49/c2/measure.py:215`), and the guard too (`:169`).
* The row uses plain `python3` in **both** the entry and self-test cells.

C3's predicate tolerates both spellings (`python3 [-I] tools/T`), so this is not a counter failure — but the
non-isolated form is measurably breakable:

```
# ambient PYTHONPATH holding a module named random.py
PYTHONPATH=$S/shadow python3 tools/pbt-staged-id.py --selftest        -> EXIT=1, RuntimeError traceback
PYTHONPATH=$S/shadow python3 -I tools/pbt-staged-id.py --selftest     -> EXIT=0, cases=35 failed=0

# a json.py sitting beside the tool (sys.path[0] = tools/)
python3  $S/shadowdir/pbt-staged-id.py --selftest  -> EXIT=1, RuntimeError: … shadow the stdlib
python3 -I $S/shadowdir/pbt-staged-id.py --selftest -> EXIT=0, cases=35 failed=0
```

And it is not hypothetical for C3: the counter's `env()` copies `os.environ` minus `GIT_*` (`measure.py:env`),
i.e. it **passes ambient `PYTHONPATH` through**. Driving the counter's own `run_row` with that variable set:

```
counter run_row  (PYTHONPATH poisoned) -> ('selftest-exit=1 last=', '')      # row graded MISSING
counter run_row  (clean env)           -> (None, 'PBT_STAGED_ID_SELFTEST: cases=35 failed=0')
```
(`counter-run-row-poisoned-pythonpath.txt`.)

Today the row passes because this host has `PYTHONPATH` unset and no file in `tools/` shadows a stdlib name
(checked: intersection with `sys.stdlib_module_names` is empty). So the row's coverage for `tools/pbt-staged-id.py`
rests on ambient environment hygiene the row never asks for and the tool's own interface already solves.

### F3 (material) — see §2.2: a hung/crashing guard mints a "violation"

60 s hang probe, verbatim receipt:
```
EXIT=1  WALL=60s
VIOLATION index=0 exit 124, oracle expects 1
VIOLATION observed_exit=124 stdout= stderr=timeout
```
The row's `1 failed (violation)` therefore over-reads: exit 1 is *not* evidence that the graded surface
violated its contract. Per PROTOCOL the class (`failed`) is correct; the parenthetical is the falsifier.

### F4 (disclosure) — `Pinned values: none` understates the entry command's dependency

See §2.3. Guard digest at CAND = `03a796c5…c2dca8`; the pin exists in round-49 evidence and matches exactly,
but the row neither cites it nor declares the entry verdict as depending on an unpinned file. Under
`PROTOCOL.md` §Gate standard "Drift pins" / "Two evidences" this is a row-completeness gap, and it is exactly
the `C3.cannot_see` surface ("that a row's … pinned-value description [is] true of the tool"). The counter
cannot see it because a `none…` cell short-circuits `row_reason`'s path checks.

### F5 (disclosure) — a green self-test says nothing about the graded surface, and only partially about the oracle

Two independent measurements:

1. **The self-test never invokes the graded surface.** With `tools/staged-id-guard.py` replaced by
   `sys.exit(3)` the self-test still exits 0 with `cases=35 failed=0`; with the file **deleted** it still
   exits 0 with `cases=35 failed=0`; restored → same. Source agrees: `:898-900` "No real guard is needed:
   every error case refuses before the guard could answer."
2. **The classifier's class set is unasserted.** The `indent_4_plus` mutant survives the self-test
   (`cases=35 failed=0`) while changing run-mode output to `CLASS indent_4_plus=0 SHORT` on 20 cases.

So the row's `PBT_STAGED_ID_SELFTEST: cases=35 failed=0` is a legitimate capability check of the oracle and
setup paths, but it is **not** a check of the twelve classes and **not** a check of the guard. Any future
reader must not treat the green row as evidence that the generator grades correctly — that is round-49's C2
counter's job, and the row does not cite it. This is PROTOCOL's own "Self-test green is capability, not a
measurement" (`PROTOCOL.md:375-424`, "Two evidences"), stated as an observation, not a row falsehood.

### F6 (no mismatch) — this row is **not** the known round-16/row-21 clone-context blocker

The brief asked me to report row16's known clone-context failure *if* my tool is it. It is not:

* table row 16 / `tools-base.json` index 16 = `tools/round21-measure.py` (the known blocker);
* my tool = `tools-base.json` index 9, round-51 table row 9 = `tools/pbt-staged-id.py`.

Positive evidence for *my* row: the self-test exits 0 from a fresh `git clone --shared` at CAND (`selftest.stdout`,
3 repeats), **and** exits 0 in an empty directory containing only the copied tool (`isolated.stdout`), i.e.
it has no sibling-fleet or lane-tree dependency at all.

---

## 4. What holds, with no mismatch found

* `Kind: gate` — truthful, genuine exit-1 reachability (§2.1).
* Code set {0,1,2} — complete; nothing exits 3/64/124 from the tool itself; the usage probe's 2 is declared.
* Entry command — names the tool, runs clean (exit 0) on a fresh clone, 400 cases, all 12 classes ≥ 20, 17.2 s,
  deterministic across repeats, dump line count matches `--cases`.
* Self-test command — exactly one backticked command, no shell metacharacters, argv `python3 tools/T --selftest`,
  exit 0, last-line first token present in the cell.
* `Pinned values: none` — truthful for the self-test path (proved in an isolated directory).
* `Write scope` — accurate for TMPDIR work root, `--dump`, and selftest scratch; zero residue; zero lane writes.
* `Owner: tameshi` — matches the lane.

---

## 5. Risks handed to the L1 (no action taken by me)

1. **F1** makes the row's literal `cases=35` a host-conditional claim. If the deciding run executes as root,
   the last line reads `cases=34 failed=0`; C3 still passes (token-only check) but the row text and the honest
   output diverge.
2. **F2** puts this row's C3 coverage at the mercy of ambient `PYTHONPATH` / any future stdlib-named module in
   `tools/`. The fix is in the row text (`-I`), which I did not touch; the tool's own interface already
   specifies it.
3. **F3** means a red `pbt staged-id generator` verdict cannot be read as "the guard broke its contract".
   If a later deciding run ever reports this row failing, the `VIOLATION observed_exit=124`/`stderr=timeout`
   line must be read before the verdict.
4. **F4** — if a future round wants the §Gate standard "Two evidences" clause satisfied *from the row*, the
   digest `03a796c5…` (already committed in round-49 evidence and matching CAND) is the value to cite.
5. **F5** — do not count this row's green self-test as coverage of the guard or of the twelve classes; only
   the round-49 C2 counter measures those.

No row, source file, counter, or lane file was written. Report and receipts only.

---

## 6. Receipt index (`./T51W2ExecTool09/`)

| file | contents |
|---|---|
| `selftest.stdout`, `selftest.stderr` | row's exact self-test from the CAND clone: full 36-line stdout, exit 0 |
| `selftest-repeat{1,2,3}.{stdout,stderr}` | same command, 3 repeats with `</dev/null`; 48/50/47 ms |
| `usage.{stdout,stderr}` + `usage-repeat{1,2,3}.*` | `--r51-no-such-flag`: exit 2, 44-46 ms |
| `selftest-as-root.stdout`, `.stderr` | same self-test under uid 0: tally `cases=34 failed=0` (F1) |
| `entry.stdout`, `entry.stderr` | the row's 400-case entry command: exit 0, 17.2 s, per-class tally |
| `counter-row-reason.txt` | counter's `registry_rows` + `row_reason` on line 2150 → `None` (conformant) |
| `counter-run-row.txt` | counter's `run_row` on this row → `(None, 'PBT_STAGED_ID_SELFTEST: cases=35 failed=0')` |
| `counter-run-row-poisoned-pythonpath.txt` | same call with ambient `PYTHONPATH` set → `selftest-exit=1` (F2) |
| `probe-exit-classes.txt` | every reachable exit code, 1 and 2 classes, `--help`, usage probe (F3) |
| `probe-selftest-independence.txt` | broken-guard / deleted-guard / restored-guard selftest; PYTHONPATH and script-dir shadowing with and without `-I` (F2, F5) |
| `selftest-isolated-dir.{stdout,stderr}` | `--selftest` in an empty dir holding only the copied tool → exit 0, `cases=35 failed=0` (F6, §2.3) |
| `probe-guard-timeout.txt` | 60 s guard-hang probe → tool exit 1 with `VIOLATION … exit 124` (F3) |
| `probe-mutants.txt` | real round-49 panel mutants M01/M04/M05 → exit 1 `VIOLATION` (kind=gate) |
| `probe-selftest-nonvacuity.txt` | 4 scratch mutations of the tool; 2 caught, classifier mutant survives (F5) |

Scratch root `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool09/` was used for the clone, TMPDIR, mutants and
shadow trees; it is deleted before yield. No `/tmp` use beyond ephemeral `--dump` probes; no tool installs;
no git/jj mutation outside the scratch `git clone --shared` (toplevel asserted before every fixture command).
