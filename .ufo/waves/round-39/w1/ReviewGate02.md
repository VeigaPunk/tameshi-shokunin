# ReviewGate02 — Gate attack: census classification of tools/command-binding.py

Round 39, wave w1, 2026-10-24. Scope: F4 write-path census (C2) classification of the
gate `tools/command-binding.py` (frozen GATES entry #2). Attack = find one write the
frozen pattern misses, or show the pattern's named limit covers it. No lane/checkout,
index, or `.ufo/state` mutation; classification exercised the pinned tool's own
`classify_text` in-process (the same function the C2 counter drives via
`--selftest`/`--census`). The deciding counters were not run.

## Verdict

**No write site is missed. The one classification-relevant write is covered by the
pattern's named limit.** No actionable defect.

The gate has exactly two filesystem write sites, both caught by frozen `WRITE_RE`
(`tools/write-path-census.py:46-49`):

- `tools/command-binding.py:182` — `expected_path.write_text(json.dumps({'schema': EXPECTED, 'bundle_sha256': digest}))` → matches `\.write_text\s*\(`
- `tools/command-binding.py:183` — `bundle_path.write_bytes(raw + (b' ' if name == 'tampered' else b''))` → matches `\.write_bytes\s*\(`

Empirical: importing the pinned module (live sha256 `bc8c660c…` == contract C2 pin)
and running `classify_text` on the gate bytes (sha256 `9230c68e…` == HEAD blob, == live
working file) yields `write_sites=2 unflagged=0`; per-line W hits at 182 and 183 only.

## Why L182 is not an unflagged-expected miss

L182 writes the trusted expected commitment (schema `command-binding-expected-v1`,
pinning the bundle digest) under the name `expected.json`, unconditionally — the gate
names no update flag (`FLAG_RE` over the file: no match). It is classified site-only
(`unflagged=0`) for one primary and one independent reason:

1. **Named limit covers it (primary).** The path literal `'expected.json'` is bound at
   `tools/command-binding.py:175` (`bundle_path, expected_path = Path(tmp) / 'bundle.json', Path(tmp) / 'expected.json'`),
   a different line from the `.write_text(` call at :182. The census docstring names
   exactly this: `tools/write-path-census.py:9-11` — "This is not a full lexer and not a
   claim that every write in every language is seen. Shell redirects and writes whose
   path is not on the same line as the call are outside the frozen patterns."

2. **Vocabulary gap (independent, redundant here).** Even a same-line
   `open("expected.json", "w")` scores `write=1 unflagged=0`: `EXPECTED_RE`
   (`write-path-census.py:51-53`) matches only `.expected`, `expected.txt`, `golden`,
   `snapshot` inside a quoted literal; `expected.json` has the dot *after* "expected"
   and the wrong extension. Control: `EXPECTED_RE` on `"case.expected"` → True (the
   planted fixtures use dot-prefixed `.expected` and pass). So this gate's
   expected-file naming is structurally invisible to the unflagged classifier at any
   line placement. This is a pattern-vocabulary observation, not a missed write site,
   and C2 is unaffected: the contract reports `live_unflagged` explicitly "not a
   pre-declared PASS conjunct".

Non-write filesystem effects are also correctly out of the census's write-site count:
`tempfile.TemporaryDirectory(...)` at :174 is scratch and matches `SCRATCH_RE`
(`/tmp/|tempfile|TemporaryDirectory|...`); `subprocess.run` at :184 re-executes this
read-only validator; `print`/`print_usage` target stdout/stderr.

## Commands and outputs

```
$ git rev-parse HEAD
233077f88d7a8d142eff329202a120457a5d5258
$ sha256sum tools/write-path-census.py      # == contract C2 tool_sha256 pin
bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62
$ git show HEAD:tools/command-binding.py | sha256sum
9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d   # == live working file
# classify_text on those bytes (pinned module imported in-process):
classify_text: write_sites=2 unflagged=0
L182 W=1 E=0 S=0 | expected_path.write_text(...)
L183 W=1 E=0 S=0 | bundle_path.write_bytes(...)
file FLAG_RE: False
EXPECTED_RE on "'expected.json'": False      EXPECTED_RE on '"case.expected"': True
hypothetical open("expected.json","w"): write=1 unflagged=0
```

## Residual risk and verification gaps

- The deciding counter `.ufo/evidence/round-39/census/measure.py` was not executed
  (kill_rule reserves one deciding run post-wave). I exercised `classify_text`
  directly on REV==HEAD bytes; the counter's `--census` path is the same function.
- Classification used HEAD `233077f…` bytes, verified identical to the live file by
  digest. If the judging REV differs from HEAD, re-check the two digests; at base
  `50aadd1…` the census tool is absent (C2 before-state), so there is nothing to
  attack there.
- Only `tools/command-binding.py` was attacked; the other 20 frozen gates are out of
  scope for this ticket.

## Godspeed axes

1. classification depth — named-limit coverage proven, plus an independent
   `EXPECTED_RE` vocabulary gap (`expected.json` never matches) documented;
2. evidence quality — every claim backed by executed classification/digest output,
   not text reading;
3. no-harm — zero mutations (read-only git, in-process pure functions, scratch
   staging under /tmp/tameshi-r39-ReviewGate02/, this Report).
