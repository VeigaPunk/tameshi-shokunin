# ExecFixtureBytes — C2 F4 fixture: update_expected(false) then (true), byte-level

Seat: executor (leaf). Axis: depth. Milestone: Actual write (in /tmp only).
Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (HEAD `233077f`, lane_base_rev `50aadd1bbd94e43cd3fcfb81459414394db2dc35`).
Contract read, not edited: `.ufo/evidence/round-39/contract.json`.

## Command

```bash
D=/tmp/tameshi-r39-ExecFixtureBytes && mkdir -p "$D"
cp <LANE>/tools/write-path-census.py "$D/write-path-census.py" && cd "$D" && python3 drive.py
```

Driver: `/tmp/tameshi-r39-ExecFixtureBytes/drive.py`; full log: `/tmp/tameshi-r39-ExecFixtureBytes/drive.out`.
The module exercised is a byte-identical copy of the pinned tool:
`sha256(bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62)` = contract `claims.C2.tool_sha256`.
No file under the lane checkout was written (see "No live-lane write" below).

## Byte transcript — real tool

Fixture file `/tmp/tameshi-r39-ExecFixtureBytes/case.expected`, seeded `b'old\n'`.

```
pre           bytes=b'old\n' hex=6f6c640a size=4 sha256=01d09d19…39dee  ino=94047954 mtime_ns=1792887319726897662
CALL update_expected(path, "new\n", False) -> False
after-false   bytes=b'old\n' hex=6f6c640a size=4 sha256=01d09d19…39dee  ino=94047954 mtime_ns=1792887319726897662
CALL update_expected(path, "new\n", True) -> True
after-true    bytes=b'new\n' hex=6e65770a size=4 sha256=7aa7a535…77d4c  ino=94047954 mtime_ns=1792887319726991662
```

- update=False: return `False`, bytes identical, **and inode and mtime_ns identical** — the gate returns at
  `tools/write-path-census.py:79-80` before `open()`, so the file is not even opened for write/truncate.
- update=True: return `True`, bytes `6e65770a`, size stays 4, same inode (truncate-in-place).

These are exactly the two observations asserted by the committed selftest,
`tools/write-path-census.py:93-106` (`old\n` seed at :95-96, false call :97/`:99`/`:100`, true call at :102/`:104`/`:105`).
Running the selftest on the /tmp copy: `rc=0`, and
`WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1`.

## Mutant probe (supplementary, /tmp copy only)

FLAG_GATE early-return removed (`if not update:` → `if False:`), sha256 `6b24439e6549759451a9c0efa7fb937707a5f96f32d56beb736b991ff913b60d`:

```
CALL update_expected(path, "new\n", False) -> True
after-false   bytes=b'new\n' hex=6e65770a sha256=7aa7a535…77d4c mtime_ns changed
```

`wrote=True` and `unchanged=False` at :99-101 ⇒ `failed` non-empty ⇒ `return 0 if not failed` (:114) is nonzero.
The fixture does kill the removed-gate mutant; this is the byte-level basis of `mutant_killed=1`.

## Findings

**F1 (real, depth). The fixture cannot distinguish the gate *form*.**
`tools/write-path-census.py:79` gates on truthiness (`if not update:`). A mutant that replaces it with
`if update is False:` (sha256 `b378c32df1616bad3f9b224f695b6a214b6034291f3cb4eb07cd031051184e38`) is **not killed**:

```
real tool                eval_false=False bytes_false='old\n' eval_true=True bytes_true='new\n' FIXTURE_PASSES=True
mutant: update is False  eval_false=False bytes_false='old\n' eval_true=True bytes_true='new\n' FIXTURE_PASSES=True
```

The two calls use Python bool literals (:97, :102), so identity and truthiness are indistinguishable.
They differ only for non-bool falsy input, e.g. `0`: pinned tool returns early, identity mutant **writes**.
Pinned tool's own behaviour on a non-bool truthy input:

```
real tool: update_expected(path,"new\n","false") -> True bytes='new\n'
```

That is, a string `"false"` writes. Live exposure is zero today: `grep -rn update_expected --include=*.py` over the lane
returns only `tools/write-path-census.py:77,97,102`, the two callers pass literals, and `main()` (:151-160) exposes
no `--update` flag. Recorded as a coverage limit of `fixture_wrote`, not as a reason to edit the pinned sha
(the contract freezes the tool after the pin). Concrete hardening, if the pin is ever reopened: pass `0` as a third
call and assert the seed survives, which kills the identity form.

**F2 (evidence quality). `noflag_unchanged` is not an independent witness.**
`tools/write-path-census.py:110` prints `noflag_unchanged=%d % (…, 1 if fixture_wrote else 0)`. It is a second copy of
the `fixture_wrote` bit, not the `unchanged` observation computed at :99; the printed line therefore looks like two
independent witnesses and is one. Predicate `C2_R39_PASS` only requires `fixture_wrote=1`, so this does not break the
claim — but `noflag_unchanged` must not be cited as separate proof that the no-flag path left the file alone. The
genuine per-call byte evidence for that is the transcript above.

**F3 (structural). `fixture_wrote` is derived from failure-message text**, :107
(`any('update flag' in item or 'no-flag' in item for item in failed)`). It is string-coupled to :101/:106: renaming
either message silently forces `fixture_wrote=0`, and any *other* failing assertion (the three planted-classification
checks, :90-92) leaves `fixture_wrote=1` while `rc` is nonzero. Consistent with the predicate as written
(`fixture_wrote` is one conjunct of several) but the printed bit is not a standalone "the fixture wrote" fact — the
`rc` and the per-call bytes are.

## No live-lane write

- `sha256sum tools/write-path-census.py` before and after the seat: both `bc8c660c…27edc62`.
- `git status --porcelain tools .ufo/evidence` → empty.
- `git cat-file -e 50aadd1…:tools/write-path-census.py` → `fatal: path … exists on disk, but not in '50aadd1…'`,
  so the tool is genuinely absent at the base rev and C2's `tool_absent=1` at base is not contradicted by this seat.
- Pre-existing `tools/__pycache__/write-path-census.cpython-314.pyc` (mtime 2026-10-24 21:15:25.81, gitignored via
  `.gitignore:4`) was **not** created here: every import in this seat targeted `/tmp/tameshi-r39-ExecFixtureBytes`
  copies (module paths visible in `drive.out`). Left untouched.
- No package installs or updates. No LSP interface is exposed to this seat; symbol callers were established by
  `grep -rn` above, and the empty-LSP caveat is recorded rather than read as absence.
