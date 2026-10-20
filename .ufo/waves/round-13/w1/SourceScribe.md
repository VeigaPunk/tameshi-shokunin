# SourceScribe — tameshi-r13-w1 (read-only evidence scribe)

Seat: TameshiR13.SourceScribe. Scope: open S003 and S041 independently; record quotes, locations, dates; count screened/included/excluded; propose mutable-cell changes. Registry (`corpus/SOURCES.md`) NOT edited.

## Method

- Registry rows read from `corpus/SOURCES.md:14` (S003) and `:50` (S041); status `queued` for both, `used-by` `—` for both.
- Opened each URL twice, independently: (a) reader fetch via `read`; (b) `curl -sSL` into scratch `/tmp/tameshi-r13-sourcescribe/` with `sha256sum`. Both fetches returned HTTP 200 on 2026-10-20 (UTC).
- Located each quote by `grep -o` against the curl body. All quotes ≤25 words.
- No installs or upgrades. Tools used: `read`, `curl`, `sha256sum`, `grep`. Nothing executed from sibling gates; no test, build, lint or formatter run.

| Source | URL | HTTP / bytes | sha256 (curl body, 2026-10-20) |
|---|---|---|---|
| S003 | https://stryker-mutator.io/docs/stryker-js/incremental/ | 200 / 33,898 B | 9054e311a0569231aa2a1427a4137729c8180d7f2687dfd450322e855cc9ad90 |
| S041 | https://pitest.org/quickstart/incremental_analysis/ | 200 / 8,892 B | e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db |

Neither body carries a publication date. The registry's `fetched 2026-10-19` and the body's own content were not contradicted. S041 body has no version string (grep `version` = 0), matching the row's "version not stated".

## S003 — StrykerJS incremental docs

Located quotes (fetched 2026-10-20):

1. §Limitations: "Any other changes to your environment are not detected, such as updates to other files" (15 words). Grep-confirmed.
2. §Limitations: "Stryker will not detect any changes you've made in files other than mutated files and test files." (17 words). Grep-confirmed. Not in the row.
3. §Incremental mode, Note: "The dry run remains required; as it discovers tests, mutation coverage per test" (13 words). Grep-confirmed "The dry run remains required".
4. §Incremental mode, reuse conditions: "A mutant was "Killed"; the culprit test still exists, and it didn't change." (13 words).

Row check (`corpus/SOURCES.md:14`):
- "when a prior verdict may be reused": supported (item 4).
- "env vars, dependencies and .snap files are not detected": supported (item 1; page says "updated (dev) dependencies", "changes to environment variables", "changes to `.snap` files").
- "the dry run stays required": supported (item 3).
- Omitted but relevant to F7: the page's broader scope limit (item 2) — any change outside mutated and test files is undetected. This bears directly on the round-13 claim that identical content is not safe reuse: identical mutated/test file bytes do not capture env, dependency or `.snap` changes, so content identity cannot stand in for environment identity. [INFERENCE for the F7 application; the page states the blind spot, not the F7 conclusion.]
- Page does not state a version for the feature beyond "Available since Stryker 6.2" (body). Row anchor is correct.

## S041 — PIT incremental analysis docs

Located quotes (fetched 2026-10-20):

1. "PIT contains an experimental feature to enable its use on very large codebases" (13 words). Grep-confirmed. Not in the row.
2. §Incremental analysis, after the numbered list: "With the exception of 4), all these optimisations introduce a degree of potential error into the analysis." (19 words). Grep-confirmed "With the exception of 4), all these optimisations introduce a degree of potential error". Matches the row's anchor and the `lessons/round-1.md:391` quote verbatim.
3. Dependency paragraph: "PIT will only consider the strongest of these dependencies - changes to super classes and outer classes" (16 words). Grep-confirmed. Not in the row.
4. Same section: "Although this assumption seems reasonable, it is currently **unproven**." (9 words plus markup). Grep-confirmed "Although this assumption seems reasonable" and "currently <strong>unproven</strong>". Not in the row.
5. Optimisation 5 is marked "*(not yet implemented)*" (grep-confirmed). Optimisation 4 is "(since 1.14.4)", a prioritisation rather than a skip.

Row check (`corpus/SOURCES.md:50`):
- "PIT states that all but one of its reuse optimisations introduce potential error": supported by item 2, read strictly. Caveat: optimisation 5 is "not yet implemented", so the implemented reuse set is 1–3 only. The row's phrasing is not wrong but overstates a live reuse set.
- "reuse of a prior verdict is an inference, not an observation": supported in substance. Page says reuse "can be assumed" / "logically inferred" and the feature's core assumption is "currently unproven" (item 4). The row does not carry the word "unproven" or the "experimental" label; a citing knowledge entry should.
- "page as accessed 2026-10-19, version not stated": consistent with the body.

## Counts (bounded to assignment)

- Screened: 2 (S003, S041). Both opened independently, two methods each.
- Included as support for F7 reuse-discipline claims: 2 (S003, S041), scoped to the limitations and assumptions quoted above. No new rows.
- Excluded: 0.
- Not screened by this seat: S004, S005, S008 (also listed for F7 in `corpus/README.md:84`). Out of assignment; L1 decides.
- Cross-check: `corpus/lessons/round-1.md:362` and `:391` already quote S003 and S041; both quotes match the fetched bodies.

## Proposed mutable-cell changes (NOT applied)

Mutable columns per the round-12 ledger convention (`corpus/lessons/round-12.md:15-18`, `:69-70`): `status`, `recheck`, `used-by`. `id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened` treated as immutable.

- S003: `status` `queued` → `mined`; `used-by` `—` → `<citing knowledge/lesson path, L1 to fill>`; `recheck` `180d` → `180d`.
- S041: `status` `queued` → `mined`; `used-by` `—` → `<citing knowledge/lesson path, L1 to fill>`; `recheck` `90d` → `90d`.

Condition: apply only if a round-13 knowledge or lesson entry with a `source:` line cites the row (QUALITY criterion 10; PROVINCE.md:40-42). If no entry cites them this round, both remain `queued`, and the F7 claim has no admitted source. Tier A is kept in both cases; no tier change proposed.

No change proposed to `teaches`, `anchor`, `scope`, or `opened`. Source-body facts above (e.g., "experimental", "unproven", the S003 scope limit) belong in the citing entry's text, not in the registry's immutable `teaches` cell.

## Checks for L1 to run (not executed here)

1. Re-fetch both URLs and compare sha256 with the table above; a mismatch means the body changed and the quotes need re-locating.
2. `grep -c` each quote in this report against the saved bodies (`/tmp/tameshi-r13-sourcescribe/s003.html`, `s041.html`, scratch only; copy into `.ufo/evidence/round-13/` before any commit that cites them, QUALITY criterion 9).
3. Registry validation: the round-12 closure ran `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` against `corpus/SOURCES.md`. Run it after the mutable-cell edits, if applied.
4. `git diff -- corpus/SOURCES.md` should show only status/used-by/recheck cells on S003 and S041 changed (and an appended search-log note if written).
5. LOG.md entry for any registry change (AGENTS.md: every change appends a LOG entry with motivating evidence).
6. If a knowledge entry cites S003/S041, check its `source:`, `verified-at:`, `recheck:` headers (QUALITY criterion 10) and that the citing file exists in `corpus/knowledge/`.
7. Path note: `corpus/SOURCES.md` header points to `SOURCES-CONTRACT-v1.md`. That file is not in the tameshi repo; it exists at `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`. Not opened in full by this seat; mutable-field list above is inferred from the round-12 ledger usage. [INFERENCE]

## Out of scope / not done

- No registry, LOG, QUALITY, knowledge, or lesson edits.
- No sibling gate executed.
- No new sources opened beyond S003 and S041.
