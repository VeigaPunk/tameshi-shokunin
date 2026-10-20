# S16 — R17-CITATIONS: S060 / S061 row and Gate-quote audit

Seat TameshiR18.S16SourcesRowsAudit (leaf, no dispatch). Lane rev
`183f87b899e6cae46be98d251cbc87fb5118f6ca`. Read-only audit; no lane file edited.

## Question

Do the S060 / S061 registry anchors and their round-17 Gate quotes match the
reopened sources and the collector's actual `strace -e` argument?

## Commands and exits

| command | exit | key output |
|---|---|---|
| `git -C <lane> show REV:corpus/SOURCES.md \| awk 'NR>=69&&NR<=70'` | 0 | S060 at line 69, S061 at line 70 |
| `git show REV:corpus/lessons/round-17.md \| awk 'NR>=30&&NR<=38'` | 0 | Gate quotes at lines 34, 35 |
| `git show REV:.ufo/evidence/round-17/coldread/trace-inputs.py \| awk 'NR==74..80,630..631'` | 0 | `TRACE_SYSCALLS` (:74-80), argv `-e trace=` + list (:630-631) |
| `git rev-parse REV:<collector>` | 0 | blob `ae8310debd02f6a259c92eb6bed075f597cc9a35` |
| `sha256sum` of blob and worktree collector | 0 | both `521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070` |
| `curl -fsSL https://man7.org/linux/man-pages/man1/strace.1.html` | 0 | 85238 B; raw-HTML sha256 `eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6`; footer `strace 7.1.0.62.c605d6 2026-06-25` |
| `curl -fsSL https://docs.jj-vcs.dev/latest/git-compatibility/` | 0 | 61334 B; sha256 `db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254` |
| `curl -fsSL https://docs.jj-vcs.dev/v0.46.0/git-compatibility/` | 0 | byte-identical, same sha256 |
| `curl -fsSL https://docs.jj-vcs.dev/versions.json` | 0 | `latest` alias of `v0.46.0` |
| `strace -V` | 0 | `strace -- version 7.2` |
| `python3 <collector> --selftest` (from /tmp, all `GIT_*` scrubbed) | 0 | `SELFTEST: 27/27` |
| `git grep -F '%file' REV -- .` | 0 | no tool source hit; only round-16/17 seat reports and dispatch JSON |

## Findings

### S060 — the quote is `%file`; the collector passes an explicit syscall list

Observed (committed collector):

- `TRACE_SYSCALLS = "open,openat,openat2,creat,execve,execveat,chdir,fchdir,fork,vfork,clone,clone3,dup,dup2,dup3,close"` — `.ufo/evidence/round-17/coldread/trace-inputs.py:74-80`; assembled as `"-e", "trace=" + TRACE_SYSCALLS` at `:630-631`.
- No lane tool contains `%file` (`git grep` above); the collector cannot be using the class.

Observed (reopened man page, §Filtering → `-e trace=syscall_set` → `%file`):

- "Traces all system calls that take a file name as an argument. You can think of this as an abbreviation for --trace=open,stat,chmod,unlink,..." and "you don't accidentally forget to include a call like newfstatat(2)".
- So `%file` is **wider** than the collector on stat/access/readlink-style probes and **narrower** on the collector's `fork/vfork/clone/clone3/dup/dup2/dup3/close` calls.
- Had the collector actually used `%file`, S060's teaches-cell phrase "never … stat-only probes" would be false. With the explicit list it is true — the list has no `stat`/`access`/`newfstatat`.

Consequence: the Gate quote (`corpus/lessons/round-17.md:34`) is verbatim and correctly located for `%file`, but it is not the text governing the collector. Correct anchors:

- §Filtering → `-e trace=syscall_set`: "Traces only the specified set of system calls." (`syscall_set` = `[!]value[,value]`).
- §Tracing → `-f`: "Traces child processes as they are created by currently traced processes as a result of the fork(2), vfork(2) and clone(2) system calls." The row's "§General `-f`" is a second off-anchor (`General` heading is at page position 218; `-f` is under `Tracing` at 293).
- §Output format → `-o`, `-y`: "Prints paths associated with file descriptor arguments and with the AT_FDCWD constant." Correct as written.

The row's conclusion stands: named opens are observable per followed process, and the trace records no reads on inherited descriptors, env vars or stat-only probes — but that follows from the explicit list, not from `%file`.

Origin of the defect: the round-17 source seat left exactly this open —
`.ufo/waves/round-17/w1/S16SrcStrace.md:133-134` asks "Whether the builder's actual argv uses `-e trace=%file` alone or adds `execve`/`%process`". Round-18 answer: neither; it is the 16-syscall explicit list above. Version facts in the row (page 7.1.0.62.c605d6 2026-06-25; host strace 7.2) both check out.

### S061 — the paragraph is ¶3, not ¶2; the quote is a recipe comment

Observed (both `/latest` and `/v0.46.0`, identical bytes):

- §Colocated Jujutsu/Git workspaces contains 14 `<p>` elements. P2 is "This mode is very convenient when tools (e.g. build tools) expect a Git repo to be present."
- The detached-HEAD statement is P3: "jj commands will usually put the Git repo in a \"detached HEAD\" state, since in jj there is not concept of a \"currently tracked branch\"" (followed by the `git switch` advice).
- The Gate quote (`corpus/lessons/round-17.md:35`) is verbatim from a shell comment in §Converting a workspace into a colocated workspace: `# Convince jj to update .git/HEAD to point to the working-copy commit's parent`, immediately before `jj new && jj undo`. It is procedural code-comment text, not section prose.
- Corroborating prose for the parent relation: §Supported features → "Staging area: Kind of.": "jj diff will show a diff from the Git HEAD to the working copy."

Consequence: S061's anchor "¶2" is off by one; the prose anchor is ¶3. The recipe-comment anchor is valid for the "working-copy commit's parent" wording but should be labelled as a code comment. The row's conclusion — a Git-side `HEAD` read is not the bookmark tip; read the branch ref or an explicit revision — stands. The `v0.46.0` (alias `latest`) version claim is confirmed by `versions.json`.

### Also affected (outside this seat's write scope)

- `corpus/knowledge/input-keyed-coldread-credit.md:1` repeats the anchors "§Filtering `%file`, §General `-f`, §Output format `-y`" — same two S060 off-anchors; `:53` abbreviates the invocation as "`strace -f -y`", omitting `-q -z -s 4096 -o` and the explicit `-e trace=` list (an abbreviation, not a falsehood).
- `.ufo/waves/round-17/w1/S16SrcStrace.md:21` (the draft row) carries the same `%file`/`§General` anchors; historical bytes, leave unchanged.

## Proposed append-only correction note

Insertion point: `corpus/SOURCES.md` notes list, after the round-16 bullet
(committed line 156), before `## Leads` (line 158). Verbatim proposal:

```markdown
- 2026-10-20 — **round-18 citation correction (S060, S061; rows retained)**.
  S060: the round-17 cold-read collector passes `-e trace=` an explicit
  16-syscall list — open,openat,openat2,creat,execve,execveat,chdir,fchdir,
  fork,vfork,clone,clone3,dup,dup2,dup3,close (trace-inputs.py:74-80,630-631;
  blob sha256 521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070)
  — never the `%file` class quoted in the round-17 Gate. The manual's `%file`
  is wider on stat ("an abbreviation for --trace=open,stat,chmod,unlink,...",
  includes newfstatat) and narrower on process/fd calls, so it would record
  stat-only probes, which this row says the trace does not. Correct anchor:
  §Filtering, `-e trace=syscall_set`, "Traces only the specified set of system
  calls."; `-f` sits in §Tracing, not §General; §Output format `-o`/`-y` is
  correct. S061: the detached-HEAD statement is §Colocated Jujutsu/Git
  workspaces ¶3, not ¶2; ¶2 is "This mode is very convenient…". The
  "working-copy commit's parent" wording is a shell comment in the §Converting
  a workspace into a colocated workspace recipe (`jj new && jj undo`), not
  prose; §Supported features, "Staging area: Kind of." corroborates it
  ("jj diff will show a diff from the Git HEAD to the working copy").
  Historical Gate quotes (corpus/lessons/round-17.md:34-35) and both rows stay
  unedited; their claims stand with these anchors. The same S060 labels appear
  in corpus/knowledge/input-keyed-coldread-credit.md:1 (separate edit, not
  made here).
```

No lesson erratum is proposed: `round-17.md` has no addendum section and its
Gate table is historical evidence; the registry note is the append-only home.
No id allocation change (no new row).

## Remaining unknowns

- Whether any round-17 seat ran an ad-hoc `strace` with `%file` outside the
  cited collector. Not checked exhaustively in seat transcripts; the row's
  used-by tool and every lane tool source contain no `%file` (`git grep`), so
  the audit conclusion does not depend on it. [INFERENCE on seat practice only]
- The knowledge entry's source line and its recheck cadence belong to that
  entry's owner; left untouched.

Verdict: partial — S060 mis-cites `%file` where the collector passes an explicit 16-syscall list (and mislabels `-f` as §General), and S061's paragraph is ¶3 not ¶2; both rows' claims stand and an append-only correction note is proposed.
