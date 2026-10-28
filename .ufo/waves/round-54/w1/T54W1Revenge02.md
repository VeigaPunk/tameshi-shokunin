# T54W1Revenge02 — attack: scratch-root paths that bypass the mapped entry point (C0)

Candidate: `59c38109bf119d0e9d4f878644a82babc937bc1e` (C0). Lane head at seat start: `59c3810`; head at
seat end: `99c3bc8` (C1 fix pass, see *Drift observed*). All C0 evidence below was taken from a
`git clone --shared` copy of the lane at C0 under my scratch
(`…/T54W1Revenge02/clone-c0`, `git rev-parse --show-toplevel` = the clone, HEAD = `59c38109bf11`,
`tools/env-diff.py` sha256 = `ab193692d78d591fa7c9e55ba9c53cbe88376354adf548cd9d5034ce722bfe56` =
`git show 59c38109bf11:tools/env-diff.py` blob), so a concurrent lane edit could not contaminate it.

## Verdict

- **One live path at C0 can traceback**: `env-diff.py --contract/--out` (its *documented primary mode*)
  exits **1** with a full `ScratchRootUnusable` traceback and writes **no** receipt, on every unusable-root
  shape. Every other entry point of the four edited tools fails closed at C0.
- Three latent paths still traceback **if reached outside `main()`** (direct function call / a future
  scratch call inside `pin-disposition.run_mode`). None is reachable through the shipped CLIs at C0; they are
  mapped-gap evidence, not live defects.
- The live C0 defect is fixed at lane head `99c3bc8` by three added lines in `env-diff.py main()`
  (verified, receipt 09). The frozen C0 claim itself is unaffected: C2 measures only the `--selftest` arm.

## Path inventory (C0 line numbers, `05-call-sites-at-c0.txt`)

| tool | only scratch call site | entry point that reaches it | mapping that catches it | C0 outcome |
|---|---|---|---|---|
| `tools/env-diff.py` | `:80` in `execute()` | **`main()` contract branch** → `probe()` (`:130`) → `execute()` (`:80`), workers of `ThreadPoolExecutor` (`:247`) | selftest branch mapped `:231-236`; contract branch `except (OSError, ValueError, KeyError, TypeError)` `:263` omits `RuntimeError`; `surface_result` `:157` omits it | **exit 1 + traceback, no receipt** |
| `tools/bash-witness-study.py` | `:1259-1260` in `cmd_selftest()` | `selftest` handler | `main()` `:1787-1790` wraps every handler | exit 2, one line |
| `tools/pin-disposition.py` | `:725` in `selftest()` | `--selftest` | `main()` `:1396-1399` | exit 2, one line |
| `tools/evidence-disposition.py` | `:2370` in `selftest()` | `--selftest` | `main()` `:3228-3231`, plus blanket `:3238` | exit 2, one line |

No module-level (import-time) call exists in any of the four: each module was imported under
`TMPDIR=/nonexistent` and none raised (`03-reachability-sweep.txt`).

## F1 — live at C0: `env-diff.py --contract` reaches the scratch root outside the mapped try

The call is inside a worker thread, and both exception filters on the way out name the wrong classes:

```python
    with tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff.", dir=strict_scratch_root()) as tmp:   # :80
...
        with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:                                      # :246
            rows = list(pool.map(lambda s: surface_result(a.fleet_root, s), surfaces))                   # :247
...
    except (OSError, ValueError, KeyError, TypeError) as exc:                                            # :263
```

while the only mapping is on the other branch:

```python
        try:
            return selftest()
        except ScratchRootUnusable as exc:                                                               # :234
```

Command (from the C0 clone; fixture = a fresh `git init` repo under scratch, contract pin matches):

```
TMPDIR=/nonexistent python3 tools/env-diff.py --fleet-root "$D" --contract "$D/contract.json" --out "$S/run/out-nonexistent.json"
```

Output (`02-env-diff-contract-traceback.txt`), on three distinct unusable-root shapes:

```
## arm=nonexistent TMPDIR=/nonexistent
exit=1
traceback_lines=1
receipt_written=no
    raise ScratchRootUnusable(
ScratchRootUnusable: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent' (could-not-evaluate)

## arm=read-only-dir TMPDIR=…/ro        → exit=1 traceback_lines=1 receipt_written=no
## arm=regular-file TMPDIR=…/notadir    → exit=1 traceback_lines=1 receipt_written=no
## 3-surface contract, bad TMPDIR       → exit=1 traceback_lines=1 receipt_written=no
```

Controls in the same receipt: same three roots through `--selftest` → `exit=2`, 1 stderr line, 0 traceback
lines; `--contract` with `TMPDIR=` (declared unset) and with a fresh usable dir → `exit=0`,
`ENVDIFF: classified=1/1`. The path itself works; only the exit class is broken.

Why it matters for operability, at C0:

1. The tool's own docstring promises the class: `Exit 0 all surfaces classified, 1 unavailable surface, 2 setup/input error,`
   (`tools/env-diff.py:10`).
2. `SKILL.md:2001` documents `python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out …`
   with `0 all surfaces classified; 1 incomplete/failed measurement; 2 could-not-evaluate; 64 usage`, and
   `SKILL.md:2171` repeats `0 clean; 1 failed; 2 and 64 could-not-evaluate`. At C0 that command yields **1**.
3. `corpus/knowledge/hermetic-env-differential.md:3` documents the same `--contract` recheck command.
4. No `tools/registry.json` row pins it: the only env-diff row is `env-diff-selftest`
   (`registry.json` rows), so the broken path has no registry coverage either.

Cross-check by injection (`03-reachability-sweep.txt`, sentinel replacing `strict_scratch_root`):

```
 "env-diff [--fleet-root FLEETFX --contract CONTRACT --out OUT]": {"reached": true, "exc": "ScratchRootUnusable", "msg": "PROBE-REACHED"}
# decisive single case: reached=True uncaught=ScratchRootUnusable msg=SENTINEL-REACHED
```

## F2 — same C0 path: exit 1 collides with "1 unavailable surface" and leaves a stale `--out` file

`env-diff.py:10` assigns exit 1 the meaning "unavailable surface"; `main()` returns 1 whenever
`done != len(rows)` (`:266-268`). A setup refusal therefore reads as "measurement incomplete", and because
`a.out.write_text(...)` (`:262`) is never reached, a pre-existing `--out` file survives untouched:

```
printf '{"stale": true}\n' > stale.json
TMPDIR=/nonexistent python3 tools/env-diff.py --fleet-root "$D" --contract "$D/contract.json" --out stale.json
exit=1 file_after={"stale": true}
```

A caller that only checks the exit code or re-reads its previous receipt cannot distinguish this from a
genuine "one surface unavailable" run. (Command and output: `02-env-diff-contract-traceback.txt`.)

## F3 — latent: the scratch call in all four tools sits *before* the function's own `try`

Each scratch call is the first statement of the selftest function, with no local guard; the exit class exists
only because `main()` wraps the dispatch:

- `bash-witness-study.py:1259-1260` `private_root = Path(tempfile.mkdtemp(` / `prefix="bash-witness-selftest-private.", dir=strict_scratch_root()))` precedes `root = None` / `try:` (`:1262-1263`);
- `pin-disposition.py:725` `scratch = tempfile.mkdtemp(prefix="tameshi-r13-pin-disposition-selftest.", dir=strict_scratch_root())` is the first line of `selftest()`;
- `evidence-disposition.py:2370` likewise;
- `env-diff.py` reaches the same `execute()` (`:80`) from `selftest()` at `:180` and `:182` (and via `probe()` `:129`→`:130` at `:175`); those are covered by `main()`'s selftest branch (`:231-236`), but `execute()` is shared with the contract branch, which is exactly F1.

Direct call under an unusable root (`04-injection-mapping.txt`, `TMPDIR=/nonexistent`):

```
 "direct env-diff.selftest()": {"uncaught": "ScratchRootUnusable", ...}
 "direct bash-witness-study.cmd_selftest()": {"uncaught": "ScratchRootUnusable", ...}
 "direct pin-disposition.selftest()": {"uncaught": "ScratchRootUnusable", ...}
 "direct evidence-disposition.selftest()": {"uncaught": "ScratchRootUnusable", ...}
```

No shipped CLI invokes them this way: the lane's only by-path module loaders load `registry-check.py`
(`tools/registry-replay.py:164`), the round-18/22/49 measures (`tools/wave-accounting.py:149`,
`tools/shrink-case.py:221`, `.ufo/evidence/round-54/c1/measure.py:166`) — never these four (receipt 10);
`registry.json` rows and the C2 counter use the CLI, so this is latent, not live: it is the same shape as F1 and would re-open the hole if any
harness ever imported `selftest()`/`cmd_selftest()`.

## F4 — latent mapping gap: `pin-disposition.run_mode` catches only `InvalidInput`

`pin-disposition.py:1406-1407` maps `run_mode` failures through `except InvalidInput as exc:` only. `run_mode`
does not call the scratch root at C0, so this is not reachable today; injection proves the gap would be a
traceback the moment it did:

```
 "pin run_mode, helper raises": {"uncaught": "ScratchRootUnusable", "msg": "INJECTED", "stderr": ""}
```

For contrast, the same injection through the other mappers is closed:

```
 "bw count, helper raises": {"rc": 2, "stderr": "WITNESS_STUDY: could-not-evaluate: INJECTED"}
 "evd run_mode, helper raises": {"rc": 2, "stdout": "{ \"error\": { \"kind\": \"internal_error\", … } \"exit\": 2 …"}
```

(`evidence-disposition.py:3238` `except Exception as exc:  # fail closed, never exit 1 on an internal error`
converts any scratch raise into exit 2 `could_not_evaluate`, though it labels it `internal_error` rather than
naming the scratch class — closed, just less legible.)

## What I checked and found closed

- Import-time: no call at module import in any of the four (import under `TMPDIR=/nonexistent`), `03`.
- Non-selftest modes of the other three never reach the scratch root — instrumented sentinel never fired for
  `count`, `check`, `run`, `rerun`, `--manifest/--root`, `--root/--dispositions`, `[]` (`03`), and each mode's
  stdout is byte-identical between `TMPDIR=/nonexistent` and `TMPDIR=` (`06`):
  `bw-count exit 0/0 identical`, `bw-check exit 1/1 identical` (a pre-existing non-scratch problem, same in
  both arms), `pin exit 0/0 identical`, `evd exit 0/0 identical`.
- Selftest arms of all four, four roots (`06`): `unset=0 empty=0 unusable=2 usable=0`, the unusable arm being
  one `could-not-evaluate` line naming the TMPDIR value, no traceback.
- `evidence-disposition` reaches scratch only in `selftest()`, under both mappings (`3231`, `3238`).

## Drift observed (not mine; I edited no lane file)

Mid-seat the lane's working tree gained an uncommitted `tools/env-diff.py` edit (mtime `2026-10-28 11:37:38`,
sha256 `57f26a21…`, HEAD still `59c3810`), then the lane advanced to `99c3bc8` whose message includes
"the env-diff run-path class". Diff `59c38109bf11..99c3bc8 -- tools/env-diff.py` is exactly:

```
+    except ScratchRootUnusable as exc:
+        print("ENVDIFF_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
+        return 2
```

Verification at the tip (`09-tip-verification.txt`, blob sha256 `57f26a21…`): all three unusable-root arms →
`exit=2`, `traceback_lines=0`, one `could-not-evaluate` line, no receipt. F1/F2 are therefore closed at the
tip; they stand at the frozen C0 candidate, which is what the wave judges. Nothing else under `tools/`
changed between C0 and the tip (1 file, +3 lines), and C2's counter is unchanged, so the other three tools'
state above is the tip state too.

## Coverage caveat for C2 / the registry

C2's counter exercises only the `--selftest` argv of the seven tools (`c2/measure.py`, `TOOLS` list). Its
"one scratch-root exit class" statement is true for that entry point and silent about every other one — at
C0 `env-diff --contract`, the tool's documented primary mode, broke the class with a traceback. If the class
is meant to be tool-wide rather than selftest-wide, the counter needs the run-path arm; if it is meant to be
selftest-only, `SKILL.md:2001`/`:2171` should not have promised `2 could-not-evaluate` for `--contract`
(now true again only because `99c3bc8` patched the run path).

## Receipts

All under `.ufo/waves/round-54/w1/T54W1Revenge02-receipts/`:

| file | content |
|---|---|
| `00-predrift-worktree-run.txt` | first reproduction from the lane working tree before the concurrent edit (same traceback) |
| `01-fixture.txt` | `mktemp -d` fixture repo + `git -C "$D" rev-parse --show-toplevel` guard PASS + pinned contract |
| `02-env-diff-contract-traceback.txt` | F1/F2 at C0: three bad-root arms, 3-surface arm, stale `--out`, selftest controls, empty/usable arms |
| `03-reachability-sweep.txt` | instrumented `strict_scratch_root` reach sweep, 15 argv cases at C0 + decisive sentinel case |
| `04-injection-mapping.txt` | mapping probes: bash-witness/evidence closed, pin `run_mode` gap, direct-call tracebacks |
| `05-call-sites-at-c0.txt` | every definition/call site and every `except` clause per tool, with blob sha256 |
| `06-other-three-invariance.txt` | bad-vs-empty `TMPDIR` invariance, four selftest arms per tool |
| `07-census.txt` | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0 |
| `08-drift-observed.txt` | uncommitted edit observed, its diff, sha256s (read-only) |
| `09-tip-verification.txt` | same three arms against tip `99c3bc8` → exit 2, no traceback |
| `10-citations.txt` | docstring/`SKILL.md:2001`/`:2171`/knowledge-note/registry/env-diff row text and the by-path module loaders, read from the C0 clone |

Reproduce: `export HYAKU_SCRATCH=/fast/scratch/hyaku`; fixture as in receipt 01; then the commands quoted in
each receipt. Lane files were only read; the only writes are this report and its receipts directory.

Scratch (`$HYAKU_SCRATCH/tameshi-r54/T54W1Revenge02/`) was removed at the end of the seat.
