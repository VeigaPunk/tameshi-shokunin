# ReviewGate06 — census attack on tools/golden-verdict.py

Seat: ReviewGate06 · Milestone: Gate attack · Judged on: depth
Target: frozen `WRITE_RE` in `tools/write-path-census.py` (pinned sha256
`bc8c660c…7edc62` per `.ufo/evidence/round-39/contract.json` claim C2) applied to
`tools/golden-verdict.py` @ 233077f88d7a8d142eff329202a120457a5d5258.

## Verdict

No uncovered missed write. Every construct `WRITE_RE` does not match in this file
falls inside the pattern's named limits. The pattern correctly counts all three
path-bearing write calls; classification stands at `write_sites=3 unflagged=0`.

## Frozen pattern and named limits (tools/write-path-census.py)

```python
WRITE_RE = re.compile(                                           # :46-50
    r"""open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]"""
    r"""|\.write_text\s*\("""
    r"""|\.write_bytes\s*\("""
)
```

Named limits (docstring, tools/write-path-census.py:9-11): "This is not a full
lexer and not a claim that every write in every language is seen. Shell
redirects and writes whose path is not on the same line as the call are outside
the frozen patterns."

## Evidence — canonical tool replayed read-only on the lane

```
$ python3 tools/write-path-census.py --census /home/vgpnk/Projects/shokunin/tameshi-shokunin
WRITE_CENSUS: gates=21/21 live_write_sites=99 live_unflagged=0 missing=0
GATE golden-verdict.py write_sites=3 unflagged=0 sha256=c5f9616be719fdce99e8aaa9d8c9b1cde5c4c2d4d4db0b517ec16c1a26d15f87
```

Line-level replay of `classify_text`'s own regexes over the file (pure regex on
read bytes; live lane untouched) confirms which lines hit:

```
HIT  52  with open(golden, 'w', encoding='utf-8') as fh:
HIT  54  with open(same, 'w', encoding='utf-8') as fh:
HIT  56  with open(other, 'w', encoding='utf-8') as fh:
MISS 53          fh.write('alpha\nbeta\n')
MISS 55          fh.write('alpha\nbeta\n')
MISS 57          fh.write('alpha\ngamma\n')
MISS 47  with tempfile.TemporaryDirectory(prefix='golden-verdict-') as tmp:
write_sites=3 unflagged=0 flagged(file-level)=False
```

## Line-by-line accounting of every unmatched construct

| Line | Construct | Covered by named limit? |
|------|-----------|-------------------------|
| tools/golden-verdict.py:53,55,57 | `fh.write(payload)` — write primitive carrying no path operand | Yes — "writes whose path is not on the same line as the call." The path (`golden`/`same`/`other`) is bound at the `open` on the prior line; the `.write` call line has no path. The write *site* is still counted via the `open` line, so nothing is silently lost. |
| tools/golden-verdict.py:47 | `tempfile.TemporaryDirectory(prefix='golden-verdict-')` — fs mutation (mkdtemp) | Yes, on either reading: the created path is runtime-generated and not on the call line, and the docstring disclaims seeing "every write in every language." Scratch-space creation, never an expected-value overwrite target. |
| tools/golden-verdict.py:62-63 | `print('GOLDEN_VERDICT_SELFTEST…')` / FAIL lines — stdout writes | Yes — no path on the call line. |
| tools/golden-verdict.py:78,86,88-90,110 | `print` / `ap.print_usage(sys.stderr)` | Yes — same, stderr/stdout writes carry no path operand. |
| tools/golden-verdict.py:40 | `subprocess.run([diff_bin, '-u', golden, actual], …)` | Not a write — `diff -u` with `capture_output=True` emits a unified diff to captured stdout and mutates no file. |
| tools/golden-verdict.py:75 | `open(path, encoding='utf-8')` | Read mode; correctly not counted. |

## Honest residuals (adjacent limbs, not a WRITE_RE miss)

1. `EXPECTED_RE` matches only quoted literals on the write line, so
   `open(golden, 'w')` at tools/golden-verdict.py:52 counts as a write site but
   not as an expected-value write — `golden` is a variable bound at :48. That is
   a recall limit of `EXPECTED_RE`, a different predicate limb; ReviewC2Literal
   already filed it at the same line. The write itself is not missed, and the
   file writes into TemporaryDirectory scratch, so `unflagged=0` is substantively
   correct.
2. A hypothetical one-liner `open(os.path.join(tmp, 'expected.txt'), 'w')` would
   trip `EXPECTED_RE` while evading `SCRATCH_RE` (no `/tmp/`, `tempfile`, or
   `scratch` on the line), inflating `unflagged` — but no such line exists in
   this file; reporting it would be a counterfactual, not a finding.

## Predicate impact

None. C2's PASS conjuncts (pinned tool sha, planted-case selftest, FLAG_GATE
mutant kill, 21/21 classification from REV bytes) do not require full-corpus
write recall; the named-limit coverage here leaves C2 unfalsified. Base-rev
control not rerun — my scope is this gate's classification at REV.
