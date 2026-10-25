# ReviewD29 — r3-snapshot-fixture-update-paths.md

## Verdict: NO ATTACK — gate condition unmet (D29 *is* the title it quotes)

Attack condition was "if D29 is not the title it quotes." The entry quotes D29's
title cell and nothing else; byte-for-byte verified.

## Evidence

| Check | Command / path:line | Observed |
|---|---|---|
| Quoted title | `corpus/knowledge/r3-snapshot-fixture-update-paths.md:10` | `Row D29's title cell is "Snapshot Testing: Use With Care - Randy Coulman"` |
| Pinned snapshot row | `.ufo/evidence/round-40/sources/s132-readme.md:33` | `|D29|Snapshot Testing: Use With Care - Randy Coulman|https://randycoulman.com/blog/2016/09/06/snapshot-testing-use-with-care/|` — identical cell text |
| Snapshot sha | `sha256sum .ufo/evidence/round-40/sources/s132-readme.md` | `8871d19c34165b60b5847f390955c247d8665758ecddb206448127bf3b1922ea` — matches source-line pin and registry `sha256 8871d19c` |
| Live artefact | `curl -sSL https://raw.githubusercontent.com/VictorGazzinelli/snapshot-testing/master/README.md` → `/tmp/tameshi-r40-ReviewD29/live-readme.md` | sha256 `8871d19c34165b60b5847f390955c247d8665758ecddb206448127bf3b1922ea` — identical to pinned snapshot; D29 row identical. `opened 2026-10-24` and raw-README artefact claims hold |
| Register mark | `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:224` | `tameshi | round3 | S132 | payload-absent | ...` — doc's "register had marked S132 payload-absent" holds |
| used-by path | `corpus/SOURCES.md:121` | `used-by: corpus/knowledge/r3-snapshot-fixture-update-paths.md` — file exists at that path |

## Residual nits (below attack threshold)

- `r3-snapshot-fixture-update-paths.md:10`: "That 7-word title" counts the ` - Randy Coulman` author suffix as title tokens. The bare blog title is 5 words. Quote itself is byte-exact; word-count label only is loose. Same phrasing in `corpus/lessons/round-40.md:21`.
- "primary document" (`:6`, and registry `the table names Snapshot Testing: Use With Care among its primary documents`): the README table is a flat `|Id|Title|Url|` list with no primacy ranking (`s132-readme.md:3-4`). Mild editorialization, not a misquote.
- Filename promises "fixture-update-paths"; content is a README document-table anchor. Cosmetic misnomer; citation target still resolves.

## Verification gaps

- Doc's side claim that the GitHub *HTML* page contains the title "as escaped markup" not re-fetched; non-load-bearing (doc itself designates the raw README as the pinned artefact, which was byte-verified live).
- No edit made to lane checkout, shokuknow, or contract.json. Tools: none installed.
