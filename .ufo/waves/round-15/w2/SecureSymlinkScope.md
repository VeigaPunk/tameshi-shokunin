# SecureSymlinkScope — wave 2 sentinel report (static only)

Seat: TameshiR15.SecureSymlinkScope (sentinel, leaf). Scope: snapshot path
handling, lstat/symlink containment and outside reads during `--selftest` in
the maintained gate `tools/context-capture.py`.

## Exact sources read

- `tools/context-capture.py` lines 1-375, 458-663, 1016-1353 and 1571-2116 of
  2116. Also every hit from a grep across the file for
  `open(|os.(stat|lstat|path|listdir|walk|readlink|scandir|environ|getcwd|chdir)|realpath|subprocess|Path(|glob|DEFAULT_LANE_ROOT|SELF`.
  Current bytes: sha256 `0ed784e0076b3de5ec5000c3862a771a3e3e2eb83241da347a6cf3f2f2c61edc`. A
  concurrent edit after this read is not covered.
- Lane convention for comparison: `tools/evidence-disposition.py:209-311`
  (`safe_file`, `read_regular`), plus grep hits for lstat and O_NOFOLLOW in
  `tools/pin-disposition.py:81,243-249,358-376`, `tools/repeat-control.py:364,414` and
  `tools/witness-metadata.py:341-385`.
- `.ufo/evidence/round-14/capture-context.py`: grepped only. Its only path
  primitive is `os.path.realpath(__file__)` at line 45.
- `corpus/lessons/round-14-verifier-spotcheck.md`, Routed defects (lines 154-162).
- Filesystem facts from `stat`/`sha256sum`: no gate was executed.
  `.ufo`, `.ufo/evidence`, `.ufo/evidence/round-14` and `tools` are real
  directories. `context-receipt.json` and `context-capture.py` are regular
  files. The receipt sha256 is
  `05cb55b8…899c1a`, which equals `FROZEN_RECEIPT_SHA256` (lines 137-139).

I did not execute the gate, the selftest or any check. I read no credential or
agent.db files. I installed or updated no tools.

## Read inventory (static)

`open()` and `os.stat()` are called at exactly four places:

| line | reader | path origin |
|---|---|---|
| 302 | `tool_sha256()` called from every `make_result` | `SELF = realpath(__file__)` |
| 332/342 | `read_regular` (stat, then open) | receipt and expected paths |
| 1622/1634 | selftest harness, write-only | `mkdtemp` root / case dir |

Frozen mode reads `DEFAULT_LANE_ROOT/.ufo/evidence/round-14/context-receipt.json`
(line 1302). Explicit mode reads the paths the caller passed in `--receipt` and
`--expected` (lines 1311-1313). There are no environment reads, no `listdir`
in check mode and no network access.

## Findings

### F1 — MEDIUM (provenance claim not enforced): frozen read follows symlinks; the claim that frozen mode reads "only the archived receipt" is unenforced

- **Evidence.** `read_regular` (330-349) calls `os.stat(path)`, which follows
  symlinks, then a plain `open(path, "rb")`. There is no lstat, no O_NOFOLLOW,
  no per-component symlink rejection and no realpath containment under
  `DEFAULT_LANE_ROOT`. The docstring (lines 13-14) and USAGE (263-264) still
  claim that "frozen mode reads only the archived receipt named by the built-in
  pin". The result reports the fixed relative label `receipt.path =
  FROZEN_RECEIPT_REL` (1301, 1234), not the path that was actually opened.
- **Counterexample.** Replace any one of these with a symlink to a directory
  outside the lane that holds a byte-identical copy of the receipt:
  `.ufo`, `.ufo/evidence`, `.ufo/evidence/round-14`, or the receipt file
  itself. `--check` then reads the outside file, passes the digest pin
  (1324), recomputes `context_consistent`, exits 0, and prints
  `receipt.path=".ufo/evidence/round-14/context-receipt.json"`, so the
  redirected read leaves no trace in the output.
- **Impact, bounded.** Verdict integrity holds because the sha256 pin binds the
  bytes. What fails is location and provenance: the tool claims a
  lane-contained archived read it does not check. This also diverges from the
  lane's own secure-read convention. `evidence-disposition.py:230-297`
  rejects symlink components, rejects non-regular files with lstat before
  open, opens with O_NOFOLLOW, compares lstat and fstat `(st_dev, st_ino)`,
  and checks that `resolve()` stays inside the lane.
  `pin-disposition.py:81` names the exact risk this exposes: "a symlink cannot
  leak an arbitrary file's digest". Today all four components are real
  directories or regular files (stat above), and git would show a type change.
  The tool itself does not enforce either fact.
- **Smallest remediation.**
  1. In frozen mode, walk the components of `FROZEN_RECEIPT_REL` from
     `DEFAULT_LANE_ROOT` with `os.lstat` and reject `S_ISLNK`. Then open with
     `os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK|os.O_CLOEXEC`, `fstat` the
     descriptor, and require `S_ISREG` and the same inode identity as the
     lstat. This reuses the `evidence-disposition.py` pattern.
  2. Map a rejection to `receipt_unreadable` (exit 2) or to a documented new
     ID, and list that ID in the docstring's stable-ID table.
  3. Alternatively, bound the claim to "reads the bytes reachable at that
     path; the digest pin is the only authority".

### F2 — LOW: stat→open TOCTOU and FIFO/device hang in `read_regular` (both modes)

- **Evidence.** The `S_ISREG` check is done on `os.stat` (332, 339). The
  `open` (342) is a separate path lookup with no `O_NONBLOCK`, and there is no
  `fstat` afterwards. No size bound applies before `handle.read()`.
- **Counterexample.** Something that can write the parent directory swaps the
  receipt path, after the stat and before the open, to a FIFO or to a symlink
  pointing at a FIFO. The open then blocks with no timeout, so check mode
  hangs instead of returning exit 2. If the path is swapped to
  `/dev/zero`, `read()` runs until the process is out of memory, which reaches
  `internal_error` or kills the process.
- **Impact.** A local same-user race causes a denial of service in a gate
  documented as fail-closed. It does not forge a verdict, because the digest
  pin still holds.
- **Remediation.** Use the same descriptor-based read as F1. Classify on the
  `fstat` of the opened descriptor, not on the pre-open stat.

### F3 — LOW: under `TMPDIR` the selftest can write inside the lane, and the leak check turns itself off

- **Evidence.** `mkdtemp` (1581) runs in the parent with the ambient
  environment. `SELFTEST_ENV` (1572-1576) applies only to the child
  processes. The leak check (1701-1703) is
  `... if DEFAULT_LANE_ROOT not in self.root else False`, a raw substring
  test.
- **Counterexample.** Set `TMPDIR=<lane>/.ufo/tmp`. All fixture writes
  (1590, 1622, 1634) land inside the lane tree. `hermetic-no-lane-path` then
  short-circuits to "no leak" and records OK. The substring test can also be
  tripped without the lane being involved: with
  `TMPDIR=/home/vgpnk/Projects/shokunin/tameshi-shokunin-scratch` (a sibling
  directory, not the lane), the guard still disables the leak check.
- **Impact.** Whether the round-15 writes are actually lane-free depends on
  the environment, while the selftest reports PASS regardless. Cleanup in the
  `finally` block limits how long the files persist but does not prevent the
  write.
- **Remediation.**
  1. After `mkdtemp`, fail and clean up if
     `os.path.commonpath([os.path.realpath(root), DEFAULT_LANE_ROOT]) == DEFAULT_LANE_ROOT`.
  2. In the leak scan, remove occurrences of `self.root` from each output
     before searching for `DEFAULT_LANE_ROOT`, instead of disabling the check.

### F4 — LOW (claim wording): "no live lane path is read" is literally false, and the hermetic cases do not test reads

- **Evidence.** Every selftest child runs `sys.executable -I SELF` (1638,
  1686), which loads the lane file `tools/context-capture.py`. Every
  `--check` child reads that file a second time through `tool_sha256()`
  (302, from 1227). The docstring (27-28) still says "No live lane path is
  read or written".
  - `hermetic-no-lane-path` only scans subprocess output for a path string,
    and a digest contains no path.
  - `hermetic-temp-only` (1708-1716) only checks the names of top-level
    entries in the temp root. It does not recurse and does not observe
    anything outside the root.
- **Bounded agreement.** Apart from the tool's own source, I found no read of
  any lane or outside path in the selftest:
  - every `--check` child gets `--receipt` and `--expected` paths inside its
    case directory (1616-1617, 1638-1639);
  - all five usage cases fail in `parse_argv` (2023-2074), before
    `run_check`;
  - no selftest case runs frozen `--check` without receipt arguments;
  - `build_fixture_receipt` has no file I/O (grep shows no
    `open` or `stat` in 1388-1570);
  - with `-I` and no `HOME` in `SELFTEST_ENV`, user site and
    `PYTHON*` variables are excluded.

  The interpreter's stdlib and system site imports are outside reads that come
  from the platform. I did not instrument these reads; this conclusion comes
  from source reading only.
- **Remediation.** Change the docstring to "no lane path other than this
  tool's own source is read". Rename or reword the two hermetic cases so they
  claim only what they observe.

### F5 — LOW (classification, coverage)

- **Classification.** A dangling symlink at the receipt or expected path fails
  `os.stat` with `FileNotFoundError` and is reported as `receipt_missing` or
  `expected_missing`. The entry exists, so lstat-based handling would report
  it as unreadable or rejected.
- **Selftest coverage.** No selftest fixture uses a symlink, a directory or a
  FIFO as the receipt. `receipt_unreadable` and `expected_unreadable` are
  stable IDs with no pinned fixture. Once F1/F2 land, add these cases:
  - a symlinked receipt inside the temp root, with a literal expected ID and
    exit;
  - a directory as the receipt: `receipt_unreadable`, exit 2.

## Not a defect (bounded agreements)

- **Explicit mode.** Following a symlink the caller supplied is within the
  caller's authority. The digest pin is computed over the bytes read and is
  compared before parsing (1323-1333). Output carries the sha256 and
  parse-error positions, not file contents.

  One exception: when an `--expected` file has extra keys, their names are
  echoed (1195). A caller who points `--expected` at an arbitrary JSON file
  would see its top-level key names. That is a caller-chosen path and is
  listed here for completeness only.
- **Fixture writes.** The temp root is created by `mkdtemp` with mode 0700,
  and `case_dir` uses `os.makedirs` on fresh names. Planting symlinks before a
  fixture write would require the same uid. No child process writes in check
  mode: the only writes are at 1622 and 1634, both in the parent harness.
- **Frozen root.** `DEFAULT_LANE_ROOT` comes from `realpath(__file__)` (122-123),
  so invoking the tool through a symlink still reaches the real lane. A copied
  tool tree would read its own receipt, which is still bound by the digest
  pin.
- **Exit codes.** Usage errors exit 64 before any file I/O. The `except
  Exception` in `main` (2106-2112) turns traceback paths into
  `internal_error`, exit 2.

## Verdict

- **Selftest outside reads:** static source supports agreement, except for
  the tool's own source and the wording claim in F4.
- **Snapshot path containment:** I found a concrete counterexample (F1), with
  a TOCTOU and hang variant (F2). The digest pin keeps the verdict honest, but
  the location and provenance claim is unenforced and diverges from the lane's
  established lstat and O_NOFOLLOW pattern.
- **Hermetic leak guard:** it can be disabled by `TMPDIR` (F3).

None of these findings forges a context verdict. L1 owns runtime confirmation.
