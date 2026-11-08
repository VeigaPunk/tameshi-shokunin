# SC1 — `corpus/QUALITY.md` append draft (round 95)

**Seat:** R95SC1 (scribe). **Lane:** tameshi. **Mode:** read-only — nothing under
`corpus/` was written; this file is a draft for the L1 to integrate.

The criteria continue the lane's numbering: the last committed criterion is **168**
(`corpus/QUALITY.md:2677`), so these are **169**, **170**, **171** and **172**. Each has
the established one-sentence rule, an "Able to fail" receipt pointer, and the lesson
mistake it comes from.

**A note on what the round already caught.** The round's own reviewer (`R95R1`) found
that the first landed lesson's Gate quotes sat on lines that did not name their sid,
which made the counter read zero quotes and `source=false`; the L1 reflowed the Gate at
`20fabad4` and the counter now passes at HEAD `3ca1981a` (`quote:1` on all four rows,
`source=true`, `C1_R95_PASS=true`, exit 0 — re-measured by this seat). **Criterion 172
below is about the layer that reflow did not reach**: the numbers *inside* the quotes'
own lines. That is not a hypothetical — it is live at HEAD today, and it is what
`lessons/round-95.md` M4 records.

---

## Criteria appended — round 95

169. A frozen self-assessment tally is reconciled by an **append-only erratum** naming
    the superseded sentence — never by editing the frozen file. The tally's operative
    value is the one the receipt prints, and the erratum names every place the
    superseded sentence is recorded, so a reader who finds the old number also finds
    the correction beside it. Round 94's C2 claim was filed `unprovable` because the
    frozen plan, the LOG and the lesson all said `DISPOSITION_SELFTEST: 8/8 pass` while
    the operative receipt printed `9/9 pass`; the frozen files are history and an
    in-place edit would have destroyed the evidence that the drift happened. Able to
    fail: `plans/round-94.plan.md:165`, `LOG.md:5085` and `corpus/lessons/round-94.md:66`
    still read `8/8`, while `.ufo/evidence/round-94/pre-freeze/c2-selftest.out:10`
    reads `9/9 pass` — the erratum in `corpus/lessons/round-95.md` § Erratum is the only
    thing that reconciles them, and it edits none of the three. (`lessons/round-95.md`
    M1; round-94 closure routed defect 1.)

170. A receipt a verdict is read from is bound to **a revision and a counter digest**,
    not to a filesystem path. A receipt that exists only in the working tree, or whose
    `counter_sha=` line is absent or differs from the digest of the counter blob at the
    revision it claims, is refused — the audit's evidence binding is the identity of
    the bytes, not the presence of a file with the right name. Round 94's checker read
    its receipts from the filesystem and never read a `counter_sha=` line, so both
    forged receipt sets passed it; the successor reads the receipts out of the object
    store at `--rev` and compares each `counter_sha=` against the counter blob it
    actually grades. Able to fail: `.ufo/waves/round-95/w1/R95E3-forge/forge-matrix.txt`
    — `forge-handwritten` (a receipt present only in the working tree) → exit 1,
    `receipt-absent-at-rev`; `forge-counter-sha` (a committed receipt whose
    `counter_sha=` is 64 zeros) → exit 1, `receipt-counter-sha-mismatch`; both print
    `findings=0` under the round-94 checker at `6a2a1fdd` in the same matrix. The
    round-94 checker has zero `counter_sha` occurrences (`grep -c counter_sha
    .ufo/evidence/round-94/conjunct-disposition-v94.py` → 0). (`lessons/round-95.md`
    M1; round-94 closure routed defect 1; `plans/round-95.plan.md` §C2.)

171. A reader's declared literal-block class names **every** Markdown literal class it
    relies on — fenced **and** indented — or the note it certifies must avoid the
    unnamed class. A reader that skips only fenced blocks and treats a 4-space-indented
    line as block structure keys a row the specification calls literal text, so its
    certificate covers a presentation it never read. Round 94's reader declared the
    fenced class (S322) and not the indented one, and its own wave showed the cost: the
    indented-code fixture was refused (`verdict_tables=false`) and an indented stray
    verdict token was read as a table row. Able to fail:
    `.ufo/waves/round-94/w1/R94C1-A8-indented-code.out` (`C1_BADROWS dup:301:C01`,
    `verdict_tables=false`, `C1_R94_PASS=false`) and
    `.ufo/waves/round-94/w1/R94C1-A8b-indent-token.out` (`C1_BADROWS
    stray-verdict:297:| C01 | KILLED |`) — the v94 reader refusing or mis-keying what
    CommonMark §4.4 calls literal text; the round-95 reader's `indent-code-row` and
    `indent-token` states are the arms that must now pass. (`lessons/round-95.md` M2,
    M3; `plans/round-95.plan.md` §C1; S323.)

172. A record's numbers about its own evidence are **printed by a command**, never
    written by hand, and a line a record cites **carries** the sentence it is cited for.
    A quote's word count is the accepting tokenizer's count (`len(q.split())`), and a
    cited line is the line that holds the quote in the snapshot rendering the record
    names — a count or a line that is eyeballed is a number nobody re-derived, and a
    line that does not carry its quote makes the record unverifiable at the point a
    reader checks it. Round 95's own records did both: the landed `S323` row claims
    `(15 words)` for a 16-token span and `line 2355` for a sentence that begins at line
    2358, and five of the six landed Gate lines mis-state their quote's word count
    while four cite a line that carries different text. Able to fail: at HEAD
    `3ca1981a`, `corpus/lessons/round-95.md:16–21` and `corpus/SOURCES.md:199` —
    `len(q.split())` on the S323 span → 16 (the row says 15), and the tag-stripped
    snapshot line carrying that sentence → 2358 (the row says 2355, a blank line);
    the same command over the corrected draft prints 16 and 2358. (`lessons/round-95.md`
    M4.)

---

## Note for the L1 on numbering and scope

The seat spec named three criteria (169, 170, 171) — a frozen-tally erratum rule, a
receipt-binding rule, and a declared-literal-class rule. **171 above is that third
criterion**, worded to the spec ("names every Markdown literal class it relies on
(fenced AND indented), or the note it certifies must avoid the unnamed class"). The
fourth, **172**, is the rule this seat's M4 measurement shows is missing from the lane:
a record's own numbers must be printed by a command and a cited line must carry its
quote. It is drafted here because M4 is precisely a violation of it, and because
QUALITY 168 (a quoted receipt line is byte-backed) and QUALITY 87 (a quote's length is
printed by a command) each cover one half and neither covers the whole. **If the L1
prefers to land exactly three criteria, 172 can be dropped** — M4 then has no criterion
to point at, which is the state the lane was in for this round's other mistakes. The
L1's call.

## Criteria-to-mistake index for this draft

| criterion | one-sentence rule | lesson mistake | able-to-fail pointer |
|---|---|---|---|
| 169 | a frozen tally is reconciled by an append-only erratum, never edited in place | M1 | `plans/round-94.plan.md:165` vs `.ufo/evidence/round-94/pre-freeze/c2-selftest.out:10` |
| 170 | a receipt a verdict reads is bound to a revision and a counter digest | M1 | `.ufo/waves/round-95/w1/R95E3-forge/forge-matrix.txt` |
| 171 | a declared literal-block class names every class relied on (fenced AND indented) | M2, M3 | `.ufo/waves/round-94/w1/R94C1-A8-indented-code.out`, `R94C1-A8b-indent-token.out` |
| 172 | a record's numbers are printed by a command and a cited line carries its quote | M4 | `corpus/lessons/round-95.md:16–21` and `corpus/SOURCES.md:199` at HEAD `3ca1981a` |
