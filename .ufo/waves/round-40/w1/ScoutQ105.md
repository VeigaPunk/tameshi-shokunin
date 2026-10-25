# ScoutQ105 — Quarantine hand-check: tameshi S105

## Verdict: ADOPT-ELIGIBLE — quote present; `payload-absent` is a fold-mismatch false positive

## Register row
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:215`
  `tameshi | round1 | S105 | payload-absent | https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html | 0 No differences were found. 1 Differences were found. >1 An error occurred.`

## URL cited for the id
The append file carries no literal `S105` row: tameshi round1 `S105` was remapped to `S109`
(`/home/vgpnk/Projects/shokuknow/lanes/tameshi/ID-REMAP.md:13`), and
`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:7` (row S109) cites the same URL —
`https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html`, POSIX `diff` (Issue 7, 2018 ed.).

## Hand check
```
curl -fsSL 'https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html' -o /tmp/tameshi-r40-ScoutQ105/diff.html
# 33988 bytes, HTTP OK
grep -c 'No differences were found' diff.html   # → 1
```
The fetched page's §EXIT STATUS is a definition list:
```html
<dt>&nbsp;0</dt><dd>No differences were found.</dd>
<dt>&nbsp;1</dt><dd>Differences were found.</dd>
<dt>&gt;1</dt><dd>An error occurred.</dd>
```
Under tag-strip + entity-unescape + whitespace-collapse the quoted span matches verbatim:
```
'The following exit values shall be returned: 0 No differences were found. 1 Differences were found. >1 An error occurred. CONSEQUENCES OF ERRORS ...'
QUOTE PRESENT (folded): True
```
The quote is a faithful whitespace-fold of three consecutive `<dt>/<dd>` pairs — no wording
alteration, no paraphrase. The register's `payload-absent` classification does not survive a
standard normalization hand-check; it is a checker fold artifact, not a fabrication.

## Decision
- Quote present in the cited source → **adopt-eligible**.
- Not refused; fabrication class does not apply.
- Register not edited (per instructions and shokuknow read-only bound).

## Notes
- The companion row `S109` in SOURCES.append.md already prescribes the same source with recheck
  string `No differences were found` (expect 1) — consistent with this finding.
- No tools installed; curl+python3 stdlib sufficed. No pacman run (transactions paused).
