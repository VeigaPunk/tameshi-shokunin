# ReviewLiveJson — registry-replay.py expected.json write_bytes is a string literal that v1 EXPECTED_RE misses

Verdict: CONFIRMED (no violation). The C1 clause "registry-replay.py has at least one expected.json write_bytes line that v2's expected pattern hits and v1's misses" holds on the frozen content. `expected.json` is referenced as a quoted string literal, not a bare token.

## Evidence

- `tools/registry-replay.py:123` — `(out / 'expected.json').write_bytes(encode({'schema': 'command-binding-expected-v1',` is the only line in the file satisfying the counter's scan filter `'.write_bytes' in line and 'expected.json' in line` (`.ufo/evidence/round-40/census/measure.py:195`). The `expected.json` operand is the single-quoted string literal `'expected.json'` fed to `Path.__truediv__`; the `write_bytes` argument itself is the call `encode({...})`, not a literal — precision noted, immaterial to the clause.
- v1 misses: embedded `V1_EXPECTED_RE` at `.ufo/evidence/round-40/census/measure.py:38-40` is `['"][^'"]*(?:\.expected\b|expected\.txt|golden|snapshot)[^'"]*['"]` — the alternation lacks `expected\.json`. `'expected.json'` fails `\.expected\b` (preceding char is the quote) and the line's other string `'command-binding-expected-v1'` has `-` before `expected`. Scratch replication of the exact regexes against the exact line: `V1_EXPECTED_RE.search(line) → None` ⇒ `live_json_v1=0`.
- v2 hits: `EXPECTED_RE` at `tools/write-path-census-v2.py:23-25` adds `expected\.json` to the alternation and `WRITE_RE` at `:16-22` retains `\.write_bytes\s*\(` — `re.search` on line 123 returns a match for both ⇒ `live_json_v2=1`. Net: `live_json_v2 >= 1 and live_json_v1 == 0` ⇒ the json half of `live_ok` (measure.py:219) holds.
- Stability across revs: `git show 304e3355705640af2879c772fc9a5c2902c61763:tools/registry-replay.py`, `git show 5641ed84c8dc148c34c8dd83f062279ddf06b4af:tools/registry-replay.py` (HEAD), and the worktree file are byte-identical (both `diff` runs return 0). Same result `live_json_v2=1 live_json_v1=0` at base and freeze.
- No second candidate: of the four `write_bytes` sites (lines 122, 123, 125, 183) only line 123 contains `expected.json`, so no other line can flip `live_json_v1` above 0.

## Residual risk

- The filter requires `.write_bytes` and `expected.json` on the same source line; a future edit wrapping the call across lines (e.g. `(out /\n    'expected.json').write_bytes(...)`) would yield zero candidates and collapse this clause. Current content is safe; flagging only as fragility of a per-line scan.
- Verification gap: the counters were not run in default mode (reserved for the L1 deciding run). Verification is by byte-exact replication of both compiled regexes against the `git show` content at base and freeze — equivalent inputs, same operator, scratch-only.
- Lane checkout and shokuknow untouched; no edits made anywhere.

Commands for re-verification:
- `grep -n "expected.json" /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-replay.py` → line 123 only.
- `python3 -c "import re; ln=open('tools/registry-replay.py').read().splitlines()[122]; v1=re.compile(r\"['\"][^'\"]*(?:\.expected\b|expected\.txt|golden|snapshot)[^'\"]*['\"]\"); v2=re.compile(r\"['\"][^'\"]*(?:\.expected\b|expected\.txt|expected\.json|golden|snapshot)[^'\"]*['\"]\"); print(bool(v1.search(ln)), bool(v2.search(ln)))"` → `False True`.
