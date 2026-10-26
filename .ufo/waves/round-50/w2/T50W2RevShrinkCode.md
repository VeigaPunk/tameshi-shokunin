# T50W2RevShrinkCode — source review of tools/shrink-case.py at 80ea77e9 (C2 forgery routes)

Seat: `T50W2RevShrinkCode` (reviewer, leaf, wave 2). Target: `tools/shrink-case.py` at candidate
revision `80ea77e99e239982ab0b93e416645ef2359725d3`, blob `d12481a1ab48e3a13c910633c1351c99c146a075`
(`git rev-parse 80ea77e9…:tools/shrink-case.py`; working tree `git hash-object` identical, `git status
--porcelain -- tools/shrink-case.py` empty). Shrinker line numbers below are that blob's; counter line
numbers are `.ufo/evidence/round-50/c2/measure.py` (frozen). No verdict on C2; findings only.

## Method
- Full read of the 632-line shrinker, the frozen counter, `tools/pbt-staged-id.py` (blob at same rev),
  and `tools/staged-id-guard.py`; wave-1 attack reports `T50SentinelShrink.md` F1–F12,
  `T50CritC2Contract.md` F1–F5 as the route list.
- Scratch probes (`T50W2RevShrinkCode.receipts/probe.py`, receipt-full.txt), all inside
  `/fast/scratch/hyaku/tameshi-r50/T50W2RevShrinkCode`, on copies of the REV blobs: `--selftest`
  (rc 0, 20/20 checks); run-mode on a killing case for the M02 edit with exec-counting wrappers;
  ddmin property fuzz (300 random predicates); `strace -f` syscall audit of a full run-mode invocation;
  determinism runs under differing `PYTHONHASHSEED`/`TMPDIR`; surrogate and no-kill CLI probes.
- The deciding counter was never executed; no lane, fleet, `~/.local/state`, or panel bytes read
  (the only panel read in my probes: none — the scratch fixture has no panel, selftest prints
  "skip (panel not reachable)", receipt-full.txt).

## Forgery routes — verdicts

### R1 Writes anywhere but `--out` and its own TMPDIR (`../ver/`, `.runs`, guard copies, `work/frozen-pbt.py`)? — **NO**
Write sites in shrinker code: `shrink-case.py:260` `tempfile.mkdtemp` (under the handed TMPDIR),
`:269-270` its removal, `:272-276` the `--out` write. Nothing else. `strace -f` over a full run-mode
invocation shows the complete write set of the process tree: the handed `--out` (1 create), files under
the handed TMPDIR (`shrink-case-*` workdir: registry.md/staged.md ×7 by the generator's `run_guard`,
`pbt-staged-id.py:768-783`; plus one `tempfile`-import probe file written+unlinked — CPython 3.14's
`"blat"` writability check, interpreter-internal), `.runs` ×7 appends performed by the *guard copies
themselves* (the counter's own device; in the deciding run the handed instrumented copies at
`measure.py:266-270` append to `shr/.runs` — the exact file the counter counts at `:281-284`), and my
wrappers' side log. Zero writes outside those (classify section, receipt-full.txt); the shrinker ran
with a distinct cwd and wrote nothing there; no `../ver/` path is constructed anywhere (grep: no
`pardir`/`..` outside the selftest's panel path at `:522-523`); `--pristine`/`--mutant`/`work/frozen-pbt.py`
are never opened for writing (guards only `isfile`-checked at `:251-253`).
Command: `strace -f -qq -e trace=execve,openat,open,creat,unlink,unlinkat,rename,renameat,mkdir,mkdirat,rmdir python3 -I shrink-case.py --pristine … --mutant … --case … --out …` + `receipts/classify.py`.

### R2 Reads any file it was not handed (other guard copies, lane, panel, `~/.local/state`)? — **NO on the deciding path**
Run-mode reads: the handed `--case` (`:254`), the handed guard paths (spawned as-is at `:169`), and
`pbt-staged-id.py` from its own directory (`:258`), which the interface sanctions and the counter
provides (`measure.py:227-230`). `os.path.abspath` at `:250` is lexical — it cannot substitute another
copy. The strace read set contains nothing else but interpreter/stdlib/libs: no lane paths, no
`~/.local`, no `ver/` copies, no panel (sweep: 0 hits for `shokunin|.local|panel.json|/ver/|evidence|state`,
receipt-full.txt). The one deliberate extra read is selftest leg C (`:515-525`): when
`staged-id-guard.py` sits beside the tool it reads that guard and the *public* round-49 panel to pin the
embedded M02 edit (`:528-530`). In the deciding run that leg is skipped: the counter's tooldir
receives only `shrink-case.py` + `pbt-staged-id.py` (`measure.py:225-230`), so `:518`'s isfile fails and
`--selftest` prints skip. Selftest leg C is therefore a checkout-time self-check, not a deciding-run
input, and it never approaches the hidden panel.

### R3 Precomputed answers keyed by the mutant's bytes? — **NO**
No hashing of mutant source anywhere (imports at `:30-37`: no hashlib/md5; no table, no dict keyed on
source). The only embedded panel knowledge is `M02_EDIT` (`:42-45`), referenced exclusively from
`selftest()` (`:528-530`, `:544-546`, `:553`) to build a synthetic killing case and cross-check the pin
against the public panel; the deciding entry point `run_from_arguments` (`:247-279`) cannot reach it.
Every output case is produced by the search over the handed inputs (`shrink()` `:180-211`). Wave-1's
LOOKUP attack (T50CritC2Contract Finding 2) is a *counter-surface* route — this tool does not carry it.

### R4 Strips or bypasses the counter's run logger? — **NO**
The shrinker never reads the guard sources on the deciding path (no `open` of `--pristine`/`--mutant`;
only `os.path.isfile`, `:251-253`; strace: every read-open of a guard file comes from a guard child
importing its own script (child pids 2977797/2977880/…), the main shrinker pid 2977757 has none), so it
cannot strip the three logger lines. It never references `.runs` in run mode: the only
`.runs` strings are inside the selftest's stub-guard text (`:332-333`), its own `RUN_LOGGER` template
(`:349-351`) and `logged()` (`:363-367`), all called only from `selftest()` (`:475`, `:564`) on copies
inside its own tempdirs (`:548-553`). `instrument()` is never applied to the handed paths. Every guard
invocation is `self.generator.run_guard(guard, …)` with `guard` taken verbatim from the handed paths
(`:167-169`), so the instrumented copies the counter handed over are the only things that ever execute,
and they log on every import. (Whether the *counter's* logger is forgeable is wave-1 F2/F3 — a counter
defect; this tool exercises none of it.)

### R5 Every guard run through the handed `--pristine`/`--mutant` paths? — **YES**
`Shrinker.matches` is the sole call site of `run_guard` (`:169`), selecting `self.mutant`/`self.pristine`
only (`:167`); those are exactly the abspath'd CLI arguments (`:250`, `:262`). strace: 15 `execve` of
python3 = 7 wrapper spawns (the handed paths) + 7 `execv` chains to the real copies behind them + 1
main process — the shrinker itself spawned only the handed paths. No third guard, no lane copy, no
`sys.executable` reuse tricks.

### R6 `runs` incremented exactly once per guard subprocess? — **YES**
`self.runs += 1` immediately precedes the single `run_guard` call (`:168-169`); the frozen generator's
`run_guard` spawns exactly one guard subprocess per call (`pbt-staged-id.py:786`, `cwd=case_dir`), after
writing only the case files into the caller's workdir (`:768-783`). Cache hits (`:164-166`) skip both.
Measured end to end: `out.runs=7`, `.runs` lines=7, wrapper-counted subprocesses=7 (receipt-full.txt);
selftest asserts the same equality on both its legs (`:509-510`, `:599-600`). Edge: a `SetupProblem`
inside `run_guard` before the spawn (unwritable workdir) would still have been counted — unreachable
on the honest path (fresh mkdtemp) and fail-closed anyway (exit 2, no out.json).

## ddmin and determinism review
- Chunking `:88-97` (balanced chunks, empty dropped), chunk-drop `:115-121`, complement-as-chunk
  `:122-129` (whole-set chunk skipped `:124-125`), refinement `:130-134`, and the final single-unit
  fixpoint `:136-144` which *restates* 1-minimality instead of assuming it. Deviation from canonical
  ddmin: `n = max(n-1, 2)` after a chunk-drop success (`:120`) instead of reset to 2 — affects only
  which 1-minimal set is reached, never soundness.
- Fuzz: 300 random predicates (monotone/non-monotone, floors, empty cores, n=0..25):
  0 violations of "result holds the predicate and no single unit is removable"; unsatisfiable → None;
  always-true → empty set (receipt-full.txt). ddmin itself re-asks some sets (3542 duplicate asks);
  the content cache absorbs them — sound, since `case_key` (`:69-73`) is exact content (registry,
  staged, canonical sorted JSON of the whole map object) plus role (`:164`); duplicate lines across
  different unit indices collapse to one run, which is behaviorally identical, not under-counting.
- Cost semantics honest: `kills()` short-circuits after a matching mutant (`:174-177`) — fewer runs,
  never uncounted runs; `units_before`/`units_after` computed with the same formula the counter
  recomputes (`:63-66`, `:259`, `:268` vs `measure.py:105-108`, `:292`, `:300-301`).
- Determinism: byte-identical `out.json` across `PYTHONHASHSEED=1` vs `31337` and different TMPDIRs
  (receipt-full.txt); no set/dict iteration leaks into results (frozensets used for membership only,
  `:116-118`, `:140`; JSON dict order is document order). The M02 probe case reduced 7 → 1 unit with
  the single retained staged row being the semantic 1-space-indented line the M02 regex no longer
  accepts — consistent with the counter's independent judge.

## Findings (severity ordered)
1. **Low — lone surrogate in the case crashes with a traceback, exit 1, not the documented exit 2.**
   `read_json` (`:235-244`) accepts JSON `\ud800` escapes; `valid_case` (`:76-82`) passes the string;
   the generator's `write_text` (`pbt-staged-id.py:762-764`) then raises `UnicodeEncodeError`, which is
   neither `OSError` nor `Unusable`, so `main`'s handler (`:626-628`) does not catch it — contradicting
   the docstring contract "exit 2 with a reason … for a bad … case" (`:24`). Fail-closed (no out.json;
   probe: rc=1, traceback in `receipts/surro.err`). Command: `TMPDIR=… python3 -I shrink-case.py --pristine … --mutant … --case surro.json --out …; echo $?`.
2. **Info — interpreter bytecode cache lands outside the declared write surface.** Importing the
   sanctioned generator (`:221-232`) makes CPython write `__pycache__/pbt-staged-id-*.pyc` beside it —
   in the deciding run, `work/tool/__pycache__/` (`measure.py:220-230`). Same class of write the
   counter itself performs at `work/__pycache__/` (`measure.py:201`); it feeds no counter term
   (`kills`/`minimal` are judged from `ver/` bytes at `measure.py:289`). Observed in my fixture tree;
   not a forgery channel at this revision.
3. **Info — `M02_EDIT` embeds public-panel knowledge in the tool** (`:42-45`). Selftest-only (R3),
   defensive pin, skipped in the deciding context; worth knowing when reading the diff.
4. **Info — `runs` can over-count by counting a spawn that never happened** if `run_guard` raises
   `SetupProblem` pre-spawn (`:168-169` vs `pbt-staged-id.py:782-790`); unreachable with a fresh
   mkdtemp, fail-closed otherwise.
5. **Info — `logged()` (`:363-367`) has no FIFO/regular-file guard** it uses only on its own
   selftest tempdirs; wave-1 F3's FIFO hang is a counter-side exposure, and this tool's run mode never
   reads `.runs` at all, so it adds nothing to that route.

## Residual risk and verification gaps
- The deciding invocation (`measure()` in its real harness, hidden panel, 20 mutants) was not executed
  — per bounds this seat runs no deciding counter; all probes are scratch-tree, `--selftest`, or
  run-mode-on-fixture. The hidden panel was never read; `~/.local/state` untouched.
- This review covers the shrinker *bytes at 80ea77e9* only. Wave-1's counter-side routes (F1 rewrite of
  `../ver/mutant.py`, F2 `.runs` fabrication, F3 FIFO/symlink, F5 generator poisoning) remain live
  *counter* exposures the deciding run must survive; this tool's code contains no route to any of them,
  but a hostile shrinker at another revision would still find those counter surfaces open.
- Not probed here: behavior under a mutant whose counterexample needs map entries (my fixture case was
  map-less; the unit model and `build()` `:193-205` for maps are reviewed statically and mirror the
  counter's `map_entries`/`removals`), and multi-MB case scaling (no size caps in the tool; bounded by
  the counter's 900 s timeout at `measure.py:277`).

## Summary
- All six forgery routes: NO (R1–R4, R6 verbatim no; R5 affirmative control). The tool writes only
  `--out` + its TMPDIR (syscall-audited), reads only handed inputs + the sanctioned generator, carries
  no mutant-keyed precomputation, never touches the logger, spawns only the handed guard paths, and
  counts exactly one increment per guard subprocess (7=7=7 measured).
- ddmin is sound and 1-minimal by construction (fixpoint pass) and by fuzz (300/300); output is
  byte-deterministic across hash seeds and TMPDIRs; cache is content+role keyed.
- One Low defect: lone-surrogate case → uncaught UnicodeEncodeError, exit 1 + traceback instead of the
  documented exit 2 (fail-closed). Three info notes: `__pycache__` outside declared surface (counter
  parity), selftest-only M02_EDIT pin, pre-spawn over-count edge.
- Selftest exits 0 (20/20) on the REV bytes. Tooling: nothing installed (strace/bwrap already present);
  no pacman/uv/npx call. Scratch deleted before yield; receipts in `T50W2RevShrinkCode.receipts/`.
