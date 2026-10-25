seat: ExecRows05

# Round-45 w1 — C1 row re-verification: S041, S047, S048 (author)

All three rows point to the same live URL (`https://pitest.org/quickstart/incremental_analysis/`); each row was fetched independently (3 separate live curls) and each fragment carries its own raw fetch. All verdicts `holds`. Raw snapshots kept at `/tmp/tameshi-r45-ExecRows05/S041.raw`, `S047.raw`, `S048.raw` for L1 integration.

## S041
- URL: `https://pitest.org/quickstart/incremental_analysis/` (byte-exact from the row's source cell)
- curl exit 0; bytes 8892; sha256 `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db`
- CHECK: `CHECK S041 verified ok` (rc 0)
- Note: quote is the potential-error sentence in §Incremental analysis; shares 5 content words with scope/anchor/teaches (optimisations, introduce, potential, error, analysis).
```json
{"id":"S041","url":"https://pitest.org/quickstart/incremental_analysis/","opened":"2026-10-25","verdict":"holds","raw_sha256":"e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db","quote":"With the exception of 4), all these optimisations introduce a degree of potential error into the analysis","snapshot":".ufo/evidence/round-45/freshness/sources/S041.raw.gz","author":"ExecRows05","note":"The live PIT incremental-analysis page still states that all reuse optimisations except 4) introduce a degree of potential error, directly matching S041's teaching that reuse of a prior verdict is an inference, not an observation."}
```

## S047
- URL: `https://pitest.org/quickstart/incremental_analysis/` (byte-exact from the row's source cell)
- curl exit 0; bytes 8892; sha256 `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db`
- CHECK: `CHECK S047 verified ok` (rc 0)
- Note: quote is the dependency-assumption sentence in §Incremental analysis; shares 3 content words with scope/anchor/teaches (assumption, unproven, currently).
```json
{"id":"S047","url":"https://pitest.org/quickstart/incremental_analysis/","opened":"2026-10-25","verdict":"holds","raw_sha256":"e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db","quote":"Although this assumption seems reasonable, it is currently unproven .","snapshot":".ufo/evidence/round-45/freshness/sources/S047.raw.gz","author":"ExecRows05","note":"The live dependency paragraph still reads 'it is currently unproven' immediately after defining the dependency assumption, matching S047's claim that the dependency assumption is unproven; the numbered optimisations 1-5 and the potential-error sentence also remain."}
```

## S048
- URL: `https://pitest.org/quickstart/incremental_analysis/` (byte-exact from the row's source cell)
- curl exit 0; bytes 8892; sha256 `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db`
- CHECK: `CHECK S048 verified ok` (rc 0)
- Note: quote is item 4's opening clause in §Incremental analysis; shares 2 content words with scope/anchor/teaches (mutation, test).
```json
{"id":"S048","url":"https://pitest.org/quickstart/incremental_analysis/","opened":"2026-10-25","verdict":"holds","raw_sha256":"e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db","quote":"If a mutation was previously killed, but the class or killing test has changed","snapshot":".ufo/evidence/round-45/freshness/sources/S048.raw.gz","author":"ExecRows05","note":"Item 4's premise sentence survives verbatim - a previously-killed mutation whose class or killer changed is assumed still killed, i.e. a prioritisation heuristic rather than a reuse skip - and item 5's '(not yet implemented)' tag remains, matching S048."}
```

## Commands run (per row)
```
mkdir -p /tmp/tameshi-r45-ExecRows05
curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecRows05/S###.raw 'https://pitest.org/quickstart/incremental_analysis/'
sha256sum /tmp/tameshi-r45-ExecRows05/S###.raw
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r45-ExecRows05/S###.raw
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-ExecRows05/S###.json --snapdir /tmp/tameshi-r45-ExecRows05
```
Results: `CHECK S041 verified ok`, `CHECK S047 verified ok`, `CHECK S048 verified ok`, all rc 0.

## Notes
- Row URLs parsed from `corpus/SOURCES.md` via the counter's own `parse_rows`/`URL_RE`: all three are byte-exact `https://pitest.org/quickstart/incremental_analysis/`; rows are `mined`, id <= S160, and in the 73-row population.
- Quotes were selected from the `--extract` normalized text only (never from row cells); each shares >= 2 content words with scope/anchor/teaches and is 6-25 whitespace tokens.
- Fetched bytes identical across the three independent curls; sha256 matches each fragment's `raw_sha256` field.
- No tools installed (none needed); no lane/fleet edits; all scratch under `/tmp/tameshi-r45-ExecRows05/`.
