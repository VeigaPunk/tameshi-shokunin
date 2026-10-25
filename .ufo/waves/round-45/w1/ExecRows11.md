seat: ExecRows11

# Round-45 w1 — C1 row re-verification: S066, S068, S077 (author)

All three rows fetched live 2026-10-25, extracted via round-45 freshness `--extract`, quotes
located afresh in the live bytes (not copied from row cells), and each fragment passed the
frozen-rev `--check` as `verified`. No tools installed (used existing python3/curl); no
tooling changes to record.

## S066 — RFC 8259 (JSON number grammar)

- URL: `https://www.rfc-editor.org/rfc/rfc8259`
- curl: `curl -fsSL -A 'Mozilla/5.0' --max-time 90` → exit 0
- bytes: 243776; sha256: `6fd09811202d477f54aa65ef3f3e9d4caba2cf6ab4ab8b235b2ca774da419f4c`
- CHECK: `CHECK S066 verified ok` (exit 0)
- note: §6 Numbers sentence before the `number` grammar still says numeric values the
  grammar cannot represent (such as Infinity and NaN) are not permitted, exactly grounding
  the teaches that NaN/Infinity are outside the JSON number grammar.
- raw kept at `/tmp/tameshi-r45-ExecRows11/S066.raw`

```json
{"id":"S066","url":"https://www.rfc-editor.org/rfc/rfc8259","opened":"2026-10-25","verdict":"holds","raw_sha256":"6fd09811202d477f54aa65ef3f3e9d4caba2cf6ab4ab8b235b2ca774da419f4c","quote":"Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted.","snapshot":".ufo/evidence/round-45/freshness/sources/S066.raw.gz","author":"ExecRows11","note":"§6 Numbers sentence before the number grammar still says numeric values the grammar cannot represent (such as Infinity and NaN) are not permitted, exactly grounding the teaches that NaN/Infinity are outside the JSON number grammar."}
```

## S068 — PR_SET_CHILD_SUBREAPER(2const) (reparenting rule)

- URL: `https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html`
- curl: `curl -fsSL -A 'Mozilla/5.0' --max-time 90` → exit 0
- bytes: 9879; sha256: `b805fe23c7251ad6c3d08a829ed755b80a8fa106929c67325c7122f3b126ef2c`
- CHECK: `CHECK S068 verified ok` (exit 0)
- note: the live man-pages 6.19 page still states the reparenting rule in DESCRIPTION: an
  orphaned process is reparented to the nearest still living ancestor subreaper, grounding
  the teaches verbatim.
- raw kept at `/tmp/tameshi-r45-ExecRows11/S068.raw`

```json
{"id":"S068","url":"https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"b805fe23c7251ad6c3d08a829ed755b80a8fa106929c67325c7122f3b126ef2c","quote":"When a process becomes orphaned (i.e., its immediate parent terminates), then that process will be reparented to the nearest still living ancestor subreaper.","snapshot":".ufo/evidence/round-45/freshness/sources/S068.raw.gz","author":"ExecRows11","note":"The live man-pages 6.19 page still states the reparenting rule in DESCRIPTION: an orphaned process is reparented to the nearest still living ancestor subreaper, grounding the teaches verbatim."}
```

## S077 — PR_SET_CHILD_SUBREAPER(2const) (anchor supersede)

- URL: `https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html`
- curl: `curl -fsSL -A 'Mozilla/5.0' --max-time 90` → exit 0
- bytes: 9879; sha256: `b805fe23c7251ad6c3d08a829ed755b80a8fa106929c67325c7122f3b126ef2c`
- CHECK: `CHECK S077 verified ok` (exit 0)
- note: the live page's DESCRIPTION paragraph after the "If set is nonzero" opening still
  begins "A subreaper fulfills", confirming the reparenting quote sits in ¶2 as the anchor
  claims (shares "subreaper" + "fulfills" with the anchor cell).
- raw kept at `/tmp/tameshi-r45-ExecRows11/S077.raw`

```json
{"id":"S077","url":"https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"b805fe23c7251ad6c3d08a829ed755b80a8fa106929c67325c7122f3b126ef2c","quote":"A subreaper fulfills the role of init(1) for its descendant processes.","snapshot":".ufo/evidence/round-45/freshness/sources/S077.raw.gz","author":"ExecRows11","note":"The live page's DESCRIPTION paragraph after the 'If set is nonzero' opening still begins 'A subreaper fulfills', confirming the reparenting quote sits in ¶2 as the anchor claims."}
```

## Verdicts

All three rows: `holds`, CHECK lines `verified ok`. No `drifted`/`unreachable` cases.
Raw bytes for all three remain in `/tmp/tameshi-r45-ExecRows11/` (S066.raw, S068.raw,
S077.raw, plus the fragment JSONs) for the L1's integration (committed snapshots under
`.ufo/evidence/round-45/freshness/sources/`).
