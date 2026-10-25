# ReopenS157 — round 42, wave 2 (FALSIFY)

Seat: `L1Tameshi42.ReopenS157` (scout, read-only). Attacked thing: the S157 row and every S157-attributed quote. Accessed 2026-10-25. No tools were installed or updated.

## Findings

1. **The live page matches the snapshot byte for byte. SURVIVES.**
   `D=$(mktemp -d /tmp/tameshi-r42w2-ReopenS157-XXXX); curl -fsSL -m 60 -o $D/python-argparse.html https://docs.python.org/3/library/argparse.html; sha256sum $D/python-argparse.html .ufo/evidence/round-42/sources/python-argparse.html`
   → rc=0, both `3158c439e504752c93f582ddec59483a75c890411c1d3ee3b733125950bf93b7`, both 2722 lines / 328434 B. The size, the sha256 prefix and the full sha256 match what the S157 row and the entry's `source:` header record. The snapshot `<title>` says "Python 3.15.1 documentation", as the row says.

2. **The S157 row is well formed. SURVIVES.** It is at `corpus/SOURCES.md:127`.
   - Parsing the line with `r[1:-1].split('|')` gives 11 cells, and `awk -F'|' 'NR==127{print NF}'` gives 13. The row has no escaped `\|` and no pipe inside a cell.
   - The cells are: id `S157`; title+URL; `docs`; `A`; why; anchor; teaches; `mined`; `2026-10-25`; `180d`; used-by `corpus/knowledge/r42-attribute-and-outflag-destinations.md`.
   - **Anchor** "§dest and §The parse_args() method": `id="dest"` is at snapshot :1490, and `id="the-parse-args-method"` is at :1645.
   - **Teaches** "dest is normally inferred from the option strings and internal dashes become underscores; parse_args assigns the converted values as namespace attributes and returns the namespace" is a faithful paraphrase of :1504–1505, :1512–1514 and :1650–1651.
   - **Used-by**: the file exists (6947 B). Its `source:` line 1 cites S157, and the `corpus/SOURCES.md:446` note agrees with it ("S157/S158 → …r42-attribute-and-outflag-destinations.md").
   - `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, `ok`, and no code mentions S157. The only codes are the W04 and W01 rows that were already there (S047…S104).

3. **Where S157 is attributed** (`grep -n S157` across the three named files):
   - `corpus/knowledge/pit-outcome-vocabulary.md`: no S157 attribution, so there are no quotes to check.
   - `corpus/lessons/round-42.md:76`: "S157 and S158 are new rows, not from the package." This is a provenance note, not a quote. The only other argparse mention, at :172, is "`parse_args` only", a scope note.
   - `corpus/knowledge/r42-attribute-and-outflag-destinations.md`: three quotes at :13–20. Line :42 ("dest is derived as S157 states") is a paraphrase.

4. **Each quote**, checked with a Python script against the snapshot. The script strips tags, unescapes HTML entities and normalises whitespace, then looks for the quote in the cited line span and in the whole page:

   | # | entry line | quote (abridged) | verbatim | ≤25 words | cited snapshot lines | actual lines | claimed count | actual count |
   |---|---|---|---|---|---|---|---|---|
   | Q1 | :13–14 | "For optional argument actions, the value of dest is normally inferred from the option strings." | yes (1 occurrence) | yes | 1504–1505 | 1504–1505 ✔ | 15 | 15 ✔ |
   | Q2 | :14–16 | "Any internal - characters will be converted to _ characters to make sure the string is a valid attribute name." | yes (1 occurrence) | yes | **1513–1514** | **1512–1514** ✘ | **19** | **20** (split on whitespace) / 18 (not counting `-` and `_`) ✘ |
   | Q3 | :19–20 | "Convert argument strings to objects and assign them as attributes of the namespace. Return the populated namespace." | yes (1 occurrence) | yes | 1650–1651 | 1650–1651 ✔ | **14** | **17** ✘ |

   - Q2: the cited span 1513–1514 does not contain the quote (`verbatim-in-cited-span False`). Its first word, "Any", ends snapshot line 1512: `…by stripping the initial <code…>-</code> character.  Any`. The claimed count of 19 matches neither counting rule.
   - Q3: Convert(1) argument strings to objects and assign them as attributes of the(12) namespace(13). Return the populated namespace(17). The page has a double space after "namespace."; the quote normalises it to one space, which is acceptable.
   - All three quotes are under the 25-word cap, so the miscounts do not break the cap.

## Verdict

BROKEN: in `corpus/knowledge/r42-attribute-and-outflag-destinations.md`, Q2 (:14–16) cites snapshot lines 1513–1514, but the quote spans 1512–1514, and its count of 19 is really 20 (18 without `-`/`_`). Q3 (:19–20) claims 14 words, but has 17. The snapshot hash, the live re-fetch, the S157 row, its anchors, its teaches cell, its used-by file, and all three quotes' wording and 25-word cap hold.
