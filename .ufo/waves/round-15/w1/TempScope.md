# TempScope: audit of selftest write confinement (sentinel, leaf)

Seat: `TameshiR15.TempScope`. Surface: the historical harness `.ufo/evidence/round-14/capture-context.py` (`#096B`), the shared plan (`.ufo/waves/round-15/spec1.json` context and integration interface, `corpus/lessons/round-15.md`), and existing selftest precedents in `tools/`. The question is whether a `--selftest` for the planned `tools/context-capture.py` can keep every write inside an isolated temp root.

## Status and basis

- **Static read only.** I executed no gate, selftest, probe, git command, or test. I ran one shell command (`ls` of the fleet root) to find `PROTOCOL.md`. It read only and wrote nothing.
- `tools/context-capture.py` did not exist when I read the tree (glob returned no match). So the findings below cover the historical source and its precedents, not delivered code. Each one says what the new tool must not inherit.
- Contract checked: `kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:398-402` (Gate standard, Self-test) requires "isolated fixtures (temp trees, no network, no live-tree write)". `:411-416` requires a registry row that records the **write scope**. The round-15 integration interface adds "no live reads/network/writes outside temp roots" and "never overwrite round14".
- No tools were installed or updated.

## Findings (supported risk only)

### F1: HIGH. Copying the lane-root derivation verbatim puts writes outside the lane

- **Evidence.** `capture-context.py:45-47` sets `SELF = realpath(__file__)`, `LANE_ROOT = dirname^4(SELF)` and `FLEET_ROOT = dirname(LANE_ROOT)`. Four levels is right only for `.ufo/evidence/round-14/`.
- **Exploit path.** If the file is copied as `tools/context-capture.py`:
  - `LANE_ROOT` becomes `/home/vgpnk/Projects` and `FLEET_ROOT` becomes `/home/vgpnk`.
  - `evaluate()` then fails with `missing_input` (`:145-150`, `:476`).
  - `main()` still writes a receipt on exit 2 (`:617-622`).
  - `write_receipt()` runs `os.makedirs(..., exist_ok=True)` and writes `/home/vgpnk/Projects/.ufo/evidence/<round>/context-receipt.json` (`:584-595`).
- **Impact.** A write outside the lane on the very first live run, and on every selftest case that runs the real CLI.
- **Smallest fix.** Use `LANE_ROOT = dirname(dirname(SELF))`, which matches the precedent `tools/witness-metadata.py:70` (`Path(__file__).resolve().parent.parent`).

### F2: HIGH. Every non-usage path writes to a fixed path tied to SELF

- **Evidence.**
  - Exit 0, 1 and 2 all reach `write_receipt()` (`:617-636`). Only `-h`/`--help` (exit 0) and unexpected arguments (exit 64) return before writing (`:606-613`).
  - The output path is `lane_path(OUTPUT_REL)` (`:141-142`, `:58`).
  - Every input read uses `LANE_ROOT`: probe, runner, manifest and expected (`:476-479`).
  - The probe runs with `cwd=LANE_ROOT` and `--root FLEET_ROOT` (`:538-540`).
  - The git control runs `git -C LANE_ROOT` (`:400-402`).
- **Exploit path.** The selftest precedents launch `[sys.executable, SELF, ...]`:
  - `pin-disposition.py:829-837`
  - `evidence-disposition.py:1526-1541`
  - `witness-metadata.py:1133-1146`

  If a capture-mode case uses that pattern without a root override, it:
  - reads live lane inputs;
  - runs the live probe over the real fleet's sibling repos;
  - runs git against the live lane;
  - writes the live round-15 receipt.
- **Impact.** Breaks the Gate standard's "no live-tree write" rule and the plan's "no live reads". The selftest would also not be hermetic, so its exit and finding pairs would depend on live state.
- **Smallest fix.**
  - One explicit `--lane-root DIR`, defaulting to the derived root. Every input path, the probe cwd, the probe `--root` (as `dirname(lane_root)`), the git `-C` target and the output path must all derive from it. Precedent: witness-metadata `--lane-root` (`:1232-1236`).
  - Every selftest capture-mode case must pass a lane root inside the scratch dir.
  - Do **not** add a free `--output` flag. Keep `OUTPUT_REL` as the fixed round-15 path under the lane root, so containment comes from the lane root alone.

### F3: HIGH. Running the live historical script without arguments overwrites round-14 evidence

- **Evidence.** The historical script derives `LANE_ROOT` from its own location (`:46`) and always writes `.ufo/evidence/round-14/context-receipt.json` (`:58`, `:583-602`), including on exit 2.
- **Exploit path.** The plan says the selftest "must distinguish old unsupported invocation from new isolated exit/finding cases" (`corpus/lessons/round-15.md:45`). If that is done by subprocessing `.ufo/evidence/round-14/capture-context.py` with no arguments, the frozen round-14 receipt is replaced atomically (`os.replace`, `:595`). A mkstemp temp file is also created in the round-14 directory.
- **Impact.**
  - Frozen round-14 evidence is destroyed. The receipt's bytes and digest change.
  - It violates "never overwrite round14" and "preserve historical raw evidence".
- **Smallest fix.** Encode the "old unsupported invocation" as the new tool's own argv rejection (exit 64, no write). Never subprocess the historical script in place. Its only write-free invocations are `--help` (exit 0) and any unexpected argument (exit 64). If the old script must run, copy it to `scratch/<lane>/.ufo/evidence/round-14/capture-context.py`. Its own four-level derivation then confines it to the scratch lane. That copy is a read of a live file, so disclose it.

### F4: MEDIUM. Importing historical or tool modules writes bytecode next to frozen evidence

- **Evidence.**
  - The plan says to "reuse decide/comparison/mapping semantics" (spec1 integration interface).
  - `.gitignore` contains only `.ufo/interactive-sessions/`, and no `__pycache__` exists in the lane today (glob, hidden and ignored files included).
  - `round-15.md:58` records that the initial `git status --short` was empty.
- **Exploit path.** `importlib` loading of `.ufo/evidence/round-14/capture-context.py` or of a `tools/*.py` module through a source loader caches bytecode beside the source. Running a file as `__main__` does not.
  - `-I` implies `-E`, which ignores `PYTHONDONTWRITEBYTECODE`, so `python -I` with that env var does not stop the cache write.
  - This is [INFERENCE] from CPython import and command-line semantics; I did not execute it.
- **Impact.**
  - A live-tree write of `.ufo/evidence/round-14/__pycache__/` (or `tools/__pycache__/`).
  - An untracked entry that dirties the lane.
  - The new directory sits inside frozen evidence even though the historical file's bytes stay the same.
- **Smallest fix (pick one).**
  - Preferred: put the reused semantics directly in `tools/context-capture.py` and import nothing from the lane.
  - Otherwise: set `sys.dont_write_bytecode = True` before any import and launch selftest children with `-B` (for example `[sys.executable, "-I", "-B", SELF, ...]`).

### F5: MEDIUM. A selftest crash can be misclassified as `failed`

- **Evidence.** The `pin-disposition.py` selftest catches only `(OSError, RuntimeError, subprocess.SubprocessError)` (`:1174`). Any other exception (`KeyError`, `ValueError` from JSON, `TypeError`) escapes. CPython then exits 1 and the scratch dir is left behind.
- **Impact.**
  - Exit 1 maps to `failed`, but a crashed selftest is `could-not-evaluate` (`PROTOCOL.md:393-395`).
  - The `/tmp` fixtures are left behind silently.
- **Smallest fix.** Use the `repeat-control.py:861-862` and `witness-metadata.py:1185-1186` pattern:
  - a broad `except Exception` that maps to exit 2;
  - `try/finally` around fixture creation.

  If fixtures are kept on failure for debugging (as the pin-disposition precedent does), they must stay inside the `mkdtemp` dir (mode 0700, random name) and their path must be printed.

### F6: MEDIUM. Where the scratch dir lives, and git discovery

- **Evidence.**
  - Three precedents pin `tempfile.mkdtemp(..., dir="/tmp")`: `pin-disposition.py:604`, `evidence-disposition.py:1512` and `repeat-control.py:597`.
  - Two do not: `witness-metadata.py:1122` and `bash-witness-study.py:1230`.
  - The capture tool strips **all** ambient `GIT_*` before the probe and the control (`safe_env`, `:184-187`). A `GIT_CEILING_DIRECTORIES` set by the selftest would therefore not reach git.
- **Exploit path.** With a bare `mkdtemp()`, an ambient `TMPDIR` inside a repo (for example the lane) places the fixtures in the live tree. Then `git -C <fixture lane> rev-parse --git-dir` walks upward:
  - It finds the enclosing live repo, which is a live read.
  - The baseline turns ok and the control becomes "effective" because of the live repo rather than the fixture.
  - The literal expected exit may still pass while the mechanism is wrong. The round-14 spotcheck (line 125) records the same "exit agreement alone" trap.
- **Smallest fix.**
  - Use `mkdtemp(prefix="tameshi-r15-context-capture-selftest.", dir="/tmp")`.
  - `git init` every fixture lane that the control should succeed against. Use the pin-disposition fixture env (`:649-665`): ambient minus `GIT_*`, plus `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `HOME=scratch`, templates and hooks under scratch, and identity under `example.invalid`.
  - Do not add a "non-repo lane" case unless git discovery is bounded inside scratch.

### F7: MEDIUM. The selftest child environment and working directory

- **Evidence.** The `capture-context.py` children inherit the ambient env minus `GIT_*` (`:184-187`). The positive control adds `GIT_CONFIG_NOSYSTEM`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_OPTIONAL_LOCKS=0` and `GIT_TERMINAL_PROMPT=0` (`:62-67`). The probe's `git_env()` (`pin-disposition.py:197-211`) adds the same set plus `GIT_NO_LAZY_FETCH=1` and `GIT_PAGER=cat`. Both stay read-only.
- **Risk.** `HOME`, `TMPDIR` and cwd come from the caller.
- **Smallest fix.** For every selftest CLI subprocess:
  - pass an explicit `env=` with `HOME=<scratch>`, `TMPDIR=<scratch>` and `LC_ALL=C`;
  - set `cwd=<scratch>/case-<name>`;
  - set `stdin=DEVNULL` and a timeout.

  This follows the S049 `env` mapping (`round-15.md:13-18`). Unlike the plain `pin-disposition.py:829-837` and `evidence-disposition.py:1526-1541`, it no longer depends on the caller's environment.

### F8: MEDIUM. Prefer read-only check mode for selftest cases

- The plan calls for a retained-receipt check CLI.
- If check mode only opens the receipt read-only and writes to stdout, synthetic-receipt cases cause zero writes beyond creating the fixture. These cases include ok, mismatch, missing field, digest mismatch, `snapshot_tampered`, and argv 64.
- **Recommendation.**
  - Check mode must never call `write_receipt()`.
  - Put most finding-id pairs on check mode.
  - Keep capture-mode cases to a minimum, and always pass a scratch `--lane-root`.
  - Use a synthetic stdlib probe stub in the fixture lane's `tools/pin-disposition.py` that only prints a fixed `pin-disposition-v1` document. This avoids live sibling reads.

### F9: LOW. Two reads outside scratch that can't be avoided, and the poison case

- **Evidence.**
  - `evaluate()` calls `os.path.lexists(POISON_PATH)` on a fixed absolute path (`:469`).
  - `base_receipt()` reads `SELF` (`:415-416`).
  - `shutil.which` searches `PATH` (`:517-518`).
  - These are stat/read operations only, with no writes.
- **Recommendation.**
  - Disclose these reads in the registry row's write scope as reads, not writes.
  - **Do not** fixture `poison_path_exists`. Creating `/nonexistent/...` needs privilege and is a write outside temp.
  - Leave that class unexercised and disclose it. The round-14 spotcheck (line 162) says not every finding ID needs its own fixture.

### F10: LOW. Temp files left by a timeout or SIGKILL

- **Evidence.**
  - `write_receipt()` creates `.context-receipt.*.tmp` in the destination dir (`:586-587`). It removes the file on Python exceptions but not on SIGKILL.
  - `run_bounded` timeouts kill only the direct child (`:190-199`), so a grandchild git process can outlive it.
- **Impact.** Inside the selftest this is confined to scratch and removed by `rmtree`. In live capture a crash can leave one stray `.tmp` file in the round-15 evidence dir. It never touches round 14 once F1 and F3 are applied.
- **Fix.** No code change. Disclose it as residual.

### F11: LOW. Plan tension with the frozen-bytes guard

- `witness-metadata.py:1188-1205` re-reads pinned live lane files after its selftest to detect mutation. That is useful, but it is a live read, which this round's interface excludes ("no live reads").
- **Recommendation.**
  - Do not copy that guard into the context-capture selftest.
  - L1's single integrated pass should confirm instead that the round-14 `capture-context.py` and `context-receipt.json` digests are unchanged. The Measure seat already counts these "historical script/receipt digests".
  - L1 should also check that `git status --short` shows no `__pycache__` and no stray `.context-receipt.*.tmp`.

## Exact bounded recommendations (minimum set)

1. Set `LANE_ROOT` to two levels for `tools/`, plus `--lane-root` as the single source for every read, the probe cwd/root, the git `-C` target and the output path. Add no `--output` flag. Output stays at `.ufo/evidence/round-15/context-receipt.json` under the lane root (F1, F2).
2. The selftest never invokes the live historical script except with `--help` or a rejected argument (exit 64). "Old unsupported invocation" is pinned as the new tool's argv rejection, 64 with no write (F3).
3. Either import nothing from the lane, or use `sys.dont_write_bytecode = True` and launch children with `-B` (F4).
4. The selftest uses `mkdtemp(dir="/tmp")`, `try/finally` rmtree, a broad exception mapped to exit 2, git-init'ed fixture lanes, and an explicit child `env`/`cwd`/`stdin`/timeout (F5–F7).
5. Most cases run in read-only check mode. Capture-mode cases use a stub probe. `poison_path_exists` is not fixtured (F8, F9).
6. The registry row's write scope says:
   - Normal capture writes `.ufo/evidence/round-15/context-receipt.json` and its transient `.context-receipt.*.tmp`.
   - Check mode writes nothing.
   - `--selftest` writes only under `/tmp/tameshi-r15-context-capture-selftest.*`.

   L1 verifies the round-14 digests once after the seats return (F10, F11).

## Not claimed

These are not claimed:
- Any execution result.
- That the delivered `tools/context-capture.py` has these properties. It was absent when I read the tree.
- Broader environment independence.
- That the CPython bytecode behaviour was observed. F4 is marked [INFERENCE].
