# T54W2Crit02 — C2 measured-scope gap: env-diff `--contract` at C1

- Seat: `T54W2Crit02` (critic, leaf). Round 54 / hyaku run 11 / L1 `TameshiR54a2`.
- Axes: **discernment**, **calibration**.
- Attack: C2 measures the seven `--selftest` arms only; wave-1 named `tools/env-diff.py --contract` as the non-self-test mode that allocates scratch via `strict_scratch_root()`.
- Cand: `99c3bc88d704566197783f66b211ee0a830e0330` (C1). Contrast: C0 `59c38109bf119d0e9d4f878644a82babc937bc1e`.
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Crit02/` (shared clones + fixtures). Write scope: this file + `T54W2Crit02-receipts/`.
- No tooling install. No lane production edits. No mutating git outside `$S/fixture` / `$S/clone`.

## Verdict up front

At C1 the `--contract` run path **now reports the class** (exit 2, one `ENVDIFF_SETUP: could-not-evaluate:` line naming the TMPDIR value, no traceback, no receipt, not `unavailable`). C0 still tracebacks with exit 1 on the same fixture. The `scratch_root` cell wording is **true for `--contract`** on all three arms at C1.

The measured-scope attack still lands on the **instrument**, not the tree: `c2/measure.py` never invokes `--contract` (`0` occurrences; TOOLS argv is `--selftest` for env-diff). C2 can PASS while a future `--contract` regression is invisible. Contract `cannot_see` already names that blind spot. This does **not** flip `C2_R54_PASS` at C1 (behavioural arms hold; live `--contract` matches the cell).

## Axes

| Axis | Question |
|---|---|
| discernment | Does C2's counter discern the real allocating path (`--contract` → `execute` → `strict_scratch_root`), or only the self-test catch? |
| calibration | Is "one scratch-root exit class across the seven tools" calibrated to production modes, or saturated by 7/7 `--selftest`? |

## Counterexample (measured scope)

`c2/measure.py` TOOLS (frozen counter):

```
('env-diff', 'tools/env-diff.py', '--selftest', 'env-diff-selftest'),
```

`--contract` count in that file: **0**. Contract `claims.C2.cannot_see`:

> whether a tool's self-test exercises the branch that allocates scratch on its real path, and whether a registry cell describes the tool as it now behaves beyond the three named arms

The real allocating call is `execute` L80 (`TemporaryDirectory(..., dir=strict_scratch_root())`), reached from both `--selftest` and `--contract` via `probe` ← `surface_result`. C1 added a `ScratchRootUnusable` catch on the `--contract` try (diff `+3` lines at L263-265); C2 still never runs that branch.

## Evidence — command + output per assertion

All runs used a `git clone --shared` of the lane under `$S/clone/…`, `git rev-parse --show-toplevel` asserted to that clone, and a minimal one-surface contract under `$S/fixture/` (`interp=bash`, local `tinyrepo`). Receipts: `T54W2Crit02-receipts/`.

### A — `--selftest` unusable TMPDIR at C1 (what C2 measures)

```
TMPDIR=$UNUSABLE python3 $CLONE_C1/tools/env-diff.py --selftest
rc=2
ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '.../never-created-tmpdir-r54-crit02' (could-not-evaluate)
has_traceback=0 has_could_not_evaluate=1 names_value=1
```

Receipt: `A-selftest-unusable.txt`.

### B — `--contract` unusable TMPDIR at C1 (the gap under attack)

```
TMPDIR=$UNUSABLE python3 $CLONE_C1/tools/env-diff.py \
  --contract $FIX/contract.json --out $FIX/out-unusable.json \
  --fleet-root $FIX/fleet --jobs 1
rc=2
ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '.../never-created-tmpdir-r54-crit02' (could-not-evaluate)
has_traceback=0 has_could_not_evaluate=1 names_value=1 has_unavailable=0 out_exists=no
```

**Not** classified as `unavailable`. Process exits 2 before writing a receipt. `ScratchRootUnusable` is not a subclass of `(OSError, ValueError, TimeoutExpired)`, so `surface_result`'s unavailable catch cannot swallow it (`H-cell-and-catch-order.txt`).

Receipt: `B-contract-unusable.txt`.

### C / D / E — other two cell arms on `--contract` at C1

| Arm | rc | Notes |
|---|---|---|
| usable TMPDIR | 0 | `ENVDIFF: classified=1/1`; control that the path works (`C-contract-usable.txt`) |
| `TMPDIR=""` | 0 | empty ⇒ unset; classified 1/1 (`D-contract-empty.txt`) |
| usable + `strace -f -e mkdir,mkdirat` | 0 | **0** `mkdir("/tmp…")`; mkdirs only under the usable root (`E-contract-strace.txt`, `E-mkdir-under-tmp.txt` empty) |

### G — same `--contract` unusable probe at C0 (pre-fix)

```
rc=1 has_traceback=1
ScratchRootUnusable: … TMPDIR is not a usable directory: '.../never-created-tmpdir-r54-crit02' (could-not-evaluate)
```

Uncaught through `ThreadPoolExecutor` → `surface_result` → `probe` → `execute` → `strict_scratch_root`. Receipt: `G-c0-contract-unusable.txt`. C1 diff: `02-c0-to-c1-env-diff.diff` (adds the `--contract` `except ScratchRootUnusable` only).

### F — counter scope (instrument)

```
--contract occurrences in c2/measure.py: 0
--selftest occurrences: 6
TOOLS env-diff argv: --selftest
```

Receipt: `F-c2-scope.txt`.

### H — registry cell vs `--contract` mode

Cell on row `env-diff-selftest` (argv is `--selftest` only):

> TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback); TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp (round 54, corpus/knowledge/scratch-root-contract.md)

Against assertions B/D/E: **wording is true for `--contract` at C1**. The row still only names the self-test entry point; the cell prose is not mode-scoped, and at C1 that prose happens to hold for the production mode too.

## Impacted axes

- **discernment**: C2's behavioural arms cannot discern a `--contract` regression; they only watch `--selftest`. C1 closed the live gap the wave-1 finding named, but the counter still cannot see it.
- **calibration**: "7/7 self-tests" is calibrated to the self-test catch, not to "every mode that allocates through `strict_scratch_root()`". Live C1 `--contract` matches the cell; the PASS line would still read the same if that catch were deleted tomorrow.

## Smallest safe correction (critic only — no edits)

Extend C2's unusable/empty/usable arms with one additional env-diff invocation: `--contract` against a pinned one-surface fixture (or the frozen round-21 contract under a scratch fleet), scored with the same exit/naming/traceback/mkdir predicates. Alternatively, narrow the claim/surface text to "seven self-test entry points" so measured scope matches the predicate. Prefer the first if the Standing-rules / note claim remains universal over every `strict_scratch_root()` caller.

## Tooling

No installs or upgrades (python3 + git + strace + bwrap sufficed).

## Bounds

- Lane mutations: none; probes only in `$S/clone/{tameshi-c0,tameshi-c1}` and `$S/fixture/`.
- Fleet-root writes: none outside `.ufo/waves/round-54/w2/T54W2Crit02.md` and `T54W2Crit02-receipts/`.
- Scratch root: `/fast/scratch/hyaku/tameshi-r54/T54W2Crit02` (seat-owned).
