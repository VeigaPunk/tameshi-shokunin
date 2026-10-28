# T54W1MutB03 — scratch-root boundary probe (operability)

Seat: mutation-tester / boundary probe. Lane tools exercised from a `git clone --shared` of `tameshi-shokunin` at C0 `59c38109bf119d0e9d4f878644a82babc937bc1e` under scratch `$HYAKU_SCRATCH/tameshi-r54/T54W1MutB03/clone`. No lane production files edited. Receipts: `.ufo/waves/round-54/w1/T54W1MutB03-receipts/`.

Tools under test (two of the seven `strict_scratch_root()` self-tests): `tools/env-diff.py --selftest`, `tools/registry-check.py --selftest`.

Axes: exit class (2 vs not-2), naming of the TMPDIR value, no traceback, class stability across shape variants of "unusable".

## Arm A — TMPDIR is a regular file (required)

Fixture: `touch` regular empty file `.../fixtures/tmpdir-is-a-file` (`stat`: regular empty file).

### env-diff

```
cd /fast/scratch/hyaku/tameshi-r54/T54W1MutB03/clone
TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1MutB03/fixtures/tmpdir-is-a-file \
  python3 tools/env-diff.py --selftest
```

- exit: **2**
- naming line: `ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/T54W1MutB03/fixtures/tmpdir-is-a-file' (could-not-evaluate)`
- traceback: none
- receipt: `T54W1MutB03-receipts/file-env-diff.txt`

### registry-check

```
TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1MutB03/fixtures/tmpdir-is-a-file \
  python3 tools/registry-check.py --selftest
```

- exit: **2**
- naming line: `registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/T54W1MutB03/fixtures/tmpdir-is-a-file' (could-not-evaluate)`
- traceback: none
- receipt: `T54W1MutB03-receipts/file-registry-check.txt`

**Verdict:** class stable — both tools exit 2, name the file path, print could-not-evaluate, no traceback. Matches the unusable arm of `corpus/knowledge/scratch-root-contract.md`.

## Arm B — TMPDIR is a symlink to a directory

Fixture: `tmpdir-symlink` → `real-dir` (directory 755). `os.path.isdir` True, `W_OK` True, `islink` True.

### env-diff

```
TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1MutB03/fixtures/tmpdir-symlink \
  python3 tools/env-diff.py --selftest
```

- exit: **0**
- output ends: `ENVDIFF_SELFTEST: 9/9 pass`
- no could-not-evaluate line
- receipt: `T54W1MutB03-receipts/symlink-env-diff.txt`

### registry-check

```
TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1MutB03/fixtures/tmpdir-symlink \
  python3 tools/registry-check.py --selftest
```

- exit: **1** (selftest body: `SELFTEST: FAIL (2 of 51 cases: rev-non-hermetic-argv, rev-external-declared)` — unrelated to scratch-root; cases ran after scratch allocation)
- no could-not-evaluate / no exit-2 naming line
- receipt: `T54W1MutB03-receipts/symlink-registry-check.txt`

**Verdict:** symlink-to-directory is treated as a **usable** scratch root (class not-2). Exit-class for scratch-root remains stable: helper follows the link via `isdir`/`access` and does not refuse. (registry-check rc=1 is a separate hermetic-case failure on this shared clone, not a scratch-root class break.)

## Arm C — directory on a read-only mount (available)

Host bind-remount in a user+mount namespace was refused (`unshare -Urm` → `mount: permission denied`). An existing user-visible RO fuse mount was used instead:

`findmnt -T /tmp/.mount_KimiColz3RmH` → `fuse.KimiCode-linux-x86_64.AppImage` options `ro,nosuid,nodev,...`. `isdir` True, `W_OK` False.

### env-diff

```
TMPDIR=/tmp/.mount_KimiColz3RmH python3 tools/env-diff.py --selftest
```

- exit: **2**
- naming line: `ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/tmp/.mount_KimiColz3RmH' (could-not-evaluate)`
- traceback: none
- receipt: `T54W1MutB03-receipts/ro-env-diff.txt`

### registry-check

```
TMPDIR=/tmp/.mount_KimiColz3RmH python3 tools/registry-check.py --selftest
```

- exit: **2**
- naming line: `registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/tmp/.mount_KimiColz3RmH' (could-not-evaluate)`
- traceback: none
- receipt: `T54W1MutB03-receipts/ro-registry-check.txt`

**Verdict:** class stable — RO mount directory fails `W_OK`, same exit-2 / naming / no-traceback class as a file TMPDIR.

## Adjacent control — mode 0555 directory on RW mount (not required; class check)

`chmod 555` dir on `/fast` (xfs rw). Same exit **2** + naming for both tools (`T54W1MutB03-receipts/mode555-*.txt`). Confirms the helper key is `isdir ∧ W_OK`, not mount flags per se.

Usable plain dir positive control: `env-diff` exit **0** (`usable-env-diff.txt`).

## Class-stability summary

| Arm | shape | env-diff rc | registry-check rc | names TMPDIR value | could-not-evaluate | traceback | scratch-root class |
|---|---|---|---|---|---|---|---|
| A | regular file | 2 | 2 | yes | yes | no | unusable (stable) |
| B | symlink → dir | 0 | 1† | n/a | no | no | usable (stable) |
| C | dir on RO fuse mount | 2 | 2 | yes | yes | no | unusable (stable) |
| ctrl | mode 555 dir | 2 | 2 | yes | yes | no | unusable (stable) |

† registry-check rc=1 from unrelated selftest cases after scratch root accepted.

**Finding:** Across file, RO-mount, and non-writable-dir shapes, both tools keep one unusable exit class (2, value named, could-not-evaluate, no traceback). A symlink to a writable directory is accepted as usable. No production defect to file against the declared contract for these arms; the probe did not kill the invariant.

## Tooling / scratch

- No pacman / uv / binary installs this seat.
- Scratch tree `$HYAKU_SCRATCH/tameshi-r54/T54W1MutB03/` removed after report write (trap cleanup).
