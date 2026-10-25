# ReviewC2Literal — literal-path limit on the C2 census

Scope: attack the census limit, not a universal claim. Seat judged on depth;
milestone "Literal limit".

## Finding (primary)

`tools/golden-verdict.py:52` — an expected-value write whose path is not a
string literal on the `open()` line:

    48:    golden = os.path.join(tmp, 'expected.txt')
    52:    with open(golden, 'w', encoding='utf-8') as fh:

The census classifier (`tools/write-path-census.py`, sha256
`bc8c660c…edc62` = contract pin) decides `unflagged` per line:
`WRITE_RE` hits line 52, `EXPECTED_RE` requires a quoted literal matching
`\.expected|expected\.txt|golden|snapshot` **on the same line** and fails on
the bare identifier `golden`. `FLAG_RE`
(`--update_goldens|--update-goldens|--update\b|update_goldens`) has zero hits
in this file (verified), and `SCRATCH_RE` does not hit line 52 — so had the
path been the literal `'expected.txt'` it binds to, this site would count as
unflagged. Only the non-literal path hides it. The write itself is
unconditional: every `--selftest` invocation rewrites the golden.

## Corroborating instances (same mechanism)

- `tools/context-capture.py:1682` `with open(expected_path, "wb")` and
  `:1685` `with open(expected_path, "w", …)` — path bound at :1662 to
  `os.path.join(directory, "expected.json")`, written on every
  `check_case(..., write_expected=True)`; no flag.
- `tools/command-binding.py:182` `expected_path.write_text(json.dumps(
  {'schema': EXPECTED, 'bundle_sha256': digest}))` — path bound at :175 to
  `Path(tmp) / 'expected.json'`, written unconditionally once per selftest
  case; no flag.
- `tools/repeat-control.py:811` `with open(duplicate_path, "wb")` — path
  bound at :808 to `os.path.join(tamper_duplicate_key, "expected.json")`,
  the snapshot's own expected manifest; no flag.
- `tools/evidence-disposition.py:1759` `_write_bytes(evidence /
  "expected.json", expected_bytes)` — literal sits on the call line but the
  callee is a user helper (`_write_bytes`, defined :1710), so `WRITE_RE`
  (which requires `open(` or `.write_bytes(`) does not count it as a write
  site at all; the site is doubly invisible.

Note the second, adjacent blind spot these expose: `expected.json` — the
lane's canonical expected-value filename — is outside `EXPECTED_RE`
(`\.expected\b` does not match `expected\.json`), so even a *literal*
`open("expected.json","w")` is uncounted. The planted corpus never probes
`expected.json` or a variable path, so the selftest cannot see either gap.

## Evidence

Command (read-only, from scratch copy of the pinned tool):

    cd /tmp/tameshi-r39-ReviewC2Literal && \
    python3 write-path-census.py --census /home/vgpnk/Projects/shokunin/tameshi-shokunin

Output:

    WRITE_CENSUS: gates=21/21 live_write_sites=99 live_unflagged=0 missing=0
    GATE golden-verdict.py write_sites=3 unflagged=0 sha256=c5f9616b…
    GATE context-capture.py write_sites=3 unflagged=0 sha256=c4a1d165…
    GATE command-binding.py write_sites=2 unflagged=0 sha256=9230c68e…
    GATE repeat-control.py write_sites=3 unflagged=0 sha256=296fe566…
    GATE evidence-disposition.py write_sites=4 unflagged=0 sha256=39ee5c5e…

Regex cross-check of the exact lines (same regexes as the pinned tool):

    golden-verdict.py flagged=False
    golden-verdict.py:52 write=True expected=False scratch=False
    context-capture.py:1682 write=True expected=False scratch=False
    command-binding.py:182 write=True expected=False scratch=False
    repeat-control.py:811 write=True expected=False scratch=False

`live_unflagged=0` on the live lane despite ≥5 real unflagged writes to
expected-value files; every one is missed specifically because the path is a
variable (or a helper call), never a literal on the write line. The tool's
own docstring concedes "writes whose path is not on the same line as the
call are outside the frozen patterns" — the census counts the limit
honestly, but `live_unflagged=0` must be read as "0 literal-path unflagged
writes", not "0 unflagged expected writes".

## Residual risk

Low to the frozen predicate: the limit is documented in-tool and
`live_unflagged` is reported-not-required by the contract kill rule, so the
miss does not falsify `C2_R39_PASS` gating — it bounds what the PASS
conveys. Any downstream consumer treating `live_unflagged=0` as semantic
"no unflagged expected writes" inherits the false negative.

No tools installed or updated this round (pacman transactions paused; no
install needed).
