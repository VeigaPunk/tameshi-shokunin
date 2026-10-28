# T54W1MutB02 — non-writable TMPDIR boundary (chmod 500)

Seat: mutation-tester boundary probe on C2 scratch-root operability.
Rev under test: `59c38109bf119d0e9d4f878644a82babc937bc1e` (C0).
uid: `1000` (`vgpnk`), non-root.
Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1MutB02` (shared clone + chmod-500 dir; removed after this report).
No tool installs. No lane production edits.

## Setup

```
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W1MutB02
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r54/T54W1MutB02/clone
git -C .../clone checkout --quiet 59c38109bf119d0e9d4f878644a82babc937bc1e
# toplevel asserted = clone path
BAD=/fast/scratch/hyaku/tameshi-r54/T54W1MutB02/nonwritable-tmpdir
mkdir -p "$BAD" && chmod 500 "$BAD"
# mode observed: dr-x------ ; os.access(BAD, W_OK) == False ; isdir True
```

## Arm A — env-diff --selftest under chmod 500 TMPDIR

Command:

```
TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1MutB02/nonwritable-tmpdir \
  python3 /fast/scratch/hyaku/tameshi-r54/T54W1MutB02/clone/tools/env-diff.py --selftest
```

- exit: `2`
- naming line (stderr): `ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/T54W1MutB02/nonwritable-tmpdir' (could-not-evaluate)`
- traceback: none
- receipt: `T54W1MutB02-receipts/env-diff-chmod500.txt`

## Arm B — pin-disposition --selftest under chmod 500 TMPDIR

Command:

```
TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1MutB02/nonwritable-tmpdir \
  python3 /fast/scratch/hyaku/tameshi-r54/T54W1MutB02/clone/tools/pin-disposition.py --selftest
```

- exit: `2`
- naming line (stderr): `pin-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/T54W1MutB02/nonwritable-tmpdir' (could-not-evaluate)`
- traceback: none
- receipt: `T54W1MutB02-receipts/pin-disposition-chmod500.txt`

Then `chmod 755 "$BAD"` (restored before mutation pass and final cleanup).

**Verdict (boundary probe):** both tools match the C2 unusable arm on a present-but-non-writable directory (not only on a nonexistent path). Exit 2, value named, class named, no traceback.

## Mutation probe — is `os.access(t, W_OK)` load-bearing?

Detector (same for pristine / mutated / restored): run `env-diff.py --selftest` with `TMPDIR=$BAD` (chmod 500); pass iff exit 2 AND stderr/stdout contain `could-not-evaluate` AND the TMPDIR path AND no `Traceback (most recent call last)`.

Mutant (isolated clone only): in `tools/env-diff.py` `strict_scratch_root`, replace

```
if not _os.path.isdir(t) or not _os.access(t, _os.W_OK):
```

with

```
if not _os.path.isdir(t):
```

| state | sha256(env-diff.py) | exit | detector_pass |
|---|---|---|---|
| pristine | `ab193692d78d591fa7c9e55ba9c53cbe88376354adf548cd9d5034ce722bfe56` | 2, naming line | 1 |
| mutated | `6a64a2590a9ef2f5df965160a76937c57de3fc6e04fbea43c8bb31871bd70b16` | 1, PermissionError traceback from `mkdtemp` | 0 |
| restored | `ab193692d78d591fa7c9e55ba9c53cbe88376354adf548cd9d5034ce722bfe56` | 2, naming line | 1 |

Mutated failure (verbatim tip): `PermissionError: [Errno 13] Permission denied: '.../nonwritable-tmpdir/tameshi-r21-envdiff.gaje3l4g'` under an uncaught traceback; exit 1. Receipts: `T54W1MutB02-receipts/mutant-{pristine,mutated,restored}.txt`, `mutation-summary.txt`.

**Mutation verdict: killed.** Restored hash equals pristine (`restored_match=yes`).

## Is `os.access(t, W_OK)` the right test, or should allocation be the test?

For this contract, **`os.access(t, W_OK)` is the right preflight**. The claimed invariant is refuse-before-allocate: exit 2, name the TMPDIR value, print `could-not-evaluate`, no traceback. Dropping the W_OK arm lets `isdir` pass on a chmod-500 directory; `tempfile.mkdtemp` then raises `PermissionError`, the self-test path does not map that to ScratchRootUnusable, and the process exits 1 with a traceback — which fails the contract even though allocation "detected" unusability.

Allocation alone can prove the directory is unusable, but only after the helper has already returned a path; without a matching catch that remaps `OSError`/`PermissionError` into the same naming line and exit 2, allocation is too late for the declared exit class. `os.access` has the usual caveats (ACLs, capability bits, TOCTOU), but under the non-root chmod-500 case exercised here it is exactly what keeps the three-arm exit class intact. A belt-and-suspenders design could keep W_OK and also map allocation `OSError` to the same class; allocation-only is not sufficient for the current helpers.

## Finding

No C2 defect on the present-but-non-writable boundary for the two tools probed. The W_OK preflight is load-bearing for the naming/exit-2/no-traceback invariant; confirmed by a killed mutant.
