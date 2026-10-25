# ReviewGate14 — C2 census attack (tameshi round 39, gate attack)

Axes: `depth` (C2 write-path census fidelity). Judged on depth; leaf, no dispatch.
Nothing in the lane was edited; all probing ran on REV bytes plus the live,
pin-verified census tool. `git show`/`diff` confirmed `tools/repeat-control.py`
in the live checkout is byte-identical to base rev
`50aadd1bbd94e43cd3fcfb81459414394db2dc35`, so every line citation is valid at
REV and live.

## Finding (primary) — frozen WRITE_RE misses the tool's only durable-write primitive

**Missed write:** `tools/repeat-control.py:183`

```python
    with open(path, "xb") as handle:
```

`WRITE_RE` (`tools/write-path-census.py:39-42`) enumerates modes
`w|a|w+|a+|wb|ab` only. Exclusive-creation `"xb"` (and the whole `x`/`xb`/`x+`/`xt`,
`wb+`/`ab+` families) are absent, so the regex does not match this line.

`write_new` is not peripheral — it is the sole file-creating primitive of the
gate. Every durable write of `repeat-control.py` flows through it:

- `:299-301` run-<k>.{stdout,stderr,exit} evidence (the gate's entire output)
- `:321` command.txt · `:338-341` finding.txt
- `:577` snapshot observations · `:586-589` `expected.json` manifest
- `:687, :689, :692, :803` selftest fixtures and tamper arms

**Observed classification** (census run on the 21 gates reconstructed from REV
bytes, mirroring `measure.py`):

```
GATE repeat-control.py write_sites=3 unflagged=0 sha256=296fe566…1b8cbc25
```

The 3 counted sites are `:792` (`"wb"` tamper byte), `:811` (`"wb"` duplicate
key), `:906` (`"w"` to `os.devnull`). The file performs writes on ≥13 lines;
the frozen pattern sees 3. Undercount: 10 of 13, including the expected-file
manifest write itself.

**Minimal repro** (classifier loaded from the pinned bytes):

```python
classify_text('    with open(path, "xb") as handle:\n        handle.write(data)\n') == (0, 0)
classify_text('    with open(path, "wb") as handle:\n        handle.write(data)\n') == (1, 0)
```

**Named-limit analysis — neither declared limit covers it.** The docstring
(`tools/write-path-census.py:6-8`) names exactly two limits: shell redirects,
and writes whose path is not on the same line as the call. Line 183 is a Python
`open()` call (not a shell redirect) and its path argument sits on the same
line. The generic "not a full lexer" hedge is not a named limit, and this miss
is inside the construct the pattern does claim to cover — same-line Python
`open(` with a quoted mode literal — the enumeration just omits a mode family.

## Secondary (same coverage class, corroboration only)

- `shutil.copytree(...)` at `tools/repeat-control.py:788, 797, 802, 807, 818, 832`
  materializes whole evidence trees (run-N.*, expected.json) with no `open(`,
  `.write_text(`, or `.write_bytes(` on the line — same-line paths, non-shell,
  missed.
- `EXPECTED_RE` (`tools/write-path-census.py:43-45`) matches
  `\.expected\b|expected\.txt|golden|snapshot`, but the manifest written at
  `:586-589` is `"expected.json"` — the dot is after "expected", so it matches
  none of the alternatives; the `snapshot` carrier (`repeat-control-snapshot-v1`,
  `:580`) is not on the write line. Even with the mode counted, the manifest
  write would not classify as an expected-file write.

## Predicate impact (stated honestly, predicate not rewritten)

No C2 conjunct flips: the pinned tool classifies 21/21 gates and exits 0
(observed `WRITE_CENSUS: gates=21/21 live_write_sites=99 live_unflagged=0
missing=0`), the selftest is green (`planted_unflagged=1 planted_flagged=0
planted_scratch=0 fixture_wrote=1`), and `live_unflagged` is explicitly
"reported, not a pre-declared PASS conjunct" (contract C2 `kill_rule`). The
misclassification is silent: all conjuncts pass while the reported per-gate
`write_sites` undercounts `repeat-control.py` by 10 of 13 lines. This is a
depth finding on the census classification, not a C2 kill.

## Evidence trail

- Census tool bytes probed = live `tools/write-path-census.py`; sha256
  computed `bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62`
  = contract C2 pin (match verified in-harness).
- `diff <(git show 50aadd1b…:tools/repeat-control.py) tools/repeat-control.py`
  → identical, so live line numbers are REV line numbers.
- `FLAG_RE` has zero hits in `repeat-control.py`, so the gate is unflagged;
  the miss is purely in `WRITE_RE`'s mode alternation.
- Scratch: `/tmp/tameshi-r39-ReviewGate14/` (REV gate reconstruction + pinned
  classifier copy). No installs performed.
