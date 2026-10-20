# N01TraceGitSafety — security review of round-17 build surfaces (sentinel, W1)

Lane tip at dispatch was 98bea7d. These file snapshots were reviewed at the end of the run (sha256):
- `tools/registry-check.py`: 60b0f503…
- `tools/registry.json`: c434f3ea…
- `.ufo/evidence/round-17/coldread/trace-inputs.py`: c587d35b…
- `.ufo/evidence/round-17/measure.py`: f654d5b6…
- `.ufo/evidence/round-17/coldread/assemble.py`: 5996bc2a…
- `.ufo/waves/round-17/staged/tools/evidence-disposition.py`: 3de4aa69…
- `.ufo/waves/round-17/staged/tools/mutate-and-run.sh`: 88450 B, mtime 12:30

Every exploit below was reproduced only in my scratch dir `/tmp/tameshi-r17w1-N01TraceGitSafety-*`. No lane file was edited apart from this report. Nothing was installed.

Axes: (A) zero mutation of live repos, (B) honest provenance (the rev, exit and inputs a record claims are the ones actually used), (C) bounded execution (process tree, time, disk), (D) secrecy (no credential reads).

## F1 — CRITICAL (A): `GIT_DIR` leaks through every fixture-building selftest; the live lane HEAD and index were already overwritten once

**What happened on the live lane.** At 12:29:33 the lane HEAD moved from 98bea7d to e16adb7, then 0559c60, then f8832ef. The author was `tameshi <tameshi@selftest>` and the commit messages were `selftest-fixture`, `-exec` and `-noexec`, which come from mutate-and-run.sh selftest lines ~1530-1628. The tree held only `exec.sh`, `noexec.sh` and `target.sh`, and `.git/index` was rewritten at 12:29:35. I reported this to the L1 as a blocker. The L1 has since restored HEAD; the reflog shows `98bea7d HEAD@{0}: round-17 L1 repair: restore HEAD after R04 seat fixture commits (GIT_DIR leak)`.

**How it happens.** I reproduced the exact signature in a sandbox. With `export GIT_DIR=<lane>/.git`, the selftest pattern `git -C "$grepo" init -q; git -C "$grepo" add -A; git -C ... commit` does three things:
- it commits into the lane;
- the fixture directory gets no `.git`;
- lane status becomes ` D target.sh` + `?? LANEFILE`.

**The new round-17 code has the same class (sandbox repo `lane2` stood in for the lane, `GIT_DIR=$S/lane2/.git`):**
- `registry-check.py --selftest` → `lane2` HEAD went from 5f55f21 to e70c41c, a commit named "selftest fixture". The selftest also reported `FAIL rev-clone-held`. The cause is `git_env = dict(os.environ, …)` at tools/registry-check.py:412-414 together with the `git init/add/commit` calls at :419-425.
- `measure.py --selftest` → printed **`MEASURE_SELFTEST: 58/58 pass`** while writing its whole fixture history into `lane2` (6b242a6 "drop SHONEN.md", …). Cause: `env = dict(os.environ, …)` at measure.py:525.
- `assemble.py --selftest` → printed **`SELFTEST: all checks passed`** while committing "selftest page" and "selftest old" into `lane2` (ddc48a5).
- The registry rows `mutate-and-run-selftest`, `measure-round17-selftest`, `assemble-round17-selftest` and `registry-check-selftest` therefore become live-lane writers whenever `GIT_DIR`, `GIT_WORK_TREE` or `GIT_INDEX_FILE` is in the environment. That happens inside git hooks, `git rebase -x`, and some editor or jj integrations.

**Fix (smallest, one pattern everywhere):**
- Put one stdlib helper in every tool that shells out to git, copied from tools/pin-disposition.py:197-211 (`git_env()`: drop every `GIT_*`, then set `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_TERMINAL_PROMPT=0`, `LC_ALL=C`). Selftests that need an author add `GIT_AUTHOR_*` and `GIT_COMMITTER_*` on top of the scrubbed base, not on top of `os.environ`.
- In mutate-and-run.sh add near the top: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR GIT_NAMESPACE GIT_PREFIX`.
- In mutate-and-run.sh, after each fixture `git init`, assert `[[ "$(git -C "$grepo" rev-parse --show-toplevel)" == "$(realpath "$grepo")" ]] || die_setup`.
- Selftest red-before: run each `--selftest` with `GIT_DIR=<decoy repo>/.git` and assert the decoy's HEAD is unchanged.

## F2 — HIGH (A): `registry-check.py --rev` with `GIT_DIR` set checks out inside the SOURCE lane

The code is `clone_lane_at_rev` at tools/registry-check.py:266-280: `git clone` and `git -C clone checkout -q REV`, both run with the inherited environment.

Sandbox run: `GIT_DIR=$L/.git python3 tools/registry-check.py --rev $V1 --registry tools/registry.json`.
- Result: `held=2/2 rc=0`.
- Afterwards the source repo's HEAD had moved from 1c9718f to 37d1de9, its reflog showed `checkout: moving from master to 37d1de9…`, and its status was ` M marker`.

So a monitor that is supposed to be read-only moves the live HEAD and index, and still reports success.

**Fix:** pass `env=git_env()` to clone, checkout and every row (see F7). Also clone with `git clone -q --no-hardlinks -c core.hooksPath=/dev/null`, since today the objects are hardlinked into the live `.git/objects` (link count 2 observed).

## F3 — HIGH (B): `--rev` accepts paths and options, then grades the default HEAD under the requested label

Sandbox lane with master at V2 and registry row `marker` expecting `v1`:

| `--rev` value | result | correct result |
|---|---|---|
| the V1 sha | `held=2/2` | ✓ |
| `marker` (a path) | runs at V2: `held=1/2 rc=1` | contract requires exit 2 |
| `tools/registry.json` | runs at V2 | exit 2 |
| `--detach` | runs at V2 | exit 2 |
| `--orphan=zz` | creates an orphan branch, rows run on V2 files, `rev` row got 128 | exit 2 |

The cause is that `git checkout -q <rev>` treats a path as a pathspec (a no-op) and a dashed value as an option. The report then echoes `"rev": <string>` and never records the commit that was actually tested.

**Fix:**
- Resolve the rev in the source repo first: `git -C root_real rev-parse --verify --quiet --end-of-options REV^{commit}`. A non-zero result means exit 2 (`rev_missing`).
- In the clone, run `git -C clone checkout -q --detach <sha>` and assert `git -C clone rev-parse HEAD == sha`.
- Emit `rev_resolved: <sha>` and `registry_sha256` in the JSON report.

## F4 — HIGH (B): trace-inputs reports a failed strace as a traced command with `exit 1`

- **Nested ptrace** (the tool run under another tracer, a seccomp sandbox, or a container): `strace -f -qq -o /dev/null python3 trace-inputs.py --root R --out r2.json -- cat tools/a.py` gives tool rc=0, receipt `exit 1, inputs {}`, stderr `strace: attach: ptrace(PTRACE_SEIZE, …): Operation not permitted`. The command never ran.
- **Missing argv0**: `-- ./no-such-cmd` gives rc=0, receipt `exit 1, inputs {}`, stderr `strace: Cannot stat './no-such-cmd'`.

The contract says this case must exit 2 (strace unavailable or setup failure). Because `-qq` is used, the trace log carries no `+++ exited with N +++` line, so strace's own failure exit and the command's exit are indistinguishable (trace-inputs.py:439-444).

**Fix:**
- In `Tracer`, record the first pid's first `execve(...) = 0`. If it was never seen, exit 2 `strace_setup_failed` and write no receipt.
- Use `-q` instead of `-qq`, and take the command's exit from the root pid's `+++ exited with N +++` or `+++ killed by SIG… +++` line.
- Treat a failed `strace_supports_y` probe as exit 2, not as a silent downgrade to no `-y`.

## F5 — MEDIUM (B): trace-inputs records the wrong input set

Sandbox root with five tracked or untracked files; I traced `cat` over all of them plus one file outside the root.
- **Escaped names are dropped.** Receipt `inputs` = `['tools/__pycache__/m.pyc', 'tools/a.py']`. These tracked files were missing: `tools/日本.md`, `tools/gt> = 3<x.txt` and `tools/q"uote.md`. strace C-escapes the `-y` annotation (`\76`, `\74`, `\"`, octal for non-ASCII), but `RET_FD_RE`/`FD_TOKEN_RE` (:59-60) take the escaped text literally, and `os.path.isfile(ann)` then fails silently (:301-304, :457-460).
  - Fix: decode the annotation with the same C-unescape used for path arguments (`_unquote`), and capture with `<((?:[^>\\]|\\.)*)>`.
  - Fix: if an annotated path does not exist after decoding, fall back to `resolve()` and count it under `unresolved` instead of dropping it.
- **Untracked files are counted.** `tools/__pycache__/m.pyc` was recorded, but the contract says "lane-tracked". On the live lane, `tools/__pycache__/registry-check.cpython-314.pyc` is untracked and not ignored. Every input like this later fails measure with `input-missing`, or is credited from bytes git never pinned.
  - Fix: intersect with `git -C root ls-files -z --cached` and emit everything else as `untracked: {rel: sha}`.
- **Read-then-modify hashes the new bytes.** A traced `python3 rw.py` read `tools/a.py` and then rewrote it. The receipt recorded sha 14309db0…, which is sha256(`MUTATED\n`), not the bytes that were read (87428fc5…). Write-mode opens are skipped (:296-298), and hashing happens after the run (:456-460).
  - Fix: also trace `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC`, `rename*` and `unlink*` on lane paths. Mark any input that was also written as `mutated`, and give it no credit. A cheaper alternative: add `matches_rev` per input (sha == sha256 of the blob at `rev`).
- **Reads through git are invisible.** Tracing `git show HEAD:tools/a.py` gave `inputs {}`, because `.git/` is excluded (:215). Commands that read lane bytes through the object store therefore look input-free.
  - Fix: count opens under `.git/objects` as `git_object_reads: N` so consumers can see it.

## F6 — MEDIUM (B): trace-inputs `rev` has no repository-identity guard and no dirty flag

- `--root .ufo/waves` (a directory with no `.git`, inside the lane) was recorded with `rev e16adb7…`, the lane's HEAD. Paths in the receipt are relative to `.ufo/waves`, so they can never match that rev. Cause: `lane_rev` at :390-400.
- While F1's corruption was live, every receipt taken in the lane recorded the fixture commit e16adb7 as its `rev`.

**Fix:** require `realpath(git -C root rev-parse --show-toplevel) == realpath(root)` (otherwise `rev: null, rev_reason: "repo_identity_mismatch"`), use `git_env()`, and add `dirty_inputs: [rel…]`: inputs whose sha ≠ the blob at `rev`.

## F7 — MEDIUM (C/A): registry-check timeouts leave orphans, and rows run unsandboxed

- **Orphans after timeout.** `subprocess.run(..., timeout=)` kills only the direct child (registry-check.py:212-219). Sandbox check: `subprocess.run(['sh','-c','sleep 37.5 & wait'], capture_output=True, timeout=1)` returned `TimeoutExpired` after 1.0 s, but `pgrep` still showed `sleep 37.5` afterwards. The 360 s `mutate-and-run-regression` row spawns process trees, and an orphan can keep writing into a removed clone or the live lane.
  - Fix: `Popen(..., start_new_session=True)`. On timeout: `os.killpg(pgid, SIGTERM)`, wait 5 s, then `SIGKILL`, then `communicate(timeout=5)`. Also `killpg` after normal completion to reap daemons.
- **Rows inherit the full environment and write to the live lane.** Live untracked files appeared during the wave: `tools/__pycache__/registry-check.cpython-314.pyc` (12:30:28) and `.ufo/waves/round-17/staged/tools/__pycache__/pin-disposition.cpython-314.pyc` (12:31:42).
  - Fix: row env = `git_env()` plus `PYTHONDONTWRITEBYTECODE=1`.
  - Fix: in live `--root` mode, snapshot `git status --porcelain=v1 -z --untracked-files=all` before and after each row. Any delta makes the row `differs` (`mutated_lane`).
- **SIGTERM to the monitor leaks the clone.** `shutil.rmtree(work)` runs only in `finally:`, so a SIGTERM leaves the mkdtemp clone behind.
  - Fix: install a SIGTERM handler that raises `SystemExit`.

## F8 — MEDIUM (B): `--rev` is not hermetic, and one registered row passes vacuously

- **The `pin-disposition-read` row ignores `--rev`.** Its argv uses the absolute `--root /home/vgpnk/Projects/shokunin`, so under `--rev` it reads the live fleet, not the clone.
- **The mirror layout makes pin-disposition see nothing.** In the mandated fleet-mirror layout (siblings symlinked), `pin-disposition.py --root $W/fleet` gave `counts {'unchanged': 0, 'changed': 0, 'unavailable': 6}` with all 6 legs `reason: repo_symlink`, and **exit 0**. The live run gives `unchanged 3, changed 3`. The row expects only `{"exit": 0}`, so it "holds" even when it observed nothing.
- **The clone is not isolated from live siblings.** Sibling symlinks point at the live, writable repos, so any row writing `../<sibling>` from the clone mutates them.
- **Fixes:**
  - Make the row `"stdout_contains": ["\"unavailable\": 0"]`.
  - In `--rev` mode, flag any argv token that is an absolute path under the live fleet root as `non_hermetic_argv`, so the row reports differs or skipped.
  - Make pin-disposition's `repo_identity` (:248-249) accept a symlinked sibling whose realpath is a `*-shokunin` sibling of the real lane.
  - Rows without `stdout_contains`: `bash-witness-count`, `evidence-disposition-round17(-before)`, `measure-round16-rev`, `verify-round15`, and the four round-17 selftests. They grade only the exit code, so a crash path that exits with the expected code passes.

## F9 — MEDIUM (A/B): measure.py `--ledger-rev` allows git option injection

- **Arbitrary file write.** `python3 measure.py --rev 98bea7d… "--ledger-rev=--output=$S/pwned:x"` gave **rc=0** and created `$S/pwned:x` (18320 B, the output of `git show` for commit 98bea7d). measure then printed a full measurement with `"ledger_error": "JSONDecodeError…"` and exit 0. Cause: `ledger_rev` is never validated (:894-899) and goes straight into `git show <ledger_rev>:<path>` (:110, :928). git parses `--output=<file>` as an option, so any path ending in `:<blob>` can be created or truncated.
- **Every blob is read through the unresolved `args.rev` string** (:911, :367-371, :263). There are two consequences:
  - If the branch moves between reads, one measurement mixes blobs from different commits.
  - With a symbolic rev, a directory used as an input is never re-checked. `git show master:tools` prints a listing whose header contains the literal rev, so its hash stays the same while file contents change. Sandbox: `dir-input master:tools before=73af771c… after=73af771c…`, while the file inside changed 60b0f503 → 9fc6c5a1.
- **The resolved rev is never emitted.**
- **Fixes:**
  - Resolve `REV` and `ledger_rev` once with `rev-parse --verify --quiet --end-of-options X^{commit}` (failure → exit 2), and use the resolved sha everywhere.
  - Emit `rev_resolved`.
  - In `blob()`: require `git ls-tree <sha> -- <path>` mode 100644/100755 (reject 040000, 120000 and 160000), then `git cat-file blob --end-of-options <sha>:<path>`.
  - Run with `git_env()`.
  - Out of my scope, but noted: an unparsable ledger should exit 2, not 0.

## F10 — MEDIUM (B): assemble credits seat-asserted `inputs` and never opens a trace

- `traces` are only list-checked and unioned (assemble.py:383-386, :568-576). `inputs` is accepted after a 64-hex format check only (:387-388), and its keys are not validated as canonical lane paths.
- So a seat can list a hand-picked or partial input set, with no trace, and get the same credit as a traced section. That makes C1's input-keyed rule only as honest as the seat.
- **Fixes:**
  - For every section with `commands_executed`, require at least one `traces` receipt. Load it, check `schema == tameshi-trace-inputs-v1`, `rev == read_rev`, and `exit == 0` when the verdict is `executed-ok`, and require receipt `inputs` ⊆ section `inputs`. Otherwise reject.
  - Reject input keys that are absolute, contain `..`, have a `.git` component, or are not canonical. Reuse evidence-disposition's `canonical_relative` (:230-248).

## F11 — MEDIUM (D): trace-inputs reads and hashes any file under `/home`, including user config and potential credentials

- Tracing `git show HEAD:…` recorded `external: ['/home/vgpnk/.config/git/config']`, and the tool hashed it. The same rule (:218-219, :462-464) would open and hash `~/.ssh/*`, `~/.netrc`, `~/.git-credentials` or `~/.omp/agent/agent.db*` if a traced command touched them, and would write their paths into a receipt that gets committed. The round contract forbids reading credential files.
- **Fix:** hash `external` only for realpaths under `/home/vgpnk/Projects/shokunin/*-shokunin/` that have no `.git` component. Report any other `/home` open as a count, never as a path or hash.

## F12 — LOW-MEDIUM (C): trace-inputs never removes its workdir

- `tempfile.mkdtemp(prefix="trace-inputs-run-")` (:430) has no matching `rmtree`. `/tmp/trace-inputs-run-*` grew from 47 to 50 during my three runs. These logs keep the argv of every exec'd process, which may include secrets.
- `-f -s 4096` with exec-heavy commands can fill a tmpfs `/tmp`.
- **Fix:** wrap the run in `try/finally: shutil.rmtree(workdir)`, add `-z` (successful syscalls only; failed opens are ignored anyway) and `--seccomp-bpf`, and parse the log as a stream.

## F13 — LOW: evidence-disposition v2 historical reads are sound but should still scrub the environment

**Verified good** (staged :230-248, :345-388):
- canonical-path rejection of absolute paths, `..`, backslash and NUL;
- the `tools/` prefix check;
- `HEX40.fullmatch`;
- `--end-of-options`;
- a 30 s timeout;
- the repo-identity guard;
- the sha256 pin after reading.

Probes on git 2.56.0: `C:tools/../x`, `C:tools/./x` and `C:tools//x` are rejected; `C:../r/x` is "outside repository"; `--output=…:path` as an argument to `cat-file blob` gives "unknown option".

**Remaining gaps** (impact is bounded because bytes must still match the pin):
- `GIT_DIR=<other>/.git` makes the guard pass while the read comes from the other repo. Sandbox: the guard's toplevel = the root, and the read returned `FORGED`.
- A tree id is accepted as `rev`: `<treeid>:tools/a.py` resolved.
- **Fix:** use `env=git_env()`, and read `rev + "^{commit}:" + path` (verified to work).

## F14 — LOW: staged mutate-and-run.sh repo guard

- The guard (staged :1001-1015) works. Rev option injection is already blocked, because `rev-parse --verify --quiet "--output=…^{commit}"` returns 1 before `git show` runs.
- The only gap is F1's missing env scrub: with `GIT_DIR` exported, `--show-toplevel` reports the env's work tree.

## F15 — LOW: registry-check output and needle hygiene

- Row `name` is not pattern-checked, so a newline in a name can forge `ROW …` or `REGISTRY_CHECK:` lines in human output.
  - Fix: require names to match `^[a-z0-9][a-z0-9._-]*$`.
- `stdout_contains` is a substring match over the whole stdout.
  - Fix: match whole lines.

## Recommended next checks for the L1

- A red-before for each fix, then the selftests run under a decoy `GIT_DIR`.
- `registry-check.py --rev marker` → exit 2.
- trace-inputs nested under `strace` → exit 2.
- The F5 fixture (escaped names) → five tracked inputs and `untracked: {m.pyc}`.

**Verdict: partial** — the historical git reads in evidence-disposition v2 hold. The rest falls: registry-check `--rev` (F2, F3), trace-inputs (F4–F6, F11) and the selftest fixtures (F1, which already overwrote the live lane HEAD and index once).
