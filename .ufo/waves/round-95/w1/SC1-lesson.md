# SC1 — `corpus/lessons/round-95.md` draft (round 95)

**Seat:** R95SC1 (scribe). **Lane:** tameshi. **Mode:** read-only — nothing under
`corpus/` was written; this file is a draft for the L1 to integrate.

**Read first.** The L1's instruments commit `0685c358` already landed a
`corpus/lessons/round-95.md`, and the L1's `20fabad4` ("lesson Gate reflow — each S32x
quote on its sid line") fixed the Gate's shape after R95R1's finding. **That fix
worked**: the counter at the current HEAD `3ca1981a` now prints
`C1_SOURCE S320=row:1,quote:1 S321=row:1,quote:1 S322=row:1,quote:1 S323=row:1,quote:1`,
`source=true`, `C1_R95_PASS=true`, exit 0 (re-measured by this seat).

What this draft corrects is the layer the reflow did not touch: **the numbers written
by hand inside the Gate and inside the `S323` registry row**. Measured at HEAD, four of
the six Gate lines cite a line that does not carry their quote, and five of the six
mis-state their quote's word count (the table in `## Mistakes` M4). This draft's Gate
carries the located line and the printed word count on every line.

**Format rule this draft obeys (the counter's rule, not a stylistic choice).**
`measure-v95.py:386` `located_quotes` collects a double-quoted span from a line **only if
that same line names the sid**, keeps those of `1 ≤ len(q.split()) ≤ 25` words, and the
`source` conjunct then requires the quote's `norm_text` to occur in the snapshot's
`norm_text` (`measure-v95.py:378`). The landed lesson satisfies the shape (that was
`20fabad4`); what it did not satisfy is that its quoted spans are the sentences the
snapshots carry and that its counts and lines are the measured ones.

---

## Gate

Sources opened for this round's rows (all four fetched 2026-11-08; the snapshot paths
are the bytes the round-95 counter reads). The quoted sentence on each line is the
located sentence the row's `teaches` rests on. **Line convention:** the tag-stripped
snapshot — HTML text extraction, one output line per source line, each line stripped;
this convention reproduces the committed round-93 `sources/s321.txt` and `s322.txt`
**byte-for-byte** from their `.html` originals (verified `True` for both), so the line
numbers here are the ones a reader gets by applying the same extraction. **Word counts**
are printed by `len(q.split())`, the tokenizer `measure-v95.py:386` uses. Each quoted
span sits on the line that names its sid, which is what `located_quotes` requires.

- S320 sha256sum(1) — `https://man.archlinux.org/man/sha256sum.1.en`, fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 08:53:29 GMT; snapshot `.ufo/evidence/round-95/sources/s320.html`, sha256 `b968bc09…2777b`, 12 127 B), tag-stripped line 88: "Print or check SHA256 (256-bit) checksums." (6 words) — the digest the `SELF_SHA256` pin computes and the audit compares is a sha256 of the counter bytes.
- S321 GitHub Flavored Markdown Spec — `https://github.github.com/gfm/`, fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 08:53:23 GMT; snapshot `.ufo/evidence/round-95/sources/s321.html`, sha256 `b153d814…a220`, 508 310 B), tag-stripped line 4496: "The table is broken at the first empty line, or beginning of another block-level structure" (15 words) — a following indented chunk ends a table, so it cannot extend an earlier verdict table. Also tag-stripped line 4396: "a single header row, a delimiter row separating the header from the data" (13 words) — the table shape the reader keys. And tag-stripped line 4403: "The delimiter row consists of cells whose only content are hyphens" (11 words) — one hyphen is a legal delimiter cell, which is the round-95 A5 rule. The span is quoted without the parenthesised code element, because the two normalisers render it differently: the counter's `norm_text` (tags → a space) gives `hyphens ( - )` while the tag-stripped text gives `hyphens (-)`, so only the prefix is in both.
- S322 CommonMark Spec 0.31.2 — Fenced code blocks — `https://spec.commonmark.org/0.31.2/`, fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 08:53:28 GMT; snapshot `.ufo/evidence/round-95/sources/s322.html`, sha256 `c85f56cc…60f0d`, 514 698 B), tag-stripped line 2618: "A fenced code block begins with a code fence, preceded by up to three spaces of indentation." (17 words) — a fence opens literal text, the declared limit the reader already held.
- S323 CommonMark Spec 0.31.2 — Indented code blocks — `https://spec.commonmark.org/0.31.2/`, fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 10:41:46 GMT; snapshot `.ufo/evidence/round-95/sources/s323.html`, sha256 `c85f56cc…60f0d`, 514 698 B — the same page bytes as S322), tag-stripped line 2358: "An indented code block is composed of one or more indented chunks separated by blank lines." (16 words) — an indented chunk is literal text, so a presented verdict row inside one is not a keyed row; this is the round-95 A2 rule.

Two further sentences from the same page are **not** usable as the lesson's quoted span
and are recorded here so the next round does not pick them: "The contents of the code
block are the literal contents of the lines, including trailing line endings, minus four
spaces of indentation." (22 words) and "An indented code block has no info string." (9
words) are verbatim in the document but **absent from the snapshot's `norm_text`** (the
tag-strip leaves a space before the comma, so the collapsed text reads `line endings ,
minus` and `info string .`). Measured: `norm_text(q) in norm_text(snapshot)` → `False`
for both, `True` for the sentences used above. The usable §4.4 alternative is
tag-stripped line 2360: "An indented chunk is a sequence of non-blank lines, each
preceded by four or more spaces of indentation." (18 words) — `norm_text` match `True`.

Rejected this round: none. Rows re-opened: S320, S321, S322 (status unchanged, `mined`;
`used-by` appended). Row added: S323 (`mined`, `used-by` = this lesson).

## Erratum — the round-94 C2 tally sentence (routed defect 1)

The frozen round-94 record says `DISPOSITION_SELFTEST: 8/8 pass` in three places —
`plans/round-94.plan.md:165`, `LOG.md:5085` ("8/8 (QUALITY 166)") and
`corpus/lessons/round-94.md:66` — while the operative committed receipt
`.ufo/evidence/round-94/pre-freeze/c2-selftest.out:10` prints
`DISPOSITION_SELFTEST: 9/9 pass` (rev 2 added the `a4-prose-state-word-cheat` case; rev 3
kept it). A1 of that round declared "No claim wording, predicate, state expectation or
target changes", which is false for that tally, so C2 was filed as `unprovable`.

This paragraph is the erratum: the superseded sentence is `DISPOSITION_SELFTEST: 8/8 pass`
as recorded at the three pointers above; the operative tally is `9/9`, and the frozen
files are not edited. QUALITY 169 records the rule.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **number-drift**: a frozen self-assessment tally was written from an earlier instrument revision and never reconciled with the operative receipt; the claims table and SCORECARD printed 9/9 while the plan, LOG and lesson printed 8/8. | `plans/round-94.plan.md:165` and `corpus/lessons/round-94.md:66` vs `.ufo/evidence/round-94/pre-freeze/c2-selftest.out:10` (`9/9 pass`); found by the round-94 closure. | none — QUALITY 168 checks quoted receipt lines, and this was a frozen predicate line; no rule compared a frozen tally to its receipt at freeze time. | the erratum above plus QUALITY 169; every frozen tally now cites its receipt path at freeze. |
| M2 | **vacuous**: the first `escaped-backslash-pipe` fixture was not discriminating — a four-column note whose witness cell ended in `C:\\` before a space-separated delimiter is padded by the round-94 reader, the verdict stays in its column, and v94 prints `C1_R94_PASS=true`. | `.ufo/evidence/round-95/pre-freeze/before-v94/escaped-backslash-pipe.out` (the corrected five-column run: exit 1, `ids=false`, `width:9:cells=4`); the non-discriminating construction is recorded in `plans/round-95.plan.md` §A1. | the round's own do-nothing control (a fixture the claimed work must change; v94 passed it, so the fixture was wrong). | plan §A1: five-column fixture with the verdict cell immediately after `\\|`. |
| M3 | **scope**: the first `double-pin` fixture inserted the decoy pin line *after* the real constant, so the decoy became the constant Python executes and v94 died `self-pin-mismatch` — the state did not discriminate the single-pin rule. | `.ufo/evidence/round-95/pre-freeze/before-v94/double-pin.out` (corrected: exit 0, `C1_R94_PASS=true`); the after-insert variant printed `C1_SETUP self-pin-mismatch`, exit 2. | the same do-nothing control. | plan §A2: the decoy goes before the real pin line; the executed constant stays the real digest. |
| M4 | **number-drift**: the round's own record wrote its quote word counts and its snapshot line numbers by hand, and both are wrong against the committed bytes — five of the six Gate lines mis-state their quote's word count, four cite a line that does not carry their quote, and the `S323` registry row repeats both errors (`(15 words)`, `line 2355`). | at HEAD `3ca1981a`: `corpus/lessons/round-95.md:16–21` — S321's delimiter quote claims `(20 words)` but the span as written is 24 tokens and is not in the tag-stripped text at all (it is the `norm_text` rendering, `hyphens ( - )`, where the text reads `hyphens (-)`); S321's header-row quote claims `(20 words)` but is 19; S323's quote claims `(15 words)` but is 16; and the cited lines `85`, `4400`, `4393`, `4493`, `2616`, `2355` carry, respectively, blank text, an unrelated sentence, a heading sentence, blank text, a different sentence and blank text — the lines that carry the quotes are 88, 4403, 4396, 4496, 2618 and 2358. `corpus/SOURCES.md:199` carries the same two errors. | none — QUALITY 168 checks that a quoted receipt line is byte-backed, and QUALITY 87 checks that a quote's length is printed by a command; neither checks that the **line** a record cites carries its quote, nor that a registry row's anchor line locates its own quote. | every Gate line now carries the line that carries its quote and its word count printed by `len(q.split())`, and the `S323` row's `teaches`/`anchor` cells carry `(16 words)` and `line 2358`; QUALITY 171 and 172 (this round) carry the two rules. |
| M5 | **number-drift**: the round-95 plan's `§Wave` declares 12 seats while the committed dispatch that executed the wave names 13 — the same plan-versus-wave roster defect the round-94 closure routed as its item 4. | `plans/round-95.plan.md:172` ("One v1 wave `w1`, 12 seats") vs `.ufo/waves/round-95/w1-dispatch.json` `counts.total=13` and its 13 registry members (roles: executor 4, reviewer 2, scribe 1, scout 1, critic 1, mutation-tester 1, sentinel 1, connector 1, revenger 1) — the 13th is the L1's own `revenger` seat `R95L1`. The freeze commit `0d3fc99b` subject line says "w1 spec (13 seats)", so the plan's roster and the dispatch it points at disagree inside the same commit. | none — the census and the counter never compare the plan's seat list with the dispatch's member count. | the plan's §Wave names 13 seats and lists the `revenger` role; the roster count is printed by `python3 -c "import json;print(json.load(open('.ufo/waves/round-95/w1-dispatch.json'))['counts']['total'])"` rather than written by hand. |

## Registry changes

| row | field | old | new |
|---|---|---|---|
| S320 | used-by | `corpus/lessons/round-92.md, corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | `corpus/lessons/round-92.md, corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-95.md` |
| S321 | used-by | `corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | `corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-95.md` |
| S322 | used-by | `corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | `corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-95.md` |
| S323 | added | — | `mined`, `corpus/lessons/round-95.md` |

Census before (round start): `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` exit 0; rows 182; tiers A=164 B=14 C=4; status
mined=148 queued=23 rejected=11 (`.ufo/waves/round-95/census-before.txt`). Census after
is recorded in the round report with its exit code.

## Measurements

Filled at the records commit from the committed receipts; every number below is a line a
command printed, never a projection.
