seat: ExecRows23

# C1 row re-verification: S153, S154, S155 (author-ledger entries)

All fetches: `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecRows23/S###.raw <url>`, exit 0 on first try (no retry needed). Raw bytes kept at `/tmp/tameshi-r45-ExecRows23/S###.raw`. Counter: `.ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check <fragment> --snapdir /tmp/tameshi-r45-ExecRows23`.

## S153 — ast docs (https://docs.python.org/3/library/ast.html)
- curl exit 0; 362029 bytes; sha256 `f4c18b31aea745258ff49b4227fca6e916a528dfb5ef77da4f3fa89323346b82`
- CHECK: `CHECK S153 verified ok`
- Quote located afresh via `--extract`: "Get source code segment of the source that generated node" (ast.get_source_segment) — shares `source`, `node`, `segment` with the row's anchor/teaches; not copied from the row's cells.
- Note: the live ast docs still state ast.get_source_segment returns the source code segment that generated a node, grounding the teaches source-recovery claim.
- Fragment:
```json
{"id":"S153","url":"https://docs.python.org/3/library/ast.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"f4c18b31aea745258ff49b4227fca6e916a528dfb5ef77da4f3fa89323346b82","quote":"Get source code segment of the source that generated node","snapshot":".ufo/evidence/round-45/freshness/sources/S153.raw.gz","author":"ExecRows23","note":"The live ast docs still state ast.get_source_segment returns the source code segment that generated a node, grounding the teaches source-recovery claim."}
```

## S154 — pathlib docs (https://docs.python.org/3/library/pathlib.html)
- curl exit 0; 271189 bytes; sha256 `7ae9b7205cf1a79380379fae860a93ddb88d9bec24284f946f4019cfd1ae016e`
- CHECK: `CHECK S154 verified ok`
- Quote located afresh via `--extract`: "Open the file pointed to in text mode, write data to it, and close the file" (§Path.write_text) — shares `file`, `data`, `write`, `close`, `text`, `mode` with scope/anchor/teaches; not copied from the row's cells.
- Note: the live pathlib docs still say write_text opens the pointed-to file in text mode, writes data and closes it, so the receiver expression is the destination path.
- Fragment:
```json
{"id":"S154","url":"https://docs.python.org/3/library/pathlib.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"7ae9b7205cf1a79380379fae860a93ddb88d9bec24284f946f4019cfd1ae016e","quote":"Open the file pointed to in text mode, write data to it, and close the file","snapshot":".ufo/evidence/round-45/freshness/sources/S154.raw.gz","author":"ExecRows23","note":"The live pathlib docs still say write_text opens the pointed-to file in text mode, writes data and closes it, so the receiver expression is the destination path."}
```

## S155 — PIT basic concepts (https://pitest.org/quickstart/basic_concepts/)
- curl exit 0; 12155 bytes; sha256 `c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a`
- CHECK: `CHECK S155 verified ok`
- Quote located afresh via `--extract`: "No coverage is the same as Survived except there were no tests that exercised the line of code where the mutation was created" (§Running the tests outcome list) — shares `coverage`, `Survived`, `mutation` with the row's teaches; not copied from the row's cells.
- Note: the live PIT outcome list still says No coverage is Survived without any exercising test, grounding the teaches outcome-vocabulary claim.
- Fragment:
```json
{"id":"S155","url":"https://pitest.org/quickstart/basic_concepts/","opened":"2026-10-25","verdict":"holds","raw_sha256":"c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a","quote":"No coverage is the same as Survived except there were no tests that exercised the line of code where the mutation was created","snapshot":".ufo/evidence/round-45/freshness/sources/S155.raw.gz","author":"ExecRows23","note":"The live PIT outcome list still says No coverage is Survived without any exercising test, grounding the teaches outcome-vocabulary claim."}
```

## Tooling/installs
None installed (no new tool/version/channel/reason to record; only stock curl/python3/git used).
