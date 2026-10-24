# W2ScoutS103Quote — S103 Gate quote location + word-count check (round 36, w2)

**Verdict: quote VERIFIED verbatim (modulo a source line-wrap); the <=25-word claim HOLDS at 18 words —
but the lesson's own "(19 words)" annotation and "first sentence" label are both wrong.**

## Attacked
The `## Gate` entry in `corpus/lessons/round-36.md:36-38` claims: quote
"Computes the object ID value for an object with specified type with the contents
of the named file", located at "§DESCRIPTION first sentence", annotated "(19 words)",
in committed snapshot `.ufo/evidence/round-36/src/s103-git-hash-object.html`.

## Observed (all from committed bytes at lane tip, snapshot sha256
`dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100`, 29,933 bytes —
matches contract `new_source_row`)

| Item | Value |
|---|---|
| Exact location | `.ufo/evidence/round-36/src/s103-git-hash-object.html`, lines **1607–1608** |
| Byte offset of `Computes` | **25436** (line 1607 starts at 25433; text follows `<p>` at 25436) |
| Wrap point | `...specified type\nwith the contents...` — newline at end of line 1607; `with` resumes at byte **25499** (line 1608) |
| Strict contiguous byte match of full quote | **-1 (absent)** — the HTML hard-wraps mid-quote; verbatim only under whitespace normalization (newline→space) |
| Word count of quoted text | **18** (≤ 25 → bound holds) |
| Full first sentence | runs to line 1610: `...(which can be outside of the work tree), and optionally writes the resulting object into the object database.` — the quote is the sentence's 18-word **prefix**, not the whole ~36-word sentence |

Context (snapshot lines 1606–1610):
```
1606 <div class="paragraph">
1607 <p>Computes the object ID value for an object with specified type
1608 with the contents of the named file (which can be outside of the
1609 work tree), and optionally writes the resulting object into the
1610 object database.  Reports its object ID to its standard output.
```

## Findings
1. **Quote present and verbatim** under whitespace normalization; in raw bytes it
   contains a `\n` where the lesson renders a space. The lesson's own rendering is
   also line-wrapped, so both sides agree only normalized. (Calibration note:
   "character-for-character" is strictly false at the byte level.)
2. **`<=25 words`: holds.** 18 words ≤ 25.
3. **Lesson annotation "(19 words)" is off by one** — recount: `Computes(1) the2
   object3 ID4 value5 for6 an7 object8 with9 specified10 type11 with12 the13
   contents14 of15 the16 named17 file18` → 18. Corroborates w1 `ScribeGateAudit` F1.
4. **"§DESCRIPTION first sentence" is a mislabel** — the quoted text is the
   sentence's opening 18 words; the sentence continues 18 more words to
   `...object database.` at line 1610. Corroborates w1 `ScribeGateAudit` F2 /
   `SimplifierReceiptDupes` C4.
5. Other Gate fields (URL, snapshot path, sha256) confirmed consistent here only
   for the digest/path; URL was not re-fetched (network out of scope).

## Commands run (read-only)
- `grep -n "Computes the object ID value" .ufo/evidence/round-36/src/s103-git-hash-object.html` (via grep tool)
- `read` `corpus/lessons/round-36.md:28-45`, contract.json
- `python3` one-off: `open(snapshot,'rb')` → `sha256`, `bytes.find` for the literal
  prefix (25436) and full normalized quote (-1), per-line start offsets, `split()`
  word count. Lane rev: working tree at tip `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`
  (per w1 RevengerContractFreeze); file unchanged since commit `e423c41b`.

## Confidence
High on all location/count facts (direct byte offsets from the committed,
hash-pinned snapshot). No unresolved unknowns within scope.

## Tools installed
None.
