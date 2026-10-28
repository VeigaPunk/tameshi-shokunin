# T55W1ScoutModes — scratch allocation paths

Scope: where each of the seven `strict_scratch_root()` tools allocates scratch on a real invocation, not only inside `--selftest`. Read-only. No production file edited.

Line numbers are `git grep` at base `0a2010acd1e92e4e332774050825e21bcfc7e079`. For these seven tools that commit equals HEAD `631cd645` (empty `git diff --stat 0a2010ac HEAD -- tools/<seven>`). No LSP server is mounted (`xd://lsp` absent); the census is literal text search, not a semantic reference query. Each helper is a direct call in a single file, and `git grep strict_scratch_root` at base lists only the definition plus the calls below (no getattr, no second name).

Receipts: `.ufo/waves/round-55/w1/T55W1ScoutModes-receipts/`.

## Call table (base)

| tool | call (file:line) | function | modes that reach it |
|---|---|---|---|
| env-diff | `tools/env-diff.py:80` `TemporaryDirectory(dir=strict_scratch_root())` | `execute` ← `probe` ← `surface_result` / `selftest` | **`--contract`** after `read_surface` succeeds (`:154-156`) and `shutil.which("bwrap")` is set (`:77-79` returns `BWRAP_UNAVAILABLE` before the `with`). **`--selftest`** via the `probe` loop (`:175`) and the timeout case (`:182`). The missing-bwrap case (`:180`, `bwrap="/nonexistent/..."`) returns before the `with`. |
| env-diff | `tools/env-diff.py:186` bare `TemporaryDirectory` (no `dir=`) | `selftest` only | **`--selftest` only**, and only if the earlier `execute` calls did not raise. With `bwrap` present, an unusable `TMPDIR` raises at `:80` first, so `:186` is not reached on that arm. |
| repeat-control | `tools/repeat-control.py:611` | `selftest` | **`--selftest` only.** `--snapshot` → `snapshot_mode`; any other argv → `run_mode`. Neither calls the helper (`dispatch`, base). |
| registry-check | `tools/registry-check.py:931` | `selftest` | **`--selftest` only** (first statement of `selftest`). On an unusable `TMPDIR` the parent raises here and does not spawn children. |
| registry-check | `tools/registry-check.py:780` | `clone_lane_at_rev`, called from `main` `:1927` only when `--rev` is set | **Any `--rev` invocation**, including `--selftest` children after the parent scratch at `:931` succeeded (`run_child` argv at `:1097`, `:1641`, `:1653`, `:1662`, `:1676`, `:1689`, `:1722`, `:1738`). Live `--root` without `--rev` does not call it (`live = rev is None`, `:1891`, `:1943-1946`). |
| bash-witness-study | `tools/bash-witness-study.py:1260` | `cmd_selftest` | **`selftest` only.** Nested `mkdtemp` at `:1264` uses `dir=private_root`, not a second helper call. `declare` / `run` / `rerun` / `count` / `check` do not call it (`main` handlers `:1784-1787`). |
| pin-disposition | `tools/pin-disposition.py:725` | `selftest` | **`--selftest` only.** `--manifest` + `--root` → `run_mode` (`main` `:1396-1406`). |
| evidence-disposition | `tools/evidence-disposition.py:2370` | `selftest` | **`--selftest` only.** `--root` + `--dispositions` [`--json`] → `run_mode` (`main` `:3228-3235`). |
| context-capture | `tools/context-capture.py:1639` | `SelftestHarness.__init__`, constructed only at `run_selftest` `:2210` | **`--selftest` only.** `--check` [`--receipt` `--expected`] [`--json`] → `run_check`. The module docstring (`:11-12`) says check mode writes nothing; the call census agrees. |

No `NamedTemporaryFile` / `mkstemp` / `TemporaryFile` in these seven files at base. The only scratch allocation that does **not** pass `dir=strict_scratch_root()` is `env-diff.py:186`.

## Flag — self-test is the only allocation (5 tools)

These tools' only `strict_scratch_root()` call sits inside the self-test. No documented product mode reaches it. A round that "covers every documented mode" is, for these five, covering a branch the product never takes; the product modes are lazy.

- `repeat-control` — only `--selftest` (`:611`). Product: `--snapshot`, and the run mode (argv after `--`).
- `bash-witness-study` — only `selftest` (`:1260`). Product: `declare`, `run`, `rerun`, `count`, `check`.
- `pin-disposition` — only `--selftest` (`:725`). Product: `--manifest` + `--root`.
- `evidence-disposition` — only `--selftest` (`:2370`). Product: `--root` + `--dispositions` [`--json`].
- `context-capture` — only `--selftest` (`:1639`). Product: `--check` with or without `--receipt`/`--expected`.

The counter's five lazy modes are one product mode from each of these five (`--snapshot`, `count`, `--manifest`/`--root`, `--json`, `--check --json`). The other product modes above are also outside the 13 and also do not allocate. Not executed here except `repeat-control --snapshot` (below); the rest is the dispatch plus the single call site.

## Flag — product path that allocates and the counter does not measure

`registry-check --rev` is a documented mode (module docstring `:59-65`, argv `--rev`) and it allocates at `:780`. It is not one of the counter's 8 allocating modes (`c2/measure.py` `modes()`: seven self-tests plus `env-diff --contract`, then five lazy; no `registry-check` product mode).

Executed against the **base** file (a scratch copy of `git show 0a2010ac:tools/registry-check.py`, not the dirty worktree), `TMPDIR` set to a nonexistent directory:

```
python3 <base copy> --root <lane> --rev HEAD
```

exit 2, stderr empty, stdout:

```
REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r55/T55W1ScoutModes/no-such-tmpdir' (could-not-evaluate))
```

Receipts: `registry-rev-base.stdout`, `registry-rev-base.stderr`, `registry-rev-base.exit`. The nonexistent `TMPDIR` was not created (`BAD-ABSENT`).

That line is not the frozen grammar. The grammar wants one stderr line `^[A-Za-z][A-Za-z0-9_.-]*(\.py)?: could-not-evaluate: cannot create clone scratch...`. Base `--rev` prints `REGISTRY_CHECK: could-not-evaluate (` on **stdout**. The measured `--selftest` arm is a different handler (`main` `:1847-1849` at base: `registry-check: could-not-evaluate: {exc}` on stderr) and it fires at `:931` before any `--rev` child. Fixing only the self-test leaves this product path on the old line.

Live `--root` without `--rev` was not executed: that mode runs registry rows in the lane. Source: `clone_lane_at_rev` is called only inside `if rev is not None`.

## env-diff — the one measured product allocation

`bwrap` is `/usr/bin/bwrap` (`bwrap.txt`). With the counter's fixture shape (no `blob_sha256`, so `read_surface` does not pin-fail) and an unusable `TMPDIR`:

```
python3 tools/env-diff.py --contract <scratch contract> --out <scratch> --fleet-root <lane>
```

exit 2, stdout empty, stderr:

```
ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r55/T55W1ScoutModes/no-such-tmpdir' (could-not-evaluate)
```

Receipts: `envdiff-contract.*`. `tools/env-diff.py` was not dirty. This is `execute` `:80`, reached from `--contract`. The same call is what `--selftest` hits first. `:186` is the self-test-only bypass and was not reached on this arm.

## One product mode that does not allocate (executed)

`repeat-control --snapshot .ufo/evidence/round-12/ControlGate` with the same unusable `TMPDIR`: exit 0, `REPEAT_CONTROL: controls_match`, empty stderr, no scratch line (`repeat-snapshot.*`). The process hashed the worktree file (`tool-sha256=a8fad68f…`) because `tools/repeat-control.py` is dirty, but the uncommitted diff only adds the `ScratchRootUnusable` handler; `snapshot_mode` is unchanged and does not call the helper.

## Worktree drift during this scout (not base)

Uncommitted, not this seat, do not treat as the tree the counter measures:

```
tools/context-capture.py  | 11 ++++++++++-
tools/registry-check.py   | 14 +++++++++++++-
tools/repeat-control.py   | 22 +++++++++++++++++++++-
```

`worktree-drift-stat.txt`. The diffs add a `ScratchRootUnusable` type and a stderr grammar print. They do not add a `strict_scratch_root()` call. A first `--rev` probe accidentally ran the dirty `registry-check.py` and got the new stderr line (`registry-rev-worktree-drift.*`); that is not the base result above.

## Counter map vs this census

| counter class | modes | what actually allocates |
|---|---|---|
| 8 allocating | 7 self-tests + `env-diff --contract` | all 8 do call `strict_scratch_root` (env-diff `--contract` only after a readable surface and `bwrap`) |
| 5 lazy | snapshot, count, pin read, evidence `--json`, context `--check` | none call it |
| not in the 13 | `registry-check --rev` | **does** allocate (`:780`), different stdout line at base |
| not in the 13 | registry-check live `--root`; bash-witness `declare`/`run`/`rerun`/`check`; repeat-control run mode; context-capture explicit receipt check | do not call it |

## Confidence

High on the call census and on the two executed product probes (`--rev` at base, `env-diff --contract`). High that the five flagged tools have no second call site (one textual hit each, dispatch read). Not executed: the five self-tests (the frozen before receipt already scores them `grammar=6/8`), bash-witness `declare`/`run`/`rerun`/`check`, repeat-control run mode, registry-check live `--root`, and `env-diff.py:186` under a missing `bwrap`.
