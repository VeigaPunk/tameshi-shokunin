# SC1 — `corpus/SOURCES.md` draft (round 96)

**Seat:** R96SC1 (scribe). **Lane:** `tameshi`. **Mode:** read-only — nothing under
`corpus/` was written; this file is a draft for the L1 to integrate.

**Verdict: one row must change.** The `used-by` appends for S320-S323 are already in
`corpus/SOURCES.md` (all four rows carry `corpus/lessons/round-96.md` at HEAD `ffb41c8f` —
read with `git show HEAD:corpus/SOURCES.md | grep '^| S32[0-3] '`), so there is no append to
make. But the **S323 row's `anchor` cell still carries the drifted line number `2355`**, and
that is a cell this round's Gate quotes against. The row's own `teaches` cell quotes the
16-word sentence whose located line is **2358**, and the row's `anchor` cell names a
renderer convention that does not produce the number it prints.

## The defect, measured

**Anchor cell (column 6) says `line 2355`.** Under the lane's canonical renderer
(`.ufo/waves/round-93/w1/R93S1-tagstrip.py`, `strip_tags`: script/style and comments
removed, each tag → one space, entities unescaped, lines right-trimmed) the quoted sentence
occupies lines **2358–2359**:

```
2355: ''                                   <- the anchor's line: blank
2356: ' 4.4 Indented code blocks'
2357: ''
2358: ' An  indented code block  is composed of one or more'
2359: ' indented chunks  separated by blank lines.'
```

Receipt: this seat's own re-measurement, `.ufo/waves/round-96/w1/R96SC1-locate.txt`
(canonical renderer, `locate()` over `.ufo/evidence/round-96/sources/s323.html`,
sha256 `c85f56cc…`): `S323 words=16 in_norm_text=True spans=[(2358, 2359)]`. The same
measurement over the byte-identical round-95 snapshot (`.ufo/evidence/round-95/sources/s323.html`,
same sha256 `c85f56cc…`) gives the same span. The scout's independent locator receipt
`.ufo/waves/round-96/w1/R96S1-quotes.txt` records the same line (`S323 2358`).

**The anchor's stated convention does not yield its own number.** The cell says
"(tag-stripped: tags replaced by one space, lines right-trimmed)". Under *that* convention
(tags → one space, script/style blocks **not** removed) the same sentence is at **2463–2464**,
not 2355 — so `2355` is wrong under **both** readings:

| renderer | S323 sentence span |
|---|---|
| canonical lane renderer (`R93S1-tagstrip.py` `strip_tags`) | **2358–2359** |
| the anchor cell's own stated convention (tags → one space only) | 2463–2464 |
| the anchor cell's printed number | 2355 (blank line under the canonical renderer) |

Receipt: `.ufo/waves/round-96/w1/R96SC1-renderer-variants.txt` (both renderers over the same
committed bytes) and `.ufo/waves/round-96/w1/R96SC1-heading-anchors.txt` (§4.4 heading at
line 2356 under the canonical renderer).

**This is D1, still open in the registry.** `corpus/lessons/round-95-verifier-spotcheck.md`
routed D1 ("Gate cited line numbers are off by 3–4 under the Gate's own stated renderer")
and its row table says of S323: *"disagree on the cited line … `line 2355` does not carry it
under the Gate's stated renderer — the sentence starts at 2358 (see D1)"*. The round-95
scribe's own draft (`round-95/w1/SC1-sources.append.md`, Part 1a, column 6) proposed
**line 2358** for this cell; the landed row carries 2355 instead. `git log -S"line 2358" --
corpus/SOURCES.md` returns nothing: 2358 was never landed in the registry.

**Why it is a row change and not only a lesson change.** QUALITY 172 requires that a cited
line be *"a line the record's named snapshot rendering shows carrying the sentence"*. The
registry row is a record of its own evidence, and this cell is the registry's own citation
of the sentence its `teaches` cell quotes. A reader who opens the named snapshot at the
named line finds a blank line. The fix is one cell in one row.

## The change — S323, 11 columns, old → new

Nine of the eleven cells are unchanged. The change is in **column 6 (`anchor`)** only: the
line number `2355` → `2358`, and the convention parenthetical corrected to the one that
produces it. Column 7 (`teaches`) already carries `(16 words)`, verified by
`len(q.split())` = 16, and stays as it is.

| # | column | old | new |
|---|---|---|---|
| 1 | id | `S323` | `S323` (unchanged) |
| 2 | source | `CommonMark Spec 0.31.2 — Indented code blocks — https://spec.commonmark.org/0.31.2/` | unchanged |
| 3 | kind | `docs` | unchanged |
| 4 | tier | `A` | unchanged |
| 5 | scope | `why the round-95 note reader treats a 4+-space-indented line as literal text, never a table row or the note's figure` | unchanged |
| 6 | **anchor** | `§4.4 Indented code blocks, tag-stripped snapshot `.ufo/evidence/round-95/sources/s323.html` line **2355** (tag-stripped: tags replaced by one space, lines right-trimmed) @ page fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 10:41:46 GMT; 514698 B; sha256 c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d)` | `§4.4 Indented code blocks, tag-stripped snapshot `.ufo/evidence/round-95/sources/s323.html` line **2358** (tag-stripped per the lane renderer `.ufo/waves/round-93/w1/R93S1-tagstrip.py`: script/style and comments removed, each tag → one space, entities unescaped, lines right-trimmed; the sentence spans 2358–2359) @ page fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 10:41:46 GMT; 514698 B; sha256 c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d)` |
| 7 | teaches | `"An indented code block is composed of one or more indented chunks separated by blank lines." (16 words): an indented chunk is literal text, so a presented verdict row inside one is not a keyed table row` | unchanged |
| 8 | status | `mined` | unchanged |
| 9 | opened | `2026-11-08` | unchanged |
| 10 | recheck | `365d` | unchanged |
| 11 | used-by | `corpus/lessons/round-95.md, corpus/lessons/round-96.md` | unchanged |

**The single-line row to land (11 columns, one line):**

```markdown
| S323 | CommonMark Spec 0.31.2 — Indented code blocks — https://spec.commonmark.org/0.31.2/ | docs | A | why the round-95 note reader treats a 4+-space-indented line as literal text, never a table row or the note's figure | §4.4 Indented code blocks, tag-stripped snapshot `.ufo/evidence/round-95/sources/s323.html` line 2358 (tag-stripped per the lane renderer `.ufo/waves/round-93/w1/R93S1-tagstrip.py`: script/style and comments removed, each tag → one space, entities unescaped, lines right-trimmed; the sentence spans 2358–2359) @ page fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 10:41:46 GMT; 514698 B; sha256 c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d) | "An indented code block is composed of one or more indented chunks separated by blank lines." (16 words): an indented chunk is literal text, so a presented verdict row inside one is not a keyed table row | mined | 2026-11-08 | 365d | corpus/lessons/round-95.md, corpus/lessons/round-96.md |
```

## The other three rows

S320, S321 and S322 need **no** cell change:

- **S320** — the row's `anchor` cites the DESCRIPTION sentence without a line number
  (`DESCRIPTION @ page fetched 2026-11-08 … `.ufo/evidence/round-92/sources/s320.html``), so
  there is no line to drift. Its `teaches` cell paraphrases three page sentences rather than
  quoting them — D4's carried observation, *"not a broken citation"*. The round-96 Gate
  quotes them verbatim instead (see `SC1-lesson.md`), which closes the paraphrase gap on the
  reading side without a registry edit.
- **S321** — the row's `anchor` cites `line 4496`; under the canonical renderer 4496 is
  exactly where the row's own quoted sentence starts
  (`.ufo/waves/round-96/w1/R96SC1-locate.txt`: `S321 words=15 in_norm_text=True
  spans=[(4496, 4497)]`). Correct as landed.
- **S322** — the row's `anchor` cites `line 2613`, the §4.5 heading line; the row's `teaches`
  sentence is at 2618–2619 and the heading at 2613, so the anchor points at the section it
  names (`§4.5 Fenced code blocks`), which is what an anchor cell is for. Correct as landed.

## Registry census

Unchanged by this draft: rows 183, tiers A=165 B=14 C=4, status mined=149 queued=23
rejected=11 — read from `corpus/SOURCES.md` at HEAD `ffb41c8f`; the census itself exits 0
both before and after (`.ufo/waves/round-96/census-before.txt`, `.ufo/waves/round-96/census-after.txt`).
This draft changes one cell of one existing row: no row is added, removed, or re-statused,
so no census number moves.

## What the L1 must decide

Landing this cell edits `corpus/SOURCES.md`, which this seat does not touch. Two options,
both defensible, and the second is the one this draft recommends:

1. **Land the anchor fix now** (one cell, S323 column 6). Closes the registry half of D1 in
   the round that measured it.
2. **Defer to round 97** and carry it in that round's source append, as an erratum-style
   note in the meantime. Also defensible, and it costs nothing this round — the round-96
   Gate quotes line 2358 and does not rely on the registry anchor.

If option 2 is chosen, the round-96 lesson must carry the D1 residue as a named limit, not
silently, or a reader comparing the lesson's 2358 with the registry's 2355 finds a
contradiction with no explanation.
