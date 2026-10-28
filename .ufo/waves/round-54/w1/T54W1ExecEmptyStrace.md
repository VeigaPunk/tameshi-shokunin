# T54W1ExecEmptyStrace — empty `TMPDIR` reaches the platform default (mkdir audit)

Seat: `T54W1ExecEmptyStrace` (attack item, lane `tameshi-shokunin`, round 54 wave w1).
Item: under `TMPDIR=""`, run each of the seven self-tests under
`strace -f -e trace=mkdir,mkdirat -o LOG` and report the mkdir paths each tool used;
show the paths, state whether any tool silently allocated under the working directory,
and report the seven (tool, exit, first mkdir path) triples.

## Environment and method

- Lane HEAD / deciding revision: `59c38109bf119d0e9d4f878644a82babc937bc1e` (`git -C <lane> rev-parse HEAD`).
- Work copy: `git clone --shared` of the lane into scratch, checked out at that revision.
  `git -C <clone> rev-parse --show-toplevel` printed the clone dir before any checkout;
  `git -C <clone> status --porcelain` was empty before and after every run.
- The tool list is **the frozen counter's**, not mine: both drivers load `TOOLS` from
  `.ufo/evidence/round-54/c2/measure.py` at that revision via `importlib`, so argv and
  self-test names are the counter's own mapping:
  `registry-check.py --selftest`, `env-diff.py --selftest`, `bash-witness-study.py selftest`,
  `evidence-disposition.py --selftest`, `pin-disposition.py --selftest`,
  `context-capture.py --selftest`, `repeat-control.py --selftest`.
- Arm: `TMPDIR=""` (empty, declared = unset), `PYTHONDONTWRITEBYTECODE=1`, cwd = clone.
- strace 7.2 (`strace --version`).
- Run 1 = the item's exact command per tool:
  `env TMPDIR= strace -f -e trace=mkdir,mkdirat -o <log> python3 <tool> <arg>`
  (driver `driver.py`, summary `run1-summary.json`).
- Run 2 = same arm, plus `-y` and `chdir,fchdir` tracing so every relative path is resolved
  against the traced cwd of that pid (`driver2.py`, summary `run2-summary2.json`). The
  resolver was validated first on a synthetic fixture (a `chdir` case and a
  `subprocess(cwd=...)` case both resolved to the directories actually created); see
  "Resolution validation" below.

## The seven triples (run 1, the item's exact command)

| # | tool | exit | first mkdir path | mkdir calls |
|---|---|---|---|---|
| 1 | registry-check | **1** | `/tmp/tameshi-r17-registry-check-selftest.wcb10a0m` | 238 |
| 2 | env-diff | 0 | `/tmp/tameshi-r21-envdiff.jvm1ryol` | 625 |
| 3 | bash-witness-study | 0 | `/tmp/bash-witness-selftest-private.39cb0p61` | 72 |
| 4 | evidence-disposition | 0 | `/tmp/tameshi-r14-evidence-disposition-selftest.9ykcc_i7` | 1965 |
| 5 | pin-disposition | 0 | `/tmp/tameshi-r13-pin-disposition-selftest.l9s8tmm8` | 96 |
| 6 | context-capture | 0 | `/tmp/context-capture-selftest-mak8_p02` | 48 |
| 7 | repeat-control | 0 | `/tmp/tameshi-r12-repeat-control-selftest.qzipmx73` | 44 |

Raw per-tool strace logs: `run1-<tool>.log`, child stdout/stderr `run1-<tool>.out`.

The single exit 1 is **not** a scratch-root result: see Observation O1. Every first mkdir of
every tool is a `mkdtemp`/`TemporaryDirectory` under `/tmp` — the platform default — which is
exactly what the empty arm declares.

Run 2, same arm, resolved (`run2-<tool>.log`):

| tool | exit | mkdir calls | resolved under `/tmp` | private-namespace / other | resolved under the clone | unresolved |
|---|---|---|---|---|---|---|
| registry-check | 1 | 238 | 238 | 0 | **0** | 0 |
| env-diff | 0 | 625 | 238 | 387 | **0** | 0 |
| bash-witness-study | 0 | 72 | 72 | 0 | **0** | 0 |
| evidence-disposition | 0 | 1968 | 1968 | 0 | **0** | 0 |
| pin-disposition | 0 | 96 | 96 | 0 | **0** | 0 |
| context-capture | 0 | 48 | 48 | 0 | **0** | 0 |
| repeat-control | 0 | 44 | 44 | 0 | **0** | 0 |

## Verdict: did any tool silently allocate under the working directory?

**No, for all seven, in the declaring environment (`/tmp` usable).** Three independent checks:

1. **Path resolution, not string matching.** Run 1 shows many mkdir arguments that are
   relative (``.git/objects/57``, `newroot`, `dev`, `/tmp`-fixture internals). Run 2 resolves
   each against the traced cwd of the calling pid: of the relative mkdirs, registry-check 25,
   env-diff 92 (plus 387 inside bwrap's private mount namespace), bash-witness-study 21,
   evidence-disposition 506, pin-disposition 39 all resolve under `/tmp` fixtures created by
   the same run; context-capture and repeat-control issue no relative mkdir at all. None
   resolves under the clone.
2. **Working-tree immutability.** The run-1 directory listing of the clone (15,297 entries,
   `.git` excluded) is byte-identical before and after all seven runs
   (`run1-tree-before.txt` / `run1-tree-after.txt`; `diff -q` clean, TREE_ADDED=0
   TREE_REMOVED=0), and `git -C <clone> status --porcelain` stayed empty.
3. **The resolver is sound.** Validated on a fixture before use: `chdir(fix1)` + `mkdir("a")`
   resolved to `fix1/a`, `subprocess(..., cwd=fix2)` + `mkdir("b")` resolved to `fix2/b`, an
   absolute mkdir resolved unchanged, and all three directories existed afterwards.

The declared arm's mechanism also checks out: with `TMPDIR=""`,
`tempfile._candidate_tempdir_list()` is `['/tmp', '/var/tmp', '/usr/tmp', <cwd>]` and
`tempfile.gettempdir()` is `/tmp` (probeA) — the empty value is skipped by the resolver,
exactly as `corpus/knowledge/scratch-root-contract.md` states (S278).

## Observations (reported, not fixed)

### O1 — registry-check's exit 1 under strace is a wall-clock assertion, not the arm

`tools/registry-check.py` case `timeout-kills-setsid-pipe` / `timeout-kills-setpgid-pipe`
asserts, besides exit 1 / no survivor / no marker, `elapsed < 3.5` s (registry-check.py
around the `run_escape_case` block). Under ptrace that threshold is missed while every other
condition holds:

```
SELFTEST_CASE timeout-kills-setsid-pipe FAIL (exit=1 elapsed=3.917s survivor=False marker=False)
SELFTEST_CASE timeout-kills-setpgid-pipe FAIL (exit=1 elapsed=4.049s survivor=False marker=False)
SELFTEST: FAIL (2 of 51 cases: ...)
```

Four strace runs of the same command all exit 1 (elapsed 3.8-4.2 s in the two sweeps,
7.5 s / 11.3 s in two later reruns as host load rose —
(`registry-check-strace-rerun1/2.out`). The same command **without** strace passed 6/6 across
all three arms (empty, unset, usable; `registry-check-no-strace-arms.txt`), and the contract's
own before line (`unusable_exit2=3 docs=0 note=0 sources=0 total=13`) leaves zero deficit for
`usable_ok` by arithmetic (4 + 7 + 1 + 1 = 13), i.e. 7/7 under strace at the base measurement.
Conclusion: host-load/tracer perturbation of one tool's timing assertion, independent of
`TMPDIR`.

**Consequence for C2:** the counter's *usable* arm is a strace arm and counts
`rc == 0 and hits == 0`. A deciding run made under load can therefore lose `usable_ok` by one
on registry-check alone and print `C2_R54_PASS=false` for a reason unrelated to scratch
roots. That is an operability risk in the instrument, not a defect in the seven tools.
Measured, not inferred: 4/4 strace runs fail here; 6/6 non-strace runs pass.

### O2 — the empty arm's "platform default" can itself be the working directory

`strict_scratch_root()` returns `tempfile.gettempdir()` for `TMPDIR=""`, and Python's
resolver list ends with the cwd and `.`. On a host where the `/tmp` candidates are unusable,
the empty arm therefore allocates under the working directory silently — the outcome the
knowledge note attributes to "a tool that treated `""` as a path". Demonstrated with bwrap
(`--ro-bind / / --dev /dev --ro-bind EMPTY /tmp --ro-bind EMPTY /var/tmp --bind <cwd> /srv
--chdir /srv`):

```
$ env TMPDIR= bwrap ... python3 -c '...'
cwd /srv
candidates ['/tmp', '/var/tmp', '/usr/tmp', '/srv']
gettempdir /srv
```

and the real self-test in the same sandbox, `TMPDIR=""`:

```
inner-rc=0
SELFTEST: PASS (29 cases)
mkdir("/srv/tameshi-r12-repeat-control-selftest.m0u6fu5b", 0700) = 0
mkdir("/srv/tameshi-r12-repeat-control-selftest.m0u6fu5b/fixtures", 0777) = 0
mkdir("/srv/tameshi-r12-repeat-control-selftest.m0u6fu5b/out", 0777) = 0
mkdir("/tmp" ...): 0 occurrences
```

So the *declared* empty arm is satisfied on any normal host (this one: `/tmp`, all seven),
but "the platform default applies" is not a guarantee against working-directory allocation;
it inherits `tempfile`'s cwd fallback when the temp roots are exhausted. Worth a one-line
bound in the note or the registry cell ("platform default; Python's last candidates are cwd"),
but it does not falsify any C2 arm as written, and no fix was attempted here.

### O3 — env-diff's non-`/tmp` mkdirs are inside bwrap's private mount namespace

`env-diff` runs its fixtures through `bwrap`, which after `chdir("/tmp")` creates
`newroot`/`oldroot` under `/tmp` (platform default), pivots into them and then mkdirs `/proc`,
`/newroot/dev{,/shm,/pts}`, `/newroot/tmp/w` inside its own mount namespace. Host checks
after the runs: `/newroot`, `/oldroot`, `/tmp/newroot`, `/tmp/oldroot` all absent (`ls -ld`,
"No such file or directory"), and `mkdir("/proc") = 0` is only possible in a private root.
387 of env-diff's 625 run-2 mkdirs are these namespace-internal calls; the remaining 238 are
the `/tmp` fixture. Nothing is created outside `/tmp` on the host.

## Resolution validation (how run 2's numbers are trustworthy)

```
$ cd <scratch>/val && env TMPDIR= strace -f -y -e trace=mkdir,mkdirat,chdir,fchdir -o log \
    python3 child.py fix1 fix2      # child: chdir(fix1); mkdir a; subprocess(cwd=fix2) mkdir b; mkdir /tmp/…
669055 mkdir AT_FDCWD a -> <scratch>/val/fix1/a ret 0
669188 mkdir AT_FDCWD b -> <scratch>/val/fix2/b ret 0
669055 mkdir AT_FDCWD /tmp/val-abs-yt -> /tmp/val-abs-yt ret 0
unresolved []
$ ls -d fix1/a fix2/b /tmp/val-abs-yt   → all three exist
```

A pid that reached its cwd via `fchdir(fd)` is marked unresolved rather than guessed; run 2
had zero unresolved mkdirs across all seven tools.

## Receipts

All under `.ufo/waves/round-54/w1/T54W1ExecEmptyStrace-receipts/`:

- `driver.py`, `driver2.py` — run 1 and run 2 drivers (tool list imported from the frozen counter).
- `run1-summary.json`, `run2-summary2.json` — per-tool exits, mkdir counts, classes, first paths.
- `run1-<tool>.log`, `run1-<tool>.out` — run 1 raw strace logs and child output (7 each).
- `run2-<tool>.log`, `run2-<tool>.out` — run 2 (cwd-resolving) raw logs and output (7 each).
- `run1-tree-before.txt`, `run1-tree-after.txt` — clone listing, identical (15,297 entries).
- `registry-check-strace-rerun1.log/.out`, `registry-check-strace-rerun2.log/.out` — O1.
- `registry-check-no-strace-arms.txt` — O1's 6/6 counter-evidence without strace.
- `probeA-tempfile-empty.txt` — empty `TMPDIR` candidate list / `gettempdir()` on the host.
- `probeB-tempfile-empty-exhausted.txt` — same with every temp candidate unusable (cwd wins).
- `probeC-repeat-control-exhausted.txt`, `probeC-residual-mkdir.log`,
  `probeC-residual-selftest.out` — O2's real self-test allocating under the working directory.

Commands are quoted in each probe file's first line; the sweep command is

```
S=/fast/scratch/hyaku/tameshi-r54/T54W1ExecEmptyStrace
git clone --shared <lane> $S/clone && git -C $S/clone checkout --quiet 59c38109bf11
python3 driver.py  $S/clone $S/run1
python3 driver2.py $S/clone $S/run2 all
```

## Limits, housekeeping

- I did not run the frozen C2 counter (its one deciding invocation belongs to L1); the tool
  mapping was imported from it read-only.
- No lane production file, counter, contract, freeze, ledger or wave spec was touched;
  writes were confined to `w1/T54W1ExecEmptyStrace.md` and the receipts dir.
- No tool was installed or upgraded (nothing was needed; pacman paused anyway).
- Census conformance: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  exited 0 (`tameshi ok corpus/SOURCES.md`).
- `/tmp` footprint: the tools' own `mkdtemp` roots (largest sweep total ≈ 0.6 MB observed);
  strace logs record every one; no `/tmp/newroot` or `/tmp/oldroot` remained. The scratch
  tree `$S` was removed after the receipts were copied.
