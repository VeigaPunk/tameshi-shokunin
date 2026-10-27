# T51W2Read05 — cold-read re-key

Read candidate `6d8c11e378aa90b12650808e1b79270742935f15` (contract and C1/C2/C3 counters also read from that revision). Exact heading: `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`, `SKILL.md:921-931`; next heading is `### Using the ledger` at 933. Section sha256 (trailing blank removed): `b5dae2b85cd606e8d8db5d34922aa995763428934ea28f728bf372c308c38ebc`.

```json
{
  "heading": "## The leg ledger — replay, receipt, and how it is read (round 7, measured)",
  "seat": "T51W2Read05",
  "read_rev": "6d8c11e378aa90b12650808e1b79270742935f15",
  "section": {"file":"SKILL.md","ranges":[[921,931]],"next_heading":"### Using the ledger (933)","sha256":"b5dae2b85cd606e8d8db5d34922aa995763428934ea28f728bf372c308c38ebc"},
  "pointers": [
    {
      "raw":"tools/mutate-and-run.sh@9f1d3c3:72-109",
      "file":"tools/mutate-and-run.sh",
      "ranges":[[72,109]],
      "revision":"9f1d3c339a7094968041c7708a65dbf7eab9fae6",
      "verdict":"holds",
      "located_excerpt":"Pinned blob lines 72-109 identifies `r7-1 leg ledger`; it lists js-kimi-census 8/10, bash-surface-census 8/10, bash-tsukuroi-census 6/10, bash-mado-verify 4/10 as recorded expectations.",
      "notes":"The pin is a real round-7 commit (2026-10-14)."
    },
    {
      "raw":":511-522",
      "file":"tools/mutate-and-run.sh",
      "ranges":[[511,522]],
      "revision":"9f1d3c339a7094968041c7708a65dbf7eab9fae6 (continuation of preceding citation)",
      "verdict":"holds",
      "located_excerpt":"Pinned blob lines 511-522 contain PIN/REV for JS, bash-surface, tsukuroi, mado and TABLE_JS, TABLE_BASH, TABLE_TSUKUROI, TABLE_MADO. The tables encode 8/10, 8/10, 6/10, 4/10 killed, respectively.",
      "notes":"The re-key targets.json parser classifies this shorthand as file=null/internal line range; the section syntax and adjacent explicit runner citation make the intended runner file and pinned revision clear. The direct runner path is separately traced."
    },
    {
      "raw":":597-620",
      "file":"tools/mutate-and-run.sh",
      "ranges":[[597,620]],
      "revision":"4b7c682 (round-18 runner; contextual qualifier: 'at round 18')",
      "verdict":"holds",
      "located_excerpt":"At 4b7c682, runner lines 597-620 contain the recorded PIN/REV/TABLE assignments through TABLE_SOURCESCHECK, i.e. the round-18 eight-leg tables. At candidate, the same range instead contains the tail of the anchor comments and PIN/REV assignments; current tables are at lines 634-643.",
      "notes":"Historically holds at round 18, but it is not a current-CAND line pointer. The qualifier is essential; a reader following the range in the candidate runner will not land on the tables."
    },
    {
      "raw":"corpus/knowledge/fleet-kill-rate-ledger.md",
      "file":"corpus/knowledge/fleet-kill-rate-ledger.md",
      "ranges":null,
      "revision":"6d8c11e378aa90b12650808e1b79270742935f15",
      "verdict":"holds",
      "located_excerpt":"Candidate file is 437 lines and unchanged from base. Standing rate rows: 1-4 at :45-48; checklist/claims rows 5-6 at :276-277; round-gate row 7 at :410; sources-check row 8 at :432. Its headings call these the seventh (round 16) and eighth (round 18) appended rows; no later rate row is present.",
      "notes":"The eight-row statement holds at CAND. Queue row :119 remains 'unmeasured by sweep; hermetic'; C2's new runner leg did not add a rate row to this knowledge ledger."
    }
  ],
  "strongest_possible_falsifier_checked":"Tested the section's present-tense leg-count progression against the candidate runner. It says 'nine since round 26'; candidate runner says 'r26 nine; r51 ten' at :84, lists ten leg names at :223-226, and asserts ten embedded tuples at :2035-2048. New bash-drift-pins leg has PIN/REV at :632-633, TABLE at :643, wired call at :1504-1508; its table is 2/10 (K_MODE_CMP and K_COUNT_GE killed). Thus the section's progression is stale/incomplete at CAND: it omits the tenth round-51 leg. The old count remains a historical round-26 count, not the current count.",
  "additional_checks": [
    "Runner TMPDIR change: no scratch path, TMPDIR behavior, or runner invocation environment is asserted in this section; the affected usage detail is in the following section, not this heading.",
    "Four panel-tool updates (tally-audit.py, tally-audit-v2.py, tally-audit-v3.py, mte-interop.py): none is cited or named in this section; no pointer here is falsified by those updates.",
    "At candidate runner :597-620 the historical round-18 pointer has moved; current TABLE_* assignments are :634-643. Treating the shorthand as an unqualified CAND pointer would be stale. The historical qualifier was verified against the round-18 runner.",
    "The four kill-rate expectations were checked against the pinned tables; the candidate runner has ten recorded cases and its drift-pins table is 2/10."
  ],
  "rekey_parser_caveat":"The round-51 targets.json records both shorthand ranges `:511-522` and `:597-620` with file=null, resolve_kind=null. This reader manually resolved them from the surrounding sentence and checked the intended runner revisions; the receipt's automatic pointer metadata does not encode that association."
}
```

## Calibration notes

The most material candidate-state falsifier is the unrefreshed count: the prose progression ends at nine while CAND has ten legs. The `:597-620` citation is correct as a round-18 historical pointer but misleading if treated as current runner lines; its current location is not the tables. No TMPDIR or panel-tool claim appears in this section. The eight-row standing-rate statement still holds: the ledger file is unchanged base-to-candidate and contains eight per-gate rate rows, ending with the round-18 sources-check row. No LSP device was available in the provided tool inventory; this task's evidence was Markdown and candidate-blob reads, not caller/definition semantics.
