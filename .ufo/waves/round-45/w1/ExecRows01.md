seat: ExecRows01

# Round 45 w1 — C1 row re-verification: S001, S002, S003

Author of all three ledger fragments. All three fetched live, extracted via the freshness counter's `--extract`, quotes located afresh in extracted normalized text (never copied from row cells), each `--check` passed against the frozen rev. Raw snapshots kept in /tmp/tameshi-r45-ExecRows01/ for L1 integration.

No tools installed (curl + python3 already present; no pacman/uv/npx installs).

## S001 — https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/
- curl exit: 0; bytes: 27068; sha256: ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11
- CHECK: `CHECK S001 verified ok` (rc=0)
- note: Live docs still define the mutation score as detected / valid * 100, exactly matching the teaches cell's score formula.
- fragment:

```json
{"id":"S001","url":"https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/","opened":"2026-10-25","verdict":"holds","raw_sha256":"ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11","quote":"Mutation score detected / valid * 100 The total percentage of mutants that were detected.","snapshot":".ufo/evidence/round-45/freshness/sources/S001.raw.gz","author":"ExecRows01","note":"Live docs still define the mutation score as detected / valid * 100, exactly matching the teaches cell's score formula."}
```

## S002 — https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/packages/report-schema/src/mutation-testing-report-schema.json
- curl exit: 0; bytes: 12799; sha256: 404575e9264686dbf85c399f6531fdb489bebc3146e7e1d793b8083bc6a041ae
- CHECK: `CHECK S002 verified ok` (rc=0)
- note: Schema at anchor lines 64-98 still carries the 8-value status enum whose property neighbors include killedBy, coveredBy, statusReason and testsCompleted, grounding the teaches cell.
- fragment:

```json
{"id":"S002","url":"https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/packages/report-schema/src/mutation-testing-report-schema.json","opened":"2026-10-25","verdict":"holds","raw_sha256":"404575e9264686dbf85c399f6531fdb489bebc3146e7e1d793b8083bc6a041ae","quote":"\"status\": { \"type\": \"string\", \"title\": \"MutantStatus\", \"description\": \"Result of the mutation.\", \"enum\": [\"Killed\", \"Survived\", \"NoCoverage\", \"CompileError\", \"RuntimeError\", \"Timeout\", \"Ignored\", \"Pending\"] }","snapshot":".ufo/evidence/round-45/freshness/sources/S002.raw.gz","author":"ExecRows01","note":"Schema at anchor lines 64-98 still carries the 8-value status enum whose property neighbors include killedBy, coveredBy, statusReason and testsCompleted, grounding the teaches cell."}
```

## S003 — https://stryker-mutator.io/docs/stryker-js/incremental/
- curl exit: 0; bytes: 33898; sha256: 4ae955dd4806682d268cd840ff268510255ec126405766598ae130fd96bae1cd
- CHECK: `CHECK S003 verified ok` (rc=0)
- note: Live Incremental Limitations section still states environment changes and (dev) dependencies are not detected, grounding the teaches blind-spot claim.
- fragment:

```json
{"id":"S003","url":"https://stryker-mutator.io/docs/stryker-js/incremental/","opened":"2026-10-25","verdict":"holds","raw_sha256":"4ae955dd4806682d268cd840ff268510255ec126405766598ae130fd96bae1cd","quote":"Any other changes to your environment are not detected, such as updates to other files, updated (dev) dependencies","snapshot":".ufo/evidence/round-45/freshness/sources/S003.raw.gz","author":"ExecRows01","note":"Live Incremental Limitations section still states environment changes and (dev) dependencies are not detected, grounding the teaches blind-spot claim."}
```

## Notes on iteration
- First S003 quote ("The dry run remains required; as it discovers tests, mutation coverage per test, and ensures Stryker runs successfully when no mutant is active.") failed `CHECK S003 invalid overlap 1`: "dry"/"run" are 3-letter tokens excluded by the counter's content-word rule (len >= 4), leaving only "required" shared. Replaced with the Limitations-passage quote sharing detected/dependencies/files with the teaches cell (verbatim in the extract, 18 tokens).
- All verdicts `holds`; no drift observed. All three rows remain live and match their teaches claims.

## Files
- Raw snapshots: /tmp/tameshi-r45-ExecRows01/S001.raw, S002.raw, S003.raw
- Fragments: /tmp/tameshi-r45-ExecRows01/S001.json, S002.json, S003.json
- Extracted texts: /tmp/tameshi-r45-ExecRows01/S00{1,2,3}.txt
