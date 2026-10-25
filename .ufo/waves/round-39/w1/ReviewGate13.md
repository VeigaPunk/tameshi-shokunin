# ReviewGate13 — C2 census attack on tools/registry-replay.py

## Finding (confirmed, not covered by the named limit)

**`tools/registry-replay.py:123` is an unflagged expected-value write the frozen pattern misses.**

```python
(out / 'expected.json').write_bytes(encode({'schema': 'command-binding-expected-v1',
                                            'bundle_sha256': report['bundle_sha256']}))
```

- `WRITE_RE` counts the site (`.write_bytes(`); `FLAG_RE` finds nothing in the
  file, so the file is unflagged; the write is unconditional inside `publish`.
- The file is literally the gate's expected-value artifact — `expected.json`,
  schema `command-binding-expected-v1` — yet `EXPECTED_RE` does not match
  `'expected.json'`: its alternatives are `.expected`, `expected.txt`,
  `golden`, `snapshot`. `expected\.json` is absent.
- Result: `classify_text` on live bytes returns `write_sites=5 unflagged=0`;
  the census undercounts `live_unflagged` by exactly this write.

## Named-limit check

The tool docstring names two exclusions: shell redirects, and writes whose
path is not on the same line as the call. Neither applies — the literal path
`'expected.json'` is on the same line as `.write_bytes(`, and the line is
already inside the counted set. The miss is in `EXPECTED_RE`'s alternation,
not in the declared limits.

## Reproduced (live checkout bytes, unmodified)

```
sha256(tools/write-path-census.py) = bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62  # matches contract pin
classify_text(registry-replay.py) -> write_sites=5 unflagged=0
EXPECTED_RE.search("'expected.json'") -> False
EXPECTED_RE.search("'case.expected'") -> True
FLAG_RE.search(<file>) -> False
```

Repro command:

```bash
python3 - <<'EOF'
import importlib.util
spec = importlib.util.spec_from_file_location('wpc', 'tools/write-path-census.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
t = open('tools/registry-replay.py', encoding='utf-8').read()
print(m.classify_text(t), bool(m.EXPECTED_RE.search("'expected.json'")))
EOF
```

## Residual risk

`live_unflagged` is reported, not a PASS conjunct, so C2_R39_PASS is
unaffected; the depth axis is. Any sibling gate writing `expected.json` /
`*-expected.*`-style names (without `.expected`, `expected.txt`, `golden`,
`snapshot`) escapes the expected-value classification the same way.
