seat: ExecRows21

C1 row re-verification (freshness), rows S105, S106, S107 — verdicts: holds, holds, holds.

All three live fetches on 2026-10-25 with `curl -fsSL -A 'Mozilla/5.0' --max-time 90`; the sha256 of each live fetch matches the prefix pinned in the row's anchor (dda9f57d / 4b2c2ad0 / eb9dcedc), so the live bytes are byte-identical to the sources the rows were opened against. No tools installed (nothing needed; channel notes: n/a).

## S105
- URL: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html
- curl exit: 0; bytes: 33988; sha256: dda9f57dac3b2420966b5f4d14417b84dfc76ac7c4bb14ead5e901af86a1de5a
- CHECK: `CHECK S105 verified ok` (exit 0)
- Quote located afresh in the live EXIT STATUS section (lines 564-574); shares content words differences/found/error/occurred with anchor+teaches; not copied from row cells.
- Note: The live EXIT STATUS section still states the three exit values 0, 1 and >1, grounding the teaches claim that a golden comparison has three outcomes.
```json
{"id":"S105","url":"https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"dda9f57dac3b2420966b5f4d14417b84dfc76ac7c4bb14ead5e901af86a1de5a","quote":"0 No differences were found. 1 Differences were found. >1 An error occurred.","snapshot":".ufo/evidence/round-45/freshness/sources/S105.raw.gz","author":"ExecRows21","note":"The live EXIT STATUS section still states the three exit values 0, 1 and >1, grounding the teaches claim that a golden comparison has three outcomes."}
```

## S106
- URL: https://raw.githubusercontent.com/google/golden/master/golden.go
- curl exit: 0; bytes: 4043; sha256: 4b2c2ad039c45a548216588cc38bb954c3356d3d76b675e7e09a019f02de4e9f
- CHECK: `CHECK S106 verified ok` (exit 0). First attempt with a quote spanning the comment line break failed (`invalid quote absent`) because the extractor keeps the `//` comment markers in the folded text; quote fixed to be verbatim from `--extract` output incl. `//`.
- Quote located afresh in the live `Compare` doc comment; shares content words update/golden/flag/value with anchor+teaches; not copied from row cells.
- Note: The live Compare doc comment still puts the overwrite path behind the -update_golden flag, grounding the teaches claim about the update-flag discipline.
```json
{"id":"S106","url":"https://raw.githubusercontent.com/google/golden/master/golden.go","opened":"2026-10-25","verdict":"holds","raw_sha256":"4b2c2ad039c45a548216588cc38bb954c3356d3d76b675e7e09a019f02de4e9f","quote":"If the -update_golden flag is set, this function will overwrite the // contents of goldenFile with the actual value.","snapshot":".ufo/evidence/round-45/freshness/sources/S106.raw.gz","author":"ExecRows21","note":"The live Compare doc comment still puts the overwrite path behind the -update_golden flag, grounding the teaches claim about the update-flag discipline."}
```

## S107
- URL: https://raw.githubusercontent.com/tensorflow/federated/4d3a89c9b72f9c19352318d1457a5f7c01462824/docs/golden_tests.md
- curl exit: 0; bytes: 2287; sha256: eb9dcedcb042ab6af1d32b7d83e6f719826511951de33c49d0c3de94544c2abe
- CHECK: `CHECK S107 verified ok` (exit 0)
- Quote located afresh in the live "How do I update .expected files?" section; shares content words resulting/diff/checked/unanticipated/changes with anchor+teaches; not copied from row cells.
- Note: The live golden_tests.md still says the resulting diff should be checked for unanticipated changes, grounding the teaches claim that .expected files update only via --update_goldens.
```json
{"id":"S107","url":"https://raw.githubusercontent.com/tensorflow/federated/4d3a89c9b72f9c19352318d1457a5f7c01462824/docs/golden_tests.md","opened":"2026-10-25","verdict":"holds","raw_sha256":"eb9dcedcb042ab6af1d32b7d83e6f719826511951de33c49d0c3de94544c2abe","quote":"The resulting diff should be checked for unanticipated changes.","snapshot":".ufo/evidence/round-45/freshness/sources/S107.raw.gz","author":"ExecRows21","note":"The live golden_tests.md still says the resulting diff should be checked for unanticipated changes, grounding the teaches claim that .expected files update only via --update_goldens."}
```

Raw files kept at /tmp/tameshi-r45-ExecRows21/S105.raw, S106.raw, S107.raw for the L1 to integrate. Risks: none; all three rows hold and the live bytes match the anchors' pinned sha256 prefixes byte-exact.
