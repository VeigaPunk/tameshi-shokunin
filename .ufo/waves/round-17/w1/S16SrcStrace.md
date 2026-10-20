# S16 — strace(1): row draft and what an input trace can honestly observe

Target: strace(1) manual page, https://man7.org/linux/man-pages/man1/strace.1.html,
options `-f`, `-e trace=%file`, `-o`, `-y`.
Opened live 2026-10-20. Page pins: man7 HTML fetched with `curl -sSL`, exit 0,
sha256 `eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6`;
footer reports `strace 7.1.0.62.c605d6  2026-06-25`, HTML rendered 2026-09-09
(upstream snapshot 2026-08-04). Host binary is `strace -- version 7.2`; the
installed 7.2 man page (`/usr/share/man/man1/strace.1.gz`, sha256
`a5a80dddd1417a887e98672a9a83104f16a62670e37843d8edc07ba430067501`) contains the
quoted sentences verbatim. Anchor records the page version, not the host version.
No tools installed or upgraded this seat.

## 1. Row draft (id left `S0xx`; L1 assigns — next unused is S058)

Drop-in, contract shape (11 columns; `NF=13`, malformed rows `0` under the
`CORPUS.md` census awk on this line):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx | strace(1) — Linux manual page — https://man7.org/linux/man-pages/man1/strace.1.html | docs | A | strace's own `%file`, `-f`, `-o` and `-y` semantics for an input observer over lane commands | §Filtering `-e trace=syscall_set` → `%file`; §General `-f`; §Output format `-o` and `-y`; §BUGS `CLONE_UNTRACED`; page footer `strace 7.1.0.62.c605d6 2026-06-25`; man7 HTML 2026-09-09, fetched 2026-10-20, sha256 eedefecf7c55 | `%file` covers only syscalls that take a file name, so an open-only list cannot speak for reads on inherited or already-open descriptors | queued | 2026-10-20 | on-release | — |

Status is `queued`, not `mined`, because no `knowledge/` entry or lesson cites it
yet. Flip to `mined` and fill `used-by` when a corpus entry or the round-17
lesson cites S0xx; a tool docstring alone does not satisfy the contract's
"knowledge entries or lessons" wording. `recheck: on-release` because the page
lags the host by a release (7.1 page vs 7.2 binary), so option text can drift.

## 2. Quotes (verbatim, each ≤25 words)

Primary, grounding the row's `teaches`, 12 words:

> Traces all system calls that take a file name as an argument.

Location: `OPTIONS` → `Filtering` → `-e trace=syscall_set` → `%file` entry;
local strace 7.2 man page line 589 (`zcat … | sed -n '589p'`). Verified
present in both after whitespace normalisation.

Supporting quotes, same page/access date, used in §3–§5 below:

| words | quote | location |
|---|---|---|
| 22 | Traces child processes as they are created by currently traced processes as a result of the fork(2), vfork(2) and clone(2) system calls. | `-f` / `--follow-forks` |
| 19 | Be careful when making inferences about the user/kernel boundary if only a subset of system calls are being monitored. | end of the `-e trace=syscall_set` block, after the `%pure` entry |
| 12 | Writes the trace output to the file filename rather than to stderr. | `Output format` → `-o filename` |
| 12 | Prints paths associated with file descriptor arguments and with the AT_FDCWD constant. | `Output format` → `-y` |
| 24 | A traced process can use the CLONE_UNTRACED flag with the clone system call to create a child process that is not traced by strace. | `BUGS` |
| 13 | Note that filenames are not considered strings and are always printed in full. | `-s strsize` |
| 10 | When command exits, strace exits with the same exit status. | `DIAGNOSTICS` |
| 18 | Shows PID prefix also for the process started by strace. Implied when -f and -o are both specified. | `--always-show-pid` |

## 3. What trace-inputs observes — with receipts

Ran on the host `strace 7.2`, scratch
`/tmp/tameshi-r17w1-S16SrcStrace-ke4JgC`. The helper itself is not on disk at
tip (`git show 98bea7d:.ufo/evidence/round-17/coldread/trace-inputs.py` →
`fatal: path … does not exist`), so "the helper" below means the wave brief §C
contract; where I assume its argv, that is [INFERENCE].

1. **`%file` is enough for "file-open/exec".** With only `-e trace=%file`,
   `strace -f -qq -o t_f.log -e trace=%file -- /bin/sh -c 'cat f; true'`
   (exit 0) logged the initial `execve("/bin/sh", …)` at `t_f.log:1` and the
   child `execve("/usr/bin/cat", …)` at `t_f.log:48`. No separate `-e execve`
   is required, though adding it is harmless.
2. **`-f` is load-bearing.** Same command without `-f`: exit 0, and
   `grep -c 'openat.*"f"'` is `0`; with `-f` it is `1`
   (`openat(AT_FDCWD, "f", O_RDONLY) = 3`). Lane sections run shells that fork
   `git`, `python3`, `node`; without `-f` their opens vanish.
3. **Only named-file syscalls, not fd reads.** `-e trace=%file` on
   `cat f` shows the `openat` and no `read(` line at all — the file's bytes
   are consumed after the open, outside the class. This is the primary
   sentence above, and the reason the row's `teaches` is limited.
4. **`-o` keeps the pass-through clean.** `-f -qq -e trace=%file` with no `-o`
   wrote 2587 bytes to stderr (the trace itself) and 0 with `-o t_o.log`;
   stdout was byte-identical. A helper that promises the command's
   stdout/stderr unchanged must use `-o`.
5. **`-y` captures the call-time cwd.** `openat(AT_FDCWD</tmp/…>, "/etc/ld.so.cache", …) = 3</etc/ld.so.cache>`.
   The `AT_FDCWD` annotation is the resolution base at the moment of the call;
   a single `--cwd` is wrong if the command `chdir`s. `-y` also appends the
   opened fd's path after `= N`.
6. **Filenames are never truncated.** `-s` does not apply to path arguments
   (13-word quote), so a parser need not handle `"…"` ellipsis in paths.
7. **Exit status is the command's** (10-word quote), so the JSON `exit` field
   can be the wrapper's exit, not a strace status. Not true for `-p`.

## 4. What it does not observe

- **Inherited descriptors.** `strace -f -qq -o t_inh.log -e trace=%file -- cat < f`
  printed `alpha` (exit 0) with `grep -c '"f"' t_inh.log` = `0`. Bytes crossed
  the process boundary but no traced syscall named the file. Anything read
  from stdin, or from an fd opened before the trace, is invisible.
- **Writes look like opens.** `printf x > out` produced
  `openat(AT_FDCWD, "out", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3`. The §C rule
  says "successful opens of regular files"; as written that credits an output
  file as an input. The access flags are on the line, so a filter on
  `O_WRONLY`/`O_CREAT` is available — the contract should say whether it is
  applied.
- **Stat-only inputs.** `%file` also covers `stat`, `access`, `chmod`, `unlink`
  (the page's own gloss), but a helper that keeps only successful opens drops
  a file that a gate merely tests for existence (`[ -e path ]`). Such a gate
  can change verdict when that path changes without invalidating the entry.
- **`CLONE_UNTRACED` children** escape entirely (24-word BUGS quote); the
  trace's completeness is a property of ordinary `fork`/`vfork`/`clone` only.
- **Non-file influence:** environment, argv, inherited cwd, time, and network
  are not `inputs` and cannot be re-pinned by the ledger's blob check.
- **Open-time vs hash-time bytes.** The contract hashes after the command
  exits. That proves the file had those bytes at trace end, not that the
  command read them; a section that rewrites a file it opened records its own
  output. For C3's literal claim ("still has its recorded sha256 at the
  measured rev") that is sufficient; the prose must not say "the bytes read".

## 5. Consequences for this round's claims

- **C3 wording.** The input rule is sound only as "every lane file the entry's
  commands *opened by name* in a followed process". The stronger phrase "every
  lane input it ran against" is falsified by the inherited-fd receipt above.
  Since C3's failure mode is exactly an overclaimed surface (R16-C2b), the
  ledger entry and the box-3 text should carry the weaker, observed phrasing.
- **Builder musts for `trace-inputs.py`** (contract §C is silent on these):
  use `-o FILE` (stderr is otherwise the trace, receipt 4); pass `-y` and
  strip the `<…>` annotations when recording paths (receipt 5); normalise
  relative paths against the call-time `AT_FDCWD` or the declared `--cwd`;
  parse both pid formats — without `-o`, the initial line has no prefix and
  children use `[pid N]`, while `-f` + `-o` implies `--always-show-pid`, so
  every line begins with a bare pid (receipt in §3 and the 18-word quote).
- **Credit rule test.** A red-before for the measure's input rule should use a
  file that was opened (so it is recorded) and then changed at REV; the
  inherited-fd case is a *hole*, not a red-before, and should be reported as
  a scoped limit rather than demonstrated as drift.

## 6. Remaining unknowns

- Whether the builder's actual argv uses `-e trace=%file` alone or adds
  `execve`/`%process`; either covers exec, verified only for `%file`.
- Opens submitted through `io_uring_enter` never appear as `openat`
  [INFERENCE — not tested]; lane commands are unlikely to use it, but the
  claim "every opened file" would still be false in general.
- Whether `assembler.py` normalises absolute paths from a `--cwd` run into
  root-relative keys; that is assembler scope, not this source's.

Verdict: row drafted and quote grounded; strace observes only named-file
syscalls in followed processes, so trace-inputs may credit opens, not reads.
