# ReviewGate03 — Gate attack: census classification of tools/context-capture.py

Scope: falsify the frozen write-site classification of `tools/context-capture.py` under
`tools/write-path-census.py` (contract pin `bc8c660c…edc62`, pattern `WRITE_RE`).
Attack question: find one write the frozen pattern misses, or show the pattern's named
limit covers it.

## Result: no falsifying miss found

`python3 tools/write-path-census.py --census .` reports:
`GATE context-capture.py write_sites=3 unflagged=0` — the only byte-write sites are the
three selftest fixture opens the pattern already counts. `unflagged=0` is correct.

## Evidence

### Writes the pattern catches (write_sites=3, all correct)
- `tools/context-capture.py:1667` `with open(receipt_path, "wb") as handle:` — matches `open(...'wb')`.
- `tools/context-capture.py:1682` `with open(expected_path, "wb") as handle:` — matches `open(...'wb')`.
- `tools/context-capture.py:1685` `with open(expected_path, "w", encoding="utf-8") as handle:` — matches `open(...'w')`.
- `unflagged=0` holds: no `.expected`/`expected.txt`/`golden`/`snapshot` *string literal* on the
  write lines (`expected_path` is a bare name), and the files land under a
  `tempfile.mkdtemp(dir="/tmp")` scratch tree anyway (SCRATCH_RE would exclude them).

### Writes the pattern misses — all covered by the named limit
The named limit (tools/write-path-census.py docstring): *"Shell redirects and writes whose
path is not on the same line as the call are outside the frozen patterns."*

- `tools/context-capture.py:1668` `handle.write(receipt_bytes)`
- `tools/context-capture.py:1683` `handle.write(expected_bytes)`
- `tools/context-capture.py:1686` `json.dump(expected_document, handle, sort_keys=True)`
- `tools/context-capture.py:1687` `handle.write("\n")`

`WRITE_RE` counts only `open()`/`.write_text(`/`.write_bytes(` call lines, so these four
body-line writes are missed as *sites* — but each is the body of a `with open(path,"w"/"wb")`
line that the census already counts as the site, and the path is not on the call line:
squarely inside the named limit. The site count (3) is exactly right.

- `tools/context-capture.py:1624-1625` `tempfile.mkdtemp(prefix=…, dir="/tmp")` — directory
  creation; the path literal is on a different line than the call, inside the named limit.

### Borderline residue (not a byte write; cannot move the verdict)
- `tools/context-capture.py:1634` `os.makedirs(path)` — filesystem mutation `WRITE_RE`
  misses and *not* covered by either named limit (path is on the call line, not a shell
  redirect). But `makedirs` creates directories and writes zero bytes, so it is outside the
  census's byte-write-site notion; even if counted it would only change `write_sites`, which
  is reported, not a PASS conjunct, and could not affect `unflagged`.

### Non-writes (correctly unclassified)
- `tools/context-capture.py:322,362` `open(…, "rb")` — read-only.
- `tools/context-capture.py:1639,1292,1296,2282-2288` `sys.stdout/sys.stderr.write` — streams, no file path.
- `tools/context-capture.py:1778,2206` `shutil.rmtree` — deletion, not a write.
- `tools/context-capture.py:134` `sys.dont_write_bytecode = True` — *suppresses* interpreter `.pyc` writes.
- `tools/context-capture.py:1647` `subprocess.run([sys.executable, "-I", SELF, "--check", …], cwd=<scratch>)` —
  the child performs no file writes (module docstring: "writes nothing; the only writes are
  --selftest fixtures under mkdtemp"), and any effect would be another process's write with
  the path not on the call line.
- No `os.write`/`os.fdopen`/`mmap`/`pickle.dump`/`shutil.copyfile`/`print(file=…)`/
  `os.environ` mutation/`sqlite3`/`shelve`/`logging.FileHandler` anywhere in the file
  (verified by module-attribute enumeration: only `os.stat`, `os.listdir`, `os.path`,
  `os.devnull`, `shutil.rmtree`, `tempfile.mkdtemp`, `os.makedirs`, `subprocess.run`).

## Verdict

The frozen `WRITE_RE` misses handle-body writes (`:1668,:1683,:1686,:1687`) but every one is
covered by the pattern's named same-line limit, and the `open()` lines that bind those paths
are counted — so the classification `write_sites=3 unflagged=0` is complete and correct for
this gate. `tools/context-capture.py:1634 os.makedirs(path)` is the nearest uncovered
miss (a mutation with the path on the call line) but writes no bytes and cannot falsify
`C2_R39` (`live_unflagged` is reported, not a conjunct; `unflagged` stays 0 either way).

## Commands used
- `python3 tools/write-path-census.py --census .` → `WRITE_CENSUS: gates=21/21 … ; GATE context-capture.py write_sites=3 unflagged=0 sha256=c4a1d165…1726`
- regex replay of `WRITE_RE`/`EXPECTED_RE`/`SCRATCH_RE`/`FLAG_RE` over the file (same 3 hits).
- write-primitive sweeps over all 2309 lines (open/write/makedirs/mkdtemp/rename/os.*/json.dump/print/environ).
