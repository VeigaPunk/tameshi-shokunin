seat: ExecRows19

# C1 row re-verification — S099, S100, S101 (author ledger entries)

All three rows fetched live on 2026-10-25, verified `holds`, and each fragment passed the counter's
`--check` against the frozen revision `3310e7be803516ca5934b4e949d91bcec824b179`.

Command shapes used (per row, same for all three):
- fetch: `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecRows19/S###.raw '<url>'`
- extract: `python3 .ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r45-ExecRows19/S###.raw`
- check: `python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-ExecRows19/S###.json --snapdir /tmp/tameshi-r45-ExecRows19`

## S099 — PIT Mutation Testing (https://pitest.org/)

- curl exit: 0; bytes: 12023; sha256: b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc
  (matches the row's committed 2026-10-23 digest byte-for-byte: corpus/SOURCES.md:107)
- CHECK line: `CHECK S099 verified ok` (rc=0)
- note: The live PIT homepage's "What is mutation testing?" passage still says faults are
  automatically seeded, tests are rerun, and a failing test kills the mutation while passing lets
  it live — exactly what the teaches cell claims (corpus/SOURCES.md:107).
- quote grounds teaches: "Faults (or mutations ) are automatically seeded into your code, then
  your tests are run." shares content words (faults, mutations, seeded, tests) with the row's
  scope/anchor/teaches; it was copied verbatim from the `--extract` output, not from the row.

```json
{"id":"S099","url":"https://pitest.org/","opened":"2026-10-25","verdict":"holds","raw_sha256":"b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc","quote":"Faults (or mutations ) are automatically seeded into your code, then your tests are run.","snapshot":".ufo/evidence/round-45/freshness/sources/S099.raw.gz","author":"ExecRows19","note":"The live PIT homepage's 'What is mutation testing?' passage still says faults are automatically seeded, tests are rerun, and a failing test kills the mutation while passing lets it live - exactly what the teaches cell claims."}
```

## S100 — doctest, Python 3.15 build (https://docs.python.org/3.15/library/doctest.html)

- curl exit: 0; bytes: 216574; sha256: 6f6c1467595ab4003a342014cc118d8fa60c20e43ce09144de11df657c80ca52
- CHECK line: `CHECK S100 verified ok` (rc=0)
- note: The 3.15 doctest module introduction still opens with the first bullet describing
  executable documentation examples as interactive Python sessions that are executed to verify
  they work, so the row's pinned 3.15 build is faithfully represented by today's live bytes
  (corpus/SOURCES.md:108).
- quote grounds teaches/scope: the first bullet sentence (anchor "module introduction, first
  bullet") shares content words `module` and `python` with the anchor; quote copied verbatim from
  the `--extract` output.

```json
{"id":"S100","url":"https://docs.python.org/3.15/library/doctest.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"6f6c1467595ab4003a342014cc118d8fa60c20e43ce09144de11df657c80ca52","quote":"doctest module searches for pieces of text that look like interactive Python sessions, and then executes those sessions to verify that they work","snapshot":".ufo/evidence/round-45/freshness/sources/S100.raw.gz","author":"ExecRows19","note":"The 3.15 doctest module introduction still opens with the first bullet describing executable documentation examples as interactive Python sessions that are executed to verify they work, so the row's pinned 3.15 build is faithfully represented by today's live bytes."}
```

## S101 — Major Mutation Framework (https://mutation-testing.org/)

- curl exit: 0; bytes: 4341; sha256: 0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420
  (matches the row's committed 2026-10-23 digest byte-for-byte: corpus/SOURCES.md:109)
- CHECK line: `CHECK S101 verified ok` (rc=0)
- note: The Major Mutation Framework overview feature list still lists suppressing equivalent
  mutants and computing the mutant-detection rate and live-mutant set, supporting the teaches
  claim that frameworks treat equivalent mutants as first-class (corpus/SOURCES.md:109).
- quote grounds teaches: shares content words (suppressing, equivalent, mutants, computing,
  mutant, detection, rate, live, set) with scope/anchor/teaches; copied verbatim from the
  `--extract` output.

```json
{"id":"S101","url":"https://mutation-testing.org/","opened":"2026-10-25","verdict":"holds","raw_sha256":"0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420","quote":"suppressing equivalent mutants; computing the mutant-detection rate and the set of live mutants","snapshot":".ufo/evidence/round-45/freshness/sources/S101.raw.gz","author":"ExecRows19","note":"The Major Mutation Framework overview feature list still lists suppressing equivalent mutants and computing the mutant-detection rate and live-mutant set, supporting the teaches claim that frameworks treat equivalent mutants as first-class."}
```

## Artifacts

- Raw snapshots kept in /tmp/tameshi-r45-ExecRows19/: S099.raw, S100.raw, S101.raw
  (for L1 integration as `.ufo/evidence/round-45/freshness/sources/S###.raw.gz`).
- Fragment JSONs: /tmp/tameshi-r45-ExecRows19/{S099,S100,S101}.json.
- No tools installed or updated (nothing beyond stock curl/python3/git); no tooling changes to record.
- No files outside the lane's report path and /tmp/tameshi-r45-ExecRows19/ were written.
