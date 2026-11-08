# R93SC1 — draft block 1: the case note's round-93 status block

**For:** TameshiR93 (L1), for integration into
`corpus/knowledge/mutation-case-fleet-sources-census.md`.
**Lane mode:** read-only; this seat wrote nothing under `corpus/`.

## What the L1 must decide before integrating

The committed note **already carries** a round-93 section — `## Certification attempt
(appended round 93) — the verdict-content reader`, at lines 277-295 of the note blob
`b529c3e4` (committed `9cad4f6e`, the instrument-rev-A commit). The text between the
markers below is drafted as a **replacement for that section**, not as a second round-93
section: it keeps the section's existing opening (the round-92 kill and the reader's
shape rule) and adds the three things the seat asks for — the located quotes for S320,
S321 and S322, an explicit statement of what the reader certifies, and an explicit
statement of what it does **not** certify. If the L1 prefers append-only, the same text
works as an amendment section titled `## Certification attempt (appended round 93,
amended) — the verdict-content reader`; the wording contains no admission claim either
way.

**Hard constraints this block obeys** (all three verified by probe, see
`R93SC1-note-block-fixture.out`):

1. **No second verdict table.** The block contains no pipe table at all, so the reader's
   `verdict_tables` stays 1.
2. **No stray verdict token.** No line carries two or more pipes, so the reader's
   one-rule stray-verdict scan finds nothing outside the verdict table.
3. **No second figure.** No line begins with `measured:`, so the reader's
   `measured: (\d+)/(\d+) killed` figure conjunct still sees exactly one block-level
   figure — the note's own `5/12 killed` line.

Applying the block to a clone of the instrument revision and re-running the frozen
counter yields `C1_R93_PASS=true`, exit 0, `verdict_tables=1 badrows=0 mismatched=0`,
all nineteen conjuncts true — i.e. **the drafted block does not break the certificate it
documents**.

--- BEGIN INTEGRATION TEXT ---

## Certification attempt (appended round 93) — the verdict-content reader

Appended; the entry and the round-92 block above are unchanged. Round 92's counter was
killed by its own rule: it refused this note when the §2b impact table below was
reformatted so its ids became cells of their own, because the reader keyed every
id-shaped row instead of the rows that assert a verdict. Round 93's successor,
`.ufo/evidence/round-93/c1/measure-v93.py` (sha256 `18903602aa040b7e…`, instrument
revision `855f0c1c`), reads the note by table shape: a table is a verdict table only when
its **header row** carries a `verdict` cell (GFM tables — one header row and one
delimiter row; S321: "The table is broken at the first empty line, or beginning of
another block-level structure" and "a single header row, a delimiter row separating the
header from the data", `.ufo/evidence/round-93/sources/s321.txt:4496-4497` and
`:4395-4396`),
fenced blocks are literal content and not block structure (CommonMark — S322: "A fenced
code block begins with a code fence, preceded by up to three spaces of indentation.",
`.ufo/evidence/round-93/sources/s322.txt:2618-2619`), and only the rows inside that one
table are keyed. An id-keyed table that asserts no verdict is not a verdict table and
does not refuse this note; a second table that carries verdict tokens under any header
does. The self-pin the counter checks before any other action is the sha256 of its own
bytes with the pin line removed — S320: "Print or check SHA256 (256-bit) checksums."
(`.ufo/evidence/round-93/sources/s320.html:88`; the same sentence at
`.ufo/evidence/round-92/sources/s320.txt:19`).

**What the reader certifies.** The twelve cells of the single verdict table above — one
cell per spec id `C01` to `C12`, in the header-named `verdict` column — agree with the
verdicts the counter itself re-derives, by re-running the pinned gate's own `selftest`
twice per mutant against the fleet's `scripts/sources-census.sh` at `f47ad6ba` (sha256
`3fb72615…4e30`); the note's `measured: 5/12 killed` figure matches the re-derived kill
count; every survivor's witness registry is rebuilt and differs between pristine and
mutant; the spec still carries its twelve ids; and the source and coverage links the
round requires are present (S320, S321 and S322 mined, each quoting its committed
snapshot). The commit's own receipt is `C1_R93_PASS=true`, exit 0, with
`verdict_tables=1`, `badrows=0`, `mismatched=0`.

**What the reader does not certify.** It certifies the twelve cells and nothing about
how they were obtained: a note that copies the committed predictions instead of the
measured receipt carries the same twelve cells and passes, because the reader compares
the cells against its own re-execution, not against the provenance of the text. It does
not certify a fenced presentation: a fenced table, or a fenced figure line, is literal
text (S322) and is neither keyed nor counted, so the figure it checks is the block-level
one. And it does not certify a table whose header row carries no `verdict` cell: such a
table is not a verdict table at all (S321), so it is never refused — §2's survivor table
and §2b's impact table are outside the reader's scope, by construction rather than by
accident.

Admission is the non-author closure's.

--- END INTEGRATION TEXT ---

## Located quotes used (verified by probe)

`R93SC1-located-quotes.py` / `.out` reproduce the counter's own rule (a quoted span of
at most 25 words on a line naming the id, whose text occurs in the committed snapshot)
at revision `855f0c1c`:

| id | quote | words | snapshot | accepted |
|---|---|---|---|---|
| S320 | "Print or check SHA256 (256-bit) checksums." | 6 | `.ufo/evidence/round-93/sources/s320.html` (sha256 `b968bc09…`) | yes |
| S321 | "The table is broken at the first empty line, or beginning of another block-level structure" | 15 | `.ufo/evidence/round-93/sources/s321.html` (sha256 `b153d814…`) | yes |
| S321 | "a single header row, a delimiter row separating the header from the data" | 13 | same | yes |
| S322 | "A fenced code block begins with a code fence, preceded by up to three spaces of indentation." | 17 | `.ufo/evidence/round-93/sources/s322.html` (sha256 `c85f56cc…`) | yes |

No other quoted span on a lesson line naming these ids is accepted, so the block quotes
exactly the sentences the counter's `source` conjunct is satisfied by.

## Evidence pointer for the block's claims

- Reader shape rule and the two limits: `.ufo/evidence/round-93/c1/measure-v93.py`
  (sha256 `18903602aa040b7e258fd6c81491cfee4ea7bb0575784fe27e351587fe094c2d`),
  `parse_note` and `block_lines`.
- The certification receipt: `.ufo/evidence/round-93/pre-freeze/controls/pos-real.out`
  (`C1_R93_PASS=true`, exit 0, nineteen conjuncts true).
- The honest states that must also pass: `pos-honest-a13.out` (the §2b table keyed by
  id) and `pos-honest-verdict-cell.out` (a data cell whose text is exactly `verdict`).
- The counter run at the instrument revision, re-run by this seat:
  `R93SC1-counter-at-freeze.out` (exit 0, `C1_R93_PASS=true`).

VERDICT: drafted
TOOLS: none
