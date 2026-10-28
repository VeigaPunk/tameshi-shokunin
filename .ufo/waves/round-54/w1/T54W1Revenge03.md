# T54W1Revenge03 — every documented invocation of the seven scratch-root tools under an unusable TMPDIR

Item: the mapping is at each tool's entry point. Enumerate every documented invocation of the
seven tools (`--help`, USAGE strings, `tools/registry.json` argv, SKILL text) and show that each
one, under an unusable TMPDIR, exits 2 with a naming line and no traceback. A `--selftest`-only
proof that misses another documented mode is the finding.

Verdict: **the claim fails outside `--selftest`.** Two documented modes of the seven tools reach
`strict_scratch_root()` and do not produce the could-not-evaluate class: one prints a traceback and
exits 1 (`env-diff.py --contract`, at C0), one turns a row's exit-2 could-not-evaluate into a
`differs` verdict and exits 1 (`registry-check.py --root`). A third documented mode exits 2 but
never names the value or the cause (`bash-witness-study.py run`/`rerun`). The seven `--selftest`
entries themselves all hold the class in both arms.

## Revisions measured, and why there are two

The lane's HEAD moved while I was measuring: C0 `59c3810` was HEAD when I started, and
`99c3bc8` ("C1 fix pass — … the env-diff run-path class") landed mid-sweep. A first pass against
the live lane therefore mixed revisions; every number below was re-measured in two isolated
`git clone --shared` fixtures, `$S/clone` at C0 and `$S/tip` at the C1 fix pass, both asserted
clean (`git status --porcelain` empty) before the sweep:

```
$ git -C $S/clone log --oneline -1
59c3810 round-54: C0 content — one scratch-root exit class across seven tools ... 
$ git -C $S/tip   log --oneline -1
99c3bc8 round-54: C1 fix pass — 26 wave-1 reader findings adjudicated and fixed (... the env-diff run-path class), QUALITY 105
$ git -C $S/tip status --porcelain     # empty
```

C0 full id (from `.ufo/waves/round-54/spec-w1.json`, 40 hex):
`59c38109bf119d0e9d4f878644a82babc937bc1e`. Note: the C0 id in my ticket text is **39 hex**
(`…ababc937c1e`, missing the `b`), which `git` rejects as `fatal: Not a valid object name`; the
spec's 40-hex string resolves and is what I cloned. Harness artifact, not a lane defect; I did not
transliterate it anywhere else.

Arms, identical for both fixtures: `TMPDIR=/nonexistent/r54-revenge03-tmpdir` (set, unusable),
`TMPDIR=""` (declared unset), `TMPDIR=$S/usable` (fresh directory). `env-diff` runs carry
`--fleet-root /home/vgpnk/Projects/shokunin` because its default derives from the tool path, which
inside a clone is the scratch parent; the flag is documented and does not change the scratch path.

## Static map of `strict_scratch_root()` call sites (AST, enclosing functions)

`receipts/ast-call-sites.json`, produced by walking each tool's AST:

| tool | call site | enclosing chain |
|---|---|---|
| env-diff | :80 | `execute` (used by `probe` ← `surface_result` ← `main --contract`, and by `selftest`) |
| bash-witness-study | :1260 | `cmd_selftest` |
| evidence-disposition | :2370 | `selftest` |
| pin-disposition | :725 | `selftest` |
| context-capture | :1639 | `SelftestHarness.__init__` ← `run_selftest` |
| registry-check | :780 / :931 | `clone_lane_at_rev` (reachable from `main --rev`) / `selftest` |
| repeat-control | :611 | `selftest` |

So exactly two of the seven allocate scratch through `strict_scratch_root()` on a documented
**non**-selftest path: `env-diff --contract` and `registry-check --rev`. Both are exercised below.

## Matrix: documented invocation × TMPDIR arm

Documentation sources: tool docstrings/USAGE parsed from `--help` and the module text; the seven
`scratch_root` rows of `tools/registry.json`; and, at C0 (`git show 59c3810:SKILL.md`, 2197 lines),
the invocation rows at `SKILL.md:1517`, `:1528` (repeat-control), `:1529`, `:2168` (bash-witness
`count`/`check`), `:1560`, `:1577`, `:1879`, `:2177` (pin-disposition), `:1609`, `:1627`, `:1707`,
`:1861`, `:1876`, `:2172` (evidence-disposition), `:1706`, `:2170` (context-capture), `:1865`,
`:1877`, `:2180` (registry-check), `:2001`, `:2171` (env-diff). The `--help`/no-arg rows are the
informational/usage modes (`SKILL.md:1730`, "Help exits0 only as a non-verdict informational
mode"); 64 is the documented usage exit.

All rows below were run with `cwd` = the fixture tree and `PYTHONDONTWRITEBYTECODE=1`, one process
per row; `receipts/matrix-C0.json` and `receipts/matrix-tip.json` record every row's `argv`, exit
code, traceback flag, naming flag and last output line, and the decisive raw captures are stored
beside them:

| invocation | scratch chain | C0 rc | C0 names TMPDIR | C0 traceback | tip rc | tip names TMPDIR | tip traceback |
|---|---|---|---|---|---|---|---|
| `env-diff --help` | no | 0 | – | no | 0 | – | no |
| `env-diff noargs` | no | 64 | – | no | 64 | – | no |
| `env-diff --selftest` | yes (main→selftest) | 2 | y | no | 2 | y | no |
| `env-diff --contract` | yes (main→surface_result→probe→execute) | **1** | y | **YES** | 2 | y | no |
| `env-diff --contract --jobs 1` | yes (same chain) | **1** | y | **YES** | 2 | y | no |
| `bash-witness --help` | no | 0 | – | no | 0 | – | no |
| `bash-witness count` | no | 0 | – | no | 0 | – | no |
| `bash-witness check` | no | 1 | – | no | 1 | – | no |
| `bash-witness selftest` | yes (cmd_selftest) | 2 | y | no | 2 | y | no |
| `bash-witness declare` | no | 0 | – | no | 0 | – | no |
| `bash-witness run` | no in-process (runner inherits TMPDIR) | 2 | **–** | no | 2 | **–** | no |
| `bash-witness rerun` | no in-process (runner inherits TMPDIR) | 2 | **–** | no | 2 | **–** | no |
| `evidence-disposition --help` | no | 0 | – | no | 0 | – | no |
| `evidence-disposition run` | no | 0 | – | no | 0 | – | no |
| `evidence-disposition --selftest` | yes (selftest) | 2 | y | no | 2 | y | no |
| `pin-disposition --help` | no | 0 | – | no | 0 | – | no |
| `pin-disposition run` | no | 0 | – | no | 0 | – | no |
| `pin-disposition --selftest` | yes (selftest) | 2 | y | no | 2 | y | no |
| `context-capture --help` | no | 0 | – | no | 0 | – | no |
| `context-capture --check` | no | 0 | – | no | 0 | – | no |
| `context-capture --check --receipt --expected` | no | 1 | – | no | 1 | – | no |
| `context-capture --selftest` | yes (run_selftest→SelftestHarness.__init__) | 2 | y | no | 2 | y | no |
| `registry-check --help` | no | 0 | – | no | 0 | – | no |
| `registry-check --selftest` | yes (selftest) | 2 | y | no | 2 | y | no |
| `registry-check --rev HEAD` | yes (main→clone_lane_at_rev) | 2 | y | no | 2 | y | no |
| `registry-check --rev HEAD --tag baseline` | yes (same) | 2 | y | no | 2 | y | no |
| `registry-check --rev HEAD --registry tools/registry.json` | yes (same) | 2 | y | no | 2 | y | no |
| `registry-check --rev HEAD --only … --json` | yes (same) | 2 | y | no | 2 | y | no |
| `registry-check --root LANE --only context-capture-selftest --json` | row allocates (child process) | **1** | y | no | **1** | y | no |
| `repeat-control --help` | no | 0 | – | no | 0 | – | no |
| `repeat-control --snapshot .ufo/evidence/round-12/ControlGate` | no | 0 | – | no | 0 | – | no |
| `repeat-control --runs 3 --out DIR -- python3 -c 'print(1)'` | no | 0 | – | no | 0 | – | no |
| `repeat-control --selftest` | yes (selftest) | 2 | y | no | 2 | y | no |

Extra registry-argv rows (the non-selftest rows that belong to these tools), tip arm, unusable
TMPDIR — all keep their documented expectations and touch no scratch:

| registry row argv | rc | documented |
|---|---|---|
| `repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch` | 1 | 1 |
| `context-capture.py --check --receipt …/mapping-suffix/receipt.json --expected …/mapping-suffix/expected.json` | 1 | 1 |
| `evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json` | 1 | 1 |
| `pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 | 0 |
| `evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` | 0 | 0 |
| `context-capture.py --check` | 0 | 0 |

Controls (usable TMPDIR, tip fixture, all exit 0; the two tool-printed lines are retained as
`receipts/tip-env-diff-selftest-usable.stdout`, `receipts/tip-registry-selftest-usable.stdout`,
`receipts/tip-bash-witness-run-usable.stdout`):
`env-diff --selftest` (`ENVDIFF_SELFTEST: 9/9 pass`), `bash-witness selftest`,
`evidence-disposition --selftest`, `pin-disposition --selftest`, `context-capture --selftest`,
`registry-check --selftest` (`SELFTEST: PASS (51 cases)`), `repeat-control --selftest`,
`registry-check --rev HEAD --only context-capture-selftest --json`, and
`bash-witness run` (`WITNESS_RUN: complete — killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10`). Empty-TMPDIR arm on the two run paths: `env-diff --contract` exit 0
(`ENVDIFF: classified=9/9`), `registry-check --rev HEAD --only …` exit 0
(`REGISTRY_CHECK: held=1/1 superseded=0`). Two extra unusable shapes at tip — TMPDIR a regular
file and a `chmod 500` directory — both exit 2 with the value named and no traceback
(`receipts/tip-env-diff-tmpdir-file-shape.stderr`, `…-readonly-shape.stderr`,
`receipts/tip-registry-selftest-tmpdir-file-shape.stderr`).

## Findings

### F1 (blocking at C0, fixed at `99c3bc8`) — `env-diff.py --contract` tracebacks and exits 1

Documented at `tools/env-diff.py:3`
(`Usage: env-diff.py --contract FILE --out FILE [--fleet-root DIR] [--jobs N]`),
`tools/env-diff.py:9` (`Exit 0 all surfaces classified, 1 unavailable surface, 2 setup/input error,`),
`SKILL.md:2001` and `SKILL.md:2171`. Command (C0 fixture, `cwd` = clone):

```
$ TMPDIR=/nonexistent/r54-revenge03-tmpdir python3 tools/env-diff.py \
    --contract .ufo/evidence/round-21/c2-contract.json --out …/envdiff-C0.json \
    --fleet-root /home/vgpnk/Projects/shokunin --jobs 3
```

Exit 1, stderr (`receipts/c0-env-diff-contract.stderr`, tail; the fixture path in the first line is
abridged to `…`):

```
  File "…/tools/env-diff.py", line 45, in strict_scratch_root
    raise ScratchRootUnusable(
        "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
ScratchRootUnusable: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/r54-revenge03-tmpdir' (could-not-evaluate)
```

Cause: `ScratchRootUnusable` is raised inside the `ThreadPoolExecutor` worker (via
`probe → execute`, `tools/env-diff.py:80`) and re-raised by `list(pool.map(…))` at
`tools/env-diff.py:247`, but `main`'s run path only catches
`except (OSError, ValueError, KeyError, TypeError)`; the scratch-root raise is a `RuntimeError`
subclass and escapes. `--jobs 1` fails identically (`receipts/c0-env-diff-contract-jobs1.stderr`, same final
`ScratchRootUnusable` line), so it is not a threading race. Same command with `TMPDIR=$S/usable` exits 0 and prints
`ENVDIFF: classified=9/9` (`receipts/c0-env-diff-contract-usable.stdout`) — the mode works, only
the scratch-root arm is mis-mapped.

Fix already present at `99c3bc8` (not mine, the C1 pass): an `except ScratchRootUnusable` clause
before the generic tuple at `tools/env-diff.py:263`. Verified at the tip fixture:

```
$ TMPDIR=/nonexistent/r54-revenge03-tmpdir python3 tools/env-diff.py --contract … --jobs 3
ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/r54-revenge03-tmpdir' (could-not-evaluate)
$ echo $?
2
```

(`receipts/tip-env-diff-contract.stderr`.) Verdict: real, measured, and closed at the tip — but the
`--selftest`-only C2 proof could not see it, which is exactly the gap this seat was sent to find.

### F2 (open at C0 and at tip) — `registry-check.py --root` reports a could-not-evaluate row as `differs`, exit 1

Documented at `tools/registry-check.py:64-66`:
`--root DIR   lane to run against; default: the lane containing this script` /
`(the parent of tools/). Live mode prints a stderr warning that` /
`rows may write into the root; prefer --rev.`;
exit doctrine at `tools/registry-check.py:52-53`
(`Exits: 0 all held · 1 any differs · 2 could-not-evaluate (registry` /
`unreadable/invalid, root or rev missing, clone failure, --only/--tag miss) ·`); row vocabulary at
`tools/registry-check.py:48`
(`ROW <name> expect=<exit> got=<exit|timeout|unavailable|non-hermetic> held|differs`).

```
$ TMPDIR=/nonexistent/r54-revenge03-tmpdir python3 tools/registry-check.py \
    --root $S/clone --only context-capture-selftest --json    # C0 fixture
registry-check: warning: live --root mode runs rows in the lane; rows may write into the root (use --rev to grade a throwaway clone)
ROW context-capture-selftest expect=0 got=2 differs
REGISTRY_CHECK: held=0/1 superseded=0
$ echo $?
1
```

(`receipts/c0-registry-live-root-warning.stderr`, `receipts/tip-registry-live-root-warning.stderr` —
identical at both revisions; the `--json` report bodies are `receipts/c0-registry-live-root.json` and
`receipts/tip-registry-live-root.json`.) The row itself is a child process that cannot allocate scratch: its own stdout,
captured in the report, is
`SELFTEST: FAIL (setup error: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/r54-revenge03-tmpdir' (could-not-evaluate))`
and its exit is 2. `registry-check` turns that into a lane verdict:

```
tools/registry-check.py:720:    fragment["held"] = got == expected_exit and not missing and cleanup_ok
tools/registry-check.py:898:    return (0 if held == len(active) else 1), report
```

So a child that says could-not-evaluate and exits 2 is graded `differs` — a defect verdict about
the lane, not a could-not-evaluate about the environment. Control, same fixture, usable TMPDIR:

```
$ TMPDIR=$S/usable python3 tools/registry-check.py --root $S/clone --only context-capture-selftest --json
ROW context-capture-selftest expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
```
(exit 0)

(`receipts/tip-registry-live-usable.stdout`.) The round-18 comment at
`tools/registry-check.py:781` shows the same inversion was already considered for the clone
allocation itself —

```
    except OSError as exc:  # round-18 w2 CR47: an unusable /tmp is could-not-evaluate (2), never "differs" (1)
```

— but only for that one allocation, not for a row's own scratch class. `--rev` does not expose the
inversion (the clone allocation fails first and keeps the class):

```
REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/r54-revenge03-tmpdir' (could-not-evaluate))
```

(`receipts/c0-registry-rev.stdout`.) So live `--root` is the exposed documented shape.
Verdict: open. Not introduced by C0 — inherited — but it contradicts the wave's "one scratch-root
exit class" claim for any caller that grades rows on a host with a broken TMPDIR.

### F3 (open at C0 and at tip) — `bash-witness-study.py run`/`rerun` exit 2 without naming the value or the cause

Documented at `tools/bash-witness-study.py:13-14`
(`run       refuse unless declared.tsv matches its recorded digest, then execute` /
`the pinned mutation CLI sweep (tools/mutate-and-run.sh, all 10`), in the `--help` subcommand list,
and exit class at `tools/bash-witness-study.py:36-37`
(`Exit codes: 0 ok/clean · 1 failed (tamper, mismatch, inconclusive) ·` /
`2 cannot evaluate (missing inputs, pin mismatch, runner SETUP) ·`,
the second line indented under `Exit codes:` in the source).

```
$ TMPDIR=/nonexistent/r54-revenge03-tmpdir python3 tools/bash-witness-study.py \
    --evidence $S/bwev-C0 --kagi /home/vgpnk/Projects/shokunin/kagi-shokunin run
WITNESS_RUN: could-not-evaluate — runner did not complete (setup/usage refusal): runner-exit=2
WITNESS_RUN: summary $S/bwev-C0/summary.json
$ echo $?
2
```

(`receipts/c0-bash-witness-run.stdout`; `rerun` prints the same two lines plus its preserved-summary
line, both revisions.) Exit and class are right and there is no traceback, but the value and the
cause appear only in the retained log, never on the tool's own output — from
`receipts/tip-bash-witness-run-unusable-cli.log`:

```
  | mktemp: failed to create directory via template ‘/nonexistent/r54-revenge03-tmpdir/tmp.XXXXXXXXXX’: No such file or directory
MUTATE: SETUP (control run on the pristine copy is red (exit=1); cannot attribute kills; log: …)
```

Control, usable TMPDIR:

```
WITNESS_RUN: complete — killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10
```

(exit 0; `receipts/tip-bash-witness-run-usable.stdout`). Verdict: the "could-not-evaluate" half of the class holds, the
"naming the TMPDIR value" half does not, for a documented mode whose failure is caused by exactly
that variable. Minor: a reader cannot tell from the tool's output whether TMPDIR, kagi, or the
target refused.

## Cleared by this sweep (checked, no finding)

- `--help` for all seven: exit 0, no scratch (documented informational mode, `SKILL.md:1730`).
- `env-diff` with no arguments: exit 64 usage, no scratch:

```
ENVDIFF_USAGE: --contract and --out are required; --jobs must be 1..3
```

  (`receipts/c0-env-diff-noargs.stderr`).
- `bash-witness count`, `check`, `declare`; `evidence-disposition run`; `pin-disposition run`;
  `context-capture --check` (frozen and pinned); `repeat-control --snapshot`, `--runs`: identical
  exit codes in both TMPDIR arms (0/1 as documented), no scratch allocation on their AST chain, no
  traceback. `declare` writes only into the caller-named `--evidence` directory.
- `bash-witness check` exits 1 in **both** arms with the same two lines
  (`WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda committed=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`,
  `WITNESS_CHECK: FAIL (1 problems; 96 files covered)`) — pre-existing evidence drift, not
  attributable to TMPDIR, and out of this seat's surface (`receipts/c0-bash-witness-check.stdout`).
- TMPDIR shapes: a regular file and a `chmod 500` directory produce the same exit 2 with the value
  named at tip for `registry-check --selftest` and `env-diff --contract`.
- `context-capture --selftest` prints `SELFTEST: FAIL (setup error: RuntimeError: …(could-not-evaluate))`
  — the word FAIL in the text, but exit 2, the value named, no traceback, so the machine class is
  right. Noted, not reported as a defect.

## Receipts index (this directory)

| file | what it holds |
|---|---|
| `matrix-C0.json`, `matrix-tip.json` | every matrix row at C0 / at the tip: argv, exit, traceback flag, naming flag, last line |
| `ast-call-sites.json` | AST map of every `strict_scratch_root()` call site and its enclosing chain |
| `c0-env-diff-contract.stderr`, `c0-env-diff-contract-jobs1.stderr` | F1: the two C0 tracebacks |
| `tip-env-diff-contract.stderr`, `tip-env-diff-tmpdir-file-shape.stderr`, `tip-env-diff-tmpdir-readonly-shape.stderr` | F1 fixed at tip, plus the two extra unusable TMPDIR shapes |
| `c0-env-diff-contract-usable.stdout`, `tip-env-diff-empty-arm.stdout` | env-diff `--contract` control (usable) and empty-TMPDIR arm |
| `c0-registry-live-root-warning.stderr`, `tip-registry-live-root-warning.stderr` | F2: the `ROW … got=2 differs` verdict at both revisions |
| `c0-registry-live-root.json`, `tip-registry-live-root.json` | F2: the `--json` report bodies naming the row's TMPDIR |
| `tip-registry-live-usable.stdout` | F2 control: the same row `held`, exit 0 |
| `c0-registry-rev.stdout` | `--rev` keeps the class (exit 2) |
| `tip-registry-rev-empty-arm.stdout` | empty-TMPDIR arm for `--rev` |
| `c0-context-capture-selftest.stdout` | the row-side `SELFTEST: FAIL (setup error: …could-not-evaluate)` line |
| `c0-bash-witness-run.stdout`, `tip-bash-witness-run-unusable-cli.log` | F3: exit 2 without naming, and the retained log that does name `mktemp`/TMPDIR |
| `tip-bash-witness-run-usable.stdout` | F3 control: complete sweep, exit 0 |
| `c0-bash-witness-check.stdout` | the pre-existing `WITNESS_CHECK: DRIFT` that is identical in both arms |
| `c0-*-selftest*`, `tip-*-selftest-usable.stdout`, `c0-env-diff-noargs.stderr` | the seven selftests and the usage row |

## Hygiene

No installs or upgrades were needed (no tool recorded). No lane production file, counter, contract,
freeze, ledger or wave spec was edited by me; the only writes are this file and its receipts
directory. Two tracked files under `.ufo/evidence/round-54/` (`c2/measure.py`, `deciding-run.sh`) showed as
modified by another process during this seat; I only read them and never wrote them, and the
`git status --porcelain` I ran at the start of the sweep listed neither.
All git use was read-only (`clone --shared`, `log`, `status`, `diff`, `archive`) against fixtures
under `$HYAKU_SCRATCH/tameshi-r54/T54W1Revenge03/`, each asserted with
`git -C <fixture> rev-parse --show-toplevel`; the scratch tree is removed at the end of the run.
