# T50W2ExecShrinkTrace — external run accounting for `tools/shrink-case.py` (round 50, C2)

Seat: T50W2ExecShrinkTrace. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (head
`4efa5cf57e2afcf5aea39903e3c620939dd42d01`; wave base `e3729de8`). Attacked revision:
`80ea77e99e239982ab0b93e416645ef2359725d3`. Counters were **not** run (no deciding run, no
`--explain`). No verdict on C2_R50 is offered; this is a measurement from outside the shrinker.

## Method (exact)

Tools taken from the revision under test, not the working tree:

    git -C LANE archive 80ea77e9 tools/shrink-case.py tools/pbt-staged-id.py tools/staged-id-guard.py | tar -x -C $S/rev

Digests of those bytes (`sha256sum`): `shrink-case.py 1ac31ae58d807df76d632d5eb18b06c2e62eae0428fc1fb3b2dc3f01ebb3526f`,
`pbt-staged-id.py a6e1253ad3542303ca31d66de69ccaa1caf32576c128dc6756daa332b9c8561e`,
`staged-id-guard.py 03a796c5…c2dca8` (equals the counter's `GUARD_SHA256` pin). Public panel
`.ufo/evidence/round-49/c2/panel.json` `d6dd2cf3…eeda1` (equals `PUBLIC_SHA256`). The rev generator
is **not** the frozen pin (`7d3d977f` = `0cbee392…`); as instructed this seat used the rev copy for
both the counterexample search and the shrinker's oracle.

Per mutant M01–M12 of the public panel, in scratch, with `TMPDIR` set to a scratch dir and `cwd` a
scratch dir outside the tool directory (`$S/rev` was never written except one bytecode cache, below):

1. apply the panel edit to a copy of the guard (`pristine.py`, `mutant.py`);
2. `python3 -I $S/rev/pbt-staged-id.py --guard M --seed 4949 --cases 400 --dump F`, read
   `counterexample=<i>` from the last stdout line and take the dump line with `"index": i` (the case
   verified byte-equal to the dump line on a second, independent run: `dump_case_matches=true` in
   `summary.json`);
3. `strace -f -yy -s 8192 -e trace=execve,openat,unlinkat,renameat2 -o T python3 -I $S/rev/shrink-case.py
   --pristine P --mutant M --case C --out O` (`-yy` and `-s 8192` were added to the item's trace set so
   the guard path inside `argv` and dirfd-relative paths are not truncated at strace's default 32 bytes);
4. parse `T`: a guard execution is `execve(python, ["python3","-I",<guard>,…])` — matched on `argv[2]`
   exactly, so the shrinker's own `execve` (whose `--pristine/--mutant` values also contain both guard
   paths) is not counted as a guard run.

Two further passes, both from outside: (a) the counter's own device — instrumented guards appending to
`.runs` beside the guard file (`measure.py` `INSTRUMENT`), same case, same arguments; (b) `-e
trace=execve,openat,unlinkat,write` to reconstruct each invocation's input and check for repeated cases.
One `%file,execve` completeness probe on M04 (most runs) covers mutating syscalls outside the item's
trace set. `strace` 7.2 was already installed; nothing was installed or upgraded (pacman paused).

Receipts: `.ufo/waves/round-50/w2/T50W2ExecShrinkTrace/` (`summary.tsv`, `summary.json`, `env.txt`,
`run-accounting.py`, per-mutant `case.json`, `out.json`, `out-instrumented.json`, `gen.log`,
`trace*.txt.gz` and `*-extract.txt`).

## Per-mutant accounting (all 12 public round-49 mutants found)

| id | cex index | reported `runs` | traced guard execve pristine/mutant | traced total | instrumented `.runs` | units before→after | writes outside TMPDIR/out |
|----|-----------|-----------------|--------------------------------------|--------------|----------------------|--------------------|---------------------------|
| M01 | 20 | 9 | 4/5 | 9 | 9 | 8→1 | 0 |
| M02 | 0 | 9 | 4/5 | 9 | 9 | 8→1 | 0 |
| M03 | 3 | 7 | 3/4 | 7 | 7 | 7→1 | 0 |
| M04 | 12 | 33 | 6/27 | 33 | 33 | 11→3 | 0 |
| M05 | 8 | 27 | 5/22 | 27 | 27 | 8→3 | 0 |
| M06 | 8 | 27 | 5/22 | 27 | 27 | 8→3 | 0 |
| M07 | 0 | 18 | 5/13 | 18 | 18 | 8→2 | 0 |
| M08 | 5 | 17 | 4/13 | 17 | 17 | 8→3 | 0 |
| M09 | 50 | 8 | 3/5 | 8 | 8 | 8→2 | 0 |
| M10 | 11 | 7 | 3/4 | 7 | 7 | 7→1 | 0 |
| M11 | 93 | 8 | 3/5 | 8 | 8 | 10→2 | 0 |
| M12 | 41 | 18 | 5/13 | 18 | 18 | 9→2 | 0 |
| **Σ** | | **188** | **50/138** | **188** | **188** | **100→24** | **0** |

Source: `summary.tsv` (same numbers), raw traces in each `Mxx/trace.txt.gz`.

## Findings

**F1 — the stated cost is the paid cost, as seen from outside (12/12).** `runs` in `out.json` equals
the number of `execve` of a guard path for every mutant, and the split is explained by the algorithm:
the mutant guard is executed far more often than the pristine one (Σ 138 vs 50), because
`Shrinker.kills` asks the mutant first and only asks the pristine guard when the mutant disagrees
(`tools/shrink-case.py:162-176` at `80ea77e9` counts one `runs` per uncached verdict, i.e. one
`run_guard` call). No case was executed that the shrinker did not count, and no counted verdict was
free. Reproducer over the receipts (excludes the shrinker's own `execve`, whose `--pristine/--mutant`
values contain both guard paths — a naive `grep -c` over-counts each role by exactly 1):

    zcat M04/trace.txt.gz | grep 'execve("' | grep -v 'shrink-case.py' | grep -c '"-I", "/[^"]*/guard/mutant.py"'
    # 27 mutant + 6 pristine = 33 = out.json runs (all 12 rows in summary.tsv; totals 50/138)

The matching rule is in `run-accounting.py` (`argv[2]` of the `execve` equals a guard path). The only
non-guard `execve` per run is the shrinker itself (1 each, `other_execve=1` in `summary.json`), so no
shell, wrapper or helper leaked an uncounted guard call.

**F2 — the reported `runs` also equals the counter's own instrumentation (12/12).** Re-running with
guards instrumented by `measure.py`'s logger (`.runs` appended beside the guard file) gives
`instrumented .runs == out.json runs == traced execve` for every mutant, and the two runs produce
byte-identical `out.json` (`cmp` on all 12 pairs, and `identical_out` in `summary.json`): the cost is
invariant under guard instrumentation. Commands: `cmp M04/out.json M04/out-instrumented.json` and the
`instrumented_logged_runs` column of `summary.tsv` (9,9,7,33,27,27,18,17,8,7,8,18).

**F3 — no case is run twice; `runs` counts distinct verdicts.** Reconstructing each invocation's
`registry.md`/`staged.md`/`map.json` from the traced `write`s (parent pid, last-write-wins, `unlinkat`
honoured), the triples `(role, registry, staged, map)` are **188 distinct over 188 executions**, 0
duplicates (`summary.tsv` `distinct_inputs`/`dup_inputs`). This is a strict superset of the shrinker's
cache key (which normalises the map through `json.dumps(sort_keys=True)`, `tools/shrink-case.py:69-73`),
so the verdict cache is not bypassed. Receipts: `Mxx/trace-write-extract.txt`. Caveat: this is a
reconstruction from write data, not from the shrinker's internals; a same-content duplicate would have
shown up, an aliasing bug that makes two different cases look identical would not.

**F4 — no writes outside its TMPDIR or `--out` in any of the 12 traced runs.** The write inventory
closes exactly: writes under TMPDIR = `2 × runs` (`registry.md` + `staged.md` rewritten per verdict)
`+ (map-bearing verdicts)` (`map.json`) `+ 1` (a stdlib probe file, F5). The identity holds for all 12
(`tmp_write_identity=true` in `summary.json`): e.g. M04 33 runs, all map-bearing → 33·3+1 = 100 write
opens under TMPDIR, 1 write open on `out.json`, 0 elsewhere; M01 9 runs, none map-bearing → 19 + 1.
All write opens are `shrink-case-<rand>/{registry,staged,map}.json` (+ `out.json`), all failures none
(every traced write open returns a valid fd). `unlinkat` 2–3 per run is the shrinker's `shutil.rmtree`
of its own case dir (`tools/shrink-case.py:260`, removed at `:270`). `renameat2` = 0 everywhere.
Completeness probe on M04 with `-e trace=%file,execve`: 107 mutating file events (openat 101, unlinkat
3, unlink 1, mkdir 1, rmdir 1), **0 outside TMPDIR/out** (`M04/trace-allfile-extract.txt`).

**F5 — one write outside TMPDIR/out exists, on the first import of the generator only: a bytecode
cache in the tool's own directory.** With a *fresh* copy of `shrink-case.py` + `pbt-staged-id.py` (no
`__pycache__`), one traced run of M01 shows, besides the TMPDIR writes:
`openat(… "/…/tool2/__pycache__/pbt-staged-id.cpython-314.pyc.<pid>", O_WRONLY|O_CREAT|O_EXCL|O_CLOEXEC)`
and after the run `tool2/__pycache__/pbt-staged-id.cpython-314.pyc` exists
(`M01/trace-fresh-tooldir-extract.txt`, `fresh-tooldir-pycache.txt`). Origin:
`spec.loader.exec_module(module)` of the generator beside the tool (`tools/shrink-case.py:217-230`).
In the 12 warm-cache runs above the count is 0 (`summary.tsv`), because the cache is reused; in the
counter's flow the tool dir is fresh per measurement, so the write lands in `work/tool/__pycache__`,
inside its own work dir, never in the lane. It is not load-bearing: with the tool dir `chmod 0555` the
run still exits 0 and prints the same result (`units 8 -> 1, runs 9`, no `.pyc` created, empty stderr).
Severity: benign, but the item's "writes outside TMPDIR/out must be none" is false for the first run
against a fresh tool directory and true otherwise.

**F6 — the 8-char 0600 file under TMPDIR is stdlib `tempfile.mkdtemp`, created and removed inside the
call.** It is not an artefact of the shrinker: `python3 -I -c "import tempfile;
tempfile.mkdtemp(prefix='shrink-case-')"` under the same trace shows
`openat(tmp/XXXXXXXX, O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC, 0600)`, `unlink(tmp/XXXXXXXX)`,
`mkdir(tmp/shrink-case-…, 0700)` (`tmpfile-probe.txt`). It accounts for the `+1` in F4 and for the
`unlink` event the item's trace set (`…unlinkat…`, no plain `unlink`) cannot show.

**F7 — unit counts are honest, recounted independently.** `units_before` equals this seat's own count
of the dumped case (`registry` lines + `staged` lines + `map['map']` entries) and `units_after` equals
the same count of `out.json`'s case, for all 12 (`units_after_indep` in `summary.json`); totals
100 → 24. The shrinker's stdout agrees (`shrink-case: units X -> Y, runs N`, `Mxx/gen.log`).

## What this does and does not see

- Covered: the cost field against two independent external counters (execve trace, guard-side log),
  the write surface of a full shrink run, and the no-duplicate-use claim for the public panel.
- Not covered: the hidden round-50 panel (not read, not opened; nothing under `~/.local/state` was
  read); cost on cases the public panel never reaches; whether a 1-minimal result is semantically
  meaningful; and the counter's own `Judge` re-runs after the shrink, which are not part of `runs` and
  were not traced here. No claim verdict is implied.
- The rev generator differs from the frozen pin (`a6e1253…` vs `0cbee392…`), so these counterexamples
  are the rev copy's, as the item specifies; a run that mixes the frozen generator's cases with the
  rev oracle's verdicts would be a different measurement.

Scratch root `/fast/scratch/hyaku/tameshi-r50/T50W2ExecShrinkTrace` was deleted before this report was
yielded; every cited receipt lives under
`.ufo/waves/round-50/w2/T50W2ExecShrinkTrace/`. Nothing in the lane checkout was modified
(`git -C LANE status --porcelain` showed only untracked `.ufo/waves/round-50/w2*`), and `/home/vgpnk/Projects/shokunin`
and `/home/vgpnk/Projects/shokuknow` were not touched.

## Summary

1. Reported `runs` equals the externally traced guard `execve` count for all 12 public round-49
   mutants (Σ 188 = 188 = 188 guard-side log = 188 distinct inputs); no uncounted or free verdict.
2. The mutant guard is executed 138 times vs the pristine guard's 50 — the mutant-first short-circuit,
   not a hidden cost.
3. Every write in the 12 traced runs lands under the run's TMPDIR or the `--out` path; the write
   inventory closes as `2·runs + map-bearing + 1`.
4. The one exception: the first import of the generator writes a `__pycache__` file in the tool's own
   directory (benign, tolerated when that directory is read-only, inside the counter's work dir).
5. The extra 0600 TMPDIR file is stdlib `tempfile.mkdtemp`'s probe, created and removed within the call.
6. Unit counts recount exactly (100 → 24 total) and match the shrinker's stdout.
7. Limits: public panel only, rev-copy generator, no verdict; hidden panel and `~/.local/state` untouched.
