# T50ScribePkgDD — receipts (assimilation triage, theme F6)

Scratch root `/fast/scratch/hyaku/tameshi-r50/T50ScribePkgDD` (deleted at exit; the pinned bytes and the
extract live beside this file under `.ufo/waves/round-50/w1/T50ScribePkgDD.src/`).

## R1 — fetch of the document the package cites as S167

```
curl -fsS -w '%{http_code} %{size_download}' -o delta-debugging.pdf \
  'https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf'
```
→ `200 247738`; `sha256sum` → `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa`

```
pdfinfo delta-debugging.pdf
```
→ `Pages: 17`, `Page size: 595 x 842 pts (A4)`, `Producer: GNU Ghostscript 5.50`,
`CreationDate: Thu Dec 20 06:50:05 2001 -02`

Mirror pagination (printed page numbers are the mirror's own, not the journal's):

```
pdftotext -layout -f 1  -l 1  delta-debugging.pdf - | sed -n '1p'
  IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002   1
pdftotext -layout -f 2  -l 2  delta-debugging.pdf - | sed -n '1p'
  2                                        IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002
pdftotext -layout -f 17 -l 17 delta-debugging.pdf - | sed -n '1p'
  ZELLER AND HILDEBRANDT: SIMPLIFYING AND ISOLATING FAILURE-INDUCING INPUT   17
```

## R2 — the package's own `recheck:` command, run against the live bytes

```
curl -fsSL 'https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf' | grep -c 'minimal test case'
```
→ stdout `0`, exit `1`. The PDF stream is compressed, so a raw-byte grep cannot see the text.

Replacement, tested (also against the committed text extract):

```
curl -fsSL 'https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf' \
  | pdftotext - - | tr -s ' \n' ' ' | grep -c 'removing any single input entity'
```
→ stdout `1`, exit `0`.

```
curl -fsSL 'https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf' \
  | pdftotext - - | tr -s ' \n' ' ' | grep -c 'After 57 test runs'
```
→ stdout `1`, exit `0`.

## R3 — located quotes, `grep -n` over `T50ScribePkgDD.src/delta-debugging.txt` (`pdftotext -layout`)

| what | lines | text |
|---|---|---|
| Abstract, case-study cost | 18-20 | `it simplified 896 lines of HTML to the single line that caused the failure. The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC.` |
| §I, ddmin definition | 30-33 | `algorithm ddmin is fed with a failing test case, which it sim- plifies by successive testing. It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappear.` (the break inside `sim- plifies` is the PDF's hyphenation) |
| §I, the same 896-line reduction, with its own count | 54-57 | `After 57 tests, the original 896-line HTML input is reduced to the minimal failing test case <SELECT>.` |
| §IV-B, Fig. 12 | 891-892 | `...ter 57 test runs, the ddmin algorithm minimizes the original 896 lines to a 1-line input` (first word split by the two-column layout) |
| Definition 10 | 350 | `Definition 10 (n-minimal test case) ...` |
| Proposition 11 | 562 | `Proposition 11 (ddmin minimizes) ... is 1-minimal in the sense of definition 10.` |
| §V, conflicting count | 1153 | `while minimizing (Figure 2) required 26 tests.` |

`grep -n '139' delta-debugging.txt` → line 19 only. No section other than the Abstract states 139.

## R4 — id collision check (0-3-space row pattern, as round 47/49 ran it)

Script (python3, read-only over both trees; lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`,
package `/home/vgpnk/Projects/shokuknow/merge/tameshi`):

```
reg = ids matched by ^ {0,3}\|\s*(S\d{3,})\s*\|  in corpus/SOURCES.md
staged = S-ids on `source:` lines and on staged rows in SOURCES.append.md + knowledge/corpus/knowledge/*.md
```
→ `reg-ids 130 staged-ids 111 collisions 9`
→ `collisions: S026,S153,S154,S155,S156,S157,S158,S159,S160`
→ `S167 in reg rows: False | S167 in staged: True`
→ `S271 in reg: False | max reg S270`
→ `id-space test: 2-space row accepted: True`

## R5 — lane anchors cited by the report

```
grep -n "B5 probe fixture size" corpus/README.md            → 83
grep -n "F6 (fixture minimization" corpus/README.md         → 440
grep -n "survivor-fixture-minimization.md" corpus/README.md → 482
grep -n "F10's next move is now" corpus/README.md           → 599
grep -n "1-minimal" corpus/knowledge/survivor-fixture-minimization.md → 16,34,35
grep -n "ddmin made" corpus/knowledge/survivor-fixture-minimization.md → 53
grep -n "Next unused id" corpus/SOURCES.md                  → 490,495,499
grep -n "stays a" corpus/SOURCES.md                         → 184 (Zeller lead stop rationale)
grep -n "Zeller & Hildebrandt" corpus/SOURCES.md             → 184,278
grep -n "held (round 50)" corpus/README.md                  → (no match at base; C2's landing adds it)
```

## R6 — tools

No install or upgrade was made (host pacman guard paused; nothing needed).
`curl 8.23.0`, `pdftotext 26.08.0` (poppler), `Python 3.14.8`.

## R7 — reading-order extract: the hyphen fold is `-layout`-specific, and the cost decomposition

```
pdftotext delta-debugging.pdf delta-debugging.reading-order.txt
sha256 2157fadf4f0c45151a5fa6bee89e839fb6cec81ce2034f110cedb1762a412145, 4,227 lines
```

| what | reading-order line | text |
|---|---|---|
| Abstract | 13-14 | `Likewise, it simplified 896 lines of HTML to the single line that caused the failure. The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC.` |
| §I, ddmin definition | 68-70 | `algorithm ddmin is fed with a failing test case, which it simplifies by successive testing. It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappear.` (unbroken here; the `-layout` extract hyphen-folds `sim-/plifies` at :30-31) |
| §IV-B, Fig. 11 (the 95-user-action run) | 2105-2106 | `After 82 test runs (or 21 minutes), only 3 out of 95 user actions are left:` |
| §IV-B, Fig. 12 (the HTML line run) | 2124 | `After 57 test runs, the ddmin algorithm minimizes the original 896 lines to a 1-line input` |
| §V-A (the line→`<SELECT>` run) | 2890 | `Figure 2 shows how ddmin simplifies the failure-inducing HTML line presented in Section IV-B: After 26 steps, the line is reduced to the single <SELECT> tag.` |

Decomposition: `82 + 57 = 139` — the Abstract's total is the user-action run plus the HTML line run. The
per-reduction counts are 82 (21 minutes) and 57; no per-reduction wall-clock is printed for the 57-run
figure (35 − 21 = 14 minutes is arithmetic, not a quote).

Independent corroboration: seat T50ExecSrcZeller fetched the same URL and reported the same sha256, byte
count and 17-page mirror, and the same `grep -c 'minimal test case'` → 0 on raw bytes
(`.ufo/waves/round-50/w1/T50ExecSrcZeller/`). It states it is not opening a registry row.
