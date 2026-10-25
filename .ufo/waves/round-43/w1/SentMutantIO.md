# SentMutantIO — counter write scope (round 43, operability milestone)

Scope: where the three round-43 counters write. Lane `tameshi-shokunin`, base
`487b8f0`, freeze `17f6ef0`. Read-only on the lane; no campaign tool run; no
assimilation.

Counters audited (on-disk sha256, all matching `contract.json` pins, so the
`self_pin=1` predicate is satisfiable at freeze):

| counter | lines | sha256 | contract pin |
|---|---|---|---|
| `.ufo/evidence/round-43/mutants/measure.py` | 617 | `ad7ecf8c…6bc875` | match |
| `.ufo/evidence/round-43/calibration/measure.py` | 439 | `092c76cd…a8f286` | match |
| `.ufo/evidence/round-43/guard/measure.py` | 276 | `6278edcd…8d78601` | match |

Environment for all runs: `TMPDIR`/`TEMP`/`TMP` unset, so `tempfile` resolves to
`/tmp`.

## 1. Verdict

The counters are write-confined to one `mkdtemp` work directory each (C1, C3) or
to nothing at all (C2). No counter opens a lane path for write, ever. The
`corpus/`, `tools/`, `SCORECARD.md`, `LOG.md`, `.ufo/evidence/**` bytes that a run
consumes are read through `git show`/`git ls-tree` (`show()` helpers), never
through the worktree.

Three surfaces can still receive bytes outside `/tmp`, in order of realism:
`TMPDIR` redirection of the work dir (C1, C3), an imported-not-executed counter
writing `__pycache__/*.pyc` inside the lane (observed, and gitignored so
porcelain is blind to it), and C3's children inheriting the caller's CWD
(latent, currently inert). Details and fixes in §5.

## 2. Complete write-site inventory

### C1 `mutants/measure.py` — all writes under `work`

| file:line | call | destination |
|---|---|---|
| `mutants/measure.py:488` | `tempfile.mkdtemp(prefix='tameshi-r43-c1-')` | `/tmp/tameshi-r43-c1-*` |
| `mutants/measure.py:413` | `os.makedirs(work/fixtures)` | work |
| `mutants/measure.py:415` | `open(work/fixtures/<name>.py, 'w')` | work — 12 fixture sources |
| `mutants/measure.py:424` | `os.makedirs(dirname(work/live/<rel>), exist_ok=True)` | work |
| `mutants/measure.py:425` | `open(work/live/<rel>, 'wb')` | work — every `tools/*.py` blob at REV |
| `mutants/measure.py:518` | `open(work/control-<mutant>.py, 'w')` | work — `--control` only |
| `mutants/measure.py:544` | `open(work/mutant-<name>.py, 'w')` | work — measurement path |
| `mutants/measure.py:479` | `open(__file__, 'rb')` | read-only (self-pin) |
| `mutants/measure.py:613` | `shutil.rmtree(work, ignore_errors=True)` | cleanup, `finally` (`:612`) |

Subprocesses: `:268` `git -C lane …` (read verbs only), `:467` `git rev-parse`,
`:283` census tool `--file <abs>` **with `cwd=work`**, `:492` tool `--selftest`
**with `cwd=work`**. Both children are anchored to `work`, so even a relative
write inside the census tool lands in the work dir, not the lane.

Not writes: the `open(..., 'w')`/`write_bytes`/`makedirs` at `:73,77,83,96,102,
112,119,125,135,152,168,181,189,201,216,240` are **fixture source text embedded in
the counter** (the `FIXTURES`/`LIVE`/self-test tables). They are written as data
to `work/fixtures/*.py` and passed to the census tool as `--file`; nothing
imports or executes them.

### C2 `calibration/measure.py` — zero writes

| file:line | call | destination |
|---|---|---|
| `calibration/measure.py:345` | `open(__file__, 'rb')` | read-only (self-pin) |
| `calibration/measure.py:78` | `git -C lane …` | read verbs only |
| `calibration/measure.py:334` | `git -C lane rev-parse master` | read-only |
| `calibration/measure.py:331-332` | `if args.selftest: return selftest()` | returns before any lane access |

No `open` for write, no `makedirs`, no `mkdtemp`, no `tempfile`, no `shutil`, no
`rmtree`, no write-capable subprocess. Git verbs reachable from this file:
`show`, `ls-tree -r --name-only`, `cat-file -e <commit>` (`:225`), `rev-parse` —
none mutate the worktree or the index.

### C3 `guard/measure.py` — all writes under `work`

| file:line | call | destination |
|---|---|---|
| `guard/measure.py:149` | `tempfile.mkdtemp(prefix='tameshi-r43-c3-')` | `/tmp/tameshi-r43-c3-*` |
| `guard/measure.py:152` | `open(work/SOURCES.md, 'wb')` | work — registry blob at REV |
| `guard/measure.py:155` | `os.makedirs(dirname(work/tools/staged-id-guard.py))` | work |
| `guard/measure.py:157` | `open(args.tool_file,'rb')` + `open(work/tools/…,'wb')` | reads operator file, writes into work |
| `guard/measure.py:160` | `open(work/tools/…, 'wb')` | work — tool blob at REV |
| `guard/measure.py:164` | `open(work/absent.py, 'w')` | work — tool-absent control |
| `guard/measure.py:206` | `open(work/naive-map.json, 'w')` | work — refused-map case |
| `guard/measure.py:219` | `open(work/safe-map.json, 'w')` | work — admitted-map case |
| `guard/measure.py:227` | `open(work/stub.py, 'w')` | work — `--control` only |
| `guard/measure.py:77` | `open(path)` | read-only (`args.staged`) |
| `guard/measure.py:136` | `open(__file__, 'rb')` | read-only (self-pin) |
| `guard/measure.py:272` | `shutil.rmtree(work, ignore_errors=True)` | cleanup, `finally` (`:271`) |

Subprocesses: `:64` `git -C lane …` (read verbs), `:125` `git rev-parse`,
`:103` guard tool `--registry … --staged … --map …`, `:167` guard tool
`--selftest` — **`:103` and `:167` pass no `cwd`** (see §5, F3).

`args.staged` defaults to `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`
(`guard/measure.py:57`, argparse `:121`). That path is outside `/tmp` and outside
the lane, and is only read: `guard/measure.py:77` and
`tools/staged-id-guard.py:321` (the tool's single `open`, read-only). The frozen
guard tool has no subprocess and no write form at all.

## 3. Paths that can receive bytes outside `/tmp`

1. **`$TMPDIR` / `$TEMP` / `$TMP` (C1 `:488`, C3 `:149`).** `tempfile.mkdtemp`
   honours the environment. If `TMPDIR` points into the lane, the entire work
   set — fixture sources, **copies of every `tools/*.py` at REV**, mutant bodies,
   map JSONs — is created inside the lane and then deleted by the `finally`
   `rmtree`. A `SIGKILL` between `mkdtemp` and `rmtree` leaves it behind. Not
   observed this run (`TMPDIR` unset; work dirs were `/tmp/tameshi-r43-*`).
2. **In-lane `__pycache__` on import, i.e. when a harness imports the counter
   instead of executing it** — observed. `.ufo/evidence/round-43/calibration/__pycache__/measure.cpython-314.pyc`
   was written at `07:47:36` (25777 B) and rewritten at `07:53:20` (26667 B,
   sha256 `a09aa634…6c8b`) by some peer importing `calibration/measure.py`. The
   pyc header carries `src_mtime=1792925282`, `src_size=17826`, i.e. it is
   compiled from the current counter. Hidden from porcelain by `.gitignore:4`
   (`__pycache__/`).
3. **C3 child CWD inheritance (`guard/measure.py:103`, `:167`).** Both
   subprocess calls omit `cwd=`, so the guard tool — including an
   operator-supplied body via the allowed `--tool-file` mode — runs in whatever
   directory invoked the counter (fleet root or lane checkout). Today inert:
   `tools/staged-id-guard.py` has exactly one `open` (`:321`) and it is
   read-only. This is the one place where a future tool change would put bytes
   into the lane without touching the counter.
4. **Counter stdout.** The only channel by which a counter's own bytes reach an
   evidence path: the caller's redirect (`python3 …/measure.py --control >
   .ufo/evidence/round-43/control/<name>.stdout`). No counter opens an evidence
   path; the receipts in `.ufo/evidence/round-43/control/` were produced this
   way, not by the counter.

Bounded by construction: `work/live/<rel>` (`:424`) uses `git ls-tree` paths
under `tools/`, which cannot be absolute or contain `..`; no counter calls
`os.chdir`; `shutil.rmtree` is always applied to the `mkdtemp` handle.

## 4. C2 `--selftest` — ran clean, wrote nothing

Command (absolute paths, as required by the seat bounds):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-43/calibration/measure.py --selftest
C2_R43_SELFTEST: cases=10 failed=0
VERDICT: PASS
selftest_exit=0
```

Syscall evidence (`strace -f -e trace=openat,open,creat,mkdir,mkdirat,unlink,unlinkat,rename,renameat,renameat2,ftruncate,write`):

```
write-intent openat/creat/mkdir/unlink/rename lines: 0
all openat flag summary: 13 O_CLOEXEC|O ...  8 O_RDONLY  156 O_RDONLY|O ...
lane paths touched: 3 (the script itself, its directory, the script again — all O_RDONLY)
write() calls: 4, all to fd 1 (the 4 stdout lines above)
process syscalls: 1 (the execve of python3 itself)
```

Re-run from a non-lane CWD (`/tmp`): same output, `non-O_RDONLY opens: 0`. So
`--selftest` needs no repo, no contract, no temp dir.

### Porcelain, verbatim

Before the selftest run:

```
?? .ufo/evidence/round-43/before/
?? .ufo/evidence/round-43/control/
?? .ufo/evidence/round-43/sources/
?? .ufo/waves/round-43/
?? corpus/knowledge/r43-survivor-resolution-rule.md
```

After the selftest run — byte-identical to the above.

Final `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain`:

```
 M corpus/SOURCES.md
?? .ufo/evidence/round-43/before/
?? .ufo/evidence/round-43/census-sources/
?? .ufo/evidence/round-43/control/
?? .ufo/evidence/round-43/sources/
?? .ufo/waves/round-43/
?? corpus/knowledge/r43-survivor-resolution-rule.md
```

**Attribution of the delta is peer activity, not the counter.** The two-line
difference from my first snapshot appeared while I was auditing and is not
produced by any counter run of mine: `corpus/SOURCES.md` mtime `07:53:57` (my
selftest ran at `07:52:4x` and `07:53:2x`), and its diff is a scribe/executor
edit — a new `S159` Wikipedia row plus `corpus/knowledge/r43-survivor-resolution-rule.md`
added to the `used-by` cells of S089/S155/S158 (`git diff --stat`: 9 insertions,
3 deletions). `census-sources/` likewise carries another seat's
`start.stdout`/`start.exit`. All three counter sha256 stayed identical before and
after every run.

Concurrency does not threaten the measurement: C2 reads `git show REV:<path>` and
`git ls-tree REV` (`calibration/measure.py:81-83`, `:349-350`), i.e. committed
bytes at `--rev`, never the worktree. A dirty worktree cannot perturb a C2/C1/C3
receipt.

## 5. Findings

**F1 (medium — the item's own witness is weaker than it looks).**
`git status --porcelain` cannot prove "nothing in the lane changed", for two
reasons, both demonstrated above: `.gitignore:4` (`__pycache__/`) hides in-lane
`.pyc` writes (one was written into `.ufo/evidence/round-43/calibration/` during
this window), and untracked directories are reported as one line, so per-file
additions inside `.ufo/evidence/round-43/control/` or `.ufo/waves/round-43/` are
invisible. The strong witness for "counters write nothing" is the syscall
trace: `non-O_RDONLY opens = 0`, `write() → fd 1 only`. Impact: a lane
"no-harm"/"read-only" claim backed only by porcelain can be true of the counters
and false of the tree. Smallest remediation: quote the syscall summary (or a
`find <lane> -newer <marker>` snapshot) next to porcelain, and use
`--ignored` when the point of the check is "no bytes anywhere in the lane".

**F2 (medium — `TMPDIR` moves the work set into the lane).**
`mutants/measure.py:488` and `guard/measure.py:149` create the work dir through
`tempfile.mkdtemp`, which honours `TMPDIR`. If it is ever set to a lane path,
C1 writes a copy of every `tools/*.py` plus all mutant bodies inside the lane,
and only the `finally` `rmtree` removes them. Smallest remediation (one check
after `mkdtemp`, both counters):

```python
if os.path.commonpath([os.path.realpath(work), lane]) == lane:
    raise Refusal('work dir %s is inside the lane' % work)
```

Or pin the dir explicitly: `tempfile.mkdtemp(prefix=…, dir='/tmp')`.

**F3 (low — C3 children inherit the caller's CWD).**
`guard/measure.py:103` and `:167` omit `cwd=`, unlike C1's
`run_tool(..., cwd=work)` (`mutants/measure.py:283`). Any relative write inside
the guard tool — reachable today through the allowed `--tool-file` mode, which
swaps the tool body — would land in the operator's CWD, i.e. the fleet root or
the lane. Currently inert because the frozen tool's single `open`
(`tools/staged-id-guard.py:321`) is read-only. Smallest remediation: add
`cwd=work` to both calls, matching C1.

**F4 (informational — the C3 staged package is a read surface outside both
repos).** `guard/measure.py:57/:121` defaults `--staged` to
`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`, a path in the
read-only assimilation package. It is read only (`guard/measure.py:77`,
`tools/staged-id-guard.py:321`) and its absence is a clean refusal (`:148`), but
the counter's receipt therefore depends on a file the lane does not own and that
is not pinned by sha in the contract. Smallest remediation: record the staged
file's sha256 in the C3 output fields, so a moving package cannot silently change
the receipt.

No blocking defect: C1/C3 write scope is one `/tmp` directory each; C2 writes
nothing; `self_pin=1` is reachable at freeze; the C2 selftest is green
(`cases=10 failed=0`, exit 0) and side-effect-free.

## 6. Tooling

None installed or upgraded. `strace` was already present
(`/usr/bin/strace`); no pacman transaction attempted (host pause respected).

Scratch under `/tmp/tameshi-r43-SentMutantIO-*` deleted before return.
