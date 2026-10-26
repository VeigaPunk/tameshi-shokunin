# T50ScribeCorrections — lesson-correction class (C1 milestone)

seat: `T50ScribeCorrections` (round-50 w1, L1 TameshiR50)
date: 2026-10-26
base: `e3729de862f73ae080d98fcf522a7081ce16e40a` (lane tip at round start)
scope: `R40.1`, `R40.4`, `R44.1`, `R46.4`, `R47.3` of `.ufo/evidence/round-50/c1/defects.json`
status: **findings and drafts, no verdict.** This seat does not set a ledger status; the L1 decides.
Nothing here edits a closed lesson, the ledger, `SCORECARD.md`, the contract or a counter.

Base equivalence: every file this report cites is byte-identical at `e3729de` and at HEAD
(`git show e3729de:<path> | sha256sum` vs `sha256sum <path>`; receipt R1), so the "exists in the lane
at base" question is answered by reading the working tree. Among tracked files, only `SCORECARD.md`
changed after base (21 added lines, the round-50 pre-registration; `git diff --stat e3729de..HEAD --
corpus/ SCORECARD.md LOG.md` → `SCORECARD.md | 21 +`), and its diff names none of these five ids — the
one matching line is the round-50 Planned paragraph (`SCORECARD.md:2410`), which names none of them
(receipt R10).

## Disposition table

| item | a correction exists? | where | commit that added it | draft below? |
|---|---|---|---|---|
| R40.1 | yes for the counts; the two naming drifts in the same sentence are uncorrected | `corpus/lessons/round-41.md:51-58` | `b37ce974b6efb8c465626d7346149549a3300a4b` | supplementary: **C1-R50-3** |
| R40.4 | implicit only (a Mistakes-table antecedent, not a named correction) | `corpus/lessons/round-41.md:75` | `b37ce974b6efb8c465626d7346149549a3300a4b` | **C1-R50-2** |
| R44.1 | yes, named and measured (Mistakes row + criterion 87) | `corpus/lessons/round-45.md:158`, `corpus/QUALITY.md:1223-1242` | `ea25e0224fc81060414b27301c27bd1344669165` | none needed |
| R46.4 | **no** | — | — | **C1-R50-1** |
| R47.3 | yes, named | `corpus/lessons/round-48.md:106-121`, `:176-189` | `50545328e7ac4ba1703d70030e37dacec9362e68` | none needed |

Ancestry checks for the three "yes" rows (`git merge-base --is-ancestor ROUTED_AT COMMIT`, exit 0 in
each case): `a3d6c69… → b37ce974…`, `5891bdb7… → ea25e022…`, `473336d9… → 50545328…`. Receipt R2.

## R40.1 — correction exists for the counts; two drifts remain

Spot-check text (`corpus/lessons/round-40-verifier-spotcheck.md:293-302`): the summary sentence
contradicts the table, and "also names eight rows under the word 'seven' and says 'two prose-class
rows' where the table marks three (S113, S123, S134)".

The appended correction, `corpus/lessons/round-41.md:51-58`, verbatim (`:53-58`):

```
The round-40 closure's routed defect 1 stands: that lesson's closing sentence says seven
refused and nine present-but-not-appended, while the verdict table in the same file
counts one adopted, six refused, ten present-but-not-appended. The table is the record;
the summary sentence is the drift. This appended correction is the fix the closure asked
for ("append a correction in the round-41 lesson — do not rewrite the closed round-40
file in place"). The round-40 file is unchanged.
```

It fixes the count contradiction. It does not name the two other drifts in the same sentence (eight
rows enumerated under "seven"; "two prose-class rows" against the table's three). Because the item is
one sentence and the closure asked for "a correction", a reader who stops at `round-41.md:58` still
cannot tell that the enumeration is also wrong. Draft **C1-R50-3** supplies the named form for those
two sub-claims; the L1 decides whether to append it or to rest on `round-41.md:51-58`.

Commands (lane root), receipt R3:

```
$ sed -n '73p' corpus/lessons/round-40.md | grep -oE 'S1[0-9]{2}' | tr '\n' ' '; echo
S109 S131 S137 S140 S141 S143
$ grep -nE '^\| S(109|131|137|140|141|143) ' corpus/lessons/round-40.md | grep -ci 'refuse'
6
$ grep -ci 'the prose class is stale' corpus/lessons/round-40.md
3
$ grep -nE '^\| S(113|123|134) ' corpus/lessons/round-40.md | cut -d'|' -f1,2
58:| S113 
61:| S123 
67:| S134 
$ awk '/^### Quarantine/{f=1;next} f&&/^\| S[0-9]/{n++} END{print n}' corpus/lessons/round-40.md
17
```

## R40.4 — implicit erratum only; no named correction

Spot-check text (`corpus/lessons/round-40-verifier-spotcheck.md:312-313`): the lesson and the seat
brief label the S152 quote "11 words"; it has 13 tokens.

The lane contains one statement of the true count: `corpus/lessons/round-41.md:75`, the
`count-label-drift` Mistakes row, verbatim:

```
| count-label-drift | this round's first draft of `corpus/knowledge/r41-variable-destination-writes.md` labelled the S153 quote "16 words" and the S154 quote "17 words"; the token counts are 15 and 16 (`python3 -c "print(len(s.split()))"` on both sentences) | the round-40 closure's routed defect 4 (a quote labelled "11 words" that has 13 tokens) — the same class, one round later, caught by re-counting instead of trusting the label | both labels corrected in the entry, and the wave's word-label seat re-counts every labelled quote in the round's drafts. The fix can fail: the label read 16 where the count reads 15, so a checker that recomputes tokens flags the pre-fix text |
```

That is an antecedent citation inside another mistake's row: it names "routed defect 4" and the true
count, but not the corrected file:line, not the wrong label verbatim, and it gives no command. It is
not a *named* correction. The slip is still live in two places: `corpus/lessons/round-40.md:14`
(closed lesson, append-only) and `corpus/knowledge/r6-snapshot-practice-corpus.md:10` (a live corpus
file). Draft **C1-R50-2** supplies the named form. Note for the L1: sibling seat `T50Disp40` already
records R40.4 `fixed` on `round-41.md:75`
(`.ufo/waves/round-50/w1/T50Disp40.rows.json`, evidence `corpus/lessons/round-41.md:75`), which the
counter accepts mechanically (`13 tokens` and `11 words` are keys); the draft is hardening, not a
contradiction of that row.

Re-count here (receipt R4):

```
$ python3 -c "import re;s='drawbacks such as fragility and lack of context can lead to false positives';print(len(s.split()), len(re.findall(r'[A-Za-z0-9]+', s)))"
13 13
$ grep -n 'Quote (11 words)' corpus/lessons/round-40.md
14:- Quote (11 words), English abstract: "drawbacks such as fragility and lack of context can lead to false positives".
$ grep -n 'The quote is 11 words' corpus/knowledge/r6-snapshot-practice-corpus.md
10:S152 is the UFMG thesis PDF. The English abstract, in the committed excerpt, says snapshot tests are easy to implement and that drawbacks such as fragility and lack of context can lead to false positives. The quote is 11 words: "drawbacks such as fragility and lack of context can lead to false positives".
```

## R44.1 — already corrected (round-45 Mistakes row + criterion 87)

Spot-check text (`corpus/lessons/round-44-verifier-spotcheck.md:73`): `corpus/lessons/round-44.md`'s
first located quote is labeled "20 words"; it tokenizes to ~28 (24 letter/digit words); "correct the
label in a future round (append-only)".

Two appended records in round 45 name it, both added by `ea25e022…` (post-`routed_at` `5891bdb7…`;
ancestry exit 0, receipt R2). First, the lesson's own Mistakes row,
`corpus/lessons/round-45.md:158`, evidence cell verbatim:

```
`corpus/lessons/round-44.md:26` labels the Stryker line-15 quote "20 words"; measured `whitespace_tokens=28 letter_digit_words=22`, and the round-45 C1 counter grades that quote `('invalid', 'quote length 28')` (`.ufo/evidence/round-45/mistakes/r44-quote-token-count.stdout`); the 20 was inherited from `corpus/lessons/round-43.md:52`, whose shorter quote is this one's suffix (`.ufo/waves/round-45/w2/ScribeQuality.md` gate 4)
```

That row names the corrected file:line, both measured counts, the receipt, and the routed-by
(`corpus/lessons/round-44-verifier-spotcheck.md:73`, "which itself wrote an unmeasured '24'").
Second, `corpus/QUALITY.md:1223-1242`, criterion 87 ("a quote's length is measured, never written by
hand"): `:1229-1231` states the rule, and `:1235-1242` repeats the errata in the same terms, verbatim:

```
Lesson: `corpus/lessons/round-44.md:26` labels the Stryker quote "20 words"; measured, it is 28
whitespace tokens (22 letter/digit words) and the round-45 C1 counter grades it
`('invalid', 'quote length 28')` — receipt
`.ufo/evidence/round-45/mistakes/r44-quote-token-count.stdout`. The number is
`corpus/lessons/round-43.md:52`'s correct "20 words" for the shorter quote that is this quote's
suffix: the round-44 quote prepends 8 tokens and inherited the label. The round-44 spotcheck
called the label cosmetic (`corpus/lessons/round-44-verifier-spotcheck.md:73`) because the row's
grounding quote was compliant, and its own parenthetical "24 letter/digit words" is itself
unmeasured (measured: 22).
```

It names the file:line, prints the measured value, corrects the spot-check's own "24" to 22, and
carries a falsifier. Re-count here: 28 whitespace tokens, 22 letter/digit words (receipt R5):

```
$ python3 -c "import re;s='Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time!';print(len(s.split()), len(re.findall(r'[A-Za-z0-9]+', s)))"
28 22
```

No draft. The closed lesson keeps "20 words", which is what append-only requires.

## R46.4 — missing; the committed lesson still prints the folded dash

Spot-check text (`corpus/lessons/round-46-verifier-spotcheck.md:102`): "Print the S259 gate quote with
the source's en dash, or state the fold at the quote, in the lesson itself."

No correction exists. `corpus/lessons/round-46.md:41-42` still prints the ASCII hyphen; the pinned
snapshot holds the en dash three times and the hyphen zero times; and the round-47 lesson's claim of a
green-after fix is about a **scratch copy**, not the committed lesson (receipt R6):

```
$ sed -n '42p' corpus/lessons/round-46.md
  for 9.8 %-16.3 % of failed pipeline runs.”
$ python3 -c "
for i,l in enumerate(open('corpus/lessons/round-46.md',encoding='utf-8'),1):
    if '9.8 %' in l: print(i, [hex(ord(c)) for c in l if c in '\u2013\u2014-'])
"
42 ['0x2d']
81 ['0x2013', '0x2d', '0x2d', '0x2013', '0x2014']
$ grep -o '9\.8 %–16\.3 %' .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html | wc -l
3
$ grep -o '9\.8 %-16\.3 %' .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html | wc -l
0
$ diff corpus/lessons/round-46.md .ufo/evidence/round-47/quality/round46-lesson-dash-restored.md
42c42
<   for 9.8 %-16.3 % of failed pipeline runs.”
---
>   for 9.8 %–16.3 % of failed pipeline runs.”
$ python3 .ufo/evidence/round-47/quality/lesson-quote-check.py corpus/lessons/round-46.md; echo exit=$?
LQ PASS arxiv-2504.16777-abs.html 'finding that 75% of flaky tests across all projects belong t'
LQ FAIL tum-portal-flaky-failures.html 'We found that, across all projects, undetected flaky failure'
LQ PASS google-flaky-feed-6277555988217606236.json 'about 84% of the transitions we observe from pass to fail in'
LESSON_QUOTE_CHECK: file=corpus/lessons/round-46.md blocks=3 quotes=3 bad=1 unbound=1
exit=1
```

`corpus/lessons/round-47.md:105` records the defect (and is the only later record that mentions it),
but it (a) contains neither key (`S259`, `en dash`) — it writes `U+2013` — so a ledger row citing it
fails `key_miss`; (b) reports "green after the one-character delta" for
`.ufo/evidence/round-47/quality/round46-lesson-dash-restored.md`, which the diff above shows is a
different file; (c) leaves the committed lesson printing the fold with no fold statement. The tree
therefore does not support `fixed`; draft **C1-R50-1** is the append-only form (QUALITY 4,
`corpus/QUALITY.md:7`) that states the fold at the quoted span.

Grep sweep that establishes "no correction elsewhere" (receipt R7): `grep -rn "S259" corpus/
SCORECARD.md LOG.md` returns the round-46 lesson, its spot-check, `r5-undetected-flaky-failures.md`,
`SOURCES.md:134`, `README.md:574` and `SCORECARD.md:2208` — no round-47+ correction block;
`grep -rn -i "correction\|errata" corpus/lessons/round-4[5-9].md` returns only the round-48
correction blocks and the round-49 references, none naming S259; `grep -n "9\.8" SCORECARD.md LOG.md`
returns nothing.

## R47.3 — already corrected (named)

Spot-check text (`corpus/lessons/round-47-verifier-spotcheck.md:105`): "append a named correction for
`corpus/lessons/round-47.md:117-118` dependence sets (conformance defect 5)."

The correction exists in `corpus/lessons/round-48.md`, added by `50545328…` (post-`routed_at`
`473336d9…`): the section heading `## Corrections to earlier lessons (append-only)` at `:106`, the
named block `## Correction C1-R48-1 — the round-47 dependence sets (unreceipted freeze-time
observation)` at `:108` with its body to `:121`, and the bullet at `:176-189` whose first line,
verbatim (`:178`):

```
- **C1-R48-1 (corrects `corpus/lessons/round-47.md:117-118`; the file is never rewritten).**
```

It states what the round-47 lesson said, what the standing rows declare, what the deciding run
observed, and a rule for later rounds. No draft.

## Sibling readings on these five items (recorded, not resolved here)

Wave-1 seats have already recorded dispositions that disagree with each other on three of the five
items. The L1 has to settle the standard; this seat only reports the tree.

**R46.4 — three readings.** `.ufo/waves/round-50/w1/T50Cross46.md:35` says "DECLINED", because "no
fold statement sits at the quote" and the lane "declined to rewrite the landed lesson record";
`.ufo/waves/round-50/w1/T50Disp46.rows.json` (id `R46.4`) says `"status": "open"` with a `fix_plan`
that begins "this round: change corpus/lessons/round-46.md:42 from 'for 9.8 %-16.3 % of failed
pipeline runs.' to the en-dash form … or keep the hyphen and add the fold sentence at the quote";
`.ufo/waves/round-50/w1/T50RevengerRecur.md:62` records it "closed" at r47 on `round-47.md:105`, whose
green-after is the scratch copy (R6). The `open` route also needs the id in the newest
`**Planned (round` paragraph of `SCORECARD.md`, which does not name it (`grep -c 'R46\.4' SCORECARD.md`
→ 0; the round-50 Planned paragraph is `SCORECARD.md:2410`; receipt R10).

**R40.4 — two readings.** `T50Disp40.rows.json` says `fixed` on `round-41.md:75`; `T50RevengerRecur.md:37`
and `:185` say `open`, because "no round appended a correction to the round-40 label"; `T50ScoutPlanned.md:66`
notes R40.4 as "corrected by `corpus/lessons/round-41.md:75`".

**R44.1 — one reading against the record above.** `T50RevengerRecur.md:53` says `open` ("no correction
was appended"), while `:135` maps the class to Q87 and records zero recurrences after it. The tree has
two appended records that name the label and the measured value (`round-45.md:158`, `QUALITY.md:1235-1242`).

**The standard the readings disagree about.** "The instance still reads the old text" cannot by itself
separate `fixed` from `open` here: an append-only correction never edits the closed file, and the
lane's own model correction (`round-48.md:106-121` for R47.3) leaves `round-47.md:117-118` byte-unchanged.
The distinguishing test is whether an appended record names the corrected location and the right value —
the strong form is `round-48.md:178` ("corrects `corpus/lessons/round-47.md:117-118`"); the weak form is
a Mistakes-table antecedent that names the id and the value but not the file:line (`round-41.md:75` for
R40.4). Drafts C1-R50-1, C1-R50-2 and C1-R50-3 supply the strong form for R46.4, R40.4 and the residual
of R40.1 respectively.

**The in-place route.** `T50Disp46.rows.json`'s `fix_plan` first branch — editing
`corpus/lessons/round-46.md:42` — contradicts QUALITY 4 ("Errata are append-only blocks",
`corpus/QUALITY.md:7`) and the lane's own precedent (`corpus/lessons/round-41.md:56-58`: "do not rewrite
the closed round-40 file in place"). The append-only-compliant form of the same remedy is C1-R50-1,
which states the fold at the quoted span in `corpus/lessons/round-50.md`. If the L1 reads "in the lesson
itself" literally, no compliant fix exists and the item is declined with a reason; if the L1 accepts the
appended fold declaration, the item is fixed by the commit that lands C1-R50-1 and
`lesson-quote-check.py corpus/lessons/round-46.md` will still exit 1 (the closed lesson is not
rewritten) — that red is the disclosed limit, not a hidden one.

## Draft blocks for `corpus/lessons/round-50.md`

Paste verbatim under a new heading `## Corrections to earlier records`. Each block names the item id,
the corrected file:line, the wrong statement verbatim, the right one, and the command. None rewrites a
closed lesson.

### Correction C1-R50-1 — R46.4: the S259 Gate quote is printed folded in the round-46 lesson

`corpus/lessons/round-46.md:41-42` prints the S259 abstract sentence with an ASCII hyphen where the
source holds an en dash. The wrong statement, verbatim:

```
  the string three times): “We found that, across all projects, undetected flaky failures account
  for 9.8 %-16.3 % of failed pipeline runs.”
```

The source's bytes are `9.8 %–16.3 %` (U+2013, en dash): the pinned snapshot holds that form three
times and the ASCII-hyphen form zero times, and the lane's `fold()` maps U+2013 to `-`, which is why
every counter passes the printed form. The printed hyphen is the lane's fold, not a misquote; the
quote is otherwise verbatim and 18 whitespace tokens. QUALITY 4 makes errata append-only blocks, so
the closed lesson is not rewritten and the fold is stated here at the quoted span: read
`9.8 %-16.3 %` in `corpus/lessons/round-46.md:42` as `9.8 %–16.3 %`.

Shown by (lane root):

```
$ sed -n '42p' corpus/lessons/round-46.md
  for 9.8 %-16.3 % of failed pipeline runs.”
$ grep -o '9\.8 %–16\.3 %' .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html | wc -l
3
$ grep -o '9\.8 %-16\.3 %' .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html | wc -l
0
$ python3 .ufo/evidence/round-47/quality/lesson-quote-check.py corpus/lessons/round-46.md; echo exit=$?
LQ PASS arxiv-2504.16777-abs.html 'finding that 75% of flaky tests across all projects belong t'
LQ FAIL tum-portal-flaky-failures.html 'We found that, across all projects, undetected flaky failure'
LQ PASS google-flaky-feed-6277555988217606236.json 'about 84% of the transitions we observe from pass to fail in'
LESSON_QUOTE_CHECK: file=corpus/lessons/round-46.md blocks=3 quotes=3 bad=1 unbound=1
exit=1
```

`corpus/lessons/round-47.md:105` records the defect and reports "green after the one-character delta";
that delta is on the scratch copy `.ufo/evidence/round-47/quality/round46-lesson-dash-restored.md`,
not on the committed lesson (`diff` → `42c42`, en dash on the right side only, exit 1). The checker
therefore stays red on the committed lesson; this block is the fold declaration, not a claim that the
file was changed.

### Correction C1-R50-2 — R40.4: the S152 quote is 13 tokens, not "11 words"

`corpus/lessons/round-40.md:14` labels the S152 abstract quote "11 words". The wrong statement,
verbatim:

```
- Quote (11 words), English abstract: "drawbacks such as fragility and lack of context can lead to false positives".
```

The quote is 13 whitespace tokens and 13 letter/digit words (tokenizer: the counter's fold, then
Python `str.split()` on the quote's own bytes — QUALITY 87's rule). The quote itself is verbatim and
correct; only the label is off. The closed lesson is not rewritten (QUALITY 4), so the label is
corrected here. The same slip sits in a live file, `corpus/knowledge/r6-snapshot-practice-corpus.md:10`
("The quote is 11 words"), which a later round may correct in place.

Shown by (lane root):

```
$ python3 -c "import re;s='drawbacks such as fragility and lack of context can lead to false positives';print(len(s.split()), len(re.findall(r'[A-Za-z0-9]+', s)))"
13 13
$ grep -n 'Quote (11 words)' corpus/lessons/round-40.md
14:- Quote (11 words), English abstract: "drawbacks such as fragility and lack of context can lead to false positives".
$ grep -n 'The quote is 11 words' corpus/knowledge/r6-snapshot-practice-corpus.md
10:S152 is the UFMG thesis PDF. The English abstract, in the committed excerpt, says snapshot tests are easy to implement and that drawbacks such as fragility and lack of context can lead to false positives. The quote is 11 words: "drawbacks such as fragility and lack of context can lead to false positives".
```

The round-41 Mistakes table already states the true count as the antecedent of its `count-label-drift`
row (`corpus/lessons/round-41.md:75`: "the round-40 closure's routed defect 4 (a quote labelled "11
words" that has 13 tokens)"); this block is the named correction, at the corrected file:line, that the
round-40 routing asked for.

### Correction C1-R50-3 — R40.1: the round-40 quarantine summary, the two drifts left

`corpus/lessons/round-40.md:73` closes the Gate block with a sentence that contradicts the file's own
17-row table. The wrong statement, verbatim:

```
One row adopted, seven refused (S109, S131, S137, S140, S141, S143 and the two prose-class rows whose premise a seat falsified), nine present-but-not-appended. No row is called a fabrication. The register and every campaign file were left byte-identical.
```

The right statement: one adopted, six refused (S109, S131, S137, S140, S141, S143) and ten
present-but-not-appended — 17 rows either way, as `corpus/lessons/round-41.md:51-58` already restates.
Two drifts in the same sentence are unnamed by that correction: it enumerates eight rows under the word
"seven" (the six refused ids plus "the two prose-class rows"), and it says "two prose-class rows"
where the table marks three — `S113` (`:58`), `S123` (`:61`) and `S134` (`:67`), each "the prose class
is stale". The table is the record; the summary sentence is the drift. The closed lesson is not
rewritten (QUALITY 4).

Shown by (lane root):

```
$ sed -n '73p' corpus/lessons/round-40.md | grep -oE 'S1[0-9]{2}' | tr '\n' ' '; echo
S109 S131 S137 S140 S141 S143
$ grep -nE '^\| S(109|131|137|140|141|143) ' corpus/lessons/round-40.md | grep -ci 'refuse'
6
$ grep -ci 'the prose class is stale' corpus/lessons/round-40.md
3
$ grep -nE '^\| S(113|123|134) ' corpus/lessons/round-40.md | cut -d'|' -f1,2
58:| S113 
61:| S123 
67:| S134 
$ awk '/^### Quarantine/{f=1;next} f&&/^\| S[0-9]/{n++} END{print n}' corpus/lessons/round-40.md
17
```

The eight-names count: six ids plus the two prose-class rows named in the parenthesis = 8 names under
the word "seven".

## Bounds of this seat

- Read-only on the lane. Wrote only this file and `T50ScribeCorrections.receipts.md`. No git/jj
  mutation, no fixture repo, no scratch dir (no fixture work was needed), no tool install.
- No counter was run as a verdict. The one checker invocation
  (`.ufo/evidence/round-47/quality/lesson-quote-check.py corpus/lessons/round-46.md`) is a read-only
  probe whose only write path is inside its own `--selftest` tempdir (`:131`); it was run on the
  lesson, not in selftest mode.
- The S259 source was re-opened through the committed snapshot named by
  `corpus/SOURCES.md:134` (`.ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html`,
  sha256 `5eb59adf…`, 51850 bytes), not fetched live. The URL was not re-requested this seat.
- Not decided here: any ledger status, the `fixed`/`open`/`declined` call for the five items, whether
  C1-R50-1's fold declaration satisfies R46.4's "in the lesson itself" literally (QUALITY 4 forbids
  editing the closed lesson, so the appended form is the compliant one), and whether C1-R50-3 should
  be appended on top of `round-41.md:51-58`.

## Summary
- R46.4 has no correction: `round-46.md:42` still prints `9.8 %-16.3 %` (0x2d); the checker exits 1.
- `round-47.md:105`'s green-after is the scratch copy `round46-lesson-dash-restored.md`, not the lesson.
- Siblings conflict: `T50Cross46.md:35` declined vs `T50Disp46.rows.json` open with an in-place edit; QUALITY 4 forbids it.
- C1-R50-1 is the append-only fold declaration; C1-R50-2 (R40.4) and C1-R50-3 (R40.1 supplementary) are the other drafts.
- R44.1 named at `round-45.md:158` + `QUALITY.md:1223-1242` (ea25e022); R47.3 at `round-48.md:106-121`,`:178` (50545328).
- R40.1 counts corrected at `round-41.md:51-58` (b37ce974); the eight-names and two-vs-three drifts remain.
- R40.4 implicit only at `round-41.md:75`; live `r6-snapshot-practice-corpus.md:10` still says 11 words (13 re-counted).
