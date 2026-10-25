# CriticUniversal — round 40 w1 (universal-classification attack)

Axes probed: (1) coverage completeness of `WRITE_RE`, (2) line-locality of
`EXPECTED_RE`, (3) whether any surviving sentence still claims universal write
classification.

## Verdict

**Any sentence asserting "every write is classified" is falsified.** The pinned
v2 census (`tools/write-path-census-v2.py`, sha
`40228532…78b` = contract pin) leaves live writes to `expected.json` entirely
unseen inside the v1 census universe (`tools/write-path-census.py:22-44` GATES
includes `repeat-control.py` at line 36). The claim survives only if it stays
bounded to the two planted classes plus the two named live sites — which the
entry `corpus/knowledge/r40-write-form-misses.md` does explicitly at its
"What is not claimed" section ("They are not a claim that every write in the
tree is classified"), so no *authored* sentence needed repair. The attack finds
the claim would be false the moment anyone asserts it.

## Finding 1 — write to `expected.json` invisible to `WRITE_RE` (counterexample)

`tools/repeat-control.py:820-823` materializes an `expected.json` via a write
form the census cannot match:

```python
os.symlink(
    os.path.join(snap_stable, "expected.json"),
    os.path.join(tamper_manifest_symlink, "expected.json"),
)
```

`os.symlink(`, `os.link(`, `Path.symlink_to`, `Path.rename`, `Path.replace`,
`shutil.copy*/rmtree`, `os.remove/unlink`, `handle.write` are all absent from
`WRITE_RE` (`tools/write-path-census-v2.py:16-22` sees only
`open(…'w|a|w+|a+|wb|ab')`, `.write_text(`, `.write_bytes(`, `os.replace(`,
`os.rename(`).

Empirical (scratch, lane untouched):

```
$ python3  # importlib load of tools/write-path-census-v2.py, then:
classify_text("os.symlink(src, 'snap/expected.json')\n")  ->  (0, 0)
```

A write that produces `expected.json` scores **zero write sites** — not merely
unflagged/miscounted, but unclassified.

## Finding 2 — same-file `expected.json` overwrite under-classified

`tools/repeat-control.py:807-814` overwrites `expected.json` through a variable
path:

```python
duplicate_path = os.path.join(tamper_duplicate_key, "expected.json")
...
with open(duplicate_path, "wb") as handle:
    handle.write(record_text.replace(marker, ...).encode("utf-8"))
```

`classify_text` returns `(1, 0)` for that snippet: line 811 matches `WRITE_RE`
as a write site, but `EXPECTED_RE` requires the literal `'…expected…'` string on
the *same line* (`write-path-census-v2.py:40`), so the expected-target write is
never flagged as such. The file-wide verdict `unflagged=0` for
`repeat-control.py` is produced despite a real unflagged `expected.json`
overwrite — the count is silent, not exhaustive.

## Finding 3 — even the named live-site files contain unclassified writes

Inside the two files the claim does name:

- `tools/registry-replay.py:161` and `:230` — `Path.symlink_to(...)` creates
  fleet aliases; `WRITE_RE` misses both (v2 counts 5 sites; broader ground-truth
  regex finds the same 5 plus these).
- `tools/bash-witness-study.py:1638` `(cev / MANIFEST_NAME).unlink()`,
  `:1705`/`:1707` `shutil.rmtree(...)` — filesystem mutations invisible to the
  census.

These are scratch-side writes, so they do not change the frozen predicate's
`live_json_v2`/`live_replace_v2` verdicts — but they refute any "every write in
the named sites is classified" reading.

## Impacted axes

- **depth (C1):** the frozen predicate is *not* falsified — it never claims
  universality, only 2 planted classes + 2 named sites, all verified true
  (`after/c1-at-5641ed84.stdout`: `C1_R40_PASS=true`). The defect is scope, not
  the pass bit.
- **calibration:** a "census" whose own GATES member (`repeat-control.py`)
  writes `expected.json` through `os.symlink` and `handle.write` without either
  being seen is a real coverage gap; the v2 docstring
  (`tools/write-path-census-v2.py:2-8`) also dropped v1's non-universal
  disclaimer that `tools/write-path-census.py:9-11` carried.

## Smallest safe correction

No contract edit needed — the claim is already bounded. If any seat writes a
sentence implying universal classification, the correction is one line:
enumerate `os.symlink|os.link|\.symlink_to|\.rename|\.replace|shutil\.|os\.(unlink|remove)|\.write\(` as out-of-scope write forms, mirroring
`tools/write-path-census.py:9-11`'s disclaimer, inside
`write-path-census-v2.py`'s docstring.

## Commands (reproducible, scratch-only)

```
sha256sum tools/write-path-census-v2.py   # 40228532…78b == contract pin
grep -n 'os.symlink' tools/repeat-control.py   # :820  expected.json target
python3 -c "…classify_text(\"os.symlink(src,'snap/expected.json')\")"  # (0,0)
```

Tool installs: none (python3 + coreutils sufficed).
