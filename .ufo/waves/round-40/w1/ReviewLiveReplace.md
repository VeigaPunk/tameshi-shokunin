# ReviewLiveReplace — write-site vs expected-unflagged at bash-witness-study.py:778

## Finding

**Confirmed.** `tools/bash-witness-study.py:778` is

```
778:    os.replace(tmp, path)
```

inside `write_json(path: Path, payload: dict)` (line 775). The `os.replace`
destination is the bare variable `path` — there is no quoted string literal on
the line — so it is a **write-site hit**, not an expected-unflagged hit.

## Evidence

- `grep 'os\.replace\s*\(' tools/bash-witness-study.py` → line 778 is the only
  `os.replace` in the file; `write_json` is called with per-call destinations at
  lines 840, 915, 945, 998, 1611, 1619, 1647, 1669, 1683, 1694 (manifest /
  declaration / summary JSON artifacts, tmp-file-then-atomic-replace).
- `git show HEAD:tools/bash-witness-study.py` at `5641ed84c8dc` prints the same
  `os.replace(tmp, path)` at line 778; identical at base rev
  `304e3355705640af2879c772fc9a5c2902c61763` (the line pre-exists; only the v2
  tool is new — `tools/write-path-census-v2.py` does not exist at base).
- Regex check (patterns copied verbatim from the committed tools):
  - v2 `WRITE_RE` (`os\.replace\s*\(` arm, `tools/write-path-census-v2.py:20`)
    **hits** line 778.
  - v1 `WRITE_RE` (open/write_text/write_bytes only) **misses** it.
  - v2 `EXPECTED_RE` (requires a quoted literal matching
    `\.expected|expected\.txt|expected\.json|golden|snapshot`,
    `write-path-census-v2.py:23-25`) **misses** line 778 — `path` is not a
    literal.
  - Contrast: planted fixture `replace_unflagged` = `os.replace(tmp,
    'case.expected')` (`.ufo/evidence/round-40/census/fixtures.json`) hits
    `EXPECTED_RE` → `unflagged=1`. Literal vs variable destination is exactly
    what separates the two classes.
- Counter plumbing (`.ufo/evidence/round-40/census/measure.py:196-204`):
  `live_replace_v2` counts any witness-study line containing `os.replace` that
  `mod.WRITE_RE` hits — keyed on `WRITE_RE` only, never `EXPECTED_RE`. Re-running
  that loop over the file yields `live_replace_v2=1, live_replace_v1=0`,
  contributed solely by line 778. `live_ok` (measure.py:221) requires exactly
  this: `live_replace_v2 >= 1 and live_replace_v1 == 0`.
- Whole-file grep for `expected\.json|\.expected\b|golden|snapshot` and
  `os\.rename` in bash-witness-study.py: **no matches** — no other line can
  inflate either class.
- `git show HEAD:tools/write-path-census-v2.py | sha256sum` =
  `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b` — matches
  the frozen C1 pin.

## Verdict

The C1 clause "bash-witness-study.py has at least one os.replace line that v2's
write pattern hits and v1's misses" is honestly served by line 778 alone, and
the variable destination keeps it disjoint from the expected-literal class the
planted `replace_unflagged` fixture exercises. No falsification found; could not
attack the frozen predicate on this point. Lane checkout and shokuknow
untouched; no counters run in default mode.
