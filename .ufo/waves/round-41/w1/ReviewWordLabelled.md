# ReviewWordLabelled — every word-count-labelled quote, round 40 + round-41 w1

Seat: read-only reviewer. Only file written is this report. Lane checkout, fleet repo, sibling
lanes, jj state and Git index untouched. No C1/C2 counter run in any mode (the deciding run is
the L1's); contract read, never edited.

## Verdict

**Exactly one wrong label survives in the read set, and it is round-40 routed defect 4 itself.**
`corpus/lessons/round-40.md:14` labels the S152 quote "11 words"; the quote has **13** tokens.
The label is wrong **11 → 13**; the quote text is verbatim and correct. The closed round-40 file
is unchanged at HEAD (`4678127`), which is what the round-40 routing asked for — the erratum is
appended in round 41 (`corpus/lessons/round-41.md:104`, draft `ScribeLesson.md:174`), and that
erratum itself states 11 and 13 correctly.

**Every other word-count-labelled quote in `corpus/lessons/round-40.md` and in every round-41
w1 draft is correct**, including all 15- and 16-word labels on the two round-41 source quotes,
which I re-derived from the committed snapshots rather than trusting any seat.

One convention-sensitive label needs a decision, not a fix: `round-40.md:21` says "7 words" for
`Snapshot Testing: Use With Care - Randy Coulman` — 7 words, **8 whitespace tokens** (`wc -w`
= 8, the standalone `-` is punctuation). Under the routed-defect-4 convention ("13 tokens",
checked with `wc -w`) a recomputing checker flags it. See F2.

## Method

Independent recount, then comparison. I did not reuse any seat's arithmetic.

```
python3 /tmp/tameshi-r41-ReviewWordLabelled-scan.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-40.md \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-41/w1/*.md
```

The scanner (`/tmp/tameshi-r41-ReviewWordLabelled-scan.py`, 3.7 KB) finds every
`<N>[- ]word(s)|token(s)` label, associates it with the quoted span in the same paragraph (so a
quote wrapped across source lines still finds its label), and prints tokens / punctuation-free
words / CJK-char counts. Its nearest-quote association is wrong for table paragraphs, so **every
hit below was read in the source and resolved by hand** — the scanner is the index, the reads are
the evidence.

Quote text ground truth, re-derived from the committed snapshots in this run:

```
sha256sum .ufo/evidence/round-41/sources/ast.html .ufo/evidence/round-41/sources/pathlib.html
183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317  ast.html
0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093  pathlib.html
# tag-strip (<script|style> removed, tags removed, entities unescaped, \s+ collapsed), then find:

printf '%s' 'drawbacks such as fragility and lack of context can lead to false positives' | wc -w   -> 13
printf '%s' 'Snapshot Testing: Use With Care - Randy Coulman'                              | wc -w   -> 8
printf '%s' 'Snapshot Testing: Use With Care'                                              | wc -w   -> 5
printf '%s' 'The ast module helps Python applications to process trees of the Python abstract syntax grammar.' | wc -w -> 15
printf '%s' 'Open the file pointed to in text mode, write data to it, and close the file'   | wc -w   -> 16
printf '%s' 'Open the file pointed to in bytes mode, write data to it, and close the file'  | wc -w   -> 16
```

Both sentences are present verbatim in the tag-stripped snapshots (checked with `in`, not with a
line grep), and the `pathlib` write_text sentence also occurs with its trailing `:` — 16 either
way, so the colon is not a counting ambiguity.

## Findings (severity ordered)

### F1 (high, out of the editable set by design) — `round-40.md:14` label is 11, count is 13

`corpus/lessons/round-40.md:14`

```
- Quote (11 words), English abstract: "drawbacks such as fragility and lack of context can lead to false positives".
```

`drawbacks(1) such(2) as(3) fragility(4) and(5) lack(6) of(7) context(8) can(9) lead(10) to(11)
false(12) positives(13)` → **13**, and `wc -w` = 13. **Off: 11 → 13.** No convention rescues 11:
13 under tokens, 13 under punctuation-free words, 0 CJK.

This is verbatim round-40 routed defect 4 (`corpus/lessons/round-40-verifier-spotcheck.md`,
`## Routed defects` item 4: "label the quoted string '11 words'; it has 13 tokens"). The quote is
verbatim in the snapshot — only the label is off.

**Do not edit `round-40.md`.** The file is byte-identical to HEAD (`git status --porcelain
corpus/lessons/round-40.md` empty; `git log -1` → `4678127 round-40: deciding receipts, …`), and
the round-40 closure directed an *appended* correction, not an in-place rewrite. The correction
is already carried correctly: `corpus/lessons/round-41.md:104` and the draft
`.ufo/waves/round-41/w1/ScribeLesson.md:174` both record "a quote labelled \"11 words\" that has
13 tokens". Nothing further is owed on this line.

### F2 (low, decision not fix) — `round-40.md:21` is correct as words, 8 as whitespace tokens

`corpus/lessons/round-40.md:21`

```
- Quote (7 words), README row D29: "Snapshot Testing: Use With Care - Randy Coulman".
```

7 words (`Snapshot Testing Use With Care Randy Coulman`); **8 whitespace tokens** because the
standalone `-` is a token but not a word; **5** if the label is meant to cover only the blog title
(the ` - Randy Coulman` suffix is the author). `ReviewD29.md:21` reached the same residual nit
independently and called the label "loose".

Verdict: **not a miscount** — the label says "words" and there are 7. But it is the only label in
the read set whose verdict flips under the routed-defect-4 convention, which the round-41 erratum
phrases as *tokens* and the round-40 closure checked with `wc -w`. If the L1 chains "recount every
labelled quote with a token counter" as the standing fix, this line fires falsely. Either accept
word-count semantics for it, or append a restatement in the round-41 lesson
(`7 words / 8 whitespace tokens; the ` - Randy Coulman` suffix is the author, the bare title is 5`)
so a token checker and the lesson agree.

### F3 (info) — every round-41 label is correct; the mid-flight 16/17 pair is already repaired

The stale pair that three seats caught is gone. `corpus/knowledge/r41-variable-destination-writes.md`
(sha256 `ee7df01249e11d53a8f29911e3c1345bb78f93be7d9b7654474470fe74f3903a` at this read) reads
`(15 words)` at `:12` and `(16 words)` at `:19`; both match my snapshot counts. Its earlier
03:38-state `(16 words)` / `(17 words)` is what `ScribeEntry.md:42-43`, `ScribeReadme.md:94-95`,
`ReviewSourceRows.md:143` (F6), `ScoutPathlibDocs.md:161-164`, `ScribeLesson.md:174` and
`ReviewScribeEntry.md:123-124` each report — every one of those passages states 15 and 16 beside
the stale numbers, so none of them is itself a bad label.

`corpus/lessons/round-41.md` (sha256 `1e4f1f5e…`) reads `(15 words)` at `:17` and `(16 words)` at
`:21`; both correct.

### F4 (info) — out-of-class counts I saw and deliberately did not score

`ExecRowFormat.md:37` (`split(/[,;]/) → 1 token` on the used-by cell), `ScribeLog.md:35`
(`18 tokens`, m8 path surface), `ScribeLog.md:122` (`24 tokens`), `ScribeLesson.md:61-62`
(`= 15 tokens` / `= 16 tokens` on the two sentences) are counts of *cells, paths or sentences in
a claim*, not labels attached to a quotation. `ScribeLesson.md:61-62` are correct (15, 16). The
`<= 25 words` occurrences (`ScoutAstDocs.md:11,111`, `ScribeLesson.md:105`, `ScribeReadme.md:100`)
are bounds, satisfied at 15 and 16.

## Complete label inventory

Round-40 lesson (assigned scope):

| file:line | label | quote | measured | verdict |
|---|---|---|---|---|
| `corpus/lessons/round-40.md:14` | `11 words` | S152 abstract | 13 tokens / 13 words | **OFF 11 → 13** |
| `corpus/lessons/round-40.md:21` | `7 words` | D29 title cell | 7 words / 8 tokens (bare title 5) | correct as words; see F2 |

Round-41 w1 drafts (assigned scope) — all correct:

| file:line | label | quote | measured |
|---|---|---|---|
| `ScoutAstDocs.md:110` | `Word count: 15` | ast sentence | 15 |
| `ScoutAstDocs.md:121` | `15-word count` | ast sentence | 15 |
| `ScoutAstDocs.md:210,217` | `WORD_COUNT: 15` | ast sentence | 15 |
| `ScoutPathlibDocs.md:122` | `Word count: 16` | write_text sentence | 16 (three conventions) |
| `ScoutPathlibDocs.md:189` | `16-word count` | write_text sentence | 16 |
| `ScoutPathlibDocs.md:298-300` | `words split() : 16` etc. | write_text sentence | 16 |
| `ScoutPathlibDocs.md:161-164` | `(16 words)` / `(15 words)` | live entry's labels (S154 / S153) | 16 / 15 — correct citation |
| `ScribeSources.md:39` | `(15 words)` | ast sentence | 15 |
| `ScribeSources.md:44` | `(16 words)` | write_text sentence | 16 |
| `ScribeLesson.md:61` | `= 15 tokens` | ast sentence | 15 |
| `ScribeLesson.md:62` | `= 16 tokens` | write_text sentence | 16 |
| `ScribeLesson.md:95` | `15 words` | ast sentence | 15 |
| `ScribeLesson.md:102` | `16 words` | write_text sentence | 16 |
| `ScribeLesson.md:105` | `≤25 words` | both | 15, 16 — bound OK |
| `ScribeLesson.md:174` | `"16 words"` / `"17 words"` / `"11 words"` / `"13 tokens"` | errata: stale labels + round-40 defect | all four statements correct |
| `ScribeEntry.md:17` | `15 words` | ast sentence | 15 |
| `ScribeEntry.md:18` | `16 words` | write_text sentence (colon noted) | 16 |
| `ScribeEntry.md:42-43` | `(16 words)` / `(17 words)` | reports the stale live pair, states 15 and 16 | correct report |
| `ReviewScribeEntry.md:123-124` | `15 words` / `16 words` | live entry `:12` / `:19` | 15 / 16 |
| `ScribeReadme.md:94-95` | `(16 words)` / `(17 words)` | reports the stale pair, settled 15/16 | correct report |
| `ScribeReadme.md:100` | `≤25 words` | both quotes | satisfied |
| `ReviewSourceRows.md:143` | `16 words` / `17 words` (F6) | reports the stale pair, states 15/16 | correct report |
| `ReviewSourceRows.md:99` | `16-word` | write_text sentence | 16 |
| `CriticR40Discharge.md:18` | `"11 words"` / `13 tokens` | round-40 defect 4 | both correct |

Adjacent live records (outside the assigned scope, checked because the drafts reproduce their
text): `corpus/knowledge/r41-variable-destination-writes.md:12` = 15 ✓, `:19` = 16 ✓;
`corpus/lessons/round-41.md:17` = 15 ✓, `:21` = 16 ✓.

43 label occurrences were found by the scanner across `round-40.md` plus the w1 drafts. Each is
either a row in the tables above or one of the scanner's table-paragraph mis-associations
(`ScribeEntry.md:14` → labels at `:17,:18`;
`ScoutPathlibDocs.md:187` → the `16-word` in the Confidence bullet; `ScribeSources.md:35` →
labels at `:39,:44`; `ReviewScribeEntry.md:118` → labels at `:123,:124`; `ScribeLesson.md:53,92,171`
→ labels at `:61,:62`, `:95,:102,:105`, `:174`), each resolved by reading the lines.

Note for any seat that scans `w1/*.md` for labelled quotes: this report is now one of those
files, and the numbers in it are **citations of audited labels**, never labels attached to a
quote of mine. The scanner's pattern matches them; the association is the paragraph, not the
sentence, so the ones to ignore are all in this file's backticks.

## Residual risk

- **The live entry and lesson are uncommitted and were rewritten twice during this seat's read
  window.** `corpus/lessons/round-41.md` shows ` M`, and the entry is untracked. A stale copy that
  still reads 16/17 would reintroduce the defect; the audited shas are the ones printed above
  (`ee7df012…` entry, `1e4f1f5e…` lesson). If either moves before the measurement commit, the
  label verdict must be re-run — the draft texts are not a substitute for the committed file.
- **`round-40.md:21` will read as a defect to any checker that uses `wc -w`** (8 vs 7). That is a
  convention mismatch, not an error in the lesson; it is unresolved until the L1 states which
  convention the standing fix uses (F2).
- **CJK convention is untested here.** The only CJK quote in `round-40.md` (`:33`, the S108
  Chinese sentence) carries no count label, so no verdict was needed; if a future lesson labels a
  Chinese quote, `split()` and CJK-character counting disagree and neither is "the" count.

## Verification gaps

- Labels were counted by whitespace split and punctuation-free split, plus `wc -w`. No
  language-aware segmentation (ICU/UAX#29) was used; for these English and code-token quotes all
  three agree, so the verdicts do not depend on it.
- `ReviewSourceRows.md`, `ReviewScribeEntry.md`, `ScribeReadme.md` and `ScribeLesson.md` were
  edited by their seats during the window (`ReviewScribeEntry.md` lost an M4 `16 words`
  parenthetical between two of my reads). I re-read each at its final sha above; a later edit is
  not covered.

## Tooling

No install or upgrade performed — `python3` and coreutils sufficed, so the pacman pause was never
engaged (no `-S`, `-Sy`, `-Syu`, `-U` or `-R`). Scratch: `/tmp/tameshi-r41-ReviewWordLabelled-*`.
This report cites no `.ufo/waves/round-35/scratch*/` path, so the round-35 scratch relocation does
not affect it.

Report: .ufo/waves/round-41/w1/ReviewWordLabelled.md
