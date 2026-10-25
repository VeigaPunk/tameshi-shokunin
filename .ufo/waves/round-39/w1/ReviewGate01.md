# ReviewGate01 — C2 census attack on tools/bash-witness-study.py

## Verdict: MISS FOUND — the frozen pattern misses a real write path.

**Missed write: `tools/bash-witness-study.py:778`**

```python
    os.replace(tmp, path)
```

`write_json()` (lines 775-778) writes every committed JSON artifact —
`declaration.json` (line 915), `summary.json` (lines 945, 998, 1619, 1647,
1683, 1694), and `manifest.json` (line 840 via `write_manifest`) — by writing
`path.tmp` and then atomically renaming it onto `path`. The census counts the
`.write_text(` on line 777 but never counts the `os.replace` that actually
commits the destination file. `os.replace`/`os.rename`/`Path.rename` are not
in the frozen `WRITE_RE`, which covers only `open(...'w'|'a'|'w+'|'a+'|'wb'|'ab')`,
`.write_text(`, and `.write_bytes(`.

Neither named limit covers this:
- It is not a shell redirect — it is a Python stdlib call.
- The path is on the same line as the call (`os.replace(tmp, path)`),
  so the "writes whose path is not on the same line" limit does not apply.

This is live behavior, not a selftest fixture: `cmd_declare`, `_cannot_summary`,
`_execute_sweep`, `cmd_rerun`, and `write_manifest` all route through
`write_json`, so every canonical artifact of this gate tool lands via an
uncounted rename.

**Secondary miss (weaker, same class):** directory-creation writes —
`rundir.mkdir(parents=True, exist_ok=False)` at :603, `evidence.mkdir(...)`
at :848, `repo.mkdir()`/:1254, `target.parent.mkdir(parents=True)`/:1256 —
plus `os.environ` mutation and `shutil.which` monkey-patching in the selftest.
`mkdir` creates a filesystem entry the frozen patterns never see; counted as
writes they would also escape. Cited as corroboration, not the finding.

## What IS counted (control)

`WRITE_RE` matches 23 lines in this file — all `.write_text(`/`.write_bytes(`
sites: 551, 563, 618, 619, 777, 868, 869, 877, 1257, 1325, 1521, 1529, 1541,
1545, 1546, 1549, 1559, 1591, 1605, 1609, 1610, 1653, 1667. The only `open(`
call, line 219, is `open(path, "rb")` — a read, correctly unmatched.

## Falsifier command used (scratch only; live lane untouched)

```bash
python3 - <<'EOF'
import re
WRITE_RE = re.compile(
    r"""open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]"""
    r"""|\.write_text\s*\("""
    r"""|\.write_bytes\s*\("""
)
text = open('tools/bash-witness-study.py', encoding='utf-8').read()
assert WRITE_RE.search(text.splitlines()[777]) is None   # line 778 os.replace
EOF
```

Line 778 confirmed un-matched; line 777 (`tmp.write_text(...)`) matched, so the
pattern is live and the miss is specific to the rename.

## Impact on C2

`live_write_sites` for this gate under-counts by at least one same-line
filesystem write. Any `unflagged` consequence is nil here — `tmp`/`path` are
not `.expected`/golden/snapshot names — so the finding is a write-sites
under-count, not an unflagged-write escape. The frozen pattern's
write-site ledger for `bash-witness-study.py` is nonetheless wrong on the
line cited.
