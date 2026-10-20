# S12 — strace feasibility for input capture (round 17, wave 1)

Scope: can `strace` capture the file inputs of `python3`, `bash` (`source`,
redirects), `node` (ESM imports) and `git show REV:path` on this host, what is the
exact invocation, what does it cost, and what does an open-trace miss.
All runs were executed; every line quoted below is observed output.

## 0. Host probe (observed)

```
$ strace -V
strace -- version 7.2
Optional features enabled: stack-trace=libunwind stack-demangle m32-mpers mx32-mpers
$ pacman -Q strace
strace 7.2-1
$ cat /proc/sys/kernel/yama/ptrace_scope
1
$ uname -a
Linux plazir27 7.2.11-arch1-1 #1 SMP PREEMPT_DYNAMIC ... x86_64 GNU/Linux
$ grep -E ' /proc ' /proc/mounts
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
```

No tools were installed or upgraded for this probe (strace 7.2-1 was already
present). `/proc` is mounted without `hidepid`, so `-y` can read `/proc/PID/fd`.

`ptrace_scope=1` does not block spawn-mode tracing (`strace -- cmd`): strace is
the tracee's parent, which Yama permits. It does block attach to a non-descendant:

```
$ bash -c 'sleep 3 & strace -qq -p $!'
strace: attach: ptrace(PTRACE_SEIZE, 320916): Operation not permitted
strace: sysctl kernel.yama.ptrace_scope = 1 may be restricting this attach
```

Consequence: `trace-inputs.py` must spawn the command (`strace ... -- ARGV`),
never attach. That is already the contract; it is load-bearing here.

## 1. Recommended exact invocation (for `trace-inputs.py`)

```
trace_dir=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-trace.XXXXXX")   # outside the lane root
strace -ff -qq -y -s 4096 --seccomp-bpf --kill-on-exit \
       -e trace=openat,openat2,open,execve,execveat \
       -e signal=none \
       -o "$trace_dir/trace" \
       -- "$@"
rc=$?          # strace exits with the tracee's status (verified: 3 -> 3, SIGTERM -> 143)
# then parse every "$trace_dir"/trace.* file (one per pid, pid = filename suffix)
```

Why each flag, with the observation that justifies it:

| flag | reason (observed) |
|---|---|
| `-ff` | One file per pid. With a single `-o` + `-f`, syscalls interleave into `<unfinished ...>` / `<... resumed>)` pairs — 842 pairs in one `--selftest` run (`grep -c '<unfinished'`), 809 of whose results sit on a resumed line. `-ff` produced **0** unfinished lines over 1,709 pid files and the identical input set. |
| `-f` (implied by `-ff`) | Mandatory: in `bash bashscript.sh`, `bashscript.sh`/`./lib.sh`/`input.txt` were opened by pid 72771 and `data.txt` by pid 72772 (the `cat` child). A single-process trace misses child reads. |
| `-y` (`--decode-fds=path`) | Prints `AT_FDCWD</abs/dir>` and `N</abs/path>`, resolving relative opens at syscall time, per pid, across `chdir` and fork/exec. This is what makes relative paths usable. Zero unresolved relative opens across every analyzed run. |
| `-s 4096` | Only affects argv/env (`execve("/usr/bin/python3", ["python3", "-c", "import os; print(os.environ['HOM"...`). **Path arguments are printed at full PATH_MAX regardless of `-s`**: a 74-char path printed intact with the default `-s 32`. Needed so `execve` argv can be scanned for lane script paths. |
| `--seccomp-bpf` | Filters untraced syscalls in the kernel. Cuts overhead from +43.4% to +13.2% on the same workload; the parsed input set and sha256s were identical with and without it. |
| `--kill-on-exit` | If the helper is killed, tracees are killed too rather than left running detached. Accepted by 7.2 and does not change normal exit. |
| `-e trace=openat,openat2,open,execve,execveat` | The input-bearing set. `openat2` was used 0 times by python3/bash/node/git on kernel 7.2 (included defensively, it is free under seccomp-bpf). `open` appears for `/proc` reads in python and for bash. `execve`/`execveat` are required to credit directly-executed files: `./lanebin` (a copy of `/bin/true`) produced **0 openat** for the binary and only `execve("./lanebin", ["./lanebin"], ...) = 0`; the kernel opens it, the tracee does not. |
| `-e signal=none` | Removes SIGCHLD noise (`1` per child otherwise); `-qq` alone does not. |
| `-qq` | Suppresses attach/detach chatter; with `-o` strace writes nothing to stderr on success. |
| `-o "$trace_dir/trace"` | Log **outside** the lane root. With `-ff` this is a filename prefix. |

Do **not** add `stat`/`access`/`readlink` syscalls to the input set (see §5): they
are existence checks, not reads, and `%file` costs 3.4× the lines for zero credit
value (57,495 vs 17,063 lines at the same wall time).

`-z` (successful-only) is optional: 73 vs ~82 lines on the python fixture and it
drops the `ENOENT` records. Filtering on the return value in the parser is
equivalent and keeps the failed probes as diagnostic evidence. `-P` is **not**
usable as a subtree filter: `-P "$PWD"` on `bash bashscript.sh` matched 0 lines
(it matches the directory itself, not children), `-P data.txt` (relative) matched
1 line, and `-P "$PWD/data.txt"` (absolute) matched 0. Do not use it.

## 2. Observed capture, per command shape

Fixtures under a scratch dir; analyzer filters successful opens, read-intent
flags, `S_ISREG`, under root, `.git/` excluded. Every run used the invocation in §1.

`python3 pyscript.py` (reads `data.txt`, imports `mymod`, reads `sub/other.txt`):

```
openat(AT_FDCWD</…/fx>, "data.txt", O_RDONLY|O_CLOEXEC) = 3</…/fx/data.txt>
openat(AT_FDCWD</…/fx>, "/…/fx/__pycache__/mymod.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = -1 ENOENT
openat(AT_FDCWD</…/fx>, "/…/fx/mymod.py", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD</…/fx>, "__pycache__/mymod.cpython-314.pyc.140414063233584", O_WRONLY|O_CREAT|O_EXCL|O_CLOEXEC, 0644) = 3
openat(AT_FDCWD</…/fx>, "sub/other.txt", O_RDONLY|O_CLOEXEC) = 3</…/fx/sub/other.txt>
```
captured: `pyscript.py`, `data.txt`, `mymod.py`, `sub/other.txt` (+ a cached
`__pycache__/*.pyc` on reruns — see §6).

`bash bashscript.sh` (`source ./lib.sh`, `read < input.txt`, `cat data.txt`):
captured `bashscript.sh`, `lib.sh`, `input.txt`, `data.txt` (the last from a
different pid — the `cat` child).

`node node.mjs` (`import './dep.mjs'`, `readFileSync('esmdata.txt')`):
```
openat(AT_FDCWD</…/fx>, "/…/fx/node.mjs", O_RDONLY|O_CLOEXEC) = 22
openat(AT_FDCWD</…/fx>, "/…/fx/dep.mjs", O_RDONLY|O_CLOEXEC) = 22
openat(AT_FDCWD</…/fx>, "esmdata.txt", O_RDONLY|O_CLOEXEC) = 22
```
captured `node.mjs`, `dep.mjs`, `esmdata.txt`. ESM resolution reads the import
graph through ordinary `openat`; no special handling needed.

`git -C repo show HEAD:f.txt`:
- `f.txt` is **never opened**. The trace shows only git internals:
```
openat(AT_FDCWD</…/fx>, "/…/fx/repo/.git/HEAD", O_RDONLY) = 3
openat(AT_FDCWD</…/repo>, ".git/objects/72/2efe7d0d189fbadd1abcda54d02fd6944ddbfc", O_RDONLY|O_CLOEXEC) = 3
```
- On the real lane clone (51 commits, 2 packs, 817 loose objects), `git show HEAD~30:SKILL.md`
  opened `.git/packed-refs`, `.git/objects/pack/multi-pack-index`,
  `.git/objects/pack` (O_DIRECTORY), pack `.idx`/`.pack`, and the loose commit
  object `objects/98/bea7da58…`.
- Lane-root non-`.git` inputs: **0**. This is the expected answer (`git show REV:path`
  reads objects, not paths), but it has a contract consequence in §6.

## 3. Relative-path resolution after `chdir`

With `-y`, resolution is done per pid at syscall time and stays correct across
`cd`, fork and exec:

```
320878 chdir("/…/fx/sub") = 0
320894 openat(AT_FDCWD</…/fx/sub>, "other.txt", O_RDONLY|O_CLOEXEC) = 3</…/fx/sub/other.txt>
320894 openat(AT_FDCWD</…/fx/sub>, "../data.txt", O_RDONLY|O_CLOEXEC) = 3</…/fx/data.txt>
320878 chdir("/…/fx") = 0
```
Note the `chdir` is on the parent bash (320878) while the opens are on the python
child (320894): without `-y` a parser would have to model `chdir`/`getcwd` per pid
**and** cwd inheritance across fork/exec. Do not build that; `-y` is exact here
and costs nothing measurable (7.43 s without `-y` vs 7.32 s with, both within noise).

## 4. Overhead on `bash tools/mutate-and-run.sh --selftest`

Run in a fleet-mirror clone of the lane at `98bea7d…` (`/tmp/.../fleet/tameshi-shokunin`,
`FLEET_ROOT` derived from the script path). All runs exit 0.

| variant | n | median wall | delta |
|---|---|---|---|
| baseline (`bash tools/mutate-and-run.sh --selftest`) | 9 | 5.203 s (range 5.163–5.273) | — |
| §1 invocation (`-ff -y --seccomp-bpf`) | 5 | 5.889 s (5.744–6.102) | **+13.2%** |
| same trace set, **no** `--seccomp-bpf` | 9 | 7.463 s (7.32–8.566) | **+43.4%** |
| `-e trace=%file` (no seccomp) | 1 | 7.463 s | +43% (3.4× lines) |

The selftest is partly timeout-dominated: its `run5` case runs the hang suite
with `--timeout 2`. That sub-sweep measured 2.056 s baseline vs 2.078 s traced
(+1.1%), so the syscall-heavy remainder is 3.147 s → 3.803 s, i.e. **~+21%** for
the traced workload itself. Fixed startup cost is small: `true` 0.2→1.6 ms,
`python3 -c pass` 6.4→8.7 ms, `git rev-parse` 0.6→2.0 ms.

Volume: single `-o` 15,534 lines / 2.80 MB; `-ff` 1,709 pid files / 2.68 MB. No
tracee behaviour change was observed (exit 0, same verdict lines; the traced
`run5` still classified the timeout as INCONCLUSIVE).

## 5. What an open-trace misses

Each item below was observed unless marked `[INFERENCE]`.

1. **Environment variables.** `getenv` makes no syscall. `python3 -c "import os;
   print(os.environ['HOME'])"` under `-e trace=%file` produced 125 lines, all
   loader/interpreter (`ld.so.cache`, `libc.so.6`, `locale-archive`); nothing
   touched a file for `HOME`. Env is visible only as `execve`'s envp and only
   with `-v` (then `PATH=…` appears). A path introduced by `PIP_CACHE_DIR`,
   `HOME`, `GIT_DIR`, `NODE_PATH` etc. is invisible until it is opened.
2. **Network.** A local `connect()` produced only socket/connect syscalls; zero
   file opens attributable to it. Fetched-and-consumed remote content has no
   input path at all.
3. **Stat-only checks.** `bash [ -f data.txt ]` → `newfstatat(AT_FDCWD,"data.txt",…)=0`
   only. `command -v git` → `faccessat2`/`access`/`newfstatat`. Python
   `os.path.exists('ghost.txt')` → `newfstatat(…)= -1 ENOENT`; `os.access('data.txt')`
   → `access("data.txt", R_OK) = 0`; `os.path.realpath` resolves with no open.
   A section whose evidence is "the file exists" has **no** open to credit.
4. **`O_PATH` opens.** `openat(AT_FDCWD, "data.txt", O_RDONLY|O_CLOEXEC|O_PATH) = 3`
   looks like an open, but is a handle-only probe with no read. Must be filtered.
5. **Directory enumeration.** `openat(AT_FDCWD,"sub",…|O_DIRECTORY)=3` followed by
   `getdents64(3, …, 32768) = 80` with only `/* 3 entries */`; entry names are not
   printed. You see that a directory was read, never which children were consulted.
6. **Inherited fds.** `bash -c 'exec 3<data.txt; strace … cat <&3'` traced
   `read(0, "payload\n", 262144) = 8` with **0** `openat` of `data.txt`; likewise
   `os.read(3,7)` after `readlink("/proc/self/fd/3")`. Any fd opened by the
   invoker (stdin redirect outside strace, a pre-opened log/db handle) or passed
   across a process boundary is invisible as an input.
7. **`git show REV:path` / git objects.** Object store reads only — loose
   `objects/xx/…`, `packed-refs`, `objects/pack/multi-pack-index`, `*.idx`,
   `*.pack`, `pack` (O_DIRECTORY). The working-tree `path` is never opened, and
   with `.git/` excluded a git-only command yields **zero** lane inputs.
8. **mmap'd files.** The dynamic loader opens each library
   (`openat(AT_FDCWD,"/usr/lib/libc.so.6",…)=3`), so library *opens* are visible
   — but they are outside the lane root and filtered. A file mapped through a fd
   that was never opened by a traced process (item 6) produces neither an open
   nor a path.
9. **io_uring.** SQE-based opens are submitted via `io_uring_enter`, not via
   `openat` at syscall entry, so they are not stopped/printed. `[INFERENCE]`
   (well-known strace limitation; no io_uring consumer was exercised here).
10. **Attach.** `strace -p` on a non-descendant fails with EPERM under
    `ptrace_scope=1`; setuid / `PR_SET_DUMPABLE=0` tracees are likewise refused.
11. **Post-run hashing is TOCTOU.** `-y` resolves the path at syscall time, but
    `trace-inputs.py` hashes the file after the command exits: a command that
    rewrites one of its own inputs yields a post-run digest, and a file deleted
    during the run cannot be hashed. `mutate-and-run` writes only mutants, but
    this is not true of arbitrary commands. `[INFERENCE]` (not exercised).
12. **`-s` truncation is not a path problem.** Path arguments print in full even
    at the default `-s 32`; only argv/env strings truncate.

## 6. Parser contract implications for `trace-inputs.py`

- **Prefer `-ff`.** Zero `<unfinished>` lines, pid is the filename suffix, and
  `glob(trace.*)` always has at least one file (`-ff` on `true` created 1 file
  holding its `execve` line and loader opens). If a single `-o` is kept, pair `<unfinished ...>` (carries pid + args)
  with `<... CALL resumed>)` (carries pid + result) — resumed lines do carry the
  pid (`1585774 <... openat resumed>) = 3</usr/lib/libz.so.1.3.2>`), so pairing
  is possible, but it is strictly more code for no gain.
- **Success filter:** keep `= >=0`; discard `= -1 ENOENT` etc. and any line still
  marked `<unfinished`.
- **Read intent:** discard `O_PATH`, `O_DIRECTORY`, and anything with
  `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC`. Observed false positive from a write:
  `__pycache__/mymod…pyc.140414063233584` with `O_WRONLY|O_CREAT|O_EXCL`.
- **Regular files only:** `os.stat`, keep `S_ISREG`. This drops `/dev/null`,
  `/dev/tty`, `/proc/self/maps`, pipes, and the `O_DIRECTORY` entries.
- **Intersect with the rev's tracked files** (`git -C root ls-tree -r --name-only REV`):
  a cached `.pyc` is opened `O_RDONLY` on reruns and would otherwise be recorded
  as an input. The ledger's rule is "lane-tracked regular file", so this is also
  the semantically correct filter.
- **Exclude `.git/`**; record git object reads only as diagnostics, never inputs.
- **`execve` credit:** credit `execve`/`execveat` path arguments that resolve to
  regular files under root (direct-exec ELF/script). Discard failed execves (the
  PATH-probe miss list such as `/home/vgpnk/.local/bin/bash = -1 ENOENT`).
- **Exit code:** propagate `strace`'s status directly (3→3, signal→128+sig).
  Command-not-found is distinguishable: exit 1, `strace: Cannot stat
  '/no/such/binary': No such file or directory`, and **zero** log files.
- **Contract caveat (git-only sections):** because `git show` opens no lane file,
  a section whose only executed command is `git show` records `inputs={}` and
  measure v2's rule (`commands_executed_count>0` requires non-empty `inputs`)
  would mark it `inputs-unrecorded`. The interface already requires the seat to
  add every lane file it opened to check the section (`opened`), and the
  assembler must merge that into `inputs`; the tracer alone cannot fix this.
- **Symlinks:** normalize with `os.path.normpath` on the resolved `-y` dir plus
  the printed argument; do not `realpath` the leaf (a symlink into the lane would
  be reported under its target path). Drop anything whose normpath escapes root.
- Path strings are printed **unresolved** (relative) in single-`-o` mode, so the
  parser must always combine the `AT_FDCWD</dir>` (or `N</dir>`) annotation with
  the quoted argument — never trust the quoted argument alone.

## 7. Remaining unknowns

- Whether a tracee that installs its own seccomp filter degrades the injected
  `--seccomp-bpf` filter was not exercised (no tracee here does so).
- `-P` absolute-path matching returning 0 lines is observed but unexplained; it
  is moot because `-P` is not a subtree filter, but do not build on it.
- io_uring blindness is `[INFERENCE]` (no io_uring consumer in the lane).
- Overhead numbers were taken while ~130 sibling agents were running; absolute
  times varied (plain trace 7.32–8.57 s) but the seccomp-vs-plain ordering was
  stable across every paired run.

VERDICT: built — `strace 7.2` with the §1 invocation captures python3/bash/node/git
file inputs exactly (+13.2% wall on the lane selftest, zero unresolved paths), and
the blind spots above are the complete limits list a v2 cold-read ledger must
respect.
