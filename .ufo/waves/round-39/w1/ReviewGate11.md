# ReviewGate11 — C2 census-classification attack: `tools/receipt-window.py`

Round 39, wave 1 gate attack. Frozen contract read at
`.ufo/evidence/round-39/contract.json` (not edited). Lane bytes verified
identical to HEAD `233077f88d7a8d142eff329202a120457a5d5258` for both files
below, so every live classification here equals the REV-bytes classification
`census/measure.py` will perform. No live-lane file was edited; no counting
command (`census/measure.py`) was run — the kill rule reserves one deciding run.

## Verdict

**The pattern's named limit covers it. No write in `receipt-window.py` escapes
the frozen pattern set in a way that changes the classification.**

## Findings (by severity)

### None — no actionable miss

Complete write inventory of `tools/receipt-window.py` (367 lines; inventory via
grep over `open(|.write(|write_text|write_bytes|json.dump|os.replace|os.rename|
os.makedirs|file=|Path(|fdopen|>>`):

| Line | Call | WRITE_RE | Classified |
|---|---|---|---|
| 63, 125 | `with open(path, encoding="utf-8") as fh:` (reads) | no | correctly not counted |
| 215, 224, 237 | `print(json.dumps(...))` (stdout only) | no | not a file write |
| 277 | `row.update(extra)` (dict method) | no | does not hit FLAG_RE (`--update\b`/`update_goldens` absent file-wide; verified `FLAG_RE.search(src) == False`) |
| 329 | `with open(bad_contract, "w", encoding="utf-8") as fh:` | **yes** | write site, not unflagged |
| 330 | `fh.write("{not json")` | no | covered by named limit |
| 338 | `with open(bad_receipts, "w", encoding="utf-8") as fh:` | **yes** | write site, not unflagged |
| 339 | `fh.write('{"receipts": 5}')` | no | covered by named limit |

The runtime path (`load_contract` :61, `load_receipts` :123, `check` :139,
`run` :209, `main` :349) performs **zero** file writes — reads and stdout only.
`unflagged=0` is therefore the true classification, and the two real write
sites (selftest-only, both inside `tempfile.TemporaryDirectory` :327) are both
seen: `WRITE_RE` matches the `open(..., "w")` lines directly.

The only pattern-invisible write calls are `fh.write(` at :330 and :339. Their
path literals (`bad-contract.json` :328, `bad-receipts.json` :337) are not on
the call line, which is exactly the limit the census docstring names:
`tools/write-path-census.py:10-12` — "This is not a full lexer … Shell
redirects and writes whose path is not on the same line as the call are
outside the frozen patterns." The sites are not lost either: the associated
opens :329/:338 are matched, so `write_sites` is complete.

## Evidence

Commands (read-only, cwd = lane root):

```
$ sha256sum tools/write-path-census.py
bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62   # == contract.json tool_sha256 pin
$ git show HEAD:tools/receipt-window.py | sha256sum   # == sha256sum tools/receipt-window.py
f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc
$ python3 tools/write-path-census.py --census .
WRITE_CENSUS: gates=21/21 live_write_sites=99 live_unflagged=0 missing=0
GATE receipt-window.py write_sites=2 unflagged=0 sha256=f03ae7e9…
$ python3 tools/write-path-census.py --selftest
WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1
```

Per-line probe through the pinned tool's own regexes (import of the pinned
module, scratch `/tmp/tameshi-r39-ReviewGate11`): :63/:125/:215/:277 all
`WRITE=False`; :329/:338 `WRITE=True EXPECTED=False`; :330/:339 `WRITE=False`;
`classify_text(whole file) == (2, 0)`, matching the census row.

## Residual risk (latent, not triggered by frozen bytes)

Path-literal/call split (:328→:329, :337→:338) means classification of these
writes reads only the quoted strings on the open line (`"w"`, `"utf-8"`);
neither the `.expected`-family name nor the `TemporaryDirectory` scratch marker
(:327) shares the write line. Probe: renaming the fixture
`bad-contract.expected` on :328 drops `classify_text` from `(1, 1)` (same-line
control) to `(1, 0)` — an expected-named scratch write would be invisible to
the unflagged count; symmetrically a same-line-`.expected` scratch write at
:329 would false-positive as unflagged because SCRATCH_RE never sees
`TemporaryDirectory` on that line. Frozen bytes don't trigger either direction
(neither `bad-contract.json` nor `bad-receipts.json` matches EXPECTED_RE), so
this is not a miss today — and it sits inside the docstring's same named limit
(classification only from the call line), not outside it.

## Verification gaps

- `census/measure.py` itself was not executed (deciding-run hygiene); REV-bytes
  equality is established by byte-identity of working tree vs `git show HEAD:`
  at `233077f`, and the tool sha matches the contract pin.
- No LSP server was consulted; this is a line-level pattern attack where the
  grep inventory + pinned-regex probe is the direct evidence.
