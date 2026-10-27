# T51W2ExecTool18 — C3 registry row falsification: `tools/staged-id-guard.py`

Seat: wave-2 falsification, C3 row audit. Lane `tameshi-shokunin`.
Base `9962033fd7a75aa2f2847e979dd687a5d28505a1`; content candidate `6d8c11e378aa90b12650808e1b79270742935f15`.
Audited row: `SKILL.md:2159`, name `staged-id adoption guard` — row **18** of the 30-row
round-51 table (round-51 table rows are `SKILL.md:2142..2171`; enumerated receipt
`08-round51-row-index.txt`). **This is not row16** — row16 is `round21 measure facade`
(`SKILL.md:2157`), whose known clone-context failure I reproduced separately (see §7).

Deliverables: this report; raw receipts under `.ufo/waves/round-51/w2/@P@ExecTool18/`.
Scratch root `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool18/` (deleted at yield).
No source or row was written or repaired.

---

## 1. Verdict up front

**The row passes the frozen C3 counter's own checks — I reproduced `run_row → (None, 'VERDICT: PASS')`
from a fresh `git clone --shared` at CAND.** The row is structurally conformant and its
self-test and usage probe behave exactly as the row claims.

**But two row-text defects are real and measurable, and one is a genuine operability hole in
the tool that the row's verdict map mis-classifies:**

| # | Finding | Severity |
|---|---|---|
| **F1** | The row's verdict map mis-classifies an **uncaught `RecursionError`** that exits **1**: a map file with ≥55 000 JSON nesting levels (≈110 KB, far under the tool's own 1 MiB cap) makes `json.loads` blow the stack; the tool exits 1 with a 20-line traceback and empty stdout. Under the row's map that exit 1 reads as `failed` (a substantive refusal), when it is a **setup/parse refusal** — the class the row assigns to exit 2. The same path breaks the tool's own docstring promise "exit 2 = setup refusal (… malformed map) — **never a bare traceback**". | **material** (row text + tool) |
| **F2** | The row's **last-line marker is the generic `VERDICT:`**, shared with two other rows in the same table. The frozen counter binds to the last stdout line's first token (`measure.py:178`), so it binds to `VERDICT:`, **not** to the tool's own stable id `STAGED_ID_GUARD_SELFTEST: cases=N failed=M` (which the tool prints on stdout **line 1**, never last). I installed a mutant that prints `VERDICT: PASS` unconditionally and returns 0 into a scratch clone: **the frozen counter still returns covered**. The marker the row records is therefore satisfied by a neutered tool. | **material** (C3's finding-id evidence for this row is hollow) |
| F3 | The row's self-test is **not exhaustive** over the guard's map-validation rules: **4 of 8** mutants I wrote survive it (safe-floor computation, below-floor recording, self-map check, dedupe same-document compare). The lane's round-50 hidden panel (`H01/H03/H04`) kills the equivalent classes via the pbt generator, so the *capability* is defended elsewhere — but this row's own evidence does not show it. | observation (not a predicate violation) |
| F4 | The row's pinned-values cell self-declares `none`, so the counter's pinned-path existence check never runs on it; the expected values live **inside the file under test** (the tool's own fixture literals), with no separate digest-pinned `expected.json`. Mitigated: the tool's bytes are unchanged from base and sha-pinned at `03a796c5…` by the round-49/50 contracts. | observation |

**Nothing here changes C3's outcome for this row.** The counter passes it (§4). F1 and F2 are
defects in what the row *claims*, which is exactly the class the C3 predicate hands to wave-2
(`contract.json` C3 `cannot_see`: *"that a row's kind, write scope and pinned-value description
are true of the tool, and that the verdict map names every code the tool can exit with beyond
0, 1 and the usage code (attacked per row by wave-2 probes)"*).

---

## 2. Method (all read-only on the lane; all fixture git ops in scratch clones)

* Fixture clone: `git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin` →
  `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool18/clone`, `git checkout --detach 6d8c11e…`.
  `git rev-parse --show-toplevel` asserted to print the fixture dir before any fixture commit
  (receipt `core.txt`; `counter-probe.txt` for the counter-shaped clone at `work2/`).
* Lane repo, sibling repos, fleet root: **read-only**; no git/jj mutation. No file written
  outside my own report + receipts under `.ufo/waves/round-51/w2/`.
* All runs: `TMPDIR` inside scratch, `stdin=/dev/null`, `cwd` = the fixture clone unless stated.
* Tool bytes at CAND = `sha256 03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`,
  **identical to base** (`git diff --stat base CAND -- tools/staged-id-guard.py` is empty), and
  identical to the sha pinned in `.ufo/evidence/round-49/freeze.json` and
  `.ufo/evidence/round-50/c2/measure.py`. The tool is a frozen, unchanged capability; only the
  *registry row* is new this round.

---

## 3. The row, verbatim (SKILL.md:2159 @ CAND)

| Cell | Content |
|---|---|
| Name | `staged-id adoption guard` |
| Kind | `gate` |
| Entry command | `python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md --staged STAGED.md --json` (add `--map MAP.json` …) |
| Verdict map | `0 clean (answered, or admitted with `--map`); 1 failed (analysis refused, or map inadmissible); 2 could-not-evaluate (usage, missing flag, or setup refusal)` |
| Self-test command | `python3 -I tools/staged-id-guard.py --selftest` → VERDICT: PASS at exit 0, FAIL at exit 1 (counter line STAGED_ID_GUARD_SELFTEST: cases=N failed=M) |
| Pinned values | `none — expected values are the fixture literals SELFTEST_REGISTRY and SELFTEST_STAGED_* committed inside tools/staged-id-guard.py; no expected file on disk` |
| Write scope | `read-only: no writes, no temp files, no lane writes; caller names the registry, staged and map paths and stdout/stderr is the whole output` |
| Owner | `tameshi` |

---

## 4. Reproduction of the frozen counter's checks on this row

Using the **frozen** counter `.ufo/evidence/round-51/c3/measure.py` (sha256
`a3abbd3b7888432919a999b1de357d4b71fa7262d55ae2f5ff97be4dddb3fd3a`, the sha in
`.ufo/evidence/round-51/freeze.json`), imported as a module, no source edited:

```
rows parsed at CAND: 32   (2 from the older "### Gate/probe registry" section + 30 from the round-51 table)
--- candidate row at SKILL.md:2150  name='pbt staged-id generator'
    row_reason -> selftest-argv-not-the-tool          (rejected: its entry names --guard tools/staged-id-guard.py)
--- candidate row at SKILL.md:2159  name='staged-id adoption guard'
    row_reason -> None
    selftest argv : ['python3', '-I', 'tools/staged-id-guard.py', '--selftest']
    usage argv    : ['python3', '-I', 'tools/staged-id-guard.py', '--r51-no-such-flag']
    run_row (fresh clone, TMPDIR=scratch, stdin=/dev/null) -> (None, 'VERDICT: PASS')
```

`row_reason` passes all eight structural checks (kind ∈ {gate,probe}; entry names the tool;
verdict map contains 0 and 1; exactly one backticked self-test command, no shell metacharacters,
argv `python3 [-I] tools/T …selftest…`; pinned cell non-empty; write scope non-empty; owner
`tameshi`). `run_row` returns no failure reason.

**Row 2150 is a false-positive risk the counter handles correctly and I confirm:** the *pbt staged-id
generator* row's entry command contains `--guard tools/staged-id-guard.py`, so the counter's
substring match on the entry cell (`measure.py` `if t not in c[2]`) pairs it to this tool. It is
rejected by `selftest-argv-not-the-tool` because its backticked self-test is pbt's, not the
guard's. Worth noting for the L1: the counter's tool↔row association is a **substring** match on
the entry cell, and this table has a row whose entry cell names *another* row's tool. It happens
to resolve correctly here; it is not guaranteed to in general.

---

## 5. Exact measurements of the two commands the row names

Receipts: `core.txt`, `01-selftest.stdout/.stderr`, `02-usage.stdout/.stderr`.

### Self-test — `python3 -I tools/staged-id-guard.py --selftest`

```
$ python3 -I tools/staged-id-guard.py --selftest   (cwd=clone, TMPDIR=scratch/tmp, stdin=/dev/null)
STAGED_ID_GUARD_SELFTEST: cases=24 failed=0
VERDICT: PASS
exit=0
```

* stdout is **two lines**; the **last** non-empty line is `VERDICT: PASS`.
* Exit 0. Wall time, 3 runs: **0.039 s / 0.041 s / 0.039 s** (first run 0.032 s).
* stderr empty. Stable: 3/3 consecutive runs exit 0.
* Counter line matches the lane's own expectation from rounds 46/47/48
  (`STAGED_ID_GUARD_SELFTEST: cases=24 failed=0`, sha `03a796c5726c`) — receipt
  `.ufo/evidence/round-46/after/c1.stdout:19`. The row's `cases=N failed=M` is accurate.
* **Hermetic and clone-context-free** (unlike row16): passes with `TMPDIR` unset, with `TMPDIR`
  pointing at a nonexistent path, and from a foreign cwd with an absolute tool path. No lane
  file, no sibling repo, no network is touched by the selftest.
* The last line is `VERDICT: PASS` — a **generic** marker. See F2.

### Usage probe — `python3 -I tools/staged-id-guard.py --r51-no-such-flag`

```
usage: staged-id-guard.py [-h] [--registry REGISTRY] [--staged STAGED]
                          [--map MAP] [--json] [--selftest]
staged-id-guard.py: error: unrecognized arguments: --r51-no-such-flag
exit=2
```

* Exit **2** (argparse). stdout empty. Wall 0.038–0.039 s over 3 runs.
* **2 is declared** in the row's verdict map ("2 could-not-evaluate (usage, …)"), so the counter's
  usage-probe check (`measure.py:183` `usage-exit-%d-undeclared`) is satisfied.

---

## 6. Row fields checked against the source

Receipt: `06-entry-exit-semantics.txt`.

| Row claim | Verdict | Evidence |
|---|---|---|
| **Kind = `gate`** (a tool that cannot fail would be a `probe`) | **TRUE** | The tool genuinely fails: an unmapped colliding staged row → `verdict: refused`, **exit 1**; an inadmissible map → `verdict: inadmissible`, **exit 1**; a missing registry file → `setup_refusal`, **exit 2**. It is not a probe. |
| **Exit 0 = "clean (answered, or admitted with `--map`)"** | **TRUE** | `answered` (no collision) → exit 0; `admitted` (by-document map, `map_ok: true`) → exit 0. Both observed. |
| **Exit 1 = "failed (analysis refused, or map inadmissible)"** | **TRUE for both semantic paths, INCOMPLETE as a class** | `refused` (unmapped collision) → exit 1; `inadmissible` (`map_reasons` non-empty) → exit 1. **But an uncaught exception also exits 1** — see F1. |
| **Exit 2 = "could-not-evaluate (usage, missing flag, or setup refusal)"** | **TRUE** | usage (unknown flag) → 2; missing `--registry`/`--staged` → 2 with `staged-id-guard: --registry and --staged are required` (`tools/staged-id-guard.py:459-460`); setup refusals → 2: missing file, non-regular file (FIFO), oversized (>32 MiB), non-UTF-8, duplicate id, malformed row (<5 cells), map not JSON, map without a `map` object, duplicate JSON key, non-S-id map key, over-long S-id. All observed, no traceback in any. |
| **Self-test cell: "VERDICT: PASS at exit 0, FAIL at exit 1"** | **TRUE** | A broken expectation literal (`held == {'S002':'S999'}`) → `VERDICT: FAIL`, **exit 1**, `cases=24 failed=1`. A neutered cascade check → same. |
| **Pinned values: "none — expected values are the fixture literals SELFTEST_REGISTRY and SELFTEST_STAGED_* committed inside tools/staged-id-guard.py; no expected file on disk"** | **TRUE, and self-disclosing** | `SELFTEST_REGISTRY` at `tools/staged-id-guard.py:273`; `SELFTEST_STAGED_INDENTED` :281, `_HELD` :289, `_UNDOCUMENTED` :295, `_MALFORMED` :301. No `expected*.json` for this tool anywhere in the tree. The counter's pinned-path check is skipped because the cell starts with `none` (`measure.py` `if not pinned.lower().startswith('none')`). |
| **Write scope: "read-only: no writes, no temp files, no lane writes"** | **TRUE** | `strace -f -e trace=openat,creat,unlink,mkdir,rename` on three invocations (selftest, entry run, `--map` run): **zero** `O_WRONLY`/`O_RDWR`/`O_CREAT`/`unlink`/`mkdir`/`rename` calls. No `__pycache__`/`.pyc` anywhere in the clone. The tool never touches `TMPDIR` (it works with `TMPDIR` unset or nonexistent) — it creates no temp files at all. The only files opened are the caller-named registry/staged/map paths, read-only (`open(path,'rb')`, `tools/staged-id-guard.py:426`). |
| **Owner = `tameshi`** | **TRUE** | Lane-owned tool, committed under `tools/`. |

### Exit-1 semantics: the row is *more* accurate than the tool's own docstring

`tools/staged-id-guard.py:38-41` says *"exit 1 = the map is not admissible"* — but the tool also
exits 1 for a plain analysis refusal with **no** `--map` at all (unmapped row, or naive-map
cascade). The lane already recorded this drift at
`.ufo/evidence/round-49/contract.json:54` (*"The guard docstring names exit 1 only for an
inadmissible map: a documentation mismatch recorded for the lesson, not edited (the guard is a
pinned capability)"*). **The round-51 row states the observed behaviour, not the docstring's
stale wording** — the row is right and the docstring is the thing out of date. Not a row defect.

---

## 7. F1 (material) — exit 1 is reachable by an uncaught traceback, and the row maps it to `failed`

Receipt: `07-deep-json-crash.txt`.

`load_map` (`tools/staged-id-guard.py:441-445`) calls `json.loads` and catches only
`json.JSONDecodeError`. Python's C json scanner recurses per nesting level, so a map file with
deeply nested arrays overflows the stack and the `RecursionError` escapes `main` uncaught.

```
$ python3 -I tools/staged-id-guard.py --registry fx/reg.md --staged fx/staged_clean.md \
      --map fx/crash60k.json --json          # 120008 bytes, depth 60000
  File ".../tools/staged-id-guard.py", line 467, in main
    load_map(args.map))
  File ".../tools/staged-id-guard.py", line 443, in load_map
    return json.loads(raw, object_pairs_hook=_no_duplicate_keys)
RecursionError: Stack overflow (used 8144 kB) while decoding a JSON array from a unicode string
exit=1
```

* **stdout empty**, stderr 20 lines of traceback. Reproducible **5/5 runs** at depth 60 000.
* Threshold: no crash at depth ≤ 50 000 (100 KB); crash at depth ≥ 55 000 (110 KB). Bisected
  boundary ≈ 52 077 (≈104 KB).
* The file is **104 KB–200 KB**, i.e. an order of magnitude under the tool's own
  `MAX_MAP = 1024 * 1024` (`tools/staged-id-guard.py:70`). The size guard never fires, so the
  tool's own cap does not bound this input.
* **The tool's docstring is broken by it.** `tools/staged-id-guard.py:38-41` promises
  *"exit 2 = setup refusal (missing or non-regular file, oversized file, malformed row, **malformed
  map**) — never a bare traceback."* A malformed map is exactly this input, and it produces a bare
  traceback at exit 1, not exit 2.
* **The row's verdict map mis-classifies it.** The row maps 1 → `failed` and 2 →
  `could-not-evaluate`. This crash exits 1, so a caller reading the row (and PROTOCOL §Gate
  standard, where an undeclared code reads as could-not-evaluate) sees an internal error reported
  as a substantive *failed* verdict. The row's map cannot distinguish "the staged package is not
  admissible" (a real refusal) from "the guard itself fell over".
* Reachability: the `--map` path is caller-named and the map file is the untrusted artefact
  (a staged package's proposed adoption map). A hostile or merely malformed map reaches it.
* Scope note: this does **not** affect the C3 predicate outcome for this row — the self-test
  still exits 0 and the usage probe still exits 2 — but it makes the row's verdict map an
  incomplete description of the tool, which is precisely what the C3 contract delegates to
  wave-2 (*"the verdict map names every code the tool can exit with beyond 0, 1 and the usage
  code"*).
* The frozen tool is sha-pinned (`03a796c5…`, unchanged from base), so repairing the guard would
  move the pin that the round-49/50 counters hold. **I did not repair it and the row must not be
  edited by me**; I report it.

### F1 corollary — a second, milder gap in exit 2

`--help` exits **0** (argparse prints usage and exits 0). Exit 0 is the row's `clean` class. So
"clean" can mean *printed help*. This is generic argparse behaviour shared by every argparse tool
in the table and the counter's usage probe is `--r51-no-such-flag` (exit 2), not `--help`, so it
does not affect the predicate. Noted for completeness only.

---

## 8. F2 (material) — the row's last-line marker is generic and a neutered tool still passes the counter

Receipts: `08-marker-binding.txt`, `09-lying-mutant.txt`.

The frozen counter's finding-id rule (`measure.py:173-183`):

```python
rc, last = run_cmd(clone, work, argv, 900)      # last = LAST non-empty stdout line
if rc != 0: return 'selftest-exit=%d last=%s' ...
marker = last.split()[0] if last.split() else ''
if not marker or marker not in st: return 'finding-id-not-in-row (%s)' % marker
```

Two consequences for this row:

1. **The marker the counter binds to is `VERDICT:`**, not the tool's own finding id. The tool
   prints `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` on stdout **line 1** and
   `VERDICT: PASS` on line 2; only the *last* line is inspected. The row names both, but the
   counter consumes the second. `VERDICT:` is shared with two other rows in the same table
   (`bash declared-witness study` SKILL.md:2142, `fleet mutation runner` SKILL.md:2149).
2. **A tool that always lies passes.** I installed, into a scratch clone only, a mutant that
   replaces the verdict print and the return value with an unconditional
   `print('VERDICT: PASS'); return 0`:

   ```
   M-L mutant in clone: exit=0 last='VERDICT: PASS'
   C3 counter run_row on the LYING mutant -> (None, 'VERDICT: PASS')
   ```

   The frozen counter reports the row **covered** for a tool whose self-test can no longer fail.
   The row's recorded marker therefore does not certify what it appears to certify. The
   tool's *real* stable id — `STAGED_ID_GUARD_SELFTEST: cases=N failed=M`, which is what the
   round-46/47/48 calibration statements already observe — would not be reachable by the
   counter's last-line rule as written, but it is the id the row should be relying on.

   For scale: the same lying-mutant trick applied to the round-49/50 pbt generator
   (`PBT_STAGED_ID_SELFTEST: cases=35 failed=0`) or to any row whose marker is tool-specific
   would be caught, because those ids are unique to the tool. Only rows with a generic marker
   are forgeable this way.

---

## 9. F3 (observation) — the self-test does not cover the guard's map rules

Receipt: `mutants.txt`. Eight mutants written into scratch copies of the tool; the self-test
re-run against each.

| Mutant | Effect | Self-test |
|---|---|---|
| M-A 0-3-space extractor → column-0 only | loses indented-row collisions | **KILLED** (`cases=24 failed=9`) |
| M-B drop scheme strip in `normalise_document` | loses form-insensitive dedupe | **KILLED** (`failed=4`) |
| M-C `floor = 'S000'` | disables the safe-floor rule | **SURVIVED** (`failed=0`, exit 0) |
| M-D drop `below_floor.append(target)` | partial maps below the floor get admitted | **SURVIVED** |
| M-E drop the self-map check | a colliding id may stay on itself | **SURVIVED** |
| M-F drop the uncovered-collision check | a partial map no longer refused | **KILLED** (`failed=1`) |
| M-G drop the held-moved check | a held document may be moved off its registry id | **KILLED** (`failed=1`) |
| M-H dedupe compare drops the registry-document guard | an empty-document registry row dedupes wrongly | **SURVIVED** |

**4 of 8 survive.** The three surviving classes are exactly the ones the round-50 hidden panel
targets by other means (`H01` safe_floor, `H03` floor comparison, `H04` self-map) — killed there
via the pbt generator and the shrinker, not via this selftest. So the **capability** is defended
by the lane's mutation discipline; what the C3 row's *own* evidence shows is weaker than the
table's overall posture. This is not a predicate violation (the predicate asks the self-test to
exit 0 and print a recorded id, both true) — it is the honest answer to "are the pinned values
really load-bearing?" for this row: the pinned fixture literals bite on the analysis rules
(M-A/M-B/M-F/M-G) but not on the map-admission rules (M-C/M-D/M-E/M-H).

---

## 10. Cross-checks that came out clean

* The tool is **unchanged** from base; `sha256 03a796c5…` equals the pin in
  `.ufo/evidence/round-49/freeze.json` and `.ufo/evidence/round-50/c2/measure.py`. Only the
  registry row is new this round.
* The row's entry command runs **against the real lane registry** at CAND:
  `python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md --staged … --json` →
  `answered`, exit 0, 133 registry rows, 114 registry docs.
* Against the **real staged package** at
  `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`: `answered`, exit 0, 8
  collisions (S153–S160), 6 held (`S153→S105`, `S154→S106`, `S155→S261`, `S158→S262`,
  `S159→S155`, `S160→S156`), 0 unmapped, 0 cascade, `next_free S274`, `safe_floor S274`. A
  by-document map covering all eight collisions is **admitted**, exit 0.
* 120 randomised/adversarial inputs (malformed rows, duplicate ids, non-UTF-8, CRLF, BOM, NUL
  bytes, random bytes, wrong JSON types, over-long S-ids, oversized files, FIFOs): **exit
  histogram {0:37, 1:14, 2:69}, zero tracebacks** — the only traceback found in the whole
  campaign is the F1 recursion case, which needs ≥55 000-deep JSON.
* The F1 crash is the **only** bare-traceback path found; the tool is otherwise fail-closed as
  its docstring claims.

---

## 11. Row16 check (explicitly requested) — the known clone-context blocker is **not** this row

* **Row16 = `round21 measure facade`, `SKILL.md:2157`.** Its `--selftest` fails from a fresh
  clone: `tools/round21-measure.py` requires rev `08175c62d661fddf052ed10abc91313dec8eb77d` of
  `tools/mutate-and-run.sh`, which is not in the clone, so `git show` returns 128 and the
  selftest dies with `subprocess.CalledProcessError` → **exit 1**. Reproduced here.
* **This row (row18, `staged-id-guard.py`) does not inherit that blocker.** Its selftest is
  hermetic — inline literals only — and exits 0 from a fresh clone with `TMPDIR` in scratch and
  `stdin=/dev/null` (measured, §5). I did not find any clone-context dependency in this tool.

---

## 12. What I did not do

* Did not write or repair `tools/staged-id-guard.py` — it is sha-pinned by the round-49/50
  counters, and a repair would move that pin.
* Did not edit the registry row.
* Did not touch the lane repo, sibling repos, or the fleet root (read-only throughout; the two
  `git clone --shared` fixture trees and all mutations live in scratch).
* Did not run the C3 counter end-to-end (the L1 owns the deciding run); I exercised the frozen
  counter's own `row_reason` / `run_row` functions on this row from a fresh clone, which is the
  deciding check for this seat.

## 13. Recommendation to the L1 (no action taken)

1. **F1**: the honest fix is in the tool (catch `RecursionError`/`ValueError` in `load_map` and
   raise `Refusal`, or bound the nesting depth), which would move the `03a796c5…` pin — an L1
   decision, not a wave-2 seat's. If the pin must not move this round, the row's verdict map
   should at least not claim that exit 1 is exclusively a refusal verdict. Either way the row
   must not be edited by this seat.
2. **F2**: the row should record the tool's own stable id (`STAGED_ID_GUARD_SELFTEST: cases=N
   failed=M`) as the finding id rather than the generic `VERDICT:` — note that the counter's
   last-line rule means a marker fix alone does not bind; the fix belongs to the row *and* to
   the counter's marker rule, and the counter is frozen. Disclose rather than repair.
3. **F3**: no action; the mutation coverage gap is already carried by the round-50 panel.

---

### Receipt index (`.ufo/waves/round-51/w2/@P@ExecTool18/`)

| File | Contents |
|---|---|
| `core.txt` | clone provenance, tool sha at base/CAND, diff, round-49/50 pins, verbatim self-test + usage runs, wall times |
| `counter-probe.txt` | frozen counter imported: `row_reason` / `run_row` on this row from a fresh clone |
| `01-selftest.stdout/.stderr` | verbatim self-test output |
| `02-usage.stdout/.stderr` | verbatim usage-probe output |
| `03-strace-selftest.txt`, `04-strace-entry-run.txt`, `05-strace-map-run.txt` | strace: no writes on any path |
| `06-entry-exit-semantics.txt` | exit-code semantics (a)–(h) for the documented entry command |
| `07-deep-json-crash.txt` | F1: RecursionError reproduction, threshold bisection, 5/5 reproducibility, flat control |
| `08-marker-binding.txt` | F2: the counter's marker rule and what it binds to for this row |
| `09-lying-mutant.txt` | F2: `VERDICT: PASS`-always mutant installed in a scratch clone → counter still reports covered |
| `mutants.txt` | F3: 8 mutants × self-test outcome |
| `08-round51-row-index.txt` | row numbering of the 30-row round-51 table (row16 vs row18) |
