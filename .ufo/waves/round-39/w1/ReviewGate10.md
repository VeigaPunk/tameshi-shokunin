# ReviewGate10 — census attack on tools/receipt-measure.py

Seat: ReviewGate10 · Milestone: Gate attack · Judged on: depth
Target: frozen `WRITE_RE` in `tools/write-path-census.py` (pinned sha256 `bc8c660c…7edc62` per
`.ufo/evidence/round-39/contract.json` claim C2) applied to `tools/receipt-measure.py`.

## Verdict

The pattern's named limits cover every write it misses in this file.
No uncovered miss found. Classification stands at `write_sites=1 unflagged=0`.

## Frozen pattern under attack (tools/write-path-census.py:46-50)

```python
WRITE_RE = re.compile(
    r"""open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]"""
    r"""|\.write_text\s*\("""
    r"""|\.write_bytes\s*\("""
)
```

Named limits (docstring, tools/write-path-census.py:10-12):
"This is not a full lexer and not a claim that every write in every language is seen.
Shell redirects and writes whose path is not on the same line as the call are outside
the frozen patterns."

## Evidence — classifier replayed on the live file

Probe `/tmp/tameshi-r39-ReviewGate10/probe.py` copies the frozen `WRITE_RE`, `EXPECTED_RE`,
`SCRATCH_RE`, `FLAG_RE` verbatim and replays `classify_text` line-by-line over
`tools/receipt-measure.py` (read-only; live lane untouched). Output:

```
file_global_flagged=False
HIT  171 expected=False scratch=False | destination.write_bytes(contents)
classify_text -> write_sites=1 unflagged=0
```

## Line-by-line accounting

Counted (1):
- `tools/receipt-measure.py:171` — `destination.write_bytes(contents)` → `write_sites=1`.
  Correctly *not* unflagged: `destination` is a `Path` variable (no quoted literal on the
  line), so `EXPECTED_RE` cannot fire — the named limit "writes whose path is not on the
  same line as the call are outside the frozen patterns." Semantically also correct: the
  bytes are fixture `contract.json`/`receipts.json`/`dispatch.json` bodies, not
  `.expected`/`golden`/`snapshot` files, so `unflagged=0` is the right answer twice over.

Missed by `WRITE_RE`, each covered by a named limit:
- `tools/receipt-measure.py:167` — `repo.mkdir(parents=True, exist_ok=True)`
- `tools/receipt-measure.py:170` — `destination.parent.mkdir(parents=True, exist_ok=True)`
  Directory creation, not a content write; the docstring disclaims full coverage
  ("not a claim that every write … is seen").
- `tools/receipt-measure.py:173` — `["git", "init", "--quiet", …]` via `checked_process`
- `tools/receipt-measure.py:176` — `["git", "-C", str(repo), "add", "--all"]`
- `tools/receipt-measure.py:186` — `"commit"` in the `git -C` subprocess block
  (lines 177-195). Subprocess writers — real writes into the fixture repo's object store
  and index — but they are command invocations in another language, inside the
  "not every write in every language" limit.
- `tools/receipt-measure.py:308` — `print("usage: …", file=sys.stderr)`. Sharpest candidate:
  a real Python write call on a single line with the stream named on the line, invisible
  to `WRITE_RE` because `print(` is outside the pattern family (open/write_text/write_bytes).
  Still covered: the docstring explicitly denies claiming every write is seen.

## Residual risk

The umbrella limit "not a claim that every write … is seen" is broad enough to swallow any
miss, including line 308. That makes the F4 axis hard to falsify from a single file — a
known property of the frozen contract, not a defect I can pin against it. If the seat ever
tightens the limit, `print(file=…)` at line 308 is the first test case: single-language,
single-line, stream named on the line, still invisible to the regex.

## Tooling

No installs needed or performed — Python stdlib only; pacman transactions paused per
RULES. Live lane checkout, `.ufo/state`, and the frozen counter were not modified;
probe ran against `/tmp/tameshi-r39-ReviewGate10/`.
