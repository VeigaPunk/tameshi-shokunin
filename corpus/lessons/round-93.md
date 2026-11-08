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

## Registry changes logged this round

| Row | Field | Old | New | Why |
|---|---|---|---|---|
| S320 | `used-by` | `corpus/lessons/round-92.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | `corpus/lessons/round-92.md, corpus/lessons/round-93.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | This round re-opened S320 and its `source:` conjunct (QUALITY 157) requires the row's used-by to name the lesson that carries the located quote. No status, tier or recheck change. |
| S321 | added (new row) | — | tier A, `mined`, `used-by` = `corpus/lessons/round-93.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | Opened this round; grounds the table-shape rule the reader keys on. |
| S322 | added (new row) | — | tier A, `mined`, `used-by` = `corpus/lessons/round-93.md, corpus/knowledge/mutation-case-fleet-sources-census.md` | Opened this round; grounds the fence rule and the fenced-figure limit. |

## Claim and kill

See `plans/round-93.plan.md` for the frozen predicate, the enumerated hostile-state set
and the declared limits. This file records the gate above at the instrument revision; the
`## Mistakes`, `## Measurements` and `## Wave` sections are appended in the records commit.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **the positive control's transform was not honest.** `controls-v93.py`'s `pos-honest-a13` edit replaced `\| C03 ` -> `\| C03 \| ` across the whole note, so it also corrupted the twelve verdict rows (`mismatched=3 badrows=3`): the "honest note" state was not honest, and the control could not have shown the QUALITY 154 fix. | first full battery run: `.ufo/evidence/round-93/pre-freeze/controls-firstrun/pos-honest-a13.out` (`C1_R93_PASS=false`, `badrows=3`) and its summary `states=35 matched=34 mismatches=1 [pos-honest-a13]`; fixed driver `69d377a0`, receipt `.ufo/evidence/round-93/pre-freeze/controls/pos-honest-a13.out` (`true`) | the battery itself — the state expected PASS and graded MISMATCH — but nothing *before* the run checked that the fixture transform hit only its intended table | the replacements are scoped to the impact-table cell text; a fixture assertion (the transformed note must still parse to twelve rows) is the round-94 addition. Able to fail: the kept first-run receipt |
| M2 | **a duplicated rule hid which removal was load-bearing.** The stray-verdict rule existed twice (per-table and per-block-line); `D01` removed only the second copy, so the mutant still refused `renamed-result` and the control read `MISMATCH`, not `PASS`. | first subset run `D01.out` (`mutant=D01 state=renamed-result`, `exit=1`, `C1_R93_PASS=false`); the counter now states the rule once, outside the verdict table (`measure-v93.py` rev `855f0c1c`), and `D01` prints `C1_R93_PASS=true` | the removal-mutant control itself; no rule required a rule to have one implementation site | QUALITY 159. Able to fail: the D01 control (a rule with two sites leaves the mutant alive) |
| M3 | **the claim's own count was wrong.** §Controls named twenty-three hostile states and the claim sentence said "twenty-five" — the exact class (wording wider than the instrument) this round exists to close, found by counting before any seat scored. | `plans/round-93.plan.md` §Controls table (23 rows) vs the pre-fix sentence; fix `4643b6ff` | none — no check compared the claim's number with the plan's own table | a freeze checklist item: every count in a claim sentence is recomputed from the table it names. Corrected pre-scoring, so the claim was never scored against the wrong number |
| M4 | **the lint was curated after the instrument revision.** At `855f0c1c` the new counter scores `defences=4/8` under the lane's lint (the pattern set still demanded shape-keyed id refusal and a hand-copied `SPEC_SHA`); the curation `7626412` makes the freeze tree `8/8`. | `R93E2.md` row 6 (`defences=4/8`, exit 1, twice) and `.ufo/evidence/round-93/hardening/lint-v93.out` (`8/8`) | QUALITY 153 read as "linted before its freeze" while the freeze tree also carries the curation — the ordering must be stated, and an instrument revision is not the freeze | the counter's defence set is a *successor* set: QUALITY 154 retired shape keying, and the lint's entries now admit the successor forms with the supersession written in its docstring. Able to fail: `lint-v91.out` still reads 5/8 (the lint still bites) |
| M5 | **the seal's root of trust was the lane's own spec.** `pin` compares the spec's declared digest to the blob the same spec names, and `pins` compares derived values to a lane-committed `pins.json`; one commit repointing the spec and regenerating pins makes the counter execute a foreign gate while printing `pin=true pins=true green=true canary=true`. | `.ufo/waves/round-93/w1/R93SN1-probe18.log` and `R93SN1.md` F1; control arm (untouched lane) shows no foreign marker | the sentinel seat; the plan's own limit sentence ("the gate bytes are pinned, so no committed lane state can falsify") was the false part | plan amendment A3 (certificate is revision-bound); round-94 remediation: anchor the gate identity in the counter's self-pinned bytes and `die` on disagreement. Able to fail: probe18 |
| M6 | **`coverage` was fence-blind.** The note reader skips fenced blocks; the README scan does not, so a fenced row appended after a committed denial flipped `coverage` to true. | `.ufo/waves/round-93/w1/R93R1-probe4.py` output and `R93R1.md` finding 2 | the reviewer seat; the plan's blanket limit said fenced blocks are literal | plan amendment A1; round-94 fix routes the README scan through `block_lines` and requires the path as its own cell (the substring test also matches a longer filename). Able to fail: probe4 |
| M7 | **the width guard read the wrong row.** `tables()` does not return the delimiter row, so `len(delim) != len(header)` compares the header to the first *data* row and the delimiter's cell count is never checked: a GFM-invalid table is keyed. | `.ufo/waves/round-93/w1/R93R1.md` finding 1, `R93C1.md` finding 1 (both ran the same probe), `R93S1.md` observation | two independent seats; the plan's limit list did not name any width rule | plan amendment A2; round-94 fix returns the delimiter cells and adds a `delim` finding. Able to fail: the R93R1 probe (5-cell header over a 3-cell delimiter still keyed) |
| M8 | **QUALITY 158 held only at conjunct granularity.** Every one of the 19 conjuncts moves in a named receipt, but eight reader *rules* have no discriminating state (source's occurrence half, both width halves, position, figure-exactly-one, verdict-column count, fence, spec count). | `.ufo/waves/round-93/w1/R93M1.md` Q2 and `R93M1-sharp-output.txt` (states the battery lacks) | the mutation-tester seat; C2 audits conjunct keys and has no notion of sub-rules | plan amendment A6; round-94 adds the sharpened states. C2's wording is conjunct-level, so it does not overclaim — the gap is stated, not hidden |
| M9 | **the M4 receipt guard had holes.** A pre-existing dangling symlink in `--outdir` makes the receipt write land outside the outdir, and a planted higher-index `<name>.rerun-9.out` outranks a fresh receipt in the summary. | `.ufo/waves/round-93/w1/R93SN1.md` F2/F3 with its probe logs | the sentinel seat; my own M4 fix covered only the plain overwrite | round-94: `O_NOFOLLOW`/`lstat` refusal and a run-scoped receipt directory. Able to fail: the R93SN1 probes |
| M10 | **the driver's mutating git calls inherited the ambient environment.** `controls-v93.py` clones/commits without scrubbing `GIT_*`, so an exported `GIT_DIR` diverts the fixture commit and an ambient hook executes — the class QUALITY 27 exists for, on this round's own driver. | `.ufo/waves/round-93/w1/R93SN1.md` F6 | the sentinel seat | round-94: `sealed_env()` on every driver git call plus the canary selftest QUALITY 27 requires. The receipts themselves were produced in a clean shell (`GIT_*` unset), so no committed state was moved |

## Measurements

Frozen command and receipts (the same two the plan names):

    python3 -I .ufo/evidence/round-93/c1/measure-v93.py --repo . --rev <REV> --work <empty dir>
    → C1_SUMMARY rev=<REV> n=12 killed=5 survived=7 inconclusive=0 unstable=0 invalid=0
      trivial=0 witnessed=7/7 note=present mismatched=0 badrows=0 verdict_tables=1
      C1_R93_PASS=true, exit 0                     (.ufo/evidence/round-93/pre-freeze/controls/pos-real.out)

    python3 -I .ufo/evidence/round-93/c1/controls-v93.py --lane . --rev 855f0c1c \
      --base 4a7e259b --work <empty dir> --outdir <dir> --jobs 6
    → C1_CONTROLS states=35 matched=35 mismatches=0 missing=0, exit 0
      (.ufo/evidence/round-93/pre-freeze/controls/C1-summary.txt)

    python3 -I tools/conjunct-disposition.py --lane . --rev <REV>
    → DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0, exit 0
    python3 -I tools/conjunct-disposition.py --selftest
    → DISPOSITION_SELFTEST: 6/6 pass, exit 0          (.ufo/evidence/round-93/pre-freeze/c2-selftest.out)

Do-nothing controls: `nowork-base` (`C1_SETUP spec-absent-at-rev`, exit 2),
`c2-nowork-base.out` (`DISPOSITION_SETUP counter-absent-at-rev`, exit 2), and
`c2-cheat-all-unfalsifiable.out` (`rows=19 falsifiable=0 unfalsifiable=19 findings=0`, exit 0 —
the checksum of the target's counts is what rejects it).

## Wave

One v1 wave `r93-w1`, 12 seats, all twelve settled with deliverables: executor 3
(R93E1 `reproduced-12/12`, R93E2 `no-regression`, R93E3 `reproduced`), scribe 1 (R93SC1
`drafted`), scout 2 (R93S1 `agree`, R93S2 `premise-holds`), reviewer 2 (R93R1
`findings:5`, R93R2 `conforms-with-findings`), critic 1 (R93C1 `survives` on 13 counter
runs), mutation-tester 1 (R93M1 `killed:17/24`, 6 inconclusive), sentinel 1 (R93SN1
`findings:10`), connector 1 (R93CN1 `no-overlap`). Attack seats by the policy's role set
4/12 = 33 %; counting sentinel and connector 6/12 = 50 %. No seat died; no residual call.
The wave did not kill either claim; it killed three sentences of the *record* (A1, A2, A3)
and one of C2's (A4), each now narrowed in the plan's amendments.

## Routed to round 94

1. A1 — fence-aware `coverage` scan, path as its own cell.
2. A2/A6 — delimiter-row width returned and checked; remainder-row policy decided.
3. A3 — externally anchor the gate identity in the counter's self-pinned bytes; `die` on
   disagreement instead of printing a false conjunct.
4. A4 — `--min-falsifiable` and a reason test that names a state or a digest.
5. A6/M1 — a fixture-assembly assertion (the transformed note still parses to twelve rows).
6. A6/M9 — `O_NOFOLLOW` receipt writes and a run-scoped receipt directory.
7. A6/M10 — `sealed_env()` on every driver git call plus the QUALITY 27 canary.
8. A6/M8 — the eight rule-level states M1's sharp probes named.
