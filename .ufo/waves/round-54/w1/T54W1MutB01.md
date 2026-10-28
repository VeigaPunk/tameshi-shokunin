# T54W1MutB01 — boundary probe: empty TMPDIR in the stdlib

Axes: operability of the scratch-root boundary (empty / unset / unusable
`TMPDIR` vs `tempfile.gettempdir()` vs `strict_scratch_root()`).

Seat item: probe `tempfile.gettempdir()` under empty, nonexistent, and unset
`TMPDIR`; report whether the stdlib itself rejects an unusable value (it does
not — the tools do); state the consequence for the note's empty arm.

Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1MutB01/` (removed on exit).
Receipts: `.ufo/waves/round-54/w1/T54W1MutB01-receipts/`.
No lane production files edited. No tools installed.

## Verdict

`tempfile.gettempdir()` **does not reject** any of the three arms: empty,
unusable (nonexistent path), and unset all exit 0 and return `/tmp`. The
lane tools overlay the refusal: `strict_scratch_root()` treats empty as
unset (exit 0, platform default) and names an unusable value with
`could-not-evaluate` (exit 2).

**Consequence for the note's empty arm**
(`corpus/knowledge/scratch-root-contract.md` rows "empty" / "unset"): the
empty arm is sound and necessary. Stdlib's `_candidate_tempdir_list`
skips empty via `if dirname:` (S278), so `TMPDIR=""` and absent `TMPDIR`
are equivalent under `gettempdir()`. The tools mirror that with
`if t:` before the usability check (`tools/env-diff.py:42-48`). Without
that declaration — e.g. testing `t is not None` — `""` would reach
`os.path.isdir("")` (False) and wrongly raise could-not-evaluate. The
empty arm therefore keeps the lane aligned with the resolver it calls;
the *unusable* arm is where the tools deliberately diverge from stdlib's
silent `/tmp` fallthrough.

## Arm 1 — empty `TMPDIR=""`

```
CMD: python3 -c "import tempfile,os; os.environ['TMPDIR']=''; print(tempfile.gettempdir())"
output: /tmp
exit: 0
naming_line: (none — tempfile.gettempdir() does not reject)
```

Receipt: `T54W1MutB01-receipts/three-arm-stdlib.txt`, `stdlib-empty.txt`.

Tool contrast (`env-diff.py --selftest` under `TMPDIR=`):
```
ENVDIFF_SELFTEST: 9/9 pass
exit: 0
naming_line: (none)
```
Receipt: `T54W1MutB01-receipts/env-diff-selftest-empty.txt`.

## Arm 2 — unusable (nonexistent path)

```
CMD: python3 -c "import tempfile,os; os.environ['TMPDIR']='/fast/scratch/hyaku/tameshi-r54/T54W1MutB01/no-such-dir-xyz'; print(tempfile.gettempdir())"
output: /tmp
exit: 0
naming_line: (none — tempfile.gettempdir() does not reject; candidate fails, fallthrough to /tmp)
```

Receipt: `T54W1MutB01-receipts/three-arm-stdlib.txt`, `stdlib-unusable.txt`.

Tool contrast (`env-diff.py --selftest` under the same nonexistent `TMPDIR`):
```
ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/T54W1MutB01/no-such-dir-xyz' (could-not-evaluate)
exit: 2
naming_line: TMPDIR is not a usable directory: '…/no-such-dir-xyz' (could-not-evaluate)
```
Receipt: `T54W1MutB01-receipts/env-diff-selftest-unusable.txt`.

Helper-only probe of `strict_scratch_root()` raised the same naming string
and mapped to exit 2 (`tool-unusable.txt`).

## Arm 3 — unset (`TMPDIR` absent)

```
CMD: env -u TMPDIR python3 -c "import tempfile,os; print(tempfile.gettempdir())"
output: /tmp
        TMPDIR= None
exit: 0
naming_line: (none — tempfile.gettempdir() does not reject)
```

Receipt: `T54W1MutB01-receipts/three-arm-stdlib.txt`, `stdlib-unset.txt`.

Tool contrast (`env -u TMPDIR … env-diff.py --selftest`):
```
ENVDIFF_SELFTEST: 9/9 pass
exit: 0
naming_line: (none)
```
Receipt: `T54W1MutB01-receipts/env-diff-selftest-unset.txt`.

## Stdlib mechanism (checked)

`tempfile._candidate_tempdir_list` (this host's Python):

```
for envname in 'TMPDIR', 'TEMP', 'TMP':
    dirname = _os.getenv(envname)
    if dirname: dirlist.append(dirname)
…
dirlist.extend(['/tmp', '/var/tmp', '/usr/tmp'])
```

- empty → skipped (`if dirname:` false) → `/tmp`
- nonexistent → appended, then `_get_default_tempdir` tries it, fails, continues → `/tmp`
- unset → no env candidate → `/tmp`

So stdlib never emits a could-not-evaluate class; the tools alone own that
refusal on the unusable arm.

## Finding summary

| Arm | stdlib `gettempdir()` | exit | naming | tools (`env-diff --selftest`) |
|---|---|---|---|---|
| empty `""` | `/tmp` | 0 | none | exit 0, no naming line |
| unusable path | `/tmp` (silent fallthrough) | 0 | none | exit 2, names value + could-not-evaluate |
| unset | `/tmp` | 0 | none | exit 0, no naming line |

No defect against the note's empty arm: empty≡unset under both stdlib and
`strict_scratch_root()`. Coverage finding only if someone claimed
`gettempdir()` itself rejects unusable `TMPDIR` — it does not; the tools do.
