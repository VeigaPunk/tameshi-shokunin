# T50ExecLogger — C2 run-logger hypothesis (`c2/measure.py instrument`)

Seat: `T50ExecLogger`. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, lane HEAD at read
`4afb060c1d6e994d1bbb9095493b1f6b2b8344f2`. Read-only on the lane; deliverables written only under
`.ufo/waves/round-50/w1/`. No tool installed or upgraded (nothing needed; no pacman transaction).

## Verdict

**CONFIRMED for the counter's own invocation path; REFUTED as an unconditional "one line per guard
process and nothing else".** Every guard *process the shrinker spawns on the in-place instrumented
files* appends exactly one line and its exit/stdout/stderr/JSON are byte-identical to the
uninstrumented guard (26/26 generator runs, 12/12 public panel mutants, selftest, `--help`,
setup-refusal). Three boundaries falsify the absolute wording, and they are all conditions on the
shrinker, not on the counter: a bare **import** also logs, a **read-only** guard directory turns the
logger into a crash, and a guard **copied out of its directory** logs somewhere else than
`<shr>/.runs`.

## Bytes probed

- Counter: `.ufo/evidence/round-50/c2/measure.py`, sha256 `c3da7e59abf279db2ebf165d1a8d8298295ca234cd83b49027b9cb0b1823dfe3`;
  identical at the freeze commit — `git -C . show cdbf24c07f9be3a991997c25b1f1d4bb375014ae:.ufo/evidence/round-50/c2/measure.py | sha256sum`
  prints the same digest, and `git diff --stat cdbf24c -- .ufo/evidence/round-50/c2/measure.py` is empty.
- `INSTRUMENT`, measure.py:62-64; `instrument()`, measure.py:82-88 (anchor = first top-level line starting
  `import `/`from `, inserted *before* it, i.e. after the module docstring).
- Guard: `tools/staged-id-guard.py`, sha256 `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`
  = `measure.GUARD_SHA256`. First top-level import is `import argparse` at guard:57 (`grep -n '^import ' tools/staged-id-guard.py | head -1`).
- Generator: `tools/pbt-staged-id.py`, sha256 `0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05`
  = `measure.GEN_SHA256`; `run_guard` at generator:756-776 (`subprocess.run([sys.executable,'-I',guard,...], cwd=case_dir)`).
- Public panel: `.ufo/evidence/round-49/c2/panel.json`, sha256 `d6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda1`
  = `measure.PUBLIC_SHA256`, 12 mutants, none of whose `old` strings touch an import line.

Probe: `python3 /fast/scratch/hyaku/tameshi-r50/T50ExecLogger/probe_logger.py` (script kept as
`.ufo/waves/round-50/w1/T50ExecLogger-probe-logger.py`, sha256 `9e643d…8ded4b`); full transcript
`.ufo/waves/round-50/w1/T50ExecLogger-receipt-logger.txt` (93 lines, sections 0-14). Every case below
cites its receipt section.

## Confirmed — exactly one line, byte-identical behaviour

1. **Insertion is sound** (receipt §1). `instrument(guard_src,'p')` adds 3 lines at guard:57-59, after
   the docstring and before `import argparse`: `import os as _r50_os` / `with open(os.path.join(
   os.path.dirname(os.path.abspath(__file__)),'.runs'),'a') as _r50_fh:` / `    _r50_fh.write('p\n')`.
   `ast.get_docstring(ast.parse(instrumented))` is still non-None, `compile()` is clean, and the first
   four top-level AST nodes are `['Expr','Import','With','Import']` — the logger is module-level, not
   inside a function or a string. `instrument` cannot land inside the docstring here because no
   docstring line begins with `import `/`from ` at column 0 (guard:2-56).
2. **One line per process, both tags** (receipt §2). 13 cases = one seeded case per
   `generator:742 RECIPES` entry (`random.Random(4949)`, same shuffle as `run()`), each run through
   `gen.run_guard` with the pristine guard **and** with the mutant-tagged copy in the same directory:
   after the first run `.runs` = 1 line, after the second = 2 lines, 26/26. No case wrote 0 or ≥2 lines
   for a single process.
3. **N runs → N lines, tags clean** (receipt §3). Seven runs into one shared guard directory: 7 lines,
   tag set `{'p'}`, no partial or foreign lines.
4. **stdout/exit identity** (receipt §2). For all 13 cases the instrumented and uninstrumented guards
   agree exactly on exit code, stdout bytes, stderr bytes and parsed JSON — including the exit-1
   refusal verdicts and the two `map`-bearing cases. The mutant-tagged copy agrees with the plain
   guard too, so the tag `m` does not leak into output.
5. **`--selftest` with and without the logger** (receipt §4): `python3 -I guard --selftest` exits 0 in
   both, stdout is byte-identical (sha256 `e5bd217dcbb85eaede000f0a728e0a96f515fcd764367ca50abf2e28afea5443`,
   last line `VERDICT: PASS`), stderr identical, and the instrumented run appends **exactly one** line
   (Δ=1). `--help` and the missing-args setup refusal (exit 2, `staged-id-guard: --registry and
   --staged are required`) are likewise identical with Δ=1 (receipt §5).
6. **All 12 public panel mutants** (receipt §9): `instrument(apply_mutant(guard_src, m),'m')` compiles,
   the logger is top-level, behaviour matches the uninstrumented mutant on the probe case, and one run
   yields one line — 12/12.
7. **Read-side isolation** (receipt §14). The counter's judging legs use the *uninstrumented* copies:
   `judge = Judge(gen, vp, vm, casedir)` (measure.py:289) with `vp/vm` in `ver/`, and `find_case` runs
   `vm`. Reproducing that layout: runs from `ver/` leave `ver/.runs=0`, `case/.runs=0`, `shr/.runs=0`;
   one shrinker-style run of `shr/pristine.py` gives `shr/.runs=1`. So `logged = sum(1 for _ in fh)`
   (measure.py:284) counts *only* guard processes started from the `shr` copies, and the `cost` flag
   (measure.py:300) compares that against the shrinker's own `runs`.
8. **Durability** (receipt §13). The `with open(...)` closes inside the import, so the line is flushed
   before the guard's `main()` runs: an `exec_module` followed immediately by `os._exit(0)` still
   leaves Δ=1 line.

## Refuted — "and nothing else" fails at three boundaries

- **B1 import-only logs a line** (receipt §6): `python3 -I -c "…exec_module(<instrumented>)"` exits 0
  having run *no* guard evaluation, and appends Δ=1 line. Cause: the logger is top-level code, so
  loading the module is the event. Consequence for C2: a shrinker that `import`s the guard (instead of
  spawning `python3 -I`) in its own process logs exactly 1 line for that process while its `runs`
  counts in-process evaluations — `out['runs'] == logged` (measure.py:300) then fails on every mutant,
  turning `ok` to 0 and tripping `ok_short`/`no_reduction`. The counter cannot see this: its own
  selftest asserts only the docstring prefix (measure.py:520), never a line count.
- **B2 read-only guard directory breaks the guard** (receipt §8): with the guard's directory at mode
  `r-x`, the plain guard answers (`exit=1`, full analysis JSON on stdout, empty stderr) while the
  instrumented guard dies at import (`exit=1`, empty stdout, `json=None`, traceback on stderr naming
  `.runs`). Exit codes coincide by luck; stdout/JSON do not. So "byte-identical" holds only while
  `dirname(abspath(guard))` is writable — true in the counter's `work/mNN/shr`, false for any
  read-only or `chmod`-hardened fixture.
- **B3 copied guard logs elsewhere** (receipt §7): running a copy in another directory leaves the
  original directory's `.runs` at Δ=0 and writes 1 line into the copy's directory. Parity therefore
  requires the shrinker to invoke the exact files the counter handed it (`--pristine`/`--mutant`) in
  place; a shrinker that stages copies into `TMPDIR` would report `runs>0, logged=0` and fail `cost`.
  Relative invocation paths are safe (`cwd=guard dir, argv guard.py` and `cwd=elsewhere, argv
  ../inst/guard.py` both give Δ=1, because `abspath(__file__)` is resolved against the process cwd).
- Non-counter paths, for completeness: `instrument(instrument(src),'p')` logs **2** lines per process
  (receipt §10), but measure.py:268,270 instrument each source exactly once, so this is not reachable.
  A guard killed by a timeout still logs one line, because the write precedes `main()` in the same
  import: `logged` counts **started** processes, not completed evaluations (`GUARD_TIMEOUT = 60`,
  generator:67) — consistent only if the shrinker counts attempts the same way.

## Risks / blockers

- `tools/shrink-case.py` does not exist at my read (`ls -l tools/shrink-case.py` → No such file,
  lane HEAD `4afb060`), so the end-to-end `runs == logged` equality could not be exercised against a
  real shrinker, and B1/B3 remain latent risks for whichever shrinker lands: they cost the whole
  `cost` flag on every mutant, i.e. a total C2 miss, with no selftest signal.
- I did not read `/home/vgpnk/.local/state/` or any hidden-panel material; the hidden 8 mutants are
  out of scope here and the logger mechanics are mutant-agnostic (receipt §9 shows the anchor is
  independent of the mutant edit).
- Nothing in this item is a claim decision; the counter was run only as an imported library
  (`--selftest`/`--explain` were not needed and no deciding invocation was made).

## Summary

- Confirmed: for every guard process the shrinker spawns on the in-place instrumented copies, `.runs`
  gains exactly one line (26/26 generator runs, 7/7 batch, 12/12 public mutants).
- Confirmed: exit code, stdout, stderr and JSON are byte-identical with and without the logger
  (13 cases × 2 copies), and `--selftest` is byte-identical with Δ=1 line.
- Confirmed: the judge/find legs use uninstrumented `ver/` copies, so `logged` counts only
  shrinker-spawned guards (ver/.runs=0, case/.runs=0, shr/.runs=1).
- Refuted: a bare module import also logs a line; a read-only guard directory turns the instrumented
  guard into a traceback with empty stdout; a copied guard logs in the copy's directory.
- These are shrinker-side conditions (spawn the given files in place, writable directory), not counter
  defects; the counter's selftest (measure.py:520) cannot detect violations of them.
- No tool installs; lane untouched; probe script and 93-line transcript kept in
  `.ufo/waves/round-50/w1/`.
