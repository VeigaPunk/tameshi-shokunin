# CensusNoHarm — round 19 attempt 1

## Axes
- **Census integrity:** independent registry row, tier, status, and malformed-row counts.
- **No-harm/admission boundary:** no registry edits or unsupported new-source admission.

## Independent census
Source: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`, `## Registry` table. Command: an inline `awk -F'|'` pass selecting only `^\| S[0-9]{3} ` rows, tallying tier field `$5` and status field `$9`, and checking structure and required metadata.

Observed:

| Measure | Count |
|---|---:|
| Registry rows | 76 |
| Tier A / B / C | 67 / 7 / 2 |
| Status mined / queued / rejected | 48 / 23 / 5 |
| Malformed rows | 0 |
| Duplicate IDs / wrong field counts / mined rows with missing used-by | 0 / 0 / 0 |

Malformed check: each selected row had the expected 13 awk fields for an 11-column Markdown row with leading/trailing delimiters, a unique `Sddd` ID, nonempty data cells, tier in A/B/C, status in mined/queued/rejected, `opened` in YYYY-MM-DD form, `recheck` as `Nd` or `on-release`, and a used-by value (mined rows were not `—`). These are my explicit row-structure checks, not a fresh run of the fleet validator. ID coverage is S001–S037 and S040–S078; SOURCES.md `## Id allocation` explicitly says S038–S039 were retired and never written, so that intentional gap is not a malformed row. S079 is the current next-unused ID.

The existing `.ufo/evidence/round-19/census-start.txt:1-10` records the official census command and exit 0 at round start, with six W04 duplicate-URL warnings (S047, S048, S075–S078). Those URL-identity warnings are distinct from malformed-row checks; I did not rerun that validator.

## No-harm / new-row decision
No new row is warranted by the round-19 source record: `corpus/lessons/round-19.md:27-40` records that S049 was reopened on 2026-10-21, its existing row gained the round-19 `used-by`, and other openings were advisory rather than admissions. The lesson states: “No new source rows or tier changes; no frontier ground moved.” S049 already exists in the registry; no additional row or tier change is indicated.

This seat read registry/lesson evidence and made no production edits, installs, or test/build/lint/formatter runs.