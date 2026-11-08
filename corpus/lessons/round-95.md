# Round 95 — the note reader's literal classes and the audit's receipt bytes

Lane `tameshi`, round 95 (2026-11-08). Base `02ff6290945dde18062a366799a774abb50fb365`.
Claims: C1 coverage (five presentation states in the successor note reader) and C2
calibration (the disposition audit reads receipt bytes from the object store). Frozen
before data in `plans/round-95.plan.md` and `.ufo/waves/round-95/claims.json`.

## Gate

Sources opened for this round's rows (all four fetched 2026-11-08; the snapshot paths are
the bytes the round-95 counter reads). Each sid line below carries its located quote on the
same line — the counter's `located_quotes` collects a quoted span only from a line naming
its sid. Line numbers are in the tag-stripped snapshot (tags replaced by spaces, entities
unescaped, whitespace collapsed: the counter's `norm_text`).

- S320 sha256sum(1) `https://man.archlinux.org/man/sha256sum.1.en` fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 08:53:29 GMT; `.ufo/evidence/round-95/sources/s320.html` sha256 `b968bc09…`), line 85: "Print or check SHA256 (256-bit) checksums." (6 words) — the digest the `SELF_SHA256` pin computes and the audit compares is a sha256 of the counter bytes.
- S321 GFM Tables `https://github.github.com/gfm/` fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 08:53:23 GMT; `.ufo/evidence/round-95/sources/s321.html` sha256 `b153d814…`), line 4400: "The delimiter row consists of cells whose only content are hyphens ( - ), and optionally, a leading or trailing colon ( : )" (20 words) — one hyphen is a legal delimiter cell, which is the round-95 A5 rule.
- S321 GFM Tables, line 4393: "a single header row, a delimiter row separating the header from the data, and zero or more data rows" (20 words) — the table shape the reader keys, which is why an indented row outside a table is not a verdict row.
- S321 GFM Tables, line 4493: "The table is broken at the first empty line, or beginning of another block-level structure" (15 words) — a following indented chunk ends a table, so it cannot extend an earlier verdict table.
- S322 CommonMark 0.31.2 Fenced code blocks `https://spec.commonmark.org/0.31.2/` fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 08:53:28 GMT; `.ufo/evidence/round-95/sources/s322.html` sha256 `c85f56cc…`), line 2616: "A fenced code block begins with a code fence, preceded by up to three spaces of indentation." (17 words) — a fence opens literal text, the declared limit the reader already held.
- S323 CommonMark 0.31.2 Indented code blocks `https://spec.commonmark.org/0.31.2/` fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 10:41:46 GMT; `.ufo/evidence/round-95/sources/s323.html` sha256 `c85f56cc…`, the same page bytes as the fenced-code snapshot above), line 2355: "An indented code block is composed of one or more indented chunks separated by blank lines." (15 words) — an indented chunk is literal text, so a presented verdict row inside one is not a keyed row; this is the round-95 A2 rule.

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

## Registry changes

| row | field | old | new |
|---|---|---|---|
| S320 | used-by | `corpus/lessons/round-92.md, corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | `…, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-95.md` |
| S321 | used-by | `corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | `…, corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-95.md` |
| S322 | used-by | `corpus/lessons/round-93.md, corpus/lessons/round-94.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | `…, corpus/knowledge/mutation-case-fleet-sources-census.md, corpus/lessons/round-95.md` |
| S323 | added | — | `mined`, `corpus/lessons/round-95.md` |

Census before (round start): `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` exit 0; rows 182; tiers A=164 B=14 C=4; status
mined=148 queued=23 rejected=11 (`.ufo/waves/round-95/census-before.txt`). Census after is
recorded in the round report with its exit code.

## Measurements

Filled at the records commit from the committed receipts; every number below is a line a
command printed, never a projection.
