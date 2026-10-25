# CriticHardcode — live_json_v2 hardcode finding

## Question
Can a v2 tool that hardcodes the five fixture strings but does not classify
`tools/registry-replay.py` pass `live_json_v2`?

## Finding: YES — `live_json_v2` is passable by a hardcoded tool

`live_json_v2` never invokes `mod.classify_text` on registry-replay.py.
`.ufo/evidence/round-40/census/measure.py:193-199` scans the replay file
line-by-line and applies the tool's module-level regexes to a single
prefiltered line:

```python
for line in replay.decode('utf-8', 'replace').splitlines():
    if '.write_bytes' in line and 'expected.json' in line:
        if mod.EXPECTED_RE.search(line) and mod.WRITE_RE.search(line):
            live_json_v2 += 1
```

Only `tools/registry-replay.py:123` survives the prefilter:

```python
(out / 'expected.json').write_bytes(encode({'schema': 'command-binding-expected-v1',
```

## Evidence (scratch reproduction)

Tool: `/tmp/tameshi-r40-CriticHardcode/hardcoded-v2.py` — `classify_text` is a
literal 5-key lookup of fixtures.json returning `(0,0)` on everything else;
`WRITE_RE`/`EXPECTED_RE` are general regexes copied in shape from the real tool.

Simulation of measure.py:193-199 against `HEAD:tools/registry-replay.py`:

```
prefiltered lines: [123]
live_json_v2 = 1  live_json_v1 = 0
classify_text(registry-replay.py full text) = (0, 0)
```

The hardcoded tool scores `live_json_v2=1` while returning `(0,0)` — refusing
to classify — on the replay file itself.

## Scope of the gap (calibration)

- `live_json_v2` and `live_json_v1` alone do not defend against fixture
  hardcoding. They test regex surfaces, not `classify_text` on live code.
- Companion axis `live_replace_v2` (measure.py:202-209) has the identical
  shape: prefilter `os.replace` lines of `tools/bash-witness-study.py`
  (only line 778, `os.replace(tmp, path)`), then `mod.WRITE_RE` — also a
  regex-only check.
- The real anti-hardcode weight is carried by the contract pin:
  `claims.C1.tool_sha256 = 4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b`
  (matches live blob). `sha_ok` at measure.py:226 gates `ok`; any divergent
  hardcoded blob fails the pin unless it collides with that sha256.
- So the hardcoded variant can pass `live_json_v2` (and `live_ok`) but cannot
  reach `C1_R40_PASS=true` under the frozen contract — unless the pinned sha
  is itself the hardcoding tool's, which would be a settlement-time concern,
  not a counter weakness.

## Impacted axes
- C1 depth capability: predicate coverage gap on `live_json_v2`/`live_ok`
  (regex-only), mitigated by `sha_ok` pin.

## Smallest safe correction
If the intent is for `live_json_v2` to prove classification of
registry-replay.py, evaluate `mod.classify_text` over the replay file (or the
prefiltered line) instead of raw `EXPECTED_RE`/`WRITE_RE` matches — e.g.
require `mod.classify_text(line)[1] >= 1` on a matching line. Otherwise the
current shape is sufficient only because the sha pin does the hard work.
