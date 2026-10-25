# ReviewGate12 — C2 census attack on tools/registry-check.py

Scope: does the pinned `tools/write-path-census.py` (sha256 bc8c660c…7edc62, matches
contract pin) correctly census the write paths of `tools/registry-check.py`?

## Finding 1 (primary): missed write site — `tools/registry-check.py:1099`

```python
with open(os.path.join(fixture_repo, "seed.txt"), "w",
          encoding="utf-8") as fh:
    fh.write("seed\n")
```

This is a genuine `open(path, "w")` write (selftest seeds `commit-fixture/seed.txt`,
then a row `git commit`s it). `WRITE_RE` arm 1 is
`open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]`: `[^)]*` cannot cross the `)` of
`os.path.join(fixture_repo, "seed.txt")`, so the match dies before the `"w"` literal.
Any `open(...)` whose path expression contains a `)` before the mode string is
invisible to the frozen pattern — a regex-mechanics hole, not a named limit.

Neither named limit covers it:
- not a shell redirect — it is a Python `open(..., "w")`;
- the path expression and the `"w"` mode are on the **same line** (line 1099) —
  the "path not on the same line" limit does not apply.

Reproduction (scratch copy, live file untouched):

```
cp tools/registry-check.py /tmp/tameshi-r39-ReviewGate12/
python3 -c '...'  # frozen WRITE_RE/EXPECTED_RE/SCRATCH_RE/FLAG_RE applied per-line
# counted sites: lines 949, 981, 1035, 1137, 1171, 1174, 1235, 1238  (8 total)
# line 1099 contains open( + quoted "w" mode and is not counted.
```

Running the pinned tool's own `classify_text` on the file returns
`write_sites=8 unflagged=0`; truth is ≥9 write sites. `live_write_sites` in
`WRITE_CENSUS` is therefore undercounted for this gate.

## Finding 2 (secondary, arguably absorbed by the docstring hedge): `tools/registry-check.py:1046`

```python
shutil.copy(reg_rev, os.path.join(git_lane, "tools", "registry.json"))
```

A same-line file-creating write the frozen pattern list does not name at all
(`open`/`.write_text`/`.write_bytes` only). Not a shell redirect; path on the same
line. The docstring hedge "not a claim that every write … is seen" is the only
cover — it names no API limit, so the miss stands unless that blanket clause is
read as covering arbitrary write APIs.

## Finding 3 (weakest): `tools/registry-check.py:1226`

`os.open(os.devnull, os.O_WRONLY)` — a write-mode open outside every named pattern;
target is only `/dev/null`, so low materiality.

## Honest check — what is NOT a miss

- `unflagged=0` for this gate is correct even after fixing Finding 1: `seed.txt`
  is not expected-named (`EXPECTED_RE` does not match), and every counted
  `.expected`-eligible write lives under the mkdtemp `scratch` root, which
  `SCRATCH_RE` suppresses only when the token is on the same line — here it is.
- `FLAG_RE` correctly finds no update flag (`env.update`, `variant.update` do not
  match `--update\b|update_goldens`); the file is genuinely flag-free.
- `sys.stdout.write`/`emit`/`print_human` are stream writes, not file writes —
  correctly uncounted.

## Verdict

The frozen pattern misses the write at `tools/registry-check.py:1099`; neither
named limit covers it. The census's `live_write_sites` (and the per-gate
`write_sites` for registry-check.py) is off by at least 1. `live_unflagged` is
unaffected for this gate.
