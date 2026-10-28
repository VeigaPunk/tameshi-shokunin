# T55W1ExecC2Full — C2 dry run at the target (one line, every mode)

Seat: T55W1ExecC2Full (leaf executor, operability). Lane:
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base
`0a2010acd1e92e4e332774050825e21bcfc7e079`; frozen counter set
`631cd6455e58dce969310b4c0466c3383d9f5108`. Receipts:
`.ufo/waves/round-55/w1/T55W1ExecC2Full-receipts/`. Machine-readable summary:
`.ufo/waves/round-55/w1/T55W1ExecC2Full.json`.

**Verdict.** At the revision carrying my assigned patch set (`71711b2`, five files, diff in
`T55W1ExecC2Full-receipts/patches.diff`) the **current** frozen counter reads

```
C2_R55: rev=71711b2eb735 grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
```

Every arm my items own is green. The single failing mode is `grammar registry-check --rev rc=2 FAIL` — a
**ninth** allocating mode the counter grew at 14:20 (`amendment 6`) that my item list does not name
(item 1 names only `tools/repeat-control.py` and `tools/context-capture.py`). With that mode's two-site
fix added in a *separate* scratch clone (proposal, not my patch set; `f9a19c4`), the same counter reads

```
C2_R55: rev=f9a19c4117d7 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
```

Against the **committed** counter bytes at `631cd64` (`9d0768`, the eight-mode version) my patch rev
reads `total=1` for a different, already-diagnosed reason: `usable registry-check --selftest rc=1`, the
tool's own wall-clock case under `strace -f`, reproducible on the **unpatched** base tree (§5).

## 1. What the patch set contains (five files, against `631cd64`)

`git -C clone diff 631cd64 71711b2` → `patches.diff`, sha256
`016d6ec335d361f2f066c697ed65534bf5745d6e5a9e20a87e02119bc825923b`, 122 insertions / 29 deletions.

| file | change |
|---|---|
| `tools/repeat-control.py` | `class ScratchRootUnusable(RuntimeError)`; helper raises it with `'%s'`-quoted value; `main` gains `except ScratchRootUnusable` → `emit_err("repeat-control.py: could-not-evaluate: <msg>")`, `status = EXIT_BY_ID["setup_error"]` (2), **no** `REPEAT_CONTROL: setup_error` on stdout |
| `tools/context-capture.py` | same class + helper raise; `run_selftest` gains `except ScratchRootUnusable` → `sys.stderr.write("context-capture.py: could-not-evaluate: <msg>\n")`, `return 2`, stdout silent |
| `tools/registry.json` | the seven `scratch_root` cells state the grammar line (marker present verbatim, `7/7`), the empty arm, the usable arm and the **eight** allocating modes this item names — `registry-check --rev` is named in the note and `SKILL.md` only, since its cell would otherwise claim a mode that does not yet carry the line |
| `corpus/knowledge/scratch-root-contract.md` | `## One line: the grammar, every allocating mode (round 55)` — frozen grammar, the nine allocating modes table (ninth marked *routed, not conforming*), the five lazy modes, and the honest statement that the class is an operator-visible line grammar, not a shared Python type; `## What measures it` rewritten for the 14-mode counter; the round-54 "residue is named, not fixed" paragraph moved to past tense |
| `SKILL.md` | `## Standing rules` scratch-root bullet: the false sentence *"Measured on each tool's `--selftest`/`selftest` path (round-54 C2 counter); other modes are outside that measurement"* is replaced with the grammar line and the 14-mode / nine-allocating / five-lazy measurement statement. No other SKILL.md line touched (`git diff --stat SKILL.md` → `10 +++-`) |

The two tool bodies, before/after (receipt `two-tools-unusable-arm.txt`, cwd = clone at `71711b2`,
`TMPDIR=<nonexistent>`):

```
== python3 tools/repeat-control.py --selftest
rc=2
stdout=[]
stderr=[repeat-control.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<...>/no-such' (could-not-evaluate)]
== python3 tools/context-capture.py --selftest
rc=2
stdout=[]
stderr=[context-capture.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<...>/no-such' (could-not-evaluate)]
```

Both match the frozen regex byte-for-byte (`docs-arms.txt`, taken at the eight-mode tree `a1ef508`, prints
the counter's own `MARKER` and `GRAMMAR.pattern`, the `any(GRAMMAR.match(line))` result `True` for both
tools, `cells=7 marker=7`, `skill raw marker: True`, and the eight note labels then in the table; the
ninth label was added in `b822c04` and the counter's own note arm reads `9/9` at `71711b2`, receipt
`c2-final-A.stdout`). `RuntimeError`/`Traceback` are absent from both streams; stdout is empty.

The nine note labels of the shipped tree are confirmed by the counter's own note arm at `71711b2`
(`EXPLAIN note 9/9 ok`, `c2-final-A.stdout`); the registry cells and `SKILL.md` marker at that same tree
are confirmed by the same run (`docs 7/7`, `skill 1/1`) and by the `docs-arms.txt` predicates.

## 2. Which counter bytes were measured (the set moved while I worked)

| bytes | sha256 | what it is |
|---|---|---|
| `631cd64:.ufo/evidence/round-55/c2/measure.py` | `9d076812d9c0…` | the freeze commit's counter; self-consistent with `631cd64:freeze.json`; 8 allocating + 5 lazy; detached clone; raw (un-normalized) doc matching; `bash-witness-study --selftest` label |
| lane working tree at 14:05 (snapshot `frozen/c2-live.py`) | `d6ca1d85b1bb…` | amendments 1-3 (branch checkout, normalized matching, corrected label); 8 allocating |
| lane working tree at 14:22-14:35 (snapshot `frozen/c2-live3.py`) | `0458f63208…` | amendments 4-6: tracer exit code no longer scored (census only), `registry-check --rev` added as the ninth allocating mode (grammar arm only), note denominator `len(allocating)` |

All four runs use `--work <empty dir> --explain`; the only writes are inside those work dirs and my
receipts. `git -C <clone> rev-parse --show-toplevel` was asserted equal to the clone path before each
commit there (three commits across two scratch clones; no lane git mutation).

## 3. Run table

| # | counter bytes | rev | verdict line | failing mode |
|---|---|---|---|---|
| R1 | `9d0768` | `a1ef508` | `grammar=8/8 lazy=5/5 empty=13/13 usable=12/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=1 C2_R55_PASS=false` | `usable registry-check --selftest rc=1` (§5) |
| R2 | `d6ca1d8` | `a1ef508` | `grammar=8/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=8/8 skill=1/1 total=0 C2_R55_PASS=true` | none |
| R3 | `0458f632` | `b822c04` | `grammar=8/9 … note=9/9 … total=1 C2_R55_PASS=false` | `grammar registry-check --rev` |
| **R4** | `0458f632` | **`71711b2`** | **`grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false`** | `grammar registry-check --rev` |
| R5 | `0458f632` | `f9a19c4` (demo clone = R4 + the §6 two-site `registry-check` fix) | `grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true` | none |

R1 vs R2 are the same tree under two counter revisions: only `usable registry-check --selftest` differs,
and `0458f632`'s own comment names that difference as amendment 4 ("registry-check rc 1 under the tracer
alone"), which my §5 measurement independently reproduces on the unpatched base.

### R4 — full verdict line and EXPLAIN lines (receipt `c2-final-A.stdout`, exit 1)

```
EXPLAIN grammar repeat-control --selftest          rc=2  ok
EXPLAIN grammar registry-check --selftest          rc=2  ok
EXPLAIN grammar bash-witness-study selftest        rc=2  ok
EXPLAIN grammar pin-disposition --selftest         rc=2  ok
EXPLAIN grammar evidence-disposition --selftest    rc=2  ok
EXPLAIN grammar context-capture --selftest         rc=2  ok
EXPLAIN grammar env-diff --selftest                rc=2  ok
EXPLAIN grammar env-diff --contract                rc=2  ok
EXPLAIN grammar registry-check --rev               rc=2  FAIL
EXPLAIN lazy repeat-control --snapshot             rc=0  ok
EXPLAIN lazy bash-witness-study count              rc=0  ok
EXPLAIN lazy pin-disposition --read                rc=0  ok
EXPLAIN lazy evidence-disposition --json           rc=0  ok
EXPLAIN lazy context-capture --check               rc=0  ok
EXPLAIN empty  repeat-control --selftest          rc=0  ok
EXPLAIN empty  registry-check --selftest          rc=0  ok
EXPLAIN empty  bash-witness-study selftest        rc=0  ok
EXPLAIN empty  pin-disposition --selftest         rc=0  ok
EXPLAIN empty  evidence-disposition --selftest    rc=0  ok
EXPLAIN empty  context-capture --selftest         rc=0  ok
EXPLAIN empty  env-diff --selftest                rc=0  ok
EXPLAIN empty  env-diff --contract                rc=0  ok
EXPLAIN empty  repeat-control --snapshot          rc=0  ok
EXPLAIN empty  bash-witness-study count           rc=0  ok
EXPLAIN empty  pin-disposition --read             rc=0  ok
EXPLAIN empty  evidence-disposition --json        rc=0  ok
EXPLAIN empty  context-capture --check            rc=0  ok
EXPLAIN usable repeat-control --selftest          rc=0  ok
EXPLAIN usable registry-check --selftest          rc=0  ok
EXPLAIN usable bash-witness-study selftest        rc=0  ok
EXPLAIN usable pin-disposition --selftest         rc=0  ok
EXPLAIN usable evidence-disposition --selftest    rc=0  ok
EXPLAIN usable context-capture --selftest         rc=0  ok
EXPLAIN usable env-diff --selftest                rc=0  ok
EXPLAIN usable env-diff --contract                rc=0  ok
EXPLAIN usable repeat-control --snapshot          rc=0  ok
EXPLAIN usable bash-witness-study count           rc=0  ok
EXPLAIN usable pin-disposition --read             rc=0  ok
EXPLAIN usable evidence-disposition --json        rc=0  ok
EXPLAIN usable context-capture --check            rc=0  ok
EXPLAIN docs                                      7/7 ok
EXPLAIN note                                      9/9 ok
EXPLAIN skill                                     1/1 ok
C2_R55: rev=71711b2eb735 grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
```

### R5 — full verdict line and EXPLAIN lines (receipt `c2-live2-0458f632-B.stdout`, exit 0)

```
EXPLAIN grammar repeat-control --selftest          rc=2  ok
EXPLAIN grammar registry-check --selftest          rc=2  ok
EXPLAIN grammar bash-witness-study selftest        rc=2  ok
EXPLAIN grammar pin-disposition --selftest         rc=2  ok
EXPLAIN grammar evidence-disposition --selftest    rc=2  ok
EXPLAIN grammar context-capture --selftest         rc=2  ok
EXPLAIN grammar env-diff --selftest                rc=2  ok
EXPLAIN grammar env-diff --contract                rc=2  ok
EXPLAIN grammar registry-check --rev               rc=2  ok
EXPLAIN lazy repeat-control --snapshot             rc=0  ok
EXPLAIN lazy bash-witness-study count              rc=0  ok
EXPLAIN lazy pin-disposition --read                rc=0  ok
EXPLAIN lazy evidence-disposition --json           rc=0  ok
EXPLAIN lazy context-capture --check               rc=0  ok
EXPLAIN empty  repeat-control --selftest          rc=0  ok
EXPLAIN empty  registry-check --selftest          rc=0  ok
EXPLAIN empty  bash-witness-study selftest        rc=0  ok
EXPLAIN empty  pin-disposition --selftest         rc=0  ok
EXPLAIN empty  evidence-disposition --selftest    rc=0  ok
EXPLAIN empty  context-capture --selftest         rc=0  ok
EXPLAIN empty  env-diff --selftest                rc=0  ok
EXPLAIN empty  env-diff --contract                rc=0  ok
EXPLAIN empty  repeat-control --snapshot          rc=0  ok
EXPLAIN empty  bash-witness-study count           rc=0  ok
EXPLAIN empty  pin-disposition --read             rc=0  ok
EXPLAIN empty  evidence-disposition --json        rc=0  ok
EXPLAIN empty  context-capture --check            rc=0  ok
EXPLAIN usable repeat-control --selftest          rc=0  ok
EXPLAIN usable registry-check --selftest          rc=0  ok
EXPLAIN usable bash-witness-study selftest        rc=0  ok
EXPLAIN usable pin-disposition --selftest         rc=0  ok
EXPLAIN usable evidence-disposition --selftest    rc=0  ok
EXPLAIN usable context-capture --selftest         rc=0  ok
EXPLAIN usable env-diff --selftest                rc=0  ok
EXPLAIN usable env-diff --contract                rc=0  ok
EXPLAIN usable repeat-control --snapshot          rc=0  ok
EXPLAIN usable bash-witness-study count           rc=0  ok
EXPLAIN usable pin-disposition --read             rc=0  ok
EXPLAIN usable evidence-disposition --json        rc=0  ok
EXPLAIN usable context-capture --check            rc=0  ok
EXPLAIN docs                                      7/7 ok
EXPLAIN note                                      9/9 ok
EXPLAIN skill                                     1/1 ok
C2_R55: rev=f9a19c4117d7 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
```

## 4. `registry-check --rev`: the mode that still fails at my rev, and its command

Command at the **base tree** (`631cd64`, clean worktree; receipt
`registry-check-rev-unusable-arm-base631cd64.txt`):

```
$ TMPDIR=<nonexistent> python3 tools/registry-check.py --rev HEAD
rc=2
stdout=[REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the scratch root: TMPDIR is
        not a usable directory: '<...>/no-such' (could-not-evaluate))]
stderr=[]
```

The class is present but on **stdout**, without the tool-name prefix, so the frozen grammar (stderr) does
not match, and the arm scores `grammar rc=2 stderr=[]` (`c2-final-A.receipts.json`). Root cause is the
same bare-`RuntimeError` helper: `tools/registry-check.py:757` raises `RuntimeError`, and `main`'s
`--rev` branch catches `except RuntimeError` and `emit`s `REGISTRY_CHECK: could-not-evaluate (...)` on
stdout (`tools/registry-check.py:1930-1949` at `631cd64`).

**The lane has since fixed it independently.** At 14:50 the lane working tree carries
`tools/registry-check.py` 20+/8- (`git status --porcelain` → ` M tools/registry-check.py`) with an
`except ScratchRootUnusable` in the `--rev` branch; running the **lane's** bytes under the same unusable
`TMPDIR` gives `rc=2`, empty stdout and
`stderr=[registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: …]`
(receipt `registry-check-rev-unusable-arm.txt`). So R4's single failure is a property of the frozen base
tree my patch set is built on, not of the lane as it now stands — the L1 should score the ninth mode
against the lane's `registry-check.py`, not against `patches.diff`.

## 5. Why the committed counter (`9d0768`) scored `usable registry-check --selftest` rc=1

Command (three shapes, plus solo re-runs; receipts `registry-check-strace-solo-rc.txt`,
`registry-check-strace-base-631cd64.txt`, `registry-check-strace-patched-a1ef508.txt`):

```
$ TMPDIR=<usable dir> strace -f -e trace=mkdir,mkdirat -o log python3 tools/registry-check.py --selftest
base   (631cd64, unpatched, solo) rc=1
br     (my rev, solo)             rc=1
SELFTEST_CASE timeout-kills-setsid-pipe FAIL (exit=1 elapsed=6.746s survivor=False marker=False)
SELFTEST_CASE timeout-kills-setpgid-pipe FAIL (exit=1 elapsed=6.186s survivor=False marker=False)
```

The case's own assertion (`tools/registry-check.py:1223`) is `elapsed < 3.5`; under `strace -f` the
traced run takes 6.2-9.4 s, so only the wall-clock budget fails — the kill semantics it guards are green
(`survivor=False marker=False`, `exit=1`). It reproduces on the **unpatched** `631cd64` tree, so it is not
caused by this seat's edits, and `0458f632` already stops scoring the tracer's exit code (amendment 4,
`c2/measure.py:200-212`). Reported, not fixed: the frozen bytes are frozen.

## 6. Proposed (not mine) ninth-mode fix, demonstrated at `f9a19c4`

Receipt `proposed-registry-check-rev.patch` (38 lines, two sites in `tools/registry-check.py`):

1. add `class ScratchRootUnusable(RuntimeError)` before `strict_scratch_root()` and raise it there with
   `'%s'` quoting — the same shape the two assigned tools now use;
2. in `main`'s `--rev` branch, `except ScratchRootUnusable as exc: emit_err(f"registry-check.py:
   could-not-evaluate: {exc}"); return 2` **before** the existing `except RuntimeError` (which keeps the
   non-scratch failures where they are).

`--selftest` is unaffected (`ScratchRootUnusable` is a `RuntimeError`, so its existing stderr line still
fires). With this added, R5 is `total=0 C2_R55_PASS=true`. This is **outside** my item list and it is now
**redundant**: the lane's `tools/registry-check.py` (20+/8-, 14:50) already carries the same `--rev`
`except ScratchRootUnusable` (and additionally keeps the `--json` report). Keep it only as the minimal
form of what the lane already does; do not stack the two.

## 7. Risks, blockers and drift I did not fix

1. **The lane working tree already carries a *different* implementation of items 1-5** (not mine, not
   committed). At 14:35 `git diff --stat` on the lane showed `tools/repeat-control.py 21+/1-`,
   `tools/context-capture.py 10+/1-`, `tools/registry.json 1275+/1026-` (reformatted), note `37+/1-`,
   `SKILL.md 7+/3-`; at 14:50 `tools/registry-check.py 20+/8-` joined them (the ninth-mode fix of §4).
   That variant: prefixes `repeat-control:` (no `.py`), keeps
   `REPEAT_CONTROL: setup_error` on stdout, keeps `%r`, and its SKILL bullet names `registry-check --rev`
   as an allocating mode. It is textually incompatible with `patches.diff`; the L1 must pick one. My diff
   is against `631cd64` and touches no other line of those files.
2. **Frozen-set digests did not agree while I read them** (report, not fix): at 14:22 the working-tree
   `freeze.json` claimed `c2/measure.py` = `ab3ae75`, while the file was `d6ca1d8`; at 14:35 it claimed
   `0458f632` for a file that had just become that. `contract.json` went `0b99dd8c` (14:12) →
   `fe5f9050` (14:20). `.ufo/evidence/round-55/before/c2.stdout` was **0 bytes** at 13:50 (a regeneration
   in flight). The committed set at `631cd64` is self-consistent, which is why R1 was run against it.
3. **My scratch tree was deleted mid-run by an outside actor**: the first R1 attempt aborted after 121 s
   with `FileNotFoundError: .../T55W1ExecC2Full/work-primary/clone`, and
   `/fast/scratch/hyaku/tameshi-r55/T55W1ExecC2Full` no longer existed; peer seats were removing scratch
   directories at the same minute. The aborted output is kept as `c2-primary.stdout` / `c2-primary.stderr`
   (its partial EXPLAIN lines show the unreferenced-rev effect of §7.4 and the tracer case of §5). I
   rebuilt from `631cd64` and re-applied the five file edits; the diff is byte-identical in intent and now
   archived in `patches.diff` under the lane receipts.
4. **The committed counter scores an unreferenced rev as a tool failure** (amendment 1 territory): with
   the rev reachable only from a detached HEAD, `evidence-disposition --json` exited 2 on the `lazy` and
   `empty` arms (first aborted run: `lazy=4/5 empty=12/13`). Putting the rev on a branch in the lane clone
   (`r55-dry`) removes it; that is also what the amended counters do with `checkout -B r55-rev`.
5. **Quoting divergence in the other five helpers**: `%r` renders a `TMPDIR` containing a single quote in
   double quotes, leaving the frozen grammar. My two tools use explicit `'%s'`; the other five still use
   `%r`. Outside the counter's fixtures; recorded in the note rather than fixed.
6. **The counter is a moving target inside the wave**: `measure.py` changed three times (13:35 → 13:50 →
   14:20) and `contract.json` twice. R4 is the state at 14:35 (`0458f632`); every receipt names its own
   bytes (`counter-bytes.txt`).

## 8. Conformance

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`, exit **0**
(receipt `census.txt`; the W01/W04 duplicate-url and tierC warnings it prints are pre-existing).

## 9. What I did not do

- No lane production file edited; no lane git/jj mutation (`git add/commit/checkout` only inside two
  scratch clones, each after asserting `rev-parse --show-toplevel` equals that clone).
- No counter, contract, freeze manifest, no-harm or deciding-run file edited; the four counters were run
  from snapshots of their own bytes.
- Nothing installed or upgraded (no `pacman`, `uv`, `npx`, binary): system `strace --version` → `strace
  -- version 7.2`, `Python 3.14.8`, `git 2.56.0` sufficed, so there is no tool/version/channel entry to
  record.
- The cold-read floor was not run here (out of this item; the counter does not measure it).
