# E03R19Verifier — round-19 routed defects 1–3

## Scope and authority

Read-only review of `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-19-verifier-spotcheck.md`. The authoritative routed-defect text is at lines 164–175. The lesson identifies these as fixes routed to round 20, “append-only fixes, never rewrites.”

## Findings

### 1. QUALITY20 recurrence

**Verbatim item** (lesson lines 166–169):

```text
1. **QUALITY20 recurrence** (second occurrence after the round-16 one QUALITY21 records): stage instrument changes at a
   separate path *before* dispatch and install only after the wave returns; add a receipt-time check that a receipt's
   instrument sha lies outside any edit interval (e.g. record frozen and installed shas and refuse a receipt whose sha
   is neither).
```

**Requested fix:** Stage instrument changes at a separate path before dispatch; install them only after the wave returns; gate receipts at receipt time against the edit interval, recording frozen and installed instrument SHAs and refusing a receipt whose SHA matches neither.

**Evidence pointer cited by the item:** “the round-16 one QUALITY21 records.” The routed item supplies no exact filename, section, line, or receipt path for that prior occurrence. The exact source location for this routed instruction is `corpus/lessons/round-19-verifier-spotcheck.md:166-169`.

**Agreement / discrepancy:** Agree that the wording routes this recurrence fix to round 20. The specific round-16 evidence pointer is underspecified in the cited item; I have not inferred a filename or line.

### 2. Wording precision on the three executor probes

**Verbatim item** (lesson lines 170–173):

```text
2. **Wording precision on the three executor probes**: the three receipts pin three different instruments
   (`96a68b60…` round-19 ruler, `8dfaa25a…`/`d22c4025…` witness tool/runner, `7ca87a7c…` round-18 measure); the
   lesson's singular "the frozen SHA" should name each instrument's sha so it is not read as all three pinning
   `bb651eef…`.
```

**Requested fix:** Replace the ambiguous singular “the frozen SHA” with the SHA for each of the three distinct instruments, so the receipts are not misrepresented as all pinning `bb651eef…`.

**Evidence pointers cited:** The item itself gives the abbreviated instrument SHAs `96a68b60…`, `8dfaa25a…`, `d22c4025…`, `7ca87a7c…`, and the contrasting frozen-ruler SHA `bb651eef…`. The same lesson maps those instrument identities to these exact relative pointers at lines 112–115: `w1/ReceiptDesign.md` (round-19 ruler), `w1/ReceiptFields.md` (witness tool/runner), `w1/RevisionBinding.md` (round-18 measure), and `w2/FRevisionBinding.md` (wave-2 frozen check / `bb651eef…`). These pointers are quoted as printed; the lesson does not expand them to a full directory path here.

**Agreement / discrepancy:** Agree with the distinction the routed item makes between the three probe instrument SHAs and the wave-2 frozen ruler SHA. The requested wording correction is clear.

### 3. S049 opened-date basis

**Verbatim item** (lesson lines 174–175):

```text
3. Keep the S049 opened-date basis explicit (row `2026-10-20` local vs lesson "reopened 2026-10-21" UTC) so the
   lesson and the census do not read as contradictory; no row change is required.
```

**Requested fix:** State the date basis explicitly to reconcile the S049 row's `2026-10-20` local date with the lesson's “reopened 2026-10-21” UTC date; do not change the row.

**Evidence pointer cited by the item:** `S049` row and the lesson’s “reopened 2026-10-21” wording. The routed item provides no filename or line for either. Nearby pointers in the same lesson are `S049 row + https://docs.python.org/3/library/subprocess.html, fetched 2026-10-21` (line 135), and the cited census command/results at lines 137–140. Those are the exact adjacent pointers printed in the lesson; they do not supply a row file:line anchor for the date comparison.

**Agreement / discrepancy:** Agree that the requested correction is explicit date-basis wording only, with no row rewrite. The routed item’s row/lesson pointers lack exact file:line anchors; I have not invented them.

## Commands and observed outputs

- `functions.glob` on `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons` → returned `round-19-verifier-spotcheck.md` among the lesson files.
- `functions.grep` for `Routed defects` in the target file → `No matches found` (the actual heading is “Routed to the lane for round 20”).
- `functions.grep` for `Routed to the lane for round 20` (case-insensitive) → matched source lines 164–175; the three items are at 166–175.
- `functions.read` of target-file lines 164–175 → returned all three verbatim routed items reproduced above.
- `functions.read` of lines 108–116 → returned the receipt-to-relative-pointer mapping listed under item 2, including the frozen-check context.
- `functions.read` of lines 129–140 → returned the S049 adjacent pointer and census command/result noted under item 3.
- `functions.read` of `xd://lsp` → `No such tool: xd://lsp`; the mounted-device response listed no LSP route. Text search/read was therefore the available source method, not semantic LSP proof.
- `functions.read` of the required report path before writing → `Path .../E03R19Verifier.md not found`.

No tools were installed or updated. No production file, evidence receipt, Git/JJ state, or other report was changed; no checks or suites were run.
