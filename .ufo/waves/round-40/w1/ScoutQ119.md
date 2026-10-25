# ScoutQ119 — Quarantine hand-check: tameshi S119

## Verdict: PRESENT — adopt-eligible; `payload-absent` is a two-column extraction artifact, not a fabrication

## Register row
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:219`
  `tameshi | round2 | S119 | payload-absent | https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf | It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappea[r]`

## ID resolution
- tameshi `round2 | S119` was remapped to `S123` at merge: `/home/vgpnk/Projects/shokuknow/lanes/tameshi/ID-REMAP.md:64` (`round2 | S119 | S123`).
- The merged row `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:21` (S123) cites the same URL — Zeller & Hildebrandt, *Simplifying and Isolating Failure-Inducing Input*, IEEE TSE 28(2):183-200.
- Gate block with the flagged quote: `/home/vgpnk/Projects/shokuknow/lanes/tameshi/round2/SOURCES-PROPOSED.md:38`.
- Note: `SOURCES.append.md:17` row `S119` is a different document (Huawei cloudtest page) — a post-remap id, not this register row's source.

## Hand check
```
curl -fsSL 'https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf' -o /tmp/tameshi-r40-ScoutQ119/delta-debugging.pdf
# HTTP OK, 247 738 B (matches the lane's recorded fetch size), PDF 1.2, 17 pages
# sha256: 7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa
pdftotext delta-debugging.pdf dd.txt
```
`dd.txt:68-70`:
```
algorithm ddmin is fed with a failing test case, which it simplifies by successive testing. It stops when a minimal test case
is reached, where removing any single input entity would cause
the failure to disappear.
```
Whitespace-folded substring check: **True** — the quoted span is verbatim in §I Introduction (the sentence sits on the article's first page, journal p. 183; the gate locator says p. 184 — off by one page, but the section is right).

## Why the checker missed it
The checker's own cached extraction `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ee097fd52aa6baaf89e799d1.txt` interleaves the PDF's two columns line-by-line:
```
algorithm ddmin is fed with a failing test case, which it sim-
                                                                                  plifies by successive testing. It stops when a minimal test case
   F you browse the Web with Netscape 6, you actually use                         is reached, where removing any single input entity would cause
   a variant of Mozilla, Netscape’s open source web browser                       the failure to disappear.
```
The span is never contiguous in that dump, so it fails under every fold — including `no-whitespace`. Absence is a fold artifact of the cached two-column extraction, not of the source.

## Decision
- Quote present in the cited source → **adopt-eligible**.
- Not refused; fabrication class does not apply.
- Register not edited (per instructions; shokuknow is read-only).
- Minor locator nit (outside the predicate): §I is correct; the page should read p. 183, not p. 184.

## Notes
- No tools installed; `curl` + system `pdftotext` sufficed. No pacman run (transactions paused).
- Scratch dir: `/tmp/tameshi-r40-ScoutQ119/`.
