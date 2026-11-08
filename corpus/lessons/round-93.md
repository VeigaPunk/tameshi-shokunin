# Round 93 — lesson (tameshi)

Base `4a7e259b407d582d2010197f32d7524d6bed5370` (round-92 verifier spot-check tip).
Two claims this round: R93-C1, coverage — the fourth attempt at certifying the round-90
fleet-gate mutation case, under a reader that refuses on verdict content instead of id
shape; R93-C2, calibration — every conjunct of that counter falsifiable by a committed
battery state or declared unfalsifiable with its reason.

## Gate

| Item | Decision | Source opened this round | Reason |
|---|---|---|---|
| S321 GitHub Flavored Markdown Spec, §4.10 Tables (extension) | admit (A, `mined`) | https://github.github.com/gfm/, fetched 2026-11-08, HTTP date `Sun, 08 Nov 2026 07:35:12 GMT`, 508 310 B, sha256 `b153d814fdfc8624bb6da7449162c1cd707a637f7d1c1b636eb44b9cf63fa220` (`.ufo/evidence/round-93/sources/s321.html`, headers `s321.headers`, text `s321.txt`) | "The table is broken at the first empty line, or beginning of another block-level structure" (15 words, `sources/s321.txt:4496`, wrapped over two lines) and "a single header row, a delimiter row separating the header from the data" (13 words, `:4396`). This is the ground for the reader's central move: a table is a bounded block with its own header, so a verdict table is identified by its own header row and rows outside it are never its rows. |
| S322 CommonMark Spec 0.31.2, §4.5 Fenced code blocks | admit (A, `mined`) | https://spec.commonmark.org/0.31.2/, fetched 2026-11-08, HTTP date `Sun, 08 Nov 2026 07:35:12 GMT`, 514 698 B, sha256 `c85f56cc2101f761cc94215c677cd2c7c1ecca9c47be016479fdfe718af60f0d` (`.ufo/evidence/round-93/sources/s322.html`, headers `s322.headers`, text `s322.txt`) | "A fenced code block begins with a code fence, preceded by up to three spaces of indentation." (17 words, `sources/s322.txt:2619`). Grounds the reader's fence rule and, with it, the declared limit that a fenced pipe row or a fenced `measured:` line is literal text rather than the note's table or figure — the limit is now stated in the plan at the same scope the reader enforces. |
| S320 sha256sum(1) re-opened (admitted round 92) | re-opened, no status change | https://man.archlinux.org/man/sha256sum.1.en, fetched 2026-11-08, HTTP date `Sun, 08 Nov 2026 07:35:12 GMT`, 12 127 B, sha256 `b968bc09839877f9b0bf892b8a37fce0f72f4fa0ff0f17208824161b8547277b` — byte-identical to round 92's snapshot | "Print or check SHA256 (256-bit) checksums." (6 words, `sources/s320.txt:19`). Re-opened because this round's `source` conjunct requires a located quote that occurs in a committed snapshot, so the pin's ground had to be re-checked rather than inherited on the round-92 receipt. |
| Candidate: relax round 92's `ID_SHAPE` to accept three-digit ids | reject | `.ufo/evidence/round-92/c1/measure-v92.py` `parse_note`; round-92 `T92C1` receipts | Widening the id shape keeps the defect that killed R92-C1: the reader still keys id-shaped rows, so the A13 reformat (an honest impact table with its ids in their own cells) refuses an honest note again, and the hidden `C001`-`C012` table still needs a second defence. The fix is a different keying rule, not a wider pattern. Flip: re-admit only if a reader keyed on id shape can be shown to accept every honest note the lane's corpus can construct. |
| Candidate: key a `measured:` line inside a fenced block | reject | `.ufo/waves/round-92/w1/T92C1-A7-measured-in-fence.out`; S322 §4.5 | The fence opens a literal block, so a `measured:` line inside it is example text, not the note's figure. Keying it would refuse an honest note that quotes a figure in a code block — the exact class that killed R92-C1. The declared limit names the fenced figure instead. Flip: re-admit only with a source that gives fenced block content block-structure semantics. |

## Claim and kill

See `plans/round-93.plan.md` for the frozen predicate, the enumerated hostile-state set
and the declared limits. This file records the gate above at the instrument revision; the
`## Mistakes`, `## Measurements` and `## Wave` sections are appended in the records commit.
