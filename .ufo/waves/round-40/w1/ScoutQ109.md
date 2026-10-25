# ScoutQ109 — Quarantine S109 (tameshi, round1)

## Row under check

- Register row: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:216`
  `tameshi | round1 | S109 | payload-absent | https://doi.org/10.21105/joss.01891 | "Property-based testing is a style of testing popularised by the QuickCheck family of libraries, first in Haskell and lat" | cited source, companion URLs and local artifacts were all checked; the quote is in none of them`
- Original linted record: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/quote-lint-full-v5.json`
  full quote: `"Property-based testing is a style of testing popularised by the QuickCheck family of libraries, first in Haskell and later in Erlang"` — a `§Abstract` gate quote, verdict ABSENT, `binding: "id"`.
- ID drift: in current `merge/tameshi/SOURCES.append.md` and `lanes/tameshi/SOURCES-PROPOSED.md` this source is **S113** (id remapped; S109 now names a POSIX `diff` row — a different sibling ticket). The quarantined quote is still live at `lanes/tameshi/SOURCES-PROPOSED.md:69` and `KNOWLEDGE-PROPOSED.md:387`.

## Fetches (2026-10-24, scratch `/tmp/tameshi-r40-ScoutQ109/`)

- `curl -fsSL -A 'Mozilla/5.0' 'https://doi.org/10.21105/joss.01891'` → 200, resolves to `https://joss.theoj.org/papers/10.21105/joss.01891`, 20,076 bytes. Landing page contains **no abstract body** — only title, metadata, citation block, tags. `grep -c 'QuickCheck family'` → **0**. The linter's ABSENT on this URL is mechanically correct.
- `curl -fsSL 'https://joss.theoj.org/papers/10.21105/joss.01891.pdf'` → 200, 128,906 bytes. `pdftotext` → 8,947 bytes.
  - `paper.txt:25` — **"Property-based testing is a style of testing popularised by the QuickCheck family of libraries,"**
  - `paper.txt:26` — **"first in Haskell (Claessen & Hughes, 2000) and later in Erlang (Arts, Hughes, Johansson, & Wiger, 2006),"**

## Finding — a quote is LOCATED, so this row is adopt-eligible, not a fabrication

The quoted sentence is the opening sentence of the paper's Summary. It is real and authoritatively attributed to the cited paper. Two linter blind spots produced the ABSENT, neither is a lane defect:

1. **Companion-URL gap.** The gate cites `https://doi.org/10.21105/joss.01891`, which resolves to the JOSS landing page — no abstract. The sentence lives in the paper PDF (`…/joss.01891.pdf`, advertised as `citation_pdf_url`). `quote-lint.py:192` `companion_urls()` adds a `_pdf/` companion only for J-STAGE-style `_article/` URLs; a DOI→JOSS landing page gets no PDF companion, so the PDF was never checked.
2. **No citation-strip fold.** In the PDF the sentence carries an inline citation between "Haskell" and "and": `first in Haskell (Claessen & Hughes, 2000) and later in Erlang`. The gate quote omits the parenthetical. `FOLD_NAMES` (quote-lint.py:636) = exact, whitespace, case, no-whitespace, markdown, nfkc, typographic, c-escape, de-wrapped, html, md-link — none removes `(...)`. After stripping parenthetical citations, the quote is present verbatim (scratch check: `True`).

Verbatim contiguous span in the cited DOI's own text: absent. Present with a parenthetical inset in the same paper's PDF (the DOI's own publication artefact). The excerpt-normalisation gap is the lint's, not the lane's.

## Verdict

**Present — adopt-eligible.** The `payload-absent` classification for tameshi round1 S109 does not hold up under hand-check: the quote is found in the paper the DOI resolves to (PDF artefact), modulo an inline citation and a companion-URL gap in the linter. Recommendation: keep the row (now numbered S113 in SOURCES.append), and if strict verbatim-against-cited-URL is the bar, the fix is adding the PDF URL to the gate block or a citation-strip fold in the linter — not refusing the row.
