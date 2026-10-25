seat: ExecRows03

# Round-45 w1 — C1 row re-verification fragments: S008, S011, S012

Author of all three ledger entries (freshness C1). Every fetch on 2026-10-25 from the row's own first http(s) URL, curl exit 0, verdict `holds` for all three. Quotes were located afresh in the `measure.py --extract` output, never copied from the registry cells. Checks run against the frozen revision only:

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 3310e7be803516ca5934b4e949d91bcec824b179 \
  --check /tmp/tameshi-r45-ExecRows03/S###.json --snapdir /tmp/tameshi-r45-ExecRows03
```

Fetch command (per row, from /tmp/tameshi-r45-ExecRows03):

```
curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S###.raw '<url>'
```

No tool installs or updates this seat (pdftotext already present; the S011 PDF went through it via `--extract`).

## S008 — Practical Mutation Testing at Scale (arXiv 2102.11378)

- URL (first http(s) URL of the source cell, exact): `https://arxiv.org/abs/2102.11378`
- curl exit: 0; bytes: 45029; sha256: `aaf66df07f514232c0eb1cdf010c9db99a1a9e886c9a6a3f933c54fb32eceeed`
- CHECK line: `CHECK S008 verified ok` (exit 0)
- quote: 23 tokens; shared content words with scope+anchor+teaches: `code, developers, line, mutants, review`
- note: Live arXiv v2 abstract still states the per-line/per-review mutant filtering and the developer-scale evaluation that the row's teaches cell claims ("more than 24,000 developers on more than 1,000 projects" is still in the same abstract paragraph).

```json
{
  "id": "S008",
  "url": "https://arxiv.org/abs/2102.11378",
  "opened": "2026-10-25",
  "verdict": "holds",
  "raw_sha256": "aaf66df07f514232c0eb1cdf010c9db99a1a9e886c9a6a3f933c54fb32eceeed",
  "quote": "removing mutants that are likely to be irrelevant to developers, and limiting the number of mutants per line and per code review process",
  "snapshot": ".ufo/evidence/round-45/freshness/sources/S008.raw.gz",
  "author": "ExecRows03",
  "note": "Live arXiv v2 abstract still states the per-line/per-review mutant filtering and the developer-scale evaluation that the row's teaches cell claims."
}
```

## S011 — Mitigating the Effects of Flaky Tests on Mutation Testing (ISSTA 2019)

- URL: `https://mir.cs.illinois.edu/awshi2/publications/ISSTA2019.pdf`
- curl exit: 0; bytes: 295016; sha256: `a5c8d2a222cc1d3c53a68c4675c4c64070e94c29f5a6ab5b6dcac3c5e8bdc21c`
- CHECK line: `CHECK S011 verified ok` (exit 0)
- quote: 24 tokens; shared content words: `between, four, mutant, mutation, pairs, points, scores, test, unknown, vary`
- note: Live PDF abstract (p.1) still reports the four-point mutation-score variation between repeated executions and the 9% unknown mutant-test pairs that the teaches cell claims; the 22% nondeterministic-coverage and 79.4% rerun-reduction figures are also still present in the same document (Table 4 / conclusions).

```json
{
  "id": "S011",
  "url": "https://mir.cs.illinois.edu/awshi2/publications/ISSTA2019.pdf",
  "opened": "2026-10-25",
  "verdict": "holds",
  "raw_sha256": "a5c8d2a222cc1d3c53a68c4675c4c64070e94c29f5a6ab5b6dcac3c5e8bdc21c",
  "quote": "in our experiments, mutation scores vary by four percentage points on average between repeated executions, and 9% of mutant-test pairs have an unknown status",
  "snapshot": ".ufo/evidence/round-45/freshness/sources/S011.raw.gz",
  "author": "ExecRows03",
  "note": "Live ISSTA 2019 PDF abstract (p.1) still reports the four-point mutation-score variation between runs and the 9% unknown mutant-test pairs that the teaches cell claims."
}
```

## S012 — Oracles That Cannot Fail (arXiv 2608.17214)

- URL: `https://arxiv.org/abs/2608.17214`
- curl exit: 0; bytes: 42588; sha256: `fb6f384d294898d2a154c248261b518e77a3363a4e40ed92f4bf17b35fea2a80`
- CHECK line: `CHECK S012 verified ok` (exit 0)
- quote: 25 tokens; shared content words: `anchored, code, expectation, flows, mutation, state`
- note: Live arXiv v1 abstract still defines state-anchored expectations as flowing (directly or transitively) from the code under mutation — the row's teaches claim; the same abstract still carries the 8-of-46 re-anchoring recovery, the 366-mutant/one-system scope and the "one system by one author" caveat.

```json
{
  "id": "S012",
  "url": "https://arxiv.org/abs/2608.17214",
  "opened": "2026-10-25",
  "verdict": "holds",
  "raw_sha256": "fb6f384d294898d2a154c248261b518e77a3363a4e40ed92f4bf17b35fea2a80",
  "quote": "An expectation is specification-anchored when composed from values fixed outside the code under mutation, and state-anchored when it flows, directly or transitively, from that code",
  "snapshot": ".ufo/evidence/round-45/freshness/sources/S012.raw.gz",
  "author": "ExecRows03",
  "note": "Live arXiv v1 abstract still names state-anchored expectations as flowing from the code under mutation, which is the row's teaches claim; the same abstract still reports the 8 of 46 re-anchoring recovery."
}
```

## Notes for the L1

- Raw bytes kept for integration at `/tmp/tameshi-r45-ExecRows03/S008.raw`, `S011.raw`, `S012.raw`; the three fragment JSONs sit beside them (`S008.json`, `S011.json`, `S012.json`). gzip each `.raw` into `.ufo/evidence/round-45/freshness/sources/S###.raw.gz` unchanged — the sha256s above are of the uncompressed bytes and match the `raw_sha256` fields.
- Row URL identity confirmed against the registry at the frozen rev by the counter's own `parse_rows` (`entry.url == row.url` true for all three).
- No `member` field: none of the three is an archive; S011 is a bare PDF that `--extract` routes through pdftotext.
- A previous run of this seat left `/tmp/tameshi-r45-ExecRows03/S011.wrapped` and empty `*.err` files plus an earlier version of this report; this report and the three fragment JSONs above are the current, re-verified set (all three `CHECK` lines re-run against them).
- No risks or blockers; no tool installs or updates this seat.
