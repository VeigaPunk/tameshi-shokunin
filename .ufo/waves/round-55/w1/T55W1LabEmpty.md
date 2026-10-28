# T55W1LabEmpty — probe: empty `TMPDIR` semantics, and the relative fourth arm

- **Seat**: T55W1LabEmpty (leaf member, no subagent dispatch)
- **Item**: falsify *"an empty `TMPDIR` is unset for these tools, and nothing is created in
  the working directory when it is empty"*; strace one of the seven self-tests; read CPython's
  `_candidate_tempdir_list`; probe a **relative** `TMPDIR` as a fourth arm.
- **Probed revision**: `631cd6455e58dce969310b4c0466c3383d9f5108` (frozen counter set), in a
  `git clone --shared` + `checkout --detach` under
  `/fast/scratch/hyaku/tameshi-r55/T55W1LabEmpty/lane`. `git diff 0a2010ac 631cd645 -- tools/`
  is **empty**, so the helper bytes probed here are byte-identical to the round's base.
- **No production file was edited.** The lane worktree was read only; the only files written
  into the lane are this report, its `.json`, and `-receipts/`.
- **Verdict**: hypothesis **confirmed in its first conjunct, confirmed-with-a-caveat in its
  second**, and the probe found something the round's three documents do not state: a
  *relative* `TMPDIR` is honoured as a path and silently roots scratch **inside the working
  directory**, with 5 of 7 tools reporting success.

---

## 1. The mechanism — read from source, not assumed

| Layer | Evidence |
|---|---|
| lane helper | `tools/bash-witness-study.py:209-222` (same fifteen lines in the six other tools; `if t:` at 217, fallback at 222): `t = _os.environ.get("TMPDIR"); if t:` → `""` is falsy → `return tempfile.gettempdir()`. The helper does **no** `abspath`, **no** `isdir`-relative guard, **no** `chdir` guard. |
| CPython resolver | `/usr/lib/python3.14/tempfile.py:164-166`: `for envname in 'TMPDIR','TEMP','TMP': dirname = _os.getenv(envname); **if dirname:** dirlist.append(dirname)` — an empty candidate is never appended. |
| CPython fallback order | `:176-180`: after the env vars the list is `['/tmp','/var/tmp','/usr/tmp', os.getcwd()]` — **the working directory is the last candidate**. `:197-199`: candidates are `abspath`'d except the literal `'.'`. |
| runtime | `TMPDIR=""` → `os.environ.get('TMPDIR') == ''`, `bool(...) is False`, candidates `['/tmp','/var/tmp','/usr/tmp', <clone>]`, `gettempdir() == '/tmp'`. |
| helper, relative value | `strict_scratch_root()` with `TMPDIR=tmp-rel` (existing) returns the **raw string** `'tmp-rel'`, `os.path.isabs(...) is False`; `mkdtemp` then resolves it against whatever CWD the process has **at call time**. |

Receipts: `01-resolver-mechanism.txt`, `04-fourth-arm-mechanism.txt`.

Two consequences follow directly, and both matter operationally:

1. The empty arm is **unset by construction** — the helper's `if t:` and the resolver's
   `if dirname:` skip `""` independently. This is not an accident of `/tmp` existing.
2. "Nothing is created in the working directory" is **contingent**: it holds because `/tmp`
   is usable on this host, not because the code forbids the CWD. `getcwd()` is a live
   candidate; `tempfile._get_default_tempdir(['/nonexistent-a', os.getcwd()])` returned the
   cwd in-process (no host change). If `/tmp`, `/var/tmp` and `/usr/tmp` were all unwritable,
   `TMPDIR=""` would root scratch in the working directory, too. (Note the resolver *raises*
   rather than silently using CWD when no candidate at all works — `FileNotFoundError` — so
   the hazard needs the CWD itself to be writable and the three OS dirs not.)
3. The "fallback" is **not `/tmp` literally** but whatever the resolver picks, which also
   consults `TEMP`/`TMP`: `TMPDIR=""` + `TEMP=<dir>` → `gettempdir() == <dir>`. On this host
   `TEMP` and `TMP` are unset, so the counter's empty arm means `/tmp` here.

## 2. The empty arm, measured across all seven self-tests

`TMPDIR=""`, cwd = the clone, `GIT_*` stripped exactly as the frozen counter does. Detector:
recursive size+mtime snapshot of the clone (`.git`, `__pycache__` excluded) before/after each
mode, plus the exit code. The snapshot **cannot** see an entry that is created and removed
inside one run, so it is not on its own evidence of "nothing written" — the syscall pass below
is.

| Mode | rc | entries created under the clone | changed |
|---|---|---|---|
| `repeat-control --selftest` | 0 | none | none |
| `registry-check --selftest` | 0 | none | none |
| `bash-witness-study selftest` | 0 | none | none |
| `pin-disposition --selftest` | 0 | none | none |
| `evidence-disposition --selftest` | 0 | none | none |
| `context-capture --selftest` | 0 | none | none |
| `env-diff --selftest` | 0 | none | none |

**7/7 exit 0, 0 entries left behind, 0 changed** (`02-empty-arm-seven-selftests.txt`).

Syscall level (`strace -f`), three tools traced, `TMPDIR=""`. Every creation syscall
(`open`/`openat` with `O_CREAT`, `mkdir`, `mkdirat`) is attributed to a real directory: calls
via `open(2)` or `openat(AT_FDCWD, …)` are resolved against a per-pid replay of `chdir`, while
`openat(<dirfd>, …)`/`mkdirat(<dirfd>, …)` are counted separately because a directory fd is not
the cwd:

| tool | rc | creations attributed to the launcher cwd | creations under `/tmp` | in a pivoted namespace rooted at a `/tmp` tmpfs | dirfd-relative (never the cwd) |
|---|---|---|---|---|---|
| `bash-witness-study selftest` | 0 | **0** | 272 (60 cwd-resolved + 212 absolute) | 0 | 0 |
| `context-capture --selftest` | 0 | **0** | 127 (all absolute) | 0 | 0 |
| `env-diff --selftest` | 0 | **0** | 326 (103 cwd-resolved + 223 absolute) | 43 (`/proc`, `/dev` after `pivot_root("/tmp","oldroot")`) | 602 |

**Self-correction, recorded because the first pass was wrong.** A grep for `O_CREAT` plus the
absolute clone prefix reported "0 under the CWD" — true, but blind to *relative* paths. A
second, naive "relative ⇒ cwd" classifier then over-reported (39 and 269 "CWD" creations)
because `openat(<dirfd>, "null")` is resolved against a directory fd, not the cwd. The table
above is the third, correct pass (`attribute.py`); the first two are withdrawn.

The `env-diff` residue is a mount-namespace fixture, proved in the trace where it is created:
`unshare(CLONE_NEWUSER)` ×43, `mount("tmpfs", "/tmp", "tmpfs", …)` ×43 and
`pivot_root("/tmp", "oldroot")` ×43 — after the pivot, `/proc` and `/dev` are directories
*inside that tmpfs*, neither the host's nor the repo's.

`bash-witness-study`'s 60 cwd-resolved creations are all under `/tmp`: every relative
`.git/objects/…` mkdir is preceded by
`chdir("/tmp/bash-witness-selftest-private.…/command-pin-fixture")` in the same trace, e.g.

```
5:1928884  chdir("/tmp/bash-witness-selftest-private.4l8y3vk2/bash-witness-selftest.i9ijml4a/command-pin-fixture") = 0
21:1928902 mkdir(".git/objects/30", 0777)  = 0
26:1928902 mkdir(".git/objects/9a", 0777)  = 0
```

So the syscall-level answer to "nothing in the working directory when it is empty" is **0
creations attributed to the CWD for all three traced tools**, with the attribution method
stated rather than assumed (`03-strace-empty-arm.txt`). The empty arm is also
**cwd-independent**: from `lane/tmp-rel/nest`, `TMPDIR=tmp-rel` exits 2 while `TMPDIR=""`
exits 0 (`04-fourth-arm-mechanism.txt`).

**No tool's behaviour differs on the empty arm.** That is the sweep result, not an absence of
testing: 7 exit codes, 7 working-tree snapshots, 3 syscall traces, 1 nested-cwd repro.

## 3. The fourth arm: a relative `TMPDIR` **is** honoured, as a CWD-relative path

The contract declares three arms (unset / empty / unusable). The frozen C2 counter measures
thirteen modes in those three. A relative value is a fourth, unmeasured state, and it splits in
two:

| Arm | `TMPDIR` | Measured behaviour |
|---|---|---|
| **rel-absent** | `tmp-rel` and no such dir under the cwd | indistinguishable from *unusable*: **7/7 exit 2**, the class line naming `'tmp-rel-missing'` |
| **rel-present** | `tmp-rel` exists under the cwd | honoured: scratch allocated under `<cwd>/tmp-rel/…`; **5/7 exit 0 silently**, `registry-check` rc 1, `context-capture` rc 1 |
| **abs-same-dir** | the *same directory*, absolute | control: `registry-check` **rc 0, 51/51**, nothing left behind |
| **dot** | `.` | honoured; scratch created **directly in the cwd**; **6/7 exit 0** (only `context-capture` rc 1); can never be "unusable" because `isdir('.')` is always true |

Full matrix (rc per mode, cwd = clone):

| arm | repeat-control | registry-check | bash-witness-study | pin-disposition | evidence-disposition | context-capture | env-diff |
|---|---|---|---|---|---|---|---|
| rel-absent | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| rel-present | 0 | **1** | 0 | 0 | 0 | **1** | 0 |
| abs-same-dir | 0 | 0 | 0 | 0 | 0 | **1** | 0 |
| dot | 0 | 0 | 0 | 0 | 0 | **1** | 0 |
| tilde `~` | 2 | – | 2 | 2 | 2 | 2 | 2 |
| path to a file | 2 | – | 2 | 2 | 2 | 2 | 2 |
| mode-0555 dir | 2 | – | 2 | 2 | 2 | 2 | 2 |
| `" "` (space) | 2 | – | 2 | 2 | 2 | 2 | 2 |
| unset | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

(`registry-check` was not run on the four cheap "clearly unusable" arms — 60 s each, and its
usability guard is shared source with the other six; it was measured on every arm that can
change the answer. Receipts `08-arm-matrix-relative-absolute.txt`, `09-edge-arms.txt`.)

Under rel-present, `strace` shows the allocation target directly:

```
mkdir("tmp-rel/bash-witness-selftest-private.b78jwy1_", 0700) = 0
mkdir("/fast/…/T55W1LabEmpty/lane/tmp-rel/bash-witness-selftest-private.b78jwy1_/…", 0700) = 0
```

and under dot, straight into the working directory:

```
mkdir("./bash-witness-selftest-private.449khm5_", 0700) = 0
```

Receipt `07-cwd-allocation-strace.txt`.

`~` is **not** expanded (`~/tmp` → exit 2), a path to a regular file → exit 2, a `0555`
directory → exit 2 (`os.access(W_OK)` false), a single space → exit 2. The guard is honest for
every value except a relative one that exists and `.`.

## 4. The two tools that differ, with mechanisms and controls

### 4.1 `registry-check --selftest`, rel-present → rc 1: **relativity**, isolated

- Selftest scratch is `mkdtemp(prefix="tameshi-r17-registry-check-selftest.", dir=strict_scratch_root())`
  (`tools/registry-check.py:929-932`, prefix literal at 931) → `tmp-rel/tameshi-r17-…` **relative to the original cwd**.
- `run_child()` launches children with `cwd=scratch` (`tools/registry-check.py:945-954`, `cwd=` at 950), and
  they inherit `TMPDIR=tmp-rel`. From the child's cwd, `tmp-rel` resolves to
  `tmp-rel/tameshi-r17-…/tmp-rel` → absent → `ScratchRootUnusable` → exit 2.
- Six cases fail, all `exit=2` (could-not-evaluate), matching one-for-one:
  `gitdir-scrub-rev, rev-clone-detached, rev-clone-held, rev-resolved-reported,
  rev-non-hermetic-argv, rev-external-declared`.
- **Direct reproduction**: cwd `lane/tmp-rel/nest`, `TMPDIR=tmp-rel` → rc 2 with
  `TMPDIR is not a usable directory: 'tmp-rel' (could-not-evaluate)`; the same cwd with
  `TMPDIR=""` → rc 0.
- **Control C (decisive)**: the same directory given **absolutely** → `rc 0, 51/51 PASS`, no
  leftovers. So the cause is the *relativity* of the value, not the location of the directory.

Receipts `04`, `06`, `08`, `11`.

### 4.2 `context-capture --selftest`, rel-present **and** abs-same-dir → rc 1: **location**

- `hermetic-no-lane-path` fails with `subprocess output names the live lane root`
  (`tools/context-capture.py:1779-1782`, in `finish()` at 1776; `DEFAULT_LANE_ROOT = dirname(dirname(SELF))`, line 138).
- Isolation: `TMPDIR=<absolute dir outside the lane>` → **49/49 PASS**;
  `TMPDIR=<absolute dir inside the lane>` → **1/49 FAIL**, same case. So this tool's failure is
  *scratch inside the lane tree*, which a relative `TMPDIR` silently produces because the cwd
  is the lane. The tool's own hermeticity check is the detector — it is not a relativity bug.

Receipts `11-context-capture-location-cause.txt`, `08`.

### 4.3 Operational reading

Five of the seven tools (`repeat-control`, `bash-witness-study`, `pin-disposition`,
`evidence-disposition`, `env-diff`) exit **0 with no diagnostic** while their scratch lives
inside the working tree, and they clean it up, so `git status` shows nothing (git cannot see
empty directories at all). That is exactly the "silent, wrong scratch root" the contract says
the empty arm exists to prevent — reached through a different value.

## 5. What this implies for the round's documents — proposed text, **not applied**

The contract's arm table and its "one line, every mode" section are correct as written, and the
empty-arm rationale ("a tool that treated `""` as a path would try to allocate under the working
directory") is right. What is missing is that a *non-empty relative* value already does that.
Proposed addition after the three-arm table (diff against
`corpus/knowledge/scratch-root-contract.md`):

```diff
@@ ## Three arms
 | unusable | a path that is not a writable directory | the tool refuses before it allocates: ... | **2, could-not-evaluate** |
 
+## The fourth arm: a relative value (round 55 probe)
+
+The three arms above are exhaustive only for absolute values. A `TMPDIR` that is a
+*relative* path is honoured as written: the helper returns the raw string and
+`mkdtemp` resolves it against the process's cwd at call time, so
+`TMPDIR=tmp-rel` (with `tmp-rel` existing) roots scratch in
+`<cwd>/tmp-rel/`, and `TMPDIR=.` roots it directly in the working directory.
+`os.path.isdir` decides, so a relative value that does *not* exist is
+indistinguishable from the unusable arm (exit 2), while one that exists is
+silently inside the tree — 5 of the 7 tools exit 0 with no diagnostic, and the
+other two fail for two different reasons (`registry-check` because its children
+run with `cwd=<scratch>` and re-resolve the relative value; `context-capture`
+because its hermeticity case sees the lane root in child output). Git cannot
+see an empty leftover directory, so neither a clean `git status` nor an exit-0
+selftest is evidence that the scratch root was outside the working tree.
+
+The C2 counter has no relative arm and this round does not add one (the counter
+is frozen); the arm is declared here so that no reader takes "three arms" as
+"every value".
```

Two ways to close the hazard, and only one of them is a document edit:

- **(a) declare it** (the diff above) — honest, zero code risk, leaves the behaviour.
- **(b) refuse it** — one line in the seven helpers, consistent with "never a silent wrong
  scratch root". **Demonstrated and measured** in the probe clone, then restored
  byte-identical (`receipt 12`): `TMPDIR=tmp-rel` → rc 2, `TMPDIR=.` → rc 2, an absolute
  usable root → rc 0, `TMPDIR=""` → rc 0, each with the frozen class line where it fails:

```diff
 def strict_scratch_root():
     t = _os.environ.get("TMPDIR")
     if t:
+        if not _os.path.isabs(t):
+            raise ScratchRootUnusable(
+                "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
         if not _os.path.isdir(t) or not _os.access(t, _os.W_OK):
```

  This turns rel-present and dot into exit 2 (both exit 0 today). **Counter impact: none** —
  none of the frozen C2 arms sets a relative `TMPDIR` (they set an absolute unusable path,
  `""`, or an absolute usable dir), so the change is invisible to the counter in both
  directions. That is precisely why it cannot ride along in round 55: it would be an
  *unmeasured* behaviour change. Route it to a later round together with an arm that measures
  it; never fold it silently into this round's deciding run.

**Recommendation to the L1**: take (a) for round 55 (docs + registry cells only; the cells
already read "TMPDIR is not a usable directory: '<value>'", which stays true for every value
the counter exercises), and route (b) as a new defect. Do **not** let the round's `SKILL.md`
`## Standing rules` replacement claim the relative arm is covered — the counter does not measure
it, and a cold reader would infer coverage from a sentence that only names 13 modes.

## 6. Report, do not fix: two observations about the frozen C2 counter

1. **The counter can produce a false FAIL under host load.** `registry-check --selftest` is one
   of the eight `grammar` modes and also appears in the `lazy`, `empty` and `usable` arms. Two
   of its cases (`timeout-kills-setsid-pipe`, `timeout-kills-setpgid-pipe`) are timing-sensitive
   and fail nondeterministically. **Same state, same cwd, different verdict**:
   `TMPDIR` unset → `rc 1` at 14:13 (`FAIL (1 of 51 cases: timeout-kills-setpgid-pipe)`), and
   `TMPDIR` unset → `rc 0, 51/51 PASS` at 14:20, with ~40 concurrent peer selftests on the host.
   A busy deciding run can therefore print `C2_R55_PASS=false` for a reason unrelated to the
   contract. Suggested mitigation for the deciding run (not a counter edit): run it on a quiet
   host, or serialise it against the fleet.
2. **The `empty` arm does not clear `TEMP`/`TMP`.** `env_with("")` sets `TMPDIR=""` and strips
   only `GIT_*`; the helper's fallback is `tempfile.gettempdir()`, which consults `TEMP`/`TMP`.
   Demonstrated: `TMPDIR=""` + `TEMP=<dir>` → `gettempdir()==<dir>`. On this host `TEMP`/`TMP`
   are unset, so the arm is sound *here*; on a host where `TEMP` is set to a relative path the
   arm would silently measure the fourth arm instead of the platform default.

Neither is edited — the counter and contract are frozen.

## 7. Sweep — every attack run, including those that found nothing

| # | Attack | Result |
|---|---|---|
| 1 | Empty `TMPDIR` × 7 self-tests, exit + working-tree snapshot | no divergence; 7/7 rc 0, 0 entries left in the CWD (the snapshot alone is not proof — it cannot see a create+delete; §2 row 2 is) |
| 2 | Empty `TMPDIR` × 3 tools under `strace -f`, every creation attributed by `chdir` replay | **0 creations under the CWD**; 272/127/326 under `/tmp`; env-diff's 43 at `/proc` proved to be inside a `pivot_root`ed tmpfs |
| 3 | Empty `TMPDIR` from a nested cwd (`lane/tmp-rel/nest`) | rc 0 — empty is cwd-independent |
| 3b | My own first-pass detector (grep on the absolute prefix, then a naive "relative ⇒ cwd" rule) | **both withdrawn** — the grep was blind to relative paths, the rule mis-attributed `openat(<dirfd>, …)`; see §2 |
| 4 | `_candidate_tempdir_list` / `_get_default_tempdir` read + probed | empty skipped (`if dirname:`); CWD is the last candidate and reachable |
| 5 | `TMPDIR=""` + `TEMP=<dir>` | resolver, not `/tmp`, is the fallback |
| 6 | Relative `tmp-rel`, absent | 7/7 rc 2 — *no* divergence from unusable |
| 7 | Relative `tmp-rel`, **present** | **divergence**: 5/7 silent rc 0 with scratch in CWD; `registry-check` rc 1, `context-capture` rc 1 |
| 8 | Same dir, absolute (`abs-same-dir`) | `registry-check` 51/51 rc 0 → relativity isolated |
| 9 | `TMPDIR=.` | scratch created in the cwd; 6/7 rc 0 |
| 10 | `~`, regular file, `0555` dir, `" "` | 2/2/2/2 — guard honest |
| 11 | `registry-check` unset × 2 + outside-lane absolute | rc 1 then rc 0 → load nondeterminism, not TMPDIR |
| 12 | `context-capture` outside-lane absolute vs inside-lane absolute | 49/49 vs 1/49 → location cause isolated |
| 13 | Leftover hunt (`ls -A` of the scratch root after every arm; `git status --ignored`) | no reproducible leftover; the one stale `/tmp/tameshi-r17-…` seen occurred while ~40 concurrent peer selftests ran → **not attributable**, dropped |

## 8. Hygiene

- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → **exit 0** (140 rows, S001-S280 — one more than the item's "139 (S001-S279)" because a
  peer added a row this round; only the pre-existing `W04` duplicate-url and `W01` tierC
  warnings).
- **No production file touched** (no `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`,
  `tools/**` edit by this seat; no mutating git command on the lane or the fleet). The only
  git writes were inside the scratch clone: `checkout --detach 631cd645`, and the restore
  `checkout -- tools/bash-witness-study.py` after the patch demonstration, verified by
  `sha256sum -c` (`f2bb50c7…` OK). The clone's `git status --porcelain --ignored` shows only
  `tools/__pycache__/` — bytecode from running the tools, no source change.
- No tool installed or upgraded; `strace 7.2`, `python 3.14.8` already present.
- Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W1LabEmpty` (drivers + logs; removed with the
  seat's `trap … EXIT`).

## 9. Deliverables

- this report
- `T55W1LabEmpty.json` — the same matrix, hypothesis verdicts, differing tools, blind spots and
  reported counter issues, generated from the measured JSON (no hand-copied numbers)
- `T55W1LabEmpty-receipts/01…12` — every cited command with its output (12 is the proposed
  refusal, demonstrated and restored). The raw `strace` logs stay in the (deleted) scratch;
  `03`'s header carries the exact command that regenerates them and its output is the
  attribution result itself, not a summary of it.
